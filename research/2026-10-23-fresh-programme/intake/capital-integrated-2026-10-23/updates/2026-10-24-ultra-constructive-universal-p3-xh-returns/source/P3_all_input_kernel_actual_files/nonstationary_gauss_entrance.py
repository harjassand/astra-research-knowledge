"""New relative entrance executor for arbitrary binary product initialization.

This extends one irreversible opening with unchanged silent Q on both sides.
The source adapter is new; the existing stationary adapter is not modified.
The demonstrated source starts every leaf deterministically off.  Its local
integrand is mu exp(Q*(t-u)) exp((Q-D)*u), not a stationary killed row.

Local rational commutator-recursion bounds plus interval semigroups produce a
positive Gauss mixture and a componentwise relative certificate.  The retained
law is exact rational and uses the existing reusable entrance schema.
"""
from fractions import Fraction as F
from math import comb, prod
from pathlib import Path
import itertools
import json
import time

from pro3_gate_experiment import I, D
from source_interface_compiler import star_source, with_product_mixture_initial, SourceError
from tensor_separator_entrance import BinaryModule
from tensor_gauss_entrance import nodes
from relative_gauss_entrance import C4, exact_mixture, node_rounding_spread
from tensor_reuse_entrance import load_acquired_action
from conditioned_count_queries import tv_from_spread


class NonstationaryEntrance:
    def __init__(self,modules,initial_rows,gamma,t,mark):
        if not modules or len(modules)!=len(initial_rows) or gamma<=0 or t<=0 or not 0<=mark<len(modules):
            raise ValueError('Invalid one-opening source')
        if any(min(m.alpha,m.beta,m.kappa)<=0 for m in modules):
            raise ValueError('This numerical bridge requires positive binary rates')
        if any(len(row)!=2 or min(row)<0 or sum(row)!=1 for row in initial_rows):
            raise ValueError('Exact local probability rows are required')
        self.modules=modules; self.initial_rows=initial_rows
        self.gamma=F(gamma); self.t=F(t); self.mark=mark
        self.data=[m.prepare() for m in modules]

    def silent_row(self,i,duration):
        module=self.modules[i]; stationary=module.alpha/(module.alpha+module.beta)
        active=I(stationary)+I(self.initial_rows[i][1]-stationary)*(-I((module.alpha+module.beta))*I(duration)).exp()
        return 1-active,active

    def vectors(self,u):
        output=[]
        for i,module in enumerate(self.modules):
            a,b,k=I(module.alpha),I(module.beta),I(module.kappa)
            _,_,_,gap,slow,fast=self.data[i]
            es=(-slow*I(u)).exp(); ef=(-fast*I(u)).exp()
            e00=((fast-a)*es+(a-slow)*ef)/gap
            e01=a*(es-ef)/gap
            e10=b*(es-ef)/gap
            e11=((fast-b-k)*es+(b+k-slow)*ef)/gap
            before0,before1=self.silent_row(i,I(self.t)-I(u))
            output.append((before0*e00+before1*e10,before0*e01+before1*e11))
        return output

    def weight(self,u):
        return I(self.gamma)*(-I(self.gamma)*(I(self.t)-I(u))).exp()


