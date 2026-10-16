import json
from pathlib import Path
import sympy as s
I=s.I; E=s.eye(2); Z=s.diag(1,-1); X=s.Matrix([[0,1],[1,0]])
ZZ=s.kronecker_product(Z,Z); XX=s.kronecker_product(X,X); Z1=s.kronecker_product(Z,E); Id=s.eye(4)
P=(Id+ZZ)*(Id+XX)/4
H=(Id-XX)/2
R=(Id-I*Z1)/s.sqrt(2)
U=Id-2*H  # exp(-i*pi*H)
W=ZZ*R.conjugate().T*U*R
psi=s.Matrix([1,0,0,1])/s.sqrt(2)
def eq(a,b): return s.simplify(a-b)==s.zeros(*a.shape)
assert eq(P*P,P) and eq(H*H,H)
assert eq(H*P,P*H) and eq(H*ZZ,ZZ*H)
assert eq(ZZ*R.conjugate().T*R,ZZ)
assert eq(U*psi,psi)
bad=s.simplify((psi.conjugate().T*W.conjugate().T*(Id-P)*W*psi)[0])
assert bad==1
out={'good_sector':'joint +1 of ZZ and XX, Bell Phi+', 'baseline_odd_norm':'0', 'baseline_projector_norm':'1', 'intermediate_pulse':'exp(-i*pi*Z1/4)', 'dwell_unitary':'exp(-i*pi*H)=XX', 'ideal_compiled_endpoint':'ZZ', 'selected_physical_S_branch_bad_probability':str(bad), 'fair_hidden_I_S_average_bad_probability':str(bad/2), 'ideal_schur_refresh_bad_probability':'0', 'exact_checks':'PASS'}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
# Exact finite-pulse Rabi calculation on invariant Bell subspace.
phi_minus=s.Matrix([1,0,0,-1])/s.sqrt(2)
V=s.Matrix.hstack(psi,phi_minus)
Hc=(s.kronecker_product(Z,E)+s.kronecker_product(E,Z))/2
assert eq(V.conjugate().T*Hc*V,X)
assert eq(V.conjugate().T*(s.sqrt(5)*H)*V,s.diag(0,s.sqrt(5)))
omega=s.sqrt(1+s.Rational(5,4))
finite_bad=s.simplify(s.sin(s.pi*omega)**2/omega**2)
assert finite_bad==s.Rational(4,9)
out['finite_constant_pulse_branch_bad_probability']=str(finite_bad)
out['finite_constant_hidden_average_bad_probability']=str(finite_bad/2)
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print('finite constant pulse:',finite_bad,'; hidden average:',finite_bad/2)
