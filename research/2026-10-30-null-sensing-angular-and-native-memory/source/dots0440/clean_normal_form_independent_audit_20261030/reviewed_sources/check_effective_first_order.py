"""One-way-commit shared-lock fixture; exact normal-form commutator diagnostic.
Not native synthesis: cleanup is an abstract clock/lock jump in this finite test.
"""
import numpy as np,json

def mat(n,es):
 a=np.zeros((n,n),complex)
 for dst,src,c in es:a[dst,src]+=c
 return a

def diss(j,o):
 a=j.conj().T@j;return j.conj().T@o@j-(a@o+o@a)/2

def sqrtp(a):
 v,u=np.linalg.eigh((a+a.conj().T)/2);assert v.min()>-1e-8
 return (u*np.sqrt(np.maximum(v,0)))@u.conj().T

def gram(eps):
 # I_f,A1_f,A2_o,C_o,Q_o,Q_f
 n=6;H=mat(n,[(1,0,eps),(0,1,eps),(2,1,1),(1,2,1)])
 js=[mat(n,[e]) for e in [(3,2,1),(5,1,1),(4,2,1),(0,4,1),(0,5,1)]]
 labels=[0,1,2,3,4,4]
 for p in range(5):js.append(np.sqrt(.7)*np.diag([int(x==p) for x in labels]))
 A=np.diag([0,0,0,1,0,0])
 def K(o):return 1j*(H@o-o@H)+sum(diss(j,o) for j in js)-(A@o+o@A)/2
 cols=[]
 for k in range(n*n):
  e=np.zeros((n,n),complex);e.flat[k]=1;cols.append(K(e).ravel())
 R=np.linalg.solve(np.stack(cols,axis=1),-np.eye(n).ravel()).reshape(n,n);R=(R+R.conj().T)/2
 rmax=np.linalg.eigvalsh(R)[-1];beta=1/(2*rmax);S=.5*np.eye(n)+beta*R
 return S,beta,R

# Phases 0 idle,1 A1,2 A2,3 C,4 Q. Q can retain or lack ownership.
states=[]
for a in range(5):
 for b in range(5):
  for lock in range(3):
   ps=[a,b]
   if any(p in [2,3] and lock!=h+1 for h,p in enumerate(ps)):continue
   if lock and ps[lock-1] not in [2,3,4]:continue
   states.append((a,b,lock))
ix={s:i for i,s in enumerate(states)};n=len(states);d=3
Vd=np.diag([2.,1.,0.]);Ks=[]
for fn in [[1,1,2],[0,2,2]]:
 ks=[]
 for j,k in enumerate(fn):
  q=np.zeros((d,d));q[k,j]=1;ks.append(q)
 Ks.append(ks)

def jump(h,src,dst,locksrc=None,clear=False):
 es=[]
 for s in states:
  if s[h]!=src or locksrc is not None and s[2]!=locksrc:continue
  q=list(s);q[h]=dst
  if clear and q[2]==h+1:q[2]=0
  if src==1 and dst==2:q[2]=h+1
  if tuple(q) in ix:es.append((ix[tuple(q)],ix[s],1))
 return mat(n,es)

def Q(o,S,h,t=1.):
 G=np.eye(n,dtype=complex);loc=[]
 for ph,owned in [(0,False),(1,False),(2,True),(3,True),(4,True),(4,False)]:
  q=[0,0,0];q[h]=ph;q[2]=h+1 if owned else 0;loc.append(ix[tuple(q)])
 G[np.ix_(loc,loc)]=S
 a=np.kron(sqrtp(G),np.eye(d));ready=loc[0]
 od=o[ready*d:(ready+1)*d,ready*d:(ready+1)*d]
 ans=a.conj().T@o@a+np.kron(np.eye(n)-G,sum(k.T@od@k for k in Ks[h]))
 return (1-t)*o+t*ans

def apparatus(eps):
 Hs=[];Jss=[]
 for h in range(2):
  a=jump(h,0,1);b=jump(h,1,2,0);H=eps*(a+a.T)+(b+b.T)
  js=[np.kron(jump(h,2,3),np.eye(d)),np.kron(jump(h,1,4),np.eye(d)),np.kron(jump(h,2,4),np.eye(d))]
  js.extend(np.kron(jump(h,4,0,locksrc=label,clear=True),np.eye(d)) for label in range(3))
  js.extend(np.kron(jump(h,3,4),k) for k in Ks[h])
  for phase in range(5):js.append(np.sqrt(.7)*np.kron(np.diag([int(s[h]==phase) for s in states]),np.eye(d)))
  Hs.append(np.kron(H,np.eye(d)));Jss.append(js)
 def Lh(o,h):
  H=Hs[h];return 1j*(H@o-o@H)+sum(diss(j,o) for j in Jss[h])
 def L(o):return Lh(o,0)+Lh(o,1)
 return L,Lh

out=[]
for eps in [.2,.1,.05,.025]:
 S,beta,R=gram(eps);L,Lh=apparatus(eps);V=np.kron(np.eye(n),Vd);LV=L(V);comm=np.zeros_like(V,dtype=complex);err=0
 for h in range(2):
  Qh=lambda o:Q(o,S,h)
  own=Lh(Qh(V),h)-Qh(Lh(V,h))
  dh=Vd-sum(k.T@Vd@k for k in Ks[h]);guard=np.diag([int(s[1-h]==0) for s in states]);A=np.diag([int(s[h]==3) for s in states])
  expected=np.kron(guard@(-beta*np.eye(n)+beta*A),dh)
  err=max(err,float(np.linalg.norm(own-expected,2)))
  comm+=L(Qh(V)-V)-(Qh(LV)-LV)
 t=.02*eps**2
 T=lambda o:Q(Q(o,S,1,t),S,0,t)
 y=L(T(V));x=y.copy()
 for _ in range(20):x=y-(T(x)-x)
 out.append(dict(epsilon=eps,beta=beta,C_lifetime=float(R[3,3].real),own_commutator_identity_error=err,effective_remainder_over_t2=float(np.linalg.norm(x-LV-t*comm,2)/(t*t)),inverse_residual=float(np.linalg.norm(T(x)-y,2))))
assert max(r['own_commutator_identity_error'] for r in out)<1e-9
assert max(r['inverse_residual'] for r in out)<1e-9
print(json.dumps({'clock_states':n,'scope':'Separate irreversible commit; 27-state clean shared-lock fixture; abstract cleanup not a native physical synthesis','all_checks_pass':True,'cases':out},indent=2))
