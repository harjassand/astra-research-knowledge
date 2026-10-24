# Positive-forest action lower bound from a compact Fisher prior

2026-10-24. New internal theorem candidate. Earlier reviewed Gaussian/truncation
proof `NONADAPTIVE_NOISE_LOWER_BOUND.md` stays unchanged. This file supplies a
separate full-data score argument that removes its logarithmic positivity
loss. Independent reconstruction is pending. No newness of score projection,
matrix Stam inequalities, or two-point testing is claimed.

## 1. Experiment and exact theorem

Let n>=4 be even, a>0 and sigma>0. The unknown matrix is a positive weighted
forest Laplacian on n labelled vertices; every nonzero weight is in [a,3a].
An action prepares a full real vector x_t and acquires all n coordinates

    Y_t = L x_t + Z_t,   Z_ti independently N(0,sigma^2).

A nonadaptive algorithm commits to q>=1 full actions before any responses.
It may randomize independently of the unknown input, use arbitrary real
coordinates, read every scalar and use unbounded computation. Every design
in the support of its randomization satisfies the pathwise row budgets

    sum_t x_ti^2 <= B,   all vertices i,   B>=0.          (1)

Exact preparation is granted as a strengthening. No global unit-input-norm
condition is imposed: the normalization is precisely (1). After commitment,
the decoder may additionally receive the two hub labels and the complete leaf
partition of the hard family below, but no weights or hub-edge status.

**Theorem.** If the algorithm decides connectivity with error at most
delta<1/2 on **every fixed promised input**, then

    q [pi^2 + 8 a^2 B/sigma^2] >= n(1-2delta)^2.         (2)

Full support recovery must obey the same necessary condition. The unknown
input is fixed before algorithm randomness; no graph, weights, or labels are
selected after seeing its design. The conclusion permits unbounded decoders
and arbitrary real precision. It is not a noiseless lower bound.

## 2. A positive product prior with finite scalar Fisher information

Independently choose ordered distinct hubs U,V uniformly, and partition the
remaining n-2 vertices into A,C of equal size d=(n-2)/2. Attach the leaves in
A only to U and leaves in C only to V. Let their independent weights have
the density

    p(w) = (1/a) cos^2[pi(w-2a)/(2a)],   a<=w<=3a,
           0 otherwise.                               (3)

This density integrates to one and vanishes with zero first derivative at
both endpoints. All actual weights already satisfy the promise. Its score
rho(w)=p'(w)/p(w), defined on the open interval, is

    rho(w)=-(pi/a) tan[pi(w-2a)/(2a)].

It has zero mean and exact finite Fisher information

    J := E rho(W)^2
       = (pi^2/a^3) integral_a^{3a} sin^2[pi(w-2a)/(2a)] dw
       = pi^2/a^2.                                    (4)

No simultaneous high-probability event for n leaf weights is needed. An
independent bit theta adds a U--V edge of weight a if theta=1. The two binary
hypotheses are respectively two stars and a connected tree. Metadata
M=(U,V,A,C) has the same law under both hypotheses. Both endpoint priors are
supported entirely on promised inputs, independently of design randomness.

## 3. Full-data directional Fisher inequality

The following lemma applies to the **entire observation**, not just its hub
coordinates or a hypothetical non-Gaussian posterior.

Let W in R^m have independent coordinates with the density (3), let
Z~N(0,sigma^2 I_D) be independent, and let H be any fixed real D-by-m matrix.
Put Y=H W+Z. For a direction v in R^D define

    I_Y(v)=E[(v^T grad log f_Y(Y))^2].

Then

    I_Y(v) <= v^T [sigma^2 I_D + J^-1 H H^T]^-1 v.     (5)

**Proof.** Choose any alpha in R^m, beta in R^D with H alpha+beta=v.
Integration by parts in each W coordinate (boundary density zero) and in Z
gives the conditional-score identity

    E[alpha^T rho_W(W) + beta^T rho_Z(Z) | Y]
          = v^T grad log f_Y(Y).                       (6)

For completeness, for a compactly supported smooth test function g,

    E[g(Y) rho_{W_j}(W_j)]
       = -E[H_j^T grad g(Y)]
       = E[g(Y) H_j^T grad log f_Y(Y)],

and the identical calculation for Z gives its beta term. The Gaussian
convolution has a smooth positive density, so the weak identity gives (6).
The latent coordinate scores have mean zero, are independent, and have
variances J and sigma^-2. Conditional Jensen therefore gives

    I_Y(v) <= J ||alpha||^2 + sigma^-2 ||beta||^2.

