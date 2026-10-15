#!/usr/bin/env python3
"""Bounded exact diagnostics only; no supplied SSA execution or imports.

All model arithmetic uses Fraction. The only floating operations are descriptive
exp/expm1 evaluations for a constant-hazard, analytically contracted fixture.
"""
from fractions import Fraction as F
from itertools import combinations
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/harjas/Downloads/astra_kinetic_investigation')


def solve(a, b):
    a = [list(row) + [rhs] for row, rhs in zip(a, b)]
    n = len(a)
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        z = a[j][j]
        a[j] = [x / z for x in a[j]]
        for i in range(n):
            if i != j:
                z = a[i][j]
                a[i] = [x - z*y for x, y in zip(a[i], a[j])]
    return [row[-1] for row in a]


def matrix_vec(a, x):
    return [sum((z*y for z, y in zip(row, x)), F(0)) for row in a]


def serialize(x):
    if isinstance(x, F):
        return {'rational': str(x), 'float': float(x)}
    if isinstance(x, dict):
        return {str(k): serialize(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serialize(y) for y in x]
    return x


def local_obstacle(q, success, failure, v, domain, outside):
    """Exact finite-domain obstacle solve by enumerating contact sets.

    Only a three-state fixture is passed. This is deliberately NOT a scalable
    solver. A candidate satisfies g>=v, Lg<=0 and complementarity on domain.
    """
    n = len(q)
    domain = list(domain)
    candidates = []
    for count in range(len(domain) + 1):
        for contact in combinations(domain, count):
            contact = set(contact)
            continuation = [i for i in domain if i not in contact]
            g = list(outside)
            for i in contact:
                g[i] = v[i]
            a, b = [], []
            for i in continuation:
                total = sum(q[i]) + success[i] + failure[i]
                a.append([total if i == j else -q[i][j]
                          for j in continuation])
                b.append(success[i] + sum(q[i][j]*g[j] for j in range(n)
                                          if j not in continuation))
            if continuation:
                values = solve(a, b)
                for i, value in zip(continuation, values):
                    g[i] = value
            drift = [sum(q[i][j]*(g[j]-g[i]) for j in range(n))
                     + success[i]*(1-g[i])-failure[i]*g[i]
                     for i in range(n)]
            if all(g[i] >= v[i] and drift[i] <= 0 for i in domain):
                if all((g[i]-v[i])*drift[i] == 0 for i in domain):
                    candidates.append((g, drift, sorted(contact)))
    assert candidates, 'No obstacle candidate'
    g, drift, contact = min(candidates, key=lambda x: sum(x[0]))
    assert all(all(g[i] <= other[0][i] for i in domain)
               for other in candidates)
    assert all(x <= 0 for x in drift), 'Extension is not globally superharmonic'
    return g, drift, contact, len(candidates)


def boundary_risk(q, success, failure, domain, outside):
    domain = list(domain)
    n = len(q)
    a, b = [], []
    for i in domain:
        total = sum(q[i]) + success[i] + failure[i]
        a.append([total if i == j else -q[i][j] for j in domain])
        b.append(sum(q[i][j]*outside[j] for j in range(n) if j not in domain))
    e = list(outside)
    for i, z in zip(domain, solve(a, b)):
        e[i] = z
    return e


def run():
    start = time.perf_counter()
    # Source receipts read bytes; do not execute the supplied implementation.
    receipts = {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
                for name in ['REPORT.md', 'PROOFS.md', 'input_contract.json',
                             'kinetics.py']}

    # Exact initial-state local rate acquisition: 16 local changes + 20 edges.
    n = 50
    birth = F('2.676')*n*(n-1)+F('108.102')
    death = F('0.040')*n*(n-1)*(n-2)+F('37.881')*n
    diffusion = 20*F('8.2207')*n
    initial_rate = 8*(birth+death)+diffusion
    assert birth == F('6664.302')
    assert death == F('6598.05')
    assert initial_rate == F('114319.516')

    # Count drift proves a nonexplosion certificate with a coercive linear V.
    def count_drift(n):
        return (-F('0.040')*n**3+F('2.796')*n**2
                -F('40.637')*n+F('108.102'))
    max_n, max_drift = max(((n, count_drift(n)) for n in range(70)),
                           key=lambda x: x[1])
    # For n>=70, n²(2.796-.040n)<=0 and -40.637n+108.102<0.
    assert F('2.796')-F('0.040')*70 < 0
    assert -F('40.637')*70+F('108.102') < 0
    assert max_drift > 0

    # Source-complete exponential overflow certificate on the full eight sites.
    # r=1.61 was selected from a bounded exploratory grid 1+k/100, k=1..100.
    # Verification needs only the fixed rational r and 111 scalar evaluations.
    r = F(161,100)
    cutoff = 111
    cubic_quadratic = F('2.676')*r+F('0.120')
    cubic_linear = -F('2.676')*r-F('37.961')+3*F('8.2207')*(r-1)
    cubic_constant = r*F('108.102')
    assert cubic_quadratic-F('0.040')*cutoff < 0
    assert cubic_linear < 0
    assert cubic_linear*cutoff+cubic_constant < 0

    def exponential_drift_factor(n):
        b = F('2.676')*n*(n-1)+F('108.102')
        a = F('0.040')*n*(n-1)*(n-2)+F('37.881')*n
        return (b*(r-1)+a*(1/r-1)
                +3*F('8.2207')*n*(r+1/r-2))

    tail_max_n, tail_k = max(
        ((n, r**n*exponential_drift_factor(n)) for n in range(cutoff)),
        key=lambda z: z[1])
    assert tail_max_n == 103
    # For n>=111, r*F_r/(r-1) is the above cubic, proved strictly negative.
    overflow_bound = (8*r**50+8*tail_k)/r**163
    assert overflow_bound < F(1,10**9)
    assert overflow_bound*r > F(1,10**9)

    # Incoming branching fixture. Exact obstruction witness, then exact repair.
    kappa, p, delta = F(1, 10**6), F(1, 10**12), F(1, 100)
    q = [[F(0) if i == j else F(1) for j in range(3)] for i in range(3)]
    success, failure = [kappa*p]*3, [kappa*(1-p)]*3
    v = [p*(1+delta), p, p*(1-delta)]
    a = [1+delta, F(1), 1-delta]
    old_k = [[F(0) if i == j else
              (sum(a[l] for l in range(3) if l != i)+kappa)
              / ((2+kappa)**2*a[j]) for j in range(3)] for i in range(3)]
    witness = [F(100000017,100000000), F(125006261,125000000), F(1)]
    growth = [x-y for x, y in zip(matrix_vec(old_k, witness), witness)]
    assert all(x > 0 for x in growth)

    g, drift, contact, _ = local_obstacle(q, success, failure, v,
                                         range(3), [F(1)]*3)
    expected = [p*(1+delta), p*(1+delta/(1+kappa)),
                p*(1+delta/(1+kappa))]
    assert g == expected
    kill = [-drift[i]/g[i] for i in range(3)]
    repaired_routing, row_sums = [], []
    for i in range(3):
        total = 2+kappa
        routing = [q[i][j]*g[j]/(g[i]*total) for j in range(3)]
        success_probability = success[i]/(g[i]*total)
        defect_probability = kill[i]/total
        row_sums.append(sum(routing)+success_probability+defect_probability)
        assert row_sums[-1] == 1
        repaired_routing.append(dict(internal=routing,
                                     success=success_probability,
                                     defect=defect_probability))
    # The success probabilities solve the repaired substochastic chain exactly.
    repaired_success = solve(
        [[F(i == j)-repaired_routing[i]['internal'][j]
          for j in range(3)] for i in range(3)],
        [row['success'] for row in repaired_routing])
    assert repaired_success == [p/x for x in g]

    # Partial-graph certificates: unknown outside is safely bounded by one.
    local = []
    for domain in [[0], [0,1], [0,1,2]]:
        gd, dd, ct, candidate_count = local_obstacle(
            q, success, failure, v, domain, [F(1)]*3)
        e = boundary_risk(q, success, failure, domain, [F(1)]*3)
        assert all(gd[i] <= (1+delta)*p+e[i] for i in domain)
        local.append(dict(domain=domain, local_obstacle_rows=len(domain),
                          initial_envelope=gd[0], initial_boundary_risk=e[0],
                          normalized_second_moment=gd[0]/p,
                          upper_moment_bound=1+delta+e[0]/p,
                          contact=ct, candidate_count=candidate_count))

    # Finite deadline: linear envelope c*p*kappa*(T-t), not the exact h(t).
    c, horizon = 1+delta, 1.0
    x = float(kappa)*horizon
    true_by_deadline = float(p)*(-math.expm1(-x))
    envelope = float(c*p*kappa)*horizon
    finite_ratio = envelope/true_by_deadline
    assert 1 <= finite_ratio <= float(c)*(1+x)
    # At any remaining time r: -(∂+L)g = p*kappa*(delta+c*kappa*r).
    for rem in [F(1), F(1,100), F(1,10**9)]:
        gg = c*p*kappa*rem
        negative_defect = p*kappa*(delta+c*kappa*rem)
        rate_b = kappa*p/gg
        rate_k = negative_defect/gg
        assert rate_b+rate_k == kappa+1/rem
        assert rate_b == 1/(c*rem)

    result = dict(
        status='BOUNDED_DIAGNOSTICS_PASSED_NO_BENCHMARK_SSA_EXECUTED',
        source_sha256=receipts,
        benchmark=dict(initial_birth_per_site=birth,
                       initial_death_per_site=death,
                       initial_total_diffusion=diffusion,
                       initial_total_event_rate=initial_rate,
                       local_channels_acquired=36,
                       one_state_domain_boundary_risk='1-exp(-114319.516)',
                       exact_lower_bound='greater than 1-2^(-114319)',
                       global_overflow_certificate=dict(
                           lyapunov='sum_i (161/100)^n_i',
                           r=r, positive_region_cutoff=cutoff,
                           scalar_max_attained_at=tail_max_n,
                           scalar_global_upper_drift=tail_k,
                           full_global_upper_drift=8*tail_k,
                           horizon=1, first_overflow_count=163,
                           retained_counts='0,...,162 at every site',
                           exact_probability_upper_bound=overflow_bound,
                           bound_strictly_below='1e-9',
                           full_box_state_count=163**8,
                           suppressed_cap_semantics='absolute hit-probability bias <= bound; not one-sided',
                           absorbing_overflow_semantics='hit_mass <= true first-hit probability <= hit_mass+bound',
                           screening='100 rational r values screened before fixed-r exact replay; no global optimality claim'),
                       nonexplosion=dict(max_single_site_drift=max_drift,
                                         attained_at_count=max_n,
                                         full_count_drift_bound=8*max_drift,
                                         finite_enumeration_counts=70,
                                         analytic_tail_from_count=70)),
        eventual_triangle=dict(kappa=kappa, p=p, delta=delta,
                               old_second_moment_growth_witness=growth,
                               repaired_envelope=g, negative_drift=drift,
                               defect_killing_rates=kill,
                               repaired_success_probabilities=repaired_success,
                               normalized_second_moments=[x/p for x in g],
                               relative_variances=[x/p-1 for x in g],
                               constant_weight_estimator=True,
                               partial_domain_certificates=local),
        finite_horizon_constant_hazard=dict(horizon=horizon,
             envelope_construction='g(t,C)=(1+delta)*p*kappa*(T-t)',
             probability=true_by_deadline, initial_envelope=envelope,
             normalized_second_moment=finite_ratio,
             relative_variance=finite_ratio-1,
             rigorous_symbolic_upper_bound=serialize(c*(1+kappa)-1),
             terminal_sampling='min(Uniform(0,T),Exp(kappa)); uniform event succeeds with probability 1/(1+delta)',
             acquisition_limit='Constant hazard family has an exact phase-type incumbent; no advantage claim'),
        cost=dict(supplied_ssa_events_executed=0,
                  maximum_fixture_transient_states=3,
                  maximum_contact_sets=8,
                  benchmark_state_rows_evaluated=1,
                  model_drift_counts_checked=70,
                  exponential_certificate_counts_checked=cutoff,
                  preliminary_rational_screen_parameters=100,
                  arithmetic='exact fractions except descriptive exponential values',
                  wall_seconds=time.perf_counter()-start),
        environment=dict(python=sys.version, executable=sys.executable,
                         platform=platform.platform()),
    )
    (HERE/'diagnostics.json').write_text(json.dumps(serialize(result), indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],
                         wall_seconds=result['cost']['wall_seconds'],
                         finite_deadline_relative_variance=finite_ratio-1,
                         benchmark_overflow_probability_bound=float(overflow_bound),
                         initial_rate=str(initial_rate),
                         source_files_hashed=len(receipts)), indent=2))


if __name__ == '__main__':
    run()
