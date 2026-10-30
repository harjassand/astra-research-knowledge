"""Fixed ordinary product recovery for all six GL(2,2) targets and stale frames.
Ideal-code regression only; native controller/noise theorem is not simulated.
"""
from pathlib import Path
import json
import numpy as np
# Copy/read definitions without executing or modifying the frozen earlier regression.
source=Path('producer-workspace/check_fixed_product_decoder.py').read_text()
exec(compile(source.split('# Logical two-qubit input')[0],'<frozen decoder definitions>','exec'))
rng=np.random.default_rng(30689)
group=[]
for bits in range(16):
 M=np.array([(bits>>j)&1 for j in range(4)],int).reshape(2,2)
 if (M[0,0]*M[1,1]-M[0,1]*M[1,0])%2:
  U=np.zeros((4,4),complex)
  for j in range(4):
   y=M@np.array([j>>1,j&1])%2;U[2*y[0]+y[1],j]=1
  group.append((M,U))
def fullperm(M):
 x=inds&127;y=inds>>7
 a=(x if M[0,0] else 0)^(y if M[0,1] else 0)
 b=(x if M[1,0] else 0)^(y if M[1,1] else 0)
 return a+(b<<7)
def column_unitary(v,i,u):
 base=inds[((inds>>i)&1)==0];base=base[((base>>(7+i))&1)==0];out=np.zeros_like(v)
 for o in range(4):
  dst=base|((o>>1)<<i)|((o&1)<<(7+i))
  for j in range(4):
   src=base|((j>>1)<<i)|((j&1)<<(7+i));out[dst]+=u[o,j]*v[src]
 return out
v=rng.normal(size=8)+1j*rng.normal(size=8);v/=np.linalg.norm(v)
encoded=E@v.reshape(4,2);rho=np.outer(v,v.conj())
results=[]
for target,(M,U) in enumerate(group):
 goalv=np.kron(U,np.eye(2))@v;goal=np.outer(goalv,goalv.conj())
 assert np.linalg.norm(applyperm(E,fullperm(M))-E@U)<1e-12
 for stale,(_,W) in enumerate(group):
  # Full target, except column0 actually carries stale W rather than target U.
  physical=applyperm(column_unitary(encoded,0,U.conj().T@W),fullperm(M))
  decoded,branches,leak=base_decode(physical)
  err=float(np.linalg.svd(decoded-goal,compute_uv=False).sum())
  assert err<1e-10
  results.append({'target':target,'stale_column_frame':stale,'trace_norm_error':err,'syndrome_branches':branches,'code_leakage':leak})
# Check repeated noncommuting relative requests really use cumulative absolute target.
Ua=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
Ub=np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]],complex)
cumulative=np.eye(4);steps=[]
for k,A in enumerate([Ua,Ub,Ua,Ua,Ub,Ub,Ua,Ub]):
 cumulative=A@cumulative
 target=next(j for j,(_,u) in enumerate(group) if np.array_equal(u,cumulative))
 physical=applyperm(encoded,fullperm(group[target][0]))
 decoded,_,_=base_decode(physical)
 goalv=np.kron(cumulative,np.eye(2))@v;goal=np.outer(goalv,goalv.conj())
 err=float(np.linalg.svd(decoded-goal,compute_uv=False).sum());assert err<1e-10
 steps.append({'step':k+1,'absolute_target':target,'trace_norm_error':err})
zero,_,_=base_decode(encoded)
out={'code':'two [[7,1,3]] Steane blocks','DATA_decoder':'ONE ordinary fixed product syndrome recovery, no logical target/inverse in recovery','all_target_stale_frame_cases':results,'cumulative_noncommuting_request_sequence':steps,'time_zero_identity_trace_norm_error':float(np.linalg.svd(zero-rho,compute_uv=False).sum()),'max_trace_norm_error':max(x['trace_norm_error'] for x in results+steps),'scope':'Ideal-code common-span regression only. No native noisy controller, settling probability, readout noise, or computational advantage is simulated.'}
Path(__file__).with_name('fixed_decoder_reusable_group_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['all_target_stale_frame_cases']},indent=2))
