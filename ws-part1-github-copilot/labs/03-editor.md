# GH3 - Try the editor features

**Time:** 20 minutes. **Starting point:** GH2, two baseline tests passing.
**Goal:** implement one helper without changing report calculations yet.

## Try it

1. Open `summarize.py`. In `top_region`, replace the `raise NotImplementedError(...)`
   line with a comment:
   `# Return the highest-total region and amount; break ties alphabetically.`
   Trigger/accept an inline suggestion, then read it.
   A comment alone is not a function body: do not run the file until the helper
   has an implementation. If suggestions are unavailable, go straight to step 2.
2. If no suggestion appears, use inline chat:

   **Prompt:** Implement top_region(totals). Return a (region, amount) tuple, or None for
   empty totals. Break ties alphabetically. Change only this helper.

3. Select `top_region` and ask inline chat:

   **Prompt:** Add type hints and a short docstring without changing behavior.

4. Rename `load` to `load_rows` in the editor. Review suggested call-site edits,
   including the test imports. If suggestions do not appear, use Rename Symbol.
   Start Rename Symbol on the function name, review its preview, and save all
   changed files. Search the demo for `load(` and `import load` to catch stale
   calls/imports; do not rename unrelated methods or built-ins.
5. Attach `data/sales.csv` in Chat:

   **Prompt:** Calculate the totals by region. Explain how you checked them. Do not edit code.

6. Ask Copilot to add tests for `top_region`: normal totals, a tie, and no totals.
   Keep the two existing tests.

The expected CSV totals are East 150, West 250 and North 75. Do not wire
`top_region` into the printed report; this lab tests the helper independently.
For the tie test, supply West before East in the dictionary so a solution that
merely takes the first maximum does not accidentally pass.

## Check

```text
python -m pytest -q
python summarize.py data/sales.csv
git diff
```

- `top_region({"East": 150, "West": 250})` returns `("West", 250)`.
- Equal East/West totals choose East; an empty dictionary returns `None`.
- Tests pass; the report output is unchanged from GH2.
- The rename updated both the application and tests.

Expect at least **5 passing cases** if you add one case per helper scenario;
parameterized tests count as separate cases. Counts may differ if more tests
are added. A `NotImplementedError`, import error or changed average is not a pass.

Commit this exercise. A generated commit message is another smart action to try.

**If blocked:** ask for just the helper implementation; do not replace the whole script.
Next: [GH4 modes](./04-modes.md).
