"""Deterministic complete-channel fixture; bounded contrast perturbations, not shots."""
import numpy as np,itertools,json
from pathlib import Path
rng=np.random.default_rng(202610285)
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex);P=[X,Y,Z]
def kron(xs):
 a=np.array([[1]],complex)
 for x in xs:a=np.kron(a,x)
 return a
def pauli(word):return kron([{'I':I,'X':X,'Y':Y,'Z':Z}[c] for c in word])
def unitary(H,t=1):
 e,v=np.linalg.eigh(H);return (v*np.exp(-1j*t*e))@v.conj().T
def sign(H):
 e,v=np.linalg.eigh(H);return (v*np.sign(e))@v.conj().T
G=[pauli(w) for w in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']]
Proj=np.eye(32,dtype=complex)
for g in G:Proj=Proj@(np.eye(32)+g)/2
z=np.zeros(32,complex);z[0]=1;z=Proj@z;z/=np.linalg.norm(z)
Enc=np.column_stack([z,pauli('XXXXX')@z]);errs=[np.eye(32)]
for i in range(5):
 for c in 'XYZ':errs.append(pauli('I'*i+c+'I'*(4-i)))
Rec=[Enc.conj().T@E.conj().T for E in errs]
assert np.linalg.norm(Enc.conj().T@Enc-np.eye(2))<1e-12
assert np.linalg.norm(sum(R.conj().T@R for R in Rec)-np.eye(32))<1e-12
KL=max(np.linalg.norm(Enc.conj().T@a.conj().T@b@Enc-(np.eye(2) if i==j else np.zeros((2,2)))) for i,a in enumerate(errs) for j,b in enumerate(errs));assert KL<1e-12
# Fixed nontrivial bounded-local mixer V12 tensor V34 tensor V5.
Vs=[]
for d in [4,4,2]:
 h=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));h=(h+h.conj().T)/2;Vs.append(unitary(h,.4))
axes=[]
for i in range(5):
 u=rng.normal(size=3);u/=np.linalg.norm(u);axes.append(u)
def ad(gamma,u):
 H=sum(u[j]*P[j] for j in range(3));e,v=np.linalg.eigh(H);U=np.column_stack([v[:,1],v[:,0]])
 return [U@np.diag([1,np.sqrt(1-gamma)])@U.conj().T,U@np.array([[0,np.sqrt(gamma)],[0,0]])@U.conj().T]
def apply_local(rho,Ks,sites,n):
 rest=[i for i in range(n) if i not in sites];perm=list(sites)+rest+[i+n for i in sites]+[i+n for i in rest];di=2**len(sites);dr=2**len(rest)
 A=rho.reshape([2]*(2*n)).transpose(perm).reshape(di,dr,di,dr)
 B=sum(np.einsum('ki,irjs,lj->krls',K,A,K.conj(),optimize=True) for K in Ks)
 return B.reshape([2]*(2*n)).transpose(np.argsort(perm)).reshape(2**n,2**n)
def channel(rho,Ks):return sum(K@rho@K.conj().T for K in Ks)
def extraction(Bs,n):
 d=2**n;W=np.eye(d*d,dtype=complex)
 for i in range(n):
  sx,sz=Bs[i][0],Bs[i][2];xi=kron([X if k==i else I for k in range(n)]);zi=kron([Z if k==i else I for k in range(n)])
  A=np.kron((np.eye(d)+sz)/2,np.eye(d))+np.kron((np.eye(d)-sz)/2,xi)
  B=np.kron(np.eye(d),(np.eye(d)+zi)/2)+np.kron(sx,(np.eye(d)-zi)/2)
  W=A@B@A@W
 # Physical output is discarded, fresh receiver started maximally mixed.
 T=W.reshape(d,d,d,d)
 return [T[p,:,:,a]/np.sqrt(d) for p in range(d) for a in range(d)]
def make_receiver(localKs,V,a):
 n=len(localKs);d=2**n;rho=[channel(I/2,ks) for ks in localKs];Bs=[];maxerr=0;guard=0;mins=[]
 for i in range(n):
  C=[]
  for j in range(3):
   out=channel(P[j]/2,localKs[i]);C.append(V@kron([out if k==i else rho[k] for k in range(n)])@V.conj().T)
  Ch=[]
  for c in C:
   e=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));e=(e+e.conj().T)/2;e*=a/np.linalg.norm(e,2);Ch.append(c+e)
  gram=np.array([[np.trace(c@e).real for e in Ch] for c in Ch]);ev,U=np.linalg.eigh(gram);W=(U*(1/np.sqrt(ev)))@U.T
  F=[sum(Ch[k]*W[k,j] for k in range(3)) for j in range(3)];S=list(map(sign,F));Bs.append(S)
  g=3*d*(2*a+a*a);h=ev[0];assert h>g
  # Floating evaluation of analytic guard; no rational certificate claim.
  ebound=np.sqrt(3)*a/np.sqrt(h)+np.sqrt(3)*g/(2*(h-g)**1.5)
  dels=[]
  for j in [0,2]:
   ell=np.min(np.abs(np.linalg.eigvalsh(F[j])));assert ell>ebound
   dels.append(2*ebound/(2*ell-ebound));mins.append(ell)
   true=V@kron([P[j] if k==i else I for k in range(n)])@V.conj().T;maxerr=max(maxerr,np.linalg.norm(S[j]-true,2))
  guard+=2*dels[1]+dels[0]
 K=extraction(Bs,n)
 assert np.linalg.norm(sum(k.conj().T@k for k in K)-np.eye(d))<1e-11
 return K,maxerr,guard,min(mins)
