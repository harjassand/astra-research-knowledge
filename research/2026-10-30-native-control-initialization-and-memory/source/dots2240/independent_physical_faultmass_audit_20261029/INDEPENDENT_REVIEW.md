# Independent hostile audit: physical-window ancestor fault mass

Date: 2026-10-29 UTC. Exact source hashes are in `SOURCE_SHA256.txt`; immutable-in-this-audit copies are retained beside this report. This is a separate audit from the reset-tail audit. Original files were not edited.

## Verdict

No counterexample or proof failure found in `ANCESTOR_WITNESS_THEOREM.md` or `MULTIPLICITY_AND_INITIAL_MARKS.md` under their explicitly stated hypotheses: actual separately recorded reset channels, additive independent state-independent Poisson CPTP kicks, initially zero marks for noise-vanishing claims, local product witnesses, bounded incidence budgets, and bounded kick-to-owner/ witness incidence. The CP insertion accounting and repeated-cell multiplicity argument withstand the challenges below. This is conditional mathematical acceptance of the physical-record envelope, not implementation certification, DATA serialization, or a memory threshold.

`TWO_HALF_GOOD_SERVICE.md` also has a valid conditional probability argument, but its derivation of a finite noise-conflict coloring needs the geometry qualification recorded below. Its exact good-terminal DATA identity is an input, not proved by this audit or by the counting argument.

## 1. CP factorial insertions: no independent-delay assumption

For additive CPTP jump sources, the total rate of a source is its state-independent Poisson intensity. Expanding the quantum evolution conditioned on the Poisson points, and distinguishing an ordered tuple of distinct points, gives the Poisson factorial/Campbell-Mecke identity with the same noisy evolution and additional deterministic inserted CPTP maps. Undistinguished kicks must remain in the evolution. The text does this; it does not replace their effect by a clean semigroup or condition the system state on a rare future reset record.

A survival event after insertion is a CP record restriction, so its effect can be dominated by the time-dependent positive product witness. Each deterministic kick costs at most D through E_e^*(Z_A)≤D Z_A. Summing the unselected-source perturbations costs at most epsilon J_R(D-1)|A|, giving rho=r/2 under the stated condition. No normalization of record branches enters.

For an unordered ancestor partition, canonically ordering its groups provides one ordered factorial-measure integration, with no extra k! and no missing inverse factorial. For factorial moments, ordered distinct ancestors are themselves what (A)_k counts. These are different but consistent conventions.

## 2. Ancestor multiplicity and interval ordering

A marked reset necessarily has a post-previous-reset incident kick ancestor. Choosing the LAST incident kick before it makes one physical kick the ancestor of at most one reset per owner and at most b resets total. An intervening reset clears the mark; a second marked reset requires a newer kick. This is deterministic record algebra, independent of clock dynamics.

For same-owner selected emissions u_i<u_j, the later last ancestor tau_j exceeds u_i. Thus full [tau_i,u_i] intervals have disjoint interiors; shortened nonempty [tau_i,s_cell_i] intervals do too. Distinct-cell binary occupancy and repeated-cell count claims both use this fact correctly. If multiple marked emissions lie in the same owner/cell, at most one can have its ancestor before the cell start. Later ancestors are inside the cell, producing empty shortened intervals.

The proof applies the product survival inequality only on the valid disjoint-interval domain. It then drops the domain indicator from a nonnegative integral. It does NOT assert the product survival estimate on overlapping same-owner intervals. This order of operations is essential and is expressly preserved in both documents.

## 3. Binary-cell partition bound

The row-sum argument, rather than raw partition counting, removes Bell-number growth. For fixed (e,tau), at most one cell per affected owner contains tau, and future cell-start weights form a geometric tail. The displayed B_Delta is conservative. For a fixed target cell, integrating its ancestor kernel gives at most nu_0(Delta+1/rho). Expanding the sum of remaining weights bounds size-j groups by the stated C_j, including the correct (j-1)! divisor.

Partition recursion then gives F(S)≤q^|S| when q=(epsilon C_*)^(1/b)≤1. The apparent q^(-b) expression should simply be bypassed in the zero-rate case; then all marks remain zero and the event is impossible. This is a harmless endpoint convention, not a failed bound.

Taking one largest clean witness color loses exactly the 1/P exponent. Physical kick incidence is already paid through b_Z and J_R; no independence between colors is claimed. The final uniform event-effect bound is equivalent to the CP event-instrument diamond norm bound for the specified all-zero initial classical mark register.

## 4. Factorial moments and multiplicity

