#!/usr/bin/env python3
"""New bounded scalar checks; stdlib only, no predecessor suites."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math
import time
from itertools import product

HERE = Path(__file__).resolve().parent

def h(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log(x) - (1-x) * math.log1p(-x)

def entropy(ps):
    return -sum(p*math.log(p) for p in ps if p)

def stopped(m, lam):
    invd = 2.0 ** (-m)
    q = 1-lam
    logd = m*math.log(2)
    w = lam+q*invd
    e = lam+q*invd*invd
    small_mass = q*invd*(1-invd)
    v = w*logd + e*math.log(e/w)
    if small_mass:
        v += small_mass*(math.log(q)-2*logd-math.log(w))
    H = -w*math.log(w) - q*(1-invd)*math.log(q)
    H += q*math.log(2)*(2-(m+2)*invd)
    rate_tail=max(0.0,v-H)
    return dict(m=m, lambda_high=lam, equality_mass=w, gross_v=v,
                classification_entropy=H, rate_tail=rate_tail,
                deficit=lam*logd-rate_tail,
                gap_bound=h(lam)+q*math.log(5),
                limiting_displayed_gap=h(lam)+2*q*math.log(2))

def coordinate(m, t, lam, D=2):
    n=m-t
    if n == 0:
        return 0.0
    s=lam+(1-lam)*D**(-t)
    pure=lam/s
    logdim=n*math.log(D)
    inverse=math.exp(-logdim)
    small_weight=(1-pure)*inverse*inverse
    F=pure+small_weight
    other_mass=(1-pure)*(1-inverse*inverse)
    S=-F*math.log(F)
    if other_mass:
        S-=other_mass*(math.log1p(-pure)-2*logdim)
    return s*(logdim-S)

def full_rank(rows, n):
    basis=[]
    for row in rows:
        for old in basis:
            row=min(row,row^old)
        if row:
            basis.append(row)
            basis.sort(reverse=True)
    return len(basis)==n

def general_dimension_admissions():
    records=[]
    for d in range(2,9):
        n=(d-1).bit_length()
        matrices=[rows for rows in product(range(1<<n),repeat=n)
                  if full_rank(rows,n)]
        histograms=[]
        for rows in matrices:
            hist=[0]*(n+1)
            for j in range(d):
                for k in range(d):
                    xor=j^k
                    first=next((i+1 for i,row in enumerate(rows)
                                if (row & xor).bit_count()%2),0)
                    hist[first]+=1
            assert hist[0]==d
            histograms.append(hist)
        totals=[sum(hist[ell] for hist in histograms) for ell in range(n+1)]
        assert totals[0]==len(matrices)*d
        for ell in range(1,n+1):
            assert Fraction(totals[ell],len(matrices)*d*(d-1))==Fraction(2**(n-ell),2**n-1)
        for lam in (.1,.5,.9):
            q=1-lam
            probabilities=[[lam+q*hist[0]/d**2]+[q*x/d**2 for x in hist[1:]]
                           for hist in histograms]
            entropies=list(map(entropy,probabilities))
            average=[sum(p[ell] for p in probabilities)/len(matrices)
                     for ell in range(n+1)]
            bound=h(lam+q/d)+2*q*(1-1/d)*math.log(2)
            assert sum(entropies)/len(entropies)<=entropy(average)+1e-12
            assert min(entropies)<=bound+1e-12
            records.append(dict(d=d,lambda_high=lam,n_bits=n,
                                matrices=len(matrices),minimum_entropy=min(entropies),
                                entropy_bound=bound))
    return records

def main():
    start=time.monotonic()
    counts={"exact_classifier_normalizations":0,
            "exact_stopped_chain_rule_admissions":0,
            "equality_spectrum_admissions":0,
            "constant_gap_checks":0,
            "coordinate_bounds":0}
    for m in range(1,31):
        for lamQ in (Fraction(1,10),Fraction(1,3),Fraction(1,2),
                     Fraction(2,3),Fraction(9,10)):
            qQ=1-lamQ
            probsQ=[lamQ+qQ/Fraction(2**m)]
            probsQ.extend(qQ/Fraction(2**j) for j in range(1,m+1))
            assert sum(probsQ)==1
            counts["exact_classifier_normalizations"]+=1
            probs=list(map(float,probsQ))
            chain=0.0
            for ell in range(1,m+1):
                remaining=probs[0]+sum(probs[ell:])
                chain+=remaining*h(probs[ell]/remaining)
            assert math.isclose(chain,entropy(probs),rel_tol=1e-12,abs_tol=1e-12)
            counts["exact_stopped_chain_rule_admissions"]+=1
            lam=float(lamQ)
            result=stopped(m,lam)
            assert math.isclose(result["classification_entropy"],entropy(probs),
                                rel_tol=1e-12,abs_tol=1e-12)
            if m <= 10:
                d=2**m
                w=result["equality_mass"]
                eigen=[(lam+(1-lam)/d**2)/w]
                eigen.extend([(1-lam)/d**2/w]*(d-1))
                assert math.isclose(sum(eigen),1,rel_tol=1e-12,abs_tol=1e-12)
                v=w*(math.log(d)-entropy(eigen))
                assert math.isclose(v,result["gross_v"],rel_tol=1e-11,abs_tol=1e-11)
                counts["equality_spectrum_admissions"]+=1
            assert result["deficit"] >= -1e-10
            assert result["deficit"] <= result["gap_bound"]+1e-10
            counts["constant_gap_checks"]+=1
            for t in range(m+1):
                s=lam+(1-lam)*2.0**(-t)
                ic=coordinate(m,t,lam)
                f=(lam*t+(1-lam)*2.0**(-t)*(m-t))*math.log(2)
                actual=lam*m*math.log(2)-ic
                assert actual>=f-1e-10
                assert actual<=f+s*h(lam/s)+1e-10
                counts["coordinate_bounds"]+=1
    table=[]
    for m in (1,2,4,8,16,32,64,128,256,512,1024,4096,16384):
        row=stopped(m,0.5)
        if m<=1024:
            rates=[coordinate(m,t,.5) for t in range(m+1)]
            best=max(range(len(rates)),key=lambda t:rates[t])
            row.update(coordinate_best_t=best,
                       coordinate_deficit=.5*m*math.log(2)-max(0,max(rates)))
        table.append(row)
    assert abs(table[-1]["deficit"]-table[-1]["limiting_displayed_gap"])<1e-10
    result={"status":"PASS","counts":counts,"table":table,
            "general_dimension_gl_admissions":general_dimension_admissions(),
            "scope":"Exact rational probabilities; floating scalar entropy admissions. No quantum coding implementation.",
            "proof_sha256":hashlib.sha256((HERE/"PROOF.txt").read_bytes()).hexdigest(),
            "wall_seconds":time.monotonic()-start}
    (HERE/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
