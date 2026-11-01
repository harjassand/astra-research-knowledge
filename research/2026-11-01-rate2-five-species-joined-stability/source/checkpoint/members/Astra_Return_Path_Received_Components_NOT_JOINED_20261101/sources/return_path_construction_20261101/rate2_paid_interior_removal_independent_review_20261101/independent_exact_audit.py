#!/usr/bin/env python3
"""Independent exact audit. This supports, but does not replace, the proof receipt."""
from pathlib import Path
import hashlib
import itertools
import json
import sympy as S

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / 'rate2_paid_interior_removal' / 'PAID_INTERIOR_REMOVAL.md'
EXPECTED = 'a8e0bd383b053021f72e8197986581c87878046cdeaa7570536e44f5cf71a1cf'
A,B,C,D,E = S.symbols('A B C D E', nonnegative=True)
x = (A,B,C,D,E)
# Species order A,B,C,D,E; reactions reconstructed from the theorem's statement.
complexes = {'0': (0,0,0,0,0), 'A': (1,0,0,0,0),
             '2A': (2,0,0,0,0), 'AC': (1,0,1,0,0),
             'AD': (1,0,0,1,0), 'AE': (1,0,0,0,1),
             'CD': (0,0,1,1,0), 'AB': (1,1,0,0,0)}
rxns = [('2A','AC',1),('AC','2A',1),('2A','AD',1),('AD','2A',1),
        ('2A','AE',1),('AE','2A',1),('AE','CD',1),('CD','AE',2),
        ('CD','AB',1),('AB','CD',1)]
ports = [('0','A',1),('A','0',1)]

def nu(src,dst):
    return S.Matrix(complexes[dst])-S.Matrix(complexes[src])

def monomial(src, variables, falling=False):
    p = S.Integer(1)
    for v,k in zip(variables, complexes[src]):
        p *= S.prod(v-j for j in range(k)) if falling else v**k
    return p

def drift(reactions, variables, falling=False):
    d = S.zeros(5,1)
    for src,dst,k in reactions:
        d += k*monomial(src,variables,falling)*nu(src,dst)
    return d.applyfunc(S.expand)

def identically_zero(expr):
    return all(S.simplify(t)==0 for t in expr) if isinstance(expr,S.MatrixBase) else S.simplify(expr)==0

F = drift(rxns,x)
count_drift = drift(rxns+ports,x,True)
s = (S.sqrt(7)-1)/2
q = S.Matrix([1,s*s,s,s,2-s])*S.Rational(2,9)
comp = [(u,v,s if u=='2A' and v in ('AC','AD') else k) for u,v,k in rxns]+[('2A','CD',1-s)]
cb = {}
for y in ('2A','AC','AD','AE','CD','AB'):
    cb[y] = S.simplify(sum(k*monomial(u,q) for u,v,k in comp if v==y)-sum(k*monomial(u,q) for u,v,k in comp if u==y))

# Independent certificates of all five deterministic boundary-entry inequalities.
# Substitute 1=sum(x), avoiding numerical optimization over the simplex.
entry_residuals = [
    F[0]+3*A*sum(x)-3*C*D - A*(2*B+4*C+4*D+3*E),
    F[1]+B*sum(x)-(C*D+B*(B+C+D+E)),
    F[2]+3*C*sum(x)-(A*A+A*E+A*B+C*(2*A+3*B+3*C+3*E)),
    F[3]+3*D*sum(x)-(A*A+A*E+A*B+D*(2*A+3*B+3*D+3*E)),
    F[4]+2*E*sum(x)-(A*A+2*C*D+2*E*(B+C+D+E)),
]

J = F.jacobian(x)
row_max = [0]*5
for corner in itertools.product((0,2), repeat=5):
    jc = J.subs(dict(zip(x,corner)))
    row_max = [max(row_max[i],sum(abs(jc[i,j]) for j in range(5))) for i in range(5)]

checks = {
    'frozen_proof_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest()==EXPECTED,
    'exact_count_drift_correction': identically_zero(count_drift-F-S.Matrix([2*A+1,0,-A,-A,-A])),
    'count_total_drift_1_minus_A': identically_zero(sum(count_drift)-(1-A)),
    'homogeneous_internal_mass_conservation': identically_zero(sum(F)),
    'competitor_identical_homogeneous_field': identically_zero(drift(comp,x)-F),
    'all_competitor_complex_balances': all(v==0 for v in cb.values()),
    'q_has_unit_mass': identically_zero(sum(q)-1),
    'q_is_equilibrium': identically_zero(F.subs(dict(zip(x,q)))),
    'stoichiometric_rank_4': S.Matrix.hstack(*(nu(u,v) for u,v,k in rxns)).rank()==4,
    'all_actual_coordinate_jumps_at_most_1': all(abs(z)<=1 for u,v,k in rxns+ports for z in nu(u,v)),
    'entry_nonnegative_polynomial_certificates': all(identically_zero(v) for v in entry_residuals),
    'jacobian_linf_bound_40': max(row_max)<=40,
    's_in_4over5_5over6': S.Rational(13,5)**2<7<S.Rational(8,3)**2,
    's_squared_plus_s_three_halves': identically_zero(s*s+s-S.Rational(3,2)),
    'qmin_is_B': all(S.simplify(v-q[1])>=0 for v in q),
    'B_path_second_flux_exceeds_first_by_half_qA_squared': identically_zero(s*s-(1-s)-S.Rational(1,2)),
    'star_flux_sufficient_for_common_kappa': bool(2*s>1-s),
    'kappa_formula': identically_zero((1-s)*q[0]**2/24-(1-s)/486),
    'segment_positive_margin_without_decimal_approximations': S.Rational(3,4)-S.Rational(2,15)>S.Rational(1,2),
    'entropy_endpoint_margin': S.Rational(1,4)+S.Rational(2,15)==S.Rational(23,60)<S.Rational(1,2),
    'entropy_whole_window_margin': 1+S.Rational(2,15)==S.Rational(17,15)<2,
    'exp_three_halves_exceeds_four_by_positive_series': sum(S.Rational(3,2)**k/S.factorial(k) for k in range(4))>4,
    'service_n_over_eight': S.Rational(3,4)*S.Rational(1,6)==S.Rational(1,8),
    'service_four_units_n_over_two': 4*S.Rational(1,8)==S.Rational(1,2),
    'poisson_lower_tail_exponent_n_over_64': S.Rational(1,2)*S.Rational(1,4)**2/2==S.Rational(1,64),
    'immigration_chernoff_at_n512': 10-S.Rational(512,8)<=-S.Rational(512,64),
    'hit_plus_immigration_seven_eighths': S.Rational(3,4)+S.Rational(1,8)==S.Rational(7,8),
}
checks = {k: bool(v) for k,v in checks.items()}
result = {
    'status': 'PASS' if all(checks.values()) else 'FAIL',
    'scope': 'Exact symbolic/rational support only. Ordinary theorem review is in INDEPENDENT_REVIEW.md.',
    'target_sha256': EXPECTED,
    'checks': checks,
    'actual_count_drift': [str(v) for v in count_drift],
    'complex_balance_residuals': {k: str(v) for k,v in cb.items()},
    'jacobian_row_maxima': [int(v) for v in row_max],
    'not_numerically_evaluated': ['tau_epsilon','c_epsilon','n0_epsilon'],
}
(HERE/'independent_exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values()), checks
