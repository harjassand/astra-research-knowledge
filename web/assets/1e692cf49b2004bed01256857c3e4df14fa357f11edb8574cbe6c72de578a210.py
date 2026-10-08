import sympy as s, json, math, pathlib, itertools, sys
from functools import lru_cache
BASE=pathlib.Path(__file__).resolve().parent

def mul(a,b,L):
 c=[s.S.Zero]*L
 for i,ai in enumerate(a):
  if ai:
   for j,bj in enumerate(b[:L-i]):
    if bj:c[i+j]+=ai*bj
 return c

def multi(n,L):
 out=[[s.S.One]+[s.S.Zero]*(L-1)]
 for i in range(1,n+1):
  f=[s.S.Zero]+[s.Rational((-1)**(k+1),k*i**k) for k in range(1,L)]
  out += [mul(x,f,L) for x in out[:]]
 return out

def extremal(n):
 L=2**n+8
 series=multi(n,L)
 A=s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix(series).T[:2**n-1,:]).convert_to(s.QQ)
 ns=A.nullspace().to_Matrix()
 print('n',n,'nullity',ns.rows,flush=True)
 v=list(ns[0,:]);den=s.ilcm(*[a.q for a in v]); v=[int(a*den) for a in v];g=math.gcd(*v);v=[a//g for a in v]
 if v[-1]<0:v=[-a for a in v]
 orders=[]
 for k in range(L):
  r=sum(c*f[k] for c,f in zip(v,series))
  if r: orders.append([k,str(r)])
  if len(orders)>=3:break
 out={'n':n,'coefficients':list(v),'first_nonzero':orders}
 (BASE/f'extremal_multiaffine_{n}.json').write_text(json.dumps(out,indent=2))
 print('degrees',[(j,sum(c!=0 for a,c in enumerate(v) if a.bit_count()==j)) for j in range(n+1)],'order',orders[0][0], 'maxbits',max(abs(c).bit_length() for c in v), flush=True)
 return v

if __name__=='__main__':
 for n in map(int,sys.argv[1:] or [2,3,4,5]):extremal(n)
