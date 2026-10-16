# Independent asynchronous adversary: analytic record

Author: gd_async_adversary. Date: 2026-10-16. Status: independent analytic derivations and bounded diagnostics, externally unreviewed. The pinned knowledge worktree is `2688d7a383502df4fc1e64001d04bb76e6ec05e5`. Incoming originals were read as data and not edited. No current peer outputs were read. No source scientific program was executed, no package installed, no repository mutation performed, and no subagent spawned.

## 1. Exact contract and conclusions

Let the finite joint space include arbitrary persistent bath and reference systems. Let the selected commuting Hermitian involutions be Z_i and let

    H(t)=H_0(t)+sum_i V_i(t),
    [H_0,Z_i]=0, {V_i,Z_i}=0, [V_i,Z_j]=0 for i != j,
    ||V_i(t)|| <= j_i(t).

The norm envelopes are nonnegative and integrable. Assume the sector-preserving baseline has a well-defined unitary propagator. Own complete pinches occur at deterministic prescribed times. Every fixed intervention has a common dilation, preserves the monitored parity under deletion, and neither reads private selected signs nor feeds back mathematical record labels. The input is in a specified joint sector P_s. All following effect inequalities hold on that whole sector, uniformly over the bath/reference input.

For own gap actions a_ik define

    s(a)=sin^2(min(a,pi/2)),
    Q_i=1-product_k(1-s(a_ik)),
    C_i=min(1,sum_k s(a_ik)).

I independently reconstructed the operator entire-function sine lemma, one-common-gap all-subset product, synchronized product Q, singleton minimax and the qualified original-Walsh lift. No flaw was found in these arguments under their exact hypotheses.

I did not prove or refute the central arbitrary-asynchronous endpoint product `product_i Q_i`. No legal finite shared-bath counterexample was acquired.

A rigorously stronger asynchronous certificate than the incoming `product_i C_i` is obtained below. It holds for the stronger event that every selected coordinate ever has a recorded own-gap mismatch, as well as for all endpoint flips. For two coordinates it is

    E_history <= min(Q_1 C_2,C_1 Q_2) P_s.                 (A1)

More generally a synchronized anchor subset A gives

    E_history <= [product_(i in A) Q_i]
                 [product_(j outside A) C_j] P_s.        (A2)

The minimum of these scalar bounds over admissible synchronized anchor subsets is valid. The empty anchor recovers the incoming certificate, a singleton anchor always exists, and the full anchor gives the known exact product when all selected schedules synchronize. This does not yield the full asynchronous product merely by assigning every coordinate its own singleton anchor.

## 2. Scalar-to-operator sine lemma

Let F be an operator-valued entire function of exponential type at most sigma, with `sup_(x real)||F(x)|| <= M` and `F(0)=0`. Then

    ||F(t)|| <= M sin(min(sigma |t|,pi/2)) for real t.   (A3)

Rectangular maps are allowed. Fix unit vectors u,v and an endpoint-dependent phase theta, set `f(z)=exp(-i theta)<u,F(z)v>`, and real-symmetrize:

    g(z)=[f(z)+overline(f(overline(z)))]/2.

This is a real entire function of the same type with `|g(x)|<=M` and g(0)=0. The classical sharpened real Bernstein inequality gives

    g'(x)^2+sigma^2 g(x)^2 <= sigma^2 M^2.

Apply the derivative estimate to `arcsin(g/(M+epsilon))`, integrate from 0 to t, and let epsilon decrease to zero. This gives the sine bound before the first pi/2, and the global bound M handles larger t. Choose theta so g(t) is the absolute endpoint matrix element and take the supremum over u,v. The zero M and zero type cases follow by constancy/continuity.

The primary source checked is Redheffer (1953), Theorem 11, printed pp. 832-833. Only the real scalar sharpened inequality is imported. Applying that sharpened derivative inequality directly to an arbitrary complex scalar amplitude would be invalid; the endpoint-phase real-symmetrization avoids that error.

