# A native transactional continuous-noise bridge: governing synthesis V1
2026-10-30. **Whole-composition proof candidate; not yet independently accepted.** This manuscript specifies one actual revised native instance, composes the earned clean and dirty mechanisms, and states the remaining audit obligations. Individual scoped receipts are not relabeled as a whole-memory receipt.

## 0. Intended theorem and exact scope

**Time convention:** u denotes elapsed physical storage time. The symbol t=c epsilon^2 below is a FIXED proof-credit interpolation strength, never elapsed time. All proof circuits are fixed once the apparatus parameters are chosen.
Assume the reviewed bounded-degree Tanner/GPT energy, active-hub density, full-animal coverage, component-edge logical-triviality and ideal-decoder interfaces. Use the NEW finite idempotent orbit-minimizing payload compiled in `native_committed_credit_audit_20261030/NATIVE_GPT_IDEMPOTENT_PAYLOAD.md`, not the old lex-first-improving table.

The proposed native instance below has fixed local qudit dimensions, actual two-site hub/resource Hamiltonians, and actual on-site complete label-resolved resets/monitors. All rates and dimensions are constants independent of N. The claim to be audited is existence of a positive full-Hilbert observable F and constants eta0,lambda,B>0 such that on the raw component-safe basin

    (L_native^*+N_u^*)F <= -lambda T_B T_t(W_G)+B N I
                         <= -lambda F+B N I,        (0.1)

for sustained bounded-incidence local Hamiltonian/Lindblad noise of joint system/bath strength <=eta0, with a retained common bath. The allowed noise-support family is fixed before the component/animal geometry and lies in the declared bounded-degree support graph. This V1 does not incorporate a separate topology-free or time-varying-support corollary. No effective Lindblad replacement or time-growing simulation error appears. Assume the stated full joint Hamiltonian/GKLS dynamics has well-defined normal CPTP propagators on every interval, bounded normal joint local perturbation maps with the declared norm/incidence budget, and a well-defined CP trace-nonincreasing basin compression. Bath-only commutation is not an existence theorem for an arbitrary unbounded generator; finite-bath models satisfy the usual finite-dimensional regularity automatically.

For N>=N0 chosen so ell>=8s (the full declared local DATA-edge support bound) and the encoded raw vacuum lies below the killed threshold M, and with fixed bath initialization independent of arbitrary logical/reference input, the existing killed-basin interface would then give

    ||Dec_frame E_u Enc-id_L||_diamond
       <=min{2,C N^(3/2) u exp(-b ell)}.              (0.2)

For a reviewed code interface with ell proportional to N this is an exponential-in-N formal lifetime. The constants may be unusably poor. This is a framed ideal-output memory statement, not noisy preparation/extraction, thermodynamic self-correction, an experimentally validated threshold, or a practical resource advantage.

## 1. ONE unified physical apparatus
Start with the reset-first native generator and full-Hilbert forest gauge in `transactional_data_bridge_20261029`. Preserve distinct A/C/Q families, irreversible complete A_k->C0 commitment, ownership-checked computation gates, complete separately workspace-labeled terminal/abort resets, and the prohibition on cleanup in C or ANY abort phase.

Install the explicit new GPT orbit-minimizer gate list. Its finite workspace, C-chain length, failed-test leaves and actual monitor alphabet are recomputed from that list. Every physical DATA gate still couples one hub qudit to one resource qudit; there is no all-lock Hamiltonian guard.

Add the actual on-site channels

    sqrt(mu_i)|Q0,0><A_i,s|,   i>=1, every workspace label s,

with fixed mu_i>0. They are exactly DATA identity in forest coordinates because A/Q gauges are identity. They give fast abort/cleanup without waiting for another owner and do not add a hidden DATA fault.

All later acquisition/reversal amplitudes have a common fixed small scale zeta>0. Only A0<->A1 has the still smaller amplitude epsilon>0. The busy-return proof avoids later acquisition edges, but the actual local norm budgets, isolated success probability p_A and isolated normalizer constants are still recomputed for the chosen positive zeta, new payload and added A_i resets; constants from an earlier fast-rate instance are not transplanted. Computation, ordinary abort, cleanup, verification, ready, workspace-refresh and actual monitor rates remain fixed positive. zeta is chosen before epsilon; it is fast relative to epsilon but not assumed large in absolute units.

