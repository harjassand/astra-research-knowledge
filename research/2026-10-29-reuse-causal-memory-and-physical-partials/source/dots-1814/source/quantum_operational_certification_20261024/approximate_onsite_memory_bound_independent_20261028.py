#!/usr/bin/env python3
"""Deterministic finite-matrix checks; zero source draws and zero RNG draws."""
import itertools,json,math
import numpy as np
from scipy.linalg import expm
from pathlib import Path
from fractions import Fraction
P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]
def kron(xs):
    r=np.ones((1,1),complex)
    for x in xs:r=np.kron(r,x)
    return r
def pauli_at(n,i,j):return kron([P[j] if k==i else P[0] for k in range(n)])
def norm(x):return float(np.linalg.norm(x,2))
def ptr_site(x,n,i):
    out=np.zeros((2,2),complex)
    for a,b in itertools.product(range(2),repeat=2):
        for rest in itertools.product(range(2),repeat=n-1):
            ia=list(rest);ib=list(rest);ia.insert(i,a);ib.insert(i,b)
            ia=sum(v<<(n-1-k) for k,v in enumerate(ia));ib=sum(v<<(n-1-k) for k,v in enumerate(ib))
            out[a,b]+=x[ia,ib]
    return out
def partial_trace_logical(x,d,g):return np.trace(x.reshape(d,g,d,g),axis1=0,axis2=2)
def proper_fit(m):
    u,_,vh=np.linalg.svd(m);c=np.eye(3);c[-1,-1]=np.linalg.det(u@vh)
    return u@c@vh
def rotation(v):return np.array([[np.trace(P[a+1]@v@P[b+1]@v.conj().T).real/2 for b in range(3)] for a in range(3)])
def unitary_from_rotation(r):
    # A stable eigenvector construction of the usual quaternion objective; check only, not finite-control implementation.
    m=r;K=np.zeros((4,4));K[0,0]=np.trace(m)
    K[1,1]=m[0,0]-m[1,1]-m[2,2];K[2,2]=-m[0,0]+m[1,1]-m[2,2];K[3,3]=-m[0,0]-m[1,1]+m[2,2]
    K[0,1]=K[1,0]=m[2,1]-m[1,2];K[0,2]=K[2,0]=m[0,2]-m[2,0];K[0,3]=K[3,0]=m[1,0]-m[0,1]
    K[1,2]=K[2,1]=m[0,1]+m[1,0];K[1,3]=K[3,1]=m[0,2]+m[2,0];K[2,3]=K[3,2]=m[1,2]+m[2,1]
    _,v=np.linalg.eigh(K);u=v[:,-1]
    return u[0]*P[0]-1j*sum((u[k]*P[k] for k in range(1,4)),np.zeros((2,2),complex))
