# Checks CSV data quality and malformed rows.
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
        reader = csv.reader(file, strict=True)

        try:
            headers = next(reader)
        except StopIteration:
            raise ValueError(
                "CSV file is empty or has no header."
            ) from None

        if not headers or any(
            not header.strip() for header in headers
        ):
            raise ValueError("CSV headers must not be empty.")

        if len(set(headers)) != len(headers):
            raise ValueError("Duplicate column names detected.")

        missing = Counter()
        seen_rows = set()
        duplicate_count = 0
        malformed_rows = []
        row_count = 0

        for line_number, fields in enumerate(reader, start=2):
            row_count += 1

            if len(fields) != len(headers):
                malformed_rows.append({
                    "line": line_number,
                    "expected_fields": len(headers),
                    "actual_fields": len(fields),
                })
                fields = (fields + [""] * len(headers))[:len(headers)]

            values = tuple(
                (value or "").strip() for value in fields
            )

            for header, value in zip(headers, values):
                if not value:
                    missing[header] += 1

            if values in seen_rows:
                duplicate_count += 1
            else:
                seen_rows.add(values)

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
        "malformed_row_count": len(malformed_rows),
        "malformed_rows": malformed_rows,
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
