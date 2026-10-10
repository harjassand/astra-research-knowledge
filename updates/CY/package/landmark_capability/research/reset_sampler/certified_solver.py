#!/usr/bin/env python3
"""Certified stationary event queries and one lazy prefix sample.

This module imports the outward-rounded dyadic interval core from
work/certified_boundary/solver.py.  The reset model is never expanded into
its 2**n global states.  Only exact rational local data, local 2x2 killed
heat kernels, product contractions, and the k by k Woodbury solve are used.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import secrets
import sys
import time
from typing import Any


CORE_PATH = Path(__file__).resolve().parents[1] / "certified_boundary" / "solver.py"
CORE_NAME = "reset_sampler_interval_core"
CORE_SPEC = importlib.util.spec_from_file_location(CORE_NAME, CORE_PATH)
if CORE_SPEC is None or CORE_SPEC.loader is None:
    raise ImportError(f"cannot load interval core at {CORE_PATH}")
IC = importlib.util.module_from_spec(CORE_SPEC)
sys.modules[CORE_NAME] = IC
CORE_SPEC.loader.exec_module(IC)


MAX_PRECISION_BITS = 768
MAX_DELTA_BITS = 640
MAX_NODES = 350_000
MAX_ADAPT_STEPS = 8


def F(x: str | int | Fraction) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x)


def frac(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def ceil_log2(x: Fraction) -> int:
    if x <= 0:
        raise ValueError("ceil_log2 requires a positive rational")
    if x <= 1:
        return 0
    b = x.numerator.bit_length() - x.denominator.bit_length()
    if Fraction(1 << max(0, b), 1) < x:
        b += 1
    return max(0, b)


def ceil_power_two_reciprocal(x: Fraction) -> Fraction:
    """Return 2^-b <= x for the least nonnegative such b."""
    if x <= 0:
        raise ValueError("need positive cutoff")
    b = ceil_log2(1 / x)
    return Fraction(1, 1 << b)


def set_interval_precision(bits: int) -> None:
    if bits < 64 or (MAX_PRECISION_BITS is not None and bits > MAX_PRECISION_BITS):
        raise ArithmeticError(f"interval precision {bits} outside supported range")
    IC.PRECISION_BITS = bits
    IC.SCALE = 1 << bits
    IC.ZERO = IC.Iv(0, 0)
    IC.ONE = IC.Iv(IC.SCALE, IC.SCALE)


@dataclass(frozen=True)
class ResetModel:
    up: tuple[Fraction, ...]
    down: tuple[Fraction, ...]
    hazards: tuple[tuple[tuple[Fraction, Fraction], ...], ...]
    reset_one: tuple[tuple[Fraction, ...], ...]
    initial_one: tuple[Fraction, ...]

    @property
    def n(self) -> int:
        return len(self.up)

    @property
    def k(self) -> int:
        return len(self.hazards)

    @property
    def base_stationary_one(self) -> tuple[Fraction, ...]:
        return tuple(u / (u + d) for u, d in zip(self.up, self.down))

    @property
    def base_stationary(self) -> tuple[tuple[Fraction, Fraction], ...]:
        return tuple((d / (u + d), u / (u + d))
                     for u, d in zip(self.up, self.down))

    @property
    def local_total_hazards(self) -> tuple[tuple[Fraction, Fraction], ...]:
        return tuple(tuple(sum(self.hazards[l][i][x] for l in range(self.k))
                           for x in range(2))
                     for i in range(self.n))

    @property
    def amax(self) -> Fraction:
        return sum(max(pair) for pair in self.local_total_hazards)

    @property
    def lambda_trace_bound(self) -> Fraction:
        # A_i is positive semidefinite and its largest eigenvalue is at most
        # its trace u_i+d_i+a_i(0)+a_i(1).
        return sum(self.up[i] + self.down[i] + sum(self.local_total_hazards[i])
                   for i in range(self.n))

    def validate(self) -> None:
        if self.n == 0 or len(self.down) != self.n or len(self.initial_one) != self.n:
            raise ValueError("up, down, and initial vectors must have equal positive length")
        if self.k == 0 or len(self.reset_one) != self.k:
            raise ValueError("need at least one reset channel")
        if any(x <= 0 for x in (*self.up, *self.down)):
            raise ValueError("two-state base flip rates must be positive")
        if any(not (0 <= x <= 1) for x in (*self.initial_one, *(x for row in self.reset_one for x in row))):
            raise ValueError("product-law probabilities must be in [0,1]")
        if any(len(row) != self.n for row in self.reset_one):
            raise ValueError("each reset law needs one probability per coordinate")
        if len(self.hazards) != self.k or any(len(row) != self.n for row in self.hazards):
            raise ValueError("hazards need shape (channels, coordinates, two states)")
        if any(len(pair) != 2 for row in self.hazards for pair in row):
            raise ValueError("each local hazard needs values for states zero and one")
        if any(x < 0 for row in self.hazards for pair in row for x in pair):
            raise ValueError("reset hazards must be nonnegative")


def make_fixture() -> ResetModel:
    """The three-coordinate slice of verify.py's heterogeneous fixture."""
    return ResetModel(
        up=tuple(map(F, ("0.35", "0.50", "0.20"))),
        down=tuple(map(F, ("0.80", "1.10", "0.60"))),
        hazards=(
            ((F("0.10"), F("0.35")), (F("0.20"), F("0.05")),
             (F("0.05"), F("0.25"))),
            ((F("0.16"), F("0.03")), (F("0.04"), F("0.19")),
             (F("0.21"), F("0.06"))),
        ),
        reset_one=(tuple(map(F, ("0.85", "0.75", "0.90"))),
                   tuple(map(F, ("0.15", "0.25", "0.35")))),
        initial_one=tuple(map(F, ("0.60", "0.20", "0.55"))),
    )


