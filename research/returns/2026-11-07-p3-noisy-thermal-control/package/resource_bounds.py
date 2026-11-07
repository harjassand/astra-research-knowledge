"""Analytic resource formulas evaluated in binary64 (not interval certificates).

The report proves the bounds. An operational schedule additionally needs a
justified positive CMLSI lower bound alpha and a warranted native rate law.
No numerical alpha is inferred from finite-size diagonalization here.
"""
import math
from scipy.special import gammainc, erfc


def exponential_tail(a, first):
    """sum_{l>=first} a**l/l!, a>=0."""
    if first <= 0:
        return math.exp(a)
    return math.exp(a)*float(gammainc(first, a))


def weighted_tail(a, first, r0):
    return exponential_tail(a, first)+2*r0*a*exponential_tail(a, first-1)


def filter_tail(q, beta, velocity):
    if q < 1:
        return float("inf")
    # log(coth z) = log1p(2/(exp(2z)-1)), stable at large z.
    z = math.pi*q/(2*math.e*velocity*beta)
    logcoth = 0.0 if 2*z > 740 else math.log1p(2/math.expm1(2*z))
    return q*math.exp(-q/2)/(2*math.e*math.pi)+2*logcoth/math.pi


def noise_completion_error(r, q, beta, strength, r0=1):
    v = 4*r0*(1+strength)
    s = beta/2
    a = v*s*math.exp(v*s)
    m = math.exp(2*strength*s+a)
    jerr = math.exp(2*strength*s)*exponential_tail(a, r+1)
    ktail = beta*strength*m*math.exp(2*strength*s)/2*weighted_tail(a, r+1, r0)
    gerr = ktail+(1+m*m)*filter_tail(q, beta, v)
    return {"half_diamond_upper": 2*m*jerr+gerr, "jump_norm_upper": m,
            "jump_error_upper": jerr, "coherent_error_upper": gerr,
            "window_sites_upper": 1+2*r0*(r+q)}


def ckg_e(r, beta, velocity):
    return velocity*beta/math.sqrt(math.pi)*math.exp(-r/2)+2*float(erfc(r/(2*math.e*velocity*beta)))


def ckg_error(r, q, beta, strength, a_proposals=0.75, r0=1):
    """Conservative closed exponential sum for K-tail, exact erfc for CP part.

    For l>=r, erfc(l/c) <= exp(-l^2/c^2). At l=r+k this is <=
    exp(-r^2/c^2)*exp(-(2r+1)k/c^2), k>=0. This keeps the Gaussian tail.
    """
    v = 4*r0*(1+strength)
    c = 2*math.e*v*beta
    # Sum_{l>=r+1} (1+2r0*l) [2a E_l + 2a E_(l-1)].
    def weighted_geometric(first, ratio, initial):
        return initial*((1+2*r0*first)/(1-ratio)+2*r0*ratio/(1-ratio)**2)
    def e_weighted(first, shift):
        k = first-shift
        z1 = v*beta/math.sqrt(math.pi)*math.exp(-k/2)
        s1 = weighted_geometric(first, math.exp(-0.5), z1)
        z2 = 2*math.exp(-(k/c)**2)
        ratio = math.exp(-(2*k+1)/(c*c))
        s2 = weighted_geometric(first, ratio, z2)
        return s1+s2
    ktail = 2*a_proposals*(e_weighted(r+1, 0)+e_weighted(r+1, 1))
    gerr = beta*strength/4*ktail+a_proposals*filter_tail(q, beta, v)
    return {"half_diamond_upper": 2*a_proposals*ckg_e(r,beta,v)+gerr,
            "coherent_error_upper": gerr,
            "window_sites_upper": 1+2*r0*(r+q)}


def select_radii(tolerance, beta, strength, kind, max_radius=20000):
    """Balanced r=q search, an explicit sufficient choice, not an optimum."""
    fn = noise_completion_error if kind == "noise" else ckg_error
    for r in range(1, max_radius+1):
        row = fn(r, r, beta, strength)
        if row["half_diamond_upper"] <= tolerance:
            return dict(row, inner_radius=r, outer_extra_radius=r,
                        tolerance=tolerance, diagnostic_arithmetic="binary64")
    raise ValueError("radius search cap reached; no success certified")


def schedule(n, d, beta, strength, alpha, u, epsilon, eta=0):
    if min(n, d, alpha, u, epsilon) <= 0:
        raise ValueError("positive parameters required")
    a = max(1.0, math.sqrt(n*(math.log(d)+beta*strength)))
    h = (1+math.log(a))/(u*alpha)
    floor = 2*eta*h
    if floor >= epsilon:
        return {"feasible_sufficient_schedule": False, "error_floor_upper": floor}
    t = max(0.0, math.log(a/(epsilon-floor))/(u*alpha))
    return {"feasible_sufficient_schedule": True, "mixing_time_upper": t,
            "memory_integral_upper": h, "error_floor_upper": floor,
            "alpha_status": "supplied proof-bound parameter, not acquired by this script"}
