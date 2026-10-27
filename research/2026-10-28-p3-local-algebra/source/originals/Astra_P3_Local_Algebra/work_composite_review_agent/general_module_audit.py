#!/usr/bin/env python3
"""General-b coefficient kernels, center precision, and transverse Gaussian audit."""
from pathlib import Path
import itertools,json,random,sys
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_local_algebra_agent','work_chain_root'):
    sys.path.insert(0,str(ROOT/folder))
from acquired_chain_counter import *
from local_algebra_acquisition import acquire_chain
from field_descent import extract_anf,kernel_columns
from stationary_chain_counter import field_matrix_rank
from top_digit_deflation_audit import brute_sum


def exponents_of_degree(b,degree):
    if b==1:return [(degree,)]
    return [(i,)+tail for i in range(degree+1) for tail in exponents_of_degree(b-1,degree-i)]


def models(R,b):
    exponents=[(0,)*b]
    for i in range(b):
        e=[0]*b;e[i]=1;exponents.append(tuple(e))
    for i,j in itertools.combinations(range(b),2):
        e=[0]*b;e[i]=e[j]=1;exponents.append(tuple(e))
    for i in range(b):
        for j in range(b):
            e=[0]*b;e[i]+=2;e[j]+=1;exponents.append(tuple(e))
    G=R.gram();columns=[];labels=[];n=b*R.m
    for ex in exponents:
        support=[i for i in range(n) if ex[i//R.m]]
        outputs=[set() for _ in range(R.m)];zero=monomial(R,ex,[0]*b);unary={}
        for c in bits(linear_apply(G,zero)):outputs[c].add(0)
        for i in support:
            point=[0]*b;point[i//R.m]=1<<(i%R.m)
            unary[i]=monomial(R,ex,point)^zero
            for c in bits(linear_apply(G,unary[i])):outputs[c].add(1<<i)
        for i,j in itertools.combinations(support,2):
            point=[0]*b;point[i//R.m]^=1<<(i%R.m);point[j//R.m]^=1<<(j%R.m)
            value=monomial(R,ex,point)^zero^unary[i]^unary[j]
            for c in bits(linear_apply(G,value)):outputs[c].add((1<<i)|(1<<j))
        columns.extend(outputs);labels.extend((ex,1<<k) for k in range(R.m))
    return columns,labels


def kernel_cases():
    R=ChainRing(11,2);b=5;polys,labels=models(R,b);count=b*b+b*(b-1)//2+b
    results=[]
    for height in range(3):
        low=sum(((1<<(R.d*height))-1)<<(R.m*i) for i in range(b))
        masks=sorted({mask for p in polys for mask in p if mask&~low});pos={m:i for i,m in enumerate(masks)}
        columns=[sum(1<<pos[m] for m in p if m in pos) for p in polys]
        relations=kernel_columns(columns);forbidden=(1<<(R.d*(R.e-height)))-1
        for relation in relations:
            P={}
            for i in bits(relation):
                ex,c=labels[i];P[ex]=P.get(ex,0)^c
            assert all(not(c&forbidden) for ex,c in P.items() if sum(ex))
        assert len(relations)==R.m+count*R.d*height
        results.append(dict(b=b,d=R.d,e=R.e,height=height,columns=len(columns),rows=len(masks),
            kernel_dimension=len(relations),rank=len(columns)-len(relations),
            expected_rank=count*R.d*(R.e-height),all_kernel_vectors_checked=True))
    return results


def contraction(C,b):
    return [[C.get(tuple(sorted((i,j,k))),0) if k not in (i,j) else 0 for k in range(b)]
            for i,j in itertools.combinations(range(b),2)]


def solve_center(R,K,B,precision):
    b=len(K[0]);pairs=len(K)
    if not precision:return [0]*b
    S=ChainRing(R.h,precision);mask=(1<<S.m)-1;columns=[]
    for k in range(b):
        for bit in range(S.m):
            columns.append(sum(S.mul(row[k]&mask,1<<bit)<<(S.m*j) for j,row in enumerate(K)))
    assert len(span(columns))==b*S.m
    target=sum((B[j]&mask)<<(S.m*j) for j in range(pairs));answer=solve(columns,target)
    return None if answer is None else [(answer>>(S.m*k))&mask for k in range(b)]


def center_and_obstruction():
    R=ChainRing(11,2);b=5;q=1<<R.d;C={(0,1,2):1,(0,3,4):1};K=contraction(C,b)
    assert field_matrix_rank(K,R.h)==b
    center=[3,17,29,45,61]
    B=[]
    for row in K:
        value=0
        for c,x in zip(row,center):value^=R.mul(c,x)
        B.append(value)
    row=list(itertools.combinations(range(b),2)).index((1,3))
    assert not any(K[row]);B[row]^=1<<R.d
    assert solve_center(R,K,B,2) is None
    reduced=solve_center(R,K,B,1)
    assert reduced==[x&(q-1) for x in center]
    P={tuple(int(i in triple) for i in range(b)):c for triple,c in C.items()}
    raw=extract_anf(lambda x:R.functional(ring_polynomial(R,P,
        [(x>>(R.m*i))&((1<<R.m)-1) for i in range(b)])),b*R.m)
    acquired=acquire_chain(raw,b*R.m)
    assert acquired['module_dimension']==b and acquired['algebra_dimension']==R.m
    F=ChainRing(R.h,1);singular=[];ranks={}
    for chart in range(b):
        for prefix in itertools.product(range(q),repeat=chart):
            x=list(prefix)+[1]+[0]*(b-1-chart)
            gradient=[0]*b
            for triple,c in C.items():
                for i in triple:
                    j,k=[v for v in triple if v!=i]
                    gradient[i]^=gf_mul(c,gf_mul(x[j],x[k],R.h),R.h)
            if any(gradient):continue
            others=[i for i in range(b) if i!=chart]
            Hess=[[0]*len(others) for _ in others]
            for ii,i in enumerate(others):
                for jj,j in enumerate(others):
                    if i==j:continue
                    value=0
                    for k in range(b):
                        if k not in (i,j):value^=gf_mul(C.get(tuple(sorted((i,j,k))),0),x[k],R.h)
                    Hess[ii][jj]=value
            rank=field_matrix_rank(Hess,R.h);ranks[rank]=ranks.get(rank,0)+1
            singular.append(x)
    assert len(singular)==(q+1)**2+1 and ranks=={2:(q+1)**2,4:1}
    return dict(b=b,d=R.d,e=R.e,contraction_rank=b,center=center,
        altered_cross_coefficients=B,full_precision_center_exists=False,
        correct_mod_ideal_center=reduced,acquired_centroid_dimension=acquired['algebra_dimension'],
        acquired_module_dimension=acquired['module_dimension'],
        critical_ray_obstruction=dict(polynomial='X1*(X2*X3+X4*X5)',
            rational_singular_points=len(singular),transverse_hessian_rank_counts=ranks,
            meaning='radical-free third tensor does not imply finitely many nondegenerate critical rays'))


def transverse_cases():
    rng=random.Random(193361);results=[];m=4;b=5
    for h,e in [(7,3),(3,4),(3,5),(11,2)]:
        R=ChainRing(h,e);q=1<<R.d;mask=(1<<R.m)-1;height=e//2
        for trial in range(3):
            rows=[[int(i==j) for j in range(m)] for i in range(m)]
            for i in range(m):
                for j in range(i+1,m):rows[i][j]=rng.randrange(mask+1)
            diag=[rng.randrange(mask+1) for _ in range(m)]
            def quadratic(x,ring=R):
                y=[]
                for row in rows:
                    value=0
                    for a,z in zip(row,x):value^=ring.mul(a,z)
                    y.append(value)
                value=ring.mul(y[0],y[1])^ring.mul(y[2],y[3])
                for a,z in zip(diag,y):value^=ring.mul(a,ring.mul(z,z))
                return value
            cubic={ex:rng.randrange(mask+1) for ex in exponents_of_degree(m,3)}
            critical=[rng.randrange(mask+1) for _ in range(m)]+[1]
            r=(rng.randrange(mask+1)&~R.mask)^rng.randrange(1,q);r3=R.mul(r,R.mul(r,r));c=rng.randrange(mask+1)
            ids=[i*R.m+j for i in range(b) for j in range(R.d*height)]
            Q={0} if rng.randrange(2) else set()
            for i in ids:
                if rng.randrange(2):Q.add(1<<i)
            for i,j in itertools.combinations(ids,2):
                if rng.randrange(2):Q.add((1<<i)|(1<<j))
            width=R.d*(e-1)
            def phase(packed):
                u=[((packed>>(width*i))&((1<<width)-1))<<R.d for i in range(m)]
                value=c^quadratic(u)^ring_polynomial(R,cubic,u)
                point=[a^z for a,z in zip(critical[:m],u)]+[1]
                ambient=sum(R.mul(r,z)<<(R.m*i) for i,z in enumerate(point))
                return R.functional(R.mul(r3,value))^polynomial_value(Q,ambient)
            raw=extract_anf(phase,m*width);actual=brute_sum(raw,m*width)
            F=ChainRing(h,1)
            field_sum=sum(1-2*F.functional(quadratic(list(x),F)) for x in itertools.product(range(q),repeat=m))
            kappa=field_sum//q**(m//2);assert kappa in (-1,1)
            ambient=sum(R.mul(r,z)<<(R.m*i) for i,z in enumerate(critical))
            parity=R.functional(R.mul(r3,c))^polynomial_value(Q,ambient)
            expected=q**(m*e//2)*(kappa if e&1 else 1)*(1-2*parity)
            assert actual==expected
            results.append(dict(b=b,m=m,d=R.d,e=e,height=height,trial=trial,
                transverse_bits=m*width,exact_sum=actual,kappa=kappa,
                squarefree_cubic_terms=sum(sum(z==1 for z in ex)==3 and bool(v) for ex,v in cubic.items())))
    return results


if __name__=='__main__':
    result=dict(status='all exact assertions passed',coefficient_kernels=kernel_cases(),
                center_and_geometric_obstruction=center_and_obstruction(),
                weighted_transverse_cases=transverse_cases())
    Path(__file__).with_name('general_module_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],kernel_cases=len(result['coefficient_kernels']),
        transverse_cases=len(result['weighted_transverse_cases']),
        singular_rays=result['center_and_geometric_obstruction']['critical_ray_obstruction']['rational_singular_points'])))
