"""Finite qubit diagnostics. PPT is exactly separability for 2x2 Choi states.

No finite result is a theorem. Objectives are minimized as nonnegative losses
to avoid subtracting two nearly equal fidelities.
"""
from pathlib import Path
import json
import numpy as np
import cvxpy as cp


def projectors(states):
    return [np.outer(x / np.linalg.norm(x), (x / np.linalg.norm(x)).conj()) for x in states]


def solve(states, prior, solver="CLARABEL"):
    ps = projectors(states)
    d = len(states[0])
    lc = sum(p * np.kron(P.T, np.eye(d*d) - np.kron(P, P)) for p, P in zip(prior, ps))
    le = sum(p * np.kron(P.T, np.eye(d) - P) for p, P in zip(prior, ps))
    jc = cp.Variable((d**3, d**3), hermitian=True)
    je = cp.Variable((d*d, d*d), hermitian=True)
    cc = [jc >> 0, cp.partial_trace(jc, (d, d*d), axis=1) == np.eye(d)]
    ce = [je >> 0, cp.partial_trace(je, (d, d), axis=1) == np.eye(d),
          cp.partial_transpose(je, (d, d), axis=1) >> 0]
    pc = cp.Problem(cp.Minimize(cp.real(cp.trace(lc @ jc))), cc)
    pe = cp.Problem(cp.Minimize(cp.real(cp.trace(le @ je))), ce)
    opts = dict(tol_gap_abs=2e-10, tol_gap_rel=2e-10, tol_feas=2e-10,
                max_iter=150)
    ec = pc.solve(solver=solver, **opts)
    ee = pe.solve(solver=solver, **opts)
    return dict(e_cl=float(ec), e_eb=float(ee), ratio=float(ee / ec),
                cl_status=pc.status, eb_status=pe.status,
                cl_min_eig=float(np.linalg.eigvalsh(jc.value).min()),
                eb_min_eig=float(np.linalg.eigvalsh(je.value).min()),
                states=[[[float(z.real), float(z.imag)] for z in x] for x in states],
                prior=[float(p) for p in prior])


def main():
    rng = np.random.default_rng(20261011)
    cases = []
    for n in (2, 3, 4, 6, 10):
        for j in range(5):
            z = rng.normal(size=(n, 2)) + 1j*rng.normal(size=(n, 2))
            for scale in (1., .1, .01):
                zz = z.copy()
                if scale < 1:
                    zz[:, 0] = 1
                    zz[:, 1] *= scale
                p = rng.dirichlet(np.full(n, .2 if j % 2 else 1.))
                cases.append((f"random-{n}-{j}-{scale}", zz, p))
    for c in (.2, .8, .95, .99, .999):
        for p in (.5, .05, .001):
            cases.append((f"binary-{c}-{p}", np.array([[1., 0.], [c, np.sqrt(1-c*c)]]), np.array([p, 1-p])))
    for n in (3, 6, 10):
        for s in (.01, .05, .2):
            angles = s * np.geomspace(1., 100., n)
            z = np.stack([np.cos(angles), np.sin(angles)], axis=1)
            p = 1/(1 + angles**2)
            p /= p.sum()
            cases.append((f"multiscale-{n}-{s}", z, p))
    out = []
    for label, states, prior in cases:
        r = solve(states, prior)
        r["label"] = label
        out.append(r)
        if r["ratio"] > 5.82:
            print(json.dumps({k: r[k] for k in ("label", "e_cl", "e_eb", "ratio", "cl_status", "eb_status")}), flush=True)
    path = Path(__file__).with_name("cloning_tradeoff_probe.json")
    path.write_text(json.dumps(dict(scope="Finite diagnostics only; no universal bound or historical priority established", results=out), indent=2))
    best = max(out, key=lambda r: r["ratio"] if r["e_cl"] > 1e-7 else -np.inf)
    print(json.dumps(dict(completed=len(out), best={k:best[k] for k in ("label", "e_cl", "e_eb", "ratio")})), flush=True)


if __name__ == "__main__":
    main()
