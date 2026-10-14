"""Comparison-only partial quadratic flag acquisition with compact execution.

The learner receives n,r,beta, a seed and a chosen-pair comparison callback.
It never receives coordinate labels, a flag, inverse, source ranks or fibers.
Modes adaptive/fixed_j/raw_pair share the same preselector and RREF sampler.
The copied fixed_j_core.py is preserved as an independent earlier baseline.
"""
from __future__ import annotations

import math
import random
import time

import fixed_j_core as core
from fixed_j_core import (Meter, Quadratic, Source, coefficient_points, combine,
                         common_stabilizer, complement, echelon, interpolate,
                         kernel, linear, matrix_inverse, parity)


def M2(n):
    return 1 + n + n * (n - 1) // 2


def D(n):
    return (n ** 3 + 5 * n) // 6


def _scatter(bits, indices, meter=None):
    out = 0
    for j, i in enumerate(indices):
        out |= ((bits >> j) & 1) << i
    if meter is not None:
        meter.add("scatter_coordinate_bits", len(indices))
    return out


def restrict_to_pivots(q, pivots, meter=None):
    """Coefficients of q(Jz), J the raw pivot-coordinate inclusion."""
    d = len(pivots)
    lin = sum(((q.linear_mask >> i) & 1) << a for a, i in enumerate(pivots))
    upper = [0] * d
    for a, i in enumerate(pivots):
        for b in range(a + 1, d):
            j = pivots[b]
            upper[a] |= ((q.upper[i] >> j) & 1) << b
    if meter is not None:
        meter.add("quotient_restriction_coefficients", M2(d))
    return Quadratic(q.constant, lin, upper)


class CompactPrefixSampler:
    """RREF minimal translation quotient; stores no dense S basis for execution.

L=[I B] after raw coordinate permutation, Jz=(z,0), F=qJ. A seed uses
d-k quotient-complement bits and n-d free raw bits. q evaluation and sampling
cost O(nd+k*d^2), including reading/writing the n-bit raw state.
"""
    def __init__(self, polys, toggles, stabilizer, n, meter=None):
        self.n, self.k = n, len(polys)
        self.s = len(stabilizer)
        self.d = n - self.s
        self.meter = meter
        self.L, self.pivots = echelon(kernel(stabilizer, n, meter), n, meter)
        if len(self.L) != self.d or self.d < self.k:
            raise ArithmeticError("invalid acquired quotient dimension")
        pivot_set = set(self.pivots)
        self.free = [i for i in range(n) if i not in pivot_set]
        self.B = [sum(((row >> i) & 1) << j for j, i in enumerate(self.free))
                  for row in self.L]
        self.F = [restrict_to_pivots(q, self.pivots, meter) for q in polys]
        self.a = [linear(self.L, v, meter) for v in toggles]
        rb, _ = echelon(self.a, self.d, meter)
        if len(rb) != self.k:
            raise ArithmeticError("dependent acquired quotient toggles")
        self.W = complement(self.a, self.d, meter)
        if len(self.W) != self.d - self.k:
            raise ArithmeticError("wrong quotient toggle complement dimension")
        self.random_bits = n - self.k

    def lift(self, z):
        return _scatter(z, self.pivots, self.meter)

    def prefix(self, x):
        z, out = linear(self.L, x, self.meter), 0
        for f in self.F:
            out = (out << 1) | f(z, self.meter)
        return out

    def sample_from_seed(self, target, seed):
        qdim = self.d - self.k
        z = combine(self.W, seed & ((1 << qdim) - 1), self.meter)
        for i, (f, a) in enumerate(zip(self.F, self.a)):
            if f(z, self.meter) != ((target >> (self.k - i - 1)) & 1):
                z ^= a
                if self.meter is not None:
                    self.meter.add("sampler_quotient_toggles")
            if self.meter is not None:
                self.meter.add("sampler_toggle_steps")
        free_seed = seed >> qdim
        pivot_bits = z ^ linear(self.B, free_seed, self.meter)
        raw = _scatter(pivot_bits, self.pivots, self.meter)
        raw |= _scatter(free_seed, self.free, self.meter)
        if self.meter is not None:
            self.meter.add("prefix_samples")
            self.meter.add("raw_output_bits", self.n)
        return raw

    def sample(self, target, rng, meter=None):
        seed = rng.getrandbits(self.random_bits)
        if meter is not None:
            meter.add("prefix_fiber_random_bits", self.random_bits)
            meter.add("independent_prefix_samples")
        return self.sample_from_seed(target, seed)

    def fiber(self, target):
        for seed in range(1 << self.random_bits):
            if self.meter is not None:
                self.meter.add("explicit_fiber_points")
            yield self.sample_from_seed(target, seed)

    def project(self, x, target):
        z = linear(self.L, x, self.meter)
        before = z
        for i, (f, a) in enumerate(zip(self.F, self.a)):
            if f(z, self.meter) != ((target >> (self.k - i - 1)) & 1):
                z ^= a
        return x ^ self.lift(z ^ before)

    def payload(self):
        # Counts the actual logical fields stored, excluding Python overhead.
        return dict(n=self.n, k=self.k, d=self.d, s=self.s,
                    quotient_polynomial_bits=self.k * M2(self.d),
                    L_row_bits=self.n * self.d,
                    B_row_bits=(self.n - self.d) * self.d,
                    quotient_toggle_bits=self.k * self.d,
                    quotient_complement_bits=(self.d - self.k) * self.d,
                    coordinate_index_bits=self.n * max(1, (self.n - 1).bit_length()),
                    entropy_bits_per_sample=self.random_bits,
                    stored_raw_stabilizer_basis=False,
                    stored_raw_polynomial_bodies=False)

    def factor_coefficient_check(self, raw_polys):
        """Optional exact ANF identity check, charged separately from sampling."""
        checks = 0
        for q, f in zip(raw_polys, self.F):
            values = {x: f(linear(self.L, x, self.meter), self.meter)
                      for x in coefficient_points(self.n)}
            reconstructed = interpolate(values, self.n, self.meter)
            if reconstructed.body() != q.body():
                return False, checks
            checks += 1
        if self.meter is not None:
            self.meter.add("factor_coefficient_bodies_checked", checks)
        return True, checks


