"""Bounded adversarial regular-graph formula diagnostic; not a theorem proof."""
from pathlib import Path
from itertools import combinations
import json,time
import numpy as np

def regular_graphs(n,r):
    residual=[r]*n
    masks=[0]*n
    def graphical(seq):
        seq=sorted(seq,reverse=True)
        if sum(seq)%2 or any(x<0 or x>=len(seq) for x in seq):return False
        for k in range(1,len(seq)+1):
            if sum(seq[:k])>k*(k-1)+sum(min(k,x) for x in seq[k:]):return False
        return True
    def rec(v):
        if v==n:
            yield masks.copy();return
        need=residual[v]
        possible=[j for j in range(v+1,n) if residual[j]>0]
        if need>len(possible):return
        for selected in combinations(possible,need):
            for j in selected:
                residual[j]-=1;masks[v]|=1<<j;masks[j]|=1<<v
            residual[v]=0
            if graphical(residual[v+1:]):
                yield from rec(v+1)
            residual[v]=need
            for j in selected:
                residual[j]+=1;masks[v]^=1<<j;masks[j]^=1<<v
    yield from rec(0)

def clique_number(masks):
    best=0
    def rec(candidates,size):
        nonlocal best
        if size+candidates.bit_count()<=best:return
        while candidates:
            p=candidates&-candidates;candidates^=p
            v=p.bit_length()-1
            best=max(best,size+1)
            rec(candidates&masks[v],size+1)
    rec((1<<len(masks))-1,0)
    return best

records=[];falsifier=None
started=time.monotonic()
for n,r in [(6,3),(8,3)]:
    count=0;worst=None
    for masks in regular_graphs(n,r):
        count+=1
        omega=clique_number(masks);mu=1-1/omega
        t=2*r/(r/mu+np.sqrt((r/mu)**2+4*r))
        A=np.array([[(masks[i]>>j)&1 for j in range(n)] for i in range(n)],dtype=float)
        assert np.all(A.sum(axis=1)==r)
        for k in range(n):
            others=[j for j in range(n) if j!=k]
            H=np.zeros((2*n-1,2*n-1));H[:n,:n]=A
            H[n:,n:]=A[np.ix_(others,others)]
            H[k,n:]=A[k,others];H[n:,k]=A[others,k]
            rho=float(np.linalg.eigvalsh(H)[-1]);gap=rho-r-t
            item={'n':n,'r':r,'omega':omega,'root':k,'rho':rho,
                  'claimed_bound':r+t,'gap':gap,
                  'edges':[[i,j] for i in range(n) for j in range(i+1,n) if A[i,j]]}
            if worst is None or gap>worst['gap']:worst=item
            if gap>1e-9:falsifier=item;break
        if falsifier:break
    records.append({'n':n,'r':r,'labelled_graphs_checked':count,'worst':worst})
    if falsifier:break
out={'scope':'bounded finite diagnostic; does not establish quantified graph theorem',
     'records':records,'falsifier':falsifier,'elapsed_seconds':time.monotonic()-started}
Path(__file__).with_name('SMALL_REGULAR_DIAGNOSTIC.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
