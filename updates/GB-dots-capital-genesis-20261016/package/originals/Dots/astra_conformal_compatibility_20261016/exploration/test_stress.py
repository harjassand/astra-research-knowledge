import numpy as np
from pathlib import Path
root=Path(__file__).parent

def stress(V,m):
 N=V.shape[-1];a,b,c,d=V;q=2*a+d
 ah=np.fft.fft(a,axis=0)/N;bh=np.fft.fft(b,axis=0)/N
 T1h=np.zeros_like(ah);T2h=np.zeros_like(ah)
 for p in range(-m,m+1):
  for l in range(-m,m+1):
   k=p+l;D=k*k+p*p+l*l
   if D:
    T1h[k%N]+=3*k*k/D*ah[p%N]*ah[l%N]
    T2h[k%N]+=-6*k*l/D*ah[p%N]*bh[l%N]
 T1=np.fft.ifft(T1h*N,axis=0).real;T2=np.fft.ifft(T2h*N,axis=0).real
 S1=2*a*q-3*a*a+c*c-2*b*c-.5*T1
 S2=-a*c-.5*T2
 S1-=S1.mean();S2-=S2.mean(axis=0,keepdims=True)
 u=a*a+c*c;j=a*d-b*c
 AA=(((a-d)**2+(b+c)**2)**2/8+j*j+u*j).mean();CC=(u*(a+d)+2*j*q).mean();QQ=(q*q+c*c).mean()
 return {'pressure_ratio':float((S1*S1+S2*S2).mean()/(4*AA)), 'cubic_ratio':float(CC*CC/(4*AA*QQ)), 'identity_residual':float(CC-(q*S1+c*S2).mean()),'a3_identity':float((a*a*a).mean()-.5*(q*T1+c*T2).mean())}
def build(m,coeff,ell=0):
 N=4*m+1;x,y=np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij');modes=[(p,q) for p in range(m+1) for q in range(-m,m+1) if p>0 or q>0];D=[]
 for p,q in modes:
  for fun in [-np.sin(p*x+q*y),np.cos(p*x+q*y)]:D.append(np.array([p*np.exp(ell)*fun,q*np.exp(-ell)*fun])/np.hypot(p,q))
 return np.einsum('oi,ijxy->ojxy',coeff,np.array(D)).reshape(4,N,N)
if __name__=='__main__':
 for fn in root.glob('cubic_search*_best.npz'):
  z=np.load(fn);m=int(z['m']);v=build(m,z['coeff'],float(z['ell']));print(fn.name,stress(v,m))
 for seed in range(8):
  rng=np.random.default_rng(seed);m=3;nm=(m+1)*(2*m+1)+m-2*m-1 # not used
  modes=[(p,q) for p in range(m+1) for q in range(-m,m+1) if p>0 or q>0]
  cc=rng.normal(size=(2,2*len(modes)));print(seed,stress(build(m,cc),m))
