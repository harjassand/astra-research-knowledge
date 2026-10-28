# Focused prior-art challenge to the scalar future-word compiler

28 October 2026. Review of the root construction, not a priority certificate.

## Finding

The individual mathematical and experimental ingredients have close, strong
predecessors. In particular, neither the acquisition of a genuine Galerkin
operator from scalar boundary responses nor the acquisition of an actual
infinite-dimensional residual from three finite matrices is new in general.
The root construction should not be presented under either claim.

The exact complete operation implemented here was not found in the inspected
primary sources. Its defensible addition is narrower and operational: compile
finite simultaneous intervals for native reciprocal word responses into an
output certificate for every future finite switching program, using arbitrary
rational coefficient maps, measured primal and dual residual norms, and a
signed correction; permit singular dictionaries and avoid a hidden-rank or
hidden-gap assertion. A separately checked finite computational contraction
can make the bound uniform in word length. This remains a candidate addition
to existing methods, with no demonstrated general cost advantage or historical
priority claim.

## Exact comparisons with primary sources

### 1. Robust GNS: the closest algebraic predecessor

Klep, Povh and Volcic, *Minimizer Extraction in Polynomial Optimization Is
Robust*, SIOPT 28 (2018), 3177–3207,
[DOI](https://doi.org/10.1137/17M1152061),
[author manuscript](https://igorklep.codeberg.page/files/cont_gns_rev1_24may18.pdf).

Read: Section 2.2, Equation 2.6; Theorem 3.2 and Corollaries 3.5–3.6;
Section 4.2, Lemma 4.3; Section 4.3.1, Theorem 4.9.
Equation 2.6 is precisely the whitened insertion-matrix compression. The
quotient construction permits singular positive moment matrices. Section 4.2
forms the canonical flat block completion and uses its positive Schur residual
without assuming a nearby flat Hankel completion. Lemma 4.3 compares extracted
word values to supplied moments within the extension degree; its stated
estimates use the smallest positive singular value, and Section 4.2 assumes
invertible H. Corollary 3.6 permits arbitrary polynomial degree but compares
two extracted finite models sharing H, not an unobserved true continuation.

The remaining distinction is the root's finite native observation contract,
arbitrary non-Galerkin maps, and a certificate for unmeasured future words.
Singular quotients, approximate flatness and the basic compression are already
covered. Their quadratic-constraint result also precludes treating preservation
of contraction inequalities by compression as a new principle.

### 2. LGST: the closest native sequence acquisition predecessor

Nielsen et al., *Gate Set Tomography*, Quantum 5, 557 (2021),
[paper](https://arxiv.org/pdf/2009.07301),
[DOI](https://doi.org/10.22331/q-2021-10-05-557).

Read: Section 3.2, Equations 36–48; Appendix C, Equations 90–94.
LGST uses native preparation/measurement fiducial circuits, their measured Gram
matrix AB, and insertion probabilities AG_iB. Inversion recovers all gates up
to a common similarity transform. It is self-calibrating with respect to SPAM,
which is a capability the root's matched reset/read premise does not supply.
Overcomplete fiducials are explicitly handled by pseudoinverses and fitting.
Appendix C nevertheless fixes reconstructed dimension d^2 and requires
informational completeness on that target space. Finite data noise raises
empirical rank; a low-rank model is fitted rather than logically certified
complete by that rank.

Thus native scalar sequence data, shared gauge, redundant fiducials, and
multi-operation prediction are established. The root's distinction is an
actual-source residual certificate without an informational-completeness or
hidden-dimension cutoff, for the narrower reciprocal-contractive source class.
GST can adopt the certificate if its apparatus satisfies that class. Such
adoption would make it the appropriate strong comparator, not erase the
certificate's contribution.

### 3. ResDMD: genuine hidden residuals are already data-driven

Colbrook, Ayton and Szoke, *Residual dynamic mode decomposition: robust and
verified Koopmanism*, JFM 955, A21 (2023),
[primary article](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/residual-dynamic-mode-decomposition-robust-and-verified-koopmanism/67F1513D7E0E182E8094ABCD3E5E94ED),
[DOI](https://doi.org/10.1017/jfm.2022.1052).

Read: Section 3.1, Equations 3.1–3.4; Theorem 3.1; Sections 3.3 and 8.
ResDMD adds the K* K Gram matrix to the ordinary dictionary Gram and insertion
matrices. This yields the norm of the residual against the actual
infinite-dimensional Koopman operator, not merely a finite-model residual.
The three data matrices are obtained from the same observable snapshots.
Spectral verification and approximate invariant-subspace diagnostics follow;
the displayed guarantees assume convergence of snapshot quadrature. The paper
also addresses dictionary selection and compression for forecasting.

The root's residual form is the same elementary norm identity with a matrix
coefficient map in place of a scalar eigenvalue. Its contribution must reside
in native reciprocal-word acquisition, explicit finite observation intervals,
and the signed primal-dual future-program certificate. Claims that existing
data-driven methods cannot measure leakage without knowing hidden states are
false without an access-model qualification.

### 4. Boundary wave ROMs: actual inaccessible-state compression is operational

Borcea, Garnier, Mamonov and Zimmerling, *When Data Driven Reduced Order
Modeling Meets Full Waveform Inversion*, SIAM Review 66 (2024), 501–532,
[DOI](https://doi.org/10.1137/23M1552826),
[author manuscript](https://public.websites.umich.edu/~borcea/Publications/SIREV.pdf).

Read: Section 2.3, Theorem 1 and its proof (preprint Equations 2.32–2.33;
equation numbers can differ in the published version).
True inaccessible wave snapshots have Gram blocks
M_ij=(D_(i+j)+D_|i-j|)/2, obtained from measured boundary responses by the
cosine product identity. Related combinations give the propagator insertion
matrix. Cholesky gives a real Galerkin ROM without knowing interior wavefields.
The theorem uses nondegenerate snapshot span; the work also develops inversion
from these ROMs.

This is a direct operational predecessor to the root's scalar-inner-product
acquisition idea, not merely abstract linear algebra. The inspected construction
uses one autonomous wave propagator and special temporal identities. The root
instead uses adjoint-reversible controlled words and residual certificates for
arbitrary future switching. That is the relevant comparison; naming all
inaccessible-state acquisition as new would overclaim.

### 5. Current multi-step correction work does not remove the access distinction

Schurig, van Goor, Worthmann and Findeisen, *On Data-Driven Unbiased Predictors
using the Koopman Operator* (2026),
[primary preprint](https://arxiv.org/pdf/2602.04720).

Read: Section II and the paper's stated construction. It uses measured state
trajectories through the chosen horizon, an injective observable lift, and a
full-row-rank initial data matrix. It modifies predictors to remove empirical
multi-step mean residual and reduce variance. This reinforces that residual
correction and arbitrary finite predictors are active established tools, while
it does not supply the root's native scalar, actual-source worst-case
continuation guarantee.

## What is mathematically being added

Let V be the inaccessible dictionary synthesis map, with Vc=b. For the
selfadjoint primitive A_i choose any rational L_i, and define

    E_i = A_i V - V L_i,
    D_i = V* E_i = M_i - G L_i,
    R_i = E_i* E_i
        = N_i - M_i L_i - L_i* M_i + L_i* G L_i.

These equations themselves are standard Gram/residual algebra. The root's
useful compilation step keeps every expression as a linear combination of
native measured moments, aggregates repeated moments before interval
propagation, and uses the signed D_i correction. A second telescoping through
the backward process leaves only pairs of actual residuals with a contractive
true source propagator between them. Consequently all error terms can be
bounded using the finite acquired records without reconstructing hidden
directions. Exact finite arithmetic supplies a certificate even when the
numerical map proposal is poor; a poor proposal merely gives a broad interval.

The all-length condition is also a certificate on the finite proposed maps:

    L_i* W L_i <= rho^2 W,    R_i <= epsilon^2 W,
    W > 0, rho < 1.

It is a common quadratic Lyapunov inequality, a standard control tool.
Applying it here bounds the sums of primal and dual residual magnitudes
geometrically without asserting that the inaccessible source itself has a
spectral gap. This separation is the useful feature. Merely finding W is not
a new stability principle.

The ordinary signed dual-weighted-residual identity has separately been
reviewed in `../scalar/TEMPORAL_SIGNED_CORRECTION_REVIEW.md`. This review does
not repeat that accepted comparison. The new load-bearing point is that the
root supplies its residual norms through the explicitly restricted native
scalar interface, including finite measurement uncertainty.

## Strongest remaining challenge

The closest plausible prior-art overlap is a certified input-output Krylov or
moment realization method already combining genuine residual acquisition with
dual-weighted scalar error. The sources above establish most of the route,
and extending their residual identities to switching is mathematically
natural. The present review found no exact full-operation match; that is not
proof that no such match exists, nor evidence that the extension is a new
foundational physical principle.

Operationally, one must compare an equally informed existing method allowed
the same reset, reverse primitives, moments, intervals and computational
budget. GNS/GST/ResDMD or a boundary ROM may use the root residual compiler as
an additional certified stage. The question is then what the stage enables
and costs, rather than whether an existing name can absorb its equations.

The component now warrants preservation as a clear theorem and executable
construction. Calling it a civilisation-changing foundation requires a further
consequence: an important family where finite native acquisition and reuse
remove a limitation at acceptable precision and total cost. The short-echo
obstruction and the parent branch's equally informed comparator remain
load-bearing checks on that ambition.

## Retrieval record

Public primary pages and PDFs were consulted on 28 October 2026. The Michigan
PDF was accessible to search extraction at Theorem 1; a later direct download
returned HTTP 403, so no locally downloaded copy is claimed. The stated source
findings come from the inspected primary text, not that failed download.
