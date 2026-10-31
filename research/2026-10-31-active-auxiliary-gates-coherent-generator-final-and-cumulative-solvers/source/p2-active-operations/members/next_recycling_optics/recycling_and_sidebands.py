"""Full recycled optical response and adversarial positive-gain sidebands.

All times, frequencies, and rates are dimensionless.  This script verifies
finite-dimensional identities and model diagnostics; it does not qualify a
microscopic atom, rotating-wave approximation, or output detector.
"""
import json
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import eigvals, expm, norm, solve_continuous_lyapunov

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "physical_window"))
from atomic_closure_checks import optical_operators


def operators(delta1=20., delta2=20., gamma=1.):
    ps, ds = optical_operators()
    h0 = np.zeros((12, 12), complex)
    h0[3:, 3:] = delta1*ps[1] + delta2*ps[2]
    v = np.zeros((12, 12), complex)
    v[3:, :3] = np.sqrt(3)*ds[2]
    jumps = []
    for dl in ds:
        j = np.zeros((12, 12), complex)
        j[:3, 3:] = np.sqrt(gamma)*dl.T
        jumps.append(j)
    return h0, v, jumps


def adjoint_matrix(h, jumps, decay):
    n = len(h)
    def adj(x):
        return (1j*(h@x-x@h) + sum(j.conj().T@x@j for j in jumps)
                - (decay@x+x@decay)/2)
    return np.column_stack([adj(np.eye(n*n)[:, k].reshape(n, n)).reshape(n*n)
                            for k in range(n*n)])


def recycling_witness(delta=20., gamma=1., g0=1., eta=.25):
    h0, v, jumps = operators(delta, delta, gamma)
    ss = [0, 1, 9, 10]  # g_x,g_y,e_zx,e_zy
    rr = [j for j in range(12) if j not in ss]
    r = np.eye(12)[:, rr]
    vv = r.T@(v+v.conj().T)@r
    h = r.T@h0@r + g0*vv
    jr = [r.T@j@r for j in jumps]
    decay = r.T@sum(j.conj().T@j for j in jumps)@r
    adj = adjoint_matrix(h, jr, decay)
    p = np.linalg.solve(adj, -np.eye(8).reshape(64)).reshape(8, 8)
    p = (p+p.conj().T)/2
    comm = 1j*(vv@p-p@vv)
    pe = np.linalg.eigvalsh(p)
    margin = 1-eta*norm(comm, 2)
    return {
        "delta": delta, "gamma": gamma, "g0": g0,
        "gain_radius": eta, "transient_indices": rr,
        "poisson_residual": float(norm((adj@p.reshape(64)).reshape(8, 8)+np.eye(8))),
        "P_real": p.real.tolist(), "P_imag": p.imag.tolist(),
        "P_eigenvalues": pe.tolist(), "gain_commutator_norm": float(norm(comm, 2)),
        "robust_negative_margin": float(margin),
        "population_decay_rate": float(margin/pe[-1]),
        "population_prefactor": float(pe[-1]/pe[0]),
        "conservative_P_min_margin": float(pe[0]-1),
        "conservative_P_max_margin": float(4.5-pe[-1]),
        "conservative_commutator_margin": float(1.6-norm(comm, 2)),
    }


def large_drive_counterexample(delta=20., gamma=1.):
    out = []
    for m in [0., 3., 10., 30., 100., 300., 1000.]:
        # Re A=1 at every M.  A's scalar phase can be removed from b.
        a = np.sqrt(1+m*m)
        h = np.array([[0, np.sqrt(3)*a, 0],
                      [np.sqrt(3)*a, 2*delta/3, -np.sqrt(2)*delta/3],
                      [0, -np.sqrt(2)*delta/3, delta/3]], complex)
        j = np.zeros((3, 3), complex); j[0, 1] = np.sqrt(gamma)
        decay = np.diag([0., gamma, gamma])
        adj = adjoint_matrix(h, [j], decay)
        gap = -max(eigvals(adj).real)
        out.append({"imag_A": m, "abs_A": float(a), "gap": float(gap),
                    "gap_times_abs_A_squared": float(gap*a*a),
                    "asymptotic_coefficient_Gamma_Delta_squared_over_13p5":
                        gamma*2*delta*delta/27})
    return out


def split_sideband_branch(delta=2., gamma=1., kappa=np.sqrt(3)/4):
    """Exact first-photon harmful branch in the large-carrier-detuning limit.

    Subsequent bright-state recovery is included analytically in the error
    expressions.  Using a no-jump propagator only UNTIL the first jump is an
    exact instrument calculation, not neglect of recycling after that jump.
    """
    h = np.array([[0, kappa, 0], [kappa, delta/2, delta/2],
                  [0, delta/2, delta/2]], complex)
    decay = gamma*np.diag([0., 1., 1.])
    n = -1j*h-decay/2
    # X = integral exp(N^dagger t) Gamma |t><t| exp(Nt) dt.
    effect = solve_continuous_lyapunov(n.conj().T, -gamma*np.diag([0., 0., 1.]))
    probability = float(effect[0, 0].real)
    formula = (delta**2*(delta**2+2*kappa**2+gamma**2)
               /(2*delta**4+(4*kappa**2+3*gamma**2)*delta**2
                 +(2*kappa**2+gamma**2)**2))
    return {"delta": delta, "gamma": gamma, "kappa": float(kappa),
            "harmful_probability_lyapunov": probability,
            "harmful_probability_formula": float(formula),
            "formula_residual": abs(probability-formula),
            "natural_recovery_choi_error": 3*formula/4,
            "optimal_fixed_cartesian_record_recovery_lower_bound": formula/2}


