"""Exact branch/fault audit of the adopted M_ZZZ teleporting cat CNOT.

The primitive is ideal only for this algebraic compilation check. The separate
buffer/receiver scripts audit sensing errors and finite-time hardware effects.
"""
from pathlib import Path
import json
import itertools
import numpy as np

I=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1])
Y=np.array([[0,-1j],[1j,0]])
P={"I":I,"X":X,"Y":Y,"Z":Z}
kron=np.kron
plus=np.array([1,1])/np.sqrt(2)
minus=np.array([1,-1])/np.sqrt(2)
Ucx=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])


def identify(k):
    err=k@Ucx.conj().T
    return [a+b for a,b in itertools.product(P,repeat=2)
            if abs(np.trace(kron(P[a],P[b]).conj().T@err)/4)>1e-10]


def gate(s,m, fault=None, position=None, reported=None):
    # Order c,t,a; output c,a, old target t is measured in X.
    prep=kron(np.eye(4),plus[:,None])
    proj=(np.eye(8)+s*kron(kron(Z,Z),Z))/2
    bra=plus if m==1 else minus
    measure=kron(kron(I,bra[None,:]),I)
    if position=="before_parity": prep=fault@prep
    if position=="after_parity": proj=fault@proj
    k=measure@proj@prep
    sr,mr=(s,m) if reported is None else reported
    correction=kron(Z if mr==-1 else I,Z if mr==-1 else I)@\
               kron(I,X if sr==-1 else I)
    return correction@k


def main():
    records=list(itertools.product((1,-1),repeat=2))
    residual=max(np.linalg.norm(gate(s,m)@Ucx.T-
                  np.trace(gate(s,m)@Ucx.T)/4*np.eye(4)) for s,m in records)
    faults={}
    for pos in ("before_parity","after_parity"):
        for subset in ((0,),(1,),(2,),(0,1),(0,2),(1,2),(0,1,2)):
            ops=[Z if j in subset else I for j in range(3)]
            f=kron(kron(ops[0],ops[1]),ops[2])
            faults[pos+"_"+"".join("cta"[j] for j in subset)]=sorted(set(
                lab for s,m in records for lab in identify(gate(s,m,f,pos))))
    readout={}
    for j in (0,1):
        readout["bad_ZZZ_record" if j==0 else "bad_X_record"]=sorted(set(
            lab for s,m in records for lab in identify(gate(s,m,reported=
                    (-s,m) if j==0 else (s,-m)))))
    output={"maximum_branch_scalar_CNOT_residual":float(residual),
            "phase_fault_output_Paulis":faults,"readout_record_faults":readout,
            "note":"Any lower-weight Z-type error within one physical M_ZZZ gadget remains at most one phase error in each output block when gadgets are transversal."}
    Path(__file__).with_name("three_cat_gate_results.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))


if __name__=="__main__":main()
