# Add a store record

Copy this when you want a new extension listed. A pull request into `main` is the only way in. The merge lists the record in the store. It does not install it, and it does not run anything.

## 1. Copy the template

```bash
cp records/TEMPLATE.json records/your-id.json
```

`your-id` is the stable name. Lower case, digits, and hyphens. The filename and the `id` field must be the same. `records/example-lyrics.json` means `"id": "example-lyrics"`. Renaming an id later is a new record, not an edit.

`TEMPLATE.json` is not listed. Leave it here.

## 2. Fill the fields

`title` is the short name a person reads. 80 characters at most.

`version` is this record's version, `1.0.0`. Three numbers, no leading zeros, no pre-release text.

`plane` is `server` or `client`. Server means the job belongs on the library host. Client means the app draws data. It is never code the app runs.

`slot` names the kind of job, such as `lyrics-provider` or `theme-pack`. Lower case and hyphens.

`status` is `on` or `not-in-build`. Use `on` only when a Gunmetal server already does that job itself, without downloading this repository. Otherwise `not-in-build`. Neither status installs a package.

`summary` is one sentence, 200 characters at most, saying what the record is for.

`detail` is one to eight sentences. Each is 240 characters at most. Say what it would do. Do not claim a file is downloaded or executed.

`grants` is one to eight permissions, each `area:action`, such as `lyrics:read`. Ask for the minimum. No wildcard.

Do not add a key the template does not have. The check refuses unknown keys.

## 3. Rebuild the index

```bash
python3 tools/pack.py
```

That rewrites `catalog.json` from every file in `records/` except this template, and writes one package file per id under `dist/`. Commit `records/your-id.json` and `catalog.json`.

## 4. Open a pull request

`main` does not take a direct push. The `package` check has to pass. When the pull request merges, the release tagged `extensions` is the store index. The player lists those records. It does not run them.
