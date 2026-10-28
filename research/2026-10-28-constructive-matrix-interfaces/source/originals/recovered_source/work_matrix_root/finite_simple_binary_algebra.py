#!/usr/bin/env python3
"""Binary certificates of a full matrix algebra over a manufactured center.

No canonical finite field or explicit matrix-algebra isomorphism is used.
The sandwich map is checked in the actual multiplication table.
"""
from adjoint_matrix_product_counter import (BinaryCoordinates,pack,unpack,product,
    apply_binary,linear_kernel,independent_basis,affine_solutions,isqrt)


def certify_finite_simple_matrix_algebra(packed_matrices,representation_dimension):
    D=representation_dimension;S=BinaryCoordinates(packed_matrices);K=len(S.basis)
    if not K:raise ValueError('zero algebra')
    unit=S.coordinates(pack([1<<i for i in range(D)],D))
    decoded=[unpack(x,D) for x in S.basis]
    multiplication=[[S.coordinates(pack(product(A,B),D)) for B in decoded] for A in decoded]
    def multiply(a,b):return apply_binary([apply_binary(row,b) for row in multiplication],a)
    center_images=[sum((multiplication[i][j]^multiplication[j][i])<<(K*j)
        for j in range(K)) for i in range(K)]
    center=linear_kernel(center_images,K*K);a=len(center)
    Z=BinaryCoordinates(center);frobenius=[Z.coordinates(multiply(z,z)) for z in center]
    if len(independent_basis(frobenius))!=a or len(linear_kernel(
        [z^(1<<i) for i,z in enumerate(frobenius)],a))!=1:
        raise ValueError('acquired center is not a field')
    if K%a:raise ValueError('inconsistent central dimension')
    p=isqrt(K//a)
    if a*p*p!=K or D%(a*p):raise ValueError('algebra has no integral matrix/module dimensions')
    sandwich=BinaryCoordinates()
    for i in range(K):
        for j in range(K):
            right=[multiplication[k][j] for k in range(K)]
            sandwich.insert(pack([apply_binary(right,multiplication[i][k]) for k in range(K)],K))
    if len(sandwich.basis)!=K*K//a:
        raise ValueError('sandwich span does not fill the center-linear endomorphism algebra')
    return dict(basis=S.basis,representation_dimension=D,dimension=K,
        unit_coordinates=unit,multiplication_table=multiplication,center_basis=center,
        center_dimension=a,center_frobenius_columns=frobenius,
        center_frobenius_injective=True,center_frobenius_fixed_dimension=1,
        field_degree=a,matrix_degree=p,module_multiplicity=D//(a*p),
        sandwich_span_dimension=len(sandwich.basis),sandwich_space_dimension=K*K//a,
        canonical_field_or_matrix_isomorphism_constructed=False)
