# Positive local Bell transition test: no protected ancilla through storage
2026-10-29. Supplements and improves THEOREM_v1 section4's physical implementation. The algebraic certificate and all confidence/future-memory caveats are unchanged. Pending review.

For a randomly chosen edge, S=V_i tensor V_j Swap (V_i tensor V_j)† has an orthonormal two-qubit Bell eigenbasis: the twisted singlet has s=−1 and the three twisted triplets have s=+1.

1. Choose one of the four Bell basis vectors uniformly. Prepare it on sites i,j in the known frame, and prepare all other sites in independent fair random computational-basis states. Record only its S eigenvalue s. The unconditional data state is I_D/D; conditional on s, it is the normalized eigenspace projector Π_s/rankΠ_s.
2. Apply the entire physical source channel N (or N_T).
3. Undo the local frame on i,j, perform a Bell-basis measurement on this pair, and record t=−1 for singlet and +1 for any triplet. Record failure iff s≠t.

There is no protected quantum ancilla or reference held through N. Only the input label's classical sign is retained. Each trial uses one random pair, pair-local entangled state preparation, pair-local Bell readout, all other sites maximally mixed via fair random product preparations, and one N call. A standard Bell preparation/readout uses one two-qubit entangling gate plus single-qubit gates, with known-frame rotations added. Pair routing and actual two-qubit calibration remain paid. Source interaction with the selected pair must be the same N as service; input sign records must not independently control the source.

Let Π_s=(I+sS)/2 on the full data array. The input subnormalized ensemble element is Π_s/D. Thus
Pr(s,t)=Tr[Π_t N(Π_s)]/D,
E[st]=Σ_s,t st Tr[Π_t N(Π_s)]/D=Tr[S N(S)]/D,
and
Pr(s≠t)=(1−Tr[S N(S)]/D)/2=δ/2.
This proof requires neither unitality nor an approximate noise model. Measurement degeneracy is handled by preparing the three triplets with equal weights. Selecting s=± with probability1/2 instead would be WRONG: the two eigenspaces have unequal ranks; the correct probabilities are3/4 and1/4. Uniform Bell labels automatically implement them.

Uniform pair sampling gives exactly the q in v1, with its unchanged bound
halfdiamond(twirled learned code,id)≤(D/K)(n−1)q.
The same binomial upper confidence bound applies. Test imperfection still enters as the amplified bias C b_test; absence of long-lived ancilla does not remove calibration requirements. This protocol supersedes the protected-ancilla cost of v1 as the preferred implementation. V1's coherent controlled-SWAP circuit remains a valid alternative and useful mathematical check, not a required interface.

Compared with full logical 2-design validation, this uses only local Bell preparation/readout rather than n-qubit compiled code operations on each test; it retains the polynomial shot penalty. Historical novelty remains unestablished.
