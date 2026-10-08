#!/usr/bin/env python3
"""Finite conventions and critical asymptotics. No theorem certification."""
from fractions import Fraction as F
from math import comb, exp, expm1, erfc, lgamma, log, sqrt
from pathlib import Path
import json


def z(q, length):
    return sum((q**k for k in range(length + 1)), F(0))


def schur_exact(n, r):
    a, b = (1 + r) / 2, (1 - r) / 2
    ans = {}
    for length in range(n % 2, n + 1, 2):
        k = (n - length) // 2
        multiplicity = comb(n, k) - (comb(n, k - 1) if k else 0)
        ans[length] = multiplicity * (a * b)**k * sum(
            (a**(length - s) * b**s for s in range(length + 1)), F(0)
        )
    assert sum(ans.values(), F(0)) == 1
    return ans


def g_exact(q, length):
    zz = z(q, length)
    t = F(length + 1) / zz
    purity_effect = z(q*q, length) / zz
    diagonal_bound = t * z(q, 2 * length) / (2 * length + 1)
    return t, purity_effect - diagonal_bound


def posterior_radius_exact(q, length):
    if length == 0:
        return F(0)
    j = F(length, 2)
    moment = sum(((j-k)*q**k for k in range(length+1)), F(0))/z(q,length)
    assert 0 <= moment <= j
    return moment/(j+1)


def schur_float(n, r):
    """Use the binomial form; n up to 65536 only, one light CPU process."""
    a, b = (1 + r) / 2, (1 - r) / 2
    beta = log(a / b)
    ans = {}
    for length in range(n % 2, n + 1, 2):
        k = (n - length) // 2
        lp = (lgamma(n+1) - lgamma(k+1) - lgamma(n-k+1)
              + (n-k)*log(a) + k*log(b))
        prefactor = 2*(length+1)/(n+length+2) * a/r
        ans[length] = prefactor * (-expm1(-beta*(length+1))) * exp(lp)
    mass = sum(ans.values())
    assert abs(mass-1) < 2e-9, (n, r, mass)
    return {length: p/mass for length, p in ans.items()}


def g_float(q, length):
    beta = -log(q)
    denominator = -expm1(-beta*(length+1))
    t = (length+1)*(1-q)/denominator
    purity_effect = (1+exp(-beta*(length+1)))/(1+q)
    diagonal_bound = ((length+1)/(2*length+1)
                      * (-expm1(-beta*(2*length+1)))/denominator)
    return t, purity_effect-diagonal_bound


def posterior_radius_float(q, length):
    if length == 0:
        return 0.0
    beta = -log(q)
    occupied = q/(1-q)-(length+1)*exp(-beta*(length+1))/(-expm1(-beta*(length+1)))
    return (length/2-occupied)/(length/2+1)


def normal_tail(x):
    return erfc(x/sqrt(2))/2


def critical_tail(c):
    return 3*exp(4*c*c)*normal_tail(3*c)-normal_tail(c)