def obtain_nonstationary_adapter(interface,event_mark,t):
    """Checked new bridge from the general source compiler, with no equilibrium requirement."""
    if len(interface.controller)!=1 or len(interface.initial)!=1:
        raise SourceError('nonstationary_executor_scope',requirement='one controller bit and one product initial branch')
    gamma=interface.controller_generator[0][1]
    if gamma<=0 or interface.controller_generator!=((-gamma,gamma),(F(0),F(0))):
        raise SourceError('nonstationary_executor_controller',requirement='single irreversible opening')
    initial=interface.initial[0]
    if initial.weight!=1 or initial.controller_state!=0:
        raise SourceError('nonstationary_executor_initial_controller',requirement='controller starts closed')
    modules=[]; chosen=[]
    for i,component in enumerate(interface.components):
        if len(component.sites)!=1 or component.generators[0]!=component.generators[1]:
            raise SourceError('nonstationary_executor_component',component=i,
                              requirement='binary silent generator unchanged by opening')
        q=component.generators[0]; a,b=q[0][1],q[1][0]
        events=[event for event in interface.events if event.owner==i]
        if len(events)!=1:
            raise SourceError('nonstationary_executor_event_count',component=i)
        event=events[0]; k=event.hazards[1][1]
        if (min(a,b,k)<=0 or event.hazards!=((F(0),F(0)),(F(0),k))
                or event.controller_reset!=(0,1) or event.component_resets!=((i,(0,0)),)):
            raise SourceError('nonstationary_executor_event_scope',event=event.name)
        modules.append(BinaryModule(a,b,k))
        if event.mark==event_mark:
            chosen.append(i)
    if any(event.owner is None for event in interface.events) or len(chosen)!=1:
        raise SourceError('nonstationary_executor_mark',mark=event_mark)
    return NonstationaryEntrance(modules,[tuple(row) for row in initial.component_rows],gamma,F(t),chosen[0])


def derivative_bounds(model,order=8):
    """Compute safe rational relative bounds from C'=-Q C+C A."""
    whole=[model.gamma**r for r in range(order+1)]; local_records=[]
    for i,module in enumerate(model.modules):
        a,b,k=module.alpha,module.beta,module.kappa
        Q=[[-a,a],[b,-b]]; A=[[-a,a],[b,-b-k]]
        final_silent=model.silent_row(i,model.t)
        minimum=min(v.lo for v in final_silent)
        if minimum<=0:
            raise ValueError('Positive silent-time support unresolved at this precision')
        domination=F((I(k*model.t).exp()/I(minimum)).hi)
        C=[[F(1),F(0)],[F(0),F(1)]]; local=[]; norms=[]
        for r in range(order+1):
            norm=max(sum(abs(x) for x in row) for row in C); norms.append(norm)
            local.append(F(1) if r==0 else k if r==1 else norm*domination)
            C=[[sum(-Q[x][z]*C[z][y]+C[x][z]*A[z][y] for z in range(2))
                for y in range(2)] for x in range(2)]
        whole=[sum(F(comb(r,j))*whole[r-j]*local[j] for j in range(r+1))
               for r in range(order+1)]
        local_records.append({'silent_distribution_lower':[str(v.lo) for v in final_silent],
            'silent_distribution_upper':[str(v.hi) for v in final_silent],
            'relative_derivative_bounds_exact':[str(x) for x in local],
            'commutator_recursion_matrix_infinity_norms_exact':[str(x) for x in norms]})
    return whole,local_records


def positive_gauss_nodes(model,cells):
    h=model.t/cells; parts=[]
    for cell in range(cells):
        for node,weight in nodes():
            u=(cell+node)*I(h); vectors=model.vectors(u)
            coefficient=I(h)*weight*model.weight(u)
            lower=[]; upper=[]
            for i,row in enumerate(vectors):
                if i==model.mark:
                    value=I(model.modules[i].kappa)*row[1]
                    lower.append((max(D(0),value.lo),D(0))); upper.append((value.hi,D(0)))
                else:
                    lower.append(tuple(max(D(0),v.lo) for v in row))
                    upper.append(tuple(v.hi for v in row))
            parts.append({'cl':coefficient.lo,'cu':coefficient.hi,'rows_l':lower,'rows_u':upper})
    return parts


