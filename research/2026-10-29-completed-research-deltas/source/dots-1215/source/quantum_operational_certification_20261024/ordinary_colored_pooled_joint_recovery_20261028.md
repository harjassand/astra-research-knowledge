# Colored causal composition and pooled ordinary acquisition for many local logical qubits

28 October 2026. **New constructive proof candidate; independent review in progress.** Earlier received manuscripts remain immutable. This changes the learned receiver's block order and its acquisition schedule; it is not an equivalent compiler of the old learned channel, and no previous holdout or encoder choice is reused. No source samples have been generated for this construction.

## 1. Contract retained, question sharpened

Import the exact source, control and comparison contract from `ordinary_joint_local_logical_swap_recovery_20261028.md`, received SHA `f22c549bcb545387b4761ff31ec90886ff7b677c1d1f32a411b05e65024f89c0`. There are q logical input qubits and n>=q known physical output qubits, exact mutually compatible hidden logical generators, and one unknown width-w interval per logical pair. Gauge states can be noncommuting, globally correlated, rank deficient and arbitrarily ill-conditioned. Ordinary calls independently reset. Aggregate local X/Z operator margins are at least kappa. The unrestricted joint-decoder comparison separately assumes G_I(x)>=G_alpha(x) for every global Pauli alpha and encoder x; local margins do NOT imply it. The four-real-coordinate encoder and paid global Clifford input/readout capabilities are unchanged.

The old proof gave joint virtual Bell loss

    ell0<=3q sum_i e_i,  e_i=delta_Zi+delta_Xi/2.            (1)

With a uniform local error target, this caused quadratic-q loss accumulation and cubic-q separate acquisition. We show this is NOT unavoidable for the stated bounded-width architecture. First, a different color-ordered receiver admits a causal-cone/Bell-projector bound with a q-independent coefficient at fixed w. Second, actual source outputs can be pooled across disjoint known envelopes without cloning or independent-bank assumptions.

## 2. Known envelopes and an operationally checked schedule

First perform ALL q coarse localizations from the received construction, before any fine acquisition. Let J_i be the selected coarse width-w interval and let W_i be J_i expanded by w−1 sites on each side, clipped at physical boundaries. Every W_i is known. On the simultaneous coarse good event, W_i contains the true support pair I_i and every fine candidate patch for i. Let

    W=min(n,3w−2),  C_max=min(q,2W−1).

Use a left-endpoint sweep/optimal interval coloring of the known W_i. This is not an arbitrary-order greedy coloring. If the observed number of colors exceeds C_max, return a prescribed physical q-qubit replacement receiver and a predetermined encoder; the exceptional history is charged, not postselected away. All coarse calls still count.

### Why the promised good history has few colors

If s independent commuting logical qubit matrix algebras are supported inside L physical qubits, then s<=L: their joint faithful representation contains M_(2^s), whose irreducible representation dimension2^s cannot fit in dimension2^L. This is an exact operator-algebra dimension statement, independent of the rank or correlations of the occupied gauge state.

All width-at-most-W envelopes covering a given site lie in an interval of at most2W−1 sites. On the coarse good event, their corresponding TRUE independent logical algebras are supported there. Thus their number is at most2W−1. The interval graph's maximum overlap, hence its optimal coloring, is at most C_max. The testable coloring cap is a safe algorithmic guard; passing it does not infer source-family membership or certify successful localization.

The NEW joint receiver executes complete three-controlled-reflection SWAP blocks in color order. Within one color, envelopes and labeled ancillas are disjoint, so these blocks commute even when the learned reflections are otherwise incompatible. One may serialize their physical implementation. Routing is reversed/tracked around each block, so its exact-reference NET support is W_i plus its own distinct ancilla A_i. Each ancilla is a private leaf touched only by its own net block. Actual routing faults are charged in the whole-process operational discrepancy; color count is NOT a claim about physical routing depth.

## 3. Causal cones, retaining the entire Bell reference

Define a directed graph with j→k when color(j)<color(k) and W_j intersects W_k. For output i let Anc(i) include i and its graph ancestors. These are the common envelope cones of both the actual and ideal circuits, not cones inferred from accidental commutations of a fitted matrix.

Each backward color step expands a cone's physical span by at most W−1 sites on either side. Disjoint same-color envelopes cannot create a within-layer propagation chain. With

    K=min(q, W+2(C_max−1)(W−1)),                           (2)

