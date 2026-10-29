import sympy as s,json
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
def kron(*args):return s.kronecker_product(*args)
bells=[s.Matrix([1,0,0,1])/s.sqrt(2),s.Matrix([0,1,1,0])/s.sqrt(2),s.Matrix([1,0,0,-1])/s.sqrt(2),s.Matrix([0,1,-1,0])/s.sqrt(2)]
E=s.Matrix.hstack(kron(bells[3],bells[3]),(kron(bells[0],bells[0])-kron(bells[2],bells[2])-kron(bells[1],bells[1]))/s.sqrt(3))
assert E.H*E==s.eye(2)
def unit(u):
 den=1+sum(a*a for a in u);q=[s.Rational(1-sum(a*a for a in u),den)]+[s.Rational(2*a,den) for a in u]
 return q[0]*I-s.I*(q[1]*X+q[2]*Y+q[3]*Z)
Vs=[unit(u) for u in [(1,2,0),(0,-1,2),(2,0,1),(1,1,1)]];W=kron(*Vs);Wrel=kron(I,*[v*Vs[0].H for v in Vs[1:]])
assert s.simplify(kron(*([Vs[0]]*4))*E-E)==s.zeros(16,2)
assert s.simplify(W*E-Wrel*E)==s.zeros(16,2)
# Canonical leakage reset to logical0.
tau=E.H*(s.eye(16)/16)*E+s.trace((s.eye(16)-E*E.H)/16)*s.diag(1,0)
assert tau==s.diag(s.Rational(15,16),s.Rational(1,16))
assert sum((p*tau*p.H for p in [I,X,Y,Z]),s.zeros(2))/4==I/2
out={'exact_generic_rational_SU2_gauge_check':True,'four_spin_singlet_isometry':True,'canonical_reset_depolarizing_output':'diag(15/16,1/16)','logical_Pauli_average':'I2/2','scope':'Exact ideal-interface consistency; no physical control errors'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
