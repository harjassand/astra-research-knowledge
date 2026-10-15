# Reproduce the certified compact law

Requires Python 3, NumPy, SciPy. No package installation is performed by these scripts. Run from any directory:

    OPENBLAS_NUM_THREADS=1 python /path/to/heterogeneous/dyadic.py
    OPENBLAS_NUM_THREADS=1 python /path/to/heterogeneous/certify.py
    OPENBLAS_NUM_THREADS=1 python /path/to/heterogeneous/package_law.py
    python /path/to/heterogeneous/moments.py

`dyadic.py` produces an exact dyadic rate histogram and floating candidate roots. Floating failures are skipped, not silently certified; `certify.py` accepts only exact integer sign and mass bounds, and bounds all remaining mass by subtraction. It does not need a proof that every floating candidate was found.

`compact_law.json` is the deliverable: exact atom and rational component probabilities, rational positive exponential rates, an exact rational failure bound, and an exact rational total relative error bound. This is a certified law representation, NOT an implementation of certified finite-random-bit exponential draws. `package_law.py` benchmarks ordinary floating draws separately.

The current certified prefix acquisition processed 304 roots in 4.9055 seconds; exact histogram compilation took .1180 seconds, and scanning floating candidates took .4212 seconds. These timings are observations from this execution environment. The earlier full acquisition processed 1,894 roots in 38.877 seconds; `full_mixture_certificate.json` retains that run.

The coupling from the original rational 128-component family to the delivered law has relative error at most 0.031991361899 (conservative displayed decimal) except on probability at most 4.851373100e-7. The exact values are stored in `compact_law.json`. The zero atom remains exactly 2^-128, because the uncertified residual probability is assigned to a positive component rather than to zero.

`moment_certificate.json` certifies that the original model's qB/A² lies in [.39031,.44271] and its mean-matched, atom-preserving exponential has a Laplace gap at least .142437 at a specified physical argument. `moments.py` derives these bounds from exact fixed-point sums and the deterministic rate compiler enclosure.

`test.py` and `reduction.py` are supplementary floating experiments. Small exact subset transforms and selected Laplace points are validation, not substitutes for a coupling certificate. `reduction.py` includes the earlier unprotected floating full-root experiment, which can fail at near-pole roots; the main pipeline deliberately replaces that approach.

See NOTES.md for the construction, limitations, baseline comparisons, and prior-work boundary. No assertion of physical-model validity, first discovery, or superiority to all hybrid approximation methods is made.
