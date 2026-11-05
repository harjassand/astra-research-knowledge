"""Exact symbolic audits and numerical demonstrations; run from any directory."""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import platform
import warnings

import cvxpy as cp
import numpy as np
import sympy as sp

from certify_fixed_law import (
    Measurement, contraction_radius, scalar_envelope, scalar_t_attainer,
    solve_equilibrium, solve_fixed_law, tail_horizon, vector_attainer,
    vector_envelope,
)

ROOT = Path(__file__).resolve().parent


def exact_audit():
    L = sp.symbols("L", positive=True)
    ax, ay, az, bx, by, bz = sp.symbols("ax ay az bx by bz", real=True)
    e = sp.Matrix([1, 0, 0])
    a, b = sp.Matrix([ax, ay, az]), sp.Matrix([bx, by, bz])
    norm2 = lambda v: (v.T * v)[0]
    g1 = norm2(a + e) - L**2
    g2 = norm2(b + e) - L**2 * norm2(a)
    g3 = norm2(b - a) - L**2 * norm2(a + e)
    s = -(1 + L) / (1 + 2 * L)
    t = -1 + L * (1 + L) / (1 + 2 * L)
    z, w = a - s * e, b - t * e
    identity_small = sp.factor(t + (g2 + g3) / (2 * L)
                              - norm2(w - z/2) / L
                              - (1 - 4 * L**2) * norm2(z) / (4 * L) - bx)
    identity_large = sp.factor(L**2 - sp.Rational(7, 8)
                              + (sp.Rational(1, 2) - 1/(8 * L**2)) * g1
                              + (g2 + g3)/(4 * L**2)
                              - norm2(a - 2 * b + (2 * L**2 - 1) * e)/(8 * L**2) - bx)
    assert identity_small == 0
    assert identity_large == 0
    G = sp.Matrix([[1, -sp.Rational(3,4), sp.Rational(1,8)],
                   [-sp.Rational(3,4), sp.Rational(3,2), sp.Rational(3,8)],
                   [sp.Rational(1,8), sp.Rational(3,8), sp.Rational(1,4)]])
    principal_minors = [G.extract(index, index).det()
                        for n in range(1, 4) for index in itertools.combinations(range(3), n)]
    assert all(v >= 0 for v in principal_minors)
    assert G.rank() == 2
    ee, aa, bb = sp.eye(3)[:,0], sp.eye(3)[:,1], sp.eye(3)[:,2]
    gramnorm = lambda v: (v.T * G * v)[0]
    exact_constraints = [gramnorm(aa + ee)-1,
                         gramnorm(bb + ee)-gramnorm(aa),
                         gramnorm(bb - aa)-gramnorm(aa + ee)]
    assert exact_constraints == [0, 0, 0]
    assert gramnorm(ee + aa - 2*bb) == 0
    # Audit scalar endpoint comparison and exact fixed-point completing square.
    scalar_difference = sp.factor(t - (L**2-L-1))
    assert sp.factor(scalar_difference - 2*L*(1+L-L**2)/(1+2*L)) == 0
    x = sp.Matrix(sp.symbols("x1 x2 x3", real=True))
    center = (b-L**2*a)/(1-L**2)
    radius_squared = L**2*norm2(b-a)/(1-L**2)**2
    ball_identity = sp.factor(norm2(x-b)-L**2*norm2(x-a)
                              -(1-L**2)*(norm2(x-center)-radius_squared))
    assert ball_identity == 0
    return {
        "small_branch_identity_zero": True,
        "large_branch_identity_zero": True,
        "equilibrium_ball_identity_zero": True,
        "L1_gram_principal_minors": [str(v) for v in principal_minors],
        "L1_gram_rank": G.rank(),
        "L1_all_interpolation_residuals": [str(v) for v in exact_constraints],
        "L1_objective": str(G[0,2]),
        "scalar_branch_difference": str(scalar_difference),
    }


def brief(result):
    keys = ["status", "value", "known_span_dimension", "unknown_vector_count",
            "physical_dimension", "interpolation_and_noise_constraint_count",
            "gram_min_eigenvalue", "maximum_constraint_violation", "anchor_max_error",
            "dual_objective_candidate", "dual_min_eigenvalue", "duality_gap_candidate"]
    out = {key: result[key] for key in keys}
    out["rank_estimate"] = result["realization"]["rank_estimate"]
    out["rank_fits_numerically"] = result["realization"]["rank_fits_numerically"]
    out["gram_reconstruction_max_error"] = result["realization"]["reconstruction_max_error"]
    return out


