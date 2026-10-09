"""Independent focused check: labelled physical molecules, no marked/count FSP code."""
import hashlib, importlib.util, itertools, json, math, pathlib, sys, time
import numpy as np
from scipy.linalg import expm
from scipy.stats import poisson
ROOT = pathlib.Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def labelled_reference(N,Q,C,lam,koff,kcat,mu,T,bind=0,product=1):
    q = len(mu)
    # q denotes a bound substrate. Each original molecule retains its label.
    states = [x for x in itertools.product(range(q+1), repeat=N) if x.count(q)<=C]
    ix = {x:i for i,x in enumerate(states)}
    G = np.zeros((len(states),len(states)))
    f0 = np.zeros(len(states))
    for k,x in enumerate(states):
        b=x.count(q)
        if b==0: f0[k]=math.prod(mu[v] for v in x)
        for label,a in enumerate(x):
            transitions=[]
            if a==q:
                transitions.extend([(bind,koff),(product,kcat)])
            else:
                transitions.extend((z,Q[a,z]) for z in range(q) if z!=a)
                if a==bind and b<C: transitions.append((q,lam*(C-b)/N))
            for z,rate in transitions:
                if rate<=0: continue
                xx=list(x); xx[label]=z
                G[k,ix[tuple(xx)]]+=rate
                G[k,k]-=rate
    f=f0@expm(T*G)
    return states,f

def query(states,f,q,obs,b):
    answer=0.
    for x,p in zip(states,f):
        if b is not None and x.count(q)!=b: continue
        n=tuple(x.count(a) for a in range(q))
        good=all(n[a]==v for a,v in obs.items()) if isinstance(obs,dict) else n==obs
        if good: answer+=p
    return float(answer)

def main():
    paths={'base':ROOT/'marked_pool.py','partial':ROOT/'product_count_extension/marked_pool_partial.py'}
    mods={k:load('focused_'+k,p) for k,p in paths.items()}
    results=[]
    cases=[(3,2,np.array([[-.7,.5,.2],[.3,-.4,.1],[.4,.2,-.6]]),np.array([.2,.5,.3]),0,1,.9,.4,.6,.7,12,
            [((1,1,1),0),((1,1,0),1),((1,0,0),2),({1:1},None)]),
           (1,3,np.array([[-.5,.5],[.2,-.2]]),np.array([.6,.4]),0,1,.8,.3,.7,.6,14,
            [((1,0),0),((0,0),1),({1:1},None)]),
           (4,2,np.array([[-.7,.7,0],[.3,-.3,0],[0,0,0]]),np.array([1.,0,0]),0,2,.9,.4,.6,.7,12,
            [({2:1},None),({2:1},1),({2:0},2)])]
    for N,C,Q,mu,bind,prod,lam,koff,kcat,T,K,observations in cases:
        states,f=labelled_reference(N,Q,C,lam,koff,kcat,mu,T,bind,prod)
        for obs,b in observations:
            exact=query(states,f,len(mu),obs,b)
            for name,mod in mods.items():
                if isinstance(obs,dict) and name=='base': continue
                start=time.perf_counter()
                ans=mod.MarkedPoolLikelihood(N,Q,bind,prod,lam,koff,kcat,mu,catalysts=C).solve(T,K,obs,b,rtol=2e-12,atol=1e-15)
                tail=float(poisson.sf(K,C*lam*T))
                err=3e-11
                passed=ans.lower-err<=exact<=ans.lower+tail+err
                capped=isinstance(obs,dict) and prod in obs and np.all(Q[:,prod]==0) and np.all(Q[prod,:]==0) and mu[prod]==0
                mass_gap=ans.mass-float(poisson.cdf(K,C*lam*T))
                if not capped: passed=passed and abs(mass_gap)<err
                row={'module':name,'N':N,'C':C,'q':len(mu),'observed':obs,'observed_bound':b,'K':K,
                     'labelled_states':len(states),'marked_states':ans.dimension,'labelled_exact':exact,'marked_lower':ans.lower,
                     'difference_exact_minus_marked':exact-ans.lower,'poisson_tail':tail,'mass_minus_poisson_cdf':mass_gap,
                     'product_cap_applies':bool(capped),'numerical_slack':err,'passed':bool(passed),'seconds':time.perf_counter()-start}
                results.append(row)
    output={'description':'Independent labelled-molecule physical CTMC; not a second implementation of the marked closure. Floating point comparison, not certified numerical enclosure.',
            'source_sha256':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},'cases':results,'all_passed':all(r['passed'] for r in results)}
    out=pathlib.Path(__file__).with_name('labeled_reference_results.json')
    out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
    assert output['all_passed']

if __name__=='__main__': main()
