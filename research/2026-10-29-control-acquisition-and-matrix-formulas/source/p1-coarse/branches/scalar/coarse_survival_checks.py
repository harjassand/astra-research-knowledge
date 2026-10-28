"""Exact small witnesses for coarse survival forms and switched decay.

No stochastic data or calls to the root acquisition implementation.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import hashlib

I = ((F(1), F(0)), (F(0), F(1)))
ONE = (F(1), F(1))
E1 = (F(1), F(0))


def mm(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def mv(a, x):
    return tuple(sum(a[i][j]*x[j] for j in range(2)) for i in range(2))


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def sub(a, b):
    return tuple(tuple(a[i][j]-b[i][j] for j in range(2)) for i in range(2))


def inv(a):
    determinant = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    assert determinant
    return ((a[1][1]/determinant, -a[0][1]/determinant),
            (-a[1][0]/determinant, a[0][0]/determinant))


def power(a, n):
    out = I
    for _ in range(n):
        out = mm(a, out)
    return out


def f(a, n, vector=ONE, norm=F(2)):
    return dot(vector, mv(power(a, n), vector))/norm


def encoded(value):
    if isinstance(value, F):
        return {'fraction': str(value), 'diagnostic': float(value)}
    if isinstance(value, dict):
        return {key: encoded(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encoded(item) for item in value]
    return value


def main():
    # Entrywise positive but with a negative eigenvalue: det(A)=-1/36.
    a = ((F(1, 2), F(1, 3)), (F(1, 3), F(1, 6)))
    determinant = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    assert determinant == -F(1, 36)
    h = tuple(ONE[j]-mv(a, ONE)[j] for j in range(2))
    assert min(h) >= 0
    inverse_dissipation = inv(sub(I, mm(a, a)))
    killing = []
    for k in (0, 1, 2, 4):
        akh = mv(power(a, k), h)
        tail = dot(akh, mv(inverse_dissipation, akh))/2
        event = f(a, 2*k)-f(a, 2*k+1)
        assert 0 <= tail <= event
        killing.append(dict(k=k, exact_tail=tail, positive_event_bound=event))

    # Selfadjointness alone, without the common order vector, fails.
    a0 = ((F(1, 2), F(1, 4)), (F(1, 4), F(1, 2)))
    a1 = ((F(1, 2), F(0)), (F(0), F(1)))
    horizon = 32
    mixed = dot(E1, mv(mm(mm(a0, power(a1, horizon)), a0), E1))
    assert mixed == F(1, 16)+F(1, 4)*F(1, 2)**horizon
    assert mv(a0, E1)[1] > E1[1]
    assert f(a0, horizon, E1, F(1)) == (F(3, 4)**horizon+F(1, 4)**horizon)/2
    assert f(a1, horizon, E1, F(1)) == F(1, 2)**horizon

    # The common order vector alone, without selfadjointness, fails.
    shift = ((F(0), F(1)), (F(0), F(0)))
    reverse_shift = ((F(0), F(0)), (F(1), F(0)))
    assert power(shift, 2) == ((F(0), F(0)), (F(0), F(0)))
    assert power(reverse_shift, 2) == power(shift, 2)
    cycle = mm(shift, reverse_shift)
    assert f(cycle, 5) == F(1, 2)

    # A noncommuting pair satisfying both structural hypotheses.
    c0 = ((F(1, 2), F(1, 4)), (F(1, 4), F(1, 4)))
    c1 = ((F(1, 4), F(1, 4)), (F(1, 4), F(1, 2)))
    assert mm(c0, c1) != mm(c1, c0)
    actions = (c0, c1)
    m = 3
    s = max(f(c0, 2*m), f(c1, 2*m))
    def z(length):
        return s+(1-F(1, m))**length*(1-s)
    checked_words = []
    for word in ('', '0', '1', '01', '10', '0011', '010101', '00101101'):
        state = ONE
        for symbol in word:
            state = mv(actions[int(symbol)], state)
        assert all(0 <= x <= 1 for x in state)
        norm2 = dot(state, state)/2
        response = sum(state)/2
        left = len(word)//2
        right = len(word)-left
        assert norm2 <= z(len(word))
        assert response**2 <= z(left)*z(right)
        checked_words.append(dict(word=word, response=response,
            exact_norm_square=norm2, norm_bound=z(len(word)),
            split_scalar_bound_squared=z(left)*z(right)))

    # The whole response changes by <=epsilon while the centered form grows.
    epsilon = F(1, 10000)
    base = F(1, 2)
    slow = 1-epsilon**2
    exact_model = (1-epsilon)*base+epsilon*slow
    q_model = ((1-epsilon)*(base-exact_model)**2/(1-base**2)
               +epsilon*(slow-exact_model)**2/(1-slow**2))
    assert q_model > 1000
    q_killing = ((1-epsilon)*(1-base)/(1+base)
                 +epsilon*(1-slow)/(1+slow))
    assert q_killing <= 1-exact_model

    # Root's new block family: exact all-scale constants, not sampled data.
    block0 = ((F(10, 16), F(2, 16)), (F(2, 16), F(2, 16)))
    block1 = ((F(8, 16), F(1, 16)), (F(1, 16), F(2, 16)))
    means = [dot(ONE, mv(inv(sub(I, block)), ONE))/2
             for block in (block0, block1)]
    assert means == [F(12, 5), F(64, 37)]
    constant_ratio = F(1, 128)
    for n in (0, 1, 3, 8):
        pn = F(1, 2**(n+1)*1024)
        en = F(1, 2**(n+4))
        assert pn/en == constant_ratio
    contributions = [constant_ratio*mean for mean in means]
    assert contributions == [F(3, 160), F(1, 74)]
    slow_weighted_e = F(1, 24576)
    fast_weight = F(1023, 1024)
    models = [1-(1-f(block, 1))*(fast_weight+slow_weighted_e)
              for block in (block0, block1)]
    assert models == [F(24599, 49152), F(73843, 196608)]

    report = dict(
        passed=True,
        scope='Exact algebra only. No stochastic trials, source equipment, or root acquisition replay.',
        killing_vector_negative_spectrum_fixture=dict(
            matrix=a, determinant=determinant, checks=killing),
        missing_common_order_counterexample=dict(
            pure0_at_32=f(a0, horizon, E1, F(1)),
            pure1_at_32=f(a1, horizon, E1, F(1)),
            switched_response=mixed, limiting_response=F(1, 16)),
        missing_selfadjointness_counterexample=dict(
            pure_two_step_survival=F(0), alternating_survival=F(1, 2)),
        valid_noncommuting_pair=dict(m=m, s=s, words=checked_words),
        rare_slow_sector=dict(preparation_mass=epsilon, slow_survival=slow,
            exact_rank_one_model=exact_model, centered_inverse_form=q_model,
            killing_inverse_form=q_killing,
            all_word_response_distance_upper=epsilon),
        countable_block_family=dict(
            base_block_mean_lifetimes=means, weight_over_slowing=constant_ratio,
            mean_lifetime_contribution_per_slow_block=contributions,
            exact_rank_one_models=models,
            conclusion='Infinite sums and every-stable-finite-word-model obstruction are proved in the companion note; finite checks do not substitute for those proofs.'),
    )
    here = Path(__file__).resolve().parent
    report['proof_sha256'] = hashlib.sha256(
        (here/'COARSE_SURVIVAL_FORMS_AND_SWITCHING.md').read_bytes()).hexdigest()
    output = here/'COARSE_SURVIVAL_CHECKS.json'
    output.write_text(json.dumps(encoded(report), indent=2)+'\n')
    print(json.dumps(dict(passed=True, output=str(output),
        killing_tail_checks=len(killing), switched_words_checked=len(checked_words),
        rare_centered_form=float(q_model))))


if __name__ == '__main__':
    main()
