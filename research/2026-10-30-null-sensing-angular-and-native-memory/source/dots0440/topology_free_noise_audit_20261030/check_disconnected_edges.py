"""Finite exhaustive algebra regression; not a proof of confinement/lifetime."""
import json
from itertools import combinations
from pathlib import Path

def components(mask,n):
    out=[]
    while mask:
        bit=mask&-mask; mask^=bit; c=bit; frontier=bit
        while frontier:
            neigh=((frontier<<1)|(frontier>>1))&((1<<n)-1)&mask
            mask^=neigh;c|=neigh;frontier=neigh
        out.append(c)
    return out

def syndrome(x,n):
    return (x^(x>>1))&((1<<(n-1))-1)

report={}
for n in [8,9]:
    reps={}
    for e in range(1<<n):
        syn=syndrome(e,n)
        if syn not in reps or (e.bit_count(),e)<(reps[syn].bit_count(),reps[syn]): reps[syn]=e
    ps=[0]+[1<<i for i in range(n)]+[(1<<i)|(1<<j) for i,j in combinations(range(n),2)]
    counts=dict(edges=0,disconnected_support_edges=0,union_components=0,nontrivial_kernel_components=0)
    for e in reps.values():
      for p in ps:
        f=reps[syndrome(e^p,n)]
        counts['edges']+=1
        if len(components(p,n))>1: counts['disconnected_support_edges']+=1
        for k in components(e|p|f,n):
          counts['union_components']+=1
          assert syndrome((e^p^f)&k,n)==0
          assert (f&k).bit_count()<=((e^p)&k).bit_count()
          assert k.bit_count()<=2*((e&k).bit_count()+(p&k).bit_count())
          assert all(not(c&k) or (c&k)==c for c in components(e,n))
          if ((e^p^f)&k):
            counts['nontrivial_kernel_components']+=1
            assert k.bit_count()>=n
    report[str(n)]=counts
report['scope']='Path repetition-check algebra only; includes disconnected 2-site supports and minimum-representative tie-breaking. Not a confinement or quantum-memory simulation.'
out=Path(__file__).with_name('disconnected_edge_checks.json')
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
