#!/usr/bin/env python3
"""Physical Fock-amplitude amplifier diagnostic; never exponentiates cut-off CCRs.

Finite input support is exact. The retained low-number output block is exact
up to floating arithmetic by the SU(1,1) disentangling series. Its omitted
tail is bounded analytically using pinching and the exact full output energy.
The bounds are mathematical cutoff bounds, not interval-arithmetic certificates.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np


def g(x):
    if x <= 0:
        return 0.0
    return math.log1p(x) + x * math.log1p(1.0 / x)


def inverse_g(s):
    if s < 1e-14:
        return 0.0
    lo, hi = 0.0, max(1.0, math.exp(s))
    for _ in range(80):
        mid = (lo + hi) / 2
        if g(mid) < s:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def entropy(rho):
    vals = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    if vals.min() < -2e-10:
        raise ValueError(f"Output not positive: {vals.min()}")
    vals = vals[vals > 1e-16]
    return float(-np.dot(vals, np.log(vals)))


def h2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log(x) - (1 - x) * math.log1p(-x)


def amplitude(p, q, m, n, gain):
    """Exact U_G coefficient <p,q|U_G|m,n>, finite sum for finite m,n."""
    if p - q != m - n:
        return 0.0
    shift = p - m
    t = math.sqrt((gain - 1) / gain)
    sech = 1 / math.sqrt(gain)
    total = 0.0
    for ell in range(max(0, -shift), min(m, n) + 1):
        k = shift + ell
        logpref = (
            0.5 * sum(math.lgamma(v + 1) for v in (m, n, p, q))
            - sum(math.lgamma(v + 1) for v in (ell, k, m - ell, n - ell))
        )
        total += ((-1) ** ell * math.exp(logpref)
                  * t ** (shift + 2 * ell)
                  * sech ** (m + n - 2 * ell + 1))
    return total


class Channel:
    def __init__(self, dimension, cutoff, gain):
        self.d, self.L, self.G = dimension, cutoff, gain
        d, L = dimension, cutoff
        self.offsets = range(-2 * (d - 1), 2 * (d - 1) + 1)
        pairs = [(m, n) for m in range(d) for n in range(d)]
        differences = [m - n for m, n in pairs]
        coeff = np.zeros((d * d, L))
        for i, (m, n) in enumerate(pairs):
            for p in range(L):
                q = p - differences[i]
                if q >= 0:
                    coeff[i, p] = amplitude(p, q, m, n, gain)
        self.coeff = coeff
        self.transfer = np.zeros((len(self.offsets) * L, d ** 4))
        for i, di in enumerate(differences):
            for j, dj in enumerate(differences):
                off = dj - di
                band = off + 2 * (d - 1)
                for p in range(max(0, -off), min(L, L - off)):
                    pprime = p + off
                    self.transfer[band * L + p, i * d * d + j] = (
                        coeff[i, p] * coeff[j, pprime]
                    )
        self.a = np.diag(np.sqrt(np.arange(1, d)), 1)
        self.number = np.diag(np.arange(d))

    def output_block(self, a, b):
        weights = np.kron(a, b).reshape(-1)
        bands = (self.transfer @ weights).reshape(len(self.offsets), self.L)
        result = np.zeros((self.L, self.L), dtype=complex)
        for row, off in enumerate(self.offsets):
            p = np.arange(max(0, -off), min(self.L, self.L - off))
            result[p, p + off] = bands[row, p]
        return (result + result.conj().T) / 2

    def evaluate(self, a, b):
        block = self.output_block(a, b)
        mass = float(np.trace(block).real)
        if not 0 < mass <= 1 + 2e-10:
            raise ValueError(f"Invalid low-block trace {mass}")
        s_low = entropy(block / mass)
        q_raw = max(0.0, 1 - mass)
        # Explicit numerical allowance. This is not certified interval rounding.
        q = min(1.0, q_raw + 2e-11)
        e_a = float(np.trace(a @ self.number).real)
        e_b = float(np.trace(b @ self.number).real)
        mu_a = np.trace(a @ self.a)
        mu_b = np.trace(b @ self.a)
        energy = (self.G * e_a + (self.G - 1) * (e_b + 1)
                  + 2 * math.sqrt(self.G * (self.G - 1)) * (mu_a * mu_b).real)
        low_energy = float(np.dot(np.arange(self.L), block.diagonal().real))
        tail_energy = max(0.0, energy - low_energy) + 2e-10
        # P_L local block, pinching: (1-q)S_low <= S <=
        # h2(q)+(1-q)S_low+q*g(E_tail/q). A conservative arithmetic allowance.
        s_lower = max(0.0, (1 - q) * s_low - 2e-10)
        s_upper = h2(q) + (1 - q_raw) * s_low + q * g(tail_energy / q) + 2e-10
        s_a, s_b = entropy(a), entropy(b)
        a_entropy, b_entropy = inverse_g(s_a), inverse_g(s_b)
        target = g(self.G * a_entropy + (self.G - 1) * (b_entropy + 1))
        return {
            "gain": self.G, "cutoff": self.L, "mass": mass,
            "tail_probability": q_raw, "tail_energy": tail_energy,
            "entropy_lower": s_lower, "entropy_upper": s_upper,
            "target_entropy": target, "gap_lower": s_lower - target,
            "gap_upper": s_upper - target, "input_entropies": [s_a, s_b],
            "input_energies": [e_a, e_b], "output_energy": energy,
            "input_means": [[mu_a.real, mu_a.imag], [mu_b.real, mu_b.imag]],
        }


def projector(v):
    v = np.asarray(v, dtype=complex)
    v = v / np.linalg.norm(v)
    return np.outer(v, v.conj())


def state(rng, d, mode):
    if mode == "pure":
        return projector(rng.normal(size=d) + 1j * rng.normal(size=d))
    if mode == "near_vacuum":
        v = (rng.normal(size=d) + 1j * rng.normal(size=d)) * 10 ** rng.uniform(-3, -.3)
        v[0] = 1
        return projector(v)
    if mode == "diagonal":
        weights = rng.dirichlet(np.repeat(10 ** rng.uniform(-1.7, 1), d))
        return np.diag(weights)
    if mode == "thermal_truncated":
        mean = 10 ** rng.uniform(-2, 0.4)
        weights = (mean / (mean + 1)) ** np.arange(d)
        return np.diag(weights / weights.sum())
    rank = rng.integers(2, d + 1)
    X = rng.normal(size=(d, rank)) + 1j * rng.normal(size=(d, rank))
    X *= (10 ** rng.uniform(-1.5, 0, size=d))[:, None]
    result = X @ X.conj().T
    return result / np.trace(result)


def serialize_state(rho):
    return {"real": rho.real.tolist(), "imag": rho.imag.tolist()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=500)
    parser.add_argument("--seed", type=int, default=195031)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "search_results.json")
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    d = 4
    modes = ["pure", "mixed", "diagonal", "near_vacuum", "thermal_truncated"]
    pairs = []
    for i in range(args.samples):
        ma, mb = modes[i % len(modes)], modes[(i // len(modes)) % len(modes)]
        pairs.append((state(rng, d, ma), state(rng, d, mb), f"random:{ma}:{mb}:{i}"))
    for m in range(d):
        for n in range(d):
            pairs.append((np.diag(np.eye(d)[m]), np.diag(np.eye(d)[n]), f"fock:{m}:{n}"))
    summaries = []
    for gain, cutoff in [(1.1, 32), (1.5, 48), (2.0, 72), (3.0, 120)]:
        chan = Channel(d, cutoff, gain)
        best = None
        best_nonvacuum = None
        negative_upper = 0
        ambiguous = 0
        max_q, max_width = 0.0, 0.0
        for a, b, label in pairs:
            result = chan.evaluate(a, b)
            result["label"] = label
            if result["gap_upper"] < -1e-8:
                negative_upper += 1
            if result["gap_lower"] < 0 < result["gap_upper"]:
                ambiguous += 1
            max_q = max(max_q, result["tail_probability"])
            max_width = max(max_width, result["entropy_upper"] - result["entropy_lower"])
            saved = result | {"state_a": serialize_state(a), "state_b": serialize_state(b)}
            if best is None or result["gap_upper"] < best["gap_upper"]:
                best = saved
            if label != "fock:0:0" and (best_nonvacuum is None or result["gap_upper"] < best_nonvacuum["gap_upper"]):
                best_nonvacuum = saved
        # Require the vacuum identity and full energy identity at representative Fock inputs.
        vac = np.diag(np.eye(d)[0])
        vacuum = chan.evaluate(vac, vac)
        q_expected = ((gain - 1) / gain) ** cutoff
        vacuum["expected_tail"] = q_expected
        summary = {
            "gain": gain, "cutoff": cutoff, "count": len(pairs),
            "negative_upper": negative_upper, "ambiguous": ambiguous,
            "max_tail_probability": max_q, "max_entropy_width": max_width,
            "best": best, "best_nonvacuum": best_nonvacuum, "vacuum_control": vacuum,
        }
        summaries.append(summary)
        print(json.dumps({k: summary[k] for k in ["gain", "cutoff", "count", "negative_upper", "ambiguous", "max_tail_probability", "max_entropy_width"]}), flush=True)
        print(json.dumps({"best_label": best["label"], "best_gap": [best["gap_lower"], best["gap_upper"]], "best_nonvacuum_label": best_nonvacuum["label"], "best_nonvacuum_gap": [best_nonvacuum["gap_lower"], best_nonvacuum["gap_upper"]]}), flush=True)
    args.output.write_text(json.dumps({"seed": args.seed, "dimension": d,
        "method": "exact physical Fock coefficients; local-output pinching tail bound; floating arithmetic",
        "summaries": summaries}, indent=2))


if __name__ == "__main__":
    main()
