"""Finite actual-source ideal-frame checks and complete synthesis budget checks."""
import numpy as np, math
z=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag([1,z,z*z]);Ws=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a in range(3) for b in range(3)]
d=4;V=np.eye(d)[:,:3];Q=np.kron(np.eye(3),V@V.T);v=np.zeros(3*d)
for j in range(3):v[j*d+j]=1/np.sqrt(3)
Phi=np.outer(v,v);count=0
for p in [.01,.05,.2,.7]:
 for a in [1e-7,1e-5,1e-3]:
  q=1-p;tauv=np.array([np.sqrt(a),0,0,np.sqrt(1-a)]);tau=np.outer(tauv,tauv)
  D=p*Q/3+2*q*np.kron(np.eye(3),tau)/3;H=p*Phi-D
  ev,U=np.linalg.eigh(H);lam=ev[-1];chi=U[:,-1];phase=np.vdot(v,chi);chi*=np.conj(phase)/abs(phase)
  t=(2*p/3-lam)/p
  polev=np.linalg.eigvalsh(p*(V@V.T)/3-q*tau/3);e=3*(p/3-polev[-3])
  if e>p/160:continue
  frame=np.column_stack([np.kron(W,np.eye(d))@chi for W in Ws]);Gram=frame.conj().T@frame
  assert np.linalg.norm(Gram-np.eye(9),2)<=16*t+1e-12
  previous=np.eye(3*d,dtype=complex);reset=0;codebound=0
  for j,W in enumerate(Ws):
   ch=frame[:,j];row=ch.conj()@previous;K=W.T@row.reshape(3,d)/np.sqrt(3);L=K@V
   err=np.linalg.norm(L-np.eye(3)/3,2)
   assert err<=130*t+1e-11
   codebound+=2*(np.linalg.norm(L,2)+1/3)*err
   S0=q*np.kron(np.eye(3)/3,tau);reset+=(row@S0@row.conj()).real
   previous=(np.eye(3*d)-np.outer(ch,ch.conj()))@previous
  assert codebound<=2340*t+1e-10
  assert reset<=30*e+1e-10
  count+=1
budgets=0
for p0 in [1.,.1,1e-3,1e-9]:
 for xi in [1.,.1,.001,1e-6]:
  L=max(1,math.ceil(math.log(1000/(p0*xi),16)));eta=(xi/(100*L))**2;h=xi/(1e9*L)
  eh=100000*h*math.exp(50000*h);eL=100000*L*h*math.exp(50000*L*h)
  u=L*(4*math.sqrt(eta)+256*h);beta=eta+eh;k=eL+eta**L
  assert eL<=xi/9000 and eh<=xi/(9000*L)
  assert u<=xi/20 and beta<=1/16 and beta**L<=p0*xi/1000
  assert k<=xi/4000 and k+eL+2*u<=xi/9
  assert 3*beta**L/p0+eh/(1-beta)+2*u<=xi/9
  f=0
  for j in range(1,10):
   f=10/9+(1+k)*f+5
   assert f<=7*j
  local=xi/18+.5*(7*8*k+xi/9)+2*u*18
  assert local<2*xi
  budgets+=1
print('PASS',count,'actual-source ideal nine-label cases;',budgets,'full resource/error budget cases.')
