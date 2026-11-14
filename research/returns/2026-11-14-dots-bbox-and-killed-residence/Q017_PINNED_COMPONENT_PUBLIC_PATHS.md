# Exact pinned-component thermal source acquisition

Implemented `Core.sample_given_component(S)` returns the exact full-core Gibbs law conditional on the specified setS being an ENTIRE augmented plus component. This is not conditioning only on the sitesS being plus, because that would allow larger components extendingS. The suppliedS must satisfy the chosen original core graph and box rule.

Algorithm: start with pinnedS, generate the same unconditioned Poisson polymer proposal as before, and reject if any retained polymers touch or overlapS or one another. The probability of a compatible background familyF is proportional to product_{T∈F}z(T). Under the desired conditional Gibbs law the factorz(S) is fixed and cancels. Thus rejection samples exactly the required thermal background without waiting forS to appear spontaneously. The empty background proposal guarantees acceptance>=exp(-Γ), so expected attempts<=expΓ<1.00000011 at either explicit box convention. Activity exp(-8P(S)+|S|/25) can be astronomically small; it does not appear in acquisition cost.

Moreover, letZ_allow(S) be the partition function of compatible backgrounds, with all-minus weight normalized to1. Then

P_μ(S is a component)=z(S) Z_allow(S)/Z_A.

Because1<=Z_allow(S)<=Z_A<=expΓ,

z(S)exp(-Γ)<=P_μ(S is a component)<=z(S).

This provides a relative-width<=expΓ certificate for this rare equilibrium source event. For a fixed6×6 square atbox_sites6, P=24,a=36 andz=exp(-4764/25)=exp(-190.56). The conditional sampler handles this event without an exp(190.56) rejection penalty. This is ordinary polymer conditioning, not claimed novel or a rare physical transition breakthrough.

Executed tests:1000 draws each for a wrapped nearest-neighbor pair, a permitted diagonal pair, and full6×6 square; every draw accepted first attempt with empty thermal background. The outputs remain valid full conditional samples, because the proposal includes all possible allowed background polymers. Tests do not empirically resolve the rare nonempty-background tail. Receipts:pinned_tests.json.

Use in source-flux importance: these conditional laws supply accurately normalized seed channels. They do not determine their continuation probabilitiesq(x), nor do they cover the entire source unless a partition or overlap-corrected mixture over seed events is explicitly constructed. Summing arbitrary pinned-channel contributions double-counts configurations with multiple components. No such sum, polynomial physical continuation cost, or full flux acquisition is claimed.
