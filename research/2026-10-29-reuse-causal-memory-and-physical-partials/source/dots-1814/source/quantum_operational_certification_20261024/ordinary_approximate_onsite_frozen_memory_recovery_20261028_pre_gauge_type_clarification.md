# Approximate on-site ordinary calibration: a frozen all-memory decoder with the correct quadratic floor

28 October 2026. **New candidate; separate receiving required.** Originals and earlier receipts are unchanged. This is a perturbative extension of the received exact on-site source `ordinary_onsite_two_axis_frozen_memory_recovery_20261028.md`, SHA256 `7df4d169cc544b79456e7410da7ac3ec991482311a0d3831569efc573455dd53`. It uses a conventional normalized two-vector Wahba/proper-Procrustes fit. There are no new sampled source calls, production optimizer timings, or hardware claims.

## Result and the two necessary changes

Suppose the two exact logical Pauli generators of each logical input are within operator norm tau<=1/4 of an unknown on-site oriented Pauli pair. The physical source otherwise retains the arbitrary coherent Pauli/gauge memory and CP-order contrasts of the exact source. A finite ordinary calibration learns the unknown sites and a product receiver. Freeze it, then introduce one unknown simultaneous q-qubit payload/reference at any later specified time while the structural promise persists. With source-call cost

    O(kappa^(-2) log(qn/beta)
      + q kappa^(-2) epsilon^(-1) log(q/beta)),

the ACTUAL averaged excess Bell loss against the current-state full-CPTP oracle is at most

    min(1, 9 q tau^2 + epsilon),                         (R1)

under the explicit implementation allocations below. The sharper good-record bound is

    ell_excess <= (3 sqrt(q/2) tau + sqrt(epsilon)/3)^2.  (R2)

The systematic floor is **q tau^2, not q tau^2/kappa^2**, and does not accumulate over calibration calls. Two changes from the exact learner matter:

1. Select the MAXIMUM coarse site score, rather than the first score above a fixed threshold. True signal and wrong-site leakage have the SAME unknown contrast weight.
2. Normalize each acquired X/Z column before the proper-rotation fit. Positive contrast blocks give a relative directional perturbation, not a fixed additive 3 tau bias.

A physical hidden-gauge construction proves that no finite fixed-horizon calibration and arbitrary frozen full-CPTP receiver can uniformly remove an Omega(min(1,q tau^2)) floor over this source class. Thus the order is a genuine future-information limitation, not merely this learner's analysis. The result does not reconstruct or invert the full approximate encoding, infer model membership, remove the source's CP/order assumptions, or solve general wide-support acquisition.

## 1. Physical source and approximation promise