def liouvillian(h, jumps):
    n = len(h); eye = np.eye(n)
    mat = -1j*(np.kron(eye, h)-np.kron(h.T, eye))
    for j in jumps:
        jj = j.conj().T@j
        mat += np.kron(j.conj(), j)-.5*np.kron(eye, jj)-.5*np.kron(jj.T, eye)
    return mat


def sideband_memory(delta1=20., delta2=40., omega=20., T=50.,
                    g0=1., eta=.25, gamma=1., settle=12., mixed_source=False):
    """Identity memory on the x/y ground code, with all optical histories.

    Positive G=g0(I+eta X). H_E=omega Z/2.  The initially occupied +Z
    source level is unprepared in the theorem's worst-case sense: one
    admissible auxiliary state is enough to test a uniform claim.
    """
    h0, v, jumps0 = operators(delta1, delta2, gamma)
    eye2 = np.eye(2); sx = np.array([[0., 1.], [1., 0.]])
    sz = np.diag([1., -1.]); he = omega*sz/2
    gain = g0*(eye2+eta*sx)
    h = np.kron(h0, eye2)+np.kron(v+v.conj().T, gain)+np.kron(np.eye(12), he)
    jumps = [np.kron(j, eye2) for j in jumps0]
    n = len(h); liou = liouvillian(h, jumps)
    rhoe = eye2/2 if mixed_source else np.diag([1., 0.])
    ini = []
    for a in range(2):
        for b in range(2):
            x = np.zeros((12, 12)); x[a, b] = .5
            ini.append(np.kron(x, rhoe).reshape(n*n, order="F"))
    ini = np.column_stack(ini)
    # Integral of all emissions, plus x/y-polarized emissions (including
    # recovery photons after the logical information has already been lost).
    effects = [sum(j.conj().T@j for j in jumps),
               jumps[0].conj().T@jumps[0]+jumps[1].conj().T@jumps[1]]
    aug = np.zeros((n*n+2, n*n+2), complex); aug[:n*n, :n*n] = liou
    for k, ef in enumerate(effects): aug[n*n+k, :n*n] = ef.T.reshape(-1, order="F")
    result = expm(T*aug)@np.vstack([ini, np.zeros((2, 4))])
    if settle:
        hoff = np.kron(h0, eye2)+np.kron(np.eye(12), he)
        aoff = aug.copy(); aoff[:n*n, :n*n] = liouvillian(hoff, jumps)
        result = expm(settle*aoff)@result
    out = np.zeros((24, 24), complex)
    for a in range(2):
        for b in range(2):
            x = result[:n*n, 2*a+b].reshape(n, n, order="F")
            red = np.einsum("aibi->ab", x.reshape(12, 2, 12, 2))
            out[a::2, b::2] = red
    bell = np.zeros(24); bell[0] = bell[3] = 1/np.sqrt(2)
    target = np.outer(bell, bell)
    err = .5*np.sum(abs(np.linalg.eigvalsh((out+out.conj().T)/2-target)))
    bright = float(np.trace(out[4:6, 4:6]).real)
    return {"delta1": delta1, "delta2": delta2, "omega": omega,
            "T": T, "settle": settle, "total_time": T+settle,
            "positive_gain_min": g0*(1-eta), "positive_gain_max": g0*(1+eta),
            "mixed_source": mixed_source,
            "logical_choi_trace_error": float(err), "remaining_ground_bright_probability": bright,
            "mean_all_emissions": float((result[n*n, 0]+result[n*n, 3]).real),
            "mean_xy_emissions": float((result[n*n+1, 0]+result[n*n+1, 3]).real),
            "trace": float(np.trace(out).real),
            "minimum_eigenvalue": float(np.linalg.eigvalsh((out+out.conj().T)/2)[0])}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(); parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    result = {"recycling_witness": recycling_witness(),
              "large_drive_counterexample": large_drive_counterexample(),
              "split_sideband_branch": [split_sideband_branch(delta=d)
                                        for d in [0., .01, .1, .5, 1., 2., 5., 10., 100.]]}
    if args.full:
        result["sideband_memories"] = [
            sideband_memory(delta1=d, delta2=2*d, omega=w)
            for d in [20., 50., 100.] for w in [0., d]]
        result["mixed_source_resonance"] = sideband_memory(delta1=100., delta2=200., omega=100., mixed_source=True)
        result["fixed_split_resonance"] = [sideband_memory(delta1=d, delta2=d+2., omega=d)
                                           for d in [20., 100., 1000.]]
    (ROOT / "recycling_and_sidebands_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
