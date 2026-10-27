#!/usr/bin/env python3
"""Raw fixed-module-rank smooth stationary counter, with rank-five fixtures.

An explicit Boolean cubic ANF is the only production input. The centroid
compiler acquires its chain algebra and coordinates. This module manufactures
each residue center and proves its uniqueness over the algebraic closure by
a degree-(b+1) Macaulay rank calculation. No enumeration is used. A depth-one
field terminal is an explicit callback, never an implicit brute-force fallback.
"""
from pathlib import Path
import argparse,itertools,json,random,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_chain_root'))
from stationary_chain_counter import (ChainRing,Solver,acquire_chain,trace_gram,
    field_linear_solve,field_matrix_rank,quadratic_matrix_from_anf,
    quadratic_coefficients,quadratic_sum,ring_polynomial,polynomial_value,
    linear_apply,gf_mul,gf_pow)
from field_descent import extract_anf,random_invertible,span,bits


def degree_monomials(variables,degree):
    if variables==1: return [(degree,)]
    return [(j,)+tail for j in range(degree+1)
            for tail in degree_monomials(variables-1,degree-j)]


def normalize_cubic(cubic):
    if isinstance(cubic,dict):
        return {tuple(indices):coefficient for indices,coefficient in cubic.items() if coefficient}
    return {tuple(row['indices']):row['coefficient'] for row in cubic if row['coefficient']}


def field_gradient_quadrics(cubic,M,b,h):
    mask=(1<<(h.bit_length()-1))-1;quadrics=[]
    for i in range(b):
        g={tuple(2*int(j==k) for j in range(b)):M[i][k]
           for k in range(b) if M[i][k]}
        for indices,coefficient in cubic.items():
            if i not in indices or not coefficient&mask: continue
            exponent=tuple(int(j in indices and j!=i) for j in range(b))
            g[exponent]=g.get(exponent,0)^(coefficient&mask)
        quadrics.append({a:c for a,c in g.items() if c})
    return quadrics


def macaulay_smooth_certificate(cubic,M,b,h):
    targets=degree_monomials(b,b+1);factors=degree_monomials(b,b-1)
    index={a:j for j,a in enumerate(targets)}
    quadrics=field_gradient_quadrics(cubic,M,b,h);rows=[]
    for g in quadrics:
        for factor in factors:
            row=[0]*len(targets)
            for exponent,c in g.items():
                row[index[tuple(a+x for a,x in zip(exponent,factor))]]^=c
            rows.append(row)
    rank=field_matrix_rank(rows,h)
    if rank!=len(targets):
        raise ValueError('homogeneous residue gradient has no full-rank Macaulay certificate')
    return dict(macaulay_degree=b+1,macaulay_rows=len(rows),
                macaulay_columns=len(targets),macaulay_rank=rank,
                homogeneous_square_coefficients=M)


def acquired_residue_center(R,cubic,Q,b):
    if R.e<2 or R.d<2:
        raise ValueError('requires chain length >=2 and field degree >=2')
    n=b*R.m;B=quadratic_matrix_from_anf(Q,n)
    gram_solver=Solver(trace_gram(R.h))
    residue_mask=sum(R.mask<<(R.m*i) for i in range(b))
    evaluation=[[1<<k,gf_mul(1<<k,1<<k,R.h)] for k in range(R.d)]
    if field_matrix_rank(evaluation,R.h)!=2:
        raise AssertionError('linear and square field maps are not independent')
    M=[[0]*b for _ in range(b)];linear=[[0]*b for _ in range(b)];constant=[]
    for i in range(b):
        top=R.m*i+R.d*(R.e-1)
        if any(B[top+a]&~residue_mask for a in range(R.d)):
            raise ValueError('highest-digit derivative depends on a nonresidue digit')
        c=gram_solver(sum(int((1<<(top+a)) in Q)<<a for a in range(R.d)))
        if c is None: raise AssertionError('field coefficient-trace pairing failed')
        constant.append(c)
        for j in range(b):
            images=[]
            for k in range(R.d):
                functional=sum(((B[top+a]>>(R.m*j+k))&1)<<a for a in range(R.d))
                image=gram_solver(functional)
                if image is None: raise AssertionError('field coefficient-trace pairing failed')
                images.append(image)
            coefficients=field_linear_solve(evaluation,images,R.h)
            if coefficients is None:
                raise ValueError('residue derivative is not a linear-plus-square field map')
            linear[i][j],M[i][j]=coefficients
    rows=[];rhs=[]
    for i in range(b):
        for j in range(b):
            row=[0]*b
            if i!=j:
                for k in range(b):
                    if k not in (i,j):
                        row[k]=cubic.get(tuple(sorted((i,j,k))),0)&R.mask
            rows.append(row);rhs.append(linear[i][j])
    contraction_rank=field_matrix_rank(rows,R.h)
    if contraction_rank!=b: raise ValueError('residue third tensor has a nonzero radical')
    center=field_linear_solve(rows,rhs,R.h)
    if center is None: raise ValueError('residue derivative has no translated homogeneous center')
    for i in range(b):
        value=constant[i]
        for indices,c in cubic.items():
            if i in indices:
                j,k=(x for x in indices if x!=i)
                value^=gf_mul(c&R.mask,gf_mul(center[j],center[k],R.h),R.h)
        for j in range(b):
            value^=gf_mul(M[i][j],gf_mul(center[j],center[j],R.h),R.h)
            value^=gf_mul(linear[i][j],center[j],R.h)
        if value: raise ValueError('manufactured affine center is not critical')
    certificate=macaulay_smooth_certificate(cubic,M,b,R.h)
    certificate.update(center=center,linear_coefficients=linear,
                       constant_coefficients=constant,
                       center_contraction_rank=contraction_rank,field_map_fit_rank=2)
    return center,certificate


