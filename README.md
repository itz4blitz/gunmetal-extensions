# Gunmetal extensions

This repository holds official extension records for Gunmetal (`gunmetal.extensions` version `1`).

An extension is a reviewed record: an id, a title, a version, a plane (`server` or `client`), a slot, a status (`on` or `not-in-build`), a summary, detail lines, and the grants it would ask for.

It is not an app and it is not a plugin you run. There is no WASM, no script for the player, and no binary.

## Approval

`main` is protected. A change lands only through a pull request, and the `package` check has to pass. That check validates [`catalog.json`](catalog.json) and packs one JSON file per extension. It does not run an extension.

On `main`, those files are also published as release assets under the `extensions` tag. One file, one extension, plus `SHA256SUMS`. A release is the package a later install would take. Publishing it does not install it on a server.

Status `on` means a Gunmetal server already does that job itself. Status `not-in-build` means the record is waiting. Neither status is an install.

The player does not download this repository. Loading or running extension code waits until the sandbox requirements pass.

Membership of this repository is how someone is added or removed as a reviewer.

Player: <https://github.com/PremierStudio/gunmetal>

Records are licensed under the GNU AGPL v3, the same license as Gunmetal.
