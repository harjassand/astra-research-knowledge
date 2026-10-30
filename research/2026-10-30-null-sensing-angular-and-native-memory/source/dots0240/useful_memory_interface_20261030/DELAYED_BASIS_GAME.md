# A delayed scientific measurement task and its optimal measure-first comparator
2026-10-30. Elementary complete calculation. This is a useful workload for the already-reviewed destructive X/Z readout, not a new readout theorem.

## Task
Let d=2^k. A source chooses b uniformly in {Z,X} and a uniformly in {0,1}^k, then supplies one encoded copy of |a>_b. The X and Z logical bases are mutually unbiased. The basis label b is withheld until after a waiting interval T. The recipient must then output the entire string a.

A quantum memory followed by the existing controlled destructive logical-basis readout wins with probability at least 1-epsilon_T, where epsilon_T is its total operational readout/storage/classical-error budget. With the Tanner memory this can remain small for T exponential in N, k=Theta(N), in its stated model. There is no arbitrary quantum output, magic-state, or universal-gate assumption.

This is the minimal form of a quantum sample archive: decide *which* complementary question to ask only after the sample has waited. It does not permit reconstructing both complementary answers from one sample. The source must supply encoded states; their physical preparation is not solved by restating the game.

## Strong classical alternative: arbitrary quantum measurement before waiting
Grant the competitor an arbitrary global POVM on the full encoded input, unlimited perfect classical storage, and arbitrary perfect processing once b arrives. It need not use a local measurement, a predetermined basis, or an entanglement-breaking state-output interface. Coarse-grain its classical outcomes so y labels its two eventual answers z(y),x(y). Let M_y be its logical POVM effects (an encoding isometry just pulls the physical POVM back).

Its exact success probability is

    P=(1/(2d)) sum_y Tr[M_y (|z(y)><z(y)| + |x(y)><x(y)|)].

The sum of the two rank-one projectors has top eigenvalue 1+1/sqrt(d). Therefore

    P <= (1/(2d))(1+1/sqrt(d)) sum_y Tr M_y
      = (1+1/sqrt(d))/2.                              (1)

This is not the weaker entanglement-breaking average-fidelity comparator, which would wrongly forbid adapting the classical answer to the revealed basis.

## Constructive attainment
Use the real k-qubit Hadamard basis and write <z|x>=s_zx/sqrt(d), s_zx in {+1,-1}. Define

    |psi_zx>=(|z>+s_zx|x>)/sqrt[2(1+1/sqrt(d))],
    M_zx=(1/d)|psi_zx><psi_zx|.

The projector sum equals d I: the two diagonal sums contribute 2d I and the cross sums contribute 2sqrt(d) I before division by 2(1+1/sqrt(d)). Hence the M_zx form a POVM. On outcome (z,x), store that pair and output z if b=Z or x if b=X. Each effect lies in the top eigenspace used in (1), so the bound is attained exactly.

For k=1 this is the familiar intermediate-basis measurement. For large k, even the optimal arbitrary collective measure-first strategy approaches success 1/2, whereas a faithful quantum archive approaches one. The gap is a constant, not an exponential speedup or a universal scientific advantage claim.

## Equal-access scope
- Exactly one input copy; additional copies are a different resource.
- b genuinely arrives later; early basis leakage lets the classical store win perfectly.
- Both sides receive the same encoded input and the same later classical label.
- Classical storage and computation were already granted perfect; the comparison is not a claim that classical hardware is fragile.
- A scheduled quantum fault-tolerant memory wins just as the autonomous memory does. The new architecture's potential value is its waiting/control guarantee, not a new quantum-information separation.
