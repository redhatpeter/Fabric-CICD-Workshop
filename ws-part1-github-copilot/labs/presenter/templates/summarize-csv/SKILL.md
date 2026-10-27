---
name: summarize-csv
description: "Use when running the sales CSV report or explaining regional totals and average per region."
---

1. Read the demo README for business rules and current interpreter instructions.
2. From the demo repository root, run `python summarize.py data/sales.csv`
   using the project virtual environment, if command execution is permitted.
3. Explain that totals sum sales by region, and the average is the sum of those
   regional totals divided by the number of regions.
4. For the supplied normal fixture, expect East 150, West 250, North 75 and an
   average of approximately 158.33 after GH4.
5. Run `python -m pytest -q` if requested and report the actual result.
6. If output differs, explain the discrepancy; do not silently change code or
   implement a later exercise. Never inspect credentials.
