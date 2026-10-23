#!/usr/bin/env python3
"""Exact finite admission of nested-prefix conditional freshness for any D."""
import itertools, json, time
from collections import Counter

def tuples(D,n): return itertools.product(range(D),repeat=n)
def check(D,L,k,js):
    # Complete joint laws; each queried threshold <=k contributes one D-ary
    # digit and each >k contributes two. Uniformity of all such coordinates
    # proves conditional freshness in arbitrary distinct order.
    counts=Counter()
    for a in tuples(D,L-1):
        for tail in tuples(D,L-k):
            e=[0]*(k-1)+list(tail)
            sa=tuple(sum(a[:j-1])%D for j in js)
            de=tuple(sum(e[:j-1])%D for j in js if j>k)
            counts[sa+de]+=1
    exponent=len(js)+sum(j>k for j in js)
    expected=D**exponent
    assert len(counts)==expected,(D,L,k,js,len(counts),expected)
    assert len(set(counts.values()))==1,(D,L,k,js)
    return 1

def main():
    start=time.perf_counter(); n=0
    for D,L in [(2,5),(3,4),(4,4),(6,3)]:
        for k in range(1,L+1):
            thresholds=list(range(2,L+1))
            # All ordered lists up to length3. Reverse/adaptive paths reduce
            # to a fixed such list after conditioning on prior transcript.
            for r in range(1,min(3,len(thresholds))+1):
                for js in itertools.permutations(thresholds,r):
                    n+=check(D,L,k,js)
    result={"status":"PASS","exact_nested_joint_uniformity_cases":n,
            "moduli":[2,3,4,6],"wall_seconds":time.perf_counter()-start,
            "scope":"finite exact counting admission; analytic proof supplies general/adaptive claim"}
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
