import sympy as S
from pathlib import Path
I=S.eye(2); q=S.Rational; j=S.I
paulis=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-j],[j,0]]),S.diag(1,-1)]
sig=[(I+q(3,5)*x)/2 for x in paulis]
M=sum((x.inv()/3 for x in sig),S.zeros(2)); U=M.inv(); omega=U/S.trace(U)
cost=[S.simplify(S.trace((x-U)*x.inv()*(x-U))) for x in sig]
assert cost==[q(3,11)]*3
# Independent noncommuting joint observable and exact operator variance bound.
A=S.Matrix([[1,1+j,2,0],[1-j,-2,j,1],[2,-j,0,2-j],[0,1,2+j,3]])/7
assert A==A.conjugate().T
def phi(s,A):
 return sum((s[b,a]*A[2*a:2*a+2,2*b:2*b+2] for a in range(2) for b in range(2)),S.zeros(2))
for s in sig:
 delta=omega-s; chi=S.simplify(S.trace(delta*s.inv()*delta)); V=phi(s,A*A)-phi(s,A)**2; d=phi(delta,A)
 defect=S.simplify(chi*V-d*d)
 assert defect==defect.conjugate().T
 assert defect[0,0]>=0 and defect[1,1]>=0 and S.det(defect)>=0
 assert chi==q(3,8)
 # At threshold q=3/11 the signed source second moment is dominated.
 reveal=q(3,11); erase=1-reveal; center=phi(omega,A); mi=phi(s,A)
 bi=(mi-erase*center)/reveal
 gap=S.simplify(phi(s,A*A)-reveal*bi*bi-erase*center*center)
 assert gap[0,0]>=0 and gap[1,1]>=0 and S.det(gap)>=0
print('Independent complex radius certificates, operator variance bounds and threshold signed observable compilation: PASS')
print('C=',cost[0],'; omega=',omega)
