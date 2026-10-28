#!/usr/bin/env python3
"""Exact arbitrary-operator counter; partitions, not field points, are listed."""
from pathlib import Path
import sys,time
from functools import lru_cache
from fractions import Fraction
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_matrix_root'),str(ROOT/'work_norm_slice_agent')]
from whittaker_hankel_obstruction import (partitions,dominates,
    whittaker_monomial_coefficient,power_monomial_expansion)
from matrix_kloosterman import Field,factor_polynomial,pmul,charpoly,primary_columns
from krylov_square_source import companion,quadratic_anf_sum
from simple_operator_quadratic import matrix_source_anf
from feedback_nilpotent_gaussians import shifted_trace_polynomial

def n_stat(lam):return sum(i*x for i,x in enumerate(lam))
def transpose_partition(lam):return tuple(sum(x>=j for x in lam) for j in range(1,max(lam,default=0)+1))

@lru_cache(None)
def hl_removals(lam,size,Q):
    z=Fraction(1,Q);result=[];lc=transpose_partition(lam)
    def visit(i,remaining,mu):
        if i==len(lam):
            if remaining:return
            mu=tuple(x for x in mu if x);mc=transpose_partition(mu);counts=Counter(mu);weight=Fraction(1)
            for j in range(1,max(lam,default=0)+1):
                d0=(lc[j-1] if j<=len(lc) else 0)-(mc[j-1] if j<=len(mc) else 0)
                d1=(lc[j] if j<len(lc) else 0)-(mc[j] if j<len(mc) else 0)
                if d0==0 and d1==1:weight*=1-z**counts[j]
            if weight:result.append((mu,weight))
            return
        low=lam[i+1] if i+1<len(lam) else 0
        for drop in range(min(lam[i]-low,remaining)+1):visit(i+1,remaining-drop,mu+(lam[i]-drop,))
    visit(0,size,());return tuple(result)

@lru_cache(None)
def hl_monomial_coefficient(lam,alpha,Q):
    if not alpha:return Fraction(int(not lam))
    if sum(lam)!=sum(alpha) or not dominates(lam,alpha):return Fraction(0)
    return sum((c*hl_monomial_coefficient(mu,alpha[:-1],Q)
                for mu,c in hl_removals(lam,alpha[-1],Q)),Fraction(0))

@lru_cache(None)
def hl_monomial(lam,Q):
    return tuple((mu,c) for mu in partitions(sum(lam)) if (c:=hl_monomial_coefficient(lam,mu,Q)))

def power_to_monomial(poly):
    result={}
    for rho,c in poly.items():
        for mu,a in power_monomial_expansion(rho):result[mu]=result.get(mu,Fraction(0))+c*a
    return {mu:c for mu,c in result.items() if c}

def monomial_to_power(poly,degree):
    residual=dict(poly);result={}
    for rho in sorted(partitions(degree)):
        expansion=dict(power_monomial_expansion(rho));c=residual.get(rho,Fraction(0))/expansion[rho]
        if not c:continue
        result[rho]=c
        for mu,a in expansion.items():residual[mu]=residual.get(mu,Fraction(0))-c*a
    if any(residual.values()):raise AssertionError('power/monomial triangular conversion failed')
    return result

@lru_cache(None)
def hl_power(lam,Q):return tuple(monomial_to_power(dict(hl_monomial(lam,Q)),sum(lam)).items())

def power_multiply(left,right):
    result={}
    for alpha,c in left.items():
        for beta,d in right.items():
            rho=tuple(sorted(alpha+beta,reverse=True));result[rho]=result.get(rho,Fraction(0))+c*d
    return {rho:c for rho,c in result.items() if c}

@lru_cache(None)
def hall_product(alpha,beta,Q):
    degree=sum(alpha)+sum(beta)
    residual=power_to_monomial(power_multiply(dict(hl_power(alpha,Q)),dict(hl_power(beta,Q))))
    result={}
    for lam in partitions(degree):
        coefficient=residual.get(lam,Fraction(0))
        if not coefficient:continue
        for mu,c in hl_monomial(lam,Q):residual[mu]=residual.get(mu,Fraction(0))-coefficient*c
        value=coefficient*Fraction(Q)**(n_stat(lam)-n_stat(alpha)-n_stat(beta))
        if value.denominator!=1 or value<0:raise AssertionError('Hall coefficient is not a nonnegative integer')
        result[lam]=value.numerator
    if any(residual.values()):raise AssertionError('Hall basis inversion failed')
    return tuple(result.items())

