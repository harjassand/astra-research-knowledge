"""Exact health and conserved-source diagnostics for the frozen f(R) target.

This is an algebra check, not proof of arbitrary-action synthesis or an
observational claim. The theorem proof is in v1--v4.txt.
"""
import json
from pathlib import Path
import sympy as s

H, M, F = s.symbols("H M F", positive=True)
varphi = s.symbols("varphi", real=True)
R = s.symbols("R", real=True)
f = R - 6*H**2 + R**2/(12*H**2)
R_of_F = 6*H**2*(F-1)
U = s.expand(R_of_F*F-f.subs(R, R_of_F))
V_E = s.simplify((M**2/3)/2 * (3/F)**2 * U)
z = s.sqrt(s.Rational(2,3))*varphi/M
canonical_V = s.simplify(V_E.subs(F,3*s.exp(z)))
target_V = 3*H**2*M**2/s.Integer(2)*(3-2*s.exp(-z)+s.exp(-2*z))

tau, tau_i = s.symbols("tau tau_i", negative=True)
k = s.symbols("k", positive=True)
rho_s = s.symbols("rho_s", real=True)
a = -1/(H*tau)
Hcal = s.diff(a,tau)/a
rho = rho_s/a**3
T00 = rho/a**2
V = -rho_s/(2*M**2*k**2*a)
dF = rho_s/(M**2*k**2*a)*(1-s.cos(k*(tau-tau_i)))
Phi = V+dF/6
Psi = V-dF/6
unknown_A, unknown_B = s.symbols("unknown_A unknown_B", real=True)
dF_any = dF+(unknown_A*s.cos(k*(tau-tau_i))+
             unknown_B*s.sin(k*(tau-tau_i)))/a
Phi_any = V+dF_any/6
Psi_any = V-dF_any/6

residuals = {
    "canonical_potential": s.simplify(canonical_V-target_V),
    "potential_at_minimum": s.simplify(canonical_V.subs(varphi,0)-3*M**2*H**2),
    "potential_first_derivative": s.simplify(s.diff(canonical_V,varphi).subs(varphi,0)),
    "canonical_mass_squared": s.simplify(s.diff(canonical_V,varphi,2).subs(varphi,0)-2*H**2),
    "dust_energy_conservation": s.simplify(s.diff(rho,tau)+3*Hcal*rho),
    "dust_contravariant_divergence_0": s.simplify(s.diff(T00,tau)+5*Hcal*T00),
    "einstein_00": s.simplify(k**2*V+3*Hcal*(s.diff(V,tau)+Hcal*V)+a**2*rho/(2*M**2)),
    "einstein_0i": s.simplify(s.diff(V,tau)+Hcal*V),
    "einstein_pressure": s.simplify(s.diff(V,tau,2)+3*Hcal*s.diff(V,tau)+(2*s.diff(Hcal,tau)+Hcal**2)*V),
    "initial_mode_independent_identity": s.simplify(s.diff(a*(Phi_any-Psi_any),tau,2)+k**2*a*(Phi_any-Psi_any)+k**2*a*(Phi_any+Psi_any)/3),
    "half_period_eta": s.simplify((Phi/Psi).subs(tau,tau_i+s.pi/k)-s.Rational(1,5)),
    "half_period_force_lensing_ratio": s.simplify((2*Psi/(Phi+Psi)).subs(tau,tau_i+s.pi/k)-s.Rational(5,3)),
}
data = {
    "scope": "Exact symbolic f(R) health, linear conserved dust, Einstein-frame constraints and initial-independent scalar identity; no empirical input.",
    "sympy_version": s.__version__,
    "U_of_F": str(U),
    "canonical_potential": str(canonical_V),
    "residuals": {key:str(value) for key,value in residuals.items()},
    "all_claimed_residuals_zero": all(value==0 for value in residuals.values()),
}
assert data["all_claimed_residuals_zero"], data
path = Path(__file__).with_name("health_source_checks_v1.json")
if path.exists():
    assert json.loads(path.read_text()) == data, "Frozen diagnostic changed; use a new version."
else:
    path.write_text(json.dumps(data,indent=2)+"\n")
print(json.dumps(data,indent=2))
