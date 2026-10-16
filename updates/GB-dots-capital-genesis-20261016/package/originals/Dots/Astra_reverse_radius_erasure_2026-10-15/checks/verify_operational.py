import sympy as s
from itertools import combinations
Q=s.Rational
T=s.Matrix([[Q(1,2),Q(1,6),Q(1,3)],[Q(1,3),Q(1,2),Q(1,6)],[Q(1,6),Q(1,3),Q(1,2)]])
c=Q(2,11); w=s.ones(3,1)/3
D=s.Matrix.hstack(*[(T[:,i]-(1-c)*w)/c for i in range(3)],w)
Eq=s.Matrix.vstack(c*s.eye(3),(1-c)*s.ones(1,3))
assert D*Eq==T
print('Exact signed compiler D=',D)
for i in range(3):
    M=s.diag(*T[:,i])-D*s.diag(*Eq[:,i])*D.T
    minors=[M.extract(ix,ix).det() for k in range(1,4) for ix in combinations(range(3),k)]
    assert all(x>=0 for x in minors)
    print('Input',i,'covariance minors:',minors)
vs=[s.Matrix([1/s.sqrt(2),1/s.sqrt(6)]),s.Matrix([-1/s.sqrt(2),1/s.sqrt(6)]),s.Matrix([0,-2/s.sqrt(6)])]
eps=Q(1,1000); delta=Q(1,1000); amplitude=Q(1,1000)
Rs=[(v*v.T+eps*s.eye(2))/(1+3*eps) for v in vs]
zs=[v/s.sqrt(3) for v in vs]
Ein=sum((4*z.T*(R+delta*s.eye(2)/3).inv()*z)[0] for R,z in zip(Rs,zs))
Nout=0
for y in range(3):
    A=sum((T[y,i]*Rs[i] for i in range(3)),s.zeros(2)); z=sum((T[y,i]*zs[i] for i in range(3)),s.zeros(2,1)); b=sum(T[y,i]/3 for i in range(3))
    Nout+=(4*z.T*(A+delta*b*s.eye(2)).inv()*z)[0]
Ein=s.simplify(Ein);Nout=s.simplify(Nout);q=Q(1,6)
assert Nout>q*Ein
# Schur complement positivity of sigma_i +/- amplitude H_i.
for R,z in zip(Rs,zs):assert s.simplify(delta/3-amplitude**2*(z.T*R.inv()*z)[0])>0
# Dividing all blocks by 2+delta normalizes. Average sigma, centered states +/- amplitude H.
risk_gap=s.factor(amplitude**2*(Nout-q*Ein)/(2+delta))
print('SLD input cost:',Ein)
print('SLD target cost:',Nout)
print('SLD ratio:',s.factor(Nout/Ein),float(Nout/Ein),' > q=',q)
print('All binary encoded states faithful by exact Schur complements.')
print('Exact MMSE(E_q)-MMSE(T):',risk_gap,'=',float(risk_gap))
