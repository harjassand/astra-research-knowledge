"""Standard-library scalar-certificate consumer, no producer import/sort.

Rebuilds the largest fully specified constructed input and verifies its
quadratic certificate and corner witness. This is same-worker replay.
"""
from fractions import Fraction as R
from pathlib import Path
from random import Random
import json,time
START=time.monotonic();OUT=Path(__file__).resolve().parent
def largest_input():
    k=100000;rng=Random(118);weights=[rng.randrange(1,33) for _ in range(k)];total=sum(weights)
    p=[R(w,total) for w in weights];mid=[];lower=[];upper=[]
    for i in range(k):
        m=rng.randrange(256,769)
        w=min(m,1024-m)*9//10 if i%97==0 else rng.randrange(1,8)
        mid.append(R(m,1024));lower.append(R(m-w,1024));upper.append(R(m+w,1024))
    normalizer=sum((a*b for a,b in zip(p,mid)),R(0))
    # B_i=1; q_i=p_i*mid_i/normalizer.
    return ([a*b for a,b in zip(p,lower)],[a*b for a,b in zip(p,upper)],
            [normalizer/(a*b) for a,b in zip(p,mid)])
rows=[]
for name in ['16_narrow','16_heterogeneous_width','4096_heterogeneous_width','100000_heterogeneous_width']:
    start=time.monotonic()
    if name.startswith('100000'):lower,upper,coef=largest_input()
    else:
        raw=json.loads((OUT/f'INPUT_{name}.json').read_text());lower,upper,coef=([R(z) for z in raw[k]] for k in ['lo','hi','r'])
    acquisition=time.monotonic()-start;start=time.monotonic()
    cert=json.loads((OUT/f'CERT_{name}.json').read_text());nu=R(cert['nu']);U=R(cert['upper'])
    offset=R(0)
    for l,h,c in zip(lower,upper,coef):
        assert 0<=l<=h and c>=0
        density=c*(l+h)
        offset+=max((density-nu)*l,(density-nu)*h)-c*l*h
    assert offset==R(cert['eta'])<0 and nu>0 and 4*U*(-offset)>=nu*nu
    # This proves U S² >= nu S+offset >= sum c_i w_i² for all box w.
    chosen=cert['lower_upper_indices'];assert len(chosen)==len(set(chosen))
    witness=list(lower)
    for i in chosen:assert 0<=i<len(witness);witness[i]=upper[i]
    S=sum(witness,R(0));N=sum((c*x*x for c,x in zip(coef,witness)),R(0));L=N/(S*S)
    assert L==R(cert['lower']) and U<=L*R(cert['factor'])
    rows.append({'name':name,'k':len(lower),'exact_upper_and_corner':'PASS',
                 'relative_gap':float(U/L-1),'input_seconds':acquisition,'check_seconds':time.monotonic()-start})
result={'status':'INDEPENDENT_LINEAR_CONSUMER_PASSED','cases':rows,'module_seconds':time.monotonic()-START,
        'scope':'No producer import or optimization. Same-worker independent code path; not a separate peer audit.'}
(OUT/'INDEPENDENT_CONSUMER.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
