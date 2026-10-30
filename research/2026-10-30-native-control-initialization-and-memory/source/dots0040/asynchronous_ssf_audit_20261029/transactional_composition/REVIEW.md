# Independent full transactional-composition review
2026-10-29. Source hashes: SOURCE_SHA256.txt. This review is distinct from the ideal-clock and component audits.

## Verdict
**The composition is mathematically valid for the explicitly specified driven, graph-local, reset-first transactional model with exogenous fixed-range Poisson CPTP kicks, subject to the already stated component premises.** I found no remaining composition-level counterexample after checking coefficientwise semantics, the real-record moment interface, branch-uniform backwards witnesses, CP effects, and the final dressed decoder. The explicit support-to-cell calculation below discharges the corollary's otherwise uninstantiated Q-interface under bounded geometry.

This is a decoded-logical memory result, not arbitrary coherent-Hamiltonian robustness, passive thermal storage, geometrically local high-rate storage in fixed Euclidean dimension, or a finished noisy physical readout implementation. The minimum-syndrome decoder can be computationally expensive. Those restrictions are substantive.

The checked corollary includes the corrected initialized domain and fixed physical-range hypothesis. Its exact initial reviewed hash is
06136a4a5ac17d9feb0b5877997c63fefb0696467ecc1a07ef7ec2eb77961c7e.

## 1. Exact model and initialization being accepted
- Use the reset-first transactional generator, complete separately labeled reset channels, controller/workspace-blind diagonal monitors, ownership-gated computation edges, distinct computation/abort structure, and disabled cleanup in abort phases required by the independent gauge audit.
- Program each intended hub channel as the actual deterministic SSF instrument: extract the complete required stabilizer information, choose an accepted candidate whenever any exists, otherwise do nothing, and apply its Pauli correction. This is not true for an arbitrary recovery channel. On a fixed-degree code, the footprint, truth table, Stinespring workspace, and exact local gate list have size independent of N.
- The physical interaction graph has bounded degree, bounded local dimension and bounded resource density. Physical kicks have fixed bounded range on this graph, bounded summed incident rate, and arbitrary local CPTP action with retained bath. Cardinality alone does not imply the required conflict/coloring constants.
- Initialize in Enc(rho_L) tensor sigma_CB in the dressed frame, with sigma_CB independent of logical input and in all good controller ranges; all passive classical marks start zero. Controller/bath correlations are allowed. Arbitrary reference entanglement with the logical input is allowed. The concrete A0/free/workspace0 state has initial F=I.
- No coherent drift or arbitrary signed perturbation is silently represented as a Poisson event. The reset channels used by the service proof remain actual physical instrument channels.

## 2. Why coefficientwise semantics close the scheduler interface
The full-Hilbert frame removes DATA from all intervening Hamiltonian/no-jump controller maps, including malformed histories. At each actual terminal/reset time the transformed event is an instantaneous bounded-support DATA/controller instrument. The time order of these actual events is therefore a serial order; no controller path or independent schedule is invented.

For an unmarked good terminal, the restricted Kraus operator is K_SSF,s tensor C_h, with C_h controller-only. Its DATA factor acts on the current dressed DATA immediately before that event. Consequently there is no stale syndrome read in this serial representation. Physical work accumulated in the finite-duration prefix is carried by F, not forgotten.

Every owner good projector in this frame is controller-only. If a local Kraus operator K preserves an unmarked good range, expand K=sum_P P_DATA tensor B_P. Applying dual Pauli functionals to (I-P_good) K P_good=0 proves the same range inclusion for every B_P. This is an operator statement, not an expectation or positivity inference. No fictitious Pauli branch can create an unmarked bad controller. Marked jumps and direct kicks may be expanded this way without assigning probabilities to their coefficients.

An induction over actual events now gives each nonzero compatible term: a Pauli error on the encoded state, a retained controller/bath coefficient, good-range conditions for every unmarked owner, and the actual common mark/reset record. At a good syndrome instrument the Pauli term has a definite syndrome, so incompatible outcomes vanish and the remaining correction is a valid accepted SSF step. Controller-only maps change its coefficient, not its logical factor. This proves the S interface needed by D0/D1; a data-independent scheduler law is unnecessary.

## 3. Explicit fault-support/cell map (discharging Q)
Define fixed DATA envelopes:

