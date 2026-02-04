## [1.0.1](https://github.com/playtron-os/cosmic-greeter/compare/v1.0.0...v1.0.1) (2026-02-04)


### Bug Fixes

* missing release CI config ([2385d6a](https://github.com/playtron-os/cosmic-greeter/commit/2385d6a0da4cafa035a4e96f299eafcb12972eca))

# 1.0.0 (2026-02-04)


### Bug Fixes

* --no-default-features ([8844f2c](https://github.com/playtron-os/cosmic-greeter/commit/8844f2ce55f869747533586cf42ab9759806ae4b))
* ACK so greetd doesn't wait forever on systems with fingerprint scanner ([f3e9de2](https://github.com/playtron-os/cosmic-greeter/commit/f3e9de242547f6e099fb6e48cf884c53b5ebc90d))
* add missing pam_namespace pam module ([b0589a1](https://github.com/playtron-os/cosmic-greeter/commit/b0589a10d49bb8ab3b976214c82ef058428f8fba))
* add missing rpm spec requires ([ae45f54](https://github.com/playtron-os/cosmic-greeter/commit/ae45f542a2e5147adfcd79d936ce7b7bd4b00cf8))
* add optional gnome keyring pam module ([b625033](https://github.com/playtron-os/cosmic-greeter/commit/b6250334a16e59683760767289c4a47e8a559dd0))
* apply military time preference to time ([9e22418](https://github.com/playtron-os/cosmic-greeter/commit/9e22418e53055cbec2e75a5b2e048b6e9dff3a61))
* avoid Fill for the left element ([525c635](https://github.com/playtron-os/cosmic-greeter/commit/525c635124d8d6dbc6b1869223665e39e5b04a43))
* binary search won't work for name comparison ([6813da2](https://github.com/playtron-os/cosmic-greeter/commit/6813da21b5eac0046c11b503aad231dd4973dd95))
* clear dropdown after enter user is selected ([ab2ae6d](https://github.com/playtron-os/cosmic-greeter/commit/ab2ae6d31eda53c61aa50e1e7f3cfa1b60ad08da))
* Correctly detect all keyboard layouts ([ae3586f](https://github.com/playtron-os/cosmic-greeter/commit/ae3586fa149642aeae2fabec24214440aacf7fae)), closes [#1160](https://github.com/playtron-os/cosmic-greeter/issues/1160) [pop-os/cosmic-applets#725](https://github.com/pop-os/cosmic-applets/issues/725) [lilyinstarlight/nixos-cosmic#484](https://github.com/lilyinstarlight/nixos-cosmic/issues/484) [lilyinstarlight/nixos-cosmic#74](https://github.com/lilyinstarlight/nixos-cosmic/issues/74)
* **daemon:** require daemon in greeter, give daemon type dbus ([aa18965](https://github.com/playtron-os/cosmic-greeter/commit/aa18965a0310305818a10ba94c98f7352a064823))
* dbus_error usage with zbus 4 ([4613fbb](https://github.com/playtron-os/cosmic-greeter/commit/4613fbb1849af68e8967ad95ce1d58158a7fb4c6))
* enable cosmic-greeter-daemon when cosmic-greeter is enabled ([9933926](https://github.com/playtron-os/cosmic-greeter/commit/9933926d443386089a39683818109a9df50564a5))
* ensure greetd is configured before cosmic-greeter ([e2e5e4e](https://github.com/playtron-os/cosmic-greeter/commit/e2e5e4ea188234c4918b714b63a23ba4e6f925c1))
* **example:** `env::set_var` is now marked as unsafe. ([54c8527](https://github.com/playtron-os/cosmic-greeter/commit/54c8527ced812d653e6c49026a6924139cf8f09e))
* exit after logind subscription error ([2294d10](https://github.com/playtron-os/cosmic-greeter/commit/2294d10a514cca365d13ddb0e86fd6d8333eb938))
* improve error handling to prevent softlock ([5dc1db2](https://github.com/playtron-os/cosmic-greeter/commit/5dc1db27edbdcffcf7a034a128bb58a15b306f36))
* in CI upload rpms ([7f44d40](https://github.com/playtron-os/cosmic-greeter/commit/7f44d4051d785be4f43a8800221a27442b0f04da))
* patch cosmic-protocols ([992480f](https://github.com/playtron-os/cosmic-greeter/commit/992480fc9f553d0e0c67c780bb124d4d675db3fa))
* reposition subsurface after layer surface size update ([16185fe](https://github.com/playtron-os/cosmic-greeter/commit/16185fe21e0fb9d5ce859eac05babae003f1d3a8))
* update cosmic-randr-shell and other dependencies ([762b92e](https://github.com/playtron-os/cosmic-greeter/commit/762b92e5d1537848da69d6270858e28d0b09c7bb))
* update nix to fix loongarch64 build ([f826b8c](https://github.com/playtron-os/cosmic-greeter/commit/f826b8cce887b0c5cb4e2fcc680cb3c08c519fa9))
* use sed in CI version replacement and add missing permissions to release CI ([e4c47ed](https://github.com/playtron-os/cosmic-greeter/commit/e4c47ed700a728d6c251a511d6da7b116ab93c03))
* XDG_SESSION_ID may contain non-numerical characters ([b93acff](https://github.com/playtron-os/cosmic-greeter/commit/b93acffd873309445a67ec05b6a1b9b2794799cf))


### Features

* accessibility menu ([09e0950](https://github.com/playtron-os/cosmic-greeter/commit/09e0950ffead68e6dc557d39b8eeae01b3d70593))
* accessibility menu ([9c1306d](https://github.com/playtron-os/cosmic-greeter/commit/9c1306d8c7e0da6cbcd99d6350986cbf65a348c2))
* add fedora pam config and update to 1.0.4 ([169353d](https://github.com/playtron-os/cosmic-greeter/commit/169353d666f8008052739c7bbfcf6bddfd807ddb))
* add help and version command line arguments ([5b383f6](https://github.com/playtron-os/cosmic-greeter/commit/5b383f669b8824cf38996d3f4cec903c86bf8bac))
* introduce cosmic-greeter-start for state cleanup ([db59a72](https://github.com/playtron-os/cosmic-greeter/commit/db59a72eb9c8bef09a8f4163948c63742a7514f4))
* last user ([bbaa193](https://github.com/playtron-os/cosmic-greeter/commit/bbaa1935f4134d1c6c0fbec85746713119656e13))
* load and apply output configs ([f3f7d5c](https://github.com/playtron-os/cosmic-greeter/commit/f3f7d5cfb61e68d5cc65897e1446a2e3d2d4b700))
* update to 1.0.5 ([a656a2d](https://github.com/playtron-os/cosmic-greeter/commit/a656a2d81a5af1ace652634a697aa3e2cde75d5e))


### Performance Improvements

* cache image handles ([9ba6a04](https://github.com/playtron-os/cosmic-greeter/commit/9ba6a0481c3ec45b579252bec0fc096acf46505d))
