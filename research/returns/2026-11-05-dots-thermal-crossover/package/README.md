# Finite-size crossover addendum

**Status:** Conditional on the delivered provisional base proof, *Exact accepting polymers and a fixed-temperature undecidable order parameter in two dimensions*. Both remain research proofs with internal audit only, not external peer review or formal verification.

`NOTE.md` gives the finite-volume experiment and full corollary proof. `SOURCES.md` distinguishes its assumptions from earlier literature.

The main statement is that a fixed infinite-volume odd-correlation decay bound does not yield a total computable finite-size crossover bound for this specified family and boundary experiment. It makes no claim about physical sample complexity, Monte Carlo mixing time, arbitrary perturbation robustness, or arbitrary delay at one fixed alphabet size.

## Reproduce the checks

Run `python check_constants.py` using Python 3. No external packages or network access are needed. It writes `numerical_checks.json`.

The checks certify the contour-series inequalities using exact rational arithmetic, verify the numerical decision gap, and enumerate the plus-boundary single-layer Ising model for square sides 1–4. The finite partition sums use floating-point arithmetic. None of these calculations establishes the base theorem or the asymptotic corollary: those are the mathematical arguments in the manuscripts.
