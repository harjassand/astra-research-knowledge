# Controller-only extension of clean activity witnesses
2026-10-30. Exact finite-support construction for a later full-Hilbert surgery. It does not claim dirty activity drift.

Let X_h be the full-Hilbert finite-support busy witness supplied by the actual fast-return/polynomial construction. Suppose

    c P_h<=X_h<=C P_h,    [X_h,P_j]=0,

where P_h are the actual BUSY projectors, and its restriction to the all-good forest range is controller-only. The latter follows from the exact clean controller closure; it is not inferred for malformed masks.

All actual history flags B_j and BUSY projectors P_j are pure-controller observables in the full forest frame. Let E_B be pinching in every commuting B_j that touches the current finite support, with the bounded support enlargement needed to include those flags. Let E_DATA be normalized partial trace over the finite DATA support, tensor identity on that support. Both maps are unital CP conditional expectations. Define

    Xbar_h=E_DATA E_B(X_h).

Then:
1. Xbar_h is Hermitian positive, finite-support and CONTROLLER-ONLY on the entire Hilbert space.
2. cP_h<=Xbar_h<=CP_h, by positivity and because both expectations fix P_h.
3. Xbar_h commutes every actual B_j and every P_j. Pinching establishes the first; the second is preserved because all pinching projections and E_DATA commute the pure-controller P_j.
4. On the all-good range, Xbar_h has exactly the same restriction as X_h. Pinching does nothing there. Since the all-good projector is pure-controller, E_DATA commutes with its compression; the clean compressed operator was already DATA identity.
5. The construction is dilation/reference stable and does not reconstruct or reset the retained physical bath. E_DATA is only a mathematical extension of a proof observable.

There is deliberately NO assertion that L0* Xbar_h<=-P_h on dirty sectors. That inequality may be lost. The clean buffered calculation survives; the already earned uniform history-B drift is intended to pay the dirty difference in a linked local-surgery argument.

Consequently positive local activity gates built from Xbar_h, and pair gates P_j Xbar_h, commute every raw animal f_A (DATA syndrome and actual B-token polynomial), globally—not just on clean states. This removes a gratuitous DATA-noncommutation complication from the animal-local circuit comparison. It does not by itself complete the required weighted dirty-error or useful-service estimates.