def rank_state_value(R,cubic,Q,x,b):
    mask=(1<<R.m)-1;values=[(x>>(R.m*i))&mask for i in range(b)];value=0
    for (i,j,k),c in cubic.items():
        value^=R.mul(c,R.mul(values[i],R.mul(values[j],values[k])))
    return R.functional(value)^polynomial_value(Q,x)


def stationary_fixed_rank_state(h,e,cubic,Q,b,*,field_terminal=None):
    cubic=normalize_cubic(cubic);Q=set(Q);stages=[];multiplier=1
    if b<3 or any(len(indices)!=3 or tuple(sorted(set(indices)))!=indices
                  or min(indices)<0 or max(indices)>=b for indices in cubic):
        raise ValueError('invalid squarefree ring cubic')
    while True:
        R=ChainRing(h,e);n=b*R.m
        if any(term<0 or term>>n or term.bit_count()>2 for term in Q):
            raise ValueError('state remainder must be an explicit binary quadratic')
        if e==1:
            if field_terminal is None:
                raise ValueError('finite-field terminal callback required at depth one')
            signed=field_terminal(h,b,cubic,Q)
            return multiplier*signed,dict(stages=stages,terminal='supplied exact finite-field callback',
                terminal_signed=signed,exact_multiplier=multiplier,
                enumerated_assignments=0,walsh_leaves=0)
        center,certificate=acquired_residue_center(R,cubic,Q,b)
        free_m=R.d*(e-1);free_n=b*free_m;free_mask=(1<<free_m)-1
        def restricted(y):
            x=sum((center[i]^(((y>>(free_m*i))&free_mask)<<R.d))<<(R.m*i)
                  for i in range(b))
            return rank_state_value(R,cubic,Q,x,b)
        if e<=3:
            residual=quadratic_coefficients(restricted,free_n)
            signed=quadratic_sum(lambda y:polynomial_value(residual,y),free_n)
            certificate.update(depth=e,free_variables=free_n,quadratic_terms=len(residual),
                               exact_third_tensor_cancellation=True)
            stages.append(certificate)
            return multiplier*signed,dict(stages=stages,terminal='exact binary quadratic elimination',
                terminal_signed=signed,exact_multiplier=multiplier,
                enumerated_assignments=0,walsh_leaves=0)
        next_e=e-3;next_R=ChainRing(h,next_e);small_mask=(1<<next_R.m)-1
        next_cubic={indices:c&small_mask for indices,c in cubic.items() if c&small_mask}
        def compress(y):
            return sum(((y>>(free_m*i))&small_mask)<<(next_R.m*i) for i in range(b))
        def discrepancy(y):
            return restricted(y)^rank_state_value(next_R,next_cubic,set(),compress(y),b)
        residual=quadratic_coefficients(discrepancy,free_n)
        kept=sum(small_mask<<(free_m*i) for i in range(b))
        if any(term&~kept for term in residual):
            raise ValueError('restricted remainder depends on a proposed unused ring layer')
        next_Q={compress(term) for term in residual}
        certificate.update(depth=e,next_depth=next_e,discarded_free_bits=2*b*R.d,
                           quadratic_terms=len(next_Q),exact_third_tensor_cancellation=True,
                           all_unused_layer_coefficients_checked=True)
        stages.append(certificate);multiplier<<=2*b*R.d
        e,cubic,Q=next_e,next_cubic,next_Q


