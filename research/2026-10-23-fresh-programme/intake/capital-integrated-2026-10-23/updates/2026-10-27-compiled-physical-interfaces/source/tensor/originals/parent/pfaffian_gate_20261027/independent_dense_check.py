"""Root direct original-basis oracle for the independent modular backend."""
import sys
sys.dont_write_bytecode=True
import importlib.util
from pathlib import Path
from itertools import product
import json
import hashlib

base=Path(__file__).resolve().parents[2]
source=base/'alternative/hidden_representation_comparator_20261027/finite_field_gate_check.py'
spec=importlib.util.spec_from_file_location('readonly_fkt',source)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def oracle(rotation,edges,tensors):
    ei={e:k for k,e in enumerate(edges)}
    z=0
    numerators=[[0,0] for _ in edges]
    for bits in product((0,1),repeat=len(edges)):
        value=1
        for v,ws in rotation.items():
            local=tuple(bits[ei[tuple(sorted((v,w)))]] for w in ws)
            value*=tensors[v][local]
        z+=value
        for k,bit in enumerate(bits):numerators[k][bit]+=value
    assert all(sum(row)==z for row in numerators)
    return z,numerators

def main():
    rotation,edges=mod.prism(3)
    cases=[]
    for odd in (False,True):
        _,dense=mod.tensors(rotation,edges,odd=odd)
        z,nums=oracle(rotation,edges,dense)
        residues=[]
        for p in (79,83):
            r=mod.modular_stage(rotation,edges,dense,p)
            assert r['residue']==z%p
            residues.append({'p':p,**r})
        if odd:
            assert z==0 and any(x for pair in nums for x in pair)
        cases.append({'odd_parity':odd,'exact_original_contraction':z,
          'original_bit_numerators':nums,'modular_results':residues})
    result={'scope':'root direct enumeration of all512 ORIGINAL dense edge assignments',
      'backend_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'vertices':6,'edges':len(edges),'cases':cases,
      'novelty_or_performance_claim':False}
    Path(__file__).with_name('INDEPENDENT_DENSE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
