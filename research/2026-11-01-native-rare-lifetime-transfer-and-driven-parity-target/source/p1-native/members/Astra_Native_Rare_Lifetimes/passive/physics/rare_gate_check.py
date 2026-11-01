"""Exact-arithmetic rare-boundary obstruction; independent small dense checks."""
from fractions import Fraction as F
from math import comb, exp, log, pi
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh, expm

OUT = Path(__file__).resolve().parent

def exact_mean(m, kappa):
    p = F(1, 2**m)
    b = 1-p
    tail = F(0)
    total = F(0)
    for j in range(m, 0, -1):
        tail += F(comb(m,j), 2**m)
        conductance = F(j*comb(m,j), 2**m)
        if j == 1:
            conductance *= kappa
        total += tail*tail/conductance
    return total/b

def exp_error(m, mean):
    p = 2.0**(-m)
    b = 1-p
    delta = 1/(2*b*float(mean))
    d = (4*delta/pi)*log(1+1/(4*delta*delta))+48*delta/pi
    return (d+p)/b

exact_bounds=[]
for m in range(6,129):
    b=F(2**m-1,2**m)
    m1=exact_mean(m,F(1))
    spectral=sum((F(comb(m,j),2*j) for j in range(1,m+1)),F(0))/b
    assert m1==spectral
    leading=F(2**m,m)*b
    remainder=m1-leading
    r=remainder/leading
    upper=(1+F(2,m))/(b*b)-1
    assert 0<=r<=upper
    m2=exact_mean(m,F(2))
    assert m2==leading/2+remainder
    assert m1/m2 >= (1+upper)/(F(1,2)+upper)
    if m in (8,16,32,48,64,96,128):
        tv=min(1.,float(F(2*m*10**6,2**m)/b))
        ratio=float(m1/m2)
        deadline_sep=exp(-1)-exp(-ratio)-exp_error(m,m1)-exp_error(m,m2)
        exact_bounds.append({
            'fixed_bits':m,'target_mass':2.**(-m),
            'base_mean':float(m1),'modified_mean':float(m2),
            'mean_ratio':ratio,'ratio_lower_bound':float((1+upper)/(F(1,2)+upper)),
            'path_tv_bound_at_observation_time_1000000':tv,
            'deadline_cdf_separation_lower_bound_at_b_times_base_mean':deadline_sep,
            'r':float(r),'r_upper':float(upper),
        })

dense=[]
for m in range(2,9):
    N=2**m
    for kappa in (1.,2.,5.):
        Q=np.zeros((N,N))
        for x in range(N):
            for i in range(m):
                y=x^(1<<i)
                Q[x,y]=kappa if x==0 or y==0 else 1.
            Q[x,x]=-Q[x].sum()
        eig=eigvalsh(-Q)
        t=np.linalg.solve(-Q[1:,1:],np.ones(N-1))
        theory=float(exact_mean(m,F(int(kappa))))
        assert abs(t.mean()/theory-1)<1e-11
        assert eig[1]>=2-1e-10
        b=1-1/N
        deadline=b*float(exact_mean(m,F(1)))
        surv=float(np.ones(N-1)@expm(deadline*Q[1:,1:])@np.ones(N-1)/(N-1))
        dense.append({'m':m,'kappa':kappa,'mean':theory,
            'mean_relative_dense_error':float(abs(t.mean()/theory-1)),
            'spectral_gap':float(eig[1]),'cdf_at_base_deadline':1-surv})

result={'exact_formula_and_bound_verified_m':list(range(6,129)),
        'rare_examples':exact_bounds,'small_dense_checks':dense,
        'note':'Exact Fraction checks establish finite algebra in tested dimensions; general proof is in PASSIVE_IDENTIFIABILITY.txt. Dense checks are numerical, not proof.'}
(OUT/'rare_gate_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'rare_examples':exact_bounds,
    'max_dense_mean_relative_error':max(x['mean_relative_dense_error'] for x in dense),
    'minimum_dense_spectral_gap':min(x['spectral_gap'] for x in dense)},indent=2))
