"""Exact rational CPTP fixture with coherent syndrome feedback and evolving references.
No imports from author programs. Full16x16 superoperators, not state-only tests.
"""
from pathlib import Path
import sympy as s
import json,hashlib
D=Path(__file__).parent
def clean(m):return m.applyfunc(s.expand)
def eq(a,b):return clean(a-b)==s.zeros(a.rows,a.cols)
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);I4=s.eye(4)
kron=s.kronecker_product
reset=[kron(I,s.Matrix([[1,0],[0,0]])),kron(I,s.Matrix([[0,1],[0,0]]))]
def superop(ks):return sum((kron(k.conjugate(),k) for k in ks),s.zeros(16)).applyfunc(s.expand)
def rot(axis,x):return ((1-x*x)*s.eye(axis.rows)-2*s.I*x*axis)/(1+x*x)
def sn(x):return 2*x/(1+x*x)
def cs(x):return (1-x*x)/(1+x*x)
def cos2(x):return 1-2*sn(x)**2
P=superop(reset);Q=s.eye(16)-P
assert P*P==P
S=P;G=s.zeros(16);T=P;reference=P;rho= s.Integer(1);g=s.Integer(0);bound=s.Integer(0);last_a=None;rows=[]
for t in range(1,9):
 a=s.Rational(1,40+t);b=s.Rational(1,51+2*t);w=s.Rational(t,23+t)
 U=rot(kron(Z,X),a);V=rot(kron(Z,X),b);W=kron(rot(Z,w),I)
 A=superop([W*k for k in reset]);E=superop([U*W*k*V for k in reset]);delta=E-A
 assert P*A==A==A*P
 assert sum((k.H*k for k in [U*W*j*V for j in reset]),s.zeros(4)).applyfunc(s.expand)==I4
 # Certified hybrid upper bound, exact unitary channel distance to identity.
 eps=2*(sn(a)+sn(b));assert eps<s.Rational(1,2)
 bt=(1-cos2(a)*cos2(b))/2
 # Exact decoded one-cycle map: evolving unitary reference plus Z dephasing.
 ZL=superop([kron(Z,I)])
 assert eq(P*delta*P,bt*(ZL*A-A))
 oldS,oldG=S,G
 T=clean(E*T);S=clean(P*T);G=clean(Q*T);reference=clean(A*reference)
 assert eq(G,Q*delta*(oldS+oldG))
 assert eq(S,A*oldS+P*delta*P*oldS+P*delta*oldG)
 # Adjacent rotations add coherently before each real syndrome reset.
 if t==1:rho=cos2(b)
 else:
  c=cs(last_a)*cs(b)-sn(last_a)*sn(b);si=sn(last_a)*cs(b)+cs(last_a)*sn(b)
  rho*=c*c-si*si
 exact_error=(1-rho*cos2(a))/2
 assert eq(S,(1-exact_error)*reference+exact_error*ZL*reference)
 # This dephasing-vs-unitary mixture has exact half-diamond=exact_error.
 bound+=bt+eps*g/2;g=2*eps*(1+g)
 assert exact_error<=bound
 rows.append({'T':t,'epsilon_hybrid_bound':str(eps),'b_exact':str(bt),'true_half_diamond':float(exact_error),'recurrence_bound':float(bound),'all_superoperator_identities_exact':True})
 last_a=a
# No-reset negative control: coherent accumulation survives without P between rounds.
x=s.Rational(1,41);U=rot(kron(Z,X),x);E=superop([U]);power=P
for t in range(1,9):
 power=clean(E*power);ut=clean(U**t)
 # Compute sin(t theta) exactly from one offdiagonal unitary entry.
 st=s.I*ut[0,1];err=s.simplify(st**2)
 assert eq(P*power,(1-err)*P+err*superop([kron(Z,I)])*P)
# At theta0 identity differs maximally from reset on |logical0,syndrome1>.
r=s.zeros(4);r[1,1]=1
assert (r-reset[1]*r*reset[1].H).eigenvals()=={s.Integer(1):1,s.Integer(-1):1,s.Integer(0):2}
files=['contractive_syndrome_reuse_20261028.md','flagged_faultfree_all_operator_reset_20261028.md','flagged_five_qubit_storage_round_20261028.md','flagged_five_qubit_storage_check_20261028.py','flagged_five_qubit_storage_check_20261028.json',Path(__file__).name]
out={'status':'PASS_EXACT_TIME_VARYING_CPTP_REFERENCE_AND_COHERENT_FEEDBACK','source_draws':0,'examples':rows,'reference':'Time-varying nonidentity logical Z unitaries with syndrome reset','tested_map_dimension':16,'negative_control':'Without reset, exact error sin^2(T theta); at zero angle full diamond distance from P is2','sha256':{f:hashlib.sha256((D/f).read_bytes()).hexdigest() for f in files}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
