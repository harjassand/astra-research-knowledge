#!/usr/bin/env python3
"""Read pinned Git objects; do not mutate the source checkout or claim a build."""
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
REPO = ROOT / "work/sources/openai-math"
OUT = Path(__file__).with_name("import_audit.json")
REV = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
todo = ["OAI.InformationTheory.PhotonNumber.Inequality", "OAI.InformationTheory.PhotonNumber.Interpolation"]
seen = {}
external = set()
while todo:
    module = todo.pop()
    if not module.startswith("OAI."):
        external.add(module)
        continue
    if module in seen:
        continue
    path = "lean/" + module.replace(".", "/") + ".lean"
    source = subprocess.check_output(["git", "-C", str(REPO), "show", REV + ":" + path], text=True)
    seen[module] = {
        "path": path,
        "sha256": hashlib.sha256(source.encode()).hexdigest(),
        "lines": len(source.splitlines()),
        "checked_out": (REPO / path).is_file(),
        "lexical_flags": [
            {"line": n, "text": line}
            for n, line in enumerate(source.splitlines(), 1)
            if re.match(r"^\s*(axiom|opaque)\b", line)
            or re.search(r"\b(sorry|admit|unsafe)\b", line)
        ],
    }
    todo.extend(re.findall(r"^import\s+(\S+)", source, re.M))

def f(x):
    return x / math.sinh(x) if x else 1.0

m, y, xs, target = 0.5, -1.0, [10.0, -10.0], -4.9
weights = [
    lambda x: m * f(x) * math.exp(x),
    lambda x: m * f(x) * math.exp(-x),
    lambda x: m * f(y) * math.exp(y),
    lambda x: m * f(y) * math.exp(-y),
]
F = lambda x: m * f(x) * f(y) / f(x + y)
counterexample = {
    "source": "span{(1,1)/sqrt(2)} with x=(10,-10), m=.5, y=-1",
    "target": "C with x=-4.9, m=.5, y=-1; L(t(1,1)/sqrt(2))=t",
    "four_comparisons": [
        {"source": sum(w(x) for x in xs) / 2, "target": w(target)} for w in weights
    ],
    "F_source": sum(F(x) for x in xs) / 2,
    "F_target": F(target),
    "missing_hypothesis": "source test space is invariant under parameter multipliers",
    "physical_amplifier_counterexample": False,
}
data = {
    "revision": REV,
    "OAI_module_count": len(seen),
    "modules": seen,
    "external_imports": sorted(external),
    "build_performed": False,
    "kernel_axiom_audit_performed": False,
    "standalone_interpolation_counterexample": counterexample,
}
OUT.write_text(json.dumps(data, indent=2) + "\n")
print(json.dumps({k: data[k] for k in ["revision", "OAI_module_count", "external_imports", "build_performed", "kernel_axiom_audit_performed"]}, indent=2))
print("Lexical flags:", sum(len(v["lexical_flags"]) for v in seen.values()))
print("Counterexample F source/target:", counterexample["F_source"], counterexample["F_target"])