every cone contains at most K block indices. Indeed all its envelopes lie in its final physical span, and the exact logical-factor packing bound applies there. The identical forward-span argument proves that a given block belongs to at most K output cones. This is a property of graph ancestors/descendants, not of a gap-filled interval algorithm that could introduce artificial cone members.

For the global Bell calculation keep the whole reference R, the gauge purifier E and receiver-ancilla purifiers S. The ideal reduced state on physical register P and all initially maximally mixed ancillas is rho_PA=rho tensor I_A/2^q. Every individual ideal controlled gate preserves it; therefore every SUBSET of ideal blocks and every ideal elementary prefix also preserves it.

For output i, peel outside-cone blocks away in the Heisenberg evolution of its Bell projector Phi_(R_i,A_i). They commute out exactly for ANY input state, even with arbitrarily correlated gauges. Do this separately for both actual and ideal circuits, then compare the TWO RESTRICTED circuits from the SAME initial purified state. One may not merely omit terms from the old full-state hybrid, where outside-cone actual gates could spoil the desired prefix state.

The restricted ideal circuit still has Bell success one for output i, by the same Heisenberg deletion from the fully ideal receiver. Its elementary gate errors are delta_Zj/2, delta_Xj/2, delta_Zj/2, as in the received proof. Unitary learned suffixes and Cauchy–Schwarz give the ACTUAL final marginal failure

    p_i<=3|Anc(i)| sum_(j in Anc(i)) e_j.                  (3)

These are marginals of one real joint receiver, not fidelities of separately deployed fitted channels. The Bell projectors on distinct R_i,A_i commute, and

    I−product_i Phi_(R_i,A_i)<=sum_i(I−Phi_(R_i,A_i)).      (4)

Hence, with no independence assumption,

    ell0_joint<=3K^2 sum_j e_j.                           (5)

The old global hybrid remains valid for this same color order. Set

    A=min(q,K^2),
    eta=epsilon/(16384 q A).                              (6)

Then ell0_joint<=3A sum_j e_j. The received local CPTP acquisition, finite sign-rounding and backward-error budget give delta_Xj,delta_Zj<=25eta, so

    ell0_joint<=(225/2)q A eta,
    sup_x[ell(D E_x)−ell_star(x)]<=450q A eta<epsilon/20.  (7)

At fixed w, A is bounded independently of q. This proves linear-q accumulation of uniform local generator errors under arbitrary correlated gauges. The construction does not claim (5) for the previous arbitrary index order: reordering incompatible learned blocks changes the channel and requires fresh global encoder learning/qualification.

## 4. Exact-fill pooled Bures banks from actual paired calls

The remaining q separate fine banks are also unnecessary after the known envelopes are colored. Within each envelope, its at-most R_max=min(n−w+1,2w−1) candidate intervals can be partitioned into c1=min(w,R_max) local colors with disjoint candidate intervals. Use local color indices per envelope; different envelopes need not share physical start residues.

Fix one envelope color, one local candidate-interval color, and one input axis j=X or Z. All simultaneously processed physical patch registers are disjoint. Acquire N_B independent PAIRS of reset source calls. In each pair:

1. Draw a fresh uniform q-bit sign vector s.
2. Prepare every logical input in P_(j,s_i) and use a fresh uniform encoder anchor for the first call.
3. Prepare every logical input in P_(j,−s_i) and use an independently uniform anchor for the second call.
4. Learner i receives only its OWN sign and routes exactly one physical patch register from the pair to its plus bank and the other to its minus bank.

Thus each logical/patch learner receives exactly N_B actual plus copies and N_B actual minus copies from2N_B RAW calls. Both calls are real; there is no cloned output, counterfactual query, rejection, fill oracle or optional stopping. One output's subregisters may serve different learners only when the selected physical patches are disjoint.

### The precise marginal law and retained-information firewall

Condition on the common PRE-pool coarse history and one learner's own sign sequence. For either ONE chosen sign bank separately, its selected other-logical sign vector is uniform in every pair: flipping a uniform independent vector does not change its law. The selected anchor remains uniform. Averaging all other sign/anchor labels therefore gives exactly its desired ordinary marginal r_(i,j,+) or r_(i,j,−). Different pairs are independent, so EACH individual sign bank marginal is exactly r_(i,j,s)^tensor N_B.

The JOINT plus/minus bank state is generally correlated. Different logical learners' banks are also correlated. Do NOT claim they are independent or jointly tensor-product. Each individual STATE estimator has a fixed local control policy using only its own selected register bank, its own routing labels and its own internal measurement records. It does not adapt to another sign bank, another learner's current labels/outcomes, or the shared anchor labels. Other bank instruments are trace preserving on disjoint registers when their records are not conditioned upon, so they preserve this individual iid marginal even with correlated quantum gauges.

