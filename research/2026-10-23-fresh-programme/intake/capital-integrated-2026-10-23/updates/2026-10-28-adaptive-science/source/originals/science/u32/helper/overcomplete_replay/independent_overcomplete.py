"""Independent rational verification of the lift and residual correction, no counts claimed."""
from fractions import Fraction as Q
from pathlib import Path
import json

def mat(a): return [[Q(x) for x in row] for row in a]
def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]
def eye(n): return [[Q(i==j) for j in range(n)] for i in range(n)]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def neg(a): return [[-x for x in row] for row in a]
def sub(a,b): return add(a,neg(b))
def absolute(a): return [[abs(x) for x in row] for row in a]
def inv(a):
    n=len(a);b=[row[:]+irow for row,irow in zip(a,eye(n))]
    for j in range(n):
        pivot=next(i for i in range(j,n) if b[i][j])
        b[j],b[pivot]=b[pivot],b[j]
        scale=b[j][j];b[j]=[x/scale for x in b[j]]
        for i in range(n):
            if i!=j:
                scale=b[i][j];b[i]=[x-scale*y for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]
def minimum(a):return min(x for row in a for x in row)
def encode(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,list):return [encode(y) for y in x]
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    return x

lam=Q(13,20)
VB=mat([[1,1,1,1],[0,1,0,-1],[1,0,-1,0]])
LB=mat([[Q(1,4),0,Q(1,2)],[Q(1,4),Q(1,2),0],
        [Q(1,4),0,Q(-1,2)],[Q(1,4),Q(-1,2),0]])
assert mm(VB,LB)==eye(3)
R=mat([[1,0,0],[0,0,lam],[0,-lam,0]])
cycle=mat([[0,0,0,1],[1,0,0,0],[0,1,0,0],[0,0,1,0]])
KR=[[lam*x+(1-lam)/4 for x in row] for row in cycle]
CB={('R',0):R};K={('R',0):KR}
for sign in [1,-1]:
    effect=mat([[Q(1,2),0,Q(sign,4)]])
    state=mat([[1],[0],[Q(sign,2)]])
    CB['M',sign]=mm(state,effect)
    weights=[Q(1,8)]*4;weights[0 if sign==1 else 2]+=Q(1,2)
    K['M',sign]=mm([[x] for x in weights],mm(effect,VB))
for z in K:
    assert mm(VB,K[z])==mm(CB[z],VB)
    assert minimum(K[z])>0
for a in ['R','M']:
    assert all(sum(K[z][i][j] for z in K if z[0]==a for i in range(4))==1 for j in range(4))
assert minimum(KR)==Q(7,80)
assert min(minimum(K[z]) for z in K if z[0]=='M')==Q(1,32)
assert sum(R[i][i] for i in range(3))==1
assert sum(mm(R,R)[i][i] for i in range(3))==1-2*lam*lam==Q(31,200)<Q(1,3)

# An explicit normalized legal core: start +Z, R once, R twice.
B=mat([[1,1,1],[0,lam,0],[1,0,-lam*lam]])
Binv=inv(B)
# Empty test, M+, and R then M+.
F=mat([[1,0,0],[Q(1,2),0,Q(1,4)],[Q(1,2),-lam/4,0]])
H=mm(F,B);Hinv=inv(H)
assert mm(H,Hinv)==eye(3)
V=mm(Binv,VB);L=mm(LB,B)
assert mm(V,L)==eye(3)
assert mm([[Q(1)]*3],V)==[[Q(1)]*4]
assert mm([[Q(1)]*4],L)==[[Q(1)]*3]
eta=[[Q(1)],[Q(0)],[Q(0)],[Q(0)]]
assert mm(V,eta)==[[Q(1)],[Q(0)],[Q(0)]]
Hz={z:mm(mm(F,c),B) for z,c in CB.items()}
C={z:mm(Hinv,hz) for z,hz in Hz.items()}
for z in C:
    assert C[z]==mm(mm(Binv,CB[z]),B)
    assert mm(V,K[z])==mm(C[z],V)

# Nonzero fit residual and nonzero confidence widths challenge the general correction.
# These are abstract algebraic intervals, not fabricated acquisition counts.
Khat={z:[row[:] for row in k] for z,k in K.items()}
epsilon=Q(1,100000)
for z in Khat:
    Khat[z][0][0]-=epsilon
    Khat[z][1][0]+=epsilon
width=Q(1,100000000)
DH=[[Q(0)]*3,[width]*3,[width]*3]
AH=mm(absolute(Hinv),DH)
nu=max(sum(row) for row in AH)
assert nu<1
MH=mm(inv(sub(eye(3),AH)),absolute(Hinv))
assert minimum(MH)>=0 and mm(sub(eye(3),AH),MH)==absolute(Hinv)
min_margin=None
for z in Khat:
    DZ=[[Q(0)]*3 if i==0 and z[0]=='R' else [width]*3 for i in range(3)]
    Rhat=sub(mm(Hz[z],V),mm(mm(H,V),Khat[z]))
    E=mm(mm(absolute(L),MH),add(add(absolute(Rhat),mm(DZ,absolute(V))),mm(DH,absolute(mm(V,Khat[z])))))
    Ktrue=add(Khat[z],mm(L,sub(mm(C[z],V),mm(V,Khat[z]))))
    assert mm(V,Ktrue)==mm(C[z],V)
    assert all(abs(Ktrue[i][j]-Khat[z][i][j])<=E[i][j] for i in range(4) for j in range(4))
    margin=minimum(sub(Khat[z],E))
    assert margin>0
    min_margin=margin if min_margin is None else min(min_margin,margin)
    Khat[z]=(Khat[z],Ktrue)
for a in ['R','M']:
    assert all(sum(Khat[z][1][i][j] for z in Khat if z[0]==a for i in range(4))==1 for j in range(4))

result={'status':'PASS','scope':'Exact algebraic fixture, no count acquisition',
        'lambda':lam,'rank_three_legal_core':'start +Z, R once, R twice; tests empty, M+, R then M+',
        'bloch_trace_covector':[1,0,0],'normalized_preparation_coordinate_translation':'V=B^{-1} V_Bloch; L=L_Bloch B',
        'three_state_trace_P_squared':Q(31,200),'three_state_necessary_lower':Q(1,3),
        'four_state_rotation_margin':Q(7,80),'four_state_measurement_margin':Q(1,32),
        'nonzero_residual_test_epsilon':epsilon,'abstract_confidence_width':width,
        'residual_test_inverse_nu':nu,'residual_test_certified_margin':min_margin,
        'all_intertwining_mass_initial_and_residual_checks':'PASS'}
root=Path(__file__).resolve().parent
(root/'INDEPENDENT_OVERCOMPLETE_CHECKS.json').write_text(json.dumps(encode(result),indent=2)+'\n')
print(json.dumps(encode(result),indent=2))
