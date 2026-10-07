from rank_frontier_sampler import RankParity
from pathlib import Path
from fractions import Fraction
from datetime import datetime,timezone
import json,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from frontier_sampler import FrontierParity

started=time.monotonic();rows=[];checks=0
for q in (1,2,3):
    n=2*q;epsilon=Fraction(1,2**12)
    F=[[Fraction(i==j) for j in range(n)] for i in range(n)]
    for i in range(q):F[i][q+i]=F[q+i][i]=epsilon
    p=RankParity(F);Z=p.partition(q)
    expected=2**q*epsilon**(2*q)
    assert Z==expected;checks+=1
    assert max(p.ranks[::2])==2*q;checks+=1
    F0=[[Fraction(i==j) for j in range(n)] for i in range(n)]
    assert RankParity(F0).partition(q)==0;checks+=1
    # Interleaving each entangled pair makes the same instance easy.
    order=[j for i in range(q) for j in (i,q+i)]
    ordered=RankParity(F,order=order)
    assert max(ordered.ranks[::2])<=2 and ordered.partition(q)==Z;checks+=1
    rows.append({'q':q,'epsilon':str(epsilon),'norm':str(Z),'grouped_cross_rank':max(p.ranks[::2]),
                 'interleaved_cross_rank':max(ordered.ranks[::2]),'exact_schmidt_rank':2**q})

# Two nonzero retained laws can be orthogonal although both matrices approach I.
epsilon=Fraction(1,2**20)
FA=[[Fraction(i==j) for j in range(4)] for i in range(4)]
FB=[[Fraction(i==j) for j in range(4)] for i in range(4)]
FA[0][1]=FA[2][3]=epsilon
FB[0][2]=FB[1][3]=epsilon
pa=FrontierParity(FA);pb=FrontierParity(FB)
assert pa.partition(2)==pb.partition(2)==epsilon**4;checks+=1
assert pa.point_weight((0,2),(1,3))==epsilon**4;checks+=1
assert pb.point_weight((0,1),(2,3))==epsilon**4;checks+=1
assert pa.point_weight((0,1),(2,3))==pb.point_weight((0,2),(1,3))==0;checks+=1

out={'status':'PASS','assertions':checks,'utc':datetime.now(timezone.utc).isoformat(),
     'wall_seconds':time.monotonic()-started,'singlet_family':rows,
     'scope':'Exact finite identities accompanying the analytic fixed-order rank and retained-norm barriers. These do not imply general classical sampling hardness.'}
Path(__file__).with_name('compression_barrier_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','assertions','wall_seconds','scope')},indent=2))
