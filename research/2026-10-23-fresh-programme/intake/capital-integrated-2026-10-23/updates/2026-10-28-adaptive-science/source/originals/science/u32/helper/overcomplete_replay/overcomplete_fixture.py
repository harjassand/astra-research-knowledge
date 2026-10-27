"""Exact rational algebra fixture; not count acquisition or a latent oracle."""
from fractions import Fraction as F
from pathlib import Path
import json

def mat(a):return [[F(v) for v in row] for row in a]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def minimum(a):return min(x for row in a for x in row)
def encode(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,list):return [encode(x) for x in v]
    if isinstance(v,dict):return {k:encode(x) for k,x in v.items()}
    return v

lam=F(13,20)
V=mat([[1,1,1,1],[0,1,0,-1],[1,0,-1,0]])
L=mat([[F(1,4),0,F(1,2)],[F(1,4),F(1,2),0],
       [F(1,4),0,F(-1,2)],[F(1,4),F(-1,2),0]])
assert mul(V,L)==mat([[1,0,0],[0,1,0],[0,0,1]])
R=mat([[1,0,0],[0,0,lam],[0,-lam,0]])
cycle=mat([[0,0,0,1],[1,0,0,0],[0,1,0,0],[0,0,1,0]])
KR=[[lam*x+(1-lam)/4 for x in row] for row in cycle]
assert mul(V,KR)==mul(R,V)

measurement=[];Kmeasurement=[]
for sign in [1,-1]:
    effect=[F(1,2),F(0),F(sign,4)]
    state=[F(1),F(0),F(sign,2)]
    C=[[x*y for y in effect] for x in state]
    weights=[F(1,8)]*4;weights[0 if sign==1 else 2]+=F(1,2)
    probabilities=mul([effect],V)[0]
    K=[[x*p for p in probabilities] for x in weights]
    assert mul(V,K)==mul(C,V)
    measurement.append(C);Kmeasurement.append(K)
for j in range(4):
    assert sum(KR[i][j] for i in range(4))==1
    assert sum(K[i][j] for K in Kmeasurement for i in range(4))==1
assert 1-2*lam**2<F(1,3)
out={'scope':'Exact representation algebra, no count acquisition',
     'observable_rank':3,'positive_lift_dimension':4,'lambda':lam,
     'three_state_trace_P_squared':1-2*lam**2,'three_state_necessary_lower':F(1,3),
     'rotation_branch_margin':minimum(KR),
     'measurement_branch_margin':min(minimum(K) for K in Kmeasurement),
     'V':V,'right_inverse_L':L,'K_rotation':KR,'K_measurement':Kmeasurement,
     'all_intertwining_and_causality_checks':'PASS'}
root=Path(__file__).resolve().parent
(root/'overcomplete_fixture.json').write_text(json.dumps(encode(out),indent=2)+'\n')
print(json.dumps(encode({k:out[k] for k in ['scope','observable_rank','positive_lift_dimension','three_state_trace_P_squared','three_state_necessary_lower','rotation_branch_margin','measurement_branch_margin','all_intertwining_and_causality_checks']}),indent=2))
