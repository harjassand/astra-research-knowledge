"""Source-free compact-polar partial-flag acquisition and local execution.

`acquire` sees only n, r, beta, a seed, and a binary comparison callback. Its
control path contains no teacher, source-rank, hidden-flag, inverse, or truth
lookup. All acquired bodies and prefix samplers are built from comparison
answers and learner-owned GF(2) algebra. `CompiledModel` below supplies local
rank and inverse operations from the returned coefficient bodies.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import random
import time
from collections import defaultdict


class Meter:
    """Deterministic logical-operation/event counts (not CPU instruction counts)."""
    def __init__(self):
        self.ops = defaultdict(int)
        self.phase = "acquisition"

    def add(self, key, amount=1):
        self.ops[key] += amount


def parity(x: int, meter: Meter | None = None) -> int:
    if meter is not None:
        meter.add("parity_calls")
    return x.bit_count() & 1


def combine(basis, a: int, meter: Meter | None = None) -> int:
    """XOR the basis vectors selected by the coefficient mask a."""
    if meter is not None:
        meter.add("combine_calls")
        meter.add("combine_selected_basis_vectors", a.bit_count())
    z = 0
    while a:
        b = a & -a
        z ^= basis[b.bit_length() - 1]
        if meter is not None:
            meter.add("basis_xors")
        a ^= b
        if meter is not None:
            meter.add("coefficient_bit_scans")
    return z


def linear(rows, x: int, meter: Meter | None = None) -> int:
    if meter is not None:
        meter.add("linear_map_evaluations")
    return sum(parity(row & x, meter) << j for j, row in enumerate(rows))


def echelon(rows, n: int, meter: Meter | None = None):
    """Reduced row echelon basis, pivot columns, in low-bit-first order."""
    rows = list(rows)
    if meter is not None:
        meter.add("echelon_calls")
        meter.add("echelon_input_rows", len(rows))
    pivots = []
    rank = 0
    for j in range(n):
        p = next((a for a in range(rank, len(rows)) if (rows[a] >> j) & 1), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        for a in range(len(rows)):
            if a != rank and ((rows[a] >> j) & 1):
                rows[a] ^= rows[rank]
                if meter is not None:
                    meter.add("gf2_row_xors")
        pivots.append(j)
        rank += 1
        if rank == len(rows):
            break
    if meter is not None:
        meter.add("gf2_pivots", rank)
    return rows[:rank], pivots


def kernel(rows, n: int, meter: Meter | None = None):
    if meter is not None:
        meter.add("kernel_calls")
        meter.add("kernel_equations", len(rows))
    reduced, pivots = echelon(rows, n, meter)
    pivot_set = set(pivots)
    out = []
    for j in range(n):
        if j not in pivot_set:
            v = 1 << j
            for row, pivot in zip(reduced, pivots):
                if (row >> j) & 1:
                    v |= 1 << pivot
            out.append(v)
    return out


def complement(basis, n: int, meter: Meter | None = None):
    """Return a deterministic basis completing `basis` to F_2^n."""
    if meter is not None:
        meter.add("complement_calls")
        meter.add("complement_input_basis_vectors", len(basis))
    kept, _ = echelon(basis, n, meter)
    out = []
    rank = len(kept)
    for j in range(n):
        v = 1 << j
        trial, _ = echelon(kept + [v], n, meter)
        if len(trial) > rank:
            kept = trial
            rank += 1
            out.append(v)
    if rank != n:
        raise ArithmeticError("basis completion failed")
    return out


def matrix_inverse(rows, n: int, meter: Meter | None = None):
    """Inverse of an invertible n-by-n binary matrix given by row masks."""
    if meter is not None:
        meter.add("matrix_inverse_calls")
        meter.add("matrix_inverse_dimension", n)
    if n == 0:
        return []
    aug = [rows[i] | (1 << (n + i)) for i in range(n)]
    pivots = []
    rank = 0
    for j in range(n):
        p = next((a for a in range(rank, n) if (aug[a] >> j) & 1), None)
        if p is None:
            raise ArithmeticError("singular matrix in quotient construction")
        aug[rank], aug[p] = aug[p], aug[rank]
        for a in range(n):
            if a != rank and ((aug[a] >> j) & 1):
                aug[a] ^= aug[rank]
                if meter is not None:
                    meter.add("gf2_row_xors")
        pivots.append(j)
        rank += 1
    if pivots != list(range(n)):
        raise ArithmeticError("matrix pivot order mismatch")
    if meter is not None:
        meter.add("gf2_pivots", n)
    return [row >> n for row in aug]


@dataclass
class Quadratic:
    constant: int
    linear_mask: int
    upper: list[int]

    def __call__(self, x: int, meter: Meter | None = None) -> int:
        z = self.constant ^ parity(self.linear_mask & x, meter)
        a = x
        while a:
            b = a & -a
            z ^= parity(self.upper[b.bit_length() - 1] & x, meter)
            a ^= b
        if meter is not None:
            meter.add("quadratic_evaluations")
        return z

    def polar(self):
        n = len(self.upper)
        rows = [0] * n
        for i, row in enumerate(self.upper):
            a = row
            while a:
                b = a & -a
                j = b.bit_length() - 1
                rows[i] |= 1 << j
                rows[j] |= 1 << i
                a ^= b
        return rows

    def translation_invariant(self, v: int, meter: Meter | None = None) -> bool:
        if any(parity(row & v, meter) for row in self.polar()):
            return False
        return (self(v, meter) ^ self.constant) == 0

    def toggles(self, v: int, meter: Meter | None = None) -> bool:
        if any(parity(row & v, meter) for row in self.polar()):
            return False
        return (self(v, meter) ^ self.constant) == 1

    def body(self):
        return {"constant": self.constant, "linear": self.linear_mask,
                "upper": list(self.upper)}


def coefficient_points(n: int):
    return ([0] + [1 << i for i in range(n)] +
            [(1 << i) | (1 << j) for i in range(n) for j in range(i + 1, n)])


def interpolate(values, n: int, meter: Meter | None = None):
    c = values[0]
    lin = 0
    for i in range(n):
        lin |= (values[1 << i] ^ c) << i
    upper = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            upper[i] |= (values[(1 << i) | (1 << j)] ^ values[1 << i]
                         ^ values[1 << j] ^ c) << j
    if meter is not None:
        meter.add("quadratic_interpolations")
        meter.add("interpolation_coefficients", 1 + n + n * (n - 1) // 2)
    return Quadratic(c, lin, upper)


def common_stabilizer(polys, n: int, meter: Meter | None = None):
    """Exact common translation stabilizer, from acquired coefficient bodies."""
    if not polys:
        return [1 << i for i in range(n)]
    radical = kernel([row for p in polys for row in p.polar()], n, meter)
    response_rows = []
    for p in polys:
        response = 0
        for j, v in enumerate(radical):
            if (p(v, meter) ^ p.constant) & 1:
                response |= 1 << j
        response_rows.append(response)
    coeff_kernel = kernel(response_rows, len(radical), meter)
    return [combine(radical, a, meter) for a in coeff_kernel]


class PrefixSampler:
    """Exact sampler for acquired-prefix fibers using the minimal S quotient."""
    def __init__(self, polys, toggles, stabilizer, n: int, meter: Meter | None = None):
        self.polys = list(polys)
        self.toggles = list(toggles)
        self.S = list(stabilizer)
        self.n = n
        self.k = len(polys)
        self.s = len(self.S)
        self.d = n - self.s
        self.meter = meter
        if self.d < self.k:
            raise ArithmeticError("acquired own-toggles exceed quotient dimension")

        # L is a basis of S^perp; U completes S; P=L U is invertible.
        self.L = kernel(self.S, n, meter)
        if len(self.L) != self.d:
            raise ArithmeticError("annihilator dimension mismatch")
        U = complement(self.S, n, meter)
        if len(U) != self.d:
            raise ArithmeticError("quotient complement dimension mismatch")
        P_rows = [sum(parity(row & u, meter) << j for j, u in enumerate(U))
                  for row in self.L]
        Pinv = matrix_inverse(P_rows, self.d, meter)
        self.J = []
        for j in range(self.d):
            coeff = sum(((Pinv[i] >> j) & 1) << i for i in range(self.d))
            self.J.append(combine(U, coeff, meter))

        self.a = [linear(self.L, w, meter) for w in self.toggles]
        self.W = complement(self.a, self.d, meter)
        if len(self.W) != self.d - self.k:
            raise ArithmeticError("quotient toggle complement dimension mismatch")
        self.random_bits = self.n - self.k

    def lift(self, z: int) -> int:
        return combine(self.J, z, self.meter)

    def sample_from_seed(self, target: int, seed: int) -> int:
        """Enumerate one of the exactly 2^(n-k) equiprobable random seeds."""
        qdim = self.d - self.k
        z = combine(self.W, seed & ((1 << qdim) - 1), self.meter)
        for i, (p, a) in enumerate(zip(self.polys, self.a)):
            self.meter.add("sampler_toggle_steps") if self.meter else None
            bit = (target >> (self.k - i - 1)) & 1
            raw = self.lift(z)
            if p(raw, self.meter) != bit:
                z ^= a
                if self.meter is not None:
                    self.meter.add("sampler_quotient_toggles")
        raw = self.lift(z)
        sseed = seed >> qdim
        raw ^= combine(self.S, sseed, self.meter)
        if self.meter is not None:
            self.meter.add("prefix_samples")
        return raw

    def sample(self, target: int, rng: random.Random, meter: Meter | None = None) -> int:
        seed = rng.getrandbits(self.random_bits)
        if meter is not None:
            meter.add("prefix_fiber_random_bits", self.random_bits)
            meter.add("independent_prefix_samples")
        return self.sample_from_seed(target, seed)

    def project(self, x: int, target: int) -> int:
        """Correct any raw state into the acquired prefix fiber."""
        for i, (p, w) in enumerate(zip(self.polys, self.toggles)):
            bit = (target >> (self.k - i - 1)) & 1
            if p(x, self.meter) != bit:
                x ^= w
                if self.meter is not None:
                    self.meter.add("sampler_raw_toggles")
        if self.meter is not None:
            self.meter.add("sampler_projections")
        return x

    def fiber(self, target: int):
        # The direct raw complement is used only for explicit finite checking
        # and the exact r-bit suffix enumeration, never for prefix sampling.
        Wraw = complement(self.toggles, self.n, self.meter)
        for seed in range(1 << len(Wraw)):
            yield self.project(combine(Wraw, seed, self.meter), target)


class AcquiredPrefix:
    def __init__(self, n: int, meter: Meter | None = None):
        self.n = n
        self.q: list[Quadratic] = []
        self.toggles: list[int] = []
        self.stabilizer = [1 << i for i in range(n)]
        self.meter = meter

    def prefix(self, x: int) -> int:
        a = 0
        for q in self.q:
            a = (a << 1) | q(x, self.meter)
        return a

    def sampler(self):
        return PrefixSampler(self.q, self.toggles, self.stabilizer, self.n, self.meter)

    def add(self, q: Quadratic, v: int):
        if not q.toggles(v, self.meter):
            raise ArithmeticError("candidate failed own-toggle gate")
        if not all(p.translation_invariant(v, self.meter) for p in self.q):
            raise ArithmeticError("selected direction escaped acquired stabilizer")
        self.q.append(q)
        self.toggles.append(v)
        self.stabilizer = common_stabilizer(self.q, self.n, self.meter)


class Source:
    def __init__(self, query):
        self.query = query
        self.calls = 0
        self.by_phase = defaultdict(int)
        self.phase = "acquisition"

    def __call__(self, x: int, y: int) -> int:
        self.calls += 1
        self.by_phase[self.phase] += 1
        return int(bool(self.query(x, y)))


def parameters(n: int, r: int, beta: float):
    if not (0 <= r <= n and 0 < beta <= 0.5):
        raise ValueError("require 0<=r<=n and 0<beta<=1/2")
    h = n - r
    M = 1 + n + n * (n - 1) // 2
    if h == 0:
        return dict(n=n, r=r, beta=beta, stages=0, M=M, p=0.0, R=0,
                    delta=0.0, t=0, J=0, tail_comparisons=M * ((1 << r) - 1))
    p = 2.0 ** (-r - 1)
    R = math.ceil(math.log(2 * h / beta) / p)
    delta = beta / (4 * h * R * R)
    t = math.ceil(math.log(1 / delta) / math.log(16 / 15))
    J = 0 if r == 0 else r + math.ceil(math.log2(4 * h * R / beta))
    tail = M * ((1 << r) - 1)
    return dict(n=n, r=r, beta=beta, stages=h, M=M, p=p, R=R,
                delta=delta, t=t, J=J, tail_comparisons=tail)


def _pair_test(k: int, v: int, sampler: PrefixSampler, source: Source,
               rng: random.Random, meter: Meter):
    prefix = rng.getrandbits(k)
    meter.add("pair_prefix_random_bits", k)
    x0 = sampler.sample(prefix, rng, meter)
    x1 = sampler.sample(prefix, rng, meter)
    g0 = 1 ^ source(x0, x0 ^ v)
    g1 = 1 ^ source(x1, x1 ^ v)
    y0 = x0 ^ (v if g0 else 0)
    y1 = x1 ^ (v if not g1 else 0)
    passed = bool(source(y0, y1))
    meter.add("pair_tests")
    return passed


def _label(source: Source, v: int, x: int):
    return 1 ^ source(x, x ^ v)


def _candidate_from_polar(n: int, k: int, r: int, v: int,
                          prefix: AcquiredPrefix, source: Source,
                          rng: random.Random, cfg: dict, meter: Meter):
    """Fixed-J sampled-image / selected-column compact-polar reconstruction."""
    S = prefix.stabilizer
    sdim = len(S)
    source.phase = "polar_base"
    q0 = _label(source, v, 0)
    qe = [_label(source, v, 1 << i) for i in range(n)]
    rows = []
    for _ in range(cfg["J"]):
        z = combine(S, rng.getrandbits(sdim), meter)
        meter.add("polar_direction_random_bits", sdim)
        qz = _label(source, v, z)
        qzi = [_label(source, v, z ^ (1 << i)) for i in range(n)]
        row = 0
        for i in range(n):
            if qzi[i] ^ qz ^ qe[i] ^ q0:
                row |= 1 << i
        rows.append(row)
        meter.add("sampled_polar_rows")
        meter.add("polar_row_coordinates", n)

    row_basis, pivots = echelon(rows, n, meter)
    b = len(row_basis)
    meter.add("sampled_image_rank_checks")
    if b > r:
        return None, dict(status="UNKNOWN", reason="sampled_image_rank_exceeds_r",
                          sampled_image_rank=b, stabilizer_dimension=sdim)

    # RREF gives an invertible selected-column submatrix equal to I_b.
    # For each basis vector of S, measure only the selected derivative columns.
    images = []
    source.phase = "selected_columns"
    for z in S:
        qz = _label(source, v, z)
        selected = 0
        for j, i in enumerate(pivots):
            qzi = _label(source, v, z ^ (1 << i))
            derivative = qzi ^ qz ^ qe[i] ^ q0
            selected |= derivative << j
        image = 0
        for j, row in enumerate(row_basis):
            if (selected >> j) & 1:
                image ^= row
                meter.add("selected_row_basis_xors")
        images.append(image)
        meter.add("selected_column_rows")
        meter.add("selected_column_derivatives", b)

    # The reconstructed map is S -> W. Its kernel is N-hat. If image samples
    # missed a true polar direction, this kernel can be too large; the dim
    # guard below does not certify completeness.
    map_rows = []
    for i in range(n):
        map_rows.append(sum(((image >> i) & 1) << j for j, image in enumerate(images)))
    coeff_kernel = kernel(map_rows, sdim, meter)
    Nhat = [combine(S, c, meter) for c in coeff_kernel]
    n_hat_dim = len(Nhat)
    min_dim = n - r - k
    if n_hat_dim < min_dim:
        return None, dict(status="UNKNOWN", reason="estimated_kernel_dimension_below_promise",
                          sampled_image_rank=b, estimated_kernel_dimension=n_hat_dim,
                          minimum_kernel_dimension=min_dim)

    U = complement(Nhat, n, meter)
    u = len(U)
    if u > k + r:
        return None, dict(status="UNKNOWN", reason="quotient_dimension_guard",
                          sampled_image_rank=b, estimated_kernel_dimension=n_hat_dim,
                          quotient_dimension=u)

    # Interpolate q on U. q(0) is already available from the polar base labels.
    source.phase = "quotient_interpolation"
    qU_values = {0: q0}
    qU_points = [0]
    qU_points.extend(1 << i for i in range(u))
    qU_points.extend((1 << i) | (1 << j) for i in range(u) for j in range(i + 1, u))
    for c in qU_points[1:]:
        x = combine(U, c, meter)
        qU_values[c] = _label(source, v, x)
    qU = interpolate(qU_values, u, meter)

    source.phase = "kernel_response"
    lambda_mask = 0
    for j, z in enumerate(Nhat):
        response = _label(source, v, z) ^ q0
        lambda_mask |= response << j
    meter.add("kernel_response_queries", len(Nhat))

    # Coordinates in the direct-sum basis U + N-hat define the learned
    # quadratic f(y+z)=q_U(y)+lambda(z). Expand from local evaluations only.
    basis = U + Nhat
    basis_rows = [sum(((basis[j] >> i) & 1) << j for j in range(n)) for i in range(n)]
    coord_rows = matrix_inverse(basis_rows, n, meter)

    def f_eval(x):
        coords = linear(coord_rows, x, meter)
        y = coords & ((1 << u) - 1)
        z = coords >> u
        return qU(y, meter) ^ parity(lambda_mask & z, meter)

    global_points = coefficient_points(n)
    f_values = {x: f_eval(x) for x in global_points}
    meter.add("candidate_global_anchor_evaluations", len(global_points))
    f = interpolate(f_values, n, meter)
    if not f.toggles(v, meter):
        return None, dict(status="UNKNOWN", reason="post_interpolation_own_toggle_failed",
                          sampled_image_rank=b, estimated_kernel_dimension=n_hat_dim,
                          quotient_dimension=u)
    if not all(old.translation_invariant(v, meter) for old in prefix.q):
        return None, dict(status="UNKNOWN", reason="selected_toggle_not_in_acquired_stabilizer",
                          sampled_image_rank=b, estimated_kernel_dimension=n_hat_dim,
                          quotient_dimension=u)

    return f, dict(status="accepted_candidate", sampled_image_rank=b,
                    estimated_kernel_dimension=n_hat_dim, quotient_dimension=u,
                    selected_pivot_columns=pivots, selected_column_rows=len(S),
                    q_quotient_anchor_count=len(qU_points),
                    kernel_response_count=len(Nhat))


def acquire(n: int, r: int, query, seed: int, beta: float = 0.01):
    """Acquire an n-coordinate quadratic model using comparisons only."""
    start = time.perf_counter()
    cfg = parameters(n, r, beta)
    rng = random.Random(seed)
    meter = Meter()
    source = Source(query)
    prefix = AcquiredPrefix(n, meter)
    stages = []

    for k in range(cfg["stages"]):
        stage_start = time.perf_counter()
        before = len(prefix.stabilizer)
        sampler = prefix.sampler()
        winner = None
        trials = []
        for j in range(cfg["R"]):
            direction_coeff = rng.getrandbits(len(prefix.stabilizer))
            v = combine(prefix.stabilizer, direction_coeff, meter)
            meter.add("direction_random_bits", len(prefix.stabilizer))
            if v == 0:
                trials.append(dict(trial=j, direction=0, status="zero_direction", pair_tests=0))
                continue
            source.phase = "pair_validation"
            passed = True
            used = 0
            for _ in range(cfg["t"]):
                used += 1
                if not _pair_test(k, v, sampler, source, rng, meter):
                    passed = False
                    break
            trials.append(dict(trial=j, direction=v,
                               status="accepted_raw" if passed else "pair_inversion_rejected",
                               pair_tests=used, comparisons=3 * used))
            if passed:
                winner = v
                break
        if winner is None:
            stages.append(dict(stage=k, dimension_S_before=before, trials=trials,
                               stage_seconds=time.perf_counter() - stage_start))
            return dict(status="UNKNOWN", reason="direction_cap_exhausted", parameters=cfg,
                        stages=stages, comparison_calls=source.calls,
                        source_calls_by_phase=dict(source.by_phase),
                        local_operations=dict(meter.ops),
                        elapsed_seconds=time.perf_counter() - start), None, prefix

        f, polar_receipt = _candidate_from_polar(n, k, r, winner, prefix, source,
                                                  rng, cfg, meter)
        if f is None:
            stages.append(dict(stage=k, dimension_S_before=before, winner=winner,
                               trials=trials, polar=polar_receipt,
                               stage_seconds=time.perf_counter() - stage_start))
            return dict(status="UNKNOWN", reason=polar_receipt["reason"], parameters=cfg,
                        stages=stages, comparison_calls=source.calls,
                        source_calls_by_phase=dict(source.by_phase),
                        local_operations=dict(meter.ops),
                        elapsed_seconds=time.perf_counter() - start), None, prefix
        prefix.add(f, winner)
        stages.append(dict(stage=k, dimension_S_before=before,
                           dimension_S_after=len(prefix.stabilizer), winner=winner,
                           trials=trials, polar=polar_receipt,
                           stage_seconds=time.perf_counter() - stage_start))

    # Exact suffix acquisition: enumerate the 2^r points in each acquired
    # prefix fiber and count how many precede each coefficient anchor.
    tail_start = time.perf_counter()
    source.phase = "tail_enumeration"
    points = coefficient_points(n)
    values = [dict() for _ in range(r)]
    suffix_sampler = prefix.sampler()
    for x in points:
        pfx = prefix.prefix(x)
        local_rank = sum(source(y, x) for y in suffix_sampler.fiber(pfx) if y != x)
        for j in range(r):
            values[j][x] = (local_rank >> (r - j - 1)) & 1
    suffix = [interpolate(values[j], n, meter) for j in range(r)]
    model = list(prefix.q) + suffix
    expected_tail = cfg["M"] * ((1 << r) - 1)
    if source.by_phase["tail_enumeration"] != expected_tail:
        raise ArithmeticError("tail comparison accounting mismatch")
    result = dict(status="returned_model", parameters=cfg, stages=stages,
                  comparison_calls=source.calls, source_calls_by_phase=dict(source.by_phase),
                  random_bits=dict((key, value) for key, value in meter.ops.items()
                                   if key.endswith("random_bits")),
                  local_operations=dict(meter.ops),
                  tail_comparisons=source.by_phase["tail_enumeration"],
                  tail_seconds=time.perf_counter() - tail_start,
                  acquisition_seconds=time.perf_counter() - start,
                  model_bodies=[q.body() for q in model],
                  acquired_toggle_vectors=list(prefix.toggles),
                  acquired_prefix_dimension=len(prefix.q),
                  acquired_stabilizer_basis=list(prefix.stabilizer))
    return result, model, prefix


class CompiledModel:
    """Execution helpers built only from the returned acquired model."""
    def __init__(self, model, toggles, n: int, r: int):
        self.model = list(model)
        self.n, self.r = n, r
        self.h = n - r
        self.prefix_q = self.model[:self.h]
        self.toggles = list(toggles)
        self._fiber_basis = complement(self.toggles, self.n)

    def rank(self, x: int) -> int:
        out = 0
        for q in self.model:
            out = (out << 1) | q(x)
        return out

    def prefix(self, x: int, k: int | None = None) -> int:
        k = self.h if k is None else k
        out = 0
        for q in self.prefix_q[:k]:
            out = (out << 1) | q(x)
        return out

    def prefix_sampler(self, k: int):
        q = self.prefix_q[:k]
        w = self.toggles[:k]
        S = common_stabilizer(q, self.n)
        return PrefixSampler(q, w, S, self.n)

    def fiber(self, prefix: int):
        for seed in range(1 << len(self._fiber_basis)):
            x = combine(self._fiber_basis, seed)
            for i, (q, v) in enumerate(zip(self.prefix_q, self.toggles)):
                bit = (prefix >> (self.h - i - 1)) & 1
                if q(x) != bit:
                    x ^= v
            yield x

    def inverse(self, rank: int):
        pfx = rank >> self.r
        hits = [x for x in self.fiber(pfx) if self.rank(x) == rank]
        return hits