def nonnegative(iv: Any) -> Any:
    if iv.hi < 0:
        raise ArithmeticError("computed interval misses known nonnegative value")
    return IC.Iv(max(0, iv.lo), max(0, iv.hi))


def plus_many(values: list[Any]) -> Any:
    out = IC.ZERO
    for value in values:
        out = IC.iv_add(out, value)
    return out


def prepare_local_spectra(model: ResetModel) -> list[dict[str, Any]]:
    """Enclose the node-independent spectral projectors once per precision."""
    data: list[dict[str, Any]] = []
    for i in range(model.n):
        up, down = model.up[i], model.down[i]
        a0, a1 = model.local_total_hazards[i]
        d0, d1 = up + a0, down + a1
        gap2 = (d0 - d1) ** 2 + 4 * up * down
        gap = IC.iv_sqrt_fraction(gap2)
        c = IC.iv_sqrt_fraction(up * down)
        high = IC.iv_scale(
            IC.iv_add(IC.iv_add(IC.iv_fraction(d0), IC.iv_fraction(d1)), gap),
            Fraction(1, 2))
        determinant = up * a1 + down * a0 + a0 * a1
        if high.lo <= 0 or gap.lo <= 0:
            raise ArithmeticError("local spectral interval lost a positive denominator; increase precision")
        low = IC.iv_div(IC.iv_fraction(determinant), high)

        p00_low = nonnegative(IC.iv_sub(high, IC.iv_fraction(d0)))
        p00_high = nonnegative(IC.iv_sub(IC.iv_fraction(d0), low))
        p11_low = nonnegative(IC.iv_sub(high, IC.iv_fraction(d1)))
        p11_high = nonnegative(IC.iv_sub(IC.iv_fraction(d1), low))
        p_low_00 = IC.iv_div(p00_low, gap)
        p_high_00 = IC.iv_div(p00_high, gap)
        p_low_11 = IC.iv_div(p11_low, gap)
        p_high_11 = IC.iv_div(p11_high, gap)
        p_off = IC.iv_div(c, gap)
        root_up_down = IC.iv_sqrt_fraction(up / down)
        root_down_up = IC.iv_sqrt_fraction(down / up)
        data.append({"low": low, "high": high,
                     "p_low_00": p_low_00, "p_high_00": p_high_00,
                     "p_low_11": p_low_11, "p_high_11": p_high_11,
                     "p_off": p_off,
                     "root_up_down": root_up_down,
                     "root_down_up": root_down_up})
    return data


