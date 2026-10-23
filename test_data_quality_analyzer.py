
import tempfile
import unittest
from pathlib import Path

from data_quality_analyzer import analyze_csv


class TestDataQualityAnalyzer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.csv_file = Path(self.temp_dir.name) / "sample.csv"

    def write_csv(self, content):
        self.csv_file.write_text(content, encoding="utf-8")

    def test_missing_values(self):
        self.write_csv("name,city\nAnu,Chennai\nRavi,\n")
        report = analyze_csv(self.csv_file)
        self.assertEqual(report["missing_cells"], 1)

    def test_duplicate_rows(self):
        self.write_csv("name,city\nAnu,Chennai\nAnu,Chennai\n")
        report = analyze_csv(self.csv_file)
        self.assertEqual(
            report["duplicate_rows_after_first_occurrence"], 1
        )

    def test_completeness(self):
        self.write_csv("name,city\nAnu,Chennai\nRavi,\n")
        report = analyze_csv(self.csv_file)
        self.assertEqual(report["completeness_percent"], 75.0)

    def test_empty_file(self):
        self.write_csv("")
        with self.assertRaises(ValueError):
            analyze_csv(self.csv_file)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            analyze_csv(self.csv_file)

    def test_rows_with_extra_fields(self):
        self.write_csv("name,city\nAnu,Chennai,Extra\n")
        report = analyze_csv(self.csv_file)
        self.assertEqual(report["rows"], 1)
        self.assertEqual(report["malformed_row_count"], 1)
        self.assertEqual(
            report["malformed_rows"],
            [{
                "line": 2,
                "expected_fields": 2,
                "actual_fields": 3,
            }],
        )

    def test_rows_with_too_few_fields(self):
        self.write_csv("name,city\nAnu\n")
        report = analyze_csv(self.csv_file)
        self.assertEqual(report["malformed_row_count"], 1)
        self.assertEqual(
            report["missing_values_by_column"]["city"], 1
        )

    def test_valid_rows_not_malformed(self):
        self.write_csv("name,city\nAnu,Chennai\n")
        report = analyze_csv(self.csv_file)
        self.assertEqual(report["malformed_row_count"], 0)


if __name__ == "__main__":
    unittest.main()