If a source formulation uses a strict type parameter or strict real-axis norm bound, apply it first with type sigma+delta and bound M+epsilon, then let both positive parameters decrease to zero. This covers the stated non-strict type-at-most and norm-at-most hypotheses.

## 3. Type and deletion checks for the actual record isometry

Scale one selected own interaction restriction by z=x+iy. For real x all Hamiltonian coefficients remain Hermitian, even at arbitrarily large x; these are mathematical interpolation parameters, not promised physical control settings. In the interaction picture of this real Hamiltonian the imaginary part has generator yV_i. Its propagator norm is at most `exp(|y| integral ||V_i||)`. Fixed record isometries and output projectors have norm at most one. Across all pieces of the scaled restriction this gives type at most the corresponding action.

The Dyson series is locally uniformly convergent in each finite set of complex scale variables, hence the projected amplitudes are entire. No bath factorization, mutual commutation of bath couplings, or norm bound on H_0 is used.

Retain each own pinch in a fresh, isolated register and include actual endpoint labels. A chosen gap mismatch is a fixed diagonal projector on these records. If the entire own interaction on that gap is deleted, all remaining Hamiltonian terms and pinches preserve its parity. Therefore its mismatch amplitude is exactly zero, as a whole-input operator identity and for all values of the other interpolation variables. This deletion identity is stronger than a claim about one selected initial bath vector.

For a common gap, project onto any selected subset of parity mismatches. The amplitude is a contraction on the whole real scale domain and vanishes when any selected scale is zero. Iterating (A3) gives

    E_(all R mismatch during common gap)
        <= [product_(i in R) s(a_i)] P_enter.           (A4)

This is an operator-effect bound. It is not a product of quantum outcome probabilities asserted to be independent.

## 4. Singleton and synchronized Q reconstructions

For a singleton, the mismatch probability in one own gap is at most s(a), uniformly over the entering sector and arbitrary bath state. Other-coordinate pinches inside the gap preserve the selected parity, so they can be retained as fixed isometries in the same argument. Equivalently, the no-mismatch conditional probability is at least 1-s(a).

Condition on actual preceding own records. The conditional entering bath/reference state may depend arbitrarily on this past; the one-gap inequality is uniform over every such state. Multiplying lower bounds along the event of no mismatch gives probability at least `product_k(1-s(a_ik))`. An endpoint flip requires at least one mismatch, giving Q_i. The finite sink bath in the pinned singleton source attains it. This is a minimax statement over arbitrary finite bath spaces, not attainment in every separately fixed smaller space.

For synchronized selected schedules retain joint sector records after every common gap, and set a permanent first-mismatch flag for every coordinate. Let U be the still-unset coordinates. If v_i is the remaining future risk after the current gap, the conditional continuation upper value is

    product_(i in U)[v_i+(1-v_i) 1_(A_i)],

where A_i is this gap's mismatch. Expand this product into indicators of joint mismatches. Every coefficient is nonnegative. Bound each subset indicator by (A4). The result is

    product_(i in U)[v_i+(1-v_i)s(a_i)].

This is exactly the Q recurrence. Backward induction proves the stronger history event that every coordinate ever mismatches is bounded by `product_i Q_i`. Endpoint all-flipped is contained in that event. The conditioning is solely on past isolated records, never on a future selected endpoint. Tensor products of independent sink baths attain both the endpoint bound and the history bound.

The unresolved asynchronous step is substantive: at one coordinate's record time another may remain coherent between its own records. Adding the missing other pinch at that time changes the stipulated channel. Nor can one apply the singleton conditional survival bound after conditioning on the other's eventual endpoint flip.

## 5. New anchored asynchronous certificate

First take two arbitrary schedules. Pick an own gap k of coordinate 2. In the full record dilation project onto coordinate 1's event of ever mismatching and coordinate 2's mismatch on gap k. Scale V_2 only on that gap by z, and call the resulting compressed amplitude F_k(z).

For every real z, all coordinate-2 interactions and pinches still preserve Z_1. Coordinate 1's actions and its own fixed schedule remain unchanged. Its exact singleton theorem therefore gives

    ||F_k(x)|| <= sqrt(Q_1) for every real x.           (A5)

