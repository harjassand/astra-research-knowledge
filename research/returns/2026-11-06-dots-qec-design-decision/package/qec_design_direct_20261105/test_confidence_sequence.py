import sys,json,math
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import sequential_decision as s
out={'outward_endpoint_checks':0,'finite_path_coverage_checks':[]}
for n in [1,2,3,5,10,20,50,100,250,1000]:
    for k in sorted(set([0,1,n//4,n//2,max(0,n-1),n])):
        lo,hi=s.confidence_sequence(n,k)
        assert lo<=F(k,n)<=hi
        if k:assert s.outside(n,k,lo.numerator,lo.denominator)
        if k<n:assert s.outside(n,k,hi.numerator,hi.denominator)
        out['outward_endpoint_checks']+=1
# Fully enumerate aggregate path mass that first exits by n=25, with a visible
# alpha=1/10 to exercise exits. This is a test, never production evidence.
s.ALPHA=F(1,10)
for p in [F(1,100),F(1,10),F(1,4),F(1,2),F(3,4),F(9,10),F(99,100)]:
    alive={0:F(1)};lost=F(0)
    for n in range(1,26):
        nxt={}
        for k,w in alive.items():
            for kk,ww in [(k,w*(1-p)),(k+1,w*p)]:
                # Exact test for M_n(p)>=1/alpha.
                if s.outside(n,kk,p.numerator,p.denominator):lost+=ww
                else:nxt[kk]=nxt.get(kk,F(0))+ww
        alive=nxt
    assert lost<=s.ALPHA
    assert lost+sum(alive.values())==1
    out['finite_path_coverage_checks'].append({'p':str(p),'alpha':'1/10','horizon':25,'probability_any_crossing_exact':str(lost),'probability_any_crossing':float(lost)})
Path(__file__).with_name('confidence_sequence_tests.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
