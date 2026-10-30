# Independent review: finite-depth relative Taylor remainder
2026-10-30. Reviewer: `producer-workspace/review_simple_compiler`.

## Verdict and scope

**PASS as a general local algebraic lemma under its stated uniform finite-depth/local-decomposition hypotheses.** Noncommuting color layers, unequal real proof strengths and indefinite total Delta do not invalidate the estimate. No global norm/condition-number cancellation is being assumed.

Reviewed source: `producer-workspace/FINITE_DEPTH_RELATIVE_TAYLOR_LEMMA.md`, SHA-256

`7a422ed268e653e6d36634f6657c2de852c6850f65cf87d318710b5387faf853`.

Exact bytes are preserved in `reviewed_sources/`. I have not changed this source or any earlier recipient review. The physical-tilt paragraph is read with **W0 strictly positive/invertible**, as its displayed inverse requires. For the parameter scaling claimed at the end, all local bounds, circuit depths and witness norms must be uniform in the parameters being sent small. These are necessary explicit qualifications, not an actual native-LOCC verification supplied by this lemma.

## 1. Exact relative Hamiltonian and Kraus algebra

Let `A_u=Y A Y^{-1}`. Since `G=Y†Y`, direct multiplication gives

    Y^{-†} J† G J Y^{-1} = J_u† J_u,
    Y^{-†} Gamma G Y^{-1} = Gamma_u†,
    Y^{-†} G Gamma Y^{-1} = Gamma_u,

for Hermitian `Gamma=J†J`. For Hermitian H,

    Y^{-†} i[H,G] Y^{-1} = i(H_u†-H_u).

Likewise, each Hermitian local D contributes `-(D_u+D_u†)/2`. These identities use neither commutation of the circuit layers nor positivity of D. Thus the source's formula (2) is exact, with the correct Hamiltonian sign and order. Every resulting contribution is Hermitian.

At zero, each conservative dissipator and Hamiltonian term vanishes, while the signed killing gives `B(0)=-Delta`. This zero-order cancellation occurs **term by term**; it is not estimated using the extensive norm of the total generator.

## 2. First derivative, including the signed killing

For a fixed set of weights and fixed layer order,

    Y(0)=I,  Y'(0)=X/2,  G'(0)=X,
    X=sum_i w_i X_i=X†.

The inverse-congruence derivatives multiplying `L_c(I)` vanish because the generator is conservative. Therefore the derivative of the relative conservative part is exactly `L_c(X)`.

For any A, `A'_0=[X,A]/2`. In particular `[X,Delta]†=-[X,Delta]`, giving

    d/du [-(Delta_u+Delta_u†)/2]_(u=0)=0.

Hence `B'(0)=L_c(X)`. There is no first-order killing error even if Delta is indefinite or fails to commute with X. Self-adjointness of X and Delta is load-bearing. Positivity of Delta is not. Noncommuting color order first appears in higher derivatives and does not change this calculation.

## 3. Exact cone reduction before taking derivatives

Here is a quantitative proof of the uniform second-derivative estimate.

Let q be an upper bound on the site cardinality of an elementary generator operator H_e, J_e or D_e (Gamma_e has the same support as J_e). Let k>=1 bound the site cardinality of a proof gate, K bound `||X_i||`, and D be the fixed number of disjoint-support layers. On a bounded-degree graph the fixed-radius assumptions imply such fixed q,k. If bounded support is specified directly by cardinality, the following argument needs no stronger metric assumption.

Conjugate a local A through the layers in the order dictated by `Y A Y^{-1}`. At the start of a layer suppose its structural support has at most m sites. Because same-layer gate supports are pairwise disjoint, at most m gates in that layer meet that support. Every other gate commutes A and also commutes all the retained gates of that layer. It can therefore be canceled with its inverse **exactly**, before any estimate. The surviving layer enlarges the support to at most k m sites. Iterating gives at most `q k^D` sites and at most

    M <= q sum_(j=0)^(D-1) k^j

retained gates. For k=1 this means M<=qD. These are conservative bounds. The selected structural gate list is independent of u; accidental cancellations at particular u are not used.

Consequently `A_u` is exactly a product containing A and at most 2M exponential factors `exp(±u w_i X_i/2)`. Define `L=M K`. For all `|u|<=u0`, repeated product differentiation and submultiplicativity yield

    ||A_u|| <= exp(u0 L)||A||,
    ||A'_u|| <= L exp(u0 L)||A||,
    ||A''_u|| <= L^2 exp(u0 L)||A||.

For example, in the second bound the sum of norms of all 2M exponential generators is at most M K; the second derivative has the corresponding ordered two-position sum, bounded by its square. Noncommutation changes the terms but not these norm estimates. No `||X||`, `||Y||` or global inverse condition number appears.

Apply these bounds individually to every H_e, J_e, Gamma_e and D_e in the exact formula. The second derivative of the gain satisfies

    ||(J_u†J_u)''||
      <= 2||J''_u||||J_u||+2||J'_u||^2
      <= 4L^2 exp(2u0 L)||J_e||^2.

