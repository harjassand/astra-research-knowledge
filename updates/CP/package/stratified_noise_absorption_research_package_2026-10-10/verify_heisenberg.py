"""Independent transition-matrix / property-based checks for Heisenberg quotient sampler."""
import sys,math,random,time
from collections import Counter
import numpy as np
from scipy.special import chdtrc
from heisenberg_quotient_sampler import *

def stationary_2site(model):
    q=model.q
    states=[(a,b,c) for a in range(q) for b in range(q) for c in range(q)]
    NG=len(states)
    idmap={g:i for i,g in enumerate(states)}
    S=NG**2
    T=np.zeros((S,S),dtype=np.float64)
    for idx in range(S):
        i,j=divmod(idx,NG)
        d=[]
        for site in range(2):
            r=np.full(NG,model.s/NG,dtype=np.float64)
            r[idmap[model.reset_value(site)]]+=model.r
            result=group_word_eval((states[i],states[j]),model.factors(site),q)
            r[idmap[result]]+=1-model.s-model.r
            d.append(r)
        T[idx,:]=np.kron(*d)
    assert np.max(np.abs(T.sum(axis=1)-1))<1e-13
    pi=np.ones(S,dtype=float)/S
    diff=1
    for count in range(1000):
        new=pi@T
        diff=np.max(np.abs(new-pi))
        pi=new
        if diff<3e-15: break
    assert abs(pi.sum()-1)<1e-9
    return states,idmap,pi,diff,count+1

def check_expr_equivalence(q=3):
    rng=random.Random(1223)
    # randomly compare formal word substitutions with direct H_p multiplication
    for rep in range(250):
        word=[]
        for _ in range(rng.randint(1,11)):
            if rng.random()<.2: word.append(('c',(rng.randrange(q),rng.randrange(q),rng.randrange(q))))
            else:word.append(('v',rng.randrange(5),rng.choice([-3,-2,-1,1,2,3])))
        e=expr_const((0,0,0),q)
        for F in word:
            t=expr_const(F[1],q) if F[0]=='c' else expr_power(expr_var((F[1],0)),F[2],q)
            e=expr_mul(e,t,q)
        vars_={i:(rng.randrange(q),rng.randrange(q),rng.randrange(q)) for i in range(5)}
        coord={(i,0,c):v[j] for i,v in vars_.items() for j,c in enumerate('abc')}
        expected=group_word_eval(vars_,word,q)
        actual=expr_eval(e,coord,q)
        assert expected==actual,(rep,word,expected,actual)
        # Test polynomial replacement involving a nontrivial word.
        z=(rng.randrange(5),0)
        after=[]
        for _ in range(rng.randint(1,6)):
            if rng.random()<.2:after.append(('c',(rng.randrange(q),rng.randrange(q),rng.randrange(q))))
            else:after.append(('v',rng.randrange(5,8),rng.choice([-2,-1,1,2])))
        R=expr_const((0,0,0),q)
        for F in after:
            t=expr_const(F[1],q) if F[0]=='c' else expr_power(expr_var((F[1],-1)),F[2],q)
            R=expr_mul(R,t,q)
        substituted=expr_replace(e,z,R,q)
        newvars={i:(rng.randrange(q),rng.randrange(q),rng.randrange(q)) for i in range(5,8)}
        val=group_word_eval(newvars,after,q)
        neworiginal=vars_.copy();neworiginal[z[0]]=val
        target=group_word_eval(neworiginal,word,q)
        assignment={(i,0,c):v[j] for i,v in vars_.items() for j,c in enumerate('abc')}
        assignment.update({(i,-1,c):v[j] for i,v in newvars.items() for j,c in enumerate('abc')})
        actual2=expr_eval(substituted,assignment,q)
        assert actual2==target,(rep,word,after,target,actual2)
    return True


def check_stationary(model, obs, runs=7000,seed=19):
    states,idmap,pi,diff,it=stationary_2site(model)
    q=model.q
    expected=np.zeros(len(states))
    for z,(i,j) in enumerate([(i,j) for i in range(len(states)) for j in range(len(states))]):
        expected[idmap[group_word_eval((states[i],states[j]),obs,q)]]+=pi[z]
    rng=random.Random(seed)
    seen=np.zeros(len(states),dtype=float)
    stats=[]
    for _ in range(runs):
        actual,st=sample_word_observable(model,obs,rng,True)
        seen[idmap[actual]]+=1
        stats.append(st)
    active=expected>1e-12
    chi=np.sum((seen[active]-runs*expected[active])**2/(runs*expected[active]))
    dof=active.sum()-1
    pval=float(chdtrc(dof,chi))
    tv=.5*np.abs(seen/runs-expected).sum()
    mean_queries=sum(x['fresh'] for x in stats)/runs
    prop_quotient=sum(x['quotient'] for x in stats)/runs
    print(f'word {obs}  n={runs}  exact stationary reached after {it} iterations gap={diff:.2e}  chi2={chi:.2f}/{dof}  pval={pval:.3f}  TV={tv:.4f}  mean_symbols={mean_queries:.3f}  quotient_use={prop_quotient:.3f}')
    return chi,dof,pval,tv,mean_queries

if __name__=='__main__':
    print('Group polynomial property tests:',check_expr_equivalence(3),check_expr_equivalence(5))
    G={0:[('v',0,1),('v',1,1),('v',0,-1),('v',1,-1)],
       1:[('v',1,1),('v',0,1),('v',1,1)]}
    m=Model(n=2,q=3,s=.16,r=.12,gates=G,residual=(1,0,1))
    for obs in [[('v',0,1)],[('v',1,1)],
                [('v',0,1),('v',1,1),('v',0,-1),('v',1,-1)],
                [('v',0,1),('v',1,1)]]:
        check_stationary(m,obs, runs=4000,seed=1729+len(obs))

# Demonstrate polynomial word-map permutation independently of stationarity.
def check_bijective_word_maps(q=3, trials=250):
    rng=random.Random(20261010)
    els=[(a,b,c) for a in range(q) for b in range(q) for c in range(q)]
    for j in range(trials):
        n=rng.randint(2,18)
        factors=[]
        for _ in range(n):
            if rng.random()<.2:factors.append(('c',rng.choice(els)))
            else:factors.append(('v',rng.randrange(3),rng.choice([-1,1])))
        exponent=sum(F[2] for F in factors if F[0]=='v' and F[1]==0)%q
        if not exponent:continue
        other=[None,rng.choice(els),rng.choice(els)]
        image=set()
        for U in els:
            other[0]=U
            image.add(group_word_eval(other,factors,q))
        assert len(image)==len(els),(factors,len(image))
    return True
