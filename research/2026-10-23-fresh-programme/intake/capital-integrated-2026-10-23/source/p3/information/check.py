"""Executable checks of retained elementary propositions, not a benchmark."""
import json
import numpy as np

rng = np.random.default_rng(20261023)
max_lower_violation = 0.0
max_upper_violation = 0.0
checks = 0
for n in [1, 2, 5, 12, 30]:
    for _ in range(30):
        u, _ = np.linalg.qr(rng.normal(size=(n, n)))
        mu = float(10 ** rng.uniform(-3, -0.1))
        lam = np.geomspace(mu, 1.0, n) if n > 1 else np.array([mu])
        a = (u * lam) @ u.T
        b = rng.normal(size=n)
        x = np.linalg.solve(a, b) + rng.normal(size=n) * rng.uniform(0, 2)
        eta = float(10 ** rng.uniform(-8, -2) * np.linalg.norm(x))
        e = rng.normal(size=n)
        e *= eta / np.linalg.norm(e)
        y = a @ x + e
        f = 2*b@x-x@y
        low = max(0.0, f-eta*np.linalg.norm(x))
        high = f+eta*np.linalg.norm(x)+(np.linalg.norm(b-y)+eta)**2/mu
        q = float(b @ np.linalg.solve(a,b))
        max_lower_violation = max(max_lower_violation, low-q)
        max_upper_violation = max(max_upper_violation, q-high)
        assert low <= q+1e-8*max(1,q)
        assert q <= high+1e-8*max(1,q)
        checks += 1

two_worlds = []
for mu, delta in [(0.1,0.01), (0.001,0.0001), (0.001,0.002)]:
    q0, q1 = 1/mu, 1/(mu+2*delta)
    estimate = 1/(mu+delta)
    err0, err1 = abs(estimate/q0-1), abs(estimate/q1-1)
    formula = delta/(mu+delta)
    assert abs(err0-formula)<1e-12 and abs(err1-formula)<1e-12
    two_worlds.append(dict(mu=mu,delta=delta,q0=q0,q1=q1,
                          estimate=estimate,minimax_relative_error=formula))
print(json.dumps(dict(checks=checks,max_lower_violation=max_lower_violation,
                      max_upper_violation=max_upper_violation,
                      two_worlds=two_worlds),indent=2))
