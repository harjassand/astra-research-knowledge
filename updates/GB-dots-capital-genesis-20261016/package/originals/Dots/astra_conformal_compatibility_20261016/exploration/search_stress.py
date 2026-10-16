"""Search the proposed nonlocal quadratic-stress contraction, not QC itself."""
from pathlib import Path
import torch,numpy as np,json,sys,time
root=Path(__file__).parent
torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
m=int(sys.argv[1]) if len(sys.argv)>1 else 3
nseeds=int(sys.argv[2]) if len(sys.argv)>2 else 10
steps=int(sys.argv[3]) if len(sys.argv)>3 else 250
start=int(sys.argv[4]) if len(sys.argv)>4 else 0
N=4*m+1;x,y=np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij')
modes=[(p,q) for p in range(m+1) for q in range(-m,m+1) if p>0 or q>0];Db=[]
for p,q in modes:
 for fun in [-np.sin(p*x+q*y),np.cos(p*x+q*y)]:Db.append(np.array([p*fun,q*fun])/np.hypot(p,q))
Db=torch.tensor(np.stack(Db));pairs=[(p,q) for p in range(-m,m+1) for q in range(-m,m+1) if p or q]
pi=torch.tensor([p%N for p,q in pairs]);qi=torch.tensor([q%N for p,q in pairs]);ki=torch.tensor([(p+q)%N for p,q in pairs]);w1=torch.tensor([3*(p+q)**2/((p+q)**2+p*p+q*q) for p,q in pairs])[:,None];w2=torch.tensor([-6*(p+q)*q/((p+q)**2+p*p+q*q) for p,q in pairs])[:,None]
def calc(coeff,ell):
 D=Db*torch.stack([torch.exp(ell),torch.exp(-ell)]).reshape(1,2,1,1)
 V=torch.einsum('oi,ijxy->ojxy',coeff,D).reshape(4,N,N);a,b,c,d=V;q=2*a+d
 ah=torch.fft.fft(a,dim=0)/N;bh=torch.fft.fft(b,dim=0)/N
 T1h=torch.zeros_like(ah).index_add(0,ki,w1*ah[pi]*ah[qi]);T2h=torch.zeros_like(ah).index_add(0,ki,w2*ah[pi]*bh[qi])
 T1=torch.fft.ifft(N*T1h,dim=0).real;T2=torch.fft.ifft(N*T2h,dim=0).real
 S1=2*a*q-3*a*a+c*c-2*b*c-.5*T1;S2=-a*c-.5*T2
 S1=S1-S1.mean();S2=S2-S2.mean(dim=0,keepdim=True)
 u=a*a+c*c;j=a*d-b*c
 A=(((a-d)**2+(b+c)**2)**2/8+j*j+u*j).mean();C=(u*(a+d)+2*j*q).mean();Q=(q*q+c*c).mean()
 P=(S1*S1+S2*S2).mean();return P/(4*A),C*C/(4*A*Q+1e-30),C-(q*S1+c*S2).mean()
rec=[];best=-1
for seed in range(start,start+nseeds):
 torch.manual_seed(seed);coeff=torch.nn.Parameter(torch.randn(2,len(Db)));ell=torch.nn.Parameter(torch.tensor(0.))
 if seed%4==0:
  with torch.no_grad():coeff[1]*=.1
 opt=torch.optim.LBFGS([coeff,ell],max_iter=steps,line_search_fn='strong_wolfe',tolerance_grad=1e-10,tolerance_change=1e-14)
 def closure():
  opt.zero_grad();P,_,_=calc(coeff,ell);loss=-P+1e-12*ell**4;loss.backward();return loss
 tt=time.time()
 try:opt.step(closure)
 except Exception as ex:print('ERROR',seed,repr(ex),flush=True);continue
 with torch.no_grad():
  P,R,res=calc(coeff,ell);P=float(P)
  vals={'seed':seed,'pressure_ratio':P,'cubic_ratio':float(R),'identity_residual':float(res),'log_aspect':float(ell),'seconds':time.time()-tt};rec.append(vals);print(vals,flush=True)
  if P>best:
   best=P;np.savez(root/f'stress_search_m{m}_s{start}_best.npz',coeff=coeff.numpy(),ell=ell.numpy(),m=m,modes=modes,pressure_ratio=P)
  (root/f'stress_search_m{m}_s{start}.json').write_text(json.dumps({'m':m,'N':N,'steps':steps,'records':rec,'status':'EXPLORATORY_NOT_CERTIFICATION'},indent=2))
