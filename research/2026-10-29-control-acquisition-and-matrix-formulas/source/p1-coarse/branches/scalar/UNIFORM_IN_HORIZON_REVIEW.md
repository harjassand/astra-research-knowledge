# Scoped independent review: uniform temporal scalar certificate

28 October 2026. Reviewed the stated theorem and the following exact code
versions, without importing their verifier into the independent replay:

- `core/echo_compiler.py`, SHA256
  `ac24ed8be0b510aeab61d80a60ce3a0345f8bbf33cb97b8b74ee2562fc4a8677`.
- `core/uniform_certificate.py`, SHA256
  `037c6786fcfbeed551bf8774474f645389e445c4247d464d0ec351731b3fd9ba`.
- Executed result `results/ECHO_EXPERIMENT.json`, SHA256
  `af91b8050d2d0796c2e4f845289249b6984cb27b3ed1bee16cbca6ba2af9483b`.

**Finding:** the uniform theorem and reported finite matrix witnesses are
sound under their stated exact-input, source and simultaneous-interval
premises. No mathematical defect was found in the reviewed implementation.
This is an independent internal algebra/code review and source-free replay
from decoded intervals. It is not a physical or complete experimental audit.

## 1. Hypotheses and exact residual identity

Use the notation and independently checked identity in
`TEMPORAL_SIGNED_CORRECTION_REVIEW.md`. The source operators A_i are actual
selfadjoint contractions in a common Hilbert metric, b=Vc0, and scalar echo
intervals cover one fixed source. The coefficient maps T_i are arbitrary
chosen rational matrices. Let the chosen computational metric W be positive
definite and suppose, for one 0<=rho<1,

    T_i^T W T_i <= rho² W,
    R_i=(A_i V-V T_i)^T(A_i V-V T_i) <= epsilon² W.           (1)

W is a computational metric. It need not equal the true Gram G, and no
positive lower eigenvalue of the true G is a premise. The source may have
infinite hidden dimension and hidden eigenvalues at or arbitrarily near one.

The exact signed output correction leaves the pairwise remainder

    f(w)-ftilde_true
      =sum_(t<s) (E_(i_s) beta_s)^T
        A_(i_(s-1))...A_(i_(t+1)) (E_(i_t) alpha_t),          (2)

where E_i=A_iV-VT_i, alpha_t is the learned prefix before operation t,
and beta_s is the learned reversed suffix after operation s.

## 2. Uniform residual bound

The learned contraction in (1) gives

    ||alpha_t||_W <= rho^(t-1)||c0||_W,
    ||beta_s||_W <= rho^(H-s)||c0||_W.

Using the actual hidden contractions only for the middle product in (2),
its pair (t,s) has magnitude at most

    ||c0||_W² epsilon² rho^(H-s+t-1).

For fixed ell=H-1-(s-t), there are exactly ell+1 such pairs, and ell ranges
from 0 through H-2. Thus for H>=2,

    |f(w)-ftilde_true|
      <=||c0||_W² epsilon² sum_(ell=0)^(H-2)(ell+1)rho^ell
      <=||c0||_W² epsilon²/(1-rho)².                        (3)

For H=0 or 1 the pair remainder is zero, so the same uniform upper bound is
still valid. rho=0 is allowed, with the usual finite-product interpretation
of zero-length products; direct treatment avoids any 0^0 ambiguity.

The proof does not need a hidden spectral gap. The gap is in the proposed
coefficient dynamics and is actually checked. This is not a promise that
every source admits an accurate certificate with a useful rho. A source
with persistent strongly observable memory will force a large residual or
a coefficient rho close to one, so (3) becomes weak. The prior precision
witnesses remain compatible with this theorem.

## 3. Uniform measurement contribution

Let Gbar,Mbar_i be the matrix midpoints induced by the same raw-word
midpoints. Suppose the actual errors obey

    ||W^-1/2 (G-Gbar) W^-1/2|| <= gamma_G,
    ||W^-1/2 (M_i-Mbar_i) W^-1/2|| <= gamma_M.                (4)

Set D_i=M_i-GT_i. The induced midpoint defect error has norm at most

    gamma_M+rho*gamma_G,

because the normalized T_i has norm at most rho. The midpoint discrepancy
in the uncorrected scalar term is at most

    ||c0||_W² gamma_G rho^H.

Each of the H correction terms is at most

    ||c0||_W² (gamma_M+rho gamma_G)rho^(H-1).

For H>=1, H rho^(H-1) <= sum_(j=0)^(H-1)rho^j <=1/(1-rho).
The H=0 case contains only the Gram term. Therefore

    |ftilde_true-ftilde_midpoint|
      <=||c0||_W² [gamma_G
          +(gamma_M+rho gamma_G)/(1-rho)].                  (5)

