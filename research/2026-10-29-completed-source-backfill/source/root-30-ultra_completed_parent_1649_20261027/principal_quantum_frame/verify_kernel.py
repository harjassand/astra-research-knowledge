"""Independent standard-library exact replay of the actual local kernels.
Rebuilds the gate superoperator using Gaussian rationals, without importing
the LP/compiler, NumPy, SymPy, or a saved Pauli transfer matrix.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,time,hashlib
ROOT=Path(__file__).resolve().parent
zero=(F(0),F(0));one=(F(1),F(0))
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def total(items):
    value=zero
    for x in items:value=add(value,x)
    return value
def mm(A,B):return [[total(mul(A[i][k],B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tensor(A,B):return [[mul(A[i//len(B)][j//len(B)],B[i%len(B)][j%len(B)]) for j in range(len(A)*len(B))] for i in range(len(A)*len(B))]
def real(A):return [[(F(x),F(0)) for x in row] for row in A]
def solve3(A,b):
    M=[[F(x) for x in a]+[F(v)] for a,v in zip(A,b)]
    for j in range(3):
        candidates=[i for i in range(j,3) if M[i][j]]
        if not candidates:return None
        i=candidates[0];M[i],M[j]=M[j],M[i];d=M[j][j];M[j]=[x/d for x in M[j]]
        for i in range(3):
            if i!=j:
                t=M[i][j];M[i]=[x-t*y for x,y in zip(M[i],M[j])]
    return tuple(row[-1] for row in M)


start=time.monotonic();raw=(ROOT/'EXACT24_KERNEL.json').read_bytes();data=json.loads(raw)
frames=[tuple(map(F,r)) for r in data['local_Bloch_vertices']]
assert len(set(frames))==24 and all(sum(x*x for x in r)==1 for r in frames)
# Exact polytope: infinity norm<=4/5 and1norm<=7/5. Check all vertices
# of this rational H-representation, not a sampled sphere.
facets=[]
for i in range(3):
    for sign in (-1,1):
        n=[0,0,0];n[i]=sign;facets.append((n,F(4,5)))
from itertools import product
facets.extend((list(s),F(7,5)) for s in product((-1,1),repeat=3))
found=set()
for triple in combinations(facets,3):
    x=solve3([a for a,b in triple],[b for a,b in triple])
    if x is not None and all(sum(ai*xi for ai,xi in zip(a,x))<=b for a,b in facets):found.add(x)
assert found==set(frames)
assert F(16,25)*3<F(49,25)  # ball4/5 fits every1norm facet
assert F(12,25)<F(16,25)    # t²=12/25, hence D_t(PSD) is inside
# Reservedwhite weight1/64 is below(1-sqrt(3)/2)^2=7/4-sqrt3.
assert F(3)<F(111,64)**2
I=real([[1,0],[0,1]]);X=real([[0,1],[1,0]])
Y=[[zero,(F(0),F(-1))],[(F(0),F(1)),zero]];Z=real([[1,0],[0,-1]])
basis=[tensor(a,b) for a in (I,X,Y,Z) for b in (I,X,Y,Z)]
U=real(data['gate_rows']);Ut=[list(row) for row in zip(*U)]
assert mm(U,Ut)==real([[int(i==j) for j in range(4)] for i in range(4)])
conjugated=[mm(mm(U,P),Ut) for P in basis]
transfer=[]
for P in basis:
    row=[]
    for Q in conjugated:
        trace=total(mul(P[i][j],Q[j][i]) for i in range(4) for j in range(4))
        assert trace[1]==0;row.append(trace[0]/4)
    transfer.append(row)
noise=[F(1),-F(2,5),F(2,5),-F(2,5)]
factors=[x*y for x in noise for y in noise]
transfer=[[factors[i]*x for x in row] for i,row in enumerate(transfer)]
ext=[(F(1),)+r for r in frames];columns=[[x*y for x in a for y in b] for a in ext for b in ext]
avg=[sum((a[i] for a in columns),F(0))/576 for i in range(16)]
assert avg==[F(1)]+[F(0)]*15
reserve=F(data['reserved_uniform_product_probability'])
assert reserve==F(1,64)
for j,kernel in enumerate(data['kernels']):
    assert kernel['input_pair']==[j//24,j%24]
    ids=kernel['output_pair_indices'];weights=list(map(F,kernel['remainder_probabilities']))
    assert len(ids)==len(weights)<=16 and all(0<=i<576 for i in ids)
    assert min(weights)>=0 and sum(weights)==1
    for row in range(16):
        lhs=reserve*avg[row]+(1-reserve)*sum((w*columns[i][row] for i,w in zip(ids,weights)),F(0))
        rhs=sum((x*y for x,y in zip(transfer[row],columns[j])),F(0))
        assert lhs==rhs
assert len(data['kernels'])==576
out={'status':'INDEPENDENT_EXACT_LOCAL_KERNEL_AND_POLYTOPE_PASS',
 'kernel_sha256':hashlib.sha256(raw).hexdigest(),'rational_polytope_vertices':len(found),
 'exact_channel_columns':576,'exact_real_Hermitian_equations':9216,
 'nonnegative_and_stochastic':True,'seconds':time.monotonic()-start,
 'scope':'Exact acquired gate/noise kernels and geometric24-frame check. General circuit composition/noise acquisition and theorem boundaries are in PROOF.md; no physical or advantage claim.'}
(ROOT/'INDEPENDENT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
