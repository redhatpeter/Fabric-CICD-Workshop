# Presenter answer key

The [completed notebook](./notebooks/nb_workshop.ipynb) differs from the attendee
seed only in `RELEASE = "tax"`. The
[release marker](./release.json) shows the matching repository state.
[Expected output](./expected-sales-tax.csv) is synthetic reference data, not a
file to upload to OneLake.

Do not copy this folder wholesale into an attendee repository. It intentionally
has no `.platform` files, logical IDs, workspace bindings or production credentials.
It is not a deployable snapshot of another person's Fabric items.

## Smallest useful intervention

1. If import is blocked, help import the **starter baseline** into Dev.
2. If the release helper is blocked, inspect the real synced notebook and apply
   only `RELEASE = "baseline"` -> `"tax"` there, plus `release.json`.
3. Keep the existing Fabric metadata, lakehouse binding and item identity.
4. Run the strict validator and tests from the attendee repository.
5. Continue through the PR and workspace update; never import the answer notebook
   directly into Test/Production to bypass the release exercise.

For recovery, the reviewed revert returns both active selectors to baseline.
The same notebook then writes the two-column, three-row baseline table.
