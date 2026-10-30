# Independent narrow audit: read-only clock compilation and maximal-height extension

2026-10-30. Reviewer: `producer-workspace/challenge_live_busy_energy`.

## Verdict

**PASS, with the exact restrictions below.** The revised read-only construction gives nondemolition conservation of classical clock-label sectors under this owner's actual nominal coefficients, including dirty private-hub faults. Its clean SUCCESS implements the promised pinching channel once copies are retained unchanged through the forward payload. A clean inverse-prefix ABORT is identity, not a pinching event. Only the full trace-preserving owner evolution preserves label probabilities; selected/signed branches may reweight them.

**PASS for maximal-relaxation §§1–2:** on a finite component attached to a nonempty frozen boundary, the stated maximal feasible height exists and is reached by finitely many real legal increments. In the specified two-dimensional exterior geometry, the far-sphere boundary has the claimed full-metric Lipschitz property and an exact integer interior extension. The source's §3 single-root accessible-range reduction remains **UNACCEPTED/OPEN**, as its author explicitly states.

Neither ingredient proves physical clock-cluster healing, an asynchronous quantum cut, safe DATA purge/rejoin, bounded active-wire exposure, or a universal architecture. Operator-norm supports remain the FULL physical read footprint. All earlier receipts are unchanged.

### Frozen governing files

- `autonomous_qca_native_bridge_20261030/READ_ONLY_CLASSICAL_CLOCK_COMPILER.md`, SHA-256 `273667e6bfbf3021dfe272ba793a64bc5a13528d43ad38f845ae1be351f28e1c`.
- `autonomous_qca_native_bridge_20261030/MAXIMAL_CLOCK_RELAXATION_EXTENSION.md`, SHA-256 `557a83aa823479fb2fa851ae381e1eca56a556463d92de43414a87f0bd2b86f0`.

Copies are frozen in `reviewed_sources/`. Earlier versions e740c3ee/f376a7ad were NOT the final receipt targets. During review the author preserved those bytes and explicitly added (i) retention of read copies until terminal discard, (ii) nonempty frozen boundary, and then (iii) SUCCESS/ABORT and branchwise-probability distinctions. We checked the revised text, rather than silently assuming these details in the original version.

## A. Read-only clock construction

### A1. Exact finite channel and its physical support

For a read-only clock C_i and a fresh private hub register r_i of the same finite dimension,

    U_i = sum_a P_{i,a} tensor X^a_{r_i}

is unitary and commutes with every P_{i,a}. A controlled Hermitian logarithm can be chosen blockwise, with spectral angles in [-pi,pi], so its norm is at most pi for unit duration. The accepted native Feynman payload edge built from U_i also commutes with these projectors. The construction does not move unknown quantum DATA out of the read-only resource.

Acquiring the FULL read/write footprint first is essential for a clean serializable snapshot. This check uses the accepted ownership/forest compiler, not an early unprotected classical predicate. Fixed finite clock alphabets and footprints give fixed finite hub dimension; they do not give a practical dimension or a source of arbitrarily many free control wires.

In a clean forward payload, preserve the copied labels as unchanged controls and perform the finite table computation in additional hub workspace. Every finite controlled operation on the declared write set W can be synthesized by the existing local unitary/Stinespring construction. The clocks in W can be pinched and rewritten by that finite channel. At the terminal, discarding the preserved read copies removes all cross terms between distinct read-label vectors. More explicitly, the clean completed channel has Kraus operators of the form

    K_{a,mu} = P_a^{read} tensor V_{a,mu}^{write},

with a complete conditional channel on the write registers. The terminal erasure/discard is physically an onsite hub reset in the accepted compiler, not a new continuous ideal dephaser.

Retaining the copy is load-bearing. If the sole copy is SWAPped into a writable register and the now-zero private copy is discarded, a coherent read input can remain entangled with the writable output. The resulting JOINT output is not pinched in the read clock. Our explicit q=3 diagnostic leaves a read cross-block of norm 1/3 in that invalid implementation. The revised source rules it out.

On a clean ABORT, reverse the entire prefix including the copies before discarding private workspace. This restores the original coherent read input and implements identity. It does not pinch. Thus only a clean completed SUCCESS of the specified channel is the asserted pinching event. The source now says this explicitly.

### A2. Full-Hilbert invariant-sector proof

For this owner's generator, every coefficient has one of the following forms on a read-only clock:

- a controlled copy/inverse, hence diagonal in its clock label;
- a hub-local operation or reset, hence identity on that clock;
- an owner/tag mask, failed-test coefficient, tag cleanup, or monitor, acting on independent tag/controller factors or diagonally in the clock label.

