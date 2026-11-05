#!/usr/bin/env python3
"""Local, recursively composable repetition gadget; tests are not a proof.

The fixed opcode basis is ID, RESET0, RESET1, COPY(x,y)=(x,x), SWAP,
SORT(x,y)=(x AND y,x OR y).  Every binary instruction is nearest-neighbor.
All unlisted cells execute ID at each tick and are exposed to corruption.

For D>=1 use n=8D+1, t=2D, B>=4n+16.  Each logical cell has n canonical
source slots, n disjoint fresh-output slots, and scratch.  Every output
replica, including BOTH outputs of COPY/SWAP/SORT, has an independent row.
Rows clear scratch, copy sources, sort copies monotonically, and store one
output.  Canonical sources only participate in COPY/SWAP until all rows are
finished.  Then fresh outputs are committed and retired records cleared.
Each child cell holds at most one live parent-level token.  Routing labels
and program counters are mathematical descriptions of the declared immutable
input-independent schedule, not protected mutable physical records.

UNKNOWN intervals represent malformed data without assigning it a consistent
Boolean value across operations.  For partial known inputs the monotone
majority forces the proper value despite t bad input replicas and at most
2D newly contacted source lineages; at most 2D output rows can be contacted.
This is the contract used in the proof; this file only tests finite examples.

All templates are padded to common duration A.  expand() recursively replaces
EVERY inactive coarse cell by a protected ID gadget too.  Width is arity*B**k,
duration A**k.  For fixed n the routed row circuits have A<=C(n)*B.  We use
the computed maximum A so the executable n=9 example remains small; the
proof can choose the uniform loose bound C(n)=100*n**3 and pad further.

Run: python burst_gadget.py --self-test
"""
from __future__ import annotations
import argparse
import itertools as it
import json
import random
from collections import Counter
from dataclasses import dataclass

U = -1
OPS = ('ID', 'RESET0', 'RESET1', 'COPY', 'SWAP', 'SORT')
BIN = {'COPY', 'SWAP', 'SORT'}

def arity(op):
    assert op in OPS
    return 2 if op in BIN else 1

@dataclass(frozen=True)
class Ins:
    op: str
    a: int
    b: int | None = None
    phase: str = ''
    row: int = -1
    @property
    def support(self):
        return (self.a,) if self.b is None else (self.a, self.b)
    def shift(self, offset):
        return Ins(self.op, self.a+offset,
                   None if self.b is None else self.b+offset, self.phase, self.row)

def local(g, width):
    assert g.op in OPS and 0 <= g.a < width
    if g.op in BIN:
        assert g.b == g.a+1 and g.b < width
    else:
        assert g.b is None

def and3(x, y):
    return 0 if 0 in (x, y) else (1 if x == y == 1 else U)

def or3(x, y):
    return 1 if 1 in (x, y) else (0 if x == y == 0 else U)

def apply(s, g):
    a, b = g.a, g.b
    if g.op == 'RESET0': s[a] = 0
    elif g.op == 'RESET1': s[a] = 1
    elif g.op == 'COPY': s[b] = s[a]
    elif g.op == 'SWAP': s[a], s[b] = s[b], s[a]
    elif g.op == 'SORT': s[a], s[b] = and3(s[a], s[b]), or3(s[a], s[b])

def route(op, a, b, phase='', row=-1):
    """Ordered abstract operands; all other tokens return to their positions."""
    assert op in BIN and a != b
    lo, hi = min(a,b), max(a,b)
    path = list(range(hi-1, lo, -1))
    for p in path: yield Ins('SWAP', p, p+1, phase, row)
    if a < b or op == 'SWAP':
        yield Ins(op, lo, lo+1, phase, row)
    elif op == 'COPY':
        for f in ('SWAP', 'COPY', 'SWAP'):
            yield Ins(f, lo, lo+1, phase, row)
    else:
        for f in ('SORT', 'SWAP'):
            yield Ins(f, lo, lo+1, phase, row)
    for p in reversed(path): yield Ins('SWAP', p, p+1, phase, row)

