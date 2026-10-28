#!/usr/bin/env python3
"""Acquire and count an irreducible quadratic square-source operator.

Full source: Tr(beta e2(WX)+tr(D(WX)^2))+phi(tr(WX)), with W a
unit, phi a Boolean quadratic with nonzero polar, and D having an
irreducible quadratic minimal polynomial over the manufactured field.
The backend also accepts arbitrary phi, since it needs no unit recovery.

This module does not alter the root-owned two_eigenspace_quadratic.py.
No matrix units, extension basis, eigenspaces, or subspaces are supplied
to the raw compiler. All substitutions are exactly coefficient-checked.
"""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_matrix_root'))
from invariant_quadratic_matrix import quadratic_anf,invariant_features,polynomial_value
from raw_matrix_trace import (hidden_groups,AcquiredMatrixAlgebra,acquire_center,
    identity,inverse,bits,linear_apply,solve,compose,flat)
from matrix_kloosterman import Field
from polynomial_nilpotent_pair import choose,gl_order


def xor(values):
    out=0
    for value in values:out^=value
    return out


def quadratic_anf_sum(poly,n):
    """Exact binary quadratic Gauss sum from its full ANF, without queries."""
    poly=set(poly)
    if any(type(m) is not int or m<0 or m.bit_length()>n or m.bit_count()>2 for m in poly):
        raise ValueError('quadratic ANF with declared binary dimension required')
    remaining=set(range(n));multiplier=1
    while True:
        pair=next((m for m in poly if m.bit_count()==2),None)
        if pair is None:
            if any(poly):return 0
            return multiplier*(-1 if 0 in poly else 1)*(1<<len(remaining))
        i,j=bits(pair)
        A={m^(1<<i) for m in poly if m>>i&1 and not (m>>j&1)}
        B={m^(1<<j) for m in poly if m>>j&1 and not (m>>i&1)}
        poly={m for m in poly if not m&pair}
        for x in A:
            for y in B:
                monomial=x|y
                if monomial in poly:poly.remove(monomial)
                else:poly.add(monomial)
        remaining.remove(i);remaining.remove(j);multiplier*=2


def extension_subspace_multiplicity(m,u,ell,q):
    """Fq-subspaces in Fq2^m with E-core u and residual Fq-dimension ell."""
    if min(u,ell)<0 or u+ell>m:return 0
    ratio,remainder=divmod(gl_order(ell,q*q),gl_order(ell,q))
    if remainder:raise AssertionError('extension/subfield group order ratio')
    return choose(m,u,q*q)*choose(m-u,ell,q*q)*ratio


def canonical_source_value(packed,t,F,beta,gamma,zeta,phi):
    """D=gamma times blocks [[0,zeta],[1,1]], zeta of absolute trace one."""
    X=[[(packed>>(F.a*(i*t+j)))&(F.q-1) for j in range(t)] for i in range(t)]
    trace=xor(X[i][i] for i in range(t))
    second=xor(F.mul(X[i][i],X[j][j])^F.mul(X[i][j],X[j][i])
               for i in range(t) for j in range(i+1,t))
    marked=0
    for i in range(0,t,2):
        for k in range(t):
            marked^=F.mul(zeta,F.mul(X[i+1][k],X[k][i]))
            marked^=F.mul(X[i][k],X[k][i+1])
            marked^=F.mul(X[i+1][k],X[k][i+1])
    return F.trace(F.mul(beta,second)^F.mul(gamma,marked))^polynomial_value(phi,trace)


def canonical_kernel_restriction(poly,t,u,ell,a):
    """Restrict X to kill E^u plus Fq^ell in subsequent E coordinates."""
    killed=set(range(2*u))|{2*(u+i) for i in range(ell)}
    kept=[j for j in range(t) if j not in killed]
    numbers={j:i for i,j in enumerate(kept)}
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


