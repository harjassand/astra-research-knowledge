# Robust passive and dissipative computation: alternative route

Prepared 31 October 2026. This note is a complementary construction, not a claim of historical novelty or a major breakthrough. All matrices below are finite dimensional; complex versions use adjoints and real parts.

## 1. Outcome and the prior-art correction

The useful learned object is an **energy-relative certificate**, rather than a fragile exact algebra. Such a certificate composes through static passive assemblies, and through arbitrary switched dissipative dynamics with an error bound independent of duration, rates, or number of switches. The latter statement has a clean nonautonomous proof below.

This route has strong predecessors. Static-condensation reduced-basis methods already build reusable component libraries for arbitrary later topology and provide system error bounds. Veselic's 2004/2006 paper already gives the autonomous cross-form semigroup perturbation bound, including the constant 1/2. The discrete certificate is the mixed-defect characterization of Shmul'yan equivalence. These components must be used as established machinery, not renamed as inventions.

The constructive learning gap remains material: absolute experimental noise cannot certify the required relative geometry at an unknown zero mode. We give the elementary indistinguishability proof, an earned full-matrix acquisition algorithm under a stated lower-energy floor, and its actual costs. The result is reusable computation under a paid contract; it does not yet earn a compact compiler or an advantage over informed numerical methods.

## 2. Static passive contexts

Let positive-definite module matrices S_a and learned matrices H_a satisfy

    exp(-epsilon) S_a <= H_a <= exp(epsilon) S_a.

For any finite assembly, any nonnegative weights w_e, any wiring matrices B_e, and any known PSD baseline A_0, set

    A = A_0 + sum_e w_e B_e^* S_type(e) B_e,
    H = A_0 + sum_e w_e B_e^* H_type(e) B_e.

Then exp(-epsilon) A <= H <= exp(epsilon) A. This follows term by term from congruence and addition. It is independent of the number of reused copies and their topology. The same event covers later adaptive choices of all these data because the certificate is deterministic and simultaneous.

For any boundary partition with invertible internal block, the Schur complement obeys the same order. Proof: x^* Schur(A) x is the minimum of [x;y]^*A[x;y] over y; taking minima preserves both pointwise inequalities. Compliance also satisfies

    exp(-epsilon) b^* A^{-1} b <= b^* H^{-1} b <= exp(epsilon) b^* A^{-1} b.

Positive sums, arbitrary repeated wiring and elimination therefore do not multiply the uncertainty factor. Negative subtraction, signed response ratios and ill-conditioned active feedback are outside this statement.

The relative Loewner condition is necessary for the class of *all* energy contexts: the identity context with arbitrary x already tests x^*Sx. Thus it characterizes the exact task geometry for this class, but this necessity is elementary.

### A constructed planning task

On a supplied finite candidate list of modules, let w lie in a compact polytope P of nonnegative doses and let A_0 >= alpha_0 I with alpha_0 > 0. The design objective

    F(w) = b^* A(w)^{-1} b + c^T w,   c >= 0,

is convex. Its epigraph has the explicit SDP representation

    minimize t + c^T w,
    w in P,
    [[A(w), b], [b^*, t]] >= 0.

Hence standard finite-dimensional convex optimization supplies an actual polynomial-time downstream algorithm, with matrix dimension, precision and conditioning paid. It is not arbitrary topology discovery: the candidate list is an input and its size counts. If the learned minimizer has additive optimization error zeta, then

    F(w_hat) <= exp(2 epsilon) min_P F(w) + exp(epsilon) zeta.

This follows from the two uniform objective inequalities. The formulation does not solve combinatorial topology selection or other nonconvex planning.

## 3. Continuous switched dissipative computation

Consider measurable locally bounded generators

    x'(t) = -(A(t)+J(t)) x(t),
    h'(t) = -(H(t)+J(t)) h(t),

with A,H PSD, J^*=-J, and h(0)=x(0). Suppose 0 <= eta < 1 and

    (1-eta) A(t) <= H(t) <= (1+eta) A(t)

almost everywhere. No spectral gap, commutativity, common eigenspace, bound on elapsed time or bound on switching count is required. Then

    ||h(t)-x(t)||^2
      <= eta^2/[4(1-eta)] (||x(0)||^2-||x(t)||^2)
      <= eta^2/[4(1-eta)] ||x(0)||^2.                  (C1)

Proof. Set e=h-x and E=H-A. The order relation yields

    |e^* E x| <= eta sqrt(e^*A e) sqrt(x^*A x)
              <= eta/sqrt(1-eta) sqrt(e^*H e) sqrt(x^*A x).

Write a=sqrt(e^*He), b=sqrt(x^*Ax), c=eta/sqrt(1-eta). The common skew generator cancels from the error energy, giving

    (1/2) d||e||^2/dt <= -a^2+cab <= c^2 b^2/4.

