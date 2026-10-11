"""Independently reload and verify the stored rational all-future example.

Run from any directory:
    python check_saved_certificate.py
Only Python's standard library and the local energy_clock.py are required.
"""
from fractions import Fraction as Q
from pathlib import Path
import gzip
import json
import sys
from energy_clock import EnergyQP, Certificate, certificate_action

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)
root = Path(__file__).resolve().parent
with gzip.open(root/'hinge_certificate.json.gz','rt',encoding='utf-8') as fh:
    data = json.load(fh)
def mat(value): return [[Q(a) for a in row] for row in value]
model = EnergyQP(mat([[1,0,0],[0,0,0],[0,0,0]]),[Q(0),Q(0),Q(1)],
                 mat([[0,0,-1],[1,-1,-1]]),[Q(0),Q(0)],2)
c = Certificate([Q(t) for t in data['times']],mat(data['primal']),
                mat(data['dual_w']),mat(data['dual_lambda']))
J = certificate_action(model,c)
assert c.primal[0][:2] == [Q(1),Q(0)]
assert model.verify_minimizer(c.primal[-1],[Q(1),Q(0)])
assert 2*J <= Q(1,40000)
assert J == Q((root/'action_exact.txt').read_text().strip())
print('PASS: exact primal/dual constraints, exact terminal minimum, and 2J <= 1/40000.')
print('The action theorem therefore bounds state error by 1/200 at every future time.')
print('This checks one supplied certificate, not the general optimization algorithm or novelty.')
