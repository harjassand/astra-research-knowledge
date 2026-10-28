"""Independent stdlib integer conditional-word replay, no producer imports.

Verifies the full5 table through centered conditional products rather than
the producer's forward-prefix enumeration, plus parity/mixing/6-word facts.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,math,time
OUT=Path(__file__).resolve().parent
START=time.monotonic()
raw=json.loads((OUT/'EXACT_MATRICES.json').read_text());res=json.loads((OUT/'RESULT.json').read_text())
seed=json.loads((OUT/'sources/seed_certificate.json').read_text());D=raw['denominator']
P=raw['target_numerators'];R=raw['parity_lift_numerators'];A=raw['ordinary_reversiblization_numerators'];lab=raw['target_labels'];theta=raw['parity_involution']
assert all(Q(P[i][j],D)==Q(i==j)+Q(seed['Q'][i][j])/2 for i in range(10) for j in range(10))
assert all(A[i][j]*2==P[i][j]+P[j][i] for i in range(10) for j in range(10))
delta=Q(raw['delta']);flip=int(delta*D)
for i in range(20):
    assert min(R[i])>=0 and sum(R[i])==D and R[i][i]>0
    for j in range(20):
        if i//10==j//10:
            expected=(P[i%10][j%10] if i<10 else P[j%10][i%10])-(flip if i==j else 0)
        else:expected=flip if i%10==j%10 else 0
        assert R[i][j]==expected
        assert R[i][j]==R[theta[j]][theta[i]]
assert all(sum(R[i][j] for i in range(20))==D for j in range(20))
def action(M,v):return [sum(x*y for x,y in zip(row,v)) for row in M]
def words2(M,labels):
    first=[action(M,[int(x==b) for x in labels]) for b in range(6)]
    return [[action(M,[int(x==a)*v for x,v in zip(labels,first[b])]) for b in range(6)] for a in range(6)]
PT=[list(x) for x in zip(*P)];plus=words2(P,lab);minus=words2(PT,lab);lift=words2(R,lab*2);ordinary=words2(A,lab)
for a in range(6):
    mask=[int(x==a) for x in lab]
    assert action(P,mask)==action(PT,mask)
for a in range(6):
    for b in range(6):assert lift[a][b]==plus[a][b]+minus[a][b]
# For each central symbol, independently compute the cross-Gram of36 futures.
tv_num=0;checked=0
for center in range(6):
    for a in range(6):
        for b in range(6):
            for c in range(6):
                for d in range(6):
                    target=sum(x*y for i,(x,y) in enumerate(zip(minus[a][b],plus[c][d])) if lab[i]==center)
                    reverse=sum(x*y for i,(x,y) in enumerate(zip(minus[c][d],plus[a][b])) if lab[i]==center)
                    assert target==reverse
                    lifted=sum(lift[a][b][theta[i]]*lift[c][d][i] for i in range(20) if (lab*2)[i]==center)
                    assert lifted==2*target
                    ordinary_value=sum(x*y for i,(x,y) in enumerate(zip(ordinary[a][b],ordinary[c][d])) if lab[i]==center)
                    tv_num+=abs(target-ordinary_value);checked+=1
assert checked==7776
assert Q(tv_num,20*D**4)==Q(res['ordinary_control_five_word_TV'])
def multiply(M,N):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*N)] for row in M]
cube=multiply(multiply(R,R),R);minimum=min(x for row in cube for x in row);assert minimum>0
beta=Q(20*minimum,D**3);assert beta==Q(res['mixing']['three_step_Doeblin_beta'])
assert sum(Q(5)**j/math.factorial(j) for j in range(7))>100
def word_prob(M,labels,w):
    # Backward conditional recursion, separate from forward row propagation.
    v=[int(x==w[-1]) for x in labels]
    for a in reversed(w[:-1]):v=[int(x==a)*p for x,p in zip(labels,action(M,v))]
    return Q(sum(v),len(labels)*D**(len(w)-1))
longer=res['longer_word_difference'];w=longer['word']
pt,pr=word_prob(P,lab,w),word_prob(R,lab*2,w)
assert pt==Q(longer['target_probability']) and pr==Q(longer['lift_probability']) and pt!=pr
out={'status':'INDEPENDENT_OPERATOR_REPLAY_PASSED','five_word_entries_checked':checked,
     'algorithm':'Backward conditional two-word cross-Grams; no producer import or forward-prefix recursion.',
     'all5_equal':'EXACT','ordinary_TV':'EXACTLY_REBUILT','all400_parity_relations':'EXACT',
     'strict_three_step_minorization':'EXACTLY_REBUILT','six_word_difference':'EXACTLY_REBUILT',
     'seconds':time.monotonic()-START,
     'scope':'Independent code path within same worker, not separate peer or physical verification. Witness formula means are not recomputed here; all5 law equality implies identical distributions of every5-letter statistic.'}
(OUT/'INDEPENDENT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