Therefore `[H_h,P_{i,a}]=[J_{h,s},P_{i,a}]=0`. For a Lindblad summand,

    D_J^*(P) = J^dagger P J - (J^dagger J P + P J^dagger J)/2 = 0,

and the Hamiltonian contribution vanishes. Summing gives `L_h^*(P_{i,a})=0` on the full Hilbert space, without any clean-prefix or diagonal-state assumption. Malformed ownership or clock masks can suppress an edge or cause an actual abort/dirty reset, but cannot change a controlled read into a label-writing matrix element.

An arbitrary operator or completely bounded map supported on the private hub/workspace (and a retained bath, if relevant) acts as identity on the read clock. Its composition with the nominal h-evolution obeys the read-sector bimodule identity

    Phi(P_a X P_b) = P_a Phi(X) P_b.

For nominal Kraus/instrument branches this follows directly from commutation; arbitrary hub-supported linear insertions preserve the same identity. Consequently a state block-diagonal in a read-only clock remains so, and no source label sector is transferred to another one. This remains true with arbitrary DATA/reference/bath correlations in each block.

For the full CPTP h-evolution, the projectors are fixed by the adjoint, so probabilities are preserved. A selected Kraus/retirement branch has only `K^dagger P K = P K^dagger K`; it can have label-dependent success weight. Signed insertions likewise have no branchwise probability interpretation. Such reweighting is explicitly permitted. We do not infer independent clock histories or erase retained correlations.

This is a statement about h and its private fault insertions. Other legitimate owners may later write these clocks, and future bath interactions may spread faults. Their effects require the separate controller/causal analysis; they are not forbidden by h's conserved algebra.

### A3. Semantic support is not norm support

Within a supplied valid classical/quantum transaction cut, the owner's dirty retirement can write classical labels only in W and act on quantum DATA only in its declared DATA-write footprint. Its dependence on read labels, read-clock phases, and retained bath correlations can still involve all of R. Thus one may charge a small CLOCK-WRITE set for the stated semantic purpose, but one may not replace R by W in the cavity derivative, locality, norm-incidence, or witness-support calculations.

An off-diagonal clock fault directly touching a resource remains charged there. Conditioning on it does not create off-diagonal blocks at other initially diagonal read clocks, but no rule here proves that arbitrary dirty clock configurations admit the needed global classical history or a quantum-safe rejoin. The full read-only conservation algebra alone cannot establish that cut.

Actual new service constants or witness supports for a substantially modified machine would still need their actual finite alphabet/monitor substitution. This receipt grants no old numerical service constants to the new repair controller.

## B. Maximal ordinary relaxation on a finite attached component

Let C be a finite connected component of unfrozen vertices, and require a NONEMPTY frozen boundary. The initial integer h is feasible on edges in C and on edges C--F. No condition is imposed on edges wholly in F. Every boundary value c_v and every path in d_C is fixed as in the source.

For any feasible height g and any path to a frozen v,

    g(x) <= c_v + path_length.

Taking the infimum gives `g(x)<=u(x)`. Every boundary is reachable in finite C, so u is finite and integer. Triangle inequalities for d_C along interior edges imply `|u(x)-u(y)|<=1`. On a boundary edge x--v,

    u(x) <= c_v+1,
    u(x) >= h(x) >= c_v-1.

Thus u is feasible. Combined with the preceding universal upper bound, u is the GREATEST feasible extension, not merely a convenient target above the particular initial h.

Suppose a vertex x has positive integer deficit `u(x)-h(x)>=1`. If it has a strictly lower neighbor y inside C, initial feasibility forces `h(y)=h(x)-1`, while

    u(y) >= u(x)-1 >= h(x) > h(y),

so y also has positive deficit. A lower frozen neighbor cannot occur: for a boundary neighbor v, positive deficit and `u(x)<=c_v+1` imply `h(x)<=c_v`. Following strictly decreasing h therefore stays within C and reaches a local minimum that still has positive deficit.

At that local minimum, `h(x)<=h(y)` for all neighbors. Increasing h(x) by one preserves every incident Lipschitz constraint, since the pre-update differences were in {0,1}; and it stays below u because its deficit was positive. This is a genuine legal ordinary increment, not a simultaneous reset or a hypothetical unpriced transition.

Every legal increment decreases the nonnegative integer potential

    Phi(h)=sum_{x in C}(u(x)-h(x))

