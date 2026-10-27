"""Replay exact mixed-bath actual source and saturated-face tangent formulas."""
exec(open('mixed_reset_purity_probe.py').read().split('best=-1e9')[0])
from scipy.integrate import quad
rng=np.random.default_rng(71023)
def f(G):
 z=np.linalg.eigvalsh(G);z=z[z>1e-14];return z@np.log(z)
def root(G):
 z,u=np.linalg.eigh(G);return (u*np.sqrt(np.maximum(z,0)))@u.conj().T
def gramvalue(d,bs,rs):
 cs=[np.sqrt(3*d*b*r) for b,r in zip(bs,rs)]
 ins=[]
 for b,c in zip(bs,cs):
  T=np.diag(np.r_[d,3*b]);T[0,1:]=T[1:,0]=c;ins.append(T)
 sz=1+sum(map(len,bs));R=np.zeros((sz,sz));R[0,0]=3*d;j=1
 for b,c in zip(bs,cs):
  k=len(b);R[j:j+k,j:j+k]=np.diag(b);R[0,j:j+k]=R[j:j+k,0]=c/np.sqrt(3);j+=k
 out=[]
 for i,j in [(0,1),(0,2),(1,2)]:
  b=np.r_[bs[i],bs[j]];c=np.r_[cs[i],cs[j]];O=np.diag(np.r_[d,b]);O[0,1:]=O[1:,0]=c/np.sqrt(6);out.append(O)
 return sum(map(f,ins))+f(R)-2*sum(map(f,out))-(3*d+3*sum(map(sum,bs)))*np.log(3)
worst=0
for case in range(18):
 k=2+case%3;p=rng.uniform(.1,.9);q=1-p;d=p/3
 Ts=[]
 for i in range(3):
  rank=k if case%2 else max(1,k-1)
  Z=rng.normal(size=(k,rank))+1j*rng.normal(size=(k,rank));Ts.append(Z@Z.conj().T)
 norm=sum(np.trace(T).real for T in Ts);Ts=[T/norm for T in Ts]
 tau=np.zeros((3*k,3*k),complex)
 for i,T in enumerate(Ts):tau[i*k:(i+1)*k,i*k:(i+1)*k]=T
 sig=np.zeros((k,k));sig[0,0]=1
 actual=delta(make(sig,tau,p));bs=[];rs=[]
 for T in Ts:
  ev,V=np.linalg.eigh(q*T/3);keep=ev>1e-13;bs.append(ev[keep]);rs.append(abs(V[0,keep])**2)
 got=gramvalue(d,bs,rs);worst=max(worst,abs(actual-got));assert abs(actual-got)<1e-11
print('actual mixed source replay18 PASS, max error',worst)
# Last case has full-rank baths and all three support caps saturated.
i=0;a,b=bs[i][:2];ra,rb=rs[i][:2]
def Gi(t):
 u=np.array([d-d*np.sum(r*bb/(bb+t)) for bb,r in zip(bs,rs)])
 return -3/(u[i]+3*t)-1/(u.sum()+t)+sum(2/(u[i]+u[j]+2*t) for j in range(3) if j!=i)
ra_der=d*(b-a)*quad(lambda t:t*Gi(t)/((a+t)*(b+t)),0,np.inf,epsabs=1e-10)[0]
a_der=-d*ra*quad(lambda t:t*Gi(t)/(a+t)**2,0,np.inf,epsabs=1e-9)[0]
b_der=-d*rb*quad(lambda t:t*Gi(t)/(b+t)**2,0,np.inf,epsabs=1e-9)[0]
h=1e-8
rp=[r.copy() for r in rs];rm=[r.copy() for r in rs];rp[i][0]+=h;rp[i][1]-=h;rm[i][0]-=h;rm[i][1]+=h
num=(gramvalue(d,bs,rp)-gramvalue(d,bs,rm))/(2*h)
print('saturated amplitude tangent',ra_der,num);assert abs(ra_der-num)<1e-7
bp=[z.copy() for z in bs];bm=[z.copy() for z in bs];bp[i][0]+=h;bp[i][1]-=h;bm[i][0]-=h;bm[i][1]+=h
num=(gramvalue(d,bp,rs)-gramvalue(d,bm,rs))/(2*h)
print('saturated spectral tangent',a_der-b_der,num);assert abs(a_der-b_der-num)<1e-5
# Replay an actual common-s eigenvector rotation, rather than only Gram coordinates.
ev,V=np.linalg.eigh(q*Ts[0]/3)
phase=np.exp(-1j*np.angle(V[0,:]));V=V*phase
assert np.max(abs(V[0,:].imag))<1e-12
h=1e-6
def actual_rot(theta):
 W=V.copy();W[:,0]=np.cos(theta)*V[:,0]+np.sin(theta)*V[:,1];W[:,1]=-np.sin(theta)*V[:,0]+np.cos(theta)*V[:,1]
 TT=(W*ev)@W.conj().T*3/q
 ta=tau.copy();ta[:k,:k]=TT
 return delta(make(sig,ta,p))
num=(actual_rot(h)-actual_rot(-h))/(2*h)
pred=ra_der*2*np.sqrt(ra*rb)
print('actual common-s eigenvector rotation',pred,num);assert abs(pred-num)<1e-7
