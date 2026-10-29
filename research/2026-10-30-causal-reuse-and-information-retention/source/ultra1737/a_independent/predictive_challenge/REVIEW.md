# Independent whole mathematical challenge: misspecified-teacher compiler

30 October 2026. Disposition: **ACCEPTED at the mathematical access and resource
scope below**, after the finite-geometry and probability-precision qualifications
recorded here. This is a substantive analytic reconstruction of the governing
proof, not an acceptance based on the T8 experiment. No producer solver, learner,
sampling run or extra scientific case was rerun for this review.

The final exact source bindings are in FINAL_BINDING.json. The initial pre-review
bindings remain separately in INITIAL_BINDING.json. PROOF.md and
JOINT_RESTRICTIONS.md govern over older normalized-child implementation and
derivation descriptions. RATIONAL_GEOMETRY.md is an independent constructive
finite-arithmetic supplement, supplied during challenge and incorporated in the
producer's stated precision port.

## 1. What is accepted

P and Q are laws on [O]^T. The true P conditional future rows have linear span
dimension at most r at each cut. The compiler receives iid **full P trajectories**,
conditional Q samples at positive-Q histories, and warranted next-token Q
probability intervals at a requested number of bits. Q may have arbitrary
predictive rank. A **given warranted rational upper bound Delta** on
D(P||Q), in nats, is an input promise; compilation neither estimates nor verifies
it. The ordinary encoded length of all supplied rational inputs is charged.

For A=ceil(1000(r+O+T+1/delta)), the accepted theorem constructs, with probability
at least 1-delta, a finite teacher-free autoregressive sampler satisfying

    TV(P,P_hat) <= epsilon + 128 A^3 Delta^(1/16384).

Calls, arithmetic, stored bits and inference work have a fixed polynomial bound
in A and 1/epsilon, relative to the warranted VALUE service. Its actual cost
C_Q(T,bits), full-trajectory acquisition and random-bit work must be multiplied
in. No P conditional or likelihood oracle, target singular-value lower bound,
positive hidden-state realization, or post-compilation Q evaluator is supplied.

The exponent and constants make the nonzero-Delta statement extraordinarily
weak, frequently vacuous. The polynomial powers are astronomical. Acceptance
does not establish a usable moderate-Delta learner, a sample-only-Q theorem,
physical forecasting, practical speed, historical priority, or an efficient
positive-HMM realization. It also does not certify an installed SVD, CLARABEL or
floating sampler at the formal budgets.

## 2. Closest constructive predecessor and the actual changed interface

I read the versioned primary Liu--Moitra source, arXiv:2411.07536v1,
Theorem 1.3, Sections 3, 5, 6 and 7, with particular attention to Fact 5.3,
Claim 5.5 and Lemmas 5.4, 5.6 and 5.10. The source is cached and bound by the
producer's source_cache/SOURCE.json. It supplies same-target conditional
learning, volume spanners, robust truncation, mixture sketches and convex KL
inference. These are established operations and receive full credit.

The primary source's same-target conditional resource cannot be relabelled as
access to arbitrary-rank Q under global KL(P||Q). In this construction the true
rank is used in an existence argument on P-sampled rows; the computed basis uses
only Q rows at those fresh prefixes. Most importantly, arbitrary propagated child
restrictions occur only inside a clipped logarithm. They are never used to define
the geometry or importance law. This changes the failed selected-child coverage
argument rather than assuming it.

Ordinary methods are granted the entire new argument if they adopt it. No claim
of superiority over all source-aware projection or low-rank learning methods is
entailed by that distinction.

## 3. Fresh population spanner and acquired teacher geometry

### Population generalization despite sample-dependent selection

Fix a cut. For each fixed set I of at most r sample indices, condition only on
the sampled true rows at I. If their symmetric coefficient-one parallelotope
has P-prefix population coverage below 1-gamma0, the remaining N-|I| independent
rows all lie in it with probability at most exp(-gamma0(N-r)). The union over
at most (r+1)N^r sets is valid before choosing a basis. A maximum-volume basis
of all sampled true rows exists and covers those rows with coefficients at most
one. Thus, except for that union probability, some sampled basis covers all but
gamma0 of the population. The learner never queries these true rows.

