# Deterministic asynchronous contraction and backward DATA witnesses
Continuation, 2026-10-29 21:51 UTC. This advances the mathematical bridge; it does not certify the physical compiler's stochastic interface.

## 1. Serial-history model and constants
One CSS sector. Correct completed transactions are actual current-syndrome SSF moves, accepted only if d(F)=|σ|−|σ⊕σ(F)|≥β|σ(F)|>0. All consulted data are reserved until completion. Each hub either chooses some accepted candidate when evaluated, or does nothing only if none is accepted. Fresh bad events are support-bounded Pauli flips; a non-SSF correction is also a bad event. Let w bound correction support, Δ bound data-check degree, and B bound |σ(F)|. All are constants.

Use a FIXED graph G_R on data sites: make each full hub read footprint a clique, include each check support as a clique, and include each allowed elementary fault support as a clique. This graph has bounded degree. Do not put all read sites of idle transactions into execution support: that would artificially merge clean regions.

FGL Proposition 14 (https://arxiv.org/html/1808.03821, §3.3) says that below its small-error cutoff, total syndrome mass of good candidate moves is at least c1|σ|. A bounded-degree conflict graph on candidate identities joins candidates if their syndrome supports intersect or they belong to the same hub. Let its degree bound be D_c. A color-class pigeonhole argument gives a family G of initial good candidates with disjoint syndrome supports, at most one per hub, and

 |G| ≥ κ|σ|,   κ=c1/[B(D_c+1)].                         (1)

This slightly wasteful packing avoids relying on ambiguous multiplicities in a same-generator candidate family.

## 2. Window contraction without complete color sweeps
Fix ANY finite serial time window, choose G at its start. Follow each candidate until its first resolution:
(a) a correct correction changes one of its syndrome bits;
(b) its own hub is correctly evaluated and executes some accepted correction;
(c) a bad event changes one of its syndrome bits;
(d) none of these happens by the end: count one missed opportunity.

While unresolved, its original syndrome bits are unchanged, so it remains good. Thus a correct evaluation at its hub cannot legitimately do nothing. A correction H can resolve at most |σ(H)| candidates through (a), and at most one additional through (b). Since |σ(H)|≥1, this is at most 2|σ(H)|≤2d(H)/β. A bad event Q resolves at most |σ(Q)| candidates. Count D=sum d(H), J=sum_bad |σ(Q)|, and M the number in (d). Then pathwise

 |G| ≤ 2D/β + J + M.

Meanwhile S_end ≤ S_start−D+J. Consequently

 S_end ≤ (1−a)S_start + A J + B_m M,                    (2)
 a=βκ/2, A=1+β/2, B_m=β/2.

No stochastic assumption or complete sweep appears. A correction's resolution of its own packed candidate is counted even if it chooses a different accepted subset. If the implementation instead has candidate-specific channels, the bookkeeping simplifies further.

A bad event which changes only control/availability but no syndrome must be classified through the missed-opportunity term; it is NOT silently covered by J. This distinction is central for the autonomous compiler.

## 3. Exact localization using future support (arriving noise included)
For a serial event list ending at L define

 U_i = E_i ∪ ⋃_{events k≥i} supp(event_k)
     = E_L ∪ ⋃_{events k≥i} supp(event_k).

The equality follows directly from XOR cancellation. Therefore U_{i+1}⊆U_i, even though physical faults arrive during the interval. For a final target S⊆E_L, let W_i be the union of G_R-components of U_i meeting S. Then W_{i+1}⊆W_i. Every actual correction/fault wholly belongs to one component, since its support is a clique in G_R.

For a fixed W_i, replay the suffix restricted to it. A correction executed inside W_i has all currently erroneous sites in its read footprint inside W_i; otherwise an outside U_i site would share that footprint and be adjacent. Thus its syndrome decision and decrease agree with the restricted history. A locally beneficial candidate's hub has a read footprint intersecting a current erroneous site in W_i. Any actual correction chosen at that hub is then inside W_i (its support is in U_i and in the same footprint). The candidate either receives a real correct evaluation, is spoiled by a restricted event, or is genuinely missed. This supplies the local version of (2), not merely a global expectation.

Initial candidates may contain sites not yet in U_i; if they actually execute those sites are, by definition, in U_i. No counterfactual execution is inserted into U_i. Read-footprint adjacency is what prevents a different correction at the same hub from being charged invisibly outside W_i.

## 4. Suffix footprint bound when the final error is reduced
Assume for now E_L is stabilizer-reduced and each relevant component remains below the FGL cutoff. Any subset of a reduced error is reduced (FGL Lemma 17), and confinement gives |E_L∩W_i|≤S_L(W_i)/h with h=β0 d_A/2.

Let Q_i(W_i) be the SUM of support sizes of bad events in the suffix within W_i; multiplicities are counted. Let D_i be total correct syndrome decrease in this restricted suffix, x_i=|σ(E_i∩W_i)|, and y_i=|σ(E_L∩W_i)|. Then

 D_i ≤ x_i−y_i+Δ Q_i,
 |W_i| ≤ |E_L∩W_i| + w D_i + Q_i.

Writing C0=max(w,1/h), these imply

 |W_i| ≤ C0 x_i + (C0 Δ+1)Q_i.                         (3)

For clarity: use wD_i≤C0D_i and |E_L∩W_i|≤C0y_i, which cancels y_i. This controls future footprint, not accumulated history extending to the infinite past.

## 5. R-window backward witness dichotomy
Partition a FIXED finite block into R windows. At boundary j define W_j as above and x_j its local syndrome. Local (2), nested W_j and J_j≤ΔQ_j imply

 x_{j+1} ≤ (1−a)x_j + AΔ Q_j(W_j)+B_m M_j(W_j).        (4)

Here M_j is the packed locally good candidates that remain genuinely unevaluated/unspoiled during window j. Set L0=max(AΔ,B_m), θ=1−a/2, and K0=2L0/a. Let Z_j=Q_suffix(W_j)+M_j(W_j).

For every nonempty target S⊆E_L, one of two cases holds:

**Fresh-obstruction witness.** Some j<R satisfies x_j≤K0 Z_j. Equation (3) then gives

 S⊆W_j, each W_j-component meets S,
 |W_j| ≤ C_bad [Q_suffix(W_j)+M_j(W_j)],                (5)
 C_bad=C0K0+C0Δ+1.

Thus a surviving target has a geometrically countable witness dense in fresh physical-fault mass or missed-opportunity cells, not just a large syndrome expectation.

**Large ancestral witness.** No such j exists. Equation (4) contracts by θ in every window. At the end, x_R≥h|S|, while x_0≤Δ|W_0|. Therefore

 |W_0| ≥ (h/Δ) θ^(−R)|S|.                              (6)

For constant but sufficiently large R, surviving targets require increasingly large ancestral supports. This is the partial-decoding analogue of the FGL backward proof. Unlike its logarithmic-completion version, this dichotomy can be used at fixed physical block time.

## 6. Reduced representatives and mergers: how to handle them
For the original history let U be its whole execution support. Choose R_min of minimum weight among ALL errors having the final syndrome. For each component K of U∪R_min in G_R, the same-syndrome property is componentwise, and minimality implies

 |R_min∩K| ≤ |E_L∩K| ≤ |U∩K|.

The original history restricted to K obeys the finite-work estimate, so with C_work=1+wΔ,

 |K| ≤ 2C_work [|E_0∩K|+Q_block(K)].                   (7)

If all such components lie below both the FGL cutoff and distance, R_min∩K differs from E_L∩K by a stabilizer. Thus R_min is a legitimate reduced residual, not a logical replacement. The virtual history starting from E'_0=R_min XOR all event masks has exactly the same syndrome sequence and accepted corrections, and ends at R_min. Its support is contained in U∪R_min. Apply §§3–5 to that virtual history.

For the large-ancestral case, W_0 itself need NOT satisfy (7): reduction may delete original-error sites that connected it to its seeds. Enlarge W_0 to the components K of U∪R_min meeting S. This enlargement still has each component meeting S, is at least as large as W_0, and satisfies (7). It is therefore a valid countable seed-dense witness.

Component mergers are incorporated in U and this component enlargement; no independence of moving components is asserted. The stopping/bad-cluster event is that one of the enlarged components reaches the cutoff.

## 7. What probabilistic interface would close the Pauli-model theorem
For each fixed W and specified outside events, one needs joint exponential tails for:
- |E_0∩W|+Q_block(W), to bound seed-dense witnesses in (7);
- Q_suffix(W)+M_j(W), to bound fresh-obstruction witnesses (5).

An exponential count-moment formulation is safer than silently converting Q to a binary fault set: repeated Poisson faults at one site must be counted. Under an independent dominating local Poisson process, bounded support/degree gives such count tails. Under a general local stochastic model they must be supplied jointly, not just as individual marginals.

Suppose schematically these tails yield for witness size m probabilities ≤A_seed^m p_seed^(αm) in the ancestral case and ≤A_bad^m p_bad^(m/C_bad) in the obstruction case. Bounded-degree connected-animal counting supplies only another constant to the mth power. Equations (5)–(7) then give output support tails with a term whose input exponent grows like θ^(−R), plus a floor from fresh faults and misses. The same seed counting bounds cutoff failure by N exp(−c√N). A correctly joint version allows iteration; a marginal success-conditioned theorem alone does not.

R and the per-window duration can be chosen constants; then physical noise accumulated over the block is O(ε R T), and both ε and the scheduler missed-event parameter must be below fixed constants. This is the mechanism for a possible autonomous high-rate memory, not a proof that the current compiler meets the interface.

## 8. Remaining physical gap and rejected branching shortcut
A uniform probability of a favorable CLOCK record does not establish that the corresponding conditioned DATA instrument is exactly a fresh SSF evaluation. That must be shown with workspace initialization, actual read locks, abort/repair histories, and both CSS sectors included. One also needs joint missed-event tails for separated hubs, uniformly under their possibly entangled data/controller state. Owner-history no-creation and repair contraction do not on their own supply either claim.

The simple birth–death comparison based on ε times syndrome size is invalid as stated: confinement bounds a reduced instantaneous representative, not ever-touched historical support. Retired correction scars and stabilizer ghosts can make historical volume arbitrarily larger than current syndrome. The finite-window future-support method above avoids charging new noise to infinite historical volume.

General coherent nonthermal perturbations still require a norm/amplitude version of this argument or an explicit Pauli reduction. These combinatorial proofs are for serial Pauli histories. Fixed-dimensional geometric routing and wall-clock readout remain separately charged resources.

## 9. Closing the IDEAL atomic Poisson/Pauli comparator (derivation for audit)
This section does not replace the physical compiler by a Poisson semigroup. It shows that the probabilistic witness interface is non-vacuous for a stronger idealized ordinary asynchronous SSF baseline.

Assume each hub has an independent rate-λ Poisson evaluation clock and correct instantaneous current-syndrome evaluation at each ring. Physical Pauli faults are dominated by independent local Poisson processes, independent of initial data; each support has size at most s≥1 and each data site intersects at most z fault-channel supports of rate ε. State/history-dependent thinning is permitted. Let τ=RT be total block duration. Let p bound the initial error distribution locally stochastically.

For fixed W of m sites, let N_f(W) count dominating fault rings on supports touching W. Its mean is at most ε z τ m; Q(W)≤sN_f(W). For t≥1, the initial-local-stochastic definition gives

 E[t^{|E_0∩W|}] ≤ (1+p(t−1))^m.

The fault generating function is at most exp[ε z τ m(t^s−1)]. These bounds remain jointly usable since the driving fault clocks are independent of initial data (and thinning only reduces counts).

A missed packed hub must have NO evaluation ring in its window: its initial local candidate remains globally good while unresolved, so any ring would resolve it by the earlier argument. All packed hubs lie among at most h0m hubs with read footprint meeting W. Thus, for fixed W and window j,

 M_j(W) ≤ sum_{h∈H(W)} 1[no ring of h during j],
 E[t^{M_j(W)}] ≤ (1+q(t−1))^(h0m),  q=e^(−λT).

This bound is for a fixed containing hub set, not for a future-adaptively selected packing. Therefore it remains a valid union-bound majorant even though W_j and G_j are chosen using the history. Evaluation-clock no-ring events are independent of the dominating fault process.

Set p_seed=max(p,ε z τ) and p_bad=max(q,ε z τ). With t=p_seed^(−1/(2s)), the seed count moment is ≤exp(C√p_seed m), for a fixed constant C; analogously the obstruction count moment at t=p_bad^(−1/(2s)) is ≤exp(C'√p_bad m). For α=1/(2C_work), Markov's inequality yields

 P[|E_0∩W|+Q(W)≥αm] ≤ [exp(C√p_seed)p_seed^(α/(2s))]^m,
 P[Q(W)+M_j(W)≥m/C_bad] ≤ [exp(C'√p_bad)p_bad^(1/(2sC_bad))]^m.

Connected-animal counting on fixed G_R contributes only a factor C_graph^m. Write the resulting bases as r_seed and r_bad. For sufficiently small parameters they are <1. The reduced residual's support tail, jointly with the good-cluster event, obeys

 P[Good and S⊆R_min] ≤ C_R [r_seed^(c_R|S|)+r_bad^|S|],
 c_R=(h/Δ)θ^(−R),                                    (8)

where rounding m to integers only changes constants, and C_R is independent of N and S. Taking |S|≥1 absorbs the prefactor into a local-stochastic parameter bounded by C_R(r_seed^c_R+r_bad).

The complementary bad-cluster event has probability ≤C N r_seed^(c_cut√N). This follows from (7), rooting a connected large K at one of N vertices, and the same seed-count tail. The cutoff c_cut√N is chosen below both the small-error confinement cutoff and code distance, so the minimum-syndrome representative on Good preserves logical sector.

To obtain a fixed invariant noise parameter: first choose R so the power of p in r_seed^c_R exceeds one; then choose sufficiently small p_* so the ancestral contribution at p_seed≈p_* is below, say, p_*/4. Next choose constant T large enough to make q small enough that the miss contribution is below p_*/4; finally choose ε sufficiently small that ε z RT preserves both budgets. All choices are independent of N. Fresh clock increments are independent of past, so (8) can be iterated using subnormalized Good histories without conditioning and renormalizing each step. The union of bad-block probabilities is at most O((t/τ)N exp(−c√N)).

This yields a plausible fully specified threshold proof for the ideal atomic asynchronous Pauli comparator, pending independent audit of the deterministic localization and counting. For quantum CSS storage with Pauli faults, apply the two sector arguments using the same bounded-degree read graph; separate ideal X/Z feedback commutes with the opposite-sector syndrome, and union-bound the two bad-sector events. The claim remains about decoded logical information, not pristine physical qubits at readout.

### Componentwise cutoff clarification
W_j may be a union of many small components and have total size exceeding the cutoff. Apply Proposition 14 and confinement to each component separately, then sum. Distinct components have disjoint syndromes. A hub containing a beneficial candidate touches a currently erroneous site in its read footprint; it cannot touch errors in two different components because that footprint is a clique. Thus candidate masses can be combined without a volume-sized small-error assumption.
