# Coherent atomic SSF: a correctable-span lift, a count-norm lemma, and the unresolved coherent sieve

Date: 2026-10-29. This is an independent non-Pauli analysis, conditional on the deterministic asynchronous SSF witness lemma being correct. It does **not** certify that lemma, the physical controller compiler, or a general coherent memory threshold.

## Outcome

The Pauli theorem cannot presently be upgraded merely by replacing probabilities with inclusive diamond norms. There are two valid constructive pieces:

1. Safe Pauli histories lift to a *linear correctable operator span*, without twirling and with a retained common bath.
2. The inclusive physical-time bound extends to *multiplicity thresholds in each deterministic cell*, with factorial suppression. This repairs the mismatch between binary cell marks and the witness's fault-mass counts.

The exact missing piece is a volume-uniform **coherent witness sieve**, not a Pauli expansion or a single-cell noise estimate. Below is a sufficient, algebraically explicit criterion for that sieve and a small counterexample to the naive union-bound inference. No counterexample to the actual ideal-SSF threshold is established.

## 1. Model and the channel being claimed

Use the ideal hub instruments: at independent Poisson rings, measure the stabilizer information needed by that hub and apply its deterministic accepted SSF Pauli correction, or do nothing if none is accepted. The measurements and feedback are actual quantum instruments, not evaluations of a hidden classical error. Retain all measurement outcomes and the Poisson schedule if useful. Both CSS sectors must be included.

Let the additional joint data-bath generator be a sum of bounded local Hamiltonian commutators and added bounded Lindblad dissipators. A term has bounded DATA support, but may act on the same arbitrarily large bath as other terms. A deterministic anchor/time cell j has budget

    ε_j = integral ||N_j(t)||_diamond dt
        <= integral (2 sum ||h_e(t)|| + 2 sum ||M_a(t)||^2) dt.

The norm acts on the full joint data-bath map, with an arbitrary reference. Uniform bounded-degree incidence and a uniform bound on these *joint* norms are indispensable. A small reduced-data generator or a small average bath matrix element is not this hypothesis.

Fix an encoding channel V and an initial bath state σ_B independent of the logical input. The desired final statement is

    || Dec o E_t o (V tensor σ_B) - id_L ||_diamond <= δ(t,N),

where bath and records are discarded only after decoding. Logical input may be arbitrarily entangled with a reference. The bath may remain correlated with data throughout the experiment and between every block.

One can instead formulate a joint logical-bath statement, with an appropriate bath/record channel on the right-hand side. Arbitrary unspecified initial system-bath correlations do NOT by themselves define a linear logical channel to which a diamond norm applies. Specify an initialization channel, or require the encoded subsystem initially factor from the bath. A noisy preparation map with its own local norm contract is another admissible input model.

This is a condition on the initialization, not a bath reset between blocks.

## 2. Correctable-span lemma: the genuinely quantum part that does work

Fix a realized ideal clock schedule. Expand a bounded-support system-bath Hamiltonian operator in a system Pauli basis, with operator-valued bath coefficients. Do the corresponding two-sided expansion for generator insertions. The number of system basis elements per insertion is constant when the support bound is constant. These coefficients are NOT probabilities.

Consider a single ket-side Pauli history h, including actual measurement outcomes. On the encoded subspace each measured stabilizer has a definite eigenvalue along that history. Thus a record-compatible history has the form

    K_h V = E_h V tensor B_h,

up to a scalar phase and with the record register included in B_h. Incompatible histories vanish. Intermediate SSF feedback is just the corresponding record-controlled Pauli correction. It need not be Clifford as an unconditioned nonlinear classical decision rule; the record-conditioned action suffices.

Let Dec be one *common*, fixed terminal recovery and decoding instrument. Suppose the deterministic good-history result says that every h in a family H_good is restored by that recovery with the identity logical action. Equivalently, for every such h,

    Dec_dilation K_h V = I_L tensor C_h.

Then every coherent linear combination of those histories has exactly the same factorization. Likewise every two-sided pair h,h' in H_good has identity logical action on the superoperator level:

    rho_L tensor X_B -> rho_L tensor C_h X_B C_h'^dagger.

