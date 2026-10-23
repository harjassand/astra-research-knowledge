#!/usr/bin/env python3
"""New finite arithmetic admissions only; not an asymptotic quantum-code run."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import log, log2, ceil, isclose
from pathlib import Path
from time import perf_counter, process_time

ROOT=Path(__file__).resolve().parent
def entropy(ps):
    return -sum(float(p)*log(float(p)) for p in ps if p)
def geo(q):
    return -log(1-q)-q*log(q)/(1-q)
def xor_law(D):
    z=[F(0)]*(1<<ceil(log2(D)))
    for a,b in product(range(D),repeat=2): z[a^b]+=F(1,D*D)
    assert sum(z)==1 and z[0]==F(1,D)
    return z
def leading_posterior(p,q):
    """H(K|leading-zero label), exact rational law, float entropy."""
    L=len(p); c=0.0
    for j in range(1,L+1):
        weights=[p[k-1]*q**(j-k) for k in range(1,j+1)]
        s=sum(weights)
        if s: c+=float(s if j==L else (1-q)*s)*entropy([x/s for x in weights])
    return c
def exact_stats(D,p,matrix_check=False):
    L=len(p); assert sum(p)==1 and all(x>=0 for x in p)
    q=F(1,D); xd=xor_law(D); hn=entropy([x/(1-q) for x in xd[1:] if x])
    joint={}; pn={}; post={}; g=0.0; cp=0.0; hkgiv=0.0; nmean=F(0)
    for n in range(1,L+1):
        weights=[p[k-1]*q**(n-k) for k in range(1,n+1)]
        s=sum(weights)
        if not s: continue
        pn[n]=s if n==L else (1-q)*s
        post[n]=[x/s for x in weights]
        for k in range(1,n+1): joint[k,n]=pn[n]*post[n][k-1]
        cphase=leading_posterior(post[n],q)
        cp+=float(pn[n])*cphase
        hk=entropy(post[n]); hkgiv+=float(pn[n])*hk
        nk=sum(F(k)*post[n][k-1] for k in range(1,n+1))
        stheta=hk+float(n-nk)*log(D)-cphase
        g+=float(pn[n])*(n*log(D)-stheta)
        nmean+=n*pn[n]
        if matrix_check:
            # Actual MC matrix entries, rational; no spectral assumption in this path.
            digits=list(product(range(D),repeat=n)); dim=D**n
            M=[[sum(post[n][k-1] for k in range(1,n+1) if a[k:]==b[k:])/dim
                for b in digits] for a in digits]
            assert sum(M[i][i] for i in range(dim))==1
            assert all(M[i][i]==F(1,dim) for i in range(dim))
            trace2=sum(M[i][j]*M[j][i] for i in range(dim) for j in range(dim))
            trace3=sum(M[i][j]*M[j][k]*M[k][i] for i in range(dim)
                       for j in range(dim) for k in range(dim))
            ev=[]
            for ell in range(n+1):
                lam=sum(post[n][k-1]*q**(n-k) for k in range(1,min(ell,n)+1))
                deg=1 if ell==n else (D-1)*D**(n-ell-1)
                ev.append((lam,deg))
            assert sum(lam*deg for lam,deg in ev)==1
            assert trace2==sum(lam**2*deg for lam,deg in ev)
            assert trace3==sum(lam**3*deg for lam,deg in ev)
            se=-sum(float(deg*lam)*log(float(lam)) for lam,deg in ev if lam)
            assert abs(se-stheta)<1e-10
    assert sum(pn.values())==1
    for k in range(1,L+1): assert sum(v for (kk,n),v in joint.items() if kk==k)==p[k-1]
    c=entropy(pn.values())+float(1-pn.get(L,F(0)))*hn
    hvk=entropy(joint.values())-entropy(p)+float(1-pn.get(L,F(0)))*hn
    B=float(sum((k+1)*pk for k,pk in enumerate(p)))*log(D); H=entropy(p)
    kap=entropy(xd)/float(1-q)
    assert hvk<=kap+1e-10
    assert abs(g-c-(B-H-hvk+cp))<1e-9
    assert g>=B-hkgiv-1e-10
    C=leading_posterior(p,F(1,D*D)); U=B-H/2+C/2
    k0=next(k+1 for k,x in enumerate(p) if x)
    rate=max(k0*log(D),g-c)
    assert rate<=U+1e-8
    return dict(D=D,L=L,B_nats=B,H_nats=H,kappa_nats=kap,
        stop_cost_nats=c,gross_hashing_nats=g,net_hashing_nats=g-c,
        baseline_nats=k0*log(D),best_new_lower_nats=rate,
        simple_new_lower_nats=max(k0*log(D),B-H-kap),
        converse_upper_nats=U,C_bell=C,H_V_given_K=hvk,H_K_given_XV=cp,
        scope="Exact rational stopped laws and MC spectra; logarithms floating. No code execution.")
def kraus_admissions():
    count=0
    # Direct ancilla amplitudes for local controls, including all pairwise coherence entries.
    for a,b,aa,bb,u,v in product(range(2),repeat=6):
        amp=lambda x,y: F(1,2) if (u^x)==(v^y) else F(0)
        # amplitude products; real amplitudes 1/sqrt2, hence product=1/2.
        actual=F(1,2) if ((u^a)==(v^b) and (u^aa)==(v^bb)) else F(0)
        projected=F(1,2) if ((a^b)==(u^v) and (aa^bb)==(u^v)) else F(0)
        assert actual==projected; count+=1
    for D in range(2,12):
        # Sum pair-subset POVM coefficients at every source index, and branch pair weights.
        for i in range(D):
            assert sum(F(1,D-1) for a in range(D) for b in range(a+1,D) if i in (a,b))==1
        assert F(D*(D-1),2)*F(2,D*(D-1))==1
        count+=D+1
    return count
def full_joint_admission(D,p):
    L=len(p); expected=defaultdict(F); brute=defaultdict(F)
    xlaw=xor_law(D)
    for k,pk in enumerate(p,1):
        if not pk: continue
        for es in product(range(len(xlaw)),repeat=L-k):
            w=pk
            for e in es: w*=xlaw[e]
            if not w: continue
            full=(0,)*k+es
            stop=next((i for i,e in enumerate(full,1) if e),L+1)
            v=(stop,0 if stop==L+1 else full[stop-1])
            brute[k,v]+=w
        for n in range(k,L+1):
            if n==L: expected[k,(L+1,0)]+=pk*F(1,D)**(L-k)
            else:
                for e in range(1,len(xlaw)):
                    expected[k,(n+1,e)]+=pk*F(1,D)**(n-k)*xlaw[e]
    assert {k:v for k,v in brute.items() if v}=={k:v for k,v in expected.items() if v}
    return len(brute)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=ROOT/'RESULT.json'); args=ap.parse_args()
    t=perf_counter(); cpu=process_time(); counters=defaultdict(int)
    rows=[]
    for D in range(2,17):
        kap=entropy(xor_law(D))/(1-1/D)
        assert kap<=D*log(D)/(D-1)+log(2)+1e-12
        if D&(D-1)==0: assert abs(kap-D*log(D)/(D-1))<1e-12
        counters['xor_noise_and_kappa']+=1
    counters['kraus_and_exact_seed']=kraus_admissions()
    # Nonuniform, zero-support, deterministic and adjacent-low-weight cases.
    for D in (2,3,4,5):
        for L in range(2,8):
            priors=[[F(1,L)]*L,[F(1)]+[F(0)]*(L-1),
                [F(1,2)]+[F(0)]*(L-2)+[F(1,2)],
                [F(k,L*(L+1)//2) for k in range(1,L+1)]]
            for p in priors:
                exact_stats(D,p); counters['general_prior_entropy_and_rate']+=1
    for D,L in ((2,2),(2,3),(3,2),(3,3),(5,2)):
        p=[F(k,L*(L+1)//2) for k in range(1,L+1)]
        exact_stats(D,p,matrix_check=True); counters['rational_MC_matrix_trace2_trace3_spectra']+=L
        counters['enumerated_complete_XOR_sector_branches']+=full_joint_admission(D,p)
    for D,L in ((2,2),(2,8),(2,16),(2,30),(2,100),(3,30),(4,30),(6,30)):
        rows.append(exact_stats(D,[F(1,L)]*L))
    sparse=[]
    for D in (2,3,6):
        kap=entropy(xor_law(D))/(1-1/D)
        for L in (100,1000000,10**12):
            B=(L+1)*log(D)/2
            sparse.append(dict(D=D,L=L,prior='p(1)=p(L)=1/2',B_nats=B,
                sufficient_absolute_deficit_nats=log(2)+kap,
                support_gap=L-1,scope='Analytic lower bound only, no L-slot allocation or simulation'))
    result=dict(status='PASS',proof_sha256=sha256((ROOT/'PROOF.txt').read_bytes()).hexdigest(),
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),admissions=dict(counters),
        uniform_actual_stopped_receiver=rows,sparse_prior_bound=sparse,
        costs=dict(wall_seconds=perf_counter()-t,cpu_seconds=process_time()-cpu,
            quantum_codes_executed=0,old_scientific_suites_rerun=0,
            paid_credits=0,hardware_calls=0,total_discovery_inference_cost='UNKNOWN'),
        limits=['No asymptotic code compiled or executed','No rigorous interval arithmetic claimed for displayed logarithms',
            'Finite exact identities/admissions do not prove all-parameter coding or novelty'])
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],admissions=result['admissions'],costs=result['costs']),indent=2))
if __name__=='__main__': main()