by exactly one. Any maximal sequence of real legal increments, with no permanent refusal to perform available updates, terminates at u after exactly Phi(h_initial) increments. The argument does not set a physical clock-time bound, assume a scheduler, or discard the DATA channel associated with each increment.

If a component has no frozen/fixed boundary, arbitrary uniform height shifts remain feasible and no finite greatest extension exists. That counterexample is why the revised source explicitly excludes it.

For O(M^2) vertices, the advertised O(M^3) count requires `max_x(u(x)-h(x))=O(M)`. This follows, for example, from a regular neighborhood with relevant distance/diameter O(M) and current/boundary height span O(M). Cardinality O(M^2) ALONE does not bound a graph's diameter or the height deficit. This is the precise interpretation of the source's height-range premise; no stronger complexity bound is certified.

Modulo clocks require the separately stated consistent lifts and sufficient alphabet range for the entire motion. An arbitrary phase defect or winding cycle cannot be assigned a convenient lift by this lemma.

## C. Far-sphere extension in Z^2

Let nonempty finite F be inside the L1 ball B_a. Use the unbounded component of its complement and only accessible frozen boundary values, of range `D=c_max-c_min`. Every x in S_R for R>a is in that exterior component.

For any path from x to F, its length is at least R-a, so

    u(x) >= R-a+c_min.

Choose any frozen point and a shortest lattice path toward it. Until its first contact with F this path lies in the exterior: it starts outside B_a and has not crossed F. The contacted boundary point is accessible and the path length is at most R+a. Hence

    u(x) <= R+a+c_max.

Therefore the total range of u on S_R is at most D+2a. Take `R>D+3a`. For x,y in S_R:

- If `|x-y|_1>=D+2a`, the range bound gives the desired Lipschitz inequality directly.
- If `|x-y|_1<D+2a`, every vertex z on a shortest path satisfies `|z|_1>=R-|x-y|_1>a`. This whole path avoids B_a, hence F, and is in the exterior. Summing the ordinary edge Lipschitz inequalities for u along it gives `|u(x)-u(y)|<=|x-y|_1`.

Thus the restriction to S_R is Lipschitz in the FULL lattice metric, not just the punctured graph's metric. The integer function

    U(z)=min_{x in S_R}(u(x)+|z-x|_1)

is 1-Lipschitz, as a minimum of common-Lipschitz distance cones. On S_R, the full-metric inequality supplies `u(x)+|z-x|_1>=u(z)`, while choosing x=z gives equality. Hence U matches u on the sphere and extends it throughout B_R. No target values inside F are preserved; this is an interior replacement, not proof that an arbitrary incorrect frozen root must be retained.

The extension is a concrete finite geometry result. Neither its existence nor a finite relaxation count supplies physical permission to replace unknown nearby DATA, a safe order for all actual writes, or a probability bound for obtaining the required uninterrupted relaxation interval.

## D. Deliberately unreviewed/open seams

The following source qualifications remain governing:

1. Maximal-relaxation §3 only motivates an O(1) accessible boundary range from a single native clock-root footprint. Its arbitrary-footprint and shrinking-frozen-set case analysis has not been supplied and is NOT accepted here.
2. Multiple roots require a noncircular radius/range/damage-count theorem. The geometric single-boundary result is not that theorem.
3. A prescribed relaxation sequence needs actual native service and a real gap between repair attempts, including already active repair owners. A slow rate or a mean waiting time alone is insufficient.
4. Every ordinary increment applies its associated DATA operation. The proof is not permission to advance only clocks. A quantum cut, local purge/rejoin, and protected active-wire waiting remain open.
5. A controller that writes a large repair ball has that large semantic write footprint. Nondemolition reads do not shrink actual write sets, and splitting a large untrusted plan into small writes requires a separate safe protocol.

No new frontier/fill source was silently incorporated into this review.

## E. Diagnostics

`check_independent.py` independently checks a q=3 read/copy/write system with arbitrary dirty hub unitary. Sector commutators vanish and the full CPTP read-population error is `7.69e-16`; the selected branch is demonstrably not trace preserving. The invalid last-copy-transfer implementation leaves read cross-block norm 1/3, while the valid clean terminal has zero cross blocks.

The same script checks 150 random attached finite graphs, reaching their maximal u in exactly the initial total deficit (778 real legal increments overall), plus 24 punctured-lattice sphere/interior-extension cases with no violated edge or full-metric inequality. These finite checks illustrate the proofs; they are not native Hamiltonian simulations, service estimates, or an asynchronous threshold.
