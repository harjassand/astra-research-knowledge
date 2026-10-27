"""Compatible unchanged-law substitutions, positive local Loewner reduction, total trace ceiling."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,numpy as np,itertools,sys
from damped_arithmetic_primitives import I,mid_guard
P=Path(__file__).resolve().parent;O=P/'same_law_AC';F=P/'fully_corrective141_half_K48';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=json.loads((O/'exact_product_box_interface_receipt.json').read_text());boxes=j['boxes'];trace=Q();group={}
def det(a):
 return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
r=Q(1,8192)
for b in boxes:
 roots={c['node_index']for c in boxes if c['catalog_index']==b['catalog_index']and c['node_index']!=b['node_index']};assert not roots.intersection(i for i,a in b['replaced_internal_action_links'])
 vs=[[Q(v)for v in vec]for vec in b['null_half_edge_vectors']];V=[[vs[col][row]for col in range(3)]for row in range(3)];d=det(V)
 # explicit 2x2 cofactors, transposed to inverse
 inv=[]
 for ii in range(3):
  row=[]
  for kk in range(3):
   a=[x for x in range(3)if x!=kk];c=[x for x in range(3)if x!=ii];row.append(Q((-1)**(ii+kk))*(V[a[0]][c[0]]*V[a[1]][c[1]]-V[a[0]][c[1]]*V[a[1]][c[0]])/d)
  inv.append(row)
 assert max(sum(abs(v)for v in row)for row in inv)*r<Q(1,2)
 trace+=Q(b['exact_root_weighted_incoming_mass'])*sum(v*v for vec in vs for v in vec)/2
 x=tuple(map(Q,b['center']));alpha=Q(b['central_half_box_occupation_matrix_lower_alpha_I'])
 for perm in itertools.permutations(range(3)):
  y=tuple(x[i]for i in perm);group[y]=group.get(y,Q())+alpha
M=np.load(F/'received_signed_moments.npy');H=np.load(P/'epsilon_half_discriminator/half_H_table.npy');k=np.arange(1,97);ks=k[:,None,None]**2+k[None,:,None]**2+k[None,None,:]**2;C=M[2:,2:,2:]*H[ks];nodes=np.load(F/'candidate_volume_nodes.npy',mmap_mode='r');patch=[];gain=Q()
for center,alpha in group.items():
 idx=[int((x+1)*128)for x in center];assert all(Q(i,128)-1==x for i,x in zip(idx,center));node=Q(float(nodes[tuple(idx)]))
 if node>=-Q(1,100000):continue
 S=[];T=[]
 for x in center:
  angle=I.mul(I.PI,I.mul(I.rat((x+1)/2),I.exact(k)));si,co=I.sincos(angle);s,_=mid_guard(si,radius=2**-37);t,_=mid_guard(I.mul(co,I.mul(I.PI,I.exact(k/2))),radius=2**-30);S.append(s);T.append(t)
 grad=[]
 for axis in range(3):
  B=list(S);B[axis]=T[axis];grad.append(float(np.einsum('ijk,i,j,k',C,*B,optimize=True)))
 gradbound=sum((abs(Q(v))for v in grad),Q())+Q(3,2**20);assert gradbound<Q(1,1000)
 q=Q(1,200000);bound=node+Q(1,2**29)+Q(1,1000)*r+150*r*r;assert bound<-q and alpha<q
 g=3*alpha*(2*r)**3;gain+=g;patch.append({'center':list(map(str,center)),'radius_infinity':str(r),'combined_Loewner_alpha':str(alpha),'stored_scalar':str(node),'guarded_gradient_L1_upper':str(gradbound),'scalar_upper_on_patch':str(bound),'negative_scalar_lower':str(q),'gain_lower':str(g)})
for a,b in itertools.combinations(patch,2):assert max(abs(Q(x)-Q(y))for x,y in zip(a['center'],b['center']))>2*r
out={'status':'COMPATIBLE_SAME_TERMINAL_LAW_AC_REDUCTION_PENDING_AUDIT','substitutions':len(boxes),'internal_subtree_compatibility':'PASS','all_S3_images_retained':True,'disjoint_negative_patches':patch,'strict_finite_bulk_reduction_lower':str(gain),'decimal_reduction_lower':float(gain),'total_replacement_positive_occupation_trace_upper':str(trace),'decimal_total_trace_upper':float(trace),'unchanged_global_N_upper_before_credit':json.loads((F/'received_full_Gram_candidate.json').read_text())['global_negative_mass_upper'],'dependencies':{str(p):sha(p)for p in[O/'exact_product_box_interface_receipt.json',O/'rational_heat_kernel_bound.json',F/'candidate_volume_nodes.npy',F/'received_signed_moments.npy',O.parent/'lorentz_occupation/tube_volume_obstruction_receipt.json']},'script_sha256':sha(Path(__file__)),'scope':'Exact same terminal law, source/cubic/completion unchanged. Compatible18 substitutions and all positive strata retained. Local Loewner reduction is strictly positive but minuscule; total available occupation trace<3.02e-7 rules out material gain from these boxes alone. No displayed bound adoption. Gradient numerical guard2^-20 per coordinate dominates guarded trig and contraction errors; global diagonal Hessian sum100 implies full directional remainder150r^2.'};(O/'compatible_box_overlap_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print('patches',len(patch),'gain',float(gain),'totaltrace',float(trace))
