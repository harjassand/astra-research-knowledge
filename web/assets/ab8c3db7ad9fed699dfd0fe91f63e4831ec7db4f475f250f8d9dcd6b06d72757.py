"""One fixed exact control: K_{2,2,2}, over Q(sqrt(13)). No scans or SDP.

Reconstructs the star blocks and a PSD-factor legal optimal Choi state;
checks all three marginals, BC swap, HS adjointness, Kraus TP and support.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
RAD=13
@dataclass(frozen=True)
class Q:
    a:F=F(0)
    b:F=F(0)
    def __post_init__(self):
        object.__setattr__(self,'a',F(self.a))
        object.__setattr__(self,'b',F(self.b))
    def __add__(self,o):
        o=coerce(o); return Q(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Q(-self.a,-self.b)
    def __sub__(self,o): return self+-coerce(o)
    def __rsub__(self,o): return coerce(o)+-self
    def __mul__(self,o):
        o=coerce(o); return Q(self.a*o.a+RAD*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=coerce(o); den=o.a*o.a-RAD*o.b*o.b
        assert den!=0
        return self*Q(o.a/den,-o.b/den)
    def __rtruediv__(self,o): return coerce(o)/self
    def sign(self):
        if self.b==0: return sgn(self.a)
        if self.a==0: return sgn(self.b)
        if self.a>0 and self.b>0: return 1
        if self.a<0 and self.b<0: return -1
        diff=self.a*self.a-RAD*self.b*self.b
        return sgn(diff) if self.a>0 else -sgn(diff)
    def encode(self): return {'a':str(self.a),'b':str(self.b),'radicand':RAD}
def coerce(o): return o if isinstance(o,Q) else Q(o)
def sgn(x): return (x>0)-(x<0)
ZERO=Q()
ONE=Q(1)

def inverse(matrix):
    n=len(matrix)
    a=[list(row)+[Q(int(i==j)) for j in range(n)] for i,row in enumerate(matrix)]
    for k in range(n):
        pivot=next(i for i in range(k,n) if a[i][k]!=ZERO)
        a[k],a[pivot]=a[pivot],a[k]
        scale=a[k][k]
        a[k]=[x/scale for x in a[k]]
        for i in range(n):
            if i!=k and a[i][k]!=ZERO:
                scale=a[i][k]
                a[i]=[x-scale*y for x,y in zip(a[i],a[k])]
    return [row[n:] for row in a]

d=6
part=lambda i:i//2
edges=[(i,j) for i in range(d) for j in range(i+1,d) if part(i)!=part(j)]
neighbors=[[j for j in range(d) if part(i)!=part(j)] for i in range(d)]
r,omega=4,3
mu=F(2,3)
lam=Q(1,1)
t=lam-r
assert t.sign()>0 and (mu-t).sign()>0
assert t*(t+F(r,1)/mu)==Q(r)
assert len(edges)==12 and all(len(row)==r for row in neighbors)
adj=[[int(j in neighbors[i]) for j in range(d)] for i in range(d)]
res=inverse([[lam-Q(adj[i][j]) if i==j else Q(-adj[i][j])
              for j in range(d)] for i in range(d)])
assert all(res[i][j]==res[j][i] for i in range(d) for j in range(d))
assert all(res[i][j].sign()>0 for i in range(d) for j in range(d))
assert all(lam*res[i][i]==Q(2) for i in range(d))
for i in range(d):
    for j in range(d):
        assert sum((lam*int(i==k)-adj[i][k])*res[k][j] for k in range(d))==Q(int(i==j))

vectors=[]
norms=[]
for k in range(d):
    v={(k,k,k):res[k][k]}
    for i in range(d):
        if i!=k:
            v[(i,i,k)]=res[i][k]
            v[(i,k,i)]=res[i][k]
    vectors.append(v)
    norms.append(sum(x*x for x in v.values()))
norm=norms[0]
assert norm.sign()>0 and all(x==norm for x in norms)

def add(mapping,key,value):
    mapping[key]=mapping.get(key,ZERO)+value
def action(vector):
    out={}
    for (a,b,c),value in vector.items():
        if a==b:
            for j in neighbors[a]: add(out,(j,j,c),2*value)
        if a==c:
            for j in neighbors[a]: add(out,(j,b,j),2*value)
    return {key:x for key,x in out.items() if x!=ZERO}

# Verify the exact block reduction on every basis vector, including the kernel.
sector_sets=[]
for k in range(d):
    states={(i,i,k) for i in range(d)}|{(i,k,i) for i in range(d)}
    assert len(states)==2*d-1
    sector_sets.append(states)
    expected={}
    for i,j in edges:
        for copy in [0,1]:
            vi=(i,i,k) if copy==0 else (i,k,i)
            vj=(j,j,k) if copy==0 else (j,k,j)
            add(expected,(vi,vj),Q(2)); add(expected,(vj,vi),Q(2))
    for row in states:
        actual=action({row:ONE})
        assert actual=={col:value for (col,rr),value in expected.items() if rr==row}
for k in range(d):
    for l in range(k): assert sector_sets[k].isdisjoint(sector_sets[l])
active=set().union(*sector_sets)
assert len(active)==66
zero_count=0
for state in product(range(d),repeat=3):
    if state not in active:
        assert action({state:ONE})=={}
        zero_count+=1
assert zero_count==150
for v in vectors:
    wv=action(v)
    assert wv=={key:2*lam*x for key,x in v.items()}

# Choi state is a manifestly PSD sum of six rank-one outer products.
choi={}
for v in vectors:
    for row,x in v.items():
        for col,y in v.items(): add(choi,(row,col),x*y/(d*norm))
assert sum(value for (row,col),value in choi.items() if row==col)==ONE
assert all(value==choi.get((col,row),ZERO) for (row,col),value in choi.items())
marg=[{} for _ in range(3)]
pair={}
for (row,col),value in choi.items():
    for reg in range(3):
        if all(row[q]==col[q] for q in range(3) if q!=reg):
            add(marg[reg],(row[reg],col[reg]),value)
    if row[2]==col[2]: add(pair,(row[:2],col[:2]),value)
    sr=(row[0],row[2],row[1]); sc=(col[0],col[2],col[1])
    assert value==choi.get((sr,sc),ZERO)
for matrix in marg:
    for i in range(d):
        for j in range(d): assert matrix.get((i,j),ZERO)==Q(F(int(i==j),d))
for (row,col),value in pair.items():
    assert value==pair.get((row[::-1],col[::-1]),ZERO)
    assert value==pair.get((col,row),ZERO)

# Independently check the explicit Kraus Gram sum, omitting common 1/sqrt(norm).
gram={}
for v in vectors:
    columns={i:{} for i in range(d)}
    for (i,b,c),value in v.items(): columns[i][(b,c)]=value
    for i in range(d):
        for j in range(d):
            inner=sum(x*columns[j].get(out,ZERO) for out,x in columns[i].items())
            add(gram,(i,j),inner/norm)
for i in range(d):
    for j in range(d): assert gram[(i,j)]==Q(int(i==j))
star=sum(sum(x*action(v).get(key,ZERO) for key,x in v.items()) for v in vectors)/(d*norm)
assert star==2*lam

# Exact common ensemble: all eight maximum cliques, each with eight sign states.
ensemble_bary=[[F(0) for _ in range(d)] for _ in range(d)]
cliques=list(product([0,1],[2,3],[4,5]))
count=0
for clique in cliques:
    for signs in product([-1,1],repeat=3):
        for a,i in enumerate(clique):
            for b,j in enumerate(clique):
                ensemble_bary[i][j]+=F(signs[a]*signs[b],3*64)
        p=[F(1,3) if i in clique else F(0) for i in range(d)]
        assert 4*sum(p[i]*p[j] for i,j in edges)==F(4,3)
        count+=1
assert count==64
assert ensemble_bary==[[F(int(i==j),d) for j in range(d)] for i in range(d)]
V=Q(8)
kval=Q(F(4,3))
ratio=(V-kval)/(V-lam)
assert ratio==Q(F(35,27),F(5,27)) and (2-ratio).sign()>0
result={
    'status':'ALL_EXACT_ASSERTIONS_PASSED',
    'graph':'K_{2,2,2}', 'vertices':d,'edges':len(edges),'degree':r,'omega':omega,
    'arithmetic':'fractions.Fraction in Q(sqrt(13)); no floats or solver',
    'scope':'one exact analytic sharp-family control; general theorem is in the proof file',
    'V':V.encode(),'k':kval.encode(),'legal_s':lam.encode(),
    'sharp_ratio':ratio.encode(),'normalizing_squared_norm':norm.encode(),
    'Choi_psd_factor_count':d,'Choi_nonzero_entries':len(choi),
    'all_marginals_tracial':True,'BC_swap':True,'HS_Choi_swap_and_transpose':True,
    'Kraus_TP':True,'star_eigen_equations':True,
    'star_block_count':d,'star_block_size':2*d-1,'zero_complement_dimension':zero_count,
    'common_support_ensemble_size':count,
    'resolvent':[[x.encode() for x in row] for row in res],
    'vectors':[{','.join(map(str,key)):value.encode() for key,value in v.items()} for v in vectors],
}
(ROOT/'K222_REPLAY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:value for key,value in result.items() if key not in ['resolvent','vectors']},indent=2))
