"""Independent finite audit of exact one-basis circuit projection.
Pure-Python forward Pauli-frame propagation is separate from the acquisition's
backward effect propagation. Exact rational squared survival checks avoid roots.
"""
import sys,json,time,itertools,hashlib
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import stim,numpy as np
start=time.perf_counter();root=Path(__file__).resolve().parents[1];adir=root/'canonical_qec_circuit_gate_20261105';p=F(1,1000);out={}
# Exhaust all binary linear maps from 2 or 4 Pauli-generator bits to 2 effect bits.
# Compare exact direct-channel Walsh coefficients with the proposed all-nonzero
# independent-factor law, eliminating the radicals through integer exponents.
factorcases=0
for k in [1,2]:
 for gens in itertools.product(range(4),repeat=2*k):
  direct=defaultdict(F)
  for e in range(4**k):
   v=0
   for j,g in enumerate(gens):
    if(e>>j)&1:v^=g
   direct[v]+=1-p if not e else p/F(4**k-1)
  image=set(direct);r=(len(image)).bit_length()-1;lam=1-F(4**k,4**k-1)*p
  for char in range(4):
   actual=sum(prob*(-1 if (char&v).bit_count()%2 else 1) for v,prob in direct.items())
   negative=sum((char&v).bit_count()%2 for v in image if v)
   if not negative:assert actual==1
   else:assert negative==1<<(r-1) and actual==lam
  factorcases+=1
out['exact_factorization_maps_checked']=factorcases
# Explicit two-qubit X-projection correlation test.
original_joint_11=4*p/15;marginal=8*p/15
assert original_joint_11!=marginal*marginal
out['invalid_marginal_independence_counterexample']={'P_11_original':str(original_joint_11),'P_11_if_independent_marginals':str(marginal*marginal),'interpretation':'The audited three-factor image-group construction preserves the original correlation; two independent marginal qubit flips would not.'}

