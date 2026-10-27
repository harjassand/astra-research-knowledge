"""Joint controlled/reference sector checks and exact budget corroboration.
No numerical experiment is used to establish the analytic theorem.
"""
import numpy as np, math
rng=np.random.default_rng(23827)
d=4; R=2
Q=np.diag([1.,1.,0.,0.]); Qj=np.kron(np.eye(2),np.kron(Q,np.eye(R)))
def randstate(n):
 z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));a=z@z.conj().T;return a/np.trace(a)
def sectorstate(proj):
 a=proj@randstate(len(proj))@proj;return a/np.trace(a)
size=2*d*R*d
swap=np.zeros((size,size),complex)
for c in range(2):
 for a in range(d):
  for r in range(R):
   for b in range(d):
    source=((c*d+a)*R+r)*d+b
    dest=((c*d+b)*R+r)*d+a
    swap[dest,source]=1
C0=np.diag([1.]*(d*R*d)+[0.]*(d*R*d));C1=np.eye(size)-C0
for p in [.001,.1,.7]:
 sigma=p*sectorstate(Q)+(1-p)*sectorstate(np.eye(d)-Q)
 for outside in [False,True]:
  a=randstate(2*d*R)
  if outside:a=(np.eye(len(Qj))-Qj)@a@(np.eye(len(Qj))-Qj);a/=np.trace(a)
  else:a=Qj@a@Qj+(np.eye(len(Qj))-Qj)@a@(np.eye(len(Qj))-Qj)
  for h in [.01,.2,-.7]:
   U=C0+C1@(np.cos(h)*np.eye(size)+1j*np.sin(h)*swap)
   out=U@np.kron(a,sigma)@U.conj().T
   out=np.trace(out.reshape(2,d,R,d,2,d,R,d),axis1=3,axis2=7).reshape(2*d*R,2*d*R)
   assert np.max(abs(Qj@out-out@Qj))<1e-12
   a11=a[d*R:,d*R:]
   expected=np.trace(Qj@a)+np.sin(h)**2*(p*np.trace(a11)-np.trace(np.kron(Q,np.eye(R))@a11))
   assert abs(np.trace(Qj@out)-expected)<1e-12
   if outside:assert np.trace(Qj@out).real<=p*np.sin(h)**2+1e-12
for p0 in [1.,.1,.01,.001]:
 for eps in [1.,.2,.01]:
  xi=eps/2;L=max(1,math.ceil(math.log(144/(p0*xi),16)));eta=(xi/(100*L))**2
  ideal=18*L*eta+162*eta**L+36*eta**(L/2)
  beta=eta+xi/(18*L)
  assert ideal<=xi/2 and beta<1/16
  assert 9*beta**L<=p0*xi/16
  assert 5*xi/4<=eps
print('PASS: 18 arbitrary joint control/reference collision cases and12 finite receiver budgets.')
