#!/usr/bin/env python3
"""Contact-factor acquisition, nilpotent nonlinearity, and unbounded-rank hardness."""
from homogeneous_chain_counter import *
from field_descent import extract_anf,random_invertible,centroid,kernel_columns
from field_kloosterman import irreducible_binary
from quotient_height_boundary import signed_sum
import itertools,json,random


def exponent(b,indices):
    a=[0]*b
    for i in indices:a[i]+=1
    return tuple(a)


def add(P,a,c):
    P[a]=P.get(a,0)^c
    if not P[a]:del P[a]


def partial(P,i):
    out={}
    for a,c in P.items():
        if a[i]&1:
            v=list(a);v[i]-=1;add(out,tuple(v),c)
    return out


def contact_value(u,v,w,h):
    m=len(u)-1
    def omega(a,b):
        s=0
        for i in range(0,m,2):s^=gf_mul(a[i],b[i+1],h)^gf_mul(a[i+1],b[i],h)
        return s
    return gf_mul(u[-1],omega(v,w),h)^gf_mul(v[-1],omega(u,w),h)^gf_mul(w[-1],omega(u,v),h)


def factor_line_checks(rng):
    cases=[]
    for h,b in [(3,5),(7,5),(11,5),(11,7),(11,9)]:
        d=h.bit_length()-1;q=1<<d
        S=[[int(i==j) for j in range(b)] for i in range(b)]
        for _ in range(6*b):
            i,j=rng.sample(range(b),2);a=rng.randrange(1,q)
            S[i]=[x^gf_mul(a,y,h) for x,y in zip(S[i],S[j])]
        T={a:contact_value(*(S[i] for i in a),h) for a in itertools.combinations(range(b),3)}
        four=list(itertools.combinations(range(b),4));columns=[]
        for i in range(b):
            for k in range(d):
                column=0
                for j,a in enumerate(four):
                    if i in a:column^=gf_mul(1<<k,T[tuple(t for t in a if t!=i)],h)<<(d*j)
                columns.append(column)
        kernel=kernel_columns(columns)
        target=[sum(gf_mul(1<<k,S[i][-1],h)<<(d*i) for i in range(b)) for k in range(d)]
        assert len(kernel)==d
        assert all(Solver(kernel)(a) is not None for a in target)
        cases.append(dict(h=h,b=b,binary_kernel_dimension=len(kernel),
            field_kernel_dimension=1,linear_factor=[S[i][-1] for i in range(b)],
            wedge_equations=len(four),binary_unknowns=b*d))
    return cases


def hardness_checks(rng):
    cases=[];R=ChainRing(3,2)
    for N in [2,4,6]:
        b=N+3;m=b-1;n=2*b;z=m
        for trial in range(4):
            F={mask for mask in range(1<<N) if mask.bit_count()<=3 and rng.randrange(2)}
            P={}
            for i in range(0,m,2):
                for indices in [(z,i,i+1),(i,i,i+1),(i,i+1,i+1)]:add(P,exponent(b,indices),1)
            G=set(F)
            for i in range(0,N,2):
                term=(1<<i)|(1<<(i+1))
                if term in G:G.remove(term)
                else:G.add(term)
            G.add(1<<N) # the auxiliary a coordinate
            for mask in G:
                support=[i for i in range(m) if (mask>>i)&1]
                add(P,exponent(b,support+[z]*(3-len(support))),2)
            columns=random_invertible(n,rng);offset=rng.randrange(1<<n)
            def phase(x):
                y=linear_apply(columns,x)^offset
                return R.functional(ring_polynomial(R,P,[(y>>(2*i))&3 for i in range(b)]))
            raw=extract_anf(phase,n);actual=signed_sum(raw,n)
            source=sum(1-2*polynomial_value(F,u) for u in range(1<<N))
            expected=(1<<b)*(1+source)
            assert actual==expected,(N,F,actual,expected)
            algebra,_,_=centroid(raw,n);assert len(algebra)==2
            cases.append(dict(source_variables=N,ring_variables=b,original_binary_variables=n,
                source_anf=sorted(F),source_signed_count=source,ring_signed_count=actual,
                expected=expected,centroid_dimension=len(algebra),chart_kernel_dimension=m,
                ring_polynomial=[dict(exponents=a,coefficient=c) for a,c in P.items()],
                raw_anf=sorted(raw),binary_disguise_columns=columns,binary_disguise_offset=offset,
                truth_points=1<<n))
    return cases


def failures():
    R=ChainRing(3,2);b=5;z=4
    bad={exponent(b,[z,z,z]):1,exponent(b,[z,0,1]):1,exponent(b,[z,2,3]):1}
    def value(x):return R.functional(ring_polynomial(R,bad,[(x>>(2*i))&3 for i in range(b)]))
    raw=extract_anf(value,10);actual=signed_sum(raw,10)
    assert actual==320 and actual!=32
    nonlinear={exponent(b,[z,0,1]):1,exponent(b,[z,2,3]):1,exponent(b,[0,1,2]):2}
    g=partial(nonlinear,0);u=[0,1,0,0,1];v=[0,0,1,0,0]
    zero=[0]*b
    discrepancy=ring_polynomial(R,g,[a^c for a,c in zip(u,v)])^ring_polynomial(R,g,u)^ring_polynomial(R,g,v)^ring_polynomial(R,g,zero)
    assert discrepancy==2
    return dict(missing_infinity_check=dict(n=10,actual_signed_count=actual,
        incorrect_origin_only_count=32,raw_anf=sorted(raw)),
        full_gradient_not_binary_linear=dict(discrepancy=discrepancy,modulus=3,length=2,
            polynomial=[dict(exponents=a,coefficient=c) for a,c in nonlinear.items()],u=u,v=v))


def run():
    rng=random.Random(501927)
    geometry=factor_line_checks(rng);hardness=hardness_checks(rng);failure=failures()
    out=dict(status='all assertions passed',factor_line_cases=geometry,hardness_cases=hardness,
        decisive_failures=failure,total_truth_points=sum(c['truth_points'] for c in hardness)+1024,
        practical_speed_claim=False)
    Path(__file__).with_name('higher_rank_boundary_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],factor_line_cases=len(geometry),hardness_cases=len(hardness),
        total_truth_points=out['total_truth_points'],failure_counts=[320,32])))

if __name__=='__main__':run()
