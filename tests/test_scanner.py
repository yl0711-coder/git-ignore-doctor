import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from git_ignore_doctor.scanner import Scanner, shell_quote


class ScannerTest(unittest.TestCase):
    def test_builds_report_from_git_file_lists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".gitignore").write_text(".DS_Store\n/vendor/\n", encoding="utf-8")

            repository = Mock()
            repository.root = root
            repository.tracked_files.return_value = [".env", ".DS_Store", "src/app.php"]
            repository.untracked_files.return_value = ["debug.log"]
            repository.tracked_ignored_files.return_value = [".DS_Store"]

            report = Scanner(repository).scan()

            self.assertEqual([".DS_Store"], report.tracked_ignored)
            self.assertEqual({".DS_Store", ".env"}, {item.path for item in report.risky_tracked})
            self.assertEqual(["debug.log"], [item.path for item in report.risky_untracked])
            self.assertIn(".env", report.suggested_ignores)
            self.assertIn("*.log", report.suggested_ignores)
            self.assertIn("git rm --cached -- .env", report.fix_plan)

    def test_shell_quote_quotes_paths_with_spaces(self) -> None:
        self.assertEqual("'my file.log'", shell_quote("my file.log"))


if __name__ == "__main__":
    unittest.main()
