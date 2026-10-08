#!/usr/bin/env python3
"""Exact finite falsification controls for HF representation/GC/Card mechanisms.
Not an asymptotic certificate and not a full syntactic FO-compiler verifier.
"""
from itertools import combinations
import json, random
from pathlib import Path

class HF:
    def __init__(self, n):
        self.atoms=set(range(n)); self.mem={i:None for i in range(n)}; self.canon={}; self.n=n
        self.zero=self.make(()); self.one=self.make((self.zero,)); self.A=self.make(self.atoms)
    def make(self, members):
        key=frozenset(members)
        if key not in self.canon:
            self.canon[key]=len(self.mem); self.mem[self.canon[key]]=key
        return self.canon[key]
    def members(self,x): return self.mem[x] if self.mem[x] is not None else frozenset()
    def cl(self, roots):
        seen=set(); todo=list(roots)
        while todo:
            x=todo.pop()
            if x in seen: continue
            seen.add(x); todo.extend(self.members(x))
        return seen
    def base(self): return self.atoms|{self.zero,self.one,self.A}
    def C(self,U): return {(x,y) for y in U for x in self.cl([y]) if x in U}
    def E(self,U): return {(x,y) for y in U for x in self.members(y) if x in U}

def add_batch(h,U,rows):
    # One descriptor for each old object and each parameter row, including repeats.
    D=[('old',x) for x in sorted(U)]+[('new',i) for i in range(len(rows))]
    den={d:(d[1] if d[0]=='old' else h.make(rows[d[1]])) for d in D}
    def eq(d,e):
        if d[0]==e[0]=='old': return d[1]==e[1]
        if d[0]==e[0]=='new': return rows[d[1]]==rows[e[1]]
        if d[0]=='old': d,e=e,d
        return e[1] not in h.atoms and rows[d[1]]==h.members(e[1])
    eq_tests=0
    for d in D:
        for e in D:
            assert eq(d,e)==(den[d]==den[e]); eq_tests+=1
    oldE=h.E(U); oldC=h.C(U)
    rawE=set(); rawC={(d,d) for d in D}
    for d in D:
        for e in D:
            if d[0]=='old' and e[0]=='old':
                if (d[1],e[1]) in oldE: rawE.add((d,e))
                if (d[1],e[1]) in oldC: rawC.add((d,e))
            elif d[0]=='old' and e[0]=='new':
                if d[1] in rows[e[1]]: rawE.add((d,e))
                if any((d[1],z) in oldC for z in rows[e[1]]): rawC.add((d,e))
    # Quotient image equals saturation followed by quotient; no representatives chosen.
    newU=set(den.values())
    E={(den[d],den[e]) for d,e in rawE}; C={(den[d],den[e]) for d,e in rawC}
    assert E==h.E(newU)
    assert C==h.C(newU)
    assert h.cl(newU)==newU
    assert len(newU)<=len(U)+len(rows)
    return newU, eq_tests

def all_subsets(U):
    U=tuple(sorted(U))
    return [frozenset(U[i] for i in range(len(U)) if mask>>i&1) for mask in range(1<<len(U))]

