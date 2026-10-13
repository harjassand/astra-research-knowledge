"""Finite diagnostics for the balanced grammar; not a numerical proof of tails."""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
import json,time
import numpy as np
from frame_grammar import Gate,strip,extend,legal,apply
from balanced_grammar import BalancedInstruction,make_balanced_module,sample_weight
from balanced_certificate import exact_strip_moment,frame_moment_upper,evaluate


def test_strip_density():
    p=F(4,5);q=1-p;states=0
    for m in range(1,11):
        output=defaultdict(F)
        for z in range(1<<m):
            zeros=[r for r in range(m) if not(z>>r)&1]
            if not zeros:continue
            initial=p**z.bit_count()*q**(m-z.bit_count())
            for r in zeros:
                shifted=sum(((z>>((i+r)%m))&1)<<i for i in range(m))
                output[shifted]+=initial/len(zeros)
        energy=F()
        for z in range(1<<m):
            mu=p**z.bit_count()*q**(m-z.bit_count());K=m-z.bit_count()
            rho=F(m,K) if not(z&1) else F()
            assert output[z]==mu*rho
            energy+=mu*rho*rho;states+=1
        assert energy==exact_strip_moment(m,p)
    upper,values=frame_moment_upper(p,32)
    assert all(values[m]>=exact_strip_moment(m,p) for m in range(1,33))
    return states


def test_symbolic_growth():
    cases=0;moves=0
    for h in range(2,9):
        for w in range(2,9):
            rect=(2,2,2+h,2+w)
            for direction in ('R','L','U','D'):
                new=strip(rect,direction)
                for r in range(len(new)):
                    zero={(y,2) for y in range(2,2+h)}|{(2,x) for x in range(2,2+w)}|{new[r]}
                    word=BalancedInstruction('grow',(rect,direction,r)).word()
                    for u,v in word:
                        assert abs(u[0]-v[0])+abs(u[1]-v[1])==1
                        for a,b in ((u,v),(v,u)):
                            y,x=a
                            assert any(z in zero and z!=b for z in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
                        zu=u in zero;zv=v in zero;zero.discard(u);zero.discard(v)
                        if zu:zero.add(v)
                        if zv:zero.add(u)
                    y0,x0,y1,x1=extend(rect,direction)
                    assert {(y,x0) for y in range(y0,y1)}|{(y0,x) for x in range(x0,x1)}<=zero
                    cases+=1;moves+=len(word)
    return dict(cases=cases,checked_microinstructions=moves)


def test_port_modules():
    rng=np.random.default_rng(720241);output=[];movechecks=0
    for L,vertical in ((4,False),(8,False),(8,True),(16,False)):
        blocks=[];trials=[]
        for which in range(2):
            for attempt in range(200000):
                block=(rng.random((L,L))<.8).astype(np.uint8)
                forced=block.copy();forced[L//2,L//2]=1
                if Gate(forced).good((0,0,L,L)):
                    blocks.append(block);trials.append(attempt+1);break
            else:raise AssertionError('no good sampled block')
        a=np.concatenate(blocks,axis=0 if vertical else 1)
        ports=((L//2,L//2),((3*L//2,L//2) if vertical else (L//2,3*L//2)))
        for seed in (73,149):
            module=make_balanced_module(a,ports,np.random.default_rng(seed))
            word=list(module.word());assert len(word)<=256*L**3
            assert word==word[::-1], 'The full port transposition word must be palindromic.'
            assert 0<sample_weight(module)<=1
            for pa,pb in ((0,0),(0,1),(1,0),(1,1)):
                x=a.copy();x[ports[0]]=pa;x[ports[1]]=pb;expected=x.copy()
                expected[ports[0]]=pb;expected[ports[1]]=pa
                repeat=make_balanced_module(x,ports,np.random.default_rng(seed))
                assert repeat.preparation==module.preparation and repeat.port_positions==module.port_positions
                for swap in word:
                    assert legal(x,swap),(L,vertical,swap,x)
                    apply(x,swap);movechecks+=1
                assert np.array_equal(x,expected)
            output.append(dict(L=L,vertical=vertical,seed=seed,
                               reservoir_trials=trials,
                               macroinstructions=len(module.preparation),
                               microinstructions=len(word),
                               exact_history_probability=str(sample_weight(module))))
    return dict(cases=output,checked_moves=movechecks,
                caveat='Rejection-sampled tests are diagnostics, not probability estimates.')


def run():
    start=time.perf_counter();states=test_strip_density();growth=test_symbolic_growth();ports=test_port_modules()
    cert=evaluate();assert cert['exponent']==11593
    return dict(status='passed',exact_strip_states=states,symbolic_growth=growth,
                port_module_tests=ports,certified_exponent=cert['exponent'],
                seconds=time.perf_counter()-start)

if __name__=='__main__':print(json.dumps(run(),indent=2))
