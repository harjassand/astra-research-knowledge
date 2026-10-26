#!/usr/local/bin/python3
"""Stage2: withheld dynamic stress and a conditional self-calibration route.

Fixed seeds/families below were chosen before executing stage2. All cases are
reported. Stage1 is imported read-only with bytecode creation disabled.
"""
import sys
sys.dont_write_bytecode = True
import csv
import hashlib
import json
import math
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import least_squares

HERE = Path(__file__).resolve().parent
STAGE1 = HERE.parent / "stage1"
sys.path.insert(0,str(STAGE1))
from tomography import (design, reconstruct, exact_reconstruct, fraction_inverse,
                        rational_sqrt, edge_list, matrix_from_parameters)


def network(n, kind, rng, integer=False):
    edges=[]
    for i,j in edge_list(n):
        if kind == "cycle": yes = (j == i+1 or (i==0 and j==n-1))
        elif kind == "bipartite": yes = (i<n//2 <=j)
        elif kind == "ladder": yes = (j==i+2 or (i%2==0 and j==i+1))
        elif kind == "two_cliques":
            yes = (j<n//2 or i>=n//2 or (i==n//2-1 and j==n//2))
        elif kind == "path": yes = j==i+1
        else: raise ValueError(kind)
        if yes: edges.append((i,j))
    if integer:
        k=np.diag(rng.integers(1,4,n))
        for i,j in edges:
            w=int(rng.integers(1,4))
            k[i,i]+=w; k[j,j]+=w; k[i,j]=k[j,i]=-w
        c=rng.integers(1,5,n)
    else:
        k=np.diag(rng.uniform(.2,2.,n))
        for i,j in edges:
            w=float(rng.uniform(.2,2.))
            k[i,i]+=w; k[j,j]+=w; k[i,j]=k[j,i]=-w
        c=rng.uniform(.3,3.,n)
    return k,c


def write_csv(name,rows):
    with (HERE/name).open("w",newline="") as out:
        w=csv.DictWriter(out,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def scalar_and_difference(k,c,load,omega,v,delta=1.):
    r=np.linalg.inv(k+np.diag(load)+1j*omega*np.diag(c))
    difference=delta*r[0,v]*r[v,0]/(1+delta*r[v,v])
    return r[0,0],difference


def gaussian_kl(f0,diff,constant_var,thermal_factor):
    f1=f0-diff
    var1=constant_var+thermal_factor*f1
    q=thermal_factor*diff/var1
    covterm=(q*q/2-q**3/3+q**4/4) if q<1e-4 else q-math.log1p(q)
    return .5*(covterm+diff*diff/var1)


def frequency_and_noise_stress():
    rng=np.random.default_rng(2026102602)
    rows=[]; raw=[]
    omega=np.r_[0.,np.logspace(-4,3,80)]
    for n in (6,10,14,18,24):
        for kind in ("cycle","bipartite","ladder","two_cliques","path"):
            k,c=network(n,kind,rng)
            v=n-1
            f0,d0=scalar_and_difference(k,c,np.zeros(n),0,v)
            f0,d0=float(f0.real),float(d0.real)
            loads=np.r_[np.zeros((1,n)),rng.exponential(1.,(7,n))]
            max_dynamic_ratio=0.; largest_loaded_dc_ratio=0.
            largest_kl_ratios=[0.,0.,0.]
            for di,d in enumerate(loads):
                fd,dd=scalar_and_difference(k,c,d,0,v)
                fd,dd=float(fd.real),float(dd.real)
                if di: largest_loaded_dc_ratio=max(largest_loaded_dc_ratio,dd/d0)
                for j,(a,b) in enumerate(((1.,0.),(0.,1.),(.01,.1))):
                    kl=gaussian_kl(fd,dd,a,b)
                    kl0=gaussian_kl(f0,d0,a,b)
                    largest_kl_ratios[j]=max(largest_kl_ratios[j],kl/kl0)
                for w in omega:
                    _,dw=scalar_and_difference(k,c,d,w,v)
                    max_dynamic_ratio=max(max_dynamic_ratio,float(abs(dw)/d0))
            assert max_dynamic_ratio <= 1+1e-10
            assert all(r<=1+1e-10 for r in largest_kl_ratios)
            rows.append({"n":n,"kind":kind,"fault_node":v,"unloaded_dc_difference":d0,
                         "load_configurations":len(loads),"frequencies_per_configuration":len(omega),
                         "max_abs_dynamic_difference_divided_by_unloaded_dc":max_dynamic_ratio,
                         "max_loaded_dc_ratio":largest_loaded_dc_ratio,
                         "constant_variance_max_KL_ratio":largest_kl_ratios[0],
                         "thermal_variance_max_KL_ratio":largest_kl_ratios[1],
                         "mixed_variance_max_KL_ratio":largest_kl_ratios[2]})
            raw.append({"n":n,"kind":kind,"K":k.tolist(),"C_diagonal":c.tolist(),
                        "loads":loads.tolist(),"omega":omega.tolist()})
    write_csv("frequency_noise_stress.csv",rows)
    (HERE/"withheld_networks.json").write_text(json.dumps(raw,indent=2)+"\n")
    return rows


def interval_difference_map(k,c,d,dt,v):
    """Positive cascade, avoiding subtracting nearly equal impulse responses."""
    n=len(k)
    a0=-(k+np.diag(d))/c[:,None]
    kp=k.copy(); kp[v,v]+=1
    a1=-(kp+np.diag(d))/c[:,None]
    p=np.zeros((n,n)); p[v,v]=1/c[v]
    aug=np.zeros((2*n+1,2*n+1))
    aug[:n,:n]=a0; aug[:n,n:2*n]=p; aug[n:2*n,n:2*n]=a1
    aug[n,2*n]=1/c[0]
    prop=expm(dt*aug)
    return prop[:2*n,:2*n],prop[:2*n,-1]


def finite_operator(k,c,schedule,dt,v):
    steps=len(schedule); n=len(k)
    z=np.zeros((2*n,steps)); h=np.zeros((steps,steps)); cache={}
    for j,d in enumerate(schedule):
        key=tuple(d)
        if key not in cache: cache[key]=interval_difference_map(k,c,d,dt,v)
        a,b=cache[key]
        z=a@z; z[:,j]+=b
        h[j]=z[0]
    return h


def transient_stress():
    rng=np.random.default_rng(2026102603)
    rows=[]; raw=[]
    for n,kind in ((6,"cycle"),(10,"ladder"),(14,"two_cliques"),(18,"path")):
        k,c=network(n,kind,rng); v=n-1; steps=64; dt=.5
        _,dc=scalar_and_difference(k,c,np.zeros(n),0,v)
        dc=float(dc.real)
        h0=finite_operator(k,c,np.zeros((steps,n)),dt,v)
        u,s,vt=np.linalg.svd(h0,full_matrices=False)
        optimum=float(s[0])
        pulse=np.ones(steps)/math.sqrt(steps)
        pulse_gain=float(np.linalg.norm(h0@pulse))
        best_ratio=0.; max_entry_ratio=0.; best=None
        for _ in range(8):
            blocks=rng.exponential(1.,(8,n))
            schedule=np.repeat(blocks,8,axis=0)
            h=finite_operator(k,c,schedule,dt,v)
            # Pointwise matrix domination is stronger than a test of one pulse.
            assert np.all(h<=h0+1e-11*max(dc,1e-30))
            ratio=float(np.linalg.svd(h,compute_uv=False)[0]/optimum)
            if ratio>best_ratio: best_ratio=ratio; best=schedule.copy()
            positive=h0>0
            max_entry_ratio=max(max_entry_ratio,float(np.max(h[positive]/h0[positive])))
        assert optimum<=dc*(1+1e-11)
        rows.append({"n":n,"kind":kind,"steps":steps,"dt":dt,
                     "dc_infinite_horizon_L2_gain":dc,
                     "ordinary_optimal_finite_horizon_gain":optimum,
                     "ordinary_constant_pulse_gain":pulse_gain,
                     "finite_optimum_divided_by_dc":optimum/dc,
                     "tested_time_varying_schedules":8,
                     "best_loaded_SVD_gain_divided_by_unloaded_optimum":best_ratio,
                     "largest_loaded_entry_ratio_to_unloaded":max_entry_ratio})
        raw.append({"n":n,"kind":kind,"K":k.tolist(),"C_diagonal":c.tolist(),
                    "unloaded_operator":h0.tolist(),"optimal_input_unit_discrete_l2":vt[0].tolist(),
                    "best_tested_loaded_schedule":best.tolist()})
    write_csv("transient_stress.csv",rows)
    (HERE/"transient_data.json").write_text(json.dumps(raw,indent=2)+"\n")
    return rows


def joint_response(k,c,h,ss,commands):
    n=len(k); mats=k[None,:,:]+np.array([np.diag(s*c+u*h) for s,u in zip(ss,commands)])
    rhs=np.zeros((len(ss),n)); rhs[:,0]=1
    return np.linalg.solve(mats,rhs)[:,0]


def self_calibrate(y1,y2,c,s1=.5,s2=2.):
    n=len(c); b1=reconstruct(y1,n); b2=reconstruct(y2,n)
    slopes=np.diag(b2-b1)/(s2-s1)
    if np.any(slopes<=0): raise ValueError("nonpositive capacity/gain slope")
    h=c/slopes
    # The port normalization is fixed by the measured source and detector.
    h[0]=1.
    root=np.sqrt(h)
    k=root[:,None]*b1*root[None,:]-s1*np.diag(c)
    return k,h


def exact_self_calibration():
    rng=np.random.default_rng(2026102604); rows=[]
    s1,s2=F(1,2),F(2)
    for n in range(3,8):
        for kind in ("cycle","bipartite","two_cliques"):
            k,c=network(n,kind,rng,integer=True)
            scale=[1]+[int(v) for v in rng.integers(1,4,n-1)]
            h=[F(v*v) for v in scale]
            commands,_=design(n)
            recovered=[]
            for s in (s1,s2):
                y=[]
                for command in commands:
                    a=[[F(int(k[i,j]))+(s*F(int(c[i]))+h[i]*F(int(command[i])) if i==j else 0)
                        for j in range(n)] for i in range(n)]
                    y.append(fraction_inverse(a)[0][0])
                recovered.append(exact_reconstruct(y,n))
            b1,b2=recovered
            hh=[(s2-s1)*F(int(c[i]))/(b2[i][i]-b1[i][i]) for i in range(n)]
            assert hh==h
            sh=[rational_sqrt(v) for v in hh]
            kh=[[sh[i]*b1[i][j]*sh[j]-(s1*F(int(c[i])) if i==j else 0)
                 for j in range(n)] for i in range(n)]
            assert kh==[[F(int(v)) for v in row] for row in k]
            rows.append({"n":n,"kind":kind,"scalar_measurements":n*(n+1),
                         "known_node_capacities":True,"exact_K_equal":True,"exact_gains_equal":True})
    write_csv("exact_self_calibration.csv",rows)
    return rows


def ordinary_joint_fit(y,c,ss,commands,n,seed):
    rng=np.random.default_rng(seed); edges=edge_list(n); d=n*(n+1)//2
    rhs=np.zeros((len(y),n)); rhs[:,0]=1; norm=abs(y[0]); best=None; neval=0
    class Eval:
        last=None
        def evaluate(self,theta):
            if self.last is not None and np.array_equal(self.last,theta):return
            k=matrix_from_parameters(theta[:d],n); h=np.r_[1.,theta[d:]]
            mats=k[None,:,:]+np.array([np.diag(s*c+u*h) for s,u in zip(ss,commands)])
            v=np.linalg.solve(mats,rhs)
            self.res=(v[:,0]-y)/norm
            j=np.empty((len(y),d+n-1)); j[:,:n]=-v*v/norm
            for a,(i,l) in enumerate(edges,n):j[:,a]=-(v[:,i]-v[:,l])**2/norm
            j[:,d:]=-commands[:,1:]*v[:,1:]**2/norm
            self.jacobian=j; self.last=theta.copy()
        def fun(self,t):self.evaluate(t);return self.res
        def jac(self,t):self.evaluate(t);return self.jacobian
    begin=time.perf_counter()
    for _ in range(8):
        e=Eval(); initial=np.exp(rng.uniform(-1,1,d+n-1))
        fit=least_squares(e.fun,initial,jac=e.jac,bounds=(1e-12,np.inf),x_scale="jac",
                          max_nfev=3000,ftol=1e-13,xtol=1e-13,gtol=1e-13)
        obj=float(fit.fun@fit.fun); neval+=fit.nfev
        if best is None or obj<best[0]:best=(obj,fit.x.copy())
    return matrix_from_parameters(best[1][:d],n),np.r_[1.,best[1][d:]],{
        "ordinary_train_scaled_sse":best[0],"ordinary_total_nfev":neval,
        "ordinary_starts":8,"ordinary_seconds":time.perf_counter()-begin}


def noisy_self_calibration():
    rng=np.random.default_rng(2026102605); rows=[]; raw=[]
    for fixture,(n,kind) in enumerate(((4,"cycle"),(5,"bipartite"),(6,"ladder"),(6,"two_cliques"))):
        k,c=network(n,kind,rng); h=np.r_[1.,rng.uniform(.3,3.,n-1)]
        ds,_=design(n); commands=np.r_[ds,ds]; ss=np.r_[np.full(len(ds),.5),np.full(len(ds),2.)]
        true=joint_response(k,c,h,ss,commands)
        withheld_commands=rng.uniform(0,3.,(32,n)); withheld_commands[:,0]=0
        withheld_s=rng.uniform(.1,3.,32)
        target=joint_response(k,c,h,withheld_s,withheld_commands)
        for noise_rel in (0.,1e-7,1e-4):
            y=true+rng.normal(0,noise_rel*true[0],len(true)); failure=""
            try:
                kh,hh=self_calibrate(y[:len(ds)],y[len(ds):],c)
                errk=float(np.linalg.norm(kh-k)/np.linalg.norm(k)); errh=float(np.linalg.norm(hh-h)/np.linalg.norm(h))
                pred=joint_response(kh,c,hh,withheld_s,withheld_commands)
                prederr=float(np.linalg.norm(pred-target)/np.linalg.norm(target))
                off=kh-np.diag(np.diag(kh))
                physical=(np.max(off)<=1e-9 and np.min(kh.sum(axis=1))>=-1e-9 and np.linalg.eigvalsh(kh)[0]>0)
            except (ValueError,np.linalg.LinAlgError) as exc:
                kh=hh=None; errk=errh=prederr=None; physical=False;failure=str(exc)
            kf,hf,info=ordinary_joint_fit(y,c,ss,commands,n,2026102650+fixture)
            pred=joint_response(kf,c,hf,withheld_s,withheld_commands)
            rows.append({"fixture":fixture,"n":n,"kind":kind,"noise_rel":noise_rel,
                         "measurements_per_method":len(y),"direct_K_relative_error":errk,
                         "direct_gain_relative_error":errh,"direct_prediction_relative_error":prederr,
                         "direct_physical":bool(physical),"direct_failure":failure,
                         "ordinary_K_relative_error":float(np.linalg.norm(kf-k)/np.linalg.norm(k)),
                         "ordinary_gain_relative_error":float(np.linalg.norm(hf-h)/np.linalg.norm(h)),
                         "ordinary_prediction_relative_error":float(np.linalg.norm(pred-target)/np.linalg.norm(target)),**info})
            raw.append({"fixture":fixture,"kind":kind,"noise_rel":noise_rel,"K":k.tolist(),
                        "C_diagonal":c.tolist(),"gains":h.tolist(),"commands":commands.tolist(),
                        "s":ss.tolist(),"observations":y.tolist(),"noise_free":true.tolist(),
                        "direct_K":None if kh is None else kh.tolist(),
                        "direct_gains":None if hh is None else hh.tolist(),
                        "ordinary_K":kf.tolist(),"ordinary_gains":hf.tolist(),
                        "withheld_commands":withheld_commands.tolist(),"withheld_s":withheld_s.tolist()})
    write_csv("self_calibration_comparison.csv",rows)
    (HERE/"self_calibration_data.json").write_text(json.dumps(raw,indent=2)+"\n")
    return rows


def main():
    started=time.perf_counter()
    freq=frequency_and_noise_stress()
    transient=transient_stress()
    exact=exact_self_calibration()
    calibration=noisy_self_calibration()
    expected=json.loads((HERE/"stage1_frozen_sha256.json").read_text())
    actual={str(p.relative_to(STAGE1)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in STAGE1.rglob('*') if p.is_file()}
    assert expected==actual,"stage1 changed"
    summary={"withheld_dynamic_networks":len(freq),"frequency_load_pairs":len(freq)*8*81,
             "noise_KL_load_models":len(freq)*8*3,"finite_horizon_cases":len(transient),
             "loaded_time_varying_schedules":len(transient)*8,
             "exact_self_calibration_cases":len(exact),"exact_self_calibration_passed":len(exact),
             "noisy_comparison_cases":len(calibration),"stage1_sha256_unchanged":True,
             "stage1_files_checked":len(actual),"elapsed_seconds":time.perf_counter()-started}
    (HERE/"run_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))


if __name__=="__main__":main()