def logical_channel(localKs,receivers=None,unframed=False):
 outs=[]
 for i in range(2):
  for j in range(2):
   A=Enc[:,i:i+1]@Enc[:,j:j+1].conj().T
   for k,ks in enumerate(localKs):A=apply_local(A,ks,[k],5)
   for sites,V in zip([[0,1],[2,3],[4]],Vs):A=apply_local(A,[V],sites,5)
   if receivers is None and not unframed:
    for sites,V in zip([[0,1],[2,3],[4]],Vs):A=apply_local(A,[V.conj().T],sites,5)
   elif receivers is not None:
    for sites,K in zip([[0,1],[2,3],[4]],receivers):A=apply_local(A,K,sites,5)
   outs.append(sum(R@A@R.conj().T for R in Rec))
 J=np.block([[outs[0],outs[1]],[outs[2],outs[3]]])/2;bell=np.array([1,0,0,1])/np.sqrt(2);Jid=np.outer(bell,bell);diff=(J-Jid+(J-Jid).conj().T)/2;tracehalf=np.sum(np.abs(np.linalg.eigvalsh(diff)))/2
 return {'entanglement_infidelity':float(1-np.vdot(bell,J@bell).real),'normalized_choi_half_trace_distance':float(tracehalf),'half_diamond_lower_bound':float(tracehalf),'half_diamond_trace_upper_bound':float(min(1,2*tracehalf)),'choi_min_eigenvalue':float(np.linalg.eigvalsh((J+J.conj().T)/2)[0]),'trace_error':float(abs(np.trace(J)-1))}
rows=[]
for gamma in [.08,.04,.02,.01,.005,.001]:
 rates=[gamma*(.6+.1*i) for i in range(5)];Ks=[ad(g,u) for g,u in zip(rates,axes)]
 a=gamma**2/1e4;receivers=[];errs=[];guards=[];gaps=[]
 for ids,V in zip([[0,1],[2,3],[4]],Vs):
  K,e,g,h=make_receiver([Ks[i] for i in ids],V,a);receivers.append(K);errs.append(e);guards.append(g);gaps.append(h)
 # Conservative analytic p_i upper bound from K0-I plus jump term.
 ps=[1-np.sqrt(1-g)+g/2 for g in rates]
 bound=.5*(np.prod([1+2*p for p in ps])-1-2*sum(ps));zeta=sum(guards)
 exact=logical_channel(Ks);learned=logical_channel(Ks,receivers);bad=logical_channel(Ks,unframed=True)
 assert learned['half_diamond_lower_bound']<=bound+zeta+1e-10
 rows.append({'gamma_max':gamma,'rates':rates,'contrast_perturbation_op_bound':a,'reflection_actual_op_error_max':max(errs),'floating_evaluation_inverse_guard_zeta':zeta,'minimum_whitened_gap':min(gaps),'native_p_upper_bounds':ps,'analytic_qec_bound':min(1,float(bound)),'analytic_qec_plus_inverse_guard':min(1,float(bound+zeta)),'exact_inverse':exact,'learned_reflection_inverse':learned,'no_inverse':bad})
# Exact first-order CPTP correction checks at all5 sites for non-Pauli AD.
first=[]
for i in range(5):
 ks=[[I] for _ in range(5)];ks[i]=ad(.37,axes[i]);r=logical_channel(ks);assert r['normalized_choi_half_trace_distance']<1e-11;first.append(r['normalized_choi_half_trace_distance'])
out={'status':'PASS_DETERMINISTIC_COMPLETE_CHANNEL_FIXTURES','source_draws':0,'seed':202610285,'standard_code':'XZZXI,IXZZX,XIXZZ,ZXIXZ; logicalX=XXXXX; known16syndrome recovery','KL_256_matrix_pair_max_residual':float(KL),'single_site_nonpauli_exact_recovery_residuals':first,'rows':rows,'scope':'Actual CPTP encoding/native noise/mixed-ancilla learned reflection extraction/syndrome recovery; bounded synthetic contrast perturbations, not acquired shots. Floating guards are diagnostic, not outward-rounded confidence certificates. Logical reference retained; bath discarded.','comparators':'Equally informed conventional five-qubit QEC with same learned inverse is identical; no performance advantage claimed. No-inverse curve diagnoses missing frame only.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