class AcquiredPrefix(core.AcquiredPrefix):
    def sampler(self):
        return CompactPrefixSampler(self.q, self.toggles, self.stabilizer,
                                    self.n, self.meter)


def parameters(n, r, beta, prefix_length=None, mode="adaptive"):
    cfg = core.parameters(n, r, beta)
    h = n - r
    m = h if prefix_length is None else prefix_length
    hybrid = mode in ("hybrid", "hybrid_fixed_j", "hybrid_raw")
    family = "fixed_j" if mode in ("fixed_j", "hybrid_fixed_j") else "raw_pair" if mode in ("raw_pair", "hybrid_raw") else "adaptive"
    if not (0 <= m <= h) or mode not in ("adaptive", "fixed_j", "raw_pair", "hybrid", "hybrid_fixed_j", "hybrid_raw"):
        raise ValueError("invalid prefix length or acquisition mode")
    cfg.update(promised_flag_length=h, stages=m, mode=mode, hybrid=hybrid, polar_family=family,
               prefix_only=prefix_length is not None,
               tail_comparisons=0 if prefix_length is not None else cfg["tail_comparisons"])
    if m:
        p = 2.0 ** (-r - 1)
        R = math.ceil(math.log((4 if hybrid else 2) * m / beta) / p)
        delta = beta / ((2 if family == "raw_pair" else 4) * m * R * R)
        zeta = beta / (4 * m * R)
        t = math.ceil(math.log(1 / delta) / math.log(16 / 15))
        J = 0 if r == 0 else r + math.ceil(math.log2(1 / zeta))
        L = 0 if r == 0 else math.ceil(math.log((r + 1) / zeta) / math.log(4 / 3))
        cfg.update(p=p, R=R, delta=delta, zeta=zeta, t=t, J=J, L=L)
    else:
        cfg.update(p=0.0, R=0, delta=0.0, zeta=0.0, t=0, J=0, L=0)
    A = sum(M2(k + r) for k in range(m))
    P = sum((n + 1) * (cfg["J"] + 1) + (n-k) * (r+1) + n
            for k in range(m))
    Pa = sum((n+1) + r*(n+1) + (r+3)*(r+1)*cfg["L"] + (n-k)*(r+1) + n
             for k in range(m))
    leading, overhead = (m*M2(n), 0) if family == "raw_pair" else (A, P if family == "fixed_j" else Pa)
    matches = sum(max(0,n-k-1) for k in range(m)) if hybrid else 0
    match_cap = math.ceil(4*matches+8*math.log(4/beta)) if matches else 0
    cfg.update(leading_interpolation_cap=leading,
               noninterpolation_polar_cap=overhead,
               worst_comparison_bound=leading + overhead + 3*m*cfg["R"]*cfg["t"] + cfg["tail_comparisons"] + 2*match_cap+matches,
               expected_comparison_bound=leading + overhead + 3*m*((1+beta/2)*cfg["t"]+16*(1-cfg["p"])/cfg["p"])+cfg["tail_comparisons"]+5*matches if m else cfg["tail_comparisons"],
               first_false_raw_acceptance_bound=beta/((2 if family == "raw_pair" else 4)*cfg["R"]) if m else 0.0,
               first_polar_miss_bound=beta/(4*cfg["R"]) if m and family != "raw_pair" else 0.0,
               raw_candidate_cap_failure_bound=beta/(4 if hybrid else 2) if m else 0.0,
               tournament_pair_count_cap=matches,
               tournament_total_attempt_cap=match_cap,
               tournament_cap_failure_bound=math.exp(-match_cap/8) if matches else 0.0,
               cap_failure_bound=beta/2 if m else 0.0,
               total_semantic_failure_bound=beta/2+beta/(2*cfg["R"]) if m else 0.0)
    return cfg


