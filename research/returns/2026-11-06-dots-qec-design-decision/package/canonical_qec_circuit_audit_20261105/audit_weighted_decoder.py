"""Check the projected pilot's weighted decoder and logical event independently."""
import sys,json,time,heapq,random
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'canonical_qec_circuit_gate_20261105'))
from tilted_pilot import CircuitModel
start=time.perf_counter();G=json.loads((root/'canonical_qec_circuit_gate_20261105/d3_r3_p1_1000_graph.json').read_text());m=CircuitModel(G);nd=G['internal_vertices'];N=len(m.edges);costs=np.array(G['costs']);cols=[]
for ends in m.edge_checks:
 mask=0
 for j in ends:mask^=1<<j
 cols.append(mask)
# Exact syndrome-space shortest paths, independent of matching.
best=[10**9]*(1<<nd);best[0]=0;heap=[(0,0)]
while heap:
 dist,s=heapq.heappop(heap)
 if dist!=best[s]:continue
 for col,w in zip(cols,G['costs']):
  z=s^col;new=dist+w
  if new<best[z]:best[z]=new;heapq.heappush(heap,(new,z))
syndromes=np.array([[(mask>>j)&1 for j in range(nd)] for mask in range(1<<nd)],dtype=np.uint8)
corrections=m.m.decode_batch(syndromes).astype(np.uint8)
assert np.array_equal(corrections@costs,np.array(best))
for idx,c in enumerate(corrections):
 s=0
 for k in np.flatnonzero(c):s^=cols[k]
 assert s==idx
# Check observable versus gauge-cut event and weighted witness with random fault
# vectors, including much higher fault density than the intended rare regime.
rng=random.Random(57207);witnesses=0
logical=np.array([e['logical'] for e in G['errors']],dtype=np.uint8)
for _ in range(10000):
 e=np.array([rng.randrange(5)==0 for k in range(N)],dtype=np.uint8);c=m.decode(e);res=e^c
 original_logical=int(res@logical)%2;cut_logical=int(res[m.cut].sum())%2
 assert original_logical==cut_logical
 wit=m.witness(e)
 assert bool(wit)==bool(original_logical)
 if wit:
  witnesses+=1;score=int(np.sum(costs[list(wit)]*(2*e[list(wit)].astype(int)-1)));assert score>=0
out={'status':'PASS: exact d3 weighted decoder/event audit','syndromes_exhausted':1<<nd,'weighted_correction_costs_match':True,'fault_vectors_tested':10000,'logical_witnesses_checked':witnesses,'decoder_scope':'Minimum total integer edge cost (4 or 5), not exact likelihood-weight MWPM or a decoder exploiting the discarded detector basis.','elapsed_seconds':time.perf_counter()-start}
Path(__file__).with_name('weighted_decoder_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
