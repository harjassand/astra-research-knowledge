"""Exact finite checks of the cyclic-Slater local-mixing obstruction.

This verifies identities for small instances; the general proof is in the report.
It is not execution of the Chen--Liu FPRAS or a quantum preparation compiler.
"""
from pathlib import Path
from fractions import Fraction
import itertools
import json


def determinant_of_unit_rows(columns):
    if len(set(columns)) < len(columns):
        return 0
    inversions = sum(columns[i] > columns[j]
                     for i in range(len(columns)) for j in range(i + 1, len(columns)))
    return (-1) ** inversions


results = []
for n in range(2, 9):
    row_columns = [column for i in range(n) for column in (i, (i - 1) % n)]
    norm = sum(determinant_of_unit_rows([row_columns[i] for i in selected]) ** 2
               for selected in itertools.combinations(range(2 * n), n))
    support = []
    for bits in itertools.product((0, 1), repeat=n):
        amplitude = determinant_of_unit_rows([row_columns[2 * i + bits[i]] for i in range(n)])
        if amplitude:
            support.append({'bits': bits, 'amp': amplitude})
    assert norm == 2 ** n and len(support) == 2
    assert support[0]['bits'] == (0,) * n and support[1]['bits'] == (1,) * n
    assert support[0]['amp'] == 1 and support[1]['amp'] == (-1) ** (n - 1)
    g = Fraction(1, 2 ** n)
    soft_z = Fraction(0)
    for bits in itertools.product((0, 1), repeat=n):
        walls = sum(bits[i] != bits[(i + 1) % n] for i in range(n))
        double = sum(bits[(i - 1) % n] == 1 and bits[i] == 0 for i in range(n))
        assert 2 * double == walls
        soft_z += g ** walls
    assert soft_z == (1 + g) ** n + (1 - g) ** n
    probability_up = 1 / soft_z
    exit_rate = g * g / n
    spectral_upper = exit_rate / (1 - probability_up)
    results.append({'n': n, 'norm': norm, 'hard_Z': 2, 'hard_W': str(Fraction(2, norm)),
                    'support': support, 'g': str(g), 'soft_Z': str(soft_z),
                    'up_exit_Metropolis': str(exit_rate), 'gap_upper': str(spectral_upper)})

destination = Path(__file__).with_name('gutzwiller_mixing_fixture.json')
destination.write_text(json.dumps({'description': 'Cyclic Slater hard-support and soft-Metropolis fixtures',
                                   'results': results}, indent=2) + '\n')
print('Verified n=2,...,8; hard support has two states; soft partition identity is exact.')
print(destination)
