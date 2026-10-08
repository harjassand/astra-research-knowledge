"""Reproduce one rational N33 plateau diagnostic with the supplied checker."""
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHECKER = ROOT / "work/agents/systems_metabolism/stochastic_safety/evidence/reaction_certificate.py"
spec = importlib.util.spec_from_file_location("reaction_certificate", CHECKER)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

candidate = {
    "c": ["1/2", "1/2"],
    "kappa": 1,
    "K": 4,
    "delta": "1/4",
    "reactions": [
        {"source": [1, 0], "target": [0, 1]},
        {"source": [0, 1], "target": [1, 0]},
    ],
    "labels": [
        {"normal": [0, 0], "offset": 0},
        {"normal": [1, 0], "offset": "-1/10"},
        {"normal": [-1, 0], "offset": "9/10"},
    ],
    "outer_box": [[0, 1], [0, 1]],
    "inner_box": [["1/20", "19/20"], ["1/20", "19/20"]],
    "containment_margin": "1/40",
}

result = checker.check(candidate, maxdepth=10, bits=48)
output = Path(__file__).with_name("CHECK_ONE_LINK.json")
output.write_text(json.dumps(checker.stringify(result), indent=2) + "\n")
print(f"wrote {output}")
print(checker.stringify({key: result.get(key) for key in ("status", "scope", "equations", "delta", "active_cells", "stats")}))
