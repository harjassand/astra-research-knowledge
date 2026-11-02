"""Two-rib inherited-edge fiber per old Fe coordinate; parent-vertex endpoints relative.
C1 order A−,A0,A+,B−,B0,B+,c0,c1.
"""
import json
from sheaf_incidence_compiler import echelon
blue=[(1<<0)|(1<<1)|(1<<6),(1<<1)|(1<<2)|(1<<7),(1<<3)|(1<<4)|(1<<6),(1<<4)|(1<<5)|(1<<7)]
red=[]
for before,after,c in [(0,1,6),(1,2,7),(3,4,6),(4,5,7)]:red.extend([(1<<before)|(1<<c),(1<<after)|(1<<c)])
rB,rR=len(echelon(blue)),len(echelon(red))
assert rB==4 and rR==7
assert all(c.bit_count()%2==0 for c in red)
print(json.dumps(dict(scope=__doc__,blue=dict(C0=4,C1=8,rankD0=rB,H0=0,H1=4,D0=blue),red=dict(C0=8,C1=8,rankD0=rR,H0=1,H1=1,D0=red,P1='total parity of8 labels; quotient isomorphism')),indent=2))
