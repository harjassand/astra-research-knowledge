# Independent whole-proof and exact-receiver review: compound seed

## Verdict

**The frozen ordinary mathematical theorem and its exact constructor are accepted within the stated biclique/arm family.** No substantive proof or receiving defect was found. The conclusion is irreducibility, positive recurrence, and every finite exponential stationary total-count moment, for arbitrary positive rates in that structural family. The quantitative executable uses positive rational rates and a requested rational t>1.

This is an ordinary mathematical review with independent exact code, not a proof-assistant formalization, a general weak-reversibility theorem, or a novelty determination. Source-process compliance receives **no PASS**: the controlling `ACCESS_CORRECTION_AND_SCOPE_ADDENDUM.md` and `independent_audit/SOURCE_ACCESS_CORRECTION.md` record and quarantine a completed noncompliant alternate-source read of previously denied literature. That comparator is not a premise of the theorem or this proof review. Frozen originals are preserved rather than silently edited.

## Frozen binding

Author manifest: `AUTHOR_MANIFEST.json`, SHA256
`3f5605a4850e0d7e638c418254b7dbd509cbfcd4a8e926677fd3f1c61198d13a`.
All 15 listed files were read/checked or replay-bound at their exact byte counts and hashes. The separately frozen controlling addendum `ACCESS_CORRECTION_AND_SCOPE_ADDENDUM.md` has SHA256 `4223dd0259c3aa2802190202fd7ac0cb02b23fa334a54cc1333e5a55516e7a56`; its source-process failure and significance quarantine govern this review, without rewriting the original author manifest. Principal sources:

- `COMPOUND_SEED_THEOREM.md`: `15f3494e35ebffa9e726e51a7f8bedd51d8edd7bbed43f951a6975c0b9534aaf`.
- `compound_seed.py`: `d62472c844fa789bd1b3791046e3626f48a3e038dbf320733e1a491e04574a80`.
- `exercise_compound.py`: `35add02bf1fc55d9b8f039e1cce38d13ca8989bb5489137820e07d61a8aaf44c`.
- `exercise_results.json`: `4d6ccee03cbeba563e4f0252b85690478fc20029beebeadb19f68e94565db061`.
- `main_demo.json`: `aa124110d80248fde0ba748c3adff98cb68f7e019ec00c951a14a92b7e7f3caf`.

The final package-relative `independent_audit/AUDIT_MANIFEST.json` binds this receipt, the correction, all frozen author files and all independently written scripts/results/replays. The manifest excludes itself to avoid a self-hash cycle. No earlier accepted package was changed.

## Ordinary proof reconstruction

### 1. Acquired geometry, including ties and sparse incidence

Raw nonconservative channels identify the unique reversible port. Every internal edge is checked as a reversible hub/active edge; each hub is square-free and has its own reversible 2A amplification edge. Every satellite has at least one arm, but full arm incidence is not required. Duplicate channels are added; validated null channels are discarded.

Two-coloring followed by every cross-pair check acquires complete bipartite connected components. For their shore totals, R=A+Σmin(L,U). The minimum is unchanged or falls by one when a satellite is consumed. Adding a hub increases its component minimum by exactly one, even when the consumed satellite lies in that same component. Thus arm capture changes R by zero or minus one, reverse arms by zero or plus one, and amplification by minus/plus one. At R=1 a decrement is impossible. At R=0 all internal sources are disabled; A=0 by itself is not the inactive face.

On strictly larger shores and outside the hub graph, every capture is neutral. Their total population dominates N−2R+A; bad-capture population is at most 2(R−A), including equal-shore ties. The K_f A R bound follows. Complete bipartiteness supplies Σ_edges x_i x_j=Σ_components L U, then the quadratic bound ≥(R−A)^2/k. No matching or grouping oracle is supplied to the receiver.

### 2. Inventory profile and both joins