@lru_cache(None)
def hall_pairs(lam,Q):
    n=sum(lam);result=[]
    for k in range(n+1):
        for alpha in partitions(k):
            for beta in partitions(n-k):
                value=dict(hall_product(alpha,beta,Q)).get(lam,0)
                if value:result.append((alpha,beta,value))
    return tuple(result)

@lru_cache(None)
def invariant_flag_power(lam,Q,degree):
    """Q^n(lambda) Q'_lambda(X;Q^-1), then p_r -> p_(degree*r)."""
    z=Fraction(1,Q);normalization=Fraction(Q)**n_stat(lam)
    for multiplicity in Counter(lam).values():
        for j in range(1,multiplicity+1):normalization*=1-z**j
    result={}
    for rho,c in hl_power(lam,Q):
        value=c*normalization
        for r in rho:value/=1-z**r
        result[tuple(degree*r for r in rho)]=value
    return tuple(result.items())

class RefinedProfileFunctional:
    def __init__(self,q,ambient):
        self.q=q;self.ambient=ambient;self.monomial={():[1,0,0,0]};self.power={():[1,0,0,0]}
        for degree in range(1,ambient+1):self.acquire_degree(degree)
    def acquire_degree(self,degree):
        shapes=sorted(partitions(degree))
        for lam in shapes:
            weight=(-1)**degree
            for i in range(lam[0]):weight*=1-self.q**(self.ambient-i)
            values=[0]*4;values[sum(lam[1::2])%4]=weight
            for mu in shapes:
                if mu>=lam:break
                c=whittaker_monomial_coefficient(lam,mu,self.q)
                if c:
                    for r in range(4):values[r]-=c*self.monomial[mu][r]
            if whittaker_monomial_coefficient(lam,lam,self.q)!=1:raise AssertionError('Whittaker basis is not monic')
            self.monomial[lam]=values
        for rho in shapes:
            self.power[rho]=[sum(c*self.monomial[mu][r] for mu,c in power_monomial_expansion(rho)) for r in range(4)]
    def evaluate(self,poly):
        values=[sum((c*self.power[rho][r] for rho,c in poly.items()),Fraction(0)) for r in range(4)]
        if any(value.denominator!=1 for value in values):raise AssertionError('profile functional did not return integers')
        return [value.numerator for value in values]

def quotient_matrix(primary,types,F):
    blocks=[]
    for item,lam in zip(primary,types):
        f=item['irreducible'];powers=[[1]]
        for _ in range(max(lam,default=0)):powers.append(pmul(powers[-1],f,F))
        blocks.extend(companion(powers[s]) for s in lam)
    n=sum(len(B) for B in blocks);D=[[0]*n for _ in range(n)];offset=0
    for B in blocks:
        for i,row in enumerate(B):D[offset+i][offset:offset+len(B)]=row
        offset+=len(B)
    return D

