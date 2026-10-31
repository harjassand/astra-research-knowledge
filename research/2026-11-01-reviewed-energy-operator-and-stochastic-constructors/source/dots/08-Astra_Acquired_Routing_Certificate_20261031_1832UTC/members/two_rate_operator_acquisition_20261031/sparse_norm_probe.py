#!/usr/bin/env python3
"""Fresh integer-probe spectral upper confidence bound with paid grid errors.

Not a deterministic norm certificate: independent random probe provenance is
an explicit premise. Sparse matrices and the partition are fixed before it.
"""
from pathlib import Path
import hashlib
import itertools
import json
import math
import random
import sys
import time
import sympy as s

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'robust_operator_reuse_20261031'/'finite_observation'))
from robust_replay import sqrt_up,psd
R=s.Rational


def rnd_div(x,d):return (2*x+d)//(2*d)


def q_step(z,parts):
    out=z[:]
    for part in parts:
        total=sum(z[i] for i in part);k=len(part)
        shift=rnd_div(-total,k)
        for i in part:out[i]=z[i]+shift
    return out


def sparse_step(rows,z,numer,denom):
    out=[];peak=0;products=0
    for row in rows:
        acc=sum(v*z[j] for j,v in row);products+=len(row)
        acc*=numer;peak=max(peak,abs(acc).bit_length())
        out.append(rnd_div(acc,denom))
    return out,peak,products


def validate_counts(rows,N,parts):
    n=len(rows)
    if type(N) is not int or N<=0 or n<1:raise ValueError('count denominator')
    if sorted(i for p in parts for i in p)!=list(range(n)) or any(not p for p in parts):
        raise ValueError('partition')
    for row in rows:
        seen=set()
        for j,v in row:
            if type(j) is not int or type(v) is not int or not 0<=j<n or v<=0 or j in seen:
                raise ValueError('sparse count entry')
            seen.add(j)
    if sum(v for row in rows for _,v in row)!=N:raise ValueError('count total')


def upper_norm(rows,N,parts,delta=R(1,10000),seed=81291,forced_probe=None):
    """C=n*counts/N. forced_probe exists ONLY for falsification tests."""
    start=time.perf_counter();validate_counts(rows,N,parts);n=len(rows)
    col=[0]*n;transpose=[[] for _ in range(n)]
    for i,row in enumerate(rows):
        for j,v in row:col[j]+=v;transpose[j].append((i,v))
    rowmax=max(sum(v for _,v in row) for row in rows)
    beta=sqrt_up(R(n*n*rowmax*max(col),N*N),bits=30)
    if beta==0:return {'upper':'0','status':'ZERO_MATRIX'}
    J=1
    while J<2/delta:J*=2
    factor=R(9,8);p=1
    while factor**(2*p)<2*n*J:p+=1
    grid=6*p+64;scale=1<<grid;rng=random.Random(seed)
    probe=[rng.randrange(J) for _ in range(n)] if forced_probe is None else list(forced_probe)
    if len(probe)!=n or any(type(x) is not int or not 0<=x<J for x in probe):raise ValueError('probe range')
    state=[x*scale for x in probe];peak=0;products=0
    numer=n*int(beta.q);denom=N*int(beta.p)
    for _ in range(p):
        state=q_step(state,parts)
        state,b,k=sparse_step(rows,state,numer,denom);peak=max(peak,b);products+=k
        state=q_step(state,parts)
        state,b,k=sparse_step(transpose,state,numer,denom);peak=max(peak,b);products+=k
        state=q_step(state,parts)
    sq=sum(x*x for x in state);root=math.isqrt(sq)
    if root*root<sq:root+=1
    z_norm_up=R(root,scale);sn=sqrt_up(n)
    error=R(5*p,2*scale)*sn;U=2*sn*(z_norm_up+error)
    bits=24;S=1<<bits
    if U>=1:out=beta;status='DETERMINISTIC_FALLBACK'
    else:
        lo=0;hi=int(s.ceiling(beta*S))
        while lo<hi:
            mid=(lo+hi)//2
            if (R(mid,S)/beta)**(2*p)>=U:hi=mid
            else:lo=mid+1
        out=min(beta,R(hi,S));status='FRESH_PROBE_BOUND'
        assert out==beta or (out/beta)**(2*p)>=U
    return {'upper':str(out),'beta':str(beta),'status':status,'delta':str(delta),'probe_alphabet':J,
            'probe_random_bits':n*(J.bit_length()-1),'power_exponent':p,'grid_bits':grid,
            'norm_rounding_error':str(error),'power_norm_up':str(z_norm_up),
            'sparse_integer_products':products,'peak_integer_accumulator_bits':peak,
            'live_state_entries':n,'nnz':sum(map(len,rows)),
            'execution_seconds':time.perf_counter()-start,
            'probe':probe,'norm_scope':'Probabilistic under fresh independent exact uniform integer probes, not adversarial records.'}


def run_checks():
    checks=0
    def check(ok):
        nonlocal checks
        assert ok;checks+=1
    rng=random.Random(51);cases=[]
    for n in (4,6,8,12):
        counts=s.Matrix(n,n,[rng.randrange(0,6) for _ in range(n*n)])
        N=int(sum(counts));rows=[[(j,int(counts[i,j])) for j in range(n) if counts[i,j]] for i in range(n)]
        parts=[list(range(n//2)),list(range(n//2,n))]
        P=s.zeros(n)
        for part in parts:
            for i in part:
                for j in part:P[i,j]=R(1,len(part))
        Q=s.eye(n)-P;F=Q*(n*counts/N)*Q
        out=upper_norm(rows,N,parts,seed=n)
        check(psd(R(out['upper'])**2*s.eye(n)-F.T*F))
        check(out['sparse_integer_products']==2*out['power_exponent']*out['nnz'])
        cases.append({k:v for k,v in out.items() if k not in ('probe','norm_rounding_error','power_norm_up')})
    # Exhaustively verify the elementary Rademacher 1/12 event for several
    # rational directions, without needing irrational unit normalization.
    for n in (3,5,8):
        for trial in range(5):
            v=[rng.randrange(-3,4) for _ in range(n)]
            if not any(v):v[0]=1
            norm2=sum(x*x for x in v);hits=0
            for signs in itertools.product((-1,1),repeat=n):
                z=sum(x*y for x,y in zip(v,signs));hits+=2*z*z>=norm2
            check(R(hits,2**n)>=R(1,12))
    # A probe chosen orthogonal to the residual can give a false norm claim.
    # Keep this explicit rather than letting the algebraic inequality be
    # mistaken for a deterministic certificate of randomness/provenance.
    n=4;rows=[[(i,1)] for i in range(n)];parts=[list(range(n))]
    bad=upper_norm(rows,n,parts,forced_probe=[1]*n)
    check(R(bad['upper'])<R(1,2)) # actual ||I-P||_2=1
    return {'checks':checks,'status':'PASS','cases':cases,
            'forced_bad_probe_upper':bad['upper'],'forced_bad_probe_actual_norm':'1',
            'forced_probe_meaning':'Expected failure of the freshness/randomness premise; not a valid sampled certificate.',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    out=run_checks();(ROOT/'sparse_norm_probe_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
