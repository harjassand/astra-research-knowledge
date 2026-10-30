# Weighted coverage margin for animal-local activity circuits
2026-10-30. Imports the accepted SSF/FGL full-animal coverage proof and its strict parameter margins; does not assert a new confinement theorem.

Use one global finite coloring/order of the local activity gates. Adding a connected patch D of m vertices changes O(m) selected gates. After finite-depth cancellation,

    exp(-C delta m) G_A <= G_(A union D)
                              <=exp(C delta m) G_A.   (1)

This remains true for LARGE component containers, not only bounded move footprints. Also I<=G_A<=exp(C delta |A|)I. Constants depend on fixed radii/degrees and not on A,m,N.

The original full-animal coverage proof has two distinct uses of weight comparison:

1. Bounded actual-move completion A->A union D_h. Equation (1) costs a fixed factor exp(C delta |D_h|). Retune the original R_move strict inequality to retain at least its declared fixed negative fraction. This gives nonnegative D_h^G and the same strict paying-animal charge, with modified fixed constants.
2. Completion by one poor reduced-error component/container. If the original comparison has a positive exponential-in-component-size margin after its entropy/preimage bound, (1) subtracts at most C delta times the container size from that exponent. Container size is bounded by a fixed multiple of component size. Reserve half the original positive exponent margin and choose delta below the resulting fixed bound. No multiplication by the total number of components is introduced.

Sparse animals acquire at most exp(C delta |A|); reserve the same positive sparse-entropy summability margin before choosing delta. Their weighted sum remains O(N)I.

For an explicit operator justification, fix a raw syndrome sector and any controller vector u. The scalar coefficients g_A=<u,G_A u> are nonnegative and satisfy every ratio bound (1). Every completion, preimage-count and sparse summability step of the imported proof therefore applies to f_A g_A with the retuned margins. The resulting inequality holds for every u, hence is a Loewner inequality. No simultaneous diagonalization of the G_A is required.

Thus the accepted clean-basin coverage becomes

    sum_h D_h^G >= c_cov W_G-b_cov N I,

with fixed positive c_cov and finite b_cov. The all-good sector has no occupied history-B tokens; when those tokens are retained as empty vertices in the graph, the same enlarged-graph constants from the accepted coverage source are used. Arbitrary occupied dirty flags require the separate full dirty coverage/surgery and are not included here.

With delta=d epsilon^2, it suffices to choose epsilon small enough to meet the already fixed margin bound. Confinement scale, canonical decoder and logical interface are still the imported ones, not newly proved by this weight comparison.
