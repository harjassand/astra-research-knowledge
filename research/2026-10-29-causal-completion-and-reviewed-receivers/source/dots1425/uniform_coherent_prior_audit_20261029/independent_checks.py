"""Independent numerical tests; the uniform result has an analytic proof.
No author code is imported. Includes singular support, rectangular channels,
complex coherent priors, entangled letters, and exact scope counterexamples.
"""
from pathlib import Path
import numpy as np,json
from fractions import Fraction as F
rng=np.random.default_rng(202610291342)
I=np.eye(2,dtype=complex);P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1]).astype(complex)]

def channel(K,a):return sum(k@a@k.conj().T for k in K)
def randisometry(n,k):return np.linalg.qr(rng.normal(size=(n,k))+1j*rng.normal(size=(n,k)))[0][:,:k]
def state(n):
 a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));a=a@a.conj().T;return a/np.trace(a)
def distance(a,b):return float(np.linalg.norm(a-b,ord='nuc')/2)
def entropy(a):
 v=np.linalg.eigvalsh((a+a.conj().T)/2);v=v[v>1e-13];return float(-np.dot(v,np.log(v)))
def entropy_loss(probs,states,K):
 mean=sum(p*a for p,a in zip(probs,states));out=[channel(K,a) for a in states]
 return entropy(mean)-sum(p*entropy(a) for p,a in zip(probs,states))-entropy(channel(K,mean))+sum(p*entropy(a) for p,a in zip(probs,out))
def support(a):
 v,u=np.linalg.eigh((a+a.conj().T)/2);mask=v>1e-12;return v[mask],u[:,mask]
def root(a):
 v,u=support(a);return (u*np.sqrt(v))@u.conj().T

def hjw(mean,extra=3):
 v,u=support(mean);rank=len(v);q=randisometry(rank+extra,rank);vecs=(u*np.sqrt(v))@q.conj().T
 probs=np.sum(abs(vecs)**2,axis=0);states=[np.outer(vecs[:,j],vecs[:,j].conj())/probs[j] for j in range(len(probs))]
 assert np.max(abs(sum(p*a for p,a in zip(probs,states))-mean))<2e-12
 return probs,states

def averaged_recovery(sigma,K):
 # Construct on output support, then complete outside it by preparing sigma.
 s,U=support(sigma);nu=channel(K,sigma);v,V=support(nu)
 R=np.stack([(np.sqrt(s)[:,None]*(U.conj().T@k.conj().T@V))/np.sqrt(v)[None,:] for k in K])
 coeff=np.einsum('ria,rjb->ijab',R,R.conj())
 f=(np.log(s)[:,None,None,None]-np.log(s)[None,:,None,None]-np.log(v)[None,None,:,None]+np.log(v)[None,None,None,:])/2
 ker=np.ones(f.shape);nz=abs(f)>1e-12;ker[nz]=f[nz]/np.sinh(f[nz]);coeff*=ker
 Pi=V@V.conj().T;outer=np.eye(len(nu))-Pi
 def recover(y):return U@np.einsum('ijab,ab->ij',coeff,V.conj().T@y@V)@U.conj().T+np.trace(outer@y)*sigma
 return recover

def extend(f,a,dA,dR):
 out=np.zeros_like(a,dtype=complex)
 for i in range(dA):
  for j in range(dA):
   e=np.zeros((dA,dA),complex);e[i,j]=1
   out+=np.kron(f(e),a[i*dR:(i+1)*dR,j*dR:(j+1)*dR])
 return out

def marginalR(a,dA,dR):return np.trace(a.reshape(dA,dR,dA,dR),axis1=0,axis2=2)

