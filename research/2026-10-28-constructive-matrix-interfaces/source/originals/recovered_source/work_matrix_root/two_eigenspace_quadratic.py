#!/usr/bin/env python3
"""Manufacture and count a noncentral quadratic matrix observable.

Raw complete family: Tr tr(XYZ)+Tr(beta e2(WX)+D(WX)^2)+p(tr(WX)),
W a unit, D split semisimple with at most two eigenvalues, p quadratic
with nonzero binary polar. The last condition manufactures W through
central commutators; no unit or eigenspace decomposition is supplied.
The intrinsic backend also accepts zero trace polar and beta=0.
"""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_slice_agent'))
from invariant_quadratic_matrix import (quadratic_anf,invariant_features,
    quadratic_sum,polynomial_value)
from raw_matrix_trace import (hidden_groups,AcquiredMatrixAlgebra,acquire_center,
    identity,inverse,bits,linear_apply,solve,compose,flat)
from matrix_kloosterman import Field
from two_invariant_quadratic_matrix import gaussian_rows


def xor(values):
    result=0
    for x in values:result^=x
    return result


def standard_source_value(packed,t,F,r,beta,gamma,phi):
    X=[[(packed>>(F.a*(i*t+j)))&(F.q-1) for j in range(t)] for i in range(t)]
    trace=xor(X[i][i] for i in range(t))
    second=xor(F.mul(X[i][i],X[j][j])^F.mul(X[i][j],X[j][i])
               for i in range(t) for j in range(i+1,t))
    marked_square=xor(F.mul(X[i][j],X[j][i]) for i in range(r) for j in range(t))
    return F.trace(F.mul(beta,second)^F.mul(gamma,marked_square))^polynomial_value(phi,trace)


def canonical_kernel_map(t,r,i,j,ell,a):
    """Bit substitution for matrices killing I+J+span(u_k+w_k)."""
    killed=set(range(i))|set(range(r,r+j))
    paired={r+j+k:i+k for k in range(ell)}
    labels=[]
    for column in range(t):
        if column in killed:labels.append(None)
        else:labels.append(paired.get(column,column))
    distinct=sorted({c for c in labels if c is not None})
    numbers={c:k for k,c in enumerate(distinct)}
    mapping=[]
    for row in range(t):
        for label in labels:
            for bit in range(a):
                mapping.append(None if label is None else a*(row*len(distinct)+numbers[label])+bit)
    return mapping,a*t*len(distinct)


def substitute_identified_bits(poly,mapping):
    """Exact quadratic substitution: some coordinates zero, others identified."""
    terms=[]
    for monomial in poly:
        value=0
        for bit in bits(monomial):
            new=mapping[bit]
            if new is None:break
            value|=1<<new
        else:terms.append(value)
    terms.sort();out=[];start=0
    while start<len(terms):
        end=start+1
        while end<len(terms) and terms[end]==terms[start]:end+=1
        if (end-start)&1:out.append(terms[start])
        start=end
    return out


def two_eigenspace_gap(t,field_h,r,beta,gamma,phi):
    """Complete polynomial backend, using three dimensions per kernel orbit."""
    F=Field(field_h);q=F.q;a=F.a;s=t-r;phi=set(phi)
    if type(t) is not int or t<1 or type(r) is not int or not 0<=r<=t:
        raise ValueError('invalid matrix/eigenspace dimension')
    if not 0<=beta<q or not 0<=gamma<q:raise ValueError('field coefficient out of range')
    if any(type(m) is not int or m<0 or m.bit_length()>a or m.bit_count()>2 for m in phi):
        raise ValueError('trace source is not quadratic')
    native=quadratic_anf(lambda x:standard_source_value(x,t,F,r,beta,gamma,phi),a*t*t)
    gaussian=gaussian_rows(t,q);gl=[1];onto=[1]
    for k in range(t):
        gl.append(gl[-1]*q**k*(q**(k+1)-1))
        onto.append(onto[-1]*(q**t-q**k))
    moments=[0]*(t+1);layers=[];orbit_counts=[0]*(t+1)
    for i in range(r+1):
        for j in range(s+1):
            for ell in range(min(r-i,s-j)+1):
                k=i+j+ell
                multiplicity=gaussian[r][i]*gaussian[s][j]*gaussian[r-i][ell]*gaussian[s-j][ell]*gl[ell]
                mapping,dimension=canonical_kernel_map(t,r,i,j,ell,a)
                restricted=substitute_identified_bits(native,mapping)
                value=quadratic_sum(lambda x:polynomial_value(restricted,x),dimension)
                moments[k]+=multiplicity*value;orbit_counts[k]+=multiplicity
                layers.append(dict(intersection_first=i,intersection_second=j,
                    graph_dimension=ell,kernel_dimension=k,multiplicity=multiplicity,
                    restricted_bits=dimension,quadratic_sum=value))
    if orbit_counts!=gaussian[t]:raise AssertionError('kernel orbit multiplicities do not exhaust Grassmannians')
    gap=q**(t*t)*sum(onto[k]*moments[k] for k in range(t+1))
    return gap,dict(route='two acquired eigenspaces, three-dimension kernel aggregation',
        matrix_size=t,field_degree=a,field_modulus=field_h,eigenspace_dimension=r,
        beta=beta,gamma=gamma,trace_quadratic_anf=sorted(phi),kernel_moments=moments,
        kernel_orbit_layers=layers,uniform_polynomial_time=True,
        enumerated_subspaces=0,enumerated_field_elements=0,enumerated_original_assignments=0)


