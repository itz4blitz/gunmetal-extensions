# Extension record template

Copy `TEMPLATE.json` when adding a record. Replace every placeholder. The copy must stay valid JSON. JSON has no comments, so this file explains the fields.

`id` is the stable name reviews and other records use. It does not change. Renaming an id is a new record, not an edit of the old one.

`title` is the short name a person reads.

`version` is this record's own version, such as `1.0.0`. It is not the interface version.

`plane` is `server` or `client`. `server` means the job belongs on the library host. `client` means the job is data the app shows.

`slot` names the kind of job, such as `metadata-provider` or `theme-pack`.

`status` is `on` or `not-in-build`. Use `on` only when a Gunmetal server already does that job itself, without downloading this repository. Otherwise use `not-in-build`. Neither status installs a package.

`summary` is one sentence saying what the record is for.

`detail` is one or two short sentences. Do not claim that a package is downloaded or executed.

`grants` lists the permissions the record would ask for. Ask for the minimum. Name each grant.

The closed list in `catalogue.json` uses the interface id `gunmetal.extensions` version `1`. A merged pull request is a reviewed record. It does not install itself on any server.