The firewall is a specified measurement/dataflow policy, not cryptographic blindness: the input controller generates the full sign vector, but the individual estimator does not use excluded current records. The resulting guarantee is a joint bad-event probability, not a posterior assertion conditional on every eventual retained transcript. A concrete warning is a two-logical identity source with learner1's patch containing both inputs: its plus-bank spectator X sign and minus-bank spectator X sign are perfectly anticorrelated. Each bank separately has maximally mixed spectator, but the joint spectator X correlation is−1 rather than the0 of product marginals. Measuring the opposite bank can reveal that spectator state; no conditional iid claim after such a measurement is licensed.

Only after ALL state estimates in these pools are frozen may their results be combined into the local CPTP-ERM candidate fits. Simultaneous fidelity confidence follows by a union bound over the individual state-estimator bad events, never by conditioning their iid proof on the eventual global success record. This exact-pair design supersedes the valid but less economical oversized-pool/fill-failure design; it has deterministic fill and no additional fill-probability allowance.

Allocate beta_F to all fine density estimates, at most4qR_max. Set

    m=kappa^2 eta/256,  zeta_ERM<=m,
    N_B=ceil[(80*4^w/m)log(48*4^w*q*R_max/beta_F)].       (8)

The known finite Bures instruments and exactly feasible local ERM are unchanged. There are two axes, at most C_max envelope colors, and c1 local patch colors; the fine source cap is

    N_fine<=4 C_max c1 N_B.                              (9)

The q factor has moved into the accuracy target eta and the confidence logarithm, not a fictitious reuse of one physical register by incompatible measurements. The number of local state-estimator circuits remains at most4qR_max, each with N_B copies and its full collective workspace. Storage can be one2N_B*n-qubit pool at a time plus the paid local estimator workspaces. All q-input preparation traffic, private sign bits, source anchors, physical output qubits and cross-copy memory routing count.

## 5. Pooled real spectrum-valued comparison tournaments

Freeze every fine candidate channel after the pool stage. Within one disjoint-envelope color, run one current comparison per active logical i on the SAME source call. Each call independently chooses an axis j_i in {X,Z} and sign s_i for EVERY logical input, including inactive ones. The active receiver i measures its actual known backward-diagonalized spectrum-difference observable on its own envelope, returning s_i times the known rational eigenvalue. The source anchor is uniformly random and ignored in each current marginal calculation.

Conditional on the entire PAST batch history, each candidate pair is fixed. Averaging all OTHER current logical input labels makes those inputs maximally mixed, so each active comparison has exactly the received marginal mean r_a−r_b and second moment<=4(r_a+r_b)/kappa, plus its paid backward-observable residual. Other disjoint physical measurements preserve that marginal. The outcomes across learners may be correlated; no independence is used. Within a batch, pairs and controls may not adapt to other learners' CURRENT outcomes. At the batch boundary each learner advances its fixed balanced bracket from its own comparison records.

Use fixed synchronized postorder comparison slots, at most R_max−1 per logical index; empty/byes slots simply trace the unused registers. For R_max>=2 put

    h=ceil(log2 R_max),
    L=log[2q(R_max−1)/beta_T],
    t=kappa eta/(4h^2),
    N_pair=ceil[2048h^2 L/(kappa^2 eta)],
    xi<=kappa*t/4096.                                    (10)

Fresh source calls in each batch give the same conditional Bernstein event for each comparison. Union over at most q(R_max−1) comparisons costs beta_T, irrespective of cross-learner correlation. The local ERM bound r_min<=22kappa eta/256 and the tournament then give r_selected<=27kappa eta/64<kappa eta/2, hence ell0_i<=eta. For R_max=1 skip all comparison formulas and calls.

The actual comparison-source cap is now

    N_tournament<=C_max(R_max−1)N_pair,                   (11)

not q(R_max−1)N_pair. Every measured observable acts within its actual known envelope. Same-output covariance is retained; neither independent decoder-error counts nor independently resampled marginal data would implement this experiment.

## 6. Complete finite cap and the linear block-call rate

Let beta_L cover all coarse localizations. With M=n−w+1, c=min(w,M), m0=kappa^2/512, use

    N0=ceil[(80*4^w/m0)log(24*4^w*q*M/beta_L)].           (12)

