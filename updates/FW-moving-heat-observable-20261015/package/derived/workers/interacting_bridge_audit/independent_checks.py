"""Independent small-state and stiffness audit; standard-library only.

No worker/source scripts are imported. Decimal diagnostics supplement the
analytic proof in AUDIT.txt and are not interval/formal proof objects.
"""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json
import math


def dec(x):
    x = F(x)
    return D(x.numerator) / D(x.denominator)


def positive_exponential_action(generator, time, shift, initial, steps=240):
    """Positive shifted Taylor action exp(time G), using Decimal diagnostics."""
    q = [D(0)] * len(generator)
    q[initial] = D(1)
    accum = q[:]
    weight = D(1)
    for j in range(1, steps + 1):
        nxt = [D(0)] * len(generator)
        for s, row in enumerate(generator):
            if not q[s]:
                continue
            for dest, rate in row.items():
                coefficient = rate / shift + (D(1) if dest == s else D(0))
                assert coefficient >= 0
                nxt[dest] += q[s] * coefficient
        q = nxt
        weight *= shift * time / j
        accum = [v + weight * x for v, x in zip(accum, q)]
    factor = (-shift * time).exp()
    return [factor * v for v in accum]


def count_hit(rates, time):
    size = len(rates) + 1
    generator = []
    for s, rate in enumerate(rates):
        generator.append({s: -rate, s + 1: rate})
    generator.append({size - 1: D(0)})
    return positive_exponential_action(generator, time, max(rates), 0)[-1]


def small_model():
    n, k, beta, time = 4, 4, F(2), F(1, 5)
    mod = 65521
    wi = [[0 if i == j else (7919*(i+1) + 104729*(j+1)
                           + 97*(i+1)*(j+1)) % mod
           for j in range(n)] for i in range(n)]
    denom = mod*n*n
    eta = {}
    rates = {}
    for x in range(1 << n):
        s = x.bit_count()
        if s == k:
            continue
        for i in range(n):
            if not x >> i & 1:
                load = sum(wi[i][j] for j in range(n) if x >> j & 1)
                eta[x, i] = beta*F(load, denom)
                rates[x, i] = F(n, n-s)*(1 + eta[x, i])
    gen, tilted = [], []
    maxexit, maxshift = F(0), F(0)
    aggregate_updates = 0
    marked_acceptance_cases = 0
    for x in range(1 << n):
        s = x.bit_count()
        if s == k:
            gen.append({x: D(0)})
            tilted.append({x: D(0)})
            continue
        alive = [i for i in range(n) if not x >> i & 1]
        total = sum((rates[x, i] for i in alive), F(0))
        base = F(n)
        maxexit = max(maxexit, total)
        maxshift = max(maxshift, 2*total-base)
        gen.append({x: -dec(total), **{x | 1 << i: dec(rates[x, i]) for i in alive}})
        tilted.append({x: dec(base-2*total), **{
            x | 1 << i: dec(rates[x, i]**2 / F(n, n-s)) for i in alive}})
        # Check marked thinning acceptance identity independently at a rational
        # holding duration, including aggregate asymmetry at every prefix.
        delta = F(s+1, 100)
        c = beta/n
        rho = sum((eta[x, i]/c for i in alive), F(0))/len(alive)
        poisson_mean = c*base*delta
        desired_holding = (total-base)*delta
        assert poisson_mean*rho == desired_holding
        marked_acceptance_cases += 1
    p = positive_exponential_action(gen, dec(time), dec(maxexit), 0)[-1]
    unconditioned_second = positive_exponential_action(
        tilted, dec(time), dec(maxshift), 0)[-1]
    h = count_hit([D(n)]*k, dec(time))
    C = math.prod((1+beta*F(s,n*n) for s in range(k)), start=F(1))
    path_rsm = h*unconditioned_second/(p*p)
    cmc = []
    per_path_weights = []
    columns = [sum(wi[i][j] for i in range(n)) for j in range(n)]
    for order in permutations(range(n), k):
        x, prefix, S = 0, [], 0
        ratio = F(1)
        stage_rates = []
        J = F(1)
        Hdirect, Hupdate = F(0), F(0)
        for s, i in enumerate(order):
            alive = [j for j in range(n) if not x >> j & 1]
            total = sum((rates[x,j] for j in alive), F(0))
            stage_rates.append(dec(total))
            average = sum((eta[x,j] for j in alive), F(0))/len(alive)
            ratio *= (1+eta[x,i])/(1+average)
            J *= 1+eta[x,i]
            delta = F(s+1, 100)
            Hdirect += (total-n)*delta
            Hupdate += F(n,n-s)*beta*F(S,denom)*delta
            load = sum(wi[i][j] for j in prefix)
            colremoved = sum(wi[j][i] for j in prefix)
            S += columns[i]-load-colremoved
            prefix.append(i)
            x |= 1 << i
            independent = sum(wi[r][j] for r in range(n) if not x >> r & 1
                              for j in range(n) if x >> j & 1)
            assert S == independent
            aggregate_updates += 1
        assert Hdirect == Hupdate
        per_path_weights.append(dec(J)*(-dec(Hdirect)).exp())
        cmc.append(dec(ratio)*count_hit(stage_rates, dec(time)))
    cmc_mean = sum(cmc)/len(cmc)
    cmc_rsm = (sum(x*x for x in cmc)/len(cmc))/(cmc_mean*cmc_mean)
    assert abs(cmc_mean-p) < D('1e-60')
    assert D(1) <= cmc_rsm <= path_rsm <= dec(C)
    assert h <= p <= dec(C)*h
    assert max(per_path_weights) <= dec(C)
    return {
        'n': n, 'k': k, 'T': str(time), 'beta': str(beta),
        'reference_h': str(h), 'target_p_enumerated_generator': str(p),
        'target_p_permutation_cmc': str(cmc_mean),
        'absolute_generator_vs_cmc_difference': str(abs(cmc_mean-p)),
        'path_likelihood_relative_second_moment': str(path_rsm),
        'permutation_cmc_relative_second_moment': str(cmc_rsm),
        'analytic_likelihood_cap': str(dec(C)),
        'exact_integer_aggregate_update_cases': aggregate_updates,
        'exact_marked_acceptance_identity_cases': marked_acceptance_cases,
        'all_assertions_passed': True,
    }


