"""Rational/algebraic exact dual certificate for the targeted rank-five frame.

Requires only sympy and numpy. Solver data proposes rational coefficients;
every final semidefinite claim is checked by exact algebraic pivots.
"""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
I=s.eye(3)
w=(-1+s.I*s.sqrt(3))/2
Z=s.diag(1,w,s.conjugate(w))
X=s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
def quad_scaled(U): return [U+U.conjugate().T,(U-U.conjugate().T)/s.I]
B=sum([quad_scaled(U) for U in [Z,X,X*Z,X*Z*Z]],[])
def k3(A,C,D): return s.kronecker_product(A,C,D)
P=s.zeros(27)
for a in range(3):
 for b in range(3):
  for c in range(3): P[a*9+c*3+b,a*9+b*3+c]=1
sym=lambda O:(O+P*O*P)/2
operators=[]
for A in B:
 for O in [k3(A,I,I),k3(I,A,I),k3(I,I,A)]:
  operators.append(sym(O))
for i,A in enumerate(B):
 for j in range(i):
  C=B[j]
  operators.append(sym(k3(A.T,C,I)-k3(C.T,A,I)))
# Exact small coefficients obtained by simplifying the numerical dual.
# No solver iterate is needed to define or verify this certificate.
coef=[s.S.Zero]*52
coef[13]=coef[14]=s.Rational(1,20)
coef[18]=s.Rational(1,2)
coef[39]=coef[46]=-s.Rational(1,35)
coef[40]=-s.sqrt(3)/35
coef[45]=s.sqrt(3)/35
coef[41]=s.Rational(2,35)
coef[48]=-s.Rational(2,35)
assert len(coef)==len(operators)==52
# Average annihilating constraints: the two receivers have identical
# marginals and the shared marginal is HS self-adjoint.
W=sum([k3(A.T,A,I)+k3(A.T,I,A) for A in B[:5]],s.zeros(27))/2
t=s.Rational(27,4)
Y=t*s.eye(27)-W+sum([c*O for c,O in zip(coef,operators)],s.zeros(27))
Y=Y.applyfunc(s.expand)
assert Y==Y.conjugate().T
K=s.QQ.algebraic_field(s.sqrt(3),s.I)
M=[[K.from_sympy(Y[i,j]) for j in range(27)] for i in range(27)]
def exact_positive_real(v):
    q=s.expand(K.to_sympy(v))
    assert s.expand(s.im(q))==0, q
    a=s.expand(q).coeff(s.sqrt(3),0)
    b=s.expand(q).coeff(s.sqrt(3),1)
    assert a.is_Rational and b.is_Rational and s.expand(q-a-b*s.sqrt(3))==0, q
    if a>=0 and b>=0: return (a>0 or b>0), q
    if a<=0 and b<=0: return False,q
    if a>=0 and b<0: return a*a>3*b*b,q
    return 3*b*b>a*a,q
pivots=[]
for k in range(27):
    pivot=M[k][k]
    positive,q=exact_positive_real(pivot)
    assert positive, (k,q)
    pivots.append(str(q))
    for i in range(k+1,27):
        for j in range(k+1,27):
            M[i][j]-=M[i][k]*M[k][j]/pivot
report={'status':'EXACT_PASS','upper_bound':'27/4','C2_threshold':7,
        'V':5,'k':2,'coefficient_field':'Q(sqrt(3)), denominators divide 140',
        'zero_moment_coefficients':[str(c) for c in coef],
        'exact_positive_ldl_pivots':pivots,
        'proof':'All 27 exact Hermitian Gaussian elimination pivots lie in Q(sqrt(3)) and are positive by rational-square comparisons. Thus (27/4)I-W+sum c_j C_j is positive definite. Every C_j has expectation zero under the exact tracial, equal-marginal, HS-self-adjoint interface.'}
(OUT/'mub_rank5_exact_exclusion.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='exact_positive_ldl_pivots'},indent=2))
print('Exact positive pivot count:',len(pivots))