Minimize over alpha, with beta=v-H alpha. Completing the quadratic, or
Woodbury's identity, gives

    min_alpha {J||alpha||^2 + sigma^-2||v-H alpha||^2}
        = v^T [sigma^2 I_D + J^-1 H H^T]^-1 v.

This proves (5), including rank-deficient H. The comparison matrix is not
asserted to be the actual covariance or a posterior covariance of Y. QED.

## 4. The comparison matrix's exact hub Schur complement

Fix a supported design and M. Write s_i=(x_1i,...,x_qi), so ||s_i||^2<=B.
For a leaf l attached to hub h put r_l=s_l-s_h. In the full vertex-major
D=nq dimensional observation, column l of H has r_l at leaf l, -r_l at
its hub, and zeros elsewhere. Set

    v = (e_U-e_V) tensor (s_U-s_V).

When the hub-edge weight is t the complete observation is exactly

    Y(t)=H W+Z+t v.                                   (7)

Only t=0,a will be used for the promised-input testing conclusion. Intermediate
t in (0,a) are an analytic translation family; no algorithm guarantee on
intermediate inputs is assumed.

Put c=J^-1 and C=sigma^2 I+c H H^T. Its leaf diagonal blocks are
sigma^2 I+c r_l r_l^T. A leaf's cross block with its hub is -c r_l r_l^T.
The hub diagonal block is sigma^2 I+c sum_l r_l r_l^T. Eliminating all leaf
blocks leaves two independent comparison blocks

    S_U=sigma^2 I+sum_{l in A} b_l r_l r_l^T,
    S_V=sigma^2 I+sum_{l in C} b_l r_l r_l^T,
    b_l=(J+||r_l||^2/sigma^2)^-1.                     (8)

Indeed the coefficient from one Schur subtraction is

    c-c^2 r_l^T(sigma^2 I+c r_l r_l^T)^-1 r_l
       = c sigma^2/(sigma^2+c||r_l||^2)=b_l.

No hub cross block is induced because the two stars' leaf sets are disjoint.
Since v has zero leaf coordinates, the block inverse identity gives exactly

    v^T C^-1 v
       = (s_U-s_V)^T (S_U^-1+S_V^-1)(s_U-s_V).         (9)

Equations (8)--(9) are algebra about C, not a conjugate-posterior assertion.
All leaf measurements are included in C and in the full-data bound (5).

## 5. Ridge leverage over hidden labels

We state and prove the required elementary averaging lemma. For fixed vectors
r_1,...,r_N in R^q with ||r_i||^2<=R^2 and lambda>0, choose j uniformly and a
d-set A uniformly excluding j. Then

    E r_j^T(lambda I+sum_{l in A}r_l r_l^T)^-1 r_j
       <= (1+R^2/lambda) q/(d+1).                     (10)

Equivalently sample a uniform (d+1)-set T and then j uniformly in T. For this
fixed T set G=lambda I+sum_{l in T}r_l r_l^T,
h_j=r_j^T G^-1 r_j, and t_j=r_j^T(G-r_jr_j^T)^-1r_j. Sherman--Morrison gives
t_j=h_j/(1-h_j)=h_j(1+t_j), while t_j<=R^2/lambda and

    sum_{j in T} h_j = tr(I-lambda G^-1) <=q.

Averaging establishes (10). It requires no generic position or incoherence.

Every ||s_l-s_U||^2<=4B, hence

    b_l >= b_*=(J+4B/sigma^2)^-1,
    lambda=sigma^2/b_*.

Positive semidefinite comparison and (10), conditional on U, give

    E (s_V-s_U)^T S_U^-1(s_V-s_U)
      <= (1/b_*)(1+4B/lambda) q/(d+1)
       = (J+8B/sigma^2)(2q/n).                        (11)

Here V is uniform among n-1 other labels and A is a uniform d-subset
excluding V. This is exactly the sampling in (10). The symmetric estimate
at V, (5) and (9) therefore imply the full conditional directional bound

    E_M I_{Y|M}(v_M) <= (4q/n)(J+8B/sigma^2).           (12)

The fixed design is arbitrary. Averaging over its independent random seed
preserves (12), since that seed and M have common laws under both hypotheses.
The constants in (12) do not depend on the particular supported design.

## 6. From the Fisher path to total variation, without a KL assertion

