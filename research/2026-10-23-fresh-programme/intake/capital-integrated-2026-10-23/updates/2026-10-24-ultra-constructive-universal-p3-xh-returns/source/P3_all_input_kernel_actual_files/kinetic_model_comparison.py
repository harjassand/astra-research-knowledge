"""New certified comparison of specified post-preparation kinetic models.

Both hypotheses begin from the SAME acquired correlated entrance.  The second
changes silent exchange after that preparation.  Its stationary active
fractions and long-run turnover rates match the first model exactly, while
turnover fluctuations and transient dynamics differ.  This is a supplied
synthetic model-comparison calculation, not identification of real chemistry.

The baseline count calculation is read from its retained outputs.  Only the
new hypothesis is propagated.  Common-entrance normalization cancels in the
Bayes factor; the entrance projective spread is charged once, not squared.
"""

from dataclasses import replace
from fractions import Fraction as F
from pathlib import Path
import json
import time

from pro3_gate_experiment import I, D
from tensor_separator_entrance import BinaryModule
from tensor_reuse_entrance import load_acquired_action
from source_interface_compiler import star_source, with_product_mixture_initial
from conditioned_count_queries import update_count_record, tv_from_spread, future_queries


def recover_retained_mass(reported,entrance_spread,numerical_spread):
    """Invert the KNOWN reporting formula, not a generic likelihood bound.

    The retained executors reported directed roundings of m/R and m*R*C,
    where m is their exact lower-filter mass.  That computational provenance
    gives the tight enclosure below without repeating either count filter.
    """
    if entrance_spread<1 or numerical_spread<1:
        raise ValueError('Projective and numerical spreads must be at least one')
    reported_lo,reported_hi=map(F,reported)
    lo=reported_lo*entrance_spread
    hi=reported_hi/(entrance_spread*numerical_spread)
    if not 0<lo<=hi:
        raise ValueError('Inconsistent retained lower-filter mass enclosure')
    return lo,hi


def define_joint_approximation(entrance_spread,baseline_mass,changed_mass,
                               baseline_numerical_spread,changed_numerical_spread):
    """Retain an explicit equal-prior joint model/state probability law.

    Each conditional state law is already an exact rational product mixture.
    Choose the LOWER rational endpoint of each mass enclosure as its joint
    coefficient.  If the unknown retained mass m_j lies in [l_j,u_j], then
    its unnormalized numerical branch lies between l_j*Q_j and u_j*Q_j.
    Thus the joint spread is R*max_j(C_j*u_j/l_j).  Model weights are serialized
    as exact fractions, so their additional rounding spread is exactly one.
    """
    intervals=(tuple(map(F,baseline_mass)),tuple(map(F,changed_mass)))
    numerical=(F(baseline_numerical_spread),F(changed_numerical_spread))
    if entrance_spread<1 or any(c<1 for c in numerical):
        raise ValueError('Invalid projective spread')
    if any(not 0<lo<=hi for lo,hi in intervals):
        raise ValueError('Invalid branch coefficient enclosure')
    coefficients=[lo for lo,_ in intervals]
    coefficient_spreads=[hi/lo for lo,hi in intervals]
    mass=sum(coefficients,F(0))
    model_weights=[coefficient/mass for coefficient in coefficients]
    assert sum(model_weights,F(0))==1
    joint_spread=entrance_spread*max(c*d for c,d in zip(numerical,coefficient_spreads))
    return {
        'scientific_object':'specified joint posterior approximation over model label and hidden state',
        'model_order':['baseline','changed'],
        'model_prior_exact':['1/2','1/2'],
        'exact_rational_model_weights':[str(w) for w in model_weights],
        'conditional_state_posterior_files':['conditioned_count_posterior_24sites.json',
                                           'fast_exchange_count_posterior_24sites.json'],
        'joint_law_definition':'model weight times the exact retained conditional-state law in the corresponding file',
        'coefficient_selection':'exact rational lower endpoint of each retained lower-filter mass enclosure',
        'selected_unnormalized_coefficients_exact':[str(x) for x in coefficients],
        'retained_lower_filter_mass_intervals_exact':[[str(x) for x in interval] for interval in intervals],
        'coefficient_enclosure_spreads_exact':[str(x) for x in coefficient_spreads],
        'serialized_model_weight_rounding_spread_exact':'1',
        'normalization_checked_exactly':True,
        'joint_projective_spread_upper_exact':str(joint_spread),
        'whole_joint_posterior_TV_upper':str(tv_from_spread(joint_spread)),
        'certificate_scope':'equal model priors and a common prepared entrance; source spread charged once; local numerical spread and both retained coefficient uncertainties included'
    }


