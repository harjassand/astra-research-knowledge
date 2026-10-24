"""Serialize the acquired correlated entrance and execute its next-event law.

New construction. Existing endpoint and Gauss outputs are retained.  The
controller remains open after the observed mark; the firing site resets to 0.
All mixture weights and local state probabilities are serialized as EXACT
rational numbers. The next-event semigroups use outward interval arithmetic.
"""
from fractions import Fraction as F
import json
from pathlib import Path
from tensor_separator_entrance import Entrance, BinaryModule
from tensor_gauss_entrance import compile_gauss
from pro3_gate_experiment import I, D, DOWN, UP


def load_acquired_action(path='tensor_correlated_entrance_24sites.json'):
    """Load the retained exact-rational law without repeating acquisition.

    Validation checks the mathematical probability object and the supported
    continuation/reset contract.  It does not reconstruct or independently
    re-prove the stored source error certificate.  Invalid retained data raise
    an error rather than silently causing a fresh acquisition.
    """
    with open(path) as f:
        action=json.load(f)
    def rational(value,name):
        if not isinstance(value,str):
            raise ValueError(f'{name} must be an exact rational string')
        try:
            return F(value)
        except (ValueError,ZeroDivisionError) as exc:
            raise ValueError(f'Invalid exact rational {name}') from exc
    if action.get('scientific_object')!='conditional correlated entrance probability law':
        raise ValueError('Unsupported retained scientific object')
    if action.get('representation')!='sum_r weight[r] product_i Bernoulli(probability_one[r][i])':
        raise ValueError('Unsupported retained mixture representation')
    source=action['source_parameters']
    gamma=rational(source['gamma'],'gamma')
    if gamma<=0 or not isinstance(source['modules'],list) or not source['modules']:
        raise ValueError('Expected a positive opening rate and nonempty local modules')
    modules=[]
    for i,record in enumerate(source['modules']):
        values=[rational(record[key],f'module {i} {key}') for key in ('alpha','beta','kappa')]
        if any(value<=0 for value in values):
            raise ValueError('This binary propagator requires positive local rates')
        modules.append(BinaryModule(*values))
    weights=[rational(w,f'weight {r}') for r,w in enumerate(action['exact_rational_weights'])]
    probabilities=[[rational(p,f'probability {r},{i}') for i,p in enumerate(row)]
                   for r,row in enumerate(action['exact_rational_probability_one'])]
    if not weights or len(weights)!=len(probabilities):
        raise ValueError('Inconsistent or empty mixture dimensions')
    if any(w<0 for w in weights) or sum(weights,F(0))!=1:
        raise ValueError('Mixture weights must be nonnegative and sum exactly to one')
    if any(len(row)!=len(modules) or any(p<0 or p>1 for p in row)
           for row in probabilities):
        raise ValueError('Invalid local probability rows')
    record=action['source_record']
    mark=record['mark']
    if type(mark) is not int or not 0<=mark<len(modules):
        raise ValueError('Invalid firing-site mark')
    if rational(record['time'],'source time')<=0:
        raise ValueError('Expected a positive observed event time')
    if record.get('controller_after_event')!=1 or record.get('firing_site_after_event')!=0:
        raise ValueError('Continuation requires open controller and firing-site reset to zero')
    if any(row[mark]!=0 for row in probabilities):
        raise ValueError('Retained entrance violates the recorded firing-site reset')
    error=rational(action['posterior_total_variation_upper'],'posterior TV bound')
    if not 0<=error<=1:
        raise ValueError('Invalid posterior total-variation bound')
    if rational(action['source_unnormalized_mass_exact'],'source mass')<=0:
        raise ValueError('Expected a positive source normalization mass')
    density=[rational(x,'source density endpoint') for x in action['source_density_interval']]
    if len(density)!=2 or not 0<density[0]<=density[1]:
        raise ValueError('Invalid positive source density enclosure')
    return modules,weights,probabilities,error