All backward denominators are positive because epsilon<lambda+beta. The recurrence is decreasing and makes the base drift equality for 1<=r<K. At r>=K, c/r<=1/2 and r/(r+1)>=1/2 give the stated negative bound. The r=K join uses the exact same tail value; no approximation occurs. The d_* minimum bounds (r+1)^2(g_r−g_(r+1)) globally.

J>=K+1 puts both neighboring g-values in the tail for every r>=J. Direct substitution into E_r gives E_r<=−D+2c(mu+K_f+beta)/r<=−D/2. The finite q maximum cancels every remaining positive E_r at 1<=r<J. This is actual finite acquisition, not a supplied good patch.

### 3. Corrector and core denominator details

For f=A/(R+1)^2, all enabled internal changes have |Delta A|<=2, |Delta R|<=1 and satisfy |Delta f|<=11/(R+1)^2. Neutral forward capture has the exact negative increment −1/(R+1)^2. Reverse-neutral arms can have positive correction drift despite zero g-drift; they are explicitly charged by s_h and absorbed source-by-source by half the same hub's amplification drift under the N+1 threshold. They are not silently discarded.

Birth/death change N as well as R. The core correction in the proof retains both denominator changes. For the displayed death bound, the first absolute-difference term is at most (11/2)q mu/(N+1). The remaining positive denominator term is bounded by

    q mu A^2/[N(R+1)^2(N+1)] <= q mu/[4(N+1)],

using N>=A and A/(R+1)^2<=1/4. The total is at most (23/4)q mu/(N+1)<6q mu/(N+1), so the final enlarged12mu allowance is safe. A=1 deaths and N=1 are included. Immigration is bounded by the displayed12lambda*t allowance. No constant protected-A clock is assumed.

### 4. Uniform master inequality and finite exception

After half-hub absorption, substitute the base profile inequality and use r²−(r−A)²<=2rA. This gives exactly the master inequality (15), with the correct negative-capture term. Its count factor N−2r+A is always nonnegative by the inventory definition.

For r<J and N>=4J the fast-capture factor divided by N+1 is at least1/4, paying A E_r by the acquired q. For r>=J, E_r is already negative. N+1>=2q C_e/epsilon leaves at most epsilon/2 error. Since g_r>=1 and h<=g_r+1/4<=2g_r, this yields the stated geometric drift. At R=0 direct immigration, including its q/[4(N+2)] correction, gives the separate negative bound.

The finite exception {N<N_*} is bounded using raw rate sums and h<=H, with no enumeration. The factored C_F covers its positive drift and zeta W. The binomial expression counts the exception correctly. It is accounting, not executed state-space search.

### 5. Nonexplosion, communicating class and moments

Nonexplosion has the simpler ordinary comparator N(t)<=N(0)+Poisson(lambda t). Finite count sublevels contain finitely many states with bounded jump rates, regardless of internal rate size. For every satellite X, the acquired arm and amplification give the reversible enabled singleton path 0→A→2A→hub→A+X→X. Translating such paths establishes full-orthant irreducibility.

The global bound LW<=−zeta W+C_F is sufficient for the standard localized semigroup estimate P_tW<=e^(−zeta t)W+C_F(1−e^(−zeta t))/zeta: apply stopped Dynkin to the integrating factor and then Fatou/nonexplosion. Normlikeness yields tight occupation averages and the usual countable-state invariant/Foster conclusion; Fatou on those averages gives pi(W)<=C_F/zeta without assuming beforehand that W lies in the invariant generator domain. Thus pi(t^N) is bounded as claimed. Repeating the finite acquisition for every finite t>1 gives all stationary exponential moments; testing finitely many t is not its justification.

## Independent receiver, not constructor self-receiving

`independent_audit/independent_receiver.py` imports no candidate code. It independently parses/normalizes raw reactions, identifies the port, reconstructs graph sides using a separate breadth-first traversal, checks every incidence, derives all rates, profile values, q, thresholds and factored bounds, and verifies the full exact wire receipt including every charged-work field. Its own raw digest is reconstructed. Candidate code is imported only by the exercise driver to supply receipts for this separate receiver.

