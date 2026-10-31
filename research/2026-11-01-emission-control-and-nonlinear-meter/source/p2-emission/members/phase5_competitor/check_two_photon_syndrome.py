"""Check root's two-cross-Kerr syndrome construction without a direct cBS.

N=2 per block; basis |20>, |11>, |02>. The helper is a second encoded
two-photon block, and its full three-outcome final measurement is retained.
Single losses are algebraically orthogonal in total number; this file tests
the nontrivial no-jump, phase, gate-angle, and finite-duration checks.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, norm

HERE=Path(__file__).resolve().parent
I=np.eye(3)
n=np.diag([2.,1.,0.]); nb=2*I-n
h=np.sqrt(2)*np.array([[0,1,0],[1,0,1],[0,1,0]],complex)
j=h/2
v=np.column_stack([np.array([0,1,0]),np.array([1,0,1])/np.sqrt(2)]).astype(complex)
p=v@v.conj().T; q=I-p
hp=(v[:,0]+v[:,1])/np.sqrt(2)
hm=(v[:,0]-v[:,1])/np.sqrt(2)
hq=np.array([1,0,-1],complex)/np.sqrt(2)
vin=np.kron(v,hp[:,None])
row=np.kron(I,hm.conj()[None,:])
HC=np.kron(n,n)
C=expm(-1j*np.pi*HC)
X=expm(-1j*np.pi*j/2)
XD=np.kron(X,I)
U=C@XD@C@XD.conj().T


def scalar_error(k):
    c=np.trace(k)/len(k)
    return float(norm(k-c*np.eye(len(k)),2))


def projected(Uop):
    raw=row@Uop@vin
    return raw,v.conj().T@raw


def timed(rates, tx=.2, tc=.5):
    # Chronological X dagger, C, X, C. Last physical interaction is Kerr.
    gam=np.kron(rates[0]*n+rates[1]*nb,I)+np.kron(I,rates[2]*n+rates[3]*nb)
    hx=np.kron((np.pi/(2*tx))*j,I)
    hc=(np.pi/tc)*HC
    sequence=[(-hx,tx),(hc,tc),(hx,tx),(hc,tc)]
    out=np.eye(9,dtype=complex)
    for H,t in sequence:
        out=expm((-1j*H-gam/2)*t)@out
    return out


def byproduct_timed(rates, tx=.2, tc=.5):
    # Improved chronological C, X, C. The known X is tracked, not undone.
    hx=np.kron((np.pi/(2*tx))*j,I)
    hc=(np.pi/tc)*HC
    out=np.eye(9,dtype=complex)
    all_rates=np.repeat(np.asarray(rates)[None,:],3,axis=0) if np.asarray(rates).ndim==1 else rates
    for (H,t),rr in zip([(hc,tc),(hx,tx),(hc,tc)],all_rates):
        gam=np.kron(rr[0]*n+rr[1]*nb,I)+np.kron(I,rr[2]*n+rr[3]*nb)
        out=expm((-1j*H-gam/2)*t)@out
    return out


def main():
    full_accept=row@U@np.kron(I,hp[:,None])
    full_reject=np.kron(I,hp.conj()[None,:])@U@np.kron(I,hp[:,None])
    noise=[]
    control=[]
    for e in [.001,.003,.01,.03]:
        raw,k=projected(timed(e*np.array([1,3,2,4])))
        noise.append({"epsilon":e,"in_code_scalar_residual":scalar_error(k),
                      "residual_div_epsilon_squared":scalar_error(k)/(e*e),
                      "accepted_Q_amplitude":float(norm(q@raw,2)),
                      "Q_amplitude_div_epsilon":float(norm(q@raw,2)/e)})
        Cerr=expm(-1j*(np.pi+e)*HC)
        Xerr=expm(-1j*(np.pi/2+e)*j)
        for label,Uerr in [
                ("last_Kerr",Cerr@XD@C@XD.conj().T),
                ("first_Kerr",C@XD@Cerr@XD.conj().T),
                ("middle_X",C@np.kron(Xerr,I)@C@XD.conj().T),
                ("initial_Xdagger",C@XD@C@np.kron(Xerr.conj().T,I))]:
            rawerr,kerr=projected(Uerr)
            control.append({"location":label,"angle_error":e,
                            "in_code_scalar_residual":scalar_error(kerr),
                            "accepted_Q_amplitude":float(norm(q@rawerr,2)),
                            "mean_accept_probability_from_code":float(np.trace(rawerr.conj().T@rawerr).real/2)})
    # Any helper number-diagonal error commutes with the whole circuit.
    helper=[]
    for label,F in [("number_phase_jump",n),
                    ("finite_unknown_phase",expm(-.31j*n)),
                    ("unequal_nojump_attenuation",expm(-.14*n-.03*nb)),
                    ("dephasing_nojump",expm(-.14*n@n))]:
        E=np.kron(I,F)
        raw,k=projected(U@E)
        helper.append({"operator":label,"commutator_norm":float(norm(E@U-U@E,2)),
                       "data_in_code_scalar_residual":scalar_error(k),
                       "data_Q_amplitude":float(norm(q@raw,2))})
    # Jx eigenbasis measurement separates logical +/- and Q. Columns are
    # those eigenstates, so M maps them to distinct number-resolved outcomes.
    eigvecs=np.column_stack([hp,hq,hm])
    M=eigvecs.conj().T
    readout={"orthonormality_error":float(norm(eigvecs.conj().T@eigvecs-I,2)),
             "Jx_eigenvalues":np.diag(eigvecs.conj().T@j@eigvecs).real.tolist(),
             "plus_read_probabilities":np.abs(M@hp).round(14).tolist(),
             "Q_read_probabilities":np.abs(M@hq).round(14).tolist(),
             "minus_read_probabilities":np.abs(M@hm).round(14).tolist(),
             "interpretation":"A physical SU(2) mode rotation maps Jx eigenstates to distinct Fock occupations; all losses lower the total helper count."}
    # The identical two-C circuit in N=1 does not reject with certainty.
    n1=np.diag([1.,0.]); j1=np.array([[0,1],[1,0]],complex)/2
    C1=expm(-1j*np.pi*np.kron(n1,n))
    X1=expm(-1j*np.pi*j1/2)
    XD1=np.kron(X1,I)
    U1=C1@XD1@C1@XD1.conj().T
    accept1=np.kron(np.eye(2),hm.conj()[None,:])@U1@np.kron(np.eye(2),hp[:,None])
    # Remove the initial X dagger, retain the logical X byproduct.
    Ub=C@XD@C
    full_accept_b=row@Ub@np.kron(I,hp[:,None])
    full_reject_b=np.kron(I,hp.conj()[None,:])@Ub@np.kron(I,hp[:,None])
    target_b=1j*np.array([[0,1],[1,0]],complex)
    byproduct=[]
    for e in [.001,.003,.01,.03]:
        Xerr=expm(-1j*(np.pi/2+e)*j)
        raw_angle,k_angle=projected(C@np.kron(Xerr,I)@C)
        raw_noise,k_noise=projected(byproduct_timed(e*np.array([1,3,2,4])))
        raw_vary,k_vary=projected(byproduct_timed(e*np.array([[1,3,2,4],[4,1,3,2],[2,5,1,3]])))
        byproduct.append({"epsilon":e,
                          "single_X_angle_accepted_target_cosine_error":float(norm(k_angle-target_b*np.cos(e),2)),
                          "single_X_angle_accepted_Q_amplitude":float(norm(q@raw_angle,2)),
                          "finite_noise_in_code_relative_to_byproduct":scalar_error(target_b.conj().T@k_noise),
                          "finite_noise_accepted_Q_amplitude":float(norm(q@raw_noise,2)),
                          "time_varying_noise_in_code_residual":scalar_error(target_b.conj().T@k_vary),
                          "time_varying_residual_div_epsilon_squared":scalar_error(target_b.conj().T@k_vary)/(e*e),
                          "time_varying_noise_accepted_Q_amplitude":float(norm(q@raw_vary,2))})
    # Known helper preparation error stays a pointer-only error for valid data.
    prep_checks=[]
    for label,helper_state in [("logical_zero",v[:,0]),("logical_one",v[:,1]),("Q",hq)]:
        got=Ub@np.kron(v,helper_state[:,None])
        # Data factor X, helper phase depends only on its occupation parity.
        helper_after=np.diag([1,-1,1])@helper_state
        expected=np.kron(v@(-target_b),helper_after[:,None])
        prep_checks.append({"initial_helper":label,"data_factorization_error":float(norm(got-expected,2))})
    out={"ideal_accepted_operator_minus_P_error":float(norm(full_accept+p,2)),
         "ideal_rejected_operator_Q_error":float(norm(full_reject-q,2)),
         "finite_duration_nojump":noise,
         "single_primitive_angle_errors":control,
         "helper_diagonal_noise":helper,
         "destructive_helper_readout":readout,
         "N1_data_max_false_accept_probability_with_perfect_helper_read":float(norm(accept1,2)**2),
         "improved_byproduct_checker":{
             "sequence":"C X C, with logical X tracked in the Pauli frame",
             "accepted_iJx_error":float(norm(full_accept_b-1j*j,2)),
             "rejected_Q_error":float(norm(full_reject_b-q,2)),
             "checks":byproduct,
             "helper_preparation_factorization":prep_checks,
             "symmetry_check_elapsed_example":2.2,
             "extra_required":"data total-number/parity check; delayed-output coverage; readout fault budget; noisy outer recovery"},
         "complete_elapsed_time_example":{
             "two_Kerr_maps":1.0,"two_data_X_pulses":.4,
             "helper_readout_rotation":.2,"helper_readout":.45,
             "helper_reload":.3,"feedforward":.05,
             "symmetry_check_total":2.4,
             "additional_required":"data total-number/parity check, input helper preparation validation, routing, outer syndrome/recovery",
             "parameters_are":"illustrative, not a hardware fit"},
         "scope":"Root-proposed construction, independently algebraically checked here. Not an external independent validation. Late Q leakage, finite readout mistakes and outer recovery remain in the contract."}
    (HERE/"two_photon_syndrome_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
