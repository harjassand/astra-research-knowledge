"""Symbolic rectangular Haar moments; independent redundant/weighted polar checks."""
from pathlib import Path
import sympy as s,numpy as np,json,hashlib,math
D=Path(__file__).parent
# Derive invariant twirl coefficients from both trace equations, not an assumed beta.
d,e,K,N=s.symbols('d e K N',positive=True);aa,bb=s.symbols('a b')
sol=s.solve([aa*d*d+bb*d-K*K,aa*d+bb*d*d-K],[aa,bb]);a,b=sol[aa],sol[bb]
g2=s.factor((a*N*d*d/e+b*d*d)/K)
beta=s.factor(g2-1)
assert s.simplify(beta-(d*K-1)*(N*d/e-1)/(d*d-1))==0
rng=np.random.default_rng(1240026)
def sqrtpos(A):
 w,V=np.linalg.eigh((A+A.conj().T)/2);return (V*np.sqrt(np.maximum(w,0)))@V.conj().T

def fvals(x,alpha,m):
 z=np.sqrt(np.maximum(x,0))/alpha;return z*sum((math.comb(2*j,j)/4**j)*(1-z*z)**j for j in range(m+1))
rows=[]
for din,dout,nerr,k in [(4,2,2,2),(6,2,3,2),(3,3,3,2)]:
 if din!=dout:
  Fs=[]
  for a0 in range(nerr):
   F=np.zeros((dout,din),complex);F[:,a0*dout:(a0+1)*dout]=np.sqrt(nerr)*np.eye(dout);Fs.append(F)
 else:
  # Orthogonal unitary phase frame, square case.
  Fs=[np.diag(np.exp(2j*np.pi*a0*np.arange(din)/din)) for a0 in range(nerr)]
 assert max(abs(np.trace(F.conj().T@H)-din*(i==j)) for i,F in enumerate(Fs) for j,H in enumerate(Fs))<1e-12
 assert np.max(abs(sum(F@F.conj().T for F in Fs)-(nerr*din/dout)*np.eye(dout)))<1e-12
 for trial in range(12):
  z=rng.normal(size=(din,k))+1j*rng.normal(size=(din,k));C=np.linalg.qr(z)[0]
  W=np.hstack([F@C for F in Fs]);G=W.conj().T@W
  z=rng.normal(size=(nerr,nerr))+1j*rng.normal(size=(nerr,nerr));T=z@z.conj().T;T*=.2/np.trace(T)
  R=np.kron(T,np.eye(k)/k);t=np.trace(T).real
  mlabels=nerr+3;z=rng.normal(size=(mlabels,nerr))+1j*rng.normal(size=(mlabels,nerr));V=np.linalg.qr(z)[0];J=np.kron(V,np.eye(k));WR=W@J.conj().T;GR=WR.conj().T@WR;RR=J@R@J.conj().T
  defect=np.trace(R@(G-np.eye(nerr*k))@(G-np.eye(nerr*k))).real;red=np.trace(RR@(GR-np.eye(mlabels*k))@(GR-np.eye(mlabels*k))).real
  assert abs(defect-red)<1e-12
  alpha=max(1,np.linalg.norm(W,2))*1.01;m=5
  # Success map f(SV(W/alpha)) dagger in both frames, exact nulls retained.
  u,sv,vh=np.linalg.svd(W,full_matrices=False);f=fvals(sv*sv,alpha,m);A=(vh.conj().T*f)@u.conj().T
  ur,sr,vhr=np.linalg.svd(WR,full_matrices=False);fr=fvals(sr*sr,alpha,m);AR=(vhr.conj().T*fr)@ur.conj().T
  lift_err=np.max(abs(AR-J@A));assert lift_err<1e-12
  # Compose the actual subnormalized source with total success/failure decoder.
  w,v=np.linalg.eigh(T);L=[sum(np.sqrt(max(w[h],0))*v[a0,h]*Fs[a0]@C for a0 in range(nerr)) for h in range(nerr)]
  failure=sqrtpos(np.eye(dout)-A.conj().T@A);decs=list(A.reshape(nerr,k,dout))
  for j in range(dout):
   h=np.zeros((k,dout),complex);h[0,:]=failure[j,:];decs.append(h)
  p=sum(np.trace(Lh.conj().T@Lh).real for Lh in L)/k;bell=sum(abs(np.trace(Dh@Lh))**2 for Dh in decs for Lh in L)/k**2
  penalty=t+p-2*np.trace(R@A@W).real;assert p-bell<=penalty+1e-12
  rows.append({'d':din,'e':dout,'N':nerr,'K':k,'defect_transfer_error':abs(defect-red),'soft_isometric_lift_error':float(lift_err),'subnormalized_actual_mass':p,'source_coefficient_trace':t,'Bell_error_mass':p-bell,'soft_penalty':penalty})
# An explicit null-label pitfall: the physical frame is unchanged but an arbitrary
# uniform coefficient weight is not the canonical lift of the source.
V=np.array([[1.],[1.]])/np.sqrt(2);P=V@V.T
canonical=np.trace(P@(P-np.eye(2))@(P-np.eye(2)));naive=np.trace(np.eye(2)/2@(P-np.eye(2))@(P-np.eye(2)))
assert abs(canonical)<1e-14 and abs(naive-.5)<1e-14
out={'status':'PASS_SYMBOLIC_RECTANGULAR_MOMENT_AND_REDUNDANT_SOURCE_TRANSFER','Haar_beta':str(beta),'weighted_cases':len(rows),'max_defect_transfer_error':max(r['defect_transfer_error'] for r in rows),'max_soft_lift_error':max(r['soft_isometric_lift_error'] for r in rows),'null_label_counterexample_naive_defect':float(naive),'rows':rows,'scope':'Independent algebraic checks. Not a representation/circuit-access receipt.','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),D/'MEAN_TRANSFER_DERIVATION_v1.md']}}
(D/'check_mean_transfer_v1.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='rows'})
