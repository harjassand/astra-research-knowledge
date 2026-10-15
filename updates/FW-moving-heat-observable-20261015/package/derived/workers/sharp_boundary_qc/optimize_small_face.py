"""Discovery only. Any eventual conclusion requires an exact certificate."""
import pickle,numpy as np,sympy as s
from pathlib import Path
from scipy.optimize import minimize
base=Path(__file__).parent
with open(base/'symmetric_face.pkl','rb') as ff:data=pickle.load(ff)
r=data['r'];y=data['y'];S=data['S']
# y4=d1, y5=d2. Normalize d1+d2=2.
Sr=S.subs({y[5]:2-y[4]})
pars=[y[0],y[1],y[3],y[4]]
fn=s.lambdify((r,*pars),Sr,'numpy')
def solve(rv):
    def get(vv):return np.linalg.eigvalsh(np.asarray(fn(rv,*vv[:4]),float))
    def con(vv):return get(vv)-vv[4]
    best=None
    for seed in range(5):
        initial=np.array([0.,0.,0.,1.,-100.])
        if seed:initial[:3]=np.random.default_rng(seed).normal(0,3,3)
        res=minimize(lambda vv:-vv[4],initial,method='SLSQP',
           constraints=[{'type':'ineq','fun':con}],
           bounds=[(None,None)]*3+[(1e-5,2-1e-5),(None,None)],
           options={'ftol':1e-10,'maxiter':2000})
        if best is None or res.x[4]>best.x[4]:best=res
    print(rv,'success',best.success,'x',best.x,'eig',get(best.x),flush=True)
    return {'r':rv,'x':best.x.tolist(),'eig':get(best.x).tolist(),'success':bool(best.success)}
import json
out=[solve(rv) for rv in [-2.5,-2.625,-8/3,-3.,-4.]]
(base/'small_face_discovery.json').write_text(json.dumps(out,indent=2)+'\n')
