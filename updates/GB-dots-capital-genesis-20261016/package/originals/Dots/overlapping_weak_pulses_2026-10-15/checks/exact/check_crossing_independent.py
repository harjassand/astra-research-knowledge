"""Independent exact causal-instrument audit of crossing shared-bath echoes."""
import sympy as S
I=S.eye(2); X=S.Matrix([[0,1],[1,0]]); Z=S.diag(1,-1)
k=S.kronecker_product; N=S.eye(8)
H=k(X,I,X); K=k(I,X,Z); ZA=k(Z,I,I); ZC=k(I,Z,I)
c=S.Rational(99,101); s=S.Rational(20,101)
R=c*N-S.I*s*H; T=c*N-S.I*s*K
assert H*K==-K*H and R.H*R==N and T.H*T==N
# Isometry from arbitrary bath input to memory |00> and bath.
V=S.zeros(8,2); V[0,0]=1; V[1,1]=1
expected={(0,0):(1-2*s**4)**2,
          (1,0):4*c*c*s**6,
          (0,1):4*s**6*c*c,
          (1,1):4*c**4*s**4}
# Whole-unitary Fourier operators computed independently from sign-toggled gates.
chars={}
for a in range(2):
 for b in range(2):
  B=S.zeros(8)
  for f in range(2):
   for g in range(2):
    Rf=c*N-S.I*(-1)**f*s*H; Tg=c*N-S.I*(-1)**g*s*K
    W=Tg.H*Rf.H*Tg*Rf
    B+=(-1)**(a*f+b*g)*W/4
  chars[a,b]=B
  assert B.H*B==expected[a,b]*N
assert sum(expected.values())==1
# Genuine syndrome measurements at the two separate completion times.
# Apply the actual frame gates at their starts and undos, not just a final twirl.
for f in range(2):
 for g in range(2):
  FA=ZA**f; FC=ZC**g
  at_A=FA*R.H*T*FC*R*FA
  finish_C=FC*T.H
  for a in range(2):
   PA=(N+(-1)**a*ZA)/2
   partial=PA*at_A*V
   assert partial.H*partial==(expected[a,0]+expected[a,1])*I
   for b in range(2):
    PC=(N+(-1)**b*ZC)/2
    M=PC*finish_C*partial
    assert M.H*M==expected[a,b]*I
prob_A=expected[1,0]+expected[1,1]
conditional=S.cancel(expected[1,1]/prob_A)
assert prob_A>0 and conditional==c*c
# a=b=2 atan(1/10)<1/5, hence squared integrated action (2b)^2<4/25.
assert conditional>S.Rational(4,25)
# Each half rotation has squared norm distance 4/101; a two-half triangle bound is 16/101.
assert (R-N).H*(R-N)==S.Rational(4,101)*N
assert conditional>S.Rational(16,101)
assert R.H*R==N and T.H*T==N # each isolated echo is identity
print('PASS: whole-character and actual causal-measurement effects agree for every bath input and every private frame.')
print('Pr(A_bad)=',prob_A,'; Pr(C_bad | A_bad)=',conditional)
print('Conditional exceeds integrated-action-square upper bound 4/25 and norm-triangle-square bound 16/101.')
# Recording the first syndrome is nondisturbing on the frame-averaged encoded domain.
for g in range(2):
 FC=ZC**g
 for i in range(2):
  for j in range(2):
   E=S.zeros(2);E[i,j]=1
   rho=S.zeros(8)
   for f in range(2):
    FA=ZA**f; partial=FA*R.H*T*FC*R*FA
    rho+=partial*V*E*V.H*partial.H/2
   assert (rho+ZA*rho*ZA)/2==rho
print('PASS: intermediate syndrome recording does not disturb the averaged encoded channel, including bath-reference coherences.')
