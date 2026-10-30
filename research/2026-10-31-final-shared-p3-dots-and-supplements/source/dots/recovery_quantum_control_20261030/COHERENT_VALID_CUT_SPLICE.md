# A common-envelope receiver for coherent valid-counter faults

30 October 2026. New local working result, not independently reviewed. This is a semantic bridge for the already-valid event-counter case, not a noisy purge algorithm or an autonomous-computation threshold.

## 1. Exact setting

Use the oriented event-poset clock model in `VALID_CLOCK_CUT_SPLICE.md`: a fixed finite number L of circuit layer types, bounded-degree overlapping-gate graph, and valid lifted cuts satisfying n_g-n_h in {0,1} on each earlier-to-later edge g->h. Every nominal accepted update is the declared channel Phi_h and a counter increment under a serializable full-footprint guard. Rejected updates act as identity. Include Stinespring outputs of channels, resets, and observations in the amplitude description. Disjoint available events commute as system operations; no unmodelled bath evolution is moved through the argument.

Consider one isolated fault at an actual clean transaction cut n. Its counter WRITE support is a set S of s vertices, each component attached to an unchanged boundary. Its actual DATA and workspace support is A. The incoming global counter state is the basis cut n, with arbitrary DATA/bath/reference state. The fault may be any linear superoperator, including a signed coefficient from a global expansion, and may produce coherent superpositions of counter residues and correlations with DATA, bath and reference. It acts on the declared counter/data interface only; no hidden in-flight native prefix is excused.

Let P_valid be the diagonal projector onto output residues satisfying the incident valid-cut constraints. The valid-output coefficient is P_valid E(.) P_valid. This is an analytic coefficient restriction, NOT a proposed physical validity measurement. Invalid-output and valid/invalid cross blocks remain unhandled. The actual task is not certified merely by discarding those terms.

The output comparison is at ONE declared terminal EVENT cut that every retained counter branch actually completes, with its full terminal DATA/dilation ports. Completion may occur at different physical times. The same intended circuit suffix and terminal decoder must apply to every branch. This is a terminal-completion interface, not a theorem of bounded physical completion time. At a fixed physical deadline, branches may have different unfinished frontiers; those additional holes must be counted or bounded separately, and the present conclusion does not automatically apply.

Take counter modulus Q>2(s+1), with the anchoring/lifting qualification of the existing finite-cut lemma. Terminal/initial crossings are included as explicit input/output holes, or excluded by a stated interior-cut qualification.

## 2. One envelope covers every coherent valid output

For every valid basis residue output c, the finite-cut lemma supplies a unique lift n(c), equal to n outside S, with |n(c)_h-n_h|<=s. Consequently the difference between its event down-set and the original down-set lies in

    H(n,S) = {(h,k): h in S, n_h-s < k <= n_h+s}.

There are at most 2s^2 vertices in H. The same envelope works for ALL possible output residues and for both ket and bra. No union over the number Q^s of formal clock states, no worst-case event set over the entire runtime, and no sum of branch norms is needed.

Include every full event tensor incident to H, every actual fault port in A, and any declared finite native transaction halo. For maximal event arity a, the number of elementary tensor legs is bounded by a times 2s^2 plus the separately stated A/halo ports. This count does not depend on global width, elapsed time, Q, or the number of branches. Its constant DOES depend on the true native write/prefix footprint; full read-norm support is not reduced by this statement.

Under the common terminal event-cut completion premise, for each classical output c remove the H envelope rather than only its minimal symmetric difference. Every retained event is then the same intended event in the same event poset. The actual nominal schedule outside the holes is merely a linear extension. Its physical ordering need not match a preselected global time order. At an open hole keep the native temporal ordering and all retained environment links. The result is a common good open network with an arbitrary boundary tensor on H and A. Events removed despite being correct can be reinserted into that boundary tensor. The same good open network therefore applies simultaneously to every c, not a different decoder chosen after observing c.

This is the existing finite-cut splice argument made uniform in its output branch. It does not prove that an arbitrary dirty native prefix is a clean event-poset root. That remains a physical receiving obligation.

## 3. Coherent and signed correctness, without norm amplification

