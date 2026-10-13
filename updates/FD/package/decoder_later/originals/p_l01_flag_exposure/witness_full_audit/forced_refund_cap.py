#!/usr/bin/env python3
"""Forced semantic-miss/refunded-defect fixture for p_s01c witness compiler.

The random tape is deliberately forced to zero only in period-probe and
post-witness outer samples. It is a positive-probability transcript under
ideal fair bits, not a probability estimate or a fair-randomness run.
"""
from __future__ import annotations
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPILER = ROOT / "p_s01c_witness_compiler"
sys.path.insert(0, str(COMPILER))
import witness_compiler as wc
fd = wc.fd
ac = wc.ac


class ScriptedRng:
    def __init__(self, values):
        self.values = list(values)
        self.i = 0
    def getrandbits(self, n):
        value = self.values[self.i] if self.i < len(self.values) else 0
        self.i += 1
        return value & ((1 << n) - 1 if n else 0)


def coord_mask(v, basis):
    for mask in range(1 << len(basis)):
        if ac.combine(basis, mask) == v:
            return mask
    raise AssertionError(f"target {v:#x} not in acquired S")


def hidden_prefix(x):
    a=(x>>0)&1; y=(x>>1)&1; s1=(x>>2)&1; s2=(x>>3)&1
    z1=(x>>4)&1; z2=(x>>5)&1; z3=(x>>6)&1
    H=s1 ^ (s1 & s2)
    return [a ^ (y&H), z1 ^ (y&H), z2 ^ (y&H), z3 ^ (y&H)]


def lex_rank(x):
    bits=hidden_prefix(x)
    y=(x>>1)&1; s1=(x>>2)&1; s2=(x>>3)&1
    out=0
    for b in bits+[y,s1,s2]: out=(out<<1)|b
    return out


def source_q(k,x):
    return hidden_prefix(x)[k]


def exact_period_dimension(k):
    periods=[]
    for v in range(1<<n_global):
        if all(source_q(j,x)==source_q(j,x^v) for j in range(k+1) for x in range(1<<n_global)):
            periods.append(v)
    # The period set is a linear subspace, so its cardinality determines rank.
    return (len(periods).bit_length()-1), periods


class CountedDictionary:
    def __init__(self, original):
        self.original=original
        self.calls=[]
    def __call__(self,label,n,W,xstar,cap,eta,rng,source,meter,cached_q0=None,cached_qx=None):
        before=source.calls
        D,receipt=self.original(label,n,W,xstar,cap,eta,rng,source,meter,cached_q0,cached_qx)
        if D is not None:
            self.calls.append(dict(input_dim=len(W),input_basis=list(W),output_dim=len(D),drop=len(W)-len(D),
                                   detected_x=xstar,period_basis=list(D),receipt=receipt,
                                   source_calls=source.calls-before,
                                   false_period_direction=wc.contains(1<<3,D,n),
                                   independent_dimension=len(ac.echelon(D,n)[0])))
        else:
            self.calls.append(dict(input_dim=len(W),input_basis=list(W),output_dim=None,drop=None,
                                   detected_x=xstar,receipt=receipt,
                                   source_calls=source.calls-before))
        return D,receipt


