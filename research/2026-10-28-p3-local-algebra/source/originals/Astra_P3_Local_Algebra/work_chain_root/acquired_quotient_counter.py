#!/usr/bin/env python3
"""Raw Boolean cubic -> acquired homogeneous ring phase -> weighted critical rays."""
from quotient_homogeneous_compiler import *
sys.path.insert(0,str(ROOT/'work_stationary_prior_agent'))
from homogeneous_chain_counter import weighted_homogeneous_sum

def compile_quotient(poly,n,*,terminal_bit_budget=24,field_terminal=None,
                     residual_bit_budget=None):
    started=time.perf_counter();poly=set(poly);acquired=acquire_chain(poly,n)
    H,noise,fit=(acquire_minimum_quotient(acquired) if residual_bit_budget is not None
                 else fit_homogeneous_quotient(acquired))
    signed,certificate=weighted_homogeneous_sum(acquired['h'],acquired['e'],H,noise,
        terminal_bit_budget=terminal_bit_budget,field_terminal=field_terminal,
        residual_bit_budget=residual_bit_budget)
    if abs(signed)>1<<n or ((1<<n)+signed)&1:raise AssertionError('invalid exact count')
    return dict(original_variables=n,raw_anf_terms=len(poly),field_degree=acquired['d'],
        chain_length=acquired['e'],field_modulus=acquired['h'],centroid_dimension=acquired['algebra_dimension'],
        coordinate_columns=acquired['coordinate_columns'],
        homogeneous_cubic=[dict(exponents=list(a),coefficient=c) for a,c in sorted(H.items())],
        quotient_quadratic=sorted(noise),fit=fit,count_certificate=certificate,
        signed_count=signed,zero_count=((1<<n)+signed)//2,seconds=time.perf_counter()-started)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--terminal-bit-budget',type=int,default=24)
    parser.add_argument('--residual-bit-budget',type=int,
                        help='acquire minimum quotient height and allow one explicitly budgeted residual')
    args=parser.parse_args();source=json.loads(args.input.read_text())
    result=compile_quotient(source['polynomial'],source['n'],terminal_bit_budget=args.terminal_bit_budget,
                            residual_bit_budget=args.residual_bit_budget)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
