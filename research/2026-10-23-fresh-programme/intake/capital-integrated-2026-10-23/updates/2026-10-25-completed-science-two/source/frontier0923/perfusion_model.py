#!/usr/bin/env python3
"""Synthetic discrimination of local oxygen-responsive perfusate rheology.

No parameters here are fitted to an organ or a measured candidate fluid.
The ideal two-state material is a hypothetical constitutive interface.
Run: python3 perfusion_model.py
"""
from pathlib import Path
import csv
import json
import math
import numpy as np

OUT = Path(__file__).resolve().parent
CA, K, CV_MIN = 1.0, 0.05, 0.20


def exposure(c):
    return CA-c+K*np.log(CA/c)


def cv_from_exposure(z):
    """Bisection in log(c), robust for near-anoxic branches."""
    z = np.asarray(z)
    lo, hi = -np.maximum(2.0*z/K, 10.0), np.zeros_like(z)
    for _ in range(65):
        mid = (lo+hi)/2
        zm = CA-np.exp(mid)-K*mid
        lo = np.where(zm > z, mid, lo)
        hi = np.where(zm > z, hi, mid)
    return np.exp((lo+hi)/2)


def flows(p, r, m, gamma, cstar):
    """Exact positive root of p/r=q+(gamma-1)zstar*q^2/m.

    All-high-state branches instead have q=p/(r*gamma).
    """
    zstar = float(exposure(cstar))
    a = (gamma-1)*zstar/m
    v = p/r
    q = 2*v/(1+np.sqrt(1+4*a*v))
    return np.where(p >= r*gamma*m/zstar, v/gamma, q)


def hydraulic(q, r, m, gamma, cstar):
    alpha = np.minimum(1.0, float(exposure(cstar))*q/m)
    avmu = 1+(gamma-1)*alpha
    p = r*q*avmu
    # Pressure mean along the idealized extraction bed, relative to outlet.
    pmean = r*q*(1+(gamma-1)*alpha**2)/2
    elasticity = np.where(alpha < 1, 1+(gamma-1)*alpha/avmu, 1.0)
    return p, pmean, elasticity


def pressure_for_flow(qtot, r, m, gamma, cstar):
    lo, hi = 0.0, max(1.0, qtot/np.sum(1/r))*gamma
    for _ in range(65):
        mid = (lo+hi)/2
        if np.sum(flows(mid,r,m,gamma,cstar)) < qtot:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def operating_point(r, m, gamma, cstar, qmax, pmax, wmax, feeder_r=0.0):
    """Maximize p subject to simultaneous Q, total P, and hydraulic power caps.

    The feeder is oxygenated, hence has the high-state viscosity gamma.
    The independent variable p is the common pressure across extraction beds.
    """
    lo, hi = 0.0, min(pmax, pressure_for_flow(qmax,r,m,gamma,cstar))
    for _ in range(58):
        mid = (lo+hi)/2
        q = flows(mid,r,m,gamma,cstar)
        qt = float(q.sum())
        pt = mid+feeder_r*gamma*qt
        if pt > pmax or pt*qt > wmax:
            hi = mid
        else:
            lo = mid
    p = (lo+hi)/2
    q = flows(p,r,m,gamma,cstar)
    qt = float(q.sum())
    pt = p+feeder_r*gamma*qt
    cv = cv_from_exposure(m/q)
    ratio = q*float(exposure(CV_MIN))/m
    pbranch, pmean, elast = hydraulic(q,r,m,gamma,cstar)
    assert np.max(np.abs(pbranch-p)) < 1e-8*max(1.0,p)
    return dict(gamma=float(gamma),cstar=float(cstar),p_bed=float(p),
                p_total=float(pt),q_total=qt,power=float(pt*qt),
                adequate_fraction=float(np.mean(cv>=CV_MIN)),
                adequate_demand_fraction=float(m[cv>=CV_MIN].sum()/m.sum()),
                relative_supply_p05=float(np.quantile(ratio,.05)),
                relative_supply_p50=float(np.quantile(ratio,.50)),
                relative_supply_p95=float(np.quantile(ratio,.95)),
                extraction=float(np.sum(q*(CA-cv))),
                mean_bed_pressure=float(np.mean(pmean)),
                max_bed_pressure_mean=float(np.max(pmean)),
                elasticity_min=float(elast.min()),elasticity_max=float(elast.max()))