This remains true if h and h' have the same syndrome and their coherence survives all measurements. If records are distinguishable the corresponding cross term disappears; that is helpful but is not assumed. No Pauli twirl or fictitious classical error distribution is involved.

The necessary hypothesis is a **common recovery corrects the whole safe span**, not that each error has some recovery chosen with knowledge of its unobserved history. Minimum-syndrome recovery is acceptable only where the deterministic theorem really proves that every safe residual is in its correct stabilizer coset. A Pauli-history analysis for only one CSS sector is insufficient for arbitrary two-sided quantum insertions; both sides and both sectors must be safe.

### Diamond-norm conversion

Suppose an exact fault-path grouping, after encoding and decoding, gives

    E_dec = G + B,       ||B||_diamond <= δ,

and every term of G belongs to the safe span. After tracing bath and records, G=a id_L for a scalar a. G need not be positive or normalized. Since E_dec is trace preserving, |1-a|<=δ, by testing any density operator. Therefore

    ||E_dec-id_L||_diamond <= 2δ.                    (1)

So a norm bound on the bad *superoperator sum* would immediately suffice. At a Stinespring-amplitude level one uses the usual cross-term estimates instead. One must not call the norm of a coherent bad sum a failure probability.

## 3. New useful extension: inclusive cell multiplicities

The existing physical-time note proves an inclusive bound when each selected deterministic cell has at least one insertion. The SSF witness counts repeated fault mass, so a binary occupied-cell estimate alone is not enough.

Assume switching each N_j independently by z_j in [0,1] leaves a CPTP joint generator. Let E(z) be its full propagator/instrument, and fix positive integers k_j on a finite selected set S. Define the Taylor-remainder operator in coordinate j by

    R_j,k f = f(z_j=1) - sum_{r=0}^{k-1} (partial_j^r f)(z_j=0)/r!.

All unselected coordinates remain at one. Set

    F(k_S) = (product_{j in S} R_j,k_j) E.

In the Dyson expansion this is exactly the inclusive sum containing at least k_j insertions from each selected cell j, with arbitrary insertions everywhere else. Iterated integral Taylor remainder and mixed Duhamel differentiation give

    ||F(k_S)||_diamond <= product_{j in S} ε_j^(k_j)/k_j!.    (2)

Proof detail: the mixed derivative of orders k_j is a sum over time-ordered marked insertions separated by interpolated CPTP propagators. All relative temporal orderings, including repeated labels, bound its norm by product ε_j^k_j. Integrating the Taylor weights (1-z_j)^(k_j-1)/(k_j-1)! contributes exactly 1/k_j! per coordinate. The proof is uniform in all unselected volume and in the retained bath. The k_j=1 case is the existing finite-difference theorem.

This is not a stochastic Poisson count statement. It is a norm statement about an exact inclusive sum. It remains valid with the ideal measurement record retained.

The same mechanism gives useful *local* coarse-count estimates. For a fixed cell region containing O(m) cells and a threshold k=Omega(m), threshold inclusion-exclusion costs only exp(O(m)), not exp(O(N)). However it still does not select which adaptive SSF witness occurred.

## 4. Exact obstruction: a witness is not a measurable record event

The SSF backward proof assigns a witness using a complete Pauli error history, its future support, and a chosen reduced representative. These labels are terms of an operator expansion. They are not generally outcomes of the actual syndrome instrument. Different labels with the same measured record can interfere.

A trace-nonincreasing CP projection onto an actual record event is norm-contracting. Selecting a subset of formal fault paths is not such a projection. Consequently

    || inclusive sum over S || <= ε^|S|

DOES NOT imply the same estimate for a history-selected sub-sum that happens to contain S. Cancellation in the full inclusive sum may be removed by the selection.

Similarly, the classical pointwise implication

    Bad(T) <= sum_W 1{W is a witness in T}

is not a norm inequality between signed/complex map sums. It is the union bound, not the local fault budget, that fails to transfer automatically.

