#!/usr/bin/env python3
"""Acquire and count matrix-trace cubics with an invariant quadratic source.

The accepted source on one block is Tr(beta*e2(DX))+q(tr(DX)), where
beta!=0, D is a unit, q is any Boolean quadratic on the acquired field,
and matrix size is at least two. Polar radicals, central commutators,
and a linear intertwiner equation manufacture D up to a harmless scalar.
No coordinates or unit D are supplied. The other two sources are zero.

After recognition, an exact orbit-incidence identity replaces all kernel
subspaces by their dimensions and binary Gaussian sums. Cost is polynomial;
there is no enumeration of field elements, matrices, or assignments.
"""
from pathlib import Path
import itertools,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_ring_count_agent'))
sys.path.insert(0,str(ROOT/'work_norm_slice_agent'))
from raw_matrix_trace import (hidden_groups,AcquiredMatrixAlgebra,acquire_center,
    identity,inverse,bits,linear_apply,solve,kernel_columns,reduced_charpoly,charpoly,
    polynomial_value,compose,flat)
from matrix_kloosterman import Field
from chain_ring_kloosterman import quadratic_sum

def quadratic_anf(value,n):
    c=value(0);single=[value(1<<i)^c for i in range(n)]
    out={0} if c else set()
    out.update(1<<i for i,v in enumerate(single) if v)
    for i in range(n):
        for j in range(i+1,n):
            if value((1<<i)|(1<<j))^single[i]^single[j]^c:
                out.add((1<<i)|(1<<j))
    return out

def gaussian_row(n,q):
    out=[1]
    for j in range(n):
        value,remainder=divmod(out[-1]*(q**(n-j)-1),q**(j+1)-1)
        if remainder:raise AssertionError('Gaussian coefficient division')
        out.append(value)
    return out

