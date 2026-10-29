"""Independent exact-rational schedule checks; not a concentration experiment.

All asserted inequalities use fractions/integers.  This checks finite schedules,
not the analytic proof of their universal validity or any #SAT solver.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

def ceil(x):
    return -(-x.numerator // x.denominator)

def ceil_log2(x):
    assert x > 0
    b = 0
    while F(2)**b < x:
        b += 1
    while F(2)**(b-1) >= x:
        b -= 1
    return b

def ceil_sqrt(x):
    b = isqrt(x.numerator // x.denominator)
    return b if b*b == x else b+1

checks = []
for n in [1, 2, 17, 1024, 10**9]:
    for k in [1, 2, 7]:
        for g in [F(1,1024), F(1,3), F(1), F(100)]:
            for tau in [F(1), F(1,2), F(1,17), F(1,4096), min(F(1), 3*g), min(F(1), F(3999,1000)*g)]:
                if g <= tau/4:
                    continue  # only the nontrivial branch is under test
                for w in [F(1,1000), F(1,2), F(1)]:
                    L = n*(tau/4 + w*(g-tau/4))
                    q = ceil(512*L*L/(tau*tau*n))
                    J = L/q
                    lam = q*g/L
                    D = ceil(9*lam) + ceil_log2(200*g/tau)
                    assert tau*tau/(528*g) <= J < tau/128
                    assert D >= 9*lam
                    # Equivalent power-of-two comparison, without materializing
                    # an integer with D bits when D is intentionally enormous.
                    assert D >= ceil_log2(200*g/tau)
                    assert D*J < 10*g
                    theta = tau/(4*g)
                    Kbar = 20*k*k*g
                    beta = 4/tau
                    r = max(1, ceil(2*Kbar*beta), ceil_sqrt(F(64,9)*Kbar*Kbar*beta*beta*g/tau))
                    # Check minimality and the exact schedule conditions.
                    assert r >= 2*Kbar*beta
                    assert r*r >= F(64,9)*Kbar*Kbar*beta*beta*g/tau
                    if r > 1:
                        assert r-1 < 2*Kbar*beta or (r-1)**2 < F(64,9)*Kbar*Kbar*beta*beta*g/tau
                    delta = beta/r
                    assert Kbar*delta <= F(1,2)
                    assert delta*J < 1
                    assert theta < 1
                    eta = delta*theta*J/16
                    assert 0 < eta < F(1,4)
                    B = max(0, ceil_log2(2*(2**k)/eta))
                    assert F(2)**(-B) <= eta/(2*(2**k))
                    assert B == 0 or F(2)**(-B+1) > eta/(2*(2**k))
                    # Local log Lipschitz constant 4, times generator factor 2.
                    assert 8*eta/delta <= theta*J
                    assert q*theta*J <= n*tau/4
                    trotter_density = 4*g*Kbar*Kbar*delta*delta/(3*(1-(Kbar*delta)**2))
                    assert trotter_density <= tau/4
                    # A-H: sampling/trim + rounding + product formula.
                    assert tau/2 + tau/4 + trotter_density <= tau
                    # Use ln2 < 1; tau=epsilon/4, so epsilon=4tau.
                    assert 2*tau + 1/beta < 4*tau
                    cap = ceil_log2(1000*q)
                    assert q*F(2)**(-cap) <= F(1,1000)
                    checks.append({"n":n,"k":k,"g":str(g),"tau":str(tau),"L":str(L),"q":q,"D":D,"r":r,"B":B})

out = {
    "status":"PASS", "exact_rational_schedule_cases":len(checks),
    "largest_n":max(x["n"] for x in checks),
    "largest_q":max(x["q"] for x in checks),
    "largest_r":max(x["r"] for x in checks),
    "largest_B":max(x["B"] for x in checks),
    "scope":"Exact finite parameter schedules, not rare-tail validation, matrix rounding, or a full counting solver."
}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
