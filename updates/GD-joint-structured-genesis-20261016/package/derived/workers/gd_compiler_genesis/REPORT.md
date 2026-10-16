# Compiler genesis result

16 October 2026. Input worktree pin: `2688d7a383502df4fc1e64001d04bb76e6ec05e5`. Status: internally derived conditional mathematics with independent finite checks; external correctness, historical priority and physical qualification remain UNKNOWN.

The strongest receiving gain is a compiler for a **specified small dictionary of correction-element errors**, even when the correction projectors have dense Pauli expansions. A known local operator of norm at most one is the average of two fixed local unitaries. Combining that fact with the direct five-Kraus unitary-pair construction in [PROOFS.md](PROOFS.md) gives

\[
\mathcal D[J+\Delta]-\mathcal D[J]+F
=\sum_e\lambda_e(\Phi_e-\mathrm{Id}),\qquad
\sum_e\lambda_e\le4a\epsilon+\epsilon^2,
\]

where \(a\ge\|J\|\), \(\Delta=\sum_r\delta_rA_r\), the \(A_r\) are fixed known local operators, and the supplied coefficient promise is \(|\delta_r|\le d_r\), \(\epsilon=\sum_rd_r\|A_r\|\). The installed floor and rates are selected before the coefficients. The quadratic \(\epsilon^2\) clock charges the union of the whole error dictionary, which must fit one bounded receiving patch. A separate \(4a\epsilon+2\epsilon^2\) construction preserves each individual pair union when needed. Nontraceless and redundant unitary dictionaries are admitted directly; no hidden identity-to-Hamiltonian gauge change is needed.

For a completed correction element \(J=\sqrt\kappa Q\Pi\), its two unitary terms are explicitly
\(Q[\Pi+i(I-\Pi)]\) and \(Q[\Pi-i(I-\Pi)]\). For a prescribed affine perturbation dictionary with relative coefficient envelope \(\eta\), the sufficient fault-proposal rate is \(\kappa(4\eta+\eta^2)\). Thus a finite list of alternative projector/correction elements can be regularized without the supplied source's generic \(4^k\) Pauli coefficient-conversion factor on a \(k\)-qubit patch. This is a change to the conditional receiving interface, not a claim that those controlled projector phases are cheap or physically available.

For the actual one-mode replacement \(aP\mapsto aP+\delta Q\), \(|\delta|\le\epsilon\), the exact minimax against all fixed CPTP baselines is \(4a\epsilon\) when \(\epsilon\le a\), and \((a+\epsilon)^2\) when \(\epsilon\ge a\). Explicit fixed positive floors and four Kraus operators attain it. This confirms that the general dictionary bound has the sharp small-error linear constant and is within additive \(\epsilon^2\) in that subfamily.

There is also a sharp uniform-rate theorem. For a collision-free Pauli pair catalog, let each correlated pair have \(|z_e|\le M_e\), and let its product Pauli have an independent Hamiltonian coefficient \(|h_e|\le u_e\). “Collision-free” means original labels and listed pair-product labels are all distinct. No commutation hypothesis is needed. Then the exact minimum total rate against **every fixed CPTP baseline** is

\[
\Lambda_*=\sum_e\left(2M_e+2\sqrt{M_e^2+u_e^2}\right).
\]

A fixed product floor of strength \(\sqrt{M_e^2+u_e^2}\) and a four-Kraus union-supported clock attain it. Pauli twirling and two principal-block trace lower bounds prove that even a global baseline or arbitrary same-system CPTP clock decomposition cannot do better. At \(u_e=0\), this proves the supplied \(4M_e\) edge rule globally minimax for this full family. When product drift is present, it improves the separate \(4M_e+2u_e\) accounting. Product collisions and smaller correlated coefficient sets are outside this optimality claim.

## What was added beyond the supplied source

| Supplied capability | New exact or conditional consequence |
| --- | --- |
| Sparse Hermitian-Pauli signed coefficients; four-Kraus Pauli pair clocks | Arbitrary fixed local **unitary** dictionaries, including nontraceless and nonorthogonal terms, with a direct five-Kraus pair clock |
| Generic bounded-body conversion may cost \(4^k\) in coefficient norm | Two-unitary polar dictionary for each **known** operator; \(4a\epsilon+\epsilon^2\) fixed-patch replacement rate without Pauli conversion |
| Sufficient independent edge and Hamiltonian clocks | Joint edge/product-drift clock and exact minimax rate \(2M+2\sqrt{M^2+u^2}\) |
| Exact rate for one completed fixed generator | Aggregate minimax against **all fixed CPTP baselines** for the collision-free uncertainty family; exact actual one-mode affine replacement minimax |

The exact Choi range criterion, identity-shift gauge and compound-Poisson expansion were treated as established ingredients. Reproving them was not the claimed research outcome. The two-unitary lemma is elementary and has no historical novelty claim; its sharper polar form was communicated by the root investigator and independently checked here. Historical priority for the new synthesis and minimax packaging has not been established.

## Receiving and cost boundary

