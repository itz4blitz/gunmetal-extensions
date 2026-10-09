# Extension record review

This repository holds reviewed records. It does not install them.

## Checklist

- [ ] What this changes is stated: a new record, or a change to an existing id.
- [ ] The extension id is named, and the id is stable. Renaming an id is a new record, not an edit.
- [ ] The record is JSON data only. No extension code, WASM, binary, or submodule. The package workflow may validate JSON. It must not run an extension.
- [ ] Grants asked for are the minimum, and each grant is named.
- [ ] Status is `on` only if the player already performs the job without downloading this repository. Otherwise `not-in-build`.
- [ ] A merge does not install the extension on a server.
- [ ] The interface id remains `gunmetal.extensions` version `1`.