def refresh_retained_joint_certificate():
    """Attach the explicit joint law using only already retained calculations."""
    result_path=Path('kinetic_model_comparison_results.json')
    result=json.loads(result_path.read_text())
    entrance=json.loads(Path('relative_correlated_entrance_24sites.json').read_text())
    baseline=json.loads(Path('conditioned_count_queries_results.json').read_text())
    baseline_posterior=json.loads(Path('conditioned_count_posterior_24sites.json').read_text())
    changed_posterior=json.loads(Path('fast_exchange_count_posterior_24sites.json').read_text())
    spread=F(entrance['relative_projective_certificate']['spread_factor_upper_exact'])
    base_numerical=F(baseline_posterior['projective_spread_upper_exact'])/spread
    changed_numerical=F(changed_posterior['projective_spread_upper_exact'])/spread
    base_mass=recover_retained_mass(baseline['full_record_probability_interval'],spread,base_numerical)
    if 'record_lower_mixture_mass_exact' in changed_posterior:
        value=F(changed_posterior['record_lower_mixture_mass_exact'])
        changed_mass=(value,value)
    else:
        changed_mass=recover_retained_mass(result['changed_model_record_probability_interval'],
                                          spread,changed_numerical)
    if F(result['speed_factor'])!=F(changed_posterior['kinetic_speed_factor']):
        raise ValueError('Retained comparison and changed-model posterior do not match')
    joint=define_joint_approximation(spread,base_mass,changed_mass,base_numerical,changed_numerical)
    result['joint_model_and_state_approximation']=joint
    result['joint_model_and_state_posterior_TV_upper']=joint['whole_joint_posterior_TV_upper']
    result['joint_certificate_attached_without_source_or_filter_recomputation']=True
    result_path.write_text(json.dumps(result,indent=2))
    return joint


def acquire_future_hypothesis(modules,weights,probabilities,speed):
    source=star_source(len(modules))
    rules=[]
    for rule in source.rules:
        if rule.name.startswith('up_'):
            i=int(rule.name.split('_')[1])
            rule=replace(rule,rate=speed*modules[i].alpha)
        elif rule.name.startswith('down_'):
            i=int(rule.name.split('_')[1])
            module=modules[i]
            rule=replace(rule,rate=speed*(module.beta+module.kappa)-module.kappa)
        rules.append(rule)
    source=replace(source,rules=tuple(rules))
    _,compiled=with_product_mixture_initial(source,weights,probabilities,((0,1),))
    obtained=[]
    for i,component in enumerate(compiled.components):
        assert component.sites==(i+1,) and component.generators[0]==component.generators[1]
        q=component.generators[1]
        events=[event for event in compiled.events if event.owner==i]
        assert len(events)==1
        obtained.append(BinaryModule(q[0][1],q[1][0],events[0].hazards[1][1]))
    identities=[]
    for before,after in zip(modules,obtained):
        r=before.alpha+before.beta+before.kappa
        rs=after.alpha+after.beta+after.kappa
        occupancy=before.alpha/r; flux=before.kappa*occupancy
        assert after.alpha/rs==occupancy
        assert after.kappa*after.alpha/rs==flux
        assert rs==speed*r
        # Interevent times reset to state0.  Their SCV distinguishes speed.
        scv=1-2*before.alpha*before.kappa/r**2
        scv_fast=1-2*after.alpha*after.kappa/rs**2
        identities.append({'stationary_active_fraction_exact':str(occupancy),
            'stationary_turnover_rate_exact':str(flux),
            'baseline_interevent_SCV_exact':str(scv),
            'changed_interevent_SCV_exact':str(scv_fast)})
    return obtained,identities,{'rules':len(source.rules),
        'components':len(compiled.components),'initial_positive_mixture_components':len(compiled.initial),
        'controller_initially_open':all(branch.controller_state==1 for branch in compiled.initial),
        'source_operators_acquired_without_product_state_expansion':True}