**Recompute**, rather than reuse, the local killed bad-sector R_h/S_h for this exact generator, INCLUDING the new A_i->Q0 gains/losses. Extra healing does not automatically preserve an old noncommuting Lyapunov coefficient. The structural absorption/owner-algebra proof transfers, and the new finite matrices define the coefficients used here.

Explicitly, with ALL acquisition edges omitted from the fast bad matrix, put M_h=B_h[sum_(i>=1)mu_i P_Ai tensor I_W]B_h. Each added gain has B_h J_(i,s)=0, so

    K_D,new,h^*=K_D,old,h^*-(1/2){M_h, dot},
    R_D,new,h=int_0^infinity exp(t K_D,new,h^*) I_bad dt.

The exact assembly, absorption, monitor-accounting and three-generator compatibility derivation is frozen in `weak_initiation_compiler_20261030/UNIFIED_GENERATOR_INTERFACE.md`, SHA-256 `c083a0d491e7eb44ee0e575d222ba256152c56a682cadedd08d7785c6032105f`. It is a governing dependency of this V1, not a whole-memory acceptance receipt.

Use THIS R_D,new,h to choose S_h, beta_bad and the later zeta margin. No old/new lifetime ordering is asserted. Fresh absorption follows from immediate A_i abort, actual A0/Q structural abort or refresh, forward C terminal, and R abort paths with the updated rate budget. A_heal,new=A_heal,old+M_h; payload intensity is unchanged. The uncompressed added loss is private-h; its bad compression M_h can depend on lock consistency through B_h and belongs to the same monitored OWNER algebra. That membership, not a falsely private compressed support, preserves exterior commutation.

## 2. Forest coordinates and physical history flags
The exact bounded-depth forest frame removes every payload Hamiltonian on the entire Hilbert space. Terminal/abort DATA actions remain actual bounded-support instruments, including nonmonomial partial aborts. Define the actual commuting history flags

    B_h=I-P_h^history,

where good means consistent clock/own-lock predicates and W_h=0 in the frame; abort labels are bad. These are physical observables, not virtual Poisson marks. Nominal Hamiltonians preserve all B_h; an h reset preserves every B_g, g!=h, and never creates B_h.

Attach R identical analytical token vertices to each B_h, not physical ancillas. For all connected animals define f_A=exp(a|A|)theta^{|A|-occupied(A)}, V=sum_A f_A and W=sum_A |A|f_A. The graph includes the full raw read/correction/reset/noise and analytic-credit footprints. There is no animal-size cutoff.

For a CSS implementation, take V=V_X+V_Z and W=W_X+W_Z with separate sector animal graphs and separate analytical copies of the same history flags. Apply the argument sectorwise and sum with common worst-case constants. A clean sector correction preserves the other raw syndrome. No joint-sector confinement theorem is silently inferred from two separate FGL/Tanner hypotheses. The repeated flag copies are perfectly correlated physical projectors, not independent ancillas.

The raw nonmonomial reset envelope is essential: on an entirely bad reset source, replace the affected unary DATA-energy occupancies by their lowest source/highest target envelope while removing all R tokens. Choose R using the bounded changed-energy-vertex count k and the strict q_R margin below; the full-animal completion then pays arbitrary CP DATA output. A complete terminal reset has zero good/dirty cross block because its good Stinespring image has a deterministic corrected raw syndrome. Thus raw V and W are nominally nonincreasing even for partial nonmonomial aborts.

**Tanner occupancy convention:** the complete raw linear syndrome is retained as the gauge/measurement label, while V and W count the declared UNARY LOCAL-ENERGY vertices. Accordingly, every reset-envelope k in this manuscript and its imported generic envelopes bounds the number of those energy vertices that an arbitrary local payload/abort can change. It is neither merely the number of raw syndrome bits nor the smaller 2w bound for a selected clean correction. With the canonical payload convention w=Delta^2, a safe reset bound is k<=2w|R_h|<=4w^3 since |R_h|<=2w^2; enlarge k for any larger declared support and take the maximum over both CSS sectors before choosing R,c,theta. All constants involving k, in particular q_R, are recomputed with this energy-vertex bound.

