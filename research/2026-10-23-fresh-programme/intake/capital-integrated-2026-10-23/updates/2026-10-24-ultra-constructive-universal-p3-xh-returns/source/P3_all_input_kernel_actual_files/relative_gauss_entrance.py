"""New projective certificate for an existing positive reaction entrance.

The retained 24-site probability law is unchanged.  Re-evaluating its Gauss
nodes obtains a componentwise numerical enclosure and checks exact identity
with the saved rational law.  A relative Peano remainder then certifies all
later common positive operations, including arbitrary nonzero conditioning.

The numerical acquisition specializes to positive stationary binary leaves,
one irreversible opening, and firing-leaf reset to zero.  The small expanded
check uses a separate rational uniformization of the full killed generator.
Existing source, absolute-error and retained-law files are never overwritten.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import itertools
import json
import time

from pro3_gate_experiment import I, D, UP
from tensor_separator_entrance import BinaryModule, Entrance
from tensor_gauss_entrance import compile_gauss
from tensor_reuse_entrance import load_acquired_action


C4=F(factorial(4)**4,9*factorial(8)**3)


def relative_derivative_bounds(modules,gamma,order=8):
    """Exact multinomial bounds |g^(r)(u)| <= B_r g(u)."""
    whole=[F(gamma)**r for r in range(order+1)]
    local_bounds=[]
    for module in modules:
        a,b,k=module.alpha,module.beta,module.kappa
        mu=[b/(a+b),a/(a+b)]
        if min(mu)<=0:
            raise ValueError('Relative derivative domination requires positive stationary rows')
        A=[[-a,a],[b,-b-k]]
        row=mu[:]; local=[]
        for d in range(order+1):
            local.append(max(abs(row[x])/mu[x] for x in range(2)))
            row=[sum(row[x]*A[x][y] for x in range(2)) for y in range(2)]
        local_bounds.append(local)
        whole=[sum(F(comb(d,r))*whole[d-r]*local[r] for r in range(d+1))
               for d in range(order+1)]
    return whole,local_bounds


def exact_mixture(parts):
    weights=[]; probabilities=[]
    for part in parts:
        weight=F(part['cl']); row=[]
        if weight<=0:
            raise ValueError('Positive Gauss coefficients are required')
        for lo0,lo1 in part['rows_l']:
            a,b=F(lo0),F(lo1); mass=a+b
            if a<0 or b<0 or mass<=0:
                raise ValueError('Invalid lower local measure')
            weight*=mass; row.append(b/mass)
        weights.append(weight); probabilities.append(row)
    mass=sum(weights,F(0))
    return [w/mass for w in weights],probabilities,mass


def node_rounding_spread(parts):
    """Bound U_node <= c_round L_node without product-state expansion.

    A zero upper/lower pair is a structural zero and contributes no ratio.
    Positive upper values with zero lower values invalidate relative control.
    The supported local coordinates must agree across all quadrature terms.
    """
    largest=D(1); support=None
    for part in parts:
        if part['cl']<=0:
            raise ValueError('A positive lower Gauss coefficient is required')
        ratio=I(part['cu'])/I(part['cl']); term_support=[]
        for low,up in zip(part['rows_l'],part['rows_u']):
            masks=[]; local=D(1)
            for l,u in zip(low,up):
                if l<0 or u<l:
                    raise ValueError('Invalid local interval enclosure')
                if u==0:
                    masks.append(False)
                    continue
                if l<=0:
                    raise ValueError('Precision insufficient on positive support')
                masks.append(True)
                local=max(local,(I(u)/I(l)).hi)
            if not any(masks):
                raise ValueError('Empty local support')
            term_support.append(tuple(masks)); ratio=ratio*I(local)
        if support is None:
            support=term_support
        elif support!=term_support:
            raise ValueError('Quadrature components do not share structural support')
        largest=max(largest,ratio.hi)
    return F(largest),support


def compile_relative(model,cells):
    # This is precisely the pre-existing Gauss node construction.  Its absolute
    # certificate is not needed for the new relative theorem.
    parts,_,_,_,_,_,_=compile_gauss(model,cells)
    bounds,_=relative_derivative_bounds(model.modules,model.gamma)
    h=model.t/cells
    log_bound=model.gamma+sum(m.kappa for m in model.modules)
    delta=F((I(C4*h**8*bounds[8])*I(log_bound*h).exp()).hi)
    if not 0<=delta<1:
        raise ValueError('Refine the time partition until relative delta is below one')
    cround,support=node_rounding_spread(parts)
    a=1/(1+delta); b=cround/(1-delta); spread=b/a
    root=I(spread).sqrt()
    posterior_tv=((I(root.hi)-1)/(I(root.hi)+1)).hi
    weights,probabilities,mass=exact_mixture(parts)
    certificate={
        'comparison':'lower_multiplier * M_approx <= M_true <= upper_multiplier * M_approx componentwise',
        'measure_scale':'unnormalized first-mark entrance density; M_approx mass is source_unnormalized_mass_exact',
        'lower_multiplier_exact':str(a),
        'upper_multiplier_exact':str(b),
        'spread_factor_upper_exact':str(spread),
        'posterior_TV_any_common_positive_operation_upper':str(posterior_tv),
        'quadrature_relative_error_upper_exact':str(delta),
        'node_rounding_spread_upper_exact':str(cround),
        'eighth_derivative_relative_bound_exact':str(bounds[8]),
        'cell_log_variation_bound_exact':str(log_bound),
        'gauss_constant_exact':str(C4),
        'time_cells':cells,
        'positive_product_components':len(parts),
        'common_local_support':[[int(x) for x,ok in enumerate(mask) if ok] for mask in support],
        'retained_state_scope':'post-event leaf configuration with known open controller at the exactly observed event time; mixture labels are representation indices, not a TV approximation of the continuous opening time',
        'later_operation_scope':'same positive linear operator on true and acquired entrance; finite nonzero output mass; subsequent numerical approximation needs its own certificate',
        'source_scope':'strictly positive stationary local distributions; finite independent binary leaves; one irreversible autonomous opening; specified local firing reset'
    }
    return parts,weights,probabilities,mass,certificate


def expanded_uniformization_check(model,parts,certificate,tolerance=F(1,10**32)):
    """Independent small full-state enclosure, with exact rational arithmetic."""
    n=len(model.modules)
    if n>6:
        raise ValueError('Expanded check is deliberately restricted to small sources')
    states=list(itertools.product((0,1),repeat=n+1)); index={x:i for i,x in enumerate(states)}
    Q=[[F(0) for _ in states] for _ in states]; mu=[F(0) for _ in states]
    for row,x in enumerate(states):
        if x[0]==0:
            Q[row][index[(1,)+x[1:]]]+=model.gamma
            p=F(1)
            for i,module in enumerate(model.modules):
                p*=((module.alpha if x[i+1] else module.beta)/(module.alpha+module.beta))
            mu[row]=p
        for i,module in enumerate(model.modules):
            y=list(x); y[i+1]=1-y[i+1]
            Q[row][index[tuple(y)]]+=module.alpha if x[i+1]==0 else module.beta
        Q[row][row]=-sum(Q[row])
        if x[0]:
            Q[row][row]-=sum(module.kappa*x[i+1] for i,module in enumerate(model.modules))
    rate=max(-Q[i][i] for i in range(len(states)))
    transition=[[(j,F(int(i==j))+q/rate) for j,q in enumerate(row)
                  if F(int(i==j))+q/rate] for i,row in enumerate(Q)]
    assert all(p>=0 for row in transition for _,p in row)
    assert all(sum(p for _,p in row)<=1 for row in transition)
    argument=rate*model.t; exponential=(-I(argument)).exp()
    vector=mu[:]; accumulated=mu[:]; poisson_term=F(1); order=0
    while True:
        first_omitted=poisson_term*argument/(order+1)
        if order+2>argument:
            tail=F(exponential.hi)*first_omitted/(1-argument/(order+2))
            if tail<=tolerance:
                break
        order+=1; poisson_term*=argument/order
        updated=[F(0) for _ in states]
        for i,row in enumerate(transition):
            for j,p in row:
                updated[j]+=vector[i]*p
        vector=updated
        accumulated=[a+poisson_term*v for a,v in zip(accumulated,vector)]
        if order>1000:
            raise RuntimeError('Expanded reference exceeded its declared series budget')
    a=F(certificate['lower_multiplier_exact']); b=F(certificate['upper_multiplier_exact'])
    kappa=model.modules[model.mark].kappa
    active=0; zeros=0; margins=[]
    for x in itertools.product((0,1),repeat=n):
        approximate=F(0)
        for part in parts:
            value=F(part['cl'])
            for i,state in enumerate(x):
                value*=F(part['rows_l'][i][state])
            approximate+=value
        if x[model.mark]:
            assert approximate==0
            zeros+=1
            continue
        before=list(x); before[model.mark]=1
        marked=accumulated[index[(1,)+tuple(before)]]*kappa
        ref_lo=F(exponential.lo)*marked
        ref_hi=F(exponential.hi)*marked+kappa*tail
        lower=a*approximate; upper=b*approximate
        if not lower<=ref_lo<=ref_hi<=upper:
            raise AssertionError('Independent expanded enclosure not contained in projective sandwich')
        active+=1
        margins.append(min((ref_lo-lower)/approximate,(upper-ref_hi)/approximate))
    return {'expanded_killed_states':len(states),'uniformization_terms':order+1,
            'poisson_tail_upper':str(I(tail).hi),'positive_output_coordinates_checked':active,
            'structural_zero_output_coordinates_checked':zeros,
            'all_expanded_coordinate_enclosures_inside_relative_sandwich':True,
            'minimum_relative_strict_margin_lower':str(I(min(margins)).lo)}


def upgrade_retained(path='tensor_correlated_entrance_24sites.json',cells=64):
    started=time.time()
    with open(path) as f:
        saved=json.load(f)
    modules,old_weights,old_probabilities,_=load_acquired_action(path)
    record=saved['source_record']; gamma=F(saved['source_parameters']['gamma'])
    model=Entrance(modules,gamma,F(record['time']),record['mark'])
    parts,weights,probabilities,mass,certificate=compile_relative(model,cells)
    if (weights!=old_weights or probabilities!=old_probabilities
            or mass!=F(saved['source_unnormalized_mass_exact'])):
        raise ValueError('Re-evaluated Gauss factors do not equal the retained probability law')
    upgraded=dict(saved)
    upgraded['previous_absolute_posterior_TV_upper']=saved['posterior_total_variation_upper']
    upgraded['posterior_total_variation_upper']=certificate['posterior_TV_any_common_positive_operation_upper']
    upgraded['relative_projective_certificate']=certificate
    upgraded['retained_probability_law_unchanged']=True
    upgraded['retained_exact_factors_verified']=True
    destination=Path('relative_correlated_entrance_24sites.json')
    destination.write_text(json.dumps(upgraded,separators=(',',':')))
    result={'new_work':True,'retained_law_unchanged':True,'exact_factor_identity_verified':True,
            'modules':len(modules),'configuration_count':str(2**(len(modules)+1)),
            'retained_law_file':str(destination),'certificate':certificate,
            'elapsed_seconds':time.time()-started}
    return result


def small_check():
    modules=[BinaryModule(F(3,5)+F(i,100),F(2,5)+F(i%5,50),F(3,2)+F(i%3,10)) for i in range(3)]
    model=Entrance(modules,F(7,10),F(2),0)
    parts,_,_,_,certificate=compile_relative(model,16)
    return {'modules':3,'certificate':certificate,
            'expanded_reference':expanded_uniformization_check(model,parts,certificate)}


if __name__=='__main__':
    result={'retained_24_site_law':upgrade_retained(),'small_independent_check':small_check()}
    Path('relative_gauss_entrance_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
