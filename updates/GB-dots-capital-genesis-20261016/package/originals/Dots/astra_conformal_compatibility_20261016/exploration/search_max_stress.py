"""Median-horizontal-frequency trilinear representation; explore its norm."""
from pathlib import Path
import torch,numpy as np,json,sys,time,sympy as sp
root=Path(__file__).parent
torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
m=int(sys.argv[1]) if len(sys.argv)>1 else 3;nseeds=int(sys.argv[2]) if len(sys.argv)>2 else 8;steps=int(sys.argv[3]) if len(sys.argv)>3 else 300;start=int(sys.argv[4]) if len(sys.argv)>4 else 0
N=4*m+1;x,y=np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij');modes=[(p,q) for p in range(m+1) for q in range(-m,m+1) if p>0 or q>0];Db=[]
for p,q in modes:
 for fun in [-np.sin(p*x+q*y),np.cos(p*x+q*y)]:Db.append(np.array([p*fun,q*fun])/np.hypot(p,q))
Db=torch.tensor(np.stack(Db));freq=[(p,q) for p in range(-m,m+1) for q in range(-m,m+1) if p or q]
P=[];L=[];K=[];W=[]
for p in freq:
 for l in freq:
  k=(p[0]+l[0],p[1]+l[1]);xx=[abs(k[0]),abs(p[0]),abs(l[0])];med=max(xx)
  if k[0]!=0 and abs(k[0])==med:
   P.append(p);L.append(l);K.append(k);W.append(1/sum(t==med for t in xx))
pv=torch.tensor(P,dtype=torch.float64);lv=torch.tensor(L,dtype=torch.float64);kv=torch.tensor(K,dtype=torch.float64);weights=torch.tensor(W)
pi=torch.tensor([(p[0]%N)*N+p[1]%N for p in P]);li=torch.tensor([(p[0]%N)*N+p[1]%N for p in L]);ki=torch.tensor([(p[0]%N)*N+p[1]%N for p in K])
aa,bb,cc,dd=sp.symbols('a b c d');XX=[aa,bb,cc,dd];CP=aa**3+5*aa*aa*dd-4*aa*bb*cc+aa*cc*cc+2*aa*dd*dd-2*bb*cc*dd+cc*cc*dd
TC=np.array([[[float(sp.diff(CP,XX[i],XX[j],XX[k])/6) for k in range(4)] for j in range(4)] for i in range(4)])
terms=[(i,j,k,float(TC[i,j,k])) for i in range(4) for j in range(4) for k in range(4) if TC[i,j,k]]
def calc(coeff,ell):
 scale=torch.stack([torch.exp(ell),torch.exp(-ell)])
 V=torch.einsum('oi,ijxy->ojxy',coeff,Db*scale.reshape(1,2,1,1)).reshape(4,N,N);a,b,c,d=V;q=2*a+d
 vh=(torch.fft.fft2(V)/(N*N)).reshape(4,-1);pol=[torch.zeros(len(W),dtype=torch.complex128) for _ in range(4)]
 for i,j,k,val in terms:pol[i]=pol[i]+val*vh[j,pi]*vh[k,li]
 slope=kv[:,1]/kv[:,0]*torch.exp(-2*ell)
 f1=3*weights*(pol[0]+slope*pol[1])/2
 f2=3*weights*(pol[2]+slope*pol[3]-slope*(pol[0]+slope*pol[1])/2)
 sh1=torch.zeros(N*N,dtype=torch.complex128).index_add(0,ki,f1);sh2=torch.zeros_like(sh1).index_add(0,ki,f2)
 S1=torch.fft.ifft2(sh1.reshape(N,N)*N*N).real;S2=torch.fft.ifft2(sh2.reshape(N,N)*N*N).real
 u=a*a+c*c;j=a*d-b*c
 AA=(((a-d)**2+(b+c)**2)**2/8+j*j+u*j).mean();CC=(u*(a+d)+2*j*q).mean();QQ=(q*q+c*c).mean()
 PP=(S1*S1+S2*S2).mean();return PP/(4*AA),CC*CC/(4*AA*QQ+1e-30),(CC-(q*S1+c*S2).mean())/(1+CC.abs())
rec=[];best=-1
for seed in range(start,start+nseeds):
 torch.manual_seed(seed);coeff=torch.nn.Parameter(torch.randn(2,len(Db)));ell=torch.nn.Parameter(torch.tensor(0.))
 opt=torch.optim.LBFGS([coeff,ell],max_iter=steps,line_search_fn='strong_wolfe',tolerance_grad=1e-10,tolerance_change=1e-14)
 def closure():
  opt.zero_grad();P,_,_=calc(coeff,ell);loss=-P+1e-2*ell**4;loss.backward();return loss
 tt=time.time()
 try:opt.step(closure)
 except Exception as ex:print('ERROR',seed,repr(ex),flush=True);continue
 with torch.no_grad():
  P,R,res=calc(coeff,ell);P=float(P);vals={'seed':seed,'pressure_ratio':P,'cubic_ratio':float(R),'identity_relative_residual':float(res),'log_aspect':float(ell),'seconds':time.time()-tt};rec.append(vals);print(vals,flush=True)
  if P>best:
   best=P;np.savez(root/f'max_stress_m{m}_s{start}_best.npz',coeff=coeff.numpy(),ell=ell.numpy(),m=m,modes=modes,pressure_ratio=P)
  (root/f'max_stress_m{m}_s{start}.json').write_text(json.dumps({'m':m,'N':N,'steps':steps,'records':rec,'status':'EXPLORATORY_NOT_CERTIFICATION'},indent=2))
