# Final normalization for the reusable register comparison
30 October 2026. Root binding clarification to ROOT_MATCHING_REGISTER_COMPOSITION.md, which is preserved unchanged.

MR3 and the dwell comparison construct positive CP/TNI exact-logical comparison maps. Their product is still subnormalized. Therefore the quantity displayed in MR5 is first a bound E_total on the actual physical channel minus the entire good comparison channel. It is not automatically the final distance to a normalized ideal logical circuit.

For the declared logically independent fixed initial auxiliary state, the good product has the form Ad_U_total tensor A_total. After the common final ideal DATA decoder and tracing auxiliary output, its reduced logical map is p Ad_U_total, with 0<=p<=1. Trace preservation of the actual map gives 1-p<=E_total. Thus the normalized logical-channel conclusion is

 ||Out_actual-Ad_U_total||_diamond <=2 E_total,

capped by2. Use this factor two with MR5. No record-conditioned renormalization or division by an unknown success probability is needed. The same bound applies when a known-state boot error is included in E_total.

If uniformity over an allowed auxiliary input space rather than one fixed initial auxiliary state is desired, use the trace-defect argument from STANDARD_FT_SUPEROPERATOR_RECEIVING.md: ||A_total^*(I)-I||<=E_total and duality after partial trace gives the same extra E_total. Do not thereby broaden the native initialization contract to arbitrary initially logical-dependent baths without its own receiving proof.

Alternatively one may complete each auxiliary TNI comparison by a CP failure branch returning a fixed allowed ready auxiliary state, at another explicit norm cost. This is an analysis comparison, not a supplied physical reset of unknown logical data. The simpler final trace-defect bound above is sufficient.
