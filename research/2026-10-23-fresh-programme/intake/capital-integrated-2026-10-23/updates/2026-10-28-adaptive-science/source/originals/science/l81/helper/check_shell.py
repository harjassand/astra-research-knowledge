#!/usr/bin/env python3
"""Diagnostics only; full proof in CHALLENGE.md. Legal endpoint queries for sin."""
import csv,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(8102713)
TAU=ETA=1/math.sqrt(2)
V=(1-math.exp(-2))/2

def q(t): return math.exp(-1)*np.cosh(t)
def r(t): return (1+2*math.exp(-2)+math.exp(-4)*np.cosh(4*t))/4

def heat(c,s,v):
    norm=np.linalg.norm(v,axis=1)
    u=np.divide(v,norm[:,None],out=np.zeros_like(v),where=norm[:,None]!=0)
    xi=rng.normal(size=v.shape)
    zperp=xi-np.sum(xi*u,axis=1)[:,None]*u
    rad=s*np.linalg.norm(rng.normal(size=(len(v),3)),axis=1)
    plus=np.sin(c+s[:,None]*zperp+rad[:,None]*u)
    minus=np.sin(c+s[:,None]*zperp-rad[:,None]*u)
    scale=np.divide(norm,2*rad,out=np.zeros_like(norm),where=rad!=0)
    return scale[:,None]*(plus-minus),np.cos(c+s[:,None]*xi)

def covaction(z):
    t=rng.uniform(size=len(z)); c=np.sqrt(t)[:,None]*rng.normal(size=z.shape)
    s=np.sqrt(1-t); j1,d1=heat(c,s,z); j2,d2=heat(c,s,j1)
    return j2,t,z*d1*d2

rows=[]
for d in [128,512,2048,8192,32768]:
    errors=[]; maxs=[]; cres=[]
    for _ in range(16):
        z=rng.normal(size=(8,d)); j,t,jtilde=covaction(z)
        errors.extend(np.sum((j-jtilde)**2,axis=1)); maxs.extend(np.max(z*z,axis=1))
        cres.extend(np.sum(z*j,axis=1)/d-q(t))
    rows.append(dict(d=d,replicates=128,mean_l2_error_squared=float(np.mean(errors)),mean_max_z_squared=float(np.mean(maxs)),conditional_cross_rmse=float(np.sqrt(np.mean(np.array(cres)**2))),mean_l2_error_squared_per_coordinate=float(np.mean(errors)/d)))
with (ROOT/'action_checks.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
print(json.dumps({'action_checks':rows},indent=2),flush=True)

shell=[]
for d in [512,2048,8192,32768,131072,262144]:
    n=8; reps=256; stats=[]; targets=[]; preds=[]
    for start in range(0,reps,4):
        b=min(4,reps-start); avg=np.zeros((b,d))
        for _ in range(n): avg+=np.sin(rng.normal(size=(b,d)))/n
        z=rng.normal(size=(b,d)); w=rng.normal(size=(b,d)); j,t,_=covaction(z)
        y=avg+TAU*z-j/(2*TAU*n)+ETA*w
        stats.extend(n*(np.mean(y*y,axis=1)-1)); target=rng.normal(size=(b,d))
        targets.extend(n*(np.mean(target*target,axis=1)-1))
        preds.extend(V-q(t)+r(t)/(4*TAU*TAU*n))
    stats=np.array(stats); targets=np.array(targets); preds=np.array(preds)
    band=2*n*math.sqrt(2/d); cp=float(np.mean(np.abs(stats)>band)); tp=float(np.mean(np.abs(targets)>band))
    row=dict(d=d,n=n,m=1,replicates=reps,scaled_shell_target_band=band,candidate_outside_probability=cp,target_outside_probability=tp,empirical_tv_lower_bound=max(0,cp-tp),scaled_shell_prediction_rmse=float(np.sqrt(np.mean((stats-preds)**2))),scaled_shell_correlation=float(np.corrcoef(stats,preds)[0,1]),scaled_shell_mean=float(np.mean(stats)),predicted_scaled_shell_mean=float(np.mean(preds)))
    shell.append(row); print(json.dumps(row),flush=True)
with (ROOT/'shell_checks.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(shell[0])); writer.writeheader(); writer.writerows(shell)
summary={'seed':8102713,'sigma':1,'tau':TAU,'eta':ETA,'v':V,'action_checks':rows,'shell_checks':shell,'scope':'Diagnostics of a proved single-action obstruction; frequencies do not certify TV upper bounds.'}
(ROOT/'diagnostic_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
