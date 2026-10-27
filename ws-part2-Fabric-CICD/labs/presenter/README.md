# Part 2 presenter guide

Keep this directory out of the attendee's repository and VS Code workspace.
Attendees copy only [starter](../starter/), just as in Part 1.

## Scope and pacing

Use the [seven numbered labs](../README.md) for a roughly 2 hour 45 minute
session after installation/admin prerequisites. Demonstrate rather than execute
the optional recovery if time is short. Leave reports, semantic models, conflicts,
variable libraries, deployment plans, service principals and automated releases
for a separate session.

The tax transformation is deliberately already implemented. Participants activate
it with the supplied helper, so the lesson is Git/PR/CI/deployment rather than
writing PySpark. The [solution](./solution/) is a reference, not a shortcut for
deploying new item identities.

## Local rehearsal

No Fabric login, Spark install or third-party Python package is required.

**macOS / WSL / Ubuntu, from Part 2 `labs`:**

```bash
python3 presenter/verify_materials.py
cd starter
python3 -m unittest discover -s tests -v
python3 checks/validate_items.py
```

**Windows PowerShell, from Part 2 `labs`:**

```powershell
py -3 presenter/verify_materials.py
Set-Location starter
py -3 -m unittest discover -s tests -v
py -3 checks/validate_items.py
```

Expect the material checks to pass, then **12 starter tests** to pass. Starter
validation without synced items must explicitly say **setup only**.
The verifier checks local links, notebook code/structure, exact seed/answer
relationship, expected CSV values, the real notebook guard with stubbed runtime
context, helper behavior and workflow content. The starter tests use temporary
**synthetic item folders**, not live or distributable Fabric identities.
Temporary fixtures are removed by the test runner.

These are not a Spark emulator or live-tenant certification. Neither the verifier
nor the helper creates, updates or deletes cloud resources.

## Reference answers and state checkpoints

| End of lab | Expected state |
| --- | --- |
| 00 | Names recorded; local starter tests pass; no cloud writes yet |
| 01 | Dev/Test run baseline; pipeline assigned; lab Production empty |
| 02 | Two real items in Git; main workflow green; developer branch workspace isolated |
| 03 | Feature changes two files; reviewed PR merged; Dev tax; Test baseline |
| 04 | Notebook-only deploy succeeded; existing Test item ID retained; Test tax |
| 05 | Approved Test -> Production deploy; both items present; Production tax |
| 06 optional recovery | New revert PR; Dev/Test baseline; Production tax unless separately recovered |

Expected baseline rows: Online 100.00, Store 200.00, Partner 50.00; total 350.00.
Tax rows: 110.00, 220.00, 55.00; total 385.00. Both releases have exactly 3 rows.

## Supplied templates

| Template | Destination / timing |
| --- | --- |
| [Workshop instructions](./templates/copilot-instructions.md) | Optional `.github/copilot-instructions.md`, before the hands-on exercises |
| [Validation workflow](../starter/workflow-templates/validate.yml) | `.github/workflows/validate.yml`, after the initial Fabric sync in lab 02 |

Do not install the workflow before real Fabric items are synced: its strict
check should fail on an empty `fabric/` directory. Do not remove the strict flag.
The workflow has read-only GitHub permissions, no Fabric secrets and no deployment
job. Never use `pull_request_target` to run attendee branch code.

If carrying Part 1 instructions forward, remove CSV-summary-specific rules and
retain approval/privacy boundaries. Adding the optional instructions is a separate
reviewed baseline change, not part of the two-file tax PR.

## Live rehearsal checklist: must complete before class

Use your own approved capacity and throwaway names. Nothing in these materials
has provisioned them for you.

