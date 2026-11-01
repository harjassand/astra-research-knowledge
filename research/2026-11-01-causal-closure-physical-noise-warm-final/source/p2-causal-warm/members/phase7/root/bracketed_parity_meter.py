"""Finite two-mode parity meter with arbitrary initial quantum memory.

The storage a and readout m obey
 H=g(t)(a^dag m+m^dag a)+chi(t) Z1 n_a+u(t) Z2(a+a^dag).
The readout outlet is sqrt(Gamma)m and intrinsic storage loss sqrt(ka)a.
Readout and mapping controls have disjoint supports. Mapping uses
 integral chi=pi and u=lambda*chi*exp(-ka*t/2), including finite ramps.
The selected temporal output mode is orthogonal to BOTH initial-mode
response columns over the full pre/map/post record.

All numerical values are dimensionless in units g_max=1 unless changed.
The exact all-state identity and repeated-use conditions are in the report.
This script does NOT simulate or assert a complete logical error rate.
"""
from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path
import json
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp, quad
from scipy.optimize import minimize
from scipy.special import ndtr, ndtri


@dataclass(frozen=True)
class Model:
    g: float = 1.0
    Gamma: float = 4.0
    chi: float = 2.0
    ka: float = 1e-4
    ramp_g: float = 0.1
    ramp_chi: float = 0.1
    eta: float = 0.5
    q: float = 0.001
    drive_cap: float = 3.0

    @property
    def mapping_time(self):
        return np.pi / self.chi + self.ramp_chi

    @property
    def target_N(self):
        return ndtri(self.q)**2 / (4*self.eta)

    @property
    def lambda_cap(self):
        # A conservative cap: exponential damping only lowers peak |u|.
        return self.drive_cap/self.chi


def envelope(t, duration, ramp):
    """C1 compact pulse with a flat center and sin^2 endpoint ramps."""
    t = np.asarray(t)
    if ramp == 0:
        return np.ones_like(t)
    if duration < 2*ramp:
        raise ValueError('A pulse must have room for its two finite ramps.')
    ans = np.ones_like(t, dtype=float)
    left = t < ramp
    right = t > duration-ramp
    ans[left] = np.sin(np.pi*t[left]/(2*ramp))**2
    ans[right] = np.sin(np.pi*(duration-t[right])/(2*ramp))**2
    return ans


def mapping_theta(t, model):
    """Integral of the finite-ramp chi pulse, exactly ending at pi."""
    t = np.asarray(t)
    T, r = model.mapping_time, model.ramp_chi
    if r == 0:
        return model.chi*t
    left = model.chi*(t/2-r*np.sin(np.pi*t/r)/(2*np.pi))
    middle = model.chi*(t-r/2)
    end = np.pi-model.chi*((T-t)/2-r*np.sin(np.pi*(T-t)/r)/(2*np.pi))
    return np.where(t < r, left, np.where(t > T-r, end, middle))


@lru_cache(maxsize=256)
def readout_fundamental(duration, model):
    if duration == 0:
        return lambda t: np.tile(np.eye(2, dtype=complex).ravel()[:, None],
                                 (1, np.asarray(t).size))
    def rhs(t, y):
        g = model.g*float(envelope(t, duration, model.ramp_g))
        A = np.array([[-model.ka/2, -1j*g], [-1j*g, -model.Gamma/2]])
        return (A@y.reshape(2, 2)).ravel()
    sol = solve_ivp(rhs, [0, duration], np.eye(2, dtype=complex).ravel(),
                    dense_output=True, method='DOP853', rtol=1e-11,
                    atol=3e-13, max_step=max(duration/25, 0.01))
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.sol


def nodes(duration, order=180):
    x, w = leggauss(order)
    return duration*(1+x)/2, duration*w/2


def fundamental_values(sol, t):
    return np.moveaxis(sol(t).reshape(2, 2, -1), -1, 0)