rows=[];min_nonmargin=1e9;min_compmargin=1e9;max_point_res=0;max_fix=0;max_bratio=0;max_inverse=0;max_identity=0;min_choi=1
# XAD includes c->1 (not uniform-family claim), c=0 singular output, pure means,
# and genuinely complex coherences. All requested family members gamma>=.5 appear.
for gamma in [.01,.25,.5,.9,1.]:
 K=[P[0]@np.diag([1,np.sqrt(1-gamma)]),P[0]@np.array([[0,np.sqrt(gamma)],[0,0]])]
 c=np.sqrt(1-gamma)
 for radius in [0,.2,.9,1-1e-6,1.]:
  for axis in range(3):
   direction=rng.normal(size=3);direction/=np.linalg.norm(direction)
   sigma=(I+radius*sum(direction[j]*P[j] for j in range(3)))/2
   probs,states=hjw(sigma);delta=entropy_loss(probs,states,K);eavg=sum(p*distance(a,sigma) for p,a in zip(probs,states));margin=np.sqrt(max(0,delta))/(1-c)-eavg
   assert margin>-2e-9;min_nonmargin=min(min_nonmargin,margin)
   rec=averaged_recovery(sigma,K);psi=lambda a:rec(channel(K,a));fix=float(np.max(abs(psi(sigma)-sigma)));max_fix=max(max_fix,fix)
   # The CPTP completion works on ALL input operators, including off support.
   if radius<1:
    B=np.array([[np.trace(p@psi(q)).real/2 for q in P] for p in P]);bn=np.linalg.norm(B,2)
    assert bn<=c+2e-9
    if c>0:max_bratio=max(max_bratio,float(bn/c))
    inv=np.linalg.inv(np.eye(3)-B);max_inverse=max(max_inverse,float((1-c)*np.linalg.norm(inv,2)));assert (1-c)*np.linalg.norm(inv,2)<1+2e-9
    cols=sum(np.linalg.norm(inv[:,j]) for j in range(3));assert cols<=3/(1-c)+2e-9
    def linear(a):return sum(P[i]*inv[i,j]*np.trace(P[j]@a)/2 for i in range(3) for j in range(3))
    for i in range(2):
     for j in range(2):
      a=np.zeros((2,2),complex);a[i,j]=1
      max_identity=max(max_identity,float(np.max(abs(a-np.trace(a)*sigma-linear(a-psi(a))))))
   # Product barycenter with a coherent reference, including singular omega.
   for dr in [2,3]:
    om=state(dr)
    if axis==2:om=np.diag([1]+[0]*(dr-1)).astype(complex)
    mean=np.kron(sigma,om);pp,rr=hjw(mean,2);KR=[np.kron(k,np.eye(dr)) for k in K]
    loss=entropy_loss(pp,rr,KR);ee=sum(p*distance(a,np.kron(sigma,marginalR(a,2,dr))) for p,a in zip(pp,rr))
    margin=3*np.sqrt(max(loss,0))/(1-c)-ee
    assert margin>-2e-8;min_compmargin=min(min_compmargin,margin)
    # Pointwise universal remainder on product-support prior.
    for a in rr:
     ar=extend(psi,a,2,dr)
     # Relative loss finite on support, evaluated in common support basis.
     ss,U=support(mean);vv,V=support(channel(KR,mean))
     la=(U*np.log(ss))@U.conj().T;lb=(V*np.log(vv))@V.conj().T
     out=channel(KR,a);ell=-entropy(a)-np.trace(a@la).real+entropy(out)+np.trace(out@lb).real
     residual=distance(a,ar)-np.sqrt(max(ell,0));max_point_res=max(max_point_res,residual)
     assert residual<2e-8
   rows.append({'gamma':gamma,'radius':radius,'axis_index':axis,'mean_rank':len(support(sigma)[0]),'delta':float(delta),'e_avg':float(eavg)})
