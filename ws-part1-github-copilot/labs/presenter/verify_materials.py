"""Check starter behavior and local Markdown file targets without extra packages."""

from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote


LABS = Path(__file__).resolve().parents[1]
PART1 = LABS.parent


class MaterialChecks(unittest.TestCase):
    def test_starter_output_is_the_exercise_baseline(self):
        result = subprocess.run(
            [sys.executable, "summarize.py", "data/sales.csv"],
            cwd=LABS / "starter",
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
