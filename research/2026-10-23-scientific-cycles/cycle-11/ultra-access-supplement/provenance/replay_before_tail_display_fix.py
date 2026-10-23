#!/usr/bin/env python3
"""Exact finite classical record laws + character admissions, no quantum code."""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import log,exp,sqrt,ceil,log2
from pathlib import Path
from time import perf_counter
import json
HERE=Path(__file__).resolve().parent
def H(vals):return -sum(float(v)*log(float(v)) for v in vals if v)
def marg(joint,indices):
    d=defaultdict(F)
    for k,v in joint.items():d[tuple(k[i] for i in indices)]+=v
    return d
def law(D,p):
    q=F(1,D*D); L=len(p); j={}
    for k,pk in enumerate(p,1):
        for z in range(k,L+1):
            v=pk*q**(z-k)*(1 if z==L else 1-q)
            if v:j[k,z]=v
    assert sum(j.values())==1
    return j
def check(D,p,r,alpha):
    base=law(D,p);beta=1-alpha; b=defaultdict(F)
    for entries in product(list(base),repeat=r):
        kv=tuple(k for k,j in entries);jv=tuple(j for k,j in entries)
        w=F(1)
        for e in entries:w*=base[e]
        b[kv,jv]+=w
    full=[]
    for mode in ('global_padded','iid'):
        out=defaultdict(F)
        for (kv,jv),w in b.items():
            for fs in product((0,1),repeat=r):
                fw=alpha**sum(fs)*beta**(r-sum(fs))
                payload=tuple(k-1 if (fs[0] if mode=='global_padded' else f) else 0
                              for k,f in zip(kv,fs))
                out[kv,jv,(fs,payload)]+=w*fw
        assert sum(out.values())==1
        assert marg(out,(0,1))=={(k,j):v for (k,j),v in b.items()}
        hk=H(marg(out,(0,)).values());hj=H(marg(out,(1,)).values());hz=H(marg(out,(2,)).values())
        hkz=H(marg(out,(0,2)).values());hjz=H(marg(out,(1,2)).values())
        hkcond=hkz-hz;ikz=hk+hz-hkz;ijz=hj+hz-hjz
        baseI=H(marg(b,(0,)).values())+H(marg(b,(1,)).values())-H(b.values())
        oneH=H(p);ha=H((alpha,beta))
        assert abs(hkcond-float(beta)*r*oneH)<1e-11
        assert abs(ikz-float(alpha)*r*oneH)<1e-11
        assert abs(ijz-float(alpha)*baseI)<1e-11
        assert abs(hz-(r*ha+float(alpha)*r*oneH))<1e-11
        if mode=='global_padded':
            bad=defaultdict(F)
            for (kv,jv,z),v in out.items():
                if z[0][0]==0:bad[kv,jv]+=v/beta
            assert dict(bad)==dict(b)
        full.append(dict(mode=mode,HZ=hz,H_K_given_Z=hkcond,I_KZ=ikz,I_JZ=ijz,
                         exact_joint_cells=len(out),record_bits_per_party=r*(1+ceil(log2(len(p))))))
    for k in ('HZ','H_K_given_Z','I_KZ','I_JZ'):
        assert abs(full[0][k]-full[1][k])<1e-11
    assert full[0]['record_bits_per_party']==full[1]['record_bits_per_party']
    return dict(D=D,p=[str(x) for x in p],r=r,alpha=str(alpha),matching=full)
def main():
    t=perf_counter();cases=[]
    for D in (2,3):
        for p in ([F(1,2)]*2,[F(1,4),F(3,4)],[F(1,3)]*3):
            for r in (1,2,3):
                for alpha in (F(1,2),F(3,4)):
                    cases.append(check(D,p,r,alpha))
    chars=0
    for N in range(2,10):
        for c,d,cc,dd in product(range(N),repeat=4):
            if (c,d)==(cc,dd):
                assert all((a*(d-dd)-b*(c-cc))%N==0 for a,b in product(range(N),repeat=2))
            else:
                assert ((d-dd)%N!=0 or (c-cc)%N!=0)
                assert any((a*(d-dd)-b*(c-cc))%N!=0 for a,b in ((1,0),(0,1)))
            chars+=1
    q=F(1,4);cq=-log(1-float(q))-float(q/(1-q))*log(float(q))
    margin=log(2)-cq/2
    assert 3**3>2**2 and abs(margin-(log(3)/2-log(2)/3))<1e-14
    D=2;L=4096;B=(L+1)*log(D)/2
    counter=dict(D=D,L=L,beta='1/4',H=12*log(2),B=B,kappa_D=2*log(2),
                 iid_rate_lower=B-5*log(2),global_rate_upper=B-6*log(2)+cq/2,
                 strict_positive_margin=margin,
                 exact_positive_integer_witness='3^3 > 2^2',
                 full_quantum_matrix_allocated=False)
    tails=[]
    for r in (100,10000,1000000):
        beta=r**(-.25);tail=exp(-2*sqrt(r))
        tails.append(dict(L=2,r=r,beta=beta,inventory_tail_upper=tail,
                          direct_global_error_upper=beta+tail))
    result=dict(status='PASS',proof_sha256=sha256((HERE/'PROOF.txt').read_bytes()).hexdigest(),
        replay_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        scope='Exact rational small record laws and Weyl character separation; floating entropy displays; no quantumcode',
        matching_record_cases=len(cases),exact_joint_cells=sum(sum(x['exact_joint_cells'] for x in c['matching']) for c in cases),
        exact_character_separation_cases=chars,records=cases,explicit_counterexample=counter,
        vanishing_outage_scalars=tails,wall_seconds=perf_counter()-t,
        quantum_codes_executed=0,historical_priority='UNKNOWN',hardware_calls=0,paid_services=0)
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','vanishing_outage_scalars')},indent=2))
if __name__=='__main__':main()
