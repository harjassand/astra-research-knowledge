"""Exact-input residual certificates. Integer kernels are guarded before use.

No floating factorisation result, condition estimate, or solver status is
trusted here. Fractions denote mathematical rationals. Square-root enclosures
use integer square roots; all other error budgets are exact rational bounds.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import gzip
import hashlib
import operator
import platform
import resource
import time
import numpy as np
from scipy.sparse import csr_matrix, isspmatrix_csr

AI_BITS = 32
VI_BITS = 29
AD = 1 << AI_BITS
VD = 1 << VI_BITS
LIMIT = (1 << 63) - 1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value, name):
    require(not isinstance(value,(bool,np.bool_)), name+' must be an integer, not bool')
    try:
        return operator.index(value)
    except TypeError as exc:
        raise ValueError(name+' must be an exact integer') from exc


def integer_vector(values,name):
    out=[integer(x,name) for x in values]
    require(all(-LIMIT-1<=x<=LIMIT for x in out),name+' exceeds int64')
    return np.array(out,dtype=np.int64)


def validate_operator(ai,tau):
    require(isspmatrix_csr(ai) and ai.dtype==np.int64,
            'stored operator must be exact int64 CSR')
    require(ai.ndim==2 and ai.shape[0]==ai.shape[1] and ai.shape[0]>0,
            'nonempty square operator required')
    require(ai.has_canonical_format,'CSR must have sorted indices and no duplicates')
    require((ai!=ai.T).nnz==0,'stored operator must be exactly symmetric')
    tau=F(tau)
    require(tau>=0,'negative original-input error allowance')
    return tau


def fj(q):
    q = F(q)
    return {"numerator": str(q.numerator), "denominator": str(q.denominator)}


def jf(q):
    return F(int(q["numerator"]), int(q["denominator"]))


def sqrt_interval(q, bits=100):
    q = F(q)
    require(q >= 0, "negative square root")
    d = 1 << bits
    a = isqrt((q.numerator << (2 * bits)) // q.denominator)
    lo = F(a, d)
    if a * a * q.denominator == q.numerator * d * d:
        return lo, lo
    return lo, F(a + 1, d)


def sqrt_hi(q):
    return sqrt_interval(q)[1]


def up(q, bits=80):
    """Dyadic outward upper rounding keeps certificate fractions compact."""
    q = F(q)
    d = 1 << bits
    return F(-((-q.numerator * d) // q.denominator), d)


def round_fraction(q):
    """Nearest integer, ties upward. The tie rule is immaterial to validity."""
    q = F(q)
    return (2 * q.numerator + q.denominator) // (2 * q.denominator)


def squared_sum(a):
    return sum(int(v) ** 2 for v in np.asarray(a).ravel())


def rss_bytes():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(r if platform.system() == "Darwin" else r * 1024)


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_mm_exact(path):
    data = gzip.decompress(Path(path).read_bytes()).decode("ascii")
    lines = data.splitlines()
    require(lines[0].strip().lower() ==
            "%%matrixmarket matrix coordinate real symmetric",
            "only the specified symmetric coordinate Matrix Market format")
    body = [s.split() for s in lines[1:] if s.strip() and not s.startswith("%")]
    n, m, count = map(int, body[0])
    require(n == m and count == len(body) - 1, "dimension or entry count")
    entries = {}
    for line in body[1:]:
        require(len(line) == 3, "bad Matrix Market record")
        i, j = int(line[0]) - 1, int(line[1]) - 1
        require(0 <= j <= i < n, "expected lower symmetric triangle")
        require((i, j) not in entries, "duplicate source entry")
        entries[i, j] = F(line[2])
    return n, entries


def load_exact_generalized(source_dir):
    """A=M^{-1/2}KM^{-1/2}/scale, for exact stored decimal K,M.

    Interval rational square roots bind the dyadic surrogate to this original
    operator. The scale is a computed power of two; no physical model error is
    asserted. M must be strictly positive and diagonal.
    """
    t, c = time.perf_counter(), time.process_time()
    source_dir = Path(source_dir)
    kp, mp = source_dir / "bcsstk08.mtx.gz", source_dir / "bcsstm08.mtx.gz"
    n, ke = read_mm_exact(kp)
    n2, me = read_mm_exact(mp)
    require(n == n2 and len(me) == n and all(i == j for i, j in me),
            "companion mass matrix must be diagonal")
    mass = [me[i, i] for i in range(n)]
    require(all(x > 0 for x in mass), "mass must be strictly positive")
    row_upper = [F(0) for _ in range(n)]
    intervals = []
    for (i, j), kval in ke.items():
        lo, hi = sqrt_interval(mass[i] * mass[j])
        require(lo > 0, "mass square-root enclosure too coarse")
        if kval >= 0:
            a, b = kval / hi, kval / lo
        else:
            a, b = kval / lo, kval / hi
        intervals.append((i, j, a, b))
        z = max(abs(a), abs(b))
        row_upper[i] += z
        if i != j:
            row_upper[j] += z
    maxrow = max(row_upper)
    scale = 1
    while scale < maxrow:
        scale *= 2
    rows, cols, values = [], [], []
    tau_rows = [F(0) for _ in range(n)]
    absrows = [0] * n
    for i, j, a, b in intervals:
        a, b = a / scale, b / scale
        z = round_fraction((a + b) * AD / 2)
        require(abs(z) <= LIMIT, "matrix coefficient exceeds int64")
        err = max(abs(a - F(z, AD)), abs(b - F(z, AD)))
        rows.append(i); cols.append(j); values.append(z)
        absrows[i] += abs(z); tau_rows[i] += err
        if i != j:
            rows.append(j); cols.append(i); values.append(z)
            absrows[j] += abs(z); tau_rows[j] += err
    ai = csr_matrix((np.array(values, dtype=np.int64), (rows, cols)), shape=(n, n))
    ai.sort_indices()
    result = {
        "n": n, "source_nnz_symmetric": len(values), "source_triangle_entries": len(ke),
        "target": "M^(-1/2) K M^(-1/2) / scale; exact decimal source entries",
        "scale": str(scale), "A_denominator": str(AD),
        "tau": fj(up(max(tau_rows))), "M": fj(F(max(absrows), AD)),
        "max_integer_abs_row_sum": str(max(absrows)),
        "input_sha256": {kp.name: digest(kp), mp.name: digest(mp)},
        "construction_wall_seconds": time.perf_counter() - t,
        "construction_cpu_seconds": time.process_time() - c,
        "peak_rss_bytes": rss_bytes(),
    }
    return ai, result


def check_int64_dot_bounds(ai, vi, diagonal, offdiagonal=None):
    """Prove no partial integer accumulation can overflow in used products."""
    require(vi.dtype == np.int64 and vi.ndim == 2, "basis must be int64 matrix")
    n, k = vi.shape
    require(ai.shape == (n, n) and len(diagonal) == k, "incompatible dimensions")
    vi_abs = max((abs(int(x)) for x in vi.ravel()), default=0)
    a_rows = [sum(abs(int(x)) for x in ai.data[ai.indptr[i]:ai.indptr[i+1]])
              for i in range(n)]
    diag = [int(x) for x in diagonal]
    jj = [abs(x) for x in diag]
    if offdiagonal is not None:
        require(len(offdiagonal) == k-1, "bad subdiagonal size")
        for i, x in enumerate(offdiagonal):
            require(int(x) > 0, "irreducible positive Jacobi subdiagonal required")
            jj[i] += abs(int(x)); jj[i+1] += abs(int(x))
    av_bound = max(a_rows, default=0) * vi_abs
    vj_bound = max(jj, default=0) * vi_abs
    require(av_bound + vj_bound <= LIMIT, "residual accumulation may overflow")
    norms2 = [squared_sum(vi[:, j]) for j in range(k)]
    require(max(norms2, default=0) + VD * VD <= LIMIT,
            "Gram integer accumulation or diagonal subtraction may overflow")
    return F(max(a_rows, default=0), AD), F(max(jj, default=0), AD), norms2


def gram_budget(vi):
    g = vi.T @ vi
    g[np.diag_indices(g.shape[0])] -= VD * VD
    return sqrt_hi(F(squared_sum(g), VD ** 4))


def start_budget(vi0, gi, gd):
    """Exact upper bound for ||v_1-g/||g||||, no floating normalisation trust."""
    gg = F(squared_sum(gi), int(gd) ** 2)
    require(gg > 0, "zero probe")
    gl, gh = sqrt_interval(gg)
    require(gl > 0, "probe norm enclosure too coarse")
    vg = F(sum(int(x)*int(y) for x, y in zip(vi0, gi)), VD * int(gd))
    vv = F(squared_sum(vi0), VD**2)
    inner_lo = vg / gh if vg >= 0 else vg / gl
    ss = vv + 1 - 2 * inner_lo
    require(ss >= 0, "internal norm enclosure inconsistency")
    return sqrt_hi(ss), gg


def certify_krylov(ai, vi, diagonal, offdiagonal, gi, gd, tau):
    t, c = time.perf_counter(), time.process_time()
    tau=validate_operator(ai,tau)
    require(isinstance(vi,np.ndarray) and vi.dtype==np.int64 and vi.ndim==2,
            'basis must be an int64 matrix')
    diagonal = integer_vector(diagonal,'diagonal')
    offdiagonal = integer_vector(offdiagonal,'offdiagonal')
    n, k = vi.shape
    require(1 <= k <= n, "invalid Krylov dimension")
    require(isinstance(gi,np.ndarray) and gi.dtype==np.int64 and gi.shape==(n,),
            'probe must be an int64 vector matching the matrix')
    gd=integer(gd,'probe denominator')
    require(gd>0,'positive probe denominator required')
    m, kval, norms2 = check_int64_dot_bounds(ai, vi, diagonal, offdiagonal)
    gamma = gram_budget(vi)
    require(gamma < 1, "polar orthogonality condition fails")
    d = up(gamma / (1 + sqrt_interval(1-gamma)[0]))
    av = ai @ vi
    vj = vi * diagonal[None, :]
    if k > 1:
        vj[:, 1:] += vi[:, :-1] * offdiagonal[None, :]
        vj[:, :-1] += vi[:, 1:] * offdiagonal[None, :]
    residual = av[:, :-1] - vj[:, :-1]
    r0 = sqrt_hi(F(squared_sum(residual), (AD*VD)**2))
    r = up(r0 + (m + kval) * d) if k > 1 else F(0)
    last_quad = F(sum(int(x)*int(y) for x,y in zip(vi[:, -1], av[:, -1])),
                  AD * VD**2)
    xi = abs(F(int(diagonal[-1]), AD) - last_quad)
    z = up(xi + m*d*(1 + sqrt_hi(1+gamma)))
    completion = up((z + 2*sqrt_hi(z*z+3*r*r))/3)
    start0, probe_norm2 = start_budget(vi[:, 0], gi, gd)
    out = {key: fj(value) for key, value in dict(
        gamma=gamma, polar_distance=d, M=m, K=kval, r0=r0, r=r,
        xi=xi, z=z, completion_error=completion, tau=F(tau),
        operator_error=F(tau)+completion, start0=start0,
        start_error=min(F(1),start0+d), probe_norm2=probe_norm2).items()}
    out.update(n=n,k=k,basis_denominator=str(VD),matrix_denominator=str(AD),
               wall_seconds=time.perf_counter()-t,cpu_seconds=time.process_time()-c,
               peak_rss_bytes=rss_bytes(),
               integer_overflow_guards_passed=True)
    return out


def certify_dense(ai, vi, diagonal, tau):
    """Full ordinary eigendecomposition, independently verified by residuals."""
    t, c = time.perf_counter(), time.process_time()
    tau=validate_operator(ai,tau)
    n = ai.shape[0]
    require(isinstance(vi,np.ndarray) and vi.dtype==np.int64 and vi.shape == (n,n),
            "full square int64 eigenbasis required")
    diagonal = integer_vector(diagonal,'diagonal')
    m,kval,_ = check_int64_dot_bounds(ai,vi,diagonal)
    gamma = gram_budget(vi)
    require(gamma<1,"full eigenbasis polar condition fails")
    d = up(gamma/(1+sqrt_interval(1-gamma)[0]))
    res = ai@vi - vi*diagonal[None,:]
    r0 = sqrt_hi(F(squared_sum(res),(AD*VD)**2))
    polar_error = F(tau)+r0+(m+kval)*d
    sorted_residual_error = F(tau)+up(r0/sqrt_interval(1-gamma)[0])
    error = min(polar_error,sorted_residual_error)
    return dict(n=n,gamma=fj(gamma),polar_distance=fj(d),r0=fj(r0),
                operator_error=fj(error),tau=fj(tau),M=fj(m),K=fj(kval),
                polar_error=fj(polar_error),sorted_residual_error=fj(sorted_residual_error),
                wall_seconds=time.perf_counter()-t,cpu_seconds=time.process_time()-c,
                peak_rss_bytes=rss_bytes(),integer_overflow_guards_passed=True)
