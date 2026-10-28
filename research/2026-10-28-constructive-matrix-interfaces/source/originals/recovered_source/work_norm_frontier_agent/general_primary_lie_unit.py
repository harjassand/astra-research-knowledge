#!/usr/bin/env python3
"""Intrinsic source units for noncyclic single-primary operators.

Only the algebra and source polar are supplied. Full source/type fitting is
mandatory. The new steps use the normalizer's multiplication defect and a
linear multiplicative lift of its projective transport.
"""
from primary_lie_unit import *
sys.path.insert(0,str(ROOT/'work_norm_glue_agent'))
from local_unit_sandwich import recover_local_unit_sandwich


def acquire_commutant_from_normalizer(A,N):
    """For N={b:[D,b] in F}, manufacture C_D intrinsically."""
    n=len(N);ann=kernel([A.coordinates(x) for x in N],A.F,A.m)
    products=[[A.coordinates(A.mul(x,y)) for y in N] for x in N]
    forms=[];kernel_rows=[]
    for row in ann:
        M=[[xor(A.F.mul(c,v) for c,v in zip(row,products[i][j]))
            for j in range(n)] for i in range(n)]
        rank=len(rref(M,A.F,n)[1])
        if not rank:continue
        if rank!=2 or any(M[i][i] for i in range(n)):
            raise ValueError('multiplication defect is not an alternating rank-two pencil')
        forms.append(M);kernel_rows.extend(kernel(M,A.F,n))
    if not forms:return N,dict(normalizer_associative=True,defect_forms=0)
    line=kernel(kernel_rows,A.F,n)
    if len(line)!=1:raise ValueError('no unique common row line in multiplication defect')
    C=[combination(A,v,N) for v in kernel(line,A.F,n)]
    for x in C:
        for y in C:coordinates_in(A,C,A.mul(x,y))
    return C,dict(normalizer_associative=False,defect_forms=len(forms),
                  acquired_commutant_codimension=1)


def lift_projective_commutant(A,stabilizer,C):
    """Remove scalar ambiguities by linear multiplicativity equations."""
    right=[A.coordinates(b) for a,b in stabilizer]
    columns=list(map(list,zip(*right)));left=[]
    for b in C:
        coeff,rank=field_solve(columns,A.coordinates(b),A.F,len(stabilizer))
        if coeff is None:raise ValueError('commutant outside polar normalizer')
        left.append(combination(A,coeff,[a for a,b in stabilizer]))
    ann=kernel([A.coordinates(A.one)],A.F,A.m)
    def project(x):
        value=A.coordinates(x)
        return [xor(A.F.mul(c,v) for c,v in zip(row,value)) for row in ann]
    projected=[project(x) for x in left];rows=[];target=[];s=len(C)
    for i,x in enumerate(C):
        for j,y in enumerate(C):
            coeff=coordinates_in(A,C,A.mul(x,y))
            defect=project(A.mul(left[i],left[j])^combination(A,coeff,left))
            for k,value in enumerate(defect):
                row=[0]*s;row[i]^=projected[j][k];row[j]^=projected[i][k]
                rows.append(row);target.append(value)
    scalars,rank=field_solve(rows,target,A.F,s)
    if scalars is None or rank!=s:
        raise ValueError('no unique multiplicative scalar lift')
    lifted=[x^scale(A,c,A.one) for x,c in zip(left,scalars)]
    for i,x in enumerate(C):
        for j,y in enumerate(C):
            coeff=coordinates_in(A,C,A.mul(x,y))
            if A.mul(lifted[i],lifted[j])!=combination(A,coeff,lifted):
                raise ValueError('corrected projective transport is not multiplicative')
    one=coordinates_in(A,C,A.one)
    if combination(A,one,lifted)!=A.one:
        raise ValueError('corrected transport is not unital')
    return list(zip(lifted,C)),dict(projective_lift_unknowns=s,
        projective_lift_rank=rank,multiplicative_transport_verified=True)