This conditional-on-fixed-indices argument is essential. Conditioning on a
data-selected basis being successful and then treating the other rows as iid
would not be valid. The source construction does not need that invalid step.

### Global KL is used only at fresh raw prefixes

The conditional chain rule gives E_h D(p_h||q_h)<=Delta. Pinsker and Markov give

    Pr_h(||p_h-q_h||_1 > eta) <= 2 Delta/eta^2.

All NT fresh queried rows are therefore eta-close except with probability
2TNDelta/eta^2. The event is not assumed for selected-parent children.
Finite global KL also implies positive Q probability at every P-sampled prefix;
no empirical zero test is substituted for that promise.

### Mixture sketch and rational selection

Use mu_geo=(Uniform+sum_i q_i)/(N+1) and M iid futures from that law. For every
i, E_mu_geo |p_i-q_i|/mu_geo=||p_i-q_i||_1. A union-Markov bound controls all
NM pointwise ratios to theta_geo with failure NM eta/theta_geo. With the
1/M sketch normalization this gives operator error

    delta0 = sqrt(N/M) theta_geo

from a rank-at-most-r matrix. Rank is retained only above a known multiple of
delta0, not above an unknown singular value of a P realization.

The literal finite geometry port is proved in RATIONAL_GEOMETRY.md. It finds an
empty rational inertia interval among r+1 thresholds, approximates the spectral
projector by an exact rational binomial-tail polynomial, acquires a rational
subspace by greedy columns, and runs exact rational volume swaps there. A
conservative selected-subspace singular bound b0=(4Md)^(-d) is paid. Its inverse
appears in internal **bit conditioning**, through log(1/b0), rather than as a
new teacher accuracy oracle. The inverse threshold and all filter work remain
fixed polynomials in x=A/tau. This supplies a complete slower alternative to a
real-arithmetic SVD invocation.

The resulting selected basis consists of actual teacher rows. Every sample row
has full ideal-sketch L1 residual at most

    6(1+2r) sqrt(N) theta_geo < zeta/10,

with coefficients at most two. The extra finite-arithmetic factor six, replacing
the ideal-real factor four, fits the same schedule. The selected projections
are not silently substituted for probability rows after selection.

### Simultaneous full-L1 generalization

For c in [-4,4]^N define g_c=|sum_i c_i q_i|/mu_geo. Its envelope is at most
4(N+1)<=8N, and its coefficient sup-norm Lipschitz constant is at most N+1<=2N.
A zeta/(80N) net and Hoeffding give, conservatively, the sufficient bound

    M >= 51200 N^2 zeta^(-2)
         [N log(1+640N/zeta)+log(2/p)].

This is dominated by (A N/zeta)^10 at the supplied schedule and confidence.
The event is uniform before the computed coefficients are selected. Hence it
applies to the spanner residual, whose coefficient vector lies in [-4,4]^N even
when the original column is itself a selected column. A sampled q_i is within
zeta/2 in full L1 of its selected-row combination.

Combining with the hidden true population basis gives, outside gamma0 P-prefix
mass, a selected-teacher combination within r zeta of p_h with coefficients at
most 2r. Its mass differs from one by at most r zeta. Exact mass normalization
then gives coefficients at most 3r and L1 error at most 4r zeta. No inverse
target condition or conditional-P resource occurs in this argument.

## 4. Projection features: why the adaptive state family is controlled

The projection importance law is the average of the S<=r+1 selected fresh rows,
including a uniform row. New projection features are independent of all geometry
selection. Every row ratio is at most S, and the mixture has a known positive
floor. Uniform concentration is over bounded coefficient boxes, not a finite
list of generated histories.

Pad the normalized proxy by weight 4tau toward this mixture. Its error is at
most 4r zeta+8tau<=9tau and it exceeds 3tau times the mixture whenever the
unpadded proxy exceeds -tau times that mixture. Since p_h is nonnegative, the
un-padded violation probability is at most 4r zeta/tau under the feature law.
The expected P-prefix mass with no feasible padded proxy is therefore at most

    gamma0 + 4D r zeta/tau <= d' tau/20.

Markov bounds the probability that this mass exceeds tau by d'/20. This is
coverage under the fixed true P-prefix law. It is not coverage conditioned on
a selected parent or on an output-model-generated prefix.

