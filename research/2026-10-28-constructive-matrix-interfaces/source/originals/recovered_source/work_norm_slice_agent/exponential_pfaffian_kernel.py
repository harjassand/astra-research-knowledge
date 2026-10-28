#!/usr/bin/env python3
"""Uniform polynomial reconstruction of L_(t,a)(p_d^j).

The exponential alphabet is virtual: p_d(X)=d*z^d and p_r(X)=0 for r!=d.
No distinct field elements, matrix assignments or partitions are enumerated.
Its Jacobi--Trudi coefficients are (q^d-1)^j*z^(dj)/j!; final coefficient
normalization by j! restores the exact integral polynomial.
"""
from cyclic_primary_pfaffian import kernel_primary_boundary,cyclic_primary_weights


def exponential_kernel(t,q,boundary=1,d=1,maximum=None):
    return kernel_primary_boundary(t,d,boundary,q,maximum,power_sum=True)


def exponential_kernel_refined(t,q,d=1):
    return cyclic_primary_weights(t,d,q,True,power_sum=True)


def involution_numbers(n):
    out=[1]
    for c in range(1,n+1):out.append(out[-1]+((c-1)*out[-2] if c>1 else 0))
    return out
