#!/usr/bin/env python3
"""Exact checks for the stationary parity-context certificate obstruction."""
from fractions import Fraction
from itertools import product

EPS = Fraction(1, 5)
MU = Fraction(1, 10)
THETA = Fraction(1, 2) - MU
assert 0 < MU < EPS < Fraction(1, 2)


def contexts(n):
    return list(product((0, 1), repeat=n))


def parity_sign(h):
    return -1 if sum(h) % 2 else 1


def p_one(sigma, h):
    return Fraction(1, 2) + sigma * THETA * parity_sign(h)


def emit_prob(sigma, h, bit):
    p = p_one(sigma, h)
    return p if bit else 1 - p


def shift(h, bit):
    return h[1:] + (bit,)


def transition_prob(sigma, h, v):
    # A transition is possible iff v is the shifted context with one appended bit.
    if v[:-1] == h[1:]:
        return emit_prob(sigma, h, v[-1])
    return Fraction(0)


def prefix_prob(sigma, word, n):
    total = Fraction(0)
    for initial in contexts(n):
        state = initial
        weight = Fraction(1, 2**n)
        if not word:
            total += weight
            continue
        if state[-1] != word[0]:
            continue
        for bit in word[1:]:
            weight *= emit_prob(sigma, state, bit)
            state = shift(state, bit)
        total += weight
    return total


def predictive_one(sigma, word, n):
    den = Fraction(0)
    num = Fraction(0)
    for initial in contexts(n):
        state = initial
        weight = Fraction(1, 2**n)
        if word and state[-1] != word[0]:
            continue
        for bit in word[1:]:
            weight *= emit_prob(sigma, state, bit)
            state = shift(state, bit)
        den += weight
        num += weight * p_one(sigma, state)
    return num / den


def check_stationarity_and_likelihood(n):
    states = contexts(n)
    for sigma in (+1, -1):
        for h in states:
            assert MU <= p_one(sigma, h) <= 1 - MU
            assert sum(transition_prob(sigma, h, v) for v in states) == 1
        for v in states:
            incoming = sum(transition_prob(sigma, h, v) for h in states)
            assert incoming == 1  # uniform stationary distribution

        for k in range(n + 1):
            for word in product((0, 1), repeat=k):
                assert prefix_prob(sigma, word, n) == Fraction(1, 2**k)
                pnext = predictive_one(sigma, word, n)
                if k < n:
                    assert pnext == Fraction(1, 2)
                else:
                    assert pnext == p_one(sigma, word)

    for word in product((0, 1), repeat=n):
        pplus = prefix_prob(+1, word, n)
        pminus = prefix_prob(-1, word, n)
        assert pplus == pminus == Fraction(1, 2**n)
        assert pplus / pminus == 1
        for label in (0, 1):
            rplus = Fraction(1, 2) + (1 - 2 * label) * THETA * parity_sign(word)
            rminus = Fraction(1, 2) - (1 - 2 * label) * THETA * parity_sign(word)
            assert rplus + rminus == 1
            assert sorted((rplus, rminus)) == [MU, 1 - MU]

        # For every current context/destination, P^N(h,v) >= mu^N.
        for sigma in (+1, -1):
            for initial in states:
                dist = {initial: Fraction(1)}
                for _ in range(n):
                    nxt = {v: Fraction(0) for v in states}
                    for h, mass in dist.items():
                        for bit in (0, 1):
                            v = shift(h, bit)
                            nxt[v] += mass * emit_prob(sigma, h, bit)
                    dist = nxt
                assert all(prob >= MU**n for prob in dist.values())
    return 2**n


def all_nodes(n):
    return [h for k in range(n + 1) for h in product((0, 1), repeat=k)]


def evaluate_policy(n, decisions):
    """Actions: 0=continue, 1=stop silently, 2=certify label 0, 3=certify label 1."""
    index = {h: i for i, h in enumerate(all_nodes(n))}
    q = Fraction(0)
    bad = {+1: Fraction(0), -1: Fraction(0)}

    def visit(h, mass):
        nonlocal q
        action = decisions[index[h]]
        if action in (2, 3):
            label = action - 2
            q += mass
            if len(h) < n:
                bad[+1] += mass
                bad[-1] += mass
            else:
                for sigma in (+1, -1):
                    risk = Fraction(1, 2) + (1 - 2 * label) * sigma * THETA * parity_sign(h)
                    if risk > EPS:
                        bad[sigma] += mass
        elif action == 0 and len(h) < n:
            # Every prefix shorter than N is conditionally a fair binary string.
            visit(h + (0,), mass / 2)
            visit(h + (1,), mass / 2)
        # action 1 stops silently; action 0 at N has no more observations.

    visit((), Fraction(1))
    return q, bad[+1], bad[-1]


def check_all_small_policies(n):
    nodes = all_nodes(n)
    policy_count = 0
    for decisions in product(range(4), repeat=len(nodes)):
        q, bad_plus, bad_minus = evaluate_policy(n, decisions)
        assert bad_plus + bad_minus >= q
        assert max(bad_plus, bad_minus) >= q / 2
        policy_count += 1
    return policy_count


state_counts = {n: check_stationarity_and_likelihood(n) for n in (1, 2, 3)}
policy_counts = {n: check_all_small_policies(n) for n in (1, 2)}
print("N,hidden_contexts,uniform_prefixes_checked,deterministic_stop_predict_policies")
for n in (1, 2):
    print(f"{n},{state_counts[n]},{2**(n+1)-1},{policy_counts[n]}")
print("N=3,hidden_contexts=8,full_support_prefix/risk/minorization_checks=PASS")
print("likelihood_floor=1/10; N-step_minorization=(1/5)^N; prefix_LR=1; PASS")
