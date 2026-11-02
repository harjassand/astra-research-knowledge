import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import sys,json,time,math,argparse
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from analog_quantization import bins,grad,HALF
from schur_channel import SchurChannel

def cartesian_flags(v,b):
    if b==1:t=[]
    else:
      opt=minimize(lambda t:bins(v,t)[0],np.linspace(0,HALF,b+1)[1:-1],jac=lambda t:grad(v,t),method='SLSQP',bounds=[(1e-8,HALF-1e-8)]*(b-1),constraints={'type':'ineq','fun':lambda t:np.diff(t)-1e-8},options={'ftol':1e-13,'maxiter':500})
      t=opt.x
    H,w,e,p=bins(v,t)
    ws=[];ps=[]
    for i in range(b):
      for j in range(b):
        ws.append(w[i]*w[j]);ps.append([(1-p[i])*(1-p[j]),p[i]*(1-p[j]),p[i]*p[j],(1-p[i])*p[j]])
    return np.array(ws),np.array(ps),dict(v=v,thresholds=list(t),one_use_ic=1-2*H)

def constraints(x):
  A=x.reshape(2,-1)
  return np.array([A[0]@A[0]-.5,A[1]@A[1]-.5,A[0]@A[1]])
def cjac(x):
  A=x.reshape(2,-1);J=np.zeros((3,2,A.shape[1]));J[0,0]=2*A[0];J[1,1]=2*A[1];J[2,0]=A[1];J[2,1]=A[0]
  return J.reshape(3,-1)

def main():
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=6);p.add_argument('--bins',type=int,default=2);p.add_argument('--starts',type=int,default=8);p.add_argument('--v',type=float,default=1/math.e+1e-5);p.add_argument('--maxiter',type=int,default=100);p.add_argument('--flags');p.add_argument('--out',required=True);args=p.parse_args()
 n=args.n;d=n+1;rng=np.random.default_rng(20261102+n)
 if args.flags:
  spec=json.load(open(args.flags));w=np.array(spec['weights']);ps=np.array(spec['paulis']);info=spec
 else:w,ps,info=cartesian_flags(args.v,args.bins)
 engine=SchurChannel(n,w,ps,True)
 record=dict(args=vars(args),channel=info,weights=w.tolist(),paulis=ps.tolist(),blocks=len(engine.meta),memory_bytes=engine.bytes,results=[])
 A=np.zeros((2,d));A[0,0]=A[1,-1]=1/math.sqrt(2)
 starts=[A]
 for k in range(1,min(n,3)):
  A=np.zeros((2,d));A[0,k]=A[1,n-k]=1/math.sqrt(2)
  if k!=n-k:starts.append(A)
 while len(starts)<args.starts:
  q=np.linalg.qr(rng.normal(size=(d,2)))[0];starts.append(q.T/math.sqrt(2))
 for idx,A in enumerate(starts[:args.starts]):
  start=time.time();calls=[0];best=[-1e10,None]
  def fg(x):
   v,g=engine.coherent(x.reshape(2,d),True);calls[0]+=1
   if v>best[0] and np.linalg.norm(constraints(x))<1e-5:best[:]=[v,x.copy()]
   return -v,-g.ravel()
  initial=engine.coherent(A)
  opt=minimize(fg,A.ravel(),jac=True,method='SLSQP',constraints={'type':'eq','fun':constraints,'jac':cjac},options={'ftol':1e-11,'maxiter':args.maxiter,'disp':False})
  v,g=engine.coherent(opt.x.reshape(2,d),True)
  item=dict(start=idx,initial=initial,final=v,A=opt.x.reshape(2,d).tolist(),calls=calls[0],seconds=time.time()-start,success=bool(opt.success),message=opt.message,constraint_error=float(np.linalg.norm(constraints(opt.x))),best_feasible=best[0])
  record['results'].append(item);json.dump(record,open(args.out,'w'),indent=2)
  print(json.dumps({k:item[k] for k in item if k!='A'}),flush=True)
if __name__=='__main__':main()
