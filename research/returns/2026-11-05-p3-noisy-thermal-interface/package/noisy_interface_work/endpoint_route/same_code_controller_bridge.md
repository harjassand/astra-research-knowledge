# A controller-closed interface and local-stochastic fanout in one code

This is the final implementation bridge. It replaces the earlier suggestion to combine CFG's concrete code with a separate measurement-free Bacon–Shor controller. No ideal mutable classical controller is used, and no noisy coherent byproduct control touches the fresh output Bell half.

## 1. A single existing measurement-free computational scheme

Use Aharonov and Ben-Or, *Fault-Tolerant Quantum Computation With Constant Error Rate*, primary full text https://arxiv.org/pdf/quant-ph/9906129 . Its §4, Theorem 4 constructs quantum procedures for a finite native gate set, including all syndrome processing, without measurements or classical operations during computation. The native gates are NOT, CNOT, S, controlled Z, H, Toffoli, SWAP, preparation of zero, and discard. All bounded-arity operations, including idle, preparation and any final measurement, have fixed independent stochastic Pauli faults in the present specialization. No classical arithmetic or decoder is exempted from noise.

One can choose an explicit fixed CSS base code rather than leave existence of sufficient distance implicit. Take the binary Reed–Muller code RM(5,11), evaluating degree-at-most-five Boolean polynomials on 2^11 points. It has length 2048, dimension 1024, and distance 64. It is self-dual: products of two generator monomials have degree at most ten, so their evaluation inner products vanish over F2, and the dimension is half the length. It is doubly even: generator weights are multiples of four and pairwise overlaps are even. Puncture one coordinate and take C2=C1-perp inside C1. The resulting one-qubit CSS code has length 2047 and distance at least 63, so corrects 31 errors. The distance claim follows by the usual elementary induction f(x,t)=g(x)+t h(x): when h is nonzero, wt(g)+wt(g+h) is at least wt(h), and when h is zero the weight doubles.

AB Theorem 4 bounds the spread of each procedure by four. Conservatively, a gate procedure preceded by one error-correction procedure has spread at most 16. The chosen base code therefore has enough correction margin. The important point is that all these constants are fixed; this deliberately conservative base code and its controller circuits can be extremely expensive.

Let A be an upper bound on the number of native locations in one fixed rectangle, including its coherent controller and idles. Recursively define a level-r rectangle as good when at most one of its level-(r-1) subrectangles is bad. Under independent physical faults, with p0=p,

\[
p_{r+1}\le a p_r^2,\qquad a=\binom A2.
\]

For ap<=1/2,

\[
p_r\le p(ap)^{2^r-1},\qquad \sum_{r\ge0}p_r\le2p.
\tag{1}
\]

AB §7, Lemma 8 is the required correctness and validity statement: sparse faults preserve the intended logical evolution on every suitably sparse-correctable incoming state, and a good correction stage maps an arbitrary incoming state into the many-to-one protected code. Its proof includes arbitrary incoming density matrices, not just freshly prepared codewords. Define the virtual syndrome/gauge subsystem to contain these correctable deviations. The margin and spread above fix the sparse class once and for all.

The many-to-one algebra in CFG arXiv:2408.05260 applies to any such representation. In particular, a channel that exactly implements a logical unitary has virtual form that unitary tensor a syndrome channel; exact pure logical preparation factors from syndrome; an exact destructive logical measurement traces its syndrome. These are code-independent statements proved using Stinespring uniqueness/purity. Their use here does not transfer CFG's measured-controller implementation to the AB code.

## 2. Actual quantum interfaces in that same scheme

Fix a constant-size Clifford encoding circuit E_C for the chosen CSS code. Fix a constant-size ideal decoder D_C consisting of coherent recovery followed by the inverse Clifford encoding and discarding the nonlogical registers. Both are finite circuits in the same native gate set; their size is a fixed constant even if enormous. These are ideal target circuits to be compiled, not ideal physical devices.

To construct the stage Gamma_(r,r+1), replace each gate of E_C by its level-r AB rectangle and finish with the level-(r+1) correction. For Gamma_(r+1,r), first correct its child blocks at level r and then execute the level-r simulation of D_C. This is the explicit adjacent-level construction in CFG Appendix C.2, applied to the AB rectangle representation itself, with its fixed spread parameter. No change of control model or code occurs.

A stage contains at most g level-r rectangles, for a fixed finite g. When all those rectangles are good, the stage is logically correct on **every** allowed incoming syndrome state. A faulty child block is corrected into the lower-level many-to-one code; its residual logical error is confined to that child, and the outer base decoder corrects the allowed sparse set of such children. Thus the stage has an input-independent bad-fault tag of probability at most g p_r.

Composing the stages from level L down to the raw qubit gives a complete output interface whose bad tag has probability

\[
q_{\rm out}\le g\sum_{r=0}^{L-1}p_r\le2gp.
\tag{2}
\]

Off that tag it decodes the correct logical qubit for every syndrome. The analogous upward interface preserves the unknown input, including arbitrary entanglement, except on a tag of probability O(p). Its final protected-code leakage is bounded by the bad probability of the last high-level correction, so can be made arbitrarily small. The O(p) input corruption remains as an encoded logical boundary channel, not an unencoded invalid state handed to an ideal encoder.

All schedules are finite, deterministic and padded. Bottom controller gadgets are fixed finite circuits. There is no call to a growing classical computation while a bare qubit waits. Higher-level waits are corrected at the corresponding code level and counted in the protected workload.

