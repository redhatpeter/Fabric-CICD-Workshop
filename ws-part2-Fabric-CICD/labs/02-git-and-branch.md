# 02 - Version the baseline and isolate a feature branch

**Time:** 30 minutes; create GitHub credentials before class where possible.
**Starting point:** [01 baseline](./01-baseline.md) complete; Test has baseline.
**Goal:** version Fabric-generated definitions and establish the PR check.

## 1. Publish the attendee starter

From your attendee repository root, review `.gitignore` and confirm no tokens,
personal files, `.venv` or presenter solutions will be staged.

```text
git init -b main
git status
git add .
git diff --cached
```

After review and approval:

```text
git commit -m "Add Fabric CI/CD starter"
gh repo create <owner>/<repository> --private --source=. --remote=origin --push
```

Replace `<owner>/<repository>` with your config value. Do not recreate an
existing repo or force-push. If Git needs an identity, configure your own approved
name/email locally. Keep your team's Co-authored-by policy for assisted commits.

The `fabric/README.md` ensures `/fabric` already exists on `main`.
The notebook under `notebooks/` is an **import seed**, not a Git-native Fabric item.

## 2. Register GitHub credentials in Fabric

1. In GitHub, open **Settings > Developer settings > Personal access tokens >
   Fine-grained tokens**.
2. Create a short-lived token scoped to **only this repository**.
3. Grant **Contents: Read and write**. Metadata read access is included.
4. If the owner organization requires token approval, get that approval first.
5. In Fabric, open the workspace **Source control > Accounts** experience and
   add the GitHub account/connection using the token.
6. Paste the token **only in that credential dialog**. Never in chat, config,
   notebook, shell history or the repository.

Menu labels can vary by tenant. Use the
[Git integration setup guide](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-get-started)
if the account flow differs. `gh auth login` does not automatically configure
Fabric's Git credentials. GitHub API integration requires a configured connection,
not automatic Azure DevOps credentials.

## 3. Connect Dev and commit the real item definitions

1. In **Dev**, open **Workspace settings > Git integration**.
2. Select your GitHub repository, branch **main**, directory **/fabric**.
3. Review the initialization direction. Dev holds the baseline items; `/fabric`
   currently has only a README. Choose the option that commits **workspace
   content to Git**, not an overwrite of the working Dev items.
4. Complete the connection/initialization and commit `lh_workshop` and
   `nb_workshop`, message `Add Fabric baseline items`.
5. Wait for synchronization to finish. Source control should show no pending changes.
6. On GitHub, inspect `/fabric`. Expect two item folders with Fabric-generated
   `.platform` files, a lakehouse definition and notebook source.

Connect, initialize and sync are separate operations when using APIs.
For CLI execution, ask Copilot to read current status/head hashes, serialize
operations, poll any HTTP 202 operation and verify synchronized heads and no
pending changes. Never reuse stale head hashes or silently resolve a conflict.

Pull the Fabric-generated commit locally:

```text
git status
git pull --ff-only
python checks/validate_items.py --require-items
python -m unittest discover -s tests -v
```

Expected strict result:

```text
PASS: 2 Fabric items; release=baseline; baseline=350.00; tax=385.00
```

The tax number means the **prebuilt pure transformation** was tested, not that
the feature has been deployed. `release=baseline` is the active version.

The validator supports `notebook-content.py` and `notebook-content.ipynb`.
If Fabric emits a different definition format, stop and ask the presenter to
update the checker to that documented format; do not bypass CI.

## 4. Install the supplied CI workflow

Copy the supplied inactive template into the active GitHub workflow directory:

**PowerShell**

```powershell
New-Item -ItemType Directory -Force .github/workflows
Copy-Item workflow-templates/validate.yml .github/workflows/validate.yml
```

**macOS / WSL / Ubuntu**

```bash
mkdir -p .github/workflows
cp workflow-templates/validate.yml .github/workflows/validate.yml
```

Review the file. It runs on PRs and pushes to `main`, uses read-only repository
permissions, and requires **no Fabric credentials or secrets**.
It validates real synced items and runs the same local tests.

```text
git add .github/workflows/validate.yml
git diff --cached
```

After approval:

```text
git commit -m "Enable Fabric item validation"
git push
gh run list --workflow validate.yml --limit 3
```

Open the latest run URL in GitHub and wait for job **validate** to pass.
If organization policy blocks Actions or the pinned action versions, ask the
admin/presenter for the approved equivalent; do not weaken organization controls.
If branch protection is available, make `validate` required on `main`.
Otherwise record that merge protection is manual for this lab.

## 5. Create one feature branch

With a clean local working tree:

```text
git switch -c feature/sales-tax
git push -u origin feature/sales-tax
```

Creating a branch pushes no feature change yet.
Dev stays attached to `main`.

## 6. Create the isolated developer workspace

1. Create your empty `wk-dev-a-<suffix>` on the same approved capacity.
2. Connect it to the **same repo and `/fabric` directory**, but branch
   **feature/sales-tax**.
3. Initialize using **Git/remote content as the source**, then update from Git.
   Do not commit the empty workspace over the branch.
4. Wait for synchronization; inspect its lakehouse and notebook.
5. Confirm the notebook's default lakehouse is **this developer workspace's**
   `lh_workshop`. Correct and save it if necessary, then restart its session.
6. If correcting the binding creates a pending source-control change, inspect
   and commit **only that intended binding change** to the feature branch from
   Fabric. Wait for sync, then `git pull --ff-only` locally before further edits.
7. Run the baseline notebook here after approving the synthetic-table overwrite.
   Expect baseline PASS and this workspace's name.
8. Re-run local strict validation if Fabric added a binding commit.

Do not switch Dev's connected branch. One connected workspace has one branch;
the extra workspace provides isolation. Workspace relations/preview branch-out
features are not needed.

**Done when:** Dev -> `main`, developer workspace -> `feature/sales-tax`,
Test/Production -> no Git; initial CI is green; all working notebooks are baseline.

**If blocked:** check tenant GitHub enablement, token scope/expiry, workspace
Admin and the exact existing directory. Do not disconnect a populated workspace
without inspecting and preserving its unsynced work.

Next: [03 change and PR](./03-change-and-pr.md).
