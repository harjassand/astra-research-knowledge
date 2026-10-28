# Joint growing-selector and decoder discovery without source resets

28 October2026. **NEW PROOF CANDIDATE; independent receiving pending.** All received prequential/fixed-selector sources remain immutable. This construction removes TWO restrictions together in a supplied common-decoder family: the encoder need not be fixed, and the source gauge memory need not reset. It uses two ordinary, conditionally unbiased learners and an honest epsilon^(-2) source cap. It does NOT substitute the fast positive-loss theorem where noisy anchors have a nonzero oracle floor.

## 1. A physical supplied selector family and retained-memory source

The source input is a known logical qubit L and a known m-dimensional selector S. A supplied encoder prepares a REAL unit vector |x>_S, x in R^m, independently of L, then sends S,L through the same complete physical port. A fixed known input embedding may be included and paid. This is a growing selector-state family, not arbitrary circuit-encoder optimization. A selector requires ceil log2m qubits but general known amplitude preparation takes O(m) controlled two-level rotations before routing/precision overhead; poly(log m) control is not claimed.

The source output P is a known w-qubit physical patch, d=2^w. It retains arbitrary quantum memory M. Its complete causal map is stipulated to have a fixed unknown U:L tensor G→P, dimG=d/2, and CP maps

    G_(alpha,t,h_public):S tensor M→G tensor M',
    alpha=I,X,Y,Z,
    sum_alpha Tr_G G_alpha trace preserving,
    G_I−G_alpha completely positive for everyalpha.      (1)

