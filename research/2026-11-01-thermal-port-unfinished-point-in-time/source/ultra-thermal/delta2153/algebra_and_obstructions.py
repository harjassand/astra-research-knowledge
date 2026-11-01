"""Thermal-port algebra and explicit failed transfers; small exact models.

No asymptotic memory theorem or photonic-device counterexample is inferred
from these finite controls. The mathematical proofs are in the output text.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from port_model import I,X,Y,Z,ten,comm,norm,perfect_code,ports,charge_hamiltonians

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/thermal_ports_20261101'
down=np.array([[0,1],[0,0]],complex);num=down.conj().T@down
def diss(j,r):
    a=j.conj().T@j
    return j@r@j.conj().T-(a@r+r@a)/2
def liouv(h,jumps):
    d=len(h);eye=np.eye(d);L=-1j*(np.kron(eye,h)-np.kron(h.T,eye))
    for j in jumps:
        a=j.conj().T@j;L+=np.kron(j.conj(),j)-(np.kron(eye,a)+np.kron(a.T,eye))/2
    return L


def main():
    model=perfect_code();entries=ports(model);E=model['energies'];hd=ten(I,np.diag(E))
    frequency=0.;reconstruction=0.;good_residual=0.
    for seed in model['seeds']:
        relevant=[p for p in entries if p['label']==seed['label']]
        rebuilt=sum(p['operator'] if p['omega']==0 else p['operator']+p['operator'].conj().T for p in relevant)
        reconstruction=max(reconstruction,norm(rebuilt-seed['recovery_pauli']))
    for p in entries:
        a=p['operator'];frequency=max(frequency,norm(comm(hd,a)+p['omega']*a))
        # Both nonidentity logical blocks and their adjoints have bad sources.
        A=16;part=(a[:A,:A]+a[A:,A:])/2;bad=a-ten(I,part)
        projector=ten(I,np.diag(p['bad_syndromes'].astype(float)))
        good_residual=max(good_residual,norm(bad-projector@bad@projector))
    assert max(frequency,reconstruction,good_residual)<1e-11
    beta=4.;blocks=charge_hamiltonians(model,entries,g=.6)
    pc=np.exp(-beta*blocks['gaps']);pc/=pc.sum();ps=np.exp(-beta*E);ps/=ps.sum()
    stationarity=0.;neutrality=0.;detuned=0.
    for k,H in enumerate(blocks['H']):
        H=H.toarray();weights=np.array([.5*ps[k^blocks['tags'][c]]*pc[c] for q in range(2) for c in range(blocks['C'])])
        sig=np.diag(weights)
        ref=np.diag([E[k^blocks['tags'][c]]+blocks['gaps'][c] for q in range(2) for c in range(blocks['C'])])
        stationarity=max(stationarity,norm(comm(H,sig)))
        neutrality=max(neutrality,norm(comm(H,ref)))
        shift=np.diag([.31*np.cos(1.7*c) for q in range(2) for c in range(blocks['C'])])
        detuned=max(detuned,norm(comm(H+shift,sig)))
    assert max(stationarity,neutrality,detuned)<1e-10
    # Exact rank-one thermal transitions of the multilevel controller.
    tau=np.diag(pc);drift=np.zeros_like(tau,dtype=complex)
    for c,p in enumerate(entries,1):
        j=np.zeros_like(tau,dtype=complex);j[0,c]=1
        drift+=diss(j,tau)+np.exp(-beta*p['omega'])*diss(j.conj().T,tau)
    assert norm(drift)<1e-12
    # Unfiltered pair coupling destroys the same-reference Gibbs identity.
    omega=2.;g=.4;Gamma=1.;b=2.
    tau1=np.diag([1,np.exp(-b*omega)]);tau1/=np.trace(tau1)
    sigma=ten(tau1,tau1);h0=omega*(ten(num,I)+ten(I,num))
    filtered=g*(ten(down,down.conj().T)+ten(down.conj().T,down))
    unfiltered=g*ten(X,X)
    js=[np.sqrt(Gamma)*ten(I,down),np.sqrt(Gamma*np.exp(-b*omega))*ten(I,down.conj().T)]
    fdef=norm(-1j*comm(h0+filtered,sigma)+sum(diss(j,sigma) for j in js))
    udef=float(np.abs(np.linalg.eigvalsh(-1j*comm(h0+unfiltered,sigma)+sum(diss(j,sigma) for j in js))).sum())
    assert fdef<1e-12 and udef>.5
    # An EXACTLY clean controller-ground compression can still leak logical
    # information through finite-speed controller relaxation. No bare Q fault.
    # This is a projection-transfer countermodel, not a model of the cited
    # photonic-Ising circuit and not a no-go for unfiltered memories.
    projection=[]
    for Omega in (4.,8.,16.):
        H=Omega*ten(I,num)+g*ten(Z,X)
        L=liouv(H,[ten(I,down)])
        iso=ten(I,np.array([[1],[0]],complex))
        compressed=norm(iso.conj().T@H@iso)
        initial=np.zeros((4,4),complex);initial[0,2]=1
        T=100.;final=(expm(T*L)@initial.reshape(-1,order='F')).reshape((4,4),order='F')
        coherence=final[0,2]+final[1,3]
        assert abs(coherence.imag)<1e-10 and compressed<1e-12
        projection.append({'Omega':Omega,'g':g,'Gamma':1.,'T':T,
                           'ground_compression_norm':compressed,'bare_logical_noise':0.,
                           'logical_coherence_retention':float(coherence.real),
                           'logical_dephasing_diamond_error':float(abs(1-coherence)),
                           'leading_small_g_dephasing_rate':g*g/(Omega*Omega+.25)})
    out={'complete_Pauli_seed_count':15,'positive_and_zero_energy_port_count':27,
         'controller_dimension':28,'reference_inverse_temperature':beta,
         'energy_component_commutator_residual':frequency,
         'Pauli_reconstruction_residual':reconstruction,
         'logical_bad_block_support_residual':good_residual,
         'reference_commutator_max_residual':stationarity,
         'reference_energy_conservation_residual':neutrality,
         'diagonal_controller_detuning_reference_residual':detuned,
         'controller_thermal_drift_residual':norm(drift),
         'unfiltered_transfer_guard':{'filtered_Gibbs_defect_norm':fdef,
                                      'unfiltered_Gibbs_defect_trace_norm':udef,
                                      'scope':'Failure of the exact same-reference stationarity proof, not a failure theorem for an unfiltered memory phase'},
         'projected_bias_transfer_countermodel':projection,
         'projection_scope':'Ground compression alone misses controller-mediated logical dephasing. This is NOT a derivation of that error in the photonic-Ising proposal.',
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'model_sha256':hashlib.sha256((Path(__file__).parent/'port_model.py').read_bytes()).hexdigest(),
         'scope':'Finite algebra, invariant-reference and admission countermodels; floating matrix checks support but do not prove the family theorem or a device regime'}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'algebra_and_obstructions.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'passed':True,'output':str(path),'frequency_residual':frequency,
                      'unfiltered_Gibbs_defect_trace_norm':udef,'projection_countermodel':projection}))


if __name__=='__main__':main()
