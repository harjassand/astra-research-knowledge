#!/usr/bin/env python3
"""Raw acquired pair counter. Generic Lauder-Wan point counting is not implemented.

The reference backend explicitly scans one field coordinate. A supplied
point_counter receives manufactured ordinary Artin-Schreier hypersurfaces.
"""
from acquired_contact_counter import *
from acquired_pair_terminal import acquire_pair_template,enumerated_terminal,moment_terminal


def moment_hypersurface(h,gamma,tau,i,j):
    if not 0<=i<=6 or not 0<=j<=6:raise ValueError('moment index outside zero through six')
    pairs=i+j;variables=2*pairs+2;w=variables-1;polynomial={}
    def add(indices,c):
        if not c:return
        a=[0]*variables
        for index in indices:a[index]+=1
        key=tuple(a);polynomial[key]=polynomial.get(key,0)^c
        if not polynomial[key]:del polynomial[key]
    add([0,0,0],tau)
    for pair in range(pairs):
        x=2*pair+1;y=x+1
        for indices in ([x,x,x],[x,y,y],[y,y,y],[0,x,y]):add(indices,gamma)
        if pair>=i:add([0,x,x],gamma);add([0,y,y],gamma)
    add([w,w],1);add([w],1)
    return dict(field_modulus=h,variables=variables,
        polynomial=[dict(exponents=list(a),coefficient=c) for a,c in sorted(polynomial.items())],
        moment_indices=[i,j],subtract_field_power=variables-1,degree_bound=3,characteristic=2)


def compile_pair_family(poly,n,*,point_counter=None,field_bit_budget=24):
    """point_counter(h,variables,ordinary_polynomial) returns exact #V(F_q)."""
    started=time.perf_counter();poly=set(poly);acquired=acquire_chain(poly,n)
    H,Q,fit=fit_rank_homogeneous_quotient(acquired);b=acquired['module_dimension']
    R=ChainRing(acquired['h'],acquired['e'])
    residue={a:c&R.mask for a,c in H.items() if c&R.mask}
    template=acquire_pair_template(R.h,residue);terminal_evidence=[]
    def terminal(h,rank,P):
        if h!=R.h or rank!=b or P!=residue:raise AssertionError('terminal residue differs from certified template')
        if point_counter is None:
            if R.d>field_bit_budget:raise ValueError('explicit reference field scan exceeds the bit budget')
            signed,evidence=enumerated_terminal(template)
            evidence['supplied_point_counter_executed']=False
        else:
            calls=[]
            def moment_backend(h,gamma,tau,i,j):
                reduction=moment_hypersurface(h,gamma,tau,i,j)
                ordinary={tuple(row['exponents']):row['coefficient'] for row in reduction['polynomial']}
                number=point_counter(h,reduction['variables'],ordinary)
                if not isinstance(number,int) or not 0<=number<=(1<<R.d)**reduction['variables']:
                    raise ValueError('point counter returned an invalid cardinality')
                calls.append(reduction)
                return number-(1<<R.d)**reduction['subtract_field_power']
            signed,counts=moment_terminal(template,moment_backend)
            evidence=dict(terminal_backend='supplied exact fixed-variable point counter',
                supplied_point_counter_executed=True,point_count_calls=calls,
                gaussian_state_multiplicities=counts,field_elements_enumerated_by_wrapper=0,
                supplied_backend_internal_work_reported=False)
        terminal_evidence.append(evidence);return signed
    signed,count=weighted_contact_sum(R.h,R.e,H,Q,b,terminal_bit_budget=0,field_terminal=terminal)
    if abs(signed)>1<<n or ((1<<n)+signed)&1:raise AssertionError('invalid exact raw count')
    return dict(original_variables=n,raw_anf_terms=len(poly),module_dimension=b,
        field_degree=R.d,chain_length=R.e,field_modulus=R.h,
        centroid_dimension=acquired['algebra_dimension'],coordinate_columns=acquired['coordinate_columns'],
        homogeneous_cubic=[dict(exponents=list(a),coefficient=c) for a,c in sorted(H.items())],
        quotient_quadratic=sorted(Q),fit=fit,acquired_pair_template=template,
        count_certificate=count,terminal_evidence=terminal_evidence,
        signed_count=signed,zero_count=((1<<n)+signed)//2,seconds=time.perf_counter()-started)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--field-bit-budget',type=int,default=24)
    args=parser.parse_args();source=json.loads(args.input.read_text())
    result=compile_pair_family(source['polynomial'],source['n'],field_bit_budget=args.field_bit_budget)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