def numerical_audit():
    e = np.array([1., 0.])
    observations = [Measurement([0., 0.], [-1., 0.])]
    envelope_checks = []
    for L in [0., .05, .25, .49, .5, .51, .75, 1., 1.5, 2.]:
        result = solve_fixed_law(observations, -e, 2, L, direction=e)
        expected = vector_envelope(L)
        error = abs(result["value"] - expected)
        assert error < 3e-6, (L, result["value"], expected)
        assert result["maximum_constraint_violation"] < 1e-6
        a = vector_attainer(-e, L)
        b = vector_attainer(a, L)
        assert np.linalg.norm(vector_attainer(np.zeros(2), L) + e) < 1e-12
        assert abs(b[0] - expected) < 1e-12
        residuals = [np.linalg.norm(a+e)**2-L**2,
                     np.linalg.norm(b+e)**2-L**2*np.linalg.norm(a)**2,
                     np.linalg.norm(b-a)**2-L**2*np.linalg.norm(a+e)**2]
        assert max(residuals) < 1e-12
        # Every pair of sampled inputs also checks the explicit global attainer.
        inputs = [np.array(p) for p in [(-2.,3.), (-1.,0.), (0.,0.), (.3,-.8), (2.,2.)]]
        for x, y in itertools.combinations(inputs, 2):
            assert np.linalg.norm(vector_attainer(x,L)-vector_attainer(y,L)) <= L*np.linalg.norm(x-y)+1e-12
        entry = brief(result)
        entry.update(L=L, expected=expected, absolute_error=error,
                     explicit_attainer_residuals=[float(v) for v in residuals])
        envelope_checks.append(entry)

    scalar_checks = []
    phi = (1+np.sqrt(5))/2
    for L in [0., .1, .5, 1., 1.5, phi, 1.7, 2., 3.]:
        if L <= phi:
            f = lambda x: scalar_t_attainer(x, L)
        else:
            f = lambda x: L*abs(x)-1
        attained = f(f(-1.))
        expected = scalar_envelope(L)
        assert abs(attained-expected) < 1e-12
        grid = np.linspace(-1-L, -1+L, 100001)
        grid_best = float(np.max(np.minimum(-1+L*np.abs(grid), grid+L*np.abs(grid+1))))
        assert grid_best <= expected+1e-10
        assert expected-grid_best < 1e-4
        scalar_checks.append({"L":float(L), "formula":expected,
                              "explicit_attainer":float(attained), "grid_lower_check":grid_best})

    rectangular = solve_fixed_law(observations, -e, 2, 1., direction=e, keep_future_pairs=False)
    assert abs(rectangular["value"]-1) < 1e-6
    scalar_relaxed = solve_fixed_law([Measurement([0.],[-1.])], [-1.], 2, 1., direction=[1.])
    assert abs(scalar_relaxed["value"]-.125) < 1e-6
    assert not scalar_relaxed["realization"]["rank_fits_numerically"]
    # A different objective exercises squared-reference Gram construction.
    squared = solve_fixed_law(observations, -e, 1, .5, reference=-e)
    assert abs(squared["value"]-.25) < 1e-6

    # Nonzero controls and uncertain measured outputs: f(x,u)=.3*x+.4*u.
    controlled_data = [Measurement([0.],[0.],[0.],.05),
                       Measurement([1.],[.7],[1.],.02)]
    controls = np.array([[1.],[-.5],[.25]])
    truth = .2
    for control in controls[:,0]:
        truth = .3*truth+.4*control
    controlled = solve_fixed_law(controlled_data, [.2], 3, .5,
                                direction=[1.], controls=controls)
    assert controlled["value"] >= truth-1e-6
    assert controlled["maximum_constraint_violation"] < 1e-6
    assert controlled["known_span_dimension"] == 1
    assert controlled["unknown_vector_count"] == 5

    equilibrium = solve_equilibrium(observations, .5, e)
    assert abs(equilibrium["value"]+2/3) < 1e-7
    assert np.max(np.abs(equilibrium["centers"]-np.array([[-4/3,0.]]))) < 1e-12
    assert abs(equilibrium["radii"][0]-2/3) < 1e-12
    radius = contraction_radius(observations[0], -e, .5)
    H = tail_horizon(.5, 1., radius, .01)
    assert radius == 3.
    assert radius*.5**(H+1) <= .01
    if H > 0:
        assert radius*.5**H > .01
    return {
        "vector_envelope": envelope_checks,
        "scalar_envelope": scalar_checks,
        "stepwise_relaxation_L1":brief(rectangular),
        "scalar_rank_obstruction_L1":brief(scalar_relaxed),
        "squared_reference_error":brief(squared),
        "controlled_noisy_case": {**brief(controlled), "known_admissible_terminal_value":truth},
        "equilibrium": {"value":equilibrium["value"], "expected":-2/3,
                        "point":equilibrium["point"].tolist(),
                        "radius_bound":radius,"epsilon":.01,"prefix_horizon":H,
                        "tail_error":radius*.5**(H+1)},
    }


def main():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        exact = exact_audit()
        numeric = numerical_audit()
    result = {
        "status":"all_checks_passed",
        "claim_boundary":"Exact symbolic checks verify identities; numerical SDP runs are candidates only.",
        "versions":{"python":platform.python_version(),"numpy":np.__version__,
                    "sympy":sp.__version__,"cvxpy":cp.__version__},
        "exact":exact,"numerical":numeric,
        "solver_warnings":[str(item.message) for item in caught],
    }
    (ROOT / "verification_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status":result["status"],
                      "exact_symbolic_identities":3,
                      "numerical_vector_cases":len(numeric["vector_envelope"]),
                      "numerical_scalar_cases":len(numeric["scalar_envelope"]),
                      "max_vector_value_error":max(row["absolute_error"] for row in numeric["vector_envelope"]),
                      "warnings":result["solver_warnings"]}, indent=2))


if __name__ == "__main__":
    main()
