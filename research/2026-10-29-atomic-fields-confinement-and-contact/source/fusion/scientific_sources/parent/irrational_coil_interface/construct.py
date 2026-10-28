"""Finite equipotential coils for the explicit irrational vacuum tube.

Established Maxwell current-potential construction; finite numerical realization,
not a uniform field, magnetic topology, particle or conductor certificate.
"""
from pathlib import Path
import sys, json, time, hashlib
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parents[1] / 'fusion_confinement_bridge' / 'sengupta_paraboloid.py'
raw = SOURCE.read_bytes()
(ROOT / 'runtime' / SOURCE.name).write_bytes(raw)
sys.path.insert(0, str(ROOT.parents[1] / 'positive_current_operation' / 'vendor'))
sys.path.insert(0, str(ROOT / 'runtime'))
import numpy as np
from scipy.interpolate import CubicSpline
import sengupta_paraboloid as s


def surface(theta, zeta, shift):
    """Vectorized bracket/bisection; keeps source radial parameterization."""
    theta, zeta = np.broadcast_arrays(theta, zeta)
    lo = np.zeros(theta.shape)
    hi = np.full(theta.shape, .731 / s.KAPPA)
    def q(r):
        return np.stack((s.U0 + r*np.cos(theta), r*np.sin(theta), zeta), axis=-1)
    assert np.all(s.surface_label(q(hi)) - s.PSI0 >= shift)
    for _ in range(45):
        mid = (lo + hi)/2
        less = s.surface_label(q(mid)) - s.PSI0 < shift
        lo = np.where(less, mid, lo)
        hi = np.where(less, hi, mid)
    out = q((lo+hi)/2)
    assert np.all(s.regular(out))
    return out


def potential_phase(q):
    """Unwrap along last coordinate axis (zeta), with alpha(zeta=0)=0.

    Each log contributes a phase. Their sum divided by two is the circle
    coordinate alpha=2*pi*Phi/C for C=4*pi/(kappa*k).
    """
    u, v, z = np.moveaxis(q, -1, 0)
    _, c1, d1 = s.complex_jacobi(s.K+s.KAPPA*(u-s.U0)+1j*s.KAPPA*z)
    _, c2, d2 = s.complex_jacobi(s.K+s.KAPPA*v+1j*(s.KP+s.KAPPA*z))
    a1 = np.unwrap(np.angle(d1-s.KMOD*c1), axis=-1)
    a2 = np.unwrap(np.angle(d2-s.KMOD*c2), axis=-1)
    alpha = (a1+a2)/2
    return alpha-alpha[..., :1]


def coils(N, M=256, Z=2048, shift=.25, offset=.5):
    theta = np.arange(M+1)*2*np.pi/M
    zeta = np.arange(Z+1)*2*np.pi/Z
    q = surface(theta[:, None], zeta[None, :], shift)
    alpha = potential_phase(q)
    assert np.min(np.diff(alpha, axis=-1)) > 0
    assert np.max(abs(alpha[:, -1]-2*np.pi)) < 1e-10
    phases = 2*np.pi*(np.arange(N)+offset)/N
    zz = np.stack([CubicSpline(al, z)(phases) for al, z in zip(alpha, q[..., 2])])
    qq = surface(theta[:, None], zz, shift)
    xx = s.embedding(qq)
    assert np.max(abs(xx[-1]-xx[0])) < 1e-11
    xx[-1] = xx[0]
    # det(X_u,X_v,X_zeta)<0: increasing theta is the opposite current
    # direction to K=-n_out x B/mu0. The first run retained in
    # INITIAL_ORIENTATION_FAILURE.json used +theta and produced -B.
    wave_numbers = np.fft.fftfreq(M, 1/M)
    tangent = -np.fft.ifft(1j*wave_numbers[:, None, None]*np.fft.fft(xx[:-1], axis=0), axis=0).real
    residual = np.max(abs(s.surface_label(qq)-s.PSI0-shift))
    source_field = s.data(qq[:-1])['B']
    tangency = np.abs(np.einsum('...i,...i->...', source_field, tangent))/(np.linalg.norm(source_field, axis=-1)*np.linalg.norm(tangent, axis=-1))
    circ = 4*np.pi/(s.KAPPA*s.KMOD)
    lengths = np.mean(np.linalg.norm(tangent, axis=-1), axis=0)*2*np.pi
    return xx[:-1], tangent, {
        'N_coils': N, 'M_loop_nodes': M, 'Z_phase_nodes': Z,
        'shift': shift, 'potential_circulation': float(circ),
        'max_surface_label_residual': float(residual),
        'minimum_phase_grid_derivative': float(np.min(np.diff(alpha, axis=-1))/(2*np.pi/Z)),
        'max_phase_period_residual': float(np.max(abs(alpha[:, -1]-2*np.pi))),
        'max_equipotential_tangency_residual': float(tangency.max()),
        'coil_length_min': float(lengths.min()), 'coil_length_max': float(lengths.max()),
        'total_coil_length': float(lengths.sum()),
        'loop_current_per_Bstar_Lstar_over_mu0': float(circ/N),
        'source_code_sha256': hashlib.sha256(raw).hexdigest()
    }