A_V counts DISTINCT ancestor points, not emissions. Its canonical representative for each ancestor is unique, so an ordered tuple of k selected ancestors gives k distinct representative emissions, even when destination cells repeat. Summing assigned destination cells therefore introduces |V|^k, not an unbounded reset-count factor. The inserted-event probability is bounded by the survival requirement; no assertion that survival ensures an endpoint reset is made. Consequently dropping reset-existence conditions only enlarges the integrand and requires no reset-rate density.

Each of the k ancestors incurs one D and one conservative alpha^-1. The k source/time integrations factorize only after removing the nonnegative disjointness/eligibility restriction, yielding E[(A_V)_k]≤(epsilon C_A|V|)^k. Because all terms are nonnegative, monotone convergence justifies summing the binomial series even before exponential integrability is established. Y_V≤b A_V gives the displayed exponential moment.

Holder over P color counts yields exactly epsilon(C_A/P)|V|(exp(bP theta)-1). It uses no color independence. Chernoff with exp(bP theta)=1/(epsilon C_A/P), plus |V|≤total prescribed positive mass, gives the stated conservative factor e per mass unit. A second Holder inequality correctly combines direct insertion mass with delayed emission mass, which can originate from the SAME physical kicks. The extra direct-rate incidence assumption is indispensable and is not silently inferred from the reset witness.

## 5. Late windows and initial marks

Late target windows retain their actual ancestors all the way back to the global zero-mark initial condition. No artificial refresh at a block boundary or rare-history conditional bound is introduced.

With specified initial marks, each initial owner contributes at most one initial-cause emission. Post-boundary kick-ancestor bounds remain uniform over the quantum state and passive initial annotations. Thus the deterministic exp(theta|M0|) multiplier is valid. For random initial classical marks correlated with quantum data, conditioning on each mark sector and averaging is legitimate because the quantum bound is uniform in that sector.

The optional burn-in expansion bounds initial descendants by owners surviving without reset to u. Within a color, the noisy product witness gives the required joint survival bound. Bernoulli generating-function expansion and Holder yield equation (9), including its possible loose factor above one at short u. Holder between initial and kick descendants yields equation (10). Neither step assumes those causes are independent.

## 6. Two-half good service: checked with explicit qualifications

Fewer than two resets implies an empty half-window. The 2^m union bound and chronological CP composition for the two owner subsets are correct. Per-window buffered packing and chronological composition extend this to distinct cells on a fixed nonoverlapping grid; duplicate/overlapping tests are correctly excluded.

Given the stated history-sector invariance and exact good-terminal instrument input, a first complete reset followed by a kick-free history neighborhood ensures the second reset is a fresh good terminal, not an abort. Charging every neighborhood kick as a control spoil is conservative. Correlated shortfall/spoil events are combined using min(x,y)≤sqrt(xy) and a subset union, not independence. The resulting q_good is valid for the record-defined witnessed-service criterion. This does not separately prove that arbitrary asynchronous decoder operations are useful or serialize as intended data updates.

**Noise-coloring qualification:** Section 4 explicitly assumes a fixed P_N, and the spoil proof is valid with it. However, bounded kick-support CARDINALITY and bounded summed incident RATES alone do not imply a bounded noise-conflict chromatic number. For N owner neighborhoods, allow a two-site kick on every pair with per-pair rate O(1/N). Each kick touches two neighborhoods and every owner's summed rate is bounded, but the conflict graph is complete and requires N colors. A uniform spatial-diameter/range condition relative to bounded-degree geometry, bounded conflict degree, or the explicit fixed-P_N hypothesis is required. If “bounded noise support/geometry” means fixed spatial range, the document's inference is justified; if it means only cardinality plus rate, it is not. No failure of the theorem conditional on its stated P_N assumption is asserted.

## Independent finite-record challenge

`check_ancestor_records.py` exhaustively checked 97,656 classical records of lengths zero through seven, using kicks on owner 0, owner 1, or both, and resets of either owner. It examined 132,492 marked emissions and 1,872 repeated owner/cell instances. PASS: distinct-owner ancestry per kick, maximum multiplicity two, disjoint same-owner ancestor intervals, and at most one pre-cell-start ancestor among repeated-cell emissions.

This is evidence only for finite classical annotation algebra. It is not numerical certification of the CP survival inequalities, factorial moment bounds, or a threshold.

## Unestablished obligations and blockers

No tool/permission block occurred. The operator witnesses, actual physical reset interface, and full local implementation hypotheses are assumed inputs rather than certified by these record-count proofs. Exact DATA-instrument factorization, in-flight boundary interfaces, decoder correctness and any quantum-memory threshold remain unestablished here. No failing source/test was edited or concealed.
