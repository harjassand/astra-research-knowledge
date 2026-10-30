# Exact intended-DATA / retained-controller decomposition
2026-10-29. Consequence of FULL_HILBERT_FOREST_GAUGE.md; no independent schedule assumption.

## Registers and record convention
Let D be all payload data. Let B contain all hub clocks, private workspaces, lock registers, monitor auxiliaries, and any actual retained external bath. Work in the local forest-gauge frame. Retain the actual kick and clean jump/monitor records. Workspace labels of a terminal reset may either be retained as the intended recovery syndrome instrument or summed as a bundle; do not coherently add them.

The proof is an equality of full unnormalized instruments on D⊗B, including arbitrary reference entanglement. It is not a normalized conditional reduced-data evolution.

## 1. Between DATA emissions: controller-only maps
The transformed Hamiltonian is I_D⊗H_B. Every complete summed reset loss is clock-diagonal and identity on payload/workspace, and monitor terms are payload-blind. Therefore the no-jump propagator between actual recorded jumps is I_D⊗M_B for an appropriate contraction M_B (or the corresponding controller-only CP instrument if some monitor records are summed).

Commit, ready, A/Q refresh, lock cleanup, and monitor jumps act only on B. A non-computation-origin abort reset also acts only on B. Thus these operations are legitimate retained-controller/bath-only maps between DATA events. This does not mean their record-conditioned effects on correlated D are trivial: postselection on a bath outcome can filter D. The full instrument retains that effect.

## 2. Good terminal factorization is an operator identity
Let K_(h,s)=<s|V_(h,L)|0> be the intended recovery Kraus operators, and let P_own be the projector onto all h resource tags o_h. On the good terminal source, h's phase is C_L, P_own=1, and W_h=|0>. The transformed physical terminal Kraus operator obeys

   J_tilde_(h,s) P_good,source
     = sqrt(kappa_T) K_(h,s) ⊗ C_h,

with tensor ordering understood and

   C_h = |Q_0><C_L|_clock ⊗ |0><0|_(W_h) ⊗ P_own,

times identities on all remaining registers. This equality is restricted to the good source; it need not hold outside it. C_h acts only on B and K_(h,s) only on D. No assumption that D and B are uncorrelated is used.

Consequently, summing s gives the exact intended recovery channel Phi_h on D tensored with the clock-source/reset CP map on B. Retaining s gives the exact intended syndrome-resolved recovery instrument instead. A good-source abort has zero support because every failed-test projector vanishes.

The statement remains true if the bath, locks or other clocks are entangled with D. Only the declared source constraints W_h=0 and all-owned mask are needed.

## 3. Local kicks and marked DATA emissions
Let a physical CPTP Poisson kick K have support X. Its transformed map is

   K_tilde = Ad_(F†) o K o Ad_F.

Let N(X) be the set of frame factors F_h whose support intersects the ORIGINAL X. Then K_tilde is supported inside

   X_plus = X union union_(h in N(X)) support(F_h).

No iterative neighborhood expansion occurs because the F_h commute. X_plus has bounded size/radius for a bounded X in bounded geometry. The transformation preserves CPTP character, reference extensions, and diamond norms; ||K_tilde-id||diamond≤2.

Maintain hub marks set by kicks in the affected history neighborhoods and cleared by terminal/abort reset. Every unmarked hub has a good source. Marked terminal/abort jumps are retained as their exact bounded-support joint D⊗B Kraus instruments; their mask controls are quantum, never dephased. There are at most sum_kicks |H_X| such marked emissions at any finite horizon. Each initial dressed kick is a separately counted bounded-support insertion.

## 4. Exact full-instrument decomposition
For every actual full record, the unnormalized evolution is an ordered composition of:

1. controller/bath-only CP maps;
2. exact intended local recovery channels Phi_h (or syndrome subinstruments), each accompanied by its controller source/reset CP factor;
3. the bounded-support dressed kick maps;
4. at most sum_kicks |H_X| marked bounded-support DATA/controller reset instruments.

All these are the actual transformed physical maps, so summing records gives exactly the physical quantum channel conjugated by the fixed local frame. There is no new schedule distribution to posit and no assertion that the record probabilities are data-independent. The maps in (2) are the intended data operations as operator identities on their actual good sources, not inferred from clock paths.

For finite record bins, every selected event map is CP trace-nonincreasing; the complete instrument is CPTP. Thus the total augmented kicked instrument has diamond norm one, and its difference from the corresponding no-kick full instrument has norm at most two for one kick. Continuous records are the usual instrument refinement limit. Never divide these estimates by a rare record probability. A density at an exact jump time is not itself a normalized quantum channel.

## What this bridge does and does not solve
This is a genuine bounded local DATA-insertion/emission decomposition with retained controller memory and the actual quantum instrument. It avoids the earlier missing step 'a monitored clock path must equal a fresh data channel'. It is stronger than controller no-creation or a graph-theoretic episode count.

A threshold/Pauli-history argument can now use the actual Phi_h maps and treat the rest as retained-controller maps, provided its correctness statement permits this actual-order scheduler and final interface. Such a theorem is not proved here. In particular, adaptive record correlations, wall-clock storage exposure, spatial-temporal clustering of multiple kicks, and a suitable recovery rule remain relevant. The decomposition does not imply fixed-schedule local-stochastic errors per completed update, nor an input-independent malformed clock law.

The final state in this identity is dressed by F†. Obtaining bare physical data requires completing/draining unfinished transactions or physically applying/including this bounded-depth frame in the decoding interface. Controller-only no-jump evolution can coexist with arbitrarily long physical waiting; this theorem does not make stored data immune to additional physical-time noise.
