"""Finite-budget sampling control for a supplied two-setting reset interface.

All controller probabilities and certificate inequalities use integers/Fraction.
The source callback must consume n fresh outcomes for source_count(cell, arm, n).
It is NOT an uncharged binomial-count oracle. Physical execution is not provided.
The controller never receives the unknown arm populations.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from fractions import Fraction as F
from typing import Callable


def ceil_fraction(x: F) -> int:
    return -(-x.numerator // x.denominator)


def ceil_log2(x: F) -> int:
    """Smallest nonnegative h with 2**h >= x, exactly."""
    if x <= 1:
        return 0
    h = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    if (1 << h) * x.denominator < x.numerator:
        h += 1
    return h


def dyadic_coin(p: F, bits: int, getbits: Callable[[int], int]) -> int:
    """Probability floor(2**bits*p)/2**bits; exactly bits fair bits consumed."""
    if not 0 <= p <= 1:
        raise ValueError("Probability outside [0,1]")
    threshold = ((1 << bits) * p.numerator) // p.denominator
    u = getbits(bits)
    if not 0 <= u < (1 << bits):
        raise ValueError("Invalid fair-bit block")
    return int(u < threshold)


@dataclass(frozen=True)
class Plan:
    cells: int
    target: F
    cold_upper: F
    hot_lower: F
    contrast: F
    mode: str
    n: int
    rounds_per_cell: int
    total_rounds: int
    fair_bits_per_draw: int
    clip_exponent: int
    race_exponent: int
    clip_bound: F
    race_bound: F
    bit_bound: F

    @property
    def margin(self) -> F:
        return min(self.target-self.cold_upper, self.hot_lower-self.target)

    @property
    def gap(self) -> F:
        return self.hot_lower-self.cold_upper

    @property
    def query_cap(self) -> int:
        return self.n*self.total_rounds

    @property
    def fair_bit_cap(self) -> int:
        return 2*self.fair_bits_per_draw*self.total_rounds

    @property
    def algorithm_error_bound(self) -> F:
        return self.clip_bound+self.race_bound+self.bit_bound

    def certificate(self) -> dict:
        r = {k: str(v) if isinstance(v, F) else v for k, v in asdict(self).items()}
        r.update(margin=str(self.margin), gap=str(self.gap),
                 query_cap=self.query_cap, fair_bit_cap=self.fair_bit_cap,
                 algorithm_error_bound=str(self.algorithm_error_bound),
                 checks={
                     "clipping": 2*self.n*self.margin**2 >= self.clip_exponent,
                     "global_success_count": self.mode != "global" or
                         self.total_rounds*self.gap >= 2*self.cells+8*self.race_exponent,
                     "per_cell_race": self.mode != "per_cell" or
                         self.rounds_per_cell*self.gap >= self.race_exponent,
                 })
        return r


def compile_plan(cells: int, target: F, cold_upper: F, hot_lower: F,
                 clip_budget: F, race_budget: F, bit_budget: F,
                 mode: str = "global", contrast: F = F(1)) -> Plan:
    if cells < 1 or not 0 <= cold_upper < target < hot_lower <= 1:
        raise ValueError("A positive population bracket is required")
    if mode not in {"global", "per_cell"}:
        raise ValueError("Unknown scheduling mode")
    if not 0 < contrast <= 1:
        raise ValueError("A calibrated positive observation contrast is required")
    if not all(0 < x < 1 for x in (clip_budget, race_budget, bit_budget)):
        raise ValueError("Budgets must lie in (0,1)")
    eta = min(target-cold_upper, hot_lower-target)
    gap = hot_lower-cold_upper
    hc = ceil_log2(F(2*cells)/(contrast*clip_budget))
    n = ceil_fraction(F(hc)/(2*eta**2))
    if mode == "global":
        hr = ceil_log2(1/race_budget)
        total = ceil_fraction(F(2*cells+8*hr)/gap)
        per_cell = 0
        race_bound = F(1, 1 << hr)
    else:
        hr = ceil_log2(F(cells)/race_budget)
        per_cell = ceil_fraction(F(hr)/gap)
        total = cells*per_cell
        race_bound = F(cells, 1 << hr)
    bits = ceil_log2(F(2*total)/bit_budget)
    p = Plan(cells, target, cold_upper, hot_lower, contrast, mode, n, per_cell,
             total, bits, hc, hr, F(2*cells, 1 << hc)/contrast, race_bound,
             F(2*total, 1 << bits))
    assert p.clip_bound <= clip_budget
    assert p.race_bound <= race_budget
    assert p.bit_bound <= bit_budget
    assert all(p.certificate()["checks"].values())
    return p


def bounded_commands(plan: Plan,
                     source_count: Callable[[int, int, int], int],
                     getbits: Callable[[int, int], int]) -> dict:
    """Arm 0 is cold, arm 1 hot. Returns all commands, including fallback.

    The public controller does not inspect source parameters or use source data
    again in another proposal. A timeout is NOT discarded or retried: its
    unconditional contribution is included in the analytic error certificate.
    """
    commands, timeouts = [], []
    rounds, queries, fair_bits = 0, 0, 0
    q, n, bits = plan.target, plan.n, plan.fair_bits_per_draw
    for cell in range(plan.cells):
        accepted = False
        local_rounds = 0
        while rounds < plan.total_rounds:
            if plan.mode == "per_cell" and local_rounds >= plan.rounds_per_cell:
                break
            hot = dyadic_coin(q, bits, lambda k: getbits(cell,k))
            fair_bits += bits
            # To choose hot, inspect cold. To choose cold, complement hot.
            arm = 0 if hot else 1
            s = source_count(cell,arm,n)
            if not isinstance(s, int) or not 0 <= s <= n:
                raise ValueError("Source must return a valid count of n fresh coins")
            if not hot:
                s = n-s
            v = q if hot else 1-q
            acceptance = max(F(0), 1-F(s, n)/v)
            yes = dyadic_coin(acceptance, bits, lambda k: getbits(cell,k))
            fair_bits += bits
            queries += n
            rounds += 1
            local_rounds += 1
            if yes:
                commands.append(hot)
                accepted = True
                break
        if not accepted:
            commands.append(0)
            timeouts.append(cell)
    assert rounds <= plan.total_rounds
    assert queries <= plan.query_cap
    assert fair_bits <= plan.fair_bit_cap
    return dict(commands=commands, timeouts=timeouts, rounds=rounds,
                source_outcomes=queries, fair_bits=fair_bits)


def native_population(lam: F, error: F, amplitude: F) -> F:
    if lam < 0 or error < 0 or amplitude <= 0:
        raise ValueError("Invalid supplied native parameters")
    return (lam+error*amplitude)/(2*lam+(1+2*error)*amplitude)


def native_bracket(lam_low: F, lam_high: F, error_low: F, error_high: F,
                   cold_amplitude: F, hot_amplitude: F, rate_cap: F) -> dict:
    if not 0 <= lam_low <= lam_high or not 0 <= error_low <= error_high:
        raise ValueError("Invalid parameter intervals")
    if not 0 < hot_amplitude < cold_amplitude <= rate_cap:
        raise ValueError("Native cap or ordering violated")
    return {
        "cold_lower": native_population(lam_low, error_low, cold_amplitude),
        "cold_upper": native_population(lam_high, error_high, cold_amplitude),
        "hot_lower": native_population(lam_low, error_low, hot_amplitude),
        "hot_upper": native_population(lam_high, error_high, hot_amplitude),
        "restoration_rate_lower": hot_amplitude/2,
        "maximum_activity_per_cell": lam_high+(1+error_high)*cold_amplitude,
    }


def physical_budget(plan: Plan, restoration_rate: F, probe_budget: F,
                    output_budget: F, extra_queries: int = 0) -> dict:
    """Finite native relaxation; measurement/control/holding errors are separate."""
    total_queries = plan.query_cap+extra_queries
    hp = ceil_log2(F(2*total_queries)/probe_budget)
    ho = ceil_log2(F(2*plan.cells)/output_budget)
    return {
        "probe_relaxation_time": str(F(hp)/restoration_rate),
        "output_relaxation_time": str(F(ho)/restoration_rate),
        "probe_complete_error_sum_bound": str(F(2*total_queries, 1 << hp)),
        "output_complete_error_sum_bound": str(F(2*plan.cells, 1 << ho)),
        "maximum_extra_error_per_probe_for_budget": str(probe_budget/total_queries),
        "extra_error_note": "The last allowance is separate from mixing and must be warranted; no measurement precision is acquired by this arithmetic.",
    }


def compile_fair_bit_plan(plan: Plan, source_low: F, source_high: F,
                          failure_budget: F) -> dict:
    """Von Neumann extraction using separately consumed cold-source outcomes."""
    if not 0 < source_low <= source_high < 1 or not 0 < failure_budget < 1:
        raise ValueError("An interior source interval and positive budget are required")
    variance_floor=min(source_low*(1-source_low),source_high*(1-source_high))
    success_floor=2*variance_floor
    if plan.mode=='per_cell':
        h=ceil_log2(F(plan.cells)/failure_budget)
        bits=plan.fair_bit_cap//plan.cells
        pairs_per_cell=ceil_fraction(F(2*bits+8*h)/success_floor)
        pairs=plan.cells*pairs_per_cell
        failure=F(plan.cells,1<<h)
    else:
        h=ceil_log2(1/failure_budget)
        pairs_per_cell=0
        pairs=ceil_fraction(F(2*plan.fair_bit_cap+8*h)/success_floor)
        failure=F(1,1<<h)
    assert failure <= failure_budget
    return dict(mode=plan.mode,source_low=str(source_low),source_high=str(source_high),
                pair_success_floor=str(success_floor),pair_cap=pairs,
                pair_cap_per_cell=pairs_per_cell,source_query_cap=2*pairs,
                failure_bound=str(failure),required_fair_bits=plan.fair_bit_cap,
                source_total_with_control=plan.query_cap+2*pairs)


class FairSourceExhausted(RuntimeError):
    pass


class SourceFairBits:
    """Fresh iid source pairs; 01 -> 0, 10 -> 1; equal pairs discarded.

    In per-cell mode each cell supplies its own bits. In global mode cell zero
    supplies the pooled bits, and this throughput limitation is part of cost.
    """
    def __init__(self, source_count, spec):
        self.source_count=source_count
        self.spec=spec
        self.used_pairs={}
        self.source_outcomes=0
        self.current_cell=None

    def __call__(self, cell, bits):
        key=cell if self.spec['mode']=='per_cell' else 0
        if self.spec['mode']=='per_cell' and key != self.current_cell:
            if self.current_cell is not None and key < self.current_cell:
                raise ValueError('Streaming per-cell source cannot revisit a completed cell')
            self.used_pairs.clear()
            self.current_cell=key
        cap=self.spec['pair_cap_per_cell'] if self.spec['mode']=='per_cell' else self.spec['pair_cap']
        value=0
        for _ in range(bits):
            while True:
                used=self.used_pairs.get(key,0)
                if used >= cap:
                    raise FairSourceExhausted('Paid source-pair budget exhausted')
                a=self.source_count(key,0,1)
                b=self.source_count(key,0,1)
                self.source_outcomes += 2
                self.used_pairs[key]=used+1
                if a != b:
                    value=2*value+a
                    break
        return value


def bounded_commands_with_source_bits(plan: Plan, source_count, fair_spec):
    bit_source=SourceFairBits(source_count,fair_spec)
    observed_control_queries=0
    def counted(cell,arm,n):
        nonlocal observed_control_queries
        observed_control_queries+=n
        return source_count(cell,arm,n)
    try:
        result=bounded_commands(plan,counted,bit_source)
        result['fair_source_timeout']=False
    except FairSourceExhausted:
        # Always produce a physical command. No postselection or silent retry.
        result=dict(commands=[0]*plan.cells, timeouts=list(range(plan.cells)),
                    source_outcomes=observed_control_queries,
                    fair_source_timeout=True)
    result['randomness_source_outcomes']=bit_source.source_outcomes
    result['all_source_outcomes']=observed_control_queries+bit_source.source_outcomes
    assert result['all_source_outcomes'] <= fair_spec['source_total_with_control']
    return result


def exact_weight(cold: F, hot: F, target: F) -> F:
    if not cold < target < hot:
        raise ValueError("Outside strict bracket")
    return (target-cold)/(hot-cold)


def query_lower_bounds(cold: F, hot: F, target: F, outputs: int = 1) -> dict:
    """Sequential KL/Fisher lower bounds for the selected-reset interface."""
    a, b, gap = hot-target, target-cold, hot-cold
    if min(a, b, cold, 1-hot) <= 0:
        raise ValueError("Interior parameters required")
    lc = outputs*cold*(1-cold)*a/(b*gap**2)
    lh = outputs*hot*(1-hot)*b/(a*gap**2)
    return {"cold_source": str(lc), "hot_source": str(lh), "total": str(lc+lh)}


def exact_query_upper(cold_upper: F, hot_lower: F, target: F,
                      outputs: int = 1, constant: F = F(19, 2)) -> F:
    """Huber 2014/2016 query guarantee; no expected bit-work claim."""
    ec = min((target-cold_upper)/target, F(1, 2))
    eh = min((hot_lower-target)/(1-target), F(1, 2))
    round_cost = constant*(1/ec+1/eh)
    return outputs*round_cost/(hot_lower-cold_upper)