Accepted receipt equality is exact; no floating proposals, tolerances, simulated trajectories, fiber stationary laws, or expanded Foster powers are used. The original semantic receivers recompute using the original constructor and remain correctly described as non-independent.

Executed independent controls:

- Five separately built raw cases: base n4, sparse K2,2, two components, K1,3 without a free passenger, and n3 with unequal rates.
- 2,021 ordinary states plus270 targeted boundary/huge states through count10^50. Every enabled local correction, aggregate rate bound, full raw generator and applicable master/Foster inequality is checked exactly.
- 341 finite profile/tail algebra checks, including both joins and huge r.
- 43 qualitative,116 numerical, and55 cap-UNKNOWN semantic leaf corruptions rejected, including all work/cost fields.
- 24 coordinate permutations; t=101/100,3/2,5 accepted and t=1000 correctly numerical-UNKNOWN under the20,000-iteration cap.
- Seven structural UNKNOWN controls plus an additional missing-both-amplification-edges control;22 exact-domain controls; duplicate splitting plus a null row with changed raw-work accounting.
- Additional very small immigration/large death case accepted at N*=5,372,292,710,499,387 with five exact target states; mu=10^(-5000) correctly numerical-UNKNOWN with qualitative success and no recurrence/head scans.
- Fresh-process reverse rate10^5000: constructor import changes CPython's decimal guard from4300 to0 as documented; a74,361-byte receipt with50,054-bit retained scalars round-trips through both receivers, with three exact huge-threshold state checks. No Foster power is expanded.

The interpreter-level decimal setting is explicit trusted-research behavior, not hardened-service admission or a global resource cap. The profile budget counts only K−1 backward iterations plus J−1 head checks. Preprocessing, exact bit growth, memory, total arithmetic and time are not bounded by it. Qualitative recognition does not execute profile construction.

Author replay: all seven cases and published totals (2,128 states,18,852 local assertions,912 outside-Foster checks,159 leaf corruptions,24 permutations,10 domain controls) reproduce byte-identically, as does the main receipt. Independent controls and all three comparator/graph script outputs also replay byte-identically from the staged package layout.

## Exact inventory boundary and no-go scope

`independent_audit/GRAPH_INVENTORY_BOUNDARY.md` gives the full elementary equivalence: every enabled hub removal lowers integer capacitated matching by exactly one for every capacity vector iff every nontrivial graph component is complete bipartite. A triangle with capacities(1,1,2), or an inducedP4 with unit capacities, supplies a drop2→0 witness. The graph script checks all1,098 graphs through five vertices, with44,392 exact edge-removal checks on admitted graphs and924 explicit obstruction witnesses on rejected ones. This is a classification of this universal inventory-removal property, not stability or all alternative inventories.

The F(A,N) and t^N g_R no-go arguments were independently checked on the same full irreducible class. They are one-step geometric-Foster representation obstructions, not transience results or exclusions of sampled-time/other composition methods. They even hold at a product-form parameter point. The primary-literature scope note is bounded, not exhaustive; its Laurence–Robert read is specifically quarantined by the access correction above. No priority claim follows.

## Costs and final boundary

For the main t=2 receipt, K=28,J=504,N*=948431; the executed acquisition uses27 backward steps and503 head checks, retaining29 profile values. The Foster constant contains2^948432 and the exception contains binomial(948434,4) states; neither is expanded/enumerated. The constants are conservative proof witnesses, not useful mixing estimates. Sparse incidence and multiple bicliques were independently tested; odd cycles, missing edges, uncovered species, missing amplification, other raw channels and numerical cap exhaustion are not stability counterexamples.

Mathematical review complete for this frozen source boundary. Source-access correction is separately explicit. No new-family expansion or modification of prior accepted files is authorized by this receipt.
