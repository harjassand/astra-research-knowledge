"""Explicit disjoint CNOT layers for the same FFT; all-to-all connectivity assumed."""
import numpy as np,json,random
from pathlib import Path
from additive_fft import Compiler
p=Path(__file__).parent;c=Compiler(11,2053);h=c.h;layers=[[] for _ in range(h*(h+1))]
def visit(j,start,alpha):
 if j<0:return
 half=1<<j;v=c.t[j][alpha];dep=h-1-j
 for i in range(half):
  aa=start+i;bb=start+half+i
  for bit in range(h):
   out=c.g.mul(v,1<<bit)
   for target in range(h):
    if (out>>target)&1:layers[dep*(h+1)+(target-bit)%h].append((bb*h+bit,aa*h+target))
  for bit in range(h):layers[dep*(h+1)+h].append((aa*h+bit,bb*h+bit))
 visit(j-1,start,alpha);visit(j-1,start+half,alpha^(1<<j))
visit(h-1,0,0)
for L in layers:
 flat=[x for pair in L for x in pair];assert len(flat)==len(set(flat))
assert sum(map(len,layers))==len(c.bits)
rng=random.Random(202610290442)
for k in range(3):
 x=[rng.randrange(c.q) for _ in range(c.q)];bits=np.array([(a>>j)&1 for a in x for j in range(h)],np.uint8)
 for L in layers:
  if L:
   a=np.array(L);bits[a[:,1]]^=bits[a[:,0]]
 y=[sum(int(bits[i*h+j])<<j for j in range(h)) for i in range(c.q)];assert y==c.apply(x)
flat=np.array([(i,a,b) for i,L in enumerate(layers) for a,b in L],np.uint16);np.savez_compressed(p/'circuit_h11_layers.npz',layer_control_target=flat)
out={'h':h,'B':c.q,'CNOT_count':len(c.bits),'depth_upper_bound':h*(h+1),'nonempty_layers':sum(bool(L) for L in layers),'per_layer_gate_counts':list(map(len,layers)),'all_layers_vertex_disjoint':True,'random_exact_function_equivalence_checks':3,'scope':'Ideal all-to-all arbitrary parallel CNOT availability; no routing time, gate errors, fanout hardware or measurement latency supplied. Empty layers removable.'};(p/'parallel_schedule.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
