#!/usr/bin/env python3
"""P1 task-contrast cut: conditional finite-sample check.

This program verifies arithmetic of a theorem conditional on independently
qualified PHYSICAL bounds; it cannot qualify a physical interface itself.
No latent-mode rank or microstate reconstruction is used.
"""
from __future__ import annotations
import argparse
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    gap_hat: float
    statistical_radius: float
    physical_contrast_error: float
    decision_margin: float
    result: str


def tv_leakage(rho: float, gamma: float, diff: float, duration: float,
               code_error: float = 0.) -> float:
    """Pinsker/Girsanov bound for constant noise sqrt(2D) and |drift leak|<=gamma.

    rho = total variation error in the reference initialization.
    code_error = worst-case probability of a wrongly decoded task label.
    Independent bounds have to be physically justified, never fitted by this code.
    """
    assert 0 <= rho <= 1 and 0 <= code_error <= 1
    assert gamma >= 0 and diff > 0 and duration >= 0
    return min(1., rho + code_error + gamma * math.sqrt(duration / (8. * diff)))


def check(k_a: int, n_a: int, k_b: int, n_b: int,
          delta: float, eta_a: float, eta_b: float) -> Result:
    """Simultaneous two-sided Hoeffding CIs and task-contrast leakage bound.

    Selection of arm a is valid only if the confidence margin is positive.
    The guarantee is conditional on all independently established physical
    premises, independent one-stage Bernoulli trials, and action costs.
    """
    assert 0 < delta < 1
    assert 0 < n_a and 0 < n_b and 0 <= k_a <= n_a and 0 <= k_b <= n_b
    assert 0 <= eta_a <= 1 and 0 <= eta_b <= 1
    gap = k_a / n_a - k_b / n_b
    ra = math.sqrt(math.log(4. / delta) / (2. * n_a))
    rb = math.sqrt(math.log(4. / delta) / (2. * n_b))
    margin = gap - ra - rb - eta_a - eta_b
    decision = 'a_dominates_b_CONDITIONAL' if margin > 0 else 'UNRESOLVED'
    return Result(gap, ra + rb, eta_a + eta_b, margin, decision)


def tests() -> None:
    assert abs(tv_leakage(0, 0, 0.29, 1)) < 1e-15
    assert abs(tv_leakage(.01, 0, .29, 1, .02) - .03) < 1e-12
    result = check(3100, 5000, 2500, 5000, .01, .02, .02)
    assert result.result == 'a_dominates_b_CONDITIONAL'
    assert .025 < result.decision_margin < .04
    no_decision = check(510, 1000, 500, 1000, .01, .01, .01)
    assert no_decision.result == 'UNRESOLVED'
    # The uniform interface constraint does not depend on the latent mode count.
    arbitrary_modes = [(-1) ** i * 1e-9 for i in range(1000)]
    assert all(.12 + x > 0 for x in arbitrary_modes)
    print('PASS: arithmetic and one-sided decision logic; no physical interface certified')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tests', action='store_true')
    ap.add_argument('--ka', type=int)
    ap.add_argument('--na', type=int)
    ap.add_argument('--kb', type=int)
    ap.add_argument('--nb', type=int)
    ap.add_argument('--delta', type=float, default=.01)
    ap.add_argument('--rho', type=float, default=None,
                    help='Physically established initial TV error; REQUIRED')
    ap.add_argument('--gamma', type=float, default=None,
                    help='Physically established max residual drift (length/time); REQUIRED')
    ap.add_argument('--diff', type=float, default=None,
                    help='Diffusion coefficient (length^2/time); REQUIRED')
    ap.add_argument('--duration', type=float, default=None,
                    help='Terminal action path duration (time); REQUIRED')
    ap.add_argument('--code-error', type=float, default=None,
                    help='Physically established misdecode bound; REQUIRED')
    args = ap.parse_args()
    if args.tests:
        tests()
        return
    required = ('ka', 'na', 'kb', 'nb', 'rho', 'gamma', 'diff', 'duration', 'code_error')
    missing = [x for x in required if getattr(args, x) is None]
    if missing:
        ap.error('missing required acquired data / physical bounds: ' + ', '.join(missing))
    eta = tv_leakage(args.rho, args.gamma, args.diff,
                     args.duration, args.code_error)
    r = check(args.ka, args.na, args.kb, args.nb, args.delta, eta, eta)
    print(f'Observed contrast: {r.gap_hat:.8g}')
    print(f'Simultaneous statistical error <= {r.statistical_radius:.8g} (1-delta)')
    print(f'Conditional physical contrast error <= {r.physical_contrast_error:.8g}')
    print(f'Lower action-contrast margin: {r.decision_margin:.8g}')
    print(f'DECISION: {r.result}')
    print('WARNING: This is conditional mathematics; physical bounds are not validated by this script.')
    print('WARNING: Applies only to the rearchitected terminal action, not unchanged latent-mode source.')


if __name__ == '__main__':
    main()
