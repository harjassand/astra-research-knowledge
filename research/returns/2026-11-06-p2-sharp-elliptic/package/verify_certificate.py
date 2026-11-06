#!/usr/bin/env python3
"""Verify the delivered Fourier answer without rerunning the solver iteration.

This checks a finite residual certificate. Its analytic interpretation is the
theorem in RESEARCH_REPORT.txt, not an empirical test of that theorem.
"""
import json
from fractions import Fraction as F
from pathlib import Path
from exact_fourier import C, ZERO, N, ZMODE, P, H, add, scale, matvec, matmat
from exact_fourier import l1_bound, real_field, divergence_zero, curl_zero


def decode(rows, width):
    result = {}
    for row in rows:
        mode = tuple(row["mode"])
        assert len(mode) == N and all(type(x) is int for x in mode)
        assert mode not in result
        values = tuple(C(F(z[0]), F(z[1])) for z in row["coefficients"])
        assert len(values) == width
        result[mode] = values
    return result


def main():
    root = Path(__file__).resolve().parent
    data = json.loads((root/"FOURIER_SOLUTION.json").read_text())
    supplied = json.loads((root/"INPUT.json").read_text())
    assert data["dimension"] == supplied["dimension"] == 2
    assert data["p"] == supplied["p"] == "4"
    for key in ("M", "h", "k", "requested_gradient_L4_error"):
        assert data[key] == supplied[key]
    M = decode(data["M"], N*N)
    h = decode(data["h"], N)
    A = decode(data["A"], N*N)
    forcing = decode(data["forcing"], N)
    f = decode(data["f"], N)
    e = decode(data["gradient"], N)
    j = decode(data["divergence_free_flux"], N)
    k = F(data["k"])
    eps = F(data["requested_gradient_L4_error"])
    cp = F(3)
    assert 0 <= k < 1/cp
    identity = {ZMODE: (C(F(1)), ZERO, ZERO, C(F(1)))}
    for mat in M.values():
        for i in range(N):
            for ell in range(N):
                assert mat[i*N+ell] == mat[ell*N+i]
    for field in (M, A, h, forcing, f, e, j):
        real_field(field)
    assert matmat(M, M) == scale(identity, k*k)
    assert matmat(A, add(identity, M)) == add(identity, M, F(-1))
    assert matvec(add(identity, M), forcing) == h
    assert add(e, j) == f
    assert P(f) == e
    assert ZMODE not in e
    curl_zero(e)
    divergence_zero(j)
    r = add(add(H(f), matvec(M, f), F(-1)), h, F(-1))
    assert r == decode(data["reflection_residual"], N)
    rphys = add(add(matvec(A, e), j, F(-1)), forcing, F(-1))
    assert rphys == decode(data["physical_residual"], N)
    assert matvec(add(identity, M), rphys) == r
    error = ((1+cp)/2)*cp/(1-k*cp)*l1_bound(r)
    assert error <= eps
    result = {"certificate_verified": True,
              "iteration_history_required": False,
              "exact_gradient_L4_error_bound": str(error),
              "target": str(eps),
              "analytic_dependency": "Sharp real Hodge-reflection theorem, proved in the accompanying report"}
    (root/"CERTIFICATE_VERIFICATION.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
