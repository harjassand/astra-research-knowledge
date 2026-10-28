# Independent statistics audit: colored and pooled joint recovery

28 October 2026. **PASS.** This analytic review binds `ordinary_colored_pooled_joint_recovery_20261028.md`, SHA256 `d63c30417caee39cc16f8b80f44bb01ac25933c7cab647f33897a651bdd22c47`. It covers the causal/Bell-union bound, antithetic state pools, pooled comparison confidence, deterministic caps, and the separate global encoder stage. No source samples, simulations, private-source reads, or changes to received manuscripts/pilots were made.

## 1. Coloring and the two causal multiplicity bounds

On the simultaneous coarse good event, each known expanded envelope W_i contains both true generators of logical i and all its possible fine candidate patches. Its length is at most W=min(n,3w-2). If s compatible logical qubit algebras are supported on L physical qubits, then s<=L. An elementary justification is to diagonalize their commuting Z operators: the corresponding X operators biject the 2^s joint-sign eigenspaces, so all have equal positive dimension and 2^s<=2^L. This uses the exact independent true logical algebra, not occupied gauge rank or learned compatibility.

All envelopes covering one physical site lie within at most 2W-1 sites. The logical packing bound therefore limits interval-graph overlap to C_max=min(q,2W-1). A left-endpoint sweep supplies an optimal interval coloring. The observed coloring-cap guard is important: on bad coarse histories it prevents a fine-source schedule with unexpectedly many colors. A guard failure returns a fixed physical replacement and is counted, never postselected away. Passing the guard does not certify the source model or correctness of localization.

The new decoder actually executes complete swap blocks in consecutive color layers. Merely having bounded overlap while retaining an arbitrary sequential order would not suffice: a long overlap chain can have a long causal cone even at clique number two. Within a color, the net block supports W_i union {A_i} are disjoint, with one distinct private ancilla leaf per block. Restored routing preserves these net supports; abstract color depth is not hardware routing depth.

Define graph edges j→k by strictly increasing color and W_j intersecting W_k. Backward and forward graph cones expand their physical spans by at most W-1 on either side per additional color. There is no same-color propagation chain. All envelopes of one cone lie in its final span, so logical packing gives at most

    K=min(q, W+2(C_max-1)(W-1))

blocks per cone. The same argument for descendants gives at most K output cones containing any fixed block. These are actual graph ancestor/descendant sets. Filling gaps in an interval and then treating artificially included blocks as graph ancestors would require a different argument; the manuscript correctly avoids that shortcut.

## 2. Why correlated gauges do not defeat the joint Bell bound

For output i, its final Bell projector acts on R_i,A_i. Outside its envelope-graph ancestor cone, net blocks can be deleted exactly from its Heisenberg evolution. This operator identity holds for any initial state, including globally correlated quantum gauges. It is performed separately for the actual and ideal circuits; one must not simply delete selected terms from a full-state hybrid containing arbitrary outside-cone actual prefixes.

Compare the two restricted circuits on the same global purified input. Every ideal elementary prefix, including a prefix of any restricted subset, preserves rho_PA=rho tensor I_A/2^q. The mixed receiver ancillas and common encoded logical/gauge tensor structure are essential here. The restricted ideal circuit has Bell success one for R_i,A_i, because the fully ideal circuit does and its outside-cone gates were deleted by an exact Heisenberg identity.

The three elementary errors for block j have squared norm delta_Zj/2, delta_Xj/2, delta_Zj/2. Actual suffixes preserve norm. Thus, writing e_j=delta_Zj+delta_Xj/2,

    p_i <=3 |Anc(i)| sum_(j in Anc(i)) e_j.

These are marginal failure probabilities of ONE actual joint receiver, not fidelities of separately deployed local channels. The Bell projectors on distinct R_i,A_i commute, so the positive operator inequality

    I-product_i Phi_i <=sum_i(I-Phi_i)

gives a union bound without independence. The two multiplicity bounds then yield

    ell0_joint <=3K^2 sum_j e_j.