def _finish_candidate(n, k, r, v, prefix, source, cfg, meter,
                      q0, qe, row_basis, pivots, acquisition_receipt,
                      skip_empty_columns=False, skip_winner_response=False):
    """Selected GLOBAL columns, exact kernel, one quotient interpolation."""
    S = prefix.stabilizer
    b = len(row_basis)
    if b > r:
        return None, dict(status="UNKNOWN", reason="sampled_image_rank_exceeds_r", **acquisition_receipt)
    source.phase = "selected_columns"
    images = []
    for z in S:
        if not pivots and skip_empty_columns:
            images.append(0)
            continue
        qz = core._label(source, v, z)
        selected = 0
        for j, i in enumerate(pivots):
            derivative = core._label(source, v, z ^ (1 << i)) ^ qz ^ qe[i] ^ q0
            selected |= derivative << j
        images.append(combine(row_basis, selected, meter))
        meter.add("selected_column_rows")
        meter.add("selected_column_derivatives", b)
    map_rows = [sum(((image >> i) & 1) << j for j, image in enumerate(images))
                for i in range(n)]
    coeff_kernel = kernel(map_rows, len(S), meter)
    Nhat = [combine(S, c, meter) for c in coeff_kernel]
    dimN = len(Nhat)
    if dimN < n-r-k:
        return None, dict(status="UNKNOWN", reason="estimated_kernel_dimension_below_promise", **acquisition_receipt)
    U = complement(Nhat, n, meter)
    u = len(U)
    if u > k+r:
        return None, dict(status="UNKNOWN", reason="quotient_dimension_guard", **acquisition_receipt)
    source.phase = "quotient_interpolation"
    qU_points = coefficient_points(u)
    qU_values = {0: q0}
    for c in qU_points[1:]:
        qU_values[c] = core._label(source, v, combine(U, c, meter))
    qU = interpolate(qU_values, u, meter)
    source.phase = "kernel_response"
    responses = 0
    saved_responses = 0
    for j,z in enumerate(Nhat):
        if skip_winner_response and z == v:
            response = 1  # g_v(v)=1-g_v(0), by strict-order antisymmetry.
            saved_responses += 1
        else:
            response = core._label(source,v,z)^q0
        responses |= response << j
    basis = U + Nhat
    basis_rows = [sum(((basis[j] >> i) & 1) << j for j in range(n)) for i in range(n)]
    coord_rows = matrix_inverse(basis_rows, n, meter)
    def f_eval(x):
        coords = linear(coord_rows, x, meter)
        return qU(coords & ((1 << u)-1), meter) ^ parity(responses & (coords >> u), meter)
    points = coefficient_points(n)
    f = interpolate({x: f_eval(x) for x in points}, n, meter)
    meter.add("candidate_global_anchor_evaluations", len(points))
    if not f.toggles(v, meter):
        return None, dict(status="UNKNOWN", reason="post_interpolation_own_toggle_failed", **acquisition_receipt)
    if not all(q.translation_invariant(v, meter) for q in prefix.q):
        return None, dict(status="UNKNOWN", reason="selected_toggle_not_in_acquired_stabilizer", **acquisition_receipt)
    return f, dict(status="accepted_candidate", **acquisition_receipt,
                   sampled_image_rank=b, estimated_kernel_dimension=dimN,
                   quotient_dimension=u, selected_pivot_columns=pivots,
                   selected_column_rows=len(S), q_quotient_anchor_count=len(qU_points),
                   kernel_response_count=dimN,
                   source_free_winner_responses=saved_responses)


