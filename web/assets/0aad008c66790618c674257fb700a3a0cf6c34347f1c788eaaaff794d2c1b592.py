from color_rank_sampler import ColorRankParity
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations
from fractions import Fraction
import sys,json,random,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from frontier_sampler import determinant,qr

started=time.monotonic();rng=random.Random(60303);checks=0;rows=[]

def brute(lines,n,k,forced=None):
    forced={} if forced is None else forced
    ans=Fraction(0)
    for ids in combinations(range(len(lines)),k):
        sources=[lines[t][0] for t in ids]
        if len(set(sources))!=k:continue
        for J in combinations([v for v in range(n) if v not in sources],k):
            z=determinant([[lines[t][1][j] for j in J] for t in ids])
            w=z[0]**2+z[1]**2
            for t in ids:w*=lines[t][2]
            ans+=w
    return ans

for n in (4,6):
    if n==4:
        F=[[(rng.randrange(-2,3),rng.randrange(-1,2)) for j in range(n)] for i in range(n)]
        edges=list(combinations(range(n),2))
    else:
        F=[[(rng.randrange(1,3),rng.randrange(-1,2)) if abs(i-j)==1 else 0 for j in range(n)] for i in range(n)]
        edges=[(i,i+1) for i in range(n-1)]
    lines=[(i,F[i],Fraction(1)) for i in range(n)]
    for i,j in edges:
        v=[0]*n;v[j]=1
        lines.append((i,v,Fraction(rng.randrange(1,4),rng.randrange(1,4))))
    p=ColorRankParity(lines,n)
    for k in range(n//2+1):
        Z=p.partition(k);assert Z==brute(lines,n,k),(n,k,Z,brute(lines,n,k));checks+=1
        if Z and k:
            out=p.sample(k,rng,max_bit_trials=14)
            ids=out['selected_lines'];J=out['J']
            assert len(ids)==len(J)==k;checks+=1
            z=determinant([[lines[t][1][j] for j in J] for t in ids])
            assert z!=(0,0);checks+=1
        rows.append({'n':n,'k':k,'norm':str(Z),**p.stats})

# Empty coordinate-only and one canonical-source repeated-line zero fixtures.
p=ColorRankParity([(0,[0,1],Fraction(2)),(0,[0,1],Fraction(3))],2)
assert p.partition(1)==5;checks+=1
p=ColorRankParity([(0,[0,1,0,0],1),(0,[0,0,1,0],1)],4)
assert p.partition(2)==0;checks+=1

out={'status':'PASS','assertions':checks,'utc':datetime.now(timezone.utc).isoformat(),
     'wall_seconds':time.monotonic()-started,'fixtures':rows,
     'scope':'Exact finite canonical colored-line plus coordinate-probe norm and output-witness identities; exponential rank cost remains explicit.'}
Path(__file__).with_name('color_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','assertions','wall_seconds','scope')},indent=2))
