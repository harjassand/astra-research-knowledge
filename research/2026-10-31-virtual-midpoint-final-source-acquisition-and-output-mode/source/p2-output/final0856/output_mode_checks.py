"""Dirty-receiver readout with a positive quantum-controlled force.

Ordinary floating-point checks supplement the analytic proof. No hardware
performance, interval arithmetic, or arbitrary-source spectral calibration
is inferred from these examples.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.special import ndtr
from scipy.optimize import minimize


def integral_exp(z, time):
    return -np.expm1(-z*time)/z


def resonant_filter(kappa, time):
    a = kappa/2
    z = np.exp(-a*time)
    V = time-2/a*np.tanh(a*time/2)

    def w(t):
        return (1-2*np.exp(-a*t)/(1+z))/np.sqrt(V)

    def kernel(t):
        u = np.exp(-a*t)
        return (1-u)*(u-z)/(a*(1+z)*u*np.sqrt(V))

    return w, kernel, V


def two_pole_filter(kappa, delta, time):
    """Real filter removes both initial quadratures at poles a +/- i delta."""
    a = kappa/2
    lam = a+1j*delta
    ie = integral_exp(lam, time)
    ie2 = integral_exp(2*lam, time)
    ireal = integral_exp(2*a, time)
    gram = np.array([[(ireal+ie2.real)/2, -ie2.imag/2],
                     [-ie2.imag/2, (ireal-ie2.real)/2]])
    rhs = np.array([ie.real, -ie.imag])
    cc, cs = np.linalg.solve(gram, rhs)
    V = time-rhs@np.array([cc, cs])
    assert V > 0
    d = -.5*(cc+1j*cs)

    def w(t):
        return (1+2*np.real(d*np.exp(-lam*t)))/np.sqrt(V)

    def kernel(t):
        remaining = time-t
        val = (integral_exp(lam, remaining)
               +d*np.exp(-lam*t)*integral_exp(2*lam, remaining)
               +d.conjugate()*np.exp(-lam.conjugate()*t)
               *integral_exp(2*a, remaining))
        return val/np.sqrt(V)

    return w, kernel, V, float(np.linalg.cond(gram))


def uniform_quantum_source_effect(kernel, kappa, time, gain_lo, gain_hi, omega):
    """Wrong-output effect for an arbitrary qubit source, not one chosen state.

    In a canonical pointer q representation, the sequence alternates exact
    source-only rotations with force translations of positive source gain.
    It is a finite product approximation to the continuous source dynamics.
    The lower integrated velocity is valid for the finite product itself.
    """
    nq, qlength, steps = 4096, 160., 1000
    dq = qlength/nq
    q = (np.arange(nq)-nq/2)*dq
    p = np.fft.fftshift(np.fft.fftfreq(nq, d=dq))*2*np.pi
    dp = p[1]-p[0]
    psi = np.pi**(-.25)*np.exp(-q*q/2)
    U = np.broadcast_to(np.eye(2, dtype=complex), (nq, 2, 2)).copy()
    dt = time/steps
    X = np.array([[0., 1.], [1., 0.]])
    half = expm(-.5j*omega*X*dt)
    gains = np.array([gain_lo, gain_hi])
    lower_shift = 0.
    for j in range(steps):
        beta = float(np.real(kernel((j+.5)*dt)))
        impulse = np.sqrt(2*kappa)*beta*dt
        lower_shift += impulse*(gain_lo if impulse >= 0 else gain_hi)
        U = np.einsum("ab,pbc->pac", half, U)
        U *= np.exp(-1j*q[:, None]*gains[None, :]*impulse)[:, :, None]
        U = np.einsum("ab,pbc->pac", half, U)
    K = (dq/np.sqrt(2*np.pi)
         *np.fft.fftshift(np.fft.fft(np.fft.ifftshift(
             psi[:, None, None]*U, axes=0), axis=0), axes=0))
    effects = np.einsum("pki,pkj->pij", K.conjugate(), K)
    complete = dp*np.sum(effects, axis=0)
    weights = (p > 0).astype(float)+.5*(p == 0)
    wrong = dp*np.einsum("p,pij->ij", weights, effects)
    max_wrong = float(np.linalg.eigvalsh(wrong)[-1])
    mu = np.sqrt(2)*lower_shift
    bound = float(ndtr(-mu))
    completeness_error = float(np.linalg.norm(complete-np.eye(2), 2))
    assert completeness_error < 3e-10
    # The p-grid quadrature uses a half-weight at zero, with finite resolution.
    assert max_wrong <= bound+3e-5
    return {"source_H_frequency": omega,
            "force_source_commutator_norm": abs(omega*(gain_hi-gain_lo)),
            "minimum_normalized_shift": mu,
            "uniform_tail_bound": bound,
            "largest_wrong_effect_eigenvalue": max_wrong,
            "complete_effect_residual": completeness_error,
            "pointer_grid_spacing": float(dp),
            "scope": "Operator-valued effect over the entire source input; floating-point and quadrature diagnostic."}


def coarse_linewidth_witness(target):
    """Feasible coarse-calibration schedule; no certified duration optimum."""
    km, kp, gm, E, variance = .8, 1.2, .3, 10., 1.
    VE = 2*E+1+2*np.sqrt(E*(E+1))

    def bound(x):
        delay, length, fraction = x
        mu = 4*gm*np.sqrt(length/kp)*(1-2*np.exp(-km*delay/2)/(km*length))
        if mu <= 0 or not 0 < fraction < 1:
            return 1., mu, 1.
        r = fraction*mu
        residue2 = 4*np.exp(-km*delay)/(km*length)
        p = ndtr(-(mu-r)/np.sqrt(variance))+residue2*VE/r**2
        return float(p), float(mu), float(residue2)

    # Closed-form feasible start: L>=4/km implies mu>=2*gm*sqrt(L/kp).
    L = max(4/km, 2*kp*variance/gm**2*np.log(1/target))
    delay = max(0., np.log(8*kp*VE/(target*km*gm**2*L**2))/km)
    initial = np.array([delay, L, .5])
    constraint = {"type":"ineq", "fun":lambda x: np.log(target)-np.log(max(bound(x)[0],1e-300))}
    opt = minimize(lambda x:x[0]+x[1], initial, method="SLSQP",
                   bounds=[(0.,None),(4/km,None),(.001,.999)],
                   constraints=[constraint], options={"ftol":1e-11,"maxiter":500})
    x = opt.x if opt.success and bound(opt.x)[0] <= target*(1+2e-8) else initial
    p, mu, residue2 = bound(x)
    assert p <= target*(1+2e-8)
    return {"target_label_bound":target,"linewidth_interval":[km,kp],
            "gain_interval":[gm,.5],"initial_mean_occupation_bound":E,
            "discarded_interval":float(x[0]),"integrated_interval":float(x[1]),
            "complete_duration":float(x[0]+x[1]),"union_threshold_fraction":float(x[2]),
            "minimum_shift":mu,"startup_coefficient_squared_bound":residue2,
            "proved_label_bound_at_witness":p,"instrument_half_distance_bound":p+np.sqrt(p),
            "scope":"Coarse static linewidth; fresh vacuum; finite initial energy; complete waiting time charged. Floating-point feasible witness, not certified optimum."}


def interacting_receiver_check(time):
    """Real common filter and positive quantum gain for a two-mode receiver."""
    K = np.array([[0.,.35],[.35,.7]])
    C = np.array([[1.,0.]], dtype=complex)
    A = -1j*K-C.conjugate().T@C/2
    ell = np.array([0.,1.], dtype=complex)
    eigenvalues, vectors = np.linalg.eig(A)
    inverse = np.linalg.inv(vectors)

    def propagator(t):
        return vectors@np.diag(np.exp(eigenvalues*t))@inverse

    nodes, weights = np.polynomial.legendre.leggauss(500)
    times, dt = (nodes+1)*time/2, weights*time/2
    def f(t):
        h=(C@propagator(t))[0]
        return np.concatenate([h.real,h.imag])
    F=np.array([f(t) for t in times])
    gram=F.T@(dt[:,None]*F)
    rhs=F.T@dt
    coefficients=np.linalg.solve(gram,rhs)
    V=time-rhs@coefficients
    def w(t): return (1-f(t)@coefficients)/np.sqrt(V)
    ws=np.array([w(t) for t in times])
    residual=ws@(dt[:,None]*np.array([(C@propagator(t))[0] for t in times]))
    z=complex((-ell.conjugate()@np.linalg.solve(A.conjugate().T,C.conjugate().T)).item())
    phase=np.angle(z)
    chi=abs(z)
    from scipy.integrate import solve_ivp
    def ode(t,k):
        return -A.conjugate().T@k-w(t)*np.exp(-1j*phase)*C.conjugate().ravel()
    sol=solve_ivp(ode,[time,0.],np.zeros(2,dtype=complex),rtol=2e-10,atol=2e-12,dense_output=True)
    assert sol.success
    def beta(t): return float(np.real(ell.conjugate()@sol.sol(t)))
    total=quad(beta,0,time,epsabs=1e-8,limit=300)[0]
    negative=quad(lambda t:max(-beta(t),0),0,time,epsabs=1e-8,limit=500)[0]
    mu=2*(.3*total-(.5-.3)*negative)
    assert np.linalg.norm(residual)<1e-9
    assert abs(total-chi*np.sqrt(V))<3e-7
    assert abs(np.sum(dt*ws**2)-1)<1e-9
    return {"T":time,"mode_count":2,"decay_eigenvalues":[[float(z.real),float(z.imag)] for z in eigenvalues],
            "real_filter_nuisance_rank":4,"gram_condition_number":float(np.linalg.cond(gram)),
            "initial_mode_coefficient_norm":float(np.linalg.norm(residual)),"effective_time_V":float(V),
            "positive_DC_response":chi,"signed_kernel_integral":total,"negative_kernel_area":negative,
            "gain_interval":[.3,.5],"guaranteed_shift":mu,
            "vacuum_label_error_bound":float(ndtr(-mu)) if mu>0 else None}


def main():
    results = {}
    kappa, time = 1., 8.
    w, kernel, V = resonant_filter(kappa, time)
    normalization = quad(lambda t: w(t)**2, 0, time, epsabs=1e-12)[0]
    startup = quad(lambda t: w(t)*np.exp(-kappa*t/2), 0, time, epsabs=1e-12)[0]
    response = quad(kernel, 0, time, epsabs=1e-12)[0]
    minimum_kernel = min(kernel(t) for t in np.linspace(0, time, 1001))
    # The input temporal mode is h(s)=w(s)-kappa*k(s)=-w(T-s).
    reflected = max(abs(w(t)-kappa*kernel(t)+w(time-t))
                    for t in np.linspace(0, time, 1001))
    assert abs(normalization-1) < 1e-12
    assert abs(startup) < 1e-12
    assert minimum_kernel >= -1e-12
    assert abs(response-2*np.sqrt(V)/kappa) < 1e-12
    assert reflected < 1e-12
    results["exact_mode_identities"] = {
        "kappa": kappa, "T": time, "effective_time_V": V,
        "normalization": normalization, "initial_mode_coefficient": startup,
        "minimum_response_kernel": minimum_kernel,
        "input_mode_reflection_residual": reflected}
    results["quantum_gain"] = [
        uniform_quantum_source_effect(kernel, kappa, time, .3, .9, omega)
        for omega in [0., 4., 40., 200.]]

    pole_rows = []
    for T in [8., 20., 40., 80.]:
        wp, kp, Vp, condition = two_pole_filter(1., .0625, T)
        residual_real = quad(lambda t: wp(t)*np.exp(-t/2)*np.cos(.0625*t),
                             0, T, epsabs=1e-12)[0]
        residual_imag = quad(lambda t: wp(t)*np.exp(-t/2)*np.sin(.0625*t),
                             0, T, epsabs=1e-12)[0]
        neg = quad(lambda t: max(-kp(t).real, 0), 0, T,
                   epsabs=2e-11, limit=300)[0]
        total = quad(lambda t: kp(t).real, 0, T, epsabs=1e-12)[0]
        expected = (.5/(.5**2+.0625**2))*np.sqrt(Vp)
        assert abs(total-expected) < 2e-10
        assert max(abs(residual_real), abs(residual_imag)) < 2e-11
        # 0.3 <= G <= 0.5; this bound allows arbitrary source time dependence.
        mu = 2*(.3*total-(.5-.3)*neg)
        pole_rows.append({"T": T, "delta_over_kappa": .0625,
                          "gain_interval": [.3, .5], "effective_time_V": Vp,
                          "gram_condition_number": condition,
                          "startup_residual": max(abs(residual_real), abs(residual_imag)),
                          "negative_kernel_area": neg, "total_kernel_area": total,
                          "guaranteed_shift": mu,
                          "vacuum_label_error_bound": float(ndtr(-mu))})
    results["known_dispersive_poles"] = pole_rows
    wp, kp, _, _ = two_pole_filter(1., .0625, 20.)
    results["signed_kernel_quantum_gain"] = uniform_quantum_source_effect(
        kp, 1., 20., .3, .5, 40.)
    results["interacting_receiver"] = [interacting_receiver_check(T) for T in [20.,80.]]
    results["coarse_calibration"] = [coarse_linewidth_witness(p) for p in [1e-3,1e-6,1e-9]]

    # Exact cancellation is not uniform under an arbitrary pole mismatch.
    actual_kappa = 1.01
    zeta = np.sqrt(actual_kappa)*quad(
        lambda t: w(t)*np.exp(-actual_kappa*t/2), 0, time, epsabs=1e-12)[0]
    assert abs(zeta) > 1e-6
    results["finite_precision_boundary"] = {
        "nominal_kappa": 1., "actual_kappa": actual_kappa,
        "initial_mode_residue": zeta,
        "coherent_initial_quadrature_for_unit_output_bias": 1/abs(zeta),
        "scope": "An arbitrarily displaced initial state defeats an approximate annihilator; an energy or tail bound is necessary."}

    # Constant-g, vacuum comparator: the best ordinary matched filter with
    # known empty initial cavity versus the exact initial-state rejecting one.
    comparators = []
    for T in [.2, 1., 8., 40.]:
        a = .5
        empty_signal_norm_sq = T-2*integral_exp(a, T)+integral_exp(2*a, T)
        V0 = T-4*np.tanh(T/4)
        comparators.append({"T": T,
                            "empty_receiver_signal_norm_sq": float(empty_signal_norm_sq),
                            "dirty_rejecting_signal_norm_sq": float(V0),
                            "amplitude_SNR_ratio": float(np.sqrt(V0/empty_signal_norm_sq))})
    results["equally_informed_comparison"] = comparators
    results["notes"] = [
        "New Gaussian thermal input field, homodyne acquisition and controlled poles are supplied resources.",
        "No reset of the initial resonator or retained quantum source is assumed in the ideal theorem.",
        "These examples do not establish a device window, pulse calibration cost, or certified rounding enclosure."]
    path = Path(__file__).with_name("output_mode_results.json")
    path.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps({"mode_startup_residual": startup,
                      "source_effects": results["quantum_gain"],
                      "known_poles": pole_rows,
                      "output": str(path)}, indent=2))


if __name__ == "__main__":
    main()
