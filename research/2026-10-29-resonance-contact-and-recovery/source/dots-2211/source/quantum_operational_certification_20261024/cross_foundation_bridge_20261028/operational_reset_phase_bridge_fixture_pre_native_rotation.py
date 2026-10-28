"""Exact physical phase-calibration plus observable reset fixture; no source sampling."""
import sympy as s,json
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);S=s.diag(1,s.I)
psi=s.Matrix([s.sqrt(3)/2,s.Rational(1,2)]);sig=psi*psi.H
states=[U*sig*U.H for U in [I,X,Z,S]]
effects=[I,(I+X)/2,(I+Y)/2,(I+Z)/2]
H=s.Matrix([[s.simplify(s.trace(F*r)) for r in states] for F in effects]);assert H.det()!=0
lam=s.Rational(1,3)
reset=lambda a:(1-lam)*a+lam*s.trace(a)*sig
HR=s.Matrix([[s.simplify(s.trace(F*reset(r))) for r in states] for F in effects]);C=s.simplify(H.inv()*HR)
m=s.ones(1,4);W=s.Matrix.vstack(-s.ones(1,3),s.eye(3));E=s.Matrix.hstack(s.zeros(3,1),s.eye(3));D=s.simplify(E*C*W)
assert D==(1-lam)*s.eye(3) and m*C==m
# USE is controlled Z from memory pointer to payload. Its pointer trace is p=1/4 dephasing.
CZ=s.diag(1,1,1,-1);p=s.Rational(1,4)
for a in [I,X,Y,Z]:
 out=CZ*s.kronecker_product(sig,a)*CZ.H
 reduced=s.Matrix(2,2,lambda j,k:s.simplify(out[j,k]+out[j+2,k+2]))
 assert reduced==(1-p)*a+p*Z*a*Z
# After |+> payload, pointer/payload joint state has nonzero coherent error cross blocks.
plus=s.Matrix([1,1])/s.sqrt(2);joint=CZ*s.kronecker_product(psi,plus)
assert joint[0]*s.conjugate(joint[3])!=0
r={'status':'PASS_EXACT_PHYSICAL_BRIDGE_FIXTURE','source_draws':0,'core_determinant':str(s.simplify(H.det())),'reset_transfer':str(C),'trace_zero_reset':str(D),'calibration_dephasing_p':str(p),'calibration_contrast_a':str(1-2*p),'actual_reset_rate_lambda':str(lam),'scope':'Native pointer rotations plus controlled-Z USE make full qubit observable; hidden counter shifts forever. RESET contracts observable pointer, not complete environment. Core acquisition still requires valid initial bank.','limits':'Exact algebra only; no completed acquisition, sampled estimator, physical implementation or general bootstrap.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
