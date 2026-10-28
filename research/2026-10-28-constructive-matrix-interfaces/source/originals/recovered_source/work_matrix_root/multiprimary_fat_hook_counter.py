#!/usr/bin/env python3
"""Complete counting at fixed TOTAL acquired primary fat-hook alphabet.

Different irreducible degrees retain separate grading variables. Residual
Gaussians are evaluated jointly, retaining cross-primary resonances.
"""
from pathlib import Path
import itertools,sys,time
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent',
    'work_norm_slice_agent','work_norm_glue_agent')]
from durfee_primary_counter import manufacture_primary_evaluation_plan,primary_fat_hook_pairs
from mixed_primary_kernel import mixed_primary_profile_kernel,coefficient_ring
from fat_hook_hall import smallest_fat_hook,n_stat,transpose
from arbitrary_operator_hall import quotient_matrix
from matrix_kloosterman import Field,charpoly,factor_polynomial,primary_columns
from simple_operator_quadratic import matrix_source_anf
from krylov_square_source import quadratic_anf_sum
from feedback_nilpotent_gaussians import shifted_trace_polynomial


def decode_tensor(values,bases,plans):
    """Exact tensor-product interpolation; no scalar degree is conflated."""
    domains=[list(range(len(p['indices']))) for p in plans];tensor=dict(values)
    for axis,(basis,plan) in enumerate(zip(bases,plans)):
        others=[j for j in range(len(domains)) if j!=axis];out={}
        for rest in itertools.product(*(domains[j] for j in others)):
            fixed=dict(zip(others,rest))
            def key(v):return tuple(v if j==axis else fixed[j] for j in range(len(domains)))
            vector=[tensor.get(key(v),Fraction(0)) for v in domains[axis]]
            for shape,coefficient in basis.decode_evaluations(vector,plan).items():out[key(shape)]=coefficient
        tensor=out;domains[axis]=[entry[1] for entry in basis.entries]
    return tensor


def joint_primary_profile_weights(t,q,primary):
    begun=time.perf_counter();data=[]
    for item in primary:
        d=len(item['irreducible'])-1;m=sum(item['rows']);r,s=item['alphabet']
        bases,points,plans,metadata=manufacture_primary_evaluation_plan(m,r,s,q**d)
        data.append(dict(degree=d,maximum=m,r=r,s=s,bases=bases,points=points,plans=plans,metadata=metadata))
    evaluations={};records=[]
    for locations in itertools.product(*(range(len(item['points'])) for item in data)):
        specs=[]
        for item,location in zip(data,locations):
            point=item['points'][location];r=item['r']
            specs.append(dict(degree=item['degree'],maximum=item['maximum'],
                cyclic=list(point[:r]),semisimple=list(point[r:])))
        values,metadata=mixed_primary_profile_kernel(t,q,specs)
        evaluations[locations]=values;records.append(dict(point_indices=locations,**metadata))
    weights={};state_ranges=[range(item['maximum']+1) for item in data]
    for state in itertools.product(*state_ranges):
        bases=[item['bases'][k] for item,k in zip(data,state)]
        plans=[item['plans'][k] for item,k in zip(data,state)]
        for residue in range(4):
            values={}
            for local in itertools.product(*(range(len(plan['indices'])) for plan in plans)):
                points=tuple(plan['indices'][j] for plan,j in zip(plans,local))
                values[local]=evaluations[points][state][residue]
            for shapes,coefficient in decode_tensor(values,bases,plans).items():
                for item,shape in zip(data,shapes):coefficient*=q**(item['degree']*n_stat(shape))
                if coefficient.denominator!=1 or coefficient<0:
                    raise AssertionError('joint physical profile weight is not a nonnegative integer')
                weights.setdefault(shapes,[0]*4)[residue]=coefficient.numerator
    zero=tuple(() for _ in data)
    if weights.get(zero)!=[1,0,0,0]:raise AssertionError('empty joint profile mismatch')
    return weights,dict(total_alphabets=sum(item['r']+item['s'] for item in data),
        primary_evaluation_plans=[item['metadata'] for item in data],kernel_calls=len(records),
        kernel_records=records,joint_profile_states=len(weights),
        primary_grading_states=math_product(item['maximum']+1 for item in data),
        unrestricted_partitions_enumerated=0,seconds=time.perf_counter()-begun)


def math_product(values):
    answer=1
    for value in values:answer*=value
    return answer


