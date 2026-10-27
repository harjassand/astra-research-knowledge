#!/usr/bin/env python3
"""SYNTHETIC allocation counterexample. Standard library; no model/API calls.

Each candidate needs both a theory gate T and an interface gate I. T succeeds
with p_t per paid call. I first needs m paid preparation calls, then attempts
succeed with p_i conditional on one candidate-specific latent viable bit
Z~Bernoulli(q). If Z=0 they always fail. Failure updates the exact posterior.
The latent bits of distinct candidates are independent. Preparation persists.

Every policy has the same q,p_t,p_i,m, full history and B one-credit calls.
It never observes Z. Gate-optimal and program-optimal are exact finite-horizon
Bayesian dynamic programs with opposite primary terminal objectives. Ties in
either primary objective favor the other objective (rounded only for floating
point tie stability). A cheap Bayesian bottleneck index is also evaluated.
This is exact expectation enumeration, not a Monte Carlo estimate or Astra data.
"""

from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path


class Model:
    def __init__(self, n=3, budget=9, q=.35, p_t=.9, p_i=.7, maturation=2):
        self.n, self.budget = n, budget
        self.q, self.p_t, self.p_i, self.m = q, p_t, p_i, maturation
        # candidate = (theory_done, preparation_done, failures, interface_done)
        self.start = ((0, 0, 0, 0),) * n

    def posterior(self, failures):
        numerator = self.q * (1 - self.p_i) ** failures
        denominator = 1 - self.q + numerator
        return numerator / denominator if denominator else 0.0

    def replace(self, state, j, candidate):
        nxt = list(state)
        nxt[j] = candidate
        return tuple(sorted(nxt))

    def actions(self, state):
        result = []
        seen = set()
        for j, candidate in enumerate(state):
            if candidate in seen:
                continue
            seen.add(candidate)
            t, prep, failures, interface = candidate
            if not t:
                result.append((j, 'T'))
            if not interface:
                result.append((j, 'I'))
        return result or [(0, 'idle')]

    def transitions(self, state, action):
        j, kind = action
        t, prep, failures, interface = state[j]
        if kind == 'idle':
            return ((1.0, state),)
        if kind == 'T':
            return ((self.p_t, self.replace(state, j, (1, prep, failures, interface))),
                    (1 - self.p_t, state))
        if prep < self.m:
            return ((1.0, self.replace(state, j, (t, prep + 1, failures, 0))),)
        success = self.posterior(failures) * self.p_i
        return ((success, self.replace(state, j, (t, self.m, 0, 1))),
                (1 - success, self.replace(state, j, (t, prep, failures + 1, 0))))

    @staticmethod
    def terminal(state):
        programs = sum(t * interface for t, _, _, interface in state)
        theory = sum(t for t, _, _, _ in state)
        interface = sum(i for _, _, _, i in state)
        return (programs, float(programs > 0), theory + interface, theory, interface)

    def run(self, audit_hidden=False):
        @lru_cache(None)
        def optimal(remaining, state, objective):
            if remaining == 0:
                programs, _, gates, _, _ = self.terminal(state)
                return ((gates, programs) if objective == 'gate_optimal'
                        else (programs, gates)), None
            best, chosen = None, None
            for action in self.actions(state):
                value = [0.0, 0.0]
                for probability, nxt in self.transitions(state, action):
                    child, _ = optimal(remaining - 1, nxt, objective)
                    for k in range(2):
                        value[k] += probability * child[k]
                value = tuple(value)
                # Disregard only floating noise in otherwise exact ties.
                if best is None or tuple(round(x, 12) for x in value) > tuple(round(x, 12) for x in best):
                    best, chosen = value, action
            return best, chosen

        def bottleneck_index(remaining, state):
            candidates = []
            for action in self.actions(state):
                j, kind = action
                t, prep, failures, interface = state[j]
                if kind == 'idle':
                    return action
                # Complete an acquired interface; otherwise investigate the
                # uncertain complement before paying for its easy prerequisite.
                wanted = 'T' if interface else 'I'
                min_cost = (1 - t) + (0 if interface else self.m - prep + 1)
                if kind != wanted or min_cost > remaining:
                    continue
                conditional_cost = ((0 if t else 1 / self.p_t)
                                    + (0 if interface else self.m - prep + 1 / self.p_i))
                success_prior = 1.0 if interface else self.posterior(failures)
                candidates.append((success_prior / conditional_cost, action))
            if candidates:
                return max(candidates, key=lambda x: (x[0], -x[1][0]))[1]
            # No program can complete in the horizon: use gate-optimal fallback
            # to preserve useful partial work, not an unpaid early stop.
            return optimal(remaining, state, 'gate_optimal')[1]

        @lru_cache(None)
        def evaluate(remaining, state, policy):
            if remaining == 0:
                return tuple(float(v) for v in self.terminal(state))
            if policy == 'bottleneck_index':
                action = bottleneck_index(remaining, state)
            else:
                action = optimal(remaining, state, policy)[1]
            result = [0.0] * 5
            for probability, nxt in self.transitions(state, action):
                child = evaluate(remaining - 1, nxt, policy)
                for k in range(5):
                    result[k] += probability * child[k]
            return tuple(result)

        results = {}
        for policy in ('gate_optimal', 'program_optimal', 'bottleneck_index'):
            metric = evaluate(self.budget, self.start, policy)
            results[policy] = dict(zip(('expected_completed_programs', 'probability_any_completed',
                                       'expected_resolved_gates', 'expected_theory_gates',
                                       'expected_interface_gates'), metric))
            results[policy]['paid_credits'] = self.budget
            results[policy]['initial_action'] = (optimal(self.budget, self.start, policy)[1][1]
                                                  if policy != 'bottleneck_index'
                                                  else bottleneck_index(self.budget, self.start)[1])
        hidden_audit = None
        if audit_hidden:
            # Independent replay: enumerate Z explicitly and generate I outcomes
            # from p_i*Z, not from the posterior transition function above.
            def replace_joint(state, latent, j, candidate):
                pairs = list(zip(state, latent))
                pairs[j] = (candidate, latent[j])
                pairs.sort(key=lambda pair: pair[0])
                return tuple(x for x, _ in pairs), tuple(z for _, z in pairs)

            @lru_cache(None)
            def hidden_evaluate(remaining, state, latent, policy):
                if remaining == 0:
                    return self.terminal(state)
                action = (bottleneck_index(remaining, state) if policy == 'bottleneck_index'
                          else optimal(remaining, state, policy)[1])
                j, kind = action
                t, prep, failures, interface = state[j]
                if kind == 'idle':
                    branches = ((1., state, latent),)
                elif kind == 'T':
                    success_state, success_latent = replace_joint(state, latent, j, (1, prep, failures, interface))
                    branches = ((self.p_t, success_state, success_latent), (1-self.p_t, state, latent))
                elif prep < self.m:
                    nxt, next_latent = replace_joint(state, latent, j, (t, prep+1, failures, 0))
                    branches = ((1., nxt, next_latent),)
                else:
                    yes, yes_z = replace_joint(state, latent, j, (t, self.m, 0, 1))
                    no, no_z = replace_joint(state, latent, j, (t, prep, failures+1, 0))
                    chance = self.p_i * latent[j]
                    branches = ((chance, yes, yes_z), (1-chance, no, no_z))
                value = [0.] * 5
                for probability, nxt, next_latent in branches:
                    child = hidden_evaluate(remaining-1, nxt, next_latent, policy)
                    for k in range(5):
                        value[k] += probability * child[k]
                return tuple(value)

            hidden_audit = {}
            keys = ('expected_completed_programs', 'probability_any_completed',
                    'expected_resolved_gates', 'expected_theory_gates', 'expected_interface_gates')
            for policy in results:
                mixture = [0.] * 5
                for latent in itertools.product((0, 1), repeat=self.n):
                    weight = self.q ** sum(latent) * (1-self.q) ** (self.n-sum(latent))
                    value = hidden_evaluate(self.budget, self.start, latent, policy)
                    for k in range(5):
                        mixture[k] += weight * value[k]
                error = max(abs(mixture[k]-results[policy][key]) for k,key in enumerate(keys))
                assert error < 1e-10
                hidden_audit[policy] = {'max_metric_difference': error}
        assert results['program_optimal']['expected_completed_programs'] + 1e-9 >= max(
            results[x]['expected_completed_programs'] for x in results)
        assert results['gate_optimal']['expected_resolved_gates'] + 1e-9 >= max(
            results[x]['expected_resolved_gates'] for x in results)
        assert all(0 <= r['probability_any_completed'] <= 1 + 1e-9 for r in results.values())
        return {
            'parameters': {'n': self.n, 'budget': self.budget, 'q': self.q,
                           'p_t': self.p_t, 'p_i': self.p_i, 'maturation': self.m},
            'policies': results,
            'optimal_dp_cache': optimal.cache_info()._asdict(),
            'explicit_hidden_world_audit': hidden_audit,
        }


