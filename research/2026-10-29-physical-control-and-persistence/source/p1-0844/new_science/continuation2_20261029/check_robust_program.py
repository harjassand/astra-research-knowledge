#!/usr/bin/env python3
"""Synthetic readouts plus exact fitted-kernel/receiver checks; no apparatus test."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, math
import numpy as np

ROOT=Path(__file__).resolve().parent
D,N,BITS,BETA=4,100000,16,F(1,100)
H=(F(-1),F(-1,3),F(1,3),F(1))
START=(1,0,1,0)
SEED=2026102902
STATES=list(product((0,1),repeat=D))
INDEX={x:i for i,x in enumerate(STATES)}
S=F(9,20)

def fs(x): return f'{x.numerator}/{x.denominator}'
def clip(x,a,b): return min(b,max(a,x))
def round_key(w):
    z=w*(2**BITS)+F(1,2)
    return F(z.numerator//z.denominator,2**BITS)
def solve(a,b):
    a=[list(row)+[rhs] for row,rhs in zip(a,b)]; n=len(a)
    for j in range(n):
        p=next(i for i in range(j,n) if a[i][j]); a[p],a[j]=a[j],a[p]
        z=a[j][j]; a[j]=[v/z for v in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                z=a[i][j]; a[i]=[v-z*w for v,w in zip(a[i],a[j])]
    return [row[-1] for row in a]
def target(x,i):
    p=(F(3,8),F(1,2),F(5,8))[x[(i-1)%D]+x[(i+1)%D]]
    return S*(p if x[i]==0 else 1-p)
def matrix(flips):
    out=[[F(0)]*len(STATES) for _ in STATES]
    for a,x in enumerate(STATES):
        for i,p in enumerate(flips[a]):
            y=list(x); y[i]^=1
            out[a][INDEX[tuple(y)]]+=p/D; out[a][a]+=(1-p)/D
    return out

def main():
    rng=np.random.default_rng(SEED)
    packed={}; calibration=[]; estimated=[]; true=[]; post=list(START)
    for i,h in enumerate(H):
        p0,p3=F(1,10)+h/20,F(7,20)+h/10; true.append((p0,p3)); counts=[]
        for j,p in ((0,p0),(3,p3)):
            bits=rng.binomial(1,float(p),size=N).astype(np.uint8)
            key=f'site_{i}_mode_{j}'; packed[key]=np.packbits(bits,bitorder='little')
            count=int(bits.sum()); counts.append(count); post[i]^=count%2
            calibration.append({'site':i,'mode':j,'trials':N,'flips':count,
                'packed_sha256':hashlib.sha256(packed[key].tobytes()).hexdigest()})
        estimated.append((clip(F(counts[0],N),F(1,20),F(3,20)),
                          clip(F(counts[1],N),F(1,4),F(9,20))))
    np.savez_compressed(ROOT/'SYNTHETIC_CALIBRATION_READOUTS.npz',**packed)
    eta=math.sqrt(math.log(4*D/float(BETA))/(2*N))
    rawerr=max(abs(t-e) for tr,er in zip(true,estimated) for t,e in zip(tr,er))
    assert float(rawerr)<=eta
    ideal=[]; actual=[]; rows=[]; rowerr=F(0); keyerr=F(0)
    for x in STATES:
        fi=[]; fa=[]
        for i in range(D):
            c=target(x,i); q0,q3=estimated[i]; r=2*q3*(1-q3)
            w=(r-c)/(r-q0); assert 0<=w<=1; wd=round_key(w)
            p0,p3=true[i]; p=wd*p0+(1-wd)*2*p3*(1-p3)
            rowerr=max(rowerr,abs(p-c)); keyerr=max(keyerr,abs(wd-w))
            fi.append(c); fa.append(p)
            rows.append({'state':''.join(map(str,x)),'site':i,'target_flip':fs(c),
                'low_word_dyadic_numerator':int(wd*2**BITS),'actual_flip':fs(p)})
        ideal.append(fi); actual.append(fa)
    assert keyerr<=F(1,2**(BITS+1)) and float(rowerr)<=eta+2**(-BITS)
    P,R=matrix(ideal),matrix(actual); k=len(STATES)
    assert all(sum(r)==1 and min(r)>=0 for r in R)
    wt=[F(5,3)**(sum(x[i]==x[(i+1)%D] for i in range(D))//2) for x in STATES]
    pi=[w/sum(wt) for w in wt]
    a=[[R[j][i]-(1 if i==j else 0) for j in range(k)] for i in range(k-1)]+[[F(1)]*k]
    mu=solve(a,[F(0)]*(k-1)+[F(1)])
    assert sum(mu)==1 and min(mu)>0
    assert [sum(mu[i]*R[i][j] for i in range(k)) for j in range(k)]==mu
    assert [sum(pi[i]*P[i][j] for i in range(k)) for j in range(k)]==pi
    rho=1-F(27,80*D); maxratio=F(0); pairs=0; means=0
    for aidx,x in enumerate(STATES):
        for bidx,y in enumerate(STATES):
            dist=sum(u!=v for u,v in zip(x,y)); expected=F(0)
            for i in range(D):
                px=ideal[aidx][i] if x[i]==0 else 1-ideal[aidx][i]
                py=ideal[bidx][i] if y[i]==0 else 1-ideal[bidx][i]
                expected+=(dist-(x[i]!=y[i])+abs(px-py))/D
            assert expected<=rho*dist
            if dist: maxratio=max(maxratio,expected/dist)
            pairs+=1
        for i in range(D):
            observed=sum(P[aidx][j]*(2*y[i]-1) for j,y in enumerate(STATES))
            predicted=(1-S/D)*(2*x[i]-1)+S/(8*D)*((2*x[(i-1)%D]-1)+(2*x[(i+1)%D]-1))
            assert observed==predicted; means+=1
    assert maxratio==rho
    mag=[F(sum(2*z-1 for z in x),D) for x in STATES]
    bond=[F(sum((2*x[i]-1)*(2*x[(i+1)%D]-1) for i in range(D)),D) for x in STATES]
    tv=sum(abs(p-q) for p,q in zip(mu,pi))/2
    em=abs(sum((p-q)*f for p,q,f in zip(mu,pi,mag)))
    ec=abs(sum((p-q)*f for p,q,f in zip(mu,pi,bond)))
    delta=eta+2**(-BITS); floor=80*delta/27; joint=min(1,floor+float(BETA))
    va=np.zeros(k); vr=np.zeros(k); va[INDEX[tuple(post)]]=vr[INDEX[tuple(post)]]=1
    pn,rn=np.array(P,dtype=float),np.array(R,dtype=float)
    fm,fc=np.array(mag,dtype=float),np.array(bond,dtype=float)
    maxima={'magnetization':0.,'bond_correlation':0.}; samples=[]
    for t in range(1001):
        dm,dc=abs(float((va-vr)@fm)),abs(float((va-vr)@fc))
        maxima['magnetization']=max(maxima['magnetization'],dm)
        maxima['bond_correlation']=max(maxima['bond_correlation'],dc)
        if t in (0,1,10,100,1000): samples.append({'macrostep':t,'magnetization_error':dm,'bond_error':dc})
        va,vr=va@rn,vr@pn
    assert maxima['magnetization']<=2*floor and maxima['bond_correlation']<=4*floor
    assert float(ec)<=4*floor
    out={'scope':'Synthetic native readouts; ideal static-H model; no physical experiment',
        'seed':SEED,'sites':D,'trials_per_site_per_mode':N,'beta':fs(BETA),'selector_bits':BITS,
        'native_calibration_calls':2*D*N,'native_calibration_label_reads':D*(2*N+1),
        'persistent_devices':D,'independent_hidden_resets':0,'initial_visible_state':START,
        'post_calibration_visible_state':post,'calibration':calibration,'eta_display_float':eta,
        'max_true_raw_estimation_error':fs(rawerr),'max_true_macro_row_error':fs(rowerr),
        'certified_macro_row_error_display_float':delta,'good_event_metric_floor':floor,
        'joint_metric_floor_with_failure_charge':joint,
        'all_deterministic_times_magnetization_bound':2*joint,
        'all_deterministic_times_bond_bound':min(2,4*floor+2*float(BETA)),
        'bond_failure_charge_uses_oscillation_2':True,'contraction_pair_checks':pairs,
        'exact_attained_contraction':fs(maxratio),'mean_equation_checks':means,
        'stationary_tv_exact':fs(tv),'stationary_tv_display_float':float(tv),
        'stationary_magnetization_error_exact':fs(em),'stationary_bond_error_exact':fs(ec),
        'stationary_bond_error_display_float':float(ec),'transient_max_through_1000':maxima,
        'transient_samples':samples,'deployment_native_calls_per_macro':[1,2],
        'fresh_fair_bits_per_macro_excluding_site_choice':BITS,'four_site_scan_extra_bits':2,
        'assumed_physical_implementation_error':0,'native_implementation_table':rows,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'ROBUST_PROGRAM_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    keys=['native_calibration_calls','eta_display_float','max_true_macro_row_error',
          'all_deterministic_times_magnetization_bound','all_deterministic_times_bond_bound',
          'stationary_tv_display_float','stationary_bond_error_display_float',
          'transient_max_through_1000','script_sha256']
    print(json.dumps({key:out[key] for key in keys},indent=2))

if __name__=='__main__': main()
