"""Stable Gibbs--Helmholtz face-enthalpy secants for NASA7 ideal species.

No chemistry coefficients are bundled or inferred. Pass the exact coefficient arrays
used by the receiving thermochemistry, shape (..., 7), and mass-specific gas constants.
The branchwise construction requires continuous g_i^0/T at each temperature splice.
It never silently repairs input coefficients. Run splice_diagnostics once on inputs.
"""
import numpy as np


def _coefficients(coeff):
    a = np.asarray(coeff, dtype=float)
    if a.ndim < 1 or a.shape[-1] != 7 or not np.all(np.isfinite(a)):
        raise ValueError('NASA coefficients must be finite with last dimension 7.')
    return a


def nasa7_h(T, coefficients, gas_constants):
    """Mass-specific species enthalpy, J/kg; NASA order a0,...,a6."""
    if not np.isfinite(T) or T <= 0:
        raise ValueError('Temperature must be finite and positive.')
    a = _coefficients(coefficients)
    R = np.asarray(gas_constants, dtype=float)
    return R*(T*(a[...,0]+T*(a[...,1]/2+T*(a[...,2]/3+T*(a[...,3]/4+T*a[...,4]/5))))+a[...,5])


def nasa7_s0(T, coefficients, gas_constants):
    """Standard-pressure mass-specific species entropy, J/(kg K)."""
    if not np.isfinite(T) or T <= 0:
        raise ValueError('Temperature must be finite and positive.')
    a = _coefficients(coefficients)
    R = np.asarray(gas_constants, dtype=float)
    return R*(a[...,0]*np.log(T)+T*(a[...,1]+T*(a[...,2]/2+T*(a[...,3]/3+T*a[...,4]/4)))+a[...,6])


def nasa7_h_secant_one_branch(TL, TR, coefficients, gas_constants):
    """Exact analytic beta-average of NASA7 enthalpy on one branch.

    The result is symmetric in TL,TR and stable down to equal floating-point
    temperatures. log1p avoids loss in log(TR/TL) near unity. a6 cancels.
    """
    if not np.isfinite(TL) or not np.isfinite(TR) or min(TL,TR) <= 0:
        raise ValueError('Both temperatures must be finite and positive.')
    a = _coefficients(coefficients)
    R = np.asarray(gas_constants, dtype=float)
    if TL == TR:
        return nasa7_h(TL,a,R)
    lo, hi = min(TL,TR), max(TL,TR)
    d = hi-lo
    log_slope = np.log1p(d/lo)/d
    polynomial = (a[...,0]*log_slope + a[...,1]/2
                  + a[...,2]*(hi+lo)/6
                  + a[...,3]*(hi*hi+hi*lo+lo*lo)/12
                  + a[...,4]*(hi**3+hi*hi*lo+hi*lo*lo+lo**3)/20)
    return R*(lo*hi*polynomial+a[...,5])


def nasa7_h_secant(TL, TR, low_coefficients, high_coefficients,
                   gas_constants, splice_temperature=1000.):
    """Piecewise exact beta-average, including a crossed NASA temperature splice.

    Arrays have shape (...,7); return shape is broadcast species shape. A single
    common splice is assumed. The weights are beta-interval fractions evaluated
    without subtracting nearly equal reciprocal temperatures.

    This equals [g0(TR)/TR-g0(TL)/TL]/[1/TR-1/TL] only when g0/T is continuous
    at the splice. Check splice_diagnostics against the receiving thermo's own
    tolerances; do not equate a discontinuous raw table to a continuous model.
    """
    if not np.isfinite(TL) or not np.isfinite(TR) or min(TL,TR) <= 0:
        raise ValueError('Both temperatures must be finite and positive.')
    cut = float(splice_temperature)
    if not np.isfinite(cut) or cut <= 0:
        raise ValueError('Splice temperature must be finite and positive.')
    lo, hi = min(TL,TR), max(TL,TR)
    if hi <= cut:
        return nasa7_h_secant_one_branch(lo,hi,low_coefficients,gas_constants)
    if lo >= cut:
        return nasa7_h_secant_one_branch(lo,hi,high_coefficients,gas_constants)
    h_low = nasa7_h_secant_one_branch(lo,cut,low_coefficients,gas_constants)
    h_high = nasa7_h_secant_one_branch(cut,hi,high_coefficients,gas_constants)
    denominator = (hi-lo)*cut
    weight_low = (cut-lo)*hi/denominator
    weight_high = (hi-cut)*lo/denominator
    return weight_low*h_low+weight_high*h_high


def splice_diagnostics(low_coefficients, high_coefficients, gas_constants,
                       splice_temperature=1000.):
    """Report high-minus-low branch discontinuities without modifying tables."""
    t=float(splice_temperature)
    hl=nasa7_h(t,low_coefficients,gas_constants)
    hh=nasa7_h(t,high_coefficients,gas_constants)
    sl=nasa7_s0(t,low_coefficients,gas_constants)
    sh=nasa7_s0(t,high_coefficients,gas_constants)
    return {'h_jump_J_per_kg':hh-hl, 's0_jump_J_per_kgK':sh-sl,
            'g0_over_T_jump_J_per_kgK':(hh-hl)/t-(sh-sl)}
