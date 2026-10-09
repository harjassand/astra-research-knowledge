"""Exact legal nontracial fast-mode/Petz Gram check, no scan or solver.

This finite check was added AFTER the independent proof freeze and origin
exposure. It supplements the analytic audit, rather than establishing the
universal theorem. SymPy only; no floating-point spectra.
"""
import json
from pathlib import Path
import sympy as s

OUT=Path(__file__).resolve().parent
I=s.eye(2)
X=s.Matrix([[0,1],[1,0]])
Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1)
sigma=s.diag(s.Rational(4,5),s.Rational(1,5))
root=s.diag(2/s.sqrt(5),1/s.sqrt(5))
invroot=s.diag(s.sqrt(5)/2,s.sqrt(5))
simple=lambda M:M.applyfunc(s.simplify)
v=[s.Matrix([2,epsilon])/s.sqrt(5) for epsilon in [1,-1]]
pi=[simple(a*a.conjugate().T) for a in v]
effects=[(I+epsilon*X)/2 for epsilon in [1,-1]]
assert simple(sum([p/2 for p in pi],s.zeros(2)))==sigma
for P,M in zip(pi,effects): assert simple(invroot*P*invroot/2)==M
Phi=lambda A:simple(sum([P*s.trace(M*A) for P,M in zip(pi,effects)],s.zeros(2)))
H=lambda A:simple(sum([M*s.trace(P*A) for P,M in zip(pi,effects)],s.zeros(2)))
assert Phi(sigma)==sigma and H(I)==I and Phi(I)==2*sigma
kms=lambda A,B:s.simplify(s.trace(root*A.conjugate().T*root*B))
gns=lambda A,B:s.simplify(s.trace(sigma*A.conjugate().T*B))
basis=[I,s.sqrt(5)*X/2,s.sqrt(5)*Y/2,s.diag(s.Rational(1,2),-2)]
metric=s.Matrix([[kms(A,B) for B in basis] for A in basis])
hm=s.Matrix([[kms(A,H(B)) for B in basis] for A in basis])
assert metric==s.eye(4) and hm==s.diag(1,s.Rational(4,5),0,0)
assert gns(X,H(Y))==0 and gns(H(X),Y)==12*s.I/25
raw=s.Matrix([[s.simplify(s.trace(sigma*(A*B+B*A)/2)) for B in basis] for A in basis])
assert raw==s.diag(1,s.Rational(5,4),s.Rational(5,4),1)

# One exact CPTP broadcast map: measure X and prepare pi_e tensor pi_e.
input_v=[s.Matrix([1,epsilon])/s.sqrt(2) for epsilon in [1,-1]]
columns=[s.kronecker_product(u,a,a) for u,a in zip(input_v,v)]
JB=simple(sum([c*c.conjugate().T for c in columns],s.zeros(8)))
assert s.Matrix.hstack(*columns).conjugate().T*s.Matrix.hstack(*columns)==I
def partial_second(M,da,db):
 return simple(s.Matrix(da,da,lambda a,b:sum(M[a*db+c,b*db+c] for c in range(db))))
Jphi=simple(sum([s.kronecker_product(M.T,P) for M,P in zip(effects,pi)],s.zeros(4)))
assert partial_second(JB,4,2)==Jphi
assert partial_second(Jphi,2,2)==I
omega=simple(sum([s.kronecker_product(P,P)/2 for P in pi],s.zeros(4)))
gamma=s.Matrix([[s.simplify(s.trace(omega*s.kronecker_product(A,B))) for B in basis] for A in basis])
assert gamma==hm
Badjoint=lambda O:simple(sum([M*s.trace(s.kronecker_product(P,P)*O) for M,P in zip(effects,pi)],s.zeros(2)))

# Depth-one actual joint POVM. The selected E_X has lambda=4/5 >1/sqrt(2),
# and its physical same-leaf variance 5/4 differs from its KMS unit norm.
lam=s.Rational(4,5)
E=basis[1]
outcomes=[]
for epsilon in [1,-1]:
 for delta in [1,-1]:
  M=Badjoint(s.kronecker_product((I+epsilon*X)/2,(I+delta*X)/2))
  p=s.simplify(s.trace(sigma*M))
  rho=simple(root*M*root/p)
  score=(epsilon+delta)*s.sqrt(5)/(4*lam)
  x=s.Matrix([s.simplify(s.trace(rho*A)) for A in basis[1:]])
  outcomes.append((M,p,rho,score,x))
assert simple(sum([p*rho for M,p,rho,score,x in outcomes],s.zeros(2)))==sigma
assert simple(sum([score*M for M,p,rho,score,x in outcomes],s.zeros(2)))==E
N=s.simplify(sum(p*score**2 for M,p,rho,score,x in outcomes))
C=simple(sum([p*x*x.T for M,p,rho,score,x in outcomes],s.zeros(3)))
cross=simple(sum([p*x*score for M,p,rho,score,x in outcomes],s.zeros(3,1)))
assert N==s.Rational(205,128)
assert C==s.diag(s.Rational(128,205),0,0) and cross==s.Matrix([1,0,0])
assert N==(s.Rational(5,4)+s.Rational(4,5))/(2*lam**2)
R=(s.Rational(5,4)+1)/(2*lam**2)
assert R==s.Rational(225,128) and C[0,0]>=1/R
assert C[0,0]*N==1
target=s.diag(1,s.Rational(7,25),0,0)
assert hm-target==s.diag(0,s.Rational(13,25),0,0)

report={'status':'EXACT_PASS','scope':'One exact legal nontracial fast-mode model; supplemental internal normalization check, not proof of universality.',
 'sigma':'diag(4/5,1/5)','H_KMS_matrix':str(hm),'Jordan_raw_metric':str(raw),
 'fast_eigenvalue':'4/5','fast_physical_leaf_variance':'5/4',
 'depth_one_estimator_second_moment':str(N),'depth_one_upper_R':str(R),
 'full_centered_posterior_Gram':str(C),'full_cross_moment':str(cross),
 'GNS_selfadjointness_failure':{'GNS_X_HY':'0','GNS_HX_Y':'12*i/25'},
 'broadcaster_Choi_PSD':'Explicit sum of two rank-one positive outer products, TP and marginal Choi checked exactly.',
 'Schrodinger_unital':'FALSE: Phi(I)=2sigma','stationarity':'Phi(sigma)=sigma',
 'floating_point_calls':0,'random_or_parameter_scans':0}
(OUT/'weighted_fast_mode_replay.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
