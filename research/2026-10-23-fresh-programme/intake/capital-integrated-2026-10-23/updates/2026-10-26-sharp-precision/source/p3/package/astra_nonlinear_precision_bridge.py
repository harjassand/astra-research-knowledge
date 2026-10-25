"""ASTRA Pro3: nonlinear-forward-to-symmetric-response precision compiler.

Conditional theorem: if F is C^3 on every allowed +/-h q segment,
||D^3 F(z)[q,q,q]||_2 <= M3 for ||q||_2<=1, and each forward
measurement error <=delta, then two evaluations give an approximate
DF(x)q action of error <= M3*h^2/6 + delta/h. The old sharp spectral
compiler can consume these certified actions, but its optimality applies
to its abstract response/noise class, NOT all nonlinear source interfaces.

This script checks an n=6 exact-rational nonlinear potential-gradient
source and independently exhibits a smooth strongly convex finite-history
counterexample to inferring a local Hessian from any finite old record.
No physical experiment, source contract acquisition, or historical helper.
"""
from __future__ import annotations
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parent


def simp(x):
    return x.applyfunc(sp.simplify) if isinstance(x,sp.MatrixBase) else sp.simplify(x)


def enc(obj):
    if isinstance(obj,sp.MatrixBase):
        return [[str(simp(obj[i,j])) for j in range(obj.cols)] for i in range(obj.rows)]
    if isinstance(obj,sp.Basic):
        return str(simp(obj))
    if isinstance(obj,dict):
        return {str(k):enc(v) for k,v in obj.items()}
    if isinstance(obj,(tuple,list)):
        return [enc(v) for v in obj]
    return obj


def householder(n):
    P=sp.eye(n)
    for signs in ([1,2,1,3,-1,2],[-2,1,3,1,2,-1]):
        v=sp.Matrix(signs)
        H=sp.eye(n)-2*v*v.T/(v.T*v)[0]
        P=simp(P*H)
    assert simp(P.T*P)==sp.eye(n)
    return P


