"""Forward packed-Pauli audit of EVERY d21 original noise-channel generator."""
import sys,json,time,hashlib,random
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import stim
start=time.perf_counter();d=int(sys.argv[1]);root=Path(__file__).resolve().parents[1];adir=root/'qec_design_direct_20261105'/'canonical_qec_circuit_gate_20261105';tag=f'd{d}_r{d}_p1_1000';p=F(1,1000)
c=stim.Circuit((adir/f'{tag}.stim').read_text()).flattened();G=json.loads((adir/f'{tag}_graph.json').read_text());R=json.loads((adir/f'{tag}_acquisition.json').read_text());coords=c.get_detector_coordinates();selected=sorted(i for i,cs in coords.items() if int(cs[0]+cs[1])%4==0);detmap={v:i for i,v in enumerate(selected)};nd=len(selected);Lbit=1<<nd
# Each bit is a different single-Pauli insertion experiment. Propagate all
# experiments forward simultaneously, with plain Python bitwise arithmetic.
x=[0]*c.num_qubits;z=x.copy();records=[];detrows=[];logical=0;channels=[];generators=[];dc=0
for instruction_index,ins in enumerate(c):
 name=ins.name;ts=[t.value for t in ins.targets_copy()]
 if name=='H':
  for q in ts:x[q],z[q]=z[q],x[q]
 elif name=='CX':
  for a,b in zip(ts[::2],ts[1::2]):x[b]^=x[a];z[a]^=z[b]
 elif name=='R':
  for q in ts:x[q]=z[q]=0
 elif name=='MR':
  for q in ts:records.append(x[q]);x[q]=z[q]=0
 elif name=='M':
  for q in ts:records.append(x[q]);z[q]=0
 elif name=='DETECTOR':
  val=0
  for j in ts:val^=records[len(records)+j]
  detrows.append(val);dc+=1
 elif name=='OBSERVABLE_INCLUDE':
  assert ins.gate_args_copy()==[0.]
  for j in ts:logical^=records[len(records)+j]
 elif name in ['X_ERROR','DEPOLARIZE1','DEPOLARIZE2']:
  assert ins.gate_args_copy()==[float(p)]
  groups=[ts[j:j+2] for j in range(0,len(ts),2)] if name=='DEPOLARIZE2' else [[q] for q in ts]
  for qs in groups:
   ids=[]
   for q in qs:
    for axis in ('X',) if name=='X_ERROR' else ('X','Z'):
     bit=1<<len(generators);ids.append(len(generators));generators.append((instruction_index,q,axis))
     if axis=='X':x[q]^=bit
     else:z[q]^=bit
   channels.append((name,len(qs),ids))
 elif name in ['TICK','QUBIT_COORDS','SHIFT_COORDS']:pass
 else:raise AssertionError(name)
effects=[0]*len(generators)
for output,row in list(enumerate(detrows[i] for i in selected))+[(nd,logical)]:
 while row:
  bit=row&-row;idx=bit.bit_length()-1;effects[idx]|=1<<output;row^=bit
survival=defaultdict(Counter);rankcounts=Counter()
for name,k,ids in channels:
 if name=='X_ERROR':
  v=effects[ids[0]]
  if v:survival[v]['X']+=1
 else:
  image={0}
  for j in ids:image|={v^effects[j] for v in tuple(image)}
  rank=len(image).bit_length()-1;rankcounts[k,rank]+=1;assert rank<=2
  for v in image:
   if v:
    assert (v&(Lbit-1)).bit_count()<=2
    survival[v][f'D{k}R{rank}']+=1
graph_effects={sum(1<<j for j in e['detectors'])|(e['logical']<<nd):e for e in G['errors']};assert set(graph_effects)==set(survival)
TV=F(0)
for v,e in graph_effects.items():
 square=F(1)
 for name,n in survival[v].items():
  if name=='X':square*=(1-2*p)**(2*n)
  else:
   k,rank=int(name[1]),int(name[3]);lam=1-F(4**k,4**k-1)*p;square*=lam**(n*(2 if rank==1 else 1))
 mid,rad=F(e['p_mid']),F(e['p_radius']);lo,hi=1-2*(mid+rad),1-2*(mid-rad)
 assert 0<=lo<=hi<=1 and lo*lo<=square<=hi*hi;TV+=rad
assert TV==F(R['total_variation_conversion_bias_upper_exact'])
left=set(G['left']);right=set(G['right']);gauge=G['gauge']
for (u,v),e in zip(G['edges'],G['errors']):
 ds=[z for z in (u,v) if z<nd];assert sorted(ds)==e['detectors']
 assert e['logical']^int(u in left)^int(v in left)==sum(gauge[z] for z in ds)%2
# Sample 100 generator insertions against an independent forward stabilizer
# simulator. This checks the packed-frame propagation on the larger layout.
rng=random.Random(512713);seq=list(c)
for idx in rng.sample(range(len(generators)),100):
 loc,q,axis=generators[idx];fault=stim.Circuit()
 for j,ins in enumerate(seq):
  if j==loc:fault.append(axis+'_ERROR',[q],1)
  if ins.name not in ['X_ERROR','DEPOLARIZE1','DEPOLARIZE2']:fault.append(ins)
 sample=fault.compile_detector_sampler(seed=41298).sample(shots=1,append_observables=True)[0]
 val=sum(int(sample[ori])<<j for j,ori in enumerate(selected))|(int(sample[-1])<<nd)
 assert val==effects[idx]
# Exact rational interpretation differs slightly from a binary64 probability.
# Bound the coupling error if somebody instead claims the literal double-noise
# simulator distribution. This is separate from, and far larger than, enclosure.
double_p=F.from_float(float(p));double_difference=abs(double_p-p);double_TV_bound=len(channels)*double_difference
out={'status':f'PASS: every d{d} channel checked by independent packed forward propagation, factor brackets and boundary gauge','original_channels':len(channels),'single_Pauli_generators':len(generators),'rank_counts':{str(k):v for k,v in rankcounts.items()},'selected_detectors':nd,'merged_edges_checked':len(graph_effects),'independent_stabilizer_crosschecks':100,'exact_model_TV_enclosure':str(TV),'exact_model_TV_enclosure_float':float(TV),'rational_vs_binary64_parameter_difference_exact':str(double_difference),'rational_vs_binary64_whole_circuit_TV_bound':float(double_TV_bound),'numerical_scope':'The 192-bit enclosure certifies exact rational p=1/1000, not the distinct binary64-parameter Stim sampling distribution. Its floating DEM comparison is diagnostic only.','elapsed_seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256((adir/'acquire_graph.py').read_bytes()).hexdigest()}
Path(__file__).with_name(f'd{d}_projection_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
