"""Exact spherical-shell diagnostic and failed metal-to-filled-volume bridge.

Purely Ohmic homogeneous continuum material, chi=i/tau. Exact boundary
conditions derive the shell formula; the finite body/loss witness concerns
METAL volume. No physical thin-shell realization is claimed.
"""
from pathlib import Path
import json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1]

def main():
    start=time.monotonic();lam,tau=s.symbols('lambda tau',positive=True)
    gap=s.factor((lam+6*tau**2)/(lam**2+tau**2)-(6-9*lam))
    assert s.simplify(gap-lam*((3*lam-1)**2+9*tau**2)/(lam**2+tau**2))==0
    eps,phi=s.symbols('eps phi');B,C,D,d=s.symbols('B C D d')
    # Outer radius1, core volume fractionphi: phi=a^3. Outside potential
    # -r cos(theta)+d cos(theta)/r^2; shell -B r cos+C/r^2; core -D r cos.
    equations=[-1+d+B-C,-1-2*d-eps*(-B-2*C),-B+C/phi+D,eps*(-B-2*C/phi)+D]
    solution=s.solve(equations,[B,C,D,d],dict=True)[0]
    chi=s.symbols('chi');delta=s.symbols('delta',positive=True)
    expected=delta*chi*(3+2*chi)/(9+9*chi+2*delta*chi**2)
    assert s.factor(solution[d].subs({eps:1+chi,phi:1-delta})-expected)==0
    f=s.factor(expected.subs(chi,s.I/tau));real=s.simplify(s.re(f));imag=s.simplify(s.im(f))
    loss=s.factor(real+6*tau*imag)
    assert s.factor(s.limit(loss/delta,delta,0)-(13+18*tau**2)/(9+9*tau**2))==0
    cases=[]
    for de,ta in ((s.Rational(1,100),s.Rational(1,1000)),(s.Rational(1,10**6),s.Rational(1,100))):
        observed=s.factor(loss.subs({delta:de,tau:ta}));ratio=observed/de
        fake_void=s.factor(1-1/ratio);truth=1-de
        assert fake_void<truth
        cases.append({'metal_fraction':str(de),'tau':str(ta),'true_void_fraction':str(truth),
                      'loss_witness_over_9eps0Vouter':str(observed),
                      'mass_normalized_witness_over_solid_PEC_scale':str(ratio),
                      'invalid_filled_volume_inference':str(fake_void),
                      'display':[float(truth),float(ratio),float(fake_void)]})
    # Continuum counterfamily: solid unit-volume sphere plus a vanishing-
    # metal-volume closed spherical balloon connected by a smooth thin wire.
    # The rigorous finite-contrast continuity bound is proved separately.
    ta=s.Rational(1,100);b=1/ta;vs=s.Rational(1,10**12)
    base=s.factor(loss.subs({delta:1,tau:ta}))
    # Upper bound sqrt(vs/(1+vs)) <= sqrt(vs)=10^-6, entirely rational.
    upper=base+(1+6*ta)*b/s.Integer(10**6)
    acceptance=s.Rational(100,99);true_void_lower=(1-vs)/2
    assert upper<acceptance and true_void_lower>s.Rational(49,100)
    # An isolated-sphere sum is only a diagnostic approximation; the PDE
    # perturbation estimate, not this sum, establishes the connected limit.
    ds=s.Rational(1,10**8);sum_observed=(base+loss.subs({delta:ds,tau:ta}))/(1+ds)
    assert sum_observed<acceptance
    # Independently check the reciprocal perturbation identity on a general
    # symmetric two-site operator. No PDE or production verifier is imported.
    aa,cc,hh=s.symbols('aa cc hh')
    e0,e1,f0,f1=s.symbols('e0 e1 f0 f1')
    gamma=s.Matrix([[aa,hh],[hh,cc]])
    incident=s.Matrix([e0,e1]);test=s.Matrix([f0,f1])
    field=(s.eye(2)+chi*gamma).inv()*incident
    test_field=(s.eye(2)+chi*gamma).inv()*test
    p_background=s.Matrix([chi*e0/(1+chi*aa),0])
    background_added=e1-hh*p_background[0]
    delta_response=(test.T*(chi*field-p_background))[0]
    reciprocal_response=chi*test_field[1]*background_added
    assert s.factor(delta_response-reciprocal_response)==0
    real_gamma=s.Matrix([[s.Rational(1,3),s.Rational(1,9)],
                         [s.Rational(1,9),s.Rational(1,2)]])
    exact_operator=s.eye(2)+s.I*b*real_gamma
    gram_difference=exact_operator.conjugate().T*exact_operator-s.eye(2)-b**2*real_gamma**2
    assert gram_difference.applyfunc(s.simplify)==s.zeros(2)
    # The stronger theorem uses ||E_D||L2(S)<=||E_background||L2(S),
    # reciprocity, and the sphere bound3. It is linear in added metal volume.
    linear_vs=s.Rational(1,10**5)
    linear_upper=base+3*(1+6*ta)*b*linear_vs
    assert linear_upper<acceptance and (1-linear_vs)/2>s.Rational(49,100)
    out={'status':'VALID_METAL_VOLUME_WITNESS; FILLED_VOLUME_RESCUE_REFUTED',
      'spectral_scalar_nonnegative_gap':str(gap),'shell_response_factor':str(expected),
      'shell_loss_factor':str(loss),'shell_cases':cases,
      'continuum_connected_balloon':{'tau':str(ta),'added_metal_volume_over_ball':str(vs),
       'rigorous_normalized_response_upper':str(upper),'upper_float':float(upper),
       'one_percent_acceptance_threshold':str(acceptance),'true_void_fraction_lower':str(true_void_lower),
       'thin_shell_atomic_physical_qualification':'NOT_ACQUIRED; this is an unqualified smooth continuum family, not a practical powder counterexample'},
      'sharper_reciprocal_linear_bound':{
       'operator_norm_bound':'||delta_alpha||op <= 9 eps0 b V_added',
       'reciprocity_general_symmetric_two_site_identity':'PASS_EXACT',
       'pure_Ohmic_contraction_Gram_identity':'PASS_EXACT',
       'tau':str(ta),'added_metal_volume_over_ball':str(linear_vs),
       'rigorous_normalized_response_upper':str(linear_upper),
       'upper_float':float(linear_upper),
       'true_void_fraction_lower':str((1-linear_vs)/2),
       'physical_qualification':'NOT_ACQUIRED; constitutive law at atomic-scale thickness and actual powder conductivity/frequency remain unqualified'},
      'isolated_spheres_diagnostic_sum':float(sum_observed),
      'scope':'Exact Ohmic continuum algebra and finite-contrast perturbation-bound arithmetic. Spectral mass is conducting-material volume. No filled-volume/void certificate or apparatus is acquired.',
      'seconds':time.monotonic()-start}
    (ROOT/'results/shell_and_loss_witness.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
