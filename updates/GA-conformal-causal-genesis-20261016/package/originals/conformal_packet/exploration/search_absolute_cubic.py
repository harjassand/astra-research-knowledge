"""Exploratory compatible Fourier ratio. No search result certifies an inequality."""
from pathlib import Path
import torch,numpy as np,json,sys,time
root=Path(__file__).parent
torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
m=int(sys.argv[1]) if len(sys.argv)>1 else 3
nseeds=int(sys.argv[2]) if len(sys.argv)>2 else 8
steps=int(sys.argv[3]) if len(sys.argv)>3 else 200
start=int(sys.argv[4]) if len(sys.argv)>4 else 0
N=4*m+1
x,y=np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij')
modes=[(p,q) for p in range(m+1) for q in range(-m,m+1) if p>0 or q>0]
Db=[]
for p,q in modes:
 th=(p*x+q*y).flatten()
 for fun in [-np.sin(th),np.cos(th)]:Db.append(np.array([p*fun,q*fun])/np.sqrt(p*p+q*q))
Db=torch.tensor(np.stack(Db))
def calc(coeff,ell):
 D=Db*torch.stack([torch.exp(ell),torch.exp(-ell)]).reshape(1,2,1)
 V=torch.einsum('oi,ijg->ojg',coeff,D).reshape(4,-1)
 a,b,c,d=V;u=a*a+c*c;j=a*d-b*c
 A=(((a-d)**2+(b+c)**2)**2/8+j*j+u*j).mean()
 Q=((2*a+d)**2+c*c).mean()
 C=(a**3+5*a*a*d-4*a*b*c+a*c*c+2*a*d*d-2*b*c*d+c*c*d).abs().mean()
 return C*C/(4*A*Q+1e-30),A,Q,C,V
out=root/f'absolute_cubic_search_m{m}_s{start}.json';rec=[];best=-1
for seed in range(start,start+nseeds):
 torch.manual_seed(seed)
 coeff=torch.nn.Parameter(torch.randn(2,len(Db)))
 ell=torch.nn.Parameter(torch.tensor(float((seed%5)-2)/2))
 if seed%4==0:
  with torch.no_grad():
   coeff[1]*=.1
 if seed%4==1:
  with torch.no_grad():
   coeff*=.05
   for i,(p,q) in enumerate(modes):
    if q==0:coeff[0,2*i:2*i+2]*=20
 opt=torch.optim.LBFGS([coeff,ell],max_iter=steps,line_search_fn='strong_wolfe',tolerance_grad=1e-10,tolerance_change=1e-14)
 def closure():
  opt.zero_grad();rho,*_=calc(coeff,ell)
  loss=-rho+1e-12*ell**4;loss.backward();return loss
 tt=time.time()
 try:opt.step(closure)
 except Exception as ex: print('ERROR',seed,repr(ex),flush=True);continue
 with torch.no_grad():
  rho,A,Q,C,V=calc(coeff,ell);rho=float(rho)
  vals={'seed':seed,'rho':rho,'A':float(A),'Q':float(Q),'C':float(C),'log_aspect':float(ell),'seconds':time.time()-tt}
  rec.append(vals);print(vals,flush=True)
  if rho>best:
   best=rho
   np.savez(root/f'absolute_cubic_search_m{m}_s{start}_best.npz',coeff=coeff.numpy(),ell=ell.numpy(),m=m,modes=modes,rho=rho)
  out.write_text(json.dumps({'m':m,'N':N,'steps':steps,'records':rec,'status':'EXPLORATORY_NOT_CERTIFICATION'},indent=2))