Use the same known n-output-qubit register, q ordinary logical input qubits, complete current-port privacy, paid preparation/readout/control and source family as the exact on-site source. Explicitly, each current source map is

    Ad_(U tensor I_M') o sum_alpha(Ad_(P_alpha) tensor G_alpha),  (1)

where U:L tensor G -> P is unknown, dim(L)=2^q, dim(G)=2^(n-q), the maps G_alpha:M->G M' are CP, and sum_alpha Tr_G G_alpha is TP. They may depend arbitrarily on time and exposed past history. Put

    G_total=sum_alpha G_alpha,
    H_(i,j)=sum_alpha chi_(i,j)(alpha) G_alpha,  j=X,Z.

The supplied rational margin 0<kappa<=1 obeys

    H_(i,j)-kappa G_total is CP.                         (2)

Also G_total-H_(i,j) is CP automatically. To claim the strongest full-CPTP oracle, separately assume

    G_I-G_alpha is CP for every alpha.                  (3)

Without (3), every upper comparison below remains against ideal logical extraction, but that decoder is not asserted optimal.

For each i there is an unknown physical site pi(i) and unknown R_i in SO(3), with A_(i,j)=(R_i e_j) dot sigma on that site, such that the exact generators

    B_(i,j)=U(sigma_(i,j) tensor I_G)U^dagger

satisfy

    ||B_(i,j)-A_(i,j)||op <= tau, j=X,Z, 0<=tau<=1/4.   (4)

These are global operator-norm bounds, not state-averaged tests. A_(i,X), A_(i,Z) are exactly an oriented orthogonal on-site pair. Neither their axes nor their sites are supplied to the learner. The rational upper bound tau, like kappa, is a structural promise and is not certified by finite calibration data. No source gauge eigenvalue floor is assumed.

The sites in (4) are necessarily distinct. If two logicals shared a site, exact cross-logical commutation and (4) would imply

    ||[A_(i,j),A_(k,X)]||op<=4 tau, j=X,Z.

For unit vectors a_x perpendicular to a_z and b, the squared cross-product norms obey |a_x cross b|^2+|a_z cross b|^2>=1, while the two commutator bounds imply this sum is <=8 tau^2. That would require tau>=1/(2 sqrt(2)), contradicting tau<=1/4. This establishes the physical distinct-site product receiver rather than assuming compatible learned marginal channels.

All promises hold at every allowed conditional memory state, and continue through the future service. The full unknown payload/reference is introduced after calibration product with source/acquisition, or conditionally product given the allowed classical record. No unknown payload is held during training. A future service can occur after arbitrary intervening source-memory evolution; the structural promise, not the fitted data, licenses its use. This note proves one simultaneous q-input service, not indefinite multi-payload use.

## 2. A sharp relative contrast-cone lemma

Condition on the complete PRIOR record and average the other current private ordinary input labels. The physical output for logical i in the j-eigenstate of sign s is rho+s Delta_j, where

    rho=U(I_L/2^q tensor G)U^dagger,
    Delta_j=B_j R_j,
    kappa rho<=R_j<=rho,   [R_j,B_(k,l)]=0.             (5)

Here lambda_j=Tr R_j lies in [kappa,1]. The signed block R_j is positive because of (2), even though Delta_j need not be. All these statements also hold retaining the future-accessible memory and a purifier. Trace(Delta_j)=0 and ||Delta_j||1=lambda_j.

On the true site write Tr_(outside)(Delta_j)=(m_j dot sigma)/2, and let r_j=R_i e_j. Trace-norm contraction on Hermitian operators gives

    ||m_j||2<=lambda_j.                                 (6)

The radial identity is more useful than a crude additive perturbation bound:

    r_j dot m_j=Tr(A_j B_j R_j)
        =lambda_j-(1/2)Tr[(A_j-B_j)^2 R_j]
        >=lambda_j(1-tau^2/2).                         (7)

The trace is real because B_j R_j is Hermitian; expanding the square and using [B_j,R_j]=0 proves the identity without assuming [A_j,R_j]=0. Consequently

    ||m_j-lambda_j r_j||2<=lambda_j tau.                 (8)

For any time average, even along adaptive histories, the corresponding average mbar_j and lambda_bar_j obey (6)--(8) with the SAME fixed r_j. Put c=1-tau^2/2>=31/32. Since lambda_bar_j>=kappa, mbar_j is nonzero, and

    ||mbar_j/||mbar_j||2-r_j||2 <= tau,
    ||mbar_j||2>=c kappa.                              (9)

Indeed r_j dot mbar_j/||mbar_j||2 >=c, using ||mbar_j||2<=lambda_bar_j. This positive relative cone is why dividing a flat O(tau) bias by kappa loses unnecessary information.

For a WRONG site k!=pi(i), every unit local Pauli Q on k commutes with A_(i,Z). Since B_(i,Z) Delta_(i,X) B_(i,Z)=-Delta_(i,X),

    |Tr Q Delta_(i,X)|
      =|Tr[(Q-B_Z Q B_Z)Delta_(i,X)]|/2
      <=tau ||Delta_(i,X)||1=tau lambda_(i,X).          (10)

The last inequality uses ||[Q,B_Z]||op<=2tau. Thus the wrong-site reduced contrast has trace norm at most tau lambda_(i,X), not merely tau. The same lambda multiplies the true-site lower bound and every wrong-site upper bound, at every history.

## 3. Ordinary coarse acquisition: maximum scores

For rational 0<epsilon,beta<=1 set beta0=beta1=beta/2 and use

    L0=ceil log2(8 q n/beta),
    N0=ceil[3072 L0/kappa^2].                           (11)

Each actual block prepares all q inputs in independently signed X states and measures every output qubit in an independently chosen Pauli basis. Use the same actual one-copy matrices s_i(3 Pi-I), qn accumulators, and conditional matrix-martingale bound as the exact source. Its concentration proof does not require exact on-site support or zero wrong-site means: bounded increments, conditional variance and the one-copy identity remain unchanged. With probability at least 1-beta0 every averaged empirical 2-by-2 contrast is within kappa/8 in trace norm of its history-dependent average conditional contrast.

Compute every known score to additive kappa/16 by the received finite rational diagonalization. For each logical choose a site of LARGEST score, breaking ties by physical index. On the good event, if lambda_bar is its actual average coarse X contrast,

    true score >= c lambda_bar-3 kappa/16,
    any wrong score <= tau lambda_bar+3 kappa/16.

Their difference is at least

    (c-tau)lambda_bar-3 kappa/8 >=11 kappa/32>0.        (12)

Thus the unique best site is the true one; no tau/kappa restriction is needed. An optional threshold kappa/2 and distinctness guard both pass on this event. On any flagged history the COMPLETE fixed fine schedule below is nevertheless carried out, with predetermined placeholder accumulators if needed; at future service return a physical q-qubit replacement. These histories and every call/control cap are charged. A passed guard is not a source-membership test.

The original first-above-threshold rule is not imported: if kappa is small, a wrong-site contrast tau lambda_bar can exceed that threshold even though the true site is much stronger.

## 4. Fresh ordinary fine bank and rational normalization

For every fine block independently draw each input axis j_i from {X,Z} and its sign s_i, and measure all n output sites in independent uniform Pauli bases. Freeze the learned matching before this bank. On a correct coarse history form exactly from the actual labels

    F_(i,t)=6 s_i b_(pi(i)) e_(a_(pi(i))) e_(j_i)^T,
    Mhat_i=(1/N1)sum_t F_(i,t).

Its conditional mean has columns m_(i,X,t),0,m_(i,Z,t) from section 2. Define

    Mbar_i=(1/N1)sum_t E[F_(i,t)|entire prior history],
    N_i=Mhat_i-Mbar_i.                                 (13)

Unlike the exact theorem, Mbar_i need not have orthogonal columns. The contrast cone, not false orthogonality, is used below. Each of six scalar entries of F lies in [-6,6]. Conditional Hoeffding, iterated over the actual history, gives

    Pr(|(N_i)_(a,j)|>=x)<=2 exp[-N1 x^2/72].            (14)

Choose

    L1=ceil log2(24q/beta),
    N1=ceil[65536 q L1/(kappa^2 epsilon)].              (15)

Union over 6q entries then gives, except probability beta1,

    ||N_i||F^2<=kappa^2 epsilon/(128q) for every i.      (16)

Indeed the exponent at the scalar threshold is N1 kappa^2 epsilon/(55296q)>=(32/27)L1>=ln(24q/beta). This can first be conditioned on ANY correct coarse record. Within-shot logical/output correlations and subsequent source-memory backaction are not removed.

Let eta=epsilon/(128q). Normalize each rational empirical X/Z column mhat to an exactly rational vector p of norm <=1. If mhat is exactly zero choose the corresponding fixed unit coordinate vector. Otherwise every entry is a multiple of 6/N1, so ||mhat||2>=6/N1; rational square-root bisection on [0,6] supplies r>=||mhat||2 with width <=6 eta/N1, and set p=mhat/r. Then

    ||p-mhat/||mhat||2||2<=eta.                         (17)

This uses O(log(N1/eta)) bisection steps/bits, exact squared comparisons, and no source spectral inverse. Every record is defined and bounded. On (16), ||mhat_j||2>=c kappa-kappa/8>0, so the zero fallback is not entered on a good record.

The elementary normalization inequality ||x/||x||-y/||y||||<=2||x-y||/||y||, combined with (9), gives

    ||p_(i,j)-r_(i,j)||2
       <=tau+2||(N_i)_j||2/(c kappa)+eta.              (18)

Consequently, with P_i=[p_iX,0,p_iZ] and D0=diag(1,0,1),

    E_i:=||P_i-R_i D0||F
       <=sqrt(2)tau+2||N_i||F/(c kappa)+sqrt(2)eta.     (19)

No tau/kappa term occurs.

## 5. Conventional finite proper-rotation fit, with only two-column loss

Set delta=epsilon/(128q). Compute an exactly physical finite-control Rhat_i in SO(3) satisfying

    <Rhat_i,P_i>>=max_(R in SO(3))<R,P_i>-delta.        (20)

This is the conventional Wahba/proper-Procrustes problem applied to normalized direction observations. Wahba's original problem explicitly requires determinant +1; Shuster--Oh formulate unit-vector observations and a weighted squared-error criterion. [Wahba, original primary problem](https://pages.stat.wisc.edu/~wahba/ftp1/oldie/wahbasproblem.pdf); [Shuster--Oh, primary paper, section I](https://malcolmdshuster.com/Pub_1981a_J_TRIAD-QUEST_scan.pdf). No novelty of direction fitting, normalization, quaternion solution, or classical attitude estimation is claimed.

Use the exact on-site source's 4-by-4 real quaternion matrix K(P_i) and its finite rational Jacobi construction, importing only known-matrix arithmetic and control. Since ||P_i||F<=sqrt(2), ||K(P_i)||op<=sqrt(6)<3 on EVERY record. The original safe scale K/48+I/4 is still valid. The received primitive from `ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md`, SHA256 `8b5859b44e398d5d97d5b14580041bd9232b9fe59188a9c090634d6a4dbab0b6`, gives rational orthogonal columns and an off-diagonal residual <=delta/2. Select a largest diagonal label. Its rational unit quaternion supplies an EXACT reference SU(2) control with objective gap <=delta, including all zero/repeated-eigenvalue/bad-record cases. No free irrational control or eigengap premise is used; actual synthesis is paid below.

A direct two-column comparison is sharper than an unnecessarily conditioned full-rotation perturbation theorem. Both feasible rotations have two unit columns, so (20) is equivalent to

    ||Rhat_i D0-P_i||F^2<=E_i^2+2delta.

Therefore, putting d_i=||Rhat_i D0-R_i D0||F,

    d_i<=E_i+sqrt(E_i^2+2delta)<=2E_i+sqrt(2delta).     (21)

No fitted Y contrast or positive Y margin is assumed. The proper rotation supplies a physically oriented Y axis but the bound only pays for the two measured generators.

## 6. Full-reference extraction: quadratic, uniform, and without approximate factorization

The actual frozen receiver applies Vhat_i^dagger to the acquired distinct sites, keeps those q sites in logical order and traces the others. It is a physical product receiver on every unflagged record. Write Ahat_(i,j)=(Rhat_i e_j) dot sigma. For the virtual noiseless logical channel U(rho_L tensor sigma_G)U^dagger, let ell0(sigma) be its global q-input Bell loss after this receiver.

The following deterministic inequality holds for EVERY gauge state, including one entangled with retained memory:

    ell0(sigma)<=1/4 sum_(i,j=X,Z)||Ahat_(i,j)-B_(i,j)||op^2
       <=1/4 sum_(i,j=X,Z)(tau+||Rhat_i e_j-R_i e_j||2)^2. (22)

Proof: purify sigma and feed q Bell pairs, retaining the ENTIRE reference and purifier. The true stabilizer T_(i,j)=B_(i,j) tensor sigma_(R_i,j)^T fixes the encoded state. The candidate stabilizer S_(i,j)=Ahat_(i,j) tensor sigma_(R_i,j)^T has failure probability

    <(I-S_(i,j))/2>
       =||(S_(i,j)-T_(i,j))|Psi>||2^2/4.

All 2q candidate stabilizers commute: on one site both the physical pair and reference pair anticommute, and across sites they are disjoint. Their joint + projector is exactly the recovered global Bell projector. Its failure is at most the sum of individual failures. This proves (22) in operator norm without any factorization of the actual output, any independence of logical errors, any reconstruction of a gauge basis, or any q-fold global-unitary hybrid.

Taking the Euclidean norm over logicals, (19)--(22) imply

    sqrt(ell0(sigma))
       <=3 sqrt(q/2)tau
         +2 sqrt(sum_i||N_i||F^2)/(c kappa)
         +sqrt(2q)eta+sqrt(q delta/2).                  (23)

On (16), the last three terms are at most

    [2/(c sqrt(128))+sqrt(2)/128+1/16]sqrt(epsilon)
       <sqrt(epsilon)/3,                              (24)

using epsilon<=1, q>=1 and c>=31/32. This proves (R2) uniformly in sigma. In particular it includes actual future memory states that were never sampled during training. The exact algebra need not have an exact physical tensor decomposition aligned with the selected sites; the stabilizer argument replaces the commutant factorization used in the exact theorem.

The anisotropic version is useful: if (4) has individual bounds tau_(i,j), let T^2=sum_(i,j)tau_(i,j)^2 and c=1-(max tau_(i,j))^2/2. The structural term in (23) becomes 3T/2. Thus the leading no-statistical-error floor is at most 9T^2/4, rather than a worst-site bound when only a few generators are perturbed.

## 7. Strongest same-state oracle and physical implementation

For any current memory sigma, the Pauli/gauge Bell-block identity from the exact source gives, for any fixed physical receiver Dhat,

    ell(Dhat E_sigma)-ell(D_* E_sigma)
       =sum_(alpha!=I)Tr[(G_(I,sigma)-G_(alpha,sigma))T_alpha]
       <=ell0(sigma).                                 (25)

The positive gauge blocks T_alpha sum to I_G and D_*=Tr_G Ad_(U^dagger). Under (3), the displayed difference is nonnegative for EVERY full-CPTP decoder, so D_* is the pointwise full-CPTP optimum on the SAME actual current memory. The benchmark is not a counterfactual past learner trajectory. All of (22)--(25) holds for each good calibration record uniformly over future memory, and no posterior acceptance conditioning is used.

Require a complete implemented-calibration discrepancy nu_cal strong enough to bound TV of the retained classical calibration record uniformly over initial memory; a whole-process half-diamond/strategy distance retaining future-accessible memory suffices. Require the one actual future q-input service to be within nu_svc in whole-q-input HALF-diamond distance of the nominal frozen receiver/source service at its ACTUAL pre-call memory, including finite controls, preparation/output frames if used, routing and service storage. Allocate

    beta<=epsilon/8,   nu_cal+nu_svc<=epsilon/4.        (26)

Let Good be the mathematical record set with correct matching and (16). It has nominal probability at least 1-beta and physical probability at least 1-beta-nu_cal. For EVERY physical good record, (23)--(25) holds at ALL actual future memory states, including states affected by imperfect calibration. Bad records cost at most one. Thus

    actual mean excess
       <=(3 sqrt(q/2)tau+sqrt(epsilon)/3)^2
          +beta+nu_cal+nu_svc
       <=9q tau^2+(2/9+1/8+1/4)epsilon
       <9q tau^2+epsilon.                             (27)

If the upper expression exceeds one, use the trivial unit loss bound. The calibration discrepancy is paid once to record probability, not once per later memory state; this valid transfer relies on the state-uniform extraction inequality. Without the stated implementation interface the physical bound is not certified.

Optional operational service: pay for 2q fresh private input Pauli bits and inverse output frames through the complete nonanticipating port. The nominal full q-input averaged channel is then Pauli, so its half-diamond distance to identity equals its Bell loss. The informed ideal extraction is itself a global Pauli channel, and its Bell optimum is also the minimum full-CPTP half-diamond distance to identity. One nu_svc triangle debit transfers (27) even if imperfect controls destroy exact Pauli form. No untwirled dimension-free diamond conversion, key-conditioned security, or indefinite joint service follows.

## 8. The floor is real, even for arbitrary frozen full-CPTP receivers

Fix q logical qubits and q physical gauge qubits, n=2q, with exact site labels already known. Let theta satisfy tau=2 sin(theta/2)<=1/4. For an unknown sign vector s in {+1,-1}^q take the fixed unitary

    U_s=product_i[ I_(L_i) tensor |0><0|_(G_i)
                  +exp(-i s_i theta Z_(L_i)/2) tensor |1><1|_(G_i) ]. (28)

There is only the identity Pauli branch, so kappa=1 and all oracle-dominance assumptions hold. A_Z=Z is exact and ||B_X-X||op=tau for every i. During a prescribed finite calibration horizon T, the gauge preparation is |0...0>; at the specified future service time T+1 it is |1...1>. These are legal time-dependent G_I maps with no source noise or inaccessible spectral floor. The whole training channel, including all physical gauge outputs, is IDENTICAL for all 2^q sign vectors. Thus even arbitrary adaptive calibration inputs, protected calibration references, and collective calibration processing cannot reveal s on that horizon; the ordinary learner is not singled out by the obstruction.

At future service every gauge output is the same |1...1>, while the logical channel is the unknown product rotation exp(-i s_i theta Z_i/2). Any frozen receiver, allowed to act collectively on ALL physical outputs and to use its entire calibration record/randomness, is independent of s. Average s uniformly. The resulting logical channel is product Z dephasing with error probability

    p=sin^2(theta/2)=tau^2/4.

For p<=1/2, its largest Pauli probability is p_I=(1-p)^q. The full-CPTP optimal Bell fidelity of a Pauli channel is its largest Pauli probability: equivalently its orthogonal Bell-block SDP is bounded by max_alpha p_alpha, with equality by the corresponding Pauli correction. Therefore the average loss of ANY frozen receiver over s is at least

    1-(1-tau^2/4)^q.                                  (29)

For at least one source completion the same lower bound holds. A source-informed full-CPTP oracle simply undoes U_s and has ZERO loss. In the regime q tau^2<=1, (29)>=q tau^2/8, and for larger q tau^2 it is bounded below by a positive constant. This proves the unavoidable Theta(min(1,q tau^2)) order. It is a fixed finite training/future-use obstruction, not a ban on a new calibration episode after the gauge change, and not an assertion that a privately timed terminal-service theorem is impossible.

## 9. A local weak-crosstalk interface, and a bounded-drift extension

Suppose U=W U0, where U0 has exact unknown on-site generators A_(i,j), and W is generated over time [0,t] by a known-bounded physical Hamiltonian H(s)=sum_e H_e(s). For its time-ordered propagator,

    ||W A_(i,j) W^dagger-A_(i,j)||op
      =||[W,A_(i,j)]||op
      <=integral_0^t ||[H(s),A_(i,j)]||op ds
      <=2 integral_0^t sum_(e touching pi(i))||H_e(s)||op ds. (30)

For time-dependent H, the first inequality follows by differentiating W(t,s) A W(s,0), whose derivative contains the FIXED commutator [H(s),A]; it is not an invalid replacement of the evolved observable by A in its Heisenberg equation. Terms disjoint from the site commute with A and do not enter. If each site's integrated incident interaction norm is <=g, set tau_i<=2g, provided max tau_i<=1/4. Then the anisotropic bound yields O(q g^2), not a square of the extensive global Hamiltonian norm. Large bath-only Hamiltonians are not separately charged by this interface. Bounds are physical promises, not inferred coupling estimates, and do not assert efficient implementation of W^dagger.

All proofs also allow U_t to depend on time and exposed history, provided there is ONE fixed set of unknown site axes A_(i,j) such that (4) holds for every allowed call/history and future memory, with (2)--(3) at each call. The contrast cone, same-lambda localization, conditional martingale and stabilizer bound are pointwise. The comparator then is the current U_t-informed full-CPTP optimum, not one common oracle decoder across time. This is bounded drift inside a persistent on-site operator-norm tube; arbitrary post-training drift is not licensed. The statement is a corollary of the displayed inequalities, not a fit-based empirical drift certificate.

## 10. Resource ledger, comparator and evidence limits

There are exactly N0+N1 calibration BLOCK calls from (11),(15), then the specified one payload call. Each calibration block prepares q actual input qubits and measures n actual physical outputs. Coarse storage is qn two-by-two accumulators; fine storage is six rational counts per logical and its site label. Classical postprocessing is q fixed-size quaternion fits plus finite score calculations and rational norm bisections; no exponential global Choi matrix, arbitrary CPTP SDP, gauge basis or source inverse is acquired. The product receiver uses q synthesized one-qubit inverses and spectator traces. Fixed-layout routing remains separately paid, conservatively O(nq) nearest-neighbor SWAPs.

Random bits and failure caps are the exact source's fixed finite ones with B=N0+N1: qN0+2qN1 sign/input-axis bits, and at most 2nB r bits for output-axis samplers with r=ceil log2(4nB/nu_rng), nu_rng<=nu_cal. Exhaustion uses a physical fallback and its mass is already inside nu_cal. Optional service framing uses 2q more bits. No cross-copy quantum memory or long-held unknown payload is needed for calibration; ordinary service-time quantum storage/routing/control remains charged. All calculations and fallback schedules can be padded to their public worst-case caps.

The strongest equally informed conventional procedure is allowed the SAME actual ordinary product records, maximum-score localization, conditional concentration, column normalization, Wahba/quaternion fit and physical product receiver. This note does not compare against a deliberately weaker unnormalized implementation or a generic dense bandit learner. It proves a useful acquisition/composition guarantee and the correct robustness floor, not a quantum learning speedup, new attitude-estimation algorithm, practical optimum constants, external peer review or priority. In particular a crude raw-fit analysis yielding tau^2/kappa^2 does NOT prove that raw Procrustes itself intrinsically needs that floor; the normalization route shows the penalty is avoidable.

Separate source-disabled algebra/statistics checks and an independent floor/complete-reference proof accompany this candidate. They evaluate exact laws and finite matrices, not sampled acquisition outcomes or a production finite Jacobi implementation. Receiving must bind this source's final bytes separately from the exact-source receipts.