def inspect(tag,full=True):
 c=stim.Circuit((adir/f'{tag}.stim').read_text()).flattened();g=json.loads((adir/f'{tag}_graph.json').read_text());r=json.loads((adir/f'{tag}_acquisition.json').read_text());coords=c.get_detector_coordinates()
 selected=sorted(i for i,cs in coords.items() if int(cs[0]+cs[1])%4==0);nd=len(selected);Lbit=1<<nd
 seq=list(c);measurement_count=0;determinants=[];observables=[];noise=[]
 for i,ins in enumerate(seq):
  ts=ins.targets_copy();name=ins.name
  if name in ['M','MR']:measurement_count+=len(ts)
  if name=='DETECTOR':determinants.append([measurement_count+t.value for t in ts])
  if name=='OBSERVABLE_INCLUDE':
   assert ins.gate_args_copy()==[0.];observables.extend(measurement_count+t.value for t in ts)
  if name=='X_ERROR':noise.extend((i,[t.value],'X_ERROR') for t in ts)
  if name=='DEPOLARIZE1':noise.extend((i,[t.value],'DEPOLARIZE1') for t in ts)
  if name=='DEPOLARIZE2':noise.extend((i,[a.value,b.value],'DEPOLARIZE2') for a,b in zip(ts[::2],ts[1::2]))
 # Endpoint detector basis really is the measured Z-memory basis; temporal
 # boundary checks all have that coordinate class, while the other class is
 # present only in interior rounds.
 times=sorted(set(cs[2] for cs in coords.values()));endpoints=[i for i,cs in coords.items() if cs[2] in (times[0],times[-1])]
 assert set(endpoints)<=set(selected)
 def forward_effect(location,qubits,pauli):
  x=[0]*c.num_qubits;z=x.copy();record=[]
  for i,ins in enumerate(seq):
   if i==location:
    for j,q in enumerate(qubits):
     x[q]^=(pauli>>(2*j))&1;z[q]^=(pauli>>(2*j+1))&1
   name=ins.name;ts=[t.value for t in ins.targets_copy()]
   if name=='H':
    for q in ts:x[q],z[q]=z[q],x[q]
   elif name=='CX':
    for a,b in zip(ts[::2],ts[1::2]):x[b]^=x[a];z[a]^=z[b]
   elif name=='R':
    for q in ts:x[q]=z[q]=0
   elif name=='MR':
    for q in ts:record.append(x[q]);x[q]=z[q]=0
   elif name=='M':
    for q in ts:record.append(x[q]);z[q]=0
   elif name in ['TICK','QUBIT_COORDS','DETECTOR','OBSERVABLE_INCLUDE','SHIFT_COORDS','X_ERROR','DEPOLARIZE1','DEPOLARIZE2']:pass
   else:raise AssertionError(name)
  ds=[sum(record[z] for z in row)%2 for row in determinants];logical=sum(record[z] for z in observables)%2
  effect=sum(ds[ori]<<j for j,ori in enumerate(selected))|(logical<<nd)
  return effect,ds+[logical]
 survivors=defaultdict(lambda:Counter());ranks=Counter();faultcases=0;hyperfull=0;single_faults=[]
 for location,qs,kind in noise:
  if kind=='X_ERROR':
   effect,full=forward_effect(location,qs,1);faultcases+=1
   if effect:survivors[effect]['X']+=1
   single_faults.append((location,qs,1,full))
  else:
   k=len(qs);image=set()
   for pauli in range(4**k):
    effect,full=forward_effect(location,qs,pauli);image.add(effect);faultcases+=1
    if sum(full[:-1])>2:hyperfull+=1
    if pauli:single_faults.append((location,qs,pauli,full))
   rr=(len(image)).bit_length()-1;ranks[k,rr]+=1
   assert rr<=2
   for effect in image:
    if effect:
     assert (effect&(Lbit-1)).bit_count()<=2
     survivors[effect][f'D{k}R{rr}']+=1
 effects={sum(1<<j for j in e['detectors'])|(e['logical']<<nd):e for e in g['errors']}
 assert set(effects)==set(survivors)
 # Each exact merged survival squared is rational because rank<=2. Compare it
 # directly against squared output brackets, independently of integer root code.
 tv=F(0);bounds_checked=0
 for effect,e in effects.items():
  counts=survivors[effect];square=F(1)
  for name,count in counts.items():
   if name=='X':square*=(1-2*p)**(2*count)
   else:
    k=int(name[1]);rr=int(name[3]);lam=1-F(4**k,4**k-1)*p
    square*=lam**(count*(2 if rr==1 else 1))
  mid=F(e['p_mid']);rad=F(e['p_radius']);low=1-2*(mid+rad);high=1-2*(mid-rad)
  assert 0<=low<=high<=1 and low*low<=square<=high*high
  tv+=rad;bounds_checked+=1
 assert tv==F(r['total_variation_conversion_bias_upper_exact'])
 # Verify the logical-label gauge and boundary identity on every edge basis.
 left=set(g['left']);right=set(g['right']);gauge=g['gauge'];assert not left&right
 for (u,v),e in zip(g['edges'],g['errors']):
  dets=[z for z in (u,v) if z<nd];assert sorted(dets)==e['detectors']
  leftbit=int(u in left)^int(v in left)
  assert e['logical']^leftbit==sum(gauge[z] for z in dets)%2
  for z in (u,v):
   if z>=nd:assert z in left|right
 # Additional independent simulator cross-check: every original d3 single
 # nonidentity Pauli fault is run through Stim's forward stabilizer simulator.
 # Selected detectors and L0 are deterministic for each such circuit.
 for location,qs,pauli,expect in single_faults:
  fault=stim.Circuit()
  for i,ins in enumerate(seq):
   if i==location:
    for j,q in enumerate(qs):
     xx=(pauli>>(2*j))&1;zz=(pauli>>(2*j+1))&1
     if xx or zz:fault.append('Y_ERROR' if xx and zz else 'X_ERROR' if xx else 'Z_ERROR',[q],1)
   if ins.name not in ['X_ERROR','DEPOLARIZE1','DEPOLARIZE2']:fault.append(ins)
  sample=fault.compile_detector_sampler(seed=4821).sample(shots=1,append_observables=True)[0]
  assert list(map(int,sample))==expect
 return {'tag':tag,'noise_channels':len(noise),'direct_pauli_cases_including_identity':faultcases,'independent_forward_stabilizer_fault_checks':len(single_faults),'rank_counts':{str(k):v for k,v in ranks.items()},'non_graphlike_full_record_fault_cases':hyperfull,'selected_detectors':nd,'enclosed_merged_edge_probabilities':bounds_checked,'TV_bound_exact_match':str(tv),'all_edge_gauge_identities_checked':len(g['edges']),'endpoint_detectors_checked':len(endpoints),'source_hash':hashlib.sha256((adir/'acquire_graph.py').read_bytes()).hexdigest()}
out['d3_exhaustive_channel_projection']=inspect('d3_r3_p1_1000')
out['status']='PASS for exact rational p, selected detector basis plus L0; no circuit-level estimator audited here.'
out['elapsed_seconds']=time.perf_counter()-start
Path(__file__).with_name('projection_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