### Minimal algebraic counterexample to that inference

For two abstract locations take scalar multiples of a fixed norm-one map D, with exact nonempty-path coefficients

    A_{1}=(η+η²)D,  A_{2}=(η+η²)D,  A_{12}=-η²D.

Then F({1})=ηD, F({2})=ηD and F({1,2})=-η²D. All stipulated inclusive bounds hold. But the sum selected by 'at least one fault' has norm 2η+η², exceeding the putative union bound 2η. Equally, selecting the exact singleton from F({1}) increases its norm.

This example can be embedded in a family of CPTP interpolation maps: take D=(Ad_X-id)/2 on a qubit and

    E(z)=id+[(η+η²)(z1+z2)-η² z1 z2]D.

For small η and z in [0,1]^2 every E(z) is a valid bit-flip channel and ||D||_diamond=1. It is an algebraic counterexample to deriving a union bound solely from inclusive norms and CPTP interpolation endpoints. It is NOT a counterexample to the specified additive local-generator model or to an asymptotic threshold; the extra η² term could be harmless in a properly controlled sieve.

## 5. A precise sufficient coherent-sieve theorem

For a finite binary-location discretization write A_T for the exact sum with precisely fault set T and

    F(S)=sum_{T superset S} A_T.

For any Boolean selector b(T), define its multilinear/Möbius coefficients

    μ_b(S)=sum_{U subset S} (-1)^(|S|-|U|) b(U).

There is the exact identity

    B_b = sum_T b(T) A_T = sum_S μ_b(S) F(S).          (3)

Therefore a sufficient norm criterion is

    K_b(ε):=sum_S |μ_b(S)| product_{j in S} ε_j,
    ||B_b||_diamond <= K_b(ε).                        (4)

For multiplicities replace Boolean Möbius inversion by the corresponding discrete inversion in count thresholds and use (2). This is a mathematically explicit target, not a claim that K_b is small for the SSF selector.

If b depends on Pauli labels rather than just occupied locations, first construct a *label-independent conservative selector*: all assignments of local Pauli components on every unmarked-safe pattern must be correctable by the common recovery. Finite support contributes constant basis-expansion factors only for insertions actually exposed by a valid sieve; decomposing all unmarked volume defeats the purpose.

For a fixed region of n cells, the selector 'at least k faults here' has

    μ_b(S)=(-1)^(|S|-k) binom(|S|-1,k-1), |S|>=k.

For a uniform η it follows that

    K_b(η) <= binom(n,k) η^k (1+η)^(n-k).             (5)

Thus n=O(m), k>=αm yields exp(O(m))η^(αm), fully compatible with connected-animal counting. This shows a single fixed dense certificate is not the fundamental obstacle. This coefficient identity is the standard fault-path inclusion-exclusion identity in AGP Section 11.2, Lemma 7 / equation (63), not a novelty claim.

What remains is bounding the selector for the UNION over all overlapping, backward, history-dependent certificates, and then iterating the output error-span contract. The existence/counting of individual classical certificates does not establish the weighted absolute Möbius bound for their union. A linked-cluster expansion, a first-failure stopping decomposition with controlled norm, or an exRec-style recursive truncation lemma could supply it. None is present in the supplied asynchronous witness proof.

A sufficient full conclusion would be: for each total observation time t, a label-independent bad selector b_t has safe complement in the common correctable span, and its joint clock-averaged coherent sieve obeys

    E_clock K_{b_t}(C_s ε) <= C (1+t/τ) N exp(-c sqrt(N)). (6)

Here C_s is a constant local basis cost, and misses enter through the actual independent Poisson schedule rather than imaginary fault probabilities. Equations (1) and (6) give the desired decoded logical diamond bound. Alternatively a stable blockwise norm-valued residual-span contract could be iterated without resetting the bath. The classical local-stochastic residual tail in the supplied file is not that contract.

## 6. Two additional scope constraints

### Independent clock schedules