The old full-state hybrid also holds for this same color order. Therefore A=min(q,K^2) gives ell0_joint<=3A sum_j e_j. With the received local rounding bound delta_Xj,delta_Zj<=25eta and eta=epsilon/(16384qA), the uniform global regret is at most 450qAeta=225epsilon/8192<epsilon/20. At fixed w, K and A are bounded independently of q. The result is a genuine full-reference/Bell-projector guarantee, not a product of marginal fidelities.

This is a different learned receiver order, not an equivalent compilation of the previous channel. Fresh global encoder learning/tests must use this frozen color-ordered receiver. The source states this distinction.

## 3. Antithetic paired calls give exactly filled individual iid banks

Fix the pre-pool coarse record, envelope color, inner candidate color, and common input axis j. All simultaneously assigned physical patch registers are disjoint. For each independent pair, draw uniform signs s in {±1}^q, use input signs s in one real source call and -s in the second real call, and use independent uniform anchors. For learner i, route the call carrying its desired own sign to its corresponding sign bank.

Conditional on i's OWN routing-sign sequence, the other q-1 signs in its selected call are still independent uniform signs: either an independent uniform vector or its negation. The selected anchor is still uniform. Averaging those excluded current labels gives the desired marginal r_(i,j,+) or r_(i,j,-). Different pairs are independent, so EACH individual sign bank has exactly the product marginal r_(i,j,s)^tensor N_B. Both raw calls per pair are charged; every bank has exactly N_B copies, without a fill event, rejection, optional stopping, cloning, or a counterfactual query.

The joint plus/minus state is generally NOT a product. The manuscript's two-logical identity example is correct: when learner 1's patch includes both inputs, its plus-bank spectator X sign and minus-bank spectator X sign are opposite. Their correlation is -1 although both separate marginals have maximally mixed spectators and their product would have correlation zero. This directly defeats conditioning one bank's iid claim on the other bank's measured records.

The implemented safeguard is a measurement/dataflow rule, not cryptographic isolation: every individual STATE estimator is a fixed local instrument on only its selected bank, with its own routing labels and internal records. It does not choose controls from another sign bank, another learner's current labels/outcomes, or shared anchor labels. Other estimators are trace preserving on disjoint registers when their outcomes are not conditioned upon, so they do not change this estimator's marginal experiment. Its own adaptive local instrument is allowed. All state estimates freeze before their results are combined into local ERM fits.

Thus each imported Bures guarantee applies marginally; a union bound makes them simultaneous without asserting independent estimation errors or a posterior guarantee on every retained transcript. The source can have arbitrary gauge correlations. Pair independence and reset access, rather than independence among bank subsystems, are what supply each bank's iid state sequence.

There are at most 4qR_max individual density estimates. Giving each failure beta_F/(4qR_max) produces exactly

    N_B=ceil[(80*4^w/m) log(48*4^w*q*R_max/beta_F)].

Two axes, at most C_max envelope colors, c1 inner patch colors, and two calls per pair give the genuine raw fine-source cap 4C_max c1 N_B. The number of local estimator circuits is still at most 4qR_max. Quantum storage for a pool can be 2N_B*n physical qubits plus the actual estimator workspaces. No physical register is assigned to two overlapping estimators.

## 4. Fresh pooled comparison batches have valid conditional Bernstein bounds

For one envelope color and one synchronized bracket slot, each active logical learner compares a fixed pair using its known spectrum-valued difference observable. Every current source call draws fresh independent X/Z axes and signs for ALL logical inputs, including inactive ones. Conditional on learner i's current labels, averaging every other current label gives maximally mixed other inputs. Its measurement therefore has the same mean r_a-r_b and variance bound as the received single-logical comparison.

The controls and contender pair remain fixed within that batch; no adaptation to another learner's CURRENT outcome is allowed. Conditional on the entire PAST batch history, fresh reset calls and fresh input-label draws give an iid sequence for each individual comparison. Cross-learner outcomes on one output may be correlated, but the marginal Bernstein bound does not condition on those outcomes. The labels used for these batches are fresh per call, not the antithetic paired labels of state tomography.

