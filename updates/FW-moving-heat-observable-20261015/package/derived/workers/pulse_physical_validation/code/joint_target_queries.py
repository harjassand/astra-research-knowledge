"""Same-information target queries for the joint LP comparator.

Finite-grid extrema are exploratory, not continuum outer certificates. Every
returned finite model is a numerical feasibility witness; noise margins are
not established physical error budgets. Pulse error 2.6/3/5mV are sensitivity
choices, not a measured bound on material discrepancy.
"""
from pathlib import Path
import json,sys,time
import numpy as np
from scipy.optimize import linprog
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]/'sources/astra_pulse_observable/code'))
from compact_model import target

def main():
    start=time.perf_counter(); rows=[]
    for which,budgets in [('pos',[.5,1.]),('both',[2.6,3.,5.])]:
        d=np.load(BASE/f'results/joint_lp_{which}_n1200_f1000_witness.npz',allow_pickle=True)
        s,A,y,B,v=(d[k] for k in ['s','F','y','B','v'])
        # 1e-5 mOhm interior guard for numerical witness residual verification.
        eps=.1-1e-5
        AA=np.r_[A,-A]; bb=np.r_[y+eps,-y+eps]
        for e in budgets:
            C=np.r_[np.column_stack([AA,np.zeros(len(AA))]),
                      np.column_stack([B,-(v+e)]),np.column_stack([-B,v-e])]
            b=np.r_[bb,np.zeros(2*len(v))]
            bounds=[(0,None)]*(A.shape[1]-1)+[(None,None),(1e-4,100)]
            q=np.r_[target(s,1000),0.,0.]
            result=[]
            for direction in [1,-1]:
                r=linprog(direction*q,A_ub=C,b_ub=b,bounds=bounds,method='highs-ds',
                          options={'primal_feasibility_tolerance':1e-8,'dual_feasibility_tolerance':1e-8})
                if not r.success:
                    result.append({'status':r.message}); continue
                coef=r.x[:-1]; rho=r.x[-1]
                result.append({'objective_Q1000_mOhm':float(q@r.x),
                    'fitted_amplitude_A':float(1/rho),
                    'EIS_max_component_error_mOhm':float(abs(A@coef-y).max()),
                    'pulse_max_error_mV':float(abs(B@coef/rho-v).max())})
                np.savez_compressed(BASE/f'results/query_{which}_e{e}_{direction}_witness.npz',
                                    s=s,coef=coef,rho=rho)
            rows.append({'which':which,'pulse_budget_mV':e,
                         'finite_grid_extrema':result,'continuum_outer_bound':False,
                         'physical_validation':False})
            print(json.dumps(rows[-1]),flush=True)
    (BASE/'results/joint_target_queries.json').write_text(json.dumps({'runs':rows,
        'elapsed_s':time.perf_counter()-start,
        'meaning':'Matched joint-domain access can remove much of the long-horizon EIS-only ambiguity conditionally, but the 92-cell model gate fails and none of these pulse discrepancy budgets was validated.'},indent=2))

if __name__=='__main__':main()
