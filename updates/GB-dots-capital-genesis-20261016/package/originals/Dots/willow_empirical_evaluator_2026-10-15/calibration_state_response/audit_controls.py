import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import resource
resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import numpy as np,json,pathlib,itertools,hashlib
O=pathlib.Path(__file__).parent;P=(pathlib.Path(__file__).resolve().parent.parent / 'measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7');D=P/'d5_at_q8_7/X/r13';src=P/'README/README.md'
a=np.fromfile(D/'sweep_bits.b8',dtype=np.uint8).reshape(50000,4);s=np.unpackbits(a,axis=1,bitorder='little')[:,:25]
u,first,inv,counts=np.unique(s,axis=0,return_index=True,return_inverse=True,return_counts=True)
# Re-label configurations in order of first appearance; no chronology is assumed.
order=np.argsort(first);remap=np.empty(len(u),dtype=int);remap[order]=np.arange(len(u));ids=remap[inv];u=u[order];counts=counts[order];first=first[order]
bounds=np.r_[0,np.flatnonzero(ids[1:]!=ids[:-1])+1,len(s)]
runs=[{'start_index_inclusive':int(l),'end_index_exclusive':int(r),'length':int(r-l),'configuration_id':int(ids[l])} for l,r in zip(bounds[:-1],bounds[1:])]
def rref(m):
 m=m.copy();p=[];i=0
 for c in range(m.shape[1]):
  cand=np.flatnonzero(m[i:,c])
  if not len(cand):continue
  k=i+int(cand[0]);m[[i,k]]=m[[k,i]]
  for j in range(len(m)):
   if j!=i and m[j,c]:m[j]^=m[i]
  p.append(c);i+=1
  if i==len(m):break
 return m,p
def null(m):
 rr,p=rref(m);out=[]
 for f in range(m.shape[1]):
  if f in p:continue
  v=np.zeros(m.shape[1],dtype=np.uint8);v[f]=1
  for j,c in enumerate(p):v[c]=rr[j,f]
  assert not np.any((m@v)%2);out.append(v)
 return np.array(out),p
n,piv=null(u);aug=np.column_stack((np.ones(len(u),dtype=np.uint8),u));an,ap=null(aug)
w=np.zeros(25,dtype=np.uint8);w[[22,23]]=1;target=u@w%2
aliases=[]
for weight in range(0,4):
 for inds in itertools.combinations(range(25),weight):
  if inds==(22,23):continue
  v=np.zeros(25,dtype=np.uint8);v[list(inds)]=1
  if np.array_equal(u@v%2,target):
   assert np.array_equal(s@v%2,s@w%2)
   aliases.append({'indices':list(inds),'weight':weight,'xor_with_original_null_mask':np.flatnonzero(v^w).tolist(),'exact_agreement_all_50000':True,'configuration_tag_values':target.tolist()})
 # Find every alias at the minimum weight, then stop.
 if aliases:break
j={'scope':'Only r13 sweep bits, own circuit metadata/reference descriptions, source README; no measured outcome bytes read in this audit.','shots':len(s),'sweep_bits':25,'distinct_configurations':len(u),'configurations':[{'configuration_id':i,'bits_index0_first':''.join(map(str,row)),'one_indices':np.flatnonzero(row).tolist(),'frequency':int(counts[i]),'first_file_index':int(first[i])} for i,row in enumerate(u)],'adjacent_complementary_pairs':[[i,i+1] for i in range(0,len(u)-1,2) if np.all(u[i]^u[i+1])],'number_contiguous_file_runs':len(runs),'runs':runs,'unique_configuration_matrix_GF2_rank':len(piv),'affine_augmented_matrix_GF2_rank':len(ap),'affine_span_dimension':len(ap)-1,'parity_alias_nullspace_dimension':len(n),'parity_alias_nullspace_basis_one_indices':[np.flatnonzero(v).tolist() for v in n],'augmented_affine_nullspace_dimension':len(an),'augmented_affine_nullspace_basis':[{'constant':int(v[0]),'one_indices':np.flatnonzero(v[1:]).tolist()} for v in an],'original_mask_indices':[22,23],'original_tag_per_configuration':target.tolist(),'distinct_minimum_weight_aliases':aliases,'nullspace_verified_exact':True,'README_findings':'README describes sweep bits as initial data-qubit 0/1 configuration choices, and r13 as calibration for RL prior optimization. It does not specify selection/randomization of preparation configurations, batching, or whether file row order is acquisition chronology.','source_README_path':str(src),'sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [D/'sweep_bits.b8',src,O/'audit_controls.py']}}
(O/'control_design_audit.json').write_text(json.dumps(j,indent=2));print(json.dumps(j,indent=2))
