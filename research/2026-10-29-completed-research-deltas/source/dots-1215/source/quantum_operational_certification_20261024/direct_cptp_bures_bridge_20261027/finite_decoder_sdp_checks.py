"""Reproducible small-instance direct-decoder SDP checks, with exact dyadic certificates.
Not an execution of the joint Schur/purification learner or a gate-resource experiment.
"""
from pathlib import Path
import json
import numpy as np
import sympy as sp

ROOT=Path(__file__).parent
rng=np.random.default_rng(27101853)
b=1.5
I2=np.eye(2)
paulis=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.])]
labels=[(I2+sign*A)/2 for A in paulis for sign in [-1,1]]
def herm(a):return (a+a.conj().T)/2
def op(a):return np.linalg.norm(a,2)
def isometry(d,k):
 z=rng.normal(size=(d,k))+1j*rng.normal(size=(d,k))
 return np.linalg.qr(z)[0][:,:k]
def channel(q,k,r):return list(isometry(k*r,q).reshape(r,k,q))
def apply(ks,x):return sum(a@x@a.conj().T for a in ks)
def dens(k):
 z=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));a=z@z.conj().T
 return a/np.trace(a).real
def ptr(c):
 k=len(c)//2;return np.einsum('aibi->ab',c.reshape(k,2,k,2))
def invsqrt(a):
 w,v=np.linalg.eigh(herm(a));return (v/np.sqrt(w))@v.conj().T
def coeff(rhos):return sum(np.kron(r.T,I2-p) for r,p in zip(rhos,labels))*b/6

def basis(k):
 out=[]
 for a in range(k):
  z=np.zeros((k,k),complex);z[a,a]=1;out.append(z)
 for a in range(k):
  for c in range(a+1,k):
   z=np.zeros((k,k),complex);z[a,c]=z[c,a]=1;out.append(z)
   z=np.zeros((k,k),complex);z[a,c]=1j;z[c,a]=-1j;out.append(z)
 return np.array(out)

def solve(h):
 k=len(h)//2;bs=basis(k);as_=np.array([np.kron(z,I2) for z in bs]);tr=np.trace(bs,axis1=1,axis2=2).real
 def make(x):return np.einsum('a,aij->ij',x,bs)
 def at(x,mu,deriv=False):
  s=herm(h-np.kron(make(x),I2));w=np.linalg.eigvalsh(s)
  if min(w)<=0:return None
  f=-np.dot(x,tr)-mu*np.log(w).sum()
  if not deriv:return f
  si=np.linalg.inv(s)
  g=-tr+mu*np.einsum('ij,aji->a',si,as_).real
  hs=mu*np.einsum('ij,ajk,kl,bli->ab',si,as_,si,as_).real
  return f,g,herm(hs).real,si
 x=np.zeros(k*k);x[:k]=-1;its=0
 for mu in [1.,.1,.01,.001,.0001,.00001,.000001,.0000001,.00000001]:
  for it in range(120):
   its+=1;f,g,hs,si=at(x,mu,True)
   dx=-np.linalg.solve(hs,g)
   if -g@dx<1e-18:break
   t=1.
   while t>2**-48:
    ff=at(x+t*dx,mu)
    if ff is not None and ff<=f+1e-4*t*(g@dx):break
    t*=.5
   if t<=2**-48:break
   x+=t*dx
 y=herm(make(x));_,g,_,si=at(x,mu,True)
 c=herm(mu*si);s=invsqrt(ptr(c));c=herm(np.kron(s,I2)@c@np.kron(s,I2))
 return c,y,{'newton_iterations':its,'terminal_mu':mu,'gradient_norm':float(np.linalg.norm(g))}

DEN=2**40
def rational(a):
 d=len(a);o=sp.zeros(d)
 for i in range(d):
  o[i,i]=sp.Rational(round(float(a[i,i].real)*DEN),DEN)
  for j in range(i+1,d):
   o[i,j]=sp.Rational(round(float(a[i,j].real)*DEN),DEN)+sp.I*sp.Rational(round(float(a[i,j].imag)*DEN),DEN)
   o[j,i]=sp.conjugate(o[i,j])
 return o
