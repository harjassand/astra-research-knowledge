#!/usr/bin/env python3
"""Independent exact checks of phase truncation and signed/Fourier recovery.

Uses exhaustive assignments for finite validation; it does not execute the
source's subexponential shared-summary counter.
"""
import argparse
import json
from pathlib import Path
import random


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def neg(a):
    return tuple(-x for x in a)


def mul(a,b):
    d=len(a)
    c=[0]*d
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            t=i+j
            c[t%d]+=(-1 if t>=d else 1)*x*y
    return tuple(c)


def power(a,e):
    ans=(1,)+(0,)*(len(a)-1)
    while e:
        if e&1:
            ans=mul(ans,a)
        a=mul(a,a)
        e//=2
    return ans


def root_power(exponent,d):
    e=exponent%(2*d)
    out=[0]*d
    out[e%d]= -1 if e>=d else 1
    return tuple(out)


def center(v,modulus):
    a=v%modulus
    return a-modulus if a>=modulus//2 else a


def truncated_phase(n, terms, b, character):
    d=1<<(b-1)
    ell=d*(n+2)
    one=(1,)+(0,)*(d-1)
    zero=(0,)*d
    total=[zero for _ in range(ell)]
    true=zero
    hist=[0]*(2*d)
    max_input_degree=0
    for x in range(1<<n):
        v=[one]+[zero for _ in range(ell-1)]
        phase=0
        for mask,coefficient in terms:
            if (mask&x)!=mask:
                continue
            phase=(phase+coefficient)%(2*d)
            c=add(root_power(character*coefficient,d),neg(one))
            for j in range(ell-1,0,-1):
                v[j]=add(v[j],mul(c,v[j-1]))
                if any(v[j]):
                    max_input_degree=max(max_input_degree,j*min(3,n))
        true=add(true,root_power(character*phase,d))
        hist[phase]+=1
        total=[add(a,c) for a,c in zip(total,v)]
    modulus=1<<(n+2)
    recovered=tuple(center(sum(row[i] for row in total),modulus) for i in range(d))
    assert recovered==true
    return recovered,hist,{"ell":ell,"max_retained_incidence_degree_bound":min(3,n)*(ell-1)}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="phase_product_audit_results.json")
    args=p.parse_args()
    rng=random.Random(202610271)
    results=[]
    characters=0
    for b in (1,2,3):
        d=1<<(b-1)
        one=(1,)+(0,)*(d-1)
        pi=add(root_power(1,d),neg(one))
        ramification=power(pi,d)
        assert all(x%2==0 for x in ramification)
        for n in range(0,6):
            for sample in range(4):
                terms=[]
                for _ in range(6+sample*7):
                    chosen=rng.sample(range(n),rng.randint(0,min(3,n)))
                    mask=sum(1<<i for i in chosen)
                    terms.append((mask,rng.randrange(2*d)))
                sums=[]
                for j in range(2*d):
                    z,hist,meta=truncated_phase(n,terms,b,j)
                    sums.append(z)
                    characters+=1
                restored=[]
                for target in range(2*d):
                    total=(0,)*d
                    for j,z in enumerate(sums):
                        total=add(total,mul(root_power(-j*target,d),z))
                    assert all(x==0 for x in total[1:])
                    assert total[0]%(2*d)==0
                    restored.append(total[0]//(2*d))
                assert restored==hist
                results.append({"n":n,"b":b,"terms":len(terms),"histogram":hist,
                                "all_character_sums":[list(z) for z in sums],**meta})
    # The signed endpoint ambiguity at n+1 precision is real.
    endpoint_aliases=[]
    for n in range(1,10):
        modulus=1<<(n+1)
        assert (1<<n)%modulus==(-(1<<n))%modulus
        endpoint_aliases.append(n)
    # A single fourth-root phase does not determine the output histogram.
    z1,h1,_=truncated_phase(1,[(1,2)],2,1)
    z2,h2,_=truncated_phase(1,[(0,1),(1,2)],2,1)
    assert z1==z2==(0,0) and h1!=h2
    out={"status":"all exact assertions passed", "fixtures":len(results),
         "character_sum_reconstructions":characters,
         "endpoint_precision_alias_cases":endpoint_aliases,
         "single_phase_histogram_collision":{"first":h1,"second":h2,"common_phase":list(z1)},
         "scope":"exhaustive finite truncation and reconstruction checks, not the fast source counter",
         "results":results}
    Path(args.output).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="results"},indent=2))


if __name__=="__main__":
    main()