def local_killed_heat(spectra: list[dict[str, Any]], qtime: Any) -> list[list[list[Any]]]:
    """Return raw exp(t L_i) entries through symmetric 2x2 spectral data."""
    out: list[list[list[Any]]] = []
    for spec in spectra:
        e_low = IC.exp_neg(IC.iv_mul(qtime, spec["low"]))
        e_high = IC.exp_neg(IC.iv_mul(qtime, spec["high"]))
        s00 = IC.iv_add(IC.iv_mul(spec["p_low_00"], e_low),
                        IC.iv_mul(spec["p_high_00"], e_high))
        s11 = IC.iv_add(IC.iv_mul(spec["p_low_11"], e_low),
                        IC.iv_mul(spec["p_high_11"], e_high))
        diff = nonnegative(IC.iv_sub(e_low, e_high))
        s01 = IC.iv_mul(spec["p_off"], diff)
        e01 = IC.iv_mul(s01, spec["root_up_down"])
        e10 = IC.iv_mul(s01, spec["root_down_up"])
        out.append([[s00, e01], [e10, s11]])
    return out


def law_vectors(model: ResetModel) -> list[tuple[Fraction, ...]]:
    return [model.initial_one, *model.reset_one]


def law_norm_upper(model: ResetModel, law: tuple[Fraction, ...]) -> Fraction:
    norm2 = Fraction(1)
    for i, r in enumerate(law):
        pi0, pi1 = model.base_stationary[i]
        norm2 *= (1 - r) ** 2 / pi0 + r * r / pi1
    return Fraction(IC.iv_sqrt_fraction(norm2).hi, IC.SCALE)


def event_norm_upper(model: ResetModel, mask: tuple[tuple[bool, bool], ...]) -> Fraction:
    prob = Fraction(1)
    for i, allowed in enumerate(mask):
        pi0, pi1 = model.base_stationary[i]
        prob *= (pi0 if allowed[0] else 0) + (pi1 if allowed[1] else 0)
    return Fraction(IC.iv_sqrt_fraction(prob).hi, IC.SCALE)


def hazard_norm_upper(model: ResetModel, channel: int) -> Fraction:
    second = Fraction(0)
    means: list[Fraction] = []
    seconds: list[Fraction] = []
    for i, (pi0, pi1) in enumerate(model.base_stationary):
        h0, h1 = model.hazards[channel][i]
        means.append(pi0 * h0 + pi1 * h1)
        seconds.append(pi0 * h0 * h0 + pi1 * h1 * h1)
    mean = sum(means, Fraction(0))
    second = sum(seconds, Fraction(0)) + 2 * sum(
        means[i] * means[j] for i in range(model.n) for j in range(i + 1, model.n))
    return Fraction(IC.iv_sqrt_fraction(second).hi, IC.SCALE)


def mixing_certificate(model: ResetModel) -> dict[str, Fraction]:
    """No-reset minorization P_1(x,y)>=eta, with rational eta>0.

    On paths with no reset in [0,1], the reset chain dominates
    exp(-Amax) times the independent base-chain transition kernel.  For a
    two-state base coordinate, every entry of P_1 is at least
    min(pi0,pi1)*min((u+d)/2,1/2), using 1-exp(-x)>=min(x/2,1/2).
    Also exp(-Amax)>=2^-ceil(2 Amax), since e<4.
    """
    t = Fraction(1)
    a_bits = (2 * model.amax * t).__ceil__()
    eta = Fraction(1, 1 << a_bits)
    for i, (up, down) in enumerate(zip(model.up, model.down)):
        total_rate = up + down
        pi0, pi1 = model.base_stationary[i]
        cross_lower = min(total_rate * t / 2, Fraction(1, 2))
        eta *= min(pi0, pi1) * cross_lower
    if not (0 < eta <= 1):
        raise ArithmeticError("failed to obtain a positive rational minorization")
    return {"T": t, "eta": eta}


def source_and_observable_data(model: ResetModel,
                               masks: list[tuple[tuple[bool, bool], ...]]) -> dict:
    laws = law_vectors(model)
    return {
        "laws": laws,
        "law_norms": [law_norm_upper(model, law) for law in laws],
        "event_norms": [event_norm_upper(model, mask) for mask in masks],
        "hazard_norms": [hazard_norm_upper(model, q) for q in range(model.k)],
    }


