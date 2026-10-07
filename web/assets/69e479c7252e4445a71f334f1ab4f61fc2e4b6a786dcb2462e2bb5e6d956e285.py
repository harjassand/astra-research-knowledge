from bandwidth_parity import *
from low_rank_parity import enumerate_count, determinant, factorize
from pathlib import Path
import random, time, json

start = time.perf_counter()
rng = random.Random(620201)
cases = []
sample_checks = 0
conditional_checks = 0
for n, b in [(4, 1), (5, 2), (6, 2), (7, 1)]:
    F = [[G(Q(rng.randrange(-2, 3), 2), Q(rng.randrange(-1, 2), 3))
          if i != j and abs(i-j) <= b else G(int(i == j)*17)
          for j in range(n)] for i in range(n)]
    rw = [Q(rng.randrange(0, 4), 3) for _ in range(n)]
    cw = [Q(rng.randrange(1, 4), 2) for _ in range(n)]
    expected, law = enumerate_count(F, row_weights=rw, col_weights=cw)
    actual, meta = count_band(F, row_weights=rw, col_weights=cw)
    assert actual == expected
    for k in range(n//2+1):
        capped, _ = count_band(F, row_weights=rw, col_weights=cw, max_pairs=k)
        assert capped == expected[:k+1]
        if expected[k]:
            word = sample_band(F, k, row_weights=rw, col_weights=cw, randbits=rng.getrandbits)
            assert word in law and word.count('R') == word.count('C') == k
            sample_checks += 1
    for i in range(n):
        for t in 'ERC':
            tables = [set('ERC') for _ in range(n)]
            tables[i] = {t}
            expected_conditioned, _ = enumerate_count(F, tables, rw, cw)
            actual_conditioned, _ = count_band(F, tables, rw, cw)
            assert actual_conditioned == expected_conditioned
            conditional_checks += 1
    tables = [set('ERC') for _ in range(n)]
    tables[0] = {'R'}
    tables[-1] = {'E', 'C'}
    expected_conditioned, conditional_law = enumerate_count(F, tables, rw, cw)
    if sum(expected_conditioned):
        word = sample_band(F, allowed=tables, row_weights=rw, col_weights=cw, randbits=rng.getrandbits)
        assert word in conditional_law
        sample_checks += 1
    # Large arbitrary diagonal entries are irrelevant and are acquired away.
    Fzero = [[G() if i == j else F[i][j] for j in range(n)] for i in range(n)]
    assert count_band(Fzero, row_weights=rw, col_weights=cw)[0] == actual
    cases.append({'n': n, 'bandwidth_requested': b, 'acquired': meta,
                  'coefficients': list(map(str, actual))})

# An extensive sector on an acquired full-rank, non-monomial, phase-interfering
# band-two matrix. The transfer computes the sector directly, not by rare-event
# rejection; independent enumeration of all 3^12 words is intentionally omitted.
n = 12
F = [[G((i+2*j) % 5 - 2, (2*i+j) % 3 - 1)
      if 0 < abs(i-j) <= 2 else G() for j in range(n)] for i in range(n)]
for i in range(n-1):
    F[i][i+1] += G(3)  # Every alternating-word diagonal entry is now nonzero.
coefficients, meta = count_band(F)
U, V = factorize(F)
rank = len(U[0])
I = list(range(0, n, 2)); J = list(range(1, n, 2))
witness = determinant([[F[i][j] for j in J] for i in I]).norm()
assert witness > 0 and coefficients[6] >= witness and rank == 12
word = sample_band(F, 6, randbits=rng.getrandbits)
Is = [i for i, t in enumerate(word) if t == 'R']
Js = [i for i, t in enumerate(word) if t == 'C']
assert len(Is) == len(Js) == 6
assert determinant([[F[i][j] for j in Js] for i in Is]).norm() > 0
extensive = {'n': n, 'rank_acquired': rank, 'meta': meta,
             'coefficients': list(map(str, coefficients)),
             'alternating_word_weight': str(witness), 'sample_k6': word}

boundaries = {}
assert count_band([])[0] == [Q(1)]
assert sample_band([], 0) == ''
assert count_band([[1, 0], [0, 1]], allowed=[{'R'}, set('ERC')])[0] == [Q(0), Q(0)]
for name, action in [
    ('negative_sector', lambda: sample_band([[0]], -1)),
    ('large_sector', lambda: sample_band([[0]], 1)),
    ('negative_activity', lambda: count_band([[0]], row_weights=[-1])),
    ('nonsquare', lambda: count_band([[0, 1]])),
    ('bad_table', lambda: count_band([[0]], allowed=[{'B'}])),
    ('zero_sector', lambda: sample_band([[0]], allowed=[{'R'}])),
]:
    try:
        action()
        raise AssertionError(name+' was accepted')
    except ValueError:
        boundaries[name] = 'REJECTED'
result = {'status': 'PASS', 'seed': 620201, 'cases': cases,
          'conditional_coefficient_checks': conditional_checks,
          'sample_support_checks': sample_checks,
          'full_rank_extensive_sector': extensive, 'boundaries': boundaries,
          'scope': 'small exact counts compared with independent disjoint-word permutation-determinant enumeration; full-rank n12 fixture has exact transfer identities and independent support witnesses only; probability law is proved by transfer/self-reduction, not frequencies',
          'elapsed_seconds': time.perf_counter()-start}
Path('work/cycle6/c02_s01/bandwidth_parity_checks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status': result['status'], 'conditional_coefficient_checks': conditional_checks,
                  'sample_support_checks': sample_checks, 'full_rank_k6_coefficient': str(coefficients[6]),
                  'elapsed_seconds': result['elapsed_seconds']}, indent=2))
