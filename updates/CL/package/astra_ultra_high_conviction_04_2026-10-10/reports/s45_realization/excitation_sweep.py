#!/usr/bin/env python3
"""Evaluate physical excitation/conditioning tradeoff; this is not acquisition."""
import json
import numpy as np
from diagnostic import ROOT, make_controls, random_spd, simulate

K=random_spd(5,316)
rows=[]
for amp in [2.5,5,10,20,40]:
    u=make_controls(714,amp)
    y,J=simulate(K,u,.05,.3,jac=True,substeps=4)
    yy,_=simulate(K,u,.05,.3,substeps=8)
    sv=np.linalg.svd(J.reshape(-1,15),compute_uv=False)
    row=dict(amplitude=amp,condition=float(sv[0]/sv[-1]),smin=float(sv[-1]),
        worst_1sigma_at_noise1e5=float(1e-5/sv[-1]),
        integration_bias=float(np.sqrt(np.mean((y-yy)**2))),
        energy=float(.05*np.sum(u*u)))
    rows.append(row)
    print(row)
(ROOT/'excitation_sweep.json').write_text(json.dumps(rows,indent=2)+'\n')
