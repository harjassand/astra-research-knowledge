"""Non-certifying numerical cross-checks of analytic maps and actual ensembles.
The finite constant is certified separately by rational_interval_check.py.
"""
import numpy as np
from scipy.integrate import quad,quad_vec
from pathlib import Path
import json
rng=np.random.default_rng(202610291319)
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex);P=[X,Y,Z]
sigma=np.array([[.5,.25],[.25,.5]],complex)
K=[X@np.diag([1,1/np.sqrt(2)]),X@np.array([[0,1/np.sqrt(2)],[0,0]])]
def apply(ks,a):return sum(k@a@k.conj().T for k in ks)
def powm(a,p):
 w,u=np.linalg.eigh(a);return (u*w.astype(complex)**p)@u.conj().T
nu=apply(K,sigma);ss=powm(sigma,.5);ni=powm(nu,-.5);RK=[ss@k.conj().T@ni for k in K]
def r0(a):return apply(RK,a)
def rotated(a,t,prior=sigma,output=nu,rks=RK):
 sp=powm(prior,-.5j*t);vp=powm(output,.5j*t)
 return sp@apply(rks,vp@a@vp.conj().T)@sp.conj().T
s,u=np.linalg.eigh(sigma);v,w=np.linalg.eigh(nu)
SP=[u[:,i:i+1]@u[:,i:i+1].conj().T for i in range(2)];VP=[w[:,i:i+1]@w[:,i:i+1].conj().T for i in range(2)]
def kernel(x):return 1 if abs(x)<1e-14 else x/np.sinh(x)
def rb(a):
 out=np.zeros((2,2),complex)
 for i in range(2):
  for j in range(2):
   for c in range(2):
    for d in range(2):
     freq=(np.log(s[i])-np.log(s[j])-np.log(v[c])+np.log(v[d]))/2
     out+=kernel(freq)*SP[i]@r0(VP[c]@a@VP[d])@SP[j]
 return out
def psi(a):return rb(apply(K,a))
BK=[np.outer(ss[:,j],np.eye(2)[j])/np.sqrt(sigma[j,j]) for j in range(2)]
def eb(a):return apply(BK,a)
units=[np.eye(2,dtype=complex)[:,i:i+1]@np.eye(2,dtype=complex)[:,j:j+1].T for i in range(2) for j in range(2)]
M=np.array([[np.trace(p@(q-psi(q))).real/2 for q in P] for p in P]);N=np.array([[np.trace(p@(q-eb(q))).real/2 for q in P] for p in P]);T=N@np.linalg.inv(M);C=np.sum(abs(T))
def lin(a):return sum(P[i]*T[i,j]*np.trace(P[j]@a)/2 for i in range(3) for j in range(3))
def extend(f,a,dr):
 # A register first, reference second.
 out=np.zeros_like(a,dtype=complex)
 for i in range(2):
  for j in range(2):out+=np.kron(f(units[2*i+j]),a[i*dr:(i+1)*dr,j*dr:(j+1)*dr])
 return out

def choi(f):return sum(np.kron(units[2*i+j],f(units[2*i+j])) for i in range(2) for j in range(2))/2
cp={}
for name,f in [('rb',rb),('psi',psi),('eb',eb)]:
 ch=choi(f);cp[name]={'minimum_choi_eigenvalue':float(np.linalg.eigvalsh(ch).min()),'TP_residual':float(np.max(abs(np.einsum('iaja->ij',ch.reshape(2,2,2,2))-.5*I)))}
 assert cp[name]['minimum_choi_eigenvalue']>-1e-12 and cp[name]['TP_residual']<1e-12
# Fourier check against directly integrated beta0(t), including negative frequencies.
freqs=sorted(set((np.log(s[i])-np.log(s[j])-np.log(v[c])+np.log(v[d]))/2 for i in range(2) for j in range(2) for c in range(2) for d in range(2)))
beta=lambda t:np.pi/(2*(np.cosh(np.pi*t)+1))
fourier=[]
for x in freqs:
 val,err=quad(lambda t:beta(t)*np.cos(x*t),-18,18,epsabs=2e-13,epsrel=2e-13)
 fourier.append(abs(val-kernel(x)))
assert max(fourier)<1e-12
# Direct spectral powers at each time, independent of projector/Fourier expansion.
def integrated(t):return beta(t)*np.stack([rotated(e,t) for e in units])
quadmap,quaderr=quad_vec(integrated,-18,18,epsabs=1e-12,epsrel=1e-12)
quadrature_residual=float(np.max(abs(quadmap-np.stack([rb(e) for e in units]))));assert quadrature_residual<1e-12
# Reference factorization at EACH rotation time for coherent nonmaximally mixed omega.
omega=np.array([[.6,.1+.08j],[.1-.08j,.4]])
ps=np.kron(sigma,omega);pn=np.kron(nu,omega);ks=[np.kron(k,I) for k in K]
rks=[powm(ps,.5)@k.conj().T@powm(pn,-.5) for k in ks]
reference_residual=0
for t in [-3,-.5,0,.8,3]:
 for i in range(4):
  for j in range(4):
   a=np.zeros((4,4),complex);a[i,j]=1
   expected=extend(lambda x:rotated(x,t),a,2)
   got=rotated(a,t,ps,pn,rks)
   reference_residual=max(reference_residual,float(np.max(abs(got-expected))))
