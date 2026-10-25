#!/usr/bin/env python3
"""Reproduce the revealing sensor-delay/resolution comparison."""
from pathlib import Path
import csv
import json
import phase_valve_model as v

p=Path(__file__).resolve().parent
r,m=v.geometry()
results=[]
for lag,dt in [(0.,.1),(5.,.1),(5.,.05)]:
    result,history=v.run(r,m,.1,lag,.02,dt=dt,trace=True)
    results.append(result)
    if lag==5 and dt==.1:
        with (p/'delay_sensitive_trace.csv').open('w',newline='') as f:
            w=csv.writer(f)
            w.writerow(['t_s','oxygen_min','oxygen_median','oxygen_max',
                        'adequate_fraction','pressure','flow','actuator_net_power',
                        'max_stroke_m'])
            w.writerows(history)
(p/'delay_resolution_checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
