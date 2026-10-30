# Full nominal raw exponential inequality for the actual native LOCC machine
2026-10-30. Independent construction from the compiled gates. Candidate for exact-source review; not a continuous-noise threshold or useful-rate theorem.

## Result

For the concrete native machine accepted in `native_locc_rollback_integration_20261030`, define the ACTUAL phase-controlled false-token count D and actual mechanical history defects B_h in its exact forest frame. There are fixed finite weights R_t,R_A,R_B such that

    E = U + R_t D + R_A sum_(Alice h) B_h + R_B sum_(Bob h) B_h,
    V = exp(s E),       s>0,
    L_nominal^*(V) <= 0                                      (1)

on the FULL Hilbert space, not merely on good histories or classical mixtures. The complete terminal good/dirty cross blocks vanish for the ACTUAL full gate circuit. Arbitrary partial dirty gates need not normalize the syndrome algebra; their reset gains are instead paid by the actual healed mechanical defect.

This establishes a nominal raw operator supermartingale with explicit endpoint charges. It supplies no volume-uniform useful correction rate and does not turn a Poisson-record theorem into continuous-noise control.

## 1. Governing physical sources and exact erasure convention

Use the five governing files and frozen hashes in the accepted stochastic-native directory's SHA256SUMS.txt. In particular the payload is exactly EXPLICIT_LOCAL_PAYLOAD_GATES.md, not an arbitrary Stinespring completion. The root proposal/ledger are motivation; the proof below rederives their claim from these gates and transitions.

Every classically overwritten input register is included among the resolved source labels. Thus an Alice terminal overwriting an arbitrary old worker v has Kraus channels indexed by `(workspace output w, erased program p, old worker v)`, with destination HOLD(DATA(y(w))). A Bob terminal resetting the master to FLUSH_SEND(0) resolves its old master/cache labels as well as erased W,P. All labels within a bundled source have the same rate. Summing them gives the actual scalar complete source loss. Registers that are retained, e.g. P at commitment, have identity rather than erasure on them.

This is the complete source-resolved reset convention already required by the machine. It is load-bearing here: a coherently summed eraser or overwriting an unknown classical value without its complete source labels is not the same instrument. Quantum communication is never added; all interparty transitions remain measured classical transport.

## 2. Energy algebra and finite local ranges

U is the reviewed relative Tanner integer potential, summed over the applicable CSS sectors. It is a sum of bounded local functions of the RAW Alice/Bob stabilizer syndromes, not a function merely of their unary energy values. All stabilizers commute. Let B_h=I-G_h be the actual mechanical history projector: in the forest frame G_h is DATA-independent and requires the relevant clock/tag consistency and W_h=0. R leaves have G_h=0; a Q0 output with W=0 is always good. Other owners' mechanical flags are unchanged by a complete h retirement.

For each DATA-valued reply, Alice HOLD, Bob WANT cache, or Bob ACTIVE program, define a false-value projector comparing its actual a with the CURRENT Alice raw checks requested by that hub. Programs are active precisely in A/C/B and R(parent=A/C/B); they are inactive in I/Q and R(parent=I/Q). ACK/empty/request slots carry no value token. Let D be the sum over these physical token projectors, not their OR. Program validity uses the engine phase even if outer control is malformed.

These projectors, U and all B_h commute in the forest frame. They are honest bounded-support observables. Conjugating the whole family by the accepted product forest frame preserves commutation and enlarges supports only by a fixed radius. No measurement of these analytical observables is added.

For an h retirement, let U_loc,h collect every local energy term whose physical DATA support it may affect. Choose K_A,K_B bounding its spectral range, uniformly over owner masks and partial prefixes. This can be the sum of the ranges of all possibly touched local terms. The fixed footprint and bounded incidence make it finite independent of N. It is also an upper bound on a clean wrong-program Pauli's increase of U; use a larger common bound if needed.

Let J_A bound the number of existing token comparisons whose Alice stabilizer supports can meet an Alice retirement's possible DATA footprint, plus its one possible newly written held token. All finite FIFO, held, WANT and phase-valid P locations are counted. Fixed degree and finite capacities make J_A finite. Bob resets cannot create any Alice-value comparison elsewhere: they leave Alice DATA unchanged, and can only delete their own cache/program tokens.

Choose

    R_t > K_B,       R_B > K_B,
    R_A > K_A + R_t J_A.                               (2)

The bounds below are deliberately conservative. No practical weight or threshold size is claimed.

## 3. Exact full-payload label map on arbitrary workspace inputs

Write sigma_A,sigma_B for the COMPLETE raw stabilizer eigenvalue strings, including checks outside the locally measured list. Let r_h(sigma) be the m-bit restriction measured by h. Syndrome eigenspaces may have large logical/gauge degeneracy; no logical computational basis is assumed.

### Alice

The actual circuit for a stabilizer S_j is H_(b_j), controlled-S_j assembled resource by resource, H_(b_j). On every S_j eigenspace, including arbitrary b_j input, it is exactly X_(b_j)^(r_j). Thus the FULL completed Alice unitary is

    |sigma_A; b> -> |sigma_A; b XOR r_h(sigma_A)>,       (3)