At most q(R_max-1) actual comparisons occur. With

    L=log[2q(R_max-1)/beta_T],
    t=kappa eta/(4h^2),
    N_pair=ceil[2048h^2L/(kappa^2 eta)],

each conditional two-sided failure is at most beta_T/[q(R_max-1)]. Union bounding, and integrating over previous histories, costs at most beta_T. A fixed balanced binary bracket on R_max leaves has R_max-1 internal nodes and height ceil(log2 R_max); padding actual smaller lists with byes and processing internal nodes in fixed postorder realizes the synchronized slots. Empty slots need no observation and do not license outcome-dependent postselection.

The local ERM bound remains r_min<=22kappa eta/256. The tournament gives r_selected<=27kappa eta/64<kappa eta/2 and hence ell0_i<=eta. The source cap is C_max(R_max-1)N_pair, not q times that amount, because disjoint-envelope comparisons share the same actual output in a batch. The R_max=1 branch skips all comparison logarithms, heights, formulas, and calls.

## 5. Confidence, complete caps, and what the scaling does not say

The coarse phase still uses separate logical-label experiments: at most 2qM density estimates with failure beta_L/(2qM), so

    N0=ceil[(80*4^w/m0)log(24*4^w*q*M/beta_L)]

and the coarse raw-source cost is 2q c N0. This does not pretend to reuse an unknown coarse physical patch simultaneously for different conditional logical tomography tasks.

Choose positive beta_L,beta_F,beta_T,beta_C with sum at most epsilon/8. The fine marginal guarantees hold conditional on the completed coarse record; the tournament guarantees hold conditional on all previous frozen estimates/comparison records; the later global encoder guarantee holds conditional on the frozen new receiver. No independence among these stages is assumed. Coloring failure cannot occur on the coarse good event, and its physical fallback does not enlarge the deterministic cap.

The complete upper cap is

    2q c N0+4C_max c1 N_B+C_max(R_max-1)N_pair+N_count+1,

with zero comparison term for R_max=1. All executed failed-history calls count; an early fixed fallback may use fewer calls, not refund any. The final one is a real payload block call. The sole full joint receiver is invoked N_count+1 times; state-estimation and comparison receivers have their own resource ledgers.

The received global Clifford/stabilizer Bernoulli test is retained, with mean 2^q/(2^q+1) times the actual joint Bell loss. It uses known entanglement within the input block and a joint inverse-Clifford readout, not a protected source reference or a product of marginal tests. Its separate active encoder design at epsilon/8 yields the same 7epsilon/20 good-event additive allowance. Statistical failure at most epsilon/8 and linked whole-process discrepancy at most epsilon/8 give total additive allowance at most 3epsilon/5, hence the claimed epsilon with slack.

At fixed w, C_max,c1,R_max,A are bounded constants, m is proportional to epsilon/q, and fine plus comparison raw block calls are linear in q up to the stated logarithms. This is NOT linear total qubit traffic: every call prepares q logical input qubits and emits n physical output qubits. Collective estimator invocations, classical processing, quantum storage, gate synthesis, routing, random bits, and input controls remain extensive and paid. Color layers do not remove restored-routing costs or certify constant physical depth.

The final witness correctly distinguishes a SUM from a MAX bound. For independent logical/gauge pairs with gauge diag(1-p,p), X'=X tensor Z_g and Z'=Z, the mixed-ancilla swap induces a Z error precisely on gauge bit one. Thus delta_X=4p, delta_Z=0 and joint loss=1-(1-p)^q. This can grow linearly with q at small p, so a q-independent coefficient on the maximum individual error is impossible in general. It does not contradict the q-independent coefficient on the SUM proved above, and it is not an acquisition lower bound or new sampled evidence.

The strongest equally informed conventional learner receives this same construction. Source-model membership, approximate locality, non-reset drift, product-only global validation, and a dimension-free untwirled diamond guarantee are not established. The optional paid discarded-key global Pauli twirl retains its separate averaged-service scope. All substantive checks pass; the companion receipt supplies final binding only.