- D_X for a physical kick on X: DATA projection of X union all frame-factor supports intersecting ORIGINAL X. Set s_d=sup_X |D_X|.
- D_h for a marked terminal/abort at h: its fixed DATA support envelope, contained in the owner's reserved footprint. Set s_e=sup_h |D_h|.

Commuting frame factors ensure there is no iterative support expansion. Fixed physical range, bounded degree and bounded frame incidence imply s_d,s_e are constants. Construct G on DATA by making all check/read footprints AND every D_X and D_h cliques. This last enlargement is necessary: bare physical kick supports alone are insufficient. G still has bounded degree.

For fixed W of size m let

  E(W)={h:D_h intersects W},       |E(W)|<=nu_e m.

Let a block consist of R aligned source windows of width T, tau=RT. The marked-emission cell set is

  V_e(W,b)=E(W) times those R window indices,
  |V_e(W,b)|<=R nu_e m.

It contains every marked emission that can contribute a Pauli fault touching W, even if the actual Pauli support is a strict subset of D_h. Let Y be its raw marked-emission count. The accepted multiplicity theorem gives

  E exp(theta Y)
  <=exp[epsilon (C_A/P)R nu_e m (exp(bP theta)-1)] Tr rho.

Here b is the kick-to-owner multiplicity from that theorem, not the block label. Earlier ancestors of emissions in V_e are retained exactly as in the source theorem; no boundary mark reset is assumed.

Let X(W,b) count physical primitive kicks in the block whose declared dressed envelope D_X intersects W. Bounded geometry and summed incident rates give a finite nu_k such that its mean is at most epsilon nu_k tau m. For example, anchor every physical support at one of its sites; any support whose D_X hits W has its anchor in a fixed-radius neighborhood of W, of cardinality O(m). Summing the incident rate budgets in that neighborhood bounds nu_k. Thus

  E exp(theta X)<=exp[epsilon nu_k tau m(exp(theta)-1)] Tr rho.

Set Q_record=s_d X+s_e Y. It dominates every branch's total DATA fault-support multiplicity touching W. Although X and Y are correlated, Cauchy–Schwarz gives Q exactly with

  H_Q=[nu_k tau+(C_A/P)R nu_e]/2,
  B_Q=2 max(s_d,s_e bP).

All constants are finite and independent of N and the block's location in time. This derivation uses the marked-emission source's equation (3) plus a direct Poisson count, avoiding any implicit extension of owner cells to unspecified direct-kick cell types. Equivalently one may use the source's combined equation (6) after explicitly verifying that anchor assignment.

## 4. Service domination and correlation handling
For every fixed containing hub set H(W), at most h0 m candidates occur in a given deterministic window. The two-half certificate has a full-state CP effect bound for every specified subset, incorporating both real reset shortfall and physical control spoil. Its positive generating-function expansion gives M without independence.

If a Pauli branch's packed candidate remains unresolved, its beneficial syndrome pattern persisted. A witnessed fresh good SSF terminal at that hub would therefore execute an accepted correction and resolve it. Thus actual conservative record misses dominate branch misses simultaneously. At most one packed candidate per hub is essential and is present. Controller-only damage is charged here rather than as fictitious syndrome noise.

The Q and M moments apply to the same real positive record measure, so scalar Cauchy–Schwarz is legitimate for every positive input. Each squared moment scales by Tr rho; the two square roots restore exactly Tr rho. For B=max(B_Q,1) and t=p^(-1/(4B)), the exponent in the corollary is correct. There is no use of ideal hub-clock independence.

Both late-block moments are unconditional from the global initialization. Summing certificates never conditions on past Good, a future witness, or a rare controller record. Thus the absence of a uniform conditional restart theorem is harmless here.

## 5. Backwards chain and all-branch event
The accepted sectorwise D0/D1 theorem applies to the serial Pauli terms just established. Use original incoming representatives for D0's seeds and the original-support component enlargement in D1's ancestral case. Do not use the virtual initial error as a random seed field.

The first cutoff-bad component is connected; the whole-target backward dichotomy produces one chain. Every earlier component meets a target contained in the next slice, so vertical same-DATA edges connect the complete animal. Its volume is at most K_vol times the terminal slice. Initial exact codespace forces termination in a fresh record obstruction. All these steps are branchwise deterministic and require no probabilistic residual distribution.

Existence of ANY failing compatible Pauli branch implies a terminal-event certificate. Each certificate is a measurable event in the actual complete primitive/reset record. Its geometry and terminal window are fixed before applying the uniform tail. Pauli labels, bath Kraus labels, and controller coefficients are not enumerated in the probability bound. The root-site factor N, R window labels, volume animal count, L possible first bad blocks, and final two-sector factor are all charged explicitly.

