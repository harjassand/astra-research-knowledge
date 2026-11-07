# Constructive dual-sector repair through the anchored double complex

7 November 2026. Follow-up after all independent initials were frozen. This is a new derivation for challenge, not a retrospective alteration of any initial report. It uses actual GJ Sections 6–7 maps, rather than equating raw transpose syndrome weight with cochain weight.

## 1. A local stable CSS duality

Let F be a fixed finite field of characteristic two, X a bounded-degree cubical complex of fixed dimension t, and Fcal its actual compatible cosheaf from GJ arXiv:2609.20780v1. All stalk dimensions and local degree constants are fixed. Its anchored arrays are

`A^{r,p}=direct_sum_{f in X(r),u in X(p), f<=u} Fcal(u)^*`.

Use the exact maps T and Delta of equations (7.2)–(7.3). They satisfy `T²=Delta²=0` and `TDelta=DeltaT`. Give A total CHAIN degree `n=p-r` and differential `d=T+Delta`. Thus d²=0 in characteristic two. Every degree has O(N) fixed-size coordinates and bounded local incidence.

**Lemma D1 (bounded-propagation stable CSS duality).** The CSS code in chain degree k of (A,d) has two local stabilizer normal forms:

1. The chain code of `C_*(Fcal)` with boundary `D^T`, plus product |0> and |+> ancillas.
2. The cochain code `C^{t-*}(Kcal)` with differential Delta, plus product |0> and |+> ancillas.

The normal-form basis changes and their inverses have bounded propagation and bounded row/column incidence, with constants depending only on t, local degrees and stalk dimensions. They give CSS Clifford coordinate changes. They can be implemented with O(N) temporary |0> work qubits and constant-depth CNOT circuits on the bounded-range interaction graph. Consequently the ORIGINAL cochain code Q_k(Fcal), after a constant-factor product-ancilla extension, is related to Q_{t-k}(Kcal) plus product ancillas by

`C = (CSS linear Clifford) H_all`,

where the linear Clifford and its inverse have bounded support spread. The word H_all here acts on the actual extended memory coordinates; temporary work used for circuit realization is not part of this abstract Clifford.

### Proof with the normal-form step made explicit

Horizontal reduction: at each fixed upper face u, Delta is the ordinary cube cochain differential with passive coefficient space Fcal(u)^*. Its cohomology is only the constant degree-zero cochain. The local cube contraction of GJ Lemma 7.3.1, or finite Gaussian elimination on this fixed-size cube, supplies a local basis of critical vectors, sources a_i and targets b_i, with `Delta a_i=b_i`, `h b_i=a_i`, `h a_i=0`. Choose the usual side conditions `h²=hi=ph=0`. The remaining perturbation is delta=T, lowering p. Its product h delta is nilpotent in at most t+1 steps. T preserves the constant-copy critical subspace, and its induced critical differential is precisely the physical transpose boundary B=D^T.

Vertical reduction: at fixed anchor f, T is the actual finite transpose evaluation complex. Theorem 7.2.1 proves exactness below top p=t and identifies its top kernel with Kcal(f). Gaussian elimination on that fixed-size local complex gives the same critical/source/target decomposition and contraction h, now raising p. The perturbation delta=Delta preserves the top-kernel critical subspace by Lemma 7.1.2. The induced differential is exactly the Kcal cochain differential. Again h delta is nilpotent in at most t+1 steps.

For either reduction, form the finite polynomial

`h'=(I+h delta)^(-1)h`, `p'=p(I+delta h)^(-1)`.

The elementary perturbation identities give

`d h'+h'd=I-ip'`, `p'i=I`, `p'h'=h'i=0`, `h'^2=0`,

and `d i=i d_H`. They can also be verified by multiplying the finite geometric series; no infinite inverse or analytic approximation is used. The critical inclusion i is unchanged because delta preserves its range and h delta i=0.

For every old source a_i set

`a_i'=h' d_0 a_i`, `b_i'=d a_i'`.

Then `d a_i'=b_i'`, `d b_i'=0`, and both a_i',b_i' lie in ker p'. The critical vectors i(H), together with these paired vectors, form an exact chain basis. In the horizontal case, each new vector equals its old vector plus terms with strictly LOWER p; in the vertical case the correction terms have strictly HIGHER p. For b_i in the vertical case, note that b_i has p one smaller than a_i, so delta a_i also has strictly higher p than b_i. Thus the complete basis-change matrix is, after the initial local block basis, I+Q with Q strictly triangular in the finite p filtration. Its inverse is the finite sum `I+Q+...+Q^t` (with the harmless sign changes outside characteristic two). Both matrices have bounded support and row/column incidence. This proves exact local normal form, not only chain homotopy equivalence.

At physical code degree k, an invertible binary coordinate change A_k is a CSS Clifford. Changes at k±1 merely change stabilizer generating bases. A contractible pair from degree k to k-1 supplies a |0> qubit; one from k+1 to k supplies a |+> qubit. All other pairs do not contribute physical code qubits. Field coordinates are converted in fixed binary/trace-dual bases, so the binary stabilizer commutation identities are exact.

