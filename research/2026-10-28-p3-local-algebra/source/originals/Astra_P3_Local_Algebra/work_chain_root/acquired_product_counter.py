#!/usr/bin/env python3
"""Acquired chain-algebra components and a global quadratic coupling."""
from acquired_chain_counter import *
from local_algebra_acquisition import acquire_product_chain

def compile_product(poly,n,*,local_decoder='gabidulin'):
    start=time.perf_counter();acquired=acquire_product_chain(set(poly),n)
    B=quadratic_matrix_from_anf(acquired['quadratic_remainder'],n)
    base=[0]*n;components=[]
    for component in acquired['components']:
        width,offset=component['n'],component['bit_offset'];mask=(1<<width)-1
        local_B=[(B[offset+i]>>offset)&mask for i in range(width)]
        R=ChainRing(component['h'],component['e'])
        if component['module_dimension']!=3 or R.d<3:raise ValueError('requires rank-three chain components, d>=3')
        if local_decoder=='gabidulin':local_base,_,_=acquire_quadratic_base(local_B,R.h,1)
        elif local_decoder=='sylvester':local_base,_,_,_=acquire_sylvester_base(local_B,R.h,1)
        elif local_decoder=='none':local_base=local_B
        else:raise ValueError('unknown local decoder')
        for i,row in enumerate(local_base):base[offset+i]=row<<offset
        local=dict(component,quadratic_remainder=component['local_quadratic_remainder'])
        polynomial,fit=fit_ordinary_cubic(local,local_base)
        balanced,columns,factor=factor_chain_cubic(R,polynomial)
        components.append(dict(component=component,R=R,polynomial=polynomial,balanced=balanced,
            columns=columns,gram=Solver(R.gram()),fit=fit,factor=factor))
    defect=[x^y for x,y in zip(B,base)];factors,unary=symplectic_factors(defect)
    rank=len(factors);numerator=0
    for selector in range(1<<rank):
        parity=unary^linear_apply(factors,selector)
        product=(-1)**sum(((selector>>(2*j))&3)==3 for j in range(rank//2))
        for item in components:
            c=item['component'];local=(parity>>c['bit_offset'])&((1<<c['n'])-1)
            shifted=shifted_polynomial(item['R'],item['balanced'],item['columns'],local,item['gram'])
            product*=balanced_count(item['R'],shifted)
            if not product:break
        numerator+=product
    denominator=1<<(rank//2)
    if numerator%denominator:raise AssertionError('global reconstruction not integral')
    signed=numerator//denominator
    return dict(original_variables=n,raw_anf_terms=len(poly),coordinate_columns=acquired['coordinate_columns'],
        component_count=len(components),components=[dict(n=item['component']['n'],
            bit_offset=item['component']['bit_offset'],field_degree=item['R'].d,
            chain_length=item['R'].e,field_modulus=item['R'].h,
            polynomial=[dict(exponents=list(e),coefficient=c) for e,c in sorted(item['polynomial'].items())],
            factor_certificate=item['factor'],fit=item['fit']) for item in components],
        acquired_defect=defect,acquired_defect_rank=rank,walsh_leaf_count=1<<rank,retained_walsh_leaves=0,
        exact_numerator=numerator,exact_denominator=denominator,signed_count=signed,
        zero_count=((1<<n)+signed)//2,seconds=time.perf_counter()-start)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--local-decoder',choices=['gabidulin','sylvester','none'],default='gabidulin')
    args=parser.parse_args();data=json.loads(args.input.read_text())
    result=compile_product(data['polynomial'],data['n'],local_decoder=args.local_decoder)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
