"""Independent small full-animal operator-weight test and singular-K regression.
All nonempty subsets of a three-vertex clique; noncommuting controller gates.
No Tanner geometry or native lifetime is inferred from this toy regression.
"""
import numpy as np,json
from scipy.linalg import expm,eigvalsh
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.])
gens=[I+.3*X,I+.4*Z,I+.2*Y];delta=.017;theta=1e-5;c=.9
circuits={};weights={}
for A in range(1,8):
 y=I.astype(complex)
 for j in range(3):
  if A>>j&1:y=y@expm(delta*gens[j])
 circuits[A]=y;weights[A]=y.conj().T@y
f=lambda A,s:theta**((1-c)*A.bit_count()-(A&s).bit_count())
move_checks=[];weighted_noncomm=max(np.linalg.norm(a@b-b@a) for a in weights.values() for b in weights.values())
# Fixed actual-controller pullback preserves every weight comparison.
J=np.array([[.8,.2j],[.1,.5]],complex)
for s in range(8):
 for D in range(1,8):
  out=s^D
  if out.bit_count()>=s.bit_count():continue
  charge=sum(weights[A]*(f(A,s)-f(A,out)) for A in range(1,8))
  resetcharge=sum(J.conj().T@weights[A]@J*(f(A,s)-f(A,out)) for A in range(1,8))
  scale=max(f(A,s) for A in range(1,8))
  low=float(eigvalsh(charge/scale)[0]);lowJ=float(eigvalsh(resetcharge/scale)[0])
  assert low>=-1e-12 and lowJ>=-1e-12
  move_checks.append({'source':s,'flip':D,'min_scaled_charge':low,'min_scaled_pulled_charge':lowJ})
# A singular coefficient invalidates a naive relative comparison even when G are close.
K=np.diag([1.,0.]);yb=expm(delta*X);bad=yb.conj().T@K@yb-.9*K
bad_det=float(np.linalg.det(bad).real)
assert bad_det<0
# Omit the only overlapping gate: Yhat=I. Exact cavity difference bound.
diff=yb.conj().T@K@yb-K;G=yb.conj().T@yb;gi=np.linalg.inv(yb)
relative=gi.conj().T@diff@gi
result={'animal_count':7,'accepted_moves_checked':len(move_checks),'controller_weight_noncommutator':float(weighted_noncomm),'minimum_normalized_charge':min(q['min_scaled_charge'] for q in move_checks),'minimum_normalized_reset_charge':min(q['min_scaled_pulled_charge'] for q in move_checks),'singular_naive_comparison_determinant':bad_det,'singular_cavity_relative_error_over_delta':float(np.linalg.norm(relative,2)/delta),'scope':'Exact finite operator-charge regression; not an expansion-code or memory simulation'}
assert weighted_noncomm>1e-6
print(json.dumps(result,indent=2))