## 6. CP effect and logical channel conclusion
For a positive-record event E the associated map is CP and trace-nonincreasing. A uniform probability bound Tr I_E(rho)<=a Tr rho implies I_E^*(I)<=a I on the specified initialized domain; equivalently the initialized event map has diamond norm at most a, including references. If a source gives full-Hilbert uniformity, the bound extends further; the logical-memory proof needs only the initialized version.

Event union is a positive CP sum over disjoint record bins (or the corresponding continuous instrument integral). Its effect is dominated by the sum of individual event effects. This justifies the union bound even when reset probabilities depend on DATA. A density at a single exact jump time is never treated as a normalized channel.

Outside the chosen bad-record event all compatible terms in both sectors are restored by the SAME sectorwise syndrome decoder. Stabilizer phases are absorbed into controller/bath coefficients. Hence each corrected Kraus restriction is I_L tensor a coefficient, and after the fixed initial ancillary state and final ancillary trace the good map equals c id_L. This proves logical-input independence of the *good weight* as a consequence, not an assumption about all reset records. The bad map is CP of norm at most delta; trace preservation gives the bound 2 delta. Same-syndrome coherent interference and common bath memory are retained.

## 7. Finite prefixes, gauges, and final decoder
The required mathematical final channel is: apply the full local F^dagger frame, measure full syndrome/use fixed sectorwise R_X R_Z, and decode. The frame is defined on malformed clocks and arbitrary masks, so this handles unfinished clean AND marked transactions at a finite observation time. No eventual-retirement limit or bounded drain deadline is needed. Unretired controller memory remains in the traced ancillary subsystem.

At intermediate analysis boundaries no physical frame change or syndrome recovery is inserted. The evolution stays in the one fixed dressed frame, and replacing a branch Pauli error by a stabilizer-equivalent representative only changes its coefficient by a phase. Controller-only good ranges are unaffected.

For an arbitrary deterministic final time, use completed full blocks plus a final partial block. D0 alone handles a first bad root in the partial block; previous chain steps use full blocks. Its direct/marked mass is dominated by the same fixed full-cell count (or a truncated cell bound). Thus the optional ceil(t/tau) extension does not need a clean completion of pending physical transactions. This remains a statement about an ideal mathematical decoder, not bare physical output.

## 8. Parameter feasibility and exact remaining obligations
Choose R for gamma>1. Use the service source's robust rate bounded below by a fixed positive fraction of its clean rate; choose constant T large enough for reset-shortfall slack. Then choose epsilon small enough for the robust Lyapunov condition, control-spoil slack, and epsilon H_Q slack. The H_Q and B_Q above may be large but are independent of N and elapsed time. There is no contradictory demand that T be simultaneously arbitrarily short and long: epsilon is chosen last.

Within the specified mathematical model, the newly load-bearing composition steps are discharged by this review. The following remain outside it and must not be claimed as solved:

1. Any omitted premise of the reset-first generator or the independently reviewed actual-reset Lyapunov certificate; variants need fresh verification.
2. A concrete numerical threshold, practical local dimension, or experimentally certified reset/monitor hardware.
3. General continuously acting coherent Hamiltonian or signed HP perturbations; the positive Poisson-record proof does not cover them.
4. Efficient final minimum-syndrome computation and a noisy operational implementation of F^dagger/syndrome extraction/logical readout. The separate noiseless-SSF readout candidate has NOT been reviewed here.
5. Fault-tolerant preparation from arbitrary physical input, arbitrary dirty-controller startup, or a claimed stationary marked-owner law.
6. Fixed-dimensional geometric routing at constant encoding rate, thermal equilibrium/passivity, or finite-fuel autonomous lifetime. The accepted locality is the declared bounded-degree interaction graph with maintained reset resources.

No denied access or external mutation occurred. This is a mathematical composition review, not publication acceptance or a novelty claim.

## Final revised-source receipt
I re-read the revised corollary's explicit Q assignment, initialized-domain statement, physical A0/free/workspace0 preparation, geometry premise, and final effect/channel conclusions. The current SHA256 is

  fc9d3f66f8c156a987b3f1137fc2d4a848f937bd77947939517ee71142021446.

Its changes implement the composition qualifications and mass assignment above. The composition verdict applies to this revised version as well. The separate noiseless-SSF readout candidate is still outside this review.
