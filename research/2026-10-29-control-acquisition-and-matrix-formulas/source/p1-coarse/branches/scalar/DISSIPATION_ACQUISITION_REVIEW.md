# Independent review: finite acquisition of inverse-dissipation residuals

28 October 2026. Scope: the new finite scalar acquisition in
core/dissipation_certificate.py and its recorded fixtures. This review proves
the finite-tail and interval steps, and checks their implementation. The
physical energy theorem that consumes Q<=theta^2 R is under separate review;
the previously accepted signed compiler and its measurement allowance are
not re-audited here.

## Finding

For selfadjoint A, a warranted bound ||A||<=a<1, nonnegative integer depth K,
and every action covered by its own warranty, the finite acquisition is
sound. The ordinary matrix inequalities below are sufficient; no hidden
dimension, exact hidden rank or dictionary Gram inverse enters the learner.

All 12 scalar records in the current results file were independently
replayed using exact rational arithmetic. This includes five source scales,
three fixed-source noise cases, and four additional depths. A separate
two-column example checked the matrix implementation with nonsymmetric
coefficient maps, a nonidentity metric and a true action with a negative
eigenvalue.

The review initially found missing guards for a short norm-bound list and
negative depth. Both guards were added and their rejection behavior was
independently verified. No issue remains in the reviewed finite acquisition.

Final reviewed SHA256 values:

- core/dissipation_certificate.py:
  a06e4f6fa789d76c351bf5cb34023dcbfd58f74a8ef54e2a79d52bc5b73bdf1b
- core/run_dissipation_experiment.py:
  63e6b2f89fe387cacced55a995fb9af9d8cf5cba5152764f1bd0684e511fcf80
- results/DISSIPATION_EXPERIMENT.json:
  e72d9b712284db24dcefd71bc4d744aa56bca58052f2e94ba92192c7858d5850

## 1. Finite spectral tail

Let D=AV-VT and B=A^2. Selfadjointness and ||A||<=a imply

    0<=B<=a^2 I<I.

For every integer K>=0, with the empty sum understood at K=0,

    (I-B)^(-1) = sum_{k=0}^{K-1} B^k + B^K(I-B)^(-1).

The last factors commute. Since (I-B)^(-1)<=(1-a^2)^(-1)I,

    (I-B)^(-1)
      <= sum_{k=0}^{K-1} B^k + B^K/(1-a^2).

Congruence by D proves exactly the proposed inequality

    Q=D*(I-A^2)^(-1)D
      <= sum_{k=0}^{K-1} D*A^(2k)D + D*A^(2K)D/(1-a^2).

No positivity of A itself is required. The even powers are positive, and
all these operators are functions of the same selfadjoint A. Commutation
must not be dropped when transferring this proof to a different operator
or nonsymmetric construction.

At exact noiseless moments the right side decreases with K. Its difference
between depths K and K+1 is

    D* B^K (a^2 I-B) D/(1-a^2) >= 0.

Interval-padded upper bounds need not be monotone with depth: additional
moments carry additional measurement uncertainty. The implementation does
not assume this monotonicity.

## 2. Native moment orientation and coefficient aggregation

For real coefficient vectors x,y, direct expansion gives

    x*D*A^(2k)Dy
      = (Vx)*A^(2k+2)(Vy)
        -(Vx)*A^(2k+1)(VTy)
        -(VTx)*A^(2k+1)(Vy)
        +(VTx)*A^(2k)(VTy).

The left transform is Tx, not T*x. Its transpose is already produced by
the bilinear inner product. Thus the code's separate tl=T left and
tr=T right have the correct orientation even for nonsymmetric T.

For dictionary words w_j, the inner product
(Vx)*A^p(Vy) uses the chronological word

    w_right + action^p + reverse(w_left).

Real scalar reversal and selfadjoint primitive operations justify the
canonical reversal used by the established echo interface. Off-diagonal
entries use the same native scalar observations when exchanged, as required
for a symmetric form.

The implementation accumulates every k term, including the weighted tail,
into one expression before evaluating intervals. Hence coefficients of a
repeated native word combine before absolute interval errors are charged.
This includes coincidences between different k values and coincidences
within a defect square. It does not assume independent measurement errors.

The independent replay used another representation: expand each state
D e_j as A V e_j minus a linear combination of dictionary states, append
k actions, and then form pairwise inner products of those expanded states.
This checks the new three-moment formula against a direct state construction,
rather than copying its expansion.

## 3. Matrix interval domination and exact computational budget

Let P_K be the finite form on the right side of the tail inequality.
Suppose C is its entrywise interval midpoint and r_jk its radius.
The native expressions imply C and r are symmetric. For the actual
Delta=P_K-C and any real x,

    x*Delta x <= sum_jk r_jk |x_j||x_k|
               <= sum_j (sum_k r_jk) x_j^2.

