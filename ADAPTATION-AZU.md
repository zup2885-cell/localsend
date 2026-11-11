# 阿祖快传 / Azu Quick Transfer

Based on [LocalSend](https://github.com/localsend/localsend), by Tien Do Nam and contributors. Apache License 2.0 is retained. This is an independent Mac adaptation, not an official LocalSend release.

Changes: independent bundle identifier, Azu name and icon, Simplified Chinese default on first launch, attribution and adaptation source links. Network protocol, confirmation prompts and encryption are retained. No owner files, device history or credentials are packaged.

Build with the pinned Flutter 3.47.9 and Rust 1.97.1: `cd app`, `flutter pub get`, `dart run build_runner build --delete-conflicting-outputs`, `dart run slang`, `flutter build macos --release`. Mac packages are ad hoc signed, without Apple notarization.

The Mac application and share extension use an independent bundle identifier and shared group. Simplified Chinese is saved only on a fresh profile; the system-language option remains available. Release builds use ad hoc signing without the upstream development team.

Packaging: after building, run `python3 azu-mac/package.py`. The development package uses an ad hoc signature without hardened runtime; sandbox entitlements are preserved. Host security settings are not changed. An Apple-notarized distribution needs the maintainer's Developer ID. Flutter and Dart notices remain in the Flutter assets; Rust dependency notices are included alongside them.
