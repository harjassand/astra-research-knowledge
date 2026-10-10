"""Exact commutator-family verification. No numerical sampling or physics claim."""
import sympy as s
from fractions import Fraction
from math import lgamma, log, exp
import json
from pathlib import Path
out={}
for k in (2,3,4):
 I=s.eye(k); B=[]; R=[]
 for a in range(k):
  E=s.zeros(k); E[a,a]=1; E-=I/k
  B.extend([E,E])
 for a in range(k):
  for b in range(a+1,k):
   U=s.zeros(k); U[a,b]=U[b,a]=1
   V=s.zeros(k); V[a,b]=s.I; V[b,a]=-s.I
   B.extend([U,V]); R.extend([U,V])
 for a in range(k-1):
  E=s.zeros(k); E[a,a]=1; E[k-1,k-1]=-1; R.append(E)
 A=[s.Matrix([[-s.I*s.trace(T*(U*V-V*U)) for V in B] for U in B]) for T in R]
 H=s.Matrix([[s.trace(U*V.T) for V in A] for U in A]); HI=H.inv()
 GR=s.Matrix([[s.trace(U*V) for V in R] for U in R]); GB=s.Matrix([[s.trace(U*V) for V in B] for U in B])
 M=s.zeros(len(B))
 for i in range(len(R)):
  for j in range(len(R)):
   if HI[i,j]: M+=HI[i,j]*A[i]*A[j].T
 assert H==8*k*GR
 assert M==GB/2
 assert M*M==M and M.rank()==k*k-1
 assert all(x.is_Rational for U in A for x in U)
 assert all(U.T==-U for U in A)
 D=9;m=k*k-1;r=D*k
 C=Fraction(1)
 for j in range(1,m+1): C*=Fraction(r,r-2*j)
 a=exp((m/2)*log(2/r)+lgamma(r/2)-lgamma((r-m)/2))
 out[str(k)]={'copies_D':D,'constraints_m':m,'raw_variables_per_copy':len(B),'raw_A_rational':True,'H_formula_verified':'H0=8*k*Gram(R)','native_M_formula_verified':'M_D=Gram(B)/(2D), eigenvalues 1/D or 0','native_rank':D,'commutator_rank':r,'acceptance_lower_bound_numeric':a,'C_r_2m_exact':str(C),'C_r_2m_numeric':float(C),'minimal_physical_config_squared_norm_mean':(D-1)*m,'naive_config_squared_norm_mean':D*m}
mu1=[s.Rational(1),s.Rational(-1),s.Rational(0)]
mu2=[s.Rational(5,7),s.Rational(-8,7),s.Rational(3,7)]
def prodmu(mu):
 return s.prod(1+4*(mu[a]-mu[b])**2 for a in range(3) for b in range(a+1,3))
assert sum(x*x for x in mu1)==sum(x*x for x in mu2)==2
assert prodmu(mu1)!=prodmu(mu2)
out['nonradial_su3']={'squared_norm_both':2,'diagonal_spectra':[[str(x) for x in mu1],[str(x) for x in mu2]],'determinant_base_values':[str(prodmu(mu1)),str(prodmu(mu2))],'full_det':'base^(2D)','exact_unequal':True}
path=Path(__file__).with_name('GAUSS_PHYSICS_EXACT_CHECKS.json');path.write_text(json.dumps(out,indent=2)+'\n')
print(path.read_text())
