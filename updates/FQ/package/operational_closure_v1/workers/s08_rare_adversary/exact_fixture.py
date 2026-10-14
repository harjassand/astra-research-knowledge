#!/usr/bin/env python3
"""Exact rational checks for the intervention/native-rate counterexample.

No stochastic sample or physical experiment is simulated.  The Poisson variance
calculation assumes independent, instantly resettable controlled preparations.
"""

from fractions import Fraction as F


def dot(row, vector):
    return sum((a * b for a, b in zip(row, vector)), F(0))


epsilon = F(1, 1024)
boost = F(64)
gamma = F(1, 64)
native_0 = (epsilon, F(0), F(0))  # x, y, z
native_1 = (epsilon, epsilon, F(0))
controlled_0 = (boost * epsilon, F(0), gamma)
controlled_1 = (boost * epsilon, F(0), gamma)
assert controlled_0 == controlled_1
assert sum(native_1) == 2 * sum(native_0)

# Unknown parameter vector theta=(native x, native y, synthetic control z).
# Only unmarked total event counts are used in the witness-control assay.
probe_rows = (
    (boost, F(0), F(1)),  # x exposed, y suppressed
    (F(0), boost, F(1)),  # y exposed, x suppressed
    (F(0), F(0), F(1)),  # synthetic-route calibration
)
target = (F(1), F(1), F(0))
combination = (F(1) / boost, F(1) / boost, -F(2) / boost)
assert tuple(sum((combination[i] * probe_rows[i][j] for i in range(3)), F(0)) for j in range(3)) == target

# Without the third probe, this direction changes the native rate but leaves
# both controlled total rates invariant: acquisition of the nuisance is essential.
unidentified_direction = (-F(1) / boost, -F(1) / boost, F(1))
assert all(dot(row, unidentified_direction) == 0 for row in probe_rows[:2])
assert dot(target, unidentified_direction) == -F(2) / boost

theta = (epsilon, epsilon, gamma)
q = [dot(row, theta) for row in probe_rows]
assert q == [F(5, 64), F(5, 64), F(1, 64)]
reconstructed_rate = sum((combination[i] * q[i] for i in range(3)), F(0))
assert reconstructed_rate == 2 * epsilon == F(1, 512)

# Equal exposure in each controlled probe.  This is statistical variance only;
# it omits setup, calibration, resetting, actuation and energy costs.
exposure_each = F(16384)
controlled_variance = sum((combination[i] ** 2 * q[i] / exposure_each for i in range(3)), F(0))
controlled_relative_variance = controlled_variance / reconstructed_rate**2
native_exposure = 3 * exposure_each
native_relative_variance = F(1) / (reconstructed_rate * native_exposure)
assert controlled_relative_variance == F(7, 8192)
assert native_relative_variance == F(1, 96)

print(f"native rates: H0={sum(native_0)}, H1={sum(native_1)}")
print(f"identical intervention intensities: {controlled_0}")
print(f"probe totals: {', '.join(map(str, q))}")
print(f"reconstructed H1 native rate: {reconstructed_rate}")
print(f"controlled relative variance at 3 x {exposure_each} exposure: {controlled_relative_variance}")
print(f"native relative variance at {native_exposure} exposure: {native_relative_variance}")
print(f"controlled/native relative-variance ratio: {controlled_relative_variance / native_relative_variance}")
