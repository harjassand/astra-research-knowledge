#!/usr/bin/env python3
"""Acquire a common bilinear split directly from binary quadratic forms.

No distinguished source, input decomposition, field or matrix units are
accepted.  The joint adjoint equations and their ordinary center manufacture
two complementary isotropic spaces.  A shared affine shift is solved exactly.
Matrices are lists of columns throughout; integers encode binary vectors.
"""
from pathlib import Path
import sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from central_quadratic_tensor_compiler import (pack,unpack,product,transpose,
    polar_rows,affine_solutions,apply_binary,linear_kernel,independent_basis,
    compose_quadratic,binary_rows)


class Coordinates:
    def __init__(self,basis):
        self.basis=list(basis);self.pivots={}
        for i,value in enumerate(self.basis):
            label=1<<i
            while value:
                p=value.bit_length()-1
                if p in self.pivots:
                    row,word=self.pivots[p];value^=row;label^=word
                else:
                    self.pivots[p]=(value,label);break
            else:raise ValueError('dependent coordinate basis')
    def __call__(self,value):
        answer=0
        while value:
            p=value.bit_length()-1
            if p not in self.pivots:raise ValueError('value outside acquired span')
            row,word=self.pivots[p];value^=row;answer^=word
        return answer


def sparse_kernel(rows,unknowns):
    """Kernel of a streamed binary row system; no dense equation table."""
    pivots={};equations=reductions=0
    for value in rows:
        if type(value) is not int or value<0 or value.bit_length()>unknowns:
            raise ValueError('invalid binary equation row')
        equations+=1
        while value:
            p=value.bit_length()-1
            if p in pivots:value^=pivots[p];reductions+=1
            else:pivots[p]=value;break
    kernel=[]
    ordered=sorted(pivots)
    for free in range(unknowns):
        if free in pivots:continue
        value=1<<free
        for p in ordered:
            if (pivots[p]&value).bit_count()%2:value^=1<<p
        kernel.append(value)
    return kernel,dict(unknowns=unknowns,equations_streamed=equations,
        independent_equations=len(pivots),row_reductions=reductions,
        kernel_dimension=len(kernel),dense_equation_table_constructed=False)


