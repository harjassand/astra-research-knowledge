"""Narrow 3-qubit source-mapping diagnostic; not a theorem certificate."""
import json
import numpy as np
from pathlib import Path

I2=np.eye(2)
I8=np.eye(8)
z=np.array([1.,0.]);o=np.array([0.,1.])
phi=np.array([1.,0.,0.,1.])/np.sqrt(2)
Pphi=np.outer(phi,phi)
Omega=np.kron(z,phi)
wrong=np.kron(phi,o)
Pout=np.kron(np.eye(4),np.outer(z,z))
Pinit=np.kron(np.outer(z,z),np.eye(4))
Pgate=np.kron(I2,Pphi)

def orth_projector(columns):
    U,s,_=np.linalg.svd(columns,full_matrices=False)
    return U@U.T

def ker_from_positive_precheck(Q,P):
    # columns of Q applied to an orthonormal basis of ker(I-P)
    eig,U=np.linalg.eigh(P)
    return orth_projector(Q@U[:,eig>.5])

rows=[]
for d in [.3,.1,.03,.01,.001,.0001]:
    Q=np.kron(Pphi+d*(np.eye(4)-Pphi),I2)
    psi=Q@Omega;psi/=np.linalg.norm(psi)
    hi=I8-ker_from_positive_precheck(Q,Pinit)
    hg=I8-ker_from_positive_precheck(Q,Pgate)
    hc=I8-np.outer(psi,psi)
    p=2*d*d/(1+3*d*d)
    split_witness=float(wrong@(hi+hg+Pout)@wrong)
    split_formula=d*d/(1+d*d)+3*d*d/(1+3*d*d)
    grouped=float(np.linalg.eigvalsh(hc+Pout)[0])
    grouped_formula=1-np.sqrt(p)
    # Literal two-vertex allocation: Qedge12, init1 at u, no Qvertex.
    # Eq116 becomes hu=I-Pinit; it does not annihilate claimed ground psi.
    hu=I8-Pinit
    literal_parent=float(np.linalg.eigvalsh(hu+hc)[0])
    hu_claimed_ground=float(psi@hu@psi)
    rows.append(dict(delta=d,split_witness=split_witness,
        split_formula=split_formula,grouped_min=grouped,
        grouped_formula=grouped_formula,literal_two_vertex_parent_min=literal_parent,
        init_energy_claimed_ground=hu_claimed_ground))
    assert abs(split_witness-split_formula)<1e-9
    assert abs(grouped-grouped_formula)<1e-9
    assert hu_claimed_ground>0
out=Path(__file__).with_name('grouping_checks.json')
out.write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
