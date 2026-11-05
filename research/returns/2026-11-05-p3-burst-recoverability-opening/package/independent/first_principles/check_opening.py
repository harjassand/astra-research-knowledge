"""Small exact checks of the independently derived opening and obstructions.
No physical validation or new general fault-tolerance claim.
"""
from fractions import Fraction
from collections import deque
from math import comb
import json

checks=[]
for N in range(2,10):
    for m in range(N+1):
        for k in range(N+1):
            expected=Fraction(comb(N-k,m-k),comb(N,m)) if m>=k else Fraction(0)
            falling=Fraction(1)
            for j in range(k):
                falling*=Fraction(max(0,m-j),N-j)
            assert expected==falling
            assert falling<=Fraction(m,N)**k
            checks.append((N,m,k))

walls=[]
for L in [4,8,16,32]:
    wall={(L//2,y) for y in range(L)}
    start=(0,0); seen={start}; q=deque([start])
    while q:
        x,y=q.popleft()
        for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if 0<=a<L and 0<=b<L and (a,b) not in wall and (a,b) not in seen:
                seen.add((a,b));q.append((a,b))
    assert not any(x==L-1 for x,y in seen)
    walls.append({'L':L,'sites':L*L,'wall_sites':len(wall),'fault_fraction':str(Fraction(len(wall),L*L)),'right_boundary_unreachable':True})

for L in range(2,15):
    one_dim=Fraction(sum(abs(i-j) for i in range(L) for j in range(L)),L*L)
    assert one_dim==Fraction(L*L-1,3*L)

out={'status':'PASS','hypergeometric_support_cases':len(checks),'wall_checks':walls,'replacement_channel_Bell_test_half_trace_norm':str((Fraction(3,4)+3*Fraction(1,4))/2),'scope':'Finite exact algebra and graph checks; no physical experiment.'}
print(json.dumps(out,indent=2))
