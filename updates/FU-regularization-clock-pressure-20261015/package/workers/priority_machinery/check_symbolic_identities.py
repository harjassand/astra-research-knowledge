"""Exact algebra diagnostics for the transfer; not a proof or priority checker."""
from pathlib import Path
import json
import sympy as s

x, c, R, L = s.symbols("x c R L", positive=True)
rho = s.sqrt(1 + x*x)
f = rho*s.log(rho)
hess_expected = (x*x + 1 + s.log(rho))/rho**3
hess_res = s.simplify(s.diff(f, x, 2) - hess_expected)
K1sq = s.sinh(R*x)**2/x**2
K2plus = R/x - (1 - s.exp(-2*R*x))/(2*x*x)
K2minus = -R/x + (s.exp(2*R*x) - 1)/(2*x*x)
d = (s.sinh(2*R*x) - 2*R*x)/(2*x*x)
resplus = s.simplify(s.expand_trig(K2plus - K1sq + d).rewrite(s.exp))
resminus = s.simplify(s.expand_trig(K2minus - K1sq - d).rewrite(s.exp))
result = {
    "status": "exact_symbolic_identity_check_only",
    "radial_hessian_residual": str(hess_res),
    "pauli_upper_residual": str(resplus),
    "pauli_lower_residual": str(resminus),
    "all_zero": hess_res == 0 and resplus == 0 and resminus == 0,
    "does_not_check": [
        "distribution estimates", "Paley-Wiener theorem",
        "all-point proof inequalities", "historical priority", "physical synthesis"
    ],
}
Path(__file__).with_name("SYMBOLIC_IDENTITY_CHECK.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(json.dumps(result, indent=2))