def acquire_primary_alphabets(D,field_h,maximum_total_alphabets=None):
    F=Field(field_h);D=[list(row) for row in D];t=len(D)
    if not t or any(len(row)!=t or any(type(x) is not int or not 0<=x<F.q for x in row) for row in D):
        raise ValueError('literal nonempty square matrix required')
    polynomial=charpoly(D,F);primary=[];h=0
    for f,m in factor_polynomial(polynomial,F):
        columns=primary_columns(D,f,m,F);rows=transpose(tuple(columns));r,s=smallest_fat_hook(rows)
        h+=(len(f)-1)*len(columns)
        primary.append(dict(irreducible=f,jordan_columns=columns,rows=rows,alphabet=(r,s)))
    K=sum(sum(item['alphabet']) for item in primary)
    if maximum_total_alphabets is not None and K>maximum_total_alphabets:
        raise ValueError('acquired total alphabet count exceeds the specified family bound')
    return F,primary,dict(characteristic_polynomial=polynomial,minimal_polynomial_degree=h,
        total_alphabets=K,primary_shapes=[dict(irreducible=x['irreducible'],rows=x['rows'],
            acquired_alphabet=x['alphabet']) for x in primary],supplied_primary_decomposition=False)


def multiprimary_matrix_count(D,field_h,beta,phi=(),eta=0,maximum_total_alphabets=None):
    begun=time.perf_counter();F,primary,acquisition=acquire_primary_alphabets(D,field_h,maximum_total_alphabets)
    q=F.q;t=len(D);phi=set(phi)
    if not 0<=beta<q or not 0<=eta<q or any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('field coefficients and a Boolean quadratic trace source required')
    weights,kernel=joint_primary_profile_weights(t,q,primary)
    options=[primary_fat_hook_pairs(item['rows'],*item['alphabet'],q**(len(item['irreducible'])-1)) for item in primary]
    phase=F.trace(F.mul(beta,F.mul(eta,eta)));gaussians={};terms=[];answer=0
    for selected in itertools.product(*options):
        alpha=tuple(item[0] for item in selected);rho=tuple(item[1] for item in selected)
        number=math_product(item[2] for item in selected)
        c=sum((len(item['irreducible'])-1)*sum(shape) for item,shape in zip(primary,alpha));b=t-c
        if rho not in gaussians:
            residual=quotient_matrix(primary,rho,F);G=[]
            for parity in range(2 if eta else 1):
                shifted=shifted_trace_polynomial(phi,F,eta if parity else 0,beta)
                G.append(quadratic_anf_sum(matrix_source_anf(residual,F,beta,shifted,eta),F.a*b*b))
            gaussians[rho]=G
        row=weights.get(alpha,[0]*4);G=gaussians[rho]
        value=sum(row[h]*(-1 if phase*(h*(h-1)//2)%2 else 1)*G[h%len(G)] for h in range(4))
        contribution=number*q**(c*(c-1)//2+c*b)*value;answer+=contribution
        terms.append(dict(controlled_types=alpha,quotient_types=rho,submodule_population=number,
            profile_weights=row,joint_quotient_gaussians=G,contribution=contribution))
    gap=q**(t*t)*answer;n=3*F.a*t*t
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid full original-domain count')
    return dict(original_independent_bits=n,gap=gap,ones=((1<<n)-gap)//2,zeros=((1<<n)+gap)//2,
        field_polynomial=field_h,source_operator=D,beta=beta,eta=eta,trace_quadratic_anf=sorted(phi),
        acquisition=acquisition,profile_kernel=kernel,terms=terms,
        joint_quotient_types=len(gaussians),joint_hall_leaves=len(terms),
        full_unrestricted_matrix_domain=True,original_domain_preserved=True,
        joint_resonances_retained=True,enumerated_original_assignments=0,
        bit_time_bound='(t+1)^O(K)*poly(a,t) for acquired total fat-hook alphabet K',
        uniformly_polynomial_in_K=False,seconds=time.perf_counter()-begun)


def compile_multiprimary_trace_response(D,field_h,beta,eta=0,maximum_total_alphabets=None):
    """Full arbitrary-program response for all even-degree primary factors."""
    begun=time.perf_counter();F,primary,acquisition=acquire_primary_alphabets(D,field_h,maximum_total_alphabets)
    q=F.q;t=len(D)
    if not 0<beta<q or not 0<=eta<q:raise ValueError('nonzero beta and field eta required')
    if any((len(item['irreducible'])-1)%2 for item in primary):
        raise ValueError('this sparse trace backend requires even-degree irreducibles')
    weights,kernel=joint_primary_profile_weights(t,q,primary)
    options=[primary_fat_hook_pairs(item['rows'],*item['alphabet'],q**(len(item['irreducible'])-1)) for item in primary]
    phase=F.trace(F.mul(beta,F.mul(eta,eta)));quotients={};points={};terms=[]
    for selected in itertools.product(*options):
        alpha=tuple(item[0] for item in selected);rho=tuple(item[1] for item in selected)
        number=math_product(item[2] for item in selected)
        c=sum((len(item['irreducible'])-1)*sum(shape) for item,shape in zip(primary,alpha));b=t-c
        if rho not in quotients:
            residual=quotient_matrix(primary,rho,F);tau=0
            for i in range(b):tau^=residual[i][i]
            constant=tau^(beta if b*(b-1)//2%2 else 0)
            sigma=F.mul(F.inv(beta),F.pow(constant,q//2)^F.mul(eta,tau)) if b else 0
            G=quadratic_anf_sum(matrix_source_anf(residual,F,beta,(),eta),F.a*b*b)
            quotients[rho]=(sigma,G)
        sigma,G=quotients[rho];row=weights.get(alpha,[0]*4)
        scale=number*q**(t*t+c*(c-1)//2+c*b)*G
        for h,value in enumerate(row):
            delta=eta if h%2 else 0;point=sigma^delta
            sign=(phase*(h*(h-1)//2))%2^F.trace(F.mul(F.mul(beta,delta),sigma))
            contribution=scale*value*(1-2*sign)
            points[point]=points.get(point,0)+contribution
        terms.append(dict(controlled_types=alpha,quotient_types=rho,
            profile_weights=row,regular_trace_point=sigma,regular_gaussian=G))
    points={point:value for point,value in points.items() if value}
    if len(points)>1<<(len(primary)+1):raise AssertionError('shared trace support bound failed')
    return dict(field_polynomial=field_h,field_degree=F.a,matrix_size=t,beta=beta,eta=eta,
        rank_cap=t,padding=t,full_matrix_domain=True,original_independent_bits=3*F.a*t*t,
        counted_domain_size=q**(3*t*t),
        response=[dict(kind='point',argument=point,coefficient=value) for point,value in sorted(points.items())],
        acquired=acquisition,profile_kernel=kernel,quotient_terms=terms,
        remaining_walsh_terms=0,manufactured_point_terms=len(points),
        trace_program_anf_expanded=False,auxiliary_independent_inputs=0,
        compiled_without_field_enumeration=True,joint_resonances_retained=True,
        bit_time_bound='(t+1)^O(K)*poly(a,t), plus at most 2^(s+1) program evaluations',
        seconds=time.perf_counter()-begun)


def compile_raw_multiprimary(poly,n,maximum_total_alphabets=None):
    """Acquire everything from a raw cubic, then count all original inputs."""
    from minimal_polynomial_compiler import acquire_raw_minimal_source
    begun=time.perf_counter();acquired=acquire_raw_minimal_source(poly,n,allow_zero_beta=True)
    algebra=acquired['algebra'];polynomial,primary=algebra.primary_data(acquired['D'])
    D=quotient_matrix(primary,[transpose(tuple(item['jordan_columns'])) for item in primary],algebra.F)
    result=multiprimary_matrix_count(D,algebra.h,acquired['beta'],acquired['phi'],
        acquired['eta'],maximum_total_alphabets)
    if result['original_independent_bits']!=n:raise AssertionError('raw independent input count changed')
    result.update(raw_cubic_input=True,raw_core_monomials=acquired['raw_monomials'],
        source_acquisition=acquired['stats'],acquisition_seconds=acquired['acquisition_seconds'],
        source_unit_and_primary_decomposition_supplied=False,total_seconds=time.perf_counter()-begun)
    return result


if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--maximum-alphabets',type=int)
    args=parser.parse_args();data=json.loads(args.source.read_text())
    if 'anf' in data:result=compile_raw_multiprimary(data['anf'],data['n'],args.maximum_alphabets)
    else:result=multiprimary_matrix_count(data['D'],data['h'],data.get('beta',1),data.get('phi',()),
        data.get('eta',0),args.maximum_alphabets)
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')
