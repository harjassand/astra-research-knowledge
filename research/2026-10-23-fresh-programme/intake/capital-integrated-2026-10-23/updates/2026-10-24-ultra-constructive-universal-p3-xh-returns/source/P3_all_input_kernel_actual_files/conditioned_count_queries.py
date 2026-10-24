"""New research: certified repeated reaction-count conditioning.

Consumes the already acquired, correlated 24-site entrance law and its
componentwise relative certificate.  Every later observation is a vector of
site-resolved turnover counts over a finite interval.  No event timestamps or
global ordering are observed.  Each local count-resolved propagator is a
positive 2x2 operator acquired from a finite local counting augmentation.

Positive uniformization supplies entrywise intervals.  After each update a
positive product mixture is retained, with an explicit multiplicative
rounding/operator enclosure.  Its spread multiplies the entrance spread;
there is no division by the probability of the observed count record.

This executor uses the supplied mathematical source and specified observation
model.  It does not claim that the count record is experimental evidence.
Existing research files and the original entrance law are never overwritten.
"""

from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import json
import time

from pro3_gate_experiment import I, D, DOWN, UP
from tensor_separator_entrance import BinaryModule
from tensor_reuse_entrance import load_acquired_action, survival_rows


def tv_from_spread(spread):
    root=I(spread).sqrt()
    return ((I(root.hi)-1)/(I(root.hi)+1)).hi


@lru_cache(maxsize=None)
def count_kernel(alpha,beta,kappa,duration,count,terms=64):
    """Entrywise enclosure of [z^count] exp(t (A+z J)).

    A=[[-alpha,alpha],[beta,-beta-kappa]],
    J=[[0,0],[kappa,0]].  The augmented counter 0,...,count is killed by
    another marked event at its last layer.  Returning its last layer gives
    exactly count events.  Only 2(count+1) local states are constructed.
    """
    if min(alpha,beta,kappa,duration)<=0 or type(count) is not int or count<0:
        raise ValueError('Positive rates/time and a nonnegative integer count are required')
    rate=max(alpha,beta+kappa)
    size=2*(count+1)
    transitions=[]
    for layer in range(count+1):
        zero=2*layer; one=zero+1
        transitions.append(((zero,1-alpha/rate),(one,alpha/rate)))
        row=[(one,1-(beta+kappa)/rate),(zero,beta/rate)]
        if layer<count:
            row.append((one+1,kappa/rate))
        transitions.append(tuple(row))
    assert all(p>=0 for row in transitions for _,p in row)
    assert all(sum(p for _,p in row)<=1 for row in transitions)
    z=rate*duration
    if terms+2<=z:
        raise ValueError('Increase the local uniformization series budget')
    exponential=(-I(z)).exp()
    matrices=[]
    for initial in (0,1):
        vector=[F(0)]*size; vector[initial]=F(1)
        accumulated=vector[:]; poisson_term=F(1)
        for order in range(1,terms+1):
            updated=[F(0)]*size
            for state,row in enumerate(transitions):
                for destination,probability in row:
                    updated[destination]+=vector[state]*probability
            vector=updated
            poisson_term*=z/order
            accumulated=[s+poisson_term*v for s,v in zip(accumulated,vector)]
        first_omitted=poisson_term*z/(terms+1)
        # Geometric Poisson tail: no subtraction of nearly equal numbers.
        tail=F(exponential.hi)*first_omitted/(1-z/(terms+2))
        row=[]
        for final in (0,1):
            partial=exponential*I(accumulated[2*count+final])
            upper=UP.add(partial.hi,I(tail).hi)
            interval=I(partial.lo,min(D(1),upper))
            if interval.lo<=0:
                raise ValueError('Local positive support not resolved at this precision')
            row.append(interval)
        matrices.append(tuple(row))
    return tuple(matrices),tail,size


