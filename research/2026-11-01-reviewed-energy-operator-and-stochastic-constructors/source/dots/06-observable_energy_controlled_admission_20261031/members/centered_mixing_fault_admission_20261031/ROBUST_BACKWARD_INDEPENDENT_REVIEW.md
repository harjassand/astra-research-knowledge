# Independent review: robust backward reference weight

31 October 2026. Whole mathematical PASS on `ROBUST_BACKWARD_OBSERVABLE_COROLLARY.md`, SHA256 `e2c7a9a80aad1bca93a50cfee8b29b2c3bb0d44679aa8675a0d0f8bdc10a5ad6`, after full read. Its exact parent is f2d89255..., independently received in `BACKWARD_CONTROLLED_INDEPENDENT_REVIEW.md` (SHA212a0918...). This is a separate corollary; no frozen earlier theorem or executable receiver is silently changed.

The reference integral uses ONLY data controls/instruments and scalar exp(-r(s-t)), not an assumed approximate source evolution. It is Hermitian, norm at most2c/r, and terminal zero. Its backward equation has the stated minus-r term. At an instrument its pullback is exactly the same unital CP adjoint as for the exact theorem.

For constant source-only G, commutation with every data control permits (G*+r) to pass into the future integral. This gives the displayed F(t) in terms of the ACTUAL J(s). Integrating its norm uses
integral_a^s exp(-r(s-t))dt <=1/r,
so the total is at most2d_J/r. No inverse source generator, experimental decay fit, or physical implementation of the reference weight has been assumed.

The tilted weighted expression adds yF(t) to the quadratic remainder from the parent theorem. Since V>= (1-q)I and q<=1/2, this adds at most2R integral||F|| to the squared-norm exponent, hence at most2R d_J/r to the norm exponent. Products over disjoint patches, endpoint factor sqrt(1+q), local instrument interfaces, retained source reuse and positive-degree Cauchy extraction are unchanged. Thus the displayed eta_J is valid on the same initialized-field input domain, including arbitrary finite source/data/reference correlations.

The fixed source-generator condition is essential: with time-varying G, applying G_t* to a future K(s) does not give J(s) defined using G_s*. The document explicitly rejects that unproved transfer. Source-blindness, fixed compatible supports and actual within-patch imperfections remain indispensable, as in the parent theorem.

A freely chosen large reference r is not a physical escape: source-independent K0 has J=rK0 and retains its ordinary integrated strength. The one-variable minimum of exp(hR)/(R-1) is correctly h exp(1+h) at R=1+1/h for h>0; it is explicitly a floor of this sufficient expression, not a lower bound for every physical mismatch. The bias versus detuning distinction is sound. As usual, the exact zero-coupling branch is handled by the parent convention without division.

No correction found. This establishes a known-model robust certificate without ideal-control variation cost; it does not acquire an unknown physical generator, certify the local master equation under hardware operation, create a gate, or establish novelty/practical advantage. Root's separately reported numerical diagnostics are outside this mathematical receipt.
