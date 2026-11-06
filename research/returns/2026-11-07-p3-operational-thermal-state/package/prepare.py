"""Compile a supplied collective model and draw ONE fresh mixture component.

Usage: python prepare.py EXAMPLE_REQUEST.json --output generated
This emits logical gates; it does not operate hardware. Redraw a component
before EACH independently requested Gibbs preparation. Repeating one fixed
component circuit does not implement the full thermal mixture.
"""
import argparse,json,random
from pathlib import Path
from fractions import Fraction as Q
from threadpoolctl import threadpool_limits
from certified_blocks import compile_blocks,serializable
from logical_circuit import sample_component,emit_component

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('request'); parser.add_argument('--output',default='generated')
    parser.add_argument('--demonstration-seed',type=int,default=None,
                        help='Reproducible diagnostic only; not fresh physical randomness.')
    a=parser.parse_args(); request=json.loads(Path(a.request).read_text()); out=Path(a.output)
    out.mkdir(parents=True,exist_ok=True)
    coeff={tuple(row['alpha']):Q(row['coefficient']) for row in request['coefficients']}
    blocks,cert=compile_blocks(request['N'],coeff,Q(request['beta']),
                              tuple(map(Q,request.get('window',['-1','1']))),
                              bits=request.get('matrix_bits',144),terms=request.get('Taylor_terms',64))
    if a.demonstration_seed is None: b,rank,failed,bits=sample_component(blocks)
    else: b,rank,failed,bits=sample_component(blocks,random.Random(a.demonstration_seed).getrandbits)
    circuit,meta=emit_component(b,rank,request.get('angle_bits',48))
    meta.update(random_bits_used=bits,capped_sampling_fallback=failed,
                demonstration_seed=a.demonstration_seed,
                instruction='Freshly draw J and multiplicity rank for each copy; discard classical label and purifier in the output contract.')
    (out/'blocks.json').write_text(json.dumps(serializable({'blocks':blocks,'certificate':cert}),indent=2)+'\n')
    (out/'component.json').write_text(json.dumps(serializable({'meta':meta,'gates':circuit.gates}),indent=2)+'\n')
    print(json.dumps(meta,indent=2))

if __name__=='__main__':
    with threadpool_limits(limits=1): main()