def update_count_record(modules,weights,probabilities,duration,counts):
    if len(counts)!=len(modules):
        raise ValueError('One count is required for each observed component')
    kernels=[]; largest_tail=F(0); states_used=0
    for module,count in zip(modules,counts):
        kernel,tail,local_states=count_kernel(module.alpha,module.beta,module.kappa,duration,count)
        kernels.append(kernel); largest_tail=max(largest_tail,tail)
        states_used+=local_states
    new_masses=[]; new_probabilities=[]; step_spread=D(1)
    for weight,probability_row in zip(weights,probabilities):
        weight_interval=I(weight)
        lower_mass=F(weight_interval.lo)
        ratio=I(weight_interval.hi)/I(weight_interval.lo)
        new_row=[]
        for probability,kernel in zip(probability_row,kernels):
            before=(I(1-probability),I(probability))
            after=[sum((before[x]*kernel[x][y] for x in (0,1)),I(0)) for y in (0,1)]
            if min(v.lo for v in after)<=0:
                raise ValueError('Positive local posterior support was lost numerically')
            local_ratio=max((I(v.hi)/I(v.lo)).hi for v in after)
            ratio=ratio*I(local_ratio)
            zero,one=F(after[0].lo),F(after[1].lo)
            mass=zero+one
            lower_mass*=mass
            new_row.append(one/mass)
        new_masses.append(lower_mass); new_probabilities.append(new_row)
        step_spread=max(step_spread,ratio.hi)
    normalizer=sum(new_masses,F(0))
    if not 0<normalizer<=1:
        raise ValueError('The retained observation subprobability must have mass in (0,1]')
    new_weights=[mass/normalizer for mass in new_masses]
    assert sum(new_weights,F(0))==1
    return new_weights,new_probabilities,normalizer,F(step_spread),{
        'largest_local_uniformization_tail_upper':str(I(largest_tail).hi),
        'sum_of_local_counter_states':states_used,
        'largest_local_counter_states':max(2*(k+1) for k in counts),
        'step_relative_spread_upper':str(I(F(step_spread)).hi),
        'step_relative_spread_minus_one_upper':str(I(F(step_spread)-1).hi)
    }


def future_queries(modules,weights,probabilities,posterior_error,lag=F(1,10)):
    means=[I(0) for _ in modules]; pair=I(0); survival=I(0)
    local=[survival_rows(module,lag) for module in modules]
    for weight,row in zip(weights,probabilities):
        w=I(weight); p=[I(x) for x in row]
        for i,pi in enumerate(p):
            means[i]=means[i]+w*pi
        pair=pair+w*p[-2]*p[-1]
        value=w
        for probability,(s0,s1) in zip(p,local):
            value=value*((1-probability)*s0+probability*s1)
        survival=survival+value
    error=I(posterior_error)
    def bounded(interval):
        return [str(max(D(0),(interval-error).lo)),str(min(D(1),(interval+error).hi))]
    cdf=1-survival
    return {'future_elapsed_time':str(lag),
            'next_reaction_CDF_interval':bounded(cdf),
            'site_22_active_probability_interval':bounded(means[-2]),
            'site_23_active_probability_interval':bounded(means[-1]),
            'sites_22_and_23_both_active_interval':bounded(pair),
            'certificate_scope':'true source posterior after the entire count record; interval arithmetic plus inherited and accumulated numerical projective errors'}


def small_local_check():
    """Separate floating-point local exponential consistency check only."""
    import numpy as np
    from scipy.linalg import expm
    a,b,k,t=F(3,5),F(2,5),F(3,2),F(1,2)
    deviations=[]
    for count in (0,1,3):
        kernel,tail,size=count_kernel(a,b,k,t,count)
        matrix=np.zeros((size,size))
        for layer in range(count+1):
            zero=2*layer; one=zero+1
            matrix[zero,zero]=-float(a); matrix[zero,one]=float(a)
            matrix[one,one]=-float(b+k); matrix[one,zero]=float(b)
            if layer<count:
                matrix[one,one+1]=float(k)
        reference=expm(float(t)*matrix)[:2,2*count:2*count+2]
        deviations.extend(abs(kernel[x][y].midfloat()-reference[x,y]) for x in (0,1) for y in (0,1))
    assert max(deviations)<1e-13
    return {'local_count_operators_checked':3,'largest_augmented_local_states':8,
            'maximum_floating_reference_difference':max(deviations),
            'role':'consistency check; the numerical certificate is the separate positive uniformization enclosure'}


