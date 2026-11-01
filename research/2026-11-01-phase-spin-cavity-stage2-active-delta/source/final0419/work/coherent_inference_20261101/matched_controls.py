"""Matched ordinary bounds and a genuine quantum-transfer rescue test.

The new sharp constant is not credited with the qualitative non-Markovian
capability already supplied by ordinary fault paths and standard encoding.
"""
import json,math,hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'
def opnorm(x):return float(np.linalg.norm(x,2))
def levels(gain):
    T=math.pi/2;p=1e-5;down=.002;phi=.001;up=down*p/(1-p);dark=1e-6;eta=.95
    w=1-(1-p)**2*(1-dark)**2*math.exp(-4*up*T)
    e=1-(1-p)**2*(1-dark)**2*math.exp(-4*(down+2*phi+up)*T)*eta*gain
    rows=[]
    for l in range(6):
        rows.append({'level':l,'data_qubits':7**l,'erasure_upper':e,'wrong_label_upper':w})
        bad=42*e*w+21*w*w;e,w=7*e**3+bad,bad
    return rows
def main():
    A=math.pi*.1/2;sharp=math.cos(A)**2;ordinary=1-A*A
    exact=levels(sharp);generic=levels(ordinary)
    threshold=lambda rows:next(r['level'] for r in rows if r['erasure_upper']+r['wrong_label_upper']<1e-8)
    assert threshold(exact)==threshold(generic)
    # A rail-blind location flag restores a whole quantum qubit IF both
    # rails have identical source operators. A hard-coded Feynman edge can
    # similarly carry any supplied Hermitian unitary, including CNOT.
    X=np.array([[0,1],[1,0]],complex);Z=np.diag([1.,-1.]);He=.7*X+1.3*Z
    G=np.eye(2)+.1*Z;T=math.pi/2
    CNOT=np.eye(4,dtype=complex);CNOT[2:,2:]=X
    H=np.kron(np.eye(2),np.kron(He,np.eye(4)))+np.kron(X,np.kron(G,CNOT))
    U=expm(-1j*T*H)
    vp=expm(-1j*T*(He+G));vm=expm(-1j*T*(He-G));B=(vp-vm)/2;Aop=(vp+vm)/2
    residual=opnorm(U[8:,:8]-np.kron(B,CNOT));failure=opnorm(U[:8,:8]-np.kron(Aop,np.eye(4)))
    assert max(residual,failure)<2e-12
    # Nonmatching source dependence breaks exact logical identity, despite
    # preserving a large and qualified probability of a receiver photon.
    delta=.8;gains=(np.eye(2)+delta*Z,np.eye(2)+delta*X);Bs=[]
    for gain in gains:
        vp=expm(-1j*T*(He+gain));vm=expm(-1j*T*(He-gain));Bs.append((vp-vm)/2)
    # Maximally entangled logical qubit/reference, source |0>. A rail-blind
    # success projects to v0|00>+v1|11>; trace out source and normalize.
    v0=Bs[0][:,0];v1=Bs[1][:,0];success=(np.vdot(v0,v0).real+np.vdot(v1,v1).real)/2
    fidelity=float(np.vdot(v0+v1,v0+v1).real/(4*success))
    assert fidelity<1-1e-6
    # I_logical tensor B_source can steer a pre-existing logical/source
    # correlation. A source-independent logical input is needed for an
    # exact conditional single-success channel on the logical marginal.
    Bsteer=np.diag(np.sin(np.array([.2,1.])*T)).astype(complex)
    rho=np.diag([.5,0,0,.5]).astype(complex)
    filtered=np.kron(np.eye(2),Bsteer)@rho@np.kron(np.eye(2),Bsteer.conj().T)
    filtered/=np.trace(filtered)
    pzero=float(np.trace(filtered[:2,:2]).real)
    assert abs(pzero-.5)>.3
    result={'status':'PASS matched ordinary comparator and quantum-transfer controls',
       'ordinary_source':'Aliferis-Gottesman-Preskill quant-ph/0504218v3 section 11.1 equations 58-59; selected fault-set amplitude <= product integrated local norms',
       'ordinary_readout_derivation':'in virtual-photon representation a miss requires a perturbation at every selected virtual location; project the standard fault-set amplitude bound and square; miss-set probability <= A^(2k)',
       'gain_uncertainty':.1,'sharp_missing_probability':1-sharp,'ordinary_fault_path_missing_probability':1-ordinary,
       'sharp_recursion':exact,'ordinary_recursion':generic,
       'minimum_concatenation_level_for_total_error_below_1e_8':{'sharp':threshold(exact),'ordinary':threshold(generic)},
       'selection':'sharp constant improves numbers but does not create the qualitative encoded-read capability in this model, or reduce the selected encoding level',
       'heralded_quantum_edge':{'full_CNOT_source_operator_factorization_residual':residual,
           'failure_identity_source_operator_factorization_residual':failure,
           'worst_source_single_attempt_success_lower':1-opnorm(Aop)**2,
           'nonmatching_rail_control_conditional_Bell_fidelity':fidelity,
           'precorrelated_source_success_steers_logical_zero_probability':pzero,
           'conditional_scope':'exact single-success logical channel only for source-independent data/reference; arbitrary correlations allow steering. Coarse success after L attempts has source-effect deficit <= sin(A)^(2L), so its reference error vanishes without conditioning on the fine attempt record',
           'limits':'needs a real rail-blind location measurement; the Hamiltonian already contains the supplied CNOT, with a four-body source-dependent term; no synthesis or locality advantage',
           'prior':'Burgarth-Bose quant-ph/0406112 / PRA71 052315 already supplies conclusive dual-rail transfer as a mechanism; Astra N1520 supplies a distinct accepted sector-readout interface'},
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'matched_controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