Suppose the actual encoded circuit and ONE fixed retained-output decoder D satisfy the full amplitude identity

    D T_open(B_alpha) V = U tensor W_alpha

for every product matrix-unit assignment to ALL ports of this common envelope, and every allowed syndrome/ancillary input. U is the intended logical isometry. This is the exact common-span premise from the accepted open-tensor lemma, not merely data-only Pauli correctness or correctness on one input.

Expand the counter root and its retained process in any basis of the finite open interface. Every coherent cross block |c><c'| contributes a coefficient tensor C_alpha,beta. Substituting the same amplitude identity on ket and bra yields

    (D tensor id) [T_open * C](V rho V*)
       = U rho U* tensor Gamma_C.

The proof is algebraic and valid for non-CP, non-Hermitian coefficients. There is NO factor counting counter branches and NO open-comb norm conversion. When the coefficient is part of a global inclusive expansion, retain its original closed-map norm estimate. Do not bound the individual matrix-unit coefficients by a triangle inequality.

For a CPTP fault, the valid-valid compression is CP/TNI. Since n is fixed and P_valid is a fixed projector on this interface, its diamond norm cannot exceed that of the root map. For a signed map, left/right projector compression is also completely contractive. This is only a bound on the compressed ROOT; it is not a bound on all unhandled valid-invalid cross terms, and not a new global adaptive-cavity theorem.

If all globally good terms have this SAME logical factorization and the remaining closed bad part B has diamond norm at most delta, the already-reviewed trace-preservation argument gives decoded logical error at most 2 delta. This note supplies a concrete common envelope for valid-counter roots; it does not supply the needed bound on B.

## 4. Why measuring the counter is not the proof

It is tempting to replace a coherent root by a classical random choice of retiming. That is unnecessary and generally invalid. A later arbitrary fault can convert clock coherence into DATA error. The common-envelope proof keeps cross blocks and the bath. Its decoder must correct their whole amplitude span.

Similarly, a channel that is correct on each basis counter label need not be correct on coherent labels unless the retained environment and common decoder satisfy the amplitude identity. A controlled operation can leak logical information to the counter even when a selected marginal looks correct. The algebraic receiver, not a probability interpretation, is what closes the single valid-root case.

## 5. Explicit scope boundaries

1. Invalid clocks, valid/invalid coherences, stale purge state and overlapping repair epochs are excluded. They cannot be made cheap by projecting them away.
2. A fault acting on an entire unanchored component can change its global phase; the anchoring hypothesis cannot be omitted.
3. No event-count argument bounds physical waiting. A valid sloping cut can require a long chain of predecessor increments before a selected next event becomes enabled.
4. Native partial prefixes, mutable gate commands, and classical source bits with repeated fanout are not automatically event-counter roots. They require a real mechanical leading rectangle and bounded semantic write support.
5. Repeated roots do not automatically share this one-root envelope. Their branches may have different incoming cuts. A multi-root theorem needs one common global open network or a proved recursive joining rule.
6. No reduction of the CP cavity exponent from full read support to write support follows. The result is a correctness transfer, not a rarity estimate.
7. Common terminal event-cut completion is essential. A fixed physical-time observation can see branch-dependent unfinished downstream events outside H. The common completed network is not earned by validity alone.
8. Practical threshold, fault-tolerant universal gadget, physical initial preparation and physical decoded quantum output remain separate.

## 6. Comparators and consequence

The mechanism combines the existing valid-cut splice with standard common-correctable-span/retained-syndrome reasoning. It is not a new quantum error-correction principle. Its useful quantitative refinement is that a single coherent valid-counter fault has one output-independent envelope of at most 2s^2 event vertices, so coherent branching does not itself force exponential branch-count norm loss. The remaining high-value target is an actual invalid-epoch controller whose damage can be brought into a comparable common envelope without circular radius/noise constants.

Source interfaces read directly: producer-workspace/VALID_CLOCK_CUT_SPLICE.md; producer-workspace/OPEN_TENSOR_CORRECTNESS_V1.md and OPEN_TENSOR_SCOPE_ADDENDUM.md; producer-workspace/READ_ONLY_CLASSICAL_CLOCK_COMPILER.md. The open-tensor review is local and does not review this new receiver.