def run(speed=F(4)):
    started=time.perf_counter()
    entrance_path=Path('relative_correlated_entrance_24sites.json')
    entrance=json.loads(entrance_path.read_text())
    original_modules,weights,probabilities,_=load_acquired_action(entrance_path)
    entrance_spread=F(entrance['relative_projective_certificate']['spread_factor_upper_exact'])
    baseline=json.loads(Path('conditioned_count_queries_results.json').read_text())
    baseline_posterior=json.loads(Path('conditioned_count_posterior_24sites.json').read_text())
    baseline_numerical_spread=F(baseline_posterior['projective_spread_upper_exact'])/entrance_spread
    # Recover a very tight enclosure of the retained baseline lower-mixture
    # likelihood from its outward reported true-likelihood enclosure and the
    # exact saved multipliers.  No baseline propagation is repeated.
    base_mass_lo,base_mass_hi=recover_retained_mass(
        baseline['full_record_probability_interval'],entrance_spread,baseline_numerical_spread)
    modules,identities,source_check=acquire_future_hypothesis(
        original_modules,weights,probabilities,speed)
    mass=F(1); numerical_spread=F(1)
    for observation in baseline['record']:
        selected=set(observation['observed_count_one_sites'])
        counts=tuple(int(i in selected) for i in range(len(modules)))
        weights,probabilities,z,c,_=update_count_record(
            modules,weights,probabilities,F(observation['duration']),counts)
        mass*=z; numerical_spread*=c
    combined_spread=entrance_spread*numerical_spread
    error=tv_from_spread(combined_spread)
    bf_lower=mass/base_mass_hi/(entrance_spread*baseline_numerical_spread)
    bf_upper=mass/base_mass_lo*entrance_spread*numerical_spread
    model_posterior_lower=bf_lower/(1+bf_lower)
    model_posterior_upper=bf_upper/(1+bf_upper)
    joint=define_joint_approximation(entrance_spread,(base_mass_lo,base_mass_hi),(mass,mass),
                                     baseline_numerical_spread,numerical_spread)
    saved={
        'scientific_object':'correlated state posterior under the specified faster-exchange hypothesis',
        'new_work':True,'common_preparation_entrance_file':str(entrance_path),
        'kinetic_speed_factor':str(speed),
        'source_parameters':{'modules':[{'alpha':str(m.alpha),'beta':str(m.beta),'kappa':str(m.kappa)} for m in modules]},
        'record_file':'conditioned_count_queries_results.json',
        'exact_rational_weights':[str(w) for w in weights],
        'exact_rational_probability_one':[[str(p) for p in row] for row in probabilities],
        'normalization_checked_exactly':sum(weights,F(0))==1,
        'record_lower_mixture_mass_exact':str(mass),
        'projective_spread_upper_exact':str(combined_spread),
        'whole_state_posterior_TV_upper':str(error)}
    Path('fast_exchange_count_posterior_24sites.json').write_text(json.dumps(saved,separators=(',',':')))
    result={
        'new_work':True,
        'source_acquisition_entrance_recomputed':False,
        'baseline_count_filter_recomputed':False,
        'model_change':'alpha_s=s alpha; beta_s=s(beta+kappa)-kappa; kappa_s=kappa',
        'speed_factor':str(speed),
        'common_entrance_assumption':'the same prepared entrance is stipulated before either future kinetic hypothesis acts',
        'stationary_active_fraction_and_turnover_rate_matched_exactly':True,
        'finite_time_mean_scope':'the acquired entrance is generally nonstationary; finite-window means need not match',
        'first_component_analytic_comparison':identities[0],
        'source_obtaining_check':source_check,
        'count_windows':baseline['whole_record_windows'],
        'observed_turnovers':baseline['whole_record_observed_turnovers'],
        'changed_model_record_probability_interval':[str(I(mass/entrance_spread).lo),str(I(mass*entrance_spread*numerical_spread).hi)],
        'Bayes_factor_changed_over_baseline_interval':[str(I(bf_lower).lo),str(I(bf_upper).hi)],
        'equal_prior_changed_model_posterior_interval':[str(I(model_posterior_lower).lo),str(I(model_posterior_upper).hi)],
        'joint_model_and_state_approximation':joint,
        'joint_model_and_state_posterior_TV_upper':joint['whole_joint_posterior_TV_upper'],
        'changed_model_later_numerical_spread_minus_one_upper':str(I(numerical_spread-1).hi),
        'changed_model_subsequent_queries':future_queries(modules,weights,probabilities,F(error)),
        'elapsed_seconds':time.perf_counter()-started,
        'scope':'certified comparison of specified mathematical kinetic hypotheses on a supplied count record; no biological adequacy or empirical identification claim'}
    Path('kinetic_model_comparison_results.json').write_text(json.dumps(result,indent=2))
    return result


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
