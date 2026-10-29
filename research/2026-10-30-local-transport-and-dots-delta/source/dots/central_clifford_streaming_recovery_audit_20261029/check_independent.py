import numpy as np, json, hashlib
from pathlib import Path
rng=np.random.default_rng(2026102916)
I=np.eye(2); ss=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
errs={'objective_identity':0.,'conditional_expectation':0.,'multiplicity_optimum':0.,'centrality':0.,'scalar_axis':0.}
rows=[]
def bloch(x):return sum((x[a]*ss[a] for a in range(3)),np.zeros((2,2),complex))
for case in range(24):
 m=1+case%3; cm=1+(case//3)%2; D=2*m+3*cm+1
 W=np.linalg.qr(rng.normal(size=(D,D))+1j*rng.normal(size=(D,D)))[0]
 z=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D)); tau=z@z.conj().T;tau/=np.trace(tau)
 eta=[0.,.3,.95,1.][case%4]; p=.43
 gamma=.1+.8*rng.random(); K0=np.diag([1,np.sqrt(1-gamma)]);K1=np.array([[0,np.sqrt(gamma)],[0,0]])
 C=lambda r:K0@r@K0+K1@r@K1.T
 ns=[np.array([np.cos(2*np.pi*j/3),np.sin(2*np.pi*j/3),0]) for j in range(3)]
 Es=[(I+bloch(n))/3 for n in ns]
 def N(r):
  out=np.zeros((D,D),complex);out[:2*m,:2*m]=p*np.kron(C(r),np.eye(m)/m)
  for j,E in enumerate(Es):
   ix=2*m+j*cm;out[ix:ix+cm,ix:ix+cm]=(1-p)*np.trace(E@r)*np.eye(cm)/cm
  return (1-eta)*W@out@W.conj().T+eta*np.trace(r)*tau
 def E(A):
  A=W.conj().T@A@W; out=np.zeros_like(A)
  B=A[:2*m,:2*m].reshape(2,m,2,m);out[:2*m,:2*m]=np.kron(np.einsum('aibi->ab',B),np.eye(m)/m)
  for j in range(3):
   ix=2*m+j*cm;out[ix:ix+cm,ix:ix+cm]=np.trace(A[ix:ix+cm,ix:ix+cm])*np.eye(cm)/cm
  out[-1,-1]=A[-1,-1]
  return W@out@W.conj().T
 def Ropt(A):
  A=W.conj().T@A@W;out=np.einsum('aibi->ab',A[:2*m,:2*m].reshape(2,m,2,m))
  for j,n in enumerate(ns):
   ix=2*m+j*cm;out+=np.trace(A[ix:ix+cm,ix:ix+cm])*(I+bloch(n))/2
  return out+A[-1,-1]*I/2
 # Independent generic CPTP decoder from a Haar isometry.
 V=np.linalg.qr(rng.normal(size=(4*D,D))+1j*rng.normal(size=(4*D,D)))[0]
 ks=V.reshape(2*D,2,D)
 R=lambda A:sum((k@A@k.conj().T for k in ks),np.zeros((2,2),complex))
 ds=[N(s) for s in ss]
 for a in ds:
  for b in ds:
   for c in ds:errs['centrality']=max(errs['centrality'],float(np.linalg.norm((a@b+b@a)@c-c@(a@b+b@a))))
 for dec in [R,Ropt]:
  direct=0j; pinched=0j
  for a in range(2):
   for b in range(2):
    mat=np.zeros((2,2));mat[a,b]=1
    direct+=dec(N(mat))[a,b]/4;pinched+=dec(E(N(mat)))[a,b]/4
  score=.25+sum(np.trace(ss[a]@dec(ds[a])) for a in range(3))/8
  errs['objective_identity']=max(errs['objective_identity'],float(abs(score-direct)))
  errs['conditional_expectation']=max(errs['conditional_expectation'],float(abs(pinched-direct)))
 predicted=.25+(1-eta)*(p*(2*np.sqrt(1-gamma)+1-gamma)/4+(1-p)/4)
 got=.25+sum(np.trace(ss[a]@Ropt(ds[a])).real for a in range(3))/8
 errs['multiplicity_optimum']=max(errs['multiplicity_optimum'],abs(got-predicted))
 rows.append({'D':D,'quantum_multiplicity':m,'each_scalar_multiplicity':cm,'replacer_weight':eta,'optimum':got,'rank':int(np.linalg.matrix_rank(sum(d@d for d in ds),tol=1e-11))})
# Scalar records: covers weak, one-axis, near-threshold signs and rank-zero.
counts={'weak':0,'one':0};max_regret_ratio=0.
for j in range(1500):
 h=10**rng.uniform(-5,-1);eps=.1;d=7;eta=eps*h*h/(8192*d)
 x=rng.normal(size=3);x*=h*10**rng.uniform(-3,3)/np.linalg.norm(x)
 if j%50==0:x*=0
 G=np.outer(x,x);Z=rng.normal(size=(3,3));Z=(Z+Z.T)/2;Z*=eta/(2*np.linalg.norm(Z,2));Gh=G+Z+eta*np.eye(3)/2
 es,V=np.linalg.eigh(Gh);ind=np.argsort(es)[::-1];es=es[ind];V=V[:,ind];gh=np.sqrt(np.maximum(es,0));v=V[:,0]
 assert gh[1]<h*(1+1e-10)
 if gh[0]<h:
  counts['weak']+=1;assert np.linalg.norm(x)<=np.sqrt(h*h+eta)*(1+1e-8)
 else:
  counts['one']+=1;s=x@v;A=s/gh[0];axiserr=abs(A-np.sign(s));errs['scalar_axis']=max(errs['scalar_axis'],float(axiserr))
  assert axiserr<=eta/h**2*(1+1e-6)
  loss=np.linalg.norm(x)-abs(s);assert loss<=2*np.sqrt(eta)+1e-12
  # Hadamard-test controlled exp[i*pi/2*(A-1)] yields signed expectation cos(pi/2*(A-1)).
  expectation=np.cos(np.pi*(A-1)/2);assert abs(expectation-np.sign(s))<=np.pi*axiserr/2+1e-12
assert max(errs[k] for k in errs if k!='scalar_axis')<1e-10
out={'scope':'Independent finite ideal-channel, reference fidelity, multiplicity and scalar-record diagnostics; not theorem-sized QPE execution','cases':rows,'scalar_records':counts,'max_residuals':errs}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'cases':len(rows),'scalar_records':counts,'max_residuals':errs}))
