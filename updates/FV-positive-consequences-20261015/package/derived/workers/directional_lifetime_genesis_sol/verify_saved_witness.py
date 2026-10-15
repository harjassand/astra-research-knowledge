#!/usr/bin/env python3
"""Reverify a saved LJ38 trial/routing witness without any coarse/full solve.

This reloads/encloses source decimal coefficients; it does not trust nominal
coefficients, a claimed cluster balance, or a cached cycle decomposition.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import terminal_mass_certificate as m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--result", required=True)
    ap.add_argument("--witness", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    source = json.loads(Path(args.result).read_text())
    receipt = source["input"]
    precision = source["adaptive"]["certificate"]["precision"]
    for filename, key in (("min.data", "minima_sha256"), ("ts.data", "transition_states_sha256")):
        if m.file_sha(Path(args.source_dir) / filename) != receipt[key]:
            raise ValueError("Source file hash mismatch")
    claimed_witness = source["adaptive"]["witness"]["sha256"]
    if m.file_sha(args.witness) != claimed_witness:
        raise ValueError("Witness hash mismatch")
    g, new_receipt = m.load_lj38(args.source_dir, receipt["temperature"], True,
        precision, receipt["source_original_1_based"], receipt["target_original_1_based"])
    z = np.load(args.witness, allow_pickle=False)
    if not (int(z["n"]) == g.n and int(z["source"]) == g.s and int(z["target"]) == g.t
            and np.array_equal(z["u"], g.u) and np.array_equal(z["v"], g.v)):
        raise ValueError("Witness topology or endpoint mismatch")
    cert = m.interval_certificate(g, z["x"], z["y"], z["tree"], precision)
    old = source["adaptive"]["certificate"]
    same = all(cert[k] == old[k] for k in ("lower", "upper", "relative_width"))
    output = dict(status="reverified" if same else "changed_interval_requires_review",
                  same_interval=same, coefficient_model=new_receipt,
                  certificate=cert, htst_time_interval=m.htst_time_interval(cert, precision),
                  performed_solve=False,
                  scope="same_implementation_postprocessing_replay_not_independent_mathematical_review")
    Path(args.output).write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
