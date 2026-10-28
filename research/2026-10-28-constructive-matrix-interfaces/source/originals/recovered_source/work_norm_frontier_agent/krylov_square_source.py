#!/usr/bin/env python3
"""Krylov elimination of quadratic matrix sources and growing-degree counters.

For arbitrary D and K, its restricted quadratic Gaussian is reduced to
the induced operator on V/Fq[D]K with an explicit profile weight.
For regular nilpotent D and simple (irreducible characteristic) D, the
classical full-profile product formulas collapse the entire kernel sum
to a two-index dynamic program. Raw acquisition supplies D and its exact
minimal polynomial, so the degree and rank of D may grow without bound.
"""
import time
from nonsplit_quadratic_orbits import (quadratic_anf,quadratic_anf_sum,
    acquire_square_source_parameters,algebra_scalar_embedding,polynomial_value,
    hidden_groups,AcquiredMatrixAlgebra,acquire_center,identity,inverse,bits,
    linear_apply,solve,Field,choose)
from matrix_kloosterman import factor_polynomial,rref,kernel,mmul,minverse


def xor(values):
    out=0
    for v in values:out^=v
    return out


def source_evaluator(D,F,beta,phi):
    t=len(D);terms=[(i,j,D[i][j]) for i in range(t) for j in range(t) if D[i][j]]
    def value(packed):
        X=[[(packed>>(F.a*(i*t+j)))&(F.q-1) for j in range(t)] for i in range(t)]
        trace=xor(X[i][i] for i in range(t))
        second=xor(F.mul(X[i][i],X[j][j])^F.mul(X[i][j],X[j][i])
                   for i in range(t) for j in range(i+1,t))
        marked=xor(F.mul(c,F.mul(X[j][k],X[k][i])) for i,j,c in terms for k in range(t))
        return F.trace(F.mul(beta,second)^marked)^polynomial_value(phi,trace)
    return value


def full_matrix_gaussian(D,F,beta,phi):
    d=F.a*len(D)**2
    return quadratic_anf_sum(quadratic_anf(source_evaluator(D,F,beta,phi),d),d)


def span_rows(rows,F,t):
    R,pivots=rref(rows,F,t)
    return R[:len(pivots)]


def apply(D,v,F):return [xor(F.mul(x,y) for x,y in zip(row,v)) for row in D]


def quotient_by_invariant(D,S,F):
    t=len(D);S=span_rows(S,F,t);s=len(S);basis=list(S)
    for i in range(t):
        v=[int(i==j) for j in range(t)]
        if len(span_rows(basis+[v],F,t))>len(basis):basis.append(v)
    P=[list(row) for row in zip(*basis)] if t else []
    coordinates=mmul(mmul(minverse(P,F),D,F),P,F) if t else []
    if any(coordinates[i][j] for i in range(s,t) for j in range(s)):
        raise ValueError('claimed invariant subspace is not invariant')
    return [row[s:] for row in coordinates[s:]]


def restricted_gaussian_by_krylov(D,K,F,beta,phi):
    """Polynomial identity for one arbitrary kernel, not a global kernel enumerator."""
    t=len(D);current=span_rows(K,F,t);profile=[];previous=0
    while len(current)>previous:
        profile.append(len(current)-previous);previous=len(current)
        current=span_rows(current+[apply(D,v,F) for v in current],F,t)
    s=len(current);u=0;exponent=0
    for h in profile:u+=h;exponent+=h*(t-u)
    quotient=quotient_by_invariant(D,current,F)
    value=F.q**exponent*full_matrix_gaussian(quotient,F,beta,phi)
    return value,dict(profile=profile,invariant_span_dimension=s,quotient_operator=quotient,
        gaussian_exponent=exponent)


def profile_weight_dp(t,q,kind):
    """No partition enumeration: state is (accumulated size,last profile part)."""
    if kind not in ('regular_nilpotent','simple'):raise ValueError('unsupported profile product family')
    onto=[1]
    for k in range(t):onto.append(onto[-1]*(q**t-q**k))
    dp=[[0]*(t+1) for _ in range(t+1)];transitions=0
    for k in range(1,t+1):
        initial=onto[k]
        if kind=='simple':
            initial,remainder=divmod(initial,q**k-1)
            if remainder:raise AssertionError('surjection divisibility')
            initial*=q**t-1
        dp[k][k]+=initial*q**(k*(t-k))
    for u in range(1,t+1):
        for h in range(1,u+1):
            if not dp[u][h]:continue
            for b in range(1,min(h,t-u)+1):
                exponent=b*(t-u-(kind=='simple'))
                dp[u+b][b]+=dp[u][h]*choose(h,b,q)*q**exponent
                transitions+=1
    return [sum(row) for row in dp],dict(states=sum(bool(x) for row in dp for x in row),transitions=transitions)