Coarse source cost is2q c N0. It is still logical-label-specific because the physical supports are not yet known; the new pooling construction does not pretend to reuse one coarse quantum patch for all q conditional tomography tasks. Choose positive beta_L,beta_F,beta_T,beta_C with sum<=epsilon/8. Keep one whole-process complete operational discrepancy nu<=epsilon/8, including input/receiver gate compilation, private randomness, memory routing and all payload controls.

After the new color-ordered joint decoder is fully frozen, run the received GLOBAL stabilizer/Clifford ordinary-input encoder test and active ten-feature design. Its mean is[2^q/(2^q+1)] times the actual GLOBAL Bell loss. Known within-input entanglement, joint inverse-Clifford readout, finite Clifford sampling and their routing remain explicitly paid. Use the received epsilon/8 scalar tolerance and N_count cap; it is not a product of marginal tests.

A deterministic complete raw source cap is

    N_total<=2q c N0+4 C_max c1 N_B
                +C_max(R_max−1)N_pair+N_count+1,          (13)

with zero comparison term for R_max=1. The +1 is a final q-logical payload. Safe coloring/estimation failure histories remain physical and are covered by the fixed cap. Every executed call on a failed history is charged; safe early termination may use fewer calls than the stated upper cap, but no executed call is refunded, hidden, or reclassified as a successful observation. The received global comparator transfer and bounded loss on exceptional histories give averaged loss<=(1+gamma)ell_star+epsilon.

Keeping the width dependence visible, the separated source scales are

    coarse: O_tilde(q c 4^w/kappa^2),
    fine: O_tilde(C_max c1 q A 4^w/(kappa^2 epsilon)),
    comparisons: O_tilde(C_max R_max q A/(kappa^2 epsilon)),
    encoder: O_tilde(1/(gamma epsilon)).                  (14)

For FIXED w, C_max,c1,R_max,A are bounded constants independent of q. Thus the fine source block-call scaling is LINEAR in q, rather than cubic, with logarithmic n and q confidence overhead. A is at most O(w^4), so the extra width factors remain explicit polynomials multiplying the local4^w dependence. This is not a claim of linear total qubit traffic: every call prepares q logical input qubits and emits n physical qubits, giving qN_total input-qubit uses and nN_total output exposures. Classical local estimator processing, per-bank quantum storage and physical control work are likewise extensive.

The payload receiver still uses3q local controlled reflections,4q Hadamards, q distinct fresh maximally mixed ancillas and the paid restored routing. It has C_max abstract block layers, not C_max physical hardware depth. Only N_count+1 invocations of this joint payload decoder occur in the schedule; acquisition and tournament controls have their separate ledgers. The optional internal whole-logical Pauli twirl and the untwirled dimension-dependent diamond boundary remain exactly as in the received joint theorem.

The strongest equally informed conventional learner can use this same colored, pooled construction. No advantage or historical priority is asserted. Structural assumptions, reset source, physical output coordinates, global identity dominance for oracle comparison, and global known-Clifford input control remain indispensable.

## 7. What is and is not established

The old q^2 coherent-hybrid amplification is not unavoidable for this bounded-width architecture: a newly color-ordered receiver has a rigorous linear-in-number-of-local-errors bound, even with correlated quantum gauges. Independent marginal decoder fidelities have NOT been substituted for the real joint-channel proof. Physical parallel banking then removes the separate-q training multiplier while retaining exact per-bank marginal laws and all controls.

The sum over logical errors in (5) cannot generally be replaced by max_i(delta_Xi+delta_Zi) with a coefficient independent of q. This is a boundary on the number of accumulated local errors, not a denial of the q-independent coefficient multiplying their SUM that (5) establishes. For example, take q independent logical/gauge pairs, true X_i,Z_i on the logical site, gauge state diag(1−p,p), and learned X'_i=X_i tensor Z_gi, Z'_i=Z_i. The actual mixed-ancilla SWAP produces a Z error on logical i exactly when its gauge bit is1. Its joint loss is1−(1−p)^q while delta_Xi=4p and delta_Zi=0. These are legitimate local controlled reflections; the example is a zero-source exact family, not acquisition evidence. It shows the natural small-error linear-q scale without imposing any lower bound on gauge weights.

No new count-acquired experiment or hardware run is claimed. A source-disabled prescribed-matrix/counting check and independent reviews will be bound separately. The earlier arbitrary-order result, its receipts, and both completed pilots are unchanged. Product-only global validation, approximate locality, unknown model violations and drift/no-reset access remain outside the received input contracts.
