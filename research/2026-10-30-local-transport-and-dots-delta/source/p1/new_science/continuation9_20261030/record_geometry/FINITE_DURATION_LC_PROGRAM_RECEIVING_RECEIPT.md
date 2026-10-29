# Receipt of the independent finite-duration LC review

The existing physical-mechanism role independently reviewed the actual
`FINITE_DURATION_LC_PROGRAM.md`, SHA-256
`49acbebb439b5eaa2305ee273239101316261d4875be45015f188f8a744b8cf2`.
I read its completed review at
`../physical_mechanism/receiving_review/FINITE_DURATION_LC_PROGRAM_RECEIVING_REVIEW.md`,
SHA-256 `ada64edabd3746c5de4d4756bace45c53d0232c17dfb5609d74add363b42c0e5`.
That directory preserves the exact reviewed input snapshot and review manifest.

The receiving decision accepts the homogeneous Gaussian program, its explicit isolated finite-duration bath operation, the low-wave-number heat receiver with full elapsed time, the Gaussian density-path action, and the whole-path harmonic native-current constraint. It does not accept an unmeasured composition through an unknown resistor, a hard amplitude or frequency cap, arbitrary hidden rates, or unmodeled schedule faults.

The review supplies a precise interpretation of the optional smooth-envelope sentence. If a common envelope c(t) multiplies the entire transport Hamiltonian generator, the actual native current during that segment is `dJ=c(t)v(t)dt`; the density continuity equation is `dx=c(t)Bv(t)dt`, and h denotes the integrated transport duration. The isolated bath stage still has zero native current. Keeping `dJ=vdt` while scaling the density equation would violate the actual current accounting and is not the claimed program.

This clarification is adopted here without changing the independently reviewed original proof. The fully specified piecewise-constant schedule in that proof needs no modification. A concrete joint path topology accepted in the review is `C([0,T],H^{-s})` for each of density and integrated current, with `s>3/2`.

No additional fixture, rerun, or new research claim is introduced by this receipt.
