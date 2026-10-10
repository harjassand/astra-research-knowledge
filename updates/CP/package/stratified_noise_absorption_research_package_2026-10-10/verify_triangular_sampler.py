"""Independent exact finite-state Markov tests for triangular joint stationary sampler."""
import random,math,sys
from collections import Counter
import numpy as np
from scipy.special import chdtrc
from triangular_entropy_sampler import *
from verify_heisenberg import stationary_2site, check_expr_equivalence
from heisenberg_quotient_sampler import Model, group_word_eval


def check_group_expr(q=3,d=4,trials=300):
    rng=random.Random(20261010)
    cs=channels(d)
    assert len(cs)==d*(d-1)//2
    for j in range(trials):
        vals={i:tuple(rng.randrange(q) for _ in cs) for i in range(4)}
        factors=[]
        for _ in range(rng.randint(1,15)):
            if rng.random()<.25:factors.append(('c',tuple(rng.randrange(q) for _ in cs)))
            else:factors.append(('v',rng.randrange(4),rng.choice([-3,-2,-1,1,2,3])))
        E=expr_identity(d)
        for F in factors:
            T=expr_constant(F[1],d,q) if F[0]=='c' else expr_power(expr_variable((F[1],0),d),F[2],d,q)
            E=expr_product(E,T,d,q)
        assignment={(i,0,a,b):v for i,g in vals.items() for (a,b),v in zip(cs,g)}
        actual=tuple(poly_eval(E[ch],assignment,q) for ch in cs)
        expected=ut_word_eval(vals,factors,d,q)
        assert expected==actual,(j,d,q,factors,expected,actual)
        for ch in cs:
            le=layer(ch)
            for mon in E[ch]:
                assert sum(v[3]-v[2] for v in mon)<=le,('nontriangular',mon,ch)
        # Check inverse independent of algebraic expression.
        assert ut_mul(vals[0],ut_inv(vals[0],d,q),d,q)==group_id(d)
    return True


def run_exact_UT3_check(runs=4000):
    d=q=3
    gates={0:[('v',0,1),('v',1,1),('v',0,-1),('v',1,-1)],
           1:[('v',1,1),('v',0,1),('v',1,1)]}
    u=UTModel(n=2,d=d,q=q,s=.16,r=.12,gates=gates,residual=(1,0,1))
    h=Model(n=2,q=q,s=.16,r=.12,gates=gates,residual=(1,0,1))
    states,idmap,pi,diff,niter=stationary_2site(h)
    observables=[ [('v',0,1)], [('v',1,1)],
                  [('v',0,1),('v',1,1)],
                  [('v',0,1),('v',1,1),('v',0,-1),('v',1,-1)]]
    for idx,obs in enumerate(observables):
        exp=np.zeros(len(states))
        for j in range(len(states)):
            for k in range(len(states)):
                x=group_word_eval((states[j],states[k]),obs,q)
                exp[idmap[x]]+=pi[j*len(states)+k]
        observed=np.zeros(len(states))
        rng=random.Random(21260+idx)
        q_count=[]
        for _ in range(runs):
            actual,st=sample_word(u,obs,rng,True)
            observed[idmap[actual]]+=1
            q_count.append(st['fresh'])
        mask=exp>1e-11
        chi=float(np.sum((observed[mask]-runs*exp[mask])**2/(runs*exp[mask])))
        dof=mask.sum()-1
        pval=float(chdtrc(dof,chi))
        tv=float(.5*np.abs(observed/runs-exp).sum())
        print(f'UT3 observable {obs}: mean symbols {np.mean(q_count):.3f}, chi2 {chi:.2f}/{dof}, pval {pval:.3f}, TV {tv:.4f}')
        assert .0000001<pval<.9999999

def one_site_reference(model,site=0):
    d,q=model.d,model.q
    cs=channels(d)
    N=q**len(cs)
    states=[tuple((i//(q**j))%q for j in range(len(cs))) for i in range(N)]
    lookup={g:i for i,g in enumerate(states)}
    mapping=[lookup[ut_word_eval([g],model.factors(site),d,q)] for g in states]
    pi=np.ones(N,dtype=float)/N
    residx=lookup[model.reset_value(site)]
    for iteration in range(10000):
        old=pi
        new=np.ones(N)*model.s/N
        new[residx]+=model.r
        for st,p in enumerate(old):new[mapping[st]]+=(1-model.s-model.r)*p
        diff=np.abs(new-old).sum()
        pi=new
        if diff<1e-13:break
    assert abs(pi.sum()-1)<1e-8
    return pi,lookup,iteration,diff

def run_UT4_reference(runs=8000):
    d,q=4,3
    cs=channels(d)
    g=(1,0,1,0,2,1)  # 6 nilpotent coordinates (3 degree1, 2 degree2, 1 degree3)
    gates={0:[('v',0,1),('c',g),('v',0,-1),('v',0,1),('v',0,1)]}
    model=UTModel(n=1,d=d,q=q,s=.17,r=.14,gates=gates,residual=g)
    exact,lookup,it,diff=one_site_reference(model)
    rng=random.Random(975210)
    obs=np.zeros_like(exact)
    ct=[]
    for _ in range(runs):
        sample,stats=sample_group_states(model,[(0,0)],rng,True)
        obs[lookup[sample[(0,0)]]]+=1
        ct.append(stats['fresh'])
    # 729 states with many very small probabilities, compare aggregated coordinate marginals / moments
    x=np.array(list(lookup))
    for chan_id,ch in enumerate(cs):
        target=np.bincount(x[:,chan_id],weights=exact,minlength=q)
        got=np.bincount(x[:,chan_id],weights=obs,minlength=q)
        chi=float(np.sum((got-runs*target)**2/(runs*target)))
        pval=float(chdtrc(q-1,chi))
        print(f'UT4 {ch} marginal: ref {target.round(4)}, empirical {(got/runs).round(4)}, chi2 {chi:.2f}/2 pval={pval:.3f}')
        assert .0000001<pval<.9999999
    tv=.5*np.abs(obs/runs-exact).sum()
    print(f'UT4 n=1 729-state exact reference iterations={it} gap={diff:.1e}; samples={runs}; observed-full-state-TV={tv:.3f}, mean update symbols {np.mean(ct):.2f}')

if __name__=='__main__':
    print('Nonabelian polynomial identities',check_group_expr(3,3),check_group_expr(3,4),check_group_expr(5,4))
    run_exact_UT3_check(3000)
    run_UT4_reference(6000)