def nonlinear_forward_control():
    n=6
    P=householder(n)
    eye=sp.eye(n)
    T=simp(P*sp.diag(144,9,-25,-16,0,0)*P.T)
    q1=P*(12*eye[:,0]+5*eye[:,2])/13
    y1=P*(13*(12*eye[:,0]-5*eye[:,2]))
    q2=P*(3*eye[:,1]+4*eye[:,3])/5
    y2=P*(5*(3*eye[:,1]-4*eye[:,3]))
    probes=[simp(q1),simp(q2)]
    decoders=[simp(y1),simp(y2)]
    assert all(simp(q.dot(q))==1 for q in probes)
    assert simp(sum([(q*y.T+y*q.T)/2 for q,y in zip(probes,decoders)],sp.zeros(n))-T)==sp.zeros(n)
    assert [simp(sp.sqrt(y.dot(y))) for y in decoders]==[169,25]
    # Private source coefficients; the learner receives only the public bound,
    # forward observations, chosen probes, bias and target.
    B=sp.Matrix([
      [0,1,-2,0,0,1],
      [1,0,1,-1,0,0],
      [-2,1,0,1,0,-1],
      [0,-1,1,0,1,0],
      [0,0,0,1,0,-1],
      [1,0,-1,0,-1,0]])
    assert B==B.T
    S=2*eye+B/40
    R=sp.Rational(1,4)
    max_abs_row=max(sum(abs(B[i,j]) for j in range(n)) for i in range(n))/40
    assert max_abs_row<=R
    alpha_true=sp.Rational(3,20)
    alpha_bound=sp.Rational(1,5)
    assert alpha_true<=alpha_bound
    M3=6*alpha_bound
    # Exact nonlinear potential gradient F(u) = S u + alpha_true * u_i^3.
    # Its unknown differential at zero is S and ||D^3 F[q,q,q]||
    # <=6 alpha_true ||q||^3 for ||q||<=1.
    def forward(u):
        return S*u+alpha_true*u.applyfunc(lambda a:a**3)
    delta=sp.Rational(1,10**6)
    h=sp.Rational(7,500)
    hmax=sp.Rational(1,10)
    assert 0<h<hmax
    eta=simp(M3*h*h/6+delta/h)
    eta_actual_conservative=simp(alpha_true*h*h+delta/h)
    assert eta_actual_conservative<=eta<R
    # Theoretical best h in (0,hmax] is (3delta/M3)^(1/3).
    h_star=(3*delta/M3)**sp.Rational(1,3)
    assert float(h_star)<float(hmax)
    eta_at_opt=float(M3*h_star*h_star/6+delta/h_star)
    observed=[];forward_inputs=[];forward_centers=[];noise_vectors=[]
    action_errors=[]
    for j,q in enumerate(probes):
        xp=h*q;xm=-h*q
        eplus=delta*eye[:,j]
        eminus=-delta*eye[:,j]
        rp=forward(xp)+eplus
        rm=forward(xm)+eminus
        y=simp((rp-rm)/(2*h))
        true_action=S*q
        action_error=simp(y-true_action)
        # Certified by exact squared norm, no untrusted numerical eigenvalue.
        assert simp(action_error.dot(action_error)-eta*eta)<=0
        assert simp(eplus.dot(eplus))==delta*delta
        assert simp(eminus.dot(eminus))==delta*delta
        observed.append(y);forward_inputs.extend([xp,xm]);forward_centers.extend([rp,rm]);
        noise_vectors.extend([eplus,eminus]);action_errors.append(action_error)
    S0=2*eye
    reference=simp(sp.trace(T*S))
    estimate=simp(sp.trace(T*S0)+sum((y.T*(z-S0*q))[0] for q,y,z in zip(probes,decoders,observed)))
    guaranteed_radius=simp(eta*sum(sp.sqrt(y.dot(y)) for y in decoders))
    assert simp(abs(estimate-reference)-guaranteed_radius)<=0
    baseline_radius=simp(R*194)
    one_query_upper=simp(R*25+eta*169)
    assert guaranteed_radius<sp.Rational(3,100)
    assert one_query_upper>sp.Rational(3,100)
    return dict(source_type='Unknown gradient of strongly convex quartic potential, evaluated as a nonlinear forward map',
        source_gradient_formula_checker='F(u)=Su+alpha*u_i^3, private S and alpha',
        hidden_S=S,hidden_alpha=alpha_true,known_contract_center=S0,
        known_contract_operator_radius=R,known_third_derivative_bound=M3,
        instrument_forward_error_delta=delta,
        chosen_rational_step_h=h,maximum_step_h=hmax,
        theoretical_continuous_optimum_step=h_star,
        theoretical_min_action_error_float=eta_at_opt,
        certified_effective_vector_action_error_eta=eta,
        task_T=T,late_experiment_inputs=sp.Matrix.hstack(*probes),
        native_forward_inputs=sp.Matrix.hstack(*forward_inputs),
        actually_returned_noisy_forward_vectors=sp.Matrix.hstack(*forward_centers),
        injected_bounded_forward_errors=sp.Matrix.hstack(*noise_vectors),
        compiled_action_decoders=sp.Matrix.hstack(*decoders),
        compiled_action_results=sp.Matrix.hstack(*observed),
        actual_action_errors=sp.Matrix.hstack(*action_errors),
        actual_reference_target=reference,learner_task_estimate=estimate,
        observed_absolute_task_error=abs(estimate-reference),
        certified_absolute_task_error=guaranteed_radius,
        prior_only_error=baseline_radius,one_action_error_bound=one_query_upper,
        requested_task_tolerance=sp.Rational(3,100),
        min_certified_vector_actions_in_declared_spectral_compiler=2,
        new_native_forward_calls=4,return_width_per_forward_call=n,
        returned_native_scalars=4*n,
        conventional_full_n_column_central_differences_forward_calls=2*n,
        exact_calibration_calls_for_third_derivative_or_spectral_bounds=0,
        remark='A sufficient accuracy result for this nonlinear native interface; not a global minimax claim among all algorithms interacting directly with nonlinear F.')


