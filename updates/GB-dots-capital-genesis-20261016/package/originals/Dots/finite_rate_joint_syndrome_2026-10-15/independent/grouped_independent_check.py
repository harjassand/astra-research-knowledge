"""Independent finite-dimensional algebra checks; no experimental input."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import numpy as np,json,pathlib
from scipy.linalg import expm
rng=np.random.default_rng(918347);out=[]
def herm(n):
 a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return (a+a.conj().T)/2

def local(d,J,rates):
 M=np.zeros((d*d,d*d))
 for a in range(d):
  for b in range(d):
   col=a*d+b;M[col,col]=-2*sum(g for k,g in enumerate(rates) if ((a^b)>>k)&1)
   for c in range(d):
    if c!=a:M[c*d+b,col]+=J
    if c!=b:M[a*d+c,col]+=J
 return M

def scalar(d,J,g,t):
 beta=2*g-2*(d-2)*J;w=np.sqrt(beta*beta/4+4*(d-1)*J*J)
 A=np.exp(-beta*t/2)*(np.cosh(w*t)+beta/(2*w)*np.sinh(w*t))
 return A-1,np.expm1(4*(d-1)*J*J*t/beta)
for sample in range(3):
 d1,d2,db=4,2,2;n=d1*d2*db;J1,J2=.15,.2;rates1=[2.,3.];rates2=[1.]
 H0=np.zeros((n,n),complex);V1=H0.copy();V2=H0.copy()
 def sl(a,b):return slice((a*d2+b)*db,(a*d2+b+1)*db)
 for a in range(d1):
  for b in range(d2):H0[sl(a,b),sl(a,b)]=2*herm(db)
 for b in range(d2):
  for a in range(d1):
   for c in range(a):
    T=rng.normal(size=(db,db))+1j*rng.normal(size=(db,db));T*=J1/np.linalg.norm(T,2)
    V1[sl(a,b),sl(c,b)]=T;V1[sl(c,b),sl(a,b)]=T.conj().T
 for a in range(d1):
  T=rng.normal(size=(db,db))+1j*rng.normal(size=(db,db));T*=J2/np.linalg.norm(T,2)
  V2[sl(a,0),sl(a,1)]=T;V2[sl(a,1),sl(a,0)]=T.conj().T
 H=H0+V1+V2;I=np.eye(n);L=1j*(np.kron(I,H)-np.kron(H.T,I))
 for which,rates in [(0,rates1),(1,rates2)]:
  for k,g in enumerate(rates):
   z=np.array([(-1)**(((a if which==0 else b)>>k)&1) for a in range(d1) for b in range(d2) for _ in range(db)]);Z=np.diag(z);L+=g*(np.kron(Z.T,Z)-np.eye(n*n))
 for t in [.1,.7]:
  Eprop=expm(L*t);C1=expm(local(d1,J1,rates1)*t);C2=expm(local(d2,J2,rates2)*t)
  for a0 in range(d1):
   for b0 in range(d2):
    F=np.diag([int(a!=a0 and b!=b0) for a in range(d1) for b in range(d2) for _ in range(db)])
    E=(Eprop@F.reshape(-1,order='F')).reshape((n,n),order='F');block=E[sl(a0,b0),sl(a0,b0)];p=float(np.linalg.eigvalsh((block+block.conj().T)/2)[-1])
    q1=sum(C1[a*d1+a,a0*d1+a0] for a in range(d1) if a!=a0);q2=sum(C2[b*d2+b,b0*d2+b0] for b in range(d2) if b!=b0)
    s1,e1=scalar(d1,J1,min(rates1),t);s2,e2=scalar(d2,J2,min(rates2),t)
    assert p<=q1*q2+1e-12 and q1<=s1+1e-12 and q2<=s2+1e-12 and s1<=e1+1e-12 and s2<=e2+1e-12
    out.append({'sample':sample,'initial':[a0,b0],'t':t,'effect_max':p,'matrix_product':float(q1*q2),'scalar_product':float(s1*s2),'whole_V1_norm':float(np.linalg.norm(V1,2)),'per_transition_J1':J1})
# Direct counting identities, including heterogeneous damping.
counting=[]
for d,rates in [(2,[2.]),(4,[2.,3.]),(8,[2.,3.,4.])]:
 J=.17;M=local(d,J,rates);diag=np.array([int(a==b) for a in range(d) for b in range(d)]);off=1-diag;g=min(rates);beta=2*g-2*(d-2)*J
 assert np.allclose(diag@M,2*J*off)
 assert np.all(off@M<=2*(d-1)*J*diag-beta*off+1e-12)
 counting.append({'d':d,'beta':beta,'identities_pass':True})
r={'cases':len(out),'max_effect_to_matrix_product':max(x['effect_max']/x['matrix_product'] for x in out),'whole_V1_norm_range':[min(x['whole_V1_norm'] for x in out),max(x['whole_V1_norm'] for x in out)],'per_transition_J1':.15,'counting':counting,'cases_detail':out}
p=pathlib.Path(__file__).with_name('grouped_independent_check.json');p.write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k!='cases_detail'},indent=2))
