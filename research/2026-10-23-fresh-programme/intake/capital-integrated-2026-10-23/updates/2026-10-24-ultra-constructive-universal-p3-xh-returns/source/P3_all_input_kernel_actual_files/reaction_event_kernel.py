"""Acquire a relative-certified reaction-event kernel once, for every input.

The controller starts closed and opens once.  Local silent Q is unchanged by
opening.  The output is the unnormalized first-mark density at a fixed elapsed
time, including its local reset.  No row is normalized during acquisition.

The retained kernel is a positive rational sum of product matrices.  It is
reused for product inputs and for a retained count-accumulator tensor train.
The latter application keeps all past count-allocation information implicit;
the controller-only reset starting the new gated phase is explicit.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import comb,prod
from pathlib import Path
import itertools
import json
import time

from pro3_gate_experiment import I,D
from source_interface_compiler import star_source,compile_interface as compile_rules
from nonstationary_gauss_entrance import obtain_nonstationary_adapter
from tensor_separator_entrance import BinaryModule
from tensor_gauss_entrance import nodes
from relative_gauss_entrance import C4
from conditioned_count_queries import tv_from_spread
from unresolved_count_interface import integerize,load_interface as load_count_interface,probability_certificate


@dataclass
class EventKernel:
    modules:list
    gamma:F
    elapsed:F
    mark:int
    coefficients:list
    matrices:list
    denominators:list
    lower:F
    upper:F
    certificate:dict

    @property
    def spread(self):
        return self.upper/self.lower


def silent_matrix(module,t):
    rate=module.alpha+module.beta
    active=I(module.alpha/rate); inactive=I(module.beta/rate)
    decay=(-I(rate)*I(t)).exp()
    return [[inactive+active*decay,active*(1-decay)],
            [inactive*(1-decay),active+inactive*decay]]


def killed_matrix(module,t,prepared):
    a,b,k=I(module.alpha),I(module.beta),I(module.kappa)
    _,_,_,gap,slow,fast=prepared
    es=(-slow*I(t)).exp(); ef=(-fast*I(t)).exp()
    return [[((fast-a)*es+(a-slow)*ef)/gap,a*(es-ef)/gap],
            [b*(es-ef)/gap,((fast-b-k)*es+(b+k-slow)*ef)/gap]]


def matrix_product(left,right):
    return [[sum((left[x][z]*right[z][y] for z in (0,1)),I(0))
             for y in (0,1)] for x in (0,1)]


def source_derivative_bounds(modules,gamma,elapsed):
    whole=[gamma**r for r in range(9)]; local_records=[]
    for module in modules:
        a,b,k=module.alpha,module.beta,module.kappa
        Q=[[-a,a],[b,-b]]; A=[[-a,a],[b,-b-k]]
        silent=silent_matrix(module,elapsed)
        minimum=min(v.lo for row in silent for v in row)
        if minimum<=0:
            raise ValueError('All-input silent transition support unresolved at this precision')
        domination=F((I(k*elapsed).exp()/I(minimum)).hi)
        C=[[F(1),F(0)],[F(0),F(1)]]; local=[]
        for r in range(9):
            local.append(F(1) if r==0 else k if r==1 else
                         max(sum(abs(x) for x in row) for row in C)*domination)
            C=[[sum(-Q[x][z]*C[z][y]+C[x][z]*A[z][y] for z in (0,1))
                for y in (0,1)] for x in (0,1)]
        whole=[sum(F(comb(r,j))*whole[r-j]*local[j] for j in range(r+1)) for r in range(9)]
        local_records.append({'minimum_silent_transition_lower':str(minimum),
                              'relative_derivative_bounds_exact':[str(x) for x in local]})
    return whole,local_records


def acquire_from_source(source,event_mark,elapsed=F(1,10),tolerance=F(1,10**8)):
    """Acquire from the checked rule source; leaf initialization is a runtime argument."""
    if not 0<tolerance<1 or elapsed<=0:
        raise ValueError('Positive elapsed time and tolerance in (0,1) required')
    compiled=compile_rules(source)
    # This existing checked bridge supplies Q, D, the opening rate, and reset.
    # Its initial leaf row is deliberately not used by the kernel construction.
    spec=obtain_nonstationary_adapter(compiled,event_mark,elapsed)
    modules,gamma,mark=spec.modules,spec.gamma,spec.mark
    bounds,local=source_derivative_bounds(modules,gamma,elapsed)
    log_bound=gamma+sum(m.kappa for m in modules); cells=1
    while True:
        if cells>16384:
            raise RuntimeError('All-input kernel exceeds its declared quadrature budget')
        h=elapsed/cells
        delta=F((I(C4*h**8*bounds[8])*I(log_bound*h).exp()).hi)
        if delta>=1 or tv_from_spread((1+delta)/(1-delta))>I(tolerance).lo:
            cells*=2
            continue
        coefficients=[]; all_matrices=[]; all_denominators=[]; rounding=D(1)
        prepared=[m.prepare() for m in modules]
        for cell in range(cells):
            for node,weight in nodes():
                u=(cell+node)*I(h)
                scalar=I(h)*weight*I(gamma)*(-I(gamma)*(I(elapsed)-u)).exp()
                if scalar.lo<=0:
                    raise ValueError('Positive quadrature coefficient unresolved')
                ratio=I(scalar.hi)/I(scalar.lo); matrices=[]; denominators=[]
                for i,module in enumerate(modules):
                    H=matrix_product(silent_matrix(module,I(elapsed)-u),killed_matrix(module,u,prepared[i]))
                    if i==mark:
                        H=[[I(module.kappa)*H[x][1],I(0)] for x in (0,1)]
                    lower=[]; local_ratio=D(1)
                    for row in H:
                        for value in row:
                            if value.hi==0:
                                if value.lo!=0:
                                    raise ValueError('Inconsistent structural zero')
                                lower.append(F(0))
                            else:
                                if value.lo<=0:
                                    raise ValueError('Positive matrix support unresolved')
                                lower.append(F(value.lo))
                                local_ratio=max(local_ratio,(I(value.hi)/I(value.lo)).hi)
                    integers,denominator=integerize(lower)
                    matrices.append([integers[:2],integers[2:]])
                    denominators.append(denominator); ratio=ratio*I(local_ratio)
                coefficients.append(F(scalar.lo)); all_matrices.append(matrices)
                all_denominators.append(denominators); rounding=max(rounding,ratio.hi)
        lower=1/(1+delta); upper=F(rounding)/(1-delta); spread=upper/lower
        if tv_from_spread(spread)<=I(tolerance).lo:
            break
        cells*=2
    certificate={
        'comparison':'lower_multiplier * Khat <= Ktrue <= upper_multiplier * Khat entrywise, for every input and output configuration',
        'lower_multiplier_exact':str(lower),'upper_multiplier_exact':str(upper),
        'spread_factor_upper_exact':str(spread),
        'posterior_TV_for_every_input_and_later_common_positive_operation_upper':str(tv_from_spread(spread)),
        'quadrature_relative_error_upper_exact':str(delta),
        'node_rounding_spread_upper_exact':str(F(rounding)),
        'eighth_derivative_relative_bound_exact':str(bounds[8]),
        'cell_log_variation_bound_exact':str(log_bound),
        'time_cells':cells,'positive_product_operator_terms':len(coefficients),
        'initial_distribution_is_runtime_argument':True,
        'common_support':'all input configurations; outputs with marked leaf reset to0; other output states unrestricted',
        'normalization_rule':'apply the unnormalized kernel to the whole input law, then normalize once by its event-time density',
        'source_scope':'binary positive local rates, unchanged silentQ across one irreversible autonomous opening, specified local mark/reset; all later operators share the same physical input state'
    }
    kernel=EventKernel(modules,gamma,elapsed,mark,coefficients,all_matrices,all_denominators,lower,upper,certificate)
    return kernel,{'source_rules':len(source.rules),'source_components':len(compiled.components),
                   'general_source_compiler_used':True,'local_derivative_bounds':local}


def acquire_kernel(n=24,elapsed=F(1,10),tolerance=F(1,10**8)):
    """Demonstration-family convenience wrapper around source acquisition."""
    return acquire_from_source(star_source(n),'reaction_0',elapsed,tolerance)


def save_kernel(kernel,path):
    data={'scientific_object':'all-input positive reaction-event density kernel',
        'new_work':True,'input_controller_state':0,'output_controller_state':1,
        'elapsed_time':str(kernel.elapsed),'event_mark':kernel.mark,'marked_leaf_output_state':0,
        'source_parameters':{'gamma':str(kernel.gamma),'modules':[{'alpha':str(m.alpha),'beta':str(m.beta),'kappa':str(m.kappa)} for m in kernel.modules]},
        'operator_definition':'Khat(x,y)=sum_l coefficient[l] product_i integer_matrix[l][i][x_i][y_i]/denominator[l][i]',
        'exact_rational_coefficients':[str(c) for c in kernel.coefficients],
        'local_integer_matrices':[[[[str(x) for x in row] for row in matrix] for matrix in term] for term in kernel.matrices],
        'local_denominators_exact':[[str(d) for d in term] for term in kernel.denominators],
        'output_measure':'first-mark density at the fixed elapsed time; time is not integrated; row sums need not be at most one',
        'relative_projective_certificate':kernel.certificate}
    Path(path).write_text(json.dumps(data,separators=(',',':')))


def load_kernel(path):
    data=json.loads(Path(path).read_text())
    if data['scientific_object']!='all-input positive reaction-event density kernel':
        raise ValueError('Unsupported kernel object')
    modules=[BinaryModule(*(F(m[k]) for k in ('alpha','beta','kappa'))) for m in data['source_parameters']['modules']]
    coefficients=list(map(F,data['exact_rational_coefficients']))
    matrices=[[[list(map(int,row)) for row in matrix] for matrix in term] for term in data['local_integer_matrices']]
    denominators=[list(map(int,term)) for term in data['local_denominators_exact']]
    mark=data['event_mark']; elapsed=F(data['elapsed_time']); gamma=F(data['source_parameters']['gamma'])
    if not modules or min(gamma,elapsed)<=0 or any(min(m.alpha,m.beta,m.kappa)<=0 for m in modules):
        raise ValueError('Invalid positive source rates/time')
    if type(mark) is not int or not 0<=mark<len(modules) or data['input_controller_state']!=0 or data['output_controller_state']!=1:
        raise ValueError('Invalid controller/mark contract')
    if not coefficients or min(coefficients)<=0 or len(coefficients)!=len(matrices) or len(matrices)!=len(denominators):
        raise ValueError('Invalid positive operator dimensions')
    for term,scales in zip(matrices,denominators):
        if len(term)!=len(modules) or len(scales)!=len(modules) or min(scales)<=0:
            raise ValueError('Invalid local operator dimensions')
        for i,matrix in enumerate(term):
            if len(matrix)!=2 or any(len(row)!=2 or min(row)<0 for row in matrix):
                raise ValueError('Invalid nonnegative local matrix')
            for row in matrix:
                if i==mark and (row[0]<=0 or row[1]!=0):
                    raise ValueError('Marked reset support differs from certificate')
                if i!=mark and min(row)<=0:
                    raise ValueError('All-input positive support differs from certificate')
    certificate=data['relative_projective_certificate']
    a,b=F(certificate['lower_multiplier_exact']),F(certificate['upper_multiplier_exact'])
    R=F(certificate['spread_factor_upper_exact']); error=F(certificate['posterior_TV_for_every_input_and_later_common_positive_operation_upper'])
    if not 0<a<=b or b/a!=R or not 0<=error<1 or R>((1+error)/(1-error))**2:
        raise ValueError('Invalid relative operator certificate')
    return EventKernel(modules,gamma,elapsed,mark,coefficients,matrices,denominators,a,b,certificate)


def scalar_integer_coefficients(kernel):
    return integerize([c/F(prod(scales)) for c,scales in zip(kernel.coefficients,kernel.denominators)])


def product_application(kernel,probability_one,name,kernel_path):
    if len(probability_one)!=len(kernel.modules) or any(not 0<=p<=1 for p in probability_one):
        raise ValueError('Invalid product input')
    coefficient,denominator=scalar_integer_coefficients(kernel)
    input_denominator=prod(p.denominator for p in probability_one)
    mass_numerator=0; active_numerator=0; rare_numerator=0
    query_site=len(kernel.modules)-1
    for scalar,term in zip(coefficient,kernel.matrices):
        rows=[]
        for p,matrix in zip(probability_one,term):
            rows.append([(p.denominator-p.numerator)*matrix[0][y]+p.numerator*matrix[1][y] for y in (0,1)])
        masses=[sum(row) for row in rows]
        mass_numerator+=scalar*prod(masses)
        active_numerator+=scalar*rows[query_site][1]*prod(mass for i,mass in enumerate(masses) if i!=query_site)
        rare_numerator+=scalar*prod(sum(row) if i==kernel.mark else row[1] for i,row in enumerate(rows))
    if mass_numerator<=0:
        raise ValueError('Event-time density is not positive')
    mass=F(mass_numerator,denominator*input_denominator)
    lazy={'scientific_object':'exact lazy conditional entrance from a retained event kernel and product input',
        'name':name,'retained_kernel_file':str(kernel_path),
        'input_probability_one_exact':[str(p) for p in probability_one],
        'normalizer_kind':'event-time density, not a probability',
        'exact_approximate_event_density':str(mass),
        'probability_law_definition':'(product input row) Khat / exact_approximate_event_density',
        'posterior_projective_spread_upper_exact':str(kernel.spread),
        'whole_posterior_TV_upper':str(tv_from_spread(kernel.spread))}
    result={'input':name,'event_density_interval':[str(I(kernel.lower*mass).lo),str(I(kernel.upper*mass).hi)],
        'site_23_active':probability_certificate(F(active_numerator,mass_numerator),kernel.spread),
        'all_nonfiring_sites_active':probability_certificate(F(rare_numerator,mass_numerator),kernel.spread),
        'quadrature_recomputed':False}
    return lazy,result


def coefficients_through_degree(polynomials,total):
    accumulator=[1]+[0]*total
    for polynomial in polynomials:
        accumulator=[sum(accumulator[j]*polynomial[k-j] for j in range(k+1)) for k in range(total+1)]
    return accumulator


def apply_to_count_tt(kernel,kernel_path,source_path):
    source=load_count_interface(source_path)
    if len(source.modules)<2:
        raise ValueError('This demonstration query distinguishes site0 and the last site; at least two sites are required')
    if source.modules!=kernel.modules or kernel.mark!=0:
        raise ValueError('This declared reuse keeps the same local kinetics and mark0 reset')
    input_scalars,input_denominator=integerize([w/F(c) for w,c in zip(source.weights,source.component_normalizers)])
    kernel_scalars,kernel_denominator=scalar_integer_coefficients(kernel)
    K=source.total; n=len(source.modules); query_site=n-1
    mass=0; attribution=0; active=0; rare=0
    for input_scalar,component in zip(input_scalars,source.factors):
        for kernel_scalar,term in zip(kernel_scalars,kernel.matrices):
            # One implicit component pair is contracted at a time.  Its local
            # maps retain the old physical count k.  No factor train is saved
            # or converted to a product distribution.
            mass_polynomials=[]; active_polynomials=[]
            for factor,matrix in zip(component,term):
                output=[[row[0]*matrix[0][y]+row[1]*matrix[1][y] for y in (0,1)] for row in factor]
                mass_polynomials.append([sum(row) for row in output])
                active_polynomials.append([row[1] for row in output])
            others=coefficients_through_degree([p for i,p in enumerate(mass_polynomials) if i not in (0,query_site)],K)
            local_mass=0; local_attribution=0; local_active=0
            for k0 in range(K+1):
                for kq in range(K-k0+1):
                    prefix=others[K-k0-kq]*mass_polynomials[0][k0]
                    joint=prefix*mass_polynomials[query_site][kq]
                    local_mass+=joint
                    if k0>0:
                        local_attribution+=joint
                    local_active+=prefix*active_polynomials[query_site][kq]
            rare_polynomials=[mass_polynomials[i] if i==kernel.mark else active_polynomials[i] for i in range(n)]
            local_rare=coefficients_through_degree(rare_polynomials,K)[K]
            scalar=input_scalar*kernel_scalar
            mass+=scalar*local_mass; attribution+=scalar*local_attribution
            active+=scalar*local_active; rare+=scalar*local_rare
    if mass<=0:
        raise ValueError('The composed event-time density is not positive')
    normalizer=F(mass,input_denominator*kernel_denominator)
    spread=source.spread*kernel.spread
    lazy={'scientific_object':'exact lazy conditional state and historical-count law from retained counterTT and event kernel',
        'source_counter_TT_file':str(source_path),'retained_event_kernel_file':str(kernel_path),
        'preparation_protocol':'reset only controller from open to closed; retain every leaf and historical count-allocation variable unchanged',
        'observation':{'first_new_event_mark':kernel.mark,'known_elapsed_time':str(kernel.elapsed)},
        'local_map_definition':'a_new[r,l,i,k,y]=sum_x a_source[r,i,k,x] B_kernel[l,i,x,y]; source and kernel scalar factors retained',
        'normalizer_kind':'event-time density, not a probability',
        'exact_approximate_event_density':str(normalizer),
        'probability_law_definition':'normalized positive application of the retained Khat to the retained counterTT, with identity on historical counts',
        'source_mixture_components':len(source.weights),'kernel_operator_terms':len(kernel.coefficients),
        'implicit_component_pairs':len(source.weights)*len(kernel.coefficients),
        'count_bond_dimension_per_implicit_pair':K+1,
        'input_or_output_TT_converted_to_CP':False,
        'implicit_pairs_materialized_or_saved':False,
        'posterior_projective_spread_upper_exact':str(spread),
        'whole_joint_count_and_state_posterior_TV_upper':str(tv_from_spread(spread)),
        'certificate_scope':'source count-TT spread times all-input event-kernel spread; exact integer/rational contraction adds no approximation error'}
    Path('event_kernel_count_tt_application.json').write_text(json.dumps(lazy,separators=(',',':')))
    before=json.loads(Path('unresolved_count_interface_results.json').read_text())['queries_from_retained_object']['site_0_contributed_at_least_one_of_observed_turnovers']['true_probability_interval']
    result={'event_density_interval':[str(I(kernel.lower*normalizer/source.spread).lo),
                                     str(I(kernel.upper*normalizer*source.spread).hi)],
        'whole_joint_count_and_state_posterior_TV_upper':str(tv_from_spread(spread)),
        'old_site0_contribution_probability_before_new_observation_interval':before,
        'old_site0_contributed_at_least_one_after_new_observation':probability_certificate(F(attribution,mass),spread),
        'site23_active_after_new_observation':probability_certificate(F(active,mass),spread),
        'all_nonfiring_sites_active_after_new_observation':probability_certificate(F(rare,mass),spread),
        'lazy_probability_object_file':'event_kernel_count_tt_application.json',
        'historical_count_allocation_retained':True,'source_acquisition_or_prior_count_filter_recomputed':False,
        'kernel_quadrature_recomputed':False,'count_bond_dimension_per_implicit_pair':K+1,
        'implicit_component_pairs':len(source.weights)*len(kernel.coefficients)}
    return result


def all_input_expanded_check():
    kernel,_=acquire_kernel(3); n=3
    states=list(itertools.product((0,1),repeat=n+1)); index={x:i for i,x in enumerate(states)}
    Q=[[F(0) for _ in states] for _ in states]
    for row,x in enumerate(states):
        if x[0]==0:
            Q[row][index[(1,)+x[1:]]]+=kernel.gamma
        for i,module in enumerate(kernel.modules):
            y=list(x); y[i+1]=1-y[i+1]
            Q[row][index[tuple(y)]]+=module.alpha if x[i+1]==0 else module.beta
        Q[row][row]=-sum(Q[row])
        if x[0]:
            Q[row][row]-=sum(m.kappa*x[i+1] for i,m in enumerate(kernel.modules))
    rate=max(-Q[i][i] for i in range(len(states))); z=rate*kernel.elapsed
    transition=[[(j,F(int(i==j))+q/rate) for j,q in enumerate(row) if F(int(i==j))+q/rate]
                for i,row in enumerate(Q)]
    exponential=(-I(z)).exp(); positive=0; zeros=0; largest_tail=F(0); largest_order=0
    scalar,denominator=scalar_integer_coefficients(kernel)
    for initial in itertools.product((0,1),repeat=n):
        vector=[F(0) for _ in states]; vector[index[(0,)+initial]]=F(1)
        accumulated=vector[:]; term=F(1); order=0
        while True:
            first=term*z/(order+1)
            if order+2>z:
                tail=F(exponential.hi)*first/(1-z/(order+2))
                if tail<F(1,10**60):
                    break
            order+=1; term*=z/order; updated=[F(0) for _ in states]
            for i,row in enumerate(transition):
                for j,p in row:
                    updated[j]+=vector[i]*p
            vector=updated; accumulated=[a+term*v for a,v in zip(accumulated,vector)]
        largest_tail=max(largest_tail,tail); largest_order=max(largest_order,order)
        for output in itertools.product((0,1),repeat=n):
            approximate=F(sum(c*prod(matrix[x][y] for matrix,x,y in zip(term,initial,output))
                              for c,term in zip(scalar,kernel.matrices)),denominator)
            if output[kernel.mark]:
                assert approximate==0; zeros+=1
                continue
            before=list(output); before[kernel.mark]=1
            partial=accumulated[index[(1,)+tuple(before)]]*kernel.modules[kernel.mark].kappa
            lo=F(exponential.lo)*partial
            hi=F(exponential.hi)*partial+kernel.modules[kernel.mark].kappa*tail
            if not kernel.lower*approximate<=lo<=hi<=kernel.upper*approximate:
                raise AssertionError('All-input expanded kernel enclosure outside acquired sandwich')
            positive+=1
    return {'leaves':3,'expanded_killed_states':len(states),'all_basis_input_rows_checked':2**n,
        'positive_input_output_entries_checked':positive,'structural_zero_entries_checked':zeros,
        'all_reference_entry_enclosures_inside_operator_sandwich':True,
        'uniformization_terms':largest_order+1,'poisson_tail_upper':str(I(largest_tail).hi)}


def run():
    started=time.perf_counter(); kernel,source=acquire_kernel()
    kernel_path=Path('reaction_event_kernel_24sites.json')
    save_kernel(kernel,kernel_path); retained=load_kernel(kernel_path)
    assert retained.coefficients==kernel.coefficients and retained.matrices==kernel.matrices
    product_laws=[]; products=[]
    for name,p in [('all_off',F(0)),('all_on',F(1))]:
        law,result=product_application(retained,[p]*len(retained.modules),name,kernel_path)
        product_laws.append(law); products.append(result)
    Path('event_kernel_product_applications.json').write_text(json.dumps(product_laws,separators=(',',':')))
    result={'new_work':True,'kernel_acquired_once':True,'elapsed_time':str(retained.elapsed),
        'event_mark':retained.mark,'kernel_file':str(kernel_path),'source_obtaining':source,
        'all_input_relative_certificate':retained.certificate,
        'exact_lazy_product_application_file':'event_kernel_product_applications.json',
        'product_input_applications':products}
    Path('reaction_event_kernel_results.json').write_text(json.dumps(result,indent=2))
    result['retained_counter_TT_application']=apply_to_count_tt(retained,kernel_path,'unresolved_count_posterior_24sites.json')
    result['independent_all_input_check']=all_input_expanded_check()
    result['elapsed_seconds']=time.perf_counter()-started
    Path('reaction_event_kernel_results.json').write_text(json.dumps(result,indent=2))
    return result


if __name__=='__main__':
    result=run()
    print(json.dumps({k:v for k,v in result.items() if k!='source_obtaining'},indent=2))
