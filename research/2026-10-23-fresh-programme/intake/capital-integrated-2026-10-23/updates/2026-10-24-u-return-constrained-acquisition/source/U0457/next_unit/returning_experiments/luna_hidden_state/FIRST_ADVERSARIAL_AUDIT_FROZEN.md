# Frozen first adversarial audit: returning discrimination

Scope: audit claims (A) and (B) in `LEAD_OPENING_FROZEN.txt` before fixture work or reading other workers' files. No source hunt, benchmark, or novelty claim.

## Definitions needed for the claims

A possible world at an experimental boundary is a consistent pointed-machine hypothesis together with its current state, written \(\omega=(M,q_0,q)\). Here \(q_0\) is that world's anchor and \(q\) its current state. Let \(V\) be the finite version set. A boundary is returned when \(q\sim_M q_0\) for every \(\omega\in V\), where \(\sim_M\) is equality of all future output traces under all future input words.

For deterministic Mealy machines, behavioral equivalence is a transition congruence: equivalent states emit the same output on each input and transition to equivalent states. Thus running any fixed adaptive input/output tree from a state equivalent to its anchor gives the same transcript as running it from the anchor, and its terminal state remains equivalent to the anchor.

## (A) Common refinement and preservation of access: true under the stated return condition

Suppose \(T\) and \(S\) are finite returning tests valid on the same boundary version set \(V\). Execute \(T\), then restart the controller for \(S\) at its root. On every possible first transcript \(\tau_T\), the surviving set is \(V_{\tau_T}\subseteq V\), and every surviving physical state is equivalent to its own anchor. By the transition-congruence fact, the run of \(S\) now has exactly its anchor-start transcript and returns. So \(T;S\) is returning. Its paired transcript \((\tau_T,\tau_S)\) refines both tests' transcript partitions (the common-refinement claim).

More generally, if a second test is only safe on the version subset reached on a particular first-test branch, choose that test on that branch. The resulting branchwise composition is still a finite returning tree. Shrinking the version set never invalidates an already safe test; the physical state is still at an equivalent anchor. No reset or state label is used.

This proves preservation of the *ability to execute* previously safe returning tests. It does not say that every arbitrary action sequence is safe, or that the machine's complete hidden state is learned.

## (B) Stage count and maximality: correct with the world-count correction

Call a returning test informative on \(V\) if its possible complete transcripts are not all identical; equivalently, it separates at least one pair of candidate worlds. If an informative test has transcript partition \(\{V_\tau\}\), every nonempty block is a proper subset of \(V\): since at least two transcript values occur, no one block contains all candidates. Therefore every possible realized transcript removes at least one world. Any greedy sequence that executes an informative returning test at each successful stage has at most \(|V_0|-1\) successful stages, where \(V_0\) is the initial set of candidate pointed worlds/triples. This is a branchwise bound, not an expected-elimination claim.

The stated \(|H|-1\) bound does **not** follow if \(H\) counts unpointed machines while the initial state is also unknown. A one-machine counterexample: machine \(M\) has states \(A,B\), one input `probe`, output 0 and self-loop at \(A\), output 1 and self-loop at \(B\). The possible anchors are \(A\) and \(B\), with different future traces. The one-step `probe` test is returning in both worlds and distinguishes them. Thus there is one successful stage although \(|H|-1=0\). The corrected bound is \(|V_0|-1\), at most \(\sum_{M\in H}|Q_M|-1\) for the initial-state uncertainty as described. If \(H\) is explicitly redefined to contain pointed machines/worlds, then \(|H|-1\) is the corrected statement.

The terminal claim is maximal only relative to finite safe returning experiments. At a returned boundary, if no finite returning tree on the current \(V_*\) separates worlds with different anchor futures, then no protocol made by concatenating/branching through further returning tests can separate them: compile that finite protocol into one adaptive tree, which is itself returning by (A). Conversely, any pair separable by such a tree is an available discriminator. Since every earlier safe tree remains safe after any returning history, an earlier greedy choice cannot create a dead end that hides a discriminator which a different safe history could reveal. A different history can expose a smaller version set, but its entire finite safe protocol is executable from the current boundary as a tree; if it separated remaining anchor futures, the current set already had a returning discriminator.

The resulting quotient is **safe-test indistinguishability**, not ordinary behavioral equivalence: two worlds with different unrestricted futures may remain if no finite experiment can separate them while guaranteeing return. The stage bound does not bound synthesis time, tree depth, storage, or controller size; those costs remain explicit. A depth-capped search can only report inconclusive when it fails to find a test.

## Boundary

Under the immutable finite deterministic Mealy assumptions and the stated equivalence-based return guarantee, (A) is a closure property and greedy elimination is not pathologically order-dependent at the level of safely distinguishable anchor futures. The only direct mathematical correction found is to count candidate pointed worlds, not merely machines, in (B). The construction itself is finite belief-space/partial-observation synthesis; these observations do not establish a new acquisition method or novelty over that conventional framework.
