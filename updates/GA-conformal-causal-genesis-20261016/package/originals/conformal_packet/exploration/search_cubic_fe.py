"""Local search on actual continuous periodic piecewise-affine maps."""
import torch,numpy as np,json,sys,time
from pathlib import Path
root=Path(__file__).parent
torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
N=int(sys.argv[1]) if len(sys.argv)>1 else 12
num=int(sys.argv[2]) if len(sys.argv)>2 else 10
steps=int(sys.argv[3]) if len(sys.argv)>3 else 500
start=int(sys.argv[4]) if len(sys.argv)>4 else 0

def calc(phi,ell):
 ux=torch.roll(phi,-1,1);uy=torch.roll(phi,-1,2);uxy=torch.roll(ux,-1,2)
 V=torch.stack([torch.stack([ux-phi,uxy-ux],dim=1),torch.stack([uxy-uy,uy-phi],dim=1)],dim=2)
 V=V*torch.stack([torch.exp(ell),torch.exp(-ell)]).reshape(1,2,1,1,1)*N
 a,b,c,d=V.reshape(4,-1)
 u=a*a+c*c;j=a*d-b*c
 A=(((a-d)**2+(b+c)**2)**2/8+j*j+u*j).mean()
 Q=((2*a+d)**2+c*c).mean()
 C=(a**3+5*a*a*d-4*a*b*c+a*c*c+2*a*d*d-2*b*c*d+c*c*d).mean()
 return C*C/(4*A*Q+1e-40),A,Q,C,V
rec=[];best=-1
for seed in range(start,start+num):
 torch.manual_seed(seed)
 phi=torch.nn.Parameter(torch.randn(2,N,N))
 ell=torch.nn.Parameter(torch.tensor(float(seed%5-2)/2))
 if seed%4==0:
  with torch.no_grad():phi[1]*=.1
 opt=torch.optim.LBFGS([phi,ell],max_iter=steps,line_search_fn='strong_wolfe',tolerance_grad=1e-10,tolerance_change=1e-14,history_size=50)
 def closure():
  opt.zero_grad();rho,*_=calc(phi,ell);loss=-rho+1e-12*ell**4;loss.backward();return loss
 tt=time.time()
 try:opt.step(closure)
 except Exception as ex:print('ERROR',seed,repr(ex),flush=True);continue
 with torch.no_grad():
  rho,A,Q,C,V=calc(phi,ell);rho=float(rho)
  vals={'seed':seed,'rho':rho,'A':float(A),'Q':float(Q),'C':float(C),'log_aspect':float(ell),'seconds':time.time()-tt}
  rec.append(vals);print(vals,flush=True)
  if rho>best:
   best=rho;np.savez(root/f'cubic_fe_N{N}_s{start}_best.npz',phi=phi.numpy(),ell=ell.numpy(),N=N,rho=rho)
  (root/f'cubic_fe_N{N}_s{start}.json').write_text(json.dumps({'N':N,'steps':steps,'records':rec,'status':'EXPLORATORY_NOT_CERTIFICATION'},indent=2))