The symmetric Gamma, H and D terms have the analogous constant bounds. The local decomposition has at most cN terms with uniformly bounded local norms. Thus `||B''(u)||<=C_2 N` for all `|u|<=u0`, with C_2 depending only on the declared fixed local constants and u0.

Taylor's integral formula, also for negative u, now gives

    ||B(u)-B(0)-uB'(0)|| <= (C_2/2) N u^2.

Substituting the zero and first derivatives proves the claimed inequality and, since the remainder is Hermitian, its Loewner upper bound. This is the missing O(N), rather than O(N^2), remainder argument. It relies on finite depth and exact layerwise support cancellation, not an assumption that extensive norms somehow cancel.

## 4. Unequal strengths and uniform small-parameter use

Given any real epsilon_i, choose `u=max_i|epsilon_i|` and `w_i=epsilon_i/u`; take all weights zero if u=0. For this one radial interpolation the weights are fixed. There is no differentiation of the nonsmooth maximum function or of w_i. The preceding constants are uniform over all `|w_i|<=1`, so

    B <= -Delta + sum_i epsilon_i L_c(X_i)
                   + C N max_i|epsilon_i|^2 I.

This permits different signs and unequal strengths in different layers. The Xi need not commute between layers.

If `0<lambda<=1`, debt strength is O(sqrt(lambda)t), other strengths are O(lambda t), and the constants above remain uniform, then the maximum squared strength is O(lambda t^2). Relative to an actual useful coefficient bounded below by `c0 lambda t` with fixed c0>0, this remainder contributes O(t) times the extensive identity. It can be affordable for a fixed positive energy-density barrier.

That last conclusion is **conditional**. A witness norm, support/color depth, local tilted coefficient or inverse local factor that diverges as lambda or t decreases could invalidate the asserted scaling even though the lemma remains true for each fixed apparatus. A first-order O(sqrt(lambda)t N) source is not absorbed by this argument. The useful coefficient, first-order debt/exposure/activity inequalities and their constant hierarchy must be separately earned for the actual generator.

## 5. Physical tilt conventions and conservative completion

Let the physical Heisenberg generator have the convention

    L*(O)=sum_e J_e† O J_e+K†O+OK,
    K=-iH-(1/2)sum_e J_e†J_e.

For `S=W0^(1/2)>0`, define `L_w(O)=S^{-1} L*(S O S) S^{-1}`. Direct algebra gives

    J'_e=S J_e S^{-1},  K'=S K S^{-1},
    L_w(O)=sum_e J'_e† O J'_e+K'†O+OK',
    Delta=-sum_e J'_e†J'_e-K'†-K'.

Thus

    L_c=L_w+{Delta,·}/2
       = i[H_c,·] + sum_e (J'_e† · J'_e
                            -{J'_e†J'_e,·}/2),
    H_c=(K'†-K')/(2i)=H_c†.

This is a conservative GKLS generator even if Delta is indefinite. The tilted semigroup is CP by invertible positive congruence similarity, but indefinite Delta does **not** imply a subunital/killed interpretation. The relative Taylor proof needs no such interpretation.

For `W=S G S=(YS)†(YS)`, the exact physical identity is

    (YS)^{-†} L*(W) (YS)^{-1}
        =Y^{-†} L_w(G)Y^{-1}=B.

The order is YS, not SY. The source uses the correct convention. Congruencing the resulting inequality back is order-preserving; it multiplies the extensive identity remainder into `CNu^2 W`, without any global condition-number estimate. The first-order and killing terms must likewise be pulled back by the exact same congruence, not silently replaced by raw operators in another frame.

An arbitrary faithful global W0 need not make J'_e or K' local, nor give a bounded local decomposition of Delta and H_c. Those are application hypotheses, not consequences of invertibility or positivity. The separate local-discount representation and actual raw-energy commutants must establish them. If W0 has a kernel, the stated full-space inverse formulas are undefined; an invariant-support reformulation would require its own hypotheses.

## 6. Independent finite algebra check and final boundary

`check_relative_taylor.py` tests N=2,...,5 qubits with three noncommuting local color layers, unequal positive/negative weights, nonzero Hamiltonian, nonnormal jump operators and signed indefinite total Delta. Exact-formula residuals are below 7e-16; the central first derivative agrees within 5e-9; measured remainder divided by Nu^2 remains finite for the tested positive and negative u. A separate genuinely conservative physical generator is tilted by noncommuting positive S. The conservative-completion identity agrees within 2.4e-15 and the YS physical congruence within 4e-16. These tests check signs/conventions only; the uniform-N theorem is the cone proof above.

The result supplies the proposed rigorous relative local-circuit remainder. It does not prove the actual LOCC local tilt, the useful-service/debt/activity first-order estimate, an exclusive-credit discount formula, weak-LOAD coverage, a scalar Foster inequality, initialization, or the common logical/confinement bridge. No whole continuous-noise LOCC lifetime theorem is accepted by this receipt. Earlier native-recipient and other whole receipts are unchanged. No external upload/publication occurred.
