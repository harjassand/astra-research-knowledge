#!/usr/bin/env python3
"""Independent flow-map/quadrature checks; not a catalyst fit or universal proof."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parents[1]/"root"
DOC=PARENT/"CAUSAL_IDENTIFIABILITY_THEOREM.md"
SCRIPT=PARENT/"causal_countermodel.py"


def pos(z, duration, mu):
    return z*math.exp(-mu*duration)


def neg(z, duration, lam):
    return 1.0-(1.0-z)*math.exp(-lam*duration)


rows=[]
for h,d,beta,rho in [(10.,.1,0.,.22117569043994356),(10.,.1,1.,.5),(3.,.2,.4,.6),(3.,.2,5.,1.)]:
    D=h+d*beta-(h+d)*rho
    assert 0<D<h
    for mu in [1e-6,1e-4,.001,.01,.03,.05]:
        L=-math.expm1(-mu*h)/mu
        if L<=D:
            continue
        v=math.exp(-mu*h)
        zstar=D/L
        u=(1-zstar)/(1-zstar*v)
        lam=-math.log(u)/d
        assert 0<zstar<1 and 0<u<1 and mu>0 and lam>0
        # Independent event sequence: start after the negative pulse; evolve a
        # full positive hold and then a negative pulse to get the next start.
        after_pos=pos(zstar,h,mu)
        after_neg=neg(after_pos,d,lam)
        assert abs(after_neg-zstar)<5e-14
        T=h
        t=np.linspace(0,T,20001)
        # Direct quadrature of actual arm output trajectories, rather than an
        # integral of the closed-form arm-difference formula.
        isolated_pulse_start=neg(0,d,lam)
        isolated_sham_start=pos(0,d,mu)
        iso_pulse=1-isolated_pulse_start*np.exp(-mu*t)
        iso_sham=1-isolated_sham_start*np.exp(-mu*t)
        iso_quad=float(np.trapezoid(iso_sham-iso_pulse,t))
        conditioned_pulse_start=neg(after_pos,d,lam)
        conditioned_sham_start=pos(after_pos,d,mu)
        cond_pulse=1-conditioned_pulse_start*np.exp(-mu*t)
        cond_sham=1-conditioned_sham_start*np.exp(-mu*t)
        cond_quad=float(np.trapezoid(cond_sham-cond_pulse,t))
        iso_formula=(1-u)*(-math.expm1(-mu*T))/mu
        cond_formula=zstar*(-math.expm1(-mu*(h+d)))*(-math.expm1(-mu*T))/mu
        period_mean=(float(np.trapezoid(1-zstar*np.exp(-mu*t),t))+d*beta)/(h+d)
        # Trapezoidal discretization of a smooth exponential is not exact.
        assert abs(iso_quad-iso_formula)<2e-8
        assert abs(cond_quad-cond_formula)<2e-8
        assert abs(period_mean-rho)<2e-9
        assert abs(cond_formula-D*(-math.expm1(-mu*(h+d))))<2e-14
        rows.append({"h":h,"d":d,"beta":beta,"rho":rho,"mu":mu,"lambda":lam,
                     "isolated_quadrature_s":iso_quad,"isolated_formula_s":iso_formula,
                     "conditioned_quadrature_s":cond_quad,"conditioned_formula_s":cond_formula,
                     "period_mean_quadrature":period_mean,"period_mean_target":rho,
                     "cycle_e_fold_count":-1/math.log(u*v)})

result={"scope":"finite independent flow-map and quadrature diagnostics; analytic audit is in AUDIT.md",
        "reviewed_root_document_sha256":hashlib.sha256(DOC.read_bytes()).hexdigest(),
        "reviewed_root_script_sha256":hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
        "tested_models":len(rows),"models":rows,
        "max_isolated_quadrature_error":max(abs(r["isolated_quadrature_s"]-r["isolated_formula_s"]) for r in rows),
        "max_conditioned_quadrature_error":max(abs(r["conditioned_quadrature_s"]-r["conditioned_formula_s"]) for r in rows),
        "max_period_mean_quadrature_error":max(abs(r["period_mean_quadrature"]-r["period_mean_target"]) for r in rows)}
(ROOT/"authored/root_countermodel_audit_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="models"},indent=2))
