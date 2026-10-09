# Gunmetal extensions

This repository holds official extension records for Gunmetal (`gunmetal.extensions` version `1`).

An extension is a reviewed record: an id, a title, a version, a plane (`server` or `client`), a slot, a status (`on` or `not-in-build`), a summary, detail lines, and the grants it would ask for.

It is not an app and it is not a downloaded plugin. There is no code to run. No WASM, no scripts, no binaries.

Status `on` means a Gunmetal server already does that job itself. Status `not-in-build` means the record is a target a later package could name. Neither status installs a package.

A merged pull request is a reviewed record. It does not install itself on any server.

Membership of this repository is how someone is added or removed as a reviewer.

The closed list is [`catalogue.json`](catalogue.json).

Player: <https://github.com/PremierStudio/gunmetal>

Records are licensed under the GNU AGPL v3, the same license as Gunmetal.
