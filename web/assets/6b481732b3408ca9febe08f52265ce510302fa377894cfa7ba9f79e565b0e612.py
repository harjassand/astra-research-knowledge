"""Exact standard-library replay of the fixed C5 obstruction and local dual.

No floating point, eigenvalue optimizer, SDP solver, or external package.
The full 125-dimensional matrix splits into 27 blocks of size at most 27.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
t = F(21, 20)
h = [t, F(1), F(1)]
w = [x*x for x in h]
z = [F(2)-t, t, t]
gs = [x*x for x in z]
ls = [F(2), t*t+1, t*t+1]
ks = [a+b for a,b in zip(ls, gs)]
dval = [F(-7,5)]*3 + [F(2), F(11,5)]
d2 = [x*x for x in dval]
L = [ls[i]+d2[i] if i<3 else d2[i] for i in range(5)]
G = [gs[i]+d2[i] if i<3 else d2[i] for i in range(5)]
K = [a+b for a,b in zip(L,G)]
X = [F(3,5)*ks[i]+d2[i] if i<3 else d2[i] for i in range(5)]
Y = [F(1,5)*ks[i]+d2[i]/2 if i<3 else d2[i]/2 for i in range(5)]
assert sum(dval)==0
assert [X[i]+2*Y[i] for i in range(5)]==K
V, kval = sum(L)/5, sum(G)/5
assert V==F(837,200) and kval==F(7131,2000)
assert V-kval==F(1239,2000) and V+kval==F(15501,2000)

# Check the matching spin plane-pair ensemble using rational populations.
beta = [4*hi-sum(h) for hi in h]
p = []
pop = [F(0)]*3
score = F(0)
for i in range(3):
    j,k = [q for q in range(3) if q!=i]
    pi = beta[i]*(z[j]+z[k])/(6*z[j]*z[k])
    ti = z[k]/(z[j]+z[k])
    p.append(pi)
    pop[j] += pi*ti
    pop[k] += pi*(1-ti)
    score += pi*4*w[i]*ti*(1-ti)
assert sum(p)==1 and pop==[F(1,3)]*3
assert score==sum(gs)/3
assert F(3,5)*score+sum(d2)/5==kval

# Ji=i Ri. Hence Ji^T tensor Ji = Ri tensor Ri, fixing the Choi sign.
R = [
    [[0,0,0],[0,0,-1],[0,1,0]],
    [[0,0,1],[0,0,0],[-1,0,0]],
    [[0,-1,0],[1,0,0],[0,0,0]],
]
def rval(q,a,b):
    return R[q][a][b] if a<3 and b<3 else 0

basis = list(product(range(5), repeat=3))
index = {v:i for i,v in enumerate(basis)}
def wentry(row,col):
    a,b,c = row
    aa,bb,cc = col
    value = F(0)
    if c==cc:
        value += sum(w[q]*rval(q,a,aa)*rval(q,b,bb) for q in range(3))
    if b==bb:
        value += sum(w[q]*rval(q,a,aa)*rval(q,c,cc) for q in range(3))
    if row==col:
        value += dval[a]*(dval[b]+dval[c])
    return value

W = [[wentry(row,col) for col in basis] for row in basis]
def local_deficit(row,col):
    a,b,c = row
    return (X[a]+Y[b]+Y[c] if row==col else F(0))-W[index[row]][index[col]]
Dmat = [[local_deficit(row,col) for col in basis] for row in basis]
assert all(Dmat[i][j]==Dmat[j][i] for i in range(125) for j in range(125))

v = {(0,0,0):4,(0,1,1):-2,(0,2,2):-2,
     (1,0,1):3,(1,1,0):3,(2,0,2):3,(2,2,0):3}
norm = sum(c*c for c in v.values())
assert norm==60
q0=q1=F(0)
for row,cr in v.items():
    for col,cc in v.items():
        a,b,c=row
        q0 += cr*cc*((K[b]+K[c])/2 if row==col else 0)
        q0 -= cr*cc*W[index[row]][index[col]]
        if row==col:
            q1 += cr*cc*(K[a]-(K[b]+K[c])/2)
q0/=norm
q1/=norm
assert q0==F(-67,2400) and q1==F(121,2400)
row=(3,4,4)
a,b,c=row
c0=(K[b]+K[c])/2-W[index[row]][index[row]]
c1=K[a]-(K[b]+K[c])/2
assert c0==F(22,25) and c1==F(-42,25)
lower,upper = -q0/q1,-c0/c1
assert lower==F(67,121) and upper==F(11,21) and lower>upper

def sector(row):
    return tuple(0 if a<3 else a for a in row)
groups={}
for i,row in enumerate(basis):
    groups.setdefault(sector(row),[]).append(i)
assert len(groups)==27 and sum(map(len,groups.values()))==125
for i,row in enumerate(basis):
    for j,col in enumerate(basis):
        if sector(row)!=sector(col):
            assert Dmat[i][j]==0

def exact_psd_ldl(matrix):
    m=[row[:] for row in matrix]
    n=len(m)
    pivots=[]
    for k in range(n):
        pivot=m[k][k]
        assert pivot>=0, (k,pivot)
        pivots.append(pivot)
        if pivot==0:
            assert all(m[k][j]==0 for j in range(k,n)), (k,'zero pivot with nonzero row')
            continue
        column=[m[i][k] for i in range(n)]
        for i in range(k+1,n):
            for j in range(i,n):
                m[i][j] -= column[i]*column[j]/pivot
                m[j][i] = m[i][j]
        for i in range(k+1,n):
            m[i][k]=m[k][i]=F(0)
    return pivots

blocks=[]
for tag,ids in sorted(groups.items()):
    matrix=[[Dmat[i][j] for j in ids] for i in ids]
    pivots=exact_psd_ldl(matrix)
    blocks.append({'sector':tag,'size':len(ids),
                   'positive_pivots':sum(x>0 for x in pivots),
                   'zero_pivots':sum(x==0 for x in pivots),
                   'pivots':[str(x) for x in pivots]})

gap=F(17,5)
pair_norm_upper_bound=sum(w)
mixed_margin=gap*gap/2-pair_norm_upper_bound
assert pair_norm_upper_bound==F(1241,400)
assert mixed_margin==F(1071,400)>0
result={
    'status':'ALL_EXACT_ASSERTIONS_PASSED',
    'arithmetic':'fractions.Fraction only',
    'scope':'fixed C5 scalar obstruction and corrected dual; not the general broadcast gate',
    'V':str(V),'k':str(kval),'V_minus_k':str(V-kval),
    'dual_budget':str(V+kval),
    'spin_ensemble_pair_weights':[str(x) for x in p],
    'spin_witness_q0':str(q0),'spin_witness_q1':str(q1),
    'classical_witness_q0':str(c0),'classical_witness_q1':str(c1),
    'alpha_lower':str(lower),'alpha_upper':str(upper),
    'pair_norm_analytic_upper_bound':str(pair_norm_upper_bound),
    'mixed_sector_margin':str(mixed_margin),
    'full_dimension':125,'block_count':len(blocks),
    'largest_block':max(item['size'] for item in blocks),
    'blocks':blocks,
}
(ROOT/'REPLAY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='blocks'},indent=2))
