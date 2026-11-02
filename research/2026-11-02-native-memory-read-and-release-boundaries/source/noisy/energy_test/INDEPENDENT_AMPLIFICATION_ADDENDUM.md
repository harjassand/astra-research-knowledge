# Independent addendum: rare-workspace amplification now reaches constant error

2026-11-01. **PASS under the explicit single-logical-qubit, syndrome-diagonal input, fresh-bank and spent-record-isolation conditions.** This new argument closes the fixed-error gap identified in my earlier physical-resource receipt; that earlier receipt is preserved and was correct about the unamplified construction.

Bindings:
- `ROOT_ENTANGLEMENT_BREAKING_AMPLIFICATION.md`: SHA256 `2c4a4cd0f64336829d7826ab1d2761f01ecb0b28f2e98bce9f0fbee41e422ae6`.
- `AMPLIFICATION_INDEPENDENT_AUDIT.md`: SHA256 `d6d51438316fb8f7ef6c8a0fe2fa2a60b59c9d336cc4f28d34ea8470c50b9c45`.
- My preserved `INDEPENDENT_PHYSICAL_RESOURCE_AUDIT.md`: SHA256 `652d31278225d8410a05b7daee3639a2206b2ed6aef0521cd1548fe8b35219ad`.

## 1. Bad-workspace trajectories preserve the required class

Use the basis of complete valid reference syndrome, decoded logical Z and classical bath/workspace energy labels. Every completed code case-swap is a permutation of syndrome/bath labels accompanied by a logical Pauli. Its source conditions depend only on syndrome and bath/workspace, never on the logical bit. Reversible predicates, bath resonant exchanges and equal-gap routing are of the same classical-label type. This remains true for arbitrary invalid battery or dirty scratch labels; functional success on those labels is unnecessary.

If S is the Hermitian off-diagonal case-swap and Q=S^2 its support projector, then h=Q-S has norm at most 2, commutes with K, and exp[-i(pi/2)h]=(I-Q)+S. Apply cases sequentially. Even when bad-input cases overlap, their composition is still a monomial/Pauli-trajectory operation, not a coherent sum of conflicting moves. Any Pauli phases are logical-state-independent phases within the completed history and do not create syndrome coherences. Intermediate pulse superpositions are harmless provided no unaccounted simultaneous coupling acts; the always-on drift K commutes with these pulses and has no logical-dependent energy.

Starting with a classical syndrome and diagonal bath, completed attempts therefore preserve syndrome block diagonality, with arbitrary logical/reference states inside blocks. This verifies the needed preserved class for BOTH Phi_good and Phi_bad, not merely successful histories.

## 2. Good branch approximates a reduced-memory entanglement-breaking map

The new independent zero-gap bit r has distribution I/2. Conditioning every code-contact gate and every flag reset on r=1 leaves the memory exactly unchanged at r=0. Refill may still run, since it is bath-only. At r=1, the previous uniform success estimate applies to every input syndrome and logical/reference state. On successful histories, the full Pauli path restores the original syndrome and conjugates by bare logical X.

For a Pauli decoder, bare X and decoded X differ only by a syndrome-dependent scalar phase. With classical unchanged syndrome that phase cancels in conjugation. Thus, after tracing out the attempt resources, the good channel is within at most a constant times delta_n in reference-safe trace norm of

    E = (id + Ad_X)/2

with syndrome unchanged. This uses classical failure-event probabilities; no square-root loss is required. A failed history has weight at most delta_n and contributes at most twice that weight to the norm comparison.

For one logical qubit, E is complete dephasing in the X basis. On a syndrome-block-diagonal memory/reference state it produces a sum of positive product operators indexed by syndrome and X outcome. It is therefore separable across the ENTIRE memory versus reference. This statement does not extend to arbitrary syndrome coherences or unrestricted additional logical qubits, neither of which is needed for the specified actual one-logical-qubit code.

## 3. Fresh-bank decomposition and the crucial error factor

The initial clean-workspace event is a classical bath-only event of probability p_n independent of memory and reference. It gives an exact convex decomposition into CPTP channels

    Phi_j = p_n Phi_good,j + (1-p_n) Phi_bad,j.

The comparison Psi_j=p_n E+(1-p_n)Phi_bad,j differs on the preserved input class by at most p_n C delta_n. All these maps preserve that class. Channel telescoping for M independently initialized, previously untouched attempt banks therefore gives reference-safe error at most M p_n C delta_n. Identical bad maps across attempts are not required.

Choosing M=ceil(log(4)/p_n) gives M p_n<=log(4)+1 and total comparison error O(delta_n). The probability of no E branch in the ideal mixture is (1-p_n)^M<=1/4. There is no demand delta_n<p_n and no simultaneous postselection of every attempt's clean workspace. Increasing logarithmic-buffer length changes polynomial exponents but does not create the previous suggested circular accuracy requirement.

## 4. Record isolation and fidelity conclusion

E describes the memory after the attempt bath is traced out. The global memory-plus-used-bath state can retain the original entanglement in r or other records. Subsequent operations may therefore be treated as fresh memory CPTP maps ONLY if used record identities never return to memory-coupled contacts. The stated dedicated-bank/tracked-routing schedule, with code contact disabled during routing, can enforce this. Old-state positions may be permuted by bath-only SWAPs, but an old record must never be mistaken for a fresh resource. The drift K does not recouple those records.

Under this isolation, every ideal history containing an E stays separable across memory/reference through all later attempts and any final memory-only decoder. Its overlap with a two-qubit Bell state is at most 1/2; histories with no E have overlap at most one. Thus

    F_Bell <= 1/2 + (1/2)(1-p_n)^M + O(delta_n)
           <= 5/8 + O(delta_n).

The actual process has Bell entanglement infidelity at least 3/8-o(1). More repetitions can make the bound approach 1/2 infidelity; no threshold stronger than the displayed number need be claimed. This is now a genuine constant-error polynomial-time attack, not merely an inverse-polynomial error-rate objection.

## 5. Resources and exact scope

At fixed nonzero preparation-noise rate q, p_n=c(q)n^-C(q), so M and the product of M with each attempt's bath size, routing and execution cost are polynomial in n. Constants/exponents may be extremely unfavorable and are not uniform as q tends to zero with n. Fresh random r bits are initially maximally mixed, not pure ancilla gifts. Each attempt's clean workspace is only a probabilistic component of its unconditioned thermal bank.

The new r controls add at most a fixed number of bodies to admitted code-contact gates and commute with K because r has zero gap and is used diagonally. All fixed-gap, bounded-strength, bounded-range and fixed-body qualifications survive; native two-body implementation is still not proved. No gate noise during this driven attack is being added silently.

The result rules out fixed-error exponential-lifetime protection against this broad class of driven, exactly reference-charge-conserving controls with preparation-noised resource banks and admitted energy-resolved code contacts. It does NOT refute the static-H interacting-equilibrium theorem, autonomous storage, a restricted benign-control model, inaccessible-bank restrictions, or an all-memory-sites-exactly-common-noise contract without its separate initial-state argument. The clean counterexample permits zero memory preparation noise and nonzero resource-bath noise, fitting a per-site noise upper-bound class.

No hardware action, publication or external source access was performed. The stronger conclusion is earned by this new reduced-channel/entanglement-breaking construction, not retroactively attributed to the original rare-branch bound.