def coil_field(targets, xx, tangent):
    M, N = xx.shape[:2]
    current = (4*np.pi/(s.KAPPA*s.KMOD))/N
    nodes, dl = xx.reshape(-1, 3), tangent.reshape(-1, 3)
    out = []
    for first in range(0, len(targets), 6):
        rr = targets[first:first+6, None, :] - nodes[None, :, :]
        r2 = np.einsum('...i,...i->...', rr, rr)
        out.append(np.sum(np.cross(dl[None], rr)/r2[..., None]**1.5, axis=1)*current/(2*M))
    return np.concatenate(out)


def targets():
    # Distinct noncommensurate phases; no shared training/coil grid nodes.
    rows, qs = [], []
    for shift in (0., .025, .1):
        th = 2*np.pi*(np.arange(12)+.217)/12 if shift else [0.]
        for theta in th:
            zz = 2*np.pi*(np.arange(29)+.319)/29
            q = surface(theta, zz, shift) if shift else np.stack((np.full(29, s.U0), np.zeros(29), zz), axis=-1)
            qs.extend(q)
            rows.extend([[shift, float(theta), float(z)] for z in zz])
    return np.array(rows), np.array(qs)


def main():
    started = time.monotonic()
    labels, q = targets()
    cart = s.embedding(q)
    exact = s.data(q)['B']
    norm = np.linalg.norm(exact, axis=-1)
    rows = []
    old = None
    for N, M, Z in [(32, 128, 512), (64, 256, 1024), (128, 256, 1024), (128, 512, 2048), (256, 512, 2048)]:
        t = time.monotonic()
        xx, tangent, meta = coils(N, M, Z)
        finite = coil_field(cart, xx, tangent)
        error = np.linalg.norm(finite-exact, axis=-1)/norm
        meta.update(max_sample_relative_field_error=float(error.max()),
            rms_sample_relative_field_error=float(np.sqrt(np.mean(error**2))),
            max_error_by_shift={str(shift):float(error[labels[:, 0]==shift].max()) for shift in (0., .025, .1)},
            seconds=time.monotonic()-t)
        if old is not None and N==old[0]:
            meta['same_N_discretization_change']=float(np.max(np.linalg.norm(finite-old[1], axis=-1)/norm))
        rows.append(meta)
        old=N,finite
        print(json.dumps(meta), flush=True)
        (ROOT/'RESULTS.json').write_text(json.dumps({'status':'FINITE_COIL_CONSTRUCTION_IN_PROGRESS',
            'target_count':len(q), 'rows':rows, 'seconds':time.monotonic()-started}, indent=2)+'\n')
    np.savez_compressed(ROOT/'finite_coils.npz', nodes=xx, tangents=tangent,
        target_labels=labels, target_coordinates=q, exact_field=exact, finite_field=finite)
    (ROOT/'RESULTS.json').write_text(json.dumps({'status':'FINITE_SAMPLED_COIL_INTERFACE',
        'target_count':len(q), 'rows':rows, 'seconds':time.monotonic()-started,
        'scope':'Source current-potential construction. Finite coils and sampled field comparison only. No uniform field/error enclosure, topological/particle certificate, optimized-coil advantage, finite-wire engineering, or physical device.'}, indent=2)+'\n')


if __name__=='__main__':
    main()
