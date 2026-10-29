use cosmic::iced::{
    Subscription,
    futures::{SinkExt, StreamExt, channel::mpsc},
};
use logind_zbus::{
    manager::{InhibitType, ManagerProxy},
    session::SessionProxy,
};
use std::{any::TypeId, error::Error, os::fd::OwnedFd, sync::Arc, time::Duration};
use zbus::Connection;

use crate::{common, locker::Message};

pub async fn power_off() -> zbus::Result<()> {
    let connection = Connection::system().await?;
    let manager = ManagerProxy::new(&connection).await?;
    manager.power_off(false).await
}

pub async fn reboot() -> zbus::Result<()> {
    let connection = Connection::system().await?;
    let manager = ManagerProxy::new(&connection).await?;
    manager.reboot(false).await
}

pub async fn suspend() -> zbus::Result<()> {
    let connection = Connection::system().await?;
    let manager = ManagerProxy::new(&connection).await?;
    manager.suspend(false).await
}

/// Tells logind whether the session is locked. Its `LockedHint` is what the
/// screensaver interface and `loginctl` report.
pub async fn set_locked_hint(locked: bool) -> zbus::Result<()> {
    let connection = Connection::system().await?;
    set_locked_hint_of(&connection, std::os::unix::process::parent_id(), locked).await
}

async fn set_locked_hint_of(connection: &Connection, pid: u32, locked: bool) -> zbus::Result<()> {
    let manager = ManagerProxy::new(connection).await?;
    let session_path = manager.get_session_by_PID(pid).await?;
    let session = SessionProxy::builder(connection)
        .path(&session_path)?
        .build()
        .await?;
    session.set_locked_hint(locked).await
}

async fn inhibit(manager: &ManagerProxy<'_>) -> zbus::Result<OwnedFd> {
    let what = InhibitType::Sleep;
    let who = "COSMIC Greeter";
    let why = "COSMIC Greeter needs to display a lock screen";
    let mode = "delay";
    //TODO: update logind-zbus to fix inhibit signature
    let fd: zbus::zvariant::OwnedFd = manager
        .inner()
        .call("Inhibit", &(what, who, why, mode))
        .await?;
    // Have to convert to std type to avoid leaking zbus dependency
    Ok(fd.into())
}

pub fn subscription() -> Subscription<Message> {
    struct LogindSubscription;

    Subscription::run_with_id(
        TypeId::of::<LogindSubscription>(),
        cosmic::iced_futures::stream::channel(16, |mut msg_tx| async move {
            match handler(&mut msg_tx).await {
                Ok(()) => {}
                Err(err) => {
                    tracing::warn!("logind error: {}", err);
                    //TODO: send error
                }
            }

            std::process::exit(1);
        }),
    )
}

//TODO: use never type?
pub async fn handler(msg_tx: &mut mpsc::Sender<Message>) -> Result<(), Box<dyn Error>> {
    let connection = Connection::system().await?;
    let manager = ManagerProxy::new(&connection).await?;
    let session_path = manager
        .get_session_by_PID(std::os::unix::process::parent_id())
        .await?;
    let session = SessionProxy::builder(&connection)
        .path(&session_path)?
        .build()
        .await?;

    let mut inhibit_opt = Some(inhibit(&manager).await?);
    let mut prepare_for_sleep = manager.receive_prepare_for_sleep().await?;
    let mut lock = session.receive_lock().await?;
    let mut unlock = session.receive_unlock().await?;

    let mut interval = tokio::time::interval(Duration::from_secs(1));

    loop {
        // Waits until a signal has been received
        tokio::select!(
            signal_opt = prepare_for_sleep.next() => {
                match signal_opt {
                    Some(signal) => match signal.args() {
                        Ok(args) => {
                            if args.start {
                                tracing::info!("logind prepare for sleep");
                                if let Some(inhibit) = inhibit_opt.take() {
                                    msg_tx.send(Message::Inhibit(Arc::new(inhibit))).await?;
                                }
                                msg_tx.send(Message::Lock).await?;
                            } else {
                                tracing::info!("logind resume");
                                if inhibit_opt.is_none() {
                                    inhibit_opt = Some(inhibit(&manager).await?);
                                }
                                // Immediately update time when resuming from sleep.
                                msg_tx.send(Message::Common(common::Message::Tick)).await?;
                            }
                        },
                        Err(err) => {
                            tracing::warn!("logind prepare to sleep invalid data: {}", err);
                        }
                    },
                    None => {
                        tracing::warn!("logind prepare to sleep missing data");
                    }
                }
            },
            _ = lock.next() =>  {
            tracing::info!("logind lock");
            msg_tx.send(Message::Lock).await?;
        }, _ = unlock.next() => {
            tracing::info!("logind unlock");
            msg_tx.send(Message::Unlock).await?;
        });

        interval.tick().await;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Mutex;
    use zbus::zvariant::OwnedObjectPath;

    const SESSION_PATH: &str = "/org/freedesktop/login1/session/_31";

    struct FakeManager;

    #[zbus::interface(name = "org.freedesktop.login1.Manager")]
    impl FakeManager {
        #[zbus(name = "GetSessionByPID")]
        fn get_session_by_pid(&self, pid: u32) -> zbus::fdo::Result<OwnedObjectPath> {
            match pid {
                4242 => Ok(OwnedObjectPath::try_from(SESSION_PATH).unwrap()),
                _ => Err(zbus::fdo::Error::Failed(format!("no session for {pid}"))),
            }
        }
    }

    struct FakeSession(Arc<Mutex<Vec<bool>>>);

    #[zbus::interface(name = "org.freedesktop.login1.Session")]
    impl FakeSession {
        fn set_locked_hint(&self, locked: bool) {
            self.0.lock().unwrap().push(locked);
        }
    }

    #[tokio::test]
    async fn the_locked_hint_is_set_on_the_lockers_session() {
        let hints = Arc::new(Mutex::new(Vec::new()));
        let (logind, locker) = tokio::net::UnixStream::pair().unwrap();
        let logind = zbus::connection::Builder::unix_stream(logind)
            .server(zbus::Guid::generate())
            .unwrap()
            .p2p()
            .serve_at("/org/freedesktop/login1", FakeManager)
            .unwrap()
            .serve_at(SESSION_PATH, FakeSession(hints.clone()))
            .unwrap()
            .build();
        let locker = zbus::connection::Builder::unix_stream(locker).p2p().build();
        let (_logind, locker) = tokio::join!(logind, locker);
        let locker = locker.unwrap();

        set_locked_hint_of(&locker, 4242, true).await.unwrap();
        set_locked_hint_of(&locker, 4242, false).await.unwrap();
        assert!(set_locked_hint_of(&locker, 1, true).await.is_err());

        assert_eq!(*hints.lock().unwrap(), [true, false]);
    }
}
