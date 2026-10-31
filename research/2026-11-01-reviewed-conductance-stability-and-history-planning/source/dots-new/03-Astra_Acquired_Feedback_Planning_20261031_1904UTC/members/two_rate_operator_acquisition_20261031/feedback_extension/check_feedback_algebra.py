#!/usr/bin/env python3
"""Exact small-case policy-family, comparison and Bellman receiving tests."""
from pathlib import Path
import hashlib,itertools,json,random,sys
import sympy as s

ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT.parent))
from retained_large_acquisition import R,sqrt_up,compression,compile_integer_replay
from plan_feedback import exact_dp,pack,unpack
sys.path.insert(0,str(ROOT.parent.parent/'robust_operator_reuse_20261031'/'finite_observation'))
from robust_replay import psd,norm_up


def run():
    checks=0;rng=random.Random(3127);cases=[]
    def ck(ok):
        nonlocal checks
        assert ok;checks+=1
    for n,parts in ((4,[[0,1],[2,3]]),(5,[[0,1],[2,3,4]])):
        r=2;m=2;Z=s.zeros(n,r);W=s.zeros(r,n)
        for g,part in enumerate(parts):
            for i in part:Z[i,g]=1;W[g,i]=R(1,len(part))
        P=Z*W;Q=s.eye(n)-P;A=[]
        for a in range(m):
            rows=[]
            for i in range(n):
                counts=[rng.randrange(1,10) for _ in range(n)];rows.append([R(x,sum(counts)) for x in counts])
            A.append(s.Matrix(rows))
        B=[W*M*Z for M in A];F=[Q*M*Q for M in A];U=s.zeros(r)
        for g,src in enumerate(parts):
            for h,dest in enumerate(parts):
                # Frobenius upper works for this exact test; production uses
                # individually acquired spectral block bounds.
                U[g,h]=max(sqrt_up(sum(Fa[i,j]**2 for i in src for j in dest)) for Fa in F)
        alpha=norm_up(U,s.eye(r));ein=sqrt_up(m)*max(sqrt_up(sum(x*x for x in Q*M*P)) for M in A)
        eout=max(sqrt_up(n*sum(x*x for x in (W*M*Q).row(g))) for M in A for g in range(r))
        policies=list(itertools.product(range(m),repeat=r));AA=[];BB=[]
        for policy in policies:
            M=s.zeros(n);C=s.zeros(r)
            for g,part in enumerate(parts):
                for i in part:M[i,:]=A[policy[g]][i,:]
                C[g,:]=B[policy[g]][g,:]
            ck(M*s.ones(n,1)==s.ones(n,1));ck(W*M*Z==C)
            ck(psd(alpha**2*s.eye(n)-(Q*M*Q).T*(Q*M*Q)))
            AA.append(M);BB.append(C)
        b=Z*s.Matrix([0,1]);ell=W[0,:].T;ub=W*b;true_opt=None
        for L in range(4):
            E=compression(ein,eout,alpha,L);opt=-1;coarse_opt=-1
            for word in itertools.product(range(len(policies)),repeat=L):
                x=b;y=ub
                for a in word:x=AA[a]*x;y=BB[a]*y
                v=(ell.T*x)[0];vhat=y[0];ck(abs(v-vhat)<=E)
                opt=max(opt,v);coarse_opt=max(coarse_opt,vhat)
            model={'rank':r,'m':m,'length':L,'partition':parts,'task_b':list(map(int,b)),
                   'task_ell_numer':[int(i in parts[0]) for i in range(n)],'task_ell_denominator':len(parts[0]),
                   'compiled':compile_integer_replay(B,ub,s.Matrix([1,0]),20)}
            dp=exact_dp(model);ck(R(dp['coarse_optimal_value'])==coarse_opt)
            v=b
            for policy in dp['policy_by_remaining_steps']:
                idx=policies.index(tuple(policy));v=AA[idx]*v
            actual=(ell.T*v)[0];ck(opt-actual<=2*E)
        cases.append({'n':n,'policy_count':len(policies),'alpha':str(alpha),'tested_horizon':3})
    for bits in (1,2,3,7):
        values=[rng.randrange(1<<bits) for _ in range(37)];ck(unpack(pack(values,bits),len(values),bits)==values)
    return {'status':'PASS','checks':checks,'cases':cases,
            'scope':'Exact finite algebra and full restricted-policy enumeration in small cases; not independent review or provenance proof.',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    out=run();(ROOT/'feedback_algebra_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