def _candidate_adaptive(n, k, r, v, prefix, source, rng, cfg, meter):
    S, sdim = prefix.stabilizer, len(prefix.stabilizer)
    source.phase = "polar_base"
    q0 = core._label(source, v, 0)
    qe = [core._label(source, v, 1 << i) for i in range(n)]
    row_basis, pivots = [], []
    consecutive = tests = additions = 0
    test_cap = (r+1)*cfg["L"]
    while len(row_basis) < r and consecutive < cfg["L"]:
        if tests >= test_cap or additions >= r:
            return None, dict(status="UNKNOWN", reason="adaptive_polar_loop_cap", cheap_tests=tests)
        s = combine(S, rng.getrandbits(sdim), meter)
        t = rng.getrandbits(n)
        meter.add("polar_direction_random_bits", sdim)
        meter.add("polar_test_point_random_bits", n)
        source.phase = "polar_cheap_test"
        qs = core._label(source, v, s)
        selected = sum((core._label(source, v, s ^ (1 << i)) ^ qs ^ qe[i] ^ q0) << j
                       for j, i in enumerate(pivots))
        projected = combine(row_basis, selected, meter)
        qt = core._label(source, v, t)
        qst = core._label(source, v, s ^ t)
        detected = qst ^ qs ^ qt ^ q0 ^ parity(projected & t, meter)
        tests += 1
        meter.add("cheap_polar_tests")
        meter.add("cheap_polar_selected_derivatives", len(pivots))
        if not detected:
            consecutive += 1
            continue
        source.phase = "polar_new_full_row"
        # qs already came from this test; no global label cache is assumed.
        row = sum((core._label(source, v, s ^ (1 << i)) ^ qs ^ qe[i] ^ q0) << i
                  for i in range(n))
        new_basis, new_pivots = echelon(row_basis + [row], n, meter)
        if len(new_basis) != len(row_basis)+1:
            return None, dict(status="UNKNOWN", reason="detected_polar_row_not_new",
                              cheap_tests=tests, full_row_additions=additions)
        row_basis, pivots = new_basis, new_pivots
        additions += 1
        meter.add("new_full_polar_rows")
        meter.add("polar_row_coordinates", n)
        consecutive = 0
    receipt = dict(cheap_tests=tests, full_row_additions=additions,
                   final_nondetection_count=consecutive, nondetection_cap=cfg["L"],
                   deterministic_test_cap=test_cap,
                   sampled_image_rank=len(row_basis),
                   stopped_at_supplied_rank=(len(row_basis) == r),
                   image_miss_bound=(r+1)*(3/4)**cfg["L"] if r else 0.0,
                   target_miss_budget=cfg["zeta"])
    # Avoid duplicate sampled_image_rank in _finish_candidate's final receipt.
    receipt.pop("sampled_image_rank")
    return _finish_candidate(n, k, r, v, prefix, source, cfg, meter,
                             q0, qe, row_basis, pivots, receipt)


