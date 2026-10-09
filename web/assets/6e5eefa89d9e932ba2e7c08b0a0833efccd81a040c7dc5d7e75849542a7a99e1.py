"""Read-only local-import inventory; this is not a Lean proof replay."""
import hashlib
import json
import re
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parents[4]
LEAN = BASE / "work/sources/openai-math/lean"
OWN = Path(__file__).resolve().parent


def inventory(root_module):
    todo = [root_module]
    modules = {}
    missing_local = []
    external = set()
    suspicious_raw_tokens = []
    while todo:
        module = todo.pop()
        if module in modules:
            continue
        path = LEAN / (module.replace(".", "/") + ".lean")
        if not path.is_file():
            if module.startswith("OAI."):
                missing_local.append(module)
            else:
                external.add(module)
            continue
        raw = path.read_bytes()
        source = raw.decode("utf-8")
        imports = []
        for match in re.finditer(r"^import\s+(.+)$", source, re.M):
            imports.extend(match.group(1).split("--", 1)[0].split())
        modules[module] = {
            "path": str(path.relative_to(BASE)),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "imports": imports,
        }
        todo.extend(imports)
        for line_no, line in enumerate(source.splitlines(), 1):
            tokens = re.findall(r"\b(?:sorry|admit|axiom|opaque|unsafe|implemented_by)\b", line)
            if tokens:
                suspicious_raw_tokens.append({
                    "module": module, "line": line_no, "tokens": tokens,
                    "text": line.strip(),
                })
    return {
        "root_module": root_module,
        "local_module_count": len(modules),
        "local_bytes": sum(v["bytes"] for v in modules.values()),
        "missing_local_imports": sorted(set(missing_local)),
        "external_imports_unverified": sorted(external),
        "raw_token_hits_including_comments": suspicious_raw_tokens,
        "modules": dict(sorted(modules.items())),
    }


result = {
    "kind": "static artifact scope inventory, not proof validation",
    "source_commit": "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb",
    "lean_command_available": shutil.which("lean"),
    "lake_command_available": shutil.which("lake"),
    "proof_replay_attempted": False,
    "source_reported_permitted_axioms": ["propext", "Quot.sound", "Classical.choice"],
    "selected_comparator": "OAI.Problem326.global_bounded_persistent_solution",
    "comparator_scope": "constant positive rates; global existence and all-time bounds dependent on x0",
    "not_comparator_scope": [
        "one class-dependent absorber independent of x0",
        "finite-time entry into that absorber",
        "Caratheodory time-measurable kinetics",
        "general uniform logarithmic valuation rates",
        "subpower state modifiers",
    ],
    "affine_certificate_scope": "arbitrary positive gauge on cube; fixed finite labels; o(h^a) offsets; all active ties; approximating exponent sequences may be outside cube",
    "inventories": [
        inventory("OAI.Analysis.MassAction.AffineExistence"),
        inventory("OAI.Analysis.MassAction.Main"),
    ],
}
output = OWN / "formal_scope_static.json"
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({
    "output": str(output.relative_to(BASE)),
    "replay": result["proof_replay_attempted"],
    "lean": result["lean_command_available"],
    "lake": result["lake_command_available"],
    "inventories": [{
        key: inv[key] for key in [
            "root_module", "local_module_count", "local_bytes", "missing_local_imports",
            "raw_token_hits_including_comments", "external_imports_unverified",
        ]
    } for inv in result["inventories"]],
}, indent=2))
