# Independent verification of root's product-Gibbs alternative

Root supplied this alternate probability route; verified independently here. It changes the scope of the earlier removable-component obstruction, but does not fill the explicit-family decoder/contraction gate.

Let C≤F_2^m be any binary linear valid-syndrome space. Give s∈C weight ∏_i q_i^{s_i}, with 0≤q_i≤1. For any coordinate set T,

    Pr[T⊂supp(s)] ≤ ∏_{i∈T}q_i.

If the all-one T fiber is empty, the statement is immediate. Otherwise its rest-coordinate fiber is C0+v, where C0 is the rest-coordinate subspace of the all-zero T fiber. Its weight is q_T Z(C0+v). Fourier expansion gives

    Z(C0+v) = |C0|/2^r Σ_{u∈C0⊥} (-1)^{u·v}
                         ∏_j [1+(-1)^{u_j}q_j].

All factors before the coset sign are nonnegative, so Z(C0+v)≤Z(C0). The full partition function contains at least the all-zero T fiber, of weight Z(C0). Division proves the claim, including q_i=0 or1 by continuity/direct inspection.

For a commuting stabilizer Hamiltonian with positive stabilizer penalties, allowed syndrome sectors have equal dimension and the induced Gibbs measure has exactly this product weight restricted to C. Thus the event bound is available even if the indicator of T is not itself a valid syndrome/coboundary. A connected witness can be counted using occupied-site suppression without physically removing it.

Consequently the earlier central-singleton metacheck example obstructs the *source-style removable-witness map* and naive decoder component restriction. It does NOT obstruct all commuting Peierls proofs. A new commuting proof can avoid the removability premise for its probability estimate. It still needs an actual explicit-family decoder, bounded dependency history, and a proof that logical failure forces a sufficiently large occupied-site witness.

The lemma is not automatically valid for generic weakly perturbed/noncommuting weights or the full native thermal join: integrating interactions need not leave a restricted product measure or nonnegative Walsh coefficients. Those transfers require their own proof and are not claimed here.
