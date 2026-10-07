"""Diagnostics for the smooth-Dicke reliability construction.

These computations are finite checks of independently proved formulas;
they are not correctness or novelty certification.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

P = (23 + 6 * math.sqrt(13)) / 61
S = math.sqrt(P * (1 - P))
H = 1 - S
ELL = 1 + 3 * P
ALPHA = (10 + 2 * math.sqrt(13)) / 3


def state(n: int, m: int) -> tuple[int, list[float]]:
    j0 = math.floor(n * P + 0.5)
    if j0 - m < 0 or j0 + m > n:
        raise ValueError("window outside count range")
    a = j0 - m
    norm = math.sqrt(m + 1)
    coefficients = [math.sin(math.pi * (r + 1) / (2 * m + 2)) / norm
                    for r in range(2 * m + 1)]
    return a, coefficients


def evaluate(n: int, m: int) -> dict:
    a, coeffs = state(n, m)
    logs = [2 * math.log(c) - n - 3 * (a + i)
            for i, c in enumerate(coeffs)]
    top = max(logs)
    log_miss = top + math.log(sum(math.exp(x - top) for x in logs))
    neighbor = sum(coeffs[i] * coeffs[i + 1]
                   for i in range(len(coeffs) - 1))
    q = n - sum(coeffs[i] * coeffs[i + 1]
                * math.sqrt((n - a - i) * (a + i + 1))
                for i in range(len(coeffs) - 1))
    ub_q_per_cell = H + S * math.pi**2 / (8 * (m + 1)**2) + 3.5 * m*m / (n*n)
    lb_rate = (ELL - 3 * (m + 0.5) / n) / ub_q_per_cell
    norm_error = abs(sum(c * c for c in coeffs) - 1)
    path_error = abs(neighbor - math.cos(math.pi / (2 * m + 2)))
    assert norm_error < 2e-14
    assert path_error < 2e-14
    if n >= 64:
        assert q / n <= ub_q_per_cell + 2e-14
    assert -log_miss >= n * ELL - 3 * (m + 0.5) - 1e-11
    return dict(n=n, m=m, a=a, b=a+2*m, q=q, log_miss=log_miss,
                rate=-log_miss/q, deficit=ALPHA+log_miss/q,
                rate_lower_bound=lb_rate,
                scaled_deficit=(ALPHA+log_miss/q)*n**(2/3),
                norm_error=norm_error, path_identity_error=path_error)


def check_sequential_preparation(n: int, j: int) -> tuple[float, float]:
    # Coherent implementation keeps a remaining-excitation counter k.
    # Here all amplitudes are expanded, only for small n.
    amps = {(j, 0): 1.0}
    for position in range(n):
        remaining = n - position
        new = {}
        for (k, bits), amp in amps.items():
            if k < remaining:
                new[(k, bits)] = amp * math.sqrt((remaining-k)/remaining)
            if k > 0:
                new[(k-1, bits | (1 << position))] = amp * math.sqrt(k/remaining)
        amps = new
    target = 1 / math.sqrt(math.comb(n, j))
    max_err = 0.0
    support_failures = 0
    for (k, bits), amp in amps.items():
        support_failures += int(k != 0 or bits.bit_count() != j)
        max_err = max(max_err, abs(amp-target))
    assert len(amps) == math.comb(n, j)
    assert support_failures == 0
    assert max_err < 2e-14
    return max_err, support_failures


def check_full_vector(n: int, m: int) -> dict:
    a, coeffs = state(n, m)
    vector = [0.0] * (1 << n)
    for bits in range(1 << n):
        j = bits.bit_count()
        if a <= j <= a+2*m:
            vector[bits] = (-1 if j % 2 else 1) * coeffs[j-a] / math.sqrt(math.comb(n,j))
    q = n * sum(v*v for v in vector)
    for bits, v in enumerate(vector):
        for pos in range(n):
            q += 0.5 * v * vector[bits ^ (1 << pos)]
    miss = sum(v*v * math.exp(-n - 3 * bits.bit_count())
               for bits,v in enumerate(vector))
    formula = evaluate(n,m)
    assert abs(q-formula['q']) < 2e-12
    assert abs(math.log(miss)-formula['log_miss']) < 2e-12
    return dict(n=n,m=m,cost_error=abs(q-formula['q']),
                log_miss_error=abs(math.log(miss)-formula['log_miss']))


def separable_beta(overhead: float) -> float:
    # Diagnostic one-variable maximum. Analytic converse does not use it.
    def ratio(p: float) -> float:
        miss = (1-p)*math.exp(-1)+p*math.exp(-4)
        cost = 1+overhead-math.sqrt(p*(1-p))
        return -math.log(miss)/cost
    left, right = 0.0, 1.0
    for _ in range(140):
        c = left + (right-left)/3
        d = right - (right-left)/3
        if ratio(c)<ratio(d): left=c
        else: right=d
    return max(ratio(0),ratio(1),ratio((left+right)/2))


def main() -> None:
    values = []
    for n in [64,128,256,512,1024,4096,16384,65536,262144,1048576]:
        m = math.floor(n**(1/3)+1e-10)
        values.append(evaluate(n,m))
    fixtures=[]
    for n in range(4,11):
        max_m=min(math.floor(n*P+0.5),n-math.floor(n*P+0.5))
        for m in range(1,max_m+1):fixtures.append(check_full_vector(n,m))
    seq=[]
    for n in range(1,11):
        for j in range(n+1):
            err,fail=check_sequential_preparation(n,j)
            seq.append(dict(n=n,j=j,max_amplitude_error=err,support_failures=fail))
    overhead=[]
    for c in [0,0.1,0.5,1,2,10]:
        d=1+c
        alpha=(5*d+math.sqrt(9*d*d+4))/(2*(d*d-0.25))
        beta=separable_beta(c)
        overhead.append(dict(c=c,alpha=alpha,beta_numeric=beta,
                             gain_numeric=alpha/beta,
                             gain_converse=(1.5+c)/(0.5+c)))
    result=dict(status='Finite numerical diagnostics only; see report.md for proofs.',
                constants=dict(p=P,s=S,h=H,ell=ELL,alpha=ALPHA),
                finite_size=values,full_vector_fixtures=fixtures,
                sequential_preparation_fixtures=seq,overhead=overhead)
    out=Path(__file__).with_name('smooth_dicke_results.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(output=str(out),finite_size=values,
                          full_vector_fixtures=len(fixtures),
                          sequential_fixtures=len(seq),overhead=overhead),indent=2))


if __name__=='__main__':main()
