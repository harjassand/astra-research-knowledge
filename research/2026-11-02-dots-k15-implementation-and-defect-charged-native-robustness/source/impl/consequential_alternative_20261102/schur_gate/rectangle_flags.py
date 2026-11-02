import sys,os,math,json
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from analog_quantization import bins,grad,HALF

def rectangle(v,r,bq=2,bp=2):
  ax=[]
  for vv,b in [(v/r,bq),(v*r,bp)]:
    if b>1:
      op=minimize(lambda t:bins(vv,t)[0],np.linspace(0,HALF,b+1)[1:-1],jac=lambda t:grad(vv,t),bounds=[(1e-8,HALF-1e-8)]*(b-1),constraints={'type':'ineq','fun':lambda t:np.diff(t)-1e-8},method='SLSQP',options={'ftol':2e-14,'maxiter':1000});t=op.x
    else:t=[]
    H,w,e,p=bins(vv,t);ax.append((H,w,p,t))
  weights=[];ps=[]
  for i in range(bq):
    for j in range(bp):
      H,w,p,t=ax[0];G,z,q,u=ax[1]
      weights.append(w[i]*z[j]);ps.append([(1-p[i])*(1-q[j]),p[i]*(1-q[j]),p[i]*q[j],(1-p[i])*q[j]])
  return dict(v=v,aspect_r=r,bins_per_quadrature=[bq,bp],weights=weights,paulis=ps,one_use_ic=1-ax[0][0]-ax[1][0],thresholds=[list(a[3]) for a in ax])
if __name__=='__main__':
 v=float(sys.argv[1]);r=float(sys.argv[2]);bq=int(sys.argv[3]);bp=int(sys.argv[4]);print(json.dumps(rectangle(v,r,bq,bp),indent=2))
