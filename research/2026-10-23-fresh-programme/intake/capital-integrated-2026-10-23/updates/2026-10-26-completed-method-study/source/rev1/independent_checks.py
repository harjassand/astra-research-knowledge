"""Reviewer reconstruction; does not import candidate code or touch frozen inputs."""
from pathlib import Path
import json
import math
import numpy as np
from scipy.linalg import expm, null_space
from scipy.integrate import solve_ivp

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(61927026)


def laplacian(n, edges):
    out = np.zeros((n, n))
    for i, j, g in edges:
        out[i, i] += g
        out[j, j] += g
        out[i, j] -= g
        out[j, i] -= g
    return out


def release_moments(capacity, grounded_lap, sink_g, source):
    """Integrate the output waveform via its independent symmetric eigensystem."""
    invroot = 1 / np.sqrt(capacity)
    rates, modes = np.linalg.eigh(invroot[:, None] * grounded_lap * invroot[None, :])
    weight = (sink_g * invroot) @ modes * (modes[source] * invroot[source])
    mass = np.sum(weight / rates)
    mean = np.sum(weight / rates**2)
    second = 2 * np.sum(weight / rates**3)
    return float(mass), float(mean), float(second - mean**2)


def ladder_spectral(c, resistance):
    n = len(c)
    full = laplacian(n + 1, [(i, i + 1, 1 / resistance[i]) for i in range(n)])
    sink_g = np.zeros(n)
    sink_g[-1] = 1 / resistance[-1]
    return release_moments(c, full[:n, :n], sink_g, 0)


def q17():
    rows = []
    for n in [2, 3, 7, 16]:
        for ratio in [1.1, 3., 80., 10000.]:
            cumulative = np.exp(np.linspace(0, np.log(ratio), n))
            c = np.diff(np.r_[0., cumulative])
            rho = ratio**(-1 / (n - 1))
            w = np.full(n, (1 - rho) / (1 + rho))
            w[0] = w[-1] = 1 / (1 + rho)
            resistance = w / w.sum() / cumulative
            mass, mean, variance = ladder_spectral(c, resistance)
            bound = 1 / (1 + (n - 1) * np.tanh(np.log(ratio) / (2 * (n - 1))))
            rows.append(dict(n=n, ratio=ratio, mass=mass, mean=mean,
                             spectral_cv2=variance / mean**2, bound=bound))
    branch = []
    for n in [5, 9, 20]:
        for trial in range(20):
            parent = {1: 0}
            for i in range(2, n + 1):
                parent[i] = int(RNG.integers(1, i))
            resistance = {i: float(np.exp(RNG.uniform(-1, 1))) for i in parent}
            source = int(RNG.integers(1, n + 1))
            c = np.exp(RNG.uniform(-1, 1, n))
            c[source - 1] = 1.
            full = laplacian(n + 1, [(i, parent[i], 1 / resistance[i]) for i in parent])
            grounded = full[1:, 1:]
            mass, mean, variance = release_moments(c, grounded, -full[0, 1:], source - 1)
            path, v = [], source
            while v:
                path.append(v)
                v = parent[v]
            members = [[] for _ in path]
            for i in parent:
                v = i
                while v not in path:
                    v = parent[v]
                members[path.index(v)].append(i - 1)
            cc = np.array([c[ids].sum() for ids in members])
            rr = np.array([resistance[v] for v in path])
            _, mean_c, variance_c = ladder_spectral(cc, rr)
            tails = np.cumsum(rr[::-1])[::-1]
            green = np.linalg.inv(grounded)
            predicted = 0.
            for k, ids in enumerate(members):
                h = green[np.ix_(ids, ids)] - tails[k]
                predicted += 2 * tails[k] * np.sum(c[ids, None] * h * c[None, ids])
            branch.append(dict(n=n, trial=trial, mean_error=abs(mean - mean_c),
                               variance_gap=variance - variance_c,
                               predicted_gap=predicted,
                               relative_identity_error=abs(variance - variance_c - predicted) /
                               max(1., abs(variance), abs(predicted))))
    continuum = []
    for ratio in [1.3, 7., 150.]:
        ell = np.log(ratio)
        kappa = 1 / (ell + 2)
        for freq in [.37, 2.1, .3 + 1.7j, 7j]:
            h = kappa * freq
            transfer = expm(np.array([[0, 1], [h, -1]], complex) * ell)
            # h*T(0)-(1+h)*T'(0)=kappa; T'(L)=-T(L).
            system = np.vstack(([h, -(1 + h)], transfer[0] + transfer[1]))
            initial = np.linalg.solve(system, [kappa, 0])
            at_end = transfer @ initial
            shooting = ratio / kappa * at_end[0]
            beta = np.sqrt(.25 + h + 0j)
            reported = np.exp(ell / 2) / ((1 + 2*h) * np.cosh(beta*ell) +
                        (h*h + 2*h + .5) / beta * np.sinh(beta*ell))
            continuum.append(float(abs(shooting - reported)))
    return dict(attaining_designs=rows, branch_collapses=branch,
                max_spectral_cv2_error=max(abs(r['spectral_cv2'] - r['bound']) for r in rows),
                max_branch_relative_identity_error=max(r['relative_identity_error'] for r in branch),
                minimum_branch_variance_gap=min(r['variance_gap'] for r in branch),
                continuum_shooting_cases=len(continuum), max_continuum_shooting_error=max(continuum))


