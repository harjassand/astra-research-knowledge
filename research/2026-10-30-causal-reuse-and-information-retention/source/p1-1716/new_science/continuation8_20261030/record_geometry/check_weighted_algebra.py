"""Exact finite-state checks for the new weighted quotient and trace algebra.

These are population identities, not acquired data, hydrodynamic tests, or an
independent proof of an asymptotic statement. Run from this file's directory.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


def swap(eta, i):
    x = list(eta)
    j = (i + 1) % len(x)
    x[i], x[j] = x[j], x[i]
    return tuple(x)


def activity(eta):
    n = len(eta)
    return tuple((eta[i] - eta[(i + 1) % n]) ** 2 for i in range(n))


def flux_q(eta, j):
    n = len(eta)
    x, y, z = [eta[(j + k) % n] for k in range(3)]
    return x + 2*y + z - 2*(x*y + x*z + y*z) + 4*x*y*z


def main():
    count = 0
    quotient_count = 0
    trace_count = 0
    max_q = 0
    assert all(0 <= flux_q(x, 0) <= 2 for x in product((0, 1), repeat=3))
    for n in (4, 6, 8):
        h = tuple(F((i*i + 3*i) % 11, 7) for i in range(n))
        hmax = max(map(abs, h))
        variation = sum(abs(h[(i+1) % n] - h[i]) for i in range(n))
        alpha = F(2, 3)
        c = F(3, 5)
        for eta in product((0, 1), repeat=n):
            a = activity(eta)
            total_a = sum(a)
            if total_a == 0:
                continue
            d = tuple(eta[i] - eta[(i+1) % n] for i in range(n))
            ah = sum(h[i]*a[i] for i in range(n))
            fh = ah / total_a
            da = 0
            dah = F(0)
            dfh = F(0)
            exfh = F(0)
            remainder = F(0)
            da_each = [0] * n
            for i in range(n):
                if not a[i]:
                    continue
                eta_i = swap(eta, i)
                ai = activity(eta_i)
                total_ai = sum(ai)
                ahi = sum(h[j]*ai[j] for j in range(n))
                fhi = ahi / total_ai
                da += d[i] * (total_ai-total_a)
                dah += d[i] * (ahi-ah)
                dfh += d[i] * (fhi-fh)
                exfh += fhi-fh
                remainder += d[i] * (total_ai-total_a) * (ahi-ah-fh*(total_ai-total_a)) / (total_a*total_ai)
                assert abs(total_ai-total_a) <= 2
                assert total_ai >= F(total_a, 2)
                assert abs(fhi-fh) <= 8*hmax/total_a
                for j in range(n):
                    da_each[j] += d[i]*(ai[j]-a[j])
            assert da == 0
            for j in range(n):
                assert da_each[j] == flux_q(eta, j-1)-flux_q(eta, j)
                max_q = max(max_q, flux_q(eta, j))
                count += 1
            assert dah == sum((h[(j+1) % n]-h[j])*flux_q(eta, j) for j in range(n))
            assert dfh == dah/total_a-remainder
            assert abs(dfh) <= (2*variation+16*hmax)/total_a
            assert abs(exfh) <= 8*hmax
            quotient_count += 1

            # Half-trace two-native path conductance is exactly unchanged
            # when its marked path is reversed. No wall-clock equivalence.
            for i in range(n):
                if not a[i]:
                    continue
                eta_i = swap(eta, i)
                ai = activity(eta_i)
                for j in range(n):
                    if not ai[j]:
                        continue
                    eta_ij = swap(eta_i, j)
                    dj = eta_i[j]-eta_i[(j+1) % n]
                    forward = c*(1+alpha*d[i])*(1-alpha*dj)/(2*sum(ai))
                    back_j = eta_ij[j]-eta_ij[(j+1) % n]
                    back_i = eta_i[i]-eta_i[(i+1) % n]
                    reverse = c*(1+alpha*back_j)*(1-alpha*back_i)/(2*sum(ai))
                    assert forward == reverse
                    assert h[i]*d[i]+h[j]*dj == -(h[j]*back_j+h[i]*back_i)
                    trace_count += 1

    source = Path(__file__)
    report = {
        "status": "all exact assertions passed",
        "sizes": [4, 6, 8],
        "local_divergence_identities": count,
        "nontrivial_configuration_quotient_checks": quotient_count,
        "marked_two_event_path_reversal_checks": trace_count,
        "maximum_local_flux_q": max_q,
        "code_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "scope": "finite population algebra only; no acquisition, asymptotic verification, or physical execution",
    }
    Path(__file__).with_name("WEIGHTED_ALGEBRA_CHECKS.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
