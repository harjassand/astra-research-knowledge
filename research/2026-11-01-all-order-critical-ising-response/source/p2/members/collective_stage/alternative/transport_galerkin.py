"""A conventional local Ritz solve, with exact infinite-medium residual bounds.

No finite periodic environment is used.  The finite matrix is the orthogonal
projection of the infinite environment-seen-from-walker generator onto all
functions of bonds [-R,R-1].  Outside Bernoulli variables are integrated exactly.
The numerical solution is rounded to an explicitly rational trial function;
the final bracket is then computed with integer arithmetic on the one-site
enlarged support.  Float arithmetic only chooses the trial function.

Rates: tau_i flips at 1 + (tau_(i-1)+tau_(i+1)+tau_(i-1)tau_(i+1))/2.
Walker: right rate (1+tau_0)/2, left rate (1+tau_-1)/2.
The certified coefficient convention is D=lim E[X_t^2]/(2t).
"""

from __future__ import annotations

import json
import math
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla


def fwht(a):
    """Unnormalized Walsh transform; all copies deliberate for view safety."""
    a = np.array(a, copy=True)
    h = 1
    while h < len(a):
        z = a.reshape(-1, 2*h)
        left, right = z[:, :h].copy(), z[:, h:].copy()
        z[:, :h], z[:, h:] = left + right, left - right
        h *= 2
    return a


def projected_generator(radius):
    length = 2*radius
    n = 1 << length
    mask = n-1
    x = np.arange(n, dtype=np.int64)
    row, col, value = [], [], []
    diagonal = np.zeros(n)
    for b in range(length):
        left = 2*((x >> (b-1)) & 1)-1 if b else np.zeros(n)
        right = 2*((x >> (b+1)) & 1)-1 if b+1 < length else np.zeros(n)
        rate = 1+(left+right+left*right)/2
        diagonal += rate
        row.append(x)
        col.append(x ^ (1 << b))
        value.append(-rate)
    cr = ((x >> radius) & 1).astype(float)
    cl = ((x >> (radius-1)) & 1).astype(float)
    diagonal += cr+cl
    for bit in (0, 1):
        row.extend((x, x))
        col.extend(((x >> 1) | (bit << (length-1)), ((x << 1) & mask) | bit))
        value.extend((-cr/2, -cl/2))
    row.append(x)
    col.append(x)
    value.append(diagonal)
    k = sp.coo_matrix((np.concatenate(value), (np.concatenate(row), np.concatenate(col))), shape=(n, n)).tocsr()
    delta = k-k.T
    assert not delta.nnz or np.max(np.abs(delta.data)) == 0
    assert np.max(np.abs(k@np.ones(n))) == 0
    current = cr-cl
    return k, current


def rational_certificate(radius, integer_trial, fractional_bits):
    """Evaluate a *global* variational/residual interval with exact integers.

    K >= m D0, m=1/2. For trial u, q=2<j,u>-<u,Ku> and r=j-Ku:
    q <= chi <= q+2<r,D0^-1r>. Thus D=1/2-chi has the interval below.
    """
    length = 2*radius
    mask = (1 << length)-1
    width = length+2
    n = 1 << width
    index = np.arange(n, dtype=np.int64)
    base = (index >> 1) & mask
    u = integer_trial[base]
    knum = np.zeros(n, dtype=np.int64)
    for b in range(1, length+1):
        left = 2*((index >> (b-1)) & 1)-1
        right = 2*((index >> (b+1)) & 1)-1
        twice_rate = 2+left+right+left*right
        knum += twice_rate*(u-integer_trial[base ^ (1 << (b-1))])
    cr = (index >> (radius+1)) & 1
    cl = (index >> radius) & 1
    knum += 2*cr*(u-integer_trial[(index >> 2) & mask])
    knum += 2*cl*(u-integer_trial[index & mask])
    current = cr-cl
    scale = 1 << fractional_bits
    rnum = 2*scale*current-knum
    assert int(np.sum(rnum)) == 0
    # Python integer sums avoid overflow of squared fixed-point numerators.
    ju_sum = sum(int(a)*int(b) for a, b in zip(current, u))
    uku_sum = sum(int(a)*int(b) for a, b in zip(u, knum))
    q = Fraction(4*scale*ju_sum-uku_sum, n*2*scale*scale)
    rhat = fwht(rnum)
    assert rhat[0] == 0
    # The intermediate FWHT is safe at the tested widths and p=32; record its
    # largest integer size instead of silently relying on a fixed precision.
    # A conservative bound is n*max(abs(rnum)); require this below 2^63.
    assert n*max(abs(int(v)) for v in rnum) < (1 << 63)
    groups = [0]*(width+1)
    for i, coefficient in enumerate(rhat):
        groups[i.bit_count()] += int(coefficient)**2
    dual_norm = sum((Fraction(groups[k], 2*k) for k in range(1, width+1)), Fraction())
    dual_norm /= (2*scale*n)**2
    error = 2*dual_norm
    lower, upper = Fraction(1, 2)-q-error, Fraction(1, 2)-q
    return lower, upper, q, error, {
        "certificate_configurations": n,
        "residual_support_bonds": width,
        "max_integer_bits": max(abs(int(v)).bit_length() for v in rhat),
    }


def solve(radius, fractional_bits=32):
    begin = time.perf_counter()
    k, current = projected_generator(radius)
    n = len(current)
    eigen = np.array([2*i.bit_count() for i in range(n)], dtype=float)
    eigen[0] = math.inf
    pre = sla.LinearOperator(k.shape, matvec=lambda x: fwht(fwht(x)/eigen)/n)
    count = [0]
    def callback(_):
        count[0] += 1
    solution, info = sla.cg(k, current, M=pre, rtol=1e-13, atol=0, callback=callback)
    assert info == 0
    solution -= np.mean(solution)
    integer_trial = np.rint(solution*(1 << fractional_bits)).astype(np.int64)
    lower, upper, q, error, details = rational_certificate(radius, integer_trial, fractional_bits)
    record = {
        "radius": radius,
        "trial_bonds": 2*radius,
        "trial_space_dimension": n-1,
        "matrix_nonzeros": k.nnz,
        "cg_steps_for_trial": count[0],
        "fixed_point_bits": fractional_bits,
        "D_lower": float(lower),
        "D_upper": float(upper),
        "D_lower_rational": str(lower),
        "D_upper_rational": str(upper),
        "midpoint_relative_error_bound": float((upper-lower)/(upper+lower)),
        "residual_inverse_comparison_error": float(error),
        "elapsed_seconds": time.perf_counter()-begin,
        **details,
    }
    print(json.dumps(record), flush=True)
    return record


if __name__ == "__main__":
    records = [solve(radius) for radius in range(1, 7)]
    out = Path(__file__).with_name("transport_galerkin_results.json")
    out.write_text(json.dumps({"method": "local Ritz with exact global residual", "results": records}, indent=2)+"\n")
