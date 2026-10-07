"""Exact arithmetic and coordinate-transcription fixtures, not a theorem checker."""
from collections import deque
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def line_of_point(p,a,q):
    t,y,z,w,v=p
    b=(y+a*t)%q
    return (a,b,(z+b*t)%q,(w+a*y)%q,(v+a*z)%q)

def point_of_line(l,t,q):
    a,b,c,d,e=l
    y=(b-a*t)%q; z=(c-b*t)%q
    return (t,y,z,(d-a*y)%q,(e-a*z)%q)

fixtures=[]
for q in (3,5):
    pts=list(product(range(q),repeat=5)); ids={p:i for i,p in enumerate(pts)}; n=len(pts)
    adj=[[] for _ in range(2*n)]
    match=set()
    for p in pts:
        l=line_of_point(p,p[0],q); match.add(l)
        assert point_of_line(l,l[0],q)==p
        for a in range(q):
            l=line_of_point(p,a,q); j=n+ids[l]
            adj[ids[p]].append(j); adj[j].append(ids[p])
            assert point_of_line(l,p[0],q)==p
    assert len(match)==n
    assert all(len(es)==q for es in adj)
    # The neighbours of each label must be one full affine line.
    for l in pts:
        v0=point_of_line(l,0,q); v1=point_of_line(l,1,q)
        direction=tuple((b-a)%q for a,b in zip(v0,v1))
        for t in range(q):
            assert point_of_line(l,t,q)==tuple((a+t*d)%q for a,d in zip(v0,direction))
    short_cycle=False
    for root in range(n):
        depths={root:0}; parents={root:-1}; todo=deque([root])
        while todo:
            u=todo.popleft()
            if depths[u]>=4: continue
            for v in adj[u]:
                if v not in depths:
                    depths[v]=depths[u]+1; parents[v]=u; todo.append(v)
                elif parents[u]!=v and parents.get(v)!=u:
                    if depths[u]+depths[v]+1<=8: short_cycle=True
    assert not short_cycle
    fixtures.append({'q':q,'point_count':n,'label_count':n,'edge_count':n*q,
                     'perfect_matching':True,'affine_lines':True,
                     'no_cycle_up_to_8_fixture':True})
q=2**61-1
s=4
for _ in range(59): s=(s*s-2)%q
assert s==0
c=F(1,100000); r=1200000
m=q**5; N=(q//10)**5
mu=F((q-1)*N,m)
assert q>=16*r*r/c and N>=F(9,10)*c*m and mu>=8*r*r
failure_bound=F(16*r,c*q)
assert failure_bound<=F(1,r)
# With |E| <= m/(2r), using the entire conservative E budget:
Delta_lower=F(N*r,4)-2*m-F(m,2)
assert Delta_lower>=F(m,5)
E_ceiling=m//(2*r)
Delta_integer_budget=F(N*r,4)-2*m-r*E_ceiling
assert Delta_integer_budget>=Delta_lower
ledger={
 'purpose':'Transcription fixtures and exact integer/rational ledger; no incidence or presentation emitted.',
 'fixtures':fixtures,
 'parameters':{'h':5,'q':q,'r':r,'c':'1/100000','S_size':q//10,
               'q_lucas_lehmer_iterations':59,'q_lucas_lehmer_residue':s},
 'bounds':{'mu_ge_8r2':True,'N_ge_0.9cm':True,'Delta_ge_m_over_5':True,
           'admissible_affine_map_probability_at_least':'1 - 1/1200000',
           'failure_bound_exact':str(failure_bound),
           'm_decimal_digits':len(str(m)),'N_decimal_digits':len(str(N)),
           'incidences_decimal_digits':len(str(N*(q-1))),
           'triangles_upper_decimal_digits':len(str(N*(q-1)*r*r)),
           'x_edges_decimal_digits':len(str(N*r*r))}}
Path('work/scouts/groups_sources/groups_checks.json').write_text(json.dumps(ledger,indent=2)+'\n')
print(json.dumps(ledger,indent=2))