For the optional finite-depth physical realization of a sparse invertible binary A with sparse inverse, use |0> work of equal size:

`|x>|0> -> |x>|Ax> -> |0>|Ax> -> |Ax>|0>`.

The two linear additions use A and A^{-1}. Each is a bounded-degree set of CNOT edges, so a fixed edge coloring gives constant depth. This works coherently on arbitrary superpositions. It proves stable circuit realizability while keeping the abstract pullback C on the memory coordinates free of work-register Pauli factors. ∎

## 2. A commuting local energy with both sectors descending

The normal form above maps `Q_k(Fcal)+A_original` to `Q_{t-k}(Kcal)+A_target`. Let

`U_F = Fcal cochain syndrome BLOCK weight + original Z-ancilla defects`,

`U_K = C^*[Kcal cochain syndrome BLOCK weight + target Z-ancilla defects]C`.

Here a Z-ancilla defect is `(I-Z)/2` for a product ancilla stabilized by Z. X-stabilized ancillas are accounted for by the other presentation. A block syndrome term is the projector onto a nonzero fixed field/stalk syndrome; it is a bounded-body commuting Pauli function.

All terms of U_F are Z-type stabilizer functions of the original extended code. All terms of U_K are X-type stabilizer functions, because C is a CSS linear Clifford after H_all. They commute. U_F=0 enforces the complete original Z stabilizer group, including original Z ancillas. U_K=0 enforces the complete original X stabilizer group: the target Z group is generated by the K cochain Z checks and target Z ancillas, and C swaps the two CSS types. Therefore their common zero space is exactly the original Q_k(Fcal) with its fixed product ancillas. No small-distance auxiliary logical modes have been added.

Use the S6 active-vertex lemma on Fcal in degree k+1 and on Kcal in degree t-k+1, plus independent single-site X flips for each Z ancilla. Both degrees are below t for `2<=k<=t-2`, exactly the GJ range. This gives at least `kappa_F U_F` and `kappa_K U_K` active labels at sufficiently low linear energy, before weighting. In the K statement, the code/syndrome is evaluated after C.

- A K X-correction pulls back to an original Z-type Pauli. It lowers U_K by at least 1 and preserves U_F exactly.
- An original F X-correction lowers U_F by at least 1 but may increase U_K by at most a fixed D_K, because its support and C's spread are bounded. The same bound covers original Z-ancilla corrections.

Choose a fixed integer A>D_K and set

`U=A U_F+U_K`, `H=J U`.

Every active F label lowers U by at least A-D_K>=1; every active K label lowers U by at least 1. The number of active labels is at least

`min(kappa_F/A,kappa_K) U`.

The catalog contains only O(N) bounded-support Pauli labels with bounded incidence. Enumerating every Pauli on each fixed star is a finite, perhaps enormous, local table. Repeated labels may be kept as separate bath coupling channels; no acquisition oracle is assumed.

Small total U implies small F and K syndrome weights, so the quantitative S6 support thresholds apply. Their physical/binary block constants are fixed. The total number of memory qubits is a constant factor of the original code length; the code distance remains linear because its ground code is original Q_k(Fcal) plus product ancillas.

## 3. Soundness and actual syndrome repair for this energy

First greedily decrease U_F, at most U_F steps. U_K can increase by at most D_K U_F during that phase. Then greedily decrease U_K, at most U_K+D_K U_F steps, preserving U_F. Every elementary correction has bounded physical support. Therefore a syndrome of sufficiently small U has a physical Pauli correction of weight at most C U, with C fixed, to the common code space. This provides the low-energy canonical correction needed for a full logical basin, not just a mean energy estimate.

Alternatively, use the established global qLTC soundness for static correction bounds; the argument above independently supplies the local descending dynamics for the engineered energy. The lower-energy canonical corrections and code distance identify all bounded local edges as logical identity when the energy cutoff is sufficiently small. The writer's intended logical action must still be proved; low energy alone does not select the logical state.

## 4. Consequence and scope

This closes the specific raw-transpose-descent gap by changing the commuting Hamiltonian and adding a constant factor of product ancillas. It does not claim that the original raw transpose syndrome weight descends under bounded-star physical moves. The local Gaussian normal form, finite-field binary conversion, energy weighting and active-density calculations should receive the hostile audit before promotion.

Li–Li–Han–Liu's original three degree-two sheaf codes (2609.26691v3, Eq.3.33) can be treated separately with this extension. Their bounded-incidence cubic gates act on the original DATA coordinates and trivially on the added product ancillas, so they still preserve the common ground code and have bounded depth/spread. Omit their optional repetition step, which is needed only for literal disjoint single-layer transversality and would otherwise require a new energy transfer.