def conditional_uniformization_tail():
    rates = [F(1,7), F(8), F(1,2)]
    k, time = len(rates), F(1,3)
    B = max(rates)
    mu = dec(B*time)
    v = [F(0)]*k + [F(1)]
    weights = []
    pois = (-mu).exp()
    poisson = []
    for m in range(180):
        if m:
            v = [(1-rates[s]/B)*v[s] + rates[s]/B*v[s+1]
                 for s in range(k)] + [F(1)]
            pois *= mu/m
        poisson.append(pois)
        weights.append(pois*dec(v[0]))
    h = sum(weights)
    checks = []
    for j in [0, 1, 2, 4, 8, 12, 20, 30]:
        actual = sum(weights[k+j+1:])/h
        domination = sum(poisson[j+1:])
        assert actual <= domination + D('1e-80')
        checks.append({'j': j, 'actual_conditional_tail': str(actual),
                       'pois_BT_upper_tail_bound': str(domination)})
    conditional_mean = sum(D(m)*w for m,w in enumerate(weights))/h
    assert conditional_mean <= k+mu
    return {'rates': [str(x) for x in rates], 'T': str(time), 'h': str(h),
            'conditioned_augmented_count_mean': str(conditional_mean),
            'mean_upper_bound_k_plus_BT': str(k+mu), 'checks': checks,
            'all_assertions_passed': True}


def stiff_counterexample():
    examples = []
    for m in [4,8,16,32]:
        eps = D(2)**(-m)
        r0, r1 = eps, 1/eps
        h = 1-(r1*(-r0).exp()-r0*(-r1).exp())/(r1-r0)
        examples.append({'rate_input_exponent_bits': m, 'b0': str(r0),
                         'b1_equal_BT': str(r1), 'h': str(h),
                         'h_over_epsilon': str(h/eps),
                         'BT_times_h': str(r1*h)})
    return examples


def main():
    with localcontext() as context:
        context.prec = 90
        out = {
            'scope': 'Independent exact rational identities and high-precision Decimal small-state diagnostics; not interval certification or proof of iid PRNG bits.',
            'small_dense_model': small_model(),
            'nonmonotone_count_tail': conditional_uniformization_tail(),
            'stiff_counterexample': stiff_counterexample(),
        }
        path = Path(__file__).with_name('independent_results.json')
        path.write_text(json.dumps(out, indent=2)+'\n')
        print(json.dumps({
            'all_assertions_passed': True,
            'target_p': out['small_dense_model']['target_p_enumerated_generator'],
            'path_RSM': out['small_dense_model']['path_likelihood_relative_second_moment'],
            'CMC_RSM': out['small_dense_model']['permutation_cmc_relative_second_moment'],
            'output': str(path),
        }, indent=2))


if __name__ == '__main__':
    main()
