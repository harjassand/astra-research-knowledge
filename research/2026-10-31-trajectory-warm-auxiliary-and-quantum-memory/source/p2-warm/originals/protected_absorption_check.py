"""Reference-uniform warm-auxiliary absorption checks.

This is a finite CP model and exact algebra check, not a Yb device simulation.
Source operators remain in the state throughout all cycles.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm


def norm(a):
    return float(np.linalg.norm(a, 2))


def lindblad_super(h, jumps):
    d = len(h)
    eye = np.eye(d)
    gen = -1j*(np.kron(eye, h)-np.kron(h.T, eye))
    for l in jumps:
        a = l.conj().T@l
        gen += np.kron(l.conj(), l)-.5*np.kron(eye, a)-.5*np.kron(a.T, eye)
    return gen


def action(channel, rho):
    d = len(rho)
    return (channel@rho.reshape(-1, order="F")).reshape(d, d, order="F")


def annihilator(mode, nmodes):
    d = 1 << nmodes
    a = np.zeros((d, d), complex)
    for i in range(d):
        if i & (1 << mode):
            a[i ^ (1 << mode), i] = (-1)**((i & ((1 << mode)-1)).bit_count())
    return a


def main():
    rng = np.random.default_rng(963101)
    result = {}

    # Exact rational common Lyapunov certificate using the sharper effect lemma.
    p, c, beta = F(4, 5), F(2, 5), F(3, 5)
    r, b, u, d = F(1, 20), F(1, 20), F(1), F(1, 20)
    M = [[1-c+beta*b, beta*r], [u*b+d, u*r]]
    alpha, theta = F(1, 20), F(13, 20)
    margins = [theta-(M[0][0]+alpha*M[1][0]),
               theta*alpha-(M[0][1]+alpha*M[1][1])]
    assert all(m >= 0 for m in margins)
    assert beta == c*(1-c)/(p-c)
    result["rational_progress_example"] = {
        "p0": str(p), "r": str(r), "b": str(b), "u": str(u), "d": str(d),
        "c": str(c), "beta_sharp": str(beta), "alpha": str(alpha),
        "theta": str(theta), "weighted_column_margins": [str(m) for m in margins],
        "cooler_floor_b_over_1_minus_r": str(b/(1-r)),
        "scope": "A coarse mathematical source box, not assigned physical Yb parameters."}

    # Full multi-orbital fermion algebra: three spatial orbitals, six modes.
    # A triplet can doubly occupy one physical port if two orbitals belong to it.
    ops = [annihilator(i, 6) for i in range(6)]
    dag = [a.conj().T for a in ops]
    vac = np.eye(64)[:, 0].astype(complex)
    trip = []
    for i in range(3):
        for j in range(i+1, 3):
            uu = dag[2*i]@dag[2*j]@vac
            ud = dag[2*i]@dag[2*j+1]@vac
            du = dag[2*i+1]@dag[2*j]@vac
            dd = dag[2*i+1]@dag[2*j+1]@vac
            trip.extend([uu, (ud+du)/np.sqrt(2), dd])
    trip = np.column_stack(trip)
    point_checks = []
    for trial in range(8):
        phi = rng.normal(size=3)+1j*rng.normal(size=3)
        psi_up = sum(phi[i]*ops[2*i] for i in range(3))
        psi_dn = sum(phi[i]*ops[2*i+1] for i in range(3))
        pair = psi_dn@psi_up
        value = norm(pair@trip)
        assert value < 2e-13
        point_checks.append(value)
    # The first two orbitals may be at port a: an up-up triplet has n_a=2.
    nport = sum(dag[i]@ops[i] for i in range(4))
    hot_triplet = dag[0]@dag[2]@vac
    n_a = float(np.real(hot_triplet.conj()@nport@hot_triplet))
    assert n_a == 2
    result["full_orbital_opacity"] = {"triplet_dimension_with_3_orbitals": trip.shape[1],
        "maximum_local_singlet_loss_norm_on_triplets": max(point_checks),
        "hot_triplet_number_in_one_port": n_a}

    # Microscopic finite-window progress: all source states are included in
    # the accepted effect, even when the source Hamiltonian is very fast.
    Xs = np.array([[0, 1], [1, 0]], complex)
    Zs = np.diag([1., -1.])
    identity_s = np.eye(2)
    orbital_h = np.diag([0., 1.3, 3.1])
    off = np.zeros((3, 3))
    off[0, 1] = off[1, 0] = .2
    drive = np.kron(off, identity_s+.2*Xs)
    Pmicro = np.diag([1., 0., 0.])
    Pfull = np.kron(Pmicro, identity_s)
    Qfull = np.eye(6)-Pfull
    f = np.sqrt([.7, .2, .1])
    gain = .9*identity_s+.3*Zs
    J = np.kron(np.outer(f, f), gain)
    j_minus = .7*.6
    j_plus = 1.2
    v_cross = norm(Qfull@drive@Pfull)
    w_rate = v_cross+j_plus/2
    crossover = np.sqrt(j_minus/j_plus)/w_rate
    window = .4*crossover
    p_micro = (j_minus*window-np.sqrt(j_minus*j_plus)*w_rate*window**2
               +j_plus*w_rate**2*window**3/3)
    micro_records = []
    for source_rate in [0., 1., 20., 1000.]:
        H = (np.kron(orbital_h, identity_s)
             +np.kron(np.eye(3), source_rate*Xs)+drive)
        Kmicro = expm((-1j*H-J/2)*window)
        accepted = np.eye(6)-Kmicro.conj().T@Kmicro
        min_probability = float(np.linalg.eigvalsh(accepted[:2, :2])[0])
        assert min_probability >= p_micro-2e-11
        assert np.linalg.eigvalsh(accepted)[0] >= -2e-11
        H0 = Pfull@H@Pfull+Qfull@H@Qfull
        U0 = expm(-1j*H0*window)
        distance = norm((Kmicro-U0)@Pfull)
        assert distance <= w_rate*window+2e-11
        micro_records.append({"source_rate": source_rate,
            "minimum_accepted_probability_over_all_source_states": min_probability,
            "forward_propagator_distance": distance})
    result["microscopic_local_progress"] = {
        "j_minus": j_minus, "j_plus": j_plus, "v_cross": v_cross,
        "window": window, "certified_p0": p_micro,
        "forward_distance_bound": w_rate*window, "records": micro_records,
        "scope": "A complete finite no-event generator with a noncommuting retained quantum source. Not a material-specific reservoir qualification."}

    # Actual no-accepted-event CP map with an additional unresolved orbital
    # jump. Its positive first-accepted-event subset gives the corrected bound.
    orbital_mix = expm(.6j*(np.ones((3, 3))-np.eye(3)))
    other_jump_rate = .7
    Lother = np.sqrt(other_jump_rate)*np.kron(orbital_mix, expm(.31j*Zs))
    w_other = v_cross+(j_plus+other_jump_rate)/2
    assert window <= np.sqrt(j_minus/j_plus)/w_other
    p_other = (j_minus*window-np.sqrt(j_minus*j_plus)*w_other*window**2
               +j_plus*w_other**2*window**3/3)
    unresolved_records = []
    for source_rate in [0., 20., 1000.]:
        H = (np.kron(orbital_h, identity_s)
             +np.kron(np.eye(3), source_rate*Xs)+drive)
        no_accepted_gen = lindblad_super(H, [Lother])
        no_accepted_gen -= .5*(np.kron(np.eye(6), J)+np.kron(J.T, np.eye(6)))
        no_accepted = expm(window*no_accepted_gen)
        actual_effect = np.eye(6)-action(no_accepted.conj().T, np.eye(6))
        min_actual = float(np.linalg.eigvalsh(actual_effect[:2, :2])[0])
        assert min_actual >= p_other-2e-11
        unresolved_records.append({"source_rate": source_rate,
            "minimum_accepted_probability": min_actual})
    bad_naive_bound = 1.-.5+(.5**2)/3
    actual_dark_loss = (1.-np.exp(-101.))/101.
    assert actual_dark_loss < bad_naive_bound
    result["unresolved_jump_correction"] = {
        "unresolved_total_rate_bound": other_jump_rate,
        "corrected_p0": p_other, "records": unresolved_records,
        "omitted_jump_counterexample": {
            "j": 1., "ell": 100., "T": 1.,
            "incorrect_jump_free_bound": bad_naive_bound,
            "actual_accepted_probability": actual_dark_loss},
        "scope": "Scalar unobserved jumps preserve spin but can change orbital progress."}

    # Actual finite cooling channel with a retained noncommuting source.
    dm, de = 6, 2
    lower = np.diag(np.sqrt(np.arange(1, dm)), 1).astype(complex)
    number = lower.conj().T@lower
    N = np.kron(number, np.eye(de))
    eye = np.eye(dm*de)
    X = np.array([[0, 1], [1, 0]], complex)
    Z = np.diag([1., -1.])
    h = np.kron(number, np.eye(de))+np.kron(np.eye(dm), 20*X)+np.kron(number, 3*Z)
    down, up = 1., .05
    gamma = down-up
    ratio = .05
    time = -np.log(ratio)/gamma
    floor = up/gamma
    b0 = floor*(1-ratio)
    jumps = [np.sqrt(down)*np.kron(lower, np.eye(de)),
             np.sqrt(up)*np.kron(lower.conj().T, np.eye(de))]
    cool = expm(time*lindblad_super(h, jumps))
    coolstarN = action(cool.conj().T, N)
    drift_margin = float(np.linalg.eigvalsh(ratio*N+b0*eye-coolstarN)[0])
    assert drift_margin > -2e-10

    # A coherent, source-controlled absorber. It is not an orbital projector.
    rotp = .8
    U = expm(.71j*Z)
    embedding = np.zeros((dm*de, de), complex)
    embedding[:de] = np.sqrt(rotp)*np.eye(de)
    embedding[de:2*de] = np.sqrt(1-rotp)*U
    proj = embedding@embedding.conj().T
    strength = np.log(5)
    K = eye+(np.exp(-strength/2)-1)*proj
    A = eye-K.conj().T@K
    p0 = (1-np.exp(-strength))*rotp
    P = np.zeros_like(eye)
    P[:de, :de] = np.eye(de)
    assert norm(P@A@P-p0*P) < 1e-12
    cc = p0/2
    bet = cc*(1-cc)/(p0-cc)
    effect_margin = float(np.linalg.eigvalsh(A-cc*eye+bet*N)[0])
    assert effect_margin > -1e-12
    uu = 1.
    dd = max(0., float(np.linalg.eigvalsh(K.conj().T@N@K-uu*N)[-1]))
    matrix = np.array([[1-cc+bet*b0, bet*ratio], [uu*b0+dd, uu*ratio]])
    lower_alpha = bet*ratio/(1-uu*ratio)
    upper_alpha = (cc-bet*b0)/(uu*b0+dd)
    assert lower_alpha < upper_alpha
    aa = (lower_alpha+upper_alpha)/2
    lam = max(matrix[0, 0]+aa*matrix[1, 0], matrix[1, 1]+matrix[0, 1]/aa)
    assert lam < 1
    weight = eye+aa*N
    adjoint_cycle = action(cool.conj().T, K.conj().T@weight@K)
    full_margin = float(np.linalg.eigvalsh(lam*weight-adjoint_cycle)[0])
    assert full_margin > -2e-10

    v = rng.normal(size=dm*de)+1j*rng.normal(size=dm*de)
    v /= np.linalg.norm(v)
    rho = np.outer(v, v.conj())
    initial_energy = float(np.real(np.trace(N@rho)))
    records = []
    for cycle in range(51):
        survival = float(np.real(np.trace(rho)))
        energy = float(np.real(np.trace(N@rho)))
        bound = lam**cycle*(1+aa*initial_energy)
        assert survival+aa*energy <= bound+2e-10
        if cycle in [0, 1, 2, 5, 10, 20, 50]:
            records.append({"cycle": cycle, "survival": survival,
                "unnormalized_energy": energy,
                "conditional_energy": energy/survival if survival else None,
                "weighted_bound": bound})
        rho = K@action(cool, rho)@K.conj().T
    result["retained_source_CP_model"] = {
        "source_frequency": 20., "noncommuting_number_source_coupling": 3.,
        "p0": p0, "r": ratio, "b": b0, "u": uu, "d_from_actual_filter": dd,
        "alpha": aa, "lambda": lam, "initial_energy": initial_energy,
        "minimum_cooling_drift_margin": drift_margin,
        "minimum_sharp_effect_margin": effect_margin,
        "minimum_complete_weighted_margin": full_margin,
        "records": records,
        "scope": "Finite CP model. The same source state is carried through every cycle; no source reset or bath inverse."}

    out = Path(__file__).with_name("protected_absorption_results.json")
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"rational_theta": str(theta),
                      "orbital_triplet_loss_residual": max(point_checks),
                      "microscopic_p0": p_micro,
                      "microscopic_worst_actual_p0": min(x["minimum_accepted_probability_over_all_source_states"] for x in micro_records),
                      "retained_source_lambda": lam,
                      "filter_energy_cost_d": dd,
                      "final_survival": records[-1]["survival"],
                      "output": str(out)}, indent=2))


if __name__ == "__main__":
    main()
