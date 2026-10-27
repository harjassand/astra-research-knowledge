#!/usr/bin/env python3
"""Command-line interface; input JSON contains only n and polynomial bit masks."""
import argparse,json
from pathlib import Path
from field_rank_decoder import compile_rank_perturbed
from field_bandwidth import acquire_trace_form,acquire_best_trace_form


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--method',choices=['count','acquire'],default='count',
        help='count uses the implemented triple-product backend; acquire emits a general representation only')
    parser.add_argument('--bandwidth',default='auto',help='general acquisition bandwidth, or auto')
    parser.add_argument('--retain-leaves',action='store_true',help='finite diagnostic only; exponential storage')
    args=parser.parse_args(); data=json.loads(args.input.read_text())
    if args.method=='count' and args.bandwidth not in ('auto','1'):
        parser.error('the implemented count backend supports bandwidth one')
    n=data.get('n',data.get('original_variables'))
    monomials=data.get('polynomial',data.get('raw_polynomial'))
    if monomials is None: parser.error('input must contain polynomial or raw_polynomial')
    poly=set()
    for mask in monomials:
        if mask in poly: poly.remove(mask)
        else: poly.add(mask)
    try:
        if args.method=='count':
            result=compile_rank_perturbed(poly,n,retain_leaf_data=args.retain_leaves)
        elif args.bandwidth=='auto': result=acquire_best_trace_form(poly,n)
        else: result=acquire_trace_form(poly,n,bandwidth=int(args.bandwidth))
    except (ValueError,TypeError) as error:
        parser.exit(2,'Representation route rejected: '+str(error)+'\n')
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
        keys=['original_variables','field_extension_degree','module_dimension',
              'acquired_defect_rank','signed_count','zero_count','certified_field_degree']
        print(json.dumps({k:result[k] for k in keys if k in result}))
    else: print(json.dumps(result,indent=2))


if __name__=='__main__': main()
