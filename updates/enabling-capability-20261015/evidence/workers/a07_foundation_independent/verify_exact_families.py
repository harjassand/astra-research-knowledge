#!/usr/bin/env python3
"""Replay finite combinatorial identities and formula-based asymptotics.

Integer family/count/negative-determinant checks are exact. Entropies and
variance comparisons use floats as sanity checks; proofs are in
EXACT_RESULTS.txt. Large examples are evaluated by formulas, not enumerated.
"""
from collections import Counter
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import time


def ordinal(d, L):
    return list(range(1 << d)) + [(1 << (d+j))-1 for j in range(1,L+1)]


def counts(f):
    return Counter(a|b for a in f for b in f)


def variance(f):
    n=len(f)
    r=counts(f)
    assert set(r)==set(f)
    c=[[math.log(r[a|b]) for b in f] for a in f]
    mean=[sum(row)/n for row in c]
    grand=sum(mean)/n
    return sum((c[i][j]-mean[i]-mean[j]+grand)**2
               for i in range(n) for j in range(n))/(n*n)


def product(f, width, k):
    return [sum(x << (j*width) for j,x in enumerate(xs))
            for xs in itertools.product(f,repeat=k)]


def main():
    start=time.perf_counter()
    exact_count_checks=0
    max_projection_bound_error=0
    for d in range(1,6):
        for L in [1,2,4,7,10]:
            f=ordinal(d,L)
            r=counts(f)
            M=1<<d
            N=M+L
            assert set(r)==set(f)
            assert sum(r.values())==N*N
            for S in range(M):
                assert r[S]==3**S.bit_count()
                exact_count_checks+=1
            for j in range(1,L+1):
                assert r[(1<<(d+j))-1]==2*(M+j)-1
                exact_count_checks+=1
            p=max(Fraction(sum(bool(S&(1<<i)) for S in f),N)
                  for i in range(d+L))
            assert p==Fraction(M//2+L,N)
            w=M/N
            g11=.75*d*math.log(3)
            g10=sum(math.log(2*(M+j)-1) for j in range(1,L+1))/L
            g00=sum((2*j-1)*math.log(2*(M+j)-1) for j in range(1,L+1))/(L*L)
            delta=g11-2*g10+g00
            v=variance(f)
            bound=w*w*(1-w)**2*delta*delta
            assert v+1e-12>=bound
            h0=-sum((n/(N*N))*math.log(n/(N*N)) for n in r.values())
            a0=.75*math.log(3)-math.log(2)
            assert math.log(N)-h0<=math.log(2)+a0*d*w*w+1e-12

    # Exact integer signs certify the small principal minors.
    determinants=[]
    for d in range(3,17):
        rU=3**d
        rT=2**(d+1)+1
        det=Fraction(rT-rU,rU*rT*rT)
        assert det<0
        determinants.append({"d":d,"minor_determinant":str(det),
                             "max_frequency":str(Fraction(2**(d-1)+1,2**d+1))})

    tensor_checks=[]
    base=[0,1,2,3,7]
    v=variance(base)
    for k in [1,2,3]:
        f=product(base,3,k)
        vk=variance(f)
        assert abs(vk-k*v)<2e-11
        tensor_checks.append({"k":k,"N":len(f),"variance":vk,
                              "expected_variance":k*v,
                              "variance_over_logN_squared":vk/math.log(len(f))**2})

    # d=t^4, L=t^3*2^d is an exact integer subsequence of Theorem C.
    # No 2^d-sized family is materialized for this formula evaluation.
    a0=.75*math.log(3)-math.log(2)
    sparse_cube=[]
    for t in [2,4,8,16,32,64,128]:
        d=t**4
        alpha=t**3
        w=1/(1+alpha)
        delta_lower=a0*d-math.log(2)-2*math.log(1+alpha)
        variance_lower=w*w*(1-w)**2*max(delta_lower,0)**2
        gain_upper=math.log(2)+a0*d*w*w
        sparse_cube.append({"t":t,"d":d,"L_over_2_to_d":alpha,
                           "variance_lower_bound":variance_lower,
                           "all_couplings_gain_upper_bound":gain_upper,
                           "gain_over_variance_upper_bound":gain_upper/variance_lower
                            if variance_lower else None,
                           "log_family_size":d*math.log(2)+math.log(1+alpha)})

    near_half=[]
    alpha=1/64
    w=1/(1+alpha)
    for d in [100,1000,10000,100000]:
        delta_lower=a0*d-math.log(2)-2*math.log(1+alpha)
        v_lower=w*w*(1-w)**2*delta_lower**2
        gain_upper=math.log(2)+a0*d*w*w
        near_half.append({"d":d,"L_over_2_to_d":alpha,
                          "max_frequency":(.5+alpha)/(1+alpha),
                          "variance_lower_bound":v_lower,
                          "all_couplings_gain_upper_bound":gain_upper,
                          "gain_over_variance_upper_bound":gain_upper/v_lower})
    output={"status":"PASS",
            "scope":"finite exact identities plus floating sanity checks; analytic proofs separate",
            "exact_multiplicity_checks":exact_count_checks,
            "negative_principal_minors":determinants,
            "tensor_variance_checks":tensor_checks,
            "large_sparse_cube_formula_checks":sparse_cube,
            "near_half_formula_checks":near_half,
            "elapsed_seconds":time.perf_counter()-start}
    Path("verification_results.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({k:v for k,v in output.items() if not isinstance(v,list)},indent=2))
    print("Largest sparse-cube formula:",json.dumps(sparse_cube[-1]))
    print("Largest near-half formula:",json.dumps(near_half[-1]))


if __name__=="__main__":
    main()
