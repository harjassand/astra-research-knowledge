#!/usr/bin/env python3
"""Manufacture a source unit for every beta-nonzero square operator, t>=4.

The input is a certified central simple matrix algebra and its source polar.
No source operator, unit, spectral decomposition, or matrix units are supplied.
Counting still requires a full coefficient fit and the charged Hall backend.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_norm_frontier_agent'),str(ROOT/'work_norm_glue_agent')]
from general_primary_lie_unit import acquire_source_commutant_coset
from primary_lie_unit import coordinates_in,recover_primary_source_unit
from lie_source_unit import (Intrinsic,scale,combination,power,independent,
    relations,field_solve,reshuffle,kernel,rref,xor,recover_source_unit,
    binary_solve,linear_apply,bits)
from local_unit_sandwich import recover_local_unit_sandwich
from matrix_kloosterman import charpoly,factor_polynomial

def element_rank(A,x):
    """Rank of left multiplication; this is t times the ordinary matrix rank."""
    return len(independent([A.coordinates(A.mul(x,e)) for e in A.basis],A.F,A.m))

def split_commutative_components(A,E):
    """Acquire CRT idempotents via the q-Frobenius fixed algebra F_q^r."""
    if not E:raise ValueError('empty commutative algebra')
    fixed=[combination(A,c,E) for c in relations(
        [A.coordinates(power(A,e,A.F.q)^e) for e in E],A.F)]
    if not fixed:raise ValueError('no scalar Frobenius-fixed subalgebra')
    pieces=[A.one];factored_degrees=[]
    for g in fixed:
        columns=[coordinates_in(A,fixed,A.mul(g,e)) for e in fixed]
        polynomial=charpoly(list(map(list,zip(*columns))),A.F)
        factors=factor_polynomial(polynomial,A.F);factored_degrees.append(len(polynomial)-1)
        if any(len(f)!=2 for f,multiplicity in factors):
            raise ValueError('Frobenius-fixed algebra is not split')
        roots=[A.F.mul(f[0],A.F.inv(f[1])) for f,multiplicity in factors]
        cuts=[]
        for root in roots:
            cut=A.one
            for other in roots:
                if other!=root:
                    cut=A.mul(cut,scale(A,A.F.inv(root^other),g^scale(A,other,A.one)))
            cuts.append(cut)
        pieces=[A.mul(p,cut) for p in pieces for cut in cuts if A.mul(p,cut)]
        if len(pieces)==len(fixed):break
    if len(pieces)!=len(fixed) or xor(pieces)!=A.one:
        raise ValueError('incomplete primitive idempotent decomposition')
    for i,p in enumerate(pieces):
        if A.mul(p,p)!=p or any(A.mul(p,q) for q in pieces[:i]):
            raise ValueError('CRT projectors are not orthogonal idempotents')
    bases=[[A.pack(v) for v in independent([A.coordinates(A.mul(p,e)) for e in E],A.F,A.m)]
           for p in pieces]
    if sum(map(len,bases))!=len(E):raise ValueError('CRT components do not span E')
    return pieces,bases,dict(primary_components=len(pieces),
        frobenius_fixed_dimension=len(fixed),factored_split_degrees=factored_degrees,
        enumerated_field_elements=0)

def manufacture_coset_unit(A,pieces,U):
    selected=[];ranks=[]
    for p in pieces:
        expected=element_rank(A,p);component=[A.pack(v) for v in independent(
            [A.coordinates(A.mul(p,x)) for x in U],A.F,A.m)]
        candidate=next((x for x in component if element_rank(A,x)==expected),None)
        if candidate is None:raise ValueError('local coset has no displayed full-rank element')
        selected.append(candidate);ranks.append(expected)
    V=xor(selected)
    if not A.is_unit(V):raise ValueError('assembled CRT coset element is singular')
    return V,ranks

def lift_global_sandwich(A,S,pieces,bases):
    """Recover sqrt(beta) H from the quotient sandwich with >=2 primaries."""
    if len(pieces)<2:raise ValueError('at least two primary components are required')
    E=sum(bases,[]);m=len(E)
    annihilator=kernel([A.coordinates(e) for e in E],A.F,A.m)
    def project(x):
        coords=A.coordinates(x)
        return [xor(A.F.mul(v,w) for v,w in zip(row,coords)) for row in annihilator]
    columns=[sum((project(A.mul(left,A.mul(x,right))) for x in A.basis),[])
             for left in E for right in E]
    target=sum((project(S(x)) for x in A.basis),[])
    coeff,rank=field_solve(list(map(list,zip(*columns))),target,A.F,m*m)
    if coeff is None:raise ValueError('no projected sandwich lift')
    C=[coeff[i*m:(i+1)*m] for i in range(m)]
    starts=[];index=0
    for basis in bases:starts.append(index);index+=len(basis)
    def block(i,j):
        return [[C[starts[i]+u][starts[j]+v] for v in range(len(bases[j]))]
                for u in range(len(bases[i]))]
    lines=[]
    for i,basis in enumerate(bases):
        j=0 if i else 1;B=block(i,j)
        if len(rref(B,A.F,len(bases[j]))[1])!=1:
            raise ValueError('cross-primary tensor is not rank one')
        col=next(v for v in range(len(bases[j])) if any(row[v] for row in B))
        line=[row[col] for row in B];lines.append(line)
    block_ranks=[element_rank(A,p)//A.t for p in pieces]
    anchor=next((i for i,size in enumerate(block_ranks) if size>=2),None)
    scaled=[None]*len(pieces)
    if anchor is not None:
        p=pieces[anchor];h=combination(A,lines[anchor],bases[anchor])
        domain=[A.mul(p,A.mul(x,p)) for x in A.basis]
        prediction=sum((project(A.mul(h,A.mul(x,h))) for x in domain),[])
        observed=sum((project(S(x)) for x in domain),[])
        index=next((i for i,x in enumerate(prediction) if x),None)
        if index is None:raise ValueError('the nonscalar component has no diagonal scale witness')
        gamma=A.F.mul(observed[index],A.F.inv(prediction[index]))
        if not gamma or observed!=[A.F.mul(gamma,x) for x in prediction]:
            raise ValueError('inconsistent diagonal sandwich scale')
        scalar=A.F.pow(gamma,A.F.q//2)
        scaled[anchor]=[A.F.mul(scalar,x) for x in lines[anchor]]
        scale_route='one nonscalar diagonal component and exact cross tensors'
    else:
        if len(pieces)<3 or any(len(b)!=1 for b in bases):
            raise ValueError('three scalar components required')
        p01=block(0,1)[0][0];p02=block(0,2)[0][0];p12=block(1,2)[0][0]
        if not p01 or not p02 or not p12:raise ValueError('vanishing cross-component scale')
        scaled[0]=[A.F.pow(A.F.mul(A.F.mul(p01,p02),A.F.inv(p12)),A.F.q//2)]
        anchor=0;scale_route='three scalar components and a square root'
    row=next(i for i,x in enumerate(scaled[anchor]) if x)
    for j in range(len(pieces)):
        if j==anchor:continue
        B=block(anchor,j)
        scaled[j]=[A.F.mul(x,A.F.inv(scaled[anchor][row])) for x in B[row]]
    for i in range(len(pieces)):
        for j in range(len(pieces)):
            if i!=j and block(i,j)!=[[A.F.mul(x,y) for y in scaled[j]] for x in scaled[i]]:
                raise ValueError('cross-primary tensors disagree after reconstruction')
    H=xor(combination(A,c,basis) for c,basis in zip(scaled,bases))
    if not A.is_unit(H):raise ValueError('recovered global sandwich is singular')
    if any(project(S(x))!=project(A.mul(H,A.mul(x,H))) for x in A.basis):
        raise ValueError('full projected source identity failed')
    return H,dict(component_matrix_sizes=block_ranks,component_ring_dimensions=list(map(len,bases)),
        tensor_unknowns=m*m,quotient_tensor_rank=rank,full_tensor_unique=(rank==m*m),
        scale_route=scale_route,all_projected_coefficients_verified=True)

def recover_arbitrary_operator_source_unit(A,P):
    C,E,U,meta=acquire_source_commutant_coset(A,P)
    pieces,bases,split=split_commutative_components(A,E);meta.update(split)
    if len(pieces)==1 and len(E)==A.t:
        # The preceding cyclic-primary proofs supply this already complete branch.
        radical=[A.pack(v) for v in relations([A.coordinates(P(x)) for x in A.basis],A.F)]
        if A.t%2 and len(radical)==1 and A.is_unit(radical[0]):
            unit=A.inv(radical[0]);meta['route']='odd-dimensional scalar radical'
            return unit,meta
        errors=[]
        for recover in (recover_source_unit,recover_primary_source_unit):
            try:
                unit,evidence=recover(A,P);meta.update(evidence);return unit,meta
            except ValueError as error:errors.append(str(error))
        raise ValueError('cyclic-primary unit recovery failed: '+'; '.join(errors))
    V,ranks=manufacture_coset_unit(A,pieces,U);Vinv=A.inv(V)
    S=reshuffle(A,lambda x:A.mul(P(A.mul(Vinv,x)),Vinv))
    if len(pieces)==1:H,more=recover_local_unit_sandwich(A,S,E)
    else:H,more=lift_global_sandwich(A,S,pieces,bases)
    unit=A.mul(H,V)
    if not A.is_unit(unit):raise ValueError('reconstructed source unit is singular')
    meta.update(more);meta.update(component_regular_ranks=ranks,
        route='multiplicative transport, manufactured CRT coset, and quotient sandwich')
    return unit,meta

def recover_from_raw_arbitrary_source(poly,algebra):
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
    return recover_arbitrary_operator_source_unit(A,P)

def count_arbitrary_square_source(poly,algebra):
    from operator_quadratic_counter import acquire_operator_linear_refinement
    from arbitrary_operator_hall import count_acquired_arbitrary_operator
    W,evidence=recover_from_raw_arbitrary_source(poly,algebra)
    inverse_unit=binary_solve(algebra.left_matrix(W),algebra.one)
    beta,D,phi,eta,fit=acquire_operator_linear_refinement(poly,algebra,inverse_unit)
    if not beta:raise ValueError('the general Lie route requires beta nonzero')
    gap,backend=count_acquired_arbitrary_operator(algebra,beta,D,phi,eta)
    fit.update(unit_acquisition=evidence,unit_acquisition_route=evidence['route'])
    return gap,backend,fit

def compile_raw_arbitrary_square(poly,n):
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
    if len(groups)!=1:raise ValueError('one acquired group must contain the quadratic source')
    group=next(iter(groups));local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    back=inverse([identity(d),algebra.Y,algebra.Z][group])
    source=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    gap,backend,evidence=count_arbitrary_square_source(source,algebra)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,seconds=time.perf_counter()-begun,
        supplied_unit_or_operator_decomposition=False,uniform_polynomial_time=False)
    return dict(original_bits=n,gap=gap,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,stats=stats)

if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    source=json.loads(args.source.read_text());result=compile_raw_arbitrary_square(source['anf'],source['n'])
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')