def main():
    base = Model().run(audit_hidden=True)
    cases = [
        ('q_low', {'q': .1}), ('q_high', {'q': .8}), ('q_certain', {'q': 1.0}),
        ('no_maturation', {'maturation': 0}), ('one_maturation', {'maturation': 1}),
        ('slow_maturation', {'maturation': 3}), ('interface_noisy', {'p_i': .3}),
        ('interface_nearly_certain', {'p_i': .95}), ('theory_hard', {'p_t': .3}),
        ('short_horizon', {'budget': 5}), ('longer_horizon', {'budget': 13}),
        ('no_complete_program_possible', {'budget': 3, 'maturation': 2}),
        ('all_easy_ample_budget', {'q': 1., 'p_t': 1., 'p_i': 1., 'maturation': 0}),
        # Exploratory stress cases selected after a coarse parameter scan;
        # these are sensitivity counterexamples, not preregistered estimates.
        ('index_failure_hard_theory', {'q': .5, 'p_t': .1, 'p_i': .5, 'maturation': 3}),
        ('index_failure_long_preparation', {'q': .9, 'p_t': 1., 'p_i': .9, 'maturation': 3}),
    ]
    sensitivity = {name: Model(**change).run() for name, change in cases}
    # Minimal analytic audit: total P(I success after k tries) equals the latent
    # mixture law, independently of the posterior sequential implementation.
    survival = 1.0
    for k in range(1, 13):
        survival *= 1 - Model().posterior(k - 1) * .7
        assert abs((1 - survival) - .35 * (1 - .3 ** k)) < 1e-12
    result = {
        'status': 'SYNTHETIC_EXACT_COUNTEREXAMPLE_NOT_ASTRA_EVIDENCE',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'method': 'Finite-horizon Bayesian dynamic programming; exact transition enumeration with binary64 arithmetic; no sampling.',
        'base': base, 'sensitivity': sensitivity,
        'correlated_repetition': {
            'q': .35, 'p_i_given_viable': .7, 'attempts': 10,
            'true_probability_any_interface_success': .35 * (1 - .3 ** 10),
            'iid_marginal_fiction': 1 - (1 - .35 * .7) ** 10,
            'pairwise_outcome_correlation': .7 * (1 - .35) / (1 - .35 * .7),
        },
        'checks': ['Bellman dominance for both terminal objectives in every case',
                   'Probability bounds', 'Posterior/latent-mixture identity at attempts 1..12',
                   'All three base policies replayed against explicit hidden Z rather than posterior transitions'],
    }
    output = Path(__file__).with_name('results.json')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