The original energy identity is d||x||^2/dt=-2 b^2. Integration proves (C1). Piecewise constant switching is a special case; no boundary error appears at switching times. Exact shared unitary operations can also be inserted because they preserve both state and error norms.

The bound is uniform over every subsequent coefficient schedule

    A(t)=sum_j u_j(t) A_j,  H(t)=sum_j u_j(t) H_j,  u_j(t)>=0,

whenever each primitive satisfies the same relative-order condition. The rates may be large. A schedule may be selected after acquisition, or computed adaptively from the learned model and then applied identically to both systems. Comparing two separately closed-loop policies that choose different schedules is not covered.

### General cross-form version

Let M(t), N(t) have negative semidefinite Hermitian parts. Assume

    |v^*(N(t)-M(t))u|
       <= gamma sqrt(v^*(-Re N(t))v) sqrt(u^*(-Re M(t))u).

The corresponding propagators satisfy ||V(T,0)-U(T,0)|| <= gamma/2. To prove it, use Duhamel's formula, test against v and u, and apply Cauchy-Schwarz in time. The forward energy integral is at most ||u||^2/2; the backward adjoint energy integral is at most ||v||^2/2. Their product gives gamma/2. This is the direct nonautonomous extension of Veselic's autonomous theorem. It is a useful extension, not asserted novel.

## 4. Discrete arbitrary words

For contractions T and H define defect operators

    D_T=(I-T^*T)^(1/2),    D_Hstar=(I-H H^*)^(1/2).

Suppose each primitive pair satisfies

    H_j-T_j = D_Hjstar X_j D_Tj,     ||X_j||<=gamma.

Then for every word W=T_m...T_1 and Hword=H_m...H_1,

    |v^*(Hword-W)u|
       <= gamma sqrt(||u||^2-||Wu||^2)
                sqrt(||v||^2-||Hword^*v||^2)
       <= gamma ||u|| ||v||.                           (D1)

Proof. Telescope the word difference. For term i let u_i=T_(i-1)...T_1u and v_i=H_(i+1)^*...H_m^*v. Apply the primitive mixed-defect bound and Cauchy-Schwarz to the sum. The two sums telescope exactly:

    sum_i ||D_Ti u_i||^2 = ||u||^2-||Wu||^2,
    sum_i ||D_Histar v_i||^2 = ||v||^2-||Hword^*v||^2.

This is stronger than adding per-letter absolute errors. It also identifies its own limit: an isometric direction has zero defect, so this certificate permits no error there. Unitaires therefore have to be exact if unrestricted word length is demanded. The factorization is the established mixed-defect characterization of Shmul'yan equivalence.

## 5. A full end-to-end imperfect-action learner

Assume the fixed unknown Hermitian A_j obey the warranted floor A_j >= alpha I for a known alpha>0. The source accepts unit coordinate e_i and returns y_ji with

    ||y_ji-A_j e_i|| <= delta.

Errors can be adversarial and correlated. Query every coordinate once. Form Y_j from returned columns and set H_j=(Y_j+Y_j^*)/2. Since the total error Frobenius norm is at most delta sqrt(n),

    ||H_j-A_j|| <= delta sqrt(n).

For eta=delta sqrt(n)/alpha<1, this yields

    (1-eta)A_j <= H_j <= (1+eta)A_j.

The learner has therefore acquired the certificates needed in sections 2 and 3, with no supplied basis or solver. It uses k n full-vector actions, reads k n^2 scalars, does O(k n^2) arithmetic and retains O(k n^2) coefficients. It has not compressed the matrix. Conventional retaining system identification ties this algorithm.

The source precision delta is a genuine premise. Repetition does not improve adversarial bias. Under independently sampled zero-mean total-vector noise with a warranted variance/tail model, averaging can reduce stochastic error with the usual inverse-square cost; dimensional dependence in that tail model and in the k n simultaneous confidence event must be included. If delta has an irreducible floor too large for eta<1, this method cannot promise horizon-free accuracy.

Standard sparse or low-rank matrix acquisition may reduce the kn cost under additional warranted structural assumptions. Those assumptions and their stable recovery costs must be proved in any implementation; no such reduced acquisition theorem is claimed here.

### Downstream numerical execution

The retained H_j are explicit matrices, so ordinary matrix-exponential algorithms or ODE solvers construct the later computation. A query with L piecewise-constant segments can use L dense exponentials and applications, with conservative O(L n^3) arithmetic plus precision costs. Krylov, scaling-and-squaring and sparsity can improve this, but those methods are conventional and their costs depend on segment activity, requested numerical accuracy and structure. The *model error* bound is horizon independent; the *execution work* is not. Arbitrary requested control schedules still have to be read.

