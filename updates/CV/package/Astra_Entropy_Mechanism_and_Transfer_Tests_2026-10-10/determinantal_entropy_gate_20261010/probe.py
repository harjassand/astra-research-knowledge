#!/usr/bin/env python3
"""Finite-output probes of the bosonic-amplifier Fredholm determinant order.

The squeezing unitary is never truncated. We use its exact disentangled Fock
matrix elements, then project the exact output vector onto total photon number
<= cutoff. The omitted-vector norm is bounded analytically in tails().
"""
from __future__ import annotations
import math
import json
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from scipy.special import gammaln


def log_amp_basis(m:int,n:int,j:int,k:int,G:float)->float:
    """Log absolute amplitude of the (m,n,j,k) disentangling summand."""
    s=(G-1.0)/G
    lam=math.sqrt(s)
    a,b=m-j,n-j
    return ((j+k)*math.log(lam) - gammaln(j+1) - gammaln(k+1)
            +0.5*(gammaln(m+1)+gammaln(n+1)-gammaln(a+1)-gammaln(b+1))
            -0.5*(m+n-2*j+1)*math.log(G)
            +0.5*(gammaln(a+k+1)+gammaln(b+k+1)-gammaln(a+1)-gammaln(b+1)))


def amp_basis(m:int,n:int,p:int,q:int,G:float)->float:
    """Exact real matrix element <p,q|S_r|m,n>, via disentangling.

    Here G=cosh(r)^2, lambda=tanh(r), and
    S=exp(lambda a^dag b^dag) G^{-(N_a+N_b+1)/2} exp(-lambda ab).
    The summation index j obeys p=m-j+k, q=n-j+k.
    """
    if p-q != m-n: return 0.0
    s=(G-1.0)/G
    if s==0.0: return 1.0 if (p,q)==(m,n) else 0.0
    lam=math.sqrt(s)
    total=0.0
    # j is fixed by k=p-m+j >=0 and 0<=j<=min(m,n).
    for j in range(min(m,n)+1):
        k=p-m+j
        if k<0 or q != n-j+k: continue
        mag=math.exp(log_amp_basis(m,n,j,k,G))
        total += (-1.0 if (j%2) else 1.0)*mag
    return total


def amp_summand(m:int,n:int,j:int,k:int,G:float)->float:
    return (-1.0 if j%2 else 1.0)*math.exp(log_amp_basis(m,n,j,k,G))


def output_triangle_cutoff(f:np.ndarray,g:np.ndarray,G:float,M:int):
    """Output amplitude matrix on p+q<=M; exact coefficients of S, no U truncation."""
    psi=np.zeros((M+1,M+1),dtype=np.complex128)
    for m, fm in enumerate(f):
      if abs(fm)==0: continue
      for n, gn in enumerate(g):
        coeff=fm*gn
        if abs(coeff)==0: continue
        for j in range(min(m,n)+1):
          a,b=m-j,n-j
          maxk=(M-(a+b))//2
          if maxk<0: continue
          for k in range(maxk+1):
            p,q=a+k,b+k
            psi[p,q] += coeff*amp_summand(m,n,j,k,G)
    return psi


