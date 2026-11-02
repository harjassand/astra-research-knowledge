"""Independent numerical and counterexample checks for the conditional theorem."""
from __future__ import annotations
import json, math, time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from experiments import create_sis, create_sir, discover, counts_initial, hetero, uniform_recovery_policy, distributed_hetero
from machinery import (Model, make_model, full_generator, build_coarse, state_to_counts,
    uniform_initial_micro, expm_distribution, deviations,quadratic_certificate)

rng=np.random.default_rng(20261102)
results={'equivariance_identities':[], 'random_holdout_certificates':[], 'counterexamples':[]}


def validate_exact_quotient(m,groups):
    fq,fs,fi=full_generator(m)
    rq,rs,ri,_=build_coarse(m,groups)
    B=np.zeros((len(fs),len(rs)))
    H=np.zeros((len(rs),len(fs)))
    for i,x in enumerate(fs):
        j=ri[state_to_counts(x,groups,m.q)]
        B[i,j]=1
        H[j,i]=1
    H/=H.sum(axis=1)[:,None]
    A=(H@fq.toarray()@B-rq.toarray())
    exact_sym=all(len(g)==1 for g in groups) or np.max(np.abs((fq@B).toarray() if False else (fq@B-B@rq.toarray())))<1e-10
    return float(np.max(np.abs(A))),float(np.max(np.abs(H@B-np.eye(len(rs))))),bool(exact_sym)

for ix,(q,grp) in enumerate([(2,[3,2]),(3,[2,2]),(2,[2,2,2])]):
    k=len(grp)
    ua=np.zeros((k,q,q));pa=np.zeros((k,k,q,q,q))
    for h in range(k):
        for s in range(q):
            for t in range(q):
                if s!=t:ua[h,s,t]=float(rng.uniform(.025,.20))
        for z in range(k):
            for r in range(q):
                for s in range(q):
                    for t in range(q):
                        if s!=t:pa[h,z,r,s,t]=float(rng.uniform(0.001,.009))
    m,_=make_model(grp,q,ua,pa)
    gg,_=discover(m)
    err,hb,exact=validate_exact_quotient(m,gg)
    assert err<1e-12 and hb<1e-12 and exact
    results['equivariance_identities'].append({'q':q,'n':m.n,'coarse':math.prod(math.comb(len(g)+q-1,q-1) for g in gg),
                 'HQB_minus_R_max':err,'HB_minus_I_max':hb,'strong_exact':exact})

# Generate held-out near-lumpable models with random rate asymmetries, both
# a binary event and a nontrivial smooth count-invariant reward.
for trial in range(36):
    q=2 if trial%2==0 else 3
    sizes=[2,2] if q==3 else [3,2]
    k=len(sizes); ua=np.zeros((k,q,q));pa=np.zeros((k,k,q,q,q))
    for h in range(k):
        for s in range(q):
            for t in range(q):
                if s!=t:ua[h,s,t]=float(rng.uniform(.05,.35))
        for z in range(k):
            for r in range(q):
                for s in range(q):
                    for t in range(q):
                        if s!=t:pa[h,z,r,s,t]=float(rng.uniform(.0,.015))
    base,_=make_model(sizes,q,ua,pa)
    groups,_=discover(base)
    m=Model(base.unary.copy(),base.pair.copy())
    delta=float(rng.choice([-1,1])*rng.uniform(1e-5,0.006))
    a,b=groups[0][0],groups[0][1]
    m.unary[a,1,0]+=delta;m.unary[b,1,0]-=delta
    m.validate()
    counts=state_to_counts(tuple([1]+[0]*(m.n-1)),groups,q)
    fq,fs,fi=full_generator(m);rq,rs,ri,_=build_coarse(m,groups)
    p0=uniform_initial_micro(counts,groups,q,fi)
    c0=np.zeros(len(rs));c0[ri[counts]]=1.
    T=float(rng.uniform(.4,3))
    pf=expm_distribution(fq,p0,T)
    pr=expm_distribution(rq,c0,T)
    pay_full=np.array([float(1 not in v) for v in fs]) if trial%3==0 else np.array([v.count(1)/m.n for v in fs])
    pay_coarse=np.array([float(all(y[1]==0 for y in c)) for c in rs]) if trial%3==0 else np.array([sum(y[1] for y in c)/m.n for c in rs])
    diff=abs(float(pf@pay_full-pr@pay_coarse))
    eta=deviations(m,groups)['eta_upper'];bound=quadratic_certificate(eta,T)
    assert diff<bound+2e-12,(trial,diff,bound)
    results['random_holdout_certificates'].append({'trial':trial,'q':q,'n':m.n,'eta':eta,'T':T,
                'diff':diff,'bound':bound,'bound_passed':True})

# Explicit essential-assumption counterexample in a minimal 2-site process:
# two independently recovering infections, rate alpha+/-epsilon.
from scipy.sparse.linalg import expm_multiply
model,hidden=create_sis([2],rates=([.30],[[0.0]]))
groups,_=discover(model)
eps=.001
m=Model(model.unary.copy(),model.pair.copy())
m.unary[0,1,0]+=.001;m.unary[1,1,0]-=.001
eta=deviations(m,groups)['eta_upper']
T=1
Q,fs,fi=full_generator(m)
R,rs,ri,_=build_coarse(m,groups)
# Non-orbit-uniform initial site 0 infected. Count-invariant extinction payoff.
p=np.zeros(len(fs));p[fi[(1,0)]]=1
p_exact=float(expm_distribution(Q,p,T)@np.array([float(x==(0,0)) for x in fs]))
c=state_to_counts((1,0),groups,2)
v=np.zeros(len(rs));v[ri[c]]=1
p_coarse=float(expm_distribution(R,v,T)@np.array([float(z[0][1]==0) for z in rs]))
err=abs(p_exact-p_coarse)
assert err>quadratic_certificate(eta,T)*10
results['counterexamples'].append({'failure':'initial_not_exchangeable',
    'task':'whole-population extinction, fixed named initial carrier',
    'exact':p_exact,'projected':p_coarse,'observed_error':err,
    'invalid_quadratic_limit':quadratic_certificate(eta,T),
    'reason':'first-order term does not cancel'})
# Exchangeable initial condition (both infected) but named-site payoff.
p=np.zeros(len(fs));p[fi[(1,1)]]=1
post=expm_distribution(Q,p,T)
p_named=float(post@np.array([float(x[0]==1) for x in fs]))
c=state_to_counts((1,1),groups,2);v=np.zeros(len(rs));v[ri[c]]=1
out=expm_distribution(R,v,T)
p_mean=float(out@np.array([z[0][1]/2 for z in rs]))
err=abs(p_named-p_mean)
assert err>10*quadratic_certificate(eta,T)
results['counterexamples'].append({'failure':'observable_not_count_invariant',
    'task':'specific site remains infected, both sites initially infected',
    'exact':p_named,'projected':p_mean,'observed_error':err,
    'invalid_quadratic_limit':quadratic_certificate(eta,T),
    'reason':'first-order term does not cancel'})

results['random_test_count']=len(results['random_holdout_certificates'])
results['max_error_over_bound']=max(v['diff']/v['bound'] for v in results['random_holdout_certificates'])
Path(__file__).with_name('validation_results.json').write_text(json.dumps(results,indent=2))
print('IDENTITIES',len(results['equivariance_identities']))
print('RANDOM',len(results['random_holdout_certificates']),'MAXERR/BND',results['max_error_over_bound'])
print('COUNTEREXAMPLES',results['counterexamples'])
