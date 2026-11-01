"""Conventional certified Ritz/CG solver for local product-equilibrium kinetics.

No full configurations, trajectory, truncation of coefficients, or assumed rank
is used by the dictionary backend. A dictionary key is an exact Walsh support.
The certificate is mathematical in exact arithmetic; printed floating-point
intervals are numerical evidence, not outward-rounded interval arithmetic.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


def dot(a, b):
    if len(a) > len(b):
        a, b = b, a
    return math.fsum(v * b.get(s, 0.0) for s, v in a.items())


def axpy(a, alpha, b):
    out = dict(a)
    for s, v in b.items():
        z = out.get(s, 0.0) + alpha * v
        if z == 0.0:
            out.pop(s, None)
        else:
            out[s] = z
    return out


def scaled(a, alpha):
    return {s: alpha * v for s, v in a.items() if alpha * v != 0.0}


class ProductFlipModel:
    """K chi_S=2 sum_{i in S} nu_i sum_B a_iB chi_{S xor B}.

    rates[i] encodes A_i = sum_B a_iB chi_B, with i not in B.
    Positive supplied pointwise bounds m <= A_i <= M are independently checked
    on every local truth table when validate=True.
    """

    def __init__(self, clocks, rates, m, M, validate=True):
        self.clocks = tuple(float(v) for v in clocks)
        self.n = len(self.clocks)
        self.rates = tuple(tuple((int(s), float(v)) for s, v in terms) for terms in rates)
        self.m, self.M = float(m), float(M)
        self.lam_cache = {}
        self.columns = {}
        self.column_entries = 0
        if self.m <= 0 or self.M < self.m or min(self.clocks) <= 0:
            raise ValueError("positive clocks and ellipticity are required")
        if len(self.rates) != self.n:
            raise ValueError("one rate polynomial per spin")
        if validate:
            self.validate_rates()

    def validate_rates(self):
        attained = [math.inf, -math.inf]
        for i, terms in enumerate(self.rates):
            union = 0
            for mask, _ in terms:
                if mask & (1 << i):
                    raise ValueError("A_i depends on flipped spin")
                union |= mask
            sites = [j for j in range(self.n) if union & (1 << j)]
            if len(sites) > 20:
                raise ValueError("rate validation truth table too large")
            for local in range(1 << len(sites)):
                negatives = sum((1 << site) for k, site in enumerate(sites) if local & (1 << k))
                a = math.fsum(coef * (-1 if (mask & negatives).bit_count() % 2 else 1)
                              for mask, coef in terms)
                attained[0] = min(attained[0], a)
                attained[1] = max(attained[1], a)
                if a < self.m - 1e-12 or a > self.M + 1e-12:
                    raise ValueError((i, a, self.m, self.M))
        return attained

    def lam(self, mask):
        if not mask:
            raise ValueError("constant sector is excluded")
        if mask not in self.lam_cache:
            s, vals = mask, []
            while s:
                b = s & -s
                vals.append(self.clocks[b.bit_length() - 1])
                s ^= b
            self.lam_cache[mask] = 2 * math.fsum(vals)
        return self.lam_cache[mask]

    def column_B(self, mask):
        """Column of B=D^(-1/2) K D^(-1/2), D=K0, cached lazily."""
        if mask not in self.columns:
            out = {}
            s = mask
            invroot = 1 / math.sqrt(self.lam(mask))
            while s:
                bit = s & -s
                i = bit.bit_length() - 1
                for rate_mask, coef in self.rates[i]:
                    target = mask ^ rate_mask
                    value = 2 * self.clocks[i] * coef * invroot / math.sqrt(self.lam(target))
                    out[target] = out.get(target, 0.0) + value
                s ^= bit
            self.columns[mask] = tuple((s, v) for s, v in out.items() if v != 0)
            self.column_entries += len(self.columns[mask])
        return self.columns[mask]

    def apply_B(self, vec):
        out = {}
        for s, val in vec.items():
            for target, coef in self.column_B(s):
                out[target] = out.get(target, 0.0) + val * coef
        return {s: v for s, v in out.items() if v != 0.0}

    def source(self, f):
        b = {s: v / math.sqrt(self.lam(s)) for s, v in f.items() if v != 0}
        b2 = dot(b, b)
        return scaled(b, 1 / math.sqrt(b2)), b2

    def cg(self, f, rtol=1e-6, maxiter=30, max_terms=3000000):
        """CG with actual, recomputed residual certificates at every iterate.

        L=2<b,y>-<y,By>; U=L+||b-By||^2/m.  Scaling by b2
        restores physical chi.  Term cap raises, rather than truncates silently.
        """
        b, b2 = self.source(f)
        y, r, p = {}, dict(b), dict(b)
        rr = dot(r, r)
        history = []
        tic = time.perf_counter()
        for k in range(1, maxiter + 1):
            Bp = self.apply_B(p)
            alpha = rr / dot(p, Bp)
            y = axpy(y, alpha, p)
            recurrence_r = axpy(r, -alpha, Bp)
            By = self.apply_B(y)
            actual_r = axpy(b, -1, By)
            lower = 2 * dot(b, y) - dot(y, By)
            gap = dot(actual_r, actual_r) / self.m
            history.append({
                "iteration": k, "lower": b2 * lower,
                "upper": b2 * (lower + gap),
                "relative_width": gap / lower,
                "source_inner_product": b2 * dot(b, y),
                "solution_terms": len(y), "residual_terms": len(actual_r),
                "cached_columns": len(self.columns),
                "cached_column_entries": self.column_entries,
                "seconds": time.perf_counter() - tic,
                "residual_recurrence_drift": math.sqrt(dot(axpy(actual_r, -1, recurrence_r),
                                                          axpy(actual_r, -1, recurrence_r))),
            })
            if gap <= rtol * lower:
                break
            if max(len(y), len(actual_r), len(self.columns)) > max_terms:
                history[-1]["stopped_term_cap"] = True
                break
            r = recurrence_r
            rr_new = dot(r, r)
            p = axpy(r, rr_new / rr, p)
            rr = rr_new
        return {"method": "matrix-free Walsh PCG", "n": self.n,
                "m": self.m, "M": self.M, "clock_min": min(self.clocks),
                "clock_max": max(self.clocks), "requested_rtol": rtol,
                "arithmetic": "IEEE float64; exact-arithmetic certificate formula",
                "source_terms": len(f), "reference_response": b2,
                "history": history}

    def direct(self, f):
        """Independent full-state generator solve, only for small n."""
        if self.n > 18:
            raise ValueError("full-state oracle restricted to n <= 18")
        N = 1 << self.n
        states = np.arange(N, dtype=np.int64)
        rows, cols, vals = [], [], []
        diag = np.zeros(N)
        for i, terms in enumerate(self.rates):
            arate = np.zeros(N)
            for mask, coef in terms:
                sign = np.fromiter(((-1.) ** ((int(s) & mask).bit_count() % 2)
                                    for s in states), dtype=float)
                arate += coef * sign
            arate *= self.clocks[i]
            diag += arate
            rows.extend(states.tolist())
            cols.extend((states ^ (1 << i)).tolist())
            vals.extend((-arate).tolist())
        rows.extend(states.tolist()); cols.extend(states.tolist()); vals.extend(diag.tolist())
        K = sp.csr_matrix((vals, (rows, cols)), shape=(N, N))
        fv = np.zeros(N)
        for mask, coef in f.items():
            fv += coef * np.fromiter(((-1.) ** ((int(s) & mask).bit_count() % 2)
                                     for s in states), dtype=float)
        # Fix a value at state zero; f has exactly zero equilibrium mean.
        u = np.zeros(N)
        u[1:] = spla.spsolve(K[1:, 1:], fv[1:])
        chi = float(fv @ u / N)
        residual = K @ u - fv
        return {"response": chi, "state_count": N,
                "relative_residual": float(np.linalg.norm(residual) / np.linalg.norm(fv)),
                "symmetry_error": float(spla.norm(K - K.T))}


def soft_east(n, softness=0.2, clock_decades=0.0):
    """A_i = softness + (1-softness)*(1+sigma_(i-1))/2."""
    clocks = [10. ** (-clock_decades * ((i * 17) % n) / max(n-1, 1)) for i in range(n)]
    rates = [[(0, (1 + softness) / 2), (1 << ((i-1) % n), (1-softness)/2)]
             for i in range(n)]
    return ProductFlipModel(clocks, rates, softness, 1.)


def pair_modulated(n, amplitude=0.6, clock_decades=0.0):
    """A_i=1+a sigma_(i-1) sigma_(i+1), extensive cubic generator."""
    clocks = [10. ** (-clock_decades * ((i * 17) % n) / max(n-1, 1)) for i in range(n)]
    rates = [[(0, 1.), ((1 << ((i-1) % n)) | (1 << ((i+1) % n)), amplitude)]
             for i in range(n)]
    return ProductFlipModel(clocks, rates, 1-abs(amplitude), 1+abs(amplitude))


def two_sided(n, clock_decades=0.0):
    """Matched hard-row test A_i=.5+2*1{sigma_L=sigma_R=+1}.

    Its constant Walsh coefficient is 1, with three .5 nonconstant terms.
    Absolute off-diagonal Fourier row sum 1.5 exceeds constant diagonal 1.
    Clocks follow nu_i=10^(-decades*((17*i) mod n)/(n-1)).
    """
    clocks = [10. ** (-clock_decades * ((i * 17) % n) / max(n-1, 1)) for i in range(n)]
    rates = []
    for i in range(n):
        left, right = 1 << ((i-1) % n), 1 << ((i+1) % n)
        rates.append([(0, 1.), (left, .5), (right, .5), (left | right, .5)])
    return ProductFlipModel(clocks, rates, .5, 2.5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=32)
    ap.add_argument("--softness", type=float, default=.2)
    ap.add_argument("--clock-decades", type=float, default=0.)
    ap.add_argument("--model", choices=["east", "pair", "two_sided"], default="east")
    ap.add_argument("--maxiter", type=int, default=20)
    ap.add_argument("--rtol", type=float, default=1e-6)
    ap.add_argument("--direct", action="store_true")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    if args.model == "east":
        model = soft_east(args.n, args.softness, args.clock_decades)
    elif args.model == "pair":
        model = pair_modulated(args.n, 1-args.softness, args.clock_decades)
    else:
        model = two_sided(args.n, args.clock_decades)
    f = {1 << i: 1/math.sqrt(args.n) for i in range(args.n)}
    result = model.cg(f, rtol=args.rtol, maxiter=args.maxiter)
    result["model"] = args.model
    result["source"] = "normalized total magnetization, sum_i sigma_i / sqrt(n)"
    if args.direct:
        result["independent_full_state"] = model.direct(f)
    payload = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()
