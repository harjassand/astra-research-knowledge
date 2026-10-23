#!/usr/bin/env python3
"""Bounded exact enumeration of the NEW Bell-ancilla primitive, no tree rerun."""
from itertools import product
from fractions import Fraction
from collections import Counter
import json,time

def main():
    start=time.perf_counter();basis_cases=0;coherence_cases=0;subgroup_cases=0
    for D,n in [(2,3),(3,2),(4,2),(6,2)]:
        rows=list(product(range(D),repeat=n))
        # Enumerate a small deterministic selection of rows, including units,
        # zero and nonunit entries at composite moduli.
        selected=rows if len(rows)<=40 else rows[::max(1,len(rows)//32)]
        digits=list(product(range(D),repeat=n))
        for h in selected:
            dot=lambda x:sum(a*b for a,b in zip(h,x))%D
            for xa in digits:
                for xb in digits:
                    actual=Counter(((z+dot(xa))%D,(z+dot(xb))%D)
                                   for z in range(D))
                    for a,b in product(range(D),repeat=2):
                        predicted=int((b-a)%D==(dot(xb)-dot(xa))%D)
                        assert actual[(a,b)]==predicted
                        basis_cases+=1
            # For every nonzero difference, uniform-row collision <=1/2.
        for e in digits:
            if not any(e):continue
            zero=sum(sum(a*b for a,b in zip(h,e))%D==0 for h in rows)
            assert Fraction(zero,len(rows))<=Fraction(1,2)
            subgroup_cases+=1
        # Prefix Bell coherence survives: differences independent of each
        # coherent prefix digit, even when the query touches mixed tail.
        for k in range(1,n+1):
            for h in selected:
                for u in product(range(D),repeat=n-k):
                    for v in product(range(D),repeat=n-k):
                        vals=set()
                        for x in product(range(D),repeat=k):
                            xa=x+u;xb=x+v
                            vals.add(sum(t*(b-a) for t,a,b in zip(h,xa,xb))%D)
                        assert len(vals)==1
                        coherence_cases+=1
    out={"status":"PASS","scaled_Kraus_basis_cases":basis_cases,
         "prefix_coherence_cases":coherence_cases,
         "nonzero_vector_collision_cases":subgroup_cases,
         "moduli":[2,3,4,6],"wall_seconds":time.perf_counter()-start,
         "scope":"new primitive exact finite admissions only; no historical search suite rerun"}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
