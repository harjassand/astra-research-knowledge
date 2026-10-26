"""Precision-optimal experiment after an acquired rank-one symmetric posterior.
Exact rational measurements, bounds and finite-source distinguishability control.
"""
import json
from pathlib import Path
import sympy as sp
from acquired_latent_controller_compiler import (S,SL,R,t,e0,e2,
    compile_term,frac,candidate_root_intervals)

true_t=R(7,4)
eta=R(1,100)
true_S=S.subs(t,true_t)


def value_range(expr,lo,hi):
    assert 1<=lo<=hi<=3
    vals=[sp.factor(expr.subs(t,lo)),sp.factor(expr.subs(t,hi))]
    # Exact stationary roots if rational; otherwise a certified outward
    # interval using a global derivative bound is necessary. This control
    # has a single rational critical point (2) outside all narrow domains.
    for a,b,m in candidate_root_intervals(expr):
        if lo<=a and b<=hi:
            assert a==b, 'Unresolved algebraic root: return outer interval instead'
            vals.append(sp.factor(expr.subs(t,a)))
        elif a<hi and b>lo:
            raise AssertionError('Stationary root isolation overlaps interval boundary')
    return (min(vals),max(vals))


def one_trial(q,noise):
    assert (q.T*q)[0]<=1
    assert (noise.T*noise)[0]<=eta**2
    measured=true_S*q+noise
    baseline=SL*q
    c=(e2.T*q)[0]
    if c==0:lo,hi=R(1),R(3)
    else:
        # v^T (measured - SL q)= (t-1)c + v^T noise, with
        # |v^T noise|<=eta. This is an exact set-membership interval.
        center=1+(e2.T*(measured-baseline))[0]/c
        lo=max(R(1),center-eta/abs(c))
        hi=min(R(3),center+eta/abs(c))
        assert lo<=true_t<=hi
    return dict(input=[frac(y) for y in q],reported_output=[frac(y) for y in measured],
                actual_added_error=[frac(y) for y in noise],
                excitation=frac(abs(c)),
                certified_latent_interval=[frac(lo),frac(hi)],
                posterior_latent_width=frac(hi-lo),
                posterior_latent_error_radius=frac((hi-lo)/2)),lo,hi


def main():
    q1=compile_term(1,e2,e2)['expr'];q2=compile_term(2,e2,e2)['expr']
    task=sp.factor(q1-R(49,16)*q2)
    plans={
      'optimal_unit_probe_e2':e2,
      'mixed_half_probe':(e0+e2)/2,
      'uninformative_probe_e0':e0,
    }
    trials={}
    for key,q in plans.items():
        # deliberately nonzero, correlated direction of instrument error
        observation,lo,hi=one_trial(q,eta*e2/3)
        low,high=value_range(task,lo,hi)
        observation.update(portfolio_certified_range=[frac(low),frac(high)],
                           portfolio_width=frac(high-low),
                           source_aware_portfolio_value=frac(task.subs(t,true_t)),
                           future_new_source_calls=0,
                           added_source_calls_for_strategy=1)
        trials[key]=observation
    optimal_w=R(trials['optimal_unit_probe_e2']['posterior_latent_width'])
    mixed_w=R(trials['mixed_half_probe']['posterior_latent_width'])
    assert mixed_w==2*optimal_w
    assert R(trials['uninformative_probe_e0']['posterior_latent_width'])==2
    # Independent exact source pair producing same new reading at q=e2
    # with bounded adversarial errors ±eta e2 at the midpoint.
    source_low=true_t-eta
    source_high=true_t+eta
    q=e2
    center=(S.subs(t,true_t)*q)
    e_low=center-S.subs(t,source_low)*q
    e_high=center-S.subs(t,source_high)*q
    assert (e_low.T*e_low)[0]==eta**2
    assert (e_high.T*e_high)[0]==eta**2
    assert e_low==-e_high
    result=dict(declared_contract=dict(spectral='I <= S <= 3I',
                 historical_first_action='exact',additional_action_error='Euclidean norm <= 1/100',
                 native_unit_input='||q||_2 <= 1',error_kind='adversarial, may be correlated across calls'),
                alternative_one_call_strategies=trials,
                lower_bound_witness=dict(source_parameters=[frac(source_low),frac(source_high)],
                                         identical_reported_vector=[frac(y) for y in center],
                                         compatible_errors=[[frac(y) for y in e_low],[frac(y) for y in e_high]],
                                         minimax_unavoidable_latent_estimation_error=frac(eta)),
                general_theorem='For rank-one S(t)=SL+(t-t0)vv^T, ||v||=1, a native vector reading with ||q||<=1 and ||error||<=eta has sharp interior latent radius eta/|v^T q|. q=v minimizes the radius for all later operations simultaneously; a pair of compatible sources attains the lower bound.',
                total_source_call_costs='One common old exact source call, plus one new synthetic native call for each of three independently compared strategies. The results are not pooled across strategies.')
    path=Path(__file__).with_name('active_latent_precision_results.json')
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASSED precision-optimal latent experiment; active portfolios:')
    for k,item in trials.items():print(k,'latent width',item['posterior_latent_width'],'task width',item['portfolio_width'])
    print('PASSED exact indistinguishability pair')

if __name__=='__main__':main()
