"""Finite Gaussian-dilation and encoded-gate checks for the warm mediator audit.

Uses exact passive-mode linear algebra, not a bosonic Fock cutoff.
"""
import json
import numpy as np
from scipy.linalg import expm
from numpy.polynomial.hermite import hermgauss


def bus_dilation(kappa=.4, duration=6., desired_phase=np.pi/2, steps=512):
    dt=duration/steps
    c=np.exp(-kappa*dt/2)
    s=np.sqrt(1-c*c)
    # A polygonal circle, with radius set to realize the exact discrete phase.
    radius=np.sqrt(desired_phase*c/(steps*np.sin(2*np.pi/steps)))
    t=np.arange(steps+1)*dt
    beta=radius*(np.exp(2j*np.pi*t/duration)-1)
    beta[-1]=0.0
    free=np.eye(steps+1)
    xi=np.zeros(steps+1,complex)
    phase=0.
    drive=[]
    for k in range(1,steps+1):
        d=beta[k]/c-beta[k-1]
        drive.append(d)
        phase+=np.imag(d*np.conjugate(xi[0]))
        xi[0]+=d
        xi[0],xi[k]=c*xi[0]+s*xi[k],-s*xi[0]+c*xi[k]
        row0=free[0].copy();rowk=free[k].copy()
        free[0]=c*row0+s*rowk
        free[k]=-s*row0+c*rowk
    xi_in=free.T@xi
    direct_initial_bus=sum((c**k)*d for k,d in enumerate(drive))
    leakage=float(np.vdot(xi,xi).real)
    V=3.5;Vbus=50.5
    exponent_out=V*leakage+(Vbus-V)*abs(np.vdot(free[:,0],xi))**2
    variances=np.full(steps+1,V);variances[0]=Vbus
    exponent_in=float(np.sum(variances*np.abs(xi_in)**2))
    return {
        "steps":steps,
        "bus_closure":float(abs(xi[0])),
        "phase_error":float(abs(phase-desired_phase)),
        "passive_unitarity_error":float(np.linalg.norm(free.T@free-np.eye(steps+1))),
        "displacement_norm_error":float(abs(np.vdot(xi_in,xi_in).real-leakage)),
        "initial_bus_coefficient_error":float(abs(xi_in[0]-direct_initial_bus)),
        "initial_bus_coefficient_abs":float(abs(xi_in[0])),
        "outgoing_displacement_squared":leakage,
        "nonstationary_covariance_consistency_error":float(abs(exponent_out-exponent_in)),
        "unit_gap_dephasing_exponent_actual":exponent_in,
        "unit_gap_exponent_if_initial_bus_ignored":float(V*leakage),
    }


def encoded_gate():
    n=np.diag(np.arange(4,dtype=float))
    V=np.zeros((4,2),complex)
    V[0,0]=.5;V[2,0]=np.sqrt(3)/2
    V[1,1]=np.sqrt(3)/2;V[3,1]=.5
    E=2/np.sqrt(3)*(n-1.5*np.eye(4))
    R=[V.conj().T,V.conj().T@E]
    ns=np.kron(n,np.eye(4))+np.kron(np.eye(4),n)
    gate=expm(1j*np.pi/2*ns@ns)
    V2=np.kron(V,V)
    target=np.diag([1,1j,1j,1]).astype(complex)
    points,weights=hermgauss(80)
    results=[]
    for variance in (.001,.01,.1):
        averaged=np.zeros((4,4),complex)
        block_coherence=0j
        for x,w in zip(points,weights):
            phi=np.sqrt(2*variance)*x
            noise=np.diag(np.exp(-1j*phi*np.arange(4)))
            k=[rr@noise@V for rr in R]
            c=sum(kk[0,0]*np.conjugate(kk[1,1]) for kk in k)
            block_coherence+=w/np.sqrt(np.pi)*c
            for ka in k:
                for kb in k:
                    diagonal=np.diag(np.kron(ka,kb))
                    averaged+=w/np.sqrt(np.pi)*np.outer(diagonal,diagonal.conj())
        expected=(9*np.exp(-variance/2)-np.exp(-9*variance/2))/8
        # The normalized Choi matrix of a Schur channel has these nonzero
        # entries on the maximally correlated subspace.
        choi_difference=(averaged-np.ones((4,4)))/4
        choi_trace_distance=np.linalg.norm(choi_difference,ord="nuc")/2
        results.append({
            "phase_variance":variance,
            "single_block_exact_logical_Z_probability":float((1-expected)/2),
            "single_block_formula_error":float(abs(block_coherence-expected)),
            "joint_channel_CP_min_eigenvalue":float(np.linalg.eigvalsh(averaged).min()),
            "joint_channel_diagonal_error":float(np.max(np.abs(np.diag(averaged)-1))),
            "joint_channel_normalized_Choi_trace_distance":float(choi_trace_distance),
            "joint_correlations_not_product_error":float(abs(averaged[0,3]-block_coherence**2)),
        })
    return {
        "KL_first_moment_error":float(np.linalg.norm(V.conj().T@n@V-1.5*np.eye(2))),
        "KL_second_moment_error":float(np.linalg.norm(V.conj().T@n@n@V-3*np.eye(2))),
        "recovery_completeness_error":float(np.linalg.norm(sum(rr.conj().T@rr for rr in R)-np.eye(4))),
        "encoded_entangling_gate_error":float(np.linalg.norm(gate@V2-V2@target)),
        "gaussian_noise_checks":results,
    }


def main():
    dilation=bus_dilation()
    encoded=encoded_gate()
    # Collection-loss counterexample: absent native hot port remains hot.
    V=100.5;collection=.9;detector=.8;Vvac=.5
    naive_eta=collection*detector
    report={
        "dilation":dilation,
        "encoded_competitor":encoded,
        "collection_counterexample":{
            "thermal_quadrature_variance":V,
            "physical_port_collection_fraction":collection,
            "detector_efficiency":detector,
            "unobserved_native_port_variance_lower_bound":(1-collection)*V,
            "incorrect_vacuum_admixture_result_if_efficiencies_merged":V*Vvac*(1-naive_eta)/(naive_eta*V+(1-naive_eta)*Vvac),
        },
    }
    errors=[v for k,v in dilation.items() if k.endswith("error")]
    errors.extend(v for k,v in encoded.items() if k.endswith("error"))
    errors.extend(r["single_block_formula_error"] for r in encoded["gaussian_noise_checks"])
    report["passed"]=max(errors)<1e-10
    print(json.dumps(report,indent=2))
    if not report["passed"]:raise SystemExit(1)


if __name__=="__main__":main()