assert max_fix<2e-9 and max_identity<2e-8
# General finite-dimensional theorem, known c by convex mixing, including
# rank-deficient means, output support smaller than ambient, and replacement c=0.
general=[]
for k in [3,4]:
 for inputrank in [1,2,k]:
  for c in [0,.3,.8]:
   b=k+1;D=b+2;E=randisometry(D,b);St=randisometry(2*b,k)
   raw=[E@St.reshape(b,2,k)[:,a,:] for a in range(2)]
   tauvec=E@randisometry(b,1)[:,0]
   K=[np.sqrt(c)*a for a in raw]+[np.sqrt(1-c)*np.outer(tauvec,np.eye(k)[i]) for i in range(k)]
   V=randisometry(k,inputrank);small=state(inputrank);sigma=V@small@V.conj().T
   probs,states=hjw(sigma,3);delta=entropy_loss(probs,states,K);eavg=sum(p*distance(a,sigma) for p,a in zip(probs,states));bound=np.sqrt(max(delta,0))/(1-c)
   assert eavg<=bound+2e-9
   rec=averaged_recovery(sigma,K);assert np.max(abs(rec(channel(K,sigma))-sigma))<2e-9
   # Check recovery TP even on the orthogonal ambient-output support.
   for i in range(D):
    ei=np.zeros((D,D),complex);ei[i,i]=1
    got=rec(ei);assert abs(np.trace(got)-1)<2e-9 and np.linalg.eigvalsh(got).min()>-2e-9
   general.append({'input_dimension':k,'input_rank':inputrank,'ambient_output_dimension':D,'output_prior_rank':len(support(channel(K,sigma))[0]),'known_coefficient_upper_bound':c,'delta':float(delta),'e_avg':float(eavg)})
# Exact boundary witnesses, no small numerical deltas are used for conclusions.
# Dephasing preserves the equiprobable Z-bit ensemble: delta=0, replacement error=1/2.
# Singleton Bell ensemble has delta=0 for EVERY channel, but local replacement
# at its marginal I/2 has distance 3/4; its mean is correlated, not product.
boundaries={'c_equals_one_dephasing':{'delta':str(F(0)),'replacement_error':str(F(1,2))},'correlated_singleton_Bell_mean':{'delta':str(F(0)),'local_replacement_error':str(F(3,4))},'untouched_reference_defeats_naive_strict_contraction':{'input_distance':str(F(1)),'output_distance':str(F(1))}}
# exact rational sanity checks of the Neumann inverse mechanism for nonnormal B
# whose Frobenius norm is <= c; the global theorem itself is analytic.
def det(a):return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
def inv3(a):
 d=det(a);assert d!=0;out=[]
 for i in range(3):
  row=[]
  for j in range(3):
   r=[x for x in range(3) if x!=j];c=[x for x in range(3) if x!=i]
   row.append((-1)**(i+j)*(a[r[0]][c[0]]*a[r[1]][c[1]]-a[r[0]][c[1]]*a[r[1]][c[0]])/d)
  out.append(row)
 return out
for seed in range(100):
 rr=np.random.default_rng(seed);B=[[F(int(x),20) for x in row] for row in rr.integers(-3,4,size=(3,3))];c=F(1,2)
 assert sum(x*x for row in B for x in row)<=c*c
 M=[[F(i==j)-B[i][j] for j in range(3)] for i in range(3)];T=inv3(M)
 assert all(sum(T[i][l]*M[l][j] for l in range(3))==F(i==j) for i in range(3) for j in range(3))
 assert all(sum(T[i][j]**2 for i in range(3))<=1/(1-c)**2 for j in range(3))
out={'scope':'analytic theorem received separately; these are independent boundary/exact-algebra/numerical diagnostics, not an empirical proof','seed':202610291342,'qubit_unreferenced_ensembles':len(rows),'qubit_product_mean_reference_ensembles':2*len(rows),'general_dimension_ensembles':len(general),'exact_rational_nonnormal_inverse_cases':100,'max_fixed_prior_residual':max_fix,'max_full_operator_deficit_identity_residual':max_identity,'max_Bloch_norm_over_c':max_bratio,'max_inverse_norm_times_1_minus_c':max_inverse,'max_pointwise_recovery_bound_excess':max_point_res,'minimum_nonreference_bound_margin':float(min_nonmargin),'minimum_complete_bound_margin':float(min_compmargin),'scope_boundary_witnesses':boundaries,'qubit_cases':rows,'general_dimension_cases':general,'passed':True}
(Path(__file__).parent/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['qubit_cases','general_dimension_cases']},indent=2))
