# Independent review: coherent ATG source lift
2026-10-30. Scoped PASS for the explicit source dictionary and conditional positive-projector/common-span lift, with the bookkeeping repairs confirmed below. No autonomous capture or receiver theorem.

Reviewed manuscript COHERENT_ATG_SOURCE_LIFT.md SHA256 ce2ac017dc0858c26d0fa7ef6006ac5925b4e1813b5c88bee66b72a39d2ae966.
Test check_source_defect_dictionary.py SHA256 7c8d81caaf98ef6e8a03461d647170b1d02953dac16e70f9927a65950b3ed468.
Deterministic source extraction: source_certificate/DETERMINISTIC_ATG_SOURCE_SPAN.md, SHA256 9114c4b34e1d77c9fc6894e6943aa34e7ad1923745c06ce69ba177cec059a8b5.

## 1. Exact coherent dictionary, independently derived
Write the ideal graph state as sum_s |s>_X,bulk tensor |psi_s>_boundary. All graph-input Z defects commute with graph CZ. Applying bulk H and CNOT to pointers initially in computational string c gives, for graph defect a,

    sum_m |m+c>_bulk |m>_pointer
          tensor Z^(a_boundary) |psi_(m+c+a_bulk)>_boundary.

This is an exact joint vector identity, including the retained graph gauge. It is stronger than a postmeasurement probability identity. Thus f=a_bulk+c is correct and there is no missing lightcone multiplicity in this completed input-basis dictionary. Intermediate physical perturbations still need the separate toggling-frame lightcone estimate and moment theorem.

For any k effective vertices, membership of each in the covering support requires one of at most two distinct corresponding input-defect bits. These choices do not reuse a bit across vertices. The positive subset-moment bound and a union over at most 2^k choices give Q=2q without independence or source-volume cost. XOR defects are a subset of this OR cover.

## 2. Decoder and common span
With beta chosen from metasyndrome alone, M m=M f implies beta(Mm)=beta(Mf). Corrected complete boundary/Bell stabilizer signs depend on f+beta(Mf), not on m. Therefore one Rep(f) suffices for all attainable records. Distinct Pauli solutions of the complete target-state sign equations act on the target ray identically up to phase. The same fixed controlled P(m) handles all components of a coherent source input; no component-dependent decoder is inserted.

Retaining |m+c> as gauge and retaining pointer coherences causes no enlargement of the frame-corrected boundary subspace. A linear combination of good-pattern vectors lies in the direct sum over m of the same Pauli-radius module, tensor arbitrary gauge and bath. This conclusion does not require dephasing, a fresh measured syndrome, or an actually executed feedforward gate. The controlled frame is an analysis isometry, not supplied physical control.

## 3. Good-set and counting
The manuscript adopts the earlier deterministic component replacement/telescoping certificate. Witness A excludes bridging mismatch components; B excludes distance-sized completed components; C is needed separately to bound TOTAL boundary repair weight. Small individual clusters alone are insufficient for that last property. The half/quarter occupancy constants and bounded-degree counting produce the stated geometric forms with adjustable constants depending on locality. O(n) direct terminal and boundary density tests are separate. At sufficiently small fixed q, d and T linear in n and positive linear radius budgets give exponential tails. This remains conditional on the actual positive subset-moment estimate; the finite dictionary test is not a proof of that estimate or the clustering theorem.

Two bookkeeping qualifications were sent to the author:
1. To call the entire Pi_good predicate hereditary, enforce terminal tests on the OR covering support (as the manuscript offers), not literally on |b(a_bulk+c)|. Removing one of two cancelling defects can increase an XOR count. A nonhereditary diagonal good projector would still support the gentle argument, but the hereditary assertion would not follow.
2. Baseline selector b may have bounded repeated outputs. For example T=1 uses the same X-check record at both boundaries. A general terminal-count tail must pay this bounded multiplicity, e.g. use threshold u/kappa, or restrict to the asymptotic T>=2 regime where those two terminal records are distinct. This only changes constants/exponents by a locality-dependent factor, not the exponential conclusion.

## 4. Gentle bound and fixed discrepancy
For the actual full toggling-frame state and diagonal good projector, Tr[(I-Pi)rho]<=delta gives ||rho-Pi rho Pi||_1<=2sqrt(delta). Unitary U and subsequent actual channels contract that norm. This is an unnormalized CP good-part comparison; no inverse acceptance probability is introduced. If the bound is uniform over input states with arbitrary reference for the actual source map, it gives the corresponding complete map estimate. It does not by itself assert a diamond bound on an arbitrary-input quantum computation: graph and pointer inputs are the stipulated fresh product state.

In one actual m block, the uncorrected local signs are b(m)+b(f)+sigma(E_B); the corrected signs are sigma(E_B)+sigma(Rep(f)). Their equality after toggling P(m) yields exactly

    D(m)=b(m)+sigma(P(m))=b(f)+sigma(Rep(f)).

Thus |D(m)|<=u+nu*t. The physical E_B cancels in this baseline discrepancy but remains in the quantum radius t+t_B. D(m) is a single fixed classical function, common to all coherent components with the same m; hence the good joint state is supported on its low-weight diagonal record sector.

## 5. Replay and unearned seams
Replayed all 65536 source dictionary branches: maximum residual zero. Saved source_replay.json. The example has only a Z-check family and does not test general ATG decoding, large-distance clustering, or memory drift.

The scheduled circuit's gate depth and degree are bounded; retaining pointers supplies no legal, stabilized classical-memory initialization. No capture fidelity, waiting protection, all-state fixed-baseline receiver, physical terminal flag, autonomous fresh-input production, final frame execution, or Bell-to-known-zero conversion follows from this receipt.

## Final-byte verification
The final manuscript incorporates both requested qualifications. It also incorporates the parallel reviewer’s correct combinatorial repairs: the globally excluded A-witness family has nT, not n, prefactor; every C-component contains a selected root. These strengthen the precision of the counting and preserve its exponential conclusion. The final hash above binds those verified bytes. The earlier source extraction has a separate precision addendum clarifying the rooted-union count; its original hash remains the one recorded above.