def pd(d):
    a = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
    return a @ a.conj().T + .4 * np.eye(d)


def herm(d):
    a = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
    return (a + a.conj().T) / 2


def tu(a, u):
    d = len(a)
    return u*np.kron(np.eye(d), a) + (1-u)*np.kron(a.T, np.eye(d))


def inner(a, b):
    return float(np.vdot(a, b).real)


def mat(a, b):
    return np.einsum('ik,kj->ij', a, b, optimize=False)


def q28():
    identities = []
    for d in [2, 3, 4]:
        for trial in range(15):
            a, b, h0, h1 = pd(d), pd(d), herm(d), herm(d)
            u = float(RNG.uniform())
            x, y = tu(a, u), tu(b, u)
            z = x + y
            eig, vec = np.linalg.eigh(z)
            assert np.min(eig) > 0
            invroot = mat(vec / np.sqrt(eig), vec.conj().T)
            q = mat(mat(invroot, x), invroot)
            assert np.all(np.isfinite(q))
            qeig, qvec = np.linalg.eigh(q)
            v0, v1 = h0.reshape(-1, order='F'), h1.reshape(-1, order='F')
            total = v0 + v1
            v = invroot @ total
            residual = invroot @ v0 - q @ v
            channel = RNG.uniform(.01, 1, (int(RNG.integers(2, 7)), 2))
            channel /= channel.sum(axis=0)
            lhs = -inner(total, np.linalg.solve(z, total))
            scalar = np.zeros_like(qeig)
            for k0, k1 in channel:
                hv = k0*v0 + k1*v1
                lhs += inner(hv, np.linalg.solve(k0*x + k1*y, hv))
                scalar += (k0-k1)**2 / (k1 + (k0-k1)*qeig)
            spectral_residual = np.einsum('ji,j->i', qvec.conj(), residual, optimize=False)
            rhs = float(np.sum(scalar * abs(spectral_residual)**2))
            identities.append(dict(d=d, trial=trial, relative_error=abs(lhs-rhs)/max(1., abs(lhs), abs(rhs)),
                                   commutator_norm=float(np.linalg.norm(a@b-b@a))))
    aa, bb = 5/8, 1/8
    optimum_x = math.sqrt(bb*(1-bb) / (aa*(1-aa)))
    t = optimum_x/(1+optimum_x)
    coefficient = (math.sqrt(aa*(1-bb))-math.sqrt(bb*(1-aa)))**2
    def kl(p, q):
        return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
    sharpness = []
    for step in [1e-2, 1e-3, 1e-4]:
        sharpness.append(dict(step=step, finite_scalar_ratio=kl(bb+(aa-bb)*(t+step), bb+(aa-bb)*t)/kl(t+step,t)))
    return dict(operator_identities=identities,
                max_operator_relative_error=max(r['relative_error'] for r in identities),
                biased_reset_coefficient=coefficient, index_transplant=.375,
                scalar_sharpness=sharpness,
                ternary_exact_integer_separation=895**10 > 4**10 * 298**9,
                ternary_exact_metric_ratio=math.log(895/4)/(3*math.log(298)))


def ode_response(phases, c, ports):
    """Adaptive numerical period map and integrated currents; no expm or candidate code."""
    m = len(c)
    period = sum(dt for dt, _ in phases)
    avg = sum(dt*ll for dt, ll in phases)/period
    astar, bstar, dstar = avg[ports:, ports:], -avg[ports:, :ports], avg[:ports, :ports]
    xstar = np.linalg.solve(astar, bstar)
    ystar = dstar - bstar.T @ xstar
    invc = np.linalg.inv(c)
    # All initial conditions and forcing columns evolve in one independent ODE solve.
    state = np.c_[np.eye(m), np.zeros((m, ports))]
    for dt, ll in phases:
        a, b = ll[ports:, ports:], -ll[ports:, :ports]
        forcing = np.c_[np.zeros((m, m)), b]
        sol = solve_ivp(lambda t, v: (invc@(-a@v.reshape(m,m+ports)+forcing)).ravel(),
                        (0, dt), state.ravel(), method='DOP853', rtol=2e-11, atol=2e-13)
        assert sol.success
        state = sol.y[:, -1].reshape(m, m+ports)
    initial = np.linalg.solve(np.eye(m)-state[:, :m], state[:, m:])
    x = initial.copy()
    current = np.zeros((ports, ports))
    gap = np.zeros((ports, ports))
    for dt, ll in phases:
        a, b, dd = ll[ports:, ports:], -ll[ports:, :ports], ll[:ports, :ports]
        def rhs(t, v):
            xx = v[:m*ports].reshape(m, ports)
            zz = xx-xstar
            return np.r_[(invc@(-a@xx+b)).ravel(), (dd-b.T@xx).ravel(), (zz.T@a@zz).ravel()]
        sol = solve_ivp(rhs, (0, dt), np.r_[x.ravel(), current.ravel(), gap.ravel()],
                        method='DOP853', rtol=2e-11, atol=2e-13)
        assert sol.success
        last = sol.y[:, -1]
        x = last[:m*ports].reshape(m, ports)
        current = last[m*ports:m*ports+ports**2].reshape(ports, ports)
        gap = last[m*ports+ports**2:].reshape(ports, ports)
    return current/period, ystar, gap/period, float(np.linalg.norm(x-initial))


