"""Actual seed->RX3->RZ3 ancestry host and paired-completion quotient.
Analytical graphs only: no added Hilbert-space vertices or Hamiltonian checks.
No Euclidean geometry is fabricated for the second-level perturbation.
"""
from pathlib import Path
import sys,json
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parent/'helpers'))
from actual_generic_rx_deterministic import rx

def bits(s):
 while s:
  t=s&-s;yield t.bit_length()-1;s^=t

def nextlevel(kind,X,Z,n,ell=3):
 XX,ZZ,qn,F=rx(X if kind=='X' else Z,Z if kind=='X' else X,n,ell)
 own={}
 for i,q in enumerate(qn):own['Q',i]=('X',q[1]) if q[0]=='xe' else ('Q',q[1])
 for i,row in enumerate(XX):
  xs={qn[q][1] for q in bits(row) if qn[q][0]=='xe'};assert len(xs)==1
  own['X',i]=('X',next(iter(xs)))
 for i,row in enumerate(ZZ):
  names=[qn[q] for q in bits(row)]
  if all(q[0]=='xe' for q in names):
   xs={q[1] for q in names};assert len(xs)==1;owner=('X',next(iter(xs)))
  elif any(q[0]=='xe' for q in names):
   qs={q[1] for q in names if q[0]=='qv'};assert len(qs)==1;owner=('Q',next(iter(qs)))
  else:
   endpoints={q[2][1] for q in names};assert len(endpoints)==1
   z=next(iter(endpoints));assert z[0]=='z';owner=('Z',z[1])
  own['Z',i]=owner
 if kind=='Z':
  swap=lambda v:({'X':'Z','Z':'X','Q':'Q'}[v[0]],v[1])
  own={swap(v):swap(p) for v,p in own.items()};XX,ZZ=ZZ,XX
 return XX,ZZ,len(qn),own

levels=[([0b10011,0b11100],[0b10101,0b11010],5)];parents={}
for level,kind in enumerate(('X','Z'),1):
 X,Z,n,owner=nextlevel(kind,*levels[-1]);levels.append((X,Z,n))
 for v,p in owner.items():parents[(level,*v)]=(level-1,*p)
H={};children={}
def edge(G,a,b):
 G.setdefault(a,set());G.setdefault(b,set())
 if a!=b:G[a].add(b);G[b].add(a)
for level,(X,Z,n) in enumerate(levels):
 inc=[[] for _ in range(n)]
 for typ,rows in [('X',X),('Z',Z)]:
  for i,row in enumerate(rows):
   check=(level,typ,i);qs=list(bits(row))
   for q in qs:edge(H,check,(level,'Q',q));inc[q].append(check)
   for u in qs:
    for v in qs:edge(H,(level,'Q',u),(level,'Q',v))
 for checks in inc:
  for a in checks:
   for b in checks:edge(H,a,b)
for v,p in parents.items():edge(H,v,p);children.setdefault(p,[]).append(v)
assert min(map(len,children.values()))>=2
L=len(levels)-1;leafmap={}
def match(v):
 if v[0]==L:leafmap[v]=v;return[v]
 free=[]
 for child in sorted(children[v]):free+=match(child)
 assert len(free)>=2
 leafmap[v]=free.pop();return free
for root in sorted(v for v in H if v[0]==0):match(root)
assert set(leafmap)==set(H) and max(Counter(leafmap.values()).values())<=2
X,Z,n=levels[-1];supp={('X',i):set(bits(s)) for i,s in enumerate(X)}|{('Z',i):set(bits(s)) for i,s in enumerate(Z)}
inc=[set() for _ in range(n)]
for a,qs in supp.items():
 for q in qs:inc[q].add(a)
def selected(v):
 leaf=leafmap[v];typ,i=leaf[1:]
 if typ=='Q':return min(inc[i]),i
 a=(typ,i);return a,min(supp[a])
Gc={a:set() for a in supp};Gq_projection={q:set() for q in range(n)}
for v,ns in H.items():
 a,x=selected(v)
 for w in sorted(ns):
  b,y=selected(w);edge(Gc,a,b);edge(Gq_projection,x,y)
# Final paired completion: support cliques and complete bipartite links for Gc.
Gq={q:set() for q in range(n)}
for a,qs in supp.items():
 for x in sorted(qs):
  for y in sorted(qs):edge(Gq,x,y)
 for b in sorted(Gc[a]):
  for x in sorted(qs):
   for y in sorted(supp[b]):edge(Gq,x,y)
assert all(ns<=Gq[q] for q,ns in Gq_projection.items())
assert all(selected((L,*a))[0]==a for a in supp)
assert all(selected((L,'Q',q))[1]==q for q in range(n))
def connected(G,A):
 todo=set(A);stack=[min(todo)];todo.remove(stack[0])
 while stack:
  v=stack.pop()
  for w in sorted(G[v]&todo):todo.remove(w);stack.append(w)
 return not todo
for a,ns in Gc.items():
 for b in ns:assert connected(Gq,supp[a]|supp[b])
for q,ns in Gq.items():
 for t in ns:assert connected(Gc,inc[q]|inc[t])
# Nonexpansion of each host edge under the check projection.
for v,ns in H.items():
 a,_=selected(v)
 for w in sorted(ns):
  b,_=selected(w);assert a==b or b in Gc[a]
result=dict(levels=[dict(n=n,X=len(X),Z=len(Z)) for X,Z,n in levels],host_vertices=len(H),
 host_max_degree=max(map(len,H.values())),minimum_children=min(map(len,children.values())),
 maximum_children=max(map(len,children.values())),leaf_projection_max_fiber=max(Counter(leafmap.values()).values()),
 real_check_vertices=len(Gc),real_qubit_vertices=len(Gq),check_supergraph_max_degree=max(map(len,Gc.values())),
 completed_qubit_supergraph_max_degree=max(map(len,Gq.values())),
 check_projection_max_fiber=max(Counter(selected(v)[0] for v in H).values()),
 qubit_projection_max_fiber=max(Counter(selected(v)[1] for v in H).values()),
 all_host_edges_check_nonexpanding=True,all_real_vertices_fixed=True,
 both_support_connectivity_implications_verified=True,
 projected_qubit_edges_retained_by_completion=True,physical_nearness_edges_added=False)
print(json.dumps(result,indent=2));Path(__file__).with_name('actual_host_quotient_deterministic_results.json').write_text(json.dumps(result,indent=2))
