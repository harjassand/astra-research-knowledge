#!/usr/bin/env python3
"""Raw exact counting with two independently acquired invariant sources.

Accepted raw sources on two matrix groups are
Tr(beta e2(DX))+phi(tr(DX)), beta!=0, D invertible, phi Boolean quadratic.
The two distinguished units need not commute or satisfy compatibility.
The third matrix group has no nonconstant source. All original inputs
remain free. No matrix units, group partition, or source unit is supplied.
"""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_matrix_root'))
from invariant_quadratic_scalar_gauss import (
    Field, polynomial_value, two_scalar_matrix_gaussians)
from invariant_quadratic_matrix import fit_invariant_quadratic, quadratic_anf
from raw_matrix_trace import (hidden_groups, AcquiredMatrixAlgebra,
                              acquire_center, identity, inverse, bits,
                              linear_apply)


def gaussian_rows(n, q):
    """All binary-Gaussian rows via polynomially many exact integer steps."""
    rows = [[1]]
    for r in range(1, n + 1):
        previous = rows[-1]
        rows.append([1] + [previous[j - 1] + q ** j * previous[j]
                           for j in range(1, r)] + [1])
    return rows


def weighted_nullity_distribution(t, q, J):
    """A_h=sum_{nullity X=h} sign(source(X)), from invariant J_r."""
    if len(J) != t + 1:
        raise ValueError('need Gauss layers 0 through matrix size')
    rows = gaussian_rows(t, q)
    A = [0] * (t + 1)
    for h in range(t, -1, -1):
        fixed_kernel_total = rows[t][h] * q ** (h * (t - h)) * J[t - h]
        A[h] = fixed_kernel_total - sum(rows[u][h] * A[u] for u in range(h + 1, t + 1))
    return A


def two_invariant_gap(t, field_h, source_x, source_y):
    """Gap of Tr tr(XYZ)+Qx(X)+Qy(Y), after unit normalization."""
    F = Field(field_h)
    beta_x, phi_x = source_x
    beta_y, phi_y = source_y
    Jx, data_x = two_scalar_matrix_gaussians(t, field_h, beta_x, phi_x)
    Jy, data_y = two_scalar_matrix_gaussians(t, field_h, beta_y, phi_y)
    A = weighted_nullity_distribution(t, F.q, Jx)
    normalized = sum(A[h] * F.q ** (h * (t - h)) * Jy[h] for h in range(t + 1))
    gap = normalized * F.q ** (t * t)
    return gap, dict(route='two invariant sources, exact nullity incidence inversion',
                     matrix_size=t, field_degree=F.a, field_modulus=field_h,
                     source_x=data_x, source_y=data_y,
                     source_x_matrix_gaussians=Jx, source_y_matrix_gaussians=Jy,
                     source_x_weighted_nullities=A, enumerated_subspaces=0,
                     enumerated_field_elements=0, enumerated_original_assignments=0,
                     uniform_polynomial_time=True)


def compile_raw_two_invariant_quadratics(poly, n):
    begun = time.perf_counter()
    poly = set(poly)
    if type(n) is not int or n <= 0 or any(type(m) is not int or m < 0 or
            m.bit_length() > n or m.bit_count() > 3 for m in poly):
        raise ValueError('raw cubic Boolean ANF required')
    grouped, slices, group_map, stats = hidden_groups(poly, n)
    algebra = AcquiredMatrixAlgebra(slices)
    d = algebra.d
    centered, offset = acquire_center(grouped, slices, d, allow_within=True)
    lower = [m for m in centered if 0 < m.bit_count() <= 2]
    groups = sorted({i // d for m in lower for i in bits(m)})
    if len(groups) != 2:
        raise ValueError('this branch requires nonconstant sources on exactly two groups')
    if any(len({i // d for i in bits(m)}) != 1 for m in lower):
        raise ValueError('mixed quadratic survived affine centering')
    maps = [identity(d), algebra.Y, algebra.Z]
    sources = []
    acquisition = []
    for number, group in enumerate(groups):
        local = {m >> (group * d) for m in lower
                 if next(bits(m)) // d == group}
        if number == 0 and 0 in centered:
            local.add(0)
        back = inverse(maps[group])
        source = quadratic_anf(lambda x: polynomial_value(local, linear_apply(back, x)), d)
        beta, phi, evidence = fit_invariant_quadratic(source, algebra)
        sources.append((beta, phi))
        acquisition.append(dict(group=group, beta=beta, trace_quadratic_anf=sorted(phi),
                                **evidence))
    gap, backend = two_invariant_gap(algebra.t, algebra.h, *sources)
    if abs(gap) > 1 << n or gap % 2:
        raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats)
    stats.update(raw_monomials=len(poly), affine_offset=offset,
                 quadratic_groups=groups, source_acquisitions=acquisition,
                 backend=backend, full_coefficient_identity_verified=True,
                 supplied_unit_or_matrix_coordinates=False,
                 seconds=time.perf_counter() - begun)
    return dict(original_bits=n, zeros=((1 << n) + gap) // 2,
                ones=((1 << n) - gap) // 2, gap=gap, stats=stats)
