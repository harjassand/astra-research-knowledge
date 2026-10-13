"""Independent finite checks for the CRAY intake and fixed-charge extension.

No original files are changed. Matrix inputs come directly from the source ZIP;
spin Hamiltonians below are reconstructed from Pauli matrices rather than the
producer's basis-loop builder. Exact rational claims are separated from floating
purification diagnostics. Successful execution is not proof of the universal
theorems, historical novelty, physical accuracy, or useful computational scaling.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import math
import time

import numpy as np
import scipy
from scipy.linalg import eigh
import sympy as s

HERE = Path(__file__).resolve().parent
ARCHIVE = Path('/Users/harjas/Downloads/CRAY_environment_energy_research.zip')
PASTE = Path('/Users/harjas/.codex/attachments/fd23bef0-78ec-4d83-b761-24461dcae8eb/Pasted text.txt')


def spin_site(axis: s.Matrix, site: int, count: int) -> s.Matrix:
    return s.kronecker_product(*(axis if k == site else s.eye(2) for k in range(count))) / 2


def spin_pair(i: int, j: int, count: int) -> s.Matrix:
    axes = [s.Matrix([[0, 1], [1, 0]]), s.Matrix([[0, -s.I], [s.I, 0]]), s.diag(1, -1)]
    return sum((spin_site(axis, i, count) * spin_site(axis, j, count) for axis in axes), s.zeros(2**count))


def require_pd(matrix: s.Matrix) -> list[s.Expr]:
    assert matrix == matrix.T
    left, diag = matrix.LDLdecomposition(hermitian=False)
    assert left * diag * left.T == matrix
    pivots = [diag[i, i] for i in range(diag.rows)]
    assert all(x > 0 for x in pivots)
    return pivots


def channel_image(choi: s.Matrix, h: s.Matrix, active: int) -> s.Matrix:
    collar = h.rows // active
    result = s.zeros(h.rows)
    for i in range(active):
        for j in range(active):
            result += s.kronecker_product(
                choi[i*active:(i+1)*active, j*active:(j+1)*active],
                h[i*collar:(i+1)*collar, j*collar:(j+1)*collar])
    return result


def rational_source_checks(h0: s.Matrix, h1: s.Matrix) -> dict:
    with ZipFile(ARCHIVE) as source:
        prefix = 'cray_relative_energy/'
        checksums = source.read(prefix+'SHA256SUMS.txt').decode().splitlines()
        for line in checksums:
            expected, name = line.split('  ', 1)
            assert hashlib.sha256(source.read(prefix+name)).hexdigest() == expected
        assert source.testzip() is None
        record = json.loads(source.read(prefix+'rational_chain_certificate.json'))
        env = json.loads(source.read(prefix+'rational_environment_fixture.json'))
        members = len(source.infolist())
    choi = s.Matrix(record['choi'])
    assert s.Matrix(record['hweak']) == h0
    assert s.Matrix(record['hstrong']) == h1
    partial = s.Matrix(4, 4, lambda a, b: sum(choi[i*4+a, i*4+b] for i in range(4)))
    assert partial == s.eye(4)
    cp = require_pd(choi)
    c = s.Rational(record['lower_reverse'])
    rp = require_pd(h0-channel_image(choi, h1, 4)-c*s.eye(16))
    t = s.Rational(env['t'])
    energies = []
    for tag, h in [('weak', h0), ('strong', h1)]:
        matrix = h+t*spin_pair(2, 3, 4)
        lower = s.Rational(env[tag+'_lower'])
        require_pd(matrix-lower*s.eye(16))
        vec = s.Matrix(env[tag+'_rayleigh_vector'])
        upper = s.cancel((vec.T*matrix*vec)[0]/(vec.T*vec)[0])
        assert upper >= lower
        energies.append((lower, upper))
    lo = s.floor((energies[1][0]-energies[0][1])*10**8)/10**8
    hi = s.ceiling((energies[1][1]-energies[0][0])*10**8)/10**8
    assert lo == s.Rational('-0.22421874') and hi == s.Rational('-0.22421872')
    # A full-Hilbert UCP certificate is not automatically sector preserving.
    charges = [k.bit_count() for k in range(4)]
    allowed = [i*4+a for i in range(4) for a in range(4) if charges[i] == charges[a]]
    forbidden_diag = [choi[k, k] for k in range(16) if k not in allowed]
    assert any(x > 0 for x in forbidden_diag)
    return {'archive_sha256': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
            'archive_bytes': ARCHIVE.stat().st_size, 'archive_members': members,
            'producer_hash_pins_passed': len(checksums), 'zip_crc_passed': True,
            'reconstructed_local_hamiltonians_equal_fixtures': True,
            'choi_unital_exact': True, 'choi_positive_pivots': len(cp),
            'residual_positive_pivots': len(rp),
            'uniform_difference_interval': ['-3/4', '-22421/100000'],
            'counterenvironment_interval_exact': [str(lo), str(hi)],
            'fixed_charge_choi_allowed_dimension': len(allowed),
            'source_choi_forbidden_diagonal_entries': [str(x) for x in forbidden_diag],
            'source_certificate_preserves_active_charge': False}


def fixed_charge_counterexample(h0: s.Matrix, h1: s.Matrix) -> dict:
    sector = [i for i in range(16) if i.bit_count() == 2]
    n2 = s.diag(*[(i >> 1) & 1 for i in range(16)])
    n3 = s.diag(*[i & 1 for i in range(16)])
    k = 100*(2*s.eye(16)-n2-n3)
    a = (h0+k).extract(sector, sector)
    b = (h1+k).extract(sector, sector)
    lower_strong = -s.Rational(9, 97)
    pivots = require_pd(b-lower_strong*s.eye(len(sector)))
    trial = s.zeros(len(sector), 1)
    trial[sector.index(3)] = 1  # |up up down down>
    upper_weak = (trial.T*a*trial)[0]
    assert upper_weak == -s.Rational(1, 4)
    difference_lower = lower_strong-upper_weak
    assert difference_lower == s.Rational(61, 388) and difference_lower > 0
    e0 = eigh(np.asarray(a, dtype=float), eigvals_only=True)[0]
    e1 = eigh(np.asarray(b, dtype=float), eigvals_only=True)[0]
    # Exact minimax upper witnesses for both repaired endpoints.
    singlet = s.Matrix([0, 1/s.sqrt(2), -1/s.sqrt(2), 0])
    c_up = s.Matrix([1, 0, 0, 0])
    embedding = s.kronecker_product(s.eye(4), c_up)
    compressed = embedding.T*h0*embedding
    q1 = [1, 2]
    assert compressed.extract(q1, q1) == spin_pair(0, 1, 2).extract(q1, q1)
    assert min(compressed.extract(q1, q1).eigenvals()) == -s.Rational(3, 4)
    trial_forward = s.kronecker_product(singlet, c_up)
    h1_trial = (trial_forward.T*h1*trial_forward)[0]
    assert h1_trial == -s.Rational(3, 2)
    minimax_forward = h1_trial+s.Rational(3, 4)
    assert minimax_forward == -s.Rational(3, 4)
    reverse_trial = s.zeros(16, 1)
    reverse_trial[3] = 1
    minimax_reverse = (reverse_trial.T*(h0-h1)*reverse_trial)[0]
    assert minimax_reverse == -s.Rational(1, 4)
    # The source's simple covariant channel explicitly transfers charge.
    ps = singlet*singlet.T
    pt = s.eye(4)-ps
    k0 = ps+pt/2
    projector_q0 = s.diag(1, 0, 0, 0)
    phi_q0 = k0*projector_q0*k0+s.Rational(3, 4)*pt*(singlet.T*projector_q0*singlet)[0]
    assert phi_q0 == projector_q0/4 and phi_q0 != projector_q0
    counts = []
    for variables in [2, 4, 6, 8, 10]:
        block = sum(math.comb(variables, q)**2 for q in range(variables+1))
        assert block == math.comb(2*variables, variables)
        counts.append({'variables': variables, 'strong_charge_choi_dimension': block,
                       'choi_entries': block**2, 'unrestricted_entries': 16**variables})
    return {'sector': 'four spins, two down spins, no additional R',
            'common_environment': '100*(2*I-N2-N3)', 'sector_dimension': len(sector),
            'strong_energy_lower_exact': str(lower_strong),
            'weak_energy_upper_exact': str(upper_weak),
            'certified_difference_lower_exact': str(difference_lower),
            'strong_shift_positive_pivots': len(pivots),
            'difference_floating_diagnostic': float(e1-e0),
            'strong_charge_sharp_forward_L_exact': str(minimax_forward),
            'strong_charge_sharp_reverse_L_exact': str(minimax_reverse),
            'closure_interval_exact': ['-3/4', '1/4'],
            'simple_source_channel_phi_Pq0_equals_Pq0_over_4': True,
            'choi_resource_counts': counts}


def grouped_reachability_diagnostics(trials: int = 20) -> dict:
    """Start with arbitrary full-rank total-Q mixed states, derive their channels.

    Unlike sampling a charge-preserving channel first, this exercises the
    converse construction from an independently generated compatible state.
    Cross-active-charge coherences within total Q are retained.
    """
    rng = np.random.default_rng(132026)
    charges = np.array([0, 1, 1, 2])
    qa, qb = charges[:, None], charges[None, :]
    sector = np.flatnonzero((qa+qb).ravel() == 2)
    max_errors = Counter()
    for _ in range(trials):
        raw = rng.normal(size=(6, 6))+1j*rng.normal(size=(6, 6))
        mixed = raw@raw.conj().T
        mixed /= np.trace(mixed)
        omega = np.zeros((16, 16), complex)
        omega[np.ix_(sector, sector)] = mixed
        sigma = np.einsum('abad->bd', omega.reshape(4, 4, 4, 4))
        vals, vecs = eigh(mixed)
        phi = np.zeros((16, 6), complex)
        phi[sector] = vecs*np.sqrt(vals)[None, :]
        phi = phi.reshape(4, 4, 6)
        psi = np.zeros((4, 4), complex)
        w = np.zeros((4, 6, 4), complex)
        for charge in [0, 1, 2]:
            active_ix = np.flatnonzero(charges == charge)
            remote_ix = np.flatnonzero(charges == 2-charge)
            sv, su = eigh(sigma[np.ix_(remote_ix, remote_ix)])
            assert np.min(sv) > 0
            for ix, value, vec in zip(active_ix, sv, su.T):
                psi[ix, remote_ix] = np.sqrt(value)*vec
                w[:, :, ix] = np.einsum('b,abe->ae', vec.conj(), phi[:, remote_ix, :])/np.sqrt(value)
        kraus = [w[:, e, :] for e in range(6)]
        unital = sum(k.conj().T@k for k in kraus)
        recovered = sum(np.outer((k@psi).ravel(), (k@psi).ravel().conj()) for k in kraus)
        errors = {'normalization': np.max(np.abs(unital-np.eye(4))),
                  'state_recovery': np.max(np.abs(recovered-omega)),
                  'charge_commutator': max(np.max(np.abs(k*charges[None, :]-charges[:, None]*k)) for k in kraus),
                  'purification_marginal': np.max(np.abs(psi.T@psi.conj()-sigma)),
                  'fixed_sector_purification_leakage': np.linalg.norm(psi[(qa+qb) != 2])}
        assert max(errors.values()) < 2e-12
        for name, error in errors.items():
            max_errors[name] = max(max_errors[name], float(error))
    return {'scope': 'finite floating check of grouped fixed-marginal reachability, not universal proof',
            'seed': 132026, 'trials': trials, 'max_errors': dict(max_errors)}


def main() -> None:
    start = time.perf_counter()
    h0 = spin_pair(0, 1, 4)+spin_pair(0, 2, 4)+spin_pair(1, 3, 4)
    h1 = h0+spin_pair(0, 1, 4)
    result = {'scientific_status': 'internally reconstructed and finite-tested; external correctness and novelty UNKNOWN',
              'source_paste_sha256': hashlib.sha256(PASTE.read_bytes()).hexdigest(),
              'runtime_versions': {'numpy': np.__version__, 'scipy': scipy.__version__, 'sympy': s.__version__},
              'source_exact_checks': rational_source_checks(h0, h1),
              'fixed_charge_counterexample': fixed_charge_counterexample(h0, h1),
              'grouped_reachability': grouped_reachability_diagnostics(),
              'elapsed_seconds': time.perf_counter()-start}
    (HERE/'independent_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