def integrate_product_contractions(model: ResetModel,
                                   masks: list[tuple[tuple[bool, bool], ...]],
                                   s: Fraction,
                                   delta_bits: int,
                                   *, spectral_floor: Fraction | None = None) -> tuple[dict, dict]:
    delta = Fraction(1, 1 << delta_bits)
    alpha_max = s + model.lambda_trace_bound
    jstep = delta_bits + 10
    floor = s if spectral_floor is None else spectral_floor
    if floor <= 0 or floor > alpha_max:
        raise ValueError("need a valid positive lower spectral bound")
    nodes, h_iv = IC.grid_nodes(floor, alpha_max, delta, delta_bits, jstep)
    if MAX_NODES is not None and len(nodes) > MAX_NODES:
        raise ArithmeticError(f"quadrature would use {len(nodes)} nodes (limit {MAX_NODES})")

    laws = law_vectors(model)
    law_iv = [[(IC.iv_fraction(1 - r), IC.iv_fraction(r)) for r in law]
              for law in laws]
    hazard_iv = [[[IC.iv_fraction(x) for x in pair] for pair in channel]
                 for channel in model.hazards]

    accum_a = [[IC.ZERO for _ in masks] for _ in laws]
    accum_h = [[IC.ZERO for _ in range(model.k)] for _ in laws]
    spectra = prepare_local_spectra(model)

    for qtime in nodes:
        exp_discount = IC.exp_neg(IC.iv_scale(qtime, s))
        weight = IC.iv_mul(IC.iv_mul(h_iv, qtime), exp_discount)
        heat = local_killed_heat(spectra, qtime)
        propagated: list[list[list[Any]]] = []
        survival: list[list[Any]] = []
        hazard_parts: list[list[list[Any]]] = []

        for source in range(len(laws)):
            source_prop: list[list[Any]] = []
            source_survival: list[Any] = []
            source_hazards: list[list[Any]] = []
            for i in range(model.n):
                p0, p1 = law_iv[source][i]
                e = [
                    IC.iv_add(IC.iv_mul(p0, heat[i][0][y]),
                              IC.iv_mul(p1, heat[i][1][y]))
                    for y in range(2)
                ]
                source_prop.append(e)
                source_survival.append(IC.iv_add(e[0], e[1]))
                parts = []
                for channel in range(model.k):
                    parts.append(IC.iv_add(
                        IC.iv_mul(e[0], hazard_iv[channel][i][0]),
                        IC.iv_mul(e[1], hazard_iv[channel][i][1])))
                source_hazards.append(parts)
            propagated.append(source_prop)
            survival.append(source_survival)
            hazard_parts.append(source_hazards)

        for source in range(len(laws)):
            prefix = [IC.ONE]
            for factor in survival[source]:
                prefix.append(IC.iv_mul(prefix[-1], factor))
            suffix = [IC.ONE for _ in range(model.n + 1)]
            for i in range(model.n - 1, -1, -1):
                suffix[i] = IC.iv_mul(survival[source][i], suffix[i + 1])
            excluding = [IC.iv_mul(prefix[i], suffix[i + 1]) for i in range(model.n)]
            for gi, mask in enumerate(masks):
                factors = []
                for i, allowed in enumerate(mask):
                    terms = [propagated[source][i][x]
                             for x in range(2) if allowed[x]]
                    factors.append(plus_many(terms))
                product = IC.ONE
                for factor in factors:
                    product = IC.iv_mul(product, factor)
                accum_a[source][gi] = IC.iv_add(
                    accum_a[source][gi], IC.iv_mul(weight, product))

            for channel in range(model.k):
                total = IC.ZERO
                for i in range(model.n):
                    product = IC.iv_mul(hazard_parts[source][i][channel], excluding[i])
                    total = IC.iv_add(total, product)
                accum_h[source][channel] = IC.iv_add(
                    accum_h[source][channel], IC.iv_mul(weight, total))

    finite = {
        "a": accum_a[0],
        "v": accum_a[1:],
        "d": accum_h[0],
        "M": accum_h[1:],
        "node_count": len(nodes),
        "delta": delta,
        "delta_bits": delta_bits,
        "jstep": jstep,
    }
    norms = source_and_observable_data(model, masks)
    return finite, norms


def scalar_interval_data(iv: Any, bilinear_bound: Fraction) -> tuple[Fraction, Fraction]:
    return IC.midpoint(iv), IC.radius(iv) + bilinear_bound


def rational_inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return IC.exact_inverse(matrix)


