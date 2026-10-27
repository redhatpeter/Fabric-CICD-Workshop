# GH4 - Compare chat modes on one bug

**Time:** 20 minutes. **Starting point:** GH3 committed; the original average is unchanged.
**Goal:** see the difference between explanation, planning and implementation.

Read the average rule in your demo README. The total is 475 across three regions,
so the expected average is approximately **158.33**, not the current 118.75.

## Compare without fixing the bug too early

1. **Ask**, new chat:

   **Prompt:** Using summarize.py, data/sales.csv and the README, explain why the average
   is wrong. Do not edit files or run commands.

2. **Plan**, new chat:

   **Prompt:** Plan the smallest average fix and a regression test. Do not implement yet.

3. **Edit**, if your VS Code version offers it: select only the script and test file.

   **Prompt:** Fix the average per region and add a regression test. Leave empty-input
   handling and validation for later labs.

4. Inspect the diff and run the tests. To compare **Agent on the same baseline**,
   use VS Code's undo/checkpoint controls to undo only this Edit turn.
   Check `git diff`: no Edit changes should remain before continuing.
   If undo is unavailable or unclear, skip Edit and compare Ask, Plan and Agent;
   do not run a destructive Git reset.
5. **Agent**, new chat:

   **Prompt:** Fix the average per region and add a regression test. Run the tests.
   Do not implement input validation, a filter or empty-input handling yet.
   Show me the diff; do not commit.

Modes vary by VS Code version. Use the closest available mode; comparing
read-only reasoning with tool-driven editing is the learning objective.

## Check

```text
python summarize.py data/sales.csv
python -m pytest -q
git diff
```

The last output line is `Average per region: 158.33`. The new test checks the
unrounded value with `pytest.approx(475 / 3)`, not a fragile float equality.
All prior tests still pass. Commit the fix.

**If blocked:** change only the denominator and add the one regression test.
Do not resolve empty input now; it is the capstone.
Next: [GH5 customization](./05-customization.md).
