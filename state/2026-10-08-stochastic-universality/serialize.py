#!/usr/bin/env python3
"""Polynomial-size Petri reachability reduction to binary chemistry.
Preserves canonical-idle reachability, NOT original stochastic rates or time.
Exactly one controller implies nonexplosion on valid initial states.
The full-rank wrapper gives order <=5, or <=7 after the positive offset.
"""
from __future__ import annotations
import argparse, json
from fractions import Fraction
from pathlib import Path
from typing import Sequence, Any
from compiler import Reaction, load, compile_network


def serialize(original: Sequence[Reaction]) -> tuple[list[Reaction],dict[str,Any]]:
    if not original:
        raise ValueError('At least one reaction is required.')
    d=len(original[0].source)
    if any(len(r.source)!=d for r in original):
        raise ValueError('Dimension mismatch.')
    levels=[max(1,max(max(r.source[i],r.target[i]) for r in original).bit_length()) for i in range(d)]
    names=[]; bundles=[]
    for i,L in enumerate(levels):
        row=[]
        for k in range(L):
            row.append(len(names));names.append(f'X{i}_bundle_{k}')
        bundles.append(row)
    idle=len(names);names.append('IDLE')
    controls=[idle]
    sparse=[]
    def new_control(name):
        idx=len(names);names.append(name);controls.append(idx);return idx
    def add(src,dst):
        sparse.append((dict(src),dict(dst)))
    for i,L in enumerate(levels):
        for k in range(L-1):
            lo,hi=bundles[i][k],bundles[i][k+1]
            pack=new_control(f'PACK_{i}_{k}')
            unpack=new_control(f'UNPACK_{i}_{k}')
            add({idle:1,lo:1},{pack:1})
            add({pack:1,lo:1},{idle:1,hi:1})
            add({idle:1,hi:1},{unpack:1,lo:1})
            add({unpack:1},{idle:1,lo:1})
    for t,r in enumerate(original):
        consume=[bundles[i][k] for i in range(d) for k in range(levels[i]) if (r.source[i]>>k)&1]
        produce=[bundles[i][k] for i in range(d) for k in range(levels[i]) if (r.target[i]>>k)&1]
        current=new_control(f'TRANSITION_{t}_0')
        add({idle:1},{current:1})
        step=0
        for b in consume:
            step+=1; nxt=new_control(f'TRANSITION_{t}_{step}')
            add({current:1,b:1},{nxt:1});current=nxt
        # No output is exposed until every input has been consumed.
        for b in produce:
            step+=1;nxt=new_control(f'TRANSITION_{t}_{step}')
            add({current:1},{nxt:1,b:1});current=nxt
        add({current:1},{idle:1})
    n=len(names)
    reactions=[]
    for s,t in sparse:
        src=tuple(s.get(i,0) for i in range(n));dst=tuple(t.get(i,0) for i in range(n))
        reactions.append(Reaction(src,dst,Fraction(1)))
    assert all(sum(r.source)<=2 and sum(r.target)<=2 for r in reactions)
    assert all(sum(r.source[i] for i in controls)==1 and sum(r.target[i] for i in controls)==1 for r in reactions)
    meta={'species_names':names,'bundle_indices':bundles,'control_indices':controls,'idle_index':idle,
          'original_species':d,'serialized_species':n,'serialized_reactions':len(reactions),
          'source_order':max(sum(r.source) for r in reactions),'target_order':max(sum(r.target) for r in reactions),
          'all_rates':'1','preserves':'canonical-idle reachability, not original rates or time',
          'nonexplosion_scope':'initial states with exactly one control token',
          'encoding':'binary stoichiometries retained via polynomially many bundle levels'}
    return reactions,meta


def encode(x:Sequence[int],meta:dict[str,Any])->tuple[int,...]:
    if len(x)!=meta['original_species'] or any(type(v)is not int or v<0 for v in x):
        raise ValueError('Invalid original state.')
    out=[0]*meta['serialized_species']
    out[meta['idle_index']]=1
    for i,v in enumerate(x):out[meta['bundle_indices'][i][0]]=v
    return tuple(out)


def decode(x:Sequence[int],meta:dict[str,Any])->tuple[int,...]:
    return tuple(sum((1<<k)*x[idx] for k,idx in enumerate(row)) for row in meta['bundle_indices'])


def positive_offset(reactions: Sequence[Reaction]) -> list[Reaction]:
    """Preserve the graph under x -> x+1, not the numerical jump rates."""
    return [Reaction(tuple(a+int(a>0) for a in r.source),
                     tuple(b+int(a>0) for a,b in zip(r.source,r.target)), r.rate)
            for r in reactions]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--wrap',action='store_true',help='Apply full-rank strongly endotactic wrapper.')
    p.add_argument('--positive',action='store_true',help='Positive-offset graph encoding, then optional wrapper.')
    args=p.parse_args()
    data=json.loads(args.input.read_text());orig=load(args.input)
    rs,meta=serialize(orig)
    result={'serialization':meta}
    for field in ('start','target'):
        if field in data:
            result[field]=list(encode(data[field],meta))
    if args.positive:
        rs=positive_offset(rs)
        result['positive_offset']='canonical states shifted by all-ones; graph preserved, rates changed'
        for field in ('start','target'):
            if field in result:result[field]=[v+1 for v in result[field]]
    if args.wrap:
        rs,wrapper_meta=compile_network(rs,mode='full_rank')
        result['wrapper']=wrapper_meta
        for field in ('start','target'):
            if field in result:result[field]+=[1,1]
    result['reactions']=[r.as_dict() for r in rs]
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='reactions'},indent=2))

if __name__=='__main__':main()
