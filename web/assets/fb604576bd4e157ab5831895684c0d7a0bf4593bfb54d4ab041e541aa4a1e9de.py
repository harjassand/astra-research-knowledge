"""Scoped algebra checks for nonequilibrium_physics.md; not a proof certificate.

Run with python3 work/scouts/nonequilibrium_derivations.py.
The symbolic checks concern a proposed exact equilibrium completion and the
spectral algebra. Quadrature checks only confirm the derived integral on fixtures.
"""
from pathlib import Path
import json
import math
import sympy as s
import mpmath as mp

checks = {}
g, r, nu = s.symbols("g r nu", positive=True, real=True)
alpha = 2 * g / (2 + r)
beta = 2 * g * (1 + r) / (2 + r)
kappa = (g - alpha) ** 2
Cq = 1 / alpha
temperature = kappa / alpha
Aeq = s.Matrix([[-alpha, 1], [-kappa, -beta]])
Ceq = s.diag(Cq, temperature)
Deq = s.diag(1, beta * temperature)
parity = s.diag(1, -1)

def zero_matrix(m):
    return all(s.simplify(z) == 0 for z in m)

checks["equilibrium_lyapunov"] = zero_matrix(
    Aeq * Ceq + Ceq * Aeq.T + 2 * Deq
)
checks["equilibrium_parity_reversal"] = zero_matrix(
    Ceq * Aeq.T * Ceq.inv() - parity * Aeq * parity
)
checks["equilibrium_poles"] = (
    s.simplify(Aeq.trace() + 2 * g) == 0
    and s.simplify(Aeq.det() - g**2) == 0
)
checks["equilibrium_observed_PSD"] = (
    s.simplify(beta**2 + beta * temperature - g**2 * (1 + r)) == 0
)

a, b, c, d = s.symbols("a b c d", positive=True, real=True)
Jc = 1 / ((a + b) * (a + c) * (b + c))
Jd = 1 / ((a + b) * (a + d) * (b + d))
I4 = (a + b + c + d) / (
    (a + b) * (c + d) * (a + c) * (b + c) * (a + d) * (b + d)
)
checks["four_pole_integral_algebra"] = s.simplify(
    (Jc - Jd) / (d**2 - c**2) - I4
) == 0

# Check the Gaussian 2x2 forward/reversed spectral trace directly.
aa, bb, cr, ci = s.symbols("aa bb cr ci", real=True)
Sm = s.Matrix([[aa, cr+s.I*ci], [cr-s.I*ci, bb]])
checks["spectral_trace_identity"] = s.simplify(
    (Sm.T.inv()*Sm).trace() - 2 - 4*ci**2/Sm.det()
) == 0

mp.mp.dps = 45
fixtures = []
for av, bv, cv, dv in [(1, 2, 3, 4), (1, 1, 1, 2), (.4, 1.3, .7, .7001)]:
    f = lambda x: x*x / (
        (x*x+av*av)*(x*x+bv*bv)*(x*x+cv*cv)*(x*x+dv*dv)
    )
    numeric = mp.quad(f, [-mp.inf, 0, mp.inf]) / mp.pi
    analytic = (av+bv+cv+dv) / (
        (av+bv)*(cv+dv)*(av+cv)*(bv+cv)*(av+dv)*(bv+dv)
    )
    fixtures.append({"poles": [av,bv,cv,dv],
                     "absolute_error": float(abs(numeric-analytic))})
checks["quadrature_fixtures"] = fixtures

# Exact stroboscopic OU observation ambiguity is represented algebraically;
# trigonometric evaluation at large integer multiples would be a floating check.
theta, decay, cov = s.symbols("theta decay cov", real=True, positive=True)
R = s.Matrix([[s.cos(theta),-s.sin(theta)],
              [s.sin(theta),s.cos(theta)]])
checks["OU_transition_noise_independent_of_rotation"] = zero_matrix(
    decay*R*(cov*s.eye(2))*(decay*R).T - decay**2*cov*s.eye(2)
)
checks["OU_sampled_EPR"] = s.simplify(
    (R - R.T).T*(R - R.T)
    - 4*s.sin(theta)**2*s.eye(2)
) == s.zeros(2)

out = {"status":"scoped_symbolic_and_quadrature_checks_only", "checks":checks}
assert all(v for v in checks.values() if isinstance(v, bool))
path = Path(__file__).with_name("nonequilibrium_derivations.json")
path.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
