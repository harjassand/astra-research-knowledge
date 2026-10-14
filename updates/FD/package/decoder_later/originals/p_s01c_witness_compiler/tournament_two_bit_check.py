#!/usr/bin/env python3
"""Enumerate match/retry branches for the proposed two-bit tournament objection."""
import json
from pathlib import Path
import witness_compiler as wc
ac=wc.ac
HERE=Path(__file__).resolve().parent

def rank(x):
    return 2*(x&1)+((x >> 1)&1)

def label(v,x):
    return 1 ^ int(rank(x)<rank(x^v))

def main():
    cases=[]
    for winner,challenger in ((1,2),(2,1)):
        for x in range(4):
            a,b=label(challenger,x),label(winner,x)
            matching=a==b
            after=(challenger if int(rank(x^challenger)<rank(x^winner))==a else winner) if matching else None
            if matching:
                assert after==1
            cases.append(dict(winner=winner,challenger=challenger,x=x,
                challenger_label=a,winner_label=b,branch='compare_and_select' if matching else 'retry',
                returned_winner=after))
    class Sequence:
        def __init__(self,values):self.values=iter(values)
        def getrandbits(self,n):return next(self.values)
    helper=[]
    for S in ([1,2],[2,1]):
        for tape in ([0],[3],[1,2,0],[2,1,3]):
            source=ac.Source(lambda x,y:int(rank(x)<rank(y)))
            state=dict(attempts=0,matches=0)
            cfg=dict(n=2,tournament_total_attempt_cap=20,tournament_pair_count_cap=1)
            winner,trials,reason=ac._select_certified_zero(S,0,source,Sequence(tape),cfg,ac.Meter(),state)
            assert winner==1 and reason is None
            helper.append(dict(basis=S,tape=tape,winner=winner,comparisons=source.calls))
    out=dict(status='PASS',scope='finite two-bit counterexample inspection; not independent general theorem proof',
             conclusion='equal-label inputs select the good e0; unequal-label inputs retry without a selection comparison',
             cases=cases,helper_runs=helper)
    (HERE/'tournament_two_bit_check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',enumerated_inputs=len(cases),helper_runs=len(helper))))
if __name__=='__main__':main()