def _candidate_raw(n, k, r, v, prefix, source, rng, cfg, meter):
    source.phase = "raw_interpolation"
    points = coefficient_points(n)
    f = interpolate({x: core._label(source, v, x) for x in points}, n, meter)
    if not f.toggles(v, meter):
        return None, dict(status="UNKNOWN", reason="post_interpolation_own_toggle_failed")
    if not all(q.translation_invariant(v, meter) for q in prefix.q):
        return None, dict(status="UNKNOWN", reason="selected_toggle_not_in_acquired_stabilizer")
    return f, dict(status="accepted_candidate", raw_anchor_count=len(points), quotient_dimension=n)


def _candidate_refined(n, k, r, v, prefix, source, rng, cfg, meter):
    """Use the observable residual rank cap r-d_k, never an estimated zero."""
    S, sdim = prefix.stabilizer, len(prefix.stabilizer)
    cap_r = sdim-(n-r-k)
    if not 0 <= cap_r <= r:
        return None,dict(status="UNKNOWN",reason="residual_rank_cap_guard")
    source.phase="polar_base"
    q0=core._label(source,v,0)
    qe=[core._label(source,v,1 << i) for i in range(n)] if cap_r else []
    rows,pivots=[],[]
    tests=additions=consecutive=0
    L=math.ceil(math.log((cap_r+1)/cfg["zeta"])/math.log(4/3)) if cap_r else 0
    J=cap_r+math.ceil(math.log2(1/cfg["zeta"])) if cap_r else 0
    if cfg["polar_family"] == "fixed_j":
        source.phase="polar_fixed_rows"
        for _ in range(J):
            s=combine(S,rng.getrandbits(sdim),meter)
            meter.add("polar_direction_random_bits",sdim)
            qs=core._label(source,v,s)
            row=sum((core._label(source,v,s^(1 << i))^qs^qe[i]^q0) << i for i in range(n))
            rows.append(row)
            meter.add("sampled_polar_rows")
        rows,pivots=echelon(rows,n,meter)
        if len(rows)>cap_r:
            return None,dict(status="UNKNOWN",reason="sampled_image_rank_exceeds_residual_cap")
    else:
        while len(rows)<cap_r and consecutive<L:
            if tests >= (cap_r+1)*L or additions >= cap_r:
                return None,dict(status="UNKNOWN",reason="adaptive_polar_loop_cap")
            s=combine(S,rng.getrandbits(sdim),meter)
            t=rng.getrandbits(n)
            meter.add("polar_direction_random_bits",sdim)
            meter.add("polar_test_point_random_bits",n)
            source.phase="polar_cheap_test"
            qs=core._label(source,v,s)
            selected=sum((core._label(source,v,s^(1 << i))^qs^qe[i]^q0) << j
                         for j,i in enumerate(pivots))
            projected=combine(rows,selected,meter)
            qt,qst=core._label(source,v,t),core._label(source,v,s^t)
            detected=qst^qs^qt^q0^parity(projected&t,meter)
            tests+=1
            meter.add("cheap_polar_tests")
            if not detected:
                consecutive+=1
                continue
            source.phase="polar_new_full_row"
            row=sum((core._label(source,v,s^(1 << i))^qs^qe[i]^q0) << i for i in range(n))
            trial,new_pivots=echelon(rows+[row],n,meter)
            if len(trial)!=len(rows)+1:
                return None,dict(status="UNKNOWN",reason="detected_polar_row_not_new")
            rows,pivots=trial,new_pivots
            additions+=1
            consecutive=0
            meter.add("new_full_polar_rows")
    receipt=dict(effective_rank_cap=cap_r,global_rank_cap=r,
                 certified_zero_polar_map=(cap_r==0),cheap_tests=tests,
                 full_row_additions=additions,fixed_J_rows=J if cfg["polar_family"]=="fixed_j" else 0,
                 nondetection_cap=L,final_nondetection_count=consecutive,
                 target_miss_budget=cfg["zeta"],
                 image_miss_bound=(cap_r+1)*(3/4)**L if cap_r and cfg["polar_family"]!="fixed_j" else 2.0**(cap_r-J) if cap_r else 0.0)
    return _finish_candidate(n,k,r,v,prefix,source,cfg,meter,q0,qe,rows,pivots,receipt,
                             skip_empty_columns=True,skip_winner_response=True)


