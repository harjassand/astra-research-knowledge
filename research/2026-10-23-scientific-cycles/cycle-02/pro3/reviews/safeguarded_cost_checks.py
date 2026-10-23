#!/usr/bin/env python3
"""Exact comparator diagnostics. Four states; all target lookups fully memoized.
No stochastic trajectories, tolerance tests, or empirical observations.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json, time, resource, sys, platform

start=time.perf_counter(); cpu=time.process_time()
q=[F(1,4)]*4
pi=[F(3,8),F(3,8),F(1,8),F(1,8)]
alpha=F(1,2)
Q=[[F(int(j==(i^1))) for j in range(4)] for i in range(4)]
W=[pi[i]/q[i] for i in range(4)]

def mh(proposal,target=pi):
    a=[[F(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            if i==j: continue
            a[i][j]=min(target[i]*proposal[i][j],target[j]*proposal[j][i])/target[i]
        a[i][i]=1-sum(a[i])
    return a
G=mh([q[:] for _ in range(4)])
R=mh(Q,q)
L=mh(R,pi)
C=[[(F(int(i==j))+alpha*G[i][j]+(1-alpha)*L[i][j])/2 for j in range(4)] for i in range(4)]

def apply(v,P): return [sum(v[i]*P[i][j] for i in range(4)) for j in range(4)]
def tv(v): return sum(abs(v[i]-pi[i]) for i in range(4))/2

def joint_step(dist,kind):
    out=defaultdict(F)
    for (x,mask),mass in dist.items():
        if kind=='C':
            branches=[('I',F(1,2)),('G',F(1,4)),('L',F(1,4))]
        else: branches=[(kind,F(1))]
        for branch,bp in branches:
            if branch=='I': out[x,mask]+=mass*bp; continue
            props=q if branch=='G' else Q[x]
            for y,pp in enumerate(props):
                if not pp: continue
                # All candidates from Q pass stage one, because q is uniform.
                # The target oracle is invoked only if y has never been evaluated.
                newmask=mask | (1<<y)
                acc=min(F(1),W[y]/W[x])
                out[y,newmask]+=mass*bp*pp*acc
                out[x,newmask]+=mass*bp*pp*(1-acc)
    return {k:v for k,v in out.items() if v}

def run(kind,n):
    law={(i,1<<i):q[i] for i in range(4)}
    for _ in range(n): law=joint_step(law,kind)
    marginal=[sum(v for (x,_),v in law.items() if x==i) for i in range(4)]
    expect_evals=sum(v*mask.bit_count() for (_,mask),v in law.items())
    # Initial target evaluation and q candidate both count.
    active=F(n,2) if kind=='C' else F(n)
    glob=F(n,4) if kind=='C' else F(n if kind=='G' else 0)
    local=F(n,4) if kind=='C' else F(n if kind=='L' else 0)
    return {'kind':kind,'steps':n,'law':marginal,'tv':tv(marginal),
      'expected_target_evals_full_memo_including_initial':expect_evals,
      'expected_target_evals_full_memo_post_initial':expect_evals-1,
      'expected_proposals_post_initial':active,
      'expected_global_draws_post_initial':glob,
      'expected_local_proposals':local,
      'augmented_states':len(law)}

results=[run('C',4),run('G',1),run('G',2)]
theta=(results[0]['expected_target_evals_full_memo_including_initial']-F(7,4))/(F(37,16)-F(7,4))
matched_target={'probability_two_updates':theta,'probability_one_update':1-theta,
  'tv':(1-theta)*results[1]['tv']+theta*results[2]['tv'],
  'expected_target_evals_full_memo_including_initial':(1-theta)*F(7,4)+theta*F(37,16),
  'expected_global_draws_post_initial':1+theta,'expected_proposals_post_initial':1+theta}
assert matched_target['tv']==F(67769,1990656)
assert matched_target['expected_target_evals_full_memo_including_initial']==results[0]['expected_target_evals_full_memo_including_initial']
assert matched_target['expected_proposals_post_initial']<results[0]['expected_proposals_post_initial']
assert matched_target['tv']<results[0]['tv']
assert results[0]['tv']==F(625,5184)
assert results[1]['tv']==F(1,12)
assert results[2]['tv']==F(1,36)
assert results[0]['expected_global_draws_post_initial']==results[1]['expected_global_draws_post_initial']==1
assert results[0]['expected_proposals_post_initial']==results[2]['expected_proposals_post_initial']==2
assert results[1]['expected_target_evals_full_memo_including_initial']<results[0]['expected_target_evals_full_memo_including_initial']
for P in [G,L,C]:
    assert all(sum(row)==1 for row in P)
    assert apply(pi,P)==pi
    assert all(pi[i]*P[i][j]==pi[j]*P[j][i] for i in range(4) for j in range(4))
assert apply(q,L)==q

# Ordinary pi-MH(Q) and delayed acceptance agree for this example.
assert mh(Q)==L
# Exact scalar forward KL = (3/4)log(3/2)+(1/4)log(1/2) < log(3/2)<1.

def enc(v):
    if isinstance(v,F): return {'exact':str(v),'decimal':float(v)}
    if isinstance(v,list): return [enc(x) for x in v]
    if isinstance(v,dict): return {k:enc(x) for k,x in v.items()}
    return v
out=enc({'input':{'q':q,'pi':pi,'Q':Q,'alpha':alpha},'G':G,'L':L,'C':C,
 'forward_KL':{'exact_expression':'(3/4)*log(3/2)+(1/4)*log(1/2)','certified_upper':'log(3/2)<1'},
 'comparisons':results,'matched_target_cost_randomized_pure_IMH':matched_target,
 'assertions':'PASS: exact laws, matched expected proposals, target memoization, invariance, reversibility, qL=q',
 'limitations':['Not a practical benchmark or simulation.','Expected resources do not imply equal pathwise budgets.','Matrices are known to diagnostic, not pre-supplied to a target-oracle algorithm.','Given all target values, direct finite sampling is a stronger ordinary alternative.'],
 'resources':{'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python':sys.version,'platform':platform.platform()}})
p=Path(__file__).with_name('safeguarded_cost_checks.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
