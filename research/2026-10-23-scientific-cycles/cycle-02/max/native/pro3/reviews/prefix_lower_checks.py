"""Exact rational diagnostic of the NEW prefix/competition limit, not a proof.

Uses generic matrix multiplication/powering and independently evaluates the
closed form in prefix_lower.md. No original funnel suite is rerun.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import resource
import time


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def power(a, n):
    ans = [[F(i == j) for j in range(len(a))] for i in range(len(a))]
    while n:
        if n & 1:
            ans = matmul(ans, a)
        n >>= 1
        if n:
            a = matmul(a, a)
    return ans


def main():
    start, cpu_start = time.perf_counter(), time.process_time()
    cases, comparisons = 0, 0
    for b, alpha, rho in [(F(2, 5), F(2, 5), F(4, 5)),
                          (F(3, 4), F(7, 8), F(9, 10)),
                          (F(1, 100), F(1, 2), F(2, 3))]:
        beta = 1-alpha
        G = [[F(1), F(0), F(0)], [F(0), b, 1-b], [F(0), F(0), F(1)]]
        L = [[F(1), F(0), F(0)], [rho, F(0), 1-rho], [F(0), F(0), F(1)]]
        C = [[(F(i == j) + alpha*G[i][j] + beta*L[i][j])/2
              for j in range(3)] for i in range(3)]
        q = [[F(0), b, 1-b]]
        z, theta = (1+alpha*b)/2, beta*rho/(1-alpha*b)
        for m in [0, 1, 4, 16, 50]:
            mu = matmul(q, power(G, m))
            assert mu == [[F(0), b**(m+1), 1-b**(m+1)]]
            comparisons += 1
            for n in [0, 1, 2, 10, 100]:
                law = matmul(mu, power(C, n))[0]
                aa = b**(m+1)*theta*(1-z**n)
                bb = b**(m+1)*z**n
                assert law == [aa, bb, 1-aa-bb]
                tv = (abs(law[0])+abs(law[1])+abs(law[2]-1))/2
                assert tv == b**(m+1)*(theta+(1-theta)*z**n)
                assert tv >= b**(m+1)*theta
                cases += 1
                comparisons += 3
    receipt = {
        "status": "PASS", "arithmetic": "fractions.Fraction (exact rational)",
        "parameter_triples": 3, "prefix_lengths": [0, 1, 4, 16, 50],
        "postprefix_steps": [0, 1, 2, 10, 100], "cases": cases,
        "asserted_comparisons": comparisons,
        "wall_seconds": time.perf_counter()-start,
        "cpu_seconds": time.process_time()-cpu_start,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "limitations": "Exact finite diagnostics of limiting matrices; full proof is in prefix_lower.md."
    }
    out = Path(__file__).with_name("prefix_lower_checks.json")
    out.write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
