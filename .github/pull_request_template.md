# Store record

Merging this into `main` lists the record in the store. It does not install it, and it does not run it.

## What this changes

- Id:
- New record, or an edit of an existing id:
- What a person can do with it, in one sentence:

## Checklist

- [ ] The file is `records/<id>.json`, and the `id` field matches the filename.
- [ ] `python3 tools/pack.py` was run, and `catalog.json` is in the diff.
- [ ] The record is JSON data only. No WASM, script, binary, or submodule.
- [ ] Grants are the minimum, and each one is named. No wildcard.
- [ ] `status` is `on` only if a Gunmetal server already does this job itself. Otherwise `not-in-build`.
- [ ] The `package` check is green.

A direct push to `main` is not a way in. A green pull request merged to `main` is the way in.
