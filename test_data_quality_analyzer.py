
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


if __name__ == "__main__":
    unittest.main()
