"""Finite clean-controller diagnostic: not native physical synthesis or Tanner proof.
Two hubs have weak ready/acquire edges, a shared lock, fast acquisition,
DATA-identity acquisition aborts, Phi terminal gains, and DATA-free cleanup.
"""
import numpy as np, json


def sqrtm(a):
    v,u=np.linalg.eigh((a+a.conj().T)/2)
    assert v.min()>-1e-9, v.min()
    return (u*np.sqrt(np.maximum(v,0)))@u.conj().T

def matrix(n, transitions):
    a=np.zeros((n,n),complex)
    for dst,src,coef in transitions:a[dst,src]+=coef
    return a

def dissip(j,o):
    a=j.conj().T@j
    return j.conj().T@o@j-(a@o+o@a)/2

def killed_gram(eps, gamma=.7):
    n=4; H=matrix(n,[(1,0,eps),(0,1,eps),(2,1,1),(1,2,1)])
    js=[matrix(n,[(0,1,1)]),matrix(n,[(0,3,1)])]
    js += [np.sqrt(gamma)*np.diag([int(k==i) for k in range(n)]) for i in range(n)]
    A=np.diag([0,0,1,0])
    def K(o): return 1j*(H@o-o@H)+sum(dissip(j,o) for j in js)-(A@o+o@A)/2
    E=[]
    for k in range(n*n):
        x=np.zeros((n,n),complex);x.flat[k]=1;E.append(K(x).reshape(-1))
    km=np.stack(E,axis=1)
    R=np.linalg.solve(km,-np.eye(n).reshape(-1)).reshape(n,n);R=(R+R.conj().T)/2
    rmax=np.linalg.eigvalsh(R)[-1]; beta=1/(2*rmax)
    S=.5*np.eye(n)+beta*R
    return S,beta,R

states=[]
for x in range(4):
 for y in range(4):
  if x<2 and y<2:states.append((x,y,0))
  if x>=2 and y<2:states.append((x,y,1))
  if y>=2 and x<2:states.append((x,y,2))
ix={s:i for i,s in enumerate(states)};n=len(states);d=3
P=np.diag([2,1,0])
fns=[[1,1,2],[0,2,2]]
Ks=[]
for fn in fns:
 ks=[]
 for j,dst in enumerate(fn):
  a=np.zeros((d,d));a[dst,j]=1;ks.append(a)
 Ks.append(ks)

def hubjump(h,src,dst,locksrc=None,lockdst=None):
 trans=[]
 for s in states:
  if s[h]!=src or (locksrc is not None and s[2]!=locksrc):continue
  t=list(s);t[h]=dst
  if lockdst is not None:t[2]=lockdst
  if tuple(t) in ix:trans.append((ix[tuple(t)],ix[s],1))
 return matrix(n,trans)

def cp_h(O,S,h,t,analytic=False):
 G=np.eye(n,dtype=complex)
 loc=[]
 for q in range(4):
  state=[0,0,0];state[h]=q
  if q>=2:state[2]=h+1
  loc.append(ix[tuple(state)])
 G[np.ix_(loc,loc)]=S
 a=np.asarray(sqrtm(G),complex);b=np.asarray(sqrtm(np.eye(n)-G),complex)
 AA=np.kron(a,np.eye(d))
 ans=AA.conj().T@O@AA
 if analytic:
  # The isolated guard has exactly the four h states with the other hub idle.
  ready=loc[0]
  block=O[ready*d:(ready+1)*d,ready*d:(ready+1)*d]
  phi=sum(k.conj().T@block@k for k in Ks[h])
  ans+=np.kron(np.eye(n)-G,phi)
 else:
  for k in Ks[h]:
   B=np.kron(b,k);ans+=B.conj().T@O@B
 return (1-t)*O+t*ans

out=[]
for eps in [.1,.05,.025,.0125,.00625,.003125]:
 S,beta,R=killed_gram(eps)
 H=np.zeros((n,n),complex);jumps=[]
 for h in range(2):
  v=hubjump(h,0,1);H+=eps*(v+v.conj().T)
  v=hubjump(h,1,2,0,h+1);H+=v+v.conj().T
  jumps.append(np.kron(hubjump(h,1,0),np.eye(d)))
  jumps.append(np.kron(hubjump(h,3,0,h+1,0),np.eye(d)))
  jt=hubjump(h,2,3)
  jumps.extend(np.kron(jt,k) for k in Ks[h])
  for phase in range(4):
   q=np.diag([int(s[h]==phase) for s in states]);jumps.append(np.sqrt(.7)*np.kron(q,np.eye(d)))
 HH=np.kron(H,np.eye(d));V=np.kron(np.eye(n),P)
 t=.1
 F=cp_h(cp_h(V,S,1,t,analytic=True),S,0,t,analytic=True)
 LF=1j*(HH@F-F@HH)+sum(dissip(j,F) for j in jumps)
 groups=[]
 for count in range(3):
  groups.append([i*d+j for i,s in enumerate(states) if (s[0]!=0)+(s[1]!=0)==count for j in range(d)])
 get=lambda a,b: LF[np.ix_(groups[a],groups[b])]
 norm=lambda x:float(np.linalg.norm(x,2))
 l00=get(0,0);d0=P-sum(k.T@P@k for k in Ks[0]);d1=P-sum(k.T@P@k for k in Ks[1])
 expected=-t*beta*(d0+d1)
 out.append(dict(epsilon=eps,beta=beta,ready_credit=float((1-S[0,0]).real),idle_residual_over_eps3=norm(l00-expected)/eps**3,idle_single_over_eps3=norm(get(0,1))/eps**3,idle_pair_over_eps2=norm(get(0,2))/eps**2,single_positive_over_eps2=max(0,float(np.linalg.eigvalsh(get(1,1))[-1]))/eps**2,single_pair_over_eps=norm(get(1,2))/eps,pair_norm=norm(get(2,2)),idle_eigs_over_eps2=(np.linalg.eigvalsh(l00)/eps**2).tolist()))
print(json.dumps({'scope':'12-state clean shared-lock diagnostic, 3-state monotone noncommuting idempotent DATA channels; not full Tanner/native proof','credit':'Analytic virtual-ready-reset B branch, not principal-sqrt B branch','clock_states':states,'cases':out},indent=2))
