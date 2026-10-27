"""Exact tree counts and full-law Gaussian-event obstruction calculations.

All source functions in the proof are legal C^{1,1}-potential gradients.
No source evaluations or fitted coefficient acquisition are hidden here;
this is an analytic obstruction check, not a general sampler.
"""
from fractions import Fraction
from math import log, sqrt, exp, pi, erf
from pathlib import Path
import csv
ROOT = Path(__file__).resolve().parent

def tree_count(K):
    # t=1/(200K) obeys the strict S1 condition for K>=2.
    t=Fraction(1,200*K)
    assert 10*t*(4*K+1) < Fraction(1,4)
    # First edge reduces gap by t; second by 1/4-10t.
    long_step=50*K-10
    root_gap=(K-1)*200*K
    counts=[1]
    for j in range(1,root_gap+1):
        a=counts[j-1]
        b=counts[j-long_step] if j>=long_step else 1
        counts.append(a+b)
    lower=2**(4*(K-1))
    assert counts[-1]>=lower
    return {
        "K": K, "t_numerator": t.numerator, "t_denominator": t.denominator,
        "exact_two_child_leaves": str(counts[-1]),
        "proved_lower_bound": str(lower),
        "log_exact_leaves": str(log(counts[-1])),
        "log_lower_bound": str(log(lower)),
    }

rows=[tree_count(k) for k in (2,3,4,8,12,16,24,32)]
with (ROOT/'two_child_tree_counts.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)

phi=lambda x: exp(-x*x/2)/sqrt(2*pi)
Phi=lambda x: (1+erf(x/sqrt(2)))/2
c0=phi(9/16)-phi(23/16)
assert c0>0
epsilon_lower=(2*Phi(2)-1-1/4)/2
assert epsilon_lower>.352

out=[]
out.append('REUSE REPRESENTATION OBSTRUCTION CHECKS')
out.append('Exact-integer tree recurrence checked for K=2,3,4,8,12,16,24,32.')
for row in rows:
    out.append(f"K={row['K']}: log leaves={float(row['log_exact_leaves']):.12g}, log proved lower={float(row['log_lower_bound']):.12g}")
out.append(f'c0=phi(9/16)-phi(23/16)={c0:.17g}')
out.append(f'Innovation threshold constant c0/(1024sqrt2)={c0/(1024*sqrt(2)):.17g}')
out.append(f'TV error lower bound at this threshold={epsilon_lower:.17g}')
out.append('The result uses a single explicit separating event of the complete joint law.')
out.append('No conclusion about the original single-output N687 minimax query complexity follows.')

for D in [100,1000,10000,1000000]:
    # Continuous lower-envelope comparison; integer tuning is no better.
    x=2*sqrt(log(2)*D)
    K=2+D/x
    bound=x+4*(K-1)*log(2)
    direct=4*sqrt(log(2)*D)+4*log(2)
    assert abs(bound-direct)<1e-9*max(1,direct)
    out.append(f'D={D}: lower bound log Q={direct:.12g}; minimizing continuous log M={x:.12g}, K={K:.12g}')

text='\n'.join(out)+'\n'
(ROOT/'CHECK_RESULTS.txt').write_text(text)
print(text,end='')
