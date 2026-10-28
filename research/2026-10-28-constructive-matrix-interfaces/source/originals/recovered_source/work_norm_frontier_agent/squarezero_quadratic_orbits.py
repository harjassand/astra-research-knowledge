#!/usr/bin/env python3
"""Manufacture a square-zero source operator and count its kernel orbits.

This is the repeated-root completion of the split/nonsplit quadratic
operator branches. The raw source is Tr(beta e2(WX)+tr(D(WX)^2))+
phi(tr(WX)), with W a unit, nonzero trace polar, and D^2 central.
All operator ranks are admitted. No source decomposition is supplied.
"""
import time
from nonsplit_quadratic_orbits import (quadratic_anf,quadratic_anf_sum,
    acquire_square_source_parameters,algebra_scalar_embedding,polynomial_value,
    hidden_groups,AcquiredMatrixAlgebra,acquire_center,identity,inverse,bits,
    linear_apply,solve,Field,choose)


def xor(values):
    out=0
    for x in values:out^=x
    return out


def squarezero_subspace_multiplicity(t,r,h,j,b,c,q):
    """Orbit indexed by K cap imN, middle quotient, NK, and their intersection."""
    s=t-2*r
    if not(0<=r<=t//2 and 0<=h<=r and 0<=j<=s and 0<=b<=r and
           max(0,h+b-r)<=c<=min(h,b)):return 0
    exponent=j*(r-h)+(h-c)*(b-c)+b*(r+s-h-j)
    return choose(r,h,q)*choose(s,j,q)*choose(h,c,q)*choose(r-h,b-c,q)*q**exponent


def squarezero_source_value(packed,t,F,r,beta,phi):
    X=[[(packed>>(F.a*(i*t+j)))&(F.q-1) for j in range(t)] for i in range(t)]
    trace=xor(X[i][i] for i in range(t))
    second=xor(F.mul(X[i][i],X[j][j])^F.mul(X[i][j],X[j][i])
               for i in range(t) for j in range(i+1,t))
    marked=xor(F.mul(X[t-r+i][k],X[k][i]) for i in range(r) for k in range(t))
    return F.trace(F.mul(beta,second)^marked)^polynomial_value(phi,trace)


def zero_columns_restriction(poly,t,killed,a):
    kept=[j for j in range(t) if j not in killed];numbers={j:i for i,j in enumerate(kept)}
    mapping=[]
    for row in range(t):
        for col in range(t):
            for bit in range(a):
                mapping.append(None if col in killed else a*(row*len(kept)+numbers[col])+bit)
    out=set()
    for monomial in poly:
        image=0
        for bit in bits(monomial):
            value=mapping[bit]
            if value is None:break
            image|=1<<value
        else:
            if image in out:out.remove(image)
            else:out.add(image)
    return out,a*t*len(kept)


def squarezero_quadratic_gap(t,field_h,r,beta,phi):
    F=Field(field_h);q=F.q;a=F.a;phi=set(phi)
    if type(t) is not int or t<1 or type(r) is not int or not 0<=r<=t//2:
        raise ValueError('invalid matrix size or square-zero rank')
    if not 0<=beta<q:raise ValueError('field coefficient out of range')
    if any(type(m) is not int or m<0 or m.bit_length()>a or m.bit_count()>2 for m in phi):
        raise ValueError('trace source is not a Boolean quadratic')
    s=t-2*r
    native=quadratic_anf(lambda x:squarezero_source_value(x,t,F,r,beta,phi),a*t*t)
    moments=[0]*(t+1);counts=[0]*(t+1);layers=[];onto=[1]
    for k in range(t):onto.append(onto[-1]*(q**t-q**k))
    for h in range(r+1):
        for j in range(s+1):
            for b in range(r+1):
                for c in range(max(0,h+b-r),min(h,b)+1):
                    k=h+j+b
                    multiplicity=squarezero_subspace_multiplicity(t,r,h,j,b,c,q)
                    killed=set(range(h))|set(range(r,r+j))
                    killed|={t-r+i for i in list(range(c))+list(range(h,h+b-c))}
                    if len(killed)!=k:raise AssertionError('canonical kernel dimension')
                    restricted,dimension=zero_columns_restriction(native,t,killed,a)
                    value=quadratic_anf_sum(restricted,dimension)
                    moments[k]+=multiplicity*value;counts[k]+=multiplicity
                    layers.append(dict(intersection_image=h,middle_dimension=j,
                        image_dimension=b,image_intersection=c,kernel_dimension=k,
                        multiplicity=multiplicity,restricted_bits=dimension,quadratic_sum=value))
    if counts!=[choose(t,k,q) for k in range(t+1)]:
        raise AssertionError('square-zero orbits do not exhaust Grassmannians')
    gap=q**(t*t)*sum(onto[k]*moments[k] for k in range(t+1))
    return gap,dict(route='square-zero source, four-dimension kernel aggregation',
        matrix_size=t,field_degree=a,field_modulus=field_h,squarezero_rank=r,
        beta=beta,trace_quadratic_anf=sorted(phi),kernel_moments=moments,
        kernel_orbit_layers=layers,uniform_polynomial_time=True,
        enumerated_subspaces=0,enumerated_field_elements=0,enumerated_original_assignments=0)


def fit_squarezero_quadratic_source(poly,algebra):
    beta,D,phi,evidence=acquire_square_source_parameters(poly,algebra)
    F=algebra.F;a=algebra.a
    scalar_columns,scalar_element=algebra_scalar_embedding(algebra)
    target=solve(scalar_columns,algebra.mul(D,D))
    if target is None:raise ValueError('square-source operator has noncentral square')
    delta=F.pow(target,1<<(a-1))
    N=D^scalar_element(delta)
    if algebra.mul(N,N):raise AssertionError('manufactured operator is not square zero')
    r=algebra.reduced_rank(N)
    if not 0<=r<=algebra.t//2:raise AssertionError('invalid square-zero rank')
    phi=quadratic_anf(lambda z:polynomial_value(phi,z)^F.trace(F.mul(delta,F.mul(z,z))),a)
    return r,beta,phi,dict(**evidence,acquired_squarezero_operator=N,squarezero_rank=r,
        acquired_scalar_translation=delta,central_square=target)


def compile_raw_squarezero_quadratic(poly,n):
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
    r,beta,phi,evidence=fit_squarezero_quadratic_source(source,algebra)
    gap,backend=squarezero_quadratic_gap(algebra.t,algebra.h,r,beta,phi)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,supplied_unit_or_operator_normal_form=False,
        seconds=time.perf_counter()-begun)
    return dict(original_bits=n,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,gap=gap,stats=stats)