On all inputs, including correlated logical/memory inputs, the complete map is

    Efrak_t=Ad_(U tensor I_M') composed with
                  sum_alpha (Ad_(P_alpha) tensor G_alpha). (2)

Tensor-order permutations in(2) are the known register reorderings, not an unknown alignment resource. The source may store quantum information about prior selectors and vary its gauge emission/Pauli instrument with time or exposed past history. U is shared across selectors and histories. CP-order dominance is a STRONG SUPPLIED STRUCTURAL PROMISE, not inferred from finite counts. No gauge eigenvalue floor, positive generator-contrast kappa, source inverse or observed noise flag is supplied.

The current complete map is independent of fresh PRIVATE probe-role, axis/sign, Pauli measurement, selector-design and terminal-time coins except through the specified quantum input. Receiver controls are private until the call is complete. Same-port/routing/timing conditions, initially independent full QR payload state, trusted payload holding and isolated terminal output are as in the received one-terminal memory theorem. Its actual-reference channel transfer is imported, not an iid state-estimation oracle.

For each actual past record h, the current memory density defines E_(h,x):L→P on a new independent input. The fixed hidden decoder

    D_*(r)=Tr_G(U†rU)

is full-CPTP optimal for EVERY current selector and memory history. This follows from the received Bell-block dual argument: CP dominance implies H_I(x)>=H_alpha(x), and every recovery supplies positive Bell-diagonal effects T_alpha summing toI_G. No sign contrast is needed for this constrained-CPTP optimum.

## 2. The nonnegative quadratic excess that allows joint learning

For any fixed physical decoder D, define current Bell excess

    R_h(x,D)=ell(D E_(h,x))−ell(D_* E_(h,x))>=0.          (3)

The source is linear in |x><x|, so its restriction to real selectors is a REAL symmetric quadratic x^T B_h(D)x. The nonnegativity for everyrealx means B_h(D)>=0. Consequently, for every unitrealx,

    R_h(x,D)<=Tr B_h(D)
              =m*(1/m)sum_(b=1)^m R_h(e_b,D).           (4)

This is a difference-effect domination, NOT a uniform density/Bures estimate or an anchor-noise bound. Its factor m is paid. It does not assert that the raw noise at every selector is small. All contrasts, rare gauge weights and source environment dimensions are absent from(4).

For each D, the ordinary six-state return-mismatch mean is

    p_h(x,D)=(2/3)ell(D E_(h,x))=x^T A_h(D)x,
    0<=A_h(D)<=I_m                                     (5)

as a real symmetric matrix. It is the real part of the physical selector effect, not a learned observable supplied for free. If X is a real density matrix, a classical ensemble of pure real selectors with mean |x><x|=X has average loss Tr[A_h(D)X].

The eventual comparator is the best FIXED real selector and full-CPTP decoder on the declared controller's genuinely visited occupation:

    ell_*=(1/N)inf_(||x||=1)sum_t E_h[ell(D_* E_(h,x))]. (6)

Because D_* is pointwise optimal, allowing an arbitrary decoder for each x or history cannot improve(6) while x remains fixed. An encoder that changes with the current history CAN do better; (6) is not a dynamic-encoder oracle or a counterfactual trajectory. The same ideal-trusted-interface convention as the received memory sources is retained when implementation discrepancy is added: the unknown noisy source is unchanged, but no free transfer of a comparator to different imperfect-control histories is claimed.

## 3. Two actual probe roles on one memory history

The learner maintains a normalized physical decoder Choi C_t in K_D and a REAL selector density X_t in K_S={X>=0,TrX=1}. Both depend only on earlier records. Before each call choose a fresh private fair role coin.

**Decoder-anchor role.** Draw b uniformly from{1,...,m}. Prepare selector e_b and an ordinary logical six-state input |j,s>. Measure one uniformly chosen physical w-qubit Pauli word W, with actual parity outcome a in±1. As in the received slow prequential source, the rational record

    g_D=−(d²/2)s a(sigma_j tensor W^T)                  (7)

has conditional mean equal to the normalized-Choi gradient of the UNIFORM-ANCHOR average calibration loss g_h(C)=(1/m)sum_b p_h(e_b,D_C). This role does not need to apply the current decoder. One source output, actual local Pauli controls and the parity record are paid; no coefficient oracle is used.

**Selector-effect role.** Draw a REAL finite even-fourth-design z: with probability2/(m+2), choose a uniform basis vector; otherwise choose m independent signs divided bysqrt(m). Prepare selector z and an ordinary six-state logical input, apply the CURRENT ACTUAL decoder D_(C_t), and record its return-mismatch bit y. Define

    T(z)=m(m+2)zz^T/2−mI_m/2,
    g_S=y T(z).                                        (8)

The received finite-design identity is

    E_z[(z^T A z)T(z)]=A,
    ||T(z)||_F²=L_m=m³(m+3)/4<=m^4.                    (9)

Thus E[g_S|h,roleS]=A_h(D_(C_t)) EXACTLY, with the current decoder frozen before the current query. No whitening, source inverse or exact scalar task oracle appears. T(z) is rational for every design point despite the normalized signs. The logical input is ordinary; no entangled source reference is retained.

The actual update gradients are

    G_D,t=2 I_roleD g_D,     G_S,t=2 I_roleS g_S.         (10)

They are conditionally unbiased for their TWO different current objectives. Their histories and records are correlated; no independent-bank assumption is made. Since the role is fresh at the SAME pre-call memory history, importance weighting is valid even though previous roles changed the source's retained state. Set

    G0=d² 2^ceil(w/2),
    ||G_D,t||_F<=2G0,  ||G_S,t||_F<=2m².               (11)

The selector objective A_h(D_(C_t)) is allowed to depend on the current decoder and all prior data; it is fixed before the current role/design coins. This is ordinary adaptive online convex learning, not a claim that the two unknown objectives are stationary or independent.

## 4. Finite projections and physical selector sampling

Choose N a power of4. Initialize C_1=I_(2d)/(2d), X_1=I_m/m, and use rational steps

    eta_D=1/(2G0 sqrt(N)), eta_S=1/(2m² sqrt(N)),
    xi=1/(16N²).                                       (12)

For each set, return an EXACTLY feasible rational point whose squared Frobenius distance to its current gradient step is withinxi of the true Euclidean projection. The received slow source supplies this finite Choi projection with a known-center SDP, fixed dyadic grid and exact TP/PSD repair. It is used on every history, including bad-looking data; a numerical fallback cannot be falsely counted as optimization success.

For completeness the selector projection has an equally explicit repair. Suppose a rational symmetric Xtilde has lambda_min>=−delta and |TrXtilde−1|<=delta. Set

    Xhat=Xtilde+(1−TrXtilde)I_m/m,
    Xphys=(Xhat+3delta I_m)/(1+3m delta).                (13)

It has trace1 and lambda_min>=delta/(1+3m delta)>0. For delta<=1/(4m), the trace norm change is at most10m delta: the trace correction costsdelta; Xhat has trace norm<=1+4m delta<=2; the subsequent mixture costs at most9m delta. On the bounded projection objective this gives a finite O(m delta) debit. Choose delta<=xi/(4096m), prescribed dyadic solver-entry grid sufficiently finer than delta/(64m), and allocate solver/rounding slack belowxi/4 each. The known interior point I_m/m and exact rational certificates yield the required finite weak quadratic solve. Fixed output grids reset bit lengths instead of permitting recursive denominator growth. The solver and all rational certificates have deterministic polynomial bit-operation caps in m,d,N and the input precision.

At a payload call, a physical PURE real selector is sampled from X_t without an uncharged eigenbasis. Exact rational LDL factorization gives

    X_t=sum_i D_i l_i l_i^T,
    w_i=D_i||l_i||²>=0, sum_i w_i=1,
    x_i=l_i/||l_i||.                                   (14)

All w_i are rational. Zero columns, if any, are omitted; the numerical repair actually makes X_t strictly positive. Sample i from these actual rational weights, then prepare the known normalized REAL vector x_i. This classical mixture has covariance X_t exactly in the ideal interface. No selector purification/reference is secretly retained. The LDL arithmetic is polynomial in m and rational bit length; preparing each sampled x_i requires O(m) known amplitude rotations plus compilation. Rational-weight sampling and all approximation errors are paid in §7.

## 5. Joint regret, without a nonconvex discovery assumption

The pathwise finite-projection argument of the received slow source applies separately to each known convex set. Their centers have squared radius at most1 and diameter at mostsqrt(2). With(11),(12), for every fixed decoder C_* and fixed selector density X_*, conditional unbiasedness gives

    sum_t E[g_h(C_t)−g_h(C_*)] <=4G0 sqrt(N),
    sum_t E[Tr A_h(D_(C_t))(X_t−X_*)] <=4m² sqrt(N).    (15)

These are expectations on the SAME actual mixed-probe process, not two independently acquired data sets. C_* and X_* are fixed; a trajectory-hindsight choice would need another argument. Although C_* may be unknown/rank deficient and X_* may be pure, both are feasible comparators for the projection bounds.

Take C_*=C_(D_*) and X_*=x_*x_*^T for any fixed unitrealx_*. For each history decompose the mean Bell loss:

    ell_h(X_t,D_t)−ell_h(x_*,D_*)
      = [ell_h(X_t,D_t)−ell_h(x_*,D_t)] +R_h(x_*,D_t).

The first bracket is the selector's linear regret times3/2. Bound the second by(4); its anchor average is exactly the decoder's excess calibration loss times3/2. Therefore

    (1/N)sum_t E[ell_h(X_t,D_t)]
       <=ell_*+6(m²+mG0)/sqrt(N).                       (16)

This removes the joint nonconvex optimization problem ONLY because one supplied common decoder is pointwise optimal and its excess difference is a positive quadratic in selectors. A generic unknown family lacking that structure does not satisfy this reduction.

## 6. One actual privately timed joint encoder/recovery decision

Choose T uniformly from{1,...,N} privately at initialization. Before T run the two-role probes and updates. At T, freeze the current C_t and X_t, sample the real selector by(14), send the independently held unknown payload with that selector through the SAME source port, apply the frozen physical decoder, isolate the output and stop. Do not measure or update from the unknown payload. Padding and all preprocessing make the current role unobservable through timing/control labels before completion.

For T=t, the actual prior history is precisely the two-role all-probe history. The resulting actual payload channel is the convex mixture

    Lambda=(1/N)sum_(t,h,i) p_t(h)w_(t,h,i)
                                 D_(t,h) E_(h,x_(t,h,i)). (17)

This equality is of complete CPTP maps, hence preserves an arbitrary independent reference. It does not use a source reset or assume that the chosen decoder works on an unseen future gauge. Its Bell loss is the left side of(16).

For 0<epsilon<=1 choose the least power of4 satisfying

    N>=(12(m²+mG0)/epsilon)².                           (18)

Then statistical excess is at mostepsilon/2 and

    N<576(m²+mG0)²/epsilon²
      <=[1152m^4+2304m²d^5]/epsilon².                  (19)

One complete operational implementation allowance nu<=epsilon/2 gives averaged terminal Bell loss<=ell_*+epsilon. The comparator(6) remains on the declared ideal trusted-interface controller's mixed occupation against the given unknown noisy source, as in the received memory theorems. No free comparator transfer to physically imperfect histories or a dynamic encoder oracle is asserted. The bound is additive and therefore also implies a multiplicative-plus-additive bound with any gamma>=0, but no gamma-dependent faster rate is claimed.

## 7. Finite physical ledger and comparison

* At mostN COMPLETE source calls, including ONE genuine unknown payload. Every input uses one logical qubit plus ceil log2m selector qubits. Each output is the known w-qubit patch. There is no environmental reconstruction or protected entangled calibration reference. The unknown payload is held in trusted storage for the entire paid prefix, and the recovered output is isolated.
* Anchor probes use at mostw local Pauli measurements and parity acquisition. Selector probes apply the actual learned general CPTP decoder, then one logical return measurement. The terminal decoder uses the same finite exact-reference Choi/Stinespring synthesis as the received sources: environment at most2d, known unitary embedding at most4d, at most two additional reset qubits, dense O(poly(w)4^w) gates before precision/routing overhead. No false equivalence to a cheap two-reflection compiler is asserted.
* The m-state selector controls are real, supplied and paid. Known basis inputs and normalized-sign design points are actually prepared; sampled payload selectors use the rational LDL mixture. O(m) amplitude synthesis is charged per general pure selector, with O(poly(m)) classical matrix processing. The family is not polynomial-control in log m merely because its register has log m qubits.
* There are two finite quadratic projections per potential round; zero-gradient roles can retain their old point. All returned points have exact rational feasibility and prescribed bounded denominator grids. Dense classical processing is polynomial in d,m,N, not claimed efficient in output widthw. Compile/pad the necessary current decoder/selector description before every potential terminal call; count its classical duration toward payload idle storage.
* Uniform T needs log2N bits. Each probe role needs one bit; physical W needs2w bits when used, logical sign one bit, and the normalized-sign design needs at mostm bits. Uniform integers for j, b, the design mixture in{0,...,m+1}, and its basis choice have a fixed worst-case number of draws per round. Each uses rejection from a binary interval of at most twice its range, capped at R=ceil log2(16N/nu_rng) retries. The ideal payload LDL weights share an integer denominator with bit length polynomial in m and the prescribed grid precision; use a uniform integer below it with the SAME type of finite capped sampler, then cumulative integer weights. Its rounding-free probability law is exact on success. Charge the worst-case denominator bit length and number of draws BEFORE outcomes, not merely log m bits for a general rational distribution. At most8N capped uniform draws conservatively cover all hypothetical preparation branches; exhaustion costs at mostnu_rng/2. A full bit cap is polynomial in N,m,w and these explicitly bounded rational bit lengths.
* Source/selector preparation, decoder synthesis, measurements, storage, timing/privacy and capped random-sampler discrepancies fit ONE declared complete-process implementation allowance. Physical fallbacks do not validate an uncertified solver. No high-probability iid confidence statement is hidden in the expected conditional-regret proof.

Known noise turns the fixed-selector ideal objective into an ordinary PSD effect/eigenvalue problem. The strongest equally informed conventional learner can use exactly these two online convex estimators and the same common-decoder promise. No quantum learning advantage, generic circuit optimization solution, unassisted capacity statement, or empirical count-acquisition result is claimed.

## 8. Why the received fast bandit rate cannot simply be substituted

Take a fixed unknown real unit selector v and a logical Pauli source with

    p_I(x)=1/4+(3/4)|v^T x|²,
    p_X(x)=p_Y(x)=p_Z(x)=(1−|v^T x|²)/4.                 (20)

These are supplied-family-compatible CP selector effects: the nonidentity branches use(I−|v><v|)/4, identity uses I/4+3|v><v|/4, and identity dominates everyother branch. A fixed hidden output unitary can make the decoder genuinely unknown. Selector v is perfect. Nevertheless the UNIFORM-ANCHOR oracle Bell loss is

    (3/4)(1−1/m),                                      (21)

which stays bounded away fromzero as m grows. A first-order bound on raw anchor loss can therefore carry a large oracle floor, even though the best selector has zero noise. Its multiplicative slack is not automatically a fast EXCESS-decoder bound. Substituting that theorem and silently claiming epsilon^(-1) would be invalid. The slow finite-gradient regret above pays epsilon^(-2) honestly and removes this floor by comparison, not by assuming it absent. Fast excess acquisition in this non-reset joint setting remains a separate open improvement.

The received multi-payload mixed-service mechanism may later combine with these two acquisition roles, with a different slow q²-type source scale and the same cumulative-comparator/global-reference restrictions. That composition is not included in this one-terminal source's claim.
