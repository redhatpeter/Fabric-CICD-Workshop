# Copilot workshop demo

A small Python sales report using synthetic data. Requires Python 3.10 or later.
This is an exercise starter, not production accounting software. Some behavior
is deliberately unfinished; follow the workshop labs rather than fixing everything at once.

## Run

Use the workshop setup instructions to create a virtual environment and install
the development dependency, then:

```text
python summarize.py data/sales.csv
python -m pytest -q
```

The two supplied tests check loading and regional totals. Passing them does not
prove the average or edge cases are correct. Add tests as you work.

## Business rules

- CSV input has required columns `region` and `amount`.
- Region names are nonempty, case-sensitive strings; surrounding whitespace is trimmed.
- Amounts are finite, nonnegative numbers. Zero is allowed.
- Sum amounts by region. The average is the mean of the **regional totals**,
  not the mean of individual sales.
- The top region is the one with the highest total. Break ties alphabetically.
  For no regions, the top-region helper returns `None`.
- A header-only CSV is valid: no totals and an average of `0.00`.
- Missing columns, invalid amounts, blank regions and missing files must result
  in a useful error on stderr and a nonzero exit code. Do not silently skip bad rows.
- The optional `--region` filter selects one region before calculating the report.
  An unknown region must produce a useful error, not an empty success report.

Not all rules are implemented yet. GH3 adds the helper, GH4 checks the average,
GH6 adds the optional filter, GH7 validates input, and GH9 handles empty data.
Use simple floats for this demonstration; a financial system needs an explicit
decimal/rounding policy.

## Data

| File | Scenario |
| --- | --- |
| `data/sales.csv` | Four sales across East, West and North |
| `data/empty.csv` | Header only |
| `data/invalid-amount.csv` | A nonnumeric amount |
| `data/missing-column.csv` | No `amount` column |

No network access is needed to run the application.
