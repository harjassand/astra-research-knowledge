import numpy as np,json
from pathlib import Path
# Clock I,A,Q; workspace 0,1. Complete guarded W/P-style erasure.
d=6;lam=.037
J=[]
for w in range(2):
 j=np.zeros((d,d),complex);j[2, w]=np.sqrt(lam);J.append(j)
loss=sum(j.conj().T@j for j in J)
P=np.diag([1,1,0,0,0,0]);assert np.linalg.norm(loss-lam*P)<1e-14
def L(r):return sum(j@r@j.conj().T for j in J)-(loss@r+r@loss)/2
rho=np.zeros((d,d),complex);rho[0,0]=1
attained=float(np.linalg.norm(L(rho),ord='nuc'))
# Id+L/lam is NOT a legitimate CPTP uniformized attempt on coherent guard blocks.
choi=np.zeros((d*d,d*d),complex)
for i in range(d):
 for k in range(d):
  e=np.zeros((d,d),complex);e[i,k]=1
  choi[i*d:(i+1)*d,k*d:(k+1)*d]=e+L(e)/lam
mineig=float(np.linalg.eigvalsh(choi).min())
assert abs(attained-2*lam)<1e-13 and mineig<-.1
out={'dimension':d,'lambda':lam,'complete_source_loss_residual':float(np.linalg.norm(loss-lam*P)),
     'gain_cp_norm_equals_lambda':float(np.linalg.norm(loss,2)),
     'generator_diamond_upper_bound':2*lam,'attained_trace_norm_on_source_state':attained,
     'false_uniformization_Id_plus_L_over_lambda_choi_min_eigenvalue':mineig,
     'scope':'Exact complete guarded LOAD bundle algebra, not a native threshold test.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
