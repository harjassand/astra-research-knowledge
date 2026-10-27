#!/usr/bin/env python3
"""H/diagonal path compiler; exact finite checks, not the asymptotic solver."""
import json, random
from collections import defaultdict
from pathlib import Path
from program_phase_compiler import truncated_phase, cyclo_power, cyclo_mul, conjugate

def paths(n, b, gates):
    # A wire is a constant if negative: -1 encodes zero, -2 encodes one.
    wires, terms, h = [-1]*n, defaultdict(int), 0
    q = 1 << b
    def add_monomial(indices, coefficient):
        if any(wires[i] == -1 for i in indices): return
        mask = 0
        for i in indices:
            if wires[i] >= 0: mask |= 1 << wires[i]
        terms[mask] += coefficient
    for op, indices, e in gates:
        if op == 'h':
            i = indices[0]
            if wires[i] >= 0: terms[(1 << h) | (1 << wires[i])] += q//2
            elif wires[i] == -2: terms[1 << h] += q//2
            wires[i] = h
            h += 1
        elif op == 'phase':
            add_monomial(indices, e)
        elif op == 'table':
            # Index bit j is the value on indices[j]. Boolean Mobius
            # interpolation is exact over Z/qZ; no division is used.
            if len(e) != 1 << len(indices): raise ValueError('table length')
            coeff = [v % q for v in e]
            for j in range(len(indices)):
                for mask in range(len(coeff)):
                    if mask >> j & 1:
                        coeff[mask] = (coeff[mask]-coeff[mask ^ (1 << j)]) % q
            for mask,c in enumerate(coeff):
                if c: add_monomial([i for j,i in enumerate(indices) if mask >> j & 1], c)
        else:
            raise ValueError('unknown gate')
    return h, [(s,c%q) for s,c in terms.items() if c%q], wires

def reduce_boundary(nvars, terms, equations, q):
    parent = list(range(nvars+2))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    def enc(i): return i if i >= 0 else nvars+(-1-i)
    for i,j in equations: parent[root(enc(i))] = root(enc(j))
    zero, one = root(nvars), root(nvars+1)
    if zero == one: return None
    free = sorted({root(i) for i in range(nvars)}-{zero,one})
    renumber = {r:i for i,r in enumerate(free)}
    out = defaultdict(int)
    for mask, c in terms:
        new, vanish = 0, False
        for i in range(nvars):
            if not (mask >> i & 1): continue
            r = root(i)
            if r == zero: vanish = True; break
            if r != one: new |= 1 << renumber[r]
        if not vanish: out[new] += c
    return len(free), [(s,c%q) for s,c in out.items() if c%q]

def amplitude(n,b,gates,y):
    h,terms,wires = paths(n,b,gates)
    eq = [(v,-1-((y>>i)&1)) for i,v in enumerate(wires)]
    return h,reduce_boundary(h,terms,eq,1<<b)

def marginal(n,b,gates,a,z):
    h,terms,wires = paths(n,b,gates)
    both = terms+[(s<<h,-c) for s,c in terms]
    eq=[]
    for i,u in enumerate(wires):
        v=u+h if u>=0 else u
        if i<a: eq += [(u,-1-((z>>i)&1)),(v,-1-((z>>i)&1))]
        else: eq += [(u,v)]
    return h,reduce_boundary(2*h,both,eq,1<<b)

def statevector(n,b,gates):
    d=1<<(b-1)
    vec=[(0,)*d for _ in range(1<<n)]
    vec[0]=(1,)+(0,)*(d-1)
    h=0
    for op,indices,e in gates:
        if op=='h':
            bit=1<<indices[0]
            for x in range(1<<n):
                if x&bit: continue
                p,v=vec[x],vec[x|bit]
                vec[x]=tuple(a+c for a,c in zip(p,v))
                vec[x|bit]=tuple(a-c for a,c in zip(p,v))
            h+=1
        elif op=='phase':
            mask=sum(1<<i for i in set(indices))
            phase=cyclo_power(e,d)
            for x in range(1<<n):
                if x&mask==mask: vec[x]=cyclo_mul(vec[x],phase)
        elif op=='table':
            if len(e) != 1 << len(indices): raise ValueError('table length')
            for x in range(1<<n):
                entry=sum(((x>>i)&1)<<j for j,i in enumerate(indices))
                vec[x]=cyclo_mul(vec[x],cyclo_power(e[entry],d))
        else:
            raise ValueError('unknown gate')
    return h,vec

def validate():
    rng=random.Random(27042026)
    fixtures=[]
    amp_checks=marg_checks=0
    for n in [2,3]:
        for b in [1,2,3]:
            for rep in range(4):
                gates=[('h',[i],0) for i in range(n)]
                for gi in range(5*n):
                    if gi in [n,3*n]: gates.append(('h',[rng.randrange(n)],0))
                    indices=rng.sample(range(n),rng.randint(1,n))
                    if rep < 2:
                        gates.append(('phase',indices,rng.randrange(1,1<<b)))
                    else:
                        gates.append(('table',indices,[rng.randrange(1<<b) for _ in range(1<<len(indices))]))
                h,vec=statevector(n,b,gates)
                d=len(vec[0])
                for y,expected in enumerate(vec):
                    hh,reduced=amplitude(n,b,gates,y)
                    actual=(0,)*d if reduced is None else truncated_phase(*reduced,b)[0]
                    assert h==hh and actual==expected
                    amp_checks+=1
                for a in range(n+1):
                    for z in range(1<<a):
                        hh,reduced=marginal(n,b,gates,a,z)
                        actual=(0,)*d if reduced is None else truncated_phase(*reduced,b)[0]
                        expected=[0]*d
                        for y,v in enumerate(vec):
                            if y&((1<<a)-1)==z:
                                norm=cyclo_mul(v,conjugate(v))
                                expected=[u+w for u,w in zip(expected,norm)]
                        assert h==hh and actual==tuple(expected)
                        marg_checks+=1
                fixtures.append({'qubits':n,'phase_order':1<<b,'hadamards':h,'diagonal_gates':5*n,
                                 'gate_description':'monomial' if rep < 2 else 'arbitrary local table'})
    assert amplitude(2,3,[('h',[0],0)],2)[1] is None
    assert marginal(2,3,[('h',[0],0)],2,2)[1] is None
    constants=[('table',[0,1],[3,2,1,0])]
    hc,vc=statevector(2,3,constants)
    hr,rc=amplitude(2,3,constants,0)
    assert hc==hr==0 and truncated_phase(*rc,3)[0]==vc[0]
    hr,rc=marginal(2,3,constants,0,0)
    assert hr==0 and truncated_phase(*rc,3)[0]==(1,0,0,0)
    return {'status':'all assertions passed','seed':27042026,
            'backend':'exact state vectors versus finite compiled sums; not the asymptotic counter',
            'raw_circuits':len(fixtures),'fixtures':fixtures,
            'exact_amplitude_checks':amp_checks,'exact_marginal_checks':marg_checks,
            'inconsistent_boundary_checks':2,
            'constant_wire_table_checks':2,
            'amplitude_normalization':'2^(-h/2)','probability_normalization':'2^(-h)'}

if __name__=='__main__':
    results=validate()
    output=Path(__file__).with_name('hadamard_phase_results.json')
    output.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'output':str(output),'status':results['status']}))