def main():
    n,r,d,m=7,3,3,4
    global n_global
    n_global=n
    beta=.5
    cfg=wc.parameters(n,r,d,beta,prefix_length=m,mode='witness')
    assert len({lex_rank(x) for x in range(1<<n)}) == 1<<n
    source=ac.Source(lambda x,y: int(lex_rank(x)<lex_rank(y)))
    meter=ac.Meter()
    prefix=fd.Prefix(n,meter)
    state=dict(global_drop=0,paid_dictionaries=0,outer_epochs=0)
    original=wc.period_dictionary
    counter=CountedDictionary(original)
    wc.period_dictionary=counter

    stage_data=[]
    toggles=[1<<0,1<<4,1<<5,1<<6]
    for k,v in enumerate(toggles):
        before=len(prefix.S)
        # Check the promised hidden triangular flag exactly on this tiny source.
        for x in range(1<<n):
            assert source_q(k,x^v)==1^source_q(k,x)
            for j in range(m):
                if j!=k:
                    assert source_q(j,x^v)==source_q(j,x)
        # Target s1 at x=e_y witnesses H(s1)=1. The rest of the tape is all
        # zero: period probes accept s2 at z=0, then all remaining outer tests
        # miss. Stage 3 is stopped by the before-dictionary global cap.
        s_mask=coord_mask(1<<2,prefix.S)
        tape=ScriptedRng([s_mask,1<<1])
        q,rec=wc.reconstruct(n,r,d,k,v,prefix,source,tape,cfg,meter,state)
        if k<3:
            assert q is not None, (k,rec)
            # Each stage's learned candidate is just its own coordinate. This
            # exhibits the three-bit geometric-defect refund explicitly.
            assert q.terms=={v}, (k,q.terms,rec)
            witness=rec['witnesses'][0]
            # The all-zero dictionary tape classifies s2 as a false period.
            assert counter.calls[-1]['false_period_direction']
            # Verify e_s2 is truly not a period of the actual P(s)=F_s(e_y)
            # on this stage's input W. Its z=0 test passes, while z=e_s1
            # separates P(e_s1) from P(e_s1+e_s2).
            xstar=witness['xstar']
            W=counter.calls[-1]['input_basis']
            assert xstar==(1<<1)
            coord_mask(1<<2,W)
            coord_mask(1<<3,W)
            def P(s):
                return source_q(k,xstar^s)^source_q(k,xstar)^source_q(k,s)^source_q(k,0)
            assert P(0)==P(1<<3)==0
            assert P(1<<2)!=P((1<<2)^(1<<3))
            assert not wc.contains(witness['detected_direction'],
                                   counter.calls[-1]['period_basis'],n)
            update=prefix.add(q,v)
            after=len(prefix.S)
            learned_defect=n-k-1-after
            true_s_dim,_=exact_period_dimension(k)
            true_defect=n-(k+1)-true_s_dim
            assert true_defect==3, (k,true_s_dim,true_defect)
            stage_data.append(dict(stage=k,source_output_degree=d,
                dimension_S_before=before,dimension_S_after=after,
                inferred_defect_after=learned_defect,
                true_stabilizer_dimension_after=true_s_dim,
                true_defect_after=true_defect, defect_refund=true_defect-learned_defect,
                candidate_terms=sorted(q.terms),exact_update=update,
                reconstruction=rec))
        else:
            assert q is None and rec['reason']=='global_witness_budget_before_dictionary', rec
            assert len(counter.calls)==r and state['paid_dictionaries']==r
            stage_data.append(dict(stage=k,dimension_S_before=before,
                reconstruction=rec,paid_dictionaries_at_abort=state['paid_dictionaries'],
                global_drop_at_abort=state['global_drop']))
            break

    # Per-call certificate bounds and exact oracle accounting.
    actual=source.calls
    assert actual<=cfg['witness_conditional_cap'], (actual,cfg['witness_conditional_cap'])
    assert actual<=cfg['worst_comparison_bound']
    assert state['paid_dictionaries']==r==len(counter.calls)
    assert state['global_drop']==r
    assert state['outer_epochs']<=m+r
    assert len(stage_data)==4
    assert all(s['inferred_defect_after']==0 for s in stage_data[:3])
    assert all(s['defect_refund']==3 for s in stage_data[:3])
    assert all(s['reconstruction']['witnesses'][0]['period_codimension']==1 for s in stage_data[:3])
    # Every q-label and every period second-derivative label is a real chosen-
    # pair comparison through ac.Source, with no direct access to hidden body.
    phase_calls=dict(source.by_phase)
    assert actual==sum(phase_calls.values())
    out=dict(scope='test-only positive-probability forced random transcript; not a fair-randomness frequency claim',
        source_model=dict(n=n,r=r,degree=d,prefix_length=m,
          outputs='(a+y(s1+s1*s2), z1+y(s1+s1*s2), z2+y(s1+s1*s2), z3+y(s1+s1*s2), y, s1, s2)',
          bijection='tail (y,s1,s2) recovers H, then each of first four outputs recovers its own bit',
          toggles=toggles),
        parameters={k:cfg[k] for k in ('stages','outer_L','period_L_max','witness_conditional_cap','worst_comparison_bound','failure_bound')},
        stages=stage_data,forced_dictionary_receipts=counter.calls,
        final_state=state,comparison_calls=actual,source_calls_by_phase=phase_calls,
        assertions=dict(defect_refunded_by_semantic_misses=True,
          global_paid_dictionary_cap_holds=True,
          next_dictionary_blocked_before_payment=True,
          conditional_and_whole_query_caps_hold=True,
          source_access_only_via_chosen_pair_comparator=True))
    out_path=Path(__file__).with_name('forced_refund_cap.json')
    out_path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',comparison_calls=actual,
       conditional_cap=cfg['witness_conditional_cap'],whole_cap=cfg['worst_comparison_bound'],
       paid_dictionaries=state['paid_dictionaries'],global_drop=state['global_drop'],
       outer_epochs=state['outer_epochs'],reason=stage_data[-1]['reconstruction']['reason'])))

if __name__=='__main__': main()
