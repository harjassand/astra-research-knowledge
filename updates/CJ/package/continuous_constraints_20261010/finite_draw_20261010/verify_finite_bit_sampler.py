#!/usr/bin/env python3
"""Replay the finite tape and exercise a small number of fallback branches.

All core integer operations and all interval checks rerun. This verifies saved
runs, not their distribution, and reuses the same implementation components.
"""
import argparse,json,time
from fractions import Fraction as Q
from pathlib import Path
from finite_bit_sampler import run_sampler, rounded_cholesky, exact_fiber, make_raw_input, acceptance_decision
from probability_budget import asq,enc
HERE=Path(__file__).resolve().parent

class Tape:
    def __init__(self,report):
        self.cells=[]
        nb=report['budget']['normal_uniform_bits']
        for t in report['trials']:
            self.cells.extend((c.get('uniform_bits',nb),int(c['uniform_cell_index'])) for c in t['normal_certificates'])
            if 'acceptance' in t:
                a=t['acceptance'];self.cells.append((a['uniform_bits'],int(a['uniform_cell_index'])))
        self.i=0
    def getrandbits(self,b):
        eb,k=self.cells[self.i];self.i+=1
        assert eb==b
        return k

class EndpointBits:
    def getrandbits(self,b):return 0
class MidpointBits:
    def getrandbits(self,b):return 1<<(b-1)

def verify(path):
    report=json.loads(path.read_text());tape=Tape(report)
    rerun=enc(run_sampler(asq(report['budget']['epsilon']),bit_source=tape))
    assert tape.i==len(tape.cells)
    for key in ['raw_input','dimensions','native_certificate','budget','H_factor','trials','terminal_reason','output']:
        assert rerun[key]==report[key], 'Replay changed '+key
    return {'file':path.name,'replayed_uniform_cells':tape.i,'terminal_reason':report['terminal_reason'],
            'exact_replay_matches':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('reports',type=Path,nargs='*');args=ap.parse_args()
    reports=args.reports or [HERE/'FINITE_BIT_DRAW.json']
    start=time.perf_counter();checks=[verify(p) for p in reports]
    endpoint=run_sampler(Q(1,16),bit_source=EndpointBits())
    assert endpoint['terminal_reason']=='normal_tail_cell_fallback'
    assert endpoint['output']['norm_squared']==0
    midpoint=run_sampler(Q(1,16),bit_source=MidpointBits())
    assert midpoint['terminal_reason']=='small_V_fallback'
    assert midpoint['output']['norm_squared']==0
    # The final zero output is feasible even when the fiber Gram is singular.
    y,s,proof=exact_fiber(make_raw_input(),[Q(0)]*128,[Q(0)]*128)
    assert y is None and s==[[Q(0),Q(0)],[Q(0),Q(0)]]
    assert acceptance_decision(Q(1,4),Q(1,4),0,2)=='accept'
    assert acceptance_decision(Q(1,4),Q(1,4),3,2)=='reject'
    assert acceptance_decision(Q(1,4),Q(1,4),1,2)=='interval_overlap_fallback'
    # Deterministic factor enclosure on a tiny non-diagonal rational SPD input.
    import numpy as np
    l,b,d,p=rounded_cholesky(np.array([[5,2],[2,3]],dtype=object),2,Q(5,2),Q(1,1<<100),Q(1,2))
    assert d<=Q(1,1<<100)
    results={'saved_tape_replays':checks,
        'additional_checks':['endpoint normal-cell zero fallback','tiny V zero fallback','singular fiber detected','100-bit deterministic rational Cholesky','exact accept/reject/overlap branch tests'],
        'wall_seconds':time.perf_counter()-start,
        'scope':'Modest deterministic implementation checks; no empirical distribution or performance claim. Replay shares code with producer.'}
    (HERE/'FINITE_BIT_VERIFICATION.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