def _select_certified_zero(S,k,source,rng,cfg,meter,state):
    """Exact-on-completion tournament; all probes share one global cap."""
    winner=S[0]
    trials=[]
    source.phase="certified_zero_tournament"
    for v in S[1:]:
        used=0
        prior=winner
        while True:
            if state["attempts"] >= cfg["tournament_total_attempt_cap"]:
                return None,trials,"global_tournament_attempt_cap"
            x=rng.getrandbits(cfg["n"])
            meter.add("tournament_input_random_bits",cfg["n"])
            a,b=core._label(source,v,x),core._label(source,winner,x)
            used+=1
            state["attempts"]+=1
            if a==b:
                break
        if bool(source(x^v,x^winner))==bool(a):
            winner=v
        state["matches"]+=1
        meter.add("tournament_completed_matches")
        if state["matches"]>cfg["tournament_pair_count_cap"]:
            return None,trials,"global_tournament_pair_cap"
        trials.append(dict(challenger=v,previous_winner=prior,winner=winner,matching_attempts=used))
    return winner,trials,None


def acquire(n, r, query, seed, beta=0.01, prefix_length=None,
            mode="adaptive", force_zero_directions=False):
    """Full model unless prefix_length is supplied; no suffix fitting in prefix mode.

force_zero_directions is an explicit test-only failure fixture. All loops are
capped even after a false accepted direction or a polar miss.
"""
    start = time.perf_counter()
    cfg = parameters(n, r, beta, prefix_length, mode)
    meter, source = Meter(), Source(query)
    prefix, stages = AcquiredPrefix(n, meter), []
    match_state=dict(attempts=0,matches=0)

    def result(status, reason=None, model=None):
        out = dict(status=status, parameters=cfg, stages=stages,
                   comparison_calls=source.calls, source_calls_by_phase=dict(source.by_phase),
                   random_bits={k:v for k,v in meter.ops.items() if k.endswith("random_bits")},
                   local_operations=dict(meter.ops),
                   acquisition_seconds=time.perf_counter()-start,
                   acquired_prefix_dimension=len(prefix.q),
                   acquired_toggle_vectors=list(prefix.toggles),
                   acquired_stabilizer_basis=list(prefix.stabilizer),
                   tournament_totals=dict(match_state),
                   model_bodies=[q.body() for q in model] if model is not None else None)
        if reason is not None:
            out["reason"] = reason
        if source.calls > cfg["worst_comparison_bound"]:
            raise ArithmeticError("deterministic comparison cap exceeded")
        return out, model, prefix

    for k in range(cfg["stages"]):
        stage_start = time.perf_counter()
        # Disjoint logical random tapes for raw validation and fresh polar
        # recovery. Deterministic PRNG seeds are finite replay conventions;
        # the probability theorem assumes independent ideal fair draws.
        selection_rng = random.Random(seed + 1000003*(k+1))
        polar_rng = random.Random(seed + 1700033*(k+1))
        before = len(prefix.stabilizer)
        if not (n-r-k <= before <= n-k):
            return result("UNKNOWN", "acquired_stabilizer_dimension_guard")
        sampler = prefix.sampler()
        winner, trials = None, []
        effective_rank_cap=before-(n-r-k)
        use_tournament=cfg["hybrid"] and effective_rank_cap==0 and not force_zero_directions
        if use_tournament:
            winner,trials,unknown=_select_certified_zero(prefix.stabilizer,k,source,
                                                        selection_rng,cfg,meter,match_state)
            if unknown:
                stages.append(dict(stage=k,dimension_S_before=before,trials=trials,
                                   selector="certified_zero_tournament"))
                return result("UNKNOWN",unknown)
        for j in range(0 if use_tournament else cfg["R"]):
            coeff = 0 if force_zero_directions else selection_rng.getrandbits(before)
            if not force_zero_directions:
                meter.add("direction_random_bits", before)
            v = combine(prefix.stabilizer, coeff, meter)
            if not v:
                trials.append(dict(trial=j, direction=0, status="zero_direction", pair_tests=0))
                continue
            source.phase = "pair_validation"
            passed, used = True, 0
            for _ in range(cfg["t"]):
                used += 1
                if not core._pair_test(k, v, sampler, source, selection_rng, meter):
                    passed = False
                    break
            trials.append(dict(trial=j, direction=v, status="accepted_raw" if passed else "pair_inversion_rejected",
                               pair_tests=used, comparisons=3*used))
            if passed:
                winner = v
                break
        if winner is None:
            stages.append(dict(stage=k, dimension_S_before=before, trials=trials,
                               stage_seconds=time.perf_counter()-stage_start))
            return result("UNKNOWN", "direction_cap_exhausted")
        candidate = _candidate_refined if mode in ("hybrid","hybrid_fixed_j") else _candidate_raw if mode in ("raw_pair","hybrid_raw") else core._candidate_from_polar if mode=="fixed_j" else _candidate_adaptive
        f, polar = candidate(n, k, r, winner, prefix, source, polar_rng, cfg, meter)
        if f is None:
            stages.append(dict(stage=k, dimension_S_before=before, winner=winner,
                               trials=trials, polar=polar, stage_seconds=time.perf_counter()-stage_start))
            return result("UNKNOWN", polar["reason"])
        prior_S=list(prefix.stabilizer)
        prefix.add(f, winner)
        defect_before=n-k-before
        defect_after=n-(k+1)-len(prefix.stabilizer)
        candidate_polar=f.polar()
        candidate_a=len(echelon([linear(candidate_polar,s,meter) for s in prior_S],n,meter)[0])
        if defect_after!=defect_before+candidate_a:
            raise ArithmeticError("stabilizer defect increment identity failed")
        if cfg["hybrid"] and defect_after>r:
            stages.append(dict(stage=k,dimension_S_before=before,dimension_S_after=len(prefix.stabilizer),
                               trials=trials,polar=polar,defect_before=defect_before,defect_after=defect_after))
            return result("UNKNOWN","acquired_stabilizer_defect_exceeds_r")
        stages.append(dict(stage=k, dimension_S_before=before,
                           dimension_S_after=len(prefix.stabilizer), winner=winner,
                           trials=trials, polar=polar, sampler=sampler.payload(),
                           selector="certified_zero_tournament" if use_tournament else "raw_paired_cut",
                           defect_before=defect_before,defect_after=defect_after,
                           candidate_polar_rank_on_S=candidate_a,
                           effective_rank_cap=effective_rank_cap,
                           stage_seconds=time.perf_counter()-stage_start))
    if prefix_length is not None:
        return result("returned_prefix", model=list(prefix.q))
    source.phase = "tail_enumeration"
    tail_start = time.perf_counter()
    points, values = coefficient_points(n), [dict() for _ in range(r)]
    sampler = prefix.sampler()
    for x in points:
        target = prefix.prefix(x)
        rank = sum(source(y, x) for y in sampler.fiber(target) if y != x)
        for j in range(r):
            values[j][x] = (rank >> (r-j-1)) & 1
    suffix = [interpolate(values[j], n, meter) for j in range(r)]
    if source.by_phase["tail_enumeration"] != cfg["tail_comparisons"]:
        raise ArithmeticError("tail comparison accounting mismatch")
    out, model, prefix = result("returned_model", model=list(prefix.q)+suffix)
    out["tail_seconds"] = time.perf_counter()-tail_start
    out["tail_comparisons"] = source.by_phase["tail_enumeration"]
    return out, model, prefix


class CompiledModel:
    """Zero-comparison execution with the compact acquired-prefix quotient."""
    def __init__(self, model, toggles, n, r, meter=None):
        self.model, self.n, self.r = list(model), n, r
        self.h = n-r
        self.meter = meter
        q = self.model[:self.h]
        self.sampler = CompactPrefixSampler(q, toggles, common_stabilizer(q, n, meter), n, meter)

    def rank(self, x):
        out = 0
        for q in self.model:
            out = (out << 1) | q(x, self.meter)
        return out

    def prefix(self, x):
        return self.sampler.prefix(x)

    def fiber(self, target):
        return self.sampler.fiber(target)

    def inverse(self, target):
        return [x for x in self.fiber(target >> self.r) if self.rank(x) == target]
