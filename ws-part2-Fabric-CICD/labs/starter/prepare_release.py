"""Preview/apply the prebuilt tax release to the synced notebook, never to Fabric."""

import argparse
import ast
import difflib
import json
from pathlib import Path
import sys

from checks.validate_items import ROOT, notebook_path, validate


def replace_release(source):
    assignments = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "RELEASE" for target in node.targets)
    ]
    if len(assignments) != 1:
        raise ValueError("Expected one RELEASE assignment")
    node = assignments[0]
    if ast.literal_eval(node.value) != "baseline":
        raise ValueError("Release is already changed; inspect your branch instead of applying again")
    lines = source.splitlines(keepends=True)
    if node.lineno != node.end_lineno:
        raise ValueError("Expected a single-line RELEASE assignment")
    index = node.lineno - 1
    line = lines[index]
    lines[index] = line[:node.col_offset] + 'RELEASE = "tax"' + line[node.end_col_offset:]
    return "".join(lines)


def release_changes(root):
    validate(root, require_items=True)
    release_path = root / "release.json"
    if json.loads(release_path.read_text(encoding="utf-8"))["release"] != "baseline":
        raise ValueError("release.json must be baseline; use a fresh feature branch")
    candidates = []
    for folder in (root / "fabric").iterdir():
        if folder.is_dir():
            metadata = json.loads((folder / ".platform").read_text(encoding="utf-8"))["metadata"]
            if metadata["type"] == "Notebook":
                candidates.append(notebook_path(folder))
    if len(candidates) != 1:
        raise ValueError("Expected exactly one synced notebook")
    path = candidates[0]
    before = path.read_bytes().decode("utf-8")
    if path.suffix == ".py":
        after = replace_release(before)
    else:
        notebook = json.loads(before)
        changed = 0
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                if any(
                    isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "RELEASE" for t in node.targets)
                    for node in ast.parse(source).body
                ):
                    cell["source"] = replace_release(source).splitlines(keepends=True)
                    changed += 1
        if changed != 1:
            raise ValueError("Expected RELEASE in one notebook cell")
        after = json.dumps(notebook, indent=2, ensure_ascii=False) + "\n"
    return [
        (path, before, after),
        (release_path, release_path.read_text(encoding="utf-8"), '{\n  "release": "tax"\n}\n'),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--apply", action="store_true", help="Write the two previewed local files")
    args = parser.parse_args()
    try:
        changes = release_changes(args.root)
        for path, before, after in changes:
            print("".join(difflib.unified_diff(
                before.splitlines(keepends=True), after.splitlines(keepends=True),
                fromfile=str(path), tofile=str(path),
            )))
        if args.apply:
            for path, _, after in changes:
                path.write_bytes(after.encode("utf-8"))
            print(validate(args.root, require_items=True))
            print("Applied locally. Nothing committed, synced, or deployed.")
        else:
            print("Preview only. Review, then use --apply to write these two local files.")
    except (OSError, ValueError, KeyError, TypeError, SyntaxError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
