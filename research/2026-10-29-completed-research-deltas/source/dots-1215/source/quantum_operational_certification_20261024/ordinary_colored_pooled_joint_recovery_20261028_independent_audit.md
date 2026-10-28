# Independent audit: colored causal composition and pooled joint recovery

28 October 2026. Auditor: `producer-workspace/audit_algebra_extraction`.

**Received under the retained exact structural, reset-source, and paid finite-control contracts.** Source: `ordinary_colored_pooled_joint_recovery_20261028.md`, frozen SHA-256 `d63c30417caee39cc16f8b80f44bb01ac25933c7cab647f33897a651bdd22c47`. This is a different learned receiver order and acquisition schedule, not a retrospective improvement of an old deployed channel or old holdout certificate. No source sampler, acquisition experiment, or hardware run was performed in this audit. Earlier received files remain unchanged.

## 1. Exact logical packing and the observed coloring guard

On simultaneous coarse success, every known envelope W_i contains the true local Pauli pair and all its permitted learned patches. Its width is at most `W=min(n,3w-2)`. If s such true logical pairs lie inside L physical qubits, their commuting Pauli representations supply a faithful unital representation of the full matrix algebra `M_(2^s)` in `M_(2^L)`. Hence `s<=L`. This is a full-operator representation argument, not a claim based on the occupied gauge rank or a local state entropy.

Envelopes containing a common site lie within at most `2W-1` sites. Packing therefore bounds their multiplicity by `C_max=min(q,2W-1)`. An interval-graph left-endpoint sweep realizes the maximum-overlap coloring. The algorithm checks the observed color count and returns a physical fallback if it exceeds the promised cap. Such a history is excluded by simultaneous coarse success, but passing the check does not certify that success or the structural family.

The receiver must actually be reordered by these colors. Learned overlapping blocks generally do not commute, so the new channel is not asserted equal to the earlier arbitrary-order receiver. Within a color, envelope registers and labeled receiver ancillas are disjoint; the net three-gate macros commute. Hardware serialization and routing are permissible only with tracked/restored net support. The abstract color count is not a constant-hardware-depth assertion.

## 2. Common envelope cones and the joint-reference argument

Use the directed overlap graph, oriented from smaller to larger color. For output i, its graph ancestors are a common support overapproximation for BOTH actual and ideal backward Heisenberg cones. A layer can extend the physical span by at most `W-1` on either side; disjoint same-color macros cannot propagate a chain within that layer. Thus every ancestor span has length at most

`L_cone=W+2(C_max-1)(W-1)`.

All ancestor envelopes, and therefore all their true logical pairs, lie in that span. Packing gives `|Anc(i)|<=K=min(q,L_cone)`. Running the same span argument forward bounds the number of output cones containing any given block by K. These are graph reachability statements; no fitted accidental commutation or independently generated marginal decoder is substituted for the actual circuit.

For each output, start with its Bell projector on `R_i,A_i`, retaining the full global reference, gauge purifier, and receiver-mixture purifiers. Heisenberg peeling removes every outside-cone macro from each circuit exactly, for every initial state. Arbitrarily correlated gauges do not defeat operator-support commutation. The two resulting RESTRICTED circuits act on the same initial purified state. This restriction step is essential: merely dropping terms from the previous full-state hybrid would leave uncontrolled outside-cone actual prefixes.

Every subset of ideal controlled gates still preserves `rho_PA=rho tensor I_A/2^q`, because each such gate acts only on encoded maximally mixed logical factors and receiver ancillas. The restricted ideal output has Bell success one for i, as follows either from Heisenberg deletion or the true compatible logical swaps. The received elementary errors remain `delta_Z/2,delta_X/2,delta_Z/2`. A restricted hybrid and Cauchy–Schwarz therefore give

`p_i <=3|Anc(i)| sum_(j in Anc(i)) e_j`,

where `e_j=delta_Zj+delta_Xj/2` and p_i is the marginal Bell failure of the REAL new joint receiver. The distinct Bell projectors commute, so

`ell_joint <=sum_i p_i <=3K² sum_j e_j`.

No independence among marginals, errors, gauges, or learned generators appears in this proof. The older full hybrid also holds for the color-ordered circuit, yielding the combined coefficient `3A` with `A=min(q,K²)`.