def run(windows=12):
    started=time.perf_counter()
    path=Path('relative_correlated_entrance_24sites.json')
    data=json.loads(path.read_text())
    modules,weights,probabilities,_=load_acquired_action(path)
    if len(modules)!=24:
        raise ValueError('This declared workload uses the acquired 24-component source')
    certificate=data['relative_projective_certificate']
    entrance_spread=F(certificate['spread_factor_upper_exact'])
    numerical_spread=F(1); record_mass=F(1); records=[]
    duration=F(1,2)
    for window in range(windows):
        # A finite-resolution count vector: six one-count components rotate
        # through the array, with zero counts in the remaining components.
        selected={(5*window+4*k)%24 for k in range(6)}
        counts=tuple(int(i in selected) for i in range(24))
        weights,probabilities,mass,spread,local=update_count_record(
            modules,weights,probabilities,duration,counts)
        record_mass*=mass; numerical_spread*=spread
        combined_spread=entrance_spread*numerical_spread
        error=tv_from_spread(combined_spread)
        likelihood_lower=I(record_mass/entrance_spread).lo
        likelihood_upper=I(record_mass*entrance_spread*numerical_spread).hi
        records.append({'window':window+1,'duration':str(duration),
            'observed_count_one_sites':sorted(selected),
            'all_other_sites_observed_count_zero':True,
            'full_record_probability_interval':[str(likelihood_lower),str(likelihood_upper)],
            'approximate_current_window_probability':str(I(mass).midfloat()),
            'whole_posterior_TV_upper':str(error),
            'cumulative_numerical_spread_minus_one_upper':str(I(numerical_spread-1).hi),
            'positive_product_components':len(weights),
            'local_operator_certificate':local})
    combined_spread=entrance_spread*numerical_spread
    error=tv_from_spread(combined_spread)
    posterior={
        'scientific_object':'conditional correlated entrance after a site-resolved finite-window count record',
        'new_work':True,
        'source_entrance_file':str(path),
        'source_parameters':data['source_parameters'],
        'controller_state':1,
        'observation_windows':records,
        'exact_rational_weights':[str(w) for w in weights],
        'exact_rational_probability_one':[[str(p) for p in row] for row in probabilities],
        'normalization_checked_exactly':True,
        'projective_spread_upper_exact':str(combined_spread),
        'whole_posterior_TV_upper':str(error),
        'certificate_scope':'true source posterior at end of record; each count update includes its own positive uniformization and arithmetic envelope; later common exact positive operations do not amplify this error'
    }
    Path('conditioned_count_posterior_24sites.json').write_text(json.dumps(posterior,separators=(',',':')))
    result={'new_work':True,'source_modules':len(modules),'source_global_configurations':str(2**25),
        'source_acquisition_recomputed':False,
        'whole_record_windows':windows,'whole_record_duration':str(windows*duration),
        'whole_record_observed_turnovers':6*windows,
        'positive_product_components_retained':len(weights),
        'entrance_projective_spread_minus_one_upper':str(I(entrance_spread-1).hi),
        'cumulative_later_numerical_spread_minus_one_upper':str(I(numerical_spread-1).hi),
        'whole_posterior_TV_upper':str(error),
        'full_record_probability_interval':records[-1]['full_record_probability_interval'],
        'record_likelihood_relative_lower':str(I(1/entrance_spread).lo),
        'record_likelihood_relative_upper':str(I(entrance_spread*numerical_spread).hi),
        'record':records,
        'subsequent_queries':future_queries(modules,weights,probabilities,F(error)),
        'independent_local_check':small_local_check(),
        'elapsed_seconds':time.perf_counter()-started,
        'comparison_scope':'all calculations retain correlations. A CTBN implementation given the same positive mixture and exact local operators computes the same filter. The additional object tested here is the source-derived all-state relative certificate and its numerical propagation.'}
    Path('conditioned_count_queries_results.json').write_text(json.dumps(result,indent=2))
    return result


if __name__=='__main__':
    result=run()
    print(json.dumps({k:v for k,v in result.items() if k!='record'},indent=2))