Combining (3) and (5) proves the total reported uniform certificate for every
finite word. The midpoint predictor is the signed-corrected scalar linear
functional. Canonical raw-word aggregation in `EchoCompiler.certificate`
gives exactly the same midpoint: centers of exact interval linear
combinations are their linear combinations of centers.

Uniform validity over finite words does not grant a stable source for an
unlimited calendar-time reuse epoch. Reset, calibration and source stability
must continue to hold for the intended physical reuse interval.

## 4. Code-level obligations checked

### Exact residual matrix upper bound

For each R_i entry, the code constructs the actual scalar linear expression

    N_i[j,k] - (M_i T_i)[j,k] - (T_i^T M_i)[j,k]
              + (T_i^T G T_i)[j,k].

The shared-word coefficients are aggregated before applying raw intervals.
The resulting interval matrix is symmetric. Let Rbar be its midpoint and
r_jk its entry radii, and put d_j=sum_k r_jk. Every compatible symmetric
matrix R_i satisfies

    R_i <= Rbar+diag(d),                                    (6)

because for every x,

    |x^T(R_i-Rbar)x| <= sum_jk r_jk |x_j x_k|
      <=sum_j d_j x_j².

The last step uses symmetry and 2|x_jx_k|<=x_j²+x_k². The same argument
bounds both signs of the raw Gram/moment perturbations. Exact dominance of
diag(d) by gamma W therefore establishes (4).

### Rational Schur PSD check

`psd` performs symmetric rational Schur elimination. A negative pivot is
incompatible with PSD. A zero pivot requires every remaining entry of its
column to vanish, also necessary for PSD; otherwise it rejects. Positive
pivots reduce PSD to the smaller Schur complement. `strict=True` requires
positive pivots and therefore verifies W positive definite. Within the
stated rational-input contract the arithmetic is exact.

### Numerical proposals are not proofs

`dominate` uses a floating generalized eigenvalue only to propose a rational
scalar. It returns only after the rational Schur test verifies qW-A>=0.
A poor numerical proposal can cause a failed call or exhausted proposal
budget; it cannot establish a false matrix inequality. This is a sound
certificate-producing routine, not a proof that the numerical proposal
stage always terminates successfully for every feasible instance.

The exact API contract matters: T_i, W, rho and interval endpoints must be
rational/integer inputs, as supplied by the reviewed experiment. The modules
do not provide a general input-validation layer that converts arbitrary
floating/malformed user arrays into exact scientific objects. This is not a
defect in the present rational execution, but should remain explicit if the
code is exposed as a public interface.

## 5. Independent source-free replay of the finite witnesses

`review_uniform_certificate.py` reads only the saved decoded intervals,
coefficient maps and certificate payloads. It imports neither Root's compiler
nor its PSD test. It independently builds residual entry expressions from
raw words, aggregates identical words, propagates intervals, reconstructs
(6), and checks every matrix inequality by **all principal minors** for the
reported three-dimensional coefficient spaces. It also independently checks
the common coefficient contraction, Gram/moment radius dominance and final
arithmetic of (3)-(5).

All four published fixtures pass. Their certified uniform absolute bounds are:

| Fixture | Uniform bound |
| --- | ---: |
| Weak hidden modes | 0.0009381979599404319 |
| Very slow hidden modes | 0.00004165929999735496 |
| Biased proposal with signed correction | 0.001791782059886236 |
| Higher measurement error | 0.06908358615769804 |

The exact fractions and code/result hashes are retained in
`UNIFORM_CERTIFICATE_REVIEW_CHECKS.json`. The finite replay verifies the
published witnesses; the all-word quantifier follows from the ordinary proof,
not from enumerating target words.

## 6. Scope and contribution boundary

Completed here: independent proof of the uniform residual and measurement
bounds, inspection of the exact certificate path, and independent exact
reconstruction/replay of four published witness sets from decoded intervals.

Not covered here: raw-standard calibration decoding, physical realization of
the common selfadjoint amplitude interface, source stability beyond the
assumed epoch, acquisition of arbitrary sources, universally efficient
proposal/basis discovery, or comparison of full physical costs. Finite echo
query counts still do not acquire their required precision.

The signed correction and primal-dual residual principle have established
model-reduction precedents; sources are listed in the preceding temporal
review. The load-bearing potential addition remains scalar echo acquisition
of the needed forms and their exact data-coordinate certification. The
uniform result shows that a certified finite **computational** contraction
can replace a hidden-system gap in this scalar error bound. It should be
presented at that conditional scope rather than as a generic resolution of
unbounded-time system identification.
