from rank_frontier_sampler import RankParity,ZERO,ONE
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from fractions import Fraction
import sys,json,random,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from frontier_sampler import qr,ga,gm,gs,gc,brute,FrontierParity

started=time.monotonic();rng=random.Random(60203);checks=0;results=[]

def pf(K):
    if not K:return ONE
    out=ZERO
    for j in range(1,len(K)):
        rest=[i for i in range(len(K)) if i not in (0,j)]
        term=gm(K[0][j],pf([[K[a][b] for b in rest] for a in rest]))
        out=ga(out,gs(term,1 if j%2 else -1))
    return out

def verify(F,activities=None,name='fixture',words=True):
    global checks
    p=RankParity(F,activities)
    for k in range(len(F)//2+1):
        norm=p.partition(k);direct=brute(F,k,activities)
        assert norm==direct,(name,k,norm,direct);checks+=1
        for a in (-1,0,1):
            if F:
                allowed={0:(a,)}
                assert p.partition(k,allowed)==brute(F,k,activities,allowed);checks+=1
        if norm and k:
            sample=p.sample(k,rng,max_bit_trials=14)
            assert len(sample['I'])==len(sample['J'])==k;checks+=1
            assert FrontierParity(F,activities).point_weight(sample['I'],sample['J'])>0;checks+=1
        results.append({'fixture':name,'n':len(F),'k':k,'norm':str(norm),**p.stats})
    if words:
        for labels in product((-1,0,1),repeat=len(F)):
            modes=[2*i+(0 if label==1 else 1) for i,label in enumerate(labels) if label]
            expected=pf([[p.K[i][j] for j in modes] for i in modes])
            actual=p.amplitude(labels)
            assert expected==actual,(name,labels,expected,actual);checks+=1
    return p

verify([],name='empty')
for n in range(1,6):
    F=[[(Fraction(rng.randrange(-2,3),rng.randrange(1,4)),Fraction(rng.randrange(-2,3),rng.randrange(1,4))) for _ in range(n)] for _ in range(n)]
    activities=[Fraction(rng.randrange(1,4),rng.randrange(1,4)) for _ in range(n)]
    verify(F,activities,name=f'dense_complex_{n}')

F4=[[0,0,1,1],[0,0,1,-1],[0,0,0,0],[0,0,0,0]]
verify(F4,name='nonwindable_4')

# Arbitrarily dense support and generically full ordinary rank, with fixed
# rank across every cut: Fij=ui*vj for i<j, xi*yj for i>j.
semiseparable=[]
for n in (6,8,10,12):
    u=[1+(i%2) for i in range(n)];v=[1+(i%3) for i in range(n)]
    x=[(1,i%2) for i in range(n)];y=[(1,-(i%3)) for i in range(n)]
    F=[[(gm(qr(u[i]),qr(v[j])) if i<j else gm(qr(x[i]),qr(y[j])) if i>j else qr(3)) for j in range(n)] for i in range(n)]
    p=RankParity(F)
    k=n//2;norm=p.partition(k)
    assert max(p.ranks[::2])<=2;checks+=1
    support=FrontierParity(F)
    if n<=8:
        assert norm==brute(F,k);checks+=1
        assert norm==support.partition(k);checks+=1
    sample=p.sample(k,rng,max_bit_trials=16)
    assert support.point_weight(sample['I'],sample['J'])>0;checks+=1
    semiseparable.append({'n':n,'k':k,'norm':str(norm),'support_width':support.width,
                         'sample':sample,**p.stats})

# Exact ordering dependence is charged, not disguised as rank acquisition.
F=[[0,1,2,3],[4,0,5,6],[7,8,0,9],[10,11,12,0]]
order=[2,0,3,1];p=RankParity(F,order=order)
for k in range(3):
    assert p.partition(k)==brute(F,k);checks+=1

result={'status':'PASS','assertions':checks,'utc':datetime.now(timezone.utc).isoformat(),
        'wall_seconds':time.monotonic()-started,'fixtures':results,'dense_semiseparable':semiseparable,
        'scope':'Exact finite Pfaffian-amplitude, determinant-norm, prefix and output-witness diagnostics; no generic polynomial counting claim.'}
Path(__file__).with_name('rank_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ('status','assertions','wall_seconds','scope')},indent=2))
