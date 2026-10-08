#!/usr/bin/env python3
"""Check RF sign after different green-light prehistories in the six-state ODE."""
import json
from pathlib import Path
import runpy

m = runpy.run_path(str(Path(__file__).with_name("sign_audit.py")), run_name="protocol_check_import")
p, y0 = m["TABLE1"], m["Y0"]
step, simulate = m["rk4_step"], m["simulate_pair"]
dt, i520, beta_off = 1e-4, 3.8, 0.68

def constant_state(duration):
    y = tuple(y0)
    for _ in range(round(duration/dt)):
        y = step(y, beta_off, p, i520, dt)
    return y

def invs(y):
    g,t,r,f,h,q=y
    return (g+t+r, f+h+q, g+t+2*f+q)

out=[]
for pre in (0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0):
    y = constant_state(pre)
    for label, beta_on in (("literal positive separation increment", 0.7151),
                           ("corrected negative separation increment", 0.6449)):
        rows = simulate(y, y, p, i520, beta_off, beta_on, 5.0, dt)
        on_rows = [r for r in rows if 0 < r["t"] < 5.0]
        rel = [(r["t"], r["dG"]/r["G_control"]) for r in on_rows]
        samples=[]
        for t in (0.1,0.5,1.0,2.5,5.0):
            r=next(r for r in rows if abs(r["t"]-t)<1e-10)
            samples.append({"t_s":t,"delta_G_uM":r["dG"],
                            "delta_G_over_G":r["dG"]/r["G_control"],
                            "G_control_uM":r["G_control"],"R_control_uM":r["R_control"]})
        out.append({"green_preexposure_s":pre,"mapping":label,
                    "pre_RF_state_G_T_R_F_H_Q_uM":list(y),
                    "pre_RF_invariants":invs(y),
                    "first_pulse_delta_G_over_G_minmax":
                        {"min":min(v for _,v in rel),"max":max(v for _,v in rel)},
                    "delta_Gdot_at_RF_on_uM_s":
                        -(beta_on-beta_off)*p.kred*y[4]*y[1],
                    "samples":samples})

path=Path(__file__).with_name("protocol_check.json")
path.write_text(json.dumps(out,indent=2)+"\n")
for r in out:
    print(r["green_preexposure_s"],r["mapping"],
          r["first_pulse_delta_G_over_G_minmax"],r["samples"][-1]["delta_G_over_G"],
          r["delta_Gdot_at_RF_on_uM_s"])
