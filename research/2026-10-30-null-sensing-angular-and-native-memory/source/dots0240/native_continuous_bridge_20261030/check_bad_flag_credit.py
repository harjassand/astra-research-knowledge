import json,numpy as np
from scipy.linalg import solve,eigvalsh
rng=np.random.default_rng(20261030)
phases=['A0','A1','C0','C1','Q','RA0','RA1','RC0','RC1'];P=len(phases);n=2*P*2;nd=2*n
ix=lambda m,p,w: (m*P+p)*2+w
bad=np.zeros(n,bool)
for m in range(2):
 for p,name in enumerate(phases):
  for w in range(2):
   consistent= (m==0 if name=='A0' else m==1 if name in ['A1','C0','C1'] else True if name=='Q' else False)
   bad[ix(m,p,w)]=not(consistent and w==0)
bi=np.where(bad)[0];nb=len(bi)
H=np.zeros((n,n),complex)
def edge(m,p,q,g=1):
 for w in range(2):
  i,j=ix(m,p,w),ix(m,q,w);H[i,j]+=g;H[j,i]+=g
edge(1,2,3)
for m,p,q in [(1,0,5),(0,1,6),(0,2,7),(0,3,8)]:edge(m,p,q)
# Controller jumps and physical DATA/workspace-coupled counterparts.
jumps=[];physical=[]
def emit(m,p,q,U=None,rate=1):
 if U is None:U=np.eye(4)
 for s in range(2):
  j=np.zeros((n,n),complex);j[ix(m,q,0),ix(m,p,s)]=np.sqrt(rate);jumps.append(j)
  jj=np.zeros((nd,nd),complex)
  for w in range(2):
   for di in range(2):
    for do in range(2):jj[2*ix(m,q,0)+do,2*ix(m,p,w)+di]=np.sqrt(rate)*U[2*s+do,2*w+di]
  physical.append(jj)
U=np.zeros((4,4),complex);U[0,0]=1;U[2,1]=1
Q,_=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))
U[np.ix_([1,3],[2,3])]=Q
Ua,_=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))
for m in range(2):
 emit(m,3,4,U if m else np.eye(4))
 for p in range(5,9):emit(m,p,4,Ua if (m and p>=7) else np.eye(4))
 for p in [0,1,4]:emit(m,p,p)
 emit(m,1,2)
 if m==0:emit(m,4,0)
# Killed generator on bad corner, retaining all complete losses.
Hb=H[np.ix_(bi,bi)];I=np.eye(nb)
K=1j*(np.kron(I,Hb)-np.kron(Hb.T,I))
for j in jumps:
 jb=j[np.ix_(bi,bi)];aa=(j.conj().T@j)[np.ix_(bi,bi)]
 K+=np.kron(jb.T,jb.conj().T)-.5*(np.kron(I,aa)+np.kron(aa.T,I))
R=solve(K,-I.reshape(-1,order='F')).reshape((nb,nb),order='F');R=(R+R.conj().T)/2
res=np.linalg.norm((K@R.reshape(-1,order='F')+I.reshape(-1,order='F')))
rmin,rmax=eigvalsh(R)[[0,-1]];Rmax=2*rmax;beta=.1/Rmax;s0=1-beta*Rmax
S=s0*I+beta*R
# Complete graph raw animal potential for 3 unary tokens plus 1 DATA syndrome.
theta=1e-4;c=.9;tok=3;k=1;b=theta**(1-c)
def val(d,f):return (1+b*theta**(-d))*(1+b*theta**(-f))**tok-1
v0=np.array([val(d,0) for d in range(2)]);D=np.array([val(d,1)-val(d,0) for d in range(2)])
scale=max(v0+D);v0/=scale;D/=scale
Sf=np.zeros((n,n),complex);Sf[np.ix_(bi,bi)]=S
F=np.kron(np.eye(n),np.diag(v0))+np.kron(Sf,np.diag(D))
BD=np.kron(np.diag(bad.astype(float)),np.diag(D))
def gen(O,HH):
 out=1j*(HH@O-O@HH)
 for j in physical:
  aa=j.conj().T@j;out+=j.conj().T@O@j-.5*(aa@O+O@aa)
 return (out+out.conj().T)/2
fast=gen(F,np.kron(H,np.eye(2)))
slow=np.zeros((n,n),complex)
for w in range(2):
 i,j=ix(0,0,w),ix(1,1,w);slow[i,j]=slow[j,i]=1
# Small actual native-style acquisition/reversal coupling.
epsilon=beta/100
full=gen(F,np.kron(H+epsilon*slow,np.eye(2)))
q=2**(tok+k)*theta**(c*tok-(2-c)*k)/(1-theta**tok)
# Ready is guarded by verified absence of own tags in this compressed Q fixture.
creation=max(np.linalg.norm(np.diag(bad)@j@np.diag(~bad)) for j in jumps)
result={'controller_dimension':n,'bad_dimension':nb,'joint_data_dimension':nd,'resolvent_residual':float(res),'resolvent_min':float(rmin),'resolvent_max':float(rmax),'q_R':q,'s0':s0,'beta':float(beta),'epsilon':float(epsilon),'no_creation_error':float(creation),'fast_drift_maxeig':float(eigvalsh(fast+beta*BD)[-1]),'slow_drift_maxeig':float(eigvalsh(full+beta/2*BD)[-1])}
print(json.dumps(result,indent=2))
assert creation<1e-12
assert rmin>0 and res<1e-10
assert q<s0
assert result['fast_drift_maxeig']<1e-10
assert result['slow_drift_maxeig']<1e-10