checks=[];max_res={k:0. for k in ['bell_bound','bloch_cap','normalized_cap','proper_fit','learned_bell_bound','povm_sum','oracle_identity','oracle_upper','duhamel','wrong_site']}
for q in [1,2,3]:
 d=2**q;g=2;n=q+1
 for angle in [.015,.07,.19]:
  for variant in range(3):
   vs=[expm(-1j*(.09*(i+1)*P[1]+.07*(variant+1)*P[2]+.04*P[3])) for i in range(q)]
   U0=kron(vs+[expm(-.08j*P[1])]);V=kron(vs+[P[0]])
   H=np.zeros((d*g,d*g),complex)
   for i in range(q):
    H+=(.31+.03*i)*pauli_at(n,i,1)@pauli_at(n,q,3)
    H+=(.21+.02*variant)*pauli_at(n,i,3)@pauli_at(n,q,1)
   if q>1:H+=.17*pauli_at(n,0,2)@pauli_at(n,1,1)
   U=expm(-1j*angle*H)@U0
   taus=[];norm_cols=[];Rtrue=[];noise2=0.;fitR=[]
   for i in range(q):
    R=rotation(vs[i]);Rtrue.append(R);cols=[];ti=[]
    for col,j in [(0,1),(2,3)]:
     A=V@pauli_at(n,i,j)@V.conj().T;B=U@pauli_at(n,i,j)@U.conj().T;tau=norm(A-B);ti.append(tau)
     incident=angle*norm(H@A-A@H);max_res['duhamel']=max(max_res['duhamel'],tau-incident)
     h=(P[0]+.29*P[1]+(.15+.03*i)*P[2]+(.11+.02*j)*P[3])/2
     delta=U@np.kron(pauli_at(q,i,j)/d,h)@U.conj().T
     reduced=ptr_site(delta,n,i);c=np.array([np.trace(x@reduced).real for x in P[1:]])
     if j==1:
      Az=V@pauli_at(n,i,3)@V.conj().T;Bz=U@pauli_at(n,i,3)@U.conj().T;tz=norm(Az-Bz)
      for k in range(n):
       if k!=i:
        wrong=ptr_site(delta,n,k);wrong_norm=sum(abs(np.linalg.eigvalsh(wrong)))
        max_res['wrong_site']=max(max_res['wrong_site'],wrong_norm-tz)

     v=c/np.linalg.norm(c)
     max_res['bloch_cap']=max(max_res['bloch_cap'],np.linalg.norm(c-R[:,col])-tau,np.linalg.norm(c)-1,1-tau*tau/2-R[:,col]@c)
     max_res['normalized_cap']=max(max_res['normalized_cap'],np.linalg.norm(v-R[:,col])-tau)
     lam=.17+.18*((i+j+variant)%4)
     noise=.0001*np.array([i+1,-j,variant+1.]);noise2+=noise@noise
     empirical=lam*c+noise;cols.append(empirical/np.linalg.norm(empirical))
    mat=np.column_stack([cols[0],np.zeros(3),cols[1]]);rh=proper_fit(mat);fitR.append(rh);taus.extend(ti)
    eta=np.linalg.norm((mat-R)[:,[0,2]]);s=np.linalg.norm((rh-R)[:,[0,2]])
    max_res['proper_fit']=max(max_res['proper_fit'],s-2*eta)
   W=V.conj().T@U;K=partial_trace_logical(W,d,g)/d;T=K.conj().T@K
   worst=1-np.linalg.eigvalsh(T).min();base=sum(x*x for x in taus)/4
   max_res['bell_bound']=max(max_res['bell_bound'],worst-base)
   Vhat=kron([unitary_from_rotation(r) for r in fitR]+[P[0]]);W=Vhat.conj().T@U
   K=partial_trace_logical(W,d,g)/d;TI=K.conj().T@K;worst_learned=1-np.linalg.eigvalsh(TI).min()
   a=1-max(taus)**2/2;bound=((1.5*math.sqrt(sum(x*x for x in taus)))+2*math.sqrt(noise2)/(.17*a))**2
   max_res['learned_bell_bound']=max(max_res['learned_bell_bound'],worst_learned-bound)
   Ts=[]
   for inds in itertools.product(range(4),repeat=q):
    pp=kron([P[j] for j in inds]);kk=partial_trace_logical(W@np.kron(pp,P[0]),d,g)/d;Ts.append(kk.conj().T@kk)
   max_res['povm_sum']=max(max_res['povm_sum'],norm(sum(Ts)-P[0]))
   GI=(P[0]+.21*P[1]+.17*P[2]+.08*P[3])/2
   ev,evec=np.linalg.eigh(GI);root=evec@np.diag(np.sqrt(ev))@evec.conj().T
   Gs=[GI]
   for k in range(1,len(Ts)):
    C=(.4*P[0]+.08*math.sin(k)*P[1]+.1*math.cos(k)*P[2]+.08*P[3])
    Gs.append(root@C@root)
   total=sum(np.trace(x).real for x in Gs);Gs=[x/total for x in Gs]
   excess=np.trace(Gs[0]).real-sum(np.trace(t@gg).real for t,gg in zip(Ts,Gs))
   identity=sum(np.trace(Ts[k]@(Gs[0]-Gs[k])).real for k in range(1,len(Ts)))
   max_res['oracle_identity']=max(max_res['oracle_identity'],abs(excess-identity))
   max_res['oracle_upper']=max(max_res['oracle_upper'],excess-worst_learned*np.trace(Gs[0]).real)
   checks.append(dict(q=q,angle=angle,variant=variant,tau_max=max(taus),base_upper=base,worst_identity_loss=worst,worst_fit_loss=worst_learned,normalized_fit_upper=bound))
lower=[]
for q in range(1,6):
 for theta in [.03,.2,.7,math.pi/2]:
  tau=2*math.sin(theta/2);p=tau*tau/4
  probs=[(1-p)**(q-k)*p**k for k in range(q+1)]
  exact=1-max(probs);claimed=1-(1-tau*tau/4)**q
  assert abs(exact-claimed)<1e-12
  # q=1 directly checks the full controlled gate and generator mismatch.
  if q==1:
   U=np.kron(P[0],np.diag([1.,0.]))+np.kron(expm(-.5j*theta*P[3]),np.diag([0.,1.]))
   actual=norm(U@np.kron(P[1],P[0])@U.conj().T-np.kron(P[1],P[0]));assert abs(actual-tau)<1e-12
  lower.append(dict(q=q,theta=theta,tau=tau,minimax_lower=claimed))
exact_lower=[]
for q in range(1,9):
 for r in [Fraction(1,100),Fraction(1,20),Fraction(1,5),Fraction(1,3)]:
  c=(1-r*r)/(1+r*r);s=2*r/(1+r*r)
  assert c*c+s*s==1
  p=s*s;tau2=4*p
  assert p<=Fraction(1,2)
  weights=[(1-p)**(q-k)*p**k for k in range(q+1)]
  assert max(weights)==(1-p)**q
  floor=1-(1-tau2/4)**q
  assert floor==1-max(weights)
  assert floor<=min(Fraction(1),q*tau2/4)
  exact_lower.append(dict(q=q,stereographic=str(r),tau_squared=str(tau2),minimax_lower=str(floor)))
assert max(max_res.values())<1e-11,max_res
result={'status':'PASS deterministic matrix identities and inequalities','source_draws':0,'rng_draws':0,'coupled_unitary_fixtures':len(checks),'controlled_rotation_lower_fixtures':len(lower),'exact_rational_finite_q_lower_fixtures':len(exact_lower),'maximum_positive_residuals':max_res,'fixtures':checks,'lower_fixtures':lower,'exact_lower_fixtures':exact_lower}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['fixtures','lower_fixtures','exact_lower_fixtures']},indent=2))