- [ ] Check the actual tenant's notebook/lakehouse Git and deployment support.
- [ ] Confirm GitHub synchronization is enabled and token/connection flow works.
- [ ] Check capacity state and permissions on workspaces **and** pipeline.
- [ ] Confirm menu labels for import, Git connection, initial sync and pipeline.
- [ ] Import the seed into Dev and attach a schema-enabled local lakehouse.
- [ ] Run Dev baseline and verify exact persisted rows/totals.
- [ ] Deploy both items to Test; inspect automatic binding and run baseline there.
- [ ] Sync the real definitions to `/fabric` and run the strict validator.
- [ ] Inspect the actual exported file names and metadata. If the platform format
  differs from the supported checker format, update and test the checker before class.
- [ ] Install the workflow, verify Actions policy/runner access and check name.
- [ ] Create the feature branch workspace; verify local lakehouse binding and
  inspect any binding-only changes before committing them back.
- [ ] Run preview/apply locally. Confirm Python exports have only the selector diff.
- [ ] Open the PR; wait for validate; run the feature in the branch workspace.
- [ ] Squash-merge and update Dev; confirm tax locally and in Dev.
- [ ] Notebook-only deployment to Test; verify retained item ID and target data.
- [ ] Approved deployment to Production; inspect binding and exact data.
- [ ] Optional revert PR and Test recovery; tax column must disappear.
- [ ] Inventory and explicitly approve cleanup. Never pause a shared capacity.

Git synchronization can preserve/remap item references, and deployment normally
remaps the default lakehouse to its paired target. These materials still require
inspection and block a cross-workspace binding before writing. If a target-local
binding fix is needed, record it as an environment adjustment and inspect it
again after future deployments. Do not treat business-logic drift in a target as
an acceptable fix.

## Failure demonstrations

Use a fresh disposable copy, not an attendee's live branch:

1. Show `--require-items` failing before sync.
2. In a synthetic fixture, corrupt `.platform` JSON and show a nonzero failure.
3. Change the tax multiplier to 1.20 and show the contract rejects 420.00.
4. Show the release helper's default leaves bytes unchanged.
5. Show cross-workspace context rejected by the notebook guard in the verifier.

The automated tests cover these cases. No intentional failed Production deployment
is needed. For a live red-PR demonstration, create a separate branch after the
main walkthrough, get approval, corrupt only a disposable item file, inspect the
failed check, then correct it; do not merge the bad version.

## Recovery when services are unavailable

- **Copilot/MCP unavailable:** all core operations have portal/Git/`gh` steps.
- **Fabric inaccessible:** show a prepared recording/evidence; label this a
  demonstration, not participant completion.
- **Actions blocked:** run the exact strict command and tests locally, document
  that CI/merge protection is not demonstrated, and resolve policy before claiming CI.
- **Private-repo approval gates unavailable:** manual review is educational only.
- **Expired token:** renew through the approved GitHub/Fabric credential dialogs.
  Do not ask for it in chat or commit it.
- **WSL login hang:** bound auth diagnostics and check the documented GSA/DNS
  issue before retrying. Network changes belong to the user/IT.
- **Async timeout:** retain operation/job ID and inspect it; do not immediately
  submit the same mutation again.
- **Pairing/deployment failure:** keep the error and inspect dependencies. Do not
  unassign stages without warning that history and rules can be lost.

## Verification status

Local material-build validation passed: **12 starter regression tests** and
**8 presenter material checks** (the latter also rerun the starter tests).
The unsynced starter passes setup mode and correctly exits nonzero in strict
CI mode. These checks are repeatable with the commands above.

Live GitHub
Actions execution, Fabric tenant permissions, portal labels, Git synchronization,
automatic binding, stage deployment and actual Spark execution require the above
rehearsal. Do not present them as tested merely because local checks pass.

Useful official references:

- [Git integration setup](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-get-started)
- [Automate Git integration](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-automation)
- [Lakehouse Git and deployment behavior](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-git-deployment-pipelines)
- [Notebook lifecycle management](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-source-control-deployment)
- [Deploy content](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/deploy-content)
- [Notebook runtime context](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-runtime)