## 6. Three explicit failures

### Absolute noise cannot learn infinite-time behavior at a zero mode

Let A_0=0 and A_1=eta I. A source reporting eta v/2 on every requested v is within eta||v||/2 of both sources. Any adaptive experiment has identical transcripts under the two worlds. At t=1/eta,

    exp(-t A_0)=I,   exp(-t A_1)=exp(-1)I.

Any common prediction has operator error at least (1-exp(-1))/2 in one world. Thus arbitrarily small absolute error does not imply an arbitrarily good horizon-independent compiler, even for scalar PSD sources. A known kernel, a lower-energy floor, relative precision, or a time/conditioning budget is unavoidable.

### Static condensation does not simulate transients

A static boundary Schur complement determines equilibrium energies but not the internal memory or masses. Two systems with identical S can have different frequency responses and transient boundary trajectories. A proposed dynamic compiler must acquire the required transfer function or memory, not reuse a static S as if it were a complete dynamics model.

### Unnormalized accuracy is not postselected accuracy

The continuous theorem controls absolute state error relative to the initial norm. If a future task normalizes a surviving state whose norm is tiny, the normalization can amplify that error arbitrarily. Similarly, a signed observable near zero does not acquire a relative guarantee from an energy guarantee. No renormalized imaginary-time ground-state algorithm, rare-event conditional probability or arbitrary rational query is covered.

## 7. Relation to Astra predecessors

Pinned corpus revision: cb87e72296824ae2a677ccd337025d02d20cbb0a.

- N1049 already preserves shared positive-source uncertainty and proves exact Loewner-interval images under boundary elimination; it explicitly warns that independently complete boundaries lose source correlations and that noisy saturation does not establish exact rank. Governing source read: `research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-retained-operator-continuation/source/ports/originals/ASTRA_PRO3_ACQUIRED_PORT_ELIMINATION_AND_ACTIVE_INTERFACES.md`, lines 7–162.
- N1082 already acquires a centered PSD Gram operational quotient from exact dose-limited scalar reactions and performs all later mixed interventions by an r-by-r inverse. Its precision-floor section explicitly leaves global noisy acquisition open. Governing source read: `research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-chemical-frontiers/source/global/ASTRA_PRO3_GLOBAL_RESPONSE_ACQUISITION.md`, lines 60–279.
- N1089 develops task-conditioned residual completion and convex intervention certificates conditional on sound noisy acquisition bounds. It does not reconstruct the missing noisy learner. Governing source read: `research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/sharp/ASTRA_PRO3_TASK_SHARP_CONTINUOUS_CERTIFICATION.md`, lines 5–110; packet review retains the acquisition gap.

This note does not promote those conditional results to measured physical facts or use missing source code as available evidence.

## 8. Primary references and scientific judgment

1. K. Veselic, *Bounds for contractive semigroups and second order systems*, 2004 preprint / 2006 volume chapter. Author PDF: https://www.fernuni-hagen.de/MATHPHYS/veselic/downloads/dissip.pdf . The autonomous theorem and its exact 1/2 constant appear at the start of the paper. It also supplies a discrete analogue.
2. C. Badea and L. Suciu, *Harnack and Shmul'yan pre-order relations for Hilbert space contractions*, arXiv:1512.01990, later Indagationes Mathematicae 2017. https://arxiv.org/abs/1512.01990 . Mixed-defect factorization is established operator geometry.
3. D. B. P. Huynh, D. J. Knezevic, and A. T. Patera, *A static condensation reduced basis element method: approximation and a posteriori error estimation*, ESAIM M2AN 47 (2013), DOI https://doi.org/10.1051/m2an/2012022 . Primary open PDF https://www.numdam.org/item/10.1051/m2an/2012022.pdf . Offline reusable component libraries, arbitrary later system topology, and rigorous global error control are explicit predecessors.
4. J. L. Eftang and A. T. Patera, *A port-reduced static condensation reduced basis element method for large component-synthesized structures*, Advanced Modeling and Simulation in Engineering Sciences 1, 3 (2014), https://doi.org/10.1186/2213-7467-1-3 . It supplies empirical port reduction and a posteriori global energy/compliance bounds.
5. H. Owhadi and C. Scovel, *Operator-Adapted Wavelets, Fast Solvers, and Numerical Homogenization*, Cambridge, 2019. https://doi.org/10.1017/9781108594967 . Strong constructive alternative when operator/locality access supports learned multiscale bases.

Scientific conclusion: relative energy/defect geometry is an effective robust target for reusable computations and answers exactly which later operations can remain controlled without a growing model-error budget. It does not by itself produce a new economical acquisition theorem. The full finite-noise construction here is honest but conventional; the reduced acquisition frontier remains open. There is no claim of civilisation-changing advance or practical superiority.
