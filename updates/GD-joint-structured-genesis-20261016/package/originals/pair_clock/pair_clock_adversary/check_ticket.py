"""Independent bounded algebra checks; not an asymptotic proof."""
from itertools import combinations
pairs=list(combinations(range(4),2))
states=[(0,0)]+[(r,s) for r in (1,2) for s in range(1,64)]
def le(x,y):
    return x[0]<y[0] or (x[0]==y[0] and x[1]&~y[1]==0)
def tick(x,a):
    r,s=x
    if not r or not (s>>a)&1:return x
    t=s&~(1<<a)
    return (r,t) if t else ((1,63) if r==2 else (0,0))
n=0
for x in states:
 for y in states:
  if le(x,y):
   for a in range(6):
    assert le(tick(x,a),tick(y,a)),(x,y,a)
    n+=1
print('Comparable state/label tick checks:',n)
# Exhaust arbitrary-length words by exploring their finite state quotient.
# No incident-edge additions between resets; center toggles a pair iff present.
seen=set(); todo=[(o,(2,63)) for o in range(16) if o.bit_count()%2==0]
terminal=set()
while todo:
 o,s=todo.pop()
 if (o,s) in seen:continue
 seen.add((o,s))
 for a,(i,j) in enumerate(pairs):
  mask=(1<<i)|(1<<j)
  oo=o^mask if o&mask==mask else o
  ss=tick(s,a)
  if s[0]==2 and ss[0]==1:assert oo.bit_count()<=2
  if ss[0]==0:
   assert oo==0,(o,s,a)
   terminal.add((oo,ss))
  elif (oo,ss) not in seen:todo.append((oo,ss))
print('Two-phase reachable local states:',len(seen))
print('Terminal states:',terminal)

# New local refinement: exact six-coupon MGF via exponential order spacings.
from fractions import Fraction
from math import log
phase_mgf=Fraction(1)
for j in range(1,7):
 phase_mgf*=Fraction(2*j,2*j-1)
assert phase_mgf==Fraction(1024,231)
service_mgf=phase_mgf**2
K=4*service_mgf
assert service_mgf==Fraction(1048576,53361)
assert K==Fraction(4194304,53361)
assert K>2
# The geometric-series bound is proved algebraically for all H>=1;
# these checks only exercise its exact arithmetic at selected H.
for H in range(1,20):
 assert sum(K**h for h in range(1,H+1))<=2*K**H
print('Exact phase MGF:',phase_mgf)
print('Exact two-phase MGF:',service_mgf,'=',float(service_mgf))
print('Exact path factor K:',K,'=',float(K))
print('Sufficient C lower limit 10 log K:',10*log(float(K)))
