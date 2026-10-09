#!/usr/bin/env python3
"""Exact 3-cycle cross-term failure and repaired clip replay; no optimizers.

Run from the workspace root. Sections 1-7 of the associated theorem file
prove the general implication; this script checks its specified witness.
"""
from fractions import Fraction as F
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent / "ENTROPY_REPLAY_RESULT.json"


def zero(n, m=None):
    return [[F(0) for _ in range(m or n)] for _ in range(n)]


def eye(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = F(1)
    return a


def add(a, b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def trans(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum((x*y for x,y in zip(row,col)), F(0))
             for col in zip(*b)] for row in a]


def tr(a):
    return sum((row[i] for i,row in enumerate(a)), F(0))


def tau(a):
    return tr(a)/len(a)


def unit(n, i, j):
    a = zero(n)
    a[i][j] = F(1)
    return a


def apply_kraus(ks, a):
    ans = zero(len(ks[0]))
    for k in ks:
        ans = add(ans, mul(mul(k,a),trans(k)))
    return ans


def ptr_output(a, keep):
    """One 3-dimensional marginal from a two-output 9 by 9 matrix."""
    r = zero(3)
    for i in range(3):
        for j in range(3):
            for z in range(3):
                ai,aj = ((3*i+z,3*j+z) if keep==0
                         else (3*z+i,3*z+j))
                r[i][j] += a[ai][aj]
    return r


def choi_single(r, keep):
    a = zero(3)
    for i in range(3):
        for j in range(3):
            for p in range(3):
                for q in range(3):
                    ix = [p,q]; iy = [p,q]
                    ix.insert(keep,i); iy.insert(keep,j)
                    flat = lambda v: 9*v[0]+3*v[1]+v[2]
                    a[i][j] += r[flat(ix)][flat(iy)]
    return a


ks=[]
bs=[]
for j in range(3):
    s=(j+1)%3
    k=zero(3); k[s][j]=F(1); ks.append(k)
    b=zero(9,3); b[3*s+s][j]=F(1); bs.append(b)

ktp=zero(3); btp=zero(3)
for k in ks:
    ktp=add(ktp,mul(trans(k),k))
for b in bs:
    btp=add(btp,mul(trans(b),b))
assert ktp==btp==eye(3)
phi=lambda a:apply_kraus(ks,a)
broad=lambda a:apply_kraus(bs,a)
assert phi(eye(3))==eye(3)
for i in range(3):
    for j in range(3):
        a=unit(3,i,j)
        ba=broad(a)
        assert ptr_output(ba,0)==ptr_output(ba,1)==phi(a)

# Normalized broadcaster Choi state is the sum of three positive rank-one
# computational-basis projectors divided by 3. No PSD solver is required.
r=zero(27)
for j in range(3):
    s=(j+1)%3
    ix=9*j+3*s+s
    r[ix][ix]=F(1,3)
assert tr(r)==1
assert all(choi_single(r,j)==scale(F(1,3),eye(3)) for j in range(3))
for i in range(27):
    for j in range(27):
        swap=lambda x:9*(x//9)+3*(x%3)+(x%9)//3
        assert r[i][j]==r[swap(i)][swap(j)]

# HS matrix in ordered matrix-unit coordinates. Entries are real here,
# so transpose is the complex HS adjoint matrix too.
p=zero(9)
for i in range(3):
    for j in range(3):
        a=phi(unit(3,i,j))
        for b in range(3):
            for c in range(3):
                p[3*b+c][3*i+j]=a[b][c]
assert p!=trans(p)
pa=trans(p)
sym=scale(F(1,2),add(p,pa))
dephase=zero(9)
for j in range(3):
    dephase[3*j+j][3*j+j]=F(1)

# Canonical basis ensemble p_j=1/3. Its map is precisely dephasing.
def canonical(a):
    ans=zero(3)
    for j in range(3):
        pi=unit(3,j,j)
        ans=add(ans,scale(tr(mul(pi,a)),pi))
    return ans
for i in range(3):
    for j in range(3):
        expected=unit(3,i,j) if i==j else zero(3)
        assert canonical(unit(3,i,j))==expected

# Exact positive Gram decomposition of Psi-symPhi, certifying C=1.
cert=zero(9)
for i,j in [(0,1),(0,2),(1,2)]:
    v=zero(9,1)
    v[3*i+i][0]=F(1); v[3*j+j][0]=F(-1)
    cert=add(cert,scale(F(1,2),mul(v,trans(v))))
assert add(dephase,scale(F(-1),sym))==cert

x=zero(3); f=zero(3); g=zero(3)
t=F(3,2)
for j in range(3):
    x[j][j]=F(j); f[j][j]=min(F(j),t); g[j][j]=x[j][j]-f[j][j]
assert tau(x)==1
assert mul(f,g)==scale(t,g)
adj=lambda a:apply_kraus([trans(k) for k in ks],a)
cross=lambda op:tau(mul(f,add(x,scale(F(-1),op(x)))))
a=cross(phi); b=cross(adj); c=(a+b)/2
energy=tau(mul(f,add(f,scale(F(-1),phi(f)))))
remainder=tau(mul(f,add(g,scale(F(-1),phi(g)))))
q=tau(g)
eps=sum((abs(x[j][j]-phi(x)[j][j]) for j in range(3)),F(0))/3
assert (a,b,c,energy,remainder,q,eps)==(F(5,6),F(2,3),F(3,4),F(7,12),F(1,4),F(1,6),F(4,3))
assert a!=c and energy==tau(mul(f,add(f,scale(F(-1),adj(f)))))
assert energy+remainder==a and 0<=energy<=a<=t*eps/2
assert remainder==tau(mul(add(scale(t,eye(3)),scale(F(-1),f)),phi(g)))
assert canonical(x)==x

result={
  "status":"EXACT_RATIONAL_REPLAY_PASS",
  "scope":"Specified legal 3-cycle witness and C=1 canonical comparator; general theorem is proved separately",
  "kraus_TP":True,"Phi_unital":True,"both_broadcaster_marginals_equal_Phi":True,
  "all_three_Choi_marginals_tracial":True,"BC_Choi_swap_symmetry":True,
  "Phi_not_HS_selfadjoint":True,"canonical_dephasing_comparator":True,
  "C1_comparator_exact_positive_Gram_certificate":True,
  "dimension":3,"t":str(t),"X_diagonal":["0","1","2"],
  "Phi_cross":str(a),"Phi_adj_cross":str(b),"sym_cross":str(c),
  "proposed_cross_equality_fails":True,"clip_energy":str(energy),
  "clip_remainder":str(remainder),"q":str(q),"epsilon":str(eps),
  "t_epsilon_over_2":str(t*eps/2),"repaired_clip_bound_holds":True,
  "no_numerical_optimizer":True,"arithmetic":"Python fractions.Fraction"
}
OUT.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
