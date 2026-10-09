#!/usr/bin/env python3
"""One exact complex noncommuting qutrit physical identity control; not a universal proof."""
import sympy as sp
import json,hashlib,time
from pathlib import Path
start=time.monotonic(); I=sp.I
S=sp.diag(1,2,4); d=sp.diag(1,sp.sqrt(2),2)
v=sp.Matrix([1,1,I]); Q=sp.eye(3)-sp.Rational(2,3)*(v*v.conjugate().T)
B=sp.Matrix([[1,1+I,2],[1-I,-1,1+2*I],[2,1-2*I,0]])
sigma=S*S/21; rho=Q*sigma*Q.conjugate().T; q=Q*S*Q.conjugate().T/sp.sqrt(21)
log2,k=sp.symbols('log2 k',real=True)
logsigma=sp.diag(0,2*log2,4*log2); logrho=Q*logsigma*Q.conjugate().T
simp=lambda x:sp.simplify(sp.expand(x))
checks={}
def check(name,x):
 ok=all(simp(z)==0 for z in x) if isinstance(x,sp.MatrixBase) else simp(x)==0
 checks[name]=bool(ok)
 if not ok:raise AssertionError((name,x))
check('unitary_Q',Q.conjugate().T*Q-sp.eye(3));check('root',q*q-rho)
assert sigma*rho-rho*sigma != sp.zeros(3)
assert B==B.conjugate().T
V=sp.Matrix(3,3,lambda i,j:2*(B*S*B)[i,j]/(S[i,i]+S[j,j]))
K=d*B*d.inv();C=d*V*d.inv()
L=lambda R:(C*R+R*C.conjugate().T)/2-K*R*K.conjugate().T
H=lambda R:(V*R+R*V)/2-B*R*B
check('trace_preserving',C+C.conjugate().T-2*K.conjugate().T*K)
check('stationary',L(sigma));check('weighted_stationary',H(S));check('tracezero',sp.trace(L(rho)))
J=simp(sp.trace(L(rho)*(logrho-logsigma)))
E=simp(sp.trace(q*H(q)))
components={w:sp.Matrix(3,3,lambda i,j:B[i,j] if i-j==w else 0) for w in range(-2,3)}
entries={w:Q.conjugate().T*M*Q for w,M in components.items()}
for w in components:check('adjoint_'+str(w),components[-w]-components[w].conjugate().T)
# Nodes are integer multiples of log2. Hyperbolic values are exact algebraic.
power=lambda n:sp.Integer(2)**n
sinh=lambda n:(power(n)-power(-n))/2
cosh=lambda n:(power(n)+power(-n))/2
def kernel(a,b):
 return (log2*(a*sinh(b)+b*sinh(a))-2*k*sinh(sp.Rational(a,2))*sinh(sp.Rational(b,2)))/(2*cosh(sp.Rational(a-b,2)))
gram=0
for i in range(3):
 for j in range(3):
  beta=i-j
  for w in components:
   for z in components:
    gram+=2*sp.Rational(power(i+j),21)*sp.conjugate(entries[w][i,j])*kernel(beta-w,beta-z)*entries[z][i,j]
gram=simp(gram)
check('physical_equals_ordered_modular_Gram',J-k*E-gram)
check('physical_entropy_log_coefficient',sp.diff(J-k*E-gram,log2))
check('physical_energy_coefficient',sp.diff(J-k*E-gram,k))
record={'status':'PASS_EXACT_FINITE_IDENTITY_CONTROL_NOT_PROOF','checks':checks,'assertions':len(checks),'dimension':3,'complex_noncommuting':True,'all_state_and_reference_eigenvalues_positive':['1/21','4/21','16/21'],'J':str(J),'E':str(E),'gram':str(gram),'elapsed_seconds':time.monotonic()-start,'sympy':sp.__version__}
print(json.dumps(record,indent=2))