## 3. Exact dirty normalization, including actual resource monitors
Use the fast-cleanup dirty-credit construction, recomputed for section 1. Exclude only acquisition/reversal from its fast bad-sector matrix. Terminal/abort gains clear B_h and are deleted in the killed matrix; remaining gains are DATA-free. Every bad state heals by structural abort, A/Q refresh, or a finite forward C path.

Fix one non-physical BOOKKEEPING partition of the existing resource monitor: assign the free-label Hamiltonian block and the already separated M_free jump ONCE to the lowest-index incident owner. Include that term and support in its own L_h/cavity. Other owner blocks go to their named owner. These free pieces annihilate all raw/resolvent owner algebras but their activity-weighted action remains present. This fixes, rather than leaves optional, the free-monitor convention.

The actual shared resource monitor is retained in the owner-block algebra

    B(span{o_h,z_h} tensor H_monitor) direct-sum C I_other,monitor.

Its Hamiltonian splits exactly into owner blocks plus the free block; its jumps were already separately label-resolved. Including the full monitor in the finite absorption matrix is legitimate because the removed other/free pieces annihilate this algebra. This is not effective dephasing. Different owners' nontrivial resource-monitor blocks are orthogonal, so their coefficient algebras commute.

Let K_h^*R_h=-I_bad, choose S_h=s0 I_bad+beta_bad R_h with 0<S_h<I, and extend S_h=I on good. The analytic private erasure Psi_h sends the hub clock/workspace to Q0,0 while retaining DATA, locks and monitors. Its CP credit is

    T_B,h(O)=sqrt(S_h)O sqrt(S_h)
                +sqrt(I-S_h) Psi_h^*(O) sqrt(I-S_h).

The DATA surplus satisfies

    E_U^*V_0-V_0 <= q_R Delta_h,
    Delta_h=V(B_h=1)-V(B_h=0),
    q_R=2^(R+k)theta^{cR-(2-c)k}/(1-theta^R).

Choose q_R with strict margin. Small fixed zeta absorbs acquisition's controller-only error against Delta_h, independently of theta. The T_B,h commute with each other and every exterior nominal term, after exact resource-monitor accounting.

The map is locally invertible but NOT inverse-CP. Its exact inverse is

    T_B,h^{-1}(O)=S_h^{-1/2}[O-C_h Psi_h^*(O)C_h]S_h^{-1/2},
    C_h=sqrt(I-S_h).

For the actual raw own drift O=L_h^*T_B,h(V), good-Q0 target compression vanishes, so the subtraction is zero and inverse congruence is positive on this particular argument. This earns the local RAW inequality for

    Lhat=T_B^{-1}L_native^*T_B:
    Lhat(V)<=-gamma sum_h B_h Delta_h-raw good terminal loss. (3.1)

Lhat is a local HP identity-annihilating operator, not a Lindblad generator. Its buffered all-good restriction is the actual clean native generator. The assigned free-monitor terms stay in their actual own L_h and its enlarged cavity; they vanish on raw V but are not silently dropped on weighted observables.

## 4. Actual weak initiation and analytic useful credit
With neighbors ready, the isolated finite controller has I/A/C/Q families and actual monitors. Kill only useful terminal gains. The corrected `GENERAL_ISOLATED_RESOLVENT.md` proves

    R_epsilon=c0 epsilon^-2 Q_return+epsilon^-1 Y+O(1),
    Q_return|I,Q=I, Q_return|C=0, Q_return|A<=1-p_A,

where the odd Y has only I/A coherence. Exact actual target-label monitor selection gives a fixed-window success probability c epsilon^2, without shrinking measurement windows. Initially idle sources are included by an actual A0 monitor/refresh ready event. Resource monitor gains preserve, but need not annihilate, the I/A corner.

The I/A-only odd coefficient and strict A success gap imply

    ||R_epsilon||<=c0 epsilon^-2+C.

