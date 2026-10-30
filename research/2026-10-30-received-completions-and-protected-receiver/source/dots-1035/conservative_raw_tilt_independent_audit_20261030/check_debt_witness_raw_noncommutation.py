"""Actual malformed Alice terminal produces a non-raw-diagonal debt effect.
Read S=XX using H, controlled-X0, controlled-X1, H. Missing ownership on0
and ownership on1 (also the onsite-gate partner) gives terminal forest
segment V=H_anc controlled-X1. All other nominal terms have zero Q drift
in this parent-bad source block, so this is an actual derivative block.
"""
import numpy as np,json
from pathlib import Path
I2=np.eye(2);I4=np.eye(4);I8=np.eye(8);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);H=np.array([[1,1],[1,-1]])/np.sqrt(2)
S=np.kron(X,X);T=np.kron(Z,Z)
CX1=np.block([[I4,np.zeros((4,4))],[np.zeros((4,4)),np.kron(X,I2)]])
V=np.kron(H,I4)@CX1
pointer_false=(I8-np.kron(Z,S))/2
pull=V.conj().T@pointer_false@V
expected=(I8-np.kron(X,np.kron(I2,X)))/2
rawU=np.kron(I2,(I4-T)/2)
Dheal=I8-pull
comm=float(np.linalg.norm(Dheal@rawU-rawU@Dheal))
assert np.max(np.abs(pull-expected))<1e-12 and comm>1
out={'read_stabilizer':'XX','other_raw_stabilizer':'ZZ','ownership_mask':[False,True],'onsite_gate_partner':1,'terminal_forest_segment':'H_anc controlled-X1','false_effect_formula_error':float(np.max(np.abs(pull-expected))),'healing_effect_min_eigenvalue':float(np.linalg.eigvalsh(Dheal).min()),'healing_effect_max_eigenvalue':float(np.linalg.eigvalsh(Dheal).max()),'raw_energy_commutator_norm':comm,'own_bad_corner_is_entire_source':True,'all_checks_pass':True,'rejected_shortcut':'the actual semantic-debt polynomial/resolvent automatically commutes raw DATA energy','surviving_result':'own-corner positive local witness and separated-support moments do not require that commutation'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
