"""Small exact checks and a rational verifier for an admitted entropy cone.

The verifier does not acquire a manifold, an h-net, Lipschitz constants,
incompressibility, or primitive tensor enclosures. Those are explicit inputs.
The homogeneous Sol identities are independently rebuilt symbolically.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time
import sympy as z

ROOT = Path(__file__).resolve().parent


def sqrt_bounds(x, bits=72):
    x = F(x)
    assert x >= 0
    if x == 0:
        return F(0), F(0)
    scale = 1 << bits
    n = math.isqrt((x.numerator * scale * scale) // x.denominator)
    lo = F(n, scale)
    hi = F(n + 1, scale)
    assert lo * lo <= x <= hi * hi
    return lo, hi


def log_cat_bounds(bits=72, terms=64):
    # log((3+sqrt(5))/2)=2 artanh(1/sqrt(5)).
    rl, ru = sqrt_bounds(F(5), bits)
    zl, zu = 1 / ru, 1 / rl
    lo = sum(2 * zl ** (2*k + 1) / (2*k + 1) for k in range(terms))
    hi = sum(2 * zu ** (2*k + 1) / (2*k + 1) for k in range(terms))
    hi += 2 * zu ** (2*terms + 1) / ((2*terms + 1) * (1 - zu*zu))
    return lo, hi


def cone_verifier(samples, h, lip_s, lip_w, eta_s, eta_w, alpha, kappa):
    """Exact arithmetic; return UNKNOWN rather than infer absent coverage."""
    h, lip_s, lip_w, eta_s, eta_w, alpha, kappa = map(
        F, (h, lip_s, lip_w, eta_s, eta_w, alpha, kappa))
    if not samples or min(h, lip_s, lip_w, eta_s, eta_w) < 0:
        return {'status': 'REJECTED_INPUT'}
    s0 = min(F(s) for s, _ in samples) - eta_s - lip_s*h
    omega = max(abs(F(w)) for _, w in samples) + eta_w + lip_w*h
    admissible = (0 < alpha < 1 and kappa > 0 and s0 > 0 and
                  omega*(1+alpha*alpha) <= 2*s0*alpha and
                  kappa <= s0-omega*alpha)
    return {'status': 'CERTIFIED' if admissible else 'UNKNOWN',
            's_lower': str(s0), 'omega_upper': str(omega),
            'alpha': str(alpha), 'entropy_lower': str(kappa) if admissible else None,
            'scope': 'Conditional on supplied covering h-net, uniform errors and Lipschitz bounds.'}


def symbolic_checks():
    a, c, u, v = z.symbols('a c u v', real=True)
    n2 = c*c+u*u+v*v
    yy = z.Matrix([c, u, v])
    # Advected coordinates in the global orthonormal left-invariant frame.
    G = z.Matrix([[0, 0, 0], [-a*u, a*c, 0], [a*v, 0, -a*c]])
    S = (G+G.T)/2
    P = z.eye(3)-yy*yy.T/n2
    Q = z.simplify(P*G*P)
    B = z.simplify((Q+Q.T)/2)
    K = z.simplify((Q-Q.T)/2)
    s2 = z.simplify(z.trace(B*B)/2)
    w2 = z.simplify(-z.trace(K*K)/2)
    checks = {
        'advected_flow_line_zero': G*yy == z.zeros(3, 1),
        'divergence_zero': z.trace(G) == 0,
        'strain_norm': z.simplify(z.trace(S*S) - 2*a*a*c*c - a*a*(u*u+v*v)/2) == 0,
        'quotient_trace_zero': z.simplify(z.trace(Q)) == 0,
        'quotient_rate_discriminant': z.simplify(s2-w2-a*a*c*c) == 0,
        'homogeneous_full_characteristic_polynomial':
            z.simplify(G.charpoly().as_expr() - z.Symbol('lambda')*(z.Symbol('lambda')-a*c)*(z.Symbol('lambda')+a*c)) == 0,
        'equal_power_zero_entropy_pair':
            z.simplify(z.trace(S*S).subs({c:0, u:2, v:0}) -
                       z.trace(S*S).subs({c:1, u:0, v:0})) == 0,
        'one_transverse_component_s': z.simplify(s2.subs(v, 0)-a*a*c*c) == 0,
        'one_transverse_component_rotation_zero': z.simplify(w2.subs(v, 0)) == 0,
    }
    ss, ww, al = z.symbols('s omega alpha', real=True)
    D = z.diag(ss, -ss)
    dD = z.Matrix([[0, 2*ss*ww], [2*ss*ww, 0]])
    frame_spin = z.Matrix([[0, -ww], [ww, 0]])
    checks['eigenframe_commutator_identity'] = z.simplify(
        (dD*D-D*dD)/(4*ss*ss)-frame_spin) == z.zeros(2)
    p = z.symbols('p', real=True)
    checks['projective_riccati_identity'] = z.simplify((ww-ss*p)-p*(ss-ww*p)-(ww*(1+p*p)-2*ss*p)) == 0
    # The cone signs are tested exactly at the rational certificate boundary.
    witness = {ss:F(9,10), ww:F(1,5), al:F(1,4)}
    checks['rational_upper_cone_points_inward'] = bool((ww*(1+al*al)-2*ss*al).subs(witness) < 0)
    checks['rational_lower_cone_points_inward'] = bool((-ww*(1+al*al)+2*ss*al).subs(witness) > 0)
    return checks, str(s2), str(w2)


def main():
    start = time.perf_counter()
    checks, s2, w2 = symbolic_checks()
    exact = cone_verifier([('1', '0')], '0', '0', '0', '0', '0', '1/4', '1')
    noisy = cone_verifier([('1', '1/10')], '1/20', '1', '1', '1/20', '1/20', '1/4', '17/20')
    boundary = cone_verifier([('1', '1')], '0', '0', '0', '0', '0', '3/4', '1/10')
    impossible = cone_verifier([('0', '0')], '0', '0', '0', '0', '0', '1/4', '1/10')
    checks.update({'exact_sol_certificate': exact['status'] == 'CERTIFIED',
                   'noise_budget_certificate': noisy['status'] == 'CERTIFIED',
                   'rotation_threshold_retains_unknown': boundary['status'] == 'UNKNOWN',
                   'shear_has_no_positive_certificate': impossible['status'] == 'UNKNOWN'})
    lo, hi = log_cat_bounds()
    checks['log_cat_enclosure_width'] = hi-lo < F(1, 10**20)
    fixtures = []
    for cc, uu, vv in [(1,0,0),(0,2,0),(1,3,0),(1,1,1),(0,1,1),(F(1,2),2,3)]:
        assert all(isinstance(x, (int,F)) for x in (cc,uu,vv))
        rate = (abs(F(cc))*lo, abs(F(cc))*hi)
        energy_factor = 4*F(cc)**2+F(uu)**2+F(vv)**2
        fixtures.append({'coefficients':list(map(str,(cc,uu,vv))),
                         'H_lower':str(rate[0]), 'H_upper':str(rate[1]),
                         'W_over_nu_V_a_squared':str(energy_factor)})
    result = {'status':'PASS' if all(checks.values()) else 'FAIL', 'checks':checks,
              'symbolic_s_squared':s2, 'symbolic_omega_squared':w2,
              'certificates':{'exact':exact,'noisy':noisy,'threshold':boundary,'shear':impossible},
              'cat_log':{'lower':str(lo),'upper':str(hi),'display_midpoint':float((lo+hi)/2)},
              'homogeneous_fixtures':fixtures, 'elapsed_seconds':time.perf_counter()-start,
              'limits':'Finite algebra and admitted verifier checks; not Pesin proof, a generic field compiler, or hardware power measurements.'}
    (ROOT/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','checks','elapsed_seconds']},indent=2))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
