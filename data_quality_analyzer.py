
"""CSV Data Quality Analyzer."""

import csv
import json
import sys
from collections import Counter
from pathlib import Path


def analyze_csv(file_path):
    """Analyze a CSV dataset and return a quality report."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or has no header.")

        headers = reader.fieldnames

        if not headers or any(
            header is None or not header.strip()
            for header in headers
        ):
            raise ValueError("CSV headers must not be empty.")

        if len(set(headers)) != len(headers):
            raise ValueError("Duplicate column names detected.")

        rows = list(reader)

    missing = Counter()
    seen_rows = set()
    duplicate_count = 0

    for row in rows:
        values = tuple(
            (row.get(header) or "").strip()
            for header in headers
        )

        for header, value in zip(headers, values):
            if not value:
                missing[header] += 1

        if values in seen_rows:
            duplicate_count += 1
        else:
            seen_rows.add(values)

    row_count = len(rows)
    column_count = len(headers)
    total_cells = row_count * column_count
    missing_count = sum(missing.values())

    completeness = (
        round(
            100 * (total_cells - missing_count) / total_cells,
            2,
        )
        if total_cells
        else 100.0
    )

    return {
        "file": path.name,
        "rows": row_count,
        "columns": column_count,
        "column_names": headers,
        "missing_values_by_column": {
            header: missing.get(header, 0)
            for header in headers
        },
        "missing_cells": missing_count,
        "duplicate_rows_after_first_occurrence": duplicate_count,
        "completeness_percent": completeness,
    }


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python data_quality_analyzer.py <input.csv>",
            file=sys.stderr,
        )
        return 2

    try:
        report = analyze_csv(sys.argv[1])
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
