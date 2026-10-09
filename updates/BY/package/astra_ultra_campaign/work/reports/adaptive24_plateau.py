"""Reproduce the constant-gamma terminal-|x| plateau calculation in the report.
Uses mpmath high-precision differentiation and adaptive quadrature; this is
numerical evidence, not interval-certified proof.
"""
import mpmath as mp

mp.mp.dps = 35
c = mp.mpf(10)
s = mp.mpf(1) / 100
d = mp.mpf(1)
alpha = c * c * s
Phi = lambda z: mp.erfc(-z / mp.sqrt(2)) / 2

# For d=1 and z=c*x, H_c(1,x)=exp(c^2/2) T(z).
T = lambda z: mp.exp(z) * Phi(c + z/c) + mp.exp(-z) * Phi(c - z/c)
L = lambda z: mp.log(T(z))

# Since u(x)=c^{-1} log H_c(1,x), its x-derivatives are
# g=c L'', h=c^2 L''', k=c^3 L''''.
def scaled_integrand(z):
    g = mp.diff(L, z, 2)
    h = mp.diff(L, z, 3)
    k = mp.diff(L, z, 4)
    return k*k - 12*g*h*h + 6*g**4

# The Doob h-transform density of z=c X_s is
# phi_alpha(z) exp(-alpha/2) T(z)/(2 Phi(c sqrt(s+d))).
normalizer = 2 * Phi(c * mp.sqrt(s + d))
def density(z):
    return (
        mp.exp(-z*z/(2*alpha)) / mp.sqrt(2*mp.pi*alpha)
        * mp.exp(-alpha/2) * T(z) / normalizer
    )

integral = mp.quad(
    lambda z: density(z) * scaled_integrand(z),
    [-mp.inf, -5, -3, -2, -1, 0, 1, 2, 3, 5, mp.inf],
)
print("s =", s, "d =", d, "c =", c)
print("Q''' / c^6 =", mp.nstr(integral, 30))
print("Q''' =", mp.nstr(c**6 * integral, 30))
z0 = mp.acosh(mp.sqrt(2))
print("z0 = arcosh(sqrt(2)) =", mp.nstr(z0, 25))
print("scaled local integrand at z0 =", mp.nstr(scaled_integrand(z0), 25))
print("actual local integrand at z0 =", mp.nstr(c**6 * scaled_integrand(z0), 25))
