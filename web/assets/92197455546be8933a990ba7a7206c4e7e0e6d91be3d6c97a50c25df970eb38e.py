"""Exact diagnostic of derivative-probe contact signs and angular factors."""
import json
from pathlib import Path
import sympy as s
from sympy.physics.wigner import clebsch_gordan
omega=s.symbols('omega', real=True)
mu=s.symbols('mu', nonnegative=True)
K=s.Matrix([[2,1],[1,3]])
C=s.Matrix([[5,1],[1,4]])
E=s.Matrix([[1,2],[-1,1]])
F=s.Matrix([[2,1],[1,-1]])
chi=-mu*s.eye(2)+(E-s.I*omega*F)*(C-omega**2*K).inv()*(E.T+s.I*omega*F.T)
contact=chi.applyfunc(lambda z:s.limit(z,omega,s.oo))
expected=-mu*s.eye(2)-F*K.inv()*F.T
contact_residual=s.simplify(contact-expected)
# A general invertible kinetic form verifies the retarded slope identity:
# K Gdot(0+)=I. With F=0, d(E G E^T)/dt at 0+=E K^-1 E^T.
slope=E*K.inv()*E.T
cg={str(j):{str(m):str(clebsch_gordan(j,1,2,m,0,m)) for m in range(min(j,2)+1)} for j in (1,2,3)}
scalar_tensor_j3_ratio=s.simplify(clebsch_gordan(3,1,2,0,0,0)**2/clebsch_gordan(3,1,2,2,0,2)**2)
result={
  'scope':'Finite frozen quadratic block and elementary representation diagnostic; no covariant action synthesis is claimed.',
  'K_principal_minors':[str(K[0,0]),str(K.det())],
  'C_principal_minors':[str(C[0,0]),str(C.det())],
  'contact_residual':str(contact_residual),
  'contact_without_minus_mu':str(-F*K.inv()*F.T),
  'F0_regular_slope':str(slope),
  'slope_principal_minors':[str(slope[0,0]),str(slope.det())],
  'clebsch_gordan_j_1_to_2':cg,
  'spin3_scalar_tensor_squared_factor_ratio':str(scalar_tensor_j3_ratio),
  'all_claimed_checks_pass':contact_residual==s.zeros(2) and scalar_tensor_j3_ratio==s.Rational(9,5)
}
print(json.dumps(result,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
assert result['all_claimed_checks_pass']
