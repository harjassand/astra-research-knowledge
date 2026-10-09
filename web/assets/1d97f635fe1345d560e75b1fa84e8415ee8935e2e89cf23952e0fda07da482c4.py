"""Finite clock construction: floating diagnostics, not proof certification."""
import math
import json
from pathlib import Path
import numpy as np

M = 100
mix = 14 / 25
switch_rate = 1e-5

def poisson_terms(mean, last):
    terms = [math.exp(-mean)]
    for k in range(last):
        terms.append(terms[-1] * mean / (k + 1))
    return terms

forward = poisson_terms(M + 1, 300)
backward = poisson_terms(1, 30)
probs = np.zeros(5)
for a, pa in enumerate(forward):
    for b, pb in enumerate(backward):
        q, rem = divmod(a-b, M)
        probs[q % 5] += pa * pb * (1-rem/M)
        probs[(q+1) % 5] += pa * pb * (rem/M)
sym = (probs + probs[(-np.arange(5)) % 5]) / 2
row = mix * sym
row[0] += 1-mix
P = np.array([[row[(j-i) % 5]/5 for j in range(5)] for i in range(5)])
W = np.ones((5,5))
for i in range(5):
    W[i,(i+1)%5] = W[i,(i-1)%5] = -1

# Chernoff bound for upper Poisson tail P[N >= K], K > mean.
def poisson_tail_bound(mean, K):
    return math.exp(-mean + K * (1 + math.log(mean/K)))
tail = poisson_tail_bound(M+1,301) + poisson_tail_bound(1,31)
switch_tv = switch_rate * max(1,mix/(1-mix))
eigenvalues = np.linalg.eigvalsh(P)
witness = float(np.sum(W*P))
out = {
  'scope':'Floating diagnostic plus analytic Poisson-tail and added-switch coupling formulas; no exact-arithmetic certificate',
  'hidden_states': 2*5*M+5,
  'M':M, 'active_mixture':mix, 'switch_rate':switch_rate,
  'lag':1, 'observed_pair_table':P.tolist(),
  'eigenvalues':eigenvalues.tolist(),
  'horn_pairing':witness,
  'poisson_omitted_mass_upper':tail,
  'switch_total_variation_upper':switch_tv,
  'psd_margin_after_analytic_perturbation':float(eigenvalues[0]-2*(tail+switch_tv)),
  'horn_pairing_upper_after_analytic_perturbation':witness+2*(tail+switch_tv),
  'copositive_linear_ep_lower':4*max(0,-witness-2*(tail+switch_tv)),
  'actual_ep':mix*M*math.log(M+1),
}
Path('work/root/horn_clock_check_v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
