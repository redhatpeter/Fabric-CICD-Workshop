"""Verify local workshop assets only; no cloud calls or persistent mutations."""

import ast
from contextlib import redirect_stdout
import csv
from decimal import Decimal
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.parse import unquote


LABS = Path(__file__).resolve().parents[1]
PART2 = LABS.parent
STARTER = LABS / "starter"
SOLUTION = LABS / "presenter" / "solution"
spec = importlib.util.spec_from_file_location("workshop_validator", STARTER / "checks/validate_items.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class MaterialChecks(unittest.TestCase):
    def test_attendee_regressions(self):
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=STARTER, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_seed_and_answer_differ_only_in_release(self):
        seed = json.loads((STARTER / "notebooks/nb_workshop.ipynb").read_text(encoding="utf-8"))
        answer = json.loads((SOLUTION / "notebooks/nb_workshop.ipynb").read_text(encoding="utf-8"))
        self.assertEqual(validator.sales_contract(STARTER / "notebooks/nb_workshop.ipynb"), "baseline")
        self.assertEqual(validator.sales_contract(SOLUTION / "notebooks/nb_workshop.ipynb"), "tax")
        answer["cells"][1]["source"] = [
            line.replace('RELEASE = "tax"', 'RELEASE = "baseline"')
            for line in answer["cells"][1]["source"]
        ]
        self.assertEqual(seed, answer)
        self.assertEqual(json.loads((SOLUTION / "release.json").read_text(encoding="utf-8")),
                         {"release": "tax"})

    def test_expected_tax_csv(self):
        with (SOLUTION / "expected-sales-tax.csv").open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(rows, [
            {"channel": "Online", "amount": "100.00", "amount_with_tax": "110.00"},
            {"channel": "Partner", "amount": "50.00", "amount_with_tax": "55.00"},
            {"channel": "Store", "amount": "200.00", "amount_with_tax": "220.00"},
        ])
        self.assertEqual(sum(Decimal(row["amount_with_tax"]) for row in rows), Decimal("385.00"))

    def test_notebook_structure_and_syntax(self):
        for path in LABS.rglob("*.ipynb"):
            notebook = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(notebook["nbformat"], 4)
            ids = [cell["id"] for cell in notebook["cells"]]
            self.assertEqual(len(ids), len(set(ids)))
            for cell in notebook["cells"]:
                self.assertIsInstance(cell["source"], list)
                self.assertTrue(all(line.endswith("\n") for line in cell["source"]))
                if cell["cell_type"] == "code":
                    self.assertIsNone(cell["execution_count"])
                    self.assertEqual(cell["outputs"], [])
                    compile("".join(cell["source"]), str(path), "exec")

    def test_real_notebook_guard_before_any_spark_write(self):
        seed = json.loads((STARTER / "notebooks/nb_workshop.ipynb").read_text(encoding="utf-8"))
        tree = ast.parse("".join(seed["cells"][2]["source"]))
        guard_nodes = []
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "table_name" for target in node.targets
            ):
                break
            guard_nodes.append(node)
        self.assertTrue(any(isinstance(node, ast.Raise) for node in ast.walk(
            ast.Module(body=guard_nodes, type_ignores=[])
        )))
        code = compile(ast.Module(body=guard_nodes, type_ignores=[]), "<notebook guard>", "exec")
        base = {
            "currentWorkspaceId": "test-workspace",
            "currentWorkspaceName": "Test",
            "defaultLakehouseWorkspaceId": "test-workspace",
            "defaultLakehouseName": "lh_workshop",
            "defaultLakehouseId": "test-lakehouse",
        }
        cases = [
            ({}, True),
            ({"defaultLakehouseWorkspaceId": "dev-workspace"}, False),
            ({"defaultLakehouseName": "real_customer_data"}, False),
            ({"defaultLakehouseId": ""}, False),
        ]
        for changes, allowed in cases:
            with self.subTest(changes=changes):
                context = base | changes
                modules = {
                    "notebookutils": SimpleNamespace(runtime=SimpleNamespace(context=context)),
                    "pyspark": SimpleNamespace(),
                    "pyspark.sql": SimpleNamespace(functions=SimpleNamespace()),
                }
                with patch.dict(sys.modules, modules), redirect_stdout(io.StringIO()):
                    if allowed:
                        exec(code, {"RELEASE": "baseline"})
                    else:
                        with self.assertRaisesRegex(RuntimeError, "STOP"):
                            exec(code, {"RELEASE": "baseline"})

    def test_python_and_json_syntax(self):
        for path in PART2.rglob("*"):
            if ".venv" in path.parts or "__pycache__" in path.parts or not path.is_file():
                continue
            with self.subTest(path=path):
                if path.suffix == ".py":
                    compile(path.read_text(encoding="utf-8"), str(path), "exec")
                elif path.suffix == ".json":
                    json.loads(path.read_text(encoding="utf-8"))

    def test_local_markdown_file_targets(self):
        for path in PART2.rglob("*.md"):
            if ".venv" in path.parts:
                continue
            for target in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                local = unquote(target.split("#", 1)[0])
                with self.subTest(document=path, target=target):
                    self.assertTrue((path.parent / local).exists(), f"Broken link: {target}")

    def test_workflow_requires_real_items_without_cloud_credentials(self):
        workflow = (STARTER / "workflow-templates/validate.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request:", workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("python checks/validate_items.py --require-items", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertNotIn("pull_request_target", workflow)
        self.assertNotIn("secrets.", workflow)
        self.assertFalse((STARTER / ".github").exists(), "Do not ship an active workflow before sync")


if __name__ == "__main__":
    unittest.main(verbosity=2)