def acquire_source_free_bilinear_split(quadratics,n,require_shared_center=True,
        allow_paired_components=False):
    """Return exact cross forms and their original affine coordinate map.

    cross_matrices[i] has right_dimension columns of left_dimension bits.
    For z=(u,v), the original x is affine_offset+coordinate_columns*z,
    and marked output i is output_constant[i]+u^T cross_matrices[i] v.
    The implementation declines when its acquired polar-center certificate
    fails. By default it also requires one common affine bilinear center.
    With require_shared_center=False it exposes residual left/right linear
    output columns when that shared affine center does not exist; no linear
    term is dropped, and shared_affine_center_acquired records the outcome.
    With allow_paired_components=True, refine central Boolean atoms and select
    the larger actual image in every adjoint-exchanged pair. Ties use packed
    matrices. This is one checked orientation, not a completeness claim.
    """
    begun=time.perf_counter()
    if type(n) is not int or n<1:raise ValueError('positive original input count required')
    quadratics=[set(f) for f in quadratics]
    if not quadratics or any(type(m) is not int or m<0 or m.bit_length()>n or
            m.bit_count()>2 for f in quadratics for m in f):
        raise ValueError('explicit binary quadratics required')
    polars=[polar_rows(f,n) for f in quadratics]
    if len(independent_basis(row for B in polars for row in B))!=n:
        raise ValueError('common original polar radical is nonzero')
    width=n*n
    # Entry (a,b): (L^T B)[a,b] = (B R)[a,b].  B is symmetric.
    rows=((B[b]<<(n*a))^(B[a]<<(width+n*b))
        for B in polars for a in range(n) for b in range(n))
    pairs,linear_metadata=sparse_kernel(rows,2*width)
    mask=(1<<width)-1
    algebra=[value&mask for value in pairs]
    partners=[value>>width for value in pairs]
    co=Coordinates(algebra)
    if len(independent_basis(algebra))!=len(pairs):
        raise AssertionError('joint-adjoint left projection is not injective')
    star=[co(value) for value in partners]
    if any(apply_binary(star,x)!=(1<<j) for j,x in enumerate(star)):
        raise AssertionError('joint-adjoint swap is not an involution')
    matrices=[unpack(value,n) for value in algebra]
    for L,value in zip(matrices,partners):
        R=unpack(value,n)
        if any(product(transpose(L),B)!=product(B,R) for B in polars):
            raise AssertionError('acquired joint adjoint violates an original polar')
    identity=pack([1<<i for i in range(n)],n)
    if apply_binary(partners,co(identity))!=identity:
        raise AssertionError('joint-adjoint identity has wrong partner')

    # Shrinking centralizer intersections avoid a k^2*n^2 commutator table.
    center=algebra[:];center_dimensions=[len(center)]
    for G in matrices:
        images=[pack(product(unpack(z,n),G),n)^pack(product(G,unpack(z,n)),n)
            for z in center]
        center=[apply_binary(center,c) for c in linear_kernel(images,width)]
        center_dimensions.append(len(center))
    center_co=Coordinates(center)
    squares=[pack(product(unpack(z,n),unpack(z,n)),n) for z in center]
    for z in squares:center_co(z)
    if len(independent_basis(squares))!=len(center):
        raise ValueError('ordinary adjoint center has noninjective Frobenius')
    fixed_coordinates=linear_kernel([square^z for square,z in zip(squares,center)],width)
    idempotents=[apply_binary(center,c) for c in fixed_coordinates]
    component_pairs=[]
    if allow_paired_components:
        atoms=[identity]
        for e in idempotents:
            refined=[]
            for f in atoms:
                z=pack(product(unpack(e,n),unpack(f,n)),n)
                if z:refined.append(z)
                if z^f:refined.append(z^f)
            atoms=refined
        if len(atoms)!=len(idempotents):raise AssertionError('central Boolean refinement failed')
        remaining=set(atoms);value=0
        while remaining:
            e=min(remaining);f=apply_binary(partners,co(e))
            if f==e or f not in remaining:
                raise ValueError('central atoms do not form adjoint-exchanged pairs')
            erank=len(independent_basis(unpack(e,n)));frank=len(independent_basis(unpack(f,n)))
            chosen=e if (erank,e)>=(frank,f) else f
            value^=chosen;remaining.remove(e);remaining.remove(f)
            component_pairs.append(dict(first_rank=erank,second_rank=frank,
                selected_rank=max(erank,frank),tie=erank==frank))
    else:
        if len(idempotents)!=2:
            raise ValueError('ordinary adjoint center does not have two Boolean atoms')
        value=next((z for z in idempotents if z and z!=identity),None)
        if value is None:raise AssertionError('two-atom center has no proper idempotent')
    E=unpack(value,n);F=unpack(value^identity,n)
    E_star=unpack(apply_binary(partners,co(value)),n)
    if product(E,E)!=E or E_star!=F:
        raise ValueError('central idempotents are not adjoint exchanged')
    U=independent_basis(E);V=independent_basis(F);columns=U+V
    left=len(U);right=len(V)
    if not left or not right or left+right!=n or len(independent_basis(columns))!=n:
        raise AssertionError('acquired isotropic spaces do not give bijective coordinates')
    if any((u&apply_binary(B,v)).bit_count()%2 for B in polars
            for space in (U,V) for u in space for v in space):
        raise AssertionError('a common acquired half is not isotropic')

    local=[compose_quadratic(f,0,columns) for f in quadratics]
    centering=[]
    for f in local:
        B=polar_rows(f,n)
        centering.extend((row,int(1<<j in f)) for j,row in enumerate(B))
    solution=affine_solutions(centering,n)
    if solution is None and require_shared_center:
        raise ValueError('marked forms do not have a shared affine bilinear center')
    if solution is not None and solution[1]:
        raise AssertionError('shared affine center is not unique despite zero common radical')
    offset=apply_binary(columns,solution[0]) if solution is not None else 0
    centered=[compose_quadratic(f,offset,columns) for f in quadratics]
    if solution is not None and any(m.bit_count()==1 for f in centered for m in f):
        raise AssertionError('shared affine centering left a linear monomial')
    cross_rows=[]
    for f in centered:
        H=[0]*left
        for monomial in f:
            if monomial==0 or monomial.bit_count()==1:continue
            low=monomial&((1<<left)-1);high=monomial>>left
            if low.bit_count()!=1 or high.bit_count()!=1:
                raise AssertionError('acquired polar split left a noncross quadratic monomial')
            H[low.bit_length()-1]^=high
        cross_rows.append(H)
    cross_columns=[binary_rows(H,right) for H in cross_rows]
    return dict(input_bits=n,marked_quadratics=len(quadratics),
        left_dimension=left,right_dimension=right,
        coordinate_columns=columns,affine_offset=offset,
        output_constant=sum(int(0 in f)<<i for i,f in enumerate(centered)),
        cross_matrices=cross_columns,cross_rows=cross_rows,
        centered_quadratics=[sorted(f) for f in centered],
        shared_affine_center_acquired=solution is not None,
        left_linear_output_columns=[sum(int(1<<j in f)<<i for i,f in enumerate(centered))
            for j in range(left)],
        right_linear_output_columns=[sum(int(1<<(left+j) in f)<<i for i,f in enumerate(centered))
            for j in range(right)],
        joint_polar_radical_dimension=0,
        joint_adjoint_algebra_dimension=len(algebra),
        ordinary_center_dimension=len(center),
        ordinary_center_frobenius_rank=len(squares),
        central_idempotent_dimension=len(idempotents),
        adjoint_component_pairs=component_pairs,
        dimension_oriented_paired_components=allow_paired_components,
        central_idempotent_columns=E,adjoint_of_idempotent_columns=E_star,
        adjoint_involution_verified=True,all_marked_halves_isotropic=True,
        center_candidate_dimensions=center_dimensions,linear_acquisition=linear_metadata,
        supplied_source_or_decomposition=False,field_or_matrix_units_constructed=False,
        original_assignments_enumerated=0,seconds=time.perf_counter()-begun)
