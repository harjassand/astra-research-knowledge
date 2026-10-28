"""Exact proof-interface checks; no source counts or sampling."""
import sympy as s, json, hashlib, itertools
from pathlib import Path
p=Path(__file__).parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);F=[I,X,Y,Z]
def choi(A):return sum((A[i,j]*s.kronecker_product(F[j].T,F[i])/2 for i in range(4) for j in range(4)),s.zeros(4))
def psd(A):
    return all(s.simplify(A.extract(ix,ix).det())>=0 for k in range(1,A.rows+1) for ix in itertools.combinations(range(A.rows),k))
a=s.Rational(1,4);b=c=s.Rational(1,8)
W=s.diag(1,a,a,a);W[1,3]=b;W[3,2]=c
B=s.eye(4)[:,[0,1,3]];K=B.T
P0=s.Matrix([[1,0,0,0],[0,0,0,1]])
Q=s.Matrix([[s.Rational(1,2)]*2,[s.Rational(1,4),s.Rational(1,16)]])
P=Q.inv()*P0*B;Pbar=Q.inv()*P0
rho=s.Matrix([s.Rational(1,2),0,0,s.Rational(1,4)])
L=K*s.Matrix.hstack(rho,W*rho);Lfull=B*L
m=s.ones(1,2);tau=s.Matrix([[2,0,0,0]])
T=K*W*B;C=P*T*L
assert P*L==s.eye(2) and Pbar*B==P and m*Pbar==tau
assert W*B==B*T and P*T==C*P and Pbar*rho==s.Matrix([1,0])
assert psd(choi(W)-s.eye(4)/4)
# Reachable span is exactly three; quotient core is rank two.
reachable=s.Matrix.hstack(rho,W*rho,W**2*rho)
assert reachable.rank()==3 and B*K*reachable==reachable
H=s.Matrix([[1,1],[s.Rational(5,8),s.Rational(17,32)]])
assert H.det()==-s.Rational(3,32)
# Native Z-test/reset branches are CP, TP when summed, and quotient-compatible.
test_maps=[]
for sign in (-1,1):
    branch=rho*s.Matrix([[1,0,0,sign*s.Rational(1,2)]])
    assert psd(choi(branch)-s.eye(4)/16)
    internal=K*branch*B
    assert branch*B==B*internal
    cq=P*internal*L;assert P*internal==cq*P
    test_maps.append(branch)
assert tau*sum(test_maps,s.zeros(4))==tau
# No invariant right inverse on reachable space: Z's Jordan defect is b X.
u=s.symbols('u');zlift=s.Matrix([0,u,0,1])
assert W*zlift-a*zlift==s.Matrix([0,b,0,0])
# No full-algebra quotient extension that agrees on W: unavoidable c Z from Y.
k=s.symbols('k');Pbarext=Q.inv()*s.Matrix([[1,0,0,0],[0,0,k,1]])
assert (Pbarext*W-C*Pbarext)[:,2]==Q.inv()*s.Matrix([0,c])
assert (Pbarext*W-C*Pbarext)[:,[0,1,3]]==s.zeros(2,3)
# A trace-zero observable perturbation lifts with all exact structural identities.
e=s.Rational(1,100000);delta=s.Matrix([[e,-2*e],[-e,2*e]])
Wtrue=W+Lfull*delta*Pbar
Ttrue=T+L*delta*P
assert Wtrue*B==B*Ttrue and P*Ttrue==(C+delta)*P and tau*Wtrue==tau
E=delta.applyfunc(abs);radius=Lfull.applyfunc(abs)*E*Pbar.applyfunc(abs)
assert all(abs(z)<=zrad for z,zrad in zip(Wtrue-W,radius))
kappa_sq=sum(x*x for x in radius)
assert kappa_sq<s.Rational(1,4)**2
Jdiff=choi(Wtrue-W)
assert s.trace(Jdiff*Jdiff)<=kappa_sq
assert all(s.simplify(choi(Wtrue)[:j,:j].det())>0 for j in range(1,5))
# Boundary terminal lift: fitted POVM is valid; exact virtual lift need not be.
alpha=s.Rational(4,5);Et=(I+Z/alpha)/2;Efit=(I+Z)/2
assert min(Et.eigenvals())==-s.Rational(1,8) and psd(Efit)
for z in [-alpha,s.Integer(0),alpha]:
    sig=(I+z*Z)/2
    prob=s.trace(Et*sig);assert 0<=prob<=1
    assert abs(s.trace((Et-Efit)*sig))<=s.Rational(1,8)
out={'kind':'exact reachable-quotient algebra; zero source samples',
     'reachable_dimension':3,'observable_rank':2,'full_dimension':4,
     'native_choi_lower':'1/4','observable_core_determinant':str(H.det()),
     'no_invariant_section_for_same_map':True,'no_full_quotient_extension_for_same_map':True,
     'lifted_error_radius_squared':str(kappa_sq),'lifted_error_radius_float':float(s.sqrt(kappa_sq)),
     'trace_and_reachable_intertwining_pass':True,'exact_perturbed_choi_pd':True,
     'terminal_exact_lift_min_eigenvalue':'-1/8','terminal_error_operator_bound':'1/8',
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
source=p/'COUNT_CERTIFIED_REACHABLE_QUOTIENT_CP_REALIZATION.md'
if source.exists():out['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
(p/'reachable_quotient_cp_exact_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