def compute(pre, post, lam, model=Model(), order=180, arrays=False):
    T = model.mapping_time
    pre_sol, post_sol = readout_fundamental(float(pre), model), readout_fundamental(float(post), model)
    Epre = fundamental_values(pre_sol, np.array([pre]))[0]
    Epost = fundamental_values(post_sol, np.array([post]))[0]
    D = np.diag([-np.exp(-model.ka*T/2), np.exp(-model.Gamma*T/2)])
    d = -2*lam*np.exp(-model.ka*T/2)
    tp, wp = nodes(pre, order)
    tm, wm = nodes(T, order)
    tq, wq = nodes(post, order)
    Fpre = fundamental_values(pre_sol, tp)
    Fpost = fundamental_values(post_sol, tq)
    Hpre = np.sqrt(model.Gamma)*Fpre[:, 1, :]
    Hmap = np.sqrt(model.Gamma)*np.exp(-model.Gamma*tm[:, None]/2)*Epre[1, :]
    Hpost = np.sqrt(model.Gamma)*(Fpost@D@Epre)[:, 1, :]
    hpost = np.sqrt(model.Gamma)*Fpost[:, 1, 0]*d
    H = np.concatenate([Hpre, Hmap, Hpost])
    h = np.concatenate([np.zeros_like(tp, complex), np.zeros_like(tm, complex), hpost])
    w = np.concatenate([wp, wm, wq])
    Gram = H.conj().T@(w[:, None]*H)
    cross = H.conj().T@(w*h)
    coeff = np.linalg.pinv(Gram, rcond=1e-12)@cross
    rejected = H@coeff
    clean = h-rejected
    Neff = float(np.real(np.vdot(clean, w*clean)))
    Nmain = float(np.real(np.vdot(h, w*h)))
    f = clean/np.sqrt(Neff) if Neff > 1e-24 else np.zeros_like(clean)
    null_residual = float(np.max(abs(f.conj()@(w[:, None]*H))))
    K = Epost@D@Epre
    dfinal = Epost[:, 0]*d
    k = float(np.linalg.norm(K, 2))
    B = 0.0
    B_tail_bound = 0.0
    vk = dfinal.copy()
    for j in range(10000):
        term = float(np.linalg.norm(vk))
        B += term
        if term < 1e-14:
            B_tail_bound = k*term/(1-k)
            break
        vk = K@vk
    B += B_tail_bound
    # Homogeneous contraction robust to arbitrary sign rotations while
    # mapping: replace D by ANY norm<=1 storage rotation/attenuation.
    k_robust = float(np.linalg.norm(Epost, 2)*np.linalg.norm(Epre, 2))
    tgrid = np.linspace(0, T, 4001)
    chi = model.chi*envelope(tgrid, T, model.ramp_chi)
    u = lam*chi*np.exp(-model.ka*tgrid/2)
    theta = mapping_theta(tgrid, model)
    # Exact overlap for same parity, including ALL mapping loss photons.
    # F(beta)=exp(i*2*lambda^2*Kphase)*exp(-C*|beta+lambda|^2).
    reC = quad(lambda t: model.ka*np.exp(-model.ka*t)*(1-np.cos(2*float(mapping_theta(t, model)))),
               0, T, epsabs=1e-13, points=[model.ramp_chi, T-model.ramp_chi])[0]
    imC = quad(lambda t: model.ka*np.exp(-model.ka*t)*np.sin(2*float(mapping_theta(t, model))),
               0, T, epsabs=1e-13, points=[model.ramp_chi, T-model.ramp_chi])[0]
    Kphase = quad(lambda t: model.chi*float(envelope(t, T, model.ramp_chi))*np.exp(-model.ka*t),
                  0, T, epsabs=1e-12, points=[model.ramp_chi, T-model.ramp_chi])[0]
    C = reC+1j*imC
    thermal = []
    pre_a_survival = float(np.sum(abs(Epre[0, :])**2))
    for n0 in [0., .001, .01, .1, 1., 10.]:
        nmap = n0*pre_a_survival
        F = np.exp(1j*2*lam**2*Kphase)/(1+nmap*C)*np.exp(-C*lam**2/(1+nmap*C))
        thermal.append(dict(initial_nbar_each_mode=n0, mapping_nbar=nmap,
                            visibility=float(abs(F)), pZ_after_known_phase=(1-float(abs(F)))/2,
                            relative_phase=float(np.angle(F))))
    q = float(ndtr(-2*np.sqrt(model.eta*max(0., Neff))))
    gamma = np.exp(-2*Neff)/2
    e = q+gamma**2/q if q > 0 else 0.
    ans = dict(model=asdict(model), pre=pre, post=post, mapping_time=T,
               total_time=pre+T+post, lam=lam, displacement=d,
               target_N=model.target_N, N_selected=Neff, N_main=Nmain,
               retained_signal_fraction=Neff/Nmain if Nmain else 0.,
               assignment_error=q, selected_pointer_CP_bad_weight=e,
               initial_mode_null_residual=null_residual,
               initial_mode_Gram_eigenvalues=np.linalg.eigvalsh(Gram).tolist(),
               peak_drive=float(np.max(abs(u))),
               peak_chi=model.chi, peak_g=model.g,
               max_drive_slew=float(np.max(abs(np.gradient(u, tgrid)))),
               finite_ramp_max_g_slew=model.g*np.pi/(2*model.ramp_g) if model.ramp_g else None,
               map_chi_area=float(mapping_theta(T, model)),
               total_homogeneous_contraction=k,
               robust_sign_history_contraction=k_robust,
               final_displacement_norm=float(np.linalg.norm(dfinal)),
               nominal_boundary_energy_bound_from_bounded_parity_history=B**2,
               nominal_energy_series_added_tail_bound=B_tail_bound,
               loose_boundary_energy_bound=(np.linalg.norm(dfinal)/(1-k))**2,
               initial_thermal_storage_survival_before_map=pre_a_survival,
               map_overlap_C_real=float(reC), map_overlap_C_imag=float(imC),
               map_phase_K=float(Kphase), thermal_cases=thermal,
               homogeneous_matrix_real=K.real.tolist(), homogeneous_matrix_imag=K.imag.tolist(),
               final_displacement_real=dfinal.real.tolist(), final_displacement_imag=dfinal.imag.tolist())
    if arrays:
        return ans, dict(t=np.concatenate([tp, pre+tm, pre+T+tq]), weights=w,
                         initial_response=H, parity_signal=h, receiver=f,
                         Epre=Epre, Epost=Epost, K=K)
    return ans


