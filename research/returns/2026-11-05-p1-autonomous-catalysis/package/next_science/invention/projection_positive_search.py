"""Synthetic one-affinity search: finite bath vs thermal projection."""
import json,math
from pathlib import Path
import numpy as np

def calc(n,edges,gamma=1.):
    N=2*n;Q=np.zeros((N,N));r=np.zeros(N)
    for x,y,kp,km,d in edges:
        Q[x,y]+=kp;Q[y,x]+=km;Q[x,x]-=kp;Q[y,y]-=km
        r[x]+=kp*d;r[y]-=km*d
    for i in range(n):
        x,y=2*i,2*i+1
        Q[x,y]+=gamma;Q[y,x]+=gamma;Q[x,x]-=gamma;Q[y,y]-=gamma
    M=Q.T.copy();M[-1,:]=1;z=np.zeros(N);z[-1]=1
    pi=np.linalg.solve(M,z)
    Qbar=Q.reshape(n,2,n,2).sum(3).mean(1);rb=r.reshape(n,2).mean(1)
    M=Qbar.T.copy();M[-1,:]=1;z=np.zeros(n);z[-1]=1
    mu=np.linalg.solve(M,z);J=pi@r;Jth=mu@rb
    M=Qbar.copy();M[-1,:]=1;z=np.full(n,Jth)-rb;z[-1]=0
    h=np.linalg.solve(M,z);Kg=Q.reshape(n,2,n,2).sum(3)
    w=r.reshape(n,2)[:,1]-r.reshape(n,2)[:,0]+(Kg[:,1]-Kg[:,0])@h
    actualmu=pi.reshape(n,2).sum(1);V=np.dot(actualmu,w*w/(8*gamma))
    sigma=0.
    for x,y,kp,km,d in edges:
        f,b=pi[x]*kp,pi[y]*km;sigma+=(f-b)*math.log(f/b)
    gate=0.
    for i in range(n):
        f,b=gamma*pi[2*i],gamma*pi[2*i+1];gate+=(f-b)*math.log(f/b)
    sigma+=gate
    if Jth<=1e-12: raise ValueError('No positive reference current')
    Vmax=max(w*w/(8*gamma))
    return {'J':J,'Jth':Jth,'gain':J/Jth,'pi':pi.tolist(),'w':w.tolist(),
            'Vmu':V,'sigma':sigma,'sigma_gate':gate,
            'Vmax':Vmax,'kappa_max':math.log(100)*Vmax/Jth,
            'bound_ratio':(J-Jth)**2/(sigma*V) if sigma*V else 0.}

def main():
    rng=np.random.default_rng(887726);best=None;best_ratio=None;best_small=None;n=3;R=100.
    pairs=[(x,y) for x in range(2*n) for y in range(x+1,2*n) if x//2!=y//2]
    for t in range(30000):
        edges=[]
        for x,y in pairs:
            if rng.random()<.25:continue
            kp=10.**int(rng.integers(-3,4));d=int(rng.integers(-1,2));km=kp/R**d
            edges.append([x,y,kp,km,d])
        try:r=calc(n,edges)
        except (np.linalg.LinAlgError,ValueError,ZeroDivisionError):continue
        if r['Jth']<=1e-10 or min(r['pi'])<=0:continue
        if best is None or r['gain']>best['result']['gain']:
            best={'synthetic':True,'states':n,'R':R,'gamma':1.,'edges':edges,'result':r,'iteration':t}
        c={'synthetic':True,'states':n,'R':R,'gamma':1.,'edges':edges,'result':r,'iteration':t}
        if r['gain']>1.001 and (best_ratio is None or r['bound_ratio']>best_ratio['result']['bound_ratio']):best_ratio=c
        if r['gain']>1.01 and (best_small is None or r['kappa_max']<best_small['result']['kappa_max']):best_small=c
    result={'largest_gain':best,'largest_positive_bound_ratio':best_ratio,'smallest_kappa_positive_gain':best_small}
    Path(__file__).with_name('projection_positive_search_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
