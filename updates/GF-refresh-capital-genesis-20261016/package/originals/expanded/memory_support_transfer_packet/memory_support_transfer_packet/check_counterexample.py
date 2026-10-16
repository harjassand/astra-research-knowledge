"""Exact full-input check of the history-event / endpoint-event distinction.
Requires only the already-installed SymPy package. No external data or code.
"""
import json
from pathlib import Path
import sympy as s

I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
P = [s.diag(1, 0), s.diag(0, 1)]
U = s.sqrt(3) * I / 2 - s.I * X / 2
# T = (Id + D_Z)/2, represented by its actual latent skip/pinch instrument.
node = [('skip', None, I/s.sqrt(2))]
node += [('pinch', m, P[m]/s.sqrt(2)) for m in range(2)]
normalization = s.zeros(2)
history_effect = s.zeros(2)
endpoint_effect = s.zeros(2)
records = []
for r in range(2):
    for kind, middle, L in node:
        for t in range(2):
            A = P[t] * U * L * U * P[r]
            E = s.simplify(A.conjugate().T * A)
            normalization += E
            endpoint_bad = t != r
            history_bad = endpoint_bad if kind == 'skip' else (middle != r or t != middle)
            if history_bad:
                history_effect += E
            if endpoint_bad:
                endpoint_effect += E
            records.append({'entering': r, 'node': kind, 'middle': middle, 'final': t,
                            'history_bad': history_bad, 'endpoint_bad': endpoint_bad,
                            'conditional_probability': str(s.simplify(E[r,r]))})
normalization = s.simplify(normalization)
history_effect = s.simplify(history_effect)
endpoint_effect = s.simplify(endpoint_effect)
assert normalization == I
assert history_effect == s.Rational(19,32)*I
assert endpoint_effect == s.Rational(18,32)*I
p = q = s.Rational(1,4)
eta = s.Rational(1,2)
Q = p+q-p*q
# For this case the binary maximizer is capped at c=1.
F = s.simplify(Q-p*q+2*eta*s.sqrt(p*q*(1-p)*(1-q)))
assert F == s.Rational(18,32)
assert history_effect-F*I == I/32
result = {'normalization': str(normalization), 'history_effect': str(history_effect),
          'endpoint_effect': str(endpoint_effect), 'new_F1': str(F),
          'history_minus_F1_effect': str(s.simplify(history_effect-F*I)),
          'assertions_passed': True, 'records': records,
          'logical_spectator': 'Tensoring an untouched logical system preserves every effect identity.'}
Path(__file__).with_name('counterexample_results.json').write_text(json.dumps(result, indent=2)+'\n')
print('PASS: old history effect = (19/32)I; endpoint effect = F_1 I = (18/32)I.')
