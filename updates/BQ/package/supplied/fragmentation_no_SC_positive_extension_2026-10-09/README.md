# Finite-time fragmentation recovery without small-chipping assumptions

Research extension snapshot, 2026-10-09.

## Result in plain terms

A daughter-size distribution can be recovered from a calibrated distribution
of fragment sizes at one known positive time after starting with one pure size.
The method accounts for repeated fragmentation. It allows common daughter laws
with positive density close to the parent size, where the earlier auxiliary
renewal transform diverges in the continuous model or becomes numerically huge
on a fine grid.

The target is the mean mass-weighted daughter law on the observed size-ratio
window, not the joint sizes of siblings in an individual break. The result
requires a known rate law and calibration; it does not solve simultaneous
unknown-rate and unknown-kernel inference.

The contribution under consideration is stable constructive recovery and a
stated error budget. There is no universal speedup over full-likelihood fitting,
no real-experiment validation, and no certification of novelty or priority.
Constant-rate decompounding, recursive clipping, semigroup conjugacy and
uniformization are established mechanisms; see the source comparison.

## Exact scope

- Known alpha>0, gamma>0 and T>0; rate at log size s is alpha exp(-gamma s).
- Pure monodisperse initial state and no unknown initial-size blur.
- Daughter log-increment density has known upper bound M and bounded variation
  V after extension by zero to negative log sizes. Positive density at zero
  is allowed. No small-chipping integrability condition is imposed.
- Independent calibrated mass-tag endpoint samples, or the same multinomial
  sampling model. Correlated physical descendants and unknown detector bias
  are not covered. A normalized number histogram is not automatically this
  observation model.
- Observed log window (0,L], with the intact atom separate and unseen tail
  retained as a count category. Prefix counts are divided by the original
  sample size, never renormalized after discarding the tail.
- Positive ceiling bins for both jump increments and measured endpoints.
  Their mismatch under repeated jumps is explicitly bounded, not ignored.
- Per-step positivity/density clipping, followed optionally by a disclosed
  mass repair. The prefix can exceed unit mass before repair.

The finite-lattice numerical construction additionally handles gamma=0 and
any known rate profile bounded by its initial rate. The continuum BV theorem
is stated for the power-law model; those extra numerical profile tests are not
silently promoted to a general continuum theorem.

## Guarantees and limitations

`NO_SC_NOISY_RECOVERY.md` derives identifiability and Lipschitz stability on
the bounded-density class, ceiling-binning bias, histogram sampling error,
rate-error effects, clipping propagation and optional mass repair.
With h proportional to N^(-1/3), its expected L1 upper-risk bound is of order
N^(-1/3). This is an upper bound, not a minimax claim. Its constants can be very
large; neither late-time observation nor arbitrary M is uniformly easy.

`STABLE_UNIFORMIZATION_INVERSE.md` gives a nonnegative weighted recurrence.
It never forms the huge renewal coefficients. It sums the one-jump diagonal
exactly, truncates only a positive remainder, and bounds the induced one-sided
data error by an explicit Poisson tail. Arithmetic cost is O(J m^2), storage
O(J m), with truncation order J explicitly selected. Bit complexity must also
include working precision; O(m^2) bit complexity is not claimed.

The conditional rounding analysis assumes the stated relative-error model,
accurate exp/expm1, and no underflow/overflow. It is not an interval certificate
for NumPy or BLAS. Under those assumptions the precision budget has no
singularity as gamma tends to zero. Large time times prefix mass can still
require higher precision.

For numerical data-error budget epsilon_num (series tail plus rounding defect),
the combined bound is the original displayed risk bound with epsilon_num
added to the endpoint-error terms. In particular, with exact rates:

    E ||estimated density - true density||_L1(0,L)
      <= h V + 2 C_inv [sqrt(m/N) + h C_forward + epsilon_num].

## Check status

The original small-chipping theorem passed one focused AI-assisted mathematical
check; not external expert review or formal certification. That original
result and archive are separate and unchanged.

This extension was derived and self-checked by the research AI and reviewed
mathematically by the coordinating AI. It received no separate audit, no
external expert review and no formal certification. The new proofs and
finite-precision argument should be treated as research claims with the exact
assumptions shown, not as an externally certified theorem or software product.

## What the targeted tests show

- Ordinary renewal inversion can fail badly near constant rates; 80-digit
  arithmetic was needed in one recorded gamma=.02 case.
- The positive double-precision inverse agreed with the 100-digit causal
  inverse within 2.6e-16 even with renewal coefficients about 2.7e40.
- Constant-rate and arbitrary finite-rate-profile cases agree with independent
  dense matrix exponentials to approximately machine precision.
- At 1001 bins a positive sweep had a one-sided forward defect below 2e-15.
- A matched capped full-likelihood fit used an efficient analytic adjoint and
  both cheap and direct-inverse initializers. In four fixed realizations its
  L1 error was 0.02–2.2% lower. It sometimes reached the direct method's error
  almost as quickly. No uniform speed or statistical-efficiency claim follows.

See `MATCHED_BASELINE_COMPARISON.md`; raw arrays and all optimizer traces are
included. Continuous-model binning/noise checks are separately recorded in
`no_sc_noise_results.json`. They are synthetic, not laboratory validation.

## Reproduce

Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0 were already installed.
Exact package versions are in `requirements.txt`. No paid or external compute
is needed. From this directory:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python no_sc_noise_test.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python positive_inverse_test.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python positive_fit_benchmark.py

These commands overwrite their result JSON files and logs if redirected.
Preserve this archive if the exact original timing outputs are required.
The source file `reference_extension_test.py` is included because its
independent continuous forward quadrature is imported by the noisy test;
the provisional reference-intertwiner proposal is not needed for this result.

`EXTENSION_SHA256.json` lists per-file hashes. The separate original SC archive
has SHA256 e203dc03a3b77a738cf48c0b1dcd349bcd9c5717811d7620db4d617644f75e76.
The earlier pre-redesign no-SC snapshot has SHA256
92996734af9bec222857af8a468957fb426a297fbe23f9667792242fe1314695.
