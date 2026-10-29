# GH7 - Delegate and review input validation

**Time:** 30 minutes. **Starting point:** GH5 (or GH6) committed and pushed to `main`.
**Goal:** turn an issue into a reviewed pull request.
Cloud agent, code review and Spaces depend on your account and organization policy.

Before continuing, run `git status --short`, `git branch --show-current` and
`gh repo view --json nameWithOwner,visibility,url`. Confirm a clean demo `main`,
the intended GitHub owner, and private visibility. Push GH3-GH6 commits with
`git push` if needed. Do not use the workshop materials repository.

## 1. Prepare GitHub

Ask the local agent:

**Prompt:** Create .github/workflows/tests.yml to run python -m pytest -q on push and
pull_request using Python 3.12 and requirements-dev.txt. Create
.github/workflows/copilot-setup-steps.yml with workflow_dispatch and a single
job named copilot-setup-steps that checks out the repository, sets up Python
3.12 and installs requirements-dev.txt. Use minimal read-only contents
permissions. Show both files before committing.

The presenter has reference workflows. Review, commit and push them to `main`
before assigning the task. Check the Actions tab: the baseline test workflow
must pass. The setup workflow alone is not a PR test check.

Use a regular Agent chat, not the read-only reviewer. After inspecting the two
workflows, run the tests locally, commit both files, and `git push`. In GitHub's
**Actions** tab open the run for this commit and verify the `tests` job succeeded;
a workflow file merely existing does not prove it ran. If Actions is disabled
or an action is disallowed, ask the organizer rather than broadening permissions.
The setup workflow prepares the cloud agent's environment; its job ID must be
exactly `copilot-setup-steps`.

## 2. Create the issue

Create an issue in the portal, or ask `gh` to create it with this title and body:

**Title:** Validate sales CSV input with useful errors

**Issue body:**

Required columns are region and amount. Trim surrounding whitespace from
region names and reject blank regions. Reject nonnumeric, negative and
nonfinite amounts. Reject missing columns and malformed rows. Do not silently
skip bad rows. On invalid CSV input, print a helpful error to stderr and exit
nonzero without a traceback. Include the CSV line number for bad rows.

Use data/invalid-amount.csv and data/missing-column.csv. Add automated tests,
including blank regions and nonfinite amounts. Keep the normal sales report
and existing tests working. Do not implement header-only CSV handling yet;
that is a separate capstone. Do not add application dependencies.

Assign it to Copilot using the available portal controls.

For a CLI-created issue, run `gh issue create` from the demo root and enter the
title/body above in its prompts. Creating an issue does **not** automatically
assign it to Copilot. Confirm the assignment or delegate action in the portal;
if unavailable, use the fallback below.

When reviewing the generated tests, check all of these cases:

| Input | Expected behavior |
| --- | --- |
| Normal fixture | Same three totals and average 158.33 |
| ` East ` and `East`, with amounts 0 and 10 | One East total of 10; zero accepted |
| Blank/whitespace-only region | Error with CSV line number |
| Nonnumeric, negative, `nan`, `inf` or `1e999` amount | Error with CSV line number |
| Missing `amount` header or zero-byte input | Helpful missing-column/header error |
| Row with a missing/extra field, or unterminated quoted field | Error with CSV line number |

Use temporary test files (`tmp_path`) for additional cases; do not change the
supplied fixtures to make tests pass. Invalid input must produce no partial
success report on stdout. Header-only *success* remains for GH9.

## 3. Observe and review

1. Inspect the session log while the agent works.
2. Open its PR; read the diff and test results before merging.
   Cloud-agent PRs may be drafts and workflow runs may require your approval.
   Inspect the code before approving a run, and mark the PR ready when suitable.
3. Request Copilot code review if enabled. Read each suggestion before applying.
4. Add a focused follow-up comment, tagging Copilot if required by the UI:

   **Comment:** Please confirm there is a regression test for a negative amount.

5. Wait for the PR tests to pass. Approve and merge only after reviewing the result.
   A PR author cannot submit an approving review on their own PR. Review the
   changes yourself and merge only if repository rules permit it; obtain another
   authorized review when required. Do not bypass branch protection.
6. Locally, with no uncommitted changes, run `git switch main` and
   `git pull --ff-only`. Stop if Git reports a conflict or divergent history.

## Check locally

```text
python summarize.py data/sales.csv
python summarize.py data/invalid-amount.csv
python summarize.py data/missing-column.csv
python -m pytest -q
```

Normal output is unchanged. Both invalid fixtures exit nonzero with useful
messages on stderr and no traceback. Check `$LASTEXITCODE` (PowerShell) or
`echo $?` (bash) immediately after each invalid command.
Run invalid commands separately, not in an `&&` chain or a multi-command block
that stops on the first failure. Otherwise you may never exercise the second
fixture or see the correct exit code. Generated error wording can vary, but
the invalid amount in the supplied fixture must identify **Line 3**.

## Spaces: a short context demo

If enabled, create a Space containing the demo README, script and normal CSV.
Ask "What does average per region mean here, and what is the expected value?"
The answer should use the documented rule and approximately 158.33.

**If blocked:** ask the local agent to implement the same issue on
`fix/input-validation`, then open a PR with `gh`. Review it yourself if Copilot
review is unavailable. If GitHub is unavailable entirely, review the local diff
and tests, and observe the presenter's prepared PR later. Skip Spaces if unavailable.

For the local-agent fallback, branch from clean `main` with
`git switch -c fix/input-validation`, implement/test the issue above, review and
commit, then `git push -u origin fix/input-validation` and `gh pr create --base main`.
After merging, follow the same clean-tree switch/pull/test steps. If GitHub is
entirely unavailable, keep the reviewed validation commit locally; you may
rehearse GH9 on top of it but neither lab's remote PR requirement is complete.

**Done when:** the validation change is reviewed, tested and available locally on `main`.
Next: [GH8 guardrails](./08-guardrails.md).
