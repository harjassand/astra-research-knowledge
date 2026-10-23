"""Exact integer matrix products using guarded signed int64 radix limbs.

Only NumPy int64 matmul performs products.  Every limb product has the explicit
absolute partial-sum bound k*(2**bits-1)**2 <= 2**63-1, so its signed arithmetic
cannot overflow.  Reconstruction uses Python arbitrary-precision integers.
Floating point is neither used nor accepted at this boundary.
"""
from __future__ import annotations

import numbers
import numpy as np

LIMIT = (1 << 63) - 1


def _integer_array(a, name):
    """Validate before conversion, including every entry in object arrays."""
    if not isinstance(a, np.ndarray) or a.ndim != 2:
        raise TypeError(f"{name} must be a two-dimensional NumPy array")
    if a.dtype == np.dtype(np.int64):
        return a
    if a.dtype != np.dtype(object):
        raise TypeError(f"{name} must have int64 or object-integer dtype")
    # Booleans are deliberately excluded despite Python's int subclass rule.
    if any(isinstance(v, (bool, np.bool_)) or not isinstance(v, numbers.Integral)
           for v in a.flat):
        raise TypeError(f"{name} object entries must all be integers, not bools")
    # np.int64 objects would overflow during a later object-array operation;
    # converting all entries to Python int is therefore part of the boundary.
    return np.fromiter((int(v) for v in a.flat), dtype=object,
                       count=a.size).reshape(a.shape)


def radix_bits(inner):
    """Largest radix width <=31 with a proved signed dot-product guard."""
    if not isinstance(inner, int) or isinstance(inner, bool) or inner < 0:
        raise ValueError("inner dimension must be a nonnegative Python int")
    if inner == 0:
        return 31
    if inner > LIMIT:
        raise OverflowError("inner dimension too large for even one-bit limbs")
    bits = min(31, (LIMIT // inner).bit_length() // 2)
    while bits > 0 and inner * ((1 << bits) - 1) ** 2 > LIMIT:
        bits -= 1
    while bits < 31 and inner * ((1 << (bits + 1)) - 1) ** 2 <= LIMIT:
        bits += 1
    if bits < 1:
        raise OverflowError("no safe radix")
    return bits


def _limbs(a, bits):
    """Signed magnitude limbs; INT64_MIN is handled in unsigned arithmetic."""
    if not a.size:
        return []
    mask = (1 << bits) - 1
    if a.dtype == np.dtype(np.int64):
        sign = np.where(a < 0, -1, 1).astype(np.int64)
        unsigned = a.astype(np.uint64)
        # Unsigned wrap is intentional only here: -uint(INT64_MIN)=2**63.
        magnitude = np.where(a < 0, np.uint64(0) - unsigned, unsigned)
        largest = int(magnitude.max())
        return [((magnitude >> shift) & np.uint64(mask)).astype(np.int64) * sign
                for shift in range(0, largest.bit_length(), bits)]
    sign = np.fromiter((-1 if v < 0 else 1 for v in a.flat), dtype=np.int64,
                       count=a.size).reshape(a.shape)
    magnitude = np.fromiter((abs(v) for v in a.flat), dtype=object,
                            count=a.size).reshape(a.shape)
    largest = max(magnitude.flat, default=0)
    return [np.asarray((magnitude >> shift) & mask, dtype=np.int64) * sign
            for shift in range(0, largest.bit_length(), bits)]


def exact_dot(a, b, *, return_info=False):
    """Return the exact matrix product as an object array of Python integers.

    Inputs must be 2D NumPy int64 arrays or object arrays of integer scalars.
    Already-overflowed caller data cannot be recovered: callers must establish
    their own input construction bounds before creating an int64 array.
    ``return_info`` optionally returns an arithmetic resource record as well.
    """
    a = _integer_array(a, "a")
    b = _integer_array(b, "b")
    if a.shape[1] != b.shape[0]:
        raise ValueError("inner dimensions do not match")
    inner = a.shape[1]
    bits = radix_bits(inner)
    aa, bb = _limbs(a, bits), _limbs(b, bits)
    out = np.zeros((a.shape[0], b.shape[1]), dtype=object)
    products = 0
    if aa and bb:
        # Horner reconstruction avoids repeatedly multiplying by wide powers.
        for degree in range(len(aa) + len(bb) - 2, -1, -1):
            if degree != len(aa) + len(bb) - 2:
                out *= 1 << bits
            for i in range(max(0, degree - len(bb) + 1), min(len(aa)-1, degree)+1):
                j = degree - i
                # Every partial sum is bounded by the sum of absolute products;
                # the guard applies irrespective of the multiplication order.
                product = aa[i] @ bb[j]
                out += product.astype(object)
                products += 1
    info = {
        "shape_a": list(a.shape), "shape_b": list(b.shape),
        "limb_bits": bits, "limbs_a": len(aa), "limbs_b": len(bb),
        "int64_dot_products": products,
        "absolute_partial_sum_bound": str(inner * ((1 << bits) - 1) ** 2),
        "int64_limit": str(LIMIT),
        "floating_point_used": False,
    }
    return (out, info) if return_info else out