def woodbury_interval(finite: dict, norms: dict, s: Fraction,
                      model: ResetModel, gi: int) -> tuple[Fraction, Fraction, dict]:
    """Center and explicit absolute error for mu R(s) g_gi."""
    delta, k, m = finite["delta"], model.k, len(norms["event_norms"])
    s_inv = 1 / s
    d_norm = norms["law_norms"][0]
    reset_norms = norms["law_norms"][1:]
    g_norms = norms["event_norms"]
    h_norms = norms["hazard_norms"]

    a_c, a_e = scalar_interval_data(
        finite["a"][gi], delta * s_inv * d_norm * g_norms[gi])
    d_data = [scalar_interval_data(finite["d"][q],
                                   delta * s_inv * d_norm * h_norms[q])
              for q in range(k)]
    v_data = [[scalar_interval_data(finite["v"][l][j],
                                    delta * s_inv * reset_norms[l] * g_norms[j])
               for j in range(m)] for l in range(k)]
    matrix_data = [[scalar_interval_data(finite["M"][l][q],
                                         delta * s_inv * reset_norms[l] * h_norms[q])
                    for q in range(k)] for l in range(k)]

    d_c = [x[0] for x in d_data]
    d_e = max(x[1] for x in d_data)
    v_c = [v_data[l][gi][0] for l in range(k)]
    v_e = max(v_data[l][gi][1] for l in range(k))
    M_c = [[matrix_data[l][q][0] for q in range(k)] for l in range(k)]
    e_M = max(matrix_data[l][q][1] for l in range(k) for q in range(k))
    e_J = k * e_M
    J_c = [[Fraction(int(l == q)) - M_c[l][q] for q in range(k)]
           for l in range(k)]

    C = 1 + model.amax / s
    if C * e_J >= Fraction(1, 2):
        raise ArithmeticError("Woodbury inverse interval too wide; increase quadrature precision")
    Jinv = rational_inverse(J_c)
    y_c = [sum(Jinv[l][q] * v_c[q] for q in range(k)) for l in range(k)]
    result_c = a_c + sum(d_c[l] * y_c[l] for l in range(k))

    d_l1 = sum(abs(x) for x in d_c)
    v_inf = max(abs(x) for x in v_c)
    result_e = (a_e
                + k * d_e * C * (v_inf + v_e)
                + d_l1 * 4 * C * C * e_J * (v_inf + v_e)
                + d_l1 * 2 * C * v_e)
    detail = {
        "resolvent_center": result_c,
        "resolvent_abs_error": result_e,
        "woodbury_inverse_bound": C,
        "woodbury_matrix_error_inf": e_J,
        "woodbury_matrix_error_entry": e_M,
        "cross_row_l1_center": d_l1,
        "reset_event_vector_inf_center": v_inf,
        "cross_row_entry_error": d_e,
        "reset_event_entry_error": v_e,
        "base_event_entry_error": a_e,
    }
    return result_c, result_e, detail


