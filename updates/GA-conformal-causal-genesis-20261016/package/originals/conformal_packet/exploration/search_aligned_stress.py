"""Adversarial test of a triad-balanced, angle-adapted nonlocal stress."""
from pathlib import Path
import torch,numpy as np,json,sys,time
root=Path(__file__).parent
torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
m=int(sys.argv[1]) if len(sys.argv)>1 else 3;nseeds=int(sys.argv[2]) if len(sys.argv)>2 else 8;steps=int(sys.argv[3]) if len(sys.argv)>3 else 300;start=int(sys.argv[4]) if len(sys.argv)>4 else 0
N=4*m+1;x,y=np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij');modes=[(p,q) for p in range(m+1) for q in range(-m,m+1) if p>0 or q>0];Db=[]
for p,q in modes:
 for fun in [-np.sin(p*x+q*y),np.cos(p*x+q*y)]:Db.append(np.array([p*fun,q*fun])/np.hypot(p,q))
Db=torch.tensor(np.stack(Db));freq=[(p,q) for p in range(-m,m+1) for q in range(-m,m+1) if p!=0]
pairs=np.array([(p,l) for p in freq for l in freq],dtype=int);pv=torch.tensor(pairs[:,0],dtype=torch.float64);lv=torch.tensor(pairs[:,1],dtype=torch.float64);kv=pv+lv
pi=torch.tensor([(int(p[0])%N)*N+int(p[1])%N for p in pv]);li=torch.tensor([(int(p[0])%N)*N+int(p[1])%N for p in lv]);ki=torch.tensor([(int(p[0])%N)*N+int(p[1])%N for p in kv])
kmask=kv[:,0]!=0

def calc(coeff,ell):
 scale=torch.stack([torch.exp(ell),torch.exp(-ell)])
 V=torch.einsum('oi,ijxy->ojxy',coeff,Db*scale.reshape(1,2,1,1)).reshape(4,N,N);a,b,c,d=V;q=2*a+d
 p=pv*scale;l=lv*scale;k=kv*scale
 fp=p[:,0]**2/p.square().sum(1);fl=l[:,0]**2/l.square().sum(1);fk=k[:,0]**2/(k.square().sum(1)+1e-100)
 h=fk/(fp+fl+fk+1e-100);F=1-3*h;G=torch.zeros_like(F);G[kmask]=3*h[kmask]*k[kmask,1]/k[kmask,0]
 ah=(torch.fft.fft2(a)/(N*N)).reshape(-1);prod=ah[pi]*ah[li]
 Fh=torch.zeros(N*N,dtype=torch.complex128).index_add(0,ki,F*prod);Gh=torch.zeros_like(Fh).index_add(0,ki,G*prod)
 FF=torch.fft.ifft2(Fh.reshape(N,N)*N*N).real;GG=torch.fft.ifft2(Gh.reshape(N,N)*N*N).real
 u=a*a+c*c;j=a*d-b*c
 S1=u/2+2*j+FF/2;S2=c*d/2+GG/2
 # exact gauges preserving the trilinear pairing may be tested separately
 S1=S1-S1.mean();S2=S2-S2.mean(dim=0,keepdim=True)
 AA=(((a-d)**2+(b+c)**2)**2/8+j*j+u*j).mean();CC=(u*(a+d)+2*j*q).mean();QQ=(q*q+c*c).mean()
 PP=((q*S1+c*S2).square()/(q*q+c*c+1e-20*QQ)).mean();return PP/(4*AA),CC*CC/(4*AA*QQ+1e-30),(CC-(q*S1+c*S2).mean())/(1+CC.abs())
rec=[];best=-1
for seed in range(start,start+nseeds):
 torch.manual_seed(seed);coeff=torch.nn.Parameter(torch.randn(2,len(Db)));ell=torch.nn.Parameter(torch.tensor(0.))
 opt=torch.optim.LBFGS([coeff,ell],max_iter=steps,line_search_fn='strong_wolfe',tolerance_grad=1e-10,tolerance_change=1e-14)
 def closure():
  opt.zero_grad();P,_,_=calc(coeff,ell);loss=-P+1e-10*ell**4;loss.backward();return loss
 tt=time.time()
 try:opt.step(closure)
 except Exception as ex:print('ERROR',seed,repr(ex),flush=True);continue
 with torch.no_grad():
  P,R,res=calc(coeff,ell);P=float(P);vals={'seed':seed,'pressure_ratio':P,'cubic_ratio':float(R),'identity_relative_residual':float(res),'log_aspect':float(ell),'seconds':time.time()-tt};rec.append(vals);print(vals,flush=True)
  if P>best:
   best=P;np.savez(root/f'aligned_stress_m{m}_s{start}_best.npz',coeff=coeff.numpy(),ell=ell.numpy(),m=m,modes=modes,pressure_ratio=P)
  (root/f'aligned_stress_m{m}_s{start}.json').write_text(json.dumps({'m':m,'N':N,'steps':steps,'records':rec,'status':'EXPLORATORY_NOT_CERTIFICATION'},indent=2))
