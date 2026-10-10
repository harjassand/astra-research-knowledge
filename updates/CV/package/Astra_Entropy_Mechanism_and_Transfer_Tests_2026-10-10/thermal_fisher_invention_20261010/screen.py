"""Exploratory thermal-mixture test of a thermal-sharp quantum Stam candidate.
No theorem or rigorous floating-point certificate is claimed by this screen.
"""
import json, math, time
from pathlib import Path
import numpy as np

def fisher(weights, means):
    weights=np.array(weights,dtype=float); means=np.array(means,dtype=float)
    r=means/(1+means)
    cut=max(30,int(math.ceil(45/(-math.log(float(max(r)))))))
    ns=np.arange(cut+1)
    p=np.sum((weights/(1+means))[:,None]*np.exp(np.log(r)[:,None]*ns),axis=0)
    mask=(p[:-1]>0)&(p[1:]>0)
    terms=(ns[:-1]+1)*(p[:-1]-p[1:])*np.log(np.divide(p[:-1],p[1:],out=np.ones(cut),where=p[1:]>0))
    j=float(np.sum(terms[mask]))
    tail=float(max(np.log1p(1/means))*np.sum(weights/(1+means)*r**cut*(cut+1+means)))
    return j,tail,cut

def K(j):return .5+1/math.expm1(j)

def run(count=2000):
    rng=np.random.default_rng(20261010);best=None; violations=[]
    for i in range(count):
        na=10**rng.uniform(-3,1.5,size=int(rng.integers(1,5)))
        nb=10**rng.uniform(-3,1.5,size=int(rng.integers(1,5)))
        wa=rng.dirichlet(np.ones(len(na)));wb=rng.dirichlet(np.ones(len(nb)))
        gain=float(1+10**rng.uniform(-2,.8))
        nc=(gain*na[:,None]+(gain-1)*nb[None,:]+gain-1).ravel()
        wc=(wa[:,None]*wb[None,:]).ravel()
        ja,ta,_=fisher(wa,na);jb,tb,_=fisher(wb,nb);jc,tc,cut=fisher(wc,nc)
        gap=K(jc)-gain*K(ja)-(gain-1)*K(jb)
        e={'index':i,'wa':wa.tolist(),'na':na.tolist(),'wb':wb.tolist(),'nb':nb.tolist(),'gain':gain,'J':[ja,jb,jc],'tail_upper':[ta,tb,tc],'gap':gap,'cut':cut}
        if best is None or gap<best['gap']:best=e
        if gap < -1e-8:
            violations.append(e)
            if len(violations)>=5:break
    return {'cases':i+1,'best':best,'violations':violations,'status':'exploratory_float_screen_only'}

if __name__=='__main__':
    start=time.time();result=run();result['seconds']=time.time()-start
    Path(__file__).with_name('screen_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