def outward_dyadic_interval(center: Fraction, radius: Fraction,
                            bits: int) -> tuple[Fraction, Fraction]:
    scale = 1 << bits
    low = max(Fraction(0), center - radius)
    high = min(Fraction(1), center + radius)
    lo_int = (low * scale).numerator // (low * scale).denominator
    hi_scaled = high * scale
    hi_int = -((-hi_scaled.numerator) // hi_scaled.denominator)
    return Fraction(lo_int, scale), Fraction(hi_int, scale)


def stationary_event_interval(model: ResetModel,
                              masks: list[tuple[tuple[bool, bool], ...]],
                              accuracy: Fraction,
                              *, max_precision: int = MAX_PRECISION_BITS,
                              max_delta_bits: int = MAX_DELTA_BITS) -> tuple[list[tuple[Fraction, Fraction]], dict]:
    """Certified intervals of width <= accuracy for product event(s)."""
    model.validate()
    if accuracy <= 0 or accuracy >= 1:
        raise ValueError("accuracy must lie in (0,1)")
    if any(len(mask) != model.n for mask in masks):
        raise ValueError("each event mask needs one two-state set per coordinate")
    mix = mixing_certificate(model)
    eta, T = mix["eta"], mix["T"]
    s = ceil_power_two_reciprocal(accuracy * eta / (32 * T))
    mixing_error = 2 * s * T / eta
    numeric_radius_target = accuracy / 8
    output_bits = ceil_log2(64 / accuracy)
    target_bits = ceil_log2(1 / accuracy)
    s_bits = ceil_log2(1 / s)
    delta_bits = max(80, target_bits + 4 * s_bits + 80)
    last_detail: dict | None = None

    for attempt in range(MAX_ADAPT_STEPS):
        precision = max(224, delta_bits + 96, output_bits + 64)
        if precision > max_precision or delta_bits > max_delta_bits:
            raise ArithmeticError(
                f"requested tolerance needs precision delta_bits={delta_bits}, fixed_bits={precision}; "
                f"limits are {max_delta_bits} and {max_precision}")
        set_interval_precision(precision)
        try:
            finite, norms = integrate_product_contractions(model, masks, s, delta_bits)
            centers_errors = [woodbury_interval(finite, norms, s, model, gi)
                              for gi in range(len(masks))]
            intervals = []
            details = []
            all_met = True
            for center, resolvent_error, detail in centers_errors:
                radius = s * resolvent_error + mixing_error
                lo, hi = outward_dyadic_interval(center * s, radius, output_bits)
                intervals.append((lo, hi))
                details.append(detail)
                if hi - lo > accuracy or s * resolvent_error > numeric_radius_target:
                    all_met = False
            last_detail = {
                "s": s,
                "mixing_error": mixing_error,
                "requested_accuracy": accuracy,
                "output_bits": output_bits,
                "precision_bits": precision,
                "delta_bits": delta_bits,
                "node_count": finite["node_count"],
                "quadrature_delta": finite["delta"],
                "minorization_eta": eta,
                "minorization_T": T,
                "event_details": details,
                "event_intervals": intervals,
            }
            if all_met:
                return intervals, last_detail
        except ArithmeticError as exc:
            last_detail = {"attempt_error": str(exc)}
        delta_bits += 32

    raise ArithmeticError(f"precision adaptation exhausted; last state={last_detail}")


def event_mask_for_prefix(prefix: tuple[int, ...], n: int,
                          next_bit: int | None = None) -> tuple[tuple[bool, bool], ...]:
    if len(prefix) > n:
        raise ValueError("prefix longer than state")
    if next_bit not in (None, 0, 1):
        raise ValueError("next_bit must be 0, 1, or None")
    mask = []
    for i in range(n):
        if i < len(prefix):
            bit = prefix[i]
            mask.append((bit == 0, bit == 1))
        elif i == len(prefix) and next_bit is not None:
            mask.append((next_bit == 0, next_bit == 1))
        else:
            mask.append((True, True))
    return tuple(mask)


def ratio_interval(x: tuple[Fraction, Fraction],
                   y: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    xlo, xhi = x
    ylo, yhi = y
    if xlo < 0 or ylo < 0 or xlo + ylo <= 0:
        raise ArithmeticError("conditional denominator lacks a positive lower bound")
    return (xlo / (xlo + yhi), xhi / (xhi + ylo))


def lazy_exact_sample(model: ResetModel, *, demo_level_cap: int = 32) -> dict:
    """Run one lazy inverse-transform path with certified conditional bounds.

    `demo_level_cap` is a guard for this recorded run.  If reached, the call
    raises and records no sample. Every returned bit is decided by disjoint
    intervals and agrees with the uncapped exact sampler on those fair bits.
    Conditioning repeated capped runs on success need not preserve the
    stationary distribution, since failure can depend on the sampled state.
    """
    model.validate()
    mix = mixing_certificate(model)
    eta = mix["eta"]
    d = 2
    prefix: list[int] = []
    trace = []

    for coordinate in range(model.n):
        uniform_prefix = 0
        decided = False
        for level in range(1, demo_level_cap + 1):
            uniform_prefix = (uniform_prefix << 1) | secrets.randbits(1)
            accuracy = eta * Fraction(1, 1 << level) / (128 * d)
            masks = [event_mask_for_prefix(tuple(prefix), model.n, 0),
                     event_mask_for_prefix(tuple(prefix), model.n, 1)]
            intervals, detail = stationary_event_interval(model, masks, accuracy)
            p0 = ratio_interval(intervals[0], intervals[1])
            ulo = Fraction(uniform_prefix, 1 << level)
            uhi = Fraction(uniform_prefix + 1, 1 << level)
            if uhi <= p0[0]:
                bit = 0
                decided = True
            elif ulo >= p0[1]:
                bit = 1
                decided = True
            else:
                continue
            prefix.append(bit)
            trace.append({
                "coordinate": coordinate,
                "decision_level": level,
                "uniform_bits": format(uniform_prefix, f"0{level}b"),
                "uniform_interval": [frac(ulo), frac(uhi)],
                "conditional_zero_interval": [frac(p0[0]), frac(p0[1])],
                "selected_bit": bit,
                "child_zero_mass_interval": [frac(intervals[0][0]), frac(intervals[0][1])],
                "child_one_mass_interval": [frac(intervals[1][0]), frac(intervals[1][1])],
                "oracle": {
                    "s": frac(detail["s"]),
                    "mixing_error": frac(detail["mixing_error"]),
                    "accuracy": frac(detail["requested_accuracy"]),
                    "quadrature_delta_bits": detail["delta_bits"],
                    "internal_precision_bits": detail["precision_bits"],
                    "positive_nodes": detail["node_count"],
                },
            })
            break
        if not decided:
            raise ArithmeticError(f"lazy sampler demo exceeded level cap {demo_level_cap}; no sample returned")

    return {"sample": prefix, "trace": trace, "minorization_eta": frac(eta),
            "minorization_T": frac(mix["T"]),
            "bit_source": "independent fair bits via secrets.randbits(1)"}


def main() -> None:
    start = time.time()
    model = make_fixture()
    model.validate()
    # A certified full-cylinder stationary expectation for the n=3 fixture.
    all_one = event_mask_for_prefix((1, 1, 1), model.n)
    expectation_intervals, expectation_detail = stationary_event_interval(
        model, [all_one], Fraction(1, 1 << 12))
    receipt = {
        "status": "certified_stationary_prefix_sample_pending",
        "elapsed_seconds": time.time() - start,
        "input": {
            "n": model.n,
            "k": model.k,
            "flip_up": [frac(x) for x in model.up],
            "flip_down": [frac(x) for x in model.down],
            "hazards_by_channel_coordinate_state": [
                [[frac(x) for x in pair] for pair in channel]
                for channel in model.hazards],
            "reset_one_probabilities": [[frac(x) for x in row] for row in model.reset_one],
            "initial_one_probabilities": [frac(x) for x in model.initial_one],
            "observable": "indicator{x=(1,1,1)}",
        },
        "stationary_expectation": {
            "event": "all three coordinates equal one",
            "lower": frac(expectation_intervals[0][0]),
            "upper": frac(expectation_intervals[0][1]),
            "width": frac(expectation_intervals[0][1] - expectation_intervals[0][0]),
            "abel_s": frac(expectation_detail["s"]),
            "abel_mixing_error": frac(expectation_detail["mixing_error"]),
            "quadrature_delta_bits": expectation_detail["delta_bits"],
            "internal_precision_bits": expectation_detail["precision_bits"],
            "positive_nodes": expectation_detail["node_count"],
            "woodbury": [
                {key: (frac(value) if isinstance(value, Fraction) else value)
                 for key, value in row.items()}
                for row in expectation_detail["event_details"]],
        },
        "minorization": {
            "method": "one-unit-time no-reset lower bound times product base-chain minimum entries",
            "T": frac(mixing_certificate(model)["T"]),
            "eta": frac(mixing_certificate(model)["eta"]),
            "abel_bias_bound": "2*G*s*T/eta for |g|<=G",
            "Amax": frac(model.amax),
            "base_spectral_trace_bound": frac(model.lambda_trace_bound),
        },
        "lazy_exact_sample": None,
        "scope": "a completed path agrees with the uncapped mathematical exact sampler under ideal fair bits; conditioning capped runs on success need not be stationary; the implementation has explicit precision and node caps and fails closed",
    }
    path = Path(__file__).with_name("certified_receipt.json")
    path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"],
                      "stationary_expectation": receipt["stationary_expectation"],
                      "receipt": str(path)}, indent=2), flush=True)
    try:
        sample_result = lazy_exact_sample(model, demo_level_cap=24)
        receipt["status"] = "certified_stationary_prefix_and_lazy_sample"
        receipt["lazy_exact_sample"] = sample_result
    except (ArithmeticError, ValueError) as exc:
        receipt["status"] = "certified_stationary_prefix_sample_unfinished"
        receipt["lazy_sample_failure"] = str(exc)
    receipt["elapsed_seconds"] = time.time() - start
    path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
