#!/usr/bin/env python3
"""Exact wide-gate compiler; validation uses brute force, not the ETH counter.
JSON: inputs n; gates [{op: AND|OR,literals:[signed one-based indices]}];
required_outputs [signed indices]. Gate i is indexed n+i+1.
Usage: --validate, or --compile FILE --width K --output FILE.
"""
import argparse,json,math
from itertools import product
from pathlib import Path
from random import Random

def norm(cs):
    out=[]
    for c in cs:
        s=set(c)
        if any(-x in s for x in s): continue
        c=tuple(sorted(s,key=lambda x:(abs(x),x<0)))
        if c not in out: out.append(c)
    return tuple(out)

def compile_circuit(spec):
    n=spec['inputs']; cs=[]; wires=0
    if n<0: raise ValueError('negative input count')
    for i,g in enumerate(spec['gates']):
        y=n+i+1; ls=tuple(g['literals']); wires+=len(ls)
        if any(l==0 or abs(l)>=y for l in ls): raise ValueError('noncausal wire')
        if g['op']=='AND': cs.extend([(-y,l) for l in ls]+[(y,)+tuple(-l for l in ls)])
        elif g['op']=='OR': cs.extend([(y,-l) for l in ls]+[(-y,)+ls])
        else: raise ValueError('unsupported gate')
    N=n+len(spec['gates'])
    if any(l==0 or abs(l)>N for l in spec.get('required_outputs',[])): raise ValueError('bad output')
    cs.extend((l,) for l in spec.get('required_outputs',[]))
    return N,norm(cs),wires

def direct(spec,x):
    vs=[None]+list(x)
    for g in spec['gates']:
        ls=[vs[abs(l)] if l>0 else not vs[abs(l)] for l in g['literals']]
        vs.append(all(ls) if g['op']=='AND' else any(ls))
    return all(vs[abs(l)]==(l>0) for l in spec.get('required_outputs',[]))

def sat(cs,x): return all(any(x[abs(l)]==(l>0) for l in c) for c in cs)

def simplify(cs,fix):
    return norm(tuple(l for l in c if abs(l) not in fix) for c in cs
                if not any(abs(l) in fix and fix[abs(l)]==(l>0) for l in c))

def leaves(N,cs,k,stats=None):
    if k<2: raise ValueError('width must be >=2')
    if stats is None: stats={'nodes':0,'leaves':0,'max_a':0,'max_b':0}
    def rec(cs,fix,a,b):
        stats['nodes']+=1; stats['max_a']=max(stats['max_a'],a); stats['max_b']=max(stats['max_b'],b)
        if () in cs: return
        j=next((j for j,c in enumerate(cs) if len(c)>k),None)
        if j is None:
            stats['leaves']+=1; yield {'fixed':fix,'clauses':cs}; return
        H=cs[j][:k]
        yield from rec(norm(cs[:j]+(H,)+cs[j+1:]),fix,a+1,b)
        f={abs(l):l<0 for l in H}
        assert len(f)==k and not(set(f)&set(fix))
        yield from rec(simplify(cs,f),fix|f,a,b+1)
    yield from rec(norm(cs),{},0,0)

def brute_leaf(N,leaf):
    fix=leaf['fixed']; free=[v for v in range(1,N+1) if v not in fix]
    return sum(sat(leaf['clauses'],fix|dict(zip(free,x))) for x in product((False,True),repeat=len(free)))

def validate():
    rng=Random(20261027); records=[]; partitions=0
    for n in range(1,7):
        for s in range(1,7):
            gs=[]
            for i in range(s):
                ls=[rng.choice((-1,1))*rng.randrange(1,n+i+1) for _ in range(rng.randrange(min(2*(n+i+1),10)+1))]
                gs.append({'op':rng.choice(('AND','OR')),'literals':ls})
            spec={'inputs':n,'gates':gs,'required_outputs':[rng.choice((-1,1))*(n+s)]}
            N,cs,W=compile_circuit(spec); target=sum(direct(spec,x) for x in product((False,True),repeat=n))
            assert brute_leaf(N,{'fixed':{},'clauses':cs})==target
            for k in (2,3,4):
                st={'nodes':0,'leaves':0,'max_a':0,'max_b':0}; ls=list(leaves(N,cs,k,st))
                assert sum(brute_leaf(N,l) for l in ls)==target
                M=sum(len(c)>k for c in cs); d=M+N//k
                bound=(d+1)*sum(math.comb(d,j) for j in range(N//k+1))
                assert st['nodes']<=bound and st['max_a']<=M and st['max_b']<=N//k
                assert all(len(c)<=k for l in ls for c in l['clauses'])
                records.append({'n':n,'gates':s,'wires':W,'k':k,'count':target,**st})
    for N in range(3,8):
        for k in (2,3):
            cs=norm([rng.choice((-1,1))*v for v in rng.sample(range(1,N+1),rng.randrange(1,N+1))] for _ in range(5))
            ls=list(leaves(N,cs,k))
            for bits in product((False,True),repeat=N):
                x=dict(zip(range(1,N+1),bits))
                z=sum(all(x[v]==b for v,b in l['fixed'].items()) and sat(l['clauses'],x) for l in ls)
                assert z==int(sat(cs,x)); partitions+=1
    example={'inputs':8,'gates':[{'op':'OR','literals':list(range(1,9))},
        {'op':'AND','literals':list(range(1,9))},{'op':'OR','literals':list(range(-9,0))},
        {'op':'AND','literals':[9,-10,11]},{'op':'OR','literals':[12]+list(range(-8,0))}],
        'required_outputs':[13]}
    N,cs,W=compile_circuit(example); ls=list(leaves(N,cs,3)); target=sum(direct(example,x) for x in product((False,True),repeat=8))
    assert sum(brute_leaf(N,l) for l in ls)==target
    result={'status':'all exact assertions passed','circuit_width_cases':len(records),
        'full_assignment_partition_checks':partitions,'dense_example':{'n':8,'gates':5,'wires':W,'trace_variables':N,'count':target,'leaves':len(ls)},
        'scope':'Compiler executed; leaves counted exhaustively. No asymptotic counter or practical speedup was executed.','cases':records}
    Path(__file__).with_name('wide_compiler_results.json').write_text(json.dumps(result,indent=2)+'\n')
    Path(__file__).with_name('wide_circuit_example.json').write_text(json.dumps(example,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--validate',action='store_true'); p.add_argument('--compile',type=Path)
    p.add_argument('--width',type=int,default=3); p.add_argument('--output',type=Path); a=p.parse_args()
    if a.validate or a.compile is None: validate()
    else:
        if a.output is None: p.error('--output is required')
        spec=json.loads(a.compile.read_text()); N,cs,W=compile_circuit(spec); st={'nodes':0,'leaves':0,'max_a':0,'max_b':0}
        out={'declared_variables':N,'original_inputs':spec['inputs'],'wires':W,'width':a.width,'leaves':list(leaves(N,cs,a.width,st)),'stats':st}
        a.output.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(st))