def make_acquired_action():
    with open('tensor_gauss_entrance_results.json') as f:
        previous=next(x for x in json.load(f) if x['modules']==24)
    n=24
    modules=[BinaryModule(F(3,5)+F(i,100),F(2,5)+F(i%5,50),F(3,2)+F(i%3,10)) for i in range(n)]
    model=Entrance(modules,F(7,10),F(3,2),0)
    parts,lower,upper,delta,eps,_,_=compile_gauss(model,previous['time_cells'])
    weights=[]; probabilities=[]
    for part in parts:
        weight=F(part['cl']); p=[]
        for row in part['rows_l']:
            a,b=F(row[0]),F(row[1]); mass=a+b
            assert mass>0
            weight*=mass; p.append(b/mass)
        weights.append(weight); probabilities.append(p)
    normalizer=sum(weights,F(0))
    weights=[w/normalizer for w in weights]
    assert sum(weights,F(0))==1
    assert all(0<=p<=1 for row in probabilities for p in row)
    assert all(row[0]==0 for row in probabilities)
    action={
      'scientific_object':'conditional correlated entrance probability law',
      'new_work':True,
      'source_record':{'time':'3/2','mark':0,'controller_after_event':1,'firing_site_after_event':0},
      'source_parameters':{'gamma':'7/10','modules':[{'alpha':str(x.alpha),'beta':str(x.beta),'kappa':str(x.kappa)} for x in modules]},
      'representation':'sum_r weight[r] product_i Bernoulli(probability_one[r][i])',
      'exact_rational_weights':[str(w) for w in weights],
      'exact_rational_probability_one':[[str(p) for p in row] for row in probabilities],
      'normalization_checked_exactly':True,
      'posterior_total_variation_upper':str(eps),
      'source_unnormalized_mass_exact':str(normalizer),
      'source_density_interval':[str(DOWN.subtract(lower.lo,delta.hi)),str(UP.add(lower.hi,delta.hi))]
    }
    with open('tensor_correlated_entrance_24sites.json','w') as f: json.dump(action,f,separators=(',',':'))
    return modules,weights,probabilities,F(eps)


def survival_rows(module,t):
    a,b,k=I(module.alpha),I(module.beta),I(module.kappa)
    total=a+b+k; gap=((a-b-k)*(a-b-k)+4*a*b).sqrt()
    slow=(total-gap)/2; fast=(total+gap)/2
    es=(-slow*I(t)).exp(); ef=(-fast*I(t)).exp()
    e00=((fast-a)*es+(a-slow)*ef)/gap
    e01=a*(es-ef)/gap
    e10=b*(es-ef)/gap
    e11=((fast-b-k)*es+(b+k-slow)*ef)/gap
    return e00+e01,e10+e11


def compose(modules,weights,probabilities,entrance_error):
    ww=[I(w) for w in weights]; pp=[[I(p) for p in row] for row in probabilities]
    marginals=[sum((w*p[i] for w,p in zip(ww,pp)),I(0)) for i in range(len(modules))]
    records=[]
    for t in [F(1,20),F(1,10),F(1,4),F(1,2),F(1)]:
        local=[survival_rows(m,t) for m in modules]
        correlated=I(0)
        for w,p in zip(ww,pp):
            value=w
            for pi,(s0,s1) in zip(p,local): value=value*((1-pi)*s0+pi*s1)
            correlated=correlated+value
        independent=I(1)
        for p,(s0,s1) in zip(marginals,local): independent=independent*((1-p)*s0+p*s1)
        cdf=1-correlated; naive=1-independent
        e=I(entrance_error)
        # Forward event prediction is a Markov kernel: no amplification of
        # the entrance TV certificate.  True-marginal product comparison
        # costs at most n*epsilon by a product coupling.
        true_cdf=[max(D(0),(cdf-e).lo),min(D(1),(cdf+e).hi)]
        naive_true_marginals=[max(D(0),(naive-len(modules)*e).lo),min(D(1),(naive+len(modules)*e).hi)]
        gap=naive-cdf
        gap_bound=[(gap-(len(modules)+1)*e).lo,(gap+(len(modules)+1)*e).hi]
        records.append({'lag':str(t),'next_event_CDF_approx':str(cdf.midfloat()),
                        'true_next_event_CDF_interval':[str(x) for x in true_cdf],
                        'product_of_exact_marginals_CDF_interval':[str(x) for x in naive_true_marginals],
                        'product_minus_correlated_CDF_interval':[str(x) for x in gap_bound]})
    return {'new_work':True,'modules':len(modules),'retained_positive_product_components':len(weights),
            'controller_stays_open':True,'firing_site_reset_to_zero':True,
            'entrance_TV_error_propagated_without_amplification':str(entrance_error),
            'next_event_calculations':records}


if __name__=='__main__':
    retained=Path('tensor_correlated_entrance_24sites.json')
    modules,weights,probabilities,error=(load_acquired_action(retained)
        if retained.exists() else make_acquired_action())
    result=compose(modules,weights,probabilities,error)
    print(json.dumps(result,indent=2))
    with open('tensor_reuse_entrance_results.json','w') as f: json.dump(result,f,indent=2)