The received sign-control construction supplies `delta_X,delta_Z<=25eta`. At `eta=epsilon/(16384qA)`, the virtual joint loss is at most `(225/2)qA eta`, and the separately promised global Pauli-gauge dominance plus four-anchor quadratic domination yields regret at most `450qA eta<epsilon/20`. Neither global dominance nor exact logical compatibility is inferred from the data.

## 3. Exact-fill antithetic pairs: one-bank iid, not joint independence

Fix a coarse history, one envelope color, one inner patch color, and one input axis. All measured physical patch registers in this pool are disjoint. Each independently reset pair of calls has independent uniformly chosen first sign vector s, followed by its complement -s, with independently uniform anchors. The two calls are both charged. Each learner routes one selected physical register to each sign bank using only its own input sign.

For a fixed learner i, condition on its own routing/sign sequence. In a chosen bank b, the selected logical-i input has sign b. The selected other-logical signs are either the independent uniform vector `s_(-i)` or its complement, hence are still uniform; the selected anchor is independent and uniform. Linearity of the physical source then makes this bank's single-copy marginal exactly the desired `r_(i,j,b)` on its patch. The source reset and fresh independent pairs give exactly `r_(i,j,b)^(tensor N_B)` for that ONE bank. This argument only needs disjoint measured registers for simultaneous instruments; it does not require a product gauge or disjoint supports of every inactive logical factor.

The plus and minus banks can be correlated, and different learners can also be correlated. Nevertheless, each complete bank instrument is trace preserving on its own disjoint register factor when its outcomes are not conditioned upon. Other such instruments cannot change an individual bank's marginal experiment. Each estimator must use only its own bank, routing labels, and internal records; it cannot adapt its measurement to the opposite bank's current outcomes, other current input labels, or shared current anchor labels. The all-estimates-frozen boundary before combining densities into CPTP fits enforces precisely this policy.

This is an algorithmic dataflow condition, not cryptographic ignorance of input controls. The controller may have generated the full sign vector, but the estimator does not use the excluded records. The guarantee is a union bound on bad events, not a posterior guarantee conditional on every eventual joint transcript. Conditioning first on other banks' measurement results would generally destroy the stated iid marginal law.

The exact counterexample in the source is correct: for a two-logical identity source and a learner-1 patch containing both logicals, the plus-bank spectator X sign and minus-bank spectator X sign are perfectly anticorrelated. Each bank individually has maximally mixed spectator, but their joint spectator correlation is -1 rather than the product-marginal value 0. Measuring the other bank reveals a conditional spectator state. This is why the statement deliberately does not claim a joint plus/minus tensor product.

There are at most `4qR_max` fine state estimates. Giving each failure budget `beta_F/(4qR_max)` yields exactly the logarithm `log(48*4^w*q*R_max/beta_F)` in the received finite Bures cap. Two actual calls per pair, two axes, and at most `C_max*c1` physical color combinations give `4C_max*c1*N_B` raw calls. There is no probabilistic fill, rejection, optional source stopping, or quantum-register cloning in this phase. The number and workspace of actual local estimators remain extensive in q.

## 4. Pooled spectrum comparisons and conditioning on past records

Candidate channels are frozen before their tournaments. In a comparison batch, condition on the entire PAST history: every active learner's pair and local spectrum observable are now known and fixed. Every current logical input receives a fresh independent axis/sign, including inactive inputs. Averaging other current labels makes their inputs maximally mixed. The common fresh source anchor is also averaged. Thus each active learner has the same individual comparison mean and second-moment bounds as in the received theorem, plus the explicitly paid backward-observable residual.

Other simultaneous measurements act on disjoint envelopes and preserve that marginal by trace preservation. Different learners' current outcomes may be correlated. One does not condition a learner's concentration proof on those other current outcomes. Within each fixed batch the source calls reset and the controls/pair are frozen. Consequently the usual individual Bernstein guarantee remains valid conditional on the past. Sharing or retaining past records is different from conditioning on another learner's current outcome.

Postorder slots preserve each balanced bracket's dependencies while permitting one current comparison per logical learner per shared call. Two incompatible comparisons on the same logical output are not attempted in parallel. Empty or finished slots use a trace-preserving discard. With

`L=log(2q(R_max-1)/beta_T)`,