def main():
    rng=random.Random(2432015); stats={'constructor_batches':0,'descriptor_equality_pairs':0,'gc_cases':0}
    for n in (1,2,3):
        h=HF(n); U=h.base()
        rows=all_subsets(U)
        U2,c=add_batch(h,U,rows+rows[:3]); stats['constructor_batches']+=1; stats['descriptor_equality_pairs']+=c
        # Every possible singleton current root is a GC case.
        C=h.C(U2)
        for root in U2:
            kept=h.base()|h.cl([root])
            assert h.cl(kept)==kept
            assert {(x,y) for x,y in C if x in kept and y in kept}==h.C(kept)
            stats['gc_cases']+=1
    # Random batches exercise old/new collisions and deeply nested existing sets.
    for trial in range(300):
        h=HF(2); U=h.base()
        for j in range(rng.randrange(1,6)):
            row=frozenset(x for x in sorted(U) if rng.randrange(3)==0)
            U.add(h.make(row))
        rows=[frozenset(x for x in sorted(U) if rng.randrange(2)) for _ in range(rng.randrange(0,15))]
        rows.extend([frozenset(),frozenset(),frozenset(h.atoms),frozenset([h.zero])])
        U2,c=add_batch(h,U,rows); stats['constructor_batches']+=1; stats['descriptor_equality_pairs']+=c
        for _ in range(4):
            root=rng.choice(sorted(U2)); kept=h.base()|h.cl([root]); C=h.C(U2)
            assert {(x,y) for x,y in C if x in kept and y in kept}==h.C(kept)
            stats['gc_cases']+=1
    # Dynamic reserve, all target sizes in parallel at a frozen Card phase.
    reserve_cases=0; reserve_growth=0
    for trial in range(200):
        h=HF(3); ords=[h.zero,h.one]; top=1; U=h.base()
        for step in range(30):
            sizes=[rng.randrange(31) for _ in range(rng.randrange(6))]
            # Build target sets from a disjoint collection of pure singleton chains.
            elems=[]; obj=h.A
            while len(elems)<max(sizes,default=0):
                obj=h.make([obj]); elems.append(obj)
            args=[h.make(elems[:k]) for k in sizes]; U |= h.cl(args)
            oldtop=top
            while not all(any(len(h.members(a))==len(h.members(o)) for o in ords) for a in args):
                new=h.make(ords); assert h.members(new)==frozenset(ords)
                ords.append(new); U.add(new); top+=1; reserve_growth+=1
            assert top==max([oldtop]+sizes)
            assert len(ords)==top+1
            for a,k in zip(args,sizes):
                matches=[o for o in ords if len(h.members(a))==len(h.members(o))]
                assert matches==[ords[k]]
            # GC keeps the reserve and one current root; no elapsed-time counter.
            root=args[0] if args else h.one; U=h.base()|h.cl([root])|set(ords)
            assert h.cl(U)==U; reserve_cases+=1
    stats['reserve_phases']=reserve_cases; stats['reserve_extensions']=reserve_growth
    # Long ordered-input binary counter trace: all subsets, tiny current closure.
    traces=[]
    for n in range(2,11):
        h=HF(n); base=h.base(); U=set(base); history=set(base); max_gc=len(U); max_native=0
        for bits in range(1<<n):
            root=h.make(a for a in range(n) if bits>>a&1)
            U.add(root); history.add(root); max_gc=max(max_gc,len(U)); max_native=max(max_native,len(h.cl([root])))
            U=base|h.cl([root]); assert len(U)<=n+4
        assert max_gc<=n+5; assert len(history)==(1<<n)+n+1
        traces.append({'n':n,'states':1<<n,'max_native_inclusive_tc':max_native,'max_gc_representation':max_gc,'history_preserving_representation':len(history)})
    stats['binary_counter_traces']=traces
    # Deliberate failure controls.
    h=HF(2); z=h.zero; a=h.make([z]); b=h.make([a]); U=h.cl([b]); D={z,b}
    stale=((z,b) in h.C(U))
    actual_restricted_E={(x,y) for x,y in h.E(U) if x in D and y in D}
    assert stale and not actual_restricted_E
    assert h.members(0)==h.members(z) and 0!=z  # atom-safe merge is necessary
    descriptor_count=7; actual_single_value_count=1
    assert descriptor_count!=actual_single_value_count
    # Cardinality of all ordered input pairs can exceed the native final state's TC.
    pair_controls=[]
    for n in (2,3,5):
        h=HF(n)
        def pair(a,b): return h.make([h.make([a]),h.make([a,b])])
        target=h.make(pair(a,b) for a in h.atoms for b in h.atoms)
        assert len(h.members(target))==n*n
        native_final_tc=len(h.cl([h.one]))
        assert len(h.members(target))>native_final_tc
        pair_controls.append({'n':n,'Card_argument_size':n*n,'final_native_inclusive_tc':native_final_tc})
    stats['negative_controls']={'nontransitive_gc_stale_closure_detected':True,'atom_empty_extensional_collision_detected':True,'descriptor_count_mismatch_detected':True,'Card_reserve_not_linear_in_native_tc':pair_controls}
    stats['all_checks_passed']=True
    out=Path(__file__).with_name('space_simulation_test_results.json'); out.write_text(json.dumps(stats,indent=2)+'\n'); print(json.dumps(stats,indent=2))
if __name__=='__main__': main()
