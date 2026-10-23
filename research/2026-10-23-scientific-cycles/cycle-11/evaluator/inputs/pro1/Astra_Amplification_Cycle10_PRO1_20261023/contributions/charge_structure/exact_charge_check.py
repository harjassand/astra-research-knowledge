#!/usr/bin/env python3
"""Exact bounded checks of the new all-k charge identity; no asymptotic fit."""
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import json,time,resource

ROOT=Path(__file__).resolve().parent
def abs_walk(j):
    return Fraction(sum(comb(j,q)*abs(2*q-j) for q in range(j+1)),2**j)

def formula(k):
    return sum((Fraction(k-1-j,8)*abs_walk(j) for j in range(1,k-1)),Fraction())

def direct(k):
    # 4 * normalized color trace of H^2, computed by the original exact
    # h>d / h=d / h<d token classification. No matrix eigenvalue tolerance.
    sum_square=0
    sum_charge_square=0
    for x in product((0,1),repeat=k):
        square4=0
        prefix=0; prefix_min=0
        for i in range(k):
            h=prefix-prefix_min
            mid=0; mid_min=0
            for j in range(i+1,k):
                if x[i]!=x[j]:
                    d=-mid_min
                    square4 += 4 if h>d else 1 if h==d else 0
                mid += 2*x[j]-1
                mid_min=min(mid_min,mid)
            prefix += 2*x[i]-1
            prefix_min=min(prefix_min,prefix)
        sum_square += square4
        sum_charge_square += (2*sum(x)-k)*square4
    return Fraction(sum_square,4*2**k),Fraction(sum_charge_square,8*2**k)

def encode(q):
    return {'exact':str(q),'float':float(q)}

def main():
    begin=time.perf_counter()
    rows=[]
    for k in range(2,12):
        v,c=direct(k); f=formula(k)
        assert c==f,(k,c,f)
        collision=sum((Fraction(k-1-n)*Fraction(comb(n,n//2),2**n) if n%2==0 else Fraction()) for n in range(k-1))
        v_expected=Fraction(k*(k-1),8)-collision/8
        assert v==v_expected,(k,v,v_expected)
        rows.append({'k':k,'second_moment':encode(v),'charge_second_moment':encode(c),'identity':'PASS'})
    report={'status':'PASS','rows':rows,'wall_seconds':time.perf_counter()-begin,'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Exact finite checks diagnose the new charge identity implementation. All-length proof and asymptotic are analytic; this is not a capacity or code replay.'}
    p=ROOT/'exact_charge_check.json';p.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