Thus

    P_K <= C+diag(row-radius sums) = Q_upper,

and consequently Q<=Q_upper. The use of row sums is correct here precisely
because the form and its interval radii are symmetric. A genuinely
nonsymmetric bilinear-form interval would require a different argument.

The computational budget is R=W-T*WT. The implementation requires W>0
and R>0, then proposes theta^2 numerically and accepts it only after an
exact rational positive-semidefinite check of theta^2 R-Q_upper. Therefore
the accepted inequalities imply

    D*(I-A^2)^(-1)D <= theta^2(W-T*WT).

Numerical eigenvalues only propose theta^2. They do not certify the
inequality. Failure to find a suitable rational domination can fail the
routine, but cannot turn the exact acceptance test into an approximate one.
The strict positivity of R is a limitation of this numerical proposal
routine; it is not established here as necessary for the underlying energy
theorem.

## 4. Independent record replay

The checker reconstructed each decoded interval directly from the two raw
standards and each raw report. It independently checked calibration signs,
all four interval-division corners and exact agreement with the saved
decoded endpoints. It then reconstructed every native moment expression
and its upper endpoint.

For every action in all 12 scalar fixtures it verified, exactly,

    Q_actual <= P_K_actual <= Q_upper <= theta_i^2 R_i.

It independently recomputed Q_actual from the stated two-dimensional source,
solely as a checker, and matched the saved checker value. The learner never
receives that hidden matrix. The source-norm warranty was verified for these
synthetic checker matrices by exact 2-by-2 principal-minor inequalities.

The two-column check additionally verified every off-diagonal expression,
symmetry of midpoint and radius matrices, the row-radius upper matrix,
and all three matrix differences by exact principal minors. Its coefficient
maps are nonsymmetric, so a mistaken left transpose would not be masked by
the scalar fixture.

For one reset dictionary column and two actions, the acquisition requests
all powers 0 through 2K+2, with the empty word shared. Hence

    source readings = 4K+5,
    primitive applications = (2K+2)(2K+3),
    maximum word length = 2K+2.

At K=8 this is 37 source readings, 342 primitive applications and maximum
length 18, plus two calibration standards. This accounts for the reported
39 total readings.

## 5. Numerical conclusions and their precision premise

At g=1/1000, K=8 and raw ADC radius 10^(-14), the replay exactly reproduces

    new all-word bound = 0.001069085762,
    previous bound on the same model/data = 1.000002004017664.

This comparison is conditional on the separate energy theorem and reuses
the previously accepted measurement allowance. The new acquisition supplies
the inverse-dissipation premise for that theorem.

The fixed-source precision sweep is material:

| Raw ADC radius | New bound, K=8 |
| --- | --- |
| 10^(-14) | 0.001069085762 |
| 10^(-10) | 0.002211425394050125 |
| 10^(-8) | 0.11531546861891181 |
| 10^(-6) | 11.435596985982395 |

The final row is vacuous for unit-scale responses. Thus 37 readings do not
purchase the required instrument precision. Calibration errors and source
errors remain correlated bounded quantities, not independent noise that
repetition is assumed to reduce.

At fixed g=1/1000 and raw radius 10^(-10), depths 0,1,2,4,8 yield new bounds
approximately 1.00168, 0.0646908, 0.00738278, 0.00222650, 0.00221143. The
short powers expose the residual's fast decay, while the final depths
approach the available noise floor. This is a useful witnessed improvement;
it does not establish an unrestricted physical runtime advantage.

## 6. Warranty and API boundaries

The strict source norm bound is an external premise. It is not inferred
from these finitely many scalar observations, and the numerical simulator's
check is not a physical warranty. It is sufficient to know such a bound on
the relevant invariant physical subspace, provided that subspace and the
inverse are defined appropriately; the implemented statement uses the
simpler full-operator warranty.

Observable data alone cannot generally certify a full hidden-operator norm:
an unobservable invariant sector can be appended without changing any
observed scalar word. Therefore this construction must not inherit the
earlier compiler's lack of a strict source-gap premise. It adds a new
conditional capability.

The finite-tail algorithm requires K to be a nonnegative integer and a norm
warranty for every action whose words it certifies. Initially those two
input contracts were not enforced. A short warranty list silently skipped
actions while still labeling the result as an all-word bound. Negative K
also invalidated the Neumann identity, because Python negative tuple
repetitions silently became empty words. These are material guard
requirements for a reusable routine, although none of the recorded fixtures
uses such inputs. The final code rejects both invalid calls, as verified
in DISSIPATION_REVIEW_CHECKS.json.

## Review boundary

The finite acquisition theorem, interval orientation, exact matrix upper
bound and recorded inequalities are independently checked. The new
energy/Julia theorem itself, a physical realization of the norm warranty,
measurement precision acquisition and complete hardware costs remain
outside this scoped review. No general hidden-system identification or new
general Neumann-series principle is claimed.