def compile_relative(model,tolerance=F(1,10**9),initial_cells=64):
    if not 0<tolerance<1 or type(initial_cells) is not int or initial_cells<=0:
        raise ValueError('A positive cell count and tolerance in (0,1) are required')
    bounds,local=derivative_bounds(model); cells=initial_cells
    log_bound=model.gamma+sum(m.kappa for m in model.modules)
    while True:
        if cells>16384:
            raise RuntimeError('Relative quadrature exceeds the declared numerical budget')
        h=model.t/cells
        delta=F((I(C4*h**8*bounds[8])*I(log_bound*h).exp()).hi)
        if delta>=1 or tv_from_spread((1+delta)/(1-delta))>I(tolerance).lo:
            cells*=2
            continue
        parts=positive_gauss_nodes(model,cells)
        rounding,support=node_rounding_spread(parts)
        a=1/(1+delta); b=rounding/(1-delta); spread=b/a
        error=tv_from_spread(spread)
        if error<=I(tolerance).lo:
            break
        cells*=2
    weights,probabilities,mass=exact_mixture(parts)
    certificate={'comparison':'lower_multiplier * M_approx <= M_true <= upper_multiplier * M_approx componentwise',
        'measure_scale':'unnormalized first-mark entrance density; M_approx mass is source_unnormalized_mass_exact',
        'lower_multiplier_exact':str(a),'upper_multiplier_exact':str(b),
        'spread_factor_upper_exact':str(spread),
        'posterior_TV_any_common_positive_operation_upper':str(error),
        'quadrature_relative_error_upper_exact':str(delta),
        'node_rounding_spread_upper_exact':str(rounding),
        'eighth_derivative_relative_bound_exact':str(bounds[8]),
        'cell_log_variation_bound_exact':str(log_bound),'time_cells':cells,
        'positive_product_components':len(parts),
        'common_local_support':[[x for x,ok in enumerate(mask) if ok] for mask in support],
        'local_derivative_bound_method':'C0=I; C_(r+1)=-Q C_r+C_r A; b0=1; b1=kappa; higher b=||C_r||infinity exp(kappa*t)/min(mu exp(Q*t))',
        'source_scope':'arbitrary binary product initialization; unchanged silent generators across one irreversible opening; specified local hazard and reset',
        'retained_state_scope':'post-event leaf configuration and known open controller at the exact observed time; latent opening time is not retained',
        'later_operation_scope':'same positive linear operation with finite nonzero output mass; further numerical operations need their own certificate'}
    return parts,weights,probabilities,mass,certificate,local


def independent_expanded_check(model,parts,certificate):
    n=len(model.modules)
    if n>6:
        raise ValueError('Expanded reference is restricted to small sources')
    states=list(itertools.product((0,1),repeat=n+1)); index={x:i for i,x in enumerate(states)}
    Q=[[F(0) for _ in states] for _ in states]; mu=[F(0) for _ in states]
    for row,x in enumerate(states):
        if x[0]==0:
            Q[row][index[(1,)+x[1:]]]+=model.gamma
            mu[row]=prod(model.initial_rows[i][bit] for i,bit in enumerate(x[1:]))
        for i,module in enumerate(model.modules):
            changed=list(x); changed[i+1]=1-changed[i+1]
            Q[row][index[tuple(changed)]]+=module.alpha if x[i+1]==0 else module.beta
        Q[row][row]=-sum(Q[row])
        if x[0]:
            Q[row][row]-=sum(module.kappa*x[i+1] for i,module in enumerate(model.modules))
    rate=max(-Q[i][i] for i in range(len(states))); argument=rate*model.t
    transition=[[(j,F(int(i==j))+q/rate) for j,q in enumerate(row) if F(int(i==j))+q/rate]
                for i,row in enumerate(Q)]
    exponential=(-I(argument)).exp(); vector=mu[:]; accumulated=mu[:]; term=F(1); order=0
    while True:
        first=term*argument/(order+1)
        if order+2>argument:
            tail=F(exponential.hi)*first/(1-argument/(order+2))
            if tail<F(1,10**50):
                break
        order+=1; term*=argument/order; updated=[F(0) for _ in states]
        for i,row in enumerate(transition):
            for j,p in row:
                updated[j]+=vector[i]*p
        vector=updated; accumulated=[a+term*v for a,v in zip(accumulated,vector)]
        if order>1000:
            raise RuntimeError('Independent reference series budget exceeded')
    a=F(certificate['lower_multiplier_exact']); b=F(certificate['upper_multiplier_exact'])
    positive=0; zeros=0
    for x in itertools.product((0,1),repeat=n):
        approximate=sum(F(part['cl'])*prod(F(part['rows_l'][i][bit]) for i,bit in enumerate(x)) for part in parts)
        if x[model.mark]:
            assert approximate==0; zeros+=1
            continue
        before=list(x); before[model.mark]=1
        partial=accumulated[index[(1,)+tuple(before)]]*model.modules[model.mark].kappa
        ref_lo=F(exponential.lo)*partial
        ref_hi=F(exponential.hi)*partial+model.modules[model.mark].kappa*tail
        if not a*approximate<=ref_lo<=ref_hi<=b*approximate:
            raise AssertionError('Nonstationary expanded coordinate enclosure outside relative bounds')
        positive+=1
    return {'expanded_killed_states':len(states),'uniformization_terms':order+1,
        'poisson_tail_upper':str(I(tail).hi),'positive_output_coordinates_checked':positive,
        'structural_zero_output_coordinates_checked':zeros,
        'all_reference_coordinate_enclosures_inside_relative_sandwich':True}


