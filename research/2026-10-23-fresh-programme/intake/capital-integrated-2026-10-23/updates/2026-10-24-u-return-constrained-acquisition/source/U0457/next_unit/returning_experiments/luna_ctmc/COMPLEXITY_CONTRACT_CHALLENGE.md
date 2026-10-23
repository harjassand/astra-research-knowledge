# Returning-discriminator existence: PSPACE-hardness challenge

24 October 2026. First bounded challenge, frozen after reading only `LEAD_OPENING_FROZEN.txt`. No opportunity-group procedures, first-failure examples, or other new-unit files were consulted.

## Exact reduction from DFA intersection

Take an instance of DFA-intersection nonemptiness: deterministic automata (D_i=(Q_i,\Sigma,\delta_i,q_i^0,F_i)), (i=1,\ldots,m), and ask whether there is a word accepted by every (D_i). This problem is PSPACE-complete for explicitly represented DFAs.

Construct the known candidate Mealy class with one world (M_{i,b}) for each (i) and bit (b\in\{0,1\}). Its states are (Q_i\cup\{\bot\}), and its hidden anchor is (q_i^0). The action alphabet is (\Sigma\cup\{p,r,s\}), and outputs are bits.

- On (a\in\Sigma), output 0 and transition by (\delta_i).
- On (p), output (b). If the current DFA state is accepting, transition to (q_i^0); otherwise transition to (\bot).
- On (r), output (b) and transition to (\bot).
- On (s), output 1 and transition to (\bot).
- State (\bot) is absorbing and outputs 0 on every action.

The map is polynomial in the DFA input size: there are (2m) candidate machines, each with (|Q_i|+1) states, and a common finite action/output alphabet. The actual machine and its anchor are unknown; the learner sees no state ID. Every ordinary DFA-letter action emits 0, so no observation branch reveals which DFA or DFA state is current.

The anchor futures of (M_{i,0}) and (M_{i,1}) differ: action (r) outputs different bits. The sink is behaviorally different from every anchor because action (s) outputs 0 at the sink and 1 at an anchor.

If a common word (w\in\cap_i L(D_i)) exists, execute (w) then (p). Every candidate world outputs 0 along (w); on (p), bit-0 worlds output 0 and bit-1 worlds output 1, and all transition exactly to their own anchor. This is a finite returning experiment and separates worlds with different anchor futures.

Conversely, consider any informative finite adaptive returning experiment. Before its first occurrence of (p,r,s), all observations are 0, so there is a single common DFA word (w) and no adaptive branch. An (r) or (s) at that point sends every compatible world to the non-equivalent sink, hence cannot be on a valid leaf. If the first special action is (p), its output depends only on (b), not on DFA acceptance. Thus each output branch still contains every (M_{i,b}) at that bit. Any (D_i) rejecting (w) leaves its corresponding still-compatible world in the sink, violating the return requirement on that branch. Consequently every (D_i) must accept (w). Later adaptive actions cannot repair a rejected world because the sink is absorbing.

Therefore an informative finite returning experiment exists iff the DFA intersection is nonempty. This proves PSPACE-hardness even with adaptive observation branches and no actual state oracle. It also shows why the “still-compatible world” clause matters: a rejection observation cannot make the true rejecting world disappear from its own branch.

## Strongest-known boundary and scope

This is a standard hidden-state planning obstruction expressed as a return-constrained partial-observation reachability problem; it does not by itself establish a new learning primitive. For any explicit finite class, belief-space synthesis can enumerate candidate ((\text{world},\text{current state})) sets, update them by action/output, and search the finite reachability game for a finite safe tree. The reduction says this search can be consequentially hard, not that it is impossible or novel. An exact broader complexity classification depends on the encoding of the informative-pair objective and depth cap, and is not claimed here.

The construction preserves all requested contract conditions: candidate machines are explicit; anchors are hidden but specified per hypothesis; outputs do not expose state IDs or DFA acceptance; every compatible world on every branch must satisfy return; and the only assumed “return” is an ordinary transition of the declared machines after a successful (p). No action is named reset, and no teacher or actual-state oracle is used. The complexity result is a first-pass reduction, not a claim of priority or practical advantage over standard belief-game synthesis.
