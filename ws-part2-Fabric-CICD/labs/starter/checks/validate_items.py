"""Offline workshop checks, not a Fabric deployment or comprehensive secret scanner."""

import argparse
import ast
from decimal import Decimal
import json
from pathlib import Path
import sys
from uuid import UUID


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ROWS = [
    ("Online", Decimal("100.00")),
    ("Store", Decimal("200.00")),
    ("Partner", Decimal("50.00")),
]


def read_source(path):
    if path.suffix == ".py":
        return path.read_bytes().decode("utf-8-sig")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
        raise ValueError(f"{path}: expected a version 4 notebook")
    return "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )


def sales_contract(path):
    """Run only the trusted workshop's pure function, never its Spark/write cells."""
    tree = ast.parse(read_source(path), filename=str(path))
    values = {}
    functions = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ("RELEASE", "SALES_ROWS"):
                    if target.id in values:
                        raise ValueError(f"{path}: duplicate {target.id}")
                    values[target.id] = ast.literal_eval(node.value)
        if isinstance(node, ast.FunctionDef) and node.name == "build_sales":
            functions.append(node)
    if set(values) != {"RELEASE", "SALES_ROWS"} or len(functions) != 1:
        raise ValueError(f"{path}: missing or duplicate workshop sales contract")
    if values["RELEASE"] not in ("baseline", "tax"):
        raise ValueError(f"{path}: release must be baseline or tax")
    namespace = {"Decimal": Decimal, "SALES_ROWS": values["SALES_ROWS"]}
    function_module = ast.Module(body=functions, type_ignores=[])
    exec(compile(function_module, str(path), "exec"), namespace)
    build_sales = namespace["build_sales"]
    for release in ("baseline", "tax"):
        expected = [
            row if release == "baseline" else row + (
                (row[1] * Decimal("1.10")).quantize(Decimal("0.01")),
            )
            for row in EXPECTED_ROWS
        ]
        if build_sales(release) != expected:
            raise ValueError(f"{path}: incorrect rows, shape, or amounts for {release}")
    try:
        build_sales("invalid")
    except ValueError:
        pass
    else:
        raise ValueError(f"{path}: unknown release must raise ValueError")
    return values["RELEASE"]


def notebook_path(folder):
    paths = [path for path in folder.iterdir() if path.name in (
        "notebook-content.py", "notebook-content.ipynb"
    ) and path.is_file()]
    if len(paths) != 1:
        raise ValueError(f"{folder}: expected exactly one notebook-content.py or .ipynb")
    return paths[0]


def validate(root, require_items=False):
    release = json.loads((root / "release.json").read_text(encoding="utf-8"))["release"]
    if release not in ("baseline", "tax"):
        raise ValueError("release.json: release must be baseline or tax")
    # The import seed remains baseline; only the Fabric-generated copy is released.
    if sales_contract(root / "notebooks" / "nb_workshop.ipynb") != "baseline":
        raise ValueError("The import seed must stay at baseline")
    fabric = root / "fabric"
    if not fabric.is_dir():
        raise ValueError("Missing fabric directory")
    folders = [path for path in fabric.iterdir() if path.is_dir()]
    if not folders:
        if require_items:
            raise ValueError("No Fabric items: complete the initial workspace-to-Git sync")
        if release != "baseline":
            raise ValueError("A tax release requires synced Fabric items")
        return "PASS: starter baseline; no synced Fabric items yet (setup only)"
    found = {}
    logical_ids = set()
    for folder in folders:
        platform = json.loads((folder / ".platform").read_text(encoding="utf-8"))
        metadata = platform["metadata"]
        identity = (metadata["type"], metadata["displayName"])
        if identity not in {("Lakehouse", "lh_workshop"), ("Notebook", "nb_workshop")}:
            raise ValueError(f"{folder}: unexpected item type/name {identity}")
        if identity in found:
            raise ValueError(f"Duplicate item: {identity}")
        logical_id = UUID(platform["config"]["logicalId"])
        if logical_id in logical_ids:
            raise ValueError("Duplicate logical item ID")
        logical_ids.add(logical_id)
        found[identity] = folder
        if identity[0] == "Notebook":
            actual = sales_contract(notebook_path(folder))
            if actual != release:
                raise ValueError(f"Notebook release {actual} differs from release.json {release}")
        else:
            definition = json.loads((folder / "lakehouse.metadata.json").read_text(encoding="utf-8"))
            if not isinstance(definition, dict):
                raise ValueError(f"{folder}: lakehouse definition must be a JSON object")
    if len(found) != 2:
        raise ValueError("Expected both lh_workshop and nb_workshop; sync both items")
    return f"PASS: 2 Fabric items; release={release}; baseline=350.00; tax=385.00"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--require-items", action="store_true")
    args = parser.parse_args()
    try:
        message = validate(args.root, args.require_items)
    except (OSError, ValueError, KeyError, TypeError, SyntaxError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
