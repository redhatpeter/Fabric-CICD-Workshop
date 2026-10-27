# GH7 - Delegate and review input validation

**Time:** 30 minutes. **Starting point:** GH5 (or GH6) committed and pushed to `main`.
**Goal:** turn an issue into a reviewed pull request.
Cloud agent, code review and Spaces depend on your account and organization policy.

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

## 3. Observe and review

1. Inspect the session log while the agent works.
2. Open its PR; read the diff and test results before merging.
3. Request Copilot code review if enabled. Read each suggestion before applying.
4. Add a focused follow-up comment, tagging Copilot if required by the UI:

   **Comment:** Please confirm there is a regression test for a negative amount.

5. Wait for the PR tests to pass. Approve and merge only after reviewing the result.
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

## Spaces: a short context demo

If enabled, create a Space containing the demo README, script and normal CSV.
Ask "What does average per region mean here, and what is the expected value?"
The answer should use the documented rule and approximately 158.33.

**If blocked:** ask the local agent to implement the same issue on
`fix/input-validation`, then open a PR with `gh`. Review it yourself if Copilot
review is unavailable. If GitHub is unavailable entirely, review the local diff
and tests, and observe the presenter's prepared PR later. Skip Spaces if unavailable.

**Done when:** the validation change is reviewed, tested and available locally on `main`.
Next: [GH8 guardrails](./08-guardrails.md).
