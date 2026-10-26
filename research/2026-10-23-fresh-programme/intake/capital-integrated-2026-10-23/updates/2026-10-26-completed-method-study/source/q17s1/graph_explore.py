"""Exploratory looped-network stress; does NOT prove a graph-wide theorem."""
from pathlib import Path
import json
import time
import numpy as np
from scipy.optimize import minimize
from explore import moments, optimum

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(17027)


def optimize_graph(n, ratio, starts=10):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    def unpack(z):
        w = np.exp(z[:n-1] - np.max(z[:n-1]))
        c = np.r_[1., (ratio-1)*w/w.sum()]
        gs = np.exp(z[n-1:])
        edges = [(i,j,float(g)) for (i,j),g in zip(pairs,gs[:-1])]
        sink = [(n-1,float(gs[-1]))]
        return c,edges,sink
    def fun(z):
        c,edges,sink=unpack(z)
        try:
            m,v,cv2=moments(c,edges,sink)
        except np.linalg.LinAlgError:
            return 1e6
        if cv2<=0 or not np.isfinite(cv2):
            return 1e6
        return cv2
    runs=[]
    best=None
    for i in range(starts):
        # Include an analytic ladder embedded in the complete graph.
        if i==0:
            c,r,b=optimum(n,ratio)
            logs_c=np.log(c[1:])
            gs=[1/r[j] if k==j+1 else 1e-5 for j,k in pairs]
            z=np.r_[logs_c,np.log(gs),np.log(1/r[-1])]
        else:
            z=rng.normal(0,2, n-1+len(pairs)+1)
        res=minimize(fun,z,method='SLSQP',bounds=[(-9,9)]*len(z),
                     options={'ftol':1e-11,'maxiter':1000})
        runs.append(dict(start=i,cv2=float(res.fun),success=bool(res.success),
                         iterations=int(res.nit),message=res.message))
        if best is None or res.fun<best.fun:
            best=res
    c,e,s=unpack(best.x)
    return dict(n=n,ratio=ratio,tree_bound=optimum(n,ratio)[2],
                best_cv2=float(best.fun),capacities=c.tolist(),edges=e,sink=s,runs=runs)


if __name__=='__main__':
    t=time.perf_counter()
    rows=[optimize_graph(n,r) for n,r in [(3,10.),(4,100.),(5,100.),(8,100.)]]
    (OUT/'looped_network_exploration.json').write_text(json.dumps(
        dict(seed=17027,results=rows,wall_seconds=time.perf_counter()-t,
             scope='Exploration only; no graph-wide lower bound established'),indent=2)+'\n')
    print(json.dumps([dict(n=x['n'],R=x['ratio'],best=x['best_cv2'],tree_bound=x['tree_bound']) for x in rows],indent=2))
