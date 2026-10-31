# Fast dissipative sources: primary comparison and an ordinary kernel construction

Status: research comparison and local mathematical derivation, 31 October 2026. The archived pure-return compiler is unchanged. The generalized dark-generator construction below is a comparator lemma, not an independently accepted general-source compiler, implementation, novelty claim, or complexity separation.

## 1. Consequential conclusion

The most defensible distinction is not fast-forwarding a mixing source by itself, changing a Lindblad gauge, using quantum trajectories, or retaining memory across interventions. All have strong ordinary constructions. The particular earned interface is a dimension-nonenumerating, uniform joint-channel implementation for a rapidly returning acquired source *continually excited* by a centered square-root-rate coupling. Its proof combines a normalized fast nonnormal kernel with a complete first-event isometry and an actual activity bound.

Even the fast-kernel operation has a strong ordinary replacement: improved linear-combination-of-Hamiltonian-simulations (LCHS), followed by grouping a certified contracting semigroup. Section 4 constructs that replacement with finite coefficient preparation and slack normalization. Therefore Poissonization of a discrete return channel is not plausibly an intrinsic computational boundary. This narrows rather than inflates the result's significance.

No source checked here supplies the entire accepted interface as a ready-made theorem. This is a bounded comparison, not evidence of priority. Sustained investment should depend on a useful end-to-end consumer beating the strongest retained-memory or elimination baseline, rather than another family extension. Presently only a theoretical interface improvement, not a practical or civilization-scale consequence, has been established.

## 2. Exact benchmark and ordinary baselines

The accepted benchmark is

    L_lambda = -i[H0 + sqrt(lambda) K, .] + lambda(Phi - I),

with acquired Stinespring W, prepared psi and c, W psi = c tensor psi, efficiently reflected P=|psi><psi|, Q=I-P, centered PKP=0, and an operator certificate

    (Phi^dagger)^m(Q) <= Q/16.

All supplied encodings, their controlled inverses and numerical refinements have real costs. The accepted addendum allows arbitrary joint source/system/reference input and prescribed joint instruments, retaining source output. Consumer circuits are external or charged separately. Simulator emission records and internal timestamps remain private. The overhead is polynomial in the acquired return horizon and physical coupling/action resources, and logarithmic in rate and requested error; it is not a practical gate-count estimate.

### Primary comparisons

