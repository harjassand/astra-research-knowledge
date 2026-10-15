"""Independent algebra/finite numerical diagnostics for the prior-art distinctions.

This does not certify the universal regularization theorem, a new gap constant,
historical priority, or mathematical sharpness.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import sympy as sp
import mpmath as mp

out = Path(__file__).resolve().parent
tau, c = sp.symbols("tau c", positive=True, real=True)
z = (sp.pi / tau) ** sp.Rational(3, 2) * sp.exp(c*c/(4*tau)) * (1+c*c/(2*tau))
coef = sp.simplify((sp.diff(z, c)/(3*z)).subs(c, 2*tau))
claimed = (3+2*tau)/(3*(1+2*tau))
assert sp.simplify(coef-claimed) == 0
assert sp.simplify((1-coef) - 4*tau/(3*(1+2*tau))) == 0
assert sp.limit(coef, tau, sp.oo) == sp.Rational(1, 3)

mp.mp.dps = 50
rows = []
for val in ["0.25", "1", "4"]:
    t = mp.mpf(val)
    # The common scalar e^{-3 tau} is irrelevant after normalization.
    zquad = 4*mp.pi * mp.quad(
        lambda r: r*r*mp.exp(-t*r*r)*mp.cosh(2*t*r), [0, 1, mp.inf]
    )
    numquad = (4*mp.pi/3) * mp.quad(
        lambda r: r**3*mp.exp(-t*r*r)*mp.sinh(2*t*r), [0, 1, mp.inf]
    )
    target = (3+2*t)/(3*(1+2*t))
    rows.append({
        "tau": val, "mean_sigma_coefficient_quad": str(numquad/zquad),
        "exact_formula_at_tau": str(target),
        "absolute_error": str(abs(numquad/zquad-target)),
        "quadrature_check": bool(abs(numquad/zquad-target) < mp.mpf("1e-40")),
    })
assert all(row["quadrature_check"] for row in rows)
sinczero = sp.simplify(sp.sin(3*sp.pi/2)/(3*sp.pi/2))
assert sinczero == -sp.Rational(2, 3)/sp.pi
data = {
    "created_at_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Independent symbolic identities and finite numerical diagnostics only.",
    "husimi_mean_symbolic": str(coef),
    "husimi_mean_gap_to_one_symbolic": str(sp.simplify(1-coef)),
    "husimi_mean_limit": str(sp.limit(coef, tau, sp.oo)),
    "husimi_quadratures": rows,
    "coherent_report3_scalar_at_pi_over2_exact": str(sinczero),
    "coherent_report3_scalar_at_pi_over2_numeric": str(mp.mpf(-2)/(3*mp.pi)),
    "root_candidate_trace_bound_numeric": str(6+16/mp.pi**3),
    "root_candidate_proof_audited_by_this_worker": False,
    "ordinary_lower_bound_proof": "Analytic Cauchy-Schwarz argument in PRIOR_ART.md; not a finite numerical test.",
}
(out/"CHECKS.json").write_text(json.dumps(data, indent=2)+"\n")
print(json.dumps({"symbolic_checks_passed": True,
                  "quadrature_checks_passed": len(rows),
                  "scope": data["scope"]}, indent=2))
