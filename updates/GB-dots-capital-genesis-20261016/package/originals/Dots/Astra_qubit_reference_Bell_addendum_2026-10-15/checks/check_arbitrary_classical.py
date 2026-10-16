import sympy as s
Q=s.Rational
S=s.Matrix([[Q(3,8),Q(1,8)],[Q(1,8),Q(3,8)],[Q(1,2),Q(1,2)]])
T=s.Matrix([[Q(13,20),Q(7,20)],[Q(7,20),Q(13,20)]])
D=s.Matrix([[Q(11,10),-Q(1,10),Q(1,2)],[-Q(1,10),Q(11,10),Q(1,2)]])
assert D*S==T and D.T*s.ones(2,1)==s.ones(3,1)
for i in range(2):
    M=s.diag(*T[:,i])-D*s.diag(*S[:,i])*D.T
    assert M==Q(7,100)*s.Matrix([[1,-1],[-1,1]])
print('POSITIVE nondegradation pair: exact common D and PSD covariance defects verified.')
# Infeasible unique-lift pair and exact dual-to-vector extraction.
S=s.Matrix([[Q(3,4),Q(1,4)],[Q(1,4),Q(3,4)]])
T=s.Matrix([[Q(9,10),Q(1,10)],[Q(1,10),Q(9,10)]])
D=T*S.inv();v=s.Matrix([1,-1]);eps=Q(1,100)
Rs=[v*v.T+eps*s.eye(2),eps*s.eye(2)]
As=[sum((S[a,i]*Rs[i] for i in range(2)),s.zeros(2)) for a in range(2)]
Bs=[sum((T[y,i]*Rs[i] for i in range(2)),s.zeros(2)) for y in range(2)]
G=s.Matrix.hstack(*[As[a]*D[:,a] for a in range(2)])
Z=G*(S.T).inv(); zs=[Z[:,i] for i in range(2)]
zS=Z*S.T;zT=Z*T.T
ES=sum((zS[:,a].T*As[a].inv()*zS[:,a])[0] for a in range(2))
NT=sum((zT[:,y].T*Bs[y].inv()*zT[:,y])[0] for y in range(2))
DUAL=sum((D[:,a].T*As[a]*D[:,a])[0] for a in range(2))-sum(s.trace(Rs[i]*s.diag(*T[:,i])) for i in range(2))
assert DUAL>0 and NT>ES
print('INFEASIBLE pair: unique D=',D,'positive dual gap=',DUAL)
print('Extracted faithful reference baselines=',Rs,'tangent vectors=',zs)
print('Exact vector target-minus-source=',s.factor(NT-ES))
for den in [10,100,1000,10000,100000]:
    delta=Q(1,den)
    gs=sum((4*zS[:,a].T*(As[a]+delta*s.eye(2)/2).inv()*zS[:,a])[0] for a in range(2))
    gt=sum((4*zT[:,y].T*(Bs[y]+delta*s.eye(2)/2).inv()*zT[:,y])[0] for y in range(2))
    if gt>gs:break
else:raise AssertionError('No finite SLD flag witness at tested delta')
amp=Q(1,1000)
while not all(delta/2-amp**2*(zs[i].T*Rs[i].inv()*zs[i])[0]>0 for i in range(2)):amp/=10
normalizer=sum(s.trace(R) for R in Rs)+delta
riskgap=s.factor(amp**2*(gt-gs)/normalizer)
assert riskgap>0
print('Finite coherent flag delta=',delta,'amplitude=',amp,'exact MMSE reversal=',riskgap)
print('All exact checks passed.')
