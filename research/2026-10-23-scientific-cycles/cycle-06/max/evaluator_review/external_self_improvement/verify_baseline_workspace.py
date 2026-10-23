#!/usr/bin/env python3
"""Verify one released baseline workspace observation without running agent code."""
from pathlib import Path
import ast
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "released_metadata" / "swe_dgm_noselfimprove"
PARENT = "20250407_212519_184190"
CHILD = "20250408_005738_095636"

child = json.loads((RUN / CHILD / "metadata.json").read_text())
assert child["parent_commit"] == PARENT
parent_patch = (RUN / PARENT / "model_patch.diff").read_text()
assert '+                    "enum": ["view", "create", "edit", "edit_range"],' in parent_patch
history = ast.literal_eval((RUN / CHILD / "self_evo.md").read_text())
request = history[3]["content"]
assert any("/dgm/tools/edit.py" in part.get("text", "") for part in request)
view = history[4]["content"][0]["text"]
assert "/dgm/tools/edit.py:" in view
observed = "\n".join(re.sub(r"^\s*\d+\t", "", line) for line in view.splitlines()[1:]) + "\n"
tree = ast.parse(observed)
info = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "tool_info")
dictionary = ast.literal_eval(next(n.value for n in info.body if isinstance(n, ast.Return)))
commands = dictionary["input_schema"]["properties"]["command"]["enum"]
assert commands == ["view", "create", "edit"]
assert "edit_range" not in observed
out = ROOT / "baseline_workspace_evidence"
out.mkdir(exist_ok=True)
(out / "child_observed_tools_edit.py").write_text(observed)
report = {
    "status": "PASS",
    "kind": "Independent parsing and consistency check of released source/trace; not a rerun of DGM",
    "run": "swe_dgm_noselfimprove",
    "parent": PARENT,
    "child": CHILD,
    "parent_patch_adds_command": "edit_range",
    "child_pre_edit_observed_commands": commands,
    "observed_file_sha256": hashlib.sha256(observed.encode()).hexdigest(),
    "conclusion": "The child trace records an edit.py lacking the parent's saved edit_range addition.",
    "limits": [
        "One observed attempt; not proof that every baseline attempt had identical behavior.",
        "Does not attribute aggregate baseline performance or failures to the workspace discrepancy.",
        "Does not independently certify the historical execution underlying the released trace.",
    ],
}
(out / "VERIFICATION.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