Metropolis/Davies completion of this catalog is an engineered Markovian thermal model. It is not an exact microscopic joint-bath theorem. The construction alone does not give universal gates, a numerical threshold, Euclidean locality, or a favorable comparison with known measurement-free or autonomous fault tolerance. Its possible additional operation is a same-energy two-sector thermal cooling service compatible with the explicit non-Clifford gate DATA, subject to the principal's gate/cooling composition checks.

## 5. Simplification after checking CSS types

The weighting in Section 2 is conservative and unnecessary. Because the exact stable duality has the form `C=P H_all`, with P a pure CSS linear Clifford on memory coordinates, U_K is purely an ORIGINAL X-stabilizer function. Every original F X-correction therefore commutes with U_K exactly, including original Z-ancilla corrections. Likewise every pulled-back K X-correction is purely original Z and commutes with U_F exactly. Thus the actual cross-energy bound is `D_K=0`. One may take `U=U_F+U_K` and obtain active density `min(kappa_F,kappa_K) U` directly. The weighted version remains true but adds no benefit. This correction is recorded rather than silently erasing the earlier conservative derivation.

The two-stage repair count also simplifies: at most U_F+U_K moves suffice, with constant support per move, since neither stage raises the other energy.

## 6. Exact gate-code ground space and two safe coordinate choices

**Preferred original-DATA presentation.** For each Li sheaf Fcal_a, perform the two exact normal-form calculations in degree k=2, t=6 and choose the memory coordinates as `Q_2(Fcal_a)` plus the product ancillas from the H-swapped horizontal normal form. In these coordinates, UF=0 imposes the COMPLETE original Z stabilizer group and UK=0 imposes the COMPLETE original X group. This follows from equality of the stabilizer groups under the CSS duality C, not merely from equality of homology dimensions. Therefore the common ground space is exactly the original Li code with those product ancillas. The logical gate is Li's original bounded-depth DATA circuit tensored with identity on the added memory ancillas. No conjugation of the DATA circuit is needed.

**Equally valid transported presentation.** One may instead choose the total anchored-complex code or the K presentation as physical memory coordinates. Then conjugate the original Li DATA gate (with identity on the fixed product ancillas) by the explicit corresponding Clifford coordinate transformation. Its support spread is still bounded. A constant-depth realization is available with the same O(N) temporary |0> work using the sparse-matrix implementation in D1; those work qubits, their noisy initialization and gate-time exposure must be charged. This version is useful if a hardware catalogue naturally realizes the total-complex coordinates, but it adds an unnecessary gate interface when original DATA coordinates are available.

In either case omit Li's optional repetition reduction: original bounded-incidence cubic gates already have constant depth by hyperedge coloring. Literal single-layer disjoint transversality is not needed for the proposed finite-duration service.

## 7. Pinned bibliography and source scope

1. William Gay and Fernando Granha Jeronimo, *Asymptotically Good Quantum Locally Testable Codes*, arXiv:2609.20780v1, 17 September 2026. Primary HTML SHA-256 `6fc3a24a86750c48d375a530ffd73894b789965942d30de6134d5627c3e2e257`. Sections 6.1–6.4 provide local cochain cominimality/support recursion; equations (7.1)–(7.6), Lemmas 7.1.1–7.1.2, Theorem 7.2.1 and Lemma 7.3.1 provide the exact anchored-array double complex, local transpose exactness/kernel charts and cube contraction used here. https://arxiv.org/html/2609.20780v1
2. Yiming Li, Zimu Li, Zhengyi Han and Zi-Wen Liu, *Parallelizable and addressable transversal non-Clifford gates on good quantum LDPC codes*, arXiv:2609.26691v3, 6 October 2026. Primary HTML SHA-256 `d8961151da7f07f54ca99b3e934902f2a7e58f8d1fba75022c13820d9fbf0ea5`. Equations (3.20), (3.31)–(3.33), Proposition 3.3 and Section 3.4 specify the actual sheaf complexes and uniform primal/dual product expansion; equations (3.223)–(3.227) give the original addressable CCZ DATA gate. The optional repetition encoding is not imported. https://arxiv.org/html/2609.26691v3
3. Yifan Hong, Jinkang Guo and Andrew Lucas, *Quantum memory at nonzero temperature in a thermodynamically trivial system*, Nature Communications 16,316 (2025), DOI 10.1038/s41467-024-55570-7; arXiv:2403.10599v3. Theorem B.8 and Appendices E.2–E.3 are prior local Gibbs-sampling passive memory and measurement-free fault-tolerance constructions. This prevents claiming a new generic Metropolis-completion or qLDPC passive-memory principle. https://www.nature.com/articles/s41467-024-55570-7

The stable normal-form and pulled-back energy arguments are derived explicitly here. Gaussian elimination, CSS coordinate changes and finite nilpotent perturbation algebra are established machinery; no historical-firstness claim is made. This note is frozen as v1 below for cross-review, while the initial independent report remains unchanged.
