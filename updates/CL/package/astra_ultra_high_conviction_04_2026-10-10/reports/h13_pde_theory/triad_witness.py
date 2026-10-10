"""Finite Fourier check of a 2D3C vorticity-stretching witness.

The field is u=(psi_y,-psi_x,W), psi=cos(2x+y), W=cos(x)+cos(x+y),
independent of z. Exact trigonometric integration gives mean(omega.S.omega)=-1/4.
This script is a numerical cross-check, not a PDE regularity test.
"""
import numpy as np

N = 64
x = 2 * np.pi * np.arange(N) / N
X, Y = np.meshgrid(x, x, indexing="ij")
q = 2 * X + Y
u = np.array([-np.sin(q), 2 * np.sin(q), np.cos(X) + np.cos(X + Y)])

freq = np.fft.fftfreq(N, d=1 / N)
KX, KY = np.meshgrid(freq, freq, indexing="ij")
uh = np.fft.fftn(u, axes=(1, 2))
grad = np.empty((3, 3, N, N))
for i in range(3):
    grad[i, 0] = np.fft.ifftn(1j * KX * uh[i]).real
    grad[i, 1] = np.fft.ifftn(1j * KY * uh[i]).real
    grad[i, 2] = 0
omega = np.array([
    grad[2, 1] - grad[1, 2],
    grad[0, 2] - grad[2, 0],
    grad[1, 0] - grad[0, 1],
])
S = (grad + grad.swapaxes(0, 1)) / 2
stretch = np.einsum("i...,ij...,j...->...", omega, S, omega)
P = float(stretch.mean())
Y = float(np.square(omega).sum(axis=0).mean())
omega_hat = np.fft.fftn(omega, axes=(1, 2))
Z = float((np.square(np.abs(1j * KX * omega_hat)).sum(axis=0)
           + np.square(np.abs(1j * KY * omega_hat)).sum(axis=0)).mean() / N**2)

# Compute the exact nonlinear vorticity RHS F=omega.grad(u)-u.grad(omega).
F = np.empty_like(omega)
for i in range(3):
    F[i] = sum(omega[j] * grad[i, j] for j in range(3))
    F[i] -= sum(u[j] * np.fft.ifftn(1j * KX * np.fft.fftn(omega[i], axes=(0, 1))).real
                 if j == 0 else
                 u[j] * np.fft.ifftn(1j * KY * np.fft.fftn(omega[i], axes=(0, 1))).real
                 if j == 1 else 0 for j in range(3))
# The transport subtraction above has only j=0,1 contributions; u[2] multiplies
# a zero z-derivative.
assert abs(float(np.einsum("i...,i...->...", omega, F).mean()) - P) < 1e-10
assert abs(P + 0.25) < 1e-10
assert abs(Y - 14.0) < 1e-10
assert abs(Z - 65.0) < 1e-10
print(f"mean(P)={P:.12f}; Y={Y:.12f}; Z={Z:.12f}; "
      f"mean(abs(local production))={float(np.abs(stretch).mean()):.12f}")