def serial(a):return [[[str(sp.re(z)),str(sp.im(z))] for z in a.row(i)] for i in range(a.rows)]
def exact_ptr(a,k):return sp.Matrix(k,k,lambda i,j:a[2*i,2*j]+a[2*i+1,2*j+1])
def positive(a):
 assert a==a.conjugate().T
 ds=[sp.simplify(a[:i,:i].det(method='domain-ge')) for i in range(1,a.rows+1)]
 assert all(z.is_positive for z in ds),ds
 return min(float(z) for z in ds)

certs=[];rows=[]
for name,k,kind in [('qubit_noisy',2,'random'),('qutrit_output',3,'random'),('reversible_rank_two',4,'reversible')]:
 if kind=='random':ks=channel(2,k,2)
 else:
  u=isometry(4,4);p=.37
  a=np.zeros((4,2),complex);a[[0,2],[0,1]]=np.sqrt(p)
  c=np.zeros((4,2),complex);c[[1,3],[0,1]]=np.sqrt(1-p)
  ks=[u@a,u@c]
 rhos=[apply(ks,p) for p in labels]
 # Inconsistent separately perturbed estimates are deliberately permitted.
 est=[.97*r+.03*dens(k) for r in rhos]
 h=herm(coeff(est));c,y,diagnostic=solve(h)
 c=(1-1e-6)*c+1e-6*np.eye(2*k)/2
 yy=rational(y)-sp.Rational(11000,DEN)*sp.eye(k)
 hh=rational(h);cc=rational(c)
 cc-=sp.kronecker_product(exact_ptr(cc,k)-sp.eye(k),sp.eye(2))/2
 assert exact_ptr(cc,k)==sp.eye(k)
 slack=hh-sp.kronecker_product(yy,sp.eye(2))
 pivots=[positive(z) for z in [hh,cc,slack]]
 primal=sp.simplify(sp.trace(hh*cc));dual=sp.trace(yy);gap=sp.simplify(primal-dual)
 assert gap.is_positive and gap<sp.Rational(1,100000),gap
 cn=np.array(cc.evalf(),complex);yn=np.array(yy.evalf(),complex)
 # Extract actual Kraus family and verify physical channel/Choi objective equality.
 vals,vec=np.linalg.eigh(cn)
 ds=[np.sqrt(v)*vec[:,a].reshape(k,2).T for a,v in enumerate(vals)]
 risk=b/6*sum(1-np.trace(p@apply(ds,t)).real for p,t in zip(labels,est))
 residual=float(abs(risk-np.trace(h@cn).real))
 tp=float(op(sum(d.conj().T@d for d in ds)-np.eye(k)))
 true_risk=b/6*sum(1-np.trace(p@apply(ds,r)).real for p,r in zip(labels,rhos))
 f=sum(abs(np.trace(d@a))**2 for d in ds for a in ks)/4
 assert residual<1e-10 and tp<1e-10 and abs(1-f-true_risk)<1e-10
 rec={'name':name,'k':k,'H':serial(hh),'C':serial(cc),'Y':serial(yy),'exact_primal':str(primal),'exact_dual':str(dual),'exact_gap':str(gap),'strict_positive_leading_minors':True,'coefficient_rounding_op_bound':4*k/DEN,'objective_rounding_bound':4*k*k/DEN}
 certs.append(rec)
 rows.append({'name':name,'k':k,**diagnostic,'gap':float(gap),'minimum_C_eigenvalue':float(min(np.linalg.eigvalsh(cn))),'tp_kraus_residual':tp,'choi_objective_residual':residual,'six_pauli_entanglement_loss_residual':float(abs(1-f-true_risk)),'estimated_risk':risk,'true_risk':true_risk,'minimum_exact_leading_minor_float':min(pivots)})
out={'status':'PASS','seed':27101853,'checks':rows,'scope':'Small direct CPTP SDP examples with exact dyadic primal/dual certificates for stated rounded coefficient problems; not an execution of the Schur/tomography learner or full gate synthesis.'}
(ROOT/'finite_decoder_sdp_certificates.json').write_text(json.dumps({'denominator':DEN,'certificates':certs},indent=2)+'\n')
(ROOT/'finite_decoder_sdp_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
