# Coherent repeated-storage cluster bound: candidate derivation

28 October 2026. **Candidate, pending independent review.** Dependencies: actual flagged EC construction and checked one-fault/common-span properties in `flagged_five_qubit_storage_round_20261028.md`. This is a finite-time fault-tolerance composition argument, not a novelty or threshold claim. The goal is to avoid both a fictitious ideal decoder between rounds and a stochastic-mixture assumption.

## Additional interfaces required

Use one fixed code embedding C and an ideal encoded memory cycle A. Its actual noiseless EC is the early-exit flagged gadget, with physical corrections and reset/reused ancillas; all records are discarded or made inert before the next cycle. Require:

1. A maps **arbitrary data input** to the code subspace and A C=C (notation C denotes the encoding channel). The perfect-code syndrome correction does this: measuring a nontrivial stabilizer triggers a fresh full syndrome pass and correction to the code; all four trivial outcomes project onto the code. The Pauli-span argument extends this to arbitrary data states entangled with a reference.
2. A corrects the whole weight≤1 error span of encoded inputs and preserves their logical state. Its ideal receiver stage must not spread an incoming correctable error outside that span. This is automatic for an ideal identity receiver, but must be established for any compiled nontrivial ideal receiver.
3. Every single faulty local slot in a cycle, on an ideal encoded input, is corrected by the **next actual fault-free cycle**. A fault-free final decoder D also corrects it. The checked EC property plus the receiver isolated-fault support premise establishes this.
4. An actual ordered local-CPTP circuit model, including branch-uniform conditional slot bounds, not merely reduced marginals or an uncontrolled common bath. No classical record from one cycle may alter later controls except through an interface included in the analysis. Discarded ancillas/environment do not re-enter later cycles. Persistent spectator reference systems are permitted, because the correction statements are complete-channel statements.
5. Fixed mathematical potential-slot unrolling as in the gadget note: EC has 751 potential locations with exact zero-duration identity bypasses on inactive branches. Add all receiver/storage locations. Physically waiting through disabled slots requires new charged and checked idles.

Initial encoding/injection C and terminal D below are ideal *interfaces for the logical metric*, not supplied hardware. Real one-off interface errors must be added separately.

## Algebraic cancellation lemma

Expand cycle t at its microscopic slots as

    N_t = A + S_t + M_t,

where S_t is the sum of terms with exactly one local difference Δ_{ti}=actual−ideal, and M_t sums terms with ≥2 differences. A is CPTP and A²=A. For each individual singleton term B_{ti}, condition 3 and linearity give

    A B_{ti} C = 0,       D B_{ti} C = 0.

Since A has range in the code, A B_{ti} A=0 and D B_{ti} A=0. Therefore any term in the T-cycle product whose selected nonideal cycles include an **isolated S_t** vanishes: its immediate neighboring cycles are A, or an encoding/final decoding boundary supplies the corresponding C/D. Earlier complicated errors do not invalidate cancellation because the preceding actual fault-free A maps arbitrary states back into the code.

This is why a code-space-reset property on arbitrary inputs, not only correctable inputs, matters here. No ideal decoder has been inserted between actual cycles; A is their actual zero-fault physical recovery operation. For time-dependent ideal cycles the corresponding cross-cycle annihilation identities must replace A²=A.

## Positive cluster majorant

Suppose every cycle obeys

    r = sum_i epsilon_i,
    a = product_i(1+epsilon_i) − 1,
    b = a − r,

where ||Δ_{ti}||_diamond≤epsilon_i uniformly over enabled branches; inactive branches have zero difference. Then ||S_t||≤r, ||M_t||≤b, and ||S_t+M_t||≤a. The bounds include all potential locations, not only the ideal clean trajectory.

Group a nonzero expansion term by maximal runs of consecutive occupied (non-A) cycles. An occupied cluster of length one contributes only M and therefore has norm at most b. A cluster of length k≥2 has norm at most a^k. Different clusters are separated by at least one A cycle, whose norm is one. Hence the logical error norm is bounded by the sum of products of these positive cluster activities over nonempty disjoint separated cluster collections.

Dropping the exclusion/separation restrictions overcounts this sum. There are at most T possible starts for each length. Thus, for a<1,

    || D N_T ... N_1 C − id ||_diamond
       ≤ exp( T [ b + a²/(1−a) ] ) − 1.

Cap the result at 2. The sum over all length≥2 activities is a²/(1−a); length-one activity is b. One can retain the finite-T sum instead of the geometric tail. For small r, a=r+O(r²), b=O(r²), so the bound is O(T r²) in its useful regime. Unlike exp(T r)−1−Tr, it does not pay first-order accumulation from isolated correctable events.

This derivation permits coherent local errors within the actual ordered CPTP model. It does not interpret diamond differences as probabilities. It does not allow persistent environmental memory to travel between cycles outside the specified operation interfaces. The conservative location count can make the bound practically weak; no useful hardware threshold or demonstrated memory lifetime is asserted.

## Obligations before acceptance

- Independently verify the cancellation identities at the full channel/instrument interface, including inert treatment of old classical records and discarded ancillas.
- Confirm arbitrary-input noiseless code-space reset for the exact implemented adaptive instrument, not just a statewise Pauli statement.
- Challenge the positive cluster overcount and boundary cases T=1,2.
- For any actual learned-frame/native receiver, prove the stated residual-span-preservation and isolated-fault support contract. The generic note does not automatically supply it.