with identity on the syndrome-sector degeneracy. Sequential checks commute, so (3) holds jointly for all m syndrome bits. The pointer y is the final computational b value. It is not an inaccessible environment outcome.

### Bob

Let b be the m-bit syndrome workspace, c the 2k-bit correction-mask workspace, and a the immutable program. Define

    b' = b XOR r_h(sigma_B),
    c' = c XOR enc[f_h(a XOR b')].

The table is the explicit onsite permutation given in the compiled source; it is defined for every initial c, not only c=0. The actual workspace-controlled physical Pauli mask c' transforms the COMPLETE raw Bob syndrome by its fixed XOR delta(c'). Hence the full completed map on labels is

    (sigma_B,b,c,a) -> (sigma_B XOR delta(c'), b', c', a).  (4)

Within a syndrome sector the Pauli may act nontrivially on logical degeneracy and phases. This does not affect any observable in the raw-syndrome/workspace/program diagonal algebra. The map on labels is invertible: recover sigma_B by XOR delta(c'), then b=b' XOR r_h(sigma_B), then c=c' XOR enc[f_h(a XOR b')]. Actual realizability constraints on global syndromes are preserved by physical Pauli operators; no invalid syndrome sector is required.

Equations (3)-(4) prove that the FULL actual circuits normalize the abelian algebra generated by ALL raw stabilizer projectors and all computational W/P labels. Retaining the entire m+2k Bob workspace until terminal erasure is essential. A prematurely discarded scratch register would not be this unitary and would require a new proof.

## 4. Complete terminal cross-block cancellation

Fix a terminal source clock and actual ownership-label block. If ownership is incomplete, the whole source is mechanically bad, so there is no good/bad cross block to combine.

For full ownership the terminal forest unitary is exactly the full circuit (3) or (4), and the good source is G=|0><0|_W (P unrestricted). After complete reset the output has W/P zero, Q0 and the specified classical pointer/master state. Pull its output weight V back through this overwrite. Before conjugating by the full circuit, the pulled weight is diagonal in:

- all raw Alice/Bob stabilizer projectors;
- final workspace computational labels, including Alice y(b);
- retained/erased classical source values;
- all other mechanical flags and ownership labels.

The other mechanical flags are DATA-independent and unaffected. By (3)-(4), conjugation keeps this algebra diagonal in INPUT W/P labels. Therefore

    G Phi_terminal^*(V) (I-G) = 0.                    (5)

V itself commutes G, so the terminal decrement is exactly block diagonal good/bad. Mask blocks have no cross terms because the reset, its controlled forest unitary and V preserve the actual ownership labels. Erased program/old-master/worker labels are fully resolved; retained ones are diagonal spectators or explicit permutation controls.

At B_(j0,0) the forest frame is I for every mask. Its complete reset has no W-good/W-bad cross term directly. Every R leaf is wholly bad; its arbitrary partial forest unitary needs no normalization. All I/A/Q source frames are identity. Thus (5) covers the only potentially dangerous mixed terminal source, without falsely applying it to intermediate prefixes.

## 5. Mechanically clean sources

These are exact commuting-label source/target inequalities, not a claim about independent classical syndrome probabilities.

- Clean Alice SUCCESS leaves every raw Alice stabilizer unchanged and writes its true current value. It may overwrite an older false held token, never create one. U and all other token comparisons are unchanged.
- Clean Bob SUCCESS with true P is the ordinary GPT move on the CURRENT relative syndrome and never raises U. Its program token was true; any simultaneous malformed WANT token may additionally be discarded.
- Clean Bob SUCCESS with false P raises U by at most K_B and deletes that false program token. All other Alice comparisons are unchanged. Therefore its V ratio is at most exp[-s(R_t-K_B)].
- Clean B0 rollback is DATA identity even with false P; its program deletion gives ratio at most exp(-s R_t) when P is false.
- LOAD I+WANT(a)->A0+BUSY copies a into the active program and consumes WANT. The old idle P was NOT a token. False count is preserved exactly, while W reset can only heal a mechanical defect.
- COMMIT A_k->C0 preserves P and its validity, resets W and preserves the identical ownership consistency predicate. READY Qk->I has no active P at either endpoint. REFRESH in I/A/Q preserves an active A program and only heals W.
- Nonprefix I/A/Q watchdog retirement has identity DATA frame, deletes any active A program/cache and sets universally good Q0.
- PREFIX C->B watchdog preserves the identical prefix, active P and mechanical status; resetting outer control to DRAIN can only discard a cache token. No DATA is changed in the forest frame.

For mechanically clean Bob C_L define F_P as the false-program projector, and Q_imp as its true-program strictly improving GPT source projector. Then its normalized gain obeys the sharper block bounds with ratios exp[-s(R_t-K_B)] on F_P and at most exp(-s) on Q_imp. The latter uses the integer U decrease; extra token deletion only helps.

## 6. Dirty source envelope without monomiality

Let P_b be an actual wholly bad source block for a complete T_h, including W!=0 in a consistent full terminal or every W in an inconsistent/abort source. T_h clears its own B_h, changes no other B_g, and has complete scalar source intensity. Factor out every unaffected commuting energy/token/history term; their exponentials commute through every Kraus leg.

For Bob, after subtracting a common lower local-U bound, the affected output weight is at most exp(s K_B), while the source has its factor exp(s R_B), and its old program/cache false debt is nonnegative. Bob creates no new token. Positivity and completeness give

    P_b Phi_h^*(V) P_b <= exp[-s(R_B-K_B)] P_b V.       (6)

For Alice include every possibly changed token comparison and the new held token in a set of size <=J_A. Its total output local weight is at most exp[s(K_A+R_t J_A)], whereas source weight is at least exp(s R_A). Thus

    P_b Phi_h^*(V) P_b
       <= exp[-s(R_A-K_A-R_t J_A)] P_b V.               (7)

These are Loewner inequalities on arbitrary DATA/W/program/retained-reference states. They do not assume that a partial prefix maps raw syndromes deterministically. Source/target local minima/maxima are uniform over every realizable exterior block; using the sum of all touched term ranges is safe even when syndrome constraints correlate local and exterior labels.

Non-T data-free resets that merely preserve/heal B do not need (6)-(7). They preserve all unchanged labels and can only lower mechanical/token debt, so their complete reset adjoints are nonincreasing directly. Their losses are retained.

## 7. Hamiltonians, all classical transitions and actual Lindblad losses

The forest Hamiltonian is DATA identity. It preserves mechanical flags, immutable program values, phase-controlled program validity and all classical packet values. Acquisition stays A, gates stay C, rollback stays B, Q verification stays Q, and an R leaf inherits its parent's validity. Cleanup does not change the clock. Therefore [H_nom,E]=0 term by term, including malformed masks. The finite monitors resolve only clock/lock labels and have no DATA/W dependence; they commute E or give zero drift on it.

Every classical measured transition is source-basis resolved and either moves the SAME value while emptying its source, or discards it. The raw syndrome is untouched. This includes malformed C+READ_WAIT: receiving DATA creates WANT while consuming the FIFO value, and the preexisting phase-valid P remains a separate token. Nothing is cloned. FIFO shifts likewise move-and-consume. Source effects are diagonal in the same energy algebra. The finite queue alphabet contains only actual legal encodings; no undefined unused code word is being treated as harmless.

For a complete quantum reset bundle, the loss is kappa P_source tensor I_erased. In the forest frame unitarity preserves this complete loss. It commutes V, so its dissipator is

    kappa [Phi_source^*(V) - P_source V].              (8)

Individual fine workspace outcomes need not obey (8) separately in a dirty partial prefix; the complete equal-rate bundle is what is proved. This is why keeping the real separate channels and summing their actual gains/losses matters.

Combine (5) with the clean bounds and (6)-(7), then sum (8) over all bundles. Other jumps are nonincreasing and Hamiltonians contribute zero. This proves (1). More explicitly, retaining only some available charges,

    L_nominal^* V
      <= -sum_(dirty T sources b) kappa_b (1-exp[-s delta_type(b)]) P_b V
         -sum_(Bob terminal h) kappa_h (1-exp[-s(R_t-K_B)]) G_h^T F_P V
         -sum_(Bob terminal h) kappa_h (1-exp[-s]) Q_imp,h V,

with delta_B=R_B-K_B and delta_A=R_A-K_A-R_t J_A. Each displayed charge is positive because its projector commutes V. Additional clean token-discard, workspace-healing and correct-move charges have only been omitted, not replaced by zero-cost faults.

## 8. Full-workspace regression and a useful negative result

`check_raw_terminal_envelope.py` uses actual H/controlled-Pauli/table/correction gates for commuting XX/ZZ, retaining EVERY workspace input column. It checks 16 Bob full-ownership sources, 48 Bob malformed-mask sources, 60 Alice full sources with old/new tokens, 180 Alice malformed-mask sources and 144 dirty partial-abort sources. Weights are R_t=3,R_B=3,R_A=12, J_A=3, s=0.17.

Minimum source-minus-gain eigenvalue is -6.42e-15 (numerical roundoff). Maximum good/dirty full-terminal cross norm is 4.28e-16. Full label maps are bijective; maximum unitary error is 8.89e-15.

The dirty PREFIX cross norm reaches 2.29. Thus partial circuits genuinely do not satisfy the terminal cancellation, and falsely extending the normalizer argument to them would fail. Their entirely bad source envelope is essential. These finite tests support the gate algebra but do not replace the general proof or establish a useful-rate/noisy theorem.

## 9. What is still missing

The strict charges above exist only at actual consuming/healing/improving source phases. A false token can wait in a channel, a dirty engine can be far from retirement, and an active code correction can be blocked in acquisition. To absorb arbitrary weak continuous joint noise one still needs local, positive, phase-aware CP credits or another explicitly proved uniform useful-drift mechanism. A bounded lifetime in a classical Poisson-root construction is not that mechanism.

No generic continuous-noise result, arbitrary dirty initialization, bare-output claim, or practical threshold follows from (1) alone. All previous stochastic sources and their independent acceptance are unchanged. This is a new nominal operator lemma to be audited on its own.
