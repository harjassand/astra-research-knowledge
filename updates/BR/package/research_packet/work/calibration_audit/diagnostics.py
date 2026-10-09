#!/usr/bin/env python3
"""Exact rational identities and reproducible finite diagnostics, stdlib only.

The physical acquisition procedure is analyzed, not hardware-executed.
The implemented sampler is exact under ideal fair random bits; seeded
Random below is used solely for a reproducible Monte Carlo diagnostic.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
from math import factorial, comb, ceil
import json
from pathlib import Path
import random


def ratios(h):
    assert h % 2 == 0 and h >= 2
    out = [Fraction(1)]
    for j in range(h // 2):
        out.append(out[-1] * Fraction((h - 2*j)**2,
                                      h*h*(2*j+1)*(2*j+2)))
    return out


def proposed_weight(h, k):
    a = Fraction(1, 4)
    b = Fraction(1, 4*h)
    if k < 0 or k > h or (h-k) % 2:
        return Fraction(0)
    return (factorial(h)**2 * a**(h-k) * b**k /
            (factorial(k)*2**(h-k)*factorial((h-k)//2)**2))


def acceptance(h, j):
    if 2*j > h:
        return Fraction(0)
    acc = Fraction(2**j, factorial(2*j))
    for r in range(j):
        acc *= Fraction((h-2*r)**2, h*h)
    return acc


def conditional_sample(h, rng):
    """Return (K, proposal count) using rational geometric rejection."""
    attempts = 0
    while True:
        attempts += 1
        j = 0
        while rng.getrandbits(1):
            j += 1
        acc = acceptance(h, j)
        if acc and rng.randrange(acc.denominator) < acc.numerator:
            return 2*j, attempts


def lazy_bernoulli(compare_endpoint, rng):
    """Exact under fair bits; comparator returns sign(u-threshold)."""
    prefix, denominator, bits = 0, 1, 0
    while True:
        if compare_endpoint(Fraction(prefix+1, denominator)) <= 0:
            return True, bits
        if compare_endpoint(Fraction(prefix, denominator)) >= 0:
            return False, bits
        prefix = 2*prefix + rng.getrandbits(1)
        denominator *= 2
        bits += 1


def sign(x):
    return (x > 0) - (x < 0)


def compare_rebalance(u, q, v):
    """Sign of u-q/(1-sqrt(v)), using exact rational operations."""
    assert 0 < q < 1 and 0 < v < 1
    if u <= q:
        return -1
    return sign((1-q/u)**2-v)


class ExactPlan:
    """Classical plan for physical on/off measurement and exact rebalancing.

    handle_click consumes a physical any-click flag. simulate_i1 below is
    explicitly an ideal-probability simulation, not a physical measurement.
    """
    def __init__(self, h):
        self.h = h
        self.z = sum(ratios(h))
        self.q = 1-1/self.z
        self.rho = 1-Fraction(8*h-1, 15*h*h)  # F^2
        # Integer doubling/bisection avoids any fixed-precision log seed.
        lower, upper = 0, 1
        bound = 1/self.z**2
        while self.rho**upper > bound:
            lower, upper = upper, 2*upper
        while upper-lower > 1:
            mid = (lower+upper)//2
            if self.rho**mid <= bound:
                upper = mid
            else:
                lower = mid
        self.n = upper
        self.v = self.rho**self.n
        assert self.v <= 1/self.z**2
        assert self.n == 0 or self.rho**(self.n-1) > 1/self.z**2

    def handle_click(self, any_click, rng):
        if not any_click:
            return 0
        accepted, _ = lazy_bernoulli(
            lambda u: compare_rebalance(u, self.q, self.v), rng)
        if not accepted:
            return 0
        while True:
            k, _ = conditional_sample(self.h, rng)
            if k > 0:
                return k

    def simulate_i1(self, rng):
        all_vacuum, _ = lazy_bernoulli(lambda u: sign(u*u-self.v), rng)
        return self.handle_click(not all_vacuum, rng)


def dec(x):
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x)


def run():
    report = {"status": "finite_diagnostics_passed",
              "hardware_execution": False,
              "independent_external_verification": False,
              "exact_identity_cases": [], "numerical_cases": [],
              "sampler_cases": [], "exact_rebalance_simulations": []}
    for m in (1, 2, 3):
        h = 4*m*m
        r = ratios(h)
        w0 = proposed_weight(h, 0)
        assert r[1] == Fraction(1, 2)
        assert all(proposed_weight(h, 2*j)/w0 == rj
                   for j, rj in enumerate(r))
        z = sum(r)
        assert 1 - 1/z >= Fraction(1, 3)
        for j, rj in enumerate(r):
            aj = acceptance(h, j)
            assert 0 <= aj <= 1
            assert Fraction(1, 2**(j+1))*aj == rj/2
        a, b = Fraction(1,4), Fraction(1,4*h)
        d0, d1 = 1-a*a, (1-b)**2-a*a
        x = Fraction(8*h-1, 15*h*h)
        assert d1/d0 == 1-x
        report["exact_identity_cases"].append({
            "m":m, "h":h, "Z_h":str(z),
            "conditional_TV":str(1-1/z),
            "squared_fidelity_squared":str(1-x),
            "mean_rejection_proposals":str(2/z)})
    with localcontext() as ctx:
        ctx.prec = 80
        for m in (1, 2, 4, 8, 16, 32):
            h = 4*m*m
            rj, z = Decimal(1), Decimal(1)
            for j in range(h//2):
                rj *= dec((h-2*j)**2)/dec(h*h*(2*j+1)*(2*j+2))
                z += rj
            x=dec(Fraction(8*h-1,15*h*h))
            f=(1-x).sqrt()
            p0=(dec(15)/16).sqrt()*dec(comb(h,h//2))/dec(2**h)*dec(4)**(-h)
            p1=p0*f*z
            assert f > 0 and f < 1
            assert p0 > 0 and p1 > 0
            assert 1-f <= dec(Fraction(8,15*h))
            assert 1-f >= dec(Fraction(7,30*h))
            lower=(dec(Fraction(36,35)).ln())/(-f.ln())
            upper=ceil(dec(12).ln()/(-f.ln()))
            # Squared overlap from the mode-2=0 Fock expansion. The
            # truncated overlap is checked separately from the closed form.
            d0=dec(15)/16
            d1=d0*(1-x)
            common=(d0*d1).sqrt().sqrt()
            overlap_partial=common*sum(dec(comb(2*n,n))*
                                      dec(Fraction(1,64))**n
                                      for n in range(80))
            assert abs(overlap_partial**2-f) < Decimal("1e-70")
            report["numerical_cases"].append({
                "m":m,"h":h,"F_squared_overlap":str(f),
                "conditional_TV":str(1-1/z),
                "physical_herald_p0":str(p0),
                "physical_herald_p1":str(p1),
                "lower_N_exact_real":str(lower),
                "lower_N_integer":ceil(lower),
                "upper_N_miss_at_most_1_over_12":upper,
                "exact_sampling_N_star_numerical":ceil(z.ln()/(-f.ln())),
                "exact_sampling_N_star_over_h":ceil(z.ln()/(-f.ln()))/h})
    # A diagnostic, not a statistical proof or a hardware experiment.
    for h in (4, 16, 64):
        rng = random.Random(20261010+h)
        samples=100_000
        hist={}
        attempts=0
        for _ in range(samples):
            k,cost=conditional_sample(h,rng)
            hist[k]=hist.get(k,0)+1
            attempts+=cost
        r=ratios(h)
        z=sum(r)
        tv=0.5*sum(abs(hist.get(2*j,0)/samples-float(rj/z))
                   for j,rj in enumerate(r))
        # Six binomial standard errors for the large zero-mass bin;
        # this deterministic seeded replay check has ample slack.
        assert tv < 0.012
        report["sampler_cases"].append({
            "h":h,"samples":samples,"histogram":hist,
            "empirical_TV":tv,"mean_proposals":attempts/samples,
            "exact_mean_proposals":float(2/z)})
    for h in (4, 16, 64):
        plan=ExactPlan(h)
        rng=random.Random(10102026+h)
        samples=20_000
        hist={}
        for _ in range(samples):
            k=plan.simulate_i1(rng)
            hist[k]=hist.get(k,0)+1
        assert plan.handle_click(False,rng) == 0
        r=ratios(h)
        tv=0.5*sum(abs(hist.get(2*j,0)/samples-float(rj/plan.z))
                   for j,rj in enumerate(r))
        assert tv < 0.03
        report["exact_rebalance_simulations"].append({
            "h":h,"optimal_N_exact_rational_certified":plan.n,
            "copies_simulated_not_hardware":True,
            "samples":samples,"histogram":hist,"empirical_TV":tv,
            "rational_v_numerator_bits":plan.v.numerator.bit_length(),
            "rational_v_denominator_bits":plan.v.denominator.bit_length()})
    target=Path(__file__).with_name("diagnostics.json")
    target.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],
                      "exact_cases":len(report["exact_identity_cases"]),
                      "numerical_cases":len(report["numerical_cases"]),
                      "sampler_cases":len(report["sampler_cases"]),
                      "exact_rebalance_cases":len(report["exact_rebalance_simulations"]),
                      "report":str(target.resolve())},indent=2))


if __name__ == "__main__":
    run()
