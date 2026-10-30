import itertools,json
from fractions import Fraction
# Regression of pathwise charging, not FGL expansion or a quantum threshold.
H=(3,6,12,9,5); n=4; beta=Fraction(1,3)
syn=lambda e:sum(((e&h).bit_count()%2)<<j for j,h in enumerate(H))
S=lambda e:syn(e).bit_count()
candidates=[1<<i for i in range(n)]
count=0
for e0 in range(1<<n):
 good=[f for f in candidates if S(e0)-S(e0^f)>=beta*syn(f).bit_count() and syn(f)]
 packs=[p for k in range(len(good)+1) for p in itertools.combinations(good,k) if all(not(syn(a)&syn(b)) for a,b in itertools.combinations(p,2))]
 G=max(packs,key=len)
 stack=[(e0,frozenset(G),0,0,0)]
 while stack:
  e,alive,D,J,depth=stack.pop();count+=1
  M=len(alive)
  assert Fraction(len(G))<=2*D/beta+J+M
  assert S(e)<=S(e0)-beta*len(G)/2+(1+beta/2)*J+beta*M/2
  if depth==5:continue
  for f in candidates:
   d=S(e)-S(e^f)
   if d>=beta*syn(f).bit_count():
    new=frozenset(g for g in alive if g!=f and not(syn(g)&syn(f)))
    stack.append((e^f,new,D+d,J,depth+1))
   else:
    assert f not in alive # genuine evaluation cannot reject unresolved candidate
    stack.append((e,alive,D,J,depth+1))
   new=frozenset(g for g in alive if not(syn(g)&syn(f)))
   stack.append((e^f,new,D,J+syn(f).bit_count(),depth+1))
print(json.dumps({'prefixes':count,'depth':5,'beta':'1/3','window_charging':'PASS','incorrect_rejection_of_unresolved_candidate':'none'},indent=2))
