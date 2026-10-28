#!/usr/bin/env python3
"""Independent subspace, matrix, and affine-hidden nonsplit quadratic checks."""
from pathlib import Path
import itertools,json,random,sys,time
from nonsplit_quadratic_orbits import (Field,quadratic_anf,quadratic_anf_sum,
    extension_subspace_multiplicity,nonsplit_quadratic_gap,compile_raw_nonsplit_quadratic)
from matrix_kloosterman import rref
from raw_matrix_checks import native_anf
from invariant_quadratic_checks import matrix,multiply,rank
from field_descent import extract_anf,linear_apply,random_invertible,polynomial_value
from validate_nilpotent_extension_fields import random_unit


def xor(values):
    result=0
    for value in values:result^=value
    return result


def subspaces(t,F):
    for k in range(t+1):
        for pivots in itertools.combinations(range(t),k):
            slots=[(i,j) for i,p in enumerate(pivots) for j in range(p+1,t) if j not in pivots]
            for coefficients in itertools.product(range(F.q),repeat=len(slots)):
                rows=[[int(j==p) for j in range(t)] for p in pivots]
                for (i,j),c in zip(slots,coefficients):rows[i][j]=c
                yield rows


def companion(t,F,gamma,zeta):
    D=[[0]*t for _ in range(t)]
    for i in range(0,t,2):
        D[i][i+1]=F.mul(gamma,zeta);D[i+1][i]=D[i+1][i+1]=gamma
    return D


def apply(D,v,F):return [xor(F.mul(x,y) for x,y in zip(row,v)) for row in D]


def inverse_matrix(A,F):
    t=len(A);rows=[row+[int(i==j) for j in range(t)] for i,row in enumerate(A)]
    reduced,pivots=rref(rows,F,t)
    if len(pivots)!=t:raise ValueError('singular matrix in validation')
    return [row[t:] for row in reduced]


def independent_features(X,D,F):
    t=len(X);square=multiply(X,X,F);marked=multiply(D,square,F)
    trace=xor(X[i][i] for i in range(t))
    second=xor(F.mul(X[i][i],X[j][j])^F.mul(X[i][j],X[j][i])
               for i in range(t) for j in range(i+1,t))
    return trace,second,xor(marked[i][i] for i in range(t))


def independent_oracle(t,F,D,beta,phi,W=None):
    total=0
    for packed in range(F.q**(t*t)):
        X=matrix(packed,t,F.a);r=rank(X,F)
        U=multiply(W,X,F) if W is not None else X
        trace,second,marked=independent_features(U,D,F)
        phase=F.trace(F.mul(beta,second)^marked)^polynomial_value(phi,trace)
        total+=(1-2*phase)*F.q**(t*(t-r))
    return total*F.q**(t*t)


