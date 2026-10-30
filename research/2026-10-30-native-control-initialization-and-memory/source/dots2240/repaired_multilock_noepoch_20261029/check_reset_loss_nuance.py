"""Exact negative regression: individual syndrome losses need not commute.
The full complete reset instrument still has exact no-creation.
"""
import sympy as s,json
from pathlib import Path
V=s.Matrix([[1,0],[0,1/s.sqrt(2)],[0,1/s.sqrt(2)],[0,0]])
P=V*V.conjugate().T;B=s.eye(4)-P
p0=s.diag(1,0);p1=s.diag(0,1)
loss0=s.kronecker_product(s.eye(2),p0);loss1=s.kronecker_product(s.eye(2),p1)
assert loss0*B-B*loss0!=s.zeros(4)
assert (loss0+loss1)*B-B*(loss0+loss1)==s.zeros(4)
Bdest=s.eye(4)-s.kronecker_product(s.eye(2),p0)
J=[s.kronecker_product(s.eye(2),s.Matrix([[1,0],[0,0]])),s.kronecker_product(s.eye(2),s.Matrix([[0,1],[0,0]]))]
for j in J:assert Bdest*j*P==s.zeros(4)
out={'individual_loss_commutator_nonzero':True,'summed_loss_commutes':True,
'all_resolved_jumps_map_good_into_good':True,'commutator_frobenius_squared':str(s.trace((loss0*B-B*loss0).conjugate().T*(loss0*B-B*loss0)))}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
