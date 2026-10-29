"""Exact Hadamard/Mahler height bound for normalized value polynomial."""
import sympy as s,json,sys,math,time,hashlib
from pathlib import Path
from macaulay_template import matrices,compositions
sys.set_int_max_str_digits(0);r=Path(__file__).parent;j=json.load(open(r/'input.json'));q=s.symbols('q0:4');lam=s.symbols('lam');F=sum(s.Rational(c)*s.prod(q[i]**e[i] for i in range(4)) for e,c in zip(j['exponents'],j['perturbed']));D=4*s.ilcm(*[s.Rational(c).q for c in j['perturbed']]);Q=sum(v*v for v in q)
a=[s.Poly(D*s.diff(F,v)/4,*q) for v in q];b=[s.Poly(-D*Q*v,*q) for v in q];S=[]
for aa,bb in zip(a,b):
 ad=aa.as_dict();bd=bb.as_dict();S.append(sum((abs(int(ad.get(e,0)))+abs(int(bd.get(e,0))))**2 for e in set(ad)|set(bd)))
counts=[0]*4
for e in compositions(9,4):counts[next(i for i in range(4) if e[i]>=3)]+=1
prod=math.prod(si**ni for si,ni in zip(S,counts));ceilroot=math.isqrt(prod);ceilroot+=ceilroot*ceilroot<prod;H=(1<<40)*ceilroot
st=time.time();M,E=matrices([v.as_expr() for v in a],q,[3]*4);prime=1000000007
def determinant_mod(X):
 A=[[int(X[i,k])%prime for k in range(X.cols)] for i in range(X.rows)];det=1
 for c in range(X.rows):
  pivot=next((rr for rr in range(c,X.rows) if A[rr][c]),None)
  if pivot is None:return 0
  if pivot!=c:A[c],A[pivot]=A[pivot],A[c];det=-det
  d=A[c][c];det=det*d%prime;inv=pow(d,-1,prime)
  for rr in range(c+1,X.rows):
   mult=A[rr][c]*inv%prime
   if mult:
    for k in range(c+1,X.cols):A[rr][k]=(A[rr][k]-mult*A[c][k])%prime
    A[rr][c]=0
 return det%prime
det=determinant_mod(E);full_det=determinant_mod(M);assert full_det

assert det%prime
out=dict(common_scale=str(D),row_l2_squared_bounds=list(map(str,S)),row_counts=counts,primitive_coefficient_height_bound=str(H),height_bound_bits=H.bit_length(),required_crt_modulus_strictly_exceeds=str(2*H*H),required_crt_bits=(2*H*H).bit_length(),denominator_prime=prime,denominator_det_at_lambda0_modp=det%prime,full_matrix_det_at_lambda0_modp=full_det,denominator_dimension=E.rows,seconds=time.time()-st,input_sha256=hashlib.sha256((r/'input.json').read_bytes()).hexdigest(),scope='For primitive integer degree40 normalized value polynomial, exact coefficient bound via integer Macaulay determinant, Hadamard and Mahler factor bound. Separate denominator-nonzero witness. Not a probabilistic reconstruction check.')
(r/'value_polynomial_height_bound.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['primitive_coefficient_height_bound','required_crt_modulus_strictly_exceeds']},flush=True)