## 3. Protected Bell fanout to raw local-stochastic copies

Start from the incoming encoded data D and an independently prepared encoded Bell resource A,B. Perform the protected logical Bell-basis unitary (CNOT followed by H) on D,A. Copy each of the resulting two logical Z bits into M freshly prepared logical-zero blocks using a protected binary CNOT tree. Discard D,A. **No gate in this fanout or its controller touches B.**

Choose the concatenation level so the total probability of bad high-level rectangles in preparation, Bell transform, fanout and protected waits is at most epsilon. Replace bad high-level paths by their exact logical counterparts in a hybrid comparison. Keep each path's original probability; do not condition on global success. The comparison logical copy pool is |b>^M, conditional on the relevant Bell bit b. All pool syndrome systems can be arbitrarily correlated with one another, with B's syndrome, and with old retained records. The Bell outcomes themselves are the usual uniform logical outcomes.

Independently apply Gamma_(L,0) to each copy and measure Z. Include the physical measurement fault in that copy's bad tag. These M descent circuits have disjoint fault variables. Their actual wrong-bit set W is contained in their bad-tag set, and therefore

\[
\Pr[S\subseteq W]\le q^{|S|},
\qquad q\le(2g+1)p,
\tag{3}
\]

for every S and uniformly over the entire incoming joint syndrome/reference state. This is a local-stochastic bound, not a product-error claim. It holds because the tags depend only on future local fault patterns, while correctness off each tag is uniform over input syndrome. Arbitrarily entangled gauges do not invalidate it. Conditioning on the coarse bit b does not alter independence of those future fault tags.

This gives exactly the input needed for the static majority-tree regenerator in ../passive_route/static_tree_regenerator.md. Its proof couples these possibly correlated leaf errors to a reference tree with all leaves equal to b, using the same fresh internal gate faults. The output differs from a fresh binary symmetric channel on b by at most q alpha^h, with alpha<1 at fixed small p. The reference-tree noise is independent of all old quantum references and gauges. This is a quantum-instrument statement: when the classical outputs agree in the coupling, the same retained quantum conditional state is used; when they disagree, trace distance is bounded by the mismatch probability.

## 4. Final feedforward and natural Pauli twirl

Run separate static trees for the two Bell bits. Their roots control only the final raw Pauli correction, after B's independent quantum descent. Their coarse controls never interact coherently with B at an encoded level. In the comparison, both roots are independent binary symmetric channels on the correct Bell bits, with explicitly computable crossover probabilities O(p).

Implement the final Pauli by two always-scheduled native gates: CNOT from the regenerated X-bit to B, and controlled-Z from the regenerated Z-bit to B. The raw controls are computational-basis classical bits and are discarded afterward. There is no ideal mutable gate-selector. Independent Pauli faults on these two bounded-arity gates propagate to a known single-output Pauli channel.

Let E_i be the independent B-side encoded-wait/descent channel on the logical qubit, with its fresh resource syndrome fixed. It is O(p)-close to identity by (2). If P_b is the Bell byproduct, the output before correction is E_i(P_b rho P_b-dagger). The uniform Bell outcomes themselves perform the Pauli twirl:

\[
K_i=Q_{i,\mathrm{terminal}}\circ Q_{i,\mathrm{tree}}
\circ\frac14\sum_b\mathcal P_b^{-1}\circ E_i\circ\mathcal P_b.
\tag{4}
\]

The Q terms are the tree-bit and final-gate Pauli channels. Thus K_i is exactly Pauli, O(p)-close to identity, and independent of old records and syndrome histories. The implementation differs from the tensor product of these K_i only by the paid high-level and tree-coupling error budgets. No additional twirling seed is needed.

After resetting the fine pool records, no signalling removes their correlations with B's syndrome. The fresh Bell-B syndrome marginal is the one from its independent resource; the independent regenerator reference channel prevents the final classical controls from reintroducing old-gauge dependence.

## 5. Synchronization and full cost

The majority-tree root and B's raw quantum output must arrive at the same predetermined clock. Run their terminal paths in parallel; pad earlier only while data and Bell copies remain protected. It is incorrect to finish regeneration and leave a raw bit waiting through a growing quantum descent. The last raw control, Pauli correction and memory SWAP occupy a bounded number of clocks and contribute to K_i.

For h=O(log(N/epsilon)), the tree has M=3^h=poly(N/epsilon) leaves. There are two trees per physical output. Creating their protected copies and descending them is therefore a potentially very large **polynomial** overhead, not the usual polylogarithmic FT overhead alone. The AB primitive gadgets have very unfavorable fixed constants as well. Preparation, corrected waits, native operations, classical leaves, trees, discard/reset and interconnect uses must all be included in spacetime and energy. These costs are supplied equally to the active comparator.

The declaration of a paid nonlocal active fabric with constant-size local final cells remains separate from a finite-speed, strictly local three-dimensional hardware realization. This note closes the noisy-controller mathematical interface, not that unproved geometry reduction.

Calibration and syndrome-sampling arithmetic are executed inside this same protected circuit. Their classical outcomes and intermediate parameters remain encoded when passed to the next stage. Logical measurements are implemented by coherent basis-label copying and discard. Thus an arbitrarily accurate internal classical decision is never exported through a single noisy raw classical output and silently treated as exact.
