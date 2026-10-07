#!/usr/bin/env python3
"""One-query sparse NC polynomial interpolation using affine word moments.
Source matrices: Lakhani-Mukhopadhyay ECCC TR26-120 July2026.
Finite exact diagnostics of independently derived Prony decoder.
"""
import sympy as sp
from math import comb
import random,json

def matrices(n,s):
 B=n+1;d=2*s
 return [sp.Matrix(d,d,lambda a,b:comb(b,a)*B**a*j**(b-a) if a<=b else 0) for j in range(1,n+1)]
def evaluate(terms,aa):
 d=aa[0].rows;f=sp.zeros(d)
 for word,c in terms.items():
  aw=sp.eye(d)
  for j in word: aw=aw*aa[j-1]
  f+=c*aw
 return f

def word_from_code(alpha,n):
 B=n+1;rev=[]
 while alpha>1:
  alpha,j=divmod(alpha,B)
  assert 1<=j<=n
  rev.append(j)
 assert alpha==1
 return tuple(reversed(rev))

def interpolate(n,s,response):
 moments=list(sp.ones(1,2*s)*response)
 H=sp.Matrix(s,s,lambda a,b:moments[a+b]);r=H.rank()
 if r==0:return {},{'rank':0}
 Hr=sp.Matrix(r,r,lambda a,b:moments[a+b]);rhs=sp.Matrix([-moments[a+r] for a in range(r)])
 coeff=Hr.inv()*rhs;z=sp.Symbol('z');p=sp.Poly(z**r+sum(coeff[j]*z**j for j in range(r)),z)
 roots=sp.polys.polytools.ground_roots(p)
 assert sum(roots.values())==r and all(v==1 and a.is_Integer and a>=1 for a,v in roots.items())
 alphas=sorted(map(int,roots));V=sp.Matrix(r,r,lambda a,b:alphas[b]**a);cs=V.inv()*sp.Matrix(moments[:r])
 result={word_from_code(a,n):c for a,c in zip(alphas,cs)}
 assert all(sum(c*a**k for a,c in zip(alphas,cs))==moments[k] for k in range(2*s))
 maxbits=max((max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for x in moments),default=0)
 return result,{'rank':r,'max_moment_height_bits':maxbits,'support_lengths':[len(w) for w in result]}

rng=random.Random(50726);cases=[]
fixtures=[{():sp.Rational(3,7),(1,2):sp.Rational(-2,5),(2,1):sp.Rational(11,3)},
          {(1,):sp.Rational(1),(2,):sp.Rational(-1)}, # zeroth moment cancellation
          {}, {(1,)*30:sp.Rational(1,13),(2,1,2)*7:sp.Rational(-9,17)}]
for _ in range(20):
 terms={}
 for __ in range(rng.randint(1,4)):
  word=tuple(rng.randint(1,3) for ___ in range(rng.randint(0,12)))
  c=sp.Rational(rng.choice([-3,-2,-1,1,2,3]),rng.randint(1,7))
  terms[word]=terms.get(word,0)+c
 terms={w:c for w,c in terms.items() if c!=0}
 fixtures.append(terms)
for case,terms in enumerate(fixtures):
 n=3;s=4;aa=matrices(n,s);response=evaluate(terms,aa)
 got,info=interpolate(n,s,response)
 assert got==terms,(terms,got)
 # Simulate each moment by a fixed first-diagonal readout, at unchanged dimension.
 for j in range(2*s):
  P=sp.Matrix([list(sp.ones(1,2*s))]+[list(sp.eye(2*s).row(k)) for k in range(2*s) if k!=j])
  assert P.det() in [1,-1]
  assert (P*response*P.inv())[0,0]==sum(response[i,j] for i in range(2*s))
 cases.append({'case':case,**info})
print(json.dumps({'status':'PASS','query_dimension':8,'cases':cases},indent=2))
