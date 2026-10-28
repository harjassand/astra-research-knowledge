"""Acquire inverse-dissipation residual bounds from finite scalar echoes.

The tail needs a warranted true-source bound ||A_i|| <= a_i < 1.
This implementation uses self-adjoint primitives and a positive definite
computational dissipation matrix; the theorem has a more general scope.
"""
from fractions import Fraction as F
from echo_compiler import bilinear_expr, add_expr, matvec, interval_expr
from uniform_certificate import mm, transpose, sub, scale, psd, dominate, diagonal


def powered_defect_expr(compiler, i, k, left, right):
    tl, tr = matvec(compiler.maps[i], left), matvec(compiler.maps[i], right)
    out = bilinear_expr(compiler.dictionary, left, (i,)*(2*k+2), right)
    add_expr(out, bilinear_expr(compiler.dictionary, left, (i,)*(2*k+1), tr), F(-1))
    add_expr(out, bilinear_expr(compiler.dictionary, tl, (i,)*(2*k+1), right), F(-1))
    add_expr(out, bilinear_expr(compiler.dictionary, tl, (i,)*(2*k), tr))
    return out


def required_words(dictionary, q, depth):
    from echo_compiler import echo_word
    return {echo_word(a, (i,)*k, b) for a in dictionary for b in dictionary
            for i in range(q) for k in range(2*depth+3)}


def acquire_dissipation_certificate(compiler, source_norm_bounds, depth, metric):
    if len(source_norm_bounds) != compiler.q:
        raise ValueError('One warranted source norm bound is required for every primitive')
    if type(depth) is not int or depth < 0:
        raise ValueError('Echo tail depth must be a nonnegative integer')
    w = metric
    if not psd(w, strict=True):
        raise ValueError('Positive computational metric required')
    r = compiler.r
    basis = [[F(i == j) for j in range(r)] for i in range(r)]
    theta2, q_upper, budgets = [], [], []
    for i, a in enumerate(source_norm_bounds):
        if not 0 <= a < 1:
            raise ValueError('A warranted strict source norm bound is required for this tail construction')
        budget = sub(w, mm(transpose(compiler.maps[i]), mm(w, compiler.maps[i])))
        if not psd(budget, strict=True):
            raise ValueError('This numerical proposal routine needs strictly positive computational dissipation')
        expressions = []
        for x in basis:
            row = []
            for y in basis:
                expr = {}
                for k in range(depth):
                    add_expr(expr, powered_defect_expr(compiler, i, k, x, y))
                add_expr(expr, powered_defect_expr(compiler, i, depth, x, y), 1/(1-a*a))
                row.append(interval_expr(expr, compiler.records))
            expressions.append(row)
        midpoint = [[x.center for x in row] for row in expressions]
        radii = [sum((x.radius for x in row), F(0)) for row in expressions]
        upper = [[midpoint[j][k]+(radii[j] if j == k else 0)
                  for k in range(r)] for j in range(r)]
        value = dominate(budget, upper)
        assert psd(sub(scale(budget, value), upper))
        theta2.append(value)
        q_upper.append(upper)
        budgets.append(budget)
    c = compiler.initial
    cwc = sum((x*y for x, y in zip(c, matvec(w, c))), F(0))
    return {"source_norm_bounds_are_premises": source_norm_bounds,
            "echo_tail_depth": depth, "metric": w,
            "computational_dissipation": budgets,
            "inverse_source_dissipation_residual_upper": q_upper,
            "per_action_theta_squared": theta2,
            "theta_squared": max(theta2),
            "signed_remainder_bound_all_words": 2*max(theta2)*cwc,
            "exact_psd_checks_passed": True}
