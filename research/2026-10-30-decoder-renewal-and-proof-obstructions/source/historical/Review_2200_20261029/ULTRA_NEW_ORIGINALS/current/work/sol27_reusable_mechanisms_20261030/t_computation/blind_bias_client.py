"""One predeclared blind scalar/vector balancing control, not a GLS run.

The client sees only a range/calibration contract and prepared-readout COUNTS.
The separate service has a hidden extremely rare original outcome and exact
systematic odds-calibration factor. Arb encloses its probabilities, a 64-bit
dyadic approximation is sampled using seeded PCG64 words, and EVERY virtual
shot is charged. Seeded PRNG execution is not a proof of iid fair bits.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time

import numpy as np
from flint import arb, ctx

HERE = Path(__file__).resolve().parent


def ceil_fraction(q):
    q = F(q)
    return -(-q.numerator // q.denominator)


def pow2(k):
    return F(1 << k) if k >= 0 else F(1, 1 << (-k))


def ceil_log2(q):
    q = F(q)
    k = q.numerator.bit_length() - q.denominator.bit_length()
    return k + int(q > pow2(k))


def aa(q):
    q = F(q)
    return arb(q.numerator) / q.denominator


def endpoint(q):
    """The input must be an exact Arb endpoint."""
    assert q.is_exact()
    mantissa, exponent = q.man_exp()
    return F(int(mantissa)) * pow2(int(exponent))


def ceil_log_upper(q):
    ctx.prec = 192
    return ceil_fraction(endpoint(aa(q).log().upper()))


def rational_approx(fn, tolerance):
    """Certified rational approximation; no float controls the result."""
    bits = 192
    while True:
        ctx.prec = bits
        ball = fn()
        lo, hi = endpoint(ball.lower()), endpoint(ball.upper())
        if hi - lo <= 2 * tolerance:
            return (lo + hi) / 2
        bits *= 2


def log_sigma_approx(r, tolerance):
    r = F(r)
    # log(1+e^-x)<=e^-x<=2^-x for x>=0; exact rational decision.
    cutoff = ceil_log2(2 / tolerance)
    if abs(r) >= cutoff:
        return min(F(0), r)
    return rational_approx(
        lambda: aa(min(F(0), r)) - (1 + (-aa(abs(r))).exp()).log(), tolerance)


class BlindBalancingClient:
    """Only calls service.count(outcome, nominal_bias, shot_count)."""
    def __init__(self, service, outcomes, alpha, eta, delta):
        self.service, self.O = service, outcomes
        self.eta, self.delta = F(eta), F(delta)
        self.bound = ceil_fraction(F(alpha) ** 2)
        self.R = 2 * self.bound + self.O + 2
        self.xi = self.eta / 128
        self.J = ceil_log2(8 * self.R) + 1
        beta0 = beta1 = self.delta / (2 * self.O)
        self.n0 = 2048 * ceil_log_upper(F(2 * self.J) / beta0)
        self.n1 = ceil_fraction(32768 * ceil_log_upper(2 / beta1) / self.eta ** 2)
        self.transcript = []

    def one(self, outcome):
        lo, hi = F(-self.R), F(self.R)
        chosen = None
        for j in range(self.J):
            u = (lo + hi) / 2
            count = self.service.count(outcome, u, self.n0)
            estimate = F(count, self.n0)
            row = {"phase": "search", "outcome": outcome, "round": j,
                   "bias": str(u), "shots": self.n0, "count": count}
            if estimate < F(3, 8):
                lo = u
                row["decision"] = "root to right"
            elif estimate > F(5, 8):
                hi = u
                row["decision"] = "root to left"
            else:
                chosen = u
                row["decision"] = "balanced interval"
            self.transcript.append(row)
            if chosen is not None:
                break
        if chosen is None:
            chosen = (lo + hi) / 2
        count = self.service.count(outcome, chosen, self.n1)
        qhat = min(F(3, 4), max(F(1, 4), F(count, self.n1)))
        estimate = rational_approx(
            lambda: aa(qhat).log() - aa(1 - qhat).log(), self.eta / 32) - chosen
        logp = log_sigma_approx(estimate, self.eta / 16)
        self.transcript.append({"phase": "final", "outcome": outcome,
                                "bias": str(chosen), "shots": self.n1,
                                "count": count, "qhat_clamped": str(qhat),
                                "estimated_binary_log_odds": str(estimate),
                                "estimated_log_probability": str(logp)})
        return logp, estimate

    def vector(self):
        results = tuple(self.one(y) for y in range(self.O))
        raw = tuple(v[0] for v in results)
        average = sum(raw) / self.O
        return tuple(v - average for v in raw), tuple(v[1] for v in results)


class HiddenBinaryBiasService:
    """A separate PREDECLARED simulator, not native-shot emulation.

    Original p(Y=1)=1/(1+2^L). The client has no access to L or to the
    probability quantization; those are exposed only by the final audit.
    """
    def __init__(self, hidden_L, calibration_factor, seed, probability_bits=64):
        self._L = hidden_L
        self._factor = F(calibration_factor)
        self._rng = np.random.Generator(np.random.PCG64(seed))
        self._seed = seed
        self._bits = probability_bits
        assert probability_bits == 64
        self.virtual_shots = self.random_words = 0
        self.requests = []

    def count(self, outcome, nominal_bias, shots):
        assert outcome in (0, 1) and shots >= 1
        ctx.prec = 256
        original_r = (-1 if outcome == 1 else 1) * self._L * arb(2).log()
        applied = aa(nominal_bias) + aa(self._factor).log()
        ideal = 1 / (1 + (-(original_r + applied)).exp())
        lower, upper = endpoint(ideal.lower()), endpoint(ideal.upper())
        denominator = 1 << self._bits
        threshold = max(0, min(denominator, (lower * denominator).numerator //
                               (lower * denominator).denominator))
        quantized = F(threshold, denominator)
        assert quantized <= lower
        assert upper - quantized <= F(2, denominator)
        count = 0
        if threshold == denominator:
            count = shots
        elif threshold:
            left = shots
            while left:
                block = min(left, 1 << 17)
                words = self._rng.bit_generator.random_raw(block)
                count += int(np.count_nonzero(words < np.uint64(threshold)))
                self.random_words += block
                left -= block
        self.virtual_shots += shots
        self.requests.append({"outcome": outcome, "bias": str(nominal_bias),
                              "virtual_shots": shots, "count": count,
                              "dyadic_threshold": threshold,
                              "dyadic_denominator_bits": self._bits,
                              "per_shot_TV_to_ideal_upper": str(F(2, denominator))})
        return count

    def audit_after_client_locked(self):
        ctx.prec = 256
        return {"hidden_L": self._L, "calibration_factor": str(self._factor),
                "calibration_log_error_arb": str(aa(self._factor).log()),
                "true_original_outcome1_log_odds_arb": str(-self._L * arb(2).log()),
                "source_probability": "p1=1/(1+2^L), p0=2^L/(1+2^L)",
                "seed": self._seed, "PRNG": "NumPy PCG64",
                "virtual_shots": self.virtual_shots,
                "random_uint64_words": self.random_words,
                "generated_PRNG_bits": 64 * self.random_words,
                "total_dyadic_simulation_TV_upper": str(F(2 * self.virtual_shots, 1 << 64)),
                "physical_shots": 0}


def main():
    started = time.perf_counter()
    service = HiddenBinaryBiasService(1443, F(1025, 1024), 2026103001)
    client = BlindBalancingClient(service, 2, 32, F(1, 4), F(1, 20))
    centered, estimated_odds = client.vector()
    # The client is now locked. Only this audit stage exposes the hidden source.
    audit = service.audit_after_client_locked()
    ctx.prec = 256
    true_r1 = -service._L * arb(2).log()
    true_centered = (-true_r1 / 2, true_r1 / 2)
    errors = [abs(aa(v) - truth) for v, truth in zip(centered, true_centered)]
    assert all(error < aa(client.eta) for error in errors)
    assert aa(service._factor).log() < aa(client.xi)
    record = {
        "status": "PASS",
        "scope": "one predeclared blind finite scalar/vector balancing client; NOT a GLS/source-learning run",
        "randomness_scope": "seeded PRNG diagnostic; iid-64-bit-word abstraction plus explicit dyadic coupling bound",
        "theorem_sha256": hashlib.sha256((HERE / "BIASED_READOUT_RECEIVER.md").read_bytes()).hexdigest(),
        "client_input": {"outcomes": 2, "alpha": 32, "eta": str(client.eta),
                         "delta": str(client.delta), "command_range": client.R,
                         "calibration_absolute_log_odds_error_bound": str(client.xi),
                         "maximum_search_rounds": client.J,
                         "search_shots_per_round": client.n0,
                         "final_shots_per_outcome": client.n1},
        "client_transcript": client.transcript,
        "centered_logit_estimates": list(map(str, centered)),
        "centered_logit_error_arb": list(map(str, errors)),
        "source_audit_after_lock": audit,
        "service_requests": service.requests,
        "source_or_GLS_learning_runs": 0,
        "no_rare_native_shot_emulation": True,
        "elapsed_seconds_after_imports": time.perf_counter() - started,
    }
    (HERE / "BLIND_BIAS_EXECUTION.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"status": record["status"], "scope": record["scope"],
                      "virtual_shots": audit["virtual_shots"],
                      "PRNG_bits": audit["generated_PRNG_bits"],
                      "logit_errors": list(map(str, errors)),
                      "elapsed_seconds_after_imports": record["elapsed_seconds_after_imports"]}, indent=2))


if __name__ == "__main__":
    main()