Choose beta_h=b_h epsilon^2 with fixed b_h>0, S_iso=(1-beta_h Rmax)I+beta_h R_epsilon, so I/2<=S_iso<=I. Its idle deficit is O(epsilon^2), idle/busy coherence O(epsilon), and its C block is EXACTLY s_h I+beta_h R_C with R_C bounded and independent of epsilon.

Use the analytic virtual-ready-reset CP map

    Q_h(O)=sqrt(S_iso)O sqrt(S_iso)
               +(I-S_iso) tensor Phi_h^*(E_ready O).

Its second branch is linear in I-S; no principal-square-root analyticity at a zero eigenvalue is assumed. Guard it by all physical overlap-neighbors ready AND a full local B-good buffer. Outside this guard it is identity, retaining the correct no-jump cross action. It fixes every B projection and maps raw-syndrome-diagonal observables to that algebra.

Interpolate Id+t(Q_h-Id), and compose by a fixed finite coloring to obtain unital CP T_t. For t<1/4 its local linear inverse is uniformly bounded. Exact local similarity gives

    T_t^{-1}Lhat T_t=Lhat+t sum_h[Lhat,Q_h]+R_t,
    ||R_t||_local<=C t^2.                            (4.1)

No positivity of that inverse is used.

## 5. Earned activity weights and operator-valued animal charging
Let P_h^busy be the complement of A0,W0 with no own o/z tags. At epsilon=0 fast terms do not create these projections. The added A_i abort provides a fast return path independent of contention. Actual finite monitors and the corner-relative local-polynomial method give fixed-support X_h with

    cP_h^busy<=X_h<=CP_h^busy,
    L0^*X_h<=-P_h^busy,
    [X_h,P_j^busy]=0.

Pinch in actual B masks and take normalized local DATA conditional expectation. The resulting Xbar_h is controller-only globally, retains the bounds/activity commutation and EXACT clean restriction, but makes no dirty-drift claim.

Use pair gates of fixed strength B0 and singleton gates of strength A0 epsilon^2, with A0 chosen sufficiently large. Guard their original active supports on the B-good buffers specified in `GUARDED_DIRTY_CAVITY_LEMMA.md`. For each animal select anchors by a fixed neighborhood union and use ONE global color order:

    Y_A=product exp(delta X_g^guard),
    G_A=Y_A^dagger Y_A,  V_G=sum_A f_A G_A, W_G=sum_A |A|f_A G_A.

Every gate commutes f_A and every activity/history projection; G_A>=I and G_A<=exp(Cdelta|A|)I.

If B=A union D for a bounded local move, the circuits differ in O(1) gates and

    e^{-Cdelta}G_A<=G_B<=e^{Cdelta}G_A.

For large one-component completion the exponent is Cdelta times the added size. The original strict scalar completion/entropy margin absorbs this cost. Thus deterministic DATA moves remain monotone in the operator-weighted full-animal sum, and D_h^G=(I-Phi_h^*)V_G>=0. Weighted coverage is

    W_G<=C_cov[sum_h D_h^G+sum_h B_h Delta_cav,h]+C_vac N. (5.1)

The flag part uses actual occupied token bundles; no confinement is imposed on flags. The large-component part reserves the original exponential entropy margin. These are Loewner inequalities, proved on each syndrome/flag sector with arbitrary controller-vector expectation.

## 6. Clean first-order drift: actual block arithmetic
The clean normal-form proof is `CLEAN_EFFECTIVE_NORMAL_FORM.md`. Its key own identity is not inverse positivity:

    [L_iso^*,Q_h]V
       =[sqrt(S_iso) A_T sqrt(S_iso)-s_h A_T-beta_h I]d_h
       =-beta_h d_h+beta_h E_h d_h,

where E_h has bounded norm and is supported on busy C. The scalar leading C block of S removes the apparent O(1) own-terminal error.

For each commutator, include the ACTUAL resource monitors on R_h in its isolated calculation. This is per-commutator grouping, not a double-counted decomposition of L into isolated generators. Other fast neighbors preserve the guard; terminal C->Q leaves them busy. Ready returns open an additional monotone credit. Neighboring weak initiations give the explicit controller commutator -i epsilon[H_j,B_h^guard]d_h.