def run():
    fixtures = 0
    max_bound_violation = 0.0
    rank_fixtures = 0
    proper_fixtures = 0
    mlr_fixtures = 0
    for n in range(1, 19):
        for r in (F(1, 8), F(1, 4), F(1, 2)):
            probs = schur_exact(n, r)
            q = (1-r)/(1+r)
            aa = sum((p*q**(length+1) for length,p in probs.items()), F(0))
            kap = n*float(r)**2
            lower = exp(-(8/3)*(kap+sqrt(3*kap)+float(r)))
            upper = min(1.0, 2*exp(-kap/8))
            assert lower <= float(aa)+1e-14 <= upper+1e-14
            fixtures += 1
            for length in probs:
                tt, gg = g_exact(q, length)
                aa_l = posterior_radius_exact(q, length)
                assert gg >= 0
                assert gg >= r/2-F(1, 2*(2*length+1))
                assert tt >= 1
                assert tt*z(q,2*length)/(2*length+1) <= 1
                for output_length in range(0, 11):
                    aa_k = posterior_radius_exact(q, output_length)
                    assert aa_k*aa_l-aa_k*aa_k/2 <= aa_l*aa_l/2
                    proper_fixtures += 1
                    total = length+output_length
                    biggest = z(q,total)/((total+1)*z(q,length))
                    for spin in range(abs(length-output_length), total+1, 2):
                        eigen = q**((total-spin)//2)*z(q,spin)/((spin+1)*z(q,length))
                        assert eigen <= biggest
                for keep in range(1, length+2):
                    omitted = (q**keep-q**(length+1))/(1-q**(length+1))
                    direct = sum((q**k/z(q,length) for k in range(keep,length+1)), F(0))
                    assert omitted == direct
                    rank_fixtures += 1
            radius_max = max(posterior_radius_exact(q,length) for length in probs)
            sharp_score = sum((p*posterior_radius_exact(q,length)**2/length
                               for length,p in probs.items() if length),F(0))/radius_max
            if n == 1:
                assert sharp_score == r/3

    for n in range(1,19):
        radii = (F(0),F(1,16),F(1,8),F(1,4),F(1,2))
        laws = [schur_exact(n,r) for r in radii]
        lengths = sorted(laws[0])
        for low,high in zip(laws,laws[1:]):
            ratios = [high[length]/low[length] for length in lengths]
            assert all(x<=y for x,y in zip(ratios,ratios[1:]))
            for cutoff in lengths:
                assert sum(high[length] for length in lengths if length>cutoff) >= sum(
                    low[length] for length in lengths if length>cutoff)
                mlr_fixtures += 1

    critical = []
    for c in (0.5, 1.0, 2.0, 3.0):
        limiting = critical_tail(c)
        assert limiting > 0
        for n in (256, 1024, 4096, 16384, 65536):
            r = c/sqrt(n)
            q = (1-r)/(1+r)
            beta = -log(q)
            probs = schur_float(n,r)
            aa = sum(p*exp(-beta*(length+1)) for length,p in probs.items())
            cutoff = min(n, int(n*r+2*sqrt(n*log(1/r)))+1)
            retained = [(length,p) for length,p in probs.items() if length<=cutoff]
            tail = sum(p for length,p in probs.items() if length>cutoff)
            normalization = max(g_float(q,length)[0] for length,p in retained)
            numerator = sum(p*g_float(q,length)[0]*g_float(q,length)[1]
                            for length,p in retained)
            bound = max(0.0, (2/3)*(numerator/normalization-tail))
            radii = {length:posterior_radius_float(q,length) for length in probs}
            sharp_bound = sum(p*radii[length]**2/length for length,p in probs.items() if length)
            sharp_bound /= max(radii.values())
            assert sharp_bound > 0
            critical.append({"n":n,"c":c,"r":r,"A_n":aa,"A_limit":limiting,
                             "canonical_tail_difference":aa-limiting,
                             "cutoff":cutoff,"omitted_sector_mass":tail,
                             "master_EB_error_lower":bound,
                             "bound_over_r":bound/r,
                             "bound_over_r_div_sqrt_log":bound*sqrt(log(1/r))/r,
                             "sharp_proper_score_EB_lower":sharp_bound,
                             "sharp_bound_over_r":sharp_bound/r})

    result = {"status":"FINITE-EVIDENCE only; scalar identities and asymptotics",
              "exact_schur_fixtures":fixtures,"exact_Fock_cutoff_fixtures":rank_fixtures,
              "exact_proper_score_fixtures":proper_fixtures,
              "exact_radius_MLR_tail_fixtures":mlr_fixtures,
              "single_qubit_exact_EB_bound":"r/3, passed",
              "exact_twirl_eigenvalue_order":"passed",
              "exact_master_scalar_inequalities":"passed",
              "critical_fixtures":critical}
    destination = Path(__file__).with_name('precision_checks.json')
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"exact_schur_fixtures":fixtures,
                      "exact_Fock_cutoff_fixtures":rank_fixtures,
                      "exact_proper_score_fixtures":proper_fixtures,
                      "exact_radius_MLR_tail_fixtures":mlr_fixtures,
                      "critical_fixtures":len(critical),"output":str(destination)},indent=2))


if __name__ == '__main__':
    run()
