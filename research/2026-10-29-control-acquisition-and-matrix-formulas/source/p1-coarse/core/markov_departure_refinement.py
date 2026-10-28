"""Reuse actual departure counts to improve the fixed-flag certificate."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from echo_compiler import sqrt_upper
from dissipation_noise import decode
from run_echo_experiment import dumpable


def bernoulli_interval(successes,trials,ell=F(10)):
    x=F(successes);n=F(trials)
    lo=max(F(0),(x-sqrt_upper(2*ell*x))/n)
    hi=min(F(1),(x+ell+sqrt_upper(ell*ell+2*ell*x))/n)
    return lo,hi


def run():
    root=Path(__file__).resolve().parents[1]
    path=root/'results'/'MARKOV_RESIDUAL_EVENTS.json'
    data=decode(json.loads(path.read_text()))
    tail=data['tail_weight'];receipts=[]
    for old in data['receipts']:
        flag=old['flag'];n=flag['trials'];depart=flag['first_step_departures']
        q=F(depart,n);t=1-q
        lo,hi=bernoulli_interval(depart,n)
        delta=max(q-lo,hi-q)
        q_upper=(sqrt_upper(old['galerkin_inverse_dissipation_upper'])+delta*sqrt_upper(tail))**2
        loss=1-t*t
        assert old['checker_actual_proposed_form']<=q_upper
        true_t=data['source_family_checker_only'][old['primitive']][0][0]
        assert abs(true_t-t)<=delta
        receipts.append({'primitive':old['primitive'],'model':t,
                         'escape_probability_interval':[lo,hi],
                         'model_error_radius':delta,'weighted_residual_upper':q_upper,
                         'theta_squared':q_upper/loss,'correction_noise_zeta':delta/loss})
    total=2*max(x['theta_squared'] for x in receipts)+max(x['correction_noise_zeta'] for x in receipts)
    result={'source_receipt_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'new_source_queries':0,'confidence_budget_unchanged':True,
            'false_certificate_probability_at_most':F(1,1000),
            'receipts':receipts,'uniform_all_word_amplitude_bound':total,
            'original_hoeffding_bound':data['uniform_all_word_amplitude_bound'],
            'total_primitive_applications':data['total_primitive_applications'],
            'total_resets':data['total_resets'],
            'total_resets_scope':'Conservative fresh reset for every logical trial in the original receipt',
            'known_boundary_reuse_reset_upper':sum(1+r['flag']['first_step_departures']-r['flag']['successes'] for r in data['receipts']),
            'known_boundary_reuse_premise':'A confirmed physical Markov state b is a valid start for the next trial; the nonintrusive predicate leaves it unchanged.',
            'total_membership_bit_observations':data['total_membership_bit_observations'],
            'all_exact_checks_passed':True}
    (root/'results'/'MARKOV_DEPARTURE_REFINEMENT.json').write_text(json.dumps(dumpable(result),indent=2)+'\n')
    print('all-word bound',float(total),'operations',result['total_primitive_applications'],'new source queries',0)


if __name__=='__main__':run()
