import sys,json,time,hashlib,os
from pathlib import Path
import numpy as np,pymatching
from scipy.sparse import csr_matrix
BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE/'canonical_qec_circuit_gate_20261105'))
from tilted_pilot import CircuitModel
G=json.loads((BASE/'qec_fault_tuple_20261105/d21/input_graph.json').read_text()); old=CircuitModel(G);cut=set(old.cut)
small=pymatching.Matching()
for i,ends in enumerate(old.edge_checks):
 kwargs=dict(fault_ids={0} if i in cut else set(),weight=G['costs'][i])
 if len(ends)==2:small.add_edge(*ends,**kwargs)
 else:small.add_boundary_edge(ends[0],**kwargs)
rr=[];cc=[]
for i,x in enumerate(old.edge_checks):rr.extend(x);cc.extend([i]*len(x))
H=csr_matrix((np.ones(len(rr),np.uint8),(rr,cc)),shape=(len(old.checks),len(old.edges)))
rng=np.random.default_rng(553)
N=4000;ok=0;times=[]
for qq in [.001,.003,.01,.03]:
 e=(rng.random((1000,len(old.edges)))<qq).astype(np.uint8);s=np.asarray((H@e.T).T,dtype=np.uint8)%2
 start=time.perf_counter();a=old.m.decode_batch(s)[:,old.cut].sum(1)%2;t1=time.perf_counter()-start
 start=time.perf_counter();b=small.decode_batch(np.packbits(s,axis=1,bitorder='little'),bit_packed_shots=True,bit_packed_predictions=True)[:,0]&1;t2=time.perf_counter()-start
 assert np.array_equal(a,b);ok+=len(a);times.append(dict(q=qq,original_seconds=t1,parity_seconds=t2))
out=dict(verified_patterns=ok,random_seed=553,graph_sha256=hashlib.sha256((BASE/'qec_fault_tuple_20261105/d21/input_graph.json').read_bytes()).hexdigest(),checks='Same edge insertion order, endpoints and costs; replace correction-edge vector fault IDs by xor logical cut parity; random identity check only, not exhaustive',timings=times)
(Path(__file__).parent/'optimization_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
