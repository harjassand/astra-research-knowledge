#!/usr/bin/env python3
"""Exponential diagnostic oracle for two-source matrix-sum invariants."""
import json,time
from pathlib import Path
from binary_modules import inverse,compose,flat,unflat,span
from raw_matrix_trace import transpose

def walsh(a):
    s=1
    while s<len(a):
        for i in range(0,len(a),2*s):
            for j in range(i,i+s):
                x,y=a[j],a[j+s]; a[j]=x+y; a[j+s]=x-y
        s*=2

def main(n=3):
    start=time.perf_counter(); d=n*n; size=1<<d
    matrices=[unflat(x,n) for x in range(size)]; ranks=[len(span(A)) for A in matrices]
    W=[0]*(1<<(2*d))
    for x,A in enumerate(matrices):
        B=inverse(A)
        if B is not None: W[flat(transpose(A),n)|(flat(transpose(B),n)<<d)]=1
    walsh(W); classes={}; failures=[]
    for a,A in enumerate(matrices):
        for b,B in enumerate(matrices):
            AB=compose(A,B); I=[1<<i for i in range(n)]; p=I; qs=[]
            for _ in range(n): p=compose(AB,p); qs.append(len(span(p)))
            J=[x^y for x,y in zip(AB,I)]; p=I; ones=[]
            for _ in range(n): p=compose(J,p); ones.append(len(span(p)))
            irr=[]
            for g in (7,11,13):
                cur=[0]*n
                for j in reversed(range(g.bit_length())):
                    cur=compose(cur,AB)
                    if (g>>j)&1: cur=[x^y for x,y in zip(cur,I)]
                irr.append(len(span(cur)))
            key=(ranks[a],ranks[b],tuple(qs),tuple(ones),tuple(irr)); val=W[a|(b<<d)]
            if key in classes and classes[key][0]!=val:
                if len(failures)<10: failures.append(dict(key=key,first=classes[key],second=(val,a,b)))
            else: classes.setdefault(key,(val,a,b))
    report=dict(matrix_rank=n,all_source_pairs=size*size,summary_classes=len(classes),
                failures=failures,seconds=time.perf_counter()-start)
    Path(__file__).with_name('singular_pair_probe_results.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