def audit(seed=734911):
    rng=np.random.default_rng(seed)
    r=np.exp(rng.normal(0,1.2,2000))
    m=np.exp(rng.normal(0,.45,2000))
    q=np.exp(rng.normal(0,2.0,2000))
    max_root_error=max_elasticity_error=0.0
    for gamma in [1,1.01,2,5,20,100]:
        for cs in [.21,.50,.80,.97]:
            p,_,ee=hydraulic(q,r,m,gamma,cs)
            qq=flows(p,r,m,gamma,cs)
            max_root_error=max(max_root_error,float(np.max(np.abs(qq/q-1))))
            assert np.all(ee>=1-1e-12) and np.all(ee<=2+1e-12)
            pp,_,_=hydraulic(q*(1+1e-6),r,m,gamma,cs)
            pm,_,_=hydraulic(q/(1+1e-6),r,m,gamma,cs)
            en=(np.log(pp)-np.log(pm))/(2*np.log1p(1e-6))
            # Exclude nondifferentiable switch crossover.
            alpha=exposure(cs)*q/m
            mask=np.abs(alpha-1)>1e-4
            max_elasticity_error=max(max_elasticity_error,float(np.max(np.abs(en[mask]-ee[mask]))))
    assert max_root_error<1e-12 and max_elasticity_error<2e-8
    # Broad smooth nonmonotone nonnegative laws: the universal E<=2
    # survives even though the lower E>=1 need not.
    zz=np.linspace(0,6,100001)
    laws=[1+4*np.exp(-zz),.02+10*np.exp(-((zz-.8)/.1)**2),
          1+3*(1+np.sin(6*zz)),.01+5/(1+np.exp(15*(zz-.3)))]
    univ=[]
    for g in laws:
        integ=np.concatenate([[0],np.cumsum((g[:-1]+g[1:])*np.diff(zz)/2)])
        take=np.arange(10,len(zz),83)
        e=zz[take]
        ee=2-g[take]/(integ[take]/e)
        assert ee.max()<=2+1e-12
        univ.append([float(ee.min()),float(ee.max())])
    # Fick/uptake coordinate inversion check away from underflow.
    cc=np.geomspace(1e-9,1,2000)
    inverse_err=float(np.max(np.abs(cv_from_exposure(exposure(cc))/cc-1)))
    assert inverse_err<1e-12
    return dict(seed=seed,random_branch_cases=48000,
                max_exact_root_relative_error=max_root_error,
                max_finite_difference_elasticity_error=max_elasticity_error,
                nonmonotone_law_elasticity_ranges=univ,
                uptake_coordinate_inverse_relative_error=inverse_err)


def main():
    rng=np.random.default_rng(20261025)
    n=1024
    z1,z2=rng.normal(size=(2,n))
    cases={
        'lognormal_independent':(np.exp(1.2*z1),np.exp(.45*z2)),
        'demand_correlated_with_resistance':(np.exp(1.2*z1),np.exp(.45*(.8*z1+.6*z2))),
        'demand_anticorrelated_with_resistance':(np.exp(1.2*z1),np.exp(.45*(-.8*z1+.6*z2))),
        'two_path_100_fold_resistance':(np.array([1.0,100.0]),np.array([1.0,1.0]))}
    rows=[]
    for name,(r,m) in cases.items():
        # Normalize mean M solely for dimensionless comparison.
        m=m/m.mean()
        qmax=1.25*float(np.sum(m)/exposure(CV_MIN))
        p0=qmax/np.sum(1/r)
        for feeder_fraction in [0.0,.25,1.0]:
            ra=feeder_fraction*p0/qmax
            pt0=p0+ra*qmax
            contracts={
                'same_pressure':(10*qmax,pt0,math.inf),
                'same_flow_pressure_x2':(qmax,2*pt0,math.inf),
                'same_flow_pressure_x4':(qmax,4*pt0,math.inf),
                'same_flow_and_power':(qmax,4*pt0,pt0*qmax)}
            for contract,(qc,pc,wc) in contracts.items():
                for gamma in [1,1.5,2,3,5,10,30,100]:
                    for cs in [.25,.4,.6,.8,.95]:
                        res=operating_point(r,m,gamma,cs,qc,pc,wc,ra)
                        res.update(case=name,contract=contract,
                                   feeder_fraction=feeder_fraction,
                                   qmax=float(qc),pmax=float(pc),
                                   wmax=None if math.isinf(wc) else float(wc),
                                   reference_pressure=float(pt0),
                                   reference_flow=float(qmax),
                                   pressure_ratio=float(res['p_total']/pt0),
                                   flow_ratio=float(res['q_total']/qmax),
                                   power_ratio=float(res['power']/(pt0*qmax)))
                        rows.append(res)
    fields=list(rows[0])
    with (OUT/'synthetic_budget_sweep.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    checks=audit()
    # Explicit two-path point at Q=2.5 q_target, no feeder; severe path
    # must remain at least tenfold below the other path by the theorem.
    rr,mm=cases['two_path_100_fold_resistance']
    qqmax=1.25*float(np.sum(mm)/exposure(CV_MIN))
    explicit=[]
    for gamma in [1,2,5,10,100,10000]:
        p=pressure_for_flow(qqmax,rr,mm,gamma,.8)
        q=flows(p,rr,mm,gamma,.8)
        explicit.append(dict(gamma=gamma,q=q.tolist(),flow_ratio=float(q[0]/q[1]),p=float(p)))
        assert q[0]/q[1]>=10-1e-8
    summary=dict(model='synthetic; no organ data; ideal unbuilt material',
                 constants=dict(inlet_oxygen=CA,uptake_half_scale=K,
                                minimum_outlet_oxygen=CV_MIN,seed=20261025),
                 checks=checks,two_path_fixed_flow=explicit,row_count=len(rows))
    (OUT/'numerical_checks.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    print('\nBest adequate fraction at no shared feeder, each contract:')
    for name in cases:
        for contract in ['same_pressure','same_flow_pressure_x2','same_flow_pressure_x4','same_flow_and_power']:
            sub=[v for v in rows if v['case']==name and v['contract']==contract and v['feeder_fraction']==0]
            base=next(v for v in sub if v['gamma']==1)
            best=max(sub,key=lambda v:(v['adequate_fraction'],-v['power']))
            print(name,contract,'baseline',round(base['adequate_fraction'],4),
                  'best',round(best['adequate_fraction'],4),'gamma',best['gamma'],
                  'cstar',best['cstar'],'pressure',round(best['pressure_ratio'],3),
                  'flow',round(best['flow_ratio'],3),'power',round(best['power_ratio'],3))


if __name__=='__main__':
    main()