For a smooth location family f_t(y)=f_0(y-t v), its directional Fisher
information is translation invariant. The fundamental theorem of calculus,
Tonelli and Cauchy--Schwarz give

    TV(P_a,P_0)
       <= (1/2) integral_0^a integral |partial_t f_t(y)| dy dt
       <= (a/2) sqrt(I_Y(v)).                         (13)

The same inequality applies conditional on the design and M. Including these
common transcript variables and averaging, Jensen gives

    TV(P_1,P_0)
      <= (a/2) sqrt(E_{design,M} I_{Y|design,M}(v_M))
      <= sqrt[(q/n)(a^2 J+8a^2B/sigma^2)]
       = sqrt[(q/n)(pi^2+8a^2B/sigma^2)].              (14)

No implication D(P_a||P_0)<=a^2 I/2 is used; that implication is not general.
There is no auxiliary signed input prior and no input-conditioning TV loss.
Gaussian sensor noise remains unconditioned and independent throughout.

A test with error <=delta on every fixed promised input has average error
<=delta under the two priors above. Its total variation must be at least
1-2delta, since optimal equal-prior Bayes error is (1-TV)/2. Combining with
(14) proves (2). The prior precedes the design; the usual averaging conclusion
produces a fixed hard promised input, not one selected after a random design.

## 7. Comparisons, charged resources, and unresolved status

For fixed a/sigma, delta and B, (2) gives q=Omega(n), including B=1. If raw
coordinates are bounded by one so B<=q, it gives q=Omega(sqrt(n)). At a
matched allowed budget B=O(log^2 n), it gives q=Omega(n/log^2 n). The latter
is still the comparison with the reviewed adaptive direct forest upper,
which uses q,B=O(log^2 n) at fixed a/sigma and recovers all support. Each full
action costs n scalar acquisitions. Its naive computation remains separately
charged; this lower permits unlimited computation.

For general-forest support with B=1, the earlier matched sensor regime
sigma_n=Theta(a/log n) still gives q_nonadaptive=Omega(n/log^2 n), because the
sensor term now dominates. This file does not supply a B=1 fixed-noise
full-support upper; the earlier adaptive single-edge information obstruction
still applies to that task.

The **separate, not yet independently endorsed** two-action star connectivity
corollary uses q=2, B<=1/2, fixed sigma/a small enough for a fixed error, and
linear arithmetic at sufficiently large n. If that corollary survives review,
the exact same positive-star promise and fixed scalar noise admit a linear
adaptivity separation: q_adaptive=2 versus q_nonadaptive=Omega(n) at B=1.
It decides only connectivity on that promised family, not full forest support.

The interface grants global simultaneous control/readout. Row budget (1) is
a nominal squared-control budget, not Joules. Dynamic range can be order n,
worst-case preparation accuracy may be order 1/n, and acquisition duration,
reset/calibration cost and stable sensor laws remain physical obligations.
The lower grants perfect controls and full real-valued readout; finite
precision can only weaken its learner. No physical trials have occurred.

Correctness: new producer proof candidate, awaiting independent reconstruction.
Source/priority: UNKNOWN; standard information and sketching ingredients are
prior art. Physical: NOT_ACQUIRED. Practical: UNKNOWN. Mission: NOT_ACHIEVED.

## 8. Finite diagnostics and primary provenance

`replay_compact_fisher.py` imports no earlier producer code. Its 436 exact
rational assertions cover 24 arbitrary rectangular quadratic-minimization
identities and 408 full-observation-versus-Schur identities, with exhaustive
metadata averages for four designs. Separate floating quadrature diagnostics
check 60 conditional-score points, 12 actual scalar convolution Fisher/TV
pairs, and nine actual full n=4 non-Gaussian Fisher examples. Maximum score
identity discrepancy is 2.15e-12; the 512/1024-node scalar Fisher refinements
differ by at most 1.82e-13. Those floating integrals are not interval-certified
proofs. The universal derivation is Sections 2--6. Actual unknown-data
acquisitions and physical observations: zero.

The classical Fisher-convolution method is prior art. Directly read
Dembo--Cover--Thomas, *Information Theoretic Inequalities* (1991), Section
III-C, Theorem 13, including its pointer to matrix versions. That source is
not asserted to state the exact rectangular-H formula (5); Section 3 supplies
its proof. [Primary author-hosted paper](https://isl.stanford.edu/~cover/papers/transIT/1501demb.pdf).
Retained PDF SHA256
`cc55f463d1e3da81bf3cccfa9c0bbccb688eace28a58598d298339d55eeff823`.
