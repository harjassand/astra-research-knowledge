#!/usr/bin/env python3
"""One acquisition pass for certified polynomial square-source families.

Recognizes affine-hidden matrix cubics with one source
Tr(beta e2(WX)+tr(D(WX)^2)+eta*tr(DWX))+phi(tr(WX)).
The source unit is manufactured by a trace marker, odd scalar radical,
rank-two field pencil, size-two Pfaffian, or intrinsic Lie algebra.
Every cyclic-primary operator has a proved acquisition route; the exact
backend also admits certified semisimple primaries, quadratic operators,
and three split eigenspaces. All coefficients and operator types are
verified before the original-domain count is returned.
"""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from raw_matrix_trace import (hidden_groups,AcquiredMatrixAlgebra,acquire_center,
    bits,identity,inverse,linear_apply,solve,compose,flat,kernel_columns)
from invariant_quadratic_matrix import (quadratic_anf,polynomial_value,
    invariant_quadratic_gap,invariant_features)
from two_eigenspace_quadratic import two_eigenspace_gap
from nonsplit_quadratic_orbits import (acquire_square_source_parameters,
    algebra_scalar_embedding,nonsplit_quadratic_gap)
from squarezero_quadratic_orbits import squarezero_quadratic_gap


def acquire_operator_linear_refinement(poly,algebra,inverse_unit=None):
    """Manufacture beta,D,phi,eta after the source polar supplies its unit.

Fit the quadratic coefficients first. Their operator is unique modulo
the center. Trace-dualize the remaining affine source and certify its
membership in F*I + F*D, keeping the induced linear chain coefficient.
"""
    poly=set(poly);d=algebra.d;a=algebra.a;F=algebra.F
    polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    H=[solve(algebra.gram,column) for column in polar]
    W=None;R=inverse_unit;route='central scalar commutator with exact linear refinement'
    if R is not None:
        if not algebra.is_unit(R):raise ValueError('manufactured inverse source unit is singular')
        W=solve(algebra.left_matrix(R),algebra.one)
        route='verified manufactured source unit with exact linear refinement'
    else:
        for scalar in algebra.center:
            C=algebra.left_matrix(scalar)
            for value in (x^y for x,y in zip(compose(H,C),compose(C,H))):
                if value and algebra.is_unit(value):W=value;break
            if W is not None:break
        if W is None and algebra.t%2:
            radical=kernel_columns(H)
            if len(radical)==a and radical and algebra.is_unit(radical[0]):
                R=radical[0];W=solve(algebra.left_matrix(R),algebra.one)
                route='odd-dimension scalar polar radical with exact linear refinement'
        if W is None:raise ValueError('source polar did not manufacture a certified unit')
        if R is None:R=solve(algebra.left_matrix(W),algebra.one)
    normalized=quadratic_anf(lambda x:polynomial_value(poly,algebra.mul(R,x)),d)
    evaluate=invariant_features(algebra)
    qfeatures=[(1<<i)|(1<<j) for i in range(a) for j in range(i+1,a)]
    positions={(1<<i)|(1<<j):number for number,(i,j) in enumerate(
        (i,j) for i in range(d) for j in range(i+1,d))}
    def packed(p):return sum(1<<positions[m] for m in p if m.bit_count()==2)
    columns=[packed(quadratic_anf(lambda x,m=m:int((evaluate(x)[0]&m)==m),d)) for m in qfeatures]
    columns += [packed(quadratic_anf(lambda x,b=1<<i:F.trace(F.mul(b,evaluate(x)[1])),d)) for i in range(a)]
    columns += [packed(quadratic_anf(lambda x,A=1<<i:algebra.trace(algebra.mul(A,algebra.mul(x,x))),d)) for i in range(d)]
    solution=solve(columns,packed(normalized))
    if solution is None:raise ValueError('polar is outside the acquired square-source family')
    p2={m for i,m in enumerate(qfeatures) if solution>>i&1}
    beta=(solution>>len(qfeatures))&(F.q-1);D=solution>>(len(qfeatures)+a)
    quadratic=quadratic_anf(lambda x:polynomial_value(p2,evaluate(x)[0])^
        F.trace(F.mul(beta,evaluate(x)[1]))^algebra.trace(algebra.mul(D,algebra.mul(x,x))),d)
    residual=normalized^quadratic
    if any(m.bit_count()>1 for m in residual):raise AssertionError('quadratic source cancellation failed')
    A=algebra.source(sum(m for m in residual if m),identity(d))
    scalar_columns,scalar_element=algebra_scalar_embedding(algebra)
    refinement=solve(scalar_columns+[algebra.mul(c,D) for c in scalar_columns],A)
    if refinement is None:raise ValueError('linear source is outside the acquired span of identity and operator')
    alpha=refinement&(F.q-1);eta=refinement>>a;constant=int(0 in residual)
    phi=quadratic_anf(lambda s:polynomial_value(p2,s)^F.trace(F.mul(alpha,s))^constant,a)
    check=quadratic_anf(lambda x:polynomial_value(phi,evaluate(x)[0])^
        F.trace(F.mul(beta,evaluate(x)[1]))^algebra.trace(algebra.mul(D,algebra.mul(x,x)))^
        F.trace(F.mul(eta,algebra.relative_trace(algebra.mul(D,x)))),d)
    if check!=normalized:raise AssertionError('full linear-refinement coefficient identity failed')
    return beta,D,phi,eta,dict(acquired_unit=W,acquired_inverse_unit=R,
        acquired_square_source=D,acquired_operator_linear_coefficient=eta,
        unit_acquisition_route=route,
        full_coefficient_identity_verified=True,quadratic_coefficients_verified=1+d+d*(d-1)//2)


def count_acquired_cyclic_refinement(algebra,beta,D,phi,eta):
    from regular_chain_quadratic import count_acquired_regular_chain
    try:return count_acquired_regular_chain(algebra,beta,D,phi,eta)
    except ValueError:
        from simple_operator_quadratic import count_acquired_simple_operator
        try:return count_acquired_simple_operator(algebra,beta,D,phi,eta)
        except ValueError:
            from acquired_primary_counter import count_acquired_primary_source
            try:return count_acquired_primary_source(algebra,beta,D,phi,eta)
            except ValueError:
                from two_block_primary_pfaffian import count_acquired_two_row_primary
                try:return count_acquired_two_row_primary(algebra,beta,D,phi,eta)
                except ValueError:
                    from two_column_primary_pfaffian import count_acquired_two_column_primary
                    try:return count_acquired_two_column_primary(algebra,beta,D,phi,eta)
                    except ValueError:
                        from hook_primary_pfaffian import count_acquired_hook_primary
                        try:return count_acquired_hook_primary(algebra,beta,D,phi,eta)
                        except ValueError:
                            from durfee_primary_counter import count_acquired_four_alphabet_primary
                            try:return count_acquired_four_alphabet_primary(algebra,beta,D,phi,eta)
                            except ValueError:
                                from equidegree_squarefree_counter import count_acquired_squarefree_equidegree
                                return count_acquired_squarefree_equidegree(algebra,beta,D,phi,eta)


def count_acquired_operator_source(algebra,beta,D,phi):
    d=algebra.d;F=algebra.F;phi=set(phi)
    scalar_columns,scalar_element=algebra_scalar_embedding(algebra)
    def shift_trace(delta):
        return quadratic_anf(lambda x:polynomial_value(phi,x)^F.trace(F.mul(delta,F.mul(x,x))),F.a)
    scalar=solve(scalar_columns,D)
    if scalar is not None:
        gap,backend=invariant_quadratic_gap(algebra.t,algebra.h,beta,shift_trace(scalar))
        backend.update(operator_class='scalar',operator_relation=[scalar,1])
        return gap,backend
    square=algebra.mul(D,D);square_scalar=solve(scalar_columns,square)
    if square_scalar is not None:
        delta=F.pow(square_scalar,1<<(F.a-1));N=D^scalar_element(delta)
        if algebra.mul(N,N):raise AssertionError('manufactured nilpotent relation')
        r=algebra.reduced_rank(N)
        gap,backend=squarezero_quadratic_gap(algebra.t,algebra.h,r,beta,shift_trace(delta))
        backend.update(operator_class='repeated quadratic',operator_relation=[square_scalar,0,1],
                       acquired_squarezero_operator=N,squarezero_rank=r)
        return gap,backend
    J=[algebra.mul(D,1<<i)^algebra.mul(1<<i,D) for i in range(d)]
    actions=[algebra.left_matrix(c) for c in scalar_columns]
    gamma=solve([flat(compose(C,J),d) for C in actions],flat(compose(J,J),d))
    if gamma is None or not gamma:
        try:return count_acquired_cyclic_refinement(algebra,beta,D,phi,0)
        except ValueError:
            from three_eigenspace_quadratic import count_acquired_three_eigenspace_source
            return count_acquired_three_eigenspace_source(algebra,beta,D,phi)
    D0=algebra.mul(scalar_element(F.inv(gamma)),D)
    zeta=solve(scalar_columns,algebra.mul(D0,D0)^D0)
    if zeta is None:raise AssertionError('quadratic commutator identity did not centralize')
    if F.trace(zeta):
        gap,backend=nonsplit_quadratic_gap(algebra.t,algebra.h,beta,gamma,zeta,phi)
        backend.update(operator_class='irreducible quadratic',operator_relation=[zeta,1,1],
                       acquired_normalized_operator=D0)
    else:
        c=solve([F.mul(1<<i,1<<i)^(1<<i) for i in range(F.a)],zeta)
        if c is None:raise AssertionError('trace-zero Artin-Schreier equation unsolved')
        P=D0^scalar_element(c)
        if algebra.mul(P,P)!=P:raise AssertionError('manufactured projector')
        r=algebra.reduced_rank(P)
        gap,backend=two_eigenspace_gap(algebra.t,algebra.h,r,beta,gamma,shift_trace(F.mul(gamma,c)))
        backend.update(operator_class='split quadratic',operator_relation=[zeta,1,1],
                       acquired_projector=P,eigenspace_dimension=r)
    return gap,backend


def compile_raw_operator_quadratic(poly,n):
    begun=time.perf_counter();poly=set(poly)
    if type(n) is not int or n<=0 or any(type(m) is not int or m<0 or m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('raw cubic Boolean ANF required')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices);d=algebra.d
    centered,offset=acquire_center(grouped,slices,d,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//d for m in lower for i in bits(m)}
    if len(groups)!=1:raise ValueError('one acquired group must contain every nonconstant source term')
    group=next(iter(groups));local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    back=inverse([identity(d),algebra.Y,algebra.Z][group])
    source=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    try:beta,D,phi,evidence=acquire_square_source_parameters(source,algebra)
    except ValueError:
        try:
            beta,D,phi,eta,evidence=acquire_operator_linear_refinement(source,algebra)
            gap,backend=count_acquired_cyclic_refinement(algebra,beta,D,phi,eta)
        except ValueError:
            from regular_chain_pencil_field import fit_center_rank_two_source
            try:gap,backend,evidence=fit_center_rank_two_source(source,algebra,
                accept_simple=True,accept_primary=True,accept_equidegree=True)
            except ValueError:
                from matrix2_pfaffian_unit import count_matrix2_pfaffian_source
                try:gap,backend,evidence=count_matrix2_pfaffian_source(source,algebra)
                except ValueError:
                    from primary_operator_quadratic import count_unmarked_primary_lie_source
                    gap,backend,evidence=count_unmarked_primary_lie_source(source,algebra)
        backend.setdefault('route','unbounded regular chain, acquired center-field pencil')
        backend.update(matrix_size=algebra.t,field_degree=algebra.a,field_modulus=algebra.h,
            uniform_polynomial_time=True,enumerated_profiles=0,
            enumerated_subspaces=0,enumerated_field_elements=0,
            enumerated_original_assignments=0)
    else:gap,backend=count_acquired_operator_source(algebra,beta,D,phi)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,supplied_unit_or_operator_decomposition=False,
        seconds=time.perf_counter()-begun)
    return dict(original_bits=n,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,gap=gap,stats=stats)