For N881, the actual miscalibrated correction generator plus the installed floor equals the completed ideal correction generator plus independent fixed-rate supported CPTP fault proposals. This is precisely the type of algebraic conversion the receiving argument can use. The universal location-only simultaneous Pauli-history certificate, whole-slab topology, accumulated homology, one fixed decoder and inherited probability theorem remain independent premises. This work does not close those gates or improve their coarse constants.

The relevant geometric charge is the sum of **actual proposal rates whose actual supports intersect each guard**. A small total coefficient bound assigned to a named patch is not enough. The union diameter, patch multiplicity, preparation/correction/readout/reset and positive floor rates remain charged. The installed unitary-kick floor rate for one replacement is at most \(3a\epsilon+\tfrac12\epsilon^2\), in addition to the proposal-rate charge used in the proof.

The dictionary has at most \(2(m+1)\) unitary labels for \(m\) error atoms. Its classical dense polar/spectral construction can cost order \(d_X^3\) arithmetic on a local dimension \(d_X\), and arbitrary unitary implementation can be expensive. The improvement concerns coefficient rate and support, not local-matrix acquisition or gate synthesis. A physical relative-error bound is not acquired here. The supplied numerical coefficients are mathematical inputs only.

An arbitrary norm-bounded unknown operator error does not supply its directions. Our finite checks retain the missing-direction countermodel: one-body Pauli floors with a two-body \(ZZ\) Hamiltonian still fail complete positivity at every tested proposal rate, consistently with the exact range obstruction. Memory-only floors also do not supply interior for arbitrary continuous memory–bath generator errors. Imperfections in the added floor need their own specified treatment.

## Strongest equally informed alternative

Quantum renewal theory already permits a continuous Lindblad generator between Poisson channel events. Vacchini's Eq. (11) gives the semigroup with generator \(L_0+\lambda(\mathcal E-\mathrm{Id})\), and Eq. (14) gives its positive trajectory expansion. This admits continuous Hamiltonian or amplitude-damping drift without our extra floor. [Vacchini, *Quantum renewal processes*, v1, pp. 8–9, Eqs. (11)–(14)](https://arxiv.org/pdf/1906.00693v1).

With the same supplied operator data, that is a strictly serious comparator: it can represent the physical total Lindbladian directly and may need fewer extra physical operations. It does **not** yield the N881 input-independent sparse-fault schedule by itself, because its memory acts continuously between fault locations. A signed replacement difference is also not separately guaranteed to be a Lindbladian. General quantum-jump trajectories retain continuous no-jump evolution and can have state-dependent jump intensities. Transferring them to the given receiver requires a different proof. The present gain is an exact zero-residual-drift sparse CPTP-fault representation after paying a fixed floor; no general simulation or device advantage over renewal dynamics is claimed.

Shifted-jump Hamiltonian engineering is also established: Shang and França's Eq. (4) explicitly expands the jump \(I-i\delta H\), and their Eqs. (19)–(20) discuss Lindblad gauge transformations. These are prior ingredients, not new conclusions here. [Shang and França, arXiv:2604.18533v2, Eqs. (4), (19)–(20)](https://arxiv.org/html/2604.18533v2).

The current N894 interface supplies a different comparator: ideal private fixed-slot toggles can outperform Poisson schedules in its exact singleton parity model. Its time-dependent control class and endpoint guarantee differ from a fixed affine baseline. Its missing general joint-support/finite-width-controller obligations are not solved by the compiler theorem, and N894 does not cover generic signed correction-jump replacements. Neither result establishes an optimal physical memory strategy.

## Checks and receipts

`python3 check_compiler_genesis.py` uses existing NumPy and Python stdlib only. All writes stay in this worker directory; no producer script was executed and no package was installed. [CHECKS.json](CHECKS.json) records:

* Nine dense/rank-deficient/zero polar-dictionary checks in dimensions 2, 4 and 8.
* Twenty-four arbitrary unitary-pair checks, including nontraceless unitaries and boundary coefficients; maximum generator error \(1.67\times10^{-16}\).
* Sixteen signed affine jump replacements using one unchanged fixed floor, including realized zero error; eight unitary labels, \(a=0.6\), \(\epsilon=0.028\), improved rate \(0.067984\), versus pairwise accounting \(0.068768\). The error coefficient matrix is genuinely indefinite in tested cases.
* Twenty joint edge/product-Hamiltonian checks, commuting and anticommuting; boundary Choi trace norms equal the analytic minimax rate.
* Forty-eight actual affine Pauli jump-replacement checks across both minimax regimes, their boundary, zero nominal jump and realized zero error.
* A five-edge graph: improved exact rate \(0.2055164776\), versus separate accounting \(0.236\); full normalized Choi and catalog block agree within \(4.35\times10^{-18}\).
* Eight additional collision-free graph checks with two anticommuting edges verify the general phase convention and full Choi identity; maximum generator error \(4.17\times10^{-17}\).
* The missing-direction control remains negative at proposal rates 1, 10 and 100.

These checks detect sign, conjugation, normalization and singular-case errors. They do not prove the general theorems, historical novelty, physical qualification or useful fault thresholds. General claims rest on the analytic arguments in [PROOFS.md](PROOFS.md). `SOURCE_RECEIPT.json`, `RESOURCE_RECEIPT.json` and `FROZEN.json` preserve the input/output integrity and the exact evidence scope.
