from itertools import combinations, permutations, product
from fractions import Fraction

n=6
old=4
FULL=(1<<n)-1
F4=[[0,0,1,1],[0,0,1,-1],[0,0,0,0],[0,0,0,0]]
G=[[0,1],[1,0]]

def det(a):
    if not a:return 1
    z=0
    for p in permutations(range(len(a))):
        inv=sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
        t=-1 if inv%2 else 1
        for i,j in enumerate(p):t*=a[i][j]
        z+=t
    return z

def sig(F):
    out={}
    for U in range(1<<n):
        R=[i for i in range(n) if not (U>>i)&1]
        if len(R)%2:out[U]=0;continue
        k=len(R)//2
        s=0
        for I in combinations(R,k):
            Is=set(I); J=[j for j in R if j not in Is]
            s+=det([[F[i][j] for j in J] for i in I])**2
        out[U]=s
    return out

old_pairs=((0,1),(0,2),(0,3))
def defect_slice(s):
    pair_masks=[(1<<i)|(1<<j) for i,j in old_pairs]
    cap=sum(s[p]*s[15^p] for p in pair_masks)
    return cap-s[0]*s[15]

def trans_slice(s, edge, w):
    a,b=edge
    e=(1<<a)|(1<<b)
    t=dict(s)
    for U in range(16):
        if U.bit_count()%2==0 and U&e==0:
            t[U]=s[U]+w*s[U|e]
    return t

base=[[0]*n for _ in range(n)]
for i in range(4):
    for j in range(4):base[i][j]=F4[i][j]
for i in range(2):
    for j in range(2):base[4+i][4+j]=G[i][j]

base_sig=sig(base)
base_slice={U:base_sig[U] for U in range(16)}
print('base block diag delta',defect_slice(base_slice),'slice',base_slice)
found=[]
for ii,jj in [(i,j) for i in range(4) for j in range(4,6)]+[(i,j) for i in range(4,6) for j in range(4)]:
  for sign in (-1,1):
    F=[row[:] for row in base];F[ii][jj]=sign
    ss=sig(F); sl={U:ss[U] for U in range(16)}
    d0=defect_slice(sl)
    if d0>=0:continue
    for a in range(4):
      for b in range(4,6):
        for w in (1,2,4,8):
          tr=trans_slice(ss,(a,b),w)
          tl={U:tr[U] for U in range(16)}
          d1=defect_slice(tl)
          if d1>=0:
            found.append((d0,d1,(ii,jj,sign),(a,b,w),sl,tl))
            print('FOUND',found[-1])
            raise SystemExit
    print('no repair for cross entry',ii,jj,sign,'base delta',d0)
print('NONE',len(found))

import random
rng=random.Random(620261007)
cross_edges=[(i,j) for i in range(4) for j in (4,5)]
def trans_cross_slice(ss,w):
  out={}
  for U in range(16):
    if U.bit_count()%2:out[U]=Fraction(0);continue
    available=FULL^U; val=ss[U]
    allowed=[e for e in cross_edges if (available>>e[0])&1 and (available>>e[1])&1]
    for e in allowed: val+=w*ss[U|(1<<e[0])|(1<<e[1])]
    for e1,e2 in combinations(allowed,2):
      if len(set(e1+e2))==4:
        val+=w*w*ss[U|(1<<e1[0])|(1<<e1[1])|(1<<e2[0])|(1<<e2[1])]
    out[U]=val
  return out

cross_vals=[Fraction(-1,4),Fraction(0),Fraction(1,4)]
aux_vals=[Fraction(1,4),Fraction(1),Fraction(4),Fraction(16),Fraction(64)]
neg=0
for trial in range(500):
  F=[[Fraction(x) for x in row] for row in base]
  for i in range(4):
    for j in (4,5):F[i][j]=rng.choice(cross_vals)
  for i in (4,5):
    for j in range(4):F[i][j]=rng.choice(cross_vals)
  ss=sig(F); sl={U:ss[U] for U in range(16)};d0=defect_slice(sl)
  if d0>=0:continue
  neg+=1
  for w in aux_vals:
    ex=trans_cross_slice(ss,w);d1=defect_slice(ex)
    if d1>=0:
      print('FOUND trial',trial,'delta',d0,d1,'aux',w,'F',[[str(x) for x in r] for r in F], 'before', {k:str(v) for k,v in sl.items()},'after',{k:str(v) for k,v in ex.items()})
      raise SystemExit
print('NO REPAIR; negative base fixtures',neg)
