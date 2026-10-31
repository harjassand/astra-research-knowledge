"""Checks a deterministic single-excitation obstruction and a two-photon escape.

These are finite-model checks, not a device fit. The two-photon code and
bosonic controlled-swap ingredients are established constructions; the
comparative resource statement and failure tests are the point of this file.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, norm

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(1031)


def haar(m):
    q, r = np.linalg.qr(rng.normal(size=(m,m)) + 1j*rng.normal(size=(m,m)))
    return q @ np.diag(np.diag(r)/np.abs(np.diag(r)))


SX = np.array([[0,1],[1,0]], complex)
SY = np.array([[0,-1j],[1j,0]], complex)
SZ = np.diag([1,-1]).astype(complex)
paulis = [SX,SY,SZ]


def scalar_residual(k, u=None):
    if u is None:
        u = np.eye(len(k))
    c = np.trace(u.conj().T @ k) / len(k)
    return float(norm(k-c*u,2))


def obstruction(m, intervals=16, samples=4096):
    dt = 1/intervals
    v0 = np.eye(m, 2, dtype=complex)
    unitaries = [haar(m) for _ in range(intervals)]
    vectors=[]
    for u in unitaries:
        w=u@v0
        e=np.einsum('ji,jk->jik',w.conj(),w)
        vectors.append(np.stack([np.einsum('jik,ki->j',e,s).real for s in paulis],axis=1))
    vectors=np.array(vectors)
    z=1-2*(np.arange(samples)+.5)/samples
    phi=np.arange(samples)*np.pi*(3-np.sqrt(5))
    directions=np.column_stack([np.sqrt(1-z*z)*np.cos(phi),np.sqrt(1-z*z)*np.sin(phi),z])
    f=np.sum(np.abs(np.einsum('tmc,kc->ktm',vectors,directions)),axis=(1,2))*dt
    best=directions[np.argmax(f)]
    signs=np.sign(np.einsum('tmc,c->tm',vectors,best))
    a=sum((u.conj().T@np.diag(sign)@u)*dt for u,sign in zip(unitaries,signs))
    projected=v0.conj().T@a@v0
    traceless=projected-np.trace(projected)*np.eye(2)/2
    _,evec=np.linalg.eigh(traceless)
    psi=(evec[:,0]+evec[:,1])/np.sqrt(2)
    rows=[]
    for epsilon in [.001,.003,.01,.03]:
        kfull=np.eye(m,dtype=complex)
        for u,sign in zip(unitaries,signs):
            gam=u.conj().T@np.diag(2*epsilon+epsilon*sign)@u
            kfull=expm(-gam*dt/2)@kfull
        k=v0.conj().T@kfull@v0
        state=k@psi
        state/=norm(state)
        td=norm(state-psi*np.vdot(psi,state))
        rows.append({"epsilon":epsilon,"conditional_trace_distance":float(td),
                     "trace_distance_div_epsilon_T":float(td/epsilon)})
    return {"modes":m,"spherical_average_lower_bound_f":1.0,
            "sampled_max_f":float(max(f)),
            "traceless_integrated_hazard_norm_div_epsilon":float(norm(traceless,2)),
            "guaranteed_lower_bound":.5,
            "finite_noise_checks":rows}


# N=2 sector ordered |20>, |11>, |02>.
na=np.diag([2.,1.,0.]); nb=2*np.eye(3)-na
hx=np.sqrt(2)*np.array([[0,1,0],[1,0,1],[0,1,0]],complex)
hy=np.sqrt(2)*np.array([[0,-1j,0],[1j,0,-1j],[0,1j,0]],complex)
v=np.column_stack([np.array([0,1,0]),np.array([1,0,1])/np.sqrt(2)]).astype(complex)
p=v@v.conj().T
q=np.eye(3)-p


def two_photon():
    v2=np.kron(v,v)
    h2=np.kron(na,na)
    target=np.diag([-1,1,1,1]).astype(complex)
    u2=expm(-1j*np.pi*h2)
    compressions=[]
    for t in np.linspace(0,np.pi,11):
        w=expm(-1j*t*h2)@v2
        compressions.append(max(norm(w.conj().T@nj@w-np.eye(4),2) for nj in
                                [np.kron(na,np.eye(3)),np.kron(nb,np.eye(3)),
                                 np.kron(np.eye(3),na),np.kron(np.eye(3),nb)]))
    # No-jump checker failure: rotate P to the easy even-parity subspace,
    # wait with unequal mode losses, then undo. Every no-jump run passes
    # parity, but it acquires a first-order logical filter.
    rotation=expm(-1j*(np.pi/4)*hy)
    peven=np.diag([1.,0.,1.])
    rot_error=norm(rotation@p@rotation.conj().T-peven,2)
    scaling=[]
    for e in [.001,.003,.01,.03]:
        gam=e*na+3*e*nb
        direct=v.conj().T@expm(-gam/2)@v
        naive=v.conj().T@rotation.conj().T@peven@expm(-gam/2)@rotation@v
        scaling.append({"epsilon":e,
                        "ideal_symmetry_projector_scalar_residual":scalar_residual(direct),
                        "residual_div_epsilon_squared":scalar_residual(direct)/(e*e),
                        "rotated_parity_checker_scalar_residual":scalar_residual(naive),
                        "rotated_residual_div_epsilon":scalar_residual(naive)/e})
    # A DIRECT controlled beam splitter preserves P at every time.
    # Ancilla basis g,e,f; f->e decay is a located failure if e readout succeeds.
    pg=np.diag([1.,0.,0.]); pf=np.diag([0.,0.,1.])
    plus=np.array([1,0,1],complex)/np.sqrt(2)
    minus=np.array([1,0,-1],complex)/np.sqrt(2)
    hctrl=np.kron(hx,pf)
    duration=np.pi/2
    uc=expm(-1j*hctrl*duration)
    vin=np.kron(v,plus[:,None])
    accepted=np.kron(v.conj().T,minus.conj()[None,:])@uc@vin
    # Ideal dephasing errors reject; relaxation to e cannot be accepted.
    zanc=np.diag([1.,0.,-1.])
    lanc=np.zeros((3,3)); lanc[1,2]=1
    acc_row=np.kron(v.conj().T,minus.conj()[None,:])
    fault_checks=[]
    for frac in [0,.1,.3,.5,.9,1]:
        left=expm(-1j*hctrl*duration*(1-frac))
        right=expm(-1j*hctrl*duration*frac)
        fault_checks.append({"fault_time_fraction":frac,
                             "dephasing_accepted_norm":float(norm(acc_row@left@np.kron(np.eye(3),zanc)@right@vin,2)),
                             "relaxation_accepted_norm":float(norm(acc_row@left@np.kron(np.eye(3),lanc)@right@vin,2))})
    # Data no-jump noise during direct cBS: code-projected accepted error is
    # quadratic, but late Q leakage in the accepted output is still linear.
    finite_checker=[]
    for e in [.001,.003,.01,.03]:
        gam=np.kron(e*na+3*e*nb,np.eye(3)) + np.kron(np.eye(3),2*e*pf)
        kn=expm((-1j*hctrl-gam/2)*duration)
        anc_accept=np.kron(np.eye(3),minus.conj()[None,:])@kn@vin
        k=v.conj().T@anc_accept
        finite_checker.append({"epsilon":e,
                               "in_code_accepted_scalar_residual":scalar_residual(k),
                               "in_code_residual_div_epsilon_squared":scalar_residual(k)/(e*e),
                               "accepted_out_of_code_amplitude":float(norm(q@anc_accept,2)),
                               "warning":"finite checker retains a linear late Q-leakage amplitude; stream/terminal treatment required"})
    return {"occupancy_compression_errors":[float(norm(v.conj().T@n@v-np.eye(2),2)) for n in [na,nb]],
            "beam_splitter_logical_2X_error":float(norm(v.conj().T@hx@v-2*SX,2)),
            "beam_splitter_leakage":float(norm(q@hx@v,2)),
            "local_Kerr_logical_matrix":(v.conj().T@na@nb@v).real.tolist(),
            "cross_Kerr_pi_entangler_error":float(norm(v2.conj().T@u2@v2-target,2)),
            "cross_Kerr_pi_leakage":float(norm((np.eye(9)-v2@v2.conj().T)@u2@v2,2)),
            "max_moving_occupancy_compression_error":float(max(compressions)),
            "naive_measurement_rotation_error":float(rot_error),
            "symmetry_measurement_scaling":scaling,
            "direct_controlled_BS_ideal_accept_error":float(norm(accepted-np.eye(2),2)),
            "direct_controlled_BS_ancilla_fault_checks":fault_checks,
            "direct_controlled_BS_finite_noise":finite_checker}


def main():
    out={"single_excitation_unknown_rate_obstruction":[obstruction(m) for m in [2,4,8]],
         "two_photon_code":two_photon(),
         "scope":"Deterministic per-branch statements. Independent physical Pauli randomization is a legitimate escape for averaged computation, and is not ruled out."}
    (HERE/"excitation_bound_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