With local sectors I=all-ready, U=collision-free busy and C=adjacent collision, the first-order errors are:

    U/U: O(epsilon^2); U/C: O(epsilon);
    I/C: O(epsilon^2); I/U: O(epsilon^3);
    C/C: O(1),

besides the useful -b_min epsilon^2 sum_h D_h^G. Disjoint local maps cancel exactly. Negative ready-opening terms use a cavity commuting their possibly singular positive coefficient; restoring its bounded omitted gates costs O(tdelta)W_G, not an invalid comparison through a singular matrix.

The actual scalar activity hierarchy, weighted by operator-valued completion, supplies

    -a delta A0 epsilon^2 M1-b delta B0 M2
      +C delta A0 epsilon^4 W_G,

where M1,M2 are weighted local singleton/pair masses. Young absorption of the useful cross blocks costs:

    O(t epsilon^2)M1, O(t)M2,
    O(t^2 epsilon^2/(delta B0))M1,
    O(t^2 epsilon^4/(delta min(A0,B0)))W_G.

Missing isolated guards are paid by local singleton mass. Finite-depth conjugation gives only O(tdelta+t^2)W_G generic remainders; no expansion of G_A-I and no |A|^2 bound is used. Individual local negative budgets are retained through these allocations before weighted coverage is applied.

## 7. Full buffered dirty surgery: not multiplication of a global drift
For each owner remove every activity gate whose original active support can interact with that owner, obtaining cavity Y_A^h. On B_h=1 the removed gates are exactly identity; retained gates strongly commute the actual own Kraus/credit/inverse. Define Delta_cav,h by replacing only h tokens in f_A, NOT reevaluating the weights.

Re-run the raw spectral envelopes with these cavity weights. Their bounded-extension comparison changes q_R only by exp(Cdelta). This earns globally B-block-diagonal baseline

    Lhat_h(V_cav,h)<=-gamma B_h Delta_cav,h-R_good,cav,h,
    R_good,cav,h>=0.

It is valid even with other dirty owners. It is not inferred from (3.1) by multiplying by G_A.

Write F_A-F_A,cav=Y_A^{h dagger} f_A Q_A Y_A^h, with bounded local Q_A=O(delta). Strong commutation gives EXACTLY

    Lhat_h(F_A-F_A,cav)
       =Y_A^{h dagger} Lhat_h(f_A Q_A)Y_A^h.

The bounded local HP norm and local animal ratios bound this by +/-Cdelta f_A G_A^h. This includes BOTH forward erasure activation and the nonzero-target inverse subtraction in section 3. Only the zero-target cavity baseline uses positive inverse congruence.

For each linked support X split P_X=all B in its buffer zero and Q_X=I-P_X. The WHOLE dirty block is charged using Q_X<=sum_{g in X}B_g and mixed-cavity comparison G_A^h≈G_(A union D_g)^g. Fixed buffer incidence prevents an extra |A|. The baseline has zero P_X/Q_X cross; Young gives clean leakage O(delta^2)W_G. Retain the actual clean P_X block from section 6.

**Coefficientwise localization rule.** First group every finite linked useful/activity family, INCLUDING all terms whose cancellation earns its epsilon power, and choose ONE common B-buffer for that complete family. Only then insert P_X/Q_X. For a terminal DATA completion, use the same fixed owner buffer for every increasing animal and every completed target; do not cut a previously summed inequality by animal-dependent masks. Keep the resulting local negative budgets until all dirty/busy errors have been allocated. Restoring useful or activity negative charges from P_X to full support costs only their small coefficients O(t epsilon^2) or O(delta), and bounded-neighborhood token completion pays those costs. The order-one raw good-terminal negative family is NEVER restored this way: retain or discard it by its global sign. This rule prevents an unpriced O(1) dirty cost and avoids mismatched buffers on terms that cancel.