def optimize_duration(model=Model(), start=(2., 2.), order=120):
    def constraint(x):
        return compute(float(x[0]), float(x[1]), model.lambda_cap, model, order)['N_selected']-model.target_N
    res = minimize(lambda x: float(x.sum()), np.array(start), method='SLSQP',
                   bounds=[(max(0.21, 2*model.ramp_g), 12.)]*2,
                   constraints={'type':'ineq', 'fun':constraint},
                   options={'ftol':2e-8, 'maxiter':80, 'eps':1e-4})
    row = compute(float(res.x[0]), float(res.x[1]), model.lambda_cap, model, 500)
    row['optimization_success'] = bool(res.success)
    row['optimization_message'] = str(res.message)
    row['optimization_iterations'] = int(res.nit)
    return row


def main():
    model = Model()
    rows = []
    for tau in [1., 1.5, 2., 3., 4.]:
        row = compute(tau, tau, model.lambda_cap, model, 350)
        rows.append(row)
        print('symmetric', tau, 'T', row['total_time'], 'N_eff', row['N_selected'],
              'q', row['assignment_error'], 'cold_pZ', row['thermal_cases'][0]['pZ_after_known_phase'], flush=True)
    optimum = optimize_duration(model)
    # No pre-observation: even a bright post signal belongs to the unknown
    # initial-storage response. Removing it annihilates all useful signal.
    post_only = compute(0., 3., model.lambda_cap, model, 450)
    # Finite quadrature/ODE checks of the actual receiver, not only an ideal
    # direct Markov replacement. Additional higher-order integration at the
    # optimum resolves the only material numerical risk here.
    refined = compute(optimum['pre'], optimum['post'], model.lambda_cap, model, 800)
    out = dict(description=__doc__, symmetric_cases=rows, duration_optimized=optimum,
               post_only_counterexample=post_only,
               refinement_N_selected_difference=refined['N_selected']-optimum['N_selected'],
               refinement_null_residual=refined['initial_mode_null_residual'])
    path = Path(__file__).with_name('bracketed_parity_results.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print('OPTIMUM', json.dumps(optimum, indent=2), flush=True)
    print('POST_ONLY_N', post_only['N_selected'], 'REFINEMENT', out['refinement_N_selected_difference'], flush=True)


if __name__ == '__main__':
    main()
