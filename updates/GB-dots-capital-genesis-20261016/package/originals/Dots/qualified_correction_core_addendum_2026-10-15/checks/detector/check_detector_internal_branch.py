"""Exact intended-target detector versus unsafe actual-internal-branch comparison."""
import sympy as S
I=S.eye(2);X=S.Matrix([[0,1],[1,0]]);p=[S.diag(1,0),S.diag(0,1)];k=S.kronecker_product
c=S.Rational(99,101);s=S.Rational(20,101)
# Data d, extraction ancilla a. Initial a=0; trusted prelabel is data Z syndrome.
CNOT=k(p[0],I)+k(p[1],X)
noise=k(I,c*I-S.I*s*X)
assert noise.H*noise==S.eye(4)
for pre in range(2):
 v=S.zeros(4,1);v[2*pre]=1
 extracted=noise*CNOT*v
 safe_bad=S.Rational(0);unsafe_bad=S.Rational(0)
 for internal in range(2):
  # Correctly recorded actual ancilla value, followed by exact conditional X.
  branch=k(X**internal,p[internal])*extracted
  for post in range(2):
   out=k(p[post],I)*branch
   prob=S.simplify((out.H*out)[0])
   # Correct ideal reset has predicted final data syndrome zero for BOTH prelabels.
   if post!=0:safe_bad+=prob
   # Unsafe prediction follows the possibly wrong measured internal branch.
   if post!=(pre^internal):unsafe_bad+=prob
 assert safe_bad==s*s and unsafe_bad==0
 # Deleting the ancilla perturbation makes the intended detector null.
 ideal=CNOT*v
 for internal in range(2):
  assert k(p[1],I)*k(X**internal,p[internal])*ideal==S.zeros(4,1)
print('PASS: intended-target mismatch probability 400/10201; actual-internal-branch comparator misses every wrong correction; deletion-null exact at zero perturbation.')