For the IDEAL comparator only, conditioning on the externally independent Poisson ring schedule leaves genuine measurement/feedback CPTP maps interleaved with the physical noise. This is legitimate, even if syndrome outcomes depend on the data and bath. One may then average unnormalized norm estimates over schedules. It does not authorize conditioning on syndrome-dependent Pauli witnesses or dividing by rare record probabilities. A bath may influence physical data but must not alter the postulated independent clock law. The actual controller problem has a separate clock/instrument semantics gap.

### General bounded HP perturbations

Hermiticity preservation alone is insufficient even to define a physical perturbation. For a signed difference of calibrated generators, it may happen that L0+sum N_j is CPTP while independently switching the N_j is not. Then the CPTP-interpolation step behind (2) fails. A simple decomposition is L0=0, N1=2D, N2=-D for a dissipator D: the total is physical, but switching off N1 leaves a negative dissipative rate. Sometimes terms can be regrouped locally to restore the contract; that must be shown rather than assumed.

A general signed local HP perturbation therefore needs a separate norm-resummation hypothesis or proof. The existing inclusive result safely covers bounded Hamiltonian terms and added Lindblad terms with legitimate independent interpolation. It does not automatically cover every small HP perturbation for which only the final total generator is known to be physical.

## 7. Standard fault-tolerance comparison and stopping conclusion

Terhal–Burkard, *Fault-tolerant quantum computation for local non-Markovian noise* (2005), treats local system-bath coupling without resetting the bath. Aliferis–Gottesman–Preskill, *Quantum accuracy threshold for concatenated distance-3 codes* (2006), explicitly handles local non-Markovian noise and ties a norm-based fault-path calculus to deterministic fault-tolerant gadgets and recursive correctness. These are the relevant strong comparators—not merely a stochastic circuit threshold.

Primary sources:
- https://arxiv.org/abs/quant-ph/0402104
- https://arxiv.org/abs/quant-ph/0504218
- https://arxiv.org/html/quant-ph/0504218 (Section 11.2 and Lemma 7 for the coherent counting identity; Section 11.3 for overlapping rectangles; Section 11.6 for surviving same-syndrome interference).

The atomic asynchronous SSF proposal avoids some gadget/scheduling assumptions, but has not supplied the corresponding coherent bad-path grouping and stable norm-valued residual induction. Calling its Pauli probability bound a diamond-norm theorem would skip exactly that work.

**Established here:** correctable-span lift; factor-two logical-channel norm conversion; inclusive multiplicity bound with retained bath; exact Möbius sufficient criterion; controlled fixed-region threshold estimate; precise initialization, clock, and HP scope conditions.

**Not established:** a volume-uniform SSF coherent sieve, its blockwise invariant residual contract, or a counterexample to the ideal coherent threshold. This is the exact stopping gap. No publication or unrelated project work was performed.

## Appendix: explicit syndrome measurement is not a free twirl

Even without a bath, the three-qubit bit-flip repetition code gives a useful exact diagnostic. Apply U=(c I-i s X)^{tensor 3}, with c=cos(theta), s=sin(theta), then measure its complete stabilizer syndrome and apply the usual minimum-weight X correction. On the logical qubit, the corrected syndrome Kraus operators are

    K_0=c^3 I+i s^3 X_L,
    K_j=-i s c^2 I-s^2 c X_L,  j=1,2,3.

Consequently the exact recovered logical channel is

    rho -> (1-p_L)rho+p_L X_L rho X_L
           -2i c^3 s^3 [X_L,rho],
    p_L=s^6+3s^4 c^2.

Its Pauli-twirled surrogate lacks the commutator term. A logical Z eigenstate already gives trace-norm deviation from identity at least 4|c^3 s^3|=Theta(|theta|^3), whereas the stochastic bit-flip logical failure probability is p_L=Theta(theta^4). Full ideal syndrome measurement therefore does not justify replacing coherent local rotation strength theta by a classical bit-flip probability sin^2(theta) in a claimed diamond-norm conclusion. The coherent term comes from errors with identical syndrome but different logical action. This is an illustrative small-code calculation, not a counterexample to SSF or to a sufficiently weak coherent threshold with different exponents.
