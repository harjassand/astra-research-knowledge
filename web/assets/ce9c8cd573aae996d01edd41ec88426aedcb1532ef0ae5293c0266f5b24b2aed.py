"""Finite diagnostic checks; these do not constitute theorem certification."""
import json
from pathlib import Path
import numpy as np

rng = np.random.default_rng(7102026)

def exp_diag(h, s):
    return np.diag(np.exp(s * h))

def rate(E, h):
    T = np.linalg.cholesky(E).conj().T
    B = np.linalg.inv(T)
    A = B.conj().T @ B
    eta = max(-np.log(np.linalg.eigvalsh(E[:i+1,:i+1])[0]) / h[i]
              for i in range(len(h)))
    def tilted_norm(s):
        weights = np.exp(-s*h/2)
        return np.linalg.eigvalsh(weights[:,None]*A*weights[None,:])[-1]
    lo, hi = 0.0, 2*len(h)*eta
    while tilted_norm(hi) > 1:
        hi *= 2
    for _ in range(100):
        mid = (lo + hi) / 2
        if tilted_norm(mid) <= 1:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2, eta, B

def tensor_power(A, n):
    out = np.ones((1,1), dtype=complex)
    for _ in range(n):
        out = np.kron(out, A)
    return out

def tensor_energy(h, n):
    vals = np.array([0.0])
    for _ in range(n):
        vals = (vals[:,None] + h[None,:]).ravel()
    return vals

identity_checks = []
ratios = []
for m in range(1, 6):
    for trial in range(40):
        Z = rng.normal(size=(m,m)) + 1j*rng.normal(size=(m,m))
        _, U = np.linalg.eigh(Z + Z.conj().T)
        es = np.exp(-rng.uniform(.01, 2.0, size=m))
        E = (U * es) @ U.conj().T
        h = np.sort(rng.uniform(.5, 4, size=m))
        s, eta, B = rate(E, h)
        ratios.append({"m":m, "s":s, "eta":eta, "gain":s/eta})
        if m <= 3 and trial < 5:
            for n in (1,2,3):
                energies = tensor_energy(h, n)
                for Q in np.quantile(energies, [0.0,.25,.5,1.0]):
                    idx = np.flatnonzero(energies <= Q + 1e-12)
                    En = tensor_power(E,n)
                    Bn = tensor_power(B,n)
                    direct = np.linalg.eigvalsh(En[np.ix_(idx,idx)])[0]
                    invnorm = 1/np.linalg.norm(Bn[:,idx],ord=2)**2
                    err = abs(direct-invnorm)
                    identity_checks.append(err)

sharp = []
for m in (2,3,4,5):
    for R in (2.,10.,100.):
        h = R ** np.arange(m)
        previous = np.concatenate(([0.],h[:-1]))
        v = np.sqrt((h-previous)/h[-1])
        for tau in (.01,.001,.0001):
            E = np.eye(m) - (1-np.exp(-tau))*np.outer(v,v)
            s, eta, _ = rate(E,h)
            sharp.append({"m":m,"R":R,"tau":tau,"gain":s/eta,
                          "small_tau_limit":m-(m-1)/R,
                          "eta_error":abs(eta-tau/h[-1])})

result = {
    "status":"finite numerical diagnostics only",
    "identity_checks":len(identity_checks),
    "max_identity_abs_error":max(identity_checks),
    "random_instances":len(ratios),
    "max_gain_by_m":{str(m):max(x["gain"] for x in ratios if x["m"]==m)
                     for m in range(1,6)},
    "dimension_bound_violations":int(sum(x["gain"]>x["m"]+1e-8 for x in ratios)),
    "sharp_family":sharp,
}
dest = Path(__file__).with_name("cholesky_diagnostics.json")
dest.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="sharp_family"},indent=2))
