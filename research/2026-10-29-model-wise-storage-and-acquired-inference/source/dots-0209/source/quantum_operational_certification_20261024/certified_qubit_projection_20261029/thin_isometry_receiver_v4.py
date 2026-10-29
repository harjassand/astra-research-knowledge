"""Compile only the two occupied Naimark input columns, not a full completion.
Old full-unitary certificates and gate lists remain untouched.
"""
from finite_povm_synthesis_v1 import *
from pathlib import Path
import json,time
P=Path(__file__).parent
# Load only definitions from immutable predecessor programs, avoiding their
# standalone test/write tails. These are explicit governing dependencies.
control_ns={'__file__':str(P/'compile_controlled_primitives_v2.py')}
exec(compile((P/'compile_controlled_primitives_v2.py').read_text().split('P=Path(__file__)')[0],control_ns['__file__'],'exec'),control_ns)
local_ns={'__file__':str(P/'compile_local_controls_v3.py')}
exec(compile((P/'compile_local_controls_v3.py').read_text().split('src=json.loads')[0],local_ns['__file__'],'exec'),local_ns)

def thin_synthesis(effects):
 padded=effects+[[F(0)]*4 for _ in range(4-len(effects))];blocks=[]
 for e in padded:
  ev,W=np.linalg.eigh(matrix(e));blocks.append((W*np.sqrt(np.maximum(ev,0))[None,:])@W.conj().T)
 work=np.concatenate(blocks);left=[]
 for j in range(2):
  for i in range(7,j,-1):
   a,b=work[i-1,j],work[i,j];r=np.sqrt(abs(a)**2+abs(b)**2)
   if r<1e-30:continue
   G=np.array([[np.conj(a)/r,np.conj(b)/r],[-b/r,a/r]])
   work[[i-1,i]]=G@work[[i-1,i]];left.append(([i-1,i],su2_round(G)))
 exact=eye(8);gates=[]
 for j in range(2):
  z=phase_round(work[j,j]/abs(work[j,j]));exact[j]=[z*x for x in exact[j]];gates.append({'kind':'basis_phase','basis':j,'phase':z.data()})
 for indices,G in reversed(left):
  G=adj(G);apply_rows(exact,indices,G);gates.append({'kind':'two_level_su2','basis':indices,'matrix':[[x.data() for x in row] for row in G]})
 actual=physical_effects(exact,4);target=[target_matrix(v) for v in padded];bounds=[]
 for A,B in zip(actual,target):
  _,hi=sqrt_interval(sum((A[i][j]-B[i][j]).norm2() for i in range(2) for j in range(2)),128);bounds.append(hi)
 return gates,sum(bounds)/2,exact

src=json.loads((P/'check_pruned_receiver_v1.json').read_text());out=[];start=time.time()
for r in src['runs']:
 effects=[[F(x) for x in e] for e in r['sampled_output_effects']]
 gates,bound,unitary=thin_synthesis(effects);ps=[];compiled=eye(8)
 for g in gates:
  new=control_ns['expand'](g);ps+=new
  for p in new:control_ns['apply_primitive'](compiled,p)
 assert compiled==unitary
 local=[];residuals=[]
 for p in ps:
  gs,delta=local_ns['compile_one'](p);local+=gs;residuals.append(delta)
 total=bound+sum(residuals)
 out.append({'seed':r['seed'],'labels':r['sampled_output_labels'],'input_effects':r['sampled_output_effects'],'two_level_phase_gate_count':len(gates),'controlled_primitive_count':len(ps),'single_qubit_count':sum(g['kind']=='single' for g in local),'cnot_count':sum(g['kind']=='cnot' for g in local),'exact_compilation_equality':True,'ideal_dilation_half_diamond_upper':str(bound),'local_control_approximation_upper':str(sum(residuals)),'total_correction_channel_half_diamond_upper':str(total),'total_correction_channel_half_diamond_upper_float':float(total),'two_level_gates':gates,'local_gates':local})
 print(r['seed'],len(gates),len(ps),len(local),float(total),flush=True)
(P/'thin_isometry_receiver_v4.json').write_text(json.dumps({'status':'PASS_EXACT_THIN_ISOMETRY_CERTIFICATES','elapsed_seconds':time.time()-start,'runs':out,'scope':'Same learned effects, reduced generic local-gate model; no new acquisition/hardware.'},indent=2)+'\n')
