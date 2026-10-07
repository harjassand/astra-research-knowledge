#!/usr/bin/env python3
"""Targeted corruption controls for the compressed posterior completion."""
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import time

import independent_filtered_verifier as check

OWN = Path(__file__).resolve().parent


def main():
    began = time.perf_counter()
    data = (OWN / "source_snapshots/scaling_N32.json").read_bytes()
    original = json.loads(data)["model"]
    cases = []

    def reject(name, model):
        try:
            check.verify(model)
        except ValueError as error:
            cases.append({"name": name, "status": "REJECTED", "reason": str(error)})
        else:
            raise ValueError("corrupt control accepted: " + name)

    bad = deepcopy(original)
    old = check.independent.rational(bad["block_population_TV"])
    bad["block_population_TV"] = check.independent.encode(Q(0))
    bad["total_target_trace_distance_upper"] = check.independent.encode(
        check.independent.rational(bad["total_target_trace_distance_upper"]) - old)
    reject("omitted actual-block-versus-fhat bridge with self-consistent total", bad)

    bad = deepcopy(original)
    bad["block_population_TV"] = check.independent.encode(old - Q(1, 2 ** 160))
    bad["total_target_trace_distance_upper"] = check.independent.encode(
        check.independent.rational(bad["total_target_trace_distance_upper"]) - Q(1, 2 ** 160))
    reject("bridge reduced by one160-bit quantum with self-consistent total", bad)

    bad = deepcopy(original)
    branch = next(b for b in bad["branches"] if b["k"] >= 2)
    branch["Dicke_model"]["phase_modulus"] = 1
    reject("recurrence of repaired child phase-modulus corruption", bad)

    result = {"utc": datetime.now(timezone.utc).isoformat(),
              "status": "PASS three consequential corrupt controls rejected",
              "source_sha256": sha256(data).hexdigest(), "controls": cases,
              "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "checker_sha256": sha256((OWN / "independent_filtered_verifier.py").read_bytes()).hexdigest(),
              "wall_seconds": time.perf_counter() - began}
    (OWN / "FILTERED_NEGATIVE_CONTROLS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "wall_seconds": result["wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
