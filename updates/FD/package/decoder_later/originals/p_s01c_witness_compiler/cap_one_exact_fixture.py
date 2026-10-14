#!/usr/bin/env python3
"""Exhaust cap-one shortcut over all eligible rows through seven W dimensions.

Conditional component test with actual comparison labels; full acquisition is
separately exercised in run_witness. Hidden affine coordinates are test-only.
"""
import json
from pathlib import Path
import random
import witness_compiler as wc
fd,ac=wc.fd,wc.ac
HERE=Path(__file__).resolve().parent

class NoRandomDraws:
    def getrandbits(self,n):
        raise AssertionError('cap-one row must be deterministic')

def span(basis):
    return {ac.combine(basis,bits) for bits in range(1 << len(basis))}

def main():
    cases=[]
    for w in range(2,8):
        n=w+2
        for row in range(1,1 << (w-1)):
            rng=random.Random(7600000+100*w+row)
            rows=[1 << j for j in range(n)]
            for _ in range(12*n):
                i,j=rng.sample(range(n),2)
                rows[i]^=rows[j]
            inverse=ac.matrix_inverse(rows,n)
            W=[ac.linear(inverse,1 << j) for j in range(2,n)]
            own=W[0]
            xstar=ac.linear(inverse,1)
            offset=rng.getrandbits(n)|2  # y1=1 at raw zero
            def hidden(x):
                return ac.linear(rows,x)^offset
            def q(x):
                z=hidden(x)
                return ((z >> 2)&1)^((z&1)*((z >> 1)&1)*ac.parity((z >> 3)&row))
            pivot=(row&-row).bit_length()-1
            defect_output_rows=[1 << j for j in range(w-1) if j!=pivot]+[row]
            assert len(ac.echelon(defect_output_rows,w-1)[0])==w-1
            def rank(x):
                z=hidden(x)
                out=0
                # Put the sole relevant linear defect form LAST. The preceding
                # defect-coordinate outputs have toggles adjusted in its pivot
                # to preserve that form, giving the promised length n-1 flag.
                tail=[ac.parity((z >> 3)&linear_row) for linear_row in defect_output_rows]
                for bit in [z&1,(z >> 1)&1,q(x)]+tail:
                    out=(out << 1)|bit
                return out
            source=ac.Source(lambda x,y:int(rank(x)<rank(y)))
            label=lambda x:ac.core._label(source,own,x)
            q0,qx=label(0),label(xstar)
            before=source.calls
            D,rec=wc.period_dictionary(label,n,W,xstar,1,1e-20,NoRandomDraws(),source,ac.Meter(),q0,qx)
            assert rec['exact_conditional_cap_one_row'] and rec['semantic_error_budget']==0
            assert source.calls-before==2*w==rec['source_comparisons']
            expected={ac.combine(W,bits) for bits in range(1 << w)
                      if ac.parity((bits >> 1)&row)==0}
            assert span(D)==expected and own in expected
            assert len(D)==w-1
            assert all(q(s)^q(s^xstar)^q0^qx==0 for s in span(D))
            cases.append(dict(n=n,dimension_W=w,nonzero_hidden_row=row,
                returned_period_dimension=len(D),source_comparisons=source.calls,
                dictionary_comparisons=source.calls-before,exact=True))
    out=dict(status='PASS',scope='conditional cap-one component; actual comparator labels and hidden affine coordinates',
             all_eligible_nonzero_rows=True,max_dimension_W=7,case_count=len(cases),
             comparisons=sum(case['source_comparisons'] for case in cases),
             no_random_draws=True,cases=cases)
    (HERE/'cap_one_exact_fixture.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
if __name__=='__main__': main()
