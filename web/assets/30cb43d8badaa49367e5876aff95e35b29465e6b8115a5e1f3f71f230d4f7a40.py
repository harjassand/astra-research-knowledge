"""Boundary family sweep and projected stochastic local attacks."""
from attack import *

def to_p(X):
    S=np.array([[1,0,0,0],[.5,.5,0,0],[1/3,1/3,1/3,0],[.25,.25,.25,.25]])
    return X @ S

def objective(X,which):
    vs=margins(to_p(X[:,:4]),to_p(X[:,4:]))
    if which=='cubic':return vs[2]
    return np.divide(vs[1],vs[3]*vs[4],out=np.full_like(vs[1],np.inf),where=vs[3]*vs[4]>1e-12)

def optimize(which):
    X=np.concatenate([RNG.dirichlet([.1]*4,size=128),RNG.dirichlet([.1]*4,size=128)],axis=1)
    # A known close boundary family to seed the cubic search.
    X[0]=[.5,0,.5,0,.5,0,.5,0]
    scores=objective(X,which)
    history=[]
    for scale in [.2,.1,.03,.01,.003,.001,.0003,.0001,.00003]:
      for _ in range(30):
       trial=np.repeat(X,16,axis=0)
       noise=RNG.standard_normal(trial.shape)*scale
       noise[::4,RNG.integers(0,8,size=len(noise[::4]))]=0
       trial=np.maximum(0,trial+noise)
       trial[:,:4][trial[:,:4].sum(axis=1)==0]=.25
       trial[:,4:][trial[:,4:].sum(axis=1)==0]=.25
       trial[:,:4]/=trial[:,:4].sum(axis=1)[:,None];trial[:,4:]/=trial[:,4:].sum(axis=1)[:,None]
       values=objective(trial,which).reshape(len(X),16)
       ids=values.argmin(axis=1);vv=values[np.arange(len(X)),ids]
       keep=vv<scores;X[keep]=trial.reshape(len(X),16,8)[np.arange(len(X)),ids][keep];scores[keep]=vv[keep]
      history.append(float(scores.min()))
    idx=int(scores.argmin());return {'value':float(scores[idx]),'p':to_p(X[idx:idx+1,:4])[0].tolist(),'q':to_p(X[idx:idx+1,4:])[0].tolist(),'history':history}

def main():
    a=np.linspace(1/3,1,20001);p=np.column_stack([a,(1-a)/2,(1-a)/2,np.zeros_like(a)])
    ratio=margins(p,p)[2];i=int(ratio.argmin())
    result={'diagonal_boundary_sweep':{'value':float(ratio[i]),'a':float(a[i]),'p':p[i].tolist()},'local_cubic':optimize('cubic'),'local_H_normalized':optimize('H')}
    (OUT/'optimized_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
