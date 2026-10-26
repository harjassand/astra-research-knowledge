#!/usr/local/bin/python3
"""Finite-duration positive pulses for the two-Laplace-point construction.

No physical measurements; exact modal calculations in the synthetic fixtures.
The bias bound is proved for the full model class in PROOF_STAGE2.md.
"""
import sys
sys.dont_write_bytecode=True
import csv,json,math
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from stress_and_completion import self_calibrate


def main():
    raw=json.loads((HERE/'self_calibration_data.json').read_text())
    fixtures=[f for f in raw if f['noise_rel']==0]
    rows=[];tau=.25;Q=tau
    for f in fixtures:
        k=np.array(f['K']);c=np.array(f['C_diagonal']);h=np.array(f['gains'])
        n=len(k); commands=np.array(f['commands']);ss=np.array(f['s']);m=len(ss)//2
        for horizon in (4.,8.,16.,32.):
            observed=[];biases=[];bounds=[]
            for s,command in zip(ss,commands):
                loaded=k+np.diag(command*h)
                normal=loaded/np.sqrt(c[:,None]*c[None,:])
                lam,v=np.linalg.eigh(normal)
                weights=v[0]**2/c[0]
                exact=float(np.sum(weights/(lam+s)))
                laplace_input=-math.expm1(-s*tau)/s
                tail=float(np.sum(weights*(np.exp(-(s+lam)*horizon+lam*tau)
                                           -np.exp(-(s+lam)*horizon))/(lam*(s+lam))))
                bias=tail/laplace_input
                bound=Q*math.exp(-s*horizon)/(s*c[0]*laplace_input)
                assert 0<=bias<=bound*(1+1e-12)
                observed.append(exact-bias);biases.append(bias);bounds.append(bound)
            failure='';physical=False
            try:
                kh,hh=self_calibrate(np.array(observed[:m]),np.array(observed[m:]),c)
                errk=float(np.linalg.norm(kh-k)/np.linalg.norm(k))
                errh=float(np.linalg.norm(hh-h)/np.linalg.norm(h))
                off=kh-np.diag(np.diag(kh))
                physical=bool(np.max(off)<=1e-9 and np.min(kh.sum(axis=1))>=-1e-9
                              and np.linalg.eigvalsh(kh)[0]>0)
            except (ValueError,np.linalg.LinAlgError) as exc:
                errk=errh=None;failure=str(exc)
            rows.append({'fixture':f['fixture'],'n':n,'kind':f['kind'],
                         'pulse_amplitude':1.,'pulse_duration':tau,'observation_horizon':horizon,
                         'independent_configurations':len(ss),
                         'max_actual_truncation_bias':max(biases),
                         'max_proven_truncation_bound':max(bounds),
                         'reconstructed_K_relative_error':errk,'gain_relative_error':errh,
                         'direct_physical':physical,'failure':failure})
    with (HERE/'finite_pulse_acquisition.csv').open('w',newline='') as out:
        w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps({'finite_pulse_cases':len(rows),'all_truncation_bounds_passed':True,
                      'returned_physical_reconstructions':sum(r['direct_physical'] for r in rows)},indent=2))


if __name__=='__main__':main()
