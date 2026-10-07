from frontier_sampler import FrontierParity, brute, ZERO, qr
from fractions import Fraction
from itertools import product
from pathlib import Path
from datetime import datetime,timezone
import json, random, time

started=time.monotonic(); rng=random.Random(60103)
checks=0; stats=[]

def verify(F,A=None,name='fixture',prefix=True):
    global checks
    p=FrontierParity(F,A)
    for k in range(len(F)//2+1):
        x=p.partition(k); y=brute(F,k,A)
        assert x==y,(name,k,x,y); checks+=1
        stats.append({'name':name,'n':len(F),'k':k,'norm':str(x),**p.stats})
        if prefix and len(F)>1:
            for a in (-1,0,1):
                forced={0:(a,)}
                assert p.partition(k,forced)==brute(F,k,A,forced),(name,k,a)
                checks+=1
        if x and k:
            for _ in range(2):
                s=p.sample(k,rng)
                assert len(s['I'])==len(s['J'])==k
                assert not set(s['I'])&set(s['J'])
                assert p.point_weight(s['I'],s['J'])>0
                checks+=3
    return p

F4=[[0,0,1,1],[0,0,1,-1],[0,0,0,0],[0,0,0,0]]
p4=verify(F4,name='nonwindable_4')
assert p4.partition(2)==4; checks+=1

F8=[[0]*8 for _ in range(8)]
for i,j in [(0,3),(2,1),(1,6),(4,0),(5,7)]: F8[i][j]=1
p8=FrontierParity(F8)
for R in ({0,1,2,3},{0,1,4,5,6,7}):
    forced={v:((1,-1) if v in R else (0,)) for v in range(8)}
    assert p8.partition(len(R)//2,forced)==1; checks+=1

for n in range(2,7):
    for rep in range(2):
        width=1+rep
        F=[[(rng.randrange(-2,3),rng.randrange(-2,3)) if 0<abs(i-j)<=width else 0 for j in range(n)] for i in range(n)]
        A=[Fraction(rng.randrange(1,4),rng.randrange(1,4)) for i in range(n)]
        verify(F,A,name=f'band_complex_{n}_{width}')
        order=list(range(n));rng.shuffle(order)
        perm=FrontierParity(F,A,order)
        for k in range(n//2+1):
            assert perm.partition(k)==brute(F,k,A); checks+=1

for n in (4,6):
    F=[[Fraction(rng.randrange(-3,4),rng.randrange(1,5)) for j in range(n)] for i in range(n)]
    verify(F,name=f'dense_rational_{n}')

cycles=[]
for n in (4,6,8,10,12):
    F=[[0]*n for _ in range(n)]
    for i in range(n):F[i][(i+1)%n]=1
    p=FrontierParity(F)
    assert p.partition(n//2)==2; checks+=1
    # A full-sector bounded-local chain disconnects, yet exact refresh succeeds.
    sample=p.sample(n//2,rng)
    assert sample['I'] in (tuple(range(0,n,2)),tuple(range(1,n,2))); checks+=1
    cycles.append({'n':n,'width':p.width,'norm':'2','sample':sample,'final_stats':p.stats})

# Exhaustively test the single-step self-reduction partition identity on F4.
for q in range(5):
    for labels in product((-1,0,1),repeat=q):
        forced={v:(a,) for v,a in enumerate(labels)}
        parent=p4.integer_partition(2,forced)
        if q<4:
            child=sum(p4.integer_partition(2,{**forced,q:(a,)}) for a in (-1,0,1))
            assert parent==child; checks+=1
        assert p4.partition(2,forced)==brute(F4,2,allowed=forced);checks+=1

# Exercise the explicit bounded random-bit fallback without a statistical claim.
class MaxBits:
    def getrandbits(self,b): return (1<<b)-1
cap=FrontierParity([[0,1],[2,0]])
out=cap.sample(1,MaxBits(),max_bit_trials=1)
assert out['fallback_events']==1; checks+=1
assert cap.point_weight(out['I'],out['J'])>0;checks+=1
for _ in range(3):
    out=p4.sample(2,rng,max_bit_trials=12)
    assert out['fallback_events']==0 and p4.point_weight(out['I'],out['J'])>0;checks+=1

result={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'assertions':checks,
        'wall_seconds':time.monotonic()-started,'fixtures':stats,'directed_cycles':cycles,
        'scope':'Exact finite identities, prefix masses, and supported output witnesses; no asymptotic or hardware certificate.'}
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ('status','assertions','wall_seconds','scope')},indent=2))
