"""Check copied starter/reference behavior and local links without extra packages."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote


LABS = Path(__file__).resolve().parents[1]
PART1 = LABS.parent
STARTER_ITEMS = (
    ".gitignore",
    "README.md",
    "data",
    "tests",
    "pytest.ini",
    "requirements-dev.txt",
    "summarize.py",
)


class MaterialChecks(unittest.TestCase):
    def test_starter_output_is_the_exercise_baseline(self):
        with tempfile.TemporaryDirectory(prefix="copilot-workshop-") as directory:
            demo = Path(directory)
            for name in STARTER_ITEMS:
                source = LABS / "starter" / name
                if source.is_dir():
                    shutil.copytree(
                        source,
                        demo / name,
                        ignore=shutil.ignore_patterns(
                            ".git", ".venv", "__pycache__", ".pytest_cache"
                        ),
                    )
                else:
                    shutil.copyfile(source, demo / name)
            self.assertEqual({path.name for path in demo.iterdir()}, set(STARTER_ITEMS))
            result = subprocess.run(
                [sys.executable, "summarize.py", "data/sales.csv"],
                cwd=demo,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "East: 150.00\nNorth: 75.00\nWest: 250.00\nAverage per region: 118.75\n",
        )
        self.assertEqual(result.stderr, "")

    def test_reference_lab_cli_examples(self):
        cases = [
            (
                "sales.csv",
                [],
                0,
                "East: 150.00\nNorth: 75.00\nWest: 250.00\nAverage per region: 158.33\n",
                "",
            ),
            ("sales.csv", ["--region", "East"], 0, "East: 150.00\nAverage per region: 150.00\n", ""),
            ("sales.csv", ["--region", "Unknown"], 2, "", "Unknown region"),
            ("invalid-amount.csv", [], 2, "", "Line 3"),
            ("missing-column.csv", [], 2, "", "region and amount columns"),
            ("empty.csv", [], 0, "Average per region: 0.00\n", ""),
        ]
        for fixture, arguments, code, output, error in cases:
            with self.subTest(fixture=fixture, arguments=arguments):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(LABS / "presenter" / "solution" / "summarize.py"),
                        str(LABS / "starter" / "data" / fixture),
                        *arguments,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual(result.stdout, output)
                if error:
                    self.assertIn(error, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                else:
                    self.assertEqual(result.stderr, "")

    def test_python_syntax(self):
        for path in PART1.rglob("*.py"):
            if ".venv" in path.parts:
                continue
            with self.subTest(path=path):
                compile(path.read_text(encoding="utf-8"), str(path), "exec")

    def test_local_markdown_file_targets(self):
        for path in PART1.rglob("*.md"):
            if ".venv" in path.parts:
                continue
            for target in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                local = unquote(target.split("#", 1)[0])
                with self.subTest(document=path, target=target):
                    self.assertTrue((path.parent / local).exists(), f"Broken link: {target}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