For all feasible coefficient vectors, the empirical negative mass is zero.
The full negative-mass function has envelope SC and coefficient Lipschitz
constant S^2. A uniform net therefore bounds the full negative mass by v. This
does not assert that the signed density is nonnegative at unseen futures.

For the asymmetric projection gradient, the finite family is

    ((z_alpha0-z_alpha)/mu) log([z_alpha]/[w_beta]).

The first factor is controlled by the fresh law; arbitrary joint children in
the second factor need only be subprobability densities bounded by one. The
envelope 2SCB and coefficient Lipschitz bound

    2S^2 B + 2SC(S+k)/delta_min

are valid even when a child has tiny or zero mass. The exponentially small
delta_min changes the **logarithm of the coefficient net size**. It does not
force importance sampling from those children. With half tolerances reserved
for finite arithmetic, the schedule D>=x^40 dominates a sufficient x^24 bound.
Uniformity covers every future adaptive coefficient choice and token. No union
over exponentially many histories and no N_prev*gamma/tau child recursion is
hidden here.

## 5. Independent check of the signed/normalized KL composition

I also reconstructed the global half, although root separately reviewed it.
The empirical objective must contain the minus-linear term: full normalization
does not imply empirical feature normalization. Its derivative is the intended
log ratio, and the known feature positivity makes the finite objective convex.
An approximate first-order gap plus the uniform gradient event gives
int(z0-z)log([z]/[w])>=-2xi.

Write k_z=int([z]-z), so k_z<=v+theta. Insert the proxy and then replace signed
z by [z]. The first operation costs eB; the second costs at most B k_z.
Log-sum applied to the positive unnormalized clipped densities gives the
normalization term log Z_w and another B k_z. Hence

    Phi(p,z) <= Phi(p,w)+log Z_w+2xi+B(e+2k_z).

For signed marginal m_o, the actual output law is the normalized max(m_o,b).
The denominator lies in [1,1+v+Ob], each output token probability is at least a,
and the reference is the **joint restriction** z(o,f)/pi_o. Since
pi_o delta_child>=delta_parent, the exact clipped chain rule keeps the negative
token-KL term. In particular the direct bound

    Z_wo <= 1+v+Ob+v/a+theta

is needed; an alternative normalization bound that cancels token KL would not
prove the theorem. Each projection resets negative mass to v, so v/a=tau does
not propagate as an a^(-T) error. The floor itself has a^T, whose numerical
accuracy is paid separately in bits.

Average under fixed P-prefix laws. The terminal potential is zero, and the
initial (1-tau)Q+tau Uniform costs at most Delta+2tau. The projection, bad-prefix,
floor, finite-cache and convex-solve budgets give the accepted conservative bound

    D(P||P_hat) <= Delta+40T(B+1)tau.

This is the KL of the full returned law, not a mean one-step prediction claim.
The proof makes no assumption that the global teacher KL is uniformly small at
every conditional history.

## 6. Finite precision, unsupported prefixes and convex inference

JOINT_RESTRICTIONS removes normalized-child calls. The stored quantity
V_i,o(f)=Q(of|h_i) is formed by next-token products beginning at a positive-Q
prefix. Before following a token whose warranted lower probability is not
positive, the fixed-budget rule can return zero: its warranted upper endpoint
then bounds the entire remaining product within the paid absolute tolerance.
Every actually queried prefix has positive Q mass. Tiny and zero probabilities
need not be distinguished exactly.

The uniform mixture floor pays ratio evaluation. Cached token rows are
nonnegative rational vectors normalized to sum one; their L1 error is at most
2O eps. The resulting virtual marginal error is at most E_m=2SC O eps. The
actual transition probabilities are always used in the exact chain inequality.
Their extra clipped-normalization charge is at most O E_m+E_m/a. Virtual true
rows retain exact mass one by sum alpha=1 even though the finite cached arrays
are not assumed to define a globally consistent oracle.

