"""Independent exact audit, including the fixed/open-loop discard-core obstruction.
No producer code is imported and no source samples are generated.
"""
import itertools, json, hashlib
from pathlib import Path
import sympy as s
root=Path(__file__).parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
F=[I,X,Y,Z]
def psd(A):
    return all(s.simplify(A.extract(ix,ix).det())>=0 for n in range(1,A.rows+1) for ix in itertools.combinations(range(A.rows),n))
def direct_choi(action):
    ans=s.zeros(4)
    for i in range(2):
        for j in range(2):
            E=s.zeros(2);E[i,j]=1;ans+=s.kronecker_product(E,action(E))
    return ans
# Independently reconstruct the Jordan channel directly on 2x2 matrices.
a=s.Rational(1,4);b=c=s.Rational(1,8)
def jordan(A):
    x0=s.trace(A)/2;xx=(A[0,1]+A[1,0])/2;xy=(A[1,0]-A[0,1])/(2*s.I);xz=(A[0,0]-A[1,1])/2
    return x0*I+(a*xx+b*xz)*X+a*xy*Y+(a*xz+c*xy)*Z
J=direct_choi(jordan);assert psd(J-s.eye(4)/4)
W=s.Matrix([[s.simplify(s.trace(f*jordan(g))/2) for g in F] for f in F])
P0=s.Matrix([[1,0,0,0],[0,0,0,1]]);B0=s.eye(4)[:,[0,1,3]];C0=s.diag(1,a)
ells=s.symbols('ell0:8');Ltest=s.Matrix(4,2,ells)
eqs=list(P0*Ltest-s.eye(2))+list(W*Ltest-Ltest*C0)
assert s.linsolve(eqs,ells)==s.EmptySet
ps=s.symbols('p0:8');Ptest=s.Matrix(2,4,ps)
eqs=list(Ptest*B0-P0*B0)+list(Ptest*W-C0*Ptest)
assert s.linsolve(eqs,ps)==s.EmptySet
# A different rational witness stresses the trace-compatible extension formula.
R=s.Matrix([[s.Rational(1,2),s.Rational(1,2),0,0],[0,0,1,0],[0,0,0,1],[s.Rational(1,8),-s.Rational(1,8),0,0]])
B=R[:,:3];P=s.Matrix([[1,0,0],[0,1,0]]);L=P.T;m=s.ones(1,2);tau=s.Matrix([[2,0,0,0]])
KB=R.inv()[:3,:]+s.Matrix([2,-1,3])*R.inv()[3,:]
assert KB*B==s.eye(3)
u=s.Matrix([1,0]);Pbar=P*KB+u*(tau-m*P*KB)
assert Pbar*B==P and m*Pbar==tau and P*L==s.eye(2)
C=s.Matrix([[s.Rational(3,4),s.Rational(1,4)],[s.Rational(1,4),s.Rational(3,4)]])
Q=s.Matrix([[s.Rational(3,4),s.Rational(1,4),0,s.Rational(1,100)],
            [s.Rational(1,4),s.Rational(3,4),0,-s.Rational(1,100)],
            [s.Rational(1,100),-s.Rational(1,100),s.Rational(1,10),s.Rational(1,100)],
            [0,0,0,s.Rational(1,10)]])
Wfit=R*Q*R.inv();Tfit=Q[:3,:3]
assert Wfit*B==B*Tfit and P*Tfit==C*P and tau*Wfit==tau
Eij=lambda A: sum((A[i,j]*s.kronecker_product(F[j].T,F[i])/2 for i in range(4) for j in range(4)),s.zeros(4))
assert psd(Eij(Wfit)-s.eye(4)/100)
delta=s.Rational(1,10**5)*s.Matrix([[1,-2],[-1,2]])
G=B*L;Wtrue=Wfit+G*delta*Pbar;Ttrue=Tfit+L*delta*P
assert Wtrue*B==B*Ttrue and P*Ttrue==(C+delta)*P and tau*Wtrue==tau
radius=G.applyfunc(abs)*delta.applyfunc(abs)*Pbar.applyfunc(abs)
radius2=sum(z*z for z in radius)
assert radius2<s.Rational(1,100)**2 and psd(Eij(Wtrue))
# Strict-interior process whose FIXED/OPEN-LOOP discard preparation span is one.
e=s.Rational(1,16)
def branch(A,sign):return s.trace(A)*I/4+sign*e*(s.trace(A)*Z+s.trace(Z*A)*I)
Jplus=direct_choi(lambda A:branch(A,1));Jminus=direct_choi(lambda A:branch(A,-1))
assert psd(Jplus-s.eye(4)/8) and psd(Jminus-s.eye(4)/8)
for f in F:assert branch(f,1)+branch(f,-1)==s.trace(f)*I/2
rho=I/2;hplus=branch(rho,1);pplus=s.trace(hplus);pplusplus=s.trace(branch(hplus,1))
H=s.Matrix([[1,pplus],[pplus,pplusplus]])
assert pplus==s.Rational(1,2) and H.det()==4*e*e>0
assert pplusplus==s.Rational(1,4)+4*e*e
# Adaptive stopping is outside that obstruction and DOES generate a biased state.
adaptive_final=branch(rho,1)+s.trace(branch(rho,-1))*I/2
assert adaptive_final==I/2+e*Z
out={'status':'PASS','kind':'independent exact algebra; zero source observations',
     'jordan_full_choi_lower':'1/4','independent_normal_form_choi_lower':'1/100',
     'independent_lift_radius_squared':str(radius2),
     'linear_solve_no_invariant_section':True,'linear_solve_no_full_quotient_extension':True,
     'discard_core_counterexample':{'branch_choi_lower':'1/8','fixed_open_loop_discard_preparation_rank':1,
          'observable_word_rank':2,'word_hankel_minor':str(H.det()),'epsilon':str(e),
          'adaptive_stopping_generates_second_preparation':True},
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'source_sha256':hashlib.sha256((root/'COUNT_CERTIFIED_REACHABLE_QUOTIENT_CP_REALIZATION.md').read_bytes()).hexdigest()}
(root/'reachable_quotient_independent_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