**Interaction-picture Lindblad simulation.** He et al., *Efficient Optimal Control of Open Quantum Systems*, Section 4, equations (80)–(83), explicitly takes the fast component to be a Hamiltonian commutator. The transformed jumps are conjugated by an acquired unitary. Its theorem does not simply replace that unitary by a rapidly mixing dissipative channel. This is an access distinction, not a lower bound against other dissipative representations. [Primary text](https://arxiv.org/html/2405.19245v1)

**Trajectory algorithms.** Borras–Marvian, *Quantum simulation algorithms based on quantum trajectories*, assumes a representation with sum L_j^dagger L_j proportional to I. The original lambda(Phi-I) representation belongs to that class: the Poisson clock has rate lambda. Direct application therefore charges lambda T. The dark representation instead has sum L_j^dagger L_j = 2I-A-A^dagger, zero on P and generally nonscalar, so the stated restricted theorem does not directly receive it. This is a genuine, constructive ordinary baseline, not an omission of trajectory methods. [Primary text, introductory restriction and Appendix A](https://arxiv.org/html/2509.10425v2)

**Best generic stacked-jump baseline checked.** Chen–Gao–Wang–Zhou, *Query-Optimal and Gate-Efficient Lindbladian Simulation*, uses Hamiltonian and stacked-jump encodings with resource tau=(alpha_H+alpha_B^2)t. It provides essentially optimal additive query scaling and polylogarithmic gate overhead; time-dependent access is also treated. Applying its declared norm budget directly to either representation above generally retains an O(lambda T) contribution. A complete channel approximation does not, solely by being accurate, expose a specified no-jump Kraus block. [Primary text](https://arxiv.org/html/2609.18757v1)

**Gauge optimization is already an explicit algorithmic idea.** Shang–Franca, *Hamiltonian dynamics from pure dissipation*, equations (20)–(21) and the following discussion, explicitly proposes choosing a better GKSL gauge to lower simulation norms. Our dark stack may still have a rate-scaled worst-case norm. Its low actual activity and acquired no-jump evolution are additional ingredients, not consequences of a small generic norm. [Primary text](https://arxiv.org/html/2604.18533v1)

**Quantum Zeno and elimination.** Popkov et al. derive reduced dynamics after a fast dissipative transient, with inverse-dissipation corrections; equations (3)–(8) describe their approximation and expansion. Azouit–Sarlette–Rouchon derive structure-preserving first-order formulas and specified second-order corrections; their abstract explicitly labels the all-orders CP assertion a conjecture. These are strong effective-model competitors when a low order meets the requested tolerance. They are not, as stated, arbitrary finite-rate, arbitrary-joint-input circuit theorems. This does not exclude later or specialized all-order constructions. [Zeno primary text](https://arxiv.org/html/1806.10422v2), [elimination primary statement](https://arxiv.org/abs/1603.04630)

**Structured fast-forwarding.** Gao–Ji–Liu obtain Hamiltonian-twirling realizations, including the Hermitian-jump Gaussian construction. Such channels are unital. A nontrivial pure reset channel is not unital, so that representation cannot directly equal every source considered here. Adding a noncommuting continually driving coupling is a further operation, not implied by source-only twirling. [Primary text](https://arxiv.org/html/2511.10253v1)

**Dissipative ODE solvers.** An–Onwunta–Yang study negative-logarithmic-norm equations and normalized history/final solution states. A vectorized density-matrix solution is not automatically a physical channel on an unknown input/reference: normalization, access, and a CP implementation must be earned. Such solvers remain legitimate kernel subroutines; Section 4 instead uses an explicit operator LCU. [Primary text, Section 1.1](https://arxiv.org/html/2410.13189v2)

**Dense exact comparator.** For a fixed, explicitly enumerated full joint dimension, ordinary matrix exponential scaling-and-squaring, finite-precision CPTP repair and Stinespring synthesis already supply logarithmic rate/precision dependence with polynomial full-dimension work. The earlier separately reviewed dense comparison remains binding. Thus logarithmic stiffness alone is not the achievement; succinct acquisition without full dimension enumeration is essential.

## 3. Two elementary comparison tests

### 3.1 Source-only mixing already gives an ordinary dimension-free shortcut

Pure stationarity implies Phi^dagger(Q)<=Q. Iterating the return certificate gives

    (Phi^dagger)^n(Q) <= 16^(-floor(n/m)) Q.

For any joint source/reference state, let p be its Q population after Phi^n. Projection onto P, the gentle bound, and the unchanged reference marginal give distance from the reference-preserving reset at most 2 sqrt(p)+p. Consequently

    ||Phi^n - Reset_psi||_diamond <= 3*4^(-floor(n/m)).

Poissonization then yields, with E_t=exp[lambda t(Phi-I)],

    ||E_t-Reset_psi||_diamond
      <= 12 exp[-lambda t (1-4^(-1/m))].

Below t_cut=log(12/epsilon)/[lambda(1-4^(-1/m))], an ordinary capped Poisson implementation uses polynomial(m,log(1/epsilon)) calls to W. Above t_cut, prepare psi and discard the source, retaining the reference. Thus a source-only mixing shortcut is already available without the elaborate coupled compiler. Segmentwise diamond errors telescope across prescribed controls.

It does not solve the continually driven problem. For example let Phi reset a source qubit to |+>, take K=b Z_system tensor Z_source, H0=0 and source input |+>. On the diagonal source algebra this is a fair sign refreshed at rate lambda. The system coherence multiplier f obeys

    f'' + lambda f' + 4 lambda b^2 f = 0,
    f(0)=1, f'(0)=0.

For fixed positive time and lambda tending to infinity, f tends to exp(-4b^2 t), not 1. Simply replacing the fast centered source by its mean deletes order-one slow dephasing. This elementary two-state example is not a hardness result: its exact scalar solution is cheap.

### 3.2 A dissipative inverse frame is not a free unitary frame

For an exact reset R, E_t=R+exp(-lambda t)(I-R). Its algebraic inverse is R+exp(lambda t)(I-R). On a nonzero trace-zero reset-annihilated direction its trace norm grows by exp(lambda t). The inverse is generally not CP. Therefore an acquired forward channel cannot silently be substituted for the unitary inverse in an interaction-picture circuit. This only rules out that naive substitution, not a positive expansion or other fast/slow algorithm.

## 4. Strong ordinary construction: bounded-time no-jump access plus grouping

This section is a local derivation under explicitly acquired finite-register operators. It is not a new full source theorem.

Suppose a dark Lindblad generator G0 has acquired Hermitian Hs and jump stack J, C=J^dagger J>=0, with J P=0 and Hs P=0 after removing a scalar phase. Put

    D=-i Hs-C/2.

Then P reduces D, D P=0, and e^(uD) is a contraction. Assume an actual survival certificate

    exp(m G0^dagger)(Q) <= Q/16.

The zero-emission branch is a CP summand of the full channel. For every vector v in Q,

    ||e^(mD)v||^2
      <= Tr[Q exp(mG0)(|v><v|)] <= ||v||^2/16.

Thus ||e^(mD)Q||<=1/4. This argument requires an actual dark generator and its acquired operators, not just a spectral gap.

### 4.1 The operator block is supplied by ordinary LCHS

The improved LCHS identity of An–Childs–Lin provides an operator LCU, not merely a postselected normalized solution: Section 4.2.1, equation (101), displays its good block explicitly. For a fixed kernel parameter 1/2, the identity here is

    e^(uD) = integral_R w(k) exp[-iu(Hs+k C/2)] dk,
    w(k) = exp[-sqrt(1+ik)] / [2 pi exp(-sqrt(2)) (1-ik)].

The positive square root is the analytic branch on the relevant strip. Their time-independent construction uses ordinary Hamiltonian simulation. The following conservative quadrature is our finite-gate receiving argument; it does not assume a free coefficient-state oracle. [Primary formula, equations (32)–(33), and block construction (101)](https://arxiv.org/html/2312.03916v2)

Fix 0<=u<=m and target operator error eta. On the real axis the kernel tail beyond R is bounded by a constant times exp(-c sqrt(R)); choose R=O(log^2(1/eta)). In the strip |Im k|<=1/2 the kernel is analytic, uniformly bounded, and

    ||exp[-iu(Hs+k C/2)]|| <= exp(m ||C||/4).

Partition [-R,R] into O(R) panels of width at most 1/4. On each panel a fixed ellipse stays inside this strip. Positive Gaussian quadrature with q=O(m alpha_C+log(R/eta)) nodes per panel, using an acquired certified upper bound alpha_C>=||C|| (for example alpha_J^2), therefore gives total operator error O(eta), by the analytic polynomial-approximation bound and exactness on polynomials of degree 2q-1. The resulting number of coefficients is polynomial in m alpha_C and log(1/eta). The absolute coefficient sum is at most O(R), since the quadrature weights are positive, sum to 2R and the real-axis kernel is bounded.

Compute the nodes, weights and complex kernel values to the required absolute precision; prepare the polynomial-sized two coefficient states explicitly, padding a zero arm to a certified O(R) normalization. No exponential table is present. Coefficient square roots are approximated at squared tolerance when needed. Each SELECT simulates the acquired Hermitian Hs+k C/2 for a time at most m, with normalization bounded by alpha_Hs+R alpha_C/2. The stack encoding gives C with normalization alpha_J^2. Hamiltonian simulation, coefficient arithmetic, state preparation and their controlled inverses all have polynomial cost in these supplied actions and log(1/eta). A binary duration is implemented with controlled fixed binary-fraction times; this is not a free variable-time oracle.

This establishes a polynomial-cost block of e^(uD) with at most polynomial-logarithmic normalization. Ordinary singular-value amplification with slack then obtains e^(uD)Q/2, whose norm is <=1/2, and 2e^(mD)Q, whose norm is <=1/2. One does not need to amplify a contraction all the way to a singular value exactly one. Numerical errors are chosen below the slack and allocated per later product. Explicitly, distinguish the requested amplified-block error eta_out from the raw quadrature/encoding error eta_raw. For an amplification polynomial of degree d, use the standard robust singular-value-transformation bound O(d sqrt(eta_raw)); choose eta_raw <= (eta_out/(100d))^2, and allocate phase-synthesis errors O(eta_out/d). A sharper operator-polynomial bound can improve this, but is not needed. The degree is polynomial in the certified O(R) normalization and log(1/eta_out); thus tightening the raw precision adds only O(log d) bits. Choose conservative polynomial bounds for R and d first, with slack in log(1/eta_raw), to resolve this dependence without a free precision oracle. Subsequent products receive eta_out=O(epsilon/(k+1)). All timing bounds use acquired alpha_Hs+alpha_C/2, not an algorithm for computing exact operator norms.

An even more optimized quadrature is available in Apel–Berntson, *Optimal kernel functions for linear combination of Hamiltonian simulation*: its finite quadrature explicitly controls operator error and LCU subnormalization. It strengthens the ordinary alternative but is not needed for the conservative polynomial construction above. [Primary text, Theorem 8 and Corollary 9](https://arxiv.org/html/2610.03669v1)

### 4.2 Grouping without Poissonization

Write t=km+r with 0<=r<m, and set

    B=2e^(mD)Q, R_r=e^(rD)Q/2, a'=log(2)/(2m),
    F_D(t)=(1/4)e^(a't)e^(tD)Q.

Reduction by Q and the semigroup law give the exact acquired product

    F_D(t)=[(1/2)e^(a't)2^(-k)] B^k R_r.

The scalar in brackets is at most 1/sqrt(2), and both B and R_r have norm at most 1/2. In addition,

    ||F_D(t)|| <= exp(-a't).

Indeed e^(2a't)4^(-k)/4 <= 2^(r/m-k)/4 <=1/2. Above a'^{-1} log(1/epsilon), choose the zero block. Below it, k=O(log(1/epsilon)); finite products with individual error O(epsilon/(k+1)) and a controlled scalar rotation give the desired operator to error epsilon. All costs are polynomial in m, supplied source actions and log(1/epsilon), and in the bit length of the queried duration. Division into k,r is performed on the finite time register; For the scaled queried block, F_D'=(a'I+D)F_D and ||F_D||<=1 give the acquired derivative bound ||F_D'||<=alpha_Hs+alpha_C/2+a', which controls input rounding (including rounding near k-boundaries, since the exact grouped formula represents the same smooth function on both sides). At the zero cutoff the discarded norm is already within budget.

This is a substantive ordinary alternative to the grouped-Poisson kernel. It does not yet establish a slow-activity bound, a full first-event instrument, or a general interacting-source compiler. It does show that demanding a normalization-one no-jump oracle from a generic channel simulator is unnecessarily restrictive: LCHS plus slack amplification supplies the needed *operator* directly.

## 5. Elimination and mixing: exact remaining operations

A useful elimination competitor must specify the same observable output. Suppose an acquired pth-order effective model, reconstruction and boundary-layer maps have a proved error C_p lambda^(-p/2). At fixed p, switching to it only above (C_p/epsilon)^(2/p), and directly simulating below that threshold, generally leaves an inverse-power precision cost. To infer polylogarithmic precision one must earn increasing-order coefficient construction, controlled C_p, actual circuit normalization and state-independent boundary handling. This conditional arithmetic is not a lower bound: special models can have exact reduced solutions or efficiently summable all-order expansions.

Arbitrary initial joint states and interventions make boundary layers relevant, but retaining them is not an exclusive feature of this compiler. Once any algorithm implements the full joint channel in diamond norm, composition with prescribed CPTP instruments is ordinary telescoping. Likewise a known exact memory kernel or process tensor can be a stronger method on compressible instances. Its bond dimension, memory construction and control interface must be charged, just as our return certificate and encodings are charged.

The principal still-interesting operation is therefore the complete positive assembly: a uniform low-activity realization, scaled fast blocks, integrable first-emission envelope, acquired conditional words, and amplification of the *complete* instrument while retaining source output. A fast matrix-function block alone does not imply that operation. Conversely, a generic accurate channel routine need not preserve a chosen emission interpretation. The accepted proof earns this assembly in its stated class, but this review does not establish its uniqueness among ordinary constructions.

## 6. Investment decision and stopping boundary

Keep the accepted compiler as reusable scientific capital. Do not invest next in another narrowly enlarged source class merely because Section 4 permits it. The consequential test is a succinct, known source and an explicit controlled observable for which (i) the acquired return/encoding costs are small, (ii) fixed-order elimination misses the requested finite-rate effect, (iii) the best exact retained-memory representation has a priced bottleneck, and (iv) the released construction has a credible resource ledger rather than unspecified polynomial overhead. No such practical winner is proved here.

The current outcome warrants targeted comparison and implementation-level resource simplification, not a north-star success claim. If an ordinary LCHS/trajectory composition recovers the entire interface with comparable bounds, adopt it and simplify the framework; that is scientifically preferable to defending provenance. No absence-of-title or bounded-search argument is used to claim novelty.

## 7. Provenance and access limits

Accepted base source: pure_return_source_20261031/PURE_RETURN_FULL_FINITE_BIT_RECEIVING.md, SHA256 1a097458af52e4b89746b2f5e38e8ba4ea9f8a835db731daef39b8e9ea71e032. Arbitrary-input addendum: SHA256 39cfffcb2c38bf13da46a380760a994787caada7ecc99f43cc93e6953fc95069. Their independent receipts remain separate; this document does not modify them.

The primary-source check used accessible arXiv and publisher/author pages. An attempted nonexistent arXiv2312.03916v3 HTML returned 404; the canonical abstract identified v2, whose accessible HTML was then read. No access denial was bypassed. Earlier denied Wisconsin Anderson–Kim, Tier publisher, Nature translation, IACR and CWI fetches were not retried, nor were alternate copies sought. This is not a comprehensive literature review. Generalized Section 4 is a local derivation pending its own independent check, not an automatic whole-source extension.