A feature threshold 2tau, true-proxy slack 3tau, ratio error at most tau/2 and a
known uniform feasible coefficient vector pay arithmetic and LP feasibility.
The stated fourth-power eps choice is smaller than all required ratio, clipped
log and token-normalization tolerances. Its value can be exponential in T, but
its requested number of bits is polynomial. The gradient/Hessian on the finite
polytope have polynomial bounds in S,B,1/tau. Exact rational LP directions and
warranted log intervals give an ordinary finite Frank--Wolfe stopping algorithm
with a polynomial number of iterations. The prototype's CLARABEL status is
not used as that algorithm's certificate.

The optional conditional-Q sampler derived from VALUES also has a paid finite
budget: cumulative precision b requires b+ceil(log2 O)+3 bits on **each** token
probability before summing. The unresolved probability is then at most
2O*2^(-b). Allocate this over the prescribed finite number of feature draws.
This was a review correction; per-token b bits alone would not justify that
particular cumulative bound. The exact conditional-sampling primitive may
instead be consumed directly. Returned rational categorical rows admit finite
expected fair-bit work, or a separately budgeted output-TV truncation.

## 7. Explicit schedule and encoded-input costs

I independently substituted the schedule, in dependency order. For x=A/tau:

    d'>=x^-2, gamma0>=x^-4, D<=x^41, zeta>=x^-50,
    N<=x^61, M<=x^1200, theta_geo>=x^-112, eta>=x^-1400.

There is no circular definition of eta and M. The teacher-row failure is at
most 2*x^(-1234) when Delta<=x^(-4096), using the displayed coarse bounds.
The resource-history exponent -1235 was aligned to this governing exponent;
the change has no effect on any confidence or theorem constant.

Population failure has negative exponent at least x^56/2 while its index-union
log is at most x^3. The geometric pointwise failure is exactly bounded by
NM eta/theta_geo<=d'/100. Full-L1 sketch and both projection nets fit the stated
M and D. The a^(-T) floors enter bit lengths and coefficient-net logarithms,
not the sample powers. The rational geometry port's inverse gap also has a
fixed polynomial bound in x; exponential inverse-basis bounds enter through
their logarithmic bit lengths only.

The accuracy choice first constructs tau_acc from epsilon and A, compares the
**given** rational Delta to (tau_acc/A)^4096, and doubles tau if required.
It never computes unnecessary bits of a tiny root of Delta. The encoded input
length is charged. Tau>=tau_acc bounds all output sizes by a fixed polynomial
in A,1/epsilon. Uniform fallback has a vacuous right side, as it must. The
Pinsker and tau inequalities give the stated Holder exponent with ample slack.

The compilation call majorant and output storage stated in PROOF are consistent
with full-density products, fresh feature sampling, joint restrictions, token
arrays and retained finite models. The slow rational spectral alternative can
have a larger fixed polynomial arithmetic exponent than the floating/SVD sketch;
no fast general library port is inferred. Actual teacher-value service and P
source costs remain outside the relative arithmetic bound and must be charged.

## 8. Executed evidence, ordinary controls and final limits

The T8 record is useful implementation evidence only. It uses 32 prefixes/cut,
64 geometry features and 128 projection features, a known-rank floating cutoff,
normalized child arrays and floating convex solvers. It does not execute the
formal schedule, interval-zero support handling or the rational geometry port.
The initial serialization/orientation failure is preserved. I read the programs
and saved summaries but did not rerun the producer, solver or saved consumer.

The corrected diagnostic reports 256 full P trajectories, 82,802 next-value
calls (including calls for 1,118 Q future draws), 0.518831917 seconds compilation,
zero inference Q calls, TV 0.02861011315 and KL 0.002922687075. The same-input
ordinary full teacher trie reports 255 value calls, zero P samples,
0.000877792 seconds compilation and TV 0.01690634597. It wins TV, query cost and
time here; its general exponential horizon cost does not supply the general
polynomial theorem. The EM comparison uses a narrower parametric source promise
and is much faster. Neither comparison can be suppressed by the general theorem.
These numerical figures are producer-saved diagnostics, not a newly implemented
independent replay or confidence certification.

The accepted advance is an access-qualified constructive compiler under a
supplied global misspecification bound and a strong probability-value oracle.
The sample-only misspecified-teacher problem, practical usefulness,
moderate-Delta guarantees, physical acquisition and best-incumbent advantage
remain unpaid. Historical priority of the particular extension is UNKNOWN.

No remaining mathematical correction is requested at this frozen scope.
