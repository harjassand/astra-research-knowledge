"""Independent original/dual source, spectra and scalar-integral replay."""
import numpy as np
from scipy.integrate import quad
from common_filter_joint_stationarity_receiver import partial,reduction,trace_f
rng=np.random.default_rng(502);worst=0
phi=np.eye(3).reshape(-1)/np.sqrt(3);Pphi=np.outer(phi,phi)
def delta(A,n):return trace_f(A)+trace_f(partial(A,n))-trace_f(reduction(A,n))+np.log(4/3)*np.trace(A).real
def nz(H):return np.linalg.eigvalsh(H)[np.linalg.eigvalsh(H)>1e-9]
for _ in range(12):
 p=rng.uniform(.08,.92);q=1-p;w=rng.dirichlet(np.ones(3));r=rng.uniform(.04,.96,3);d=p/3;b=q*w/3;c=np.sqrt(3*d*b*r)
 tau=np.zeros((6,6),complex)
 for i in range(3):
  v=np.array([np.sqrt(r[i]),np.exp(1j*rng.uniform(0,6))*np.sqrt(1-r[i])]);tau[2*i:2*i+2,2*i:2*i+2]=w[i]*np.outer(v,v.conj())
 orig=p*np.kron(Pphi,np.diag([1,0]))+q*np.kron(np.eye(3)/3,tau)
 dual=np.zeros((30,30),complex);inp=[]
 for i in range(3):
  om=np.zeros(30);ff=np.zeros(30)
  for a in range(3):om[10*a+1+3*i+a]=1/np.sqrt(3)
  ff[10*i]=1;dual+=3*b[i]*np.outer(om,om)+d*np.outer(ff,ff)+c[i]*(np.outer(om,ff)+np.outer(ff,om))
  inp.extend(np.linalg.eigvalsh([[d,c[i]],[c[i],3*b[i]]]))
 RR=np.diag(np.r_[3*d,b]);RR[0,1:]=c/np.sqrt(3);RR[1:,0]=c/np.sqrt(3)
 ref=np.r_[np.linalg.eigvalsh(RR),np.repeat(b,2)];out=list(b)
 for i,j in [(0,1),(0,2),(1,2)]:
  O=np.diag([d,b[i],b[j]]);O[0,1:]=c[[i,j]]/np.sqrt(6);O[1:,0]=c[[i,j]]/np.sqrt(6);out.extend(np.linalg.eigvalsh(O))
 for H,ev in [(dual,inp),(partial(dual,10),ref),(reduction(dual,10)/2,out)]:
  err=max(abs(nz(H)-np.sort(ev)));worst=max(worst,err);assert err<1e-10
 def fun(t):
  u=d-c*c/(3*(b+t));return -3*np.log1p((u-d)/(d+3*t)).sum()-np.log1p((u.sum()-3*d)/(3*d+t))+2*sum(np.log1p((u[i]+u[j]-2*d)/(2*d+2*t)) for i,j in [(0,1),(0,2),(1,2)])
 val=quad(fun,0,np.inf,epsabs=1e-10)[0]
 for vv in [delta(orig,6),delta(dual,10)]:worst=max(worst,abs(val-vv));assert abs(val-vv)<1e-8
print('PASS12 original/dual complex sources, all spectra and integral; max error',worst)