Deleting the selected coordinate-2 gap makes its mismatch impossible, so F_k(0)=0. The type is at most a_2k. Applying (A3) with the improved global real-axis bound (A5) gives

    F_k(1)^dagger F_k(1) <= Q_1 s(a_2k) P_s.          (A6)

The event that both coordinates ever mismatch is contained in the union over k of these events. The positive record union thus gives `Q_1 sum_k s(a_2k)`. Independently dropping coordinate 2 gives Q_1; these two bounds together give `Q_1 C_2`. Swapping coordinates proves (A1).

For an arbitrary nonempty anchor subset A whose own schedules synchronize, scale one chosen own gap for each j outside A. The full selected set need not synchronize. Project onto every anchor coordinate's history-OR flag and the chosen outside gap mismatches. For all real scales, the synchronized history theorem on A still gives uniform amplitude norm at most `sqrt(product_(i in A)Q_i)`: all outside interactions and pinches preserve A's parities, even though they need not commute on the bath. Intra-gap outside record isometries are parity-preserving and do not spoil (A4).

Apply the sine lemma in each chosen outside scale; deletion-nullness holds for all values of the other variables. This proves the chosen-gap effect bound

    [product_(i in A)Q_i] [product_(j outside A)s(a_j,k_j)].

Union over one witness gap per outside coordinate, and drop outside constraints whose sum is at least one, to obtain (A2). All history projectors commute because their registers are isolated, including neighboring gaps sharing a label. The projector onto all selected history-OR flags is bounded by that positive union. Pullback through the fixed isometry preserves the positive operator inequality. This is a mixed proof, not an inference that arbitrary unrelated product certificates can always be minimized coordinate by coordinate.

For completeness, the capping step is applied before summing: retain only outside coordinates with `sum_k s(a_jk)<1` and discard the others from the target. Use the same synchronized anchor theorem and selected-gap proof on this retained set. The right side is exactly the anchor product times the product of individually capped C_j. Thus one does not require a probability independence assertion or a cap on a previously unioned product.

With a finite selected set there are finitely many synchronized subsets. Since every certificate is a scalar multiple of the same P_s, taking their minimum is legitimate. Including the empty anchor gives the final bound

    E_history <= min( product_i C_i,
         min_(nonempty synchronized A)
              [product_(i in A)Q_i product_(j outside A)C_j] ) P_s.

Every singleton is synchronized by itself. All endpoint-flipped effects are bounded by E_history since a binary label cannot change from its input to its endpoint without some successive own-label mismatch.

An explicit staggered example has horizon T=3, coordinate-1 cut at time 1, and coordinate-2 cut at time 2. Let t=arcsin(3/5). Set j_1=t on [0,1] and t/2 on [1,3], and set j_2=t/2 on [0,2] and t on [2,3]. Both coordinates have own gap actions (t,t), but their schedules are asynchronous. Then `Q=369/625`, `C=18/25`. The incoming history product-C certificate is `324/625=0.5184`; the anchored bound is `6642/15625=0.425088`; the unproved desired product is `136161/390625=0.34857216`. The anchored certificate is smaller by `1458/15625=0.093312`, or exactly 18 percent. These are exact scalar certificate comparisons, not computed actual failure probabilities for a specified Hamiltonian.

No sharpness or minimax equality is asserted for the new anchored bound. Independent sink copies attain the desired product as a lower witness, while the universal upper supplied here is generally larger.

## 6. Exact counterexamples to analytic shortcuts

These are mathematical proof-technique counterexamples. None is asserted to be an admissible Hamiltonian/pinch protocol or an original-Walsh counterexample.

### 6.1 A one-variable ellipse shortcut is false

Let t satisfy sin t=3/5 and cos t=4/5. Define

    F(z)=(cos(z-t)/2, 5 sin z/sqrt(28)).

