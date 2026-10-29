from finite_pruned_receiver_v1 import *
from pathlib import Path
import numpy as np,json,gzip,random,time
P=Path(__file__).parent;results=[];start=time.time()
for seed in [7301,7302,7303]:
 with gzip.open(P/f'memory_certificates_seed{seed}_N4096_v2.json.gz','rt') as f:last=json.load(f)[-1]
 records=np.load(P/f'memory_records_seed{seed}_N4096_v2.npy');known=list(dict.fromkeys(int(r[2]) for r in records))
 E=[[F(x) for x in e] for e in last['output_E']];A=16;K=A-len(known)
 leaves=list(enumerate_exact(E));assert sum(p for p,w in leaves)==1
 mean=[[sum(p*w[i]*E[i][j] for p,w in leaves) for j in range(4)] for i in range(len(E))]
 assert mean==E
 # Assigning the default aggregate uniformly to an actual unseen label then
 # recovers exactly E_default/K on each unseen label. No alphabet enumeration
 # is used in compact_default; this small fixture checks its rank map.
 counts={}
 class Fixed:
  def __init__(self,x):self.x=x
  def getrandbits(self,b):return self.x
 for rank in range(K):
  labels,_,_=compact_default(known,E,A,Fixed(rank));counts[labels[-1]]=1
 assert set(counts)==set(range(A))-set(known)
 labels,cols,ds=compact_default(known,E,A,random.Random(seed));out,stats=prune(labels,cols,random.Random(seed+1))
 results.append({'seed':seed,'input_effects':len(E),'exact_enumerated_pruning_leaves':len(leaves),'exact_average_effect_identity':True,'exact_default_rank_map':True,'sampled_output_labels':[x for x,e in out],'sampled_output_effects':[[str(x) for x in e] for _,e in out],'prune_stats':stats,'default_stats':ds,'whole_channel_coupling_bound':str(F(ds['draws']+stats['draws'],1<<128))})
(P/'check_pruned_receiver_v1.json').write_text(json.dumps({'status':'PASS_EXACT_AVERAGED_CORRECTION_CHANNEL_IDENTITY','elapsed_seconds':time.time()-start,'runs':results,'scope':'Exact classical effects and channel linearity; no hardware POVM synthesis or new source calls.'},indent=2)+'\n')
print([(r['seed'],r['exact_enumerated_pruning_leaves'],r['sampled_output_labels']) for r in results])
