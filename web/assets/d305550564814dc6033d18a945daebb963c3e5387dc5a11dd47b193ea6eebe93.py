"""Finite d=2 check of weighted design, raw OLS, and the perturbation bound."""
import numpy as np

rng = np.random.default_rng(20261008)
d, N = 2, 3
omega = np.exp(2j * np.pi / N)
rows = [np.array([1, omega**k], dtype=complex) / np.sqrt(d) for k in range(N)]
rows += [np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)]
rows = np.stack(rows)
m = len(rows)
p = np.array([2 / 9] * N + [1 / 6] * d, dtype=float)
Pis = np.einsum("mi,mj->mij", rows, rows.conj())

swap = np.zeros((d*d, d*d), dtype=complex)
for i in range(d):
    for j in range(d):
        swap[i*d+j, j*d+i] = 1
moment = np.einsum("m,mij,mkl->ikjl", p, Pis, Pis).reshape(d*d, d*d)
target = (np.eye(d*d) + swap) / (d*(d+1))
moment_error = np.max(np.abs(moment-target))

S = 1.0
t = (S * p) ** 0.25
x = rng.normal(size=d) + 1j*rng.normal(size=d)
X = np.outer(x, x.conj())

# Build projective perturbations by rotating each row in its orthogonal direction.
delta_target = 0.01
vrows = []
delta_actual = 0.0
for u in rows:
    w = np.array([-np.conj(u[1]), np.conj(u[0])], dtype=complex)
    w /= np.linalg.norm(w)
    theta = delta_target / 2
    v = np.cos(theta)*u + np.sin(theta)*w
    vrows.append(v)
    delta_actual = max(delta_actual, np.linalg.norm(v-u))
vrows = np.stack(vrows)
gain_bound = 0.02
gammas = rng.uniform(-gain_bound, gain_bound, size=m)
noise = 1e-5*rng.normal(size=m)
y = t**2 * (1+gammas) * np.abs(np.einsum("mi,i->m", vrows.conj(), x))**2 + noise

D = d*(d+1)*Pis - d*np.eye(d)[None, :, :]
Xhat = np.einsum("m,mij->ij", t**2*y/S, D)

# Same lifted raw-row OLS problem in an orthonormal real Hermitian basis.
basis = [np.eye(d)[:, [i]] @ np.eye(d)[[i], :] for i in range(d)]
for i in range(d):
    for j in range(i+1, d):
        Eij = np.zeros((d, d), dtype=complex)
        Eij[i, j] = Eij[j, i] = 1/np.sqrt(2)
        basis.append(Eij)
        Eij = np.zeros((d, d), dtype=complex)
        Eij[i, j], Eij[j, i] = -1j/np.sqrt(2), 1j/np.sqrt(2)
        basis.append(Eij)
design = np.array([[t[k]**2*np.trace(Pis[k] @ B).real for B in basis] for k in range(m)])
coef, *_ = np.linalg.lstsq(design, y, rcond=None)
Xols = np.einsum("k,kij->ij", coef, np.stack(basis))
ols_gap = np.max(np.abs(Xhat-Xols))

gamma = gain_bound
R = np.linalg.norm(x)
bound = R**2*(np.sqrt(2)*gamma + (1+gamma)*(2*np.sqrt(d+1)*delta_actual + np.sqrt(d*(d+1))*delta_actual**2))
bound += np.sqrt(d*(d+1)/S)*np.linalg.norm(noise)
observed_error = np.linalg.norm(Xhat-X, "fro")

assert moment_error < 1e-12
assert ols_gap < 1e-10
assert observed_error <= bound + 1e-10
print(f"m={m}, p={p.tolist()}, max_weight_deviation={max(abs(m*p-1)):.6g}")
print(f"design_moment_max_abs_error={moment_error:.3e}")
print(f"weighted_inverse_vs_raw_OLS_max_abs_gap={ols_gap:.3e}")
print(f"projective_delta={delta_actual:.6g}, observed_Frobenius_error={observed_error:.6g}, theorem_bound={bound:.6g}")
