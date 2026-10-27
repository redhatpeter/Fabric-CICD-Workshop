# Fabric CI/CD attendee starter

Copy **this folder's contents only**, including `.gitignore`, into a new folder
outside the workshop materials. Open that folder in VS Code. Keep presenter
answers out of your workspace.

Follow the numbered labs supplied by the presenter. There are no cloud side
effects until you explicitly perform the portal/CLI steps.

## Inventory

| File/folder | Use |
| --- | --- |
| [notebooks/nb_workshop.ipynb](./notebooks/nb_workshop.ipynb) | Importable, working baseline notebook; embeds the sample rows |
| [data/sales.csv](./data/sales.csv) | Readable copy of the same synthetic rows; no upload required |
| [fabric](./fabric/) | Destination for Fabric-generated Git-native item folders |
| [release.json](./release.json) | Expected release of the synced notebook, baseline or tax |
| [prepare_release.py](./prepare_release.py) | Preview/apply the prebuilt local feature change |
| [checks/validate_items.py](./checks/validate_items.py) | Offline definitions and pure transformation checks |
| [tests/test_workshop.py](./tests/test_workshop.py) | Local regression/failure-path tests |
| [workflow-templates/validate.yml](./workflow-templates/validate.yml) | Inactive PR-check workflow; install in lab 02 |
| [workshop-config.example.json](./workshop-config.example.json) | Names to copy into ignored `workshop-config.local.json` |

The config is a human reference, not a deployment engine. No credentials belong here.
The supplied [requirements file](./requirements-dev.txt) documents that there are
no third-party dependencies. Use Python 3.10+ and a virtual environment.

## Commands from this directory

Before the first Fabric sync:

```text
python -m unittest discover -s tests -v
python checks/validate_items.py
```

After the first Fabric sync:

```text
python checks/validate_items.py --require-items
```

Expected: two supported items and `release=baseline`.
The strict command intentionally fails if the initial sync has not happened.

On `feature/sales-tax`, after that sync:

```text
python prepare_release.py
```

Inspect the diff. Only after approval:

```text
python prepare_release.py --apply
python checks/validate_items.py --require-items
python -m unittest discover -s tests -v
```

Review and stage only the two changed files. Nothing is committed, pushed or
deployed by these helpers. Applying twice fails explicitly; inspect your branch
rather than trying to reset it.

## Notebook behavior and safety

- Import into Dev once; later promote the **existing item** through Git/deployment.
- Attach schema-enabled `lh_workshop` from the current workspace as default.
- Read the workspace/binding before Run all. After binding changes restart the session.
- Run all overwrites only `lh_workshop.dbo.sales_wk`, including its schema.
  This destructive behavior is intentional for the disposable synthetic table.
- baseline: 3 rows, amount 350.00, no tax column.
- tax: 3 rows, amount 350.00, amount_with_tax 385.00.
- Embedded input means every stage can independently generate its data.
  Deployment itself never copies table data.
- The pure Python transformation supports both releases from the start.
  Lab 03 activates tax with a selector change so you can focus on CI/CD.

## What offline checks do not prove

The checker verifies expected item names/types, unique logical UUIDs, required
definition files, parseable Python/JSON, the active release marker, and the
pure sales calculation. It executes the notebook's **trusted workshop
`build_sales` function only**, not the Spark/write cells. Like running project
tests, this executes repository code; review changes before running locally.

It is **not** a general Fabric schema validator, sandbox, comprehensive secret
scanner, Spark emulator, binding verifier or permission test. PR CI has no Fabric
credentials and does not deploy. Verify each target in Fabric with the notebook.
Never weaken `--require-items` to make a PR green.
