# Independent review of continuous learned-inverse control

28 October 2026. Accepted as an explicit finite-channel model and changed-clock comparison, conditional on received code-boundary, EC and adaptive single-carrier dependencies. No new calibration data, physical measurement or hardware advantage is established.

## Executed control, not a free saved matrix

The reviewer independently multiplies complex Z/Y/Z unitaries from every saved angle and checks equality up to phase to each acquired W-dagger. Every local pulse duration is abs(theta)/pi + .2; all layer maxima and padded intervals are independently recalculated. The saved matrices are in the specified nonsingular Euler chart; a general compiler needs its stated zero-entry branches.

The declared Hamiltonian during each interval is H=[(1+epsilon)theta sigma_axis + eta X]/(2d). The independent checker constructs the complex 4-by-4 column-vectorized Lindblad generator

    -i(I tensor H - H^T tensor I) + (lambda/2)(Z^T tensor Z-I),

exponentiates it, applies it to each Pauli input and converts back to a real PTM. This differs from the author's real 3-by-3 Bloch cross-product generator. All 45 actual pulse cases (three errors, five sites, three layers) agree to floating roundoff; trace preservation and Choi positivity are checked. The dissipative factor is lambda, not twice lambda, on X/Y. Hamiltonian rotation and dephasing act simultaneously in this pulse model.

The advertised pi speed bound is NOMINAL commanded rotation speed. Multiplicative error and the extra eta X field can increase actual norm slightly; the author explicitly labels the nominal bound and states all error fields. The .2 switching allowance is part of a rectangular driven interval, not claimed separate pulse-off time. These qualifications are necessary if converting dimensionless values to a physical device.

## Full physical composition

The independent replay assembles native maps directly from the saved source Kraus matrices, then uses its own complex pulse solutions and padded dephasing. It propagates full five-qubit coordinates by the full tensor native map, not by the author's local routine. Actual physical states, including residual syndrome sectors, are carried through all 32 uses; only the separately received full EC primitive is reused. Independent density-matrix implementations supply preparation, encoding, terminal inverse-Clifford gates, immediate measurement branches, feedback and physical correction. All three complete output PTMs agree within 2e-13. This is a floating replay, not interval arithmetic.

The clock recomputes to 3425.787242023335 units, including 72 boundary units, 32 native-plus-pulse phases and 16 EC windows. The former 203-unit cycle convention is not reused. In the zero-background/control-error limit the pulse compilation reduces to the old native-plus-learned-inverse map, as independently checked against the saved target matrices.

The native source is still a supplied discrete map followed by one unit's background dephasing, both assigned to one declared effective native phase. It is NOT derived from simultaneous microscopic native evolution and dephasing. The exact continuous-time assertion belongs only to the controlled pulse segments. A laboratory realization must validate or measure the composite native operation rather than infer it from this calculation.

## Changed-clock one-carrier bound

For one retained qubit, the accepted concurrence theorem gives factor sqrt(1-gamma) for each compulsory native channel and exp(-lambda*d) for each fixed dephasing interval. Local ideal controls and classical-history instruments do not increase average concurrence. For a driven dephasing interval, a Lie-Trotter product of infinitesimal unitary control and fixed dephasing factors has the same exp(-lambda*d) upper bound; continuity passes it to the finite-dimensional Lindblad limit. Thus granting arbitrary ideal controls cannot remove this Markovian contraction while the stipulated noise exposure remains fixed.

The appropriate total factor is (399/401)^32 exp(-lambda*3425.787242023335), including the native-phase background, all padded pulses, EC time and the extra 72 input/output units. This yields F_e<=.7555188634395273. The independently replayed encoded fidelities are approximately .815747556, .815570293 and .804106807 for epsilon=0,.001,.01, respectively. These are numerical separations within the declared model and resource restrictions, not acquired empirical confidence bounds.

The comparator may know the source, use free ideal controls and arbitrary genuinely classical records. It may not retain a spare quantum carrier, bypass compulsory native exposures, access the noise environment or alter the stipulated dissipative generator. It compares one carrier with redundant coded quantum resources; a conventional multi-qubit implementation can run the identical code and controls. No equal-resource algorithmic superiority follows.

## Limitations preserved

The new pipeline changes the executed channel. Previous ideal-boundary or ideal-inverse holdouts cannot certify it. A fresh test at actual physical input/output planes, with trusted/calibrated external SPAM and an appropriate stationarity/confidence contract, is needed for acquisition claims. Noise parameters and Hamiltonian calibration in this file are declared model inputs, not learned environment data. Unknown input injection and output errors remain first-order costs. Native bath memory, leakage, crosstalk, connectivity, controller faults, finite precision and energy are not silently resolved. The terminal instrument successor is outside this receipt unless separately reviewed.
