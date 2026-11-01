"""Exact code/reference/flag coherent-span checks; no storage simulation.

Ordinary DATA syndrome recovery is fixed, with no target gate in it.
The flag register and a retained two-level bath remain quantum outputs.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np
from steane_model import encoder_and_syndrome_unitary,ALL,parity
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/latched_gate_20261101'

def cnot_column(v,i):
    j=np.arange(16384,dtype=np.int64)
    # Tensor order is A, B, reference. A's bit i controls B's bit i.
    perm=j ^ (((j>>(7+i))&1)<<i)
    return v[perm]
def ordinary_recover_pure(v,dec):
    # Coherent syndrome extraction is a Stinespring representation of the
    # same ordinary measured-syndrome recovery; the syndrome is traced later.
    a=v.reshape(128,128,4)
    a=np.einsum('sa,abr,tb->str',dec,a,dec,optimize=True)
    # (syndrome_A,logical_A,syndrome_B,logical_B,reference)
    return a.reshape(64,2,64,2,4).transpose(1,3,4,0,2).reshape(16,4096)
def logical_choi(target=False):
    v=np.zeros((2,2,4),complex)
    for a in range(2):
        for b in range(2):v[a,b^a if target else b,2*a+b]=.5
    return v.reshape(16)
def trace_norm(a):return float(np.abs(np.linalg.eigvalsh((a+a.conj().T)/2)).sum())

def main():
    enc,dec=encoder_and_syndrome_unitary()
    v=np.zeros((128,128,4),complex)
    for a in range(2):
        for b in range(2):v[:,:,2*a+b]=np.outer(enc[:,a],enc[:,b])*.5
    initial=v.reshape(16384,4);target=initial.copy()
    for i in range(7):target=cnot_column(target,i)
    ideal=logical_choi(True);identity=logical_choi(False)
    recovered=ordinary_recover_pure(target,dec)
    trans_error=float(np.linalg.norm(recovered-ideal[:,None]*np.conj(ideal)@recovered))
    assert trans_error<1e-12
    zero=ordinary_recover_pure(initial,dec);rho0=zero@zero.conj().T
    assert trace_norm(rho0-np.outer(identity,identity.conj()))<1e-12
    # Superpose eight different missing masks, correlated with a retained B.
    # Each nonempty branch has additional coherent Y error on THAT column.
    rng=np.random.default_rng(20261101)
    coeff=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2));coeff/=np.linalg.norm(coeff)
    decoded=np.zeros((16,8,2,4096),complex)
    for h in range(8):
        vv=target.copy()
        if h:
            i=h-1;j=np.arange(16384,dtype=np.int64)
            # (I+i Y_A)/sqrt(2), on the same column as the missing CNOT.
            yy=np.empty_like(vv)
            yy[j^(1<<(7+i))]=1j*(1-2*((j>>(7+i))&1))[:,None]*vv
            vv=(vv+1j*yy)/np.sqrt(2)
            vv=cnot_column(vv,i)
        d=ordinary_recover_pure(vv,dec)
        decoded[:,h,:,:]=coeff[h,:,None][None,:,:]*d[:,None,:]
    flat=decoded.reshape(32*8,4096);joint=flat@flat.conj().T
    assert abs(np.trace(joint)-1)<1e-12
    assert np.linalg.eigvalsh((joint+joint.conj().T)/2)[0]>-1e-12
    arr=joint.reshape(16,16,16,16)
    aux=np.einsum('iaib->ab',arr)
    want=np.kron(np.outer(ideal,ideal.conj()),aux)
    coherent_error=trace_norm(joint-want)
    assert coherent_error<2e-12
    bad=target.copy()
    for i in (0,1):bad=cnot_column(bad,i)
    bad=ordinary_recover_pure(bad,dec);bad_rho=bad@bad.conj().T
    bad_distance=trace_norm(bad_rho-np.outer(ideal,ideal.conj()))
    assert bad_distance>.01
    # Independent tableau sanity checks on all single-site Pauli errors.
    from steane_model import choi_stabilizer,recover,target_fidelity
    worst=0
    for i in range(14):
        for x,z,p in ((1,0,0),(0,1,0),(1,1,1)):
            s=choi_stabilizer()
            for j in range(7):s.cnot(j,j+7)
            s.pauli((x<<i,z<<i,p));recover(s,0,rng);recover(s,1,rng)
            worst=max(worst,abs(1-target_fidelity(s)))
    assert worst==0
    result={'scope':'exact finite-code coherent algebra, not controller dynamics or a threshold',
            'transversal_CNOT_code_reference_residual':trans_error,
            'coherent_missing_flags_and_bath_joint_distance':coherent_error,
            'coherent_auxiliary_purity':float(np.trace(aux@aux).real),
            'time_zero_identity_to_CNOT_choi_distance':trace_norm(rho0-np.outer(ideal,ideal.conj())),
            'two_unfinished_columns_CNOT_choi_distance':bad_distance,
            'all_42_single_Pauli_tableau_fidelity_error':worst,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'model_sha256':hashlib.sha256(Path(__file__).with_name('steane_model.py').read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'coherent_decoder_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
