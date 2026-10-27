from itertools import combinations
from math import comb
import json

PRIME=1000003

def exact_modular_rank(rows,p):
    rows=[[v%p for v in row] for row in rows]
    r=0
    for c in range(len(rows[0])):
        pivot=next((i for i in range(r,len(rows)) if rows[i][c]),None)
        if pivot is None:
            continue
        rows[r],rows[pivot]=rows[pivot],rows[r]
        inv=pow(rows[r][c],p-2,p)
        rows[r]=[(v*inv)%p for v in rows[r]]
        for i in range(r+1,len(rows)):
            factor=rows[i][c]
            if factor:
                rows[i]=[(a-factor*b)%p for a,b in zip(rows[i],rows[r])]
        r+=1
        if r==len(rows):
            break
    return r

checks=[]
for n in range(1,9):
    for d in range(0,min(3,n)+1):
        subsets=[frozenset(S) for j in range(d+1) for S in combinations(range(n),j)]
        G=[[2**(n-len(S|T)) for T in subsets] for S in subsets]
        target=sum(comb(n,j) for j in range(d+1))
        rank=exact_modular_rank(G,PRIME)
        assert rank==target
        checks.append({'n':n,'d':d,'dimension_lower_bound':target,'rank_mod_prime':rank})
print(json.dumps({'prime':PRIME,'checks':checks,'passed':len(checks)},indent=2))
