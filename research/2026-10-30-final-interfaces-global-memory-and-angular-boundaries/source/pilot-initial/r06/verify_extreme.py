"""Independent exact exposed-ray verifier; Python standard library only.

Reconstructs all 35 quartics, 64 acoustic-kernel equations, a nonzero
34 by 34 minor, and the rational positive exposing functional.
No imports from the symbolic derivation or supplied producer/verifier.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import permutations
from math import gcd,lcm,prod
import json,time

HERE=Path(__file__).resolve().parent
start=time.perf_counter()
data=json.loads((HERE/'acoustic_face_result.json').read_text())
C=Q(83981,2710)
assert C>2  # t^4-C t^2+1 has four distinct REAL roots.
K=[{0:761510,2:-25254181}, {1:761510,3:1655520},
   {1:810290,3:-1710280}, {0:810290,2:-23400039}]
exponents=[(i,j,k,4-i-j-k) for i in range(5) for j in range(5-i) for k in range(5-i-j)]
assert len(exponents)==35 and [list(e) for e in exponents]==data['monomial_exponents']

def add(*polys):
    out={}
    for pp in polys:
        for e,co in pp.items():out[e]=out.get(e,Q(0))+co
    return {e:co for e,co in out.items() if co}

def scale(pp,co):return {e:co*x for e,x in pp.items() if co*x}

def mul(pp,qq):
    out={}
    for a,co in pp.items():
        for b,cc in qq.items():
            e=tuple(x+y for x,y in zip(a,b))
            out[e]=out.get(e,Q(0))+co*cc
    return {e:co for e,co in out.items() if co}

def reduced(pp):
    # monomials are s^u t^v. Relation t^4=C t^2-1.
    out=dict(pp)
    while any(v>=4 for u,v in out):
        u,v=max((e for e in out if e[1]>=4),key=lambda e:e[1])
        co=out.pop((u,v))
        out[(u,v-2)]=out.get((u,v-2),Q(0))+C*co
        out[(u,v-4)]=out.get((u,v-4),Q(0))-co
        out={e:co for e,co in out.items() if co}
    return out

KK=[]
for i,j,sign in ((0,2,-1),(1,3,-1),(2,0,1),(3,1,1)):
    KK.append(add({(0,n):Q(co) for n,co in K[i].items()},
                  {(1,n):Q(sign*co) for n,co in K[j].items()}))

def evaluated_hessian(exponent):
    out=[[{} for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            co=exponent[i]*(exponent[j]-int(i==j))
            if not co:continue
            e=list(exponent);e[i]-=1;e[j]-=1
            out[i][j]={(e[2]+e[3],e[1]+e[3]):Q(co)}
    return out

rows=[(i,u,v) for i in range(4) for u in range(4) for v in range(4)]
columns=[];functional=[];hessians=[]
for exponent in exponents:
    hh=evaluated_hessian(exponent);hessians.append(hh)
    vv=[reduced(add(*(mul(hh[i][j],KK[j]) for j in range(4)))) for i in range(4)]
    assert all(u<=3 and v<=3 for pp in vv for u,v in pp)
    columns.append([vv[i].get((u,v),Q(0)) for i,u,v in rows])
    scalar=reduced(add(*(mul(KK[i],vv[i]) for i in range(4))))
    assert all(u<=4 and v<=3 for u,v in scalar)
    average={v:sum((Q(weight,8)*scalar.get((u,v),0) for u,weight in ((0,3),(2,1),(4,3))),Q(0)) for v in range(4)}
    # Newton sums for the four roots of t^4-Ct^2+1:
    # tr(1)=4, tr(t)=tr(t^3)=0, tr(t^2)=2C.
    functional.append(4*average[0]+2*C*average[2])
E=[list(row) for row in zip(*columns)]

# Reconstruct F exactly from its invariant formula.
AA=[{tuple(int(i==j) for j in range(4)):Q(1)} for i in range(4)]
T=add(*(mul(x,x) for x in AA))
q=add(mul(AA[0],AA[3]),scale(mul(AA[1],AA[2]),-1))
X=add(mul(AA[0],AA[0]),mul(AA[2],AA[2]),scale(mul(AA[1],AA[1]),-1),scale(mul(AA[3],AA[3]),-1))
F=add(mul(T,T),scale(mul(q,q),Q(3132,301)),scale(mul(q,X),Q(1196,301)))
fv=[F.get(e,Q(0)) for e in exponents]
assert fv[-1]==1
assert all(sum(x*y for x,y in zip(row,fv))==0 for row in E)

def determinant(matrix):
    n=len(matrix)
    den=[lcm(*(Q(x).denominator for x in row)) for row in matrix]
    aa=[[int(Q(x)*den[i]) for x in row] for i,row in enumerate(matrix)]
    previous=1;sign=1
    for k in range(n-1):
        pivot_row=next((i for i in range(k,n) if aa[i][k]),None)
        if pivot_row is None:return Q(0)
        if pivot_row!=k:aa[k],aa[pivot_row]=aa[pivot_row],aa[k];sign=-sign
        pivot=aa[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                val=aa[i][j]*pivot-aa[i][k]*aa[k][j]
                assert val%previous==0
                aa[i][j]=val//previous
            aa[i][k]=0
        previous=pivot
    return Q(sign*aa[-1][-1],prod(den))

ii=data['nonzero_minor_rows'];jj=data['nonzero_minor_columns']
minor=[[E[i][j] for j in jj] for i in ii]
det=determinant(minor)
assert det!=0 and det==Q(data['nonzero_minor_determinant'])
# One nonzero 34-minor and the exhibited nonzero kernel imply exact rank 34.
den=lcm(*(x.denominator for x in functional))
raw=[int(x*den) for x in functional]
common=gcd(*raw)
primitive=[x//common for x in raw]
assert primitive==data['positive_exposing_functional_coefficients']
assert Q(den,common)==Q(data['exposing_functional_scale'])
assert sum(x*y for x,y in zip(primitive,fv))==0 and primitive[-1]>0

# Hessian at each rank-one R_t=(1,t,0,0). Compute its determinant as a
# polynomial, then compare the exact acoustic determinant factorization.
HR=[[add(*(scale(hessians[k][i][j],fv[k]) for k in range(35))) for j in range(4)] for i in range(4)]
HR=[[{e:co for e,co in pp.items() if e[0]==0} for pp in row] for row in HR]
detpoly={}
for perm in permutations(range(4)):
    inv=sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
    term={(0,0):Q((-1)**inv)}
    for i in range(4):term=mul(term,HR[i][perm[i]])
    detpoly=add(detpoly,term)
m={(0,4):Q(2710),(0,2):Q(-83981),(0,0):Q(2710)}
assert detpoly==scale(mul(m,m),Q(36864,8208541201))
H0=[[pp.get((0,0),Q(0)) for pp in row] for row in HR]
assert all(determinant([row[:n] for row in H0[:n]])>0 for n in range(1,5))

out={'quartic_dimension':35,'acoustic_constraint_matrix':[64,35],
     'exact_rank':34,'four_simple_real_acoustic_roots':True,
     'nonzero_minor_checked':True,'only_kernel_is_the_inherited_seed':True,
     'rational_exposing_functional_rebuilt':True,
     'acoustic_determinant_square_identity':True,
     'rank_one_Hessian_positive_definite_at_E11':True,
     'conclusion':'F_(299/301,1084/301) spans an exposed ray of the FULL homogeneous-quartic rank-one-convex cone; inherited quasiconvexity gives the same exposed ray in the quasiconvex cone.',
     'seconds':time.perf_counter()-start}
(HERE/'extreme_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