def arbitrary_operator_gap(primary,field_h,beta,phi,eta=0):
    begun=time.perf_counter();F=Field(field_h);q=F.q;phi=set(phi);primary=list(primary);types=[];t=0
    if not 0<=beta<q or not 0<=eta<q or any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('invalid source coefficient or trace polynomial')
    seen=set()
    for item in primary:
        f=list(item['irreducible']);columns=tuple(item['jordan_columns'])
        if tuple(f) in seen or factor_polynomial(f,F)!=[(f,1)]:raise ValueError('distinct irreducible primary factors required')
        seen.add(tuple(f))
        if not columns or any(type(c) is not int or c<=0 for c in columns) or tuple(sorted(columns,reverse=True))!=columns:
            raise ValueError('positive weakly decreasing Jordan columns required')
        lam=transpose_partition(columns);d=len(f)-1;t+=d*sum(lam);types.append(lam)
    functional=RefinedProfileFunctional(q,t);phase=F.trace(F.mul(beta,F.mul(eta,eta)))
    options=[hall_pairs(lam,q**(len(item['irreducible'])-1)) for item,lam in zip(primary,types)]
    gaussian_cache={};answer=0;leaves=0;terms=[]
    def gaussians(quotient):
        key=tuple(quotient)
        if key not in gaussian_cache:
            D=quotient_matrix(primary,quotient,F);b=len(D);values=[]
            for r in range(4):
                shifted=shifted_trace_polynomial(phi,F,eta if r%2 else 0,beta)
                source=matrix_source_anf(D,F,beta,shifted,eta)
                values.append(quadratic_anf_sum(source,F.a*b*b))
            gaussian_cache[key]=values
        return gaussian_cache[key]
    def visit(index,controlled,quotient,multiplicity,flag):
        nonlocal answer,leaves
        if index==len(primary):
            leaves+=1;c=controlled;b=t-c;weights=functional.evaluate(flag);G=gaussians(quotient)
            value=sum(weights[r]*(-1 if phase*(r*(r-1)//2)%2 else 1)*G[r] for r in range(4))
            contribution=multiplicity*q**(c*(c-1)//2+c*b)*value;answer+=contribution
            terms.append(dict(controlled_dimension=c,quotient_types=quotient,multiplicity=multiplicity,
                profile_weights=weights,gaussians=G,contribution=contribution))
            return
        d=len(primary[index]['irreducible'])-1;Q=q**d
        for alpha,residual,number in options[index]:
            next_flag=power_multiply(flag,dict(invariant_flag_power(alpha,Q,d)))
            visit(index+1,controlled+d*sum(alpha),quotient+[residual],multiplicity*number,next_flag)
    visit(0,0,[],1,{():Fraction(1)})
    gap=q**(t*t)*answer
    return gap,dict(route='arbitrary operator, exact Hall types and Whittaker inversion',
        matrix_size=t,field_degree=F.a,primary_data=primary,
        original_bits=3*F.a*t*t,beta=beta,eta=eta,phi=sorted(phi),
        primary_pair_options=[len(x) for x in options],joint_type_leaves=leaves,
        residual_gaussian_types=len(gaussian_cache),symmetric_function_states=len(functional.power),
        terms=terms,seconds=time.perf_counter()-begun,
        enumerated_field_elements=0,enumerated_matrices=0,enumerated_subspaces=0,
        uniform_polynomial_time=False)

def count_acquired_arbitrary_operator(algebra,beta,D,phi,eta=0):
    cp,primary=algebra.primary_data(D)
    gap,meta=arbitrary_operator_gap(primary,algebra.h,beta,phi,eta)
    meta.update(acquired_reduced_charpoly=cp,supplied_primary_decomposition=False)
    return gap,meta

def count_literal_operator(D,h,beta,phi,eta=0):
    """Exact original-domain count from an explicit operator, with no types supplied."""
    begun=time.perf_counter();F=Field(h);D=[list(row) for row in D];t=len(D);phi=set(phi)
    if not t or any(len(row)!=t for row in D) or any(type(x) is not int or not 0<=x<F.q for row in D for x in row):
        raise ValueError('a nonempty square matrix over the specified binary field is required')
    polynomial=charpoly(D,F);primary=[]
    for f,multiplicity in factor_polynomial(polynomial,F):
        columns=primary_columns(D,f,multiplicity,F)
        primary.append(dict(irreducible=f,multiplicity=multiplicity,jordan_columns=columns))
    acquisition_seconds=time.perf_counter()-begun
    gap,metadata=arbitrary_operator_gap(primary,h,beta,phi,eta)
    n=3*F.a*t*t
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain signed count')
    metadata.update(acquired_characteristic_polynomial=polynomial,
        supplied_primary_decomposition=False,primary_acquisition_seconds=acquisition_seconds,
        total_seconds=time.perf_counter()-begun,
        input_matrix_field_elements=t*t,input_matrix_bits=F.a*t*t,
        field_modulus_bits=h.bit_length(),source_field_coefficient_bits=2*F.a,
        trace_anf_monomials=len(phi),trace_anf_fixed_mask_bits=F.a*len(phi),
        dense_trace_quadratic_coefficients=1+F.a+F.a*(F.a-1)//2,
        partition_dimensions=[len(partitions(j)) for j in range(t+1)],
        bit_time_bound='2^{O(sqrt(t)+sum_f sqrt(m_f))} poly(a,t)',
        field_sensitive_bit_time_bound='2^{O(t min(1,a/log2(t+1)))} poly(a,t)',
        intermediate_integer_bits_bound='exp(O(sqrt(t))) poly(a,t)',
        field_arithmetic_and_primary_acquisition='deterministic polynomial bit cost included')
    return dict(original_bits=n,gap=gap,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,stats=metadata)

def main():
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',nargs='?',default='-',help='JSON file, or - for stdin: D,h,beta,phi,eta')
    parser.add_argument('--output',help='write complete exact result JSON to this path')
    args=parser.parse_args()
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    try:
        source=sys.stdin.read() if args.input=='-' else Path(args.input).read_text()
        data=json.loads(source)
        result=count_literal_operator(data['D'],data['h'],data.get('beta',0),data.get('phi',[]),data.get('eta',0))
        result['stats']['input_json_bytes']=len(source.encode('utf-8'))
    except (ValueError,KeyError,TypeError) as error:parser.error(str(error))
    text=json.dumps(result,indent=2)+'\n'
    if args.output:Path(args.output).write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