def q42():
    rows = []
    for trial in range(12):
        ports, m = 3, 2 + trial%3
        phases = []
        for k in range(2 + trial%4):
            # Some phases have ungrounded/isolated internal nodes; the mean graph is connected.
            edges = [(ports+i, ports+i+1, .7) for i in range(m-1)] if k%2 == 0 else []
            edges += [(k%ports, ports+k%m, 1.2), ((k+1)%ports, ports+(k+1)%m, .8)]
            if k == 0:
                edges += [(j, ports, .2) for j in range(ports)]
            phases.append((float(RNG.uniform(.3, 1.5)), laplacian(ports+m, edges)))
        c = np.diag(np.exp(RNG.uniform(-.7, .7, m)))
        if trial%2:
            dense = RNG.normal(size=(m,m))
            c += dense@dense.T/m
        y, ys, gap, residual = ode_response(phases, c, ports)
        back, _, _, _ = ode_response(list(reversed(phases)), c, ports)
        sym = (y+y.T)/2
        u = null_space(np.ones((1,ports)))
        yc, ysc = u.T@y@u, u.T@ys@u
        circle = (yc+yc.T)/2-yc.T@np.linalg.solve(ysc,yc)
        rows.append(dict(trial=trial, phases=len(phases), dense_capacity=bool(trial%2),
                         gap_identity_error=float(np.linalg.norm(ys-sym-gap)),
                         reversal_error=float(np.linalg.norm(y-back.T)),
                         min_circle_eigenvalue=float(np.linalg.eigvalsh((circle+circle.T)/2)[0]),
                         periodic_residual=residual,
                         dc_antisymmetry=float(np.linalg.norm(y-y.T))))
    circ = []
    for leakage, period in [(0., .4), (0., 7.), (.001, 18.7416), (.07, 2.1)]:
        on = 1/(1+2*leakage)
        off = leakage*on
        phases = [(period/3, laplacian(4, [(j,3,on if j==k else off) for j in range(3)])) for k in range(3)]
        y, ys, gap, res = ode_response(phases, np.eye(1), 3)
        z = period/3
        r = math.exp(-z)
        a = (1-r)/(period*(1+r+r*r))
        yy = a*np.array([[1+r,-r,-1],[-1,1+r,-r],[-r,-1,1+r]])
        alpha = on-off
        exact = alpha**2*yy+(1-alpha**2)/3*(np.eye(3)-np.ones((3,3))/3)
        circ.append(dict(leakage=leakage, period=period, formula_error=float(np.max(abs(y-exact))),
                         isolation=float(y[1,0]/y[0,1]), cooling_over_static=float(y[0,0]/ys[0,0])))
    return dict(network_cases=rows, circulators=circ,
                max_gap_identity_error=max(r['gap_identity_error'] for r in rows),
                max_reversal_error=max(r['reversal_error'] for r in rows),
                min_circle_eigenvalue=min(r['min_circle_eigenvalue'] for r in rows),
                max_circulator_formula_error=max(r['formula_error'] for r in circ))


if __name__ == '__main__':
    output = dict(seed=61927026, method='independent reviewer reconstruction; local models only',
                  Q17=q17(), Q28=q28(), Q42=q42())
    assert output['Q17']['max_spectral_cv2_error'] < 1e-9
    assert output['Q17']['max_branch_relative_identity_error'] < 1e-9
    assert output['Q17']['minimum_branch_variance_gap'] >= -1e-9
    assert output['Q17']['max_continuum_shooting_error'] < 1e-10
    assert output['Q28']['max_operator_relative_error'] < 1e-10
    assert output['Q28']['ternary_exact_integer_separation']
    assert output['Q42']['max_gap_identity_error'] < 1e-9
    assert output['Q42']['max_reversal_error'] < 1e-9
    assert output['Q42']['min_circle_eigenvalue'] >= -1e-9
    assert output['Q42']['max_circulator_formula_error'] < 1e-9
    (OUT/'independent_checks.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
    compact = {q:{k:v for k,v in output[q].items() if not isinstance(v,list)} for q in ['Q17','Q28','Q42']}
    print(json.dumps(compact,indent=2))
