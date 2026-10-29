# GH9 - Ship empty-input handling

**Time:** 20 minutes. **Starting point:** GH7 changes on `main`, clean working tree.
The optional GH6 filter is not required.
**Goal:** complete a small plan-to-PR workflow yourself.

First run `python -m pytest -q` and the normal sales report. Expect the validated
GH7 behavior and an average of 158.33 before starting. If GH7 was skipped, finish
its local validation fallback first; the capstone must preserve validation, not
replace it. If GitHub is unavailable, work from that reviewed local commit and
record the PR/merge steps as blocked instead of claiming full completion.

## Task

**Prompt:** A CSV with the correct header but no sales rows is valid. It should print
only "Average per region: 0.00" and exit successfully. The summary function
should return ({}, 0.0). Do not treat a zero-byte file with no header as valid.
Keep existing validation and normal report behavior. Add regression tests.

## Follow the loop

1. Inspect `git status` and the current tests.
2. Use Plan mode with the task above. Review the proposed files and tests.
3. Ask Agent to implement it on a new branch `fix/empty-input`.
   Do not commit until you have inspected the diff.
   Run `git switch -c fix/empty-input` yourself if the agent only proposes the
   command. If the branch already exists, inspect it or choose a fresh name and
   use that name consistently; do not delete/reset the existing branch.
4. Run:

   ```text
   python summarize.py data/empty.csv
   python summarize.py data/sales.csv
   python -m pytest -q
   git diff
   ```

5. Confirm the empty fixture has only the average line and exits 0.
   Normal data must still show the three totals and average 158.33.
   Inspect `data/empty.csv`: it contains the `region,amount` header and no rows.
   Keep it unchanged. Require both a function test for `({}, 0.0)` and a
   subprocess test for exact stdout, empty stderr and exit 0. Add a separate
   `tmp_path` test for a zero-byte CSV: it must still fail without a traceback.
   Rerun GH7's invalid-input tests. If GH6 was done, also retain the East and
   unknown-region tests; the empty-report requirement here uses **no filter**.
6. Stage the changes. Run `git diff --cached` yourself and supply the diff to
   `/review-changes` or the read-only reviewer.
7. Commit, push and open a PR:

   After inspecting the staged diff and review findings, commit it (for example
   `git commit -m "Handle header-only sales CSV"`), preserving your team's
   Copilot coauthor policy. Then run:

   ```text
   git push -u origin fix/empty-input
   gh pr create --base main --title "Handle header-only sales CSV" --body "Return an empty summary with a zero average; add regression tests."
   ```

8. Request Copilot review if available. Otherwise review manually.
   Wait for the **tests** check to pass; a review comment is not a test run.
   Approve a pending Actions run only after inspecting its code. If required
   approving reviews cannot come from the PR author, obtain an authorized
   reviewer; do not bypass the repository's merge rules.
9. Merge using your repository's allowed method. With a clean local tree,
   switch to `main`, pull with `--ff-only`, and rerun the tests.

   ```text
   git status --short
   git switch main
   git pull --ff-only
   python -m pytest -q
   python summarize.py data/empty.csv
   python summarize.py data/sales.csv
   ```

   Stop if the tree is dirty, a pull fails, or the branch diverged. The final
   success criterion is the merged local `main`, not only your feature branch.

**Done when:** the PR is merged and the local `main` passes all tests.
If GitHub is unavailable, a locally reviewed/tested branch is a partial completion;
finish the PR steps when access is restored.

## Handoff

Carry only the reviewed repository instructions, review prompt and reviewer agent
into Part 2. The prompt references the reviewer, so keep both files together.
Remove sales-specific rules. Part 2 has its own Azure/Fabric setup and data.

Keep or archive your demo repository for reference. Do not delete anything
automatically. Remove only workshop-only MCP connections if you added them.