assert reference_residual<2e-12
# Arbitrary non-Hermitian reference operators exercise the complete map identity.
identity_residual=0;max_observed_norm_ratio=0
for dr in [1,2,3,5]:
 for _ in range(20):
  a=rng.normal(size=(2*dr,2*dr))+1j*rng.normal(size=(2*dr,2*dr))
  left=a-extend(eb,a,dr);right=extend(lin,a-extend(psi,a,dr),dr)
  identity_residual=max(identity_residual,float(np.max(abs(left-right))))
  ratio=np.linalg.norm(extend(lin,a,dr),ord='nuc')/np.linalg.norm(a,ord='nuc');max_observed_norm_ratio=max(max_observed_norm_ratio,float(ratio))
assert identity_residual<1e-11 and max_observed_norm_ratio<C+1e-12

def entropy(rho):
 vals=np.linalg.eigvalsh((rho+rho.conj().T)/2);vals=vals[vals>1e-13]
 return float(-np.dot(vals,np.log(vals)))
def logmfaith(a):
 ev,vec=np.linalg.eigh(a);assert ev.min()>0;return (vec*np.log(ev))@vec.conj().T

def rel(a,b):return -entropy(a)-np.trace(a@logmfaith(b)).real
def distance(a,b):return np.linalg.norm(a-b,ord='nuc')/2
# HJW rank-one decompositions have the exact intended mean, with generally
# entangled letters when dr>1, not merely independent product-state samples.
ensembles=[];maxmean=0;maxloss=0;minpointmargin=1e9;minensemblemargin=1e9
for dr in [1,2,3]:
 wr=np.array([[1.]]) if dr==1 else (omega if dr==2 else np.diag([.2,.3,.5]))
 base=np.kron(sigma,wr);outbase=np.kron(nu,wr);basehalf=powm(base,.5);dim=2*dr
 for nextra in [0,1,4]:
  for repeat in range(6):
   z=rng.normal(size=(dim+nextra,dim))+1j*rng.normal(size=(dim+nextra,dim))
   q,_=np.linalg.qr(z);vv=basehalf@q.conj().T
   probs=np.sum(abs(vv)**2,axis=0);states=[np.outer(vv[:,j],vv[:,j].conj())/probs[j] for j in range(len(probs))]
   mean=sum(p*a for p,a in zip(probs,states));maxmean=max(maxmean,float(np.max(abs(mean-base))))
   outs=[extend(lambda a:apply(K,a),a,dr) for a in states]
   delta=entropy(base)-sum(p*entropy(a) for p,a in zip(probs,states))-entropy(outbase)+sum(p*entropy(a) for p,a in zip(probs,outs))
   losses=[rel(a,base)-rel(b,outbase) for a,b in zip(states,outs)];maxloss=max(maxloss,abs(delta-np.dot(probs,losses)))
   errors=[]
   for a,ell in zip(states,losses):
    assert ell>-1e-11
    rerr=distance(a,extend(psi,a,dr));eerr=distance(a,extend(eb,a,dr))
    assert rerr<=np.sqrt(max(ell,0))+1e-10
    minpointmargin=min(minpointmargin,float(C*np.sqrt(max(ell,0))-eerr));errors.append(eerr)
   eavg=float(np.dot(probs,errors));margin=5*np.sqrt(max(delta,0))-eavg;minensemblemargin=min(minensemblemargin,float(margin));assert margin>-1e-10
   ensembles.append({'reference_dimension':dr,'letters':len(probs),'delta_nats':float(delta),'e_avg':eavg})
assert maxmean<1e-12 and maxloss<1e-11 and minpointmargin>-1e-10
out={'scope':'Numerical diagnostics only; universal certificate uses analytic proof and independent exact rational intervals','seed':202610291319,'choi':cp,'fourier_frequencies':len(freqs),'max_fourier_residual':float(max(fourier)),'direct_rotated_map_quadrature_residual':quadrature_residual,'quadrature_reported_error':float(quaderr),'rotated_reference_matrix_unit_cases':80,'rotated_reference_factorization_residual':reference_residual,'arbitrary_joint_operator_cases':80,'complete_identity_residual':identity_residual,'max_sampled_L_trace_norm_ratio':max_observed_norm_ratio,'analytic_entry_l1_bound_float':float(C),'actual_mean_ensembles':len(ensembles),'max_actual_mean_residual':maxmean,'max_loss_equals_Holevo_residual':float(maxloss),'minimum_pointwise_comparator_margin':minpointmargin,'minimum_ensemble_comparator_margin':minensemblemargin,'ensembles':ensembles,'passed':True}
(Path(__file__).parent/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='ensembles'},indent=2))
