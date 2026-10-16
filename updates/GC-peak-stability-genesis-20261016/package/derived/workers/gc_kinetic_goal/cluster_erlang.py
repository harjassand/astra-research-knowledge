#!/usr/bin/env python3
"""Bounded two-site comparison, never the eight-site full CME.

Numerical candidate: block-tridiagonal resolvent recurrence. Certificate:
integer arithmetic against the exact decimal generator and fixed dyadic
stored vectors. All outgoing cap transitions are counted as comparison
success (an upper-bound device, not the original success event).
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
import argparse
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
import hashlib
import resource
import sys
import time
import numpy as np

sys.set_int_max_str_digits(100000)

DEN = 10000
DYAD = 1 << 60
DIFF = 82207

def b(n): return 26760*n*(n-1)+1081020
def a(n): return 400*n*(n-1)*(n-2)+378810*n

def frac(x):
    return {'exact': str(x), 'approximate': float(x)}

def erlang_survival(k, r):
    """Exact rational enclosure of P(Gamma(k,r)>=1), integer r."""
    terms = sum((F(r**j, factorial(j)) for j in range(k)), F(0))
    en = sum((F(1, factorial(j)) for j in range(33)), F(0))
    eup = en + F(34, 33*factorial(33))
    return terms/eup**r, terms/en**r

def build(cap, external, r):
    d = cap+1
    blocks=[]; lows=[]; ups=[]; successes=[]
    for n in range(d):
        M=np.zeros((d,d)); L=np.zeros((d,d)); U=np.zeros((d,d))
        suc=np.zeros(d)
        for m in range(d):
            if n<=15 and m<=15:
                M[m,m]=r
                continue
            rates=[((n+1,m),b(n)), ((n,m+1),b(m))]
            if n: rates.append(((n-1,m),a(n)+external*DIFF*n))
            if m: rates.append(((n,m-1),a(m)+external*DIFF*m))
            if n: rates.append(((n-1,m+1),DIFF*n))
            if m: rates.append(((n+1,m-1),DIFF*m))
            M[m,m]=r+sum(v for _,v in rates)/DEN
            for (nn,mm), rate in rates:
                if nn>cap or mm>cap:
                    suc[m]+=rate/DEN
                elif nn==n:
                    M[m,mm]-=rate/DEN
                elif nn==n-1:
                    L[m,mm]-=rate/DEN
                elif nn==n+1:
                    U[m,mm]-=rate/DEN
                else: raise AssertionError('Non-neighbor block')
        blocks.append(M); lows.append(L); ups.append(U); successes.append(suc)
    return blocks, lows, ups, np.array(successes)

def factor(blocks, lows, ups):
    # dense block factors only: O((cap+1)^3) memory, never 163^8.
    inv=[]; ell=[]; hh=[]
    for n, M in enumerate(blocks):
        if n:
            E=lows[n]@inv[-1]
            D=M-E@ups[n-1]
        else:
            E=np.zeros_like(M); D=M
        I=np.linalg.inv(D)
        inv.append(I); ell.append(E); hh.append(I@ups[n])
    return inv, ell, hh

def solve(fact, rhs):
    inv, ell, hh=fact
    v=[]
    for n in range(len(inv)):
        v.append(rhs[n] if n==0 else rhs[n]-ell[n]@v[-1])
    x=[None]*len(inv)
    for n in reversed(range(len(inv))):
        x[n]=inv[n]@v[n]
        if n+1<len(inv): x[n]-=hh[n]@x[n+1]
    return np.array(x)

def exact_residual(U, previous, cap, external, r):
    """max |(rI-Q)U-r previous-q_success*DYAD| as integer numerator.

    Denominator of the actual residual is DEN*DYAD. This also checks all
    frozen target rows and all physical one-step predecessor/overflow terms.
    """
    worst=0; point=None
    for n in range(cap+1):
        for m in range(cap+1):
            if n<=15 and m<=15:
                z=r*DEN*(U[n][m]-previous[n][m])
            else:
                rates=[((n+1,m),b(n)), ((n,m+1),b(m))]
                if n: rates.append(((n-1,m),a(n)+external*DIFF*n))
                if m: rates.append(((n,m-1),a(m)+external*DIFF*m))
                if n: rates.append(((n-1,m+1),DIFF*n))
                if m: rates.append(((n+1,m-1),DIFF*m))
                z=(r*DEN+sum(v for _,v in rates))*U[n][m]-r*DEN*previous[n][m]
                for (nn,mm), v in rates:
                    z-=v*(DYAD if nn>cap or mm>cap else U[nn][mm])
            if abs(z)>worst: worst=abs(z); point=[n,m]
    return worst, point

def run(args):
    start=time.monotonic()
    resource.setrlimit(resource.RLIMIT_CPU,(args.cpu_seconds,args.cpu_seconds+1))
    if args.cap<50 or args.cap>162: raise ValueError('Require50<=cap<=162')
    if args.k>256: raise ValueError('At most256 phases')
    estimates={}; saved={}; target=np.zeros((args.cap+1,args.cap+1)); target[:16,:16]=1
    lo_surv, hi_surv=erlang_survival(args.k,args.rate)
    for external in [1,2]:
        construct=time.monotonic()
        matrices=build(args.cap, external,args.rate)
        fact=factor(*matrices[:3])
        overflow=matrices[3]
        # Original sparse generator definition is re-evaluated by integer code.
        del matrices
        u=target.copy(); prev=[[int(x*DYAD) for x in row] for row in u]
        stages=[np.array(prev,dtype=np.uint64)]
        error_numerator=0; phases=[]
        for j in range(1,args.k+1):
            if time.monotonic()-start>args.wall_seconds: raise TimeoutError('Declared wall cap')
            u=solve(fact,args.rate*u+overflow)
            u[:16,:16]=1
            U=[[int(round(float(x)*DYAD)) for x in row] for row in u]
            defect, point=exact_residual(U,prev,args.cap,external,args.rate)
            error_numerator+=defect
            phases.append({'phase':j,'exact_residual_max_integer_numerator':str(defect),'maximizer':point})
            prev=U
            if any(x<0 or x>=(1<<64) for row in U for x in row): raise ValueError('Vector outside uint64 export range')
            stages.append(np.array(U,dtype=np.uint64))
            u=np.array([[x/DYAD for x in row] for row in U])
        radius=F(error_numerator,DEN*DYAD*args.rate)
        val=F(prev[50][50],DYAD)
        lower=max(F(0),val-radius); upper=min(F(1),val+radius)
        deterministic_upper=min(F(1),upper/lo_surv)
        deterministic_lower=max(F(0),(lower-hi_surv)/(1-hi_surv))
        estimates[str(external)]={
            'pair_initial':[50,50], 'external_departure_degree_per_site':external,
            'phases':phases, 'random_horizon_estimate_exact':str(val),
            'uniform_error_radius':frac(radius),
            'random_horizon_probability_interval':[frac(lower),frac(upper)],
            'deadline1_probability_upper':frac(deterministic_upper),
            'deadline1_probability_lower':frac(deterministic_lower),
            'elapsed_seconds':time.monotonic()-construct,
        }
        Path(args.output+'.progress.json').write_text(json.dumps(estimates,indent=2))
        saved['external_'+str(external)]=np.stack(stages)
        del fact, overflow
    # Two corner columns with external degree1 and two inner columns degree2.
    global_up=F(estimates['1']['deadline1_probability_upper']['exact'])**2 * F(estimates['2']['deadline1_probability_upper']['exact'])**2
    npz=Path(args.output).with_suffix('.npz')
    np.savez_compressed(npz,**saved)
    report={
        'status':'CERTIFIED_SPATIAL_CLUSTER_UPPER_BOUND',
        'actual_model':'Original unbounded eight-site open2x4 Schlogl CTMC, initial50^8, targetmax<=15, deadline1',
        'comparison':'Delete all horizontal immigration in four independent vertical two-site chains; retain horizontal departures as local deaths; cap overflow is comparison success.',
        'cap':args.cap, 'target_max':15, 'states_per_pair':(args.cap+1)**2,
        'erlang_shape':args.k,'erlang_rate':args.rate,
        'erlang_survival_at1_interval':[frac(lo_surv),frac(hi_surv)],
        'arithmetic':'Exact rates integer/DEN; stored vectors integer/2^60; all recurrence defects exact integers. Dense factors are only candidate generation.',
        'denominator_rate':DEN,'dyadic_denominator':str(DYAD),
        'stored_vectors_npz':npz.name,
        'stored_vectors_sha256':hashlib.sha256(npz.read_bytes()).hexdigest(),
        'stored_vectors_bytes':npz.stat().st_size,
        'pair_estimates':estimates,
        'actual_eight_site_deadline_probability_upper':frac(global_up),
        'certifies_requested_1e9_absolute_target':global_up<=F('1e-9'),
        'elapsed_seconds':time.monotonic()-start,
        'peak_rss_native_units':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'platform':sys.platform,'cpu_limit_seconds':args.cpu_seconds,
        'wall_limit_seconds':args.wall_seconds,'npz_or_raw_inputs_modified':False,
    }
    Path(args.output).write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['pair_estimates','erlang_survival_at1_interval']},indent=2))
    for e,v in estimates.items(): print(e, v['random_horizon_probability_interval'], v['deadline1_probability_upper'], 'radius',v['uniform_error_radius'])

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cap',type=int,default=162)
    p.add_argument('--k',type=int,default=64)
    p.add_argument('--rate',type=int,default=64)
    p.add_argument('--cpu-seconds',type=int,default=160)
    p.add_argument('--wall-seconds',type=int,default=180)
    p.add_argument('--output',required=True)
    run(p.parse_args())
