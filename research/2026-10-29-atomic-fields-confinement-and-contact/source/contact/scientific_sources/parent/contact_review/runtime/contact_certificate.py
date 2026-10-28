"""Conditional contact-aware radius certificate; no physical acquisition claim.

Certificate arithmetic uses fractions and integer square-root enclosures.
The caller supplies a Loewner upper U on contact-weighted crack moments,
in units of a_scale**3, and an operator/model contact lower bound k.
See PRIMARY_PROOF.md for the measurement and model obligations.
"""
from dataclasses import asdict, dataclass
from fractions import Fraction as F
from heapq import heappop, heappush
from math import isqrt

PI_LO = F("3.1415926535897932384626433832795028841971")
PI_HI = PI_LO + F(1, 10**40)

def sqrt_bounds(x, digits=40):
    x = F(x)
    if x < 0:
        raise ValueError("negative square-root argument")
    scale = 10**digits
    t = isqrt((x.numerator * scale * scale) // x.denominator)
    lo = F(t, scale)
    hi = lo if lo * lo == x else F(t + 1, scale)
    assert lo * lo <= x <= hi * hi
    return lo, hi

def reference_mass_bounds():
    """M_ref / (100 micrometres)^3 = pi^(-3/2), enclosed."""
    sl, _ = sqrt_bounds(PI_LO)
    _, sh = sqrt_bounds(PI_HI)
    return 1 / (PI_HI * sh), 1 / (PI_LO * sl)

@dataclass(frozen=True)
class Parameters:
    E: F = F(110_000_000_000)
    nu: F = F(34, 100)
    H: F = F(1, 100)
    a_scale: F = F(1, 10_000)
    a_max: F = F(1, 2_000)
    service0: F = F(500_000_000)
    service1: F = F(250_000_000)
    service_residual0: F = F(0)
    service_residual_gradient: F = F(0)
    @property
    def beta(self):
        return 16 * (1 - self.nu**2) / (3 * self.E)
    def check(self):
        if not (self.E > 0 and -1 < self.nu < F(1, 2)):
            raise ValueError("invalid isotropic elastic constants")
        if not (self.H > 0 and self.a_scale > 0 and self.a_max > 0):
            raise ValueError("positive lengths required")
        if self.service_residual0 < 0 or self.service_residual_gradient < 0:
            raise ValueError("residual envelopes must be nonnegative")

def corrected_upper(measured, entry_error=(0, 0, 0), nuisance_norm=0):
    """Entrywise noise plus symmetric nuisance operator-norm enclosure.

    Triples are (00,01,11), already in a_scale**3 moment units.
    Nuisance includes remaining background, fixture and model differences.
    """
    m0, m1, m2 = map(F, measured)
    e0, e1, e2 = map(F, entry_error)
    b = F(nuisance_norm)
    if min(e0, e1, e2, b) < 0:
        raise ValueError("nonnegative error bounds required")
    return (m0 + e0 + e1 + b, m1, m2 + e2 + e1 + b)

def inverse_quadratic(U):
    """q(r)=[1,r]^T U^-1[1,r] = A r^2+B r+C."""
    u0, u1, u2 = map(F, U)
    det = u0 * u2 - u1 * u1
    if u0 <= 0 or det <= 0:
        raise ValueError("strictly positive definite upper matrix required")
    return u0 / det, -2 * u1 / det, u2 / det

def quadratic_min(q, left, right):
    A, B, C = q
    left, right = F(left), F(right)
    if left > right:
        raise ValueError("reversed interval")
    x = min(right, max(left, -B / (2 * A)))
    return A * x * x + B * x + C

def h_dimensionless(t, params, k, pi):
    """h_k(a)/a_scale^3. k=None denotes ideal rigid closure."""
    t = F(t)
    if t < 0:
        raise ValueError("negative radius")
    if k is None:
        return t**3
    k = F(k)
    if k <= 0:
        raise ValueError("positive contact lower bound required")
    theta = params.beta * k * params.a_scale / pi
    return theta * t**4 / (1 + theta * t)

def radius_bounds(mass, params, k, steps=65):
    """Enclose min(a_max, h_k^-1(mass*a_scale^3)), in metres.

    h increases with theta=beta*k*a_scale/pi. Bisection at lower pi
    supplies a lower root; at upper pi supplies an upper root.
    """
    mass = F(mass)
    if mass < 0:
        raise ValueError("negative mass allowance")
    tcap = params.a_max / params.a_scale
    bounds = []
    for pi in (PI_LO, PI_HI):
        lo, hi = F(0), tcap
        if h_dimensionless(hi, params, k, pi) <= mass:
            lo = hi
        else:
            for _ in range(steps):
                mid = (lo + hi) / 2
                if h_dimensionless(mid, params, k, pi) <= mass:
                    lo = mid
                else:
                    hi = mid
        bounds.append((lo * params.a_scale, hi * params.a_scale))
    return bounds[0][0], bounds[1][1]

def service_k_bounds(a, r, params):
    """Enclose the declared isolated-disk tensile K upper law."""
    a, r = F(a), F(r)
    center = max(F(0), params.service0 + params.service1 * r
                 + params.service_residual0)
    gradient = 2 * abs(params.service1) / params.H + params.service_residual_gradient
    stress = center + F(2, 3) * gradient * a
    sl, _ = sqrt_bounds(a / PI_HI)
    _, sh = sqrt_bounds(a / PI_LO)
    return 2 * sl * stress, 2 * sh * stress

def point_function_bounds(r, q, params, k):
    """Enclose the radius-bound function, not an attainable physical flaw."""
    A, B, C = q
    mass = 1 / (A * r * r + B * r + C)
    al, au = radius_bounds(mass, params, k)
    return service_k_bounds(al, r, params)[0], service_k_bounds(au, r, params)[1]

def interval_upper(left, right, q, params, k):
    mass = 1 / quadratic_min(q, left, right)
    _, au = radius_bounds(mass, params, k)
    sr = right if params.service1 >= 0 else left
    return service_k_bounds(au, sr, params)[1]

def certify(U, params, k, depth=(-F(4, 5), F(4, 5)),
            tolerance=F(1_000), max_cells=5000):
    """Rational interval branch-and-bound; tolerance in Pa sqrt(m).

    The returned upper stays valid on budget exhaustion; only tightness
    changes. All leaves are retained; no floating-point pruning is used.
    """
    params.check()
    if k is not None and F(k) <= 0:
        raise ValueError("positive contact operator lower bound required")
    left, right = map(F, depth)
    if not (-1 < left < right < 1):
        raise ValueError("depth interval must lie strictly within thickness")
    thickness_clearance = params.H * (1 - max(abs(left), abs(right))) / 2
    if params.a_max >= thickness_clearance:
        raise ValueError("radius/depth domain must keep every disk strictly buried in thickness")
    minimum_center = min(params.service0 + params.service1 * left,
                         params.service0 + params.service1 * right)
    gradient_bound = 2 * abs(params.service1) / params.H + params.service_residual_gradient
    if minimum_center - params.service_residual0 < F(2, 3) * gradient_bound * params.a_max:
        raise ValueError("service all-open affine-disk margin not supplied")
    q = inverse_quadratic(U)
    if F(tolerance) <= 0 or max_cells < 1:
        raise ValueError("positive termination budgets required")
    serial = 0
    heap = [(-interval_upper(left, right, q, params, k), serial, left, right)]
    best, best_r, evaluations, splits = F(0), left, 0, 0
    while heap:
        if -heap[0][0] <= best + F(tolerance) or len(heap) >= max_cells:
            break
        _, _, l, r = heappop(heap)
        mid = (l + r) / 2
        low, _ = point_function_bounds(mid, q, params, k)
        evaluations += 1
        if low > best:
            best, best_r = low, mid
        for x, y in ((l, mid), (mid, r)):
            serial += 1
            heappush(heap, (-interval_upper(x, y, q, params, k), serial, x, y))
        splits += 1
    bound = max(-leaf[0] for leaf in heap)
    return {
        "status": "CONDITIONAL_MATHEMATICAL_UPPER_BOUND",
        "upper_Pa_sqrt_m": str(bound),
        "upper_MPa_sqrt_m": float(bound / 1_000_000),
        "bound_function_lower_Pa_sqrt_m": str(best),
        "enclosure_gap_Pa_sqrt_m": float(bound - best),
        "bound_function_argmax_candidate_r": float(best_r),
        "leaf_count": len(heap), "split_count": splits,
        "point_evaluations": evaluations,
        "contact_lower_Pa_per_m": None if k is None else str(F(k)),
        "U_dimensionless_triple": [str(F(u)) for u in U],
        "a_scale_m": str(params.a_scale),
        "parameter_rationals": {key: str(value) for key, value in asdict(params).items()},
        "depth_interval": [str(left), str(right)],
        "thickness_burial_clearance_m": str(thickness_clearance),
        "remaining_geometric_admission": "LATERAL_BURIAL_AND_COMPONENT_MODEL_ERROR_SUPPLIED_EXTERNALLY",
        "coverage_leaves": [
            {"left": str(l), "right": str(r), "upper_Pa_sqrt_m": str(-neg)}
            for neg, _, l, r in sorted(heap, key=lambda leaf: leaf[2])
        ],
        "pi_enclosure": [str(PI_LO), str(PI_HI)],
        "physical_acquisition": "NOT_PERFORMED",
        "contact_coercivity_for_component": "NOT_ACQUIRED",
        "material_and_fixture_nuisance_bound": "SUPPLIED_NOT_ACQUIRED",
    }

def acquisition_envelope(params, preload, h0, h1, depth_radius,
                         residual0, residual_gradient=0, gap_equivalent_stress=0):
    """Ideal affine switching and maximum test opening K guards.

    Contact stiffness, no-growth envelope, finite-boundary corrections
    and background linearity remain independent prerequisites.
    """
    P, h0, h1, R, rho0, rhog, gap = map(
        F, (preload, h0, h1, depth_radius, residual0,
            residual_gradient, gap_equivalent_stress))
    if min(P, h0, h1, R, rho0, rhog, gap) < 0:
        raise ValueError("envelope parameters must be nonnegative")
    # The eight-point protocol probes one mode at a time. Do not charge
    # simultaneous h0 and h1 unless such combined probes are actually used.
    required = rho0 + params.a_max * rhog + max(
        h0, h1 * (R + 2 * params.a_max / params.H)) + gap
    _, root = sqrt_bounds(params.a_max / PI_LO)
    kmax = 2 * root * (P + rho0 + F(2, 3) * rhog * params.a_max + max(
        h0, h1 * R + F(4, 3) * h1 * params.a_max / params.H))
    return {
        "switch_required_Pa": float(required), "preload_Pa": float(P),
        "strict_switch_margin_Pa": float(P - required),
        "ideal_affine_switch_sufficient": P > required,
        "maximum_test_K_upper_MPa_sqrt_m": float(kmax / 1_000_000),
        "contact_coercivity": "NOT_IMPLIED_BY_SWITCH_MARGIN",
        "nondestructive_protocol": "NOT_ESTABLISHED",
    }
