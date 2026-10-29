"""Modular witness for an explicitly good quartic perturbation direction.
This verifies separateness of normalized eigenvalues, not only z coordinates.
"""
import sympy as s,json,sys,time,hashlib
from pathlib import Path
sys.set_int_max_str_digits(0);r=Path(__file__).parent;st=time.time();j=json.load(open(r/'input.json'));shape=json.load(open(r/'shape.json'));x,y,z=s.symbols('x y z');basis=[s.sympify(v) for v in shape['lex_basis']];prime=1000000007

def modrat(c):
 c=s.Rational(c);a,b=int(c.p),int(c.q);assert b%prime;return (a%prime)*pow(b%prime,-1,prime)%prime

def mp(expr):
 p=s.Poly(expr,z);return s.Poly.from_dict({(e[0],):modrat(c) for e,c in p.terms()},z,modulus=prime)
U=mp(basis[2]).monic();assert U.degree()==40 and s.gcd(U,U.diff()).degree()==0
cx=s.Poly(basis[0],x,y,z).coeff_monomial(x);cy=s.Poly(basis[1],x,y,z).coeff_monomial(y)
P=mp(-basis[0].subs(x,0)/cx)%U;Q=mp(-basis[1].subs(y,0)/cy)%U
one=mp(1);zz=mp(z);vs=[one,P,Q,zz]
def mul(a,b):return (a*b)%U
def power(a,k):
 out=one
 for _ in range(k):out=mul(out,a)
 return out
norm=(one+mul(P,P)+mul(Q,Q)+mul(zz,zz))%U;assert s.gcd(norm,U).degree()==0
num=mp(0)
for e,c in zip(j['exponents'],j['perturbed']):
 if e[0]==0:continue
 v=mp(modrat(s.Rational(c)*e[0]));ee=list(e);ee[0]-=1
 for a,k in zip(vs,ee):v=mul(v,power(a,k))
 num=(num+v)%U
lam=mul(num,s.invert(norm,U)).mul_ground(pow(4,-1,prime))%U
cols=[];v=one
for k in range(40):
 cols.append([int(v.nth(i))%prime for i in range(40)]);v=mul(v,lam)
A=[[cols[c][rr] for c in range(40)] for rr in range(40)];rank=0;det=1
for c in range(40):
 pivot=next((rr for rr in range(rank,40) if A[rr][c]),None)
 if pivot is None:continue
 if pivot!=rank:A[rank],A[pivot]=A[pivot],A[rank];det=-det
 d=A[rank][c];det=det*d%prime;iv=pow(d,-1,prime);A[rank]=[v*iv%prime for v in A[rank]]
 for rr in range(rank+1,40):
  a=A[rr][c]
  if a:A[rr]=[(u-a*v)%prime for u,v in zip(A[rr],A[rank])]
 rank+=1
assert rank==40
out=dict(prime=prime,U_degree=40,U_squarefree=True,norm_invertible=True,krylov_rank=rank,krylov_determinant_modp=det%prime,lambda_coefficients_low_to_high=[int(lam.nth(i))%prime for i in range(40)],seconds=time.time()-st,input_sha256=hashlib.sha256((r/'input.json').read_bytes()).hexdigest(),shape_sha256=hashlib.sha256((r/'shape.json').read_bytes()).hexdigest(),scope='Given exact radical degree40 shape and projective coverage, full-rank normalized-objective Krylov witness implies40 distinct normalized eigenvalues overQ. Combined with retained B!=0 witness makes this one rational quartic a fixed good direction.')
(r/'fixed_good_direction_modp.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
