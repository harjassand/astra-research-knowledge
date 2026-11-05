"""Exact symbolic single-basis projection of a generated Clifford memory circuit.
Uniform depolarizing channels are factored on their projected Pauli image group;
no disjoint-error approximation or split of a correlated hyperedge is used.
"""
from fractions import Fraction as F
from math import isqrt,log,sqrt,ceil
from collections import Counter,defaultdict,deque
from pathlib import Path
import stim,numpy as np,json,hashlib,argparse,time
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs

def ceildiv(a,b):return -(-a//b)
def floorroot(n,k):
 if k==1:return n
 if k==2:return isqrt(n)
 lo=0;hi=1<<((n.bit_length()+k-1)//k)
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**k<=n:lo=mid
  else:hi=mid
 return lo

def acquire(d,rounds,p=F(1,1000),bits=192):
 t0=time.perf_counter();c=stim.Circuit.generated('surface_code:rotated_memory_z',distance=d,rounds=rounds,after_clifford_depolarization=float(p),before_round_data_depolarization=float(p),before_measure_flip_probability=float(p),after_reset_flip_probability=float(p)).flattened()
 coords=c.get_detector_coordinates();selected=sorted(i for i,cs in coords.items() if int(cs[0]+cs[1])%4==0);detmap={v:i for i,v in enumerate(selected)};nd=len(selected);Lbit=1<<nd
 masks=[0]*c.num_measurements;seq=[];mc=0;dc=0
 for ins in c:
  seq.append((ins,mc));tar=ins.targets_copy()
  if ins.name in ['M','MR']:mc+=len(tar)
  elif ins.name=='DETECTOR':
   if dc in detmap:
    for x in tar:masks[mc+x.value]^=1<<detmap[dc]
   dc+=1
  elif ins.name=='OBSERVABLE_INCLUDE':
   assert ins.gate_args_copy()==[0.]
   for x in tar:masks[mc+x.value]^=Lbit
 assert mc==len(masks)
 sx=[0]*c.num_qubits;sz=[0]*c.num_qubits;D=1<<bits;survival={};ranks=Counter();channels=0;hyperedges=[]
 def addfactor(effect,lo,hi):
  if effect==0:return
  if (effect&(Lbit-1)).bit_count()>2:hyperedges.append(effect)
  oldlo,oldhi=survival.get(effect,(D,D));survival[effect]=(oldlo*lo//D,ceildiv(oldhi*hi,D))
 def process(gens,k,prob):
  nonlocal channels
  image={0}
  for g in gens:image|={v^g for v in tuple(image)}
  rank=(len(image)).bit_length()-1;ranks[(k,rank)]+=1;channels+=1
  if rank==0:return
  lam=1-F(4**k,4**k-1)*prob;power=1<<(rank-1)
  num=lam.numerator<<(bits*power);den=lam.denominator;root=floorroot(num//den,power)
  lo=root;hi=root if root**power*den==num else root+1
  for v in image:
   if v:addfactor(v,lo,hi)
 for ins,mi in reversed(seq):
  name=ins.name;tar=[x.value for x in ins.targets_copy()];args=ins.gate_args_copy()
  if name=='H':
   for q in tar:sx[q],sz[q]=sz[q],sx[q]
  elif name=='CX':
   for a,b in zip(tar[::2],tar[1::2]):sx[a]^=sx[b];sz[b]^=sz[a]
  elif name=='R':
   for q in tar:sx[q]=sz[q]=0
  elif name=='MR':
   for j,q in enumerate(tar):sx[q]=masks[mi+j];sz[q]=0
  elif name=='M':
   for j,q in enumerate(tar):sx[q]^=masks[mi+j];sz[q]=0
  elif name=='X_ERROR':
   prob=p;value=1-2*prob;lo=value.numerator*D//value.denominator;hi=ceildiv(value.numerator*D,value.denominator)
   for q in tar:addfactor(sx[q],lo,hi);channels+=1
  elif name=='DEPOLARIZE1':
   for q in tar:process([sx[q],sz[q]],1,p)
  elif name=='DEPOLARIZE2':
   for a,b in zip(tar[::2],tar[1::2]):process([sx[a],sz[a],sx[b],sz[b]],2,p)
  elif name in ['TICK','QUBIT_COORDS','DETECTOR','OBSERVABLE_INCLUDE','SHIFT_COORDS']:pass
  else:raise NotImplementedError(name)
 assert not hyperedges,('projected hyperedges',len(hyperedges))
 # Cross-check exact symbolic effects/probability brackets against unapproximated Stim DEM.
 dem=c.detector_error_model(decompose_errors=False,approximate_disjoint_errors=False).flattened();dem_s={}
 for ins in dem:
  if ins.type!='error':continue
  effect=0
  for x in ins.targets_copy():
   if x.is_relative_detector_id() and x.val in detmap:effect^=1<<detmap[x.val]
   elif x.is_logical_observable_id():assert x.val==0;effect^=Lbit
  if effect:dem_s[effect]=dem_s.get(effect,1.)*(1-2*ins.args_copy()[0])
 assert set(dem_s)==set(survival)
 errors=[];bias=F(0);maxdiff=0.
 for effect,(lo,hi) in sorted(survival.items()):
  pmid=F(2*D-lo-hi,4*D);radius=F(hi-lo,4*D);bias+=radius
  maxdiff=max(maxdiff,abs(float(pmid)-(1-dem_s[effect])/2))
  dets=[i for i in range(nd) if (effect>>i)&1];logical=int(bool(effect&Lbit))
  errors.append({'detectors':dets,'logical':logical,'p_mid':str(pmid),'p_radius':str(radius),'p_float':float(pmid)})
 # Gauge internal logical labels away, and split boundary fault mechanisms into leaves.
 adj=[[] for _ in range(nd)]
 for i,e in enumerate(errors):
  if len(e['detectors'])==2:
   u,v=e['detectors'];adj[u].append((v,e['logical']));adj[v].append((u,e['logical']))
 gauge={}
 for root in range(nd):
  if root in gauge:continue
  gauge[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   for v,l in adj[u]:
    if v not in gauge:gauge[v]=gauge[u]^l;q.append(v)
    else:assert gauge[v]==gauge[u]^l,'nontrivial interior logical cycle'
 edges=[];left=[];right=[];n=nd
 for e in errors:
  ds=e['detectors']
  if len(ds)==2:u,v=ds
  elif len(ds)==1:
   u=ds[0];v=n;n+=1
   side=e['logical']^gauge[u]
   (left if side else right).append(v)
  else:raise AssertionError('undetected standalone logical fault')
  edges.append((u,v))
 # Floating diagnostic only: integer-weight tilted-path envelope with t=1/2.
 probs=np.array([e['p_float'] for e in errors]);costs=np.maximum(1,np.rint(.5*np.log2((1-probs)/probs)).astype(int))
 g=(1-probs)*2.**(-costs)+probs*2.**costs
 states=[];nodeadj=[[] for _ in range(n)]
 for i,(u,v) in enumerate(edges):
  states.extend([(u,v,i),(v,u,i)]);nodeadj[u].append((v,i));nodeadj[v].append((u,i))
 sid={(u,v):i for i,(u,v,e) in enumerate(states)};rows=[];cols=[];vals=[]
 for i,(u,v,e) in enumerate(states):
  if v>=nd:continue
  for w,f in nodeadj[v]:
   if w!=u:rows.append(i);cols.append(sid[v,w]);vals.append(g[f])
 T=csr_matrix((vals,(rows,cols)),shape=(len(states),len(states)))
 vec=np.ones(len(states));rho=None
 for _ in range(300):
  new=T@vec;scale=np.max(new)
  if scale==0:rho=0.;break
  new/=scale
  if np.max(abs(new-vec))<1e-12:rho=float(scale);break
  vec=new;rho=float(scale)
 result={'distance':d,'rounds':rounds,'physical_qubits':d*d,'physical_and_ancilla_qubits_used':len(c.get_final_qubit_coordinates()),'stim_qubit_index_span':c.num_qubits,'circuit_p_exact':str(p),'selected_detectors':nd,'merged_independent_graph_edges':len(edges),'noise_channels':channels,'depolarizing_image_rank_counts':{str(k):v for k,v in ranks.items()},'exact_projection_hyperedges':len(hyperedges),'probability_enclosure_bits':bits,'total_variation_conversion_bias_upper_exact':str(bias),'total_variation_conversion_bias_upper':float(bias),'maximum_abs_difference_from_float_stim_dem':maxdiff,'standalone_logical_faults':0,'interior_label_gauge_consistent':True,'left_boundary_mechanisms':len(left),'right_boundary_mechanisms':len(right),'max_internal_degree':max(len(a) for a in nodeadj[:nd]),'integer_matching_costs':sorted(set(int(x) for x in costs)),'tilted_envelope_g_range':[float(min(g)),float(max(g))],'weighted_nonbacktracking_spectral_radius_diagnostic':rho,'spectral_diagnostic_not_a_certificate':True,'time_seconds':time.perf_counter()-t0}
 graph={'detector_coordinates':[coords[i] for i in selected],'edges':edges,'left':left,'right':right,'internal_vertices':nd,'gauge':[gauge[i] for i in range(nd)],'errors':errors,'costs':[int(x) for x in costs]}
 return c,result,graph
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--distance',type=int,default=3);a.add_argument('--rounds',type=int,default=3);a.add_argument('--p',default='1/1000');v=a.parse_args();c,r,g=acquire(v.distance,v.rounds,F(v.p));root=Path(__file__).parent;tag=f'd{v.distance}_r{v.rounds}_p{v.p.replace("/","_")}'
 (root/f'{tag}.stim').write_text(str(c)+'\n');(root/f'{tag}_graph.json').write_text(json.dumps(g,separators=(',',':'))+'\n');(root/f'{tag}_acquisition.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