This is entire of type one. The quadratic form for its squared real-axis norm has eigenvalues 1 and 1/7, so the norm is at most one. The first component is uniformly at most 1/2, and the second vanishes at zero. Nevertheless

    ||F(t)||^2=4/7 > 13/25
      =1/4+(1-1/4)sin^2 t.

Thus a bound on an existing component plus deletion-nullness of a new component does not by itself yield the Q recurrence.

### 6.2 Orthogonal zero-hyperplane data alone are insufficient

For k=1/3 define

    G(x,y)=sqrt(8/9) *
       (sin x(cos y+k sin y), sin y(cos x+k sin x)).

Each component has its designated zero hyperplane. Put u=x+y, v=x-y. Before normalization its squared norm is

    [(sin u-k cos u+k cos v)^2+sin^2 v]/2.

Maximizing first over u and then over cos v gives `1/(1-k^2)=9/8`, so G is globally contractive. At x=y=t as above, its norm square is `16/25`, exceeding `1-cos^4 t=369/625` by `31/625`. This map mixes the wrong reflection parities within a putative record component, so it does not satisfy the full parity record algebra.

### 6.3 Even exact reflection parity and full isometry are insufficient

The following stronger abstract example has the required reflection characters and only odd mismatch histories in its endpoint subvector. Write c=cos x,d=cos y, and set

    F10=sin x(3+2d)/5,
    F01=sin y(3+2c)/5,
    F11=sin x sin y/5,
    F00=(sqrt(6)(1-c-d-cd)/5, cd/5).

The 00 component lives in a two-dimensional output space. Direct polynomial expansion gives the exact identity

    ||F00||^2+|F10|^2+|F01|^2+|F11|^2=1.             (A7)

Each component is even/odd in x and y exactly according to its binary label. Thus the terminal odd subvector `(F10,F01)` is an entire contraction, with zero hyperplanes and reflection symmetry. Yet at x=y=t,

    |F10|^2+|F01|^2=9522/15625,
    Q(t,t)=9225/15625,
    difference=297/15625>0.                            (A8)

A general completion is obtained with a+b=1 and `1/2<=a<=(sqrt(5)-1)/2`:

    F10=sin x(a+b cos y), F01=sin y(a+b cos x),
    F11=sqrt(b-a^2) sin x sin y,
    F00=(sqrt(ab)(1-c-d-cd),(2a-1)cd).

Equation (A7) again holds. The rational example is a=3/5,b=2/5.

The exact reflection identity for a genuine fully resolved own gap follows from conjugation by its monitored involution: the gap propagator with scale -z is Z_i times the scale-z propagator times Z_i. Sandwiching the entering and exiting gap projectors makes a record component odd for mismatch and even for no mismatch. The abstract example respects this invariant, so reflection alone does not repair the analytic argument.

The displayed abstract isometry is not itself the full unprojected causal record dilation of a singleton two-gap protocol. Its first-record mismatch probability is

    |F10|^2+|F11|^2
      =sin^2 x [b+2ab d+(a^2-ab)d^2],

which depends on the future scale y. A full causal record marginal cannot have that dependence. However, a submap projected onto another coordinate's future bad event CAN legitimately have such dependence. Consequently this observation does not rule out embedding the abstract contraction as a postselected branch of a larger legal asynchronous protocol. No such embedding or exclusion was established here. Near saturation of the other coordinate's singleton bound may impose further constraints beyond global entire contraction and reflection symmetry.

This exact example refutes the proposed coordinate-by-coordinate analytic Q tensorization lemma at the level at which that lemma would be used. It does not refute the actual asynchronous endpoint product.

## 7. Legal finite-model attempts and numerical boundary

All model searches used fixed numerical random seeds and already installed libraries. Their Hamiltonians do not read selected private control signs or mathematical record outcomes. Broad parity and seed-factorized families were kept separate.

The broad family has four joint parity sectors of bath dimension d. H_0 is arbitrary Hermitian block diagonal. V_1 has arbitrary complex bath edges 00--10 and 01--11; V_2 has edges 00--01 and 10--11. Each edge is divided by at least its spectral norm, so each V_i has norm at most one. This admits conditional sector couplings under the broad parity contract but does not claim that every such coupling has the original factorized seed form.

