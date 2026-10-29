"""Numerical high-precision finder only; exact interval verification is a separate obligation."""
import sys,json,time,mpmath as mp,sympy as sp
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).parent;SRC=Path('producer-workspace/grevlex_value_oracle_20261029');j=json.loads((SRC/'quotient.json').read_text());mp.mp.dps=160;st=time.time()
def cv(s):
 x=F(s);return mp.mpf(x.numerator)/x.denominator
m=[mp.matrix([[cv(cols[c][r]) for c in range(40)] for r in range(40)]) for cols in j['multiplication_columns']];I=mp.eye(40);Q=I.copy()
for A in m:Q+=A*A
powers=[[I,A,A*A,A*A*A] for A in m];num=mp.zeros(40)
for e,c in j['f0_terms']:
 v=I
 for k,a in enumerate(e):
  if a:v=v*powers[k][a]
 num+=cv(c)*v
L=mp.inverse(Q)*num/4
old_iv=json.loads((SRC/'root_candidate_certificate.json').read_text())['least_real_value_interval'];cs=list(map(int,json.loads((SRC/'candidate.json').read_text())['integer_coefficients_low_to_high']));t=sp.Symbol('t');poly=sp.Poly.from_list(cs[::-1],t);iv=[str(x) for x in sp.refine_root(poly,sp.Rational(old_iv[0]),sp.Rational(old_iv[1]),eps=sp.Rational(1,2**100),fast=True)];mid=(F(iv[0])+F(iv[1]))/2;A=L.T-cv(str(mid))*I
for k in range(40):A[0,k]=int(k==0)
b=mp.zeros(40,1);b[0]=1;C=mp.inverse(A);w=C*b;print('coords',[str(w[i]) for i in [3,2,1]],'seconds',time.time()-st,flush=True)
bits=512;scale=1<<bits
def dyad(M):return [[str(int(mp.nint(M[r,c]*scale))) for c in range(M.cols)] for r in range(M.rows)]
out={'status':'HIGH_PRECISION_FINDER_NOT_INTERVAL_CERTIFICATE','seconds':time.time()-st,'precision_digits':mp.mp.dps,'dyadic_bits':bits,'approximate_Q_inverse_integer':dyad(mp.inverse(Q)),'approximate_L_integer':dyad(L),'approximate_A_inverse_integer':dyad(C),'midpoint':str(mid),'root_interval':iv,'coordinate_approx':[str(w[i]) for i in [3,2,1]]};(P/'left_eigenvector_finder.json').write_text(json.dumps(out,indent=2)+'\n')
