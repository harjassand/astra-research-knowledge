"""Numerical falsification checks for the P1 quantum acquisition theorem.

These are floating-point checks of finite models, not a formal or interval proof.
Run: python3 verify_access.py
"""
import json
import math
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import csr_matrix, eye, kron as skron
from scipy.sparse.linalg import expm_multiply

HERE = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1., -1.]).astype(complex)
P = [I, X, Y, Z]

def tensor(matrices):
    z = np.ones((1, 1), complex)
    for matrix in matrices:
        z = np.kron(z, matrix)
    return z

def meter_beta(w, omega, lam=1.):
    T = 1. / lam
    def f(t, ab):
        pulse = omega * lam * min(t, T-t)
        a, b = ab
        return [pulse*b, -pulse*a - 2*w*lam*b]
    ab = np.array([0., 1.])
    for lo, hi in [(0., T/2), (T/2, T)]:
        sol = solve_ivp(f, (lo, hi), ab, method="Radau", rtol=2e-10, atol=2e-14)
        if not sol.success:
            raise RuntimeError(sol.message)
        ab = sol.y[:, -1]
    integral = omega/(4*w*w*lam) * (1-math.exp(-w))**2
    q = omega**2/(8*w*lam**2)
    rigorous_lower = integral * (1-2*q)/(1-q)
    simple_lower = omega/(12*w*w*lam)
    assert ab[0] >= rigorous_lower - 2e-11
    assert rigorous_lower >= simple_lower - 2e-14
    return dict(w=w, omega=omega, beta=float(ab[0]),
                volterra_lower=rigorous_lower, simple_lower=simple_lower,
                ratio_to_simple=float(ab[0]/simple_lower))

def random_channel_check(seed, n, k, omega=1., lam=1.):
    rng = np.random.default_rng(seed)
    na = 2
    da = 2**na
    ds = 2**n
    dt = ds*da
    raw = []
    for _ in range(2*n+1):
        size = int(rng.integers(1, k+1))
        sites = tuple(sorted(rng.choice(n, size=size, replace=False).tolist()))
        source = [P[int(rng.choice([0, 3]))] for _ in range(n)]
        for site in sites:
            source[site] = P[int(rng.choice([1, 2]))]
        ancilla = [P[int(rng.integers(0, 4))] for _ in range(na)]
        raw.append((sites, float(rng.uniform(.05, 1.)), tensor(source+ancilla)))
    maximum = max(sum(h for sites, h, _ in raw if i in sites) for i in range(n))
    terms = [(sites, omega*h/maximum, matrix) for sites, h, matrix in raw]
    H = sum(h/2 * matrix for sites, h, matrix in terms)
    for _ in range(4):
        source = [P[int(rng.choice([0, 3]))] for _ in range(n)]
        ancilla = [P[int(rng.integers(0, 4))] for _ in range(na)]
        H += rng.uniform(-3, 3) * tensor(source+ancilla)
    ident = eye(dt, dtype=complex, format="csr")
    hs = csr_matrix(H)
    generator = -1j*(skron(ident, hs)-skron(hs.T, ident))
    for i in range(n):
        zi = csr_matrix(tensor([Z if j==i else I for j in range(n+na)]))
        generator += lam*(skron(zi.conj(), zi)-eye(dt*dt, dtype=complex))
    bell = np.array([1., 0., 0., 1.], complex)/math.sqrt(2)
    apparatus = np.outer(bell, bell.conj())
    transverse = tensor([X]*n)/ds
    ghz_difference = np.zeros((ds, ds), complex)
    ghz_difference[0, -1] = ghz_difference[-1, 0] = .5
    @lru_cache(None)
    def certificate(mask):
        if mask == 0:
            return 1.
        numerator = 0.
        for sites, h, _ in terms:
            b = sum(1<<i for i in sites)
            if mask & b:
                numerator += h*certificate(mask & ~b)
        return min(1., numerator/(2*lam*mask.bit_count()))
    r = omega/(2*lam)
    x = max((r/j)**(1/j) for j in range(1, k+1))
    uniform = min(x**n, r**math.ceil(n/k))
    graph = certificate((1<<n)-1)
    rows = []
    for label, difference in [("full_pauli", transverse), ("GHZ_purity_gap", ghz_difference)]:
        initial = np.kron(difference, apparatus).reshape(-1, order="F")
        for t in [.1, .4, 1., 3., 8.]:
            state = expm_multiply(generator*t, initial).reshape((dt, dt), order="F")
            out = np.einsum("iaib->ab", state.reshape(ds, da, ds, da))
            norm = float(np.linalg.svd(out, compute_uv=False).sum())
            assert norm <= min(uniform, graph) + 5e-10, (seed, label, t, norm, uniform, graph)
            rows.append(dict(seed=seed, n=n, k=k, label=label, time=t,
                             trace_norm=norm, uniform_bound=uniform,
                             hypergraph_bound=graph))
    return rows

def constant_meter_optimum(k, omega, lam=1.):
    L = k*lam
    q = math.sqrt(max(0., L*L-omega*omega))
    if q < 1e-12:
        t = 1/L
    else:
        t = math.log((L+q)/omega)/q
    beta = math.exp(-L*t)
    return dict(k=k, omega=omega, time=t, beta=beta,
                theorem_bound=omega/(2*k*lam), ratio=beta/(omega/(2*k*lam)))

def main():
    meter = [meter_beta(w, omega) for w in [1,2,5,10,30,100,300,1000] for omega in [.1,.3,1.]]
    channels = []
    for n, k, seed in [(2,1,101),(2,2,102),(3,1,103),(3,2,104),(3,3,105),(3,2,106)]:
        channels.extend(random_channel_check(seed,n,k))
    optimum = [constant_meter_optimum(k,o) for k in [1,2,4,8] for o in [.001,.01,.1,1.]]
    report = dict(status="all finite-model checks passed", caveat="Floating-point illustrative checks; proof is analytic.",
                  triangular_meters=meter, shared_receiver_checks=channels,
                  weak_control_optimum=optimum,
                  max_observed_to_bound=max(r["trace_norm"]/min(r["uniform_bound"],r["hypergraph_bound"]) for r in channels))
    (HERE/"verification_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"meter_cases":len(meter),"shared_receiver_cases":len(channels),
                      "max_observed_to_bound":report["max_observed_to_bound"],
                      "minimum_slew_meter_ratio":min(r["ratio_to_simple"] for r in meter)},indent=2))
    make_plot()

def make_plot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ns = np.arange(2,161,2)
    ratio = .25
    fig, ax = plt.subplots(figsize=(8.5,4.8))
    for k, color in [(1,"#1f4d70"),(2,"#b04832"),(4,"#805b9b")]:
        ax.plot(ns, np.log10(1.8)+(ns/k)*np.log10(2*k/ratio),label=f"Necessary copies: source order k={k}",color=color,lw=2)
    ax.plot(ns,np.log10(1152*np.log(20)/ratio**2)+4*np.log10(ns),"--",color="#25836b",lw=2,
            label="Sufficient copies: native n-body, finite-slew meter")
    ax.set(xlabel="Number of source qubits n",ylabel="log10(number of fresh copies)",
           title="Physical access order separates exponential and polynomial readout")
    ax.text(.02,.98,"Illustrative model: Ω=λ/4; parity amplitude 1/2; error probability ≤5%",
            transform=ax.transAxes,ha="left",va="top",fontsize=8.5)
    ax.grid(alpha=.2)
    ax.legend(loc="center left",fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE/"access_scaling.png",dpi=190)
    plt.close(fig)

if __name__ == "__main__":
    main()