def invariant_quadratic_gap_diagonal(t,field_h,beta,trace_quadratic):
    """Full-domain gap of Tr tr(XYZ)+Tr(beta*e2(X))+q(tr X)."""
    F=Field(field_h);a=F.a;q=F.q
    trace_quadratic=set(trace_quadratic)
    if type(t) is not int or t<1 or not 0<=beta<q:
        raise ValueError('invalid dimension or coefficient')
    if any(type(m) is not int or m<0 or m.bit_length()>a or m.bit_count()>2
           for m in trace_quadratic):raise ValueError('trace source is not quadratic')
    matrix_gaussians=[];diagnostics=[]
    for r in range(t+1):
        def diagonal_phase(packed):
            diagonal=[(packed>>(a*i))&(q-1) for i in range(r)]
            trace=0;second=0
            for i,x in enumerate(diagonal):
                trace^=x
                for y in diagonal[:i]:second^=F.mul(x,y)
            return polynomial_value(trace_quadratic,trace)^F.trace(F.mul(beta,second))
        diagonal_sum=quadratic_sum(diagonal_phase,a*r)
        offdiag_power=a*(r*(r-1)//2 if beta else r*(r-1))
        value=diagonal_sum<<offdiag_power
        matrix_gaussians.append(value)
        diagnostics.append(dict(matrix_size=r,diagonal_bits=a*r,
            diagonal_gaussian=diagonal_sum,off_diagonal_factor_power=offdiag_power,
            full_matrix_gaussian=value))
    gaussian=gaussian_row(t,q);onto=[1]
    for j in range(t):onto.append(onto[-1]*(q**t-q**j))
    normalized=0
    for h in range(t+1):
        r=t-h
        normalized+=gaussian[h]*onto[h]*(q**(h*r))*matrix_gaussians[r]
    gap=(q**(t*t))*normalized
    return gap,dict(route='conjugation-invariant quadratic incidence aggregation',
        matrix_size=t,field_degree=a,field_modulus=field_h,beta=beta,
        trace_quadratic_anf=sorted(trace_quadratic),gaussian_layers=diagnostics,
        enumerated_subspaces=0,enumerated_field_elements=0,
        enumerated_original_assignments=0,uniform_polynomial_time=True)

def invariant_quadratic_gap(t,field_h,beta,trace_quadratic):
    """Polynomial backend using only two quadratic Gauss sums on field bits."""
    if type(t) is not int or t<1:raise ValueError('positive matrix size required')
    if not beta:return invariant_quadratic_gap_diagonal(t,field_h,beta,trace_quadratic)
    from invariant_quadratic_scalar_gauss import scalar_incidence_gap
    gap,data=scalar_incidence_gap(t,field_h,beta,trace_quadratic)
    data.update(route='conjugation-invariant quadratic incidence aggregation',
        gaussian_backend='two scalar quadratic Gauss sums',matrix_size=t,
        enumerated_subspaces=0,enumerated_original_assignments=0,
        uniform_polynomial_time=True)
    return gap,data

def invariant_features(algebra):
    """Intrinsic trace and second-characteristic-coefficient quadratic data."""
    d=algebra.d;F=algebra.F;taus=[];sigmas=[]
    for i in range(d):
        cp=reduced_charpoly(charpoly(algebra.field_left_matrix(1<<i),F),algebra.t,F)
        taus.append(cp[-2]);sigmas.append(cp[-3])
    pairs={}
    for i in range(d):
        for j in range(i+1,d):
            pairs[i,j]=F.mul(taus[i],taus[j])^linear_apply(taus,algebra.table[i][j])
    def evaluate(x):
        selected=list(bits(x));trace=linear_apply(taus,x);second=linear_apply(sigmas,x)
        for ii,i in enumerate(selected):
            for j in selected[ii+1:]:second^=pairs[i,j]
        return trace,second
    return evaluate

def fit_invariant_quadratic(poly,algebra):
    """Acquire a distinguished unit by linear algebra in the polar operator."""
    d=algebra.d;a=algebra.a;F=algebra.F
    polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    radical=kernel_columns(polar);R=None;D=None;route=None;tested=0
    for v in radical:
        tested+=1
        if algebra.is_unit(v):R=v;route='polar radical';break
    evaluate=invariant_features(algebra)
    qfeatures=[0]+[1<<i for i in range(a)]+[(1<<i)|(1<<j) for i in range(a) for j in range(i+1,a)]
    monomials=[0]+[1<<i for i in range(d)]+[(1<<i)|(1<<j) for i in range(d) for j in range(i+1,d)]
    positions={m:i for i,m in enumerate(monomials)}
    def packed(p):return sum(1<<positions[m] for m in p)
    columns=[]
    for monomial in qfeatures:
        columns.append(packed(quadratic_anf(
            lambda x,m=monomial:int((evaluate(x)[0]&m)==m),d)))
    for i in range(a):
        columns.append(packed(quadratic_anf(
            lambda x,beta=1<<i:F.trace(F.mul(beta,evaluate(x)[1])),d)))
    if R is None:
        H=[solve(algebra.gram,c) for c in polar]
        if any(v is None for v in H):raise AssertionError('polar trace-dual operator')
        for scalar in algebra.center:
            C=algebra.left_matrix(scalar)
            comm=[x^y for x,y in zip(compose(H,C),compose(C,H))]
            for v in comm:
                if v:
                    tested+=1
                    if algebra.is_unit(v):D=v;route='central scalar commutator';break
            if D is not None:break
        if D is None and algebra.t>=3:
            one_coordinates=solve(algebra.field_columns,algebra.one)
            if one_coordinates is None:raise AssertionError('field coordinates of identity')
            def scalar_element(s):
                coordinates=0
                for j in range(algebra.D):
                    c=(one_coordinates>>(a*j))&((1<<a)-1)
                    coordinates|=F.mul(s,c)<<(a*j)
                return linear_apply(algebra.field_columns,coordinates)
            J=[(1<<i)^scalar_element(evaluate(1<<i)[0]) for i in range(d)]
            equations=[flat(compose(H,L),d) for L in algebra.left]
            equations += [flat(compose(Right,J),d) for Right in algebra.right]
            solutions=kernel_columns(equations)
            for v in solutions:
                e=v&((1<<d)-1)
                if e:
                    tested+=1
                    if algebra.is_unit(e):R=e;route='linear polar intertwiner';break
        if D is None and R is None and algebra.t==2:
            start=1+d
            beta0=solve([c>>start for c in columns[len(qfeatures):]],packed(poly)>>start)
            if beta0 is None or not beta0:
                raise ValueError('two-by-two polar is not a nonzero determinant form')
            determinant_part=quadratic_anf(lambda x:F.trace(F.mul(beta0,evaluate(x)[1])),d)
            residual=poly^determinant_part
            if any(m.bit_count()>1 for m in residual):raise AssertionError('determinant polar removal')
            linear=sum(m for m in residual if m)
            source=algebra.source(linear,identity(d))
            if not source:D=algebra.one
            elif algebra.is_unit(source):D=source
            else:raise ValueError('two-by-two determinant has an inadmissible singular linear source')
            route='two-by-two determinant and linear source';tested+=int(bool(source))
    if D is None and R is not None:D=solve(algebra.left_matrix(R),algebra.one)
    if R is None and D is not None:R=solve(algebra.left_matrix(D),algebra.one)
    if D is None or R is None:raise ValueError('polar equations did not acquire a unit')
    if algebra.mul(D,R)!=algebra.one or algebra.mul(R,D)!=algebra.one:
        raise AssertionError('unit inverse acquisition')
    normalized=quadratic_anf(lambda x:polynomial_value(poly,algebra.mul(R,x)),d)
    solution=solve(columns,packed(normalized))
    if solution is None:raise ValueError('quadratic source is not an acquired trace/e2 invariant')
    qpoly={m for i,m in enumerate(qfeatures) if (solution>>i)&1}
    beta=solution>>len(qfeatures)
    if not beta:raise ValueError('this acquisition branch requires nonzero e2 coefficient')
    reconstructed=quadratic_anf(lambda x:polynomial_value(qpoly,evaluate(x)[0])^
        F.trace(F.mul(beta,evaluate(x)[1])),d)
    if reconstructed!=normalized:raise AssertionError('invariant coefficient identity failed')
    return beta,qpoly,dict(acquired_unit=D,acquired_inverse_unit=R,
        polar_rank=d-len(radical),polar_radical_dimension=len(radical),
        unit_acquisition_route=route,unit_candidates_tested=tested,
        invariant_features=len(columns),quadratic_coefficients_verified=len(monomials))

def compile_raw_invariant_quadratic(poly,n):
    begun=time.perf_counter();poly=set(poly)
    if type(n) is not int or n<=0 or any(type(m) is not int or m<0 or m.bit_length()>n
        or m.bit_count()>3 for m in poly):raise ValueError('raw cubic Boolean ANF required')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices);d=algebra.d
    centered,offset=acquire_center(grouped,slices,d,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//d for m in lower for i in bits(m)}
    if len(groups)!=1:raise ValueError('nonconstant lower terms must lie in one acquired group')
    group=next(iter(groups));local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    maps=[identity(d),algebra.Y,algebra.Z];back=inverse(maps[group])
    in_algebra=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    beta,qpoly,acquired=fit_invariant_quadratic(in_algebra,algebra)
    gap,backend=invariant_quadratic_gap(algebra.t,algebra.h,beta,qpoly)
    if abs(gap)>(1<<n) or gap%2:raise AssertionError('invalid exact output count')
    stats.update(algebra.stats);stats.update(acquired)
    stats.update(raw_monomials=len(poly),affine_offset=offset,quadratic_group=group,
        backend=backend,full_coefficient_identity_verified=True,
        supplied_unit_or_matrix_coordinates=False,seconds=time.perf_counter()-begun)
    return dict(original_bits=n,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,gap=gap,stats=stats)
