# First C mechanism: a learned coherent interface must retain its frame

30 October 2026. Question/phenomenon-first warm-context proposal, not a blind experiment. This mechanism was formed after B supplied the actual N1291 prior scope and before importing a programmable-decoder theorem. B's PGM and root's balanced information-window ideas are separate antecedent attempts, not the mechanism proposed here.

The consequential capability question is LEARN ONCE, then decode an arbitrary late stream of unknown qubits without further source/training access. Jointly processing a training set and a late payload is a different operation from retaining an intrinsic-size decoder program BEFORE the payload arrives. Unknown code orientation may remain a physical information resource even when every payload has intrinsic dimension2.

Consider an ambient space of dimension D>=3 and the native pure-isometry family

    V_j|0>=|0>,  V_j|1>=|j>,  j=1,...,D-1.

An arbitrary offline training protocol, even with unlimited queries, retains a j-dependent quantum/classical program P of dimension d. All j-dependent classical descriptions, control settings and retained ancillas count in P. The online processor Lambda:P tensor C^D -> C^2 is fixed independently of j; work ancillas may be arbitrarily large but start j-independent. No source call, inverse oracle or extra reference state is available after the late payload arrives.

Operative lemma: if every induced qubit channel has Bell entanglement fidelity>=1-epsilon, then with delta=2sqrt(epsilon)+epsilon,

    log d >= (1-2delta)log(D-1)-2log2
               -(1+delta)h(delta/(1+delta)).

For fixed sufficiently small epsilon this is Omega(logD) retained bits/qubits, despite the intrinsic qubit dimension being fixed. The proposed proof uses coherence restoration, complementary leakage and dimension-of-classical-label conditional-entropy continuity, rather than an exact no-programming slogan.

Let a_j,b_j be the Stinespring outputs of the program purification and payload0,j. Writing a=|0>a0+|1>a1,b=|0>b0+|1>b1, Bell fidelity gives

    ||a1||^2+||b0||^2<=2epsilon,
    ||a0-b1||<=2sqrt(epsilon).

The physical environment states for payload0 andj are consequently within half-trace distance delta. With uniform J, the payloadj+program inputs have orthogonal supports, so I(J:BE_1)=log(D-1). Discarding the qubit loses at most2log2. Conditional-entropy continuity on the finite CLASSICAL label J transfers that information to E_0, with no ambient-environment dimension factor. But input0 is fixed, so I(J:E_0)<=I(J:P)<=log d. Mixed program purifications are used only to prove the per-j continuity and are NOT granted as free accessible memory.

There is a tight ordinary construction on this family: one offline query on logical1 and a computational-basis measurement learns j exactly; retain its logD-bit address. An O(logD)-gate reversible linear basis change maps j to the first basis bit while preserving0, hence decodes every future payload exactly with no new source. This is not a new algorithm or an advantage claim; it establishes what ambient frame resource actually pays for reuse.

Strong conventional predecessors to acquire NEXT: approximate no-programming/programmable processors, quantum reference frames and learned isometry inversion. N1291's actual joint-training/late-payload compression may already delimit precisely this issue; it is not contradicted merely by this model. The lemma and source mapping must be paid before a scientific conclusion. If existing machinery already supplies the whole consequence, retire the intrinsic-only streaming claim and choose a better surviving question with B rather than promoting a renamed lower bound.
