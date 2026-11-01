"""Exhaustive exact-gas bijection on the actual RX ell3 Bell fixture.
Retains all12 original Z-check couplings, including the redundant check.
Uses finite full-stencil histories, not an independently assumed contour gas.
"""
import contextlib,io,json,math
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
 import actual_rx_recognizer_fixture as f
host={v:i for i,v in enumerate(sorted(f.C.adj,key=repr))}
def code(M):return sum(1<<host[v] for v in M)
polymers={};decompositions={};accept=[]
for s in range(1<<f.r):
 ok,vals,M=f.C.run(s)
 if not ok:continue
 accept.append(s);parts=f.C.components(M);key=[]
 for p in parts:
  top=sum(1<<j for j in range(f.r) if s>>j&1 and ('W',('s0',j)) in p)
  item=code(p)
  if top in polymers:assert polymers[top]==item
  polymers[top]=item;key.append(top)
 key=tuple(sorted(key));assert key not in decompositions;decompositions[key]=s
labels=sorted(polymers);adj={s:set() for s in labels};pairs=[]
for i,s in enumerate(labels):
 assert (s,) in decompositions
 for t in labels[:i]:
  if polymers[s]&polymers[t]:continue
  pair=tuple(sorted((s,t)));assert pair in decompositions
  assert not s&t and decompositions[pair]==s^t
  adj[s].add(t);adj[t].add(s);pairs.append(pair)
# If there were a compatible triple it would be a triangle in this graph.
assert all(not(adj[s]&adj[t]) for s,t in pairs)
assert len(accept)==1+len(labels)+len(pairs)
assert set(decompositions)=={()}|{(s,) for s in labels}|set(pairs)
# Nonuniform original couplings; the positive gas must retain every term.
J=[1+j/17 for j in range(f.r)];beta=2.3
def energy(s):return sum(j for i,j in enumerate(J) if s>>i&1)
w={s:math.exp(-beta*energy(s)) for s in labels}
Zphysical=sum(math.exp(-beta*energy(s)) for s in accept)
Zpolymer=1+sum(w.values())+sum(w[s]*w[t] for s,t in pairs)
assert abs(Zphysical-Zpolymer)<=1e-12*Zphysical
result=dict(valid_syndromes=len(accept),distinct_connected_polymers=len(labels),compatible_pairs=len(pairs),
 compatible_triples=0,exact_decomposition_bijection=True,original_check_couplings=J,beta=beta,
 physical_partition_function=Zphysical,polymer_partition_function=Zpolymer,
 relative_partition_discrepancy=abs(Zphysical-Zpolymer)/Zphysical)
print(json.dumps(result,indent=2))
Path(__file__).with_name('actual_rx_polymer_bijection_results.json').write_text(json.dumps(result,indent=2))