def fit_two_eigenspace_source(poly,algebra):
    d=algebra.d;a=algebra.a;F=algebra.F
    polar=[0]*d
    for m in poly:
        if m.bit_count()==2:
            i,j=bits(m);polar[i]^=1<<j;polar[j]^=1<<i
    H=[solve(algebra.gram,c) for c in polar]
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
    phi={m for i,m in enumerate(qfeatures) if (solution>>i)&1}
    beta=(solution>>len(qfeatures))&(F.q-1)
    D=solution>>(len(qfeatures)+a)
    check=quadratic_anf(lambda x:polynomial_value(phi,evaluate(x)[0])^
        F.trace(F.mul(beta,evaluate(x)[1]))^algebra.trace(algebra.mul(D,algebra.mul(x,x))),d)
    if check!=normalized:raise AssertionError('quadratic coefficient reconstruction')
    one_coordinates=solve(algebra.field_columns,algebra.one)
    def scalar_element(s):
        coords=0
        for j in range(algebra.D):
            coords|=F.mul(s,(one_coordinates>>(a*j))&(F.q-1))<<(a*j)
        return linear_apply(algebra.field_columns,coords)
    scalar_columns=[scalar_element(1<<i) for i in range(a)]
    commutator=[algebra.mul(D,1<<i)^algebra.mul(1<<i,D) for i in range(d)]
    if not any(commutator):
        delta=solve(scalar_columns,D)
        if delta is None:raise AssertionError('central D not in acquired field')
        gamma=0;r=0;P=0
    else:
        scalar_actions=[algebra.left_matrix(c) for c in scalar_columns]
        gamma=solve([flat(compose(C,commutator),d) for C in scalar_actions],
                    flat(compose(commutator,commutator),d))
        if gamma is None or not gamma:raise ValueError('source matrix does not have two split eigenvalues')
        D0=algebra.mul(scalar_element(F.inv(gamma)),D)
        center_value=algebra.mul(D0,D0)^D0
        target=solve(scalar_columns,center_value)
        if target is None:raise AssertionError('squared commutator identity lost centrality')
        c=solve([F.mul(1<<i,1<<i)^(1<<i) for i in range(a)],target)
        if c is None:raise ValueError('the two eigenvalues do not split in the acquired field')
        P=D0^scalar_element(c);delta=F.mul(gamma,c)
        if algebra.mul(P,P)!=P:raise AssertionError('manufactured projector is not idempotent')
        r=algebra.reduced_rank(P)
        if not 0<r<algebra.t:raise AssertionError('noncentral projector has trivial rank')
    phi=quadratic_anf(lambda s:polynomial_value(phi,s)^F.trace(F.mul(delta,F.mul(s,s))),a)
    return r,beta,gamma,phi,dict(acquired_unit=W,acquired_inverse_unit=R,
        acquired_square_source=D,acquired_projector=P,eigenspace_dimension=r,
        unit_acquisition_route='central scalar commutator',quadratic_coefficients_verified=len(monomials),
        full_coefficient_identity_verified=True)


def compile_raw_two_eigenspace_quadratic(poly,n):
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
    r,beta,gamma,phi,evidence=fit_two_eigenspace_source(source,algebra)
    gap,backend=two_eigenspace_gap(algebra.t,algebra.h,r,beta,gamma,phi)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,supplied_unit_or_eigenspaces=False,seconds=time.perf_counter()-begun)
    return dict(original_bits=n,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,gap=gap,stats=stats)
