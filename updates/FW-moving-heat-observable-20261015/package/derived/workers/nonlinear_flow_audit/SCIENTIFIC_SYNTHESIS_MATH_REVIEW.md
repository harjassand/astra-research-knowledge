# Scientific synthesis: mathematical claim and promotion audit

15 October 2026. Same-team internal analytic review. The root synthesis is
an evolving draft; this review is tied to exact bytes rather than later edits.

Initial inspected draft SHA-256:
`9c1f42392f6c798e815ee8a528b19ae0df4fd72afd314bf0eb737b171efc753d`.
Re-read updated draft, copied as `SCIENTIFIC_SYNTHESIS_REVIEWED_v0002.md`,
SHA-256:
`8310cd8faa7fb865253b3970b59949db5a3c907c00c63482b6053276101babe5`.

**Verdict:** the updated principal mathematical and coercivity/storage
sections are supported by the current internally checked proofs. The earlier
missing restriction on the H-remainder coercivity claim was repaired: it
now explicitly assumes the negative-delta two-LMI hypotheses. The universal
exact certificate auditor has now reported PASS, so the universal QC claim
is no longer resting on pending algebra. External correctness, historical
priority, boundary coercivity and the positive-delta QC branch remain open
as stated. One minor reference-bridge precision clarification is recommended
below; it does not change the proven mathematical results.

## 1. Principal cone theorem and generators

The contact span is four-dimensional, and its ambient nine-dimensional
left-SO(2)-invariant ROC cone is correctly specified. Both acoustic necessity
tests, the universal sharp-ray ROC factorization, and the exact coefficient
decomposition justify the full two-LMI ROC classification, including the
singular delta=0 cases. The listed non-axis generators J_r cover r<-2 or
r>0. H,u^2,j^2 are the remaining extreme rays of that contact cone. Every
delta!=0 point with a nonzero H or j^2 remainder is a nontrivial positive
decomposition; the two rank-one block images prove extremality when both
remainders vanish. No normalization singularity is hidden.

The universal negative certificate and fixed-r heat argument prove QC for
all finite r<-2. Positive addition then proves QC iff ROC iff the LMIs for
the closed delta<=0 sector. Delta=0 is handled directly. The synthesis
correctly does not promote this to the positive-delta sector, the whole
nine-dimensional invariant cone, or the unrestricted planar Morrey problem.

The corrected-heat parameter proof concerns positive rational functions on
an unbounded branch, not sampled parameters. Its qualitative QC implication
is pointwise in r; no uniform ellipticity follows as r tends to negative
infinity. The all-affine-background and W0^(1,4) scope is reconstructed in
`UNIVERSAL_QC_ANALYTIC_AUDIT.md`.

## 2. Non-PC, extreme and nonexposed quantifiers

The synthesis's all-r non-PC statement relies on the separate support-gap
proof, not solely the interval lifted four-point law. This distinction is
necessary: J_r(I) is not negative throughout the negative branch. The
support Hessian at I forces determinant multiplier r+2, and its null-curve
gap has nonzero cubic -r(r+2)/3 for all r<-2 or r>0. That proof is valid.

The extremality and exposure statements are also correctly separated:

* extreme in the full nine-dimensional left-invariant ROC cone;
* extreme in its invariant QC subcone only where QC has been proved;
* exposed as a ray in the four-dimensional contact face;
* nonexposed as a ray in the ambient invariant ROC cone;
* minimal ambient exposed face cone{J_r,j^2};
* no unrestricted noninvariant extremality claim.

The nonexposure conclusion requires the dual-cone acoustic-evaluation
argument, which the current structural proof supplies. It would not follow
from merely displaying two contacts. The compact normalized evaluation set,
the strict interior test |A|^4, and closedness of its generated dual cone
justify the argument. All zero acoustic evaluations of J_r also kill j^2.
The two selected contact evaluations then expose precisely the claimed
two-dimensional face. These are supported statements, not automatic
consequences of the heat Gram.

The integer example 24J_(-5/2)=45H+35u^2+24j^2-60u j and its value -1 at I
are exact. Pointwise negativity at a full-rank matrix is not used as a
quasiconvexity counterexample.

## 3. Coercivity and storage transfer

The updated negative-delta restriction is essential: positive-delta QC is
unresolved, so a positive H coefficient there cannot by itself establish a
Jensen gap for the entire polynomial. Under the stated negative-delta LMIs,
the explicit H remainder gives 4(alpha-alpha0)/1875. The complex-valued
Beurling theorem, Bregman factor, exact 6000 ratio and same-G receiving
interface are independently reconstructed in `COERCIVITY_STORAGE_AUDIT.md`.

The new G lower constant 3/1250 is uniform on the original alpha=3 compact
family. It is not an optimality statement, a boundary constant, or a uniform
claim over the whole negative parameter branch. The new R<21 and sufficient
N=10^17 meet the identical N866 example's exact horizon test. The old
Heat18 diffusion remains the operator used by its spatial proof. The
synthesis correctly says that the full spatial grid was not reoptimized,
enumerated, or used to compute a storage value. It does not promote a better
analytic sufficient budget to measured algorithmic or physical advantage.

## 4. Older ray and conditional sampler

The older N863 ray is explicitly distinguished from the new QC family.
Its tangent obstruction uses a quadratic-polynomial Hessian null correction
with a second-order coefficient jet, all-jet pointwise positivity, and a
strongly parabolic tangent at zero. The exact canonical density and explicit
constant-coefficient form bridge are correct. Degenerate, singular/angular,
nonlocal and higher-jet operations remain outside. The old support-selection
obstruction retains its regularity restriction and does not decide ordinary
polyconvexity. No invalid transfer between the two rays was found.

The marked conditional sampler's likelihood, rejection law, local-query
bound and supplied-rate/exact-reference boundaries were checked separately
in `ROOT_ARTIFACT_REVIEW.md`. The synthesis preserves those information and
cost restrictions. For precision before freezing, clarify that its M delta
law-error statement refers to a retained reference cutoff or an L1/TV
error in the reference bridge with the same exact acceptance kernel. It
does not automatically cover errors in rates, Bernoulli/Poisson primitives,
likelihood factors or the probability normalizer used by an estimator.

For completeness, the M delta bound also holds for arbitrary reference TV
error under that exact-kernel contract. Let mu be the exact reference,
nu an approximation, ||mu-nu||_TV<=delta, and w=L/M in [0,1]. Put a=mu(w),
b=nu(w), c=integral w d(mu wedge nu). Then a-c,b-c<=delta. The overlap of
the normalized accepted measures is at least c/max(a,b), so their TV is
at most delta/max(a,b)<=delta/a<=M delta. Acceptance must be defined
(b>0); for valid paths here L>0. This calculation does not certify an
implementation's claimed reference TV error or approximate kernel.

## 5. Review boundary

This review covers the mathematical cone, QC, coercivity, fixed-G budget,
tangent and sampler-law implications. It does not re-audit the battery
models/data, physical material claims, empirical rare-event confidence
bands, inference accounting, repository integration, or external priority
searches. Those are not premises for the cone/QC proofs and retain their
separate worker/source evidence and open gates. No synthesis prose was
edited by this auditor.
