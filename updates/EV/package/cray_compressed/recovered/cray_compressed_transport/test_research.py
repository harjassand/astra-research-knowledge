from __future__ import annotations
from fractions import Fraction as F
import json,time,copy
import numpy as np
from cylinder_flow import line_exchange
from invariant_pivot import *
from frame_grammar import *
from probability_certificate import evaluate


def test_small_flow():
    tested=0
    for m in range(2,6):
        flow=direct_all_pivots(m)
        p=F(4,5);energy=F()
        for z in range(1<<(2*m)):
            a=np.array([[(z>>y)&1,(z>>(m+y))&1] for y in range(m)],dtype=np.uint8)
            div=F(); e=F()
            for b in flow.terms:
                j=normalized_current(flow,z,b);div+=j;e+=j*j
                zz=z ^ ((1<<b[0])|(1<<b[1])) if ((z>>b[0])^(z>>b[1]))&1 else z
                assert normalized_current(flow,zz,b)==-j
                if j:
                    s=tuple((i%m,i//m) for i in b)
                    assert legal(a,s) and a[s[0]]!=a[s[1]]
            Aempty=(z&((1<<m)-1))==0
            Bempty=(z>>m)==0
            Anonfull=(z&((1<<m)-1))!=((1<<m)-1)
            Bnonfull=(z>>m)!=((1<<m)-1)
            assert div==int(Aempty and Bnonfull)-int(Bempty and Anonfull)
            n=z.bit_count();energy+=p**n*(1-p)**(2*m-n)*e;tested+=1
        assert energy==exact_energy(m,p)
    return tested


def symbolic_growth():
    checks=0;instructions=0
    for h in range(2,9):
        for w in range(2,9):
            rect=(2,2,2+h,2+w)
            for direction in ('R','L','U','D'):
                new=strip(rect,direction)
                for r in range(len(new)):
                    zero={(y,2) for y in range(2,2+h)}|{(2,x) for x in range(2,2+w)}|{new[r]}
                    word=Instruction('grow',(rect,direction,r)).word()
                    for u,v in word:
                        assert abs(u[0]-v[0])+abs(u[1]-v[1])==1
                        for a,b in ((u,v),(v,u)):
                            y,x=a
                            assert any(z in zero and z!=b for z in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
                        zu=u in zero;zv=v in zero
                        zero.discard(u);zero.discard(v)
                        if zu:zero.add(v)
                        if zv:zero.add(u)
                    y0,x0,y1,x1=extend(rect,direction)
                    assert {(y,x0) for y in range(y0,y1)}|{(y0,x) for x in range(x0,x1)}<=zero
                    checks+=1;instructions+=len(word)
    return dict(growth_cases=checks,microscopic_instructions=instructions)


def dense_module_tests():
    rng=np.random.default_rng(20261013)
    cases=[];attempts=0;movechecks=0
    for L,vertical in ((4,False),(8,False),(8,True),(16,False)):
        shape=(2*L,L) if vertical else (L,2*L)
        ports=((L//2,L//2),((3*L//2,L//2) if vertical else (L//2,3*L//2)))
        # Independent rejection sampling for each good block, not for a
        # pair of rare events. These draws have no role in any probability proof.
        blocks=[];block_trials=[]
        for which in range(2):
            for attempt in range(200000):
                block=(rng.random((L,L))<.8).astype(np.uint8);attempts+=1
                forced=block.copy();forced[L//2,L//2]=1
                if Gate(forced).good((0,0,L,L)):
                    blocks.append(block);block_trials.append(attempt+1);break
            else:raise AssertionError('no accepted dense test configuration')
        a=np.concatenate(blocks,axis=0 if vertical else 1)
        module=make_module(a,ports)
        word=list(module.word());assert len(word)<=96*L**3
        # Every reservoir is tested with all four port assignments.
        for pa,pb in ((0,0),(0,1),(1,0),(1,1)):
            x=a.copy();x[ports[0]]=pa;x[ports[1]]=pb;expected=x.copy()
            expected[ports[0]]=pb;expected[ports[1]]=pa
            for s in word:
                assert legal(x,s),(L,vertical,s,x)
                apply(x,s);movechecks+=1
            assert np.array_equal(x,expected)
            other=make_module(x,ports)
            assert other.preparation==module.preparation and other.port_positions==module.port_positions
        cases.append(dict(L=L,vertical=vertical,random_trials_for_each_block=block_trials,
                          compressed_instructions=len(module.preparation),microscopic_swaps=len(word)))
    return dict(cases=cases,draws=attempts,checked_moves=movechecks,
                caveat='Random tests are diagnostics; not estimates used in a certificate.')


def run():
    t=time.perf_counter()
    for m in range(2,33):
        f=direct_all_pivots(m)
        assert f.terms==line_exchange(m,True).terms
        assert sum(map(len,f.terms.values()))==8*m-10
        assert f.energy_polynomial()==unnormalized_polynomial(m)
        assert line_exchange(m).energy(F(4,5))==first_pivot_energy(m,F(4,5))
        assert all(e>=0 for e in sector_energies(m))
    states=test_small_flow(); growth=symbolic_growth();dense=dense_module_tests()
    # Adversarial corruption must break at least one source equation.
    f=direct_all_pivots(3);bond=next(iter(f.terms));c=next(iter(f.terms[bond]));f.terms[bond][c]+=1
    assert any(sum(f.current(z,b) for b in f.terms)!=
               (sum(k for (zz,oo),k in f.initial.items() if not(z&zz) and z&oo==oo)
                -sum(k for (zz,oo),k in f.final.items() if not(z&zz) and z&oo==oo))
               for z in range(64))
    cert=evaluate();assert cert['exponent']==52114
    return dict(status='passed',symbolic_sizes_checked='2 through 32',
                exhaustive_primitive_states=states,growth=growth,dense_module_tests=dense,
                corrupted_current_rejected=True,dense_bound_exponent=cert['exponent'],
                wall_seconds=time.perf_counter()-t)

if __name__=='__main__':print(json.dumps(run(),indent=2))