def acquire_source_commutant_coset(A,P):
    """Return (C_D,F[D],F[D]W,evidence), valid for arbitrary D, t>=4."""
    if A.t<4:raise ValueError('rank-gap unit route requires matrix size at least four')
    stabilizer=polar_stabilizer(A,P)
    N=[A.pack(v) for v in independent([A.coordinates(b) for a,b in stabilizer],A.F,A.m)]
    C,meta=acquire_commutant_from_normalizer(A,N)
    pairs,lift=lift_projective_commutant(A,stabilizer,C)
    U=intertwiner_space(A,pairs)
    E=intertwiner_space(A,[(b,b) for b in C])
    if len(E)!=len(U):raise ValueError('commutant and transported coset have different dimensions')
    if any(A.mul(x,y)!=A.mul(y,x) for x in E for y in E):
        raise ValueError('double commutant is not commutative')
    meta.update(lift)
    meta.update(matrix_size=A.t,field_degree=A.F.a,
        stabilizer_dimension=len(stabilizer),normalizer_dimension=len(N),
        commutant_dimension=len(C),unit_intertwiner_dimension=len(U),
        supplied_source_unit=False,supplied_operator=False,supplied_matrix_units=False)
    return C,E,U,meta


def recover_general_primary_source_unit(A,P):
    C,E,U,meta=acquire_source_commutant_coset(A,P)
    if not 1<=len(U)<A.t:raise ValueError('operator must be noncyclic')
    V=next((x for x in U if A.is_unit(x)),None)
    if V is None:raise ValueError('no displayed unit in manufactured local-ring coset')
    Vinv=A.inv(V);E=[A.mul(x,Vinv) for x in U]
    normalized=lambda x:A.mul(P(A.mul(Vinv,x)),Vinv)
    S=reshuffle(A,normalized);H,sandwich=recover_local_unit_sandwich(A,S,E)
    W=A.mul(H,V)
    if not A.is_unit(W):raise ValueError('manufactured source unit is singular')
    meta.update(sandwich)
    meta.update(route='normalizer multiplication defect, linear projective lift, and radical sandwich',
        supplied_source_unit=False,supplied_operator=False,supplied_matrix_units=False)
    return W,meta


def recover_from_raw_general_primary_source(poly,algebra):
    d=algebra.d;polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    columns=[binary_solve(algebra.gram,v) for v in polar]
    P=lambda x:linear_apply(columns,x);A=Intrinsic(algebra)
    for e in A.basis:
        for bit in range(A.F.a):
            if P(scale(A,1<<bit,e))!=scale(A,1<<bit,P(e)):
                raise ValueError('source polar is not linear over the acquired center')
    return recover_general_primary_source_unit(A,P)


def count_general_primary_source(poly,algebra):
    from operator_quadratic_counter import acquire_operator_linear_refinement
    from arbitrary_operator_hall import arbitrary_operator_gap
    W,evidence=recover_from_raw_general_primary_source(poly,algebra)
    inverse_unit=binary_solve(algebra.left_matrix(W),algebra.one)
    beta,D,phi,eta,fit=acquire_operator_linear_refinement(poly,algebra,inverse_unit)
    polynomial,primary=algebra.primary_data(D)
    if not beta or any(m.bit_count()>1 for m in phi) or len(primary)!=1 or primary[0]['jordan_columns'][0]<2:
        raise ValueError('fitted operator must be a noncyclic single primary')
    gap,backend=arbitrary_operator_gap(primary,algebra.h,beta,phi,eta)
    fit.update(unit_acquisition=evidence,acquired_reduced_charpoly=polynomial,
        unit_acquisition_route=evidence['route'])
    return gap,backend,fit


def compile_raw_general_primary(poly,n):
    import time
    from raw_matrix_trace import hidden_groups,AcquiredMatrixAlgebra,acquire_center,identity,inverse
    from invariant_quadratic_matrix import quadratic_anf,polynomial_value
    begun=time.perf_counter();poly=set(poly)
    if type(n) is not int or n<=0 or any(type(m) is not int or m<0 or m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('raw cubic Boolean ANF required')
    grouped,slices,group_map,stats=hidden_groups(poly,n);algebra=AcquiredMatrixAlgebra(slices);d=algebra.d
    centered,offset=acquire_center(grouped,slices,d,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//d for m in lower for i in bits(m)}
    if len(groups)!=1:raise ValueError('one acquired group must contain all nonconstant source terms')
    group=next(iter(groups));local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    back=inverse([identity(d),algebra.Y,algebra.Z][group])
    source=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    gap,backend,evidence=count_general_primary_source(source,algebra)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,seconds=time.perf_counter()-begun,
        supplied_unit_or_operator_decomposition=False)
    return dict(original_bits=n,gap=gap,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,stats=stats)