The seed family has `H_0=I_seed tensor B`, `V_1=X_1 tensor A_1`, `V_2=X_2 tensor A_2`, with Hermitian A_i normalized to norm at most one. This is within the additive private-sign virtual-seed algebra. The initial bath state is optimized by taking the top eigenvalue of the initial-sector endpoint effect, rather than testing only one bath vector.

The staggered three-stage schedule pinches coordinate 1 after stage one and coordinate 2 after stage two. Every stage has actions .35 per coordinate, hence own gaps (.35,.70) and (.70,.35), and `Q_1Q_2=0.234060656831004` numerically. A further family splits each stage into three controlled subsegments and separates free sector-preserving baseline rotations from charged interactions.

The exact independent sink baseline uses a 9-dimensional physical bath, two independent three-level sink flags, and the seed-factorized form. It saturates Q_1Q_2 for this asynchronous schedule. Norm-preserving bath conjugations of each interaction and arbitrary seed-independent bath baselines give a legal neighborhood with shared, generally noncommuting bath operators. The 960 random perturbations and four local optimizations in a 108-parameter sparse bath-control family found no value above the product.

Local optimizer convergence flags and evaluation limits are recorded. A local optimum, absence of a violation, small hypothesis residual, or an equality check at the sink is not a universal proof. Search families and bath dimensions are finite. No numerical candidate was promoted to a refutation.

Some NumPy 1.26/Apple BLAS matrix products emitted floating-point status warnings despite bounded finite model entries; final candidates were recomputed separately with NumPy 2.5 and explicit einsum matrix multiplication. The independent verification receipt records finite output, unitarity, exact-shape hypothesis residuals, and discrepancies. This does not certify the optimizer globally.

## 8. Original-Walsh receiving and physical limits

The pinned additive private-sign model is

    H_(f,b)=H_base+sum_i (-1)^f_i xi_i,b A_i,

where selected initial bits and fair refresh bits are independent and all physical coefficients and common dilations are independent of them. There are no terms bearing products of selected signs. Mathematical seed qubits initialized in the X-plus state give Hamiltonian `I tensor H_base+sum_i Z_seed,i tensor xi_i,b A_i`. Projecting seeds onto X-minus gives exactly the selected Walsh amplitude with normalization `2^(-|S|)`.

Gauge away xi using seed X toggles. The initial and final X-basis labels are invariant under the gauge. Averaging each private fair toggle at its prescribed node gives the exact complete seed pinch. Hadamards put this into the parity convention used above. Therefore the anchored theorem applies to the original averaged positive Walsh effects on the whole physical input/reference space under this qualified interface.

The broad sector-conditional search family is not automatically a literal factorized virtual-seed Hamiltonian. Conversely, the seed-factorized sink and its bath-conjugation perturbations do satisfy the additive private-sign algebra. Neither the virtual dilation nor any bound supplies a physical syndrome detector, finite-width pulse model, protected controller, reset, calibrated envelope, scalable memory construction, or uncharged simultaneous control. Full support/completion/covariance/privacy assumptions and all implementation costs remain receiving gates.

## 9. Priority and final status

The sharpened real entire-function Bernstein inequality is classical. Random fixed-grid dynamical decoupling is established prior art in the inspected pinned sources. The anchored receiving bound is an internally derived improvement over the specific incoming asynchronous certificate, not a claim of historical novelty. Only the stated primary entire-function source was independently checked for this investigation; no exhaustive prior-art search was performed.

Rigorous: sine-lemma reconstruction; synchronized and singleton reconstruction under stated assumptions; anchored asynchronous certificate; exact abstract counterexamples and their scoped limitations; algebraic original-Walsh transfer under its qualified premises.

Finite evidence only: optimized Hamiltonian examples, bath sizes, perturbation neighborhoods, residuals, and numerical equalities.

Unresolved: a proof or legal finite shared-bath counterexample for the full arbitrary-asynchronous endpoint product, exhaustive historical novelty, external analytic review, and physical implementation.