def tails(f:np.ndarray,g:np.ndarray,G:float,M:int)->dict:
    """Certified upper bound on ||1_{Ntot>M} S(f tensor g)||.

    For a fixed (m,n,j) summand, squared successive coefficients have ratio
    s*(k+a+1)*(k+b+1)/(k+1)^2, decreasing in k. Bound the remaining squared
    tail by its first term divided by 1-ratio, then use Minkowski over the
    finite input superposition and j-summands. This can be conservative.
    """
    s=(G-1.0)/G
    B=0.0
    for m,fm in enumerate(f):
      for n,gn in enumerate(g):
        w=abs(fm*gn)
        if w==0: continue
        for j in range(min(m,n)+1):
          a,b=m-j,n-j
          k0=max(0,(M-(a+b))//2+1)
          r=s*(k0+a+1)*(k0+b+1)/(k0+1)**2
          if r>=1:
            return {"amplitude_bound":1.0,"probability_bound":1.0,"not_yet_geometric":True}
          first=math.exp(log_amp_basis(m,n,j,k0,G))
          norm=first/math.sqrt(1-r)
          B += w*norm
    B=min(1.0,B)
    return {"amplitude_bound":B,"probability_bound":min(1.0,B*B),"not_yet_geometric":False}


def thermal_e3(G:float)->float:
    s=(G-1.0)/G
    # e_k = (1-s)^k s^{k(k-1)/2}/prod_{j=1}^k(1-s^j), q-binomial theorem.
    return (1-s)**3*s**3/((1-s)*(1-s*s)*(1-s**3))


def thermal_logdet(G:float,t:float,cut:int=100000)->tuple[float,float]:
    s=(G-1.0)/G
    # Keep terms p_n with n < cut; remainder <= t * sum_{n>=cut} p_n = t*s^cut.
    val=0.0
    p=1-s
    for n in range(cut):
        val+=math.log1p(t*p)
        p*=s
    return val,t*(s**cut)


def invariants(psi:np.ndarray,G:float,ts=(0.1,0.3,1.0,3.0,10.0,30.0)):
    rho=psi@psi.conj().T
    rho=(rho+rho.conj().T)/2
    vals=np.linalg.eigvalsh(rho)
    vals=np.maximum(vals,0)
    tr=float(vals.sum())
    tr2=float(np.dot(vals,vals))
    tr3=float(np.dot(vals,vals*vals))
    e3=(tr**3-3*tr*tr*tr2+2*tr3)/6
    dets={}
    for t in ts:
        lhs=float(np.log1p(t*vals).sum())
        rhs,tail=thermal_logdet(G,t,cut=len(vals)+1000)
        dets[str(t)]={"logdet_gap_cut":lhs-rhs,"thermal_tail_bound":tail}
    return {"trace_cut":tr,"tr2_cut":tr2,"tr3_cut":tr3,"e3_cut":e3,
            "e3_thermal":thermal_e3(G),"e3_gap_cut":e3-thermal_e3(G),
            "logdet_gaps":dets}


def rand_state(rng,d):
    x=rng.normal(size=d+1)+1j*rng.normal(size=d+1)
    return x/np.linalg.norm(x)


def main():
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--seed',type=int,default=20261010)
    ap.add_argument('--M',type=int,default=90)
    ap.add_argument('--samples',type=int,default=200)
    ap.add_argument('--d',type=int,default=3)
    args=ap.parse_args()
    rng=np.random.default_rng(args.seed)
    ts=tuple(float(x) for x in np.logspace(-3,4,15))
    cases=[]
    for G in (1.25,1.5,2.0,3.0):
      cases.append((f"vacuum_G{G}",G,np.array([1+0j]),np.array([1+0j])))
      for m,n in ((1,0),(1,1),(2,0),(2,1),(2,2),(3,1)):
        f=np.zeros(m+1,complex);f[m]=1
        g=np.zeros(n+1,complex);g[n]=1
        cases.append((f"fock_{m}_{n}_G{G}",G,f,g))
    for i in range(args.samples):
      G=(1.12,1.25,1.5,2.0,3.0)[i%5]
      cases.append((f"random_{i}_G{G}",G,rand_state(rng,args.d),rand_state(rng,args.d)))
    rows=[]
    for name,G,f,g in cases:
      psi=output_triangle_cutoff(f,g,G,args.M)
      b=tails(f,g,G,args.M)
      inv=invariants(psi,G,ts=ts)
      # trace-norm error from output cutoff: ||rho-rho_M||_1 <= 2||tail||.
      eps=2*math.sqrt(b['probability_bound'])
      inv.update({"name":name,"G":G,"f": [[x.real,x.imag] for x in f],"g":[[x.real,x.imag] for x in g],
                  "M":args.M,"tail_bound":b,"rho_trace_norm_error_bound":eps,
                  "e3_gap_error_bound":eps/2})
      inv['det_lower_bounds']={t:(d['logdet_gap_cut'] - float(t)*eps - d['thermal_tail_bound'])
                               for t,d in inv['logdet_gaps'].items()}
      inv['e3_gap_lower_bound']=inv['e3_gap_cut']-inv['e3_gap_error_bound']
      rows.append(inv)
    # Report minima after conservative numerical/tail error bars.
    out={"seed":args.seed,"M":args.M,"samples":args.samples,"d":args.d,"rows":rows}
    outpath=Path(__file__).with_name('probe_results.json')
    with open(outpath,'w') as f: json.dump(out,f,indent=2)
    # Per-gain minima over random samples and the sampled t grid.
    random_rows=[r for r in rows if r['name'].startswith('random')]
    for G in sorted({r['G'] for r in random_rows}):
      rr=[r for r in random_rows if r['G']==G]
      worst_e=min(rr,key=lambda r:r['e3_gap_lower_bound'])
      detmin=min((v,r,t) for r in rr for t,v in r['det_lower_bounds'].items())
      print('G',G,'min sampled e3 lower bound',worst_e['e3_gap_lower_bound'],worst_e['name'])
      print('G',G,'min sampled determinant lower bound',detmin[0],'state',detmin[1]['name'],'t',detmin[2])
    # Global certified lower margins over random samples and the fixed t grid.
    min_e=min(random_rows,key=lambda r:r['e3_gap_lower_bound'])
    print('global minimum sampled e3 lower bound',min_e['e3_gap_lower_bound'],min_e['name'])
    detmin=min((v,r,t) for r in random_rows for t,v in r['det_lower_bounds'].items())
    print('global minimum sampled det lower bound',detmin[0],detmin[1]['name'],'t',detmin[2])
    print('wrote',outpath)

if __name__=='__main__':main()