class Family:
    def __init__(self, D=1, B=None):
        assert isinstance(D, int) and D >= 1
        self.D, self.n, self.t = D, 8*D+1, 2*D
        self.B = 4*self.n+16 if B is None else B
        assert self.B >= 4*self.n+16
        self.raw = {op: tuple(self.build(op)) for op in OPS}
        self.lift_raw = tuple(self.build_lift())
        self.descent_raw = tuple(self.build_descent())
        self.A = max(map(len, (*self.raw.values(),self.lift_raw,self.descent_raw)))
        assert self.A <= 100*self.n**3*self.B
    def canonical(self, cell): return tuple(cell*self.B+i for i in range(self.n))
    def fresh(self, cell): return tuple(cell*self.B+self.n+i for i in range(self.n))
    def width(self, op): return arity(op)*self.B
    def build(self, op):
        n, m = self.n, arity(op)
        canonical = set(it.chain.from_iterable(self.canonical(c) for c in range(m)))
        fresh = set(it.chain.from_iterable(self.fresh(c) for c in range(m)))
        scratch = [p for p in range(self.width(op)) if p not in canonical|fresh]
        work = [tuple(2*n+c*n+j for j in range(n)) for c in range(m)]
        median = [w[n//2] for w in work]
        for p in sorted(fresh): yield Ins('RESET0', p, phase='fresh-init')
        for out in range(m):
            for replica in range(n):
                row = out*n+replica
                for p in scratch: yield Ins('RESET0', p, phase='clear', row=row)
                if op.startswith('RESET'):
                    result = 4*n
                    yield Ins(op, result, phase='constant', row=row)
                else:
                    for c in range(m):
                        for a,b in zip(self.canonical(c), work[c]):
                            yield from route('COPY', a,b,'copy-source',row)
                        # Adjacent odd-even transposition sorter, n passes.
                        for r in range(n):
                            for j in range(r%2,n-1,2):
                                yield Ins('SORT',work[c][j],work[c][j+1],'majority',row)
                    if op in ('ID','COPY'): result = median[0]
                    elif op == 'SWAP': result = median[1-out]
                    else:
                        yield from route('SORT',median[0],median[1],'function',row)
                        result = median[out]
                yield from route('COPY',result,self.fresh(out)[replica],'store',row)
        for c in range(m):
            for a,b in zip(self.canonical(c),self.fresh(c)):
                yield from route('SWAP',a,b,'commit')
        for p in range(self.width(op)):
            if p not in canonical: yield Ins('RESET0',p,phase='retire')
    def instructions(self, op):
        yield from self.raw[op]
        for _ in range(self.A-len(self.raw[op])): yield Ins('ID',0,phase='padding')
    def build_lift(self):
        """One valid child at 0 -> n valid canonical children; all-child-good.

        This finite circuit has no D-fault-tolerance claim of its own.  Its
        constituent opcodes are expanded at the current protected level.
        Unused destination hardware can have arbitrary state before RESET.
        """
        for p in range(1,self.B): yield Ins('RESET0',p,phase='lift-reset')
        for p in range(1,self.n): yield from route('COPY',0,p,'lift-copy')
    def build_descent(self):
        """A parent's majority -> valid child 0; all-child-good analysis."""
        for p in range(self.n,self.B): yield Ins('RESET0',p,phase='descent-reset')
        for p in range(self.n):
            yield from route('COPY',p,self.n+p,'descent-copy')
        for r in range(self.n):
            for j in range(r%2,self.n-1,2):
                yield Ins('SORT',self.n+j,self.n+j+1,'descent-majority')
        yield from route('COPY',self.n+self.n//2,0,'descent-output')
        for p in range(1,self.B): yield Ins('RESET0',p,phase='descent-retire')
    def lift(self):
        yield from self.lift_raw
        for _ in range(self.A-len(self.lift_raw)):
            yield Ins('ID',0,phase='lift-padding')
    def descent(self):
        yield from self.descent_raw
        for _ in range(self.A-len(self.descent_raw)):
            yield Ins('ID',0,phase='descent-padding')
    def simulate(self,op,initial,faults=()):
        """Fault=(tick, positions or None, replacement values or None).

        None positions replaces active outputs.  An explicit singleton can
        replace any implicit idle cell.  One fault cannot cover unrelated idles.
        None values means arbitrary outputs represented by UNKNOWN intervals.
        """
        assert len(initial)==self.width(op) and all(x in (0,1,U) for x in initial)
        by_tick = {}
        for tick,positions,values in faults:
            assert 0 <= tick < self.A
            by_tick.setdefault(tick,[]).append((positions,values))
        s = list(initial)
        for tick,g in enumerate(self.instructions(op)):
            apply(s,g)
            for positions,values in by_tick.get(tick,()):
                positions = g.support if positions is None else tuple(positions)
                assert positions and len(set(positions))==len(positions)
                assert len(positions)==1 or positions==g.support
                values = (U,)*len(positions) if values is None else tuple(values)
                assert len(values)==len(positions)
                for p,v in zip(positions,values):
                    assert 0<=p<len(s) and v in (0,1,U)
                    s[p]=v
        return s
    def expand(self, op, level):
        """Lazy tuples of disjoint physical instructions; full idle protection."""
        assert level>=0
        if level==0:
            yield (Ins(op,0,1 if arity(op)==2 else None),)
        else:
            yield from self.expand_circuit(self.instructions(op),self.width(op),level-1)
    def expand_circuit(self,instructions,width,level):
        """Expand a local coarse circuit, including every inactive coarse ID.

        A coarse tick takes A**level physical ticks on width*B**level cells.
        Outside this finite active prefix there are only raw physical idles;
        those cells are RESET when a later lift first uses their information.
        """
        assert level>=0
        for g in instructions:
            local(g,width)
            if level==0:
                yield (g,)
                continue
            groups=[]; p=0
            while p<width:
                op=g.op if p==g.a else 'ID'
                groups.append((self.expand(op,level),p*self.B**level))
                p+=arity(op)
            for _ in range(self.A**level):
                layer=[]
                for generator,offset in groups:
                    layer.extend(h.shift(offset) for h in next(generator))
                yield tuple(layer)
    def memory_layers(self,T,m):
        """Finite seed-to-readout protocol, with T requested holding ticks.

        Only physical cell 0 initially carries the input.  Growth uses the
        first B**k cells at stage k.  Hold for ceil(T/A**m) protected level-m
        ID operations, then descend to physical cell 0 and retain it through
        one final noisy physical ID/read window.  Read cell 0 at completion.
        All lower locations in each lift/descent are included in its union
        bound; no correction of a bad lift/descent location is asserted.
        """
        assert isinstance(T,int) and T>=0 and isinstance(m,int) and m>=0
        for k in range(1,m+1):
            yield from self.expand_circuit(self.lift(),self.B,k-1)
        for _ in range((T+self.A**m-1)//self.A**m):
            yield from self.expand('ID',m)
        for k in range(m,0,-1):
            yield from self.expand_circuit(self.descent(),self.B,k-1)
        yield (Ins('ID',0,phase='terminal-read-window'),)
    def memory_costs(self,T,m):
        """Exact ticks and local-gate counts, charging idles on ALL hardware.

        One binary gate counts as one operation and two cell updates.  The
        permanently installed line has B**m cells even during small prefixes.
        Construction requires that many cells and their adjacent connections;
        energy is obtained by assigning costs to these explicit operations.
        """
        assert isinstance(T,int) and T>=0 and isinstance(m,int) and m>=0
        def histogram(raw):
            h=Counter(g.op for g in raw); h['ID']+=self.A-len(raw); return h
        hist={op:histogram(self.raw[op]) for op in OPS}
        lift_hist,down_hist=histogram(self.lift_raw),histogram(self.descent_raw)
        def binary_count(h,width,lower):
            active=sum(count*lower[op] for op,count in h.items())
            idle=width*self.A-sum(count*arity(op) for op,count in h.items())
            return active+idle*lower['ID']
        lower={op:int(op in BIN) for op in OPS}
        transport_binary=0
        for _ in range(1,m+1):
            transport_binary+=binary_count(lift_hist,self.B,lower)
            transport_binary+=binary_count(down_hist,self.B,lower)
            lower={op:binary_count(hist[op],self.width(op),lower) for op in OPS}
        holding=(T+self.A**m-1)//self.A**m
        stage_ticks=sum(self.A**k for k in range(1,m+1))
        ticks=2*stage_ticks+holding*self.A**m+1
        cells=self.B**m
        binary=transport_binary+holding*lower['ID']
        return dict(physical_cells=cells,preparation_ticks=stage_ticks,
                    hold_repetitions=holding,holding_ticks=holding*self.A**m,
                    descent_ticks=stage_ticks,terminal_ticks=1,total_ticks=ticks,
                    binary_gates=binary,all_cell_updates_including_idle=cells*ticks,
                    all_local_gates_including_idle=cells*ticks-binary)

def outputs(op,bits):
    x=bits[0]
    if op=='ID': return (x,)
    if op=='RESET0': return (0,)
    if op=='RESET1': return (1,)
    y=bits[1]
    if op=='COPY': return (x,x)
    if op=='SWAP': return (y,x)
    return (x&y,x|y)

def forced(op,known):
    poss=[set() for _ in range(arity(op))]
    for bits in it.product(*[(0,1) if b is None else (b,) for b in known]):
        for s,v in zip(poss,outputs(op,bits)): s.add(v)
    return tuple(next(iter(s)) if len(s)==1 else None for s in poss)

def initial(f,op,known,rng,damage=True):
    s=[rng.choice((0,1,U)) for _ in range(f.width(op))]
    for c,b in enumerate(known):
        if b is not None:
            for p in f.canonical(c): s[p]=b
            if damage:
                for p in rng.sample(f.canonical(c),f.t): s[p]=rng.choice((1-b,U))
    return s

def check(f,op,s,known,tolerance=None):
    count=0
    for c,b in enumerate(forced(op,known)):
        if b is not None:
            bad=sum(s[p]!=b for p in f.canonical(c))
            assert bad <= (f.t if tolerance is None else tolerance), (op,known,c,bad)
            count+=1
    return count

def self_test(seed=20261105,trials=32):
    rng=random.Random(seed); f=Family()
    counts=dict(local_instructions=0,router_cases=0,clean_truth_tables=0,
                partial_input_cases=0,random_fault_traces=0,active_faults=0,
                idle_faults=0,forced_output_blocks=0,recursive_layers=0,
                finite_seed_memory_cases=0,descent_with_malformed_children=0)
    for op in OPS:
        for g in f.instructions(op): local(g,f.width(op)); counts['local_instructions']+=1
    for schedule in (f.lift(),f.descent()):
        for g in schedule: local(g,f.B); counts['local_instructions']+=1
    for a,b in it.permutations(range(12),2):
        for op in sorted(BIN):
            s=[rng.randrange(2) for _ in range(12)]; want=s[:]
            want[a],want[b]=outputs(op,(s[a],s[b]))
            for g in route(op,a,b): local(g,12); apply(s,g)
            assert s==want
            counts['router_cases']+=1
    for op in OPS:
        for known in it.product((0,1),repeat=arity(op)):
            s=f.simulate(op,initial(f,op,known,rng,False))
            counts['forced_output_blocks']+=check(f,op,s,known,0)
            counts['clean_truth_tables']+=1
        patterns=list(it.product((None,0,1),repeat=arity(op)))
        for known in patterns:
            s=f.simulate(op,initial(f,op,known,rng))
            counts['forced_output_blocks']+=check(f,op,s,known,0)
            counts['partial_input_cases']+=1
        for trial in range(trials):
            known=patterns[trial%len(patterns)]; tick=rng.randrange(f.A)
            g=f.raw[op][tick] if tick<len(f.raw[op]) else Ins('ID',0)
            if trial%2:
                positions=(rng.choice([p for p in range(f.width(op)) if p not in g.support]),)
                counts['idle_faults']+=1
            else:
                positions=None; counts['active_faults']+=1
            s=f.simulate(op,initial(f,op,known,rng),((tick,positions,None),))
            counts['forced_output_blocks']+=check(f,op,s,known)
            counts['random_fault_traces']+=1
    # Explicit source-refresh check for COPY with fully malformed destination.
    for b in (0,1):
        known=(b,None)
        s=f.simulate('COPY',initial(f,'COPY',known,rng),((len(f.raw['COPY'])//2,None,None),))
        counts['forced_output_blocks']+=check(f,'COPY',s,known)
        counts['random_fault_traces']+=1; counts['active_faults']+=1
    for layer in it.islice(f.expand('SORT',2),3):
        used=set(); assert len(layer)>1
        for g in layer:
            local(g,2*f.B**2); assert not used.intersection(g.support); used.update(g.support)
        counts['recursive_layers']+=1
    # The actual finite-seed wrapper: ONLY cell 0 starts input-dependent.
    # Lift/descent have no injected fault.  One interval-valued active fault
    # occurs during the protected hold; no claim is made to correct lift faults.
    costs=f.memory_costs(T=1,m=1)
    for b in (0,1):
        s=[U]*f.B; s[0]=b
        tick_count=binary_count=0
        fault_tick=f.A+len(f.raw['ID'])//2
        for tick,layer in enumerate(f.memory_layers(T=1,m=1)):
            for g in layer:
                local(g,f.B); apply(s,g); binary_count+=int(g.op in BIN)
            if tick==fault_tick:
                for p in layer[0].support: s[p]=U
            tick_count+=1
        assert s[0]==b
        assert tick_count==costs['total_ticks']
        assert binary_count==costs['binary_gates']
        assert f.B*tick_count-binary_count==costs['all_local_gates_including_idle']
        counts['finite_seed_memory_cases']+=1
        # The explicit descent also works on t entirely malformed children.
        s=[U]*f.B
        for p in range(f.n-f.t): s[p]=b
        for g in f.descent(): apply(s,g)
        assert s[0]==b
        counts['descent_with_malformed_children']+=1
    return dict(status='passed',seed=seed,D=f.D,n=f.n,t=f.t,B=f.B,A=f.A,
                raw_lengths={op:len(f.raw[op]) for op in OPS},
                lift_raw_length=len(f.lift_raw),descent_raw_length=len(f.descent_raw),
                memory_example_costs=costs,counts=counts,
                scope='Finite-gadget validation, not proof of the multiscale theorem.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--self-test',action='store_true')
    p.add_argument('--seed',type=int,default=20261105)
    p.add_argument('--trials',type=int,default=32)
    a=p.parse_args()
    if a.self_test: print(json.dumps(self_test(a.seed,a.trials),indent=2))
    else:
        f=Family(); print(json.dumps(dict(D=f.D,n=f.n,t=f.t,B=f.B,A=f.A),indent=2))
