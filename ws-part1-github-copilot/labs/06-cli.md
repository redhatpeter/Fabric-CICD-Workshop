# GH6 - Add a filter with Copilot CLI

**Time:** 15 minutes, optional. **Starting point:** GH5 committed.
**Goal:** make one small change through the terminal agent.

1. In your demo root with the virtual environment active, start `copilot`.
   Sign in if needed. Confirm that this is the disposable demo folder.
2. Ask for context first:

   **Prompt:** Explain this project and its current tests. Do not edit anything.

3. Ask for a scoped change:

   **Prompt:** Add an optional --region argument to summarize.py. Filter loaded rows
   before summarizing. Keep existing behavior when it is omitted. Unknown
   regions should exit nonzero with a useful error, not a traceback.
   Add tests for East, an unknown region, and the unchanged default.
   Do not change validation or empty-input behavior yet. Run the tests.
   Show the diff and wait before committing.

4. Read proposed commands and approve only those needed for this task.

## Check

```text
python summarize.py data/sales.csv --region East
python summarize.py data/sales.csv
python summarize.py data/sales.csv --region Unknown
python -m pytest -q
git diff
```

East output:

```text
East: 150.00
Average per region: 150.00
```

The default still reports all three regions and an average of 158.33.
Unknown must fail with a useful error. Check the exit code immediately:
`$LASTEXITCODE` in PowerShell or `echo $?` in bash.
Commit after reviewing the tests and diff.

**If blocked:** skip this optional feature. GH7 and GH9 use no filter.
Next: [GH7 GitHub](./07-github.md).