Free-resource monitors use the canonical assign-once convention of section 3. Their support is included in that owner's cavity. They therefore enter the same exact baseline/activation decomposition and whole buffered Q_X estimate, including cases where that assigned owner is good but a different buffered owner is dirty. Their clean action remains in the actual activity generator. No arbitrary-buffer zero-dirty assertion is used.

For the CONCRETE history-guarded useful primitives of section 4, local t[Lhat,Q_h] has uniform relative norm O(t). On Q_X this is a local bad-token charge; P_X/Q_X Young costs O(t^2)W_G. Its P_X block is exactly section 6. Thus total dirty diagonal errors O(t+delta) are absorbed in gamma, and clean leakage is O((t+delta)^2)W_G. This is not a claim about arbitrary near-identity CP maps.

## 8. Compatible noncircular parameters
Choose in this order:
1. Physical payload/gate list, fast nonacquisition rates, actual monitors and added A_i aborts.
2. Recomputed finite bad resolvents, beta_bad and their fixed positive margin.
3. Later acquisition zeta below the raw dirty margin; this controller norm bound factors Delta_h and does not depend on theta. Keep zeta fixed thereafter.
4. Actual zero-first-drive activity witnesses, controller-only extensions, all active/guard/cone supports and pair graphs.
5. Enlarged component/animal geometry, token multiplicity R, nearby exponent choices and sufficiently small theta. Reserve margins for q_R, full-animal charging, component entropy, bad-credit no-jump comparison and the eventual activity upper bound.
6. General isolated normalizer and fixed useful b_h; activity B0, then A0 and all weighted local constants.
7. Set t=c epsilon^2 and delta=d epsilon^2. Choose fixed ratio r=d/c large enough that dA0,dB0 dominate every c-scaled singleton/pair error. Then choose c>0 sufficiently small that

       C(c+d)^2 << c b_min / C_cov.

   This is possible with d=rc by taking c<<b_min/[C(1+r)^2]. Finally choose epsilon>0 sufficiently small for all analytic bounds, t,delta smallness, q_R margin, activity expansion, epsilon<zeta, and the remaining epsilon^6 terms.
8. Choose the sustained noise budget below the positive final margin.

Useful coercive service is c b_min epsilon^4. The t^2, tdelta and dirty-cross terms have epsilon^4 coefficients controlled by step 7. Activity idle and Young idle sources are O(epsilon^6). Lost dirty or busy service is charged BEFORE coverage. Applying (5.1) yields, with positive fixed lambda0,

    (T_t^{-1}Lhat T_t)V_G<=-lambda0 W_G+B0' N.        (8.1)

All constants are independent of N and storage time. This is an exact generator inequality with bounded local remainders absorbed at fixed parameters.

## 9. Positive pullback, arbitrary local common-bath noise and initialization
Define

    F=T_B T_t(V_G).

Both outer maps are actual mathematical unital CP circuits; positivity, not inverse positivity, transfers (8.1) to the nominal physical drift. A local Stinespring dilation of T_B T_t transfers any local joint system/bath perturbation to a bounded enlarged support with the same joint cb budget. The direct nonunital relative-norm estimate for each f_A G_A then gives

    N_u^*F<=eta C_noise T_B T_t(W_G).

Bath-only terms commute F; the bath is not reset, twirled or reconstructed. Choose eta C_noise<lambda0/2. Since W_G>=V_G, this gives (0.1).

Initialize Enc(rho_LR) tensor |all clocks/workspaces/locks ready><ready| tensor sigma_(monitors,bath), with ONE fixed monitor/bath state independent of the arbitrary logical/reference input. Monitor/bath correlations in that fixed state are allowed.

For initialization, G_A>=I but is not generally bounded by I. Use

    V_G<=V_(a+Cdelta).

Both CP credits are monotone on that slightly larger tuned RAW potential: dirty credit removes flags, and useful branches apply accepted DATA corrections while resetting only good controller sectors. Thus F<=V_(a+Cdelta) and the encoded/all-ready expectation is O(N), independent of arbitrary fixed monitor/bath state.

