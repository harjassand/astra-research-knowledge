"""Small standard [[5,1,3]] interface test, NOT actual recursive-family proof."""
import numpy as np, scipy.linalg as la, json
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=dict(I=I,X=X,Y=Y,Z=Z)
def kron(*v):
 a=np.array([[1.]])
 for b in v:a=np.kron(a,b)
 return a
def word(s):return kron(*(P[x] for x in s))
def tn(a):return float(la.svdvals(a).sum())
S=[word(s) for s in ('XZZXI','IXZZX','XIXZZ','ZXIXZ')];pc=np.eye(32)
for a in S:pc=pc@(np.eye(32)+a)/2
v0=pc[:,0]/la.norm(pc[:,0]);v1=word('XXXXX')@v0;basis=np.column_stack([v0,v1])
Es=[np.eye(32)]
for j in range(5):
 for p in 'XYZ':
  s=['I']*5;s[j]=p;Es.append(word(s))
D=np.column_stack([E@v for v in (v0,v1) for E in Es]);H0=sum((np.eye(32)-s)/2 for s in S)
rng=np.random.default_rng(543);V=np.zeros((32,32),complex)
for j in range(5):
 for p in 'XYZ':
  s=['I']*5;s[j]=p;V+=rng.uniform(-1,1)*word(s)
eps=.003;beta=2.5;H=H0+eps*V;Gfull=la.expm(-beta*H);Zpart=np.trace(Gfull).real;rho=Gfull/Zpart
rd=D.conj().T@rho@D;sg=np.trace(rd.reshape(2,16,2,16),axis1=0,axis2=2);bar=D@kron(I/2,sg)@D.conj().T
bell=np.array([1,0,0,1])/np.sqrt(2);br=np.outer(bell,bell)
ideal=kron(br,sg).reshape(2,2,16,2,2,16).transpose(0,2,1,3,5,4).reshape(64,64);ideal=kron(D,I)@ideal@kron(D.conj().T,I)
loaded=np.zeros_like(ideal,dtype=complex);rows=[];weight=0
for k,E in enumerate(Es):
 B=E@basis;signs=[float(np.vdot(B[:,0],s@B[:,0]).real) for s in S];Q=[(np.eye(32)-z*s)/2 for z,s in zip(signs,S)]
 gaps=[];kernel=[];gramdev=[];berry=[]
 for t in [0,beta/2,beta]:
  F=la.expm(-t*H/2);Finv=la.expm(t*H/2);A=F@B;gram=A.conj().T@A;ev,U=la.eigh(gram);inv=(U*ev**-.5)@U.conj().T;W=A@inv
  parent=sum((F@q@Finv).conj().T@(F@q@Finv) for q in Q);pe=la.eigvalsh(parent);gaps.append(float(pe[2]));kernel.append(float(la.norm(parent@W)))
  gramdev.append(float(la.norm(gram/(np.trace(gram).real/2)-I,2)))
  gp=-A.conj().T@H@A;dd=U.conj().T@gp@U;div=np.empty((2,2))
  for i in range(2):
   for j in range(2):div[i,j]=-.5*ev[i]**-1.5 if abs(ev[i]-ev[j])<1e-10*max(ev) else (ev[i]**-.5-ev[j]**-.5)/(ev[i]-ev[j])
  invp=U@(div*dd)@U.conj().T;connection=.5*inv@gp@inv+(U*np.sqrt(ev))@U.conj().T@invp;berry.append(float(la.norm(connection,2)))
 p=float(np.trace(gram).real/Zpart);weight+=p;WR=kron(W,I);loaded+=p*WR@br@WR.conj().T
 rows.append(dict(syndrome_index=k,gaps=gaps,kernel_residual=kernel,relative_gram_error=gramdev,berry_connection_norm=berry))
res=dict(scope='standard five-qubit perfect-code interface only; no all-level gap or circuit claim',epsilon=eps,beta=beta,total_weight=weight,minimum_parent_gap=min(min(x['gaps']) for x in rows),maximum_kernel_residual=max(max(x['kernel_residual']) for x in rows),maximum_relative_gram_error=max(max(x['relative_gram_error']) for x in rows),maximum_berry_connection=max(max(x['berry_connection_norm']) for x in rows),filtered_ensemble_vs_thermal_overwrite=tn(loaded-ideal),actual_gibbs_vs_logical_twirl=tn(rho-bar),syndromes=rows)
assert abs(weight-1)<1e-12 and res['maximum_kernel_residual']<1e-10 and res['minimum_parent_gap']>.5
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='syndromes'},indent=2))
