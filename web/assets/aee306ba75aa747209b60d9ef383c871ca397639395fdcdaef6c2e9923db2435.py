"""Finite computations for the Werner endpoint. No numerical run proves all-copy positivity."""
from __future__ import annotations
from numbers import Integral
import numpy as np
from numpy.typing import NDArray


def partial_trace(a: NDArray, dims: tuple[int, ...], traced: tuple[int, ...]) -> NDArray:
    """Contract matching row/column tensor slots, retaining their original order."""
    if a.shape != (int(np.prod(dims)),) * 2:
        raise ValueError('Matrix shape and tensor dimensions disagree.')
    t = a.reshape(dims + dims)
    left = list(dims)
    for i in sorted(traced, reverse=True):
        if not 0 <= i < len(left):
            raise ValueError('Invalid trace slot.')
        t = np.trace(t, axis1=i, axis2=i+len(left))
        left.pop(i)
    outdim = int(np.prod(left)) if left else 1
    return np.asarray(t).reshape(outdim, outdim)


def endpoint_action(a: NDArray, dims: tuple[int, ...]) -> NDArray:
    """Apply the commuting Hilbert--Schmidt operators I - (1/2) Tr_i(.) tensor I_i."""
    n = len(dims)
    out = a.reshape(dims + dims).copy()
    for i, d in enumerate(dims):
        perm = [i, n+i] + [j for j in range(2*n) if j not in (i, n+i)]
        inv = np.argsort(perm)
        v = out.transpose(perm)
        tr = np.trace(v, axis1=0, axis2=1)
        correction = np.eye(d).reshape((d,d)+(1,)*(2*n-2)) * tr
        out = (v - 0.5*correction).transpose(inv)
    return out.reshape(a.shape)


def endpoint(a: NDArray, dims: tuple[int, ...]) -> float:
    return float(np.vdot(a, endpoint_action(a, dims)).real)


def endpoint_numerator(a: NDArray, dims: tuple[int, ...]) -> int:
    """Return exactly 2**n*q_n(a) for a matrix of Python integer entries."""
    a = np.asarray(a, dtype=object)
    if any(not isinstance(x, Integral) for x in a.flat):
        raise TypeError('Exact evaluation requires integer entries, without rounding.')
    n = len(dims)
    total = 0
    for mask in range(1 << n):
        traced = tuple(i for i in range(n) if (mask >> i) & 1)
        t = partial_trace(a, dims, traced)
        norm2 = sum(int(x)*int(x) for x in t.flat)
        total += (-1)**len(traced) * 2**(n-len(traced))*norm2
    return int(total)


def swap_metric_numerator(z: NDArray, dims: tuple[int, ...]) -> int:
    """Exactly evaluate z^T [tensor_i (2I-F_i)] z using integer arithmetic."""
    n = len(dims)
    z = np.asarray(z, dtype=object).reshape(dims+dims)
    if any(not isinstance(x, Integral) for x in z.flat):
        raise TypeError('Exact evaluation requires integer entries, without rounding.')
    out = z.copy()
    for i in range(n):
        out = 2*out - out.swapaxes(i,n+i)
    return int(sum(int(a)*int(b) for a,b in zip(z.flat, out.flat)))
