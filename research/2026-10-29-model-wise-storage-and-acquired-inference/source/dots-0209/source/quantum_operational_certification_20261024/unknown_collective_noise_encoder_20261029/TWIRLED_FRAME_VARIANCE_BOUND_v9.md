# Twirled uniform-memory bound from singlet frame variance
2026-10-29. New extension, pending independent review. It adds physical logical Pauli twirling; it does NOT replace the earlier untwirled worst-case bound.

Retain the exact full joint collective-algebra deployment promise and ordinary pooled frame learner of v1–v5. Let P be the entire exact singlet sector (dimension d0), E a K-dimensional power-of-two subcode with K>d0/2, and W the product-unitary mismatch between learned and exact frames. Choose signs of local SU(2) lifts so
W=exp(−iH), H=(1/2)Σ_i h_i·σ_i,
with ||h_i||≤π (short rotation vector). Independent local signs change only an irrelevant overall phase. Let hbar=(1/n)Σh_i.

## Exact singlet covariance
The state P/d0 is permutation invariant and collectively rotationally invariant. Thus its one-body Pauli mean is zero and, for i≠j,
Tr[P σ_i^a σ_j^b]/d0=−δ_ab/(n−1).
Indeed rotational invariance makes it a scalar multiple of δ_ab, permutation invariance makes the scalar independent of the pair, and total-spin-zero identity (Σσ_i^a)P=0 fixes the scalar. Consequently
Tr(PH²)/d0
=1/4[Σ||h_i||²−(1/(n−1))Σ_{i≠j}h_i·h_j]
=n/[4(n−1)]Σ||h_i−hbar||².
This exact variance vanishes for a global common frame rotation, as it should.

## Average leakage controls Bell loss uniformly over storage
Let Q=I−P and L=QWE. Since QP=0,
||QWP||F≤||(W−I)P||F≤||HP||F.
The last inequality follows from (W−I)P=−i∫_0^1 exp(−itH)HP dt and unitary invariance of Frobenius norm. It does not assume H commutes with P or that errors are infinitesimal.

Any full joint storage unitary U in the promised algebra has U|P=I_P tensor U0 and no cross-sector blocks. For a normalized encoded logical Bell input and purified independent initial bath,
||(U−I tensor U0)(WE tensor I)|Φ_K,b>||²
≤4||QWE||F²/K.
The ideal physical Bell vector tensored with arbitrary bath lies in the code-return Bell subspace. The squared component of the actual output orthogonal to that subspace is no greater than this squared vector difference. Therefore the completed learned decoder satisfies
1−Fe(Λ_T)≤4||QWE||F²/K
≤4(d0/K)Tr(PH²)/d0
=(d0/K)n/(n−1)Σ||h_i−hbar||²,
for EVERY storage horizon T and every permitted initial bath state independent of the fresh payload. No sampled-current-channel certificate is required for this conditional theorem; it relies on the stronger full joint algebra promise as before.

Now physically apply the fresh retired-key logical Pauli twirl from singlet_dirichlet_certificate_20261029/THEOREM_v1.md. Then
(1/2)||Λ_T,tw−id||diamond=1−Fe(Λ_T),
so the same frame-variance bound becomes reference-complete for the averaged key-retired service. It is NOT a bound for an individual revealed key or for the untwirled channel. Implementation errors and any model-breaking noise are separate.

## Finite pooled acquisition improvement
Earlier SO(3) rounding gives ||Ohat_i−O_i O_1^T||F≤4sqrt(6)e/g for each nonroot site. A rotation angle θ∈[0,π] obeys θ≤[π/(2sqrt(2))]||R−I||F, hence
||h_i||²≤12π² e²/g².
The root mismatch is zero, so Σ||h_i−hbar||²≤Σ||h_i||²≤12π²(n−1)e²/g². Therefore
halfdiamond(Λ_T,tw,id)≤12π²(d0/K)n e²/g²
<24π² n e²/g²≤1944π² n η²/g²,
where e≤9η is the learned pair-block error. Choose
η=g0 sqrt(ε)/(140 sqrt(n)), 0<ε≤1,
with known g0≤g. Since140²>1944π², this gives halfdiamond≤ε and also satisfies the earlier ±SO(3) sign-separation condition for n≥4. Pooled acquisition uses
O(n g0^(−2) ε^(−1) log(n/δ)) full-array calls,
O(n²...) physical preparation/readout, and the same deterministic polynomial compiler plus O(logK) logical Pauli gates and2logK retired key bits per service. The earlier O(n²/ε) frame acquisition for the UNTWiRLED diamond target remains valid and distinct.

A gap-adaptive version can use the earlier confidence lower bound gL and stop when24π² n e²/gL²≤ε, with the same confidence-spending caveats. No gap-free guaranteed runtime is asserted.

## Scope
This extension combines exact singlet-state covariance, the physical mismatch model and an actual service randomization. It does not assume independent frame-estimation errors, does not treat cross-edge data as independent, and does not infer full joint dynamics from local probes. It replaces a worst-case coherent-error estimate by a code-average estimate only because the service is deliberately twirled. The model-free current-channel witness is a separate validation option. Historical novelty and practical advantage remain unestablished.
