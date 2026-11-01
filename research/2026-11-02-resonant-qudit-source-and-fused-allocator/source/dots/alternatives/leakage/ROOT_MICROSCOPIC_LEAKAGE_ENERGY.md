# Root microscopic leakage-energy construction (pending audit)

2026-11-01. Reconciles the independently originated Raman parity latch after its first artifact was frozen. This is a proposed occupation-charged admission, not a completed refresh/memory theorem.

## Obstruction actually measured

For the w=4 finite latch, endpoint-only decay leaves high intermediate modes with gap much smaller than J. Cleanup at rate delta~J restores a gap of order J in the isolated numerical model, with actual stationary cleanup flux of order J eta^2. But a cleanup-count Poisson observable has O(1) spectral range even as eta goes to zero: one initially loaded intermediate excitation must cause about one cleanup fault. Small stationary flux alone is not an operator-uniform small-cost certificate.

That O(1) cost need not rule out a memory proof. Treat leakage as genuine error debt with its own negative restoring drift and charge initial leakage, rather than demand its entire positive maximum vanish.

## Microscopic energy witness

For the small-dimension apparatus model, let N sum intermediate-level projectors (not endpoint levels). Write the actual static Hamiltonian as

  H=Delta N+V_boundary+V_middle+H_low.

Boundary terms connect intermediate levels to low ground/endpoint states, with norm scale g; middle terms connect intermediate levels, with bounded graph degree. Set eta=g/Delta. Assume the finite Stark counterterms and reference edges obey ||H_low||_local<=C eta^2 Delta, as the Schur-complement tuning does for bounded weight w>=2. All data factors are norm-one Paulis; overlapping checks are allowed.

Local completion of squares gives, for sufficiently small eta and fixed degree,

  (1/2)N-C0 eta^2 n I <= H/Delta
      <= (3/2)N+C0 eta^2 n I.

The middle terms are bounded by O(eta)N. For each boundary edge use
  +/- (g/Delta)(|v><l| tensor P+h.c.)
       <= epsilon Q_v+(eta^2/epsilon)Q_l.
Choose epsilon as a fixed small inverse-degree constant and sum. No commutation between distinct Hamiltonian terms is needed. Therefore

  E=H/Delta+C0 eta^2 n I

is positive, E>=N/2, and E<=3N/2+2C0 eta^2 n I. It is a sum of local terms with an explicit identity offset. [H,E]=0 EXACTLY.

Let every intermediate level have cleanup jump sqrt(delta)|g_c><v_cj|, and endpoints have the specified decay rate kappa. The cleanup action on Delta N is -delta Delta N. On a boundary edge it contributes -delta/2 times that edge; on a middle edge -delta times the edge. Endpoint decay adds bounded boundary coherences and low-level terms. Ground Stark energies injected by cleanup and endpoint decay are O(eta^2 Delta), not silently zero.

The proposed global operator bound, to check term by term, is

  L* E <= -(delta/4)N
           +C1 [ (delta+kappa)^2/delta ] eta^2 n I,

for delta,kappa of comparable positive order, with additional C kappa J/Delta absorbed into the same floor when J/Delta=O(eta^2). It follows from the exact dissipator action above and Young inequalities on every boundary coherence, not from an effective generator. In particular delta~kappa~J yields

  L*E <= -c_E J E+C_E J eta^2 n I.

This persists at the level of operator inequalities for arbitrary intermediate populations and coherences. A physical perturbation that injects excitation is separately charged through its action on E; finite reservoir upward rates are not free.

## Paying cleanup-induced data disturbance

In the exact controlled-prefix frame, each intermediate cleanup applies a bounded partial-check Pauli. If it can increase a protected base potential W by at most D_W, then

  L_cleanup* W <=D_W delta N.

A sufficiently large FIXED coefficient multiplying E pays this term using its negative N drift. The resulting extensive floor is O(delta eta^2 n), rather than O(delta n) from treating all cleanup as unconditioned faults. This is a genuine resource-flow mechanism if the displayed operator inequalities are verified.

Unlike the bounded-Z dilute-clock construction, the full potential need not satisfy V<=W+o(1)n uniformly on arbitrary hot apparatus states. Its leakage part has its OWN restoring drift. Require a sufficiently small INITIAL exponential leakage moment, or an explicitly prepared admitted low-energy subspace. One cannot replace that requirement by a small initial mean or claim arbitrary unencoded hot apparatus is safe.

## Still missing

This energy certificate does NOT earn conditional cache refresh in the full overlapping Raman-latch network. It only prices leakage and cleanup faults. The useful cache observable must be constructed from the actual microscopic generator, with harmful overlap terms controlled relative to J. Large Stark shifts commuting with the cache should not be charged as if all their norm caused report errors, but that observation alone supplies no refresh theorem.

The alternate dump-level cleanup developed by the independent constructor coherently undoes prefixes, making its ideal jumps dressed-logically benign, at dimension4w and potentially driven reservoir cost. Compare both routes against active extraction with the same couplings, dimension, reservoirs and faults. Neither isolated gap nor low stationary fault flux is a complete memory admission.
