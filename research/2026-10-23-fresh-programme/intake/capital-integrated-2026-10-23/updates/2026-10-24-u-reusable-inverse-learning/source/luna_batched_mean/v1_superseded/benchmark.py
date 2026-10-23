#!/usr/bin/env python3
"""Exact finite replay for the frozen logistic inverse-sampling challenge.

All decisions use rational/integer arithmetic.  This is a deterministic PRNG
fixture; the ideal sampler theorem is conditional on independent fair bits.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import random
import sys
import time
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
H = 4
K = 6
N = 8
TASKS = 8
DRAWS_PER_TASK = 16
EPS = Fraction(1, 8)
SCALE = Fraction(3, 4)
ZERO = Fraction(0)
ONE = Fraction(1)
HALF = Fraction(1, 2)
QUARTER = Fraction(1, 4)
GRID = 1 << H
TOTAL_POINTS = GRID * GRID


def fb(q: Fraction) -> int:
    """Bits needed for the magnitude of one integer, with zero using one bit."""
    return max(1, abs(q).bit_length())


def qjson(q: Fraction) -> list[str]:
    return [str(q.numerator), str(q.denominator)]


def from_qjson(x: list[str]) -> Fraction:
    return Fraction(int(x[0]), int(x[1]))


class Ledger:
    def __init__(self, name: str):
        self.name = name
        self.ops = Counter()
        self.int_bits = Counter()
        self.max_int_bits = 0
        self.gcd_count = 0
        self.rational_results = 0
        self.max_rational_numerator_bits = 0
        self.max_rational_denominator_bits = 0
        self.rational_payload_binary_bytes = 0
        self.events: list[dict[str, Any]] = []
        self.counters = Counter()
        self.size_records: list[tuple[int, int]] = []

    def event(self, kind: str, **fields: Any) -> None:
        self.events.append({"kind": kind, **fields})

    def note_int(self, n: int, role: str = "integer") -> None:
        b = max(1, abs(n).bit_length())
        self.int_bits[role + "_bits_sum"] += b
        self.int_bits[role + "_bits_count"] += 1
        self.max_int_bits = max(self.max_int_bits, b)

    def note_q(self, q: Fraction, role: str) -> None:
        bn, bd = fb(q.numerator), fb(q.denominator)
        self.int_bits[role + "_numerator_bits_sum"] += bn
        self.int_bits[role + "_denominator_bits_sum"] += bd
        self.int_bits[role + "_count"] += 1
        self.max_int_bits = max(self.max_int_bits, bn, bd)
        self.max_rational_numerator_bits = max(self.max_rational_numerator_bits, bn)
        self.max_rational_denominator_bits = max(self.max_rational_denominator_bits, bd)

    def make(self, n: int, d: int, op: str, temp: tuple[int, ...] = ()) -> Fraction:
        if d == 0:
            raise ZeroDivisionError
        self.ops[op] += 1
        self.rational_results += 1
        for z in temp:
            self.note_int(z, "temporary_" + op)
        if d < 0:
            n, d = -n, -d
        g = math.gcd(abs(n), d)
        self.gcd_count += 1
        self.note_int(g, "gcd_argument_result")
        n //= g
        d //= g
        self.note_int(n, "result_" + op)
        self.note_int(d, "result_" + op)
        self.max_rational_numerator_bits = max(self.max_rational_numerator_bits, fb(n))
        self.max_rational_denominator_bits = max(self.max_rational_denominator_bits, fb(d))
        self.rational_payload_binary_bytes += (abs(n).bit_length()+7)//8 + (d.bit_length()+7)//8
        return Fraction(n, d)

    def add(self, a: Fraction, b: Fraction) -> Fraction:
        x, y, d = a.numerator * b.denominator, b.numerator * a.denominator, a.denominator * b.denominator
        self.note_q(a, "operand_add"); self.note_q(b, "operand_add")
        return self.make(x + y, d, "add", (x, y, d, x + y))

    def sub(self, a: Fraction, b: Fraction) -> Fraction:
        x, y, d = a.numerator * b.denominator, b.numerator * a.denominator, a.denominator * b.denominator
        self.note_q(a, "operand_sub"); self.note_q(b, "operand_sub")
        return self.make(x - y, d, "sub", (x, y, d, x - y))

    def mul(self, a: Fraction, b: Fraction) -> Fraction:
        x, d = a.numerator * b.numerator, a.denominator * b.denominator
        self.note_q(a, "operand_mul"); self.note_q(b, "operand_mul")
        return self.make(x, d, "mul", (x, d))

    def div(self, a: Fraction, b: Fraction) -> Fraction:
        if b.numerator == 0:
            raise ZeroDivisionError
        x, d = a.numerator * b.denominator, a.denominator * b.numerator
        self.note_q(a, "operand_div"); self.note_q(b, "operand_div")
        return self.make(x, d, "div", (x, d))

    def cmp(self, a: Fraction, b: Fraction, op: str = "compare") -> int:
        x, y = a.numerator * b.denominator, b.numerator * a.denominator
        self.ops[op] += 1
        self.note_q(a, "operand_" + op); self.note_q(b, "operand_" + op)
        self.note_int(x, "temporary_" + op); self.note_int(y, "temporary_" + op)
        return (x > y) - (x < y)

    def pow(self, a: Fraction, k: int) -> Fraction:
        out = ONE
        for _ in range(k):
            out = self.mul(out, a)
        return out

    def summary(self) -> dict[str, Any]:
        return {
            "explicit_exact_arithmetic_operations": dict(sorted(self.ops.items())),
            "gcd_reductions_requested_by_explicit_rational_ops": self.gcd_count,
            "exact_integer_operand_temporary_result_bit_accounting": dict(sorted(self.int_bits.items())),
            "maximum_integer_bit_length_seen": self.max_int_bits,
            "maximum_reduced_rational_numerator_bits": self.max_rational_numerator_bits,
            "maximum_reduced_rational_denominator_bits": self.max_rational_denominator_bits,
            "cumulative_binary_payload_bytes_of_reduced_rational_results": self.rational_payload_binary_bytes,
        }


class BitSource:
    """A finite reproducible tape; seed is not part of public output."""
    def __init__(self, seed: int, tape: str | None = None):
        self.rng = random.Random(seed) if tape is None else None
        self.tape = tape
        self.pos = 0
        self.generated: list[str] = []
        self.reason_counts = Counter()
        self.segments: list[dict[str, Any]] = []

    def bit(self, reason: str) -> int:
        start = self.pos
        if self.tape is None:
            b = self.rng.getrandbits(1)
            self.generated.append(str(b))
        else:
            if self.pos >= len(self.tape):
                raise RuntimeError("public random tape exhausted")
            b = int(self.tape[self.pos])
        self.pos += 1
        self.reason_counts[reason] += 1
        if self.segments and self.segments[-1]["reason"] == reason and self.segments[-1]["end"] == start:
            self.segments[-1]["end"] = self.pos
        else:
            self.segments.append({"reason": reason, "start": start, "end": self.pos})
        return b

    def tape_string(self) -> str:
        if self.tape is None:
            return "".join(self.generated)
        return self.tape[:self.pos]


class LazyUniform:
    def __init__(self, source: BitSource, reason: str):
        self.source = source
        self.reason = reason
        self.prefix = 0
        self.bits = 0
        self.comparisons: list[dict[str, Any]] = []

    def lt(self, q: Fraction) -> bool:
        before = self.bits
        while True:
            scale = 1 << self.bits
            low_num = self.prefix
            high_num = self.prefix + 1
            # Compare [low, high) to q with integer cross-products. At high==q,
            # every represented value is strictly below q; at low==q it is >=q.
            if high_num * q.denominator <= q.numerator * scale:
                ans = True
                break
            if low_num * q.denominator >= q.numerator * scale:
                ans = False
                break
            bit = self.source.bit(self.reason)
            self.prefix = (self.prefix << 1) | bit
            self.bits += 1
        self.comparisons.append({"threshold": qjson(q), "result_uniform_lt": ans,
                                 "bits_before": before, "bits_after": self.bits})
        return ans

    def categorical(self, boundaries: list[Fraction]) -> int:
        lo, hi = 0, len(boundaries)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.lt(boundaries[mid]):
                hi = mid
            else:
                lo = mid + 1
        return lo


def randbelow(src: BitSource, n: int, reason: str) -> tuple[int, dict[str, Any]]:
    if n <= 0:
        raise ValueError(n)
    if n == 1:
        return 0, {"bits": 0, "attempts": 0, "rejected_integers": []}
    k = (n - 1).bit_length()
    attempts = 0
    rejected = []
    total_bits = 0
    while True:
        attempts += 1
        x = 0
        for _ in range(k):
            x = (x << 1) | src.bit(reason)
            total_bits += 1
        if x < n:
            return x, {"bits": total_bits, "attempts": attempts, "rejected_integers": rejected, "selected_integer": x}
        rejected.append(x)


NodeKey = tuple[int, int, int]  # depth, first row, first column


@dataclass
class Node:
    key: NodeKey
    parent: NodeKey | None
    rows: tuple[int, int]  # half-open grid-index range
    cols: tuple[int, int]
    raw: tuple[Fraction, Fraction]
    interval: tuple[Fraction, Fraction]


def grid_a(i: int) -> Fraction:
    return Fraction(97 + 2 * i, 32)


def grid_b(j: int) -> Fraction:
    return Fraction(19 + 6 * j, 128)


def node_ranges(key: NodeKey) -> tuple[tuple[int, int], tuple[int, int]]:
    depth, i0, j0 = key
    side = 1 << (H - depth)
    return (i0, i0 + side), (j0, j0 + side)


def rational_interval_for_node(key: NodeKey, parent: tuple[Fraction, Fraction] | None,
                                ledger: Ledger) -> tuple[Node, int]:
    depth, i0, j0 = key
    rr, cc = node_ranges(key)
    a_lo, a_hi = grid_a(rr[0]), grid_a(rr[1] - 1)
    b_lo, b_hi = grid_b(cc[0]), grid_b(cc[1] - 1)
    if depth == H:
        u = b_lo
        a = a_lo
        for _ in range(K):
            u = ledger.mul(a, ledger.mul(u, ledger.sub(ONE, u)))
        raw = (u, u)
    else:
        u_lo, u_hi = b_lo, b_hi
        for _ in range(K):
            g0 = ledger.mul(u_lo, ledger.sub(ONE, u_lo))
            g1 = ledger.mul(u_hi, ledger.sub(ONE, u_hi))
            g_lo = g0 if ledger.cmp(g0, g1, "compare_endpoint") <= 0 else g1
            has_half = ledger.cmp(u_lo, HALF, "compare_half") <= 0 and ledger.cmp(HALF, u_hi, "compare_half") <= 0
            g_hi = QUARTER if has_half else (g0 if ledger.cmp(g0, g1, "compare_endpoint") >= 0 else g1)
            u_lo = ledger.mul(a_lo, g_lo)
            u_hi = ledger.mul(a_hi, g_hi)
            # Exact range is contained in [0,1] for all recurrence steps.
        raw = (u_lo, u_hi)
    lo, hi = raw
    if parent is not None:
        if ledger.cmp(lo, parent[0], "compare_intersection") < 0:
            lo = parent[0]
        if ledger.cmp(hi, parent[1], "compare_intersection") > 0:
            hi = parent[1]
    if ledger.cmp(lo, ZERO, "compare_clip") < 0:
        lo = ZERO
    if ledger.cmp(hi, ONE, "compare_clip") > 0:
        hi = ONE
    node = Node(key, None, rr, cc, raw, (lo, hi))
    return node, K


def children(key: NodeKey) -> list[NodeKey]:
    depth, i0, j0 = key
    if depth >= H:
        return []
    side = 1 << (H - depth - 1)
    return [(depth + 1, i0 + di * side, j0 + dj * side)
            for di in range(2) for dj in range(2)]


def point_f(i: int, j: int, ledger: Ledger) -> Fraction:
    a, u = grid_a(i), grid_b(j)
    for _ in range(K):
        u = ledger.mul(a, ledger.mul(u, ledger.sub(ONE, u)))
    return u


def likelihood(p: Fraction, s: int, n: int, ledger: Ledger) -> Fraction:
    return ledger.mul(ledger.pow(p, s), ledger.pow(ledger.sub(ONE, p), n - s))


def bounds_for_node(interval: tuple[Fraction, Fraction], s: int, n: int,
                    ledger: Ledger) -> tuple[Fraction, Fraction]:
    plo = ledger.add(EPS, ledger.mul(SCALE, interval[0]))
    phi = ledger.add(EPS, ledger.mul(SCALE, interval[1]))
    w0, w1 = likelihood(plo, s, n, ledger), likelihood(phi, s, n, ledger)
    low = w0 if ledger.cmp(w0, w1, "compare_likelihood") <= 0 else w1
    high = w0 if ledger.cmp(w0, w1, "compare_likelihood") >= 0 else w1
    mode = Fraction(s, n)
    if ledger.cmp(plo, mode, "compare_mode") <= 0 and ledger.cmp(mode, phi, "compare_mode") <= 0:
        wm = likelihood(mode, s, n, ledger)
        if ledger.cmp(wm, high, "compare_likelihood") > 0:
            high = wm
    return low, high


class InferenceMethod:
    def __init__(self, name: str, seed: int, tape: str | None = None):
        self.name = name
        self.ledger = Ledger(name)
        self.bits = BitSource(seed, tape)
        self.nodes: dict[NodeKey, Node] = {}
        self.active: set[NodeKey] = set()
        self.bounds: dict[tuple[NodeKey, int, int], tuple[Fraction, Fraction]] = {}
        self.cdf_cache: dict[tuple[tuple[NodeKey, ...], int, int], tuple[list[NodeKey], list[Fraction]]] = {}
        self.point_cache: dict[tuple[int, int], Fraction] = {}
        self.outputs: list[list[int]] = []
        self.task_counts: list[int] = []
        self.total_proposals = 0
        self.accepts = 0
        self.rejects = 0
        self.refinements = 0
        self.proposal_attempts = 0
        self.wall_seconds = 0.0

    def create_node(self, key: NodeKey, parent_key: NodeKey | None) -> None:
        if key in self.nodes:
            self.ledger.counters["node_cache_hits"] += 1
            self.ledger.event("node_cache_hit", node=key)
            return
        par = self.nodes[parent_key].interval if parent_key is not None else None
        start = time.perf_counter()
        node, steps = rational_interval_for_node(key, par, self.ledger)
        elapsed = time.perf_counter() - start
        node.parent = parent_key
        self.nodes[key] = node
        self.ledger.counters["source_calls"] += 1
        self.ledger.counters["recurrence_steps"] += steps
        self.ledger.counters["node_interval_evaluations"] += 1
        self.ledger.counters["node_eval_wall_seconds"] += elapsed
        self.ledger.event("node_created", node=list(key), parent=None if parent_key is None else list(parent_key),
                          grid_rows=list(node.rows), grid_cols=list(node.cols),
                          coordinate_hull_a=[qjson(grid_a(node.rows[0])), qjson(grid_a(node.rows[1]-1))],
                          coordinate_hull_b=[qjson(grid_b(node.cols[0])), qjson(grid_b(node.cols[1]-1))],
                          raw=[qjson(node.raw[0]), qjson(node.raw[1])],
                          parent_intersected=[qjson(node.interval[0]), qjson(node.interval[1])],
                          recurrence_steps=steps,
                          endpoint_bits=[[fb(x.numerator), fb(x.denominator)] for x in node.interval])
        if key[0] == H:
            self.point_cache[(key[1], key[2])] = node.interval[0]
        self.active.add(key)

    def init_tree(self) -> None:
        self.create_node((0, 0, 0), None)

    def ensure_bounds(self, key: NodeKey, s: int, n: int) -> tuple[Fraction, Fraction]:
        ident = (key, s, n)
        if ident in self.bounds:
            self.ledger.counters["likelihood_bound_cache_hits"] += 1
            return self.bounds[ident]
        self.ledger.counters["likelihood_bound_cache_misses"] += 1
        start = time.perf_counter()
        b = bounds_for_node(self.nodes[key].interval, s, n, self.ledger)
        self.ledger.counters["likelihood_bound_wall_seconds"] += time.perf_counter() - start
        self.bounds[ident] = b
        self.ledger.counters["likelihood_conversions"] += 1
        self.ledger.event("likelihood_bound", node=list(key), s=s, n=n,
                          lower=qjson(b[0]), upper=qjson(b[1]))
        return b

    def active_signature(self) -> tuple[NodeKey, ...]:
        return tuple(sorted(self.active, key=lambda x: (x[1], x[2], x[0])))

    def cdf(self, s: int, n: int) -> tuple[list[NodeKey], list[Fraction]]:
        sig = self.active_signature()
        ck = (sig, s, n)
        if ck in self.cdf_cache:
            self.ledger.counters["proposal_cdf_cache_hits"] += 1
            return self.cdf_cache[ck]
        self.ledger.counters["proposal_cdf_cache_misses"] += 1
        weights = []
        for key in sig:
            node = self.nodes[key]
            rows = node.rows[1] - node.rows[0]
            cols = node.cols[1] - node.cols[0]
            prior = Fraction(rows * cols, TOTAL_POINTS)
            upper = self.ensure_bounds(key, s, n)[1]
            weights.append(self.ledger.mul(prior, upper))
        total = ZERO
        for w in weights:
            total = self.ledger.add(total, w)
        cumulative = ZERO
        boundaries: list[Fraction] = []
        for w in weights[:-1]:
            cumulative = self.ledger.add(cumulative, w)
            boundaries.append(self.ledger.div(cumulative, total))
        self.cdf_cache[ck] = (list(sig), boundaries)
        return list(sig), boundaries

    def choose_proposal_cell(self, s: int, n: int) -> tuple[NodeKey, dict[str, Any]]:
        keys, boundaries = self.cdf(s, n)
        start = self.bits.pos
        u = LazyUniform(self.bits, "proposal_cdf")
        idx = u.categorical(boundaries)
        return keys[idx], {"start": start, "end": self.bits.pos, "comparisons": u.comparisons,
                           "selected_index": idx, "active_leaf_count": len(keys)}

    def draw_point_in_node(self, key: NodeKey) -> tuple[int, int, dict[str, Any]]:
        node = self.nodes[key]
        nr, nc = node.rows[1] - node.rows[0], node.cols[1] - node.cols[0]
        start = self.bits.pos
        rank, info = randbelow(self.bits, nr * nc, "within_cell")
        i = node.rows[0] + rank // nc
        j = node.cols[0] + rank % nc
        return i, j, {"start": start, "end": self.bits.pos, **info, "point": [i, j]}

    def split(self, key: NodeKey) -> list[NodeKey]:
        if key not in self.active:
            raise RuntimeError("attempt to split non-leaf")
        kids = children(key)
        if not kids:
            raise RuntimeError("cannot split singleton")
        self.active.remove(key)
        for child in kids:
            self.create_node(child, key)
        self.refinements += 1
        self.ledger.counters["refinement_splits"] += 1
        self.ledger.event("split", parent=list(key), children=[list(x) for x in kids])
        return kids

    def posterior_bounds(self, s: int, n: int) -> tuple[Fraction, Fraction]:
        zl = zu = ZERO
        for key in self.active_signature():
            node = self.nodes[key]
            prior = Fraction((node.rows[1]-node.rows[0]) * (node.cols[1]-node.cols[0]), TOTAL_POINTS)
            lo, hi = self.ensure_bounds(key, s, n)
            zl = self.ledger.add(zl, self.ledger.mul(prior, lo))
            zu = self.ledger.add(zu, self.ledger.mul(prior, hi))
        return zl, zu

    def run_lead_task(self, s: int) -> list[int]:
        out = []
        for draw_idx in range(DRAWS_PER_TASK):
            self.total_proposals += 1
            self.proposal_attempts += 1
            key, cinfo = self.choose_proposal_cell(s, N)
            i, j, pinfo = self.draw_point_in_node(key)
            u = LazyUniform(self.bits, "acceptance_threshold")
            original_hi = self.ensure_bounds(key, s, N)[1]
            pinned = original_hi
            self.ledger.event("proposal", method="lead_demand_refinement", s=s, n=N, draw=draw_idx,
                              cell=list(key), point=[i,j], proposal_cdf=cinfo, point_draw=pinfo,
                              pinned_u_old=qjson(pinned))
            current = key
            while True:
                lo, hi = self.ensure_bounds(current, s, N)
                low_ratio = self.ledger.div(lo, pinned)
                high_ratio = self.ledger.div(hi, pinned)
                before = self.bits.pos
                below_low = u.lt(low_ratio)
                after_low = self.bits.pos
                if below_low:
                    decision = "accept"
                    break
                below_high = u.lt(high_ratio)
                after_high = self.bits.pos
                if not below_high:
                    decision = "reject"
                    break
                # The same actual lazy uniform has now been proved to lie in
                # [low_ratio, high_ratio); only this condition triggers refinement.
                if current[0] == H:
                    raise AssertionError("singleton likelihood interval failed to decide")
                kids = self.split(current)
                side = 1 << (H-current[0]-1)
                current = next(k for k in kids if k[1] <= i < k[1]+side and k[2] <= j < k[2]+side)
                self.ledger.event("threshold_refine", draw=draw_idx, from_node=list(kids[0][:1])+list(current[1:]),
                                  chosen_child=list(current), low_ratio=qjson(low_ratio),
                                  high_ratio=qjson(high_ratio), bits_start=before,
                                  bits_after_low=after_low, bits_after_high=after_high,
                                  comparisons=copy.deepcopy(u.comparisons[-2:]))
            self.ledger.event("threshold_decision", draw=draw_idx, selected_cell=list(key), final_node=list(current),
                              pinned_u_old=qjson(pinned), lower_ratio=qjson(low_ratio),
                              upper_ratio=qjson(high_ratio), decision=decision,
                              bits_start=before, bits_end=self.bits.pos,
                              comparisons=copy.deepcopy(u.comparisons[-(2 if decision=="reject" else 1):]))
            if decision == "accept":
                self.accepts += 1
                r = 16*i + j
                out.append(r)
                self.ledger.event("posterior_output", task_s=s, draw=draw_idx, row_major_index=r,
                                  point=[i,j], proposals_used=1)
                break
            self.rejects += 1
            # Rejected proposal restarts from the posterior envelope on current leaves.
            self.ledger.event("proposal_rejected", task_s=s, draw=draw_idx, point=[i,j])
            # The loop around a single draw must retry with a fresh proposal.
            # Keep this draw index fixed but increment total attempts.
            while True:
                self.total_proposals += 1
                self.proposal_attempts += 1
                key, cinfo = self.choose_proposal_cell(s, N)
                i, j, pinfo = self.draw_point_in_node(key)
                u = LazyUniform(self.bits, "acceptance_threshold")
                pinned = self.ensure_bounds(key, s, N)[1]
                self.ledger.event("proposal", method="lead_demand_refinement", s=s, n=N, draw=draw_idx,
                                  cell=list(key), point=[i,j], proposal_cdf=cinfo, point_draw=pinfo,
                                  pinned_u_old=qjson(pinned), retry=True)
                current = key
                while True:
                    lo, hi = self.ensure_bounds(current, s, N)
                    low_ratio = self.ledger.div(lo, pinned)
                    high_ratio = self.ledger.div(hi, pinned)
                    before = self.bits.pos
                    below_low = u.lt(low_ratio)
                    after_low = self.bits.pos
                    if below_low:
                        decision = "accept"
                        break
                    below_high = u.lt(high_ratio)
                    after_high = self.bits.pos
                    if not below_high:
                        decision = "reject"
                        break
                    if current[0] == H:
                        raise AssertionError("singleton likelihood interval failed to decide")
                    old = current
                    kids = self.split(old)
                    side = 1 << (H-old[0]-1)
                    current = next(k for k in kids if k[1] <= i < k[1]+side and k[2] <= j < k[2]+side)
                    self.ledger.event("threshold_refine", draw=draw_idx, from_node=list(old), chosen_child=list(current),
                                      low_ratio=qjson(low_ratio), high_ratio=qjson(high_ratio),
                                      bits_start=before, bits_after_low=after_low, bits_after_high=after_high,
                                      comparisons=copy.deepcopy(u.comparisons[-2:]))
                self.ledger.event("threshold_decision", draw=draw_idx, selected_cell=list(key), final_node=list(current),
                                  pinned_u_old=qjson(pinned), lower_ratio=qjson(low_ratio),
                                  upper_ratio=qjson(high_ratio), decision=decision,
                                  bits_start=before, bits_end=self.bits.pos,
                                  comparisons=copy.deepcopy(u.comparisons[-(2 if decision=="reject" else 1):]))
                if decision == "accept":
                    self.accepts += 1
                    r = 16*i + j
                    out.append(r)
                    self.ledger.event("posterior_output", task_s=s, draw=draw_idx, row_major_index=r,
                                      point=[i,j], proposals_used=self.total_proposals)
                    break
                self.rejects += 1
                self.ledger.event("proposal_rejected", task_s=s, draw=draw_idx, point=[i,j])
            break
        return out

    def run_lead(self) -> dict[str, Any]:
        start = time.perf_counter()
        self.init_tree()
        s = 3
        for t in range(TASKS):
            self.task_counts.append(s)
            self.ledger.event("task_start", task=t, s=s, n=N, draws=DRAWS_PER_TASK)
            task_out = []
            for draw_idx in range(DRAWS_PER_TASK):
                # The sampler routine handles arbitrary rejection retries.
                task_out.extend(self.run_one_lead_draw(s, draw_idx))
            self.outputs.append(task_out)
            self.ledger.event("task_complete", task=t, s=s, outputs=task_out)
            if t + 1 < TASKS:
                s = (s + task_out[-1] + 1) % 9
        self.wall_seconds = time.perf_counter() - start
        return self.result()

    def run_one_lead_draw(self, s: int, draw_idx: int) -> list[int]:
        while True:
            self.total_proposals += 1
            self.proposal_attempts += 1
            key, cinfo = self.choose_proposal_cell(s, N)
            i, j, pinfo = self.draw_point_in_node(key)
            u = LazyUniform(self.bits, "acceptance_threshold")
            pinned = self.ensure_bounds(key, s, N)[1]
            self.ledger.event("proposal", method="lead_demand_refinement", s=s, n=N, draw=draw_idx,
                              cell=list(key), point=[i,j], proposal_cdf=cinfo, point_draw=pinfo,
                              pinned_u_old=qjson(pinned))
            current = key
            while True:
                lo, hi = self.ensure_bounds(current, s, N)
                low_ratio, high_ratio = self.ledger.div(lo, pinned), self.ledger.div(hi, pinned)
                before = self.bits.pos
                below_low = u.lt(low_ratio)
                after_low = self.bits.pos
                if below_low:
                    decision = "accept"
                else:
                    below_high = u.lt(high_ratio)
                    after_high = self.bits.pos
                    if not below_high:
                        decision = "reject"
                    else:
                        if current[0] == H:
                            raise AssertionError("singleton likelihood interval failed to decide")
                        old = current
                        kids = self.split(old)
                        side = 1 << (H-old[0]-1)
                        current = next(k for k in kids if k[1] <= i < k[1]+side and k[2] <= j < k[2]+side)
                        self.ledger.event("threshold_refine", draw=draw_idx, from_node=list(old),
                                          chosen_child=list(current), low_ratio=qjson(low_ratio),
                                          high_ratio=qjson(high_ratio), bits_start=before,
                                          bits_after_low=after_low, bits_after_high=after_high,
                                          comparisons=copy.deepcopy(u.comparisons[-2:]))
                        continue
                self.ledger.event("threshold_decision", draw=draw_idx, selected_cell=list(key), final_node=list(current),
                                  pinned_u_old=qjson(pinned), lower_ratio=qjson(low_ratio),
                                  upper_ratio=qjson(high_ratio), decision=decision,
                                  bits_start=before, bits_end=self.bits.pos,
                                  comparisons=copy.deepcopy(u.comparisons[-(2 if decision=="reject" else 1):]))
                if decision == "accept":
                    self.accepts += 1
                    r = 16*i+j
                    self.ledger.event("posterior_output", task_s=s, draw=draw_idx, row_major_index=r,
                                      point=[i,j], proposals_used=self.total_proposals)
                    return [r]
                self.rejects += 1
                self.ledger.event("proposal_rejected", task_s=s, draw=draw_idx, point=[i,j])
                break

    def result(self) -> dict[str, Any]:
        zlzu = []
        for s in sorted(set(self.task_counts)):
            zl, zu = self.posterior_bounds(s, N)
            zlzu.append({"s":s,"z_lower":qjson(zl),"z_upper":qjson(zu),
                         "lower_over_upper":qjson(self.ledger.div(zl,zu))})
        nodes_serial = sum(1 for _ in self.nodes)
        node_payload = sum(len(str(qjson(v))) for node in self.nodes.values() for v in (node.raw[0],node.raw[1],node.interval[0],node.interval[1]))
        bounds_payload = sum(len(str(qjson(x))) for pair in self.bounds.values() for x in pair)
        extra_counters = {
            "retained_node_count":len(self.nodes), "active_leaf_count_final":len(self.active),
            "cached_likelihood_bound_count":len(self.bounds), "proposal_cdf_cache_entries":len(self.cdf_cache),
            "node_exact_fraction_json_characters":node_payload,"likelihood_bound_fraction_json_characters":bounds_payload,
            "node_endpoint_binary_payload_bytes":sum((abs(q.numerator).bit_length()+7)//8+(q.denominator.bit_length()+7)//8
                                                       for node in self.nodes.values() for q in (*node.raw,*node.interval)),
            "likelihood_bound_binary_payload_bytes":sum((abs(q.numerator).bit_length()+7)//8+(q.denominator.bit_length()+7)//8
                                                           for pair in self.bounds.values() for q in pair),
            "proposal_cdf_boundary_binary_payload_bytes":sum((abs(q.numerator).bit_length()+7)//8+(q.denominator.bit_length()+7)//8
                                                               for _, boundaries in self.cdf_cache.values() for q in boundaries),
            "random_bits_consumed":self.bits.pos,
            "random_bits_by_use":dict(self.bits.reason_counts),
            "ideal_bit_tape_binary_bytes_lower_bound":(self.bits.pos+7)//8,
            "actual_ascii_bit_tape_bytes":len(self.bits.tape_string()),
            "proposal_attempts":self.proposal_attempts,"posterior_draws":sum(map(len,self.outputs)),
            "acceptances":self.accepts,"rejections":self.rejects,"refinement_splits":self.refinements,
            "total_source_calls_including_direct_points":self.ledger.counters.get("source_calls",0)+self.ledger.counters.get("point_source_calls",0),
            "total_recurrence_steps_including_direct_points":self.ledger.counters.get("recurrence_steps",0)+self.ledger.counters.get("point_recurrence_steps",0),
        }
        counters = dict(self.ledger.counters)
        counters.update(extra_counters)
        return {"method":self.name,"task_counts":self.task_counts,"outputs":self.outputs,
                "posterior_normalizer_interval_by_observed_s":zlzu,
                "counters":counters,"rational_ledger":self.ledger.summary(),
                "wall_seconds_including_exact_logic":self.wall_seconds,
                "bit_tape":self.bits.tape_string(),"bit_segments":self.bits.segments,
                "events":self.ledger.events}


class LeadMethod(InferenceMethod):
    pass


class OSStarMethod(InferenceMethod):
    def split_rejected_original(self, key: NodeKey) -> None:
        if key[0] < H:
            self.split(key)

    def run(self, task_counts: list[int]) -> dict[str, Any]:
        start = time.perf_counter()
        self.init_tree()
        self.task_counts = list(task_counts)
        for ti, s in enumerate(task_counts):
            task_out=[]
            self.ledger.event("task_start", task=ti, s=s, n=N, draws=DRAWS_PER_TASK)
            for di in range(DRAWS_PER_TASK):
                while True:
                    self.proposal_attempts += 1
                    self.total_proposals += 1
                    key,cinfo=self.choose_proposal_cell(s,N)
                    i,j,pinfo=self.draw_point_in_node(key)
                    if (i,j) in self.point_cache:
                        fval=self.point_cache[(i,j)]
                        self.ledger.counters["point_evaluation_cache_hits"]+=1
                    else:
                        fval=point_f(i,j,self.ledger)
                        self.point_cache[(i,j)]=fval
                        self.ledger.counters["point_source_calls"]+=1
                        self.ledger.counters["point_recurrence_steps"]+=K
                        self.ledger.event("point_evaluation", point=[i,j], value=qjson(fval), recurrence_steps=K)
                    # The selected proposal cell's exact upper likelihood is pinned.
                    u_bound=self.ensure_bounds(key,s,N)[1]
                    p= self.ledger.add(EPS,self.ledger.mul(SCALE,fval))
                    w=likelihood(p,s,N,self.ledger)
                    ratio=self.ledger.div(w,u_bound)
                    u=LazyUniform(self.bits,"acceptance_threshold")
                    startbit=self.bits.pos
                    accept=u.lt(ratio)
                    self.ledger.event("osstar_trial", task=ti, draw=di, s=s, cell=list(key),point=[i,j],
                                      proposal_cdf=cinfo,point_draw=pinfo, upper=qjson(u_bound),
                                      exact_likelihood=qjson(w),acceptance_ratio=qjson(ratio),
                                      accepted=accept,bits_start=startbit,bits_end=self.bits.pos,
                                      comparisons=u.comparisons)
                    if accept:
                        self.accepts+=1
                        r=16*i+j;task_out.append(r)
                        self.ledger.event("posterior_output",task=ti,task_s=s,draw=di,row_major_index=r,point=[i,j])
                        break
                    self.rejects+=1
                    self.ledger.event("proposal_rejected",task=ti,task_s=s,draw=di,point=[i,j])
                    # Standard OS*: retain the exact rejected point result, then
                    # split the original selected proposal region for future draws.
                    self.split_rejected_original(key)
            self.outputs.append(task_out)
            self.ledger.event("task_complete", task=ti, s=s, outputs=task_out)
        self.wall_seconds=time.perf_counter()-start
        return self.result()


class FullGridMethod:
    def __init__(self, seed: int, tape: str | None = None):
        self.name="full_grid_exact_cache"
        self.ledger=Ledger(self.name)
        self.bits=BitSource(seed,tape)
        self.table: list[list[Fraction]]=[]
        self.weight_cache: dict[int,tuple[list[Fraction],list[Fraction]]]={}
        self.outputs=[]
        self.task_counts=[]
        self.wall_seconds=0.0

    def run(self, task_counts: list[int]) -> dict[str,Any]:
        start=time.perf_counter()
        for i in range(GRID):
            row=[]
            for j in range(GRID):
                f=point_f(i,j,self.ledger)
                row.append(f)
                self.ledger.counters["source_calls"]+=1
                self.ledger.counters["recurrence_steps"]+=K
            self.table.append(row)
        self.ledger.event("full_grid_table_built", points=TOTAL_POINTS, recurrence_steps=TOTAL_POINTS*K,
                          table_sha256=hashlib.sha256(json.dumps([[qjson(x) for x in row] for row in self.table],separators=(",",":")).encode()).hexdigest())
        self.task_counts=list(task_counts)
        for ti,s in enumerate(task_counts):
            if s not in self.weight_cache:
                startw=time.perf_counter()
                weights=[]
                for i in range(GRID):
                    for j in range(GRID):
                        p=self.ledger.add(EPS,self.ledger.mul(SCALE,self.table[i][j]))
                        weights.append(likelihood(p,s,N,self.ledger))
                total=ZERO
                for w in weights: total=self.ledger.add(total,w)
                cumulative=ZERO;boundaries=[]
                for w in weights[:-1]:
                    cumulative=self.ledger.add(cumulative,w)
                    boundaries.append(self.ledger.div(cumulative,total))
                self.weight_cache[s]=(weights,boundaries)
                self.ledger.counters["posterior_weight_build_wall_seconds"]+=time.perf_counter()-startw
                self.ledger.counters["likelihood_conversions"]+=TOTAL_POINTS
                self.ledger.counters["posterior_weight_cache_misses"]+=1
                self.ledger.event("posterior_cdf_built",s=s,n=N,points=TOTAL_POINTS,
                                  exact_weights=[qjson(x) for x in weights],
                                  boundary_count=len(boundaries))
            else:
                self.ledger.counters["posterior_weight_cache_hits"]+=1
            weights,boundaries=self.weight_cache[s]
            task_out=[]
            self.ledger.event("task_start",task=ti,s=s,n=N,draws=DRAWS_PER_TASK)
            for di in range(DRAWS_PER_TASK):
                u=LazyUniform(self.bits,"posterior_cdf")
                bs=self.bits.pos
                idx=u.categorical(boundaries)
                i,j=divmod(idx,GRID)
                task_out.append(idx)
                self.ledger.event("posterior_output",task=ti,task_s=s,draw=di,row_major_index=idx,
                                  point=[i,j],bits_start=bs,bits_end=self.bits.pos,comparisons=u.comparisons)
            self.outputs.append(task_out)
            self.ledger.event("task_complete",task=ti,s=s,outputs=task_out)
        self.wall_seconds=time.perf_counter()-start
        countset=set(task_counts)
        tablechars=sum(len(str(qjson(q))) for row in self.table for q in row)
        weightchars=sum(len(str(qjson(q))) for s in countset for q in self.weight_cache[s][0])
        extra_counters={"retained_exact_grid_points":TOTAL_POINTS,
                                     "retained_task_weight_vectors":len(self.weight_cache),
                                     "total_source_calls":TOTAL_POINTS,
                                     "total_recurrence_steps":TOTAL_POINTS*K,
                                     "grid_table_fraction_json_characters":tablechars,
                                     "weight_vector_fraction_json_characters":weightchars,
                                     "grid_table_binary_payload_bytes":sum((abs(q.numerator).bit_length()+7)//8+(q.denominator.bit_length()+7)//8 for row in self.table for q in row),
                                     "posterior_weight_cdf_binary_payload_bytes":sum((abs(q.numerator).bit_length()+7)//8+(q.denominator.bit_length()+7)//8 for s in countset for q in self.weight_cache[s][0])+sum((abs(q.numerator).bit_length()+7)//8+(q.denominator.bit_length()+7)//8 for s in countset for q in self.weight_cache[s][1]),
                                     "random_bits_consumed":self.bits.pos,
                                     "random_bits_by_use":dict(self.bits.reason_counts),
                                     "ideal_bit_tape_binary_bytes_lower_bound":(self.bits.pos+7)//8,
                                     "actual_ascii_bit_tape_bytes":len(self.bits.tape_string()),
                                     "posterior_draws":sum(map(len,self.outputs))}
        counters=dict(self.ledger.counters);counters.update(extra_counters)
        return {"method":self.name,"task_counts":self.task_counts,"outputs":self.outputs,
                "counters":counters,"rational_ledger":self.ledger.summary(),
                "wall_seconds_including_exact_logic":self.wall_seconds,
                "bit_tape":self.bits.tape_string(),"bit_segments":self.bits.segments,
                "events":self.ledger.events,
                "control_paid_grid_table":[[qjson(x) for x in row] for row in self.table]}


def config_dict() -> dict[str,Any]:
    return {"fixture":"finite synthetic logistic recurrence inverse-inference",
            "K":K,"H":H,"n":N,"epsilon":qjson(EPS),"scale":qjson(SCALE),
            "grid_points":TOTAL_POINTS,"grid_formula_a":"a_i=(97+2i)/32, i=0..15",
            "grid_formula_b":"b_j=(19+6j)/128, j=0..15",
            "node_hull":"smallest coordinate hull of grid centers in each node; singleton is exact center",
            "prior":"uniform over 256 center points; node mass is number of grid points / 256",
            "tasks":TASKS,"draws_per_task":DRAWS_PER_TASK,
            "task_rule":"s1=3; after lead task t, s_(t+1)=(s_t+r_t+1) mod 9 where r_t is lead task final output; controls replay the same realized count sequence",
            "randomness":"deterministic Python random.Random bit fixture; exact-law arguments are conditional on ideal iid fair bits; consumed tapes are public",
            "float_usage":"only wall-clock measurement; exact decisions and outputs use Fraction/integer arithmetic",
            "learner_access":"no full-grid table; source is only paid node interval execution and exact queried point evaluations where method explicitly pays for them"}


def execute(seed_map: dict[str,int], tapes: dict[str,str] | None = None) -> dict[str,Any]:
    tapes=tapes or {}
    lead=LeadMethod("lead_demand_refinement",seed_map.get("lead",0),tapes.get("lead"))
    lead_result=lead.run_lead()
    counts=lead_result["task_counts"]
    osstar=OSStarMethod("retained_OS_star",seed_map.get("osstar",0),tapes.get("osstar"))
    os_result=osstar.run(counts)
    full=FullGridMethod(seed_map.get("fullgrid",0),tapes.get("fullgrid"))
    full_result=full.run(counts)
    methods={"lead":lead_result,"osstar":os_result,"fullgrid":full_result}
    for obj, key in ((lead,"lead"),(osstar,"osstar"),(full,"fullgrid")):
        if tapes.get(key) is not None and obj.bits.pos != len(tapes[key]):
            raise RuntimeError(f"{key} replay consumed {obj.bits.pos} of {len(tapes[key])} public bits")
    return {"config":config_dict(),"task_counts_lead_generated":counts,
            "methods":methods,"replay":{"seed_used":False,"source_hash":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                           "exact_bit_tape_replayable":True}}


def write_run() -> None:
    seed_path=HERE/"private_evaluator_seed_manifest_DO_NOT_PASS_TO_LEARNER.json"
    if not seed_path.exists():
        seeds={"lead":3141592653,"osstar":2718281828,"fullgrid":1618033988,
               "purpose":"evaluator-only deterministic PRNG seeds; not supplied to learners or public replay"}
        seed_path.write_text(json.dumps(seeds,indent=2)+"\n")
    seeds=json.loads(seed_path.read_text())
    result=execute(seeds)
    public={k:v for k,v in result.items() if k!="methods"}
    public["method_summaries"]={k:{kk:vv for kk,vv in m.items() if kk not in ("events","bit_tape","control_paid_grid_table","bit_segments")}
                                for k,m in result["methods"].items()}
    # Each method's public transcript contains exact events and consumed bit tape.
    for key,m in result["methods"].items():
        path=HERE/f"{key.upper()}_PUBLIC_TRANSCRIPT.json"
        path.write_text(json.dumps({"method":key,"task_counts":m["task_counts"],"outputs":m["outputs"],
                                    "bit_tape":m["bit_tape"],"bit_segments":m["bit_segments"],
                                    "events":m["events"],"control_paid_grid_table":m.get("control_paid_grid_table")},
                                   separators=(",",":"))+"\n")
    out={"config":result["config"],"task_counts_lead_generated":result["task_counts_lead_generated"],
         "source_hash":result["replay"]["source_hash"],"method_summaries":public["method_summaries"]}
    (HERE/"RUN_SUMMARY.json").write_text(json.dumps(out,indent=2)+"\n")


if __name__=="__main__":
    write_run()
