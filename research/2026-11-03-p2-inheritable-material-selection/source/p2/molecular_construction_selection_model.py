#!/usr/bin/env python3
"""Exact minimal model for a genotype-to-material lock step.
Only a mathematical research check, not measured chemistry.
State E (empty), C/W (reversibly docked), C*/W* (locked).
All quantities are per second. Leak d is wrong permanent locking from E.
No independent-site assumption enters the single-site absorption formulas.
"""
from math import exp, log, sqrt

def lock_model(a_c, a_w, b_c, b_w, lock_c, lock_w, leak=0.0):
    values = [a_c, a_w, b_c, b_w, lock_c, lock_w, leak]
    if any(x < 0 for x in values) or a_c <= 0 or lock_c <= 0 or (a_w > 0 and b_w + lock_w == 0):
        raise ValueError("nonnegative rates; a_c, lock_c strictly positive")
    correct_flux = a_c * lock_c / (b_c + lock_c)
    wrong_flux = a_w * lock_w / (b_w + lock_w) if (b_w + lock_w) else 0.
    total = correct_flux + wrong_flux + leak
    # Renewal at E: sum of excursion times divided by per-excursion absorption.
    time = (1.0 + a_c/(b_c+lock_c)
            + (a_w/(b_w+lock_w) if (b_w+lock_w) else 0)) / total
    return {
        "P_correct": correct_flux/total,
        "P_wrong": (wrong_flux+leak)/total,
        "wrong_correct_odds": (wrong_flux+leak)/correct_flux,
        "mean_lock_seconds": time,
        "correct_flux": correct_flux,
        "wrong_flux": wrong_flux,
        "leak_flux": leak,
    }

def whole_structure_purity(p_wrong, n):
    """Only if sites have independent, identical final lock errors."""
    return exp(n*log(1.0-p_wrong))

def max_site_error(n, target=0.99):
    """Independent identical-site necessity/sufficiency for target fidelity."""
    return 1.0-target**(1.0/n)

def photon_count_for_poisson_bhattacharyya(relative_gain, target_error=0.01):
    """Sufficient lower-brightness count if only shot noise and zero background.
    P_Bayes_error <= .5 exp[-(sqrt(lambda1)-sqrt(lambda0))^2/2].
    Here lambda1=relative_gain*lambda0. This is NOT a necessary count.
    """
    if relative_gain <= 1. or not (0 < target_error < .5):
        raise ValueError("gain>1 and 0<target_error<0.5")
    return 2*log(.5/target_error)/(sqrt(relative_gain)-1.)**2

if __name__ == "__main__":
    n = 10000
    models = {
        "undiscriminating_lock": (1., 1., .01, 10., .1, .1, 0.),
        "idealized_two_gates_UNMEASURED": (1., .001, .01, 10., .1, .0001, 0.),
        "same_with_off_template_leak_UNMEASURED": (1., .001, .01, 10., .1, .0001, 1e-7)
    }
    print("target 99%% all-correct for n=%s: per-site p<=%.9g"
          % (n,max_site_error(n)))
    for label, pars in models.items():
        result = lock_model(*pars)
        print(label, result, "whole_structure_if_independent=",
              whole_structure_purity(result["P_wrong"], n))
    print("shot-noise-only photons to distinguish 10% brighter",
          photon_count_for_poisson_bhattacharyya(1.1, .01))

def symmetric_lock_optimum(a_c, a_w, b_c, b_w, leak):
    """Exact optimum common irreversible-lock hazard ell for b_w>b_c, a_w>0.

    Wrong/correct odds = (a_w/a_c)*(b_c+ell)/(b_w+ell)
                         +(leak/a_c)*(1+b_c/ell).
    Leak is a separately sustained hazard, independent of ell.
    Returns (ell_star, minimum_odds); infinity if optimum at ell->infinity.
    """
    if not (a_c > 0 and a_w > 0 and b_w > b_c > 0 and leak >= 0):
        raise ValueError('Requires a_c,a_w,b_c>0, b_w>b_c, leak>=0')
    q = sqrt(leak*b_c/(a_w*(b_w-b_c)))
    if q == 0:
        return 0., (a_w/a_c)*(b_c/b_w)
    if q >= 1:
        return float('inf'), (a_w+leak)/a_c
    ell_star = q*b_w/(1-q)
    r_min = (a_w/a_c)*(b_c+ell_star)/(b_w+ell_star) + (leak/a_c)*(1+b_c/ell_star)
    return ell_star, r_min

if __name__ == "__main__":
    for leak in [0, 1e-6, 1e-4, 1e-2]:
        ell, odds = symmetric_lock_optimum(1., 1., .01, 10., leak)
        print("equal-lock-optimum", "leak=", leak, "ell*=", ell,
              "pwrong_min=", odds/(1+odds))
        if ell > 0 and ell < float('inf'):
            result = lock_model(1., 1., .01, 10., ell, ell, leak)
            assert abs(result['wrong_correct_odds']-odds) < 1e-12

def poisson_compartment_cost(lam):
    """Random genotype loading: occupied fraction, multi-genotype fraction conditional
    on an occupied droplet, and mean droplets per occupied droplet.
    No assertion that two molecules necessarily have distinct genotypes.
    """
    from math import expm1
    if not lam > 0:
        raise ValueError('lambda>0')
    occupied = -expm1(-lam)
    conditional_multi = 1 - lam/expm1(lam)
    return occupied, conditional_multi, 1/occupied

if __name__ == '__main__':
    for lam in [0.1, 0.02, 0.002]:
        print('Poisson compartment', lam, poisson_compartment_cost(lam))
