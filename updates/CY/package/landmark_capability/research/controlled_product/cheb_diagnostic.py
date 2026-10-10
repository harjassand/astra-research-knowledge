"""Floating diagnostic for the two-level Chebyshev state compiler.

All F_b values here come from explicit 2^3-state uniformization.  This does
not implement the claimed finite-bit large-n marked-CDF primitive, nor does
it certify node rounding or interpolation errors.  It checks the algebraic
acquisition formula and product-state reconstruction on a small instance.
"""

from __future__ import annotations

import json
import math

from demo import (INITIAL, N, STAGES, TARGETS, age_kernel, killed_evolve,
                  marked_cdf, mixture_vector, product_vector)


def poly_mul_linear(poly, root):
    result = [0.0] * (len(poly) + 1)
    for j, coeff in enumerate(poly):
        result[j] -= root * coeff
        result[j + 1] += coeff
    return result


def poly_add_scaled(out, poly, scale):
    for j, value in enumerate(poly):
        out[j] += scale * value


def poly_eval(poly, x):
    value = 0.0
    for coeff in reversed(poly):
        value = value * x + coeff
    return value


def poly_derivative(poly):
    return [j * poly[j] for j in range(1, len(poly))]


def poly_mul(a, b):
    out = [0.0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def integrate_minus_one_to_one(poly):
    return sum(2.0 * coeff / (j + 1) for j, coeff in enumerate(poly)
               if j % 2 == 0)


def cheb_lagrange(degree):
    nodes = [math.cos(math.pi * j / degree) for j in range(degree + 1)]
    basis = []
    for j in range(degree + 1):
        poly = [1.0]
        den = 1.0
        for k, x in enumerate(nodes):
            if k == j:
                continue
            poly = poly_mul_linear(poly, x)
            den *= nodes[j] - x
        basis.append([a / den for a in poly])
    return nodes, basis


def balanced_cells(T, tau):
    if T <= 2 * tau:
        return []
    out = []
    a = tau
    while a < T - tau - 1e-13:
        b = min(a + 0.25 * min(a, T - a), T - tau)
        if b <= a:
            raise ArithmeticError("balanced age grid stalled")
        out.append((a, b))
        a = b
    return out


def run(degree, cdf_degree, tau=0.01):
    p, lam, T = STAGES[0]
    incoming = product_vector(INITIAL)
    true = killed_evolve(incoming, p, lam, T)
    cells = balanced_cells(T, tau)
    d_nodes, d_basis = cheb_lagrange(degree)
    q_nodes, q_basis = cheb_lagrange(cdf_degree)
    cdf_cache = {}

    def F(t):
        if t not in cdf_cache:
            cdf_cache[t] = marked_cdf(incoming, p, lam, t)
        return cdf_cache[t]

    F0 = F(0.0)
    propagated_q = tuple(p[i] + (INITIAL[i] - p[i]) *
                         math.exp(-lam[i] * T) for i in range(N))
    components = [(1.0, propagated_q)]
    for j, b in enumerate(TARGETS):
        components.append((-F0[j], age_kernel(b, T, p, lam)))

    for a, b_age in cells:
        center = (a + b_age) / 2.0
        halfwidth = (b_age - a) / 2.0
        f_nodes = [F(T - center - halfwidth * x) for x in q_nodes]
        left = F(T - a)
        right = F(T - b_age)
        for target_j, target in enumerate(TARGETS):
            f_poly = [0.0] * (cdf_degree + 1)
            for j, lag in enumerate(q_basis):
                poly_add_scaled(f_poly, lag, f_nodes[j][target_j] - F0[target_j])
            for j, lag in enumerate(d_basis):
                coeff = (poly_eval(lag, -1.0) *
                         (left[target_j] - F0[target_j]) -
                         poly_eval(lag, 1.0) *
                         (right[target_j] - F0[target_j]) +
                         integrate_minus_one_to_one(
                             poly_mul(poly_derivative(lag), f_poly)))
                age_node = center + halfwidth * d_nodes[j]
                components.append((-coeff, age_kernel(target, age_node, p, lam)))

    compiled = mixture_vector(components)
    f_tau, f_T, f_before_terminal = F(tau), F(T), F(T - tau)
    omitted_edge_mass = sum(
        f_tau[j] - F0[j] + f_T[j] - f_before_terminal[j]
        for j in range(len(TARGETS))
    )
    return {
        "kernel_degree": degree,
        "cdf_degree": cdf_degree,
        "omitted_edge_width": tau,
        "balanced_cells": len(cells),
        "marked_cdf_times": len(cdf_cache),
        "product_terms": len(components),
        "coefficient_l1": sum(abs(c) for c, _ in components),
        "state_l1_error": sum(abs(x - y) for x, y in zip(compiled, true)),
        "omitted_edge_hit_mass": omitted_edge_mass,
        "survival_mass": sum(true),
        "compiled_mass": sum(compiled),
    }


if __name__ == "__main__":
    print(json.dumps({
        "coarse": run(4, 6, tau=0.01),
        "fine": run(7, 11, tau=0.001),
    }, indent=2))
