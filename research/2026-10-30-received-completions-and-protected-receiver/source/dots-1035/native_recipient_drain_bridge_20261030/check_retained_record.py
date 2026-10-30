import numpy as np,json
from scipy.linalg import expm
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);down=np.array([[0,1],[0,0]],complex)
kr=lambda *ops: __import__('functools').reduce(np.kron,ops)
P=kr(np.diag([1,0]),I,I);J=.8*kr(I,down,X) # real AB jump, passive parity record
H0=.7*kr(I,X,I);Hn=.09*kr(X,Z,I);d=8
assert np.linalg.norm(P@J-J@P)<1e-14
loss=J.conj().T@J
def L0(r):return -1j*(H0@r-r@H0)+J@r@J.conj().T-(loss@r+r@loss)/2
def L(r):return L0(r)-1j*(Hn@r-r@Hn)
def KP(r):return P@L(P@r@P)@P
def mat(f):
 out=np.zeros((d*d,d*d),complex)
 for k in range(d*d):
  e=np.zeros((d,d),complex);e.flat[k]=1;out[:,k]=f(e).reshape(-1)
 return out
rho=np.zeros((d,d),complex);rho[0,0]=1
T=1.7
full=(expm(T*mat(L))@rho.reshape(-1)).reshape(d,d)
killed=(expm(T*mat(KP))@rho.reshape(-1)).reshape(d,d)
diff=full-killed
B=kr(I,I,np.diag([0,1]));bad_full=float(np.trace(B@full).real);bad_kill=float(np.trace(B@killed).real)
eps=float(np.linalg.norm(diff,ord='nuc'))
assert bad_kill<=bad_full+eps+1e-12
# Exact cancellation of all known AB+record dynamics in the Q boundary map.
rng=np.random.default_rng(9);a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));r=P@(a@a.conj().T)@P;r/=np.trace(r)
res=float(np.linalg.norm(L0(r)-P@L0(r)@P))
# Record refinement leaves physical marginal unchanged, even on correlated inputs.
def trrec(z):return np.trace(z.reshape(4,2,4,2),axis1=1,axis2=3)
Jp=.8*kr(I,down);Hp=.7*kr(I,X)
def Lphys(z):
 lp=Jp.conj().T@Jp
 return -1j*(Hp@z-z@Hp)+Jp@z@Jp.conj().T-(lp@z+z@lp)/2
marg=float(np.linalg.norm(trrec(L0(r))-Lphys(trrec(r))))
assert res<1e-12 and marg<1e-12
out={'dimension':d,'known_AB_record_boundary_cancellation':res,'record_refinement_physical_marginal_residual':marg,
     'full_minus_killed_trace_norm':eps,'full_minus_killed_min_eigenvalue':float(np.linalg.eigvalsh(diff).min()),
     'actual_bad_record_mass':bad_full,'killed_bad_record_mass':bad_kill,'filter_triangle_bound_slack':bad_full+eps-bad_kill,
     'scope':'Finite record-extension/boundary/filter algebra. Coherent test coupling is not an old-source continuous-memory claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
