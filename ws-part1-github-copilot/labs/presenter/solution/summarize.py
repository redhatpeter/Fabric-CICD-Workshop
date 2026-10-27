import argparse
import csv
import math


def load_rows(path: str) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source, strict=True)
        rows = []
        try:
            if reader.fieldnames is None or not {"region", "amount"} <= set(reader.fieldnames):
                raise ValueError("CSV must have region and amount columns.")
            for row in reader:
                line = reader.line_num
                if None in row or any(value is None for value in row.values()):
                    raise ValueError(f"Line {line}: malformed CSV row.")
                region = row["region"].strip()
                if not region:
                    raise ValueError(f"Line {line}: region must not be blank.")
                try:
                    amount = float(row["amount"])
                except ValueError as error:
                    raise ValueError(f"Line {line}: amount must be a number.") from error
                if not math.isfinite(amount) or amount < 0:
                    raise ValueError(f"Line {line}: amount must be finite and nonnegative.")
                rows.append({"region": region, "amount": row["amount"]})
        except csv.Error as error:
            raise ValueError(f"Line {reader.reader.line_num}: invalid CSV: {error}") from error
    return rows


def summarize(rows: list[dict[str, str]]) -> tuple[dict[str, float], float]:
    """Return regional totals and the mean of those totals."""
    totals: dict[str, float] = {}
    for row in rows:
        region = row["region"]
        totals[region] = totals.get(region, 0.0) + float(row["amount"])
    average = sum(totals.values()) / len(totals) if totals else 0.0
    return totals, average


def top_region(totals: dict[str, float]) -> tuple[str, float] | None:
    """Return the highest-total region, breaking ties alphabetically."""
    if not totals:
        return None
    region = min(totals, key=lambda name: (-totals[name], name))
    return region, totals[region]


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize sales by region.")
    parser.add_argument("path", help="Path to the sales CSV")
    parser.add_argument("--region", help="Report only this region (case-sensitive)")
    args = parser.parse_args()
    try:
        rows = load_rows(args.path)
        if args.region is not None:
            rows = [row for row in rows if row["region"] == args.region]
            if not rows:
                raise ValueError(f"Unknown region: {args.region}")
        totals, average = summarize(rows)
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    for region, amount in sorted(totals.items()):
        print(f"{region}: {amount:.2f}")
    print(f"Average per region: {average:.2f}")


if __name__ == "__main__":
    main()