def smooth_history_obstruction():
    # The smooth counterexample is not a single analytic polynomial globally:
    # it is a C^5 piecewise polynomial compactly supported potential bump.
    # It defeats learning local curvature from a finite set of gradient values,
    # even when an old source record includes the requested bias itself.
    z,t=sp.symbols('z t',real=True)
    xstar=sp.Rational(1,2);radius=sp.Rational(1,8)
    f=z*z*(1-z*z)**6/2
    f2=simp(sp.diff(f,z,2))
    C=sum(abs(c) for c in sp.Poly(f2,z).all_coeffs())
    assert C==1984
    gamma=sp.Rational(1,1024)
    lam=sp.Rational(2)
    assert lam-gamma*C>0
    # For |z|<=1 we have |f''(z)| <= coefficient l1 norm C,
    # so 0 < lambda-gamma C <= Phi1'' <= lambda+gamma C.
    perturb=gamma*radius**2*f.subs(z,(t-xstar)/radius)
    phi0=lam*t*t/2
    phi1_inside=simp(phi0+perturb)
    F0=simp(sp.diff(phi0,t)); F1_inside=simp(sp.diff(phi1_inside,t))
    observed_inputs=[-2,-1,0,sp.Rational(1,2),1,2]
    old_record=[]
    for x in observed_inputs:
        inside=abs(x-xstar)<radius
        f0val=simp(F0.subs(t,x))
        f1val=simp(F1_inside.subs(t,x)) if inside else f0val
        assert f0val==f1val
        old_record.append(dict(input=x,source0_value=f0val,source1_value=f1val))
    dF0=simp(sp.diff(F0,t).subs(t,xstar))
    dF1=simp(sp.diff(F1_inside,t).subs(t,xstar))
    assert dF1-dF0==gamma
    # The source1 potential is equal to phi0 outside support. Its perturbation
    # and first five derivatives vanish at the boundary because (1-z^2)^6.
    boundary_vanishing=[simp(sp.diff(f,z,k).subs(z,1)) for k in range(6)]
    assert all(v==0 for v in boundary_vanishing)
    return dict(native_interface='pointwise gradient value of a C5 strongly convex potential',
        source0_potential_outside_and_inside=phi0,
        source1_potential_inside_support=phi1_inside,
        source1_potential_outside_support=phi0,
        bump_center=xstar,bump_radius=radius,
        support='open interval centered at xstar; zero elsewhere',
        bump_shape=f,rigorous_derivative_coefficient_bound=C,
        convexity_lower_bound=lam-gamma*C,
        convexity_upper_bound=lam+gamma*C,
        historical_response_pairs=old_record,
        old_reference_call_at_future_bias_is_present=True,
        source0_local_derivative=dF0,
        source1_local_derivative=dF1,
        unidentifiable_local_derivative_gap=gamma,
        argument='For any finite old input list, shrink bump support below the closest nonzero separation from the future bias. Convexity follows for suitably small gamma. Two smooth positive-gradient sources then match every old response but have different late local derivatives.',
        contract_boundary='A supplied uniform higher-derivative bound can restrict the bump amplitude as its support shrinks. The finite old records alone do not establish such a bound.')


def main():
    results=dict(nonlinear_forward_experiment=nonlinear_forward_control(),
                 finite_history_hessian_nonidentifiability=smooth_history_obstruction(),
                 interpretation='Synthesized later native nonlinear forward experiments from a new task, conditional smoothness/spectral/error contracts; analytically indistinguishable convex alternative sources prohibit unconstrained historic derivative extrapolation. Neither experiment measures a physical system.')
    output=ROOT/'astra_nonlinear_precision_bridge_results.json'
    output.write_text(json.dumps(enc(results),indent=2))
    p=results['nonlinear_forward_experiment']
    print('Chosen central difference h',float(p['chosen_rational_step_h']),
          'theoretical best h',float(p['theoretical_continuous_optimum_step']))
    print('effective response error',float(p['certified_effective_vector_action_error_eta']))
    print('late task bound',float(p['certified_absolute_task_error']),
          'observed error',float(p['observed_absolute_task_error']))
    print('native forward source calls',p['new_native_forward_calls'],
          'vs n-column finite differencing',p['conventional_full_n_column_central_differences_forward_calls'])
    print('two-source derivative gap',float(results['finite_history_hessian_nonidentifiability']['unidentifiable_local_derivative_gap']))
    print('results',output)

if __name__=='__main__':main()