def run_case(n=24,save=False):
    started=time.perf_counter()
    source,compiled=with_product_mixture_initial(star_source(n),[F(1)],[[F(0)]*n],((0,0),))
    model=obtain_nonstationary_adapter(compiled,'reaction_0',F(3,2))
    parts,weights,probabilities,mass,certificate,local=compile_relative(model,initial_cells=64 if n==24 else 4)
    a=F(certificate['lower_multiplier_exact']); b=F(certificate['upper_multiplier_exact'])
    result={'new_work':True,'initialization':'every leaf deterministically off; controller initially closed',
        'source_modules':n,'source_rules':len(source.rules),'source_initial_branches':len(compiled.initial),
        'new_source_obtained_through_general_compiler':True,
        'old_stationary_executor_unchanged':True,'event_time':str(model.t),'event_mark':model.mark,
        'entrance_density_interval':[str(I(a*mass).lo),str(I(b*mass).hi)],
        'relative_projective_certificate':certificate,
        'local_derivative_bounds':local,'elapsed_seconds':time.perf_counter()-started}
    if save:
        path=Path('nonstationary_correlated_entrance_24sites.json')
        data={'scientific_object':'conditional correlated entrance probability law','new_work':True,
            'source_record':{'time':str(model.t),'mark':model.mark,'controller_after_event':1,'firing_site_after_event':0},
            'source_parameters':{'gamma':str(model.gamma),
                'modules':[{'alpha':str(m.alpha),'beta':str(m.beta),'kappa':str(m.kappa)} for m in model.modules],
                'initial_local_probability_one':[str(row[1]) for row in model.initial_rows]},
            'representation':'sum_r weight[r] product_i Bernoulli(probability_one[r][i])',
            'exact_rational_weights':[str(w) for w in weights],
            'exact_rational_probability_one':[[str(p) for p in row] for row in probabilities],
            'normalization_checked_exactly':True,
            'posterior_total_variation_upper':certificate['posterior_TV_any_common_positive_operation_upper'],
            'source_unnormalized_mass_exact':str(mass),
            'source_density_interval':result['entrance_density_interval'],
            'relative_projective_certificate':certificate,
            'source_initialization_scope':'new deterministic-off scientific source, not the earlier stationary entrance'}
        path.write_text(json.dumps(data,separators=(',',':')))
        loaded=load_acquired_action(path)
        assert loaded[1]==weights and loaded[2]==probabilities
        result['retained_probability_law_file']=str(path)
        result['existing_loader_validated_new_retained_law']=True
    else:
        result['independent_expanded_check']=independent_expanded_check(model,parts,certificate)
    return result


if __name__=='__main__':
    output={'deterministic_off_24_sites':run_case(24,True),
            'deterministic_off_small_reference':run_case(3,False)}
    Path('nonstationary_gauss_entrance_results.json').write_text(json.dumps(output,indent=2))
    print(json.dumps({name:{k:v for k,v in result.items() if k!='local_derivative_bounds'}
                      for name,result in output.items()},indent=2))
