"""Compatible finite-pitch piezoelectric gate: exact rational checks.

No material fit, atomistic calculation, acquired measurement or physical test.
The universal derivation is in COMPATIBLE_PIEZO_GATE.txt. This dependency-free
script checks elastic coefficients exactly and supplies an exact toy witness.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import math

OUT = Path(__file__).resolve().parent
SNAP = OUT.parent/'source_snapshot'
revision = '0451552424b4679fa9a73faf5849ea5a4af21cf6'

def reduced_parameters(C, KE, Cp, theta, alpha):
    KD = KE+theta*theta/Cp
    Ce = Cp+theta*theta/(C+KE)
    Theta = theta*C*alpha/(C+KE)
    u0 = 2*alpha*alpha*C*KE/(C+KE)
    U = 2*Theta*Theta/Ce
    uD = 2*alpha*alpha*C*KD/(C+KD)
    A = C+KD
    # Independent coefficients of r^2, rz and z^2 after minimizing strain.
    direct = [C*alpha*alpha/2-(C*alpha)**2/(2*A),
              -C*alpha*theta/(Cp*A),
              1/(2*Cp)-theta*theta/(2*Cp*Cp*A)]
    completed_square = [u0/4+Theta*Theta/(2*Ce),-Theta/Ce,1/(2*Ce)]
    assert direct == completed_square
    assert uD-u0 == U
    return dict(KD=KD,Ceff=Ce,Theta=Theta,u0=u0,U=U,uD=uD)

check_cases = [list(map(F,x)) for x in [
    (1,1,1,1,1),(2,3,5,7,11),(7,5,3,2,1),(3,2,7,5,4),
    (F(1,7),F(2,5),F(3,4),F(5,3),F(7,2)),
]]
for case in check_cases:
    reduced_parameters(*case)

# Reset polynomial coefficients in variables M2 and mean(q). Both signs.
for u in (F(2,3),F(7,5)):
    for B in (F(1,2),F(5,3)):
        for frac in (F(0),F(2,5),F(1)):
            for sign in (-1,1):
                direct = [u/4,-u*frac*B*B/2,-u*(1-frac)*sign*B**3,
                          u*(frac*frac-(1-frac)**2)*B**4/4+u*(1-frac)*B**4]
                square = [u/4,-u*B*B/2+u*(1-frac)*B*B/2,
                          -u*(1-frac)*sign*B**3,
                          u*B**4/4+u*(1-frac)*B**4/2]
                assert direct == square

# All numbers below are declared dimensionless, compatible synthetic constants.
C,KE,Cp,theta,alpha = F(1),F(1,5),F(5),F(2),F(1)
p = reduced_parameters(C,KE,Cp,theta,alpha)
bm,c,kappa = F(1),F(1),F(1)
b = bm-p['u0']
a = 3*b*b/(16*c)
B2 = 3*b/(4*c)
lam = F(9,20)*bm*bm/c-a
mu = a-F(9,20)*max(b-p['U'],F(0))**2/c
pitch_sufficient = math.pi*math.sqrt(float(kappa/lam))
ell_good = F(4)
gamma_good = float(kappa)*math.pi**2/float(ell_good**2)-float(lam)
assert gamma_good>0

# q(x)=p0+A cos(pi x/ell), p0^2=1/5, A=1/10, ell=10.
# The energy is averaged analytically using the exact cosine moments.
p2,Amp,ell_bad = F(1,5),F(1,10),F(10)
lambda_trans = a-(3*bm-p['uD'])*p2+5*c*p2*p2
quartic = Amp**4*(-3*bm/32+p['uD']/16+15*c*p2/16)
sextic = 5*c*Amp**6/96
gap_constant = Amp**2*lambda_trans/4+quartic+sextic
gap_pi2 = Amp**2*kappa/(4*ell_bad**2)
gap_per_length = float(gap_constant)+float(gap_pi2)*math.pi**2
gap_upper_rational = gap_constant+10*gap_pi2  # pi^2 < 10.
assert gap_upper_rational<0

WB = p['U']*B2*B2/4
zB = p['Theta']*B2
Vpeak = zB/p['Ceff']
assert p['Ceff']*Vpeak*Vpeak/2 == WB

sources = [
 'frontier/dossiers/N805.txt','frontier/dossiers/N777.txt',
 'updates/FI/package/barrier/README.md',
 'updates/FI/synthesis/barrier/DERIVATIONS.md',
 'updates/FI/synthesis/root/MIXED_COMPLIANCE_GATE_THEOREM.md',
 'updates/FI/synthesis/barrier/DELTA_MIXED_GATE_AUDIT.md',
]
source_hashes={path:hashlib.sha256((SNAP/path).read_bytes()).hexdigest() for path in sources}
exact = lambda value:{'exact':str(value),'float':float(value)}
result={
 'status':'MODEL THEOREM AND SYNTHETIC COUNTEREXAMPLE; NOT MATERIAL PERFORMANCE',
 'corpus_revision':revision,'source_sha256':source_hashes,
 'verification':{
   'universal_proof':'Analytical proof in COMPATIBLE_PIEZO_GATE.txt; finite checks are not a universal proof.',
   'exact_elastic_coefficient_and_range_checks':len(check_cases),
   'exact_spatial_reset_coefficient_checks':24,
   'additional_dependency_installations':0,
 },
 'synthetic_compatible_example':{
   'C':1,'alpha':1,'KE':'1/5','Cp':5,'theta':2,
   **{key:exact(value) for key,value in p.items()},
   'intrinsic_bm':1,'homogeneous_short_b':exact(b),'a':exact(a),'c':1,'kappa':1,
   'qB_squared':exact(B2),'lambda_m':exact(lam),'mu':exact(mu),
   'sufficient_pitch_strictly_less_than':pitch_sufficient,
   'chosen_good_pitch':4,'variance_margin_at_good_pitch':gamma_good,
   'global_path_quadratic_growth_margin':min(float(mu),gamma_good),
   'charge_swing_zB':exact(zB),'maximum_quasistatic_piezo_voltage':exact(Vpeak),
   'circulated_engagement_work_per_volume':exact(WB),
   'same_initial_final_actuator_state_for_polarity_inversion':True,
   'material_parameter_certification':'UNKNOWN',
 },
 'explicit_spatial_failure_at_pitch_10':{
   'selected_q_squared':exact(p2),'perturbation_amplitude':exact(Amp),
   'zero_mean_mode_curvature_without_gradient':exact(lambda_trans),
   'with_gradient':float(lambda_trans)+float(kappa/ell_bad**2)*math.pi**2,
   'energy_gap_per_length':gap_per_length,
   'energy_gap_exact_form':str(gap_constant)+' + ('+str(gap_pi2)+')*pi^2',
   'strict_rational_upper_bound_using_pi_squared_less_than_10':exact(gap_upper_rational),
   'meaning':'Scalar homogeneous curvature stays positive; a compatible nonuniform spatial mode lowers energy.',
 },
 'finite_time_contract':{
   'electrical_reset_resistive_loss_lower_bound':'R_e*(Delta z)^2/T for each charge stroke',
   'relative_to_circulated_work':'at least 2*(R_e*Ceff)/T',
   'direct_passive_RC_reset_heat':'equals circulated work in complete relaxation; residual remains at every finite time',
   'quasistatic_warning':'Static elastic elimination does not eliminate bulk inertia or the longest acoustic mode.',
   'finite_temperature_retention':'UNKNOWN; restored controls do not provide a pure Gibbs endpoint.',
 },
 'receipts':{'new_workers':0,'actual_model_token_billing':'UNKNOWN'},
}
(OUT/'compatible_gate_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