`N_pair=ceil(2048h²L/(kappa² eta))`,

the individual failure budget is `beta_T/[q(R_max-1)]`. Union bounding all real comparisons gives beta_T without cross-learner independence. The source cap is `C_max(R_max-1)N_pair`, not q separate copies of this experiment.

The local constants check exactly: `2*(22/256)+1/4=27/64<1/2`. Hence selected calibration excess is at most `(27/64)kappa eta`, implying `ell0_i<eta`. The single-candidate case correctly skips all comparison formulas, including logarithms of zero.

## 5. Complete ledger and claimed scaling

The coarse stage remains q separate localization modules; its `2qM` state estimates and total beta_L allocation give the stated `log(24*4^w*q*M/beta_L)` and source cost `2q c N0`. No unknown-overlap coarse patch is reused for incompatible tomography tasks.

The complete cap adds coarse calls, pooled fine calls, pooled comparisons, the fresh GLOBAL Clifford/stabilizer encoder stage, and one payload. Safe early termination can use fewer calls than this upper cap; every executed call, including failed histories, remains charged. All returned channels are physical, and no failure branch is postselected out. The statistical allocations sum to at most `epsilon/8`; all finite controls, private randomness, routing, and payload operations share the existing operational discrepancy allowance.

For fixed w, `C_max,c1,R_max,A` are bounded independently of q. Since `1/eta=16384qA/epsilon`, the preferred fine and comparison BLOCK-call counts are linear in q, with the displayed width and confidence factors. This does not imply linear total qubit traffic: each call uses q logical input qubits and emits n physical outputs. Collective bank memory, its interconnect, the number of local estimators, receiver processing, and routing remain explicitly paid. A pool can retain `2N_B*n` physical qubits plus its estimator workspaces.

The newly ordered joint decoder is frozen before fresh global encoder optimization. The received global stabilizer survival score, not a product of marginal scores or a previous holdout, is used. Only `N_count+1` joint receiver invocations occur; all acquisition and comparison controls have separate costs. The untwirled dimension-dependent diamond bound and the optional additional discarded-key Pauli-twirled service retain their earlier, distinct meanings.

## 6. Exact linear-loss witness and deterministic evidence

For one logical/gauge pair let `X'=X_L tensor Z_g`, `Z'=Z_L`, and use the literal three-gate receiver with a maximally mixed receiver ancilla. Conditional on gauge bit zero, it is an ideal SWAP. Conditional on gauge bit one,

`C_Z C_X(-X_L) C_Z=(Z_L tensor Z_A) SWAP`.

After tracing the residual logical register, the output channel is therefore `(1-p)Id+p Ad_Z` for gauge `diag(1-p,p)`. Its weighted generator errors are exactly `delta_X=4p`, `delta_Z=0`. Independent gauge pairs give joint Bell loss `1-(1-p)^q`. This rules out replacing the SUM of local errors by their MAX with a q-independent coefficient; it does not contradict the proved constant coefficient multiplying the sum.

`colored_pooled_joint_recovery_independent_check_20261028.py` performs zero-source exact/deterministic checks:

- all matrix units through the literal one-pair channel, proving the conditional identity/Z channels exactly;
- the symbolic weighted generator error `4p`;
- exact antithetic individual bank marginals, nonproduct joint state, spectator correlation -1, and altered marginal after opposite-bank conditioning;
- 1,965 deterministic envelope families with explicit one-site independent logical-factor packing witnesses, including exhaustive small families and long patterned families up to q=257 and W=8;
- exact optimal interval coloring, directed ancestor/descendant counts and physical span caps, and their double-counting identity;
- the rational tournament and global error constants.

All checks pass. The largest tested color count is 15 and the largest ancestor/descendant count is 43; every tested count obeys its own stated K bound. The code uses no random sampling and no acquisition or optimizer run. These diagnostics supplement, rather than establish by finite testing, the general causal and marginal-law proofs above.

The result remains conditional on exact compatible local algebra, known output coordinates, independent source resets, relative visibility, the separate global dominance promise for oracle comparison, allowed global known-Clifford input/readout control, and the paid whole-process implementation guarantee. Approximate locality, hidden drift, product-only global validation, source-family certification, and advantage over an equally informed conventional learner are not received.
