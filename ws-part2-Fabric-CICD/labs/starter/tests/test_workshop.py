import csv
from decimal import Decimal
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from checks.validate_items import ROOT, sales_contract, validate
from prepare_release import release_changes, replace_release


class WorkshopTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("notebooks", "fabric"):
            shutil.copytree(ROOT / name, self.root / name)
        shutil.copy2(ROOT / "release.json", self.root / "release.json")
        # Fixtures below model a fresh sync, independent of the attendee's release.
        for path in (self.root / "fabric").iterdir():
            if path.is_dir():
                shutil.rmtree(path)
        (self.root / "release.json").write_text('{"release":"baseline"}', encoding="utf-8")

    def add_items(self, ipynb=False):
        for kind, name, identity in (
            ("Lakehouse", "lh_workshop", "00000000-0000-0000-0000-000000000001"),
            ("Notebook", "nb_workshop", "00000000-0000-0000-0000-000000000002"),
        ):
            folder = self.root / "fabric" / f"{name}.{kind}"
            folder.mkdir()
            (folder / ".platform").write_text(json.dumps({
                "metadata": {"type": kind, "displayName": name},
                "config": {"logicalId": identity, "version": "2.0"},
            }), encoding="utf-8")
            if kind == "Lakehouse":
                (folder / "lakehouse.metadata.json").write_text("{}", encoding="utf-8")
            else:
                seed = self.root / "notebooks" / "nb_workshop.ipynb"
                if ipynb:
                    shutil.copy2(seed, folder / "notebook-content.ipynb")
                else:
                    notebook = json.loads(seed.read_text(encoding="utf-8"))
                    source = "\n\n".join("".join(cell["source"]) for cell in notebook["cells"]
                                        if cell["cell_type"] == "code")
                    (folder / "notebook-content.py").write_text(source, encoding="utf-8")
                self.notebook = folder / ("notebook-content.ipynb" if ipynb else "notebook-content.py")

    def test_seed_and_csv_match_exactly(self):
        self.assertEqual(sales_contract(ROOT / "notebooks" / "nb_workshop.ipynb"), "baseline")
        with (ROOT / "data" / "sales.csv").open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(rows, [
            {"channel": "Online", "amount": "100.00"},
            {"channel": "Store", "amount": "200.00"},
            {"channel": "Partner", "amount": "50.00"},
        ])
        self.assertEqual(sum(Decimal(row["amount"]) for row in rows), Decimal("350.00"))

    def test_setup_mode_allows_no_items_but_ci_does_not(self):
        self.assertIn("setup only", validate(self.root))
        with self.assertRaisesRegex(ValueError, "No Fabric items"):
            validate(self.root, require_items=True)

    def test_synced_baseline_passes(self):
        self.add_items()
        self.assertIn("release=baseline", validate(self.root, require_items=True))

    def test_both_export_formats_support_release(self):
        for ipynb in (False, True):
            with self.subTest(ipynb=ipynb):
                if ipynb:
                    for folder in (self.root / "fabric").iterdir():
                        if folder.is_dir():
                            shutil.rmtree(folder)
                    (self.root / "release.json").write_text('{"release":"baseline"}', encoding="utf-8")
                self.add_items(ipynb=ipynb)
                changes = release_changes(self.root)
                self.assertEqual(len(changes), 2)
                self.assertEqual(sales_contract(self.notebook), "baseline")
                for path, _, after in changes:
                    path.write_bytes(after.encode("utf-8"))
                self.assertIn("release=tax", validate(self.root, require_items=True))
                with self.assertRaises(ValueError):
                    release_changes(self.root)

    def test_missing_and_invalid_platform_fail(self):
        self.add_items()
        platform = self.notebook.parent / ".platform"
        platform.write_text("{", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            validate(self.root, require_items=True)
        platform.unlink()
        with self.assertRaises(FileNotFoundError):
            validate(self.root, require_items=True)

    def test_missing_lakehouse_definition_fails(self):
        self.add_items()
        (self.root / "fabric/lh_workshop.Lakehouse/lakehouse.metadata.json").unlink()
        with self.assertRaises(FileNotFoundError):
            validate(self.root, require_items=True)

    def test_release_mismatch_fails(self):
        self.add_items()
        (self.root / "release.json").write_text('{"release":"tax"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs"):
            validate(self.root, require_items=True)

    def test_wrong_tax_logic_fails(self):
        self.add_items()
        source = self.notebook.read_text(encoding="utf-8").replace('Decimal("1.10")', 'Decimal("1.20")')
        self.notebook.write_text(source, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "incorrect"):
            validate(self.root, require_items=True)

    def test_duplicate_logical_id_fails(self):
        self.add_items()
        platform = self.notebook.parent / ".platform"
        value = json.loads(platform.read_text(encoding="utf-8"))
        value["config"]["logicalId"] = "00000000-0000-0000-0000-000000000001"
        platform.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate logical"):
            validate(self.root, require_items=True)

    def test_release_patch_preserves_metadata_and_line_endings(self):
        source = '# META\r\nRELEASE = "baseline"  # release\r\n# binding\r\n'
        self.assertEqual(replace_release(source),
                         '# META\r\nRELEASE = "tax"  # release\r\n# binding\r\n')

    def test_cli_preview_apply_and_failure_exit_codes(self):
        command = [sys.executable, str(ROOT / "prepare_release.py"), "--root", str(self.root)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL:", result.stderr)
        self.add_items()
        before = self.notebook.read_bytes()
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.notebook.read_bytes(), before)
        result = subprocess.run(command + ["--apply"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sales_contract(self.notebook), "tax")

    def test_validator_cli_rejects_empty_ci(self):
        result = subprocess.run([
            sys.executable, str(ROOT / "checks/validate_items.py"),
            "--root", str(self.root), "--require-items",
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL:", result.stderr)


if __name__ == "__main__":
    unittest.main()
