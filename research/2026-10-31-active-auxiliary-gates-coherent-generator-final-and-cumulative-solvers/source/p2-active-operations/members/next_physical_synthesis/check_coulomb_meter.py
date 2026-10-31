"""Finite checks for the explicit prepared Coulomb charge probe.

The analytic proof is in COULOMB_PROBE_AND_DOMAIN.txt. These ordinary double
precision checks are not interval certificates, device predictions, or tests
of the full continuum reservoir reduction.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, eigvalsh, norm

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1., -1.]).astype(complex)
Np = np.diag([0., 1.]).astype(complex)
HAD = (X+Z)/np.sqrt(2)
plus = np.array([1., 1.], complex)/np.sqrt(2)


def charge_kraus(q, omega, xi=.02, chi=1., finite_rotation=None):
    """Source first, probe second. All source states are tested via effects."""
    HE = omega*(.8*X+.6*Z)
    source = np.kron(HE, I)
    charge = np.kron(I, chi*q*Np)
    perturbation = np.kron(xi*Z, Np)
    U = expm(-1j*(source+charge+perturbation)*np.pi/(2*chi))
    if finite_rotation is None:
        U = np.kron(I, HAD) @ U
    else:
        om = finite_rotation
        U = expm(-1j*(source+charge+perturbation+
                     np.kron(I, om*HAD/2))*np.pi/om) @ U
    entrance = np.kron(I, plus.reshape(2, 1))
    return [np.kron(I, np.eye(2)[j].reshape(1, 2)) @ U @ entrance
            for j in (0, 1)]


def count_effects(K, m):
    """All count-history effects, without enumerating 2**m strings."""
    effects = [I]
    for _ in range(m):
        nxt = [np.zeros((2, 2), complex) for __ in range(len(effects)+1)]
        for k, E in enumerate(effects):
            nxt[k] += K[1].conj().T @ E @ K[1]
            nxt[k+1] += K[0].conj().T @ E @ K[0]
        effects = nxt
    return effects


def classify(k, m):
    if k/m > .75:
        return 0
    if k/m < .25:
        return 2
    return 1


def main():
    result = {}
    # Check density decomposition over the complete allowed occupation domain.
    V = np.array([[.7, .22], [.31, .91]])
    c = 2*V[1, 0]
    a = V[0, 0]-V[1, 0]
    b = 2*(V[1, 1]-V[1, 0])
    chi = V[0, 1]-V[0, 0]-V[1, 1]+V[1, 0]
    residual = []
    for q in range(3):
        for n in range(2):
            full = q*((1-n)*V[0, 0]+n*V[0, 1]) + \
                   (2-q)*((1-n)*V[1, 0]+n*V[1, 1])
            residual.append(abs(full-(c+a*q+b*n+chi*q*n)))
    result['coulomb_decomposition_max_residual'] = max(residual)
    ideal = []
    for q in range(3):
        K = charge_kraus(q, 0., xi=0.)
        ideal.append(float(np.trace(K[0].conj().T@K[0]).real/2))
    result['ideal_port0_probabilities_q012'] = ideal

    tests = []
    for omega in [0., .3, 3., 30., 300., 3000.]:
        for q in range(3):
            K = charge_kraus(q, omega)
            effect = K[0].conj().T@K[0]
            vals = eigvalsh(effect)
            central = [1., .5, 0.][q]
            max_dev = max(abs(vals-central))
            source_bound = .02*np.pi/2
            assert max_dev <= source_bound+1e-11
            assert norm(sum(k.conj().T@k for k in K)-I, 2) < 1e-10
            tests.append({'q':q, 'omega':omega,
                          'port0_effect_min':float(vals[0]),
                          'port0_effect_max':float(vals[-1]),
                          'source_Duhamel_bound':source_bound})
    result['all_source_states_effect_checks'] = tests

    # Deliberately noncommuting source perturbation; a source state is never reset.
    record_tests = []
    nu = .02*np.pi/2
    for m in [8, 16, 32, 64, 128]:
        for q in range(3):
            K = charge_kraus(q, .3)
            effects = count_effects(K, m)
            bad = sum((E for k, E in enumerate(effects)
                       if classify(k, m) != q), np.zeros((2, 2), complex))
            wrong = float(eigvalsh((bad+bad.conj().T)/2)[-1])
            bound = min(1., 2*np.exp(-2*m*(.25-nu)**2))
            assert wrong <= bound+1e-11
            record_tests.append({'m':m, 'q':q,
                                 'worst_source_label_error':wrong,
                                 'martingale_upper_bound':float(bound)})
    result['complete_correlated_record_checks'] = record_tests

    finite = []
    for q in range(3):
        K = charge_kraus(q, .3, finite_rotation=200.)
        vals = eigvalsh(K[0].conj().T@K[0])
        finite.append({'q':q,'min':float(vals[0]),'max':float(vals[-1])})
    result['finite_helper_rotation_effects_Omega200'] = finite

    # Static joint-gap inequality with an explicitly included finite source.
    rng = np.random.default_rng(3102026)
    gap_tests = []
    for index in range(12):
        low = rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        low = (low+low.conj().T)/2
        high = rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        high = (high+high.conj().T)/2+30*np.eye(4)
        W = rng.normal(size=(3,4))+1j*rng.normal(size=(3,4))
        W *= .2/norm(W,2)
        H0=np.zeros((7,7),complex)
        H0[:3,:3]=low; H0[3:,3:]=high
        off=np.zeros_like(H0); off[:3,3:]=W; off[3:,:3]=W.conj().T
        gap=float(eigvalsh(high)[0]-eigvalsh(low)[-1])
        v=float(norm(off,2))
        t=[.1,1.,10.][index%3]
        measured=float(norm(expm(-1j*(H0+off)*t)-expm(-1j*H0*t),2))
        bound=2*v/gap+4*v*v*t/gap
        assert measured<=bound+1e-11
        gap_tests.append({'gap':gap,'off_norm':v,'t':t,
                          'unitary_operator_difference':measured,
                          'proved_bound':bound})
    result['static_joint_gap_checks'] = gap_tests
    result['limitations'] = [
        'Finite double-precision checks; analytic inequalities are in the note.',
        'No numerical semiconductor or continuum reservoir qualification.',
        'Finite-rotation tests include only the final rotation, not a full loading circuit.',
        'No claim of detector independence across records or a classical source model.'
    ]
    target=Path(__file__).with_name('coulomb_meter_results.json')
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({
        'decomposition_residual':max(residual),
        'ideal_port0_probabilities':ideal,
        'effect_cases':len(tests),
        'record_cases':len(record_tests),
        'record_128_errors':[r for r in record_tests if r['m']==128],
        'joint_gap_cases':len(gap_tests),
        'result_file':str(target.resolve())
    },indent=2))


if __name__=='__main__':
    main()
