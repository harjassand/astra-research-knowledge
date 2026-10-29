"""Additional exact circuit consistency and failure diagnostics; separate from frozen v1 manifest."""
import numpy as np,itertools,json
from pathlib import Path
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex);ps=[I,X,Y,Z]
def cj(ks):
 a=np.array([k.reshape(-1) for k in ks]);return a.T@a.conj()
t=.37;K=np.cos(t)*I+1j*np.sin(t)*X
G=cj([np.cos(t)*I]);B=cj([np.sin(t)*X]);b=2;m=4
unpadded=np.zeros((4,4),complex);padded=unpadded.copy();worst=0.
for checks in itertools.product(ps,repeat=b):
 # pre is first Q0 then Q1, and post exactly inverse.
 pre=np.zeros((m*2,m*2),complex)
 for s in range(m):
  u=I.copy()
  for i,q in enumerate(checks):
   if (s>>i)&1:u=q@u
  pre[2*s:2*s+2,2*s:2*s+2]=u
 vin=np.kron(np.ones((m,1))/np.sqrt(m),I)
 actual=vin.conj().T@pre.conj().T@np.kron(np.eye(m),K)@pre@vin
 projected=K.copy()
 for q in checks:projected=(projected+q@projected@q)/2
 worst=max(worst,float(np.max(abs(actual-projected))))
 unpadded+=cj([actual])/4**b
 for pad in ps:padded+=cj([pad@actual@pad])/4**(b+1)
target=G+B/m
# Full flag dephasing means no offdiagonal flag histories; accepting uniform costs1/m.
tw=sum(cj([p@K@p]) for p in ps)/4
dephased=tw/m
# Reusing the same branch key instead of independent choices makes sum_j K_g/m=K_g.
reused=tw
out=dict(actual_nested_control_residual=worst,without_pad_full_choi_error=float(np.max(abs(unpadded-target))),with_pad_full_choi_error=float(np.max(abs(padded-target))),dephased_acceptance=float(np.trace(dephased).real/2),dephased_conditional_map_residual=float(np.max(abs(dephased*m-tw))),reused_keys_error=float(np.max(abs(reused-target))))
assert worst<1e-14 and out['with_pad_full_choi_error']<1e-14
assert out['without_pad_full_choi_error']>.01 and out['reused_keys_error']>.01
Path(__file__).with_name('obstructions.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