def regular_nilpotent(t):return [[int(j==i+1) for j in range(t)] for i in range(t)]


def companion(poly):
    t=len(poly)-1;D=[[0]*t for _ in range(t)]
    for i in range(t):
        D[i][t-1]=poly[i]
        if i<t-1:D[i+1][i]=1
    return D


def cyclic_square_source_gap(t,field_h,beta,phi,kind,irreducible_polynomial=None):
    F=Field(field_h);phi=set(phi)
    if type(t) is not int or t<1 or not 0<=beta<F.q:raise ValueError('invalid dimension or coefficient')
    if any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('trace source must be a Boolean quadratic')
    weights,stats=profile_weight_dp(t,F.q,kind)
    if kind=='regular_nilpotent':
        gaussians=[full_matrix_gaussian(regular_nilpotent(r),F,beta,phi) for r in range(t+1)]
        normalized=gaussians[t]+sum(weights[s]*gaussians[t-s] for s in range(1,t+1))
    else:
        polynomial=list(irreducible_polynomial or [])
        factors=factor_polynomial(polynomial,F)
        if len(polynomial)!=t+1 or polynomial[-1]!=1 or factors!=[(polynomial,1)]:
            raise ValueError('monic irreducible polynomial of matrix degree required')
        gaussians=[1-2*polynomial_value(phi,0),full_matrix_gaussian(companion(polynomial),F,beta,phi)]
        normalized=gaussians[1]+weights[t]*gaussians[0]
    gap=F.q**(t*t)*normalized
    return gap,dict(route='Krylov Gaussian elimination and two-index profile DP',
        operator_kind=kind,matrix_size=t,field_degree=F.a,field_modulus=field_h,beta=beta,
        trace_quadratic_anf=sorted(phi),irreducible_polynomial=irreducible_polynomial,
        profile_weights=weights,quotient_gaussians=gaussians,**stats,
        uniform_polynomial_time=True,enumerated_partitions=0,enumerated_subspaces=0,
        enumerated_field_elements=0,enumerated_original_assignments=0)


def fit_cyclic_square_source(poly,algebra):
    beta,D,phi,evidence=acquire_square_source_parameters(poly,algebra)
    F=algebra.F;a=algebra.a;t=algebra.t
    scalar_columns,scalar_element=algebra_scalar_embedding(algebra)
    powers=[algebra.one];columns=[];minimal=None
    for degree in range(1,t+1):
        columns.extend(algebra.mul(scalar_element(1<<i),powers[-1]) for i in range(a))
        powers.append(algebra.mul(powers[-1],D));solution=solve(columns,powers[-1])
        if solution is not None:
            minimal=[(solution>>(a*i))&(F.q-1) for i in range(degree)]+[1]
            break
    if minimal is None or len(minimal)!=t+1:raise ValueError('source operator is not cyclic')
    factors=factor_polynomial(minimal,F)
    if len(factors)==1 and factors[0][1]==1:
        kind='simple';irreducible=minimal;delta=None
    elif len(factors)==1 and len(factors[0][0])==2 and factors[0][1]==t:
        kind='regular_nilpotent';irreducible=None;delta=factors[0][0][0]
        phi=quadratic_anf(lambda z:polynomial_value(phi,z)^F.trace(F.mul(delta,F.mul(z,z))),a)
    else:raise ValueError('cyclic source has neither a single linear primary nor irreducible polynomial')
    return kind,beta,phi,irreducible,dict(**evidence,acquired_minimal_polynomial=minimal,
        source_operator_kind=kind,scalar_translation=delta)


def compile_raw_cyclic_square_quadratic(poly,n):
    begun=time.perf_counter();poly=set(poly)
    if type(n) is not int or n<=0 or any(type(m) is not int or m<0 or m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('raw cubic Boolean ANF required')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices);d=algebra.d
    centered,offset=acquire_center(grouped,slices,d,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//d for m in lower for i in bits(m)}
    if len(groups)!=1:raise ValueError('nonconstant source must occupy one acquired group')
    group=next(iter(groups));local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    back=inverse([identity(d),algebra.Y,algebra.Z][group])
    source=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    kind,beta,phi,polynomial,evidence=fit_cyclic_square_source(source,algebra)
    gap,backend=cyclic_square_source_gap(algebra.t,algebra.h,beta,phi,kind,polynomial)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,supplied_unit_or_cyclic_basis=False,seconds=time.perf_counter()-begun)
    return dict(original_bits=n,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,gap=gap,stats=stats)
