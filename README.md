# Gunmetal extensions

This repository is the store index for Gunmetal (`gunmetal.extensions` version `1`).

An extension is a reviewed record: an id, a title, a version, a plane (`server` or `client`), a slot, a status (`on` or `not-in-build`), a summary, detail lines, and the grants it would ask for.

It is not an app and it is not a plugin you run. There is no WASM, no script for the player, and no binary.

## The only way in

`main` is protected. A direct push does not land. A pull request is the only way to add or change a record, and the `package` check has to pass.

That check reads every file in [`records/`](records/) except [`TEMPLATE.json`](records/TEMPLATE.json), refuses code, and rebuilds [`catalog.json`](catalog.json). It does not run an extension.

When the pull request merges, those files are published as the `extensions` release. `catalog.json` is the store index. One JSON file per extension is a release asset, plus `SHA256SUMS`.

A record in that release is listed in the store. Publishing it does not install it on a server.

Status `on` means a Gunmetal server already does that job itself. Status `not-in-build` means the record is listed and waiting. Neither status is an install.

Copy [`records/TEMPLATE.md`](records/TEMPLATE.md) to add one.

Membership of this repository is how someone is added or removed as a reviewer.

Player: <https://github.com/PremierStudio/gunmetal>

Review home: <https://github.com/itz4blitz/gunmetal-extensions>

Records are licensed under the GNU AGPL v3, the same license as Gunmetal.
