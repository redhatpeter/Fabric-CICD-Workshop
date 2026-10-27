# Part 2 hands-on labs: release a tiny Fabric notebook

Practice CI/CD, not data engineering. The supplied notebook contains three
synthetic sales rows, a working transformation, a prebuilt tax feature, and
persisted-data checks. No external data source or package install is needed.

Start with [00 readiness](./00-readiness.md). Copy **only the contents of
[starter](./starter/)** into a new attendee repository outside these materials.
Open that repository in VS Code, not the materials or presenter folder.

## What you will ship

```text
local feature branch --> GitHub PR + CI --> main --> update Dev from Git
          |                                             |
          +--> update isolated developer workspace       +--> Test --> approve --> Production
```

Dev and the developer workspace use Git. Test and Production use deployment
pipelines, **not Git connections**. Everyone plays developer and release manager
for their own disposable resources. Production here is a **lab workspace**.

| Lab | Time | Done when | Reference |
| --- | --- | --- | --- |
| [00 Readiness](./00-readiness.md) | 20 min | Tools, credentials, names and starter checks are ready | UC0 |
| [01 Baseline](./01-baseline.md) | 30 min | Dev and Test both run baseline successfully | UC0, UC1 |
| [02 Git and branch](./02-git-and-branch.md) | 30 min | Git-native definitions, CI and an isolated branch workspace exist | UC2, UC3, UC6 |
| [03 Change and PR](./03-change-and-pr.md) | 30 min | Tax feature passes CI, runs in the branch workspace, merges and reaches Dev | UC4, UC5, UC6 |
| [04 Deploy to Test](./04-deploy-test.md) | 20 min | A notebook-only deployment passes Test checks | UC7 |
| [05 Promote to Production](./05-promote-production.md) | 15 min | Approved release runs in Production | UC10 |
| [06 Recovery and cleanup](./06-recovery-and-cleanup.md) | 20 min | Recovery is rehearsed or explained; cleanup decisions are explicit | UC11, UC14 |

Allow about **2 hours 45 minutes**, plus installations, sign-in, admin setup and
Spark startup delays. Skip the optional live recovery to save time. This is the
small required path through the [full Part 2 reference](../workshop-part2-Fabric-CICD.md).
Reports, semantic models, conflicts, variable libraries, preview deployment
plans, service principals and automated releases are follow-on topics.

## Expected results

| Release | Persisted columns | Rows | Sum(amount) | Sum(amount_with_tax) |
| --- | --- | --- | --- | --- |
| baseline | channel, amount | 3 | 350.00 | Column absent |
| tax | channel, amount, amount_with_tax | 3 | 350.00 | 385.00 |

Both use **schema-enabled** `lh_workshop`, table `dbo.sales_wk`. The notebook
targets `lh_workshop.dbo.sales_wk`. It refuses a default lakehouse in another
workspace. Check the workspace name before running: the guard cannot know
whether you intended Dev, Test or Production.

Deployments copy definitions, **not rows**. Running the notebook creates or
overwrites this one synthetic table in the target. Repeated runs do not append
duplicates. Never attach a real/shared lakehouse.

## Working rules

- Replace all `<placeholders>` before executing a command; do not type the brackets.
- Commands run from your attendee repository root. `python` means its virtual environment.
- Save before switching branches; use `git status` and inspect diffs before committing.
- Do not let Fabric and a local editor write to the same branch at the same time.
  Baseline is committed from Fabric; the feature is committed locally.
- Preview mutations and wait for approval. Never paste passwords or tokens into chat.
- The provided helpers modify **local files only**; they do not call Fabric,
  create resources, commit, push or deploy.
- No MCP server is required. Portal + Git + `gh` is the dependable path;
  Copilot can use installed Fabric skills/CLI to carry out the same approved steps.
- Chat approval is a teaching convention, **not an enforceable release gate**.
  A production setup needs controlled identities and platform-enforced approvals.

## If something fails

Stop at the first failed check. Record the workspace, branch, item and operation
ID, but no credentials. Check permissions, capacity, current branch and sync state.
Do not repeatedly submit jobs or deployments: inspect the existing operation
first. Do not reconnect or unassign stages just to clear an error.

The [presenter guide](./presenter/README.md) includes rehearsal, expected answers,
limitations and recovery guidance. Local verification does not prove tenant
permissions, UI labels, automatic binding or actual Spark execution.