def compile_fixed_rank_stationary(poly,n,*,field_terminal=None):
    started=time.perf_counter();acquired=acquire_chain(set(poly),n);b=acquired['module_dimension']
    signed,certificate=stationary_fixed_rank_state(acquired['h'],acquired['e'],
        acquired['cubic'],acquired['quadratic_remainder'],b,field_terminal=field_terminal)
    if abs(signed)>1<<n or ((1<<n)+signed)&1: raise AssertionError('invalid signed count')
    return dict(original_variables=n,raw_anf_terms=len(poly),module_dimension=b,
        field_degree=acquired['d'],chain_length=acquired['e'],field_modulus=acquired['h'],
        centroid_dimension=acquired['algebra_dimension'],
        centroid_dimension_trail=acquired['centroid_dimension_trail'],
        coordinate_columns=acquired['coordinate_columns'],canonical_cubic=acquired['cubic'],
        quadratic_remainder=acquired['quadratic_remainder'],certificate=certificate,
        signed_count=signed,zero_count=((1<<n)+signed)//2,seconds=time.perf_counter()-started)


def smooth_rank_five_polynomial(R,*,rng=None):
    if R.d!=3: raise ValueError('this concrete smooth fixture uses F8')
    alpha=2;alpha2=gf_mul(alpha,alpha,R.h)
    if len(span([1,alpha,alpha2]))!=3:
        raise AssertionError('fixture field elements are not binary independent')
    P={(0,0,0,0,3):1,(1,1,0,0,1):1,(0,0,1,1,1):1,
       (2,1,0,0,0):1,(1,2,0,0,0):gf_pow(alpha,6,R.h),
       (0,0,2,1,0):1,(0,0,1,2,0):gf_pow(alpha2,6,R.h)}
    if rng is not None and R.e>1:
        for exponent in degree_monomials(5,3):
            P[exponent]=P.get(exponent,0)^(rng.randrange(1<<(R.m-R.d))<<R.d)
    return {a:c for a,c in P.items() if c}


def rank_five_fixture(e,seed,*,disguise=True):
    R=ChainRing(0b1011,e);b=5;n=b*R.m;rng=random.Random(seed)
    P=smooth_rank_five_polynomial(R,rng=rng)
    height=(e+1)//3;qn=b*R.d*height;rank=qn-qn%2
    source_forms=random_invertible(qn,rng)
    factors=[sum(((a>>(R.d*height*i))&((1<<(R.d*height))-1))<<(R.m*i)
                 for i in range(b)) for a in source_forms[:rank]]
    constant=seed&1;mask=(1<<R.m)-1
    columns=random_invertible(n,rng) if disguise else [1<<i for i in range(n)]
    offset=rng.randrange(1<<n) if disguise else 0
    def hidden(x):
        value=R.functional(ring_polynomial(R,P,[(x>>(R.m*i))&mask for i in range(b)]))^constant
        for j in range(rank//2):
            value^=((factors[2*j]&x).bit_count()&1)*((factors[2*j+1]&x).bit_count()&1)
        return value
    def evaluate(x): return hidden(linear_apply(columns,x)^offset)
    raw=extract_anf(evaluate,n);q=1<<R.d
    if e%3==0: reference=q**(2*b*(e//3))
    elif e%3==2: reference=q**(2*b*(e//3)+b)
    else: raise ValueError('fixture oracle only uses lengths zero or two modulo three')
    reference*=1-2*constant
    metadata=dict(seed=seed,planted_field_modulus=R.h,planted_chain_length=e,
        planted_module_dimension=b,quotient_height=height,planted_error_rank=rank,
        planted_polynomial=[dict(exponents=list(a),coefficient=c) for a,c in sorted(P.items())],
        planted_error_factors=factors,planted_constant=constant,
        planted_binary_columns=columns,planted_binary_offset=offset)
    return raw,n,evaluate,reference,metadata


def run_raw_checks():
    results=[]
    for e,seed in [(2,9502),(3,9503)]:
        t=time.perf_counter();raw,n,evaluate,reference,metadata=rank_five_fixture(e,seed)
        source=Path(__file__).with_name(f'rank_five_{n}_input.json')
        source.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),separators=(',',':'))+'\n')
        print(json.dumps(dict(stage='raw centroid and stationary compiler',n=n,terms=len(raw),
                              fixture_seconds=time.perf_counter()-t)),flush=True)
        result=compile_fixed_rank_stationary(raw,n)
        assert result['module_dimension']==5
        assert result['centroid_dimension']==3*e
        assert result['field_degree']==3 and result['chain_length']==e
        assert result['signed_count']==reference
        assert result['certificate']['enumerated_assignments']==0
        assert result['certificate']['walsh_leaves']==0
        R=ChainRing(result['field_modulus'],e)
        cubic=normalize_cubic(result['canonical_cubic']);Q=set(result['quadratic_remainder'])
        rng=random.Random(seed+1000000)
        for _ in range(1024):
            y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y)
            assert rank_state_value(R,cubic,Q,y,5)==evaluate(x)
        result.update(metadata,reference=reference,pointwise_checks=1024,
                      raw_input_file=source.name,practical_speed_claim=False)
        results.append(result)
        Path(__file__).with_name('rank_five_stationary_results.json').write_text(
            json.dumps(dict(raw_cases=results),indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ['original_variables','module_dimension',
            'centroid_dimension','signed_count','zero_count','seconds']}),flush=True)
    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,nargs='?')
    parser.add_argument('--output',type=Path);parser.add_argument('--checks',action='store_true')
    args=parser.parse_args()
    if args.checks: run_raw_checks()
    elif args.input:
        source=json.loads(args.input.read_text())
        result=compile_fixed_rank_stationary(source['polynomial'],source['n'])
        text=json.dumps(result,indent=2)+'\n'
        if args.output: args.output.write_text(text)
        else: print(text,end='')
    else: parser.error('provide an input file or --checks')