def nonsplit_quadratic_gap(t,field_h,beta,gamma,zeta,phi):
    """Exact polynomial full-domain cubic count via two extension-orbit dimensions."""
    F=Field(field_h);q=F.q;a=F.a;phi=set(phi)
    if type(t) is not int or t<2 or t%2:raise ValueError('positive even matrix size required')
    if not 0<=beta<q or not 0<gamma<q or not 0<=zeta<q:
        raise ValueError('field coefficient out of range')
    if F.trace(zeta)!=1:raise ValueError('quadratic operator is not irreducible')
    if any(type(v) is not int or v<0 or v.bit_length()>a or v.bit_count()>2 for v in phi):
        raise ValueError('trace source must be a Boolean quadratic')
    native=quadratic_anf(lambda x:canonical_source_value(x,t,F,beta,gamma,zeta,phi),a*t*t)
    m=t//2;moments=[0]*(t+1);orbit_counts=[0]*(t+1);layers=[];onto=[1]
    for k in range(t):onto.append(onto[-1]*(q**t-q**k))
    for u in range(m+1):
        for ell in range(m-u+1):
            k=2*u+ell
            multiplicity=extension_subspace_multiplicity(m,u,ell,q)
            restricted,dimension=canonical_kernel_restriction(native,t,u,ell,a)
            value=quadratic_anf_sum(restricted,dimension)
            moments[k]+=multiplicity*value;orbit_counts[k]+=multiplicity
            layers.append(dict(extension_core_dimension=u,residual_subfield_dimension=ell,
                kernel_dimension=k,multiplicity=multiplicity,restricted_bits=dimension,
                quadratic_sum=value))
    if orbit_counts!=[choose(t,k,q) for k in range(t+1)]:
        raise AssertionError('extension orbits do not exhaust Grassmannians')
    gap=q**(t*t)*sum(onto[k]*moments[k] for k in range(t+1))
    return gap,dict(route='irreducible quadratic operator, two-dimension kernel aggregation',
        matrix_size=t,field_degree=a,field_modulus=field_h,beta=beta,gamma=gamma,zeta=zeta,
        trace_quadratic_anf=sorted(phi),kernel_moments=moments,kernel_orbit_layers=layers,
        uniform_polynomial_time=True,enumerated_subspaces=0,enumerated_field_elements=0,
        enumerated_original_assignments=0)


def acquire_square_source_parameters(poly,algebra):
    """Manufacture a unit and exact e2/square/trace coefficients before classification."""
    d=algebra.d;a=algebra.a;F=algebra.F
    polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    H=[solve(algebra.gram,column) for column in polar]
    if any(x is None for x in H):raise AssertionError('trace-dual polar solve')
    W=None
    for scalar in algebra.center:
        C=algebra.left_matrix(scalar)
        comm=[x^y for x,y in zip(compose(H,C),compose(C,H))]
        for value in comm:
            if value and algebra.is_unit(value):W=value;break
        if W is not None:break
    if W is None:raise ValueError('nonzero trace polar did not manufacture a unit')
    R=solve(algebra.left_matrix(W),algebra.one)
    if R is None or algebra.mul(R,W)!=algebra.one:raise AssertionError('unit inverse')
    normalized=quadratic_anf(lambda x:polynomial_value(poly,algebra.mul(R,x)),d)
    evaluate=invariant_features(algebra)
    qfeatures=[0]+[1<<i for i in range(a)]+[(1<<i)|(1<<j) for i in range(a) for j in range(i+1,a)]
    monomials=[0]+[1<<i for i in range(d)]+[(1<<i)|(1<<j) for i in range(d) for j in range(i+1,d)]
    positions={m:i for i,m in enumerate(monomials)}
    def packed(p):return sum(1<<positions[m] for m in p)
    columns=[packed(quadratic_anf(lambda x,m=m:int((evaluate(x)[0]&m)==m),d)) for m in qfeatures]
    columns += [packed(quadratic_anf(lambda x,b=1<<i:F.trace(F.mul(b,evaluate(x)[1])),d)) for i in range(a)]
    columns += [packed(quadratic_anf(lambda x,D=1<<i:algebra.trace(algebra.mul(D,algebra.mul(x,x))),d)) for i in range(d)]
    solution=solve(columns,packed(normalized))
    if solution is None:raise ValueError('source is not an acquired e2/square/trace quadratic')
    phi={m for i,m in enumerate(qfeatures) if solution>>i&1}
    beta=(solution>>len(qfeatures))&(F.q-1)
    D=solution>>(len(qfeatures)+a)
    check=quadratic_anf(lambda x:polynomial_value(phi,evaluate(x)[0])^
        F.trace(F.mul(beta,evaluate(x)[1]))^algebra.trace(algebra.mul(D,algebra.mul(x,x))),d)
    if check!=normalized:raise AssertionError('quadratic coefficient reconstruction')
    return beta,D,phi,dict(acquired_unit=W,acquired_inverse_unit=R,acquired_square_source=D,
        unit_acquisition_route='central scalar commutator',
        quadratic_coefficients_verified=len(monomials),full_coefficient_identity_verified=True)


