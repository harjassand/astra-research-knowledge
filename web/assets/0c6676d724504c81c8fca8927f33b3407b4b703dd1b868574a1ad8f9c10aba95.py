#!/usr/bin/env python3
"""Step-halving check for the 5 s RF pulse endpoints in the sign audit."""
import json
from pathlib import Path
import runpy

model = runpy.run_path(str(Path(__file__).with_name("sign_audit.py")), run_name="sign_check_import")
P = model["TABLE1"]
Y0 = model["Y0"]
simulate = model["simulate_pair"]

cases = [
    ("literal positive separation-fraction increment", 0.68, 0.7151),
    ("same baseline with corrected negative separation-fraction increment", 0.68, 0.6449),
]
out = []
for label, beta_off, beta_on in cases:
    for dt in (1e-4, 5e-5, 2.5e-5):
        rows = simulate(Y0, Y0, P, 3.8, beta_off, beta_on, 5.0, dt)
        end = rows[-1]
        out.append({"mapping": label, "dt_s": dt, "t5_G_control_uM": end["G_control"],
                    "t5_G_RF_uM": end["G_pulse"], "t5_delta_G_uM": end["dG"],
                    "t5_delta_G_over_G": end["dG"]/end["G_control"],
                    "sampled_invariant_error_inf_uM":
                        max(r["invariant_error_inf"] for r in rows),
                    "minimum_sampled_species_uM": min(r["min_species"] for r in rows)})
    vals = [r["t5_delta_G_over_G"] for r in out if r["mapping"] == label]
    out[-1]["max_abs_change_under_step_halving"] = max(abs(vals[i]-vals[i-1])
                                                        for i in range(1, len(vals)))

path = Path(__file__).with_name("convergence_check.json")
path.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
