# GH6 - Add a filter with Copilot CLI

**Time:** 15 minutes, optional. **Starting point:** GH5 committed.
**Goal:** make one small change through the terminal agent.

Run `copilot --version` first. Use the current standalone **Copilot CLI**, not
the retired `gh copilot` suggest/explain flow. If it is missing, use the
[main guide's tool setup](../workshop-part1-github-copilot.md#21-tools-to-install);
skip this optional lab if installation or organization policy blocks it.
Check the shell is in the demo folder and `python -c "import sys; print(sys.executable)"`
points to its virtual environment. Trust only that folder when prompted.

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

   Add: **Use this project's virtual environment. Treat region names as
   case-sensitive; do not add a top-region line to the report. Ask before
   overwriting files and do not commit, push or create a PR.**

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

The Unknown command is an **expected failure**, not a reason to stop the lab.
Its stdout should be empty, stderr should explain the unknown region, and there
must be no traceback. Check the exit code before running pytest (a later command
replaces it). Ask for a subprocess-based test so argument parsing and the exit
code are tested, not just the filtering expression. Exit the CLI session with
its documented exit control before running your own shell checks.

**If blocked:** skip this optional feature. GH7 and GH9 use no filter.
Next: [GH7 GitHub](./07-github.md).