def algebra_scalar_embedding(algebra):
    """Manufacture the central field embedding in the acquired algebra coordinates."""
    a=algebra.a;F=algebra.F
    one_coordinates=solve(algebra.field_columns,algebra.one)
    if one_coordinates is None:raise AssertionError('identity not in field-module coordinates')
    def scalar_element(s):
        coords=0
        for j in range(algebra.D):coords|=F.mul(s,(one_coordinates>>(a*j))&(F.q-1))<<(a*j)
        return linear_apply(algebra.field_columns,coords)
    scalar_columns=[scalar_element(1<<i) for i in range(a)]
    return scalar_columns,scalar_element


def fit_nonsplit_quadratic_source(poly,algebra):
    """Manufacture a source unit and irreducible quadratic operator intrinsically."""
    if algebra.t%2:raise ValueError('irreducible quadratic action requires even matrix size')
    beta,D,phi,evidence=acquire_square_source_parameters(poly,algebra)
    d=algebra.d;F=algebra.F
    scalar_columns,scalar_element=algebra_scalar_embedding(algebra)
    commutator=[algebra.mul(D,1<<i)^algebra.mul(1<<i,D) for i in range(d)]
    if not any(commutator):raise ValueError('square-source operator is central')
    scalar_actions=[algebra.left_matrix(c) for c in scalar_columns]
    gamma=solve([flat(compose(C,commutator),d) for C in scalar_actions],
                flat(compose(commutator,commutator),d))
    if gamma is None or not gamma:raise ValueError('source operator has no separable quadratic relation')
    D0=algebra.mul(scalar_element(F.inv(gamma)),D)
    center_value=algebra.mul(D0,D0)^D0
    zeta=solve(scalar_columns,center_value)
    if zeta is None:raise AssertionError('squared commutator identity lost centrality')
    if F.trace(zeta)!=1:raise ValueError('quadratic operator splits in the acquired field')
    if algebra.mul(D0,D0)^D0^scalar_element(zeta):raise AssertionError('quadratic relation')
    return beta,gamma,zeta,phi,dict(**evidence,acquired_normalized_operator=D0,
        irreducible_polynomial=[zeta,1,1],absolute_trace_irreducibility_test=1,
        extension_module_dimension=algebra.t//2)


def compile_raw_nonsplit_quadratic(poly,n):
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
    beta,gamma,zeta,phi,evidence=fit_nonsplit_quadratic_source(source,algebra)
    gap,backend=nonsplit_quadratic_gap(algebra.t,algebra.h,beta,gamma,zeta,phi)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,supplied_unit_or_extension_coordinates=False,
        seconds=time.perf_counter()-begun)
    return dict(original_bits=n,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,gap=gap,stats=stats)