def audit_subspaces():
    cases=[]
    for t,h,zeta in [(2,3,1),(4,3,1),(6,3,1),(2,7,2),(4,7,2),(2,11,1)]:
        F=Field(h);D=companion(t,F,1,zeta);hist={}
        for K in subspaces(t,F):
            DK=[apply(D,v,F) for v in K]
            dim_intersection=2*len(K)-len(rref(K+DK,F,t)[1])
            assert dim_intersection%2==0
            u=dim_intersection//2;ell=len(K)-2*u
            hist[u,ell]=hist.get((u,ell),0)+1
        expected={(u,ell):extension_subspace_multiplicity(t//2,u,ell,F.q)
                  for u in range(t//2+1) for ell in range(t//2-u+1)}
        assert hist==expected,(t,h,hist,expected)
        cases.append(dict(t=t,h=h,zeta=zeta,subspaces=sum(hist.values()),
            histogram=[dict(extension_core=u,residual=ell,count=count) for (u,ell),count in sorted(hist.items())]))
        print('subspace orbits',t,h,sum(hist.values()),flush=True)
    return cases


def audit_matrix_counts():
    cases=[];rng=random.Random(48802)
    for t,h,zeta in [(2,3,1),(2,7,2),(2,7,3),(2,11,1),(4,3,1)]:
        F=Field(h);D=companion(t,F,1,zeta);hist={}
        for packed in range(F.q**(t*t)):
            X=matrix(packed,t,F.a);key=independent_features(X,D,F)
            hist[key]=hist.get(key,0)+F.q**(t*(t-rank(X,F)))
        features=[0]+[1<<i for i in range(F.a)]+[(1<<i)|(1<<j) for i in range(F.a) for j in range(i+1,F.a)]
        parameters=[]
        if F.q<=4:
            for beta in range(F.q):
                for gamma in range(1,F.q):
                    for mask in range(1<<len(features)):
                        parameters.append((beta,gamma,{m for i,m in enumerate(features) if mask>>i&1}))
        else:
            parameters=[(rng.randrange(F.q),rng.randrange(1,F.q),
                {m for m in features if rng.randrange(2)}) for _ in range(32)]
        for beta,gamma,phi in parameters:
            expected=F.q**(t*t)*sum(weight*(1-2*(F.trace(F.mul(beta,s)^F.mul(gamma,d))^
                polynomial_value(phi,tr))) for (tr,s,d),weight in hist.items())
            actual,meta=nonsplit_quadratic_gap(t,h,beta,gamma,zeta,phi)
            assert actual==expected,(t,h,zeta,beta,gamma,phi,actual,expected)
        cases.append(dict(t=t,h=h,zeta=zeta,enumerated_X=F.q**(t*t),
            phase_parameter_cases=len(parameters),last_parameters=dict(beta=beta,gamma=gamma,phi=sorted(phi)),
            last_gap=actual,last_backend=meta))
        print('matrix count',t,h,zeta,len(parameters),flush=True)
    return cases


def audit_raw():
    out=[]
    for h,zeta,group,constant,seed in [(7,2,0,0,97610),(7,3,1,1,97611),(11,1,2,1,97612)]:
        F=Field(h);t=2;d=F.a*t*t;rng=random.Random(seed)
        beta=rng.randrange(F.q);gamma=rng.randrange(1,F.q)
        phi={3,1}|({4} if F.a>2 else set())
        W=random_unit(t,F,rng);P=random_unit(t,F,rng)
        D=multiply(multiply(P,companion(t,F,gamma,zeta),F),inverse_matrix(P,F),F)
        def source(packed):
            U=multiply(W,matrix(packed,t,F.a),F)
            trace,second,marked=independent_features(U,D,F)
            return F.trace(F.mul(beta,second)^marked)^polynomial_value(phi,trace)
        zero=[[0]*t for _ in range(t)];base,n=native_anf(t,h,zero,zero,zero,constant)
        base^={monomial<<(group*d) for monomial in quadratic_anf(source,d)}
        change=random_invertible(n,rng);offset=rng.randrange(1<<n)
        raw=extract_anf(lambda x:polynomial_value(base,linear_apply(change,x)^offset),n)
        answer=compile_raw_nonsplit_quadratic(raw,n)
        expected=(-1)**constant*independent_oracle(t,F,D,beta,phi,W)
        assert answer['gap']==expected,(h,group,answer['gap'],expected)
        out.append(dict(t=t,h=h,zeta=zeta,seed=seed,original_group=group,constant=constant,
            beta=beta,gamma=gamma,trace_quadratic=sorted(phi),source_unit=W,square_operator=D,
            affine_columns=change,affine_offset=offset,raw_anf=sorted(raw),independent_gap=expected,
            production_result=answer))
        print('raw nonsplit',h,n,group,answer['stats']['seconds'],flush=True)
    return out


def controlled_rejections():
    F=Field(7);t=2;d=8;zero=[[0]*t for _ in range(t)];base,n=native_anf(t,7,zero,zero,zero)
    cases=[]
    for D,phi in [([[0,0],[0,1]],{3}),(companion(t,F,1,2),set())]:
        def source(x):
            tr,square,marked=independent_features(matrix(x,t,F.a),D,F)
            return F.trace(square^marked)^polynomial_value(phi,tr)
        raw=base^quadratic_anf(source,d)
        try:compile_raw_nonsplit_quadratic(raw,n)
        except ValueError as error:cases.append(str(error))
        else:raise AssertionError('split operator or zero trace polar incorrectly admitted')
    return cases


def run():
    begun=time.perf_counter();rng=random.Random(8881);gauss=0
    for n in range(11):
        features=[0]+[1<<i for i in range(n)]+[(1<<i)|(1<<j) for i in range(n) for j in range(i+1,n)]
        for _ in range(20):
            poly={m for m in features if rng.randrange(2)}
            assert quadratic_anf_sum(poly,n)==sum(1-2*polynomial_value(poly,x) for x in range(1<<n))
            gauss+=1
    result=dict(status='all exact comparisons passed',direct_gauss_cases=gauss,
        subspace_cases=audit_subspaces(),matrix_cases=audit_matrix_counts(),raw_cases=audit_raw(),
        controlled_rejections=controlled_rejections(),practical_speed_claim=False,
        seconds=time.perf_counter()-begun)
    Path(__file__).with_name('nonsplit_quadratic_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('all nonsplit quadratic checks passed',result['seconds'],flush=True)
    return result


if __name__=='__main__':run()