For a lower barrier, V_G>=V_a. Retain the interpolation-Id branches of T_t in each finite animal causal cone, and the no-jump branches of T_B, whose coefficients commute raw animals and have fixed minimum singular value. Reserve two exponent margins to obtain F>=V_a0. The fixed beta_bad loss is covered by theta/exponent selection after geometry, not by changing zeta retroactively.

## 10. Raw basin, block commutation and logical channel
Use the existing raw component-safe low-potential basin defined by V_a0<M. Activity factors are controller-only and commute every B and DATA syndrome, so they commute its projector. Dirty CP Kraus either preserve raw syndrome/flags or clear one flag. Useful CP branches preserve all history flags and perform an accepted syndrome move, or act controller-only within a good flag sector. Their bounded local DATA supports are included in the component-edge graph. Hence both CP circuits preserve this raw basin.

Separately, every map used here preserves the DATA raw-syndrome-diagonal and actual B-block-diagonal algebra on the observables in question. The payload adjoint maps raw-syndrome-diagonal functions to such functions; all other coefficients are controller-only and B-preserving, with dirty erasure producing source-B-diagonal effects. Therefore [F,P_basin]=0; this is not inferred from basin preservation alone.

These facts let the positive pullback of the basin-local inequality remain valid after analytic killing. Outgoing killed gains subtract positive F. The resulting boundary estimate is O(N/M). Every actual bounded local Hamiltonian, jump and loss Pauli edge in the killed basin has identity canonical logical action under the assumed Tanner interface, with arbitrary retained controller/bath factors. The killed decoded map is a_u id_L for the fixed initial bath state. Variation of constants and cross-block Cauchy-Schwarz then give (0.2), exactly as in the reviewed ideal killed-basin interface.

The displayed decoded bound is asserted only for the stated N>=N0 initialization range. No unproved small-size extension is used; one could separately import an independently reviewed finite-size argument with an enlarged prefactor.

Readout applies the bounded-depth forest inverse and the fixed ideal mathematical decoder. None of the CP proof credits is physically applied. No noisy preparation/retrieval guarantee has been inserted.

## 11. Review gate and exact dependencies
Scoped committed, dirty-history, fast-cleanup and clean normal-form receipts exist in their separate audit folders. The repaired activity-only buffered cavity, complete inverse correction and mixed-cavity charge have a scoped receipt at `native_dirty_cavity_audit_20261030/INDEPENDENT_REVIEW.md`; its concrete useful-credit interface remains conditional on the separate clean review. The full composition and unified-resolvent substitution require their own exact-source review. This V1 is NOT to be labeled a native theorem merely because those component receipts exist.

Primary scoped receipts and exact-source dependencies:
- `native_committed_credit_audit_20261030/INDEPENDENT_REVIEW.md` plus its frozen new GPT payload addendum;
- `native_bad_credit_root_audit_20261030/REVIEW.md` and `native_fast_cleanup_credit_audit_20261030/INDEPENDENT_REVIEW.md`, transferred only by the fresh unified-generator derivation above;
- `weak_activity_independent_audit_20261030` and `weak_useful_credit_independent_audit_20261030` for actual fast BUSY and isolated useful interfaces;
- `clean_normal_form_independent_audit_20261030/INDEPENDENT_REVIEW.md` for the clean first-order weighted synthesis;
- `native_dirty_cavity_audit_20261030/INDEPENDENT_REVIEW.md` for repaired activity-only buffered dirty surgery, full inverse and controller extension;
- `weak_initiation_compiler_20261030/UNIFIED_GENERATOR_INTERFACE.md` at the exact hash in section 1.

Load-bearing whole-review checks:
- actual unified rate/gate instance and recomputed bad matrices with A_i aborts;
- activity/usable supports fixed before animal constants, including free-monitor accounting;
- clean first-order coefficientwise budgets retained through buffered dirty localization;
- mixed-cavity completion and both erasure activation terms;
- positive final pullback, noise dilation, upper/lower exponent margins, raw basin preservation AND block commutation;
- fixed-bath decoded-channel quantifiers and correct code-family interface.

Until that review passes, generic native coherent/common-bath memory robustness remains **OPEN at whole composition** despite the substantive local construction in this manuscript.
