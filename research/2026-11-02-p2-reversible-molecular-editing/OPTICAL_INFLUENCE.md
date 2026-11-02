# P2 physical influence ledger: a route to earn collateral limits
**Scope:** conditional, optical-geometry and hazard-accounting construction, not measured Action-PAINT device constants. Part of P2's separate joint-phase branch (2026-11-02).

## Motivation
A bound on collateral chemical errors c cannot be read from a handful of error-free experiments in the presence of P1's rare hidden persistent modes. Instead ask whether any wrong-site chemistry requires external photons that can be bounded **for all physical modes** by a calibrated incident photon budget. This does not reprogram or log thermal Brownian noise.

## Derivation
Let source address j be targeted with an actual illumination command, and let I_j(r_i,t) denote externally measured or separately electrodynamically bounded intensity at untargeted site i. Suppose each NEW wrong-site edit at i requires at least one photon-triggered reaction, and the conditional reaction intensity, even after an arbitrary retained chemical history, is everywhere bounded by
  lambda_i(t|H) <= kappa_i I_j(r_i,t)/(h nu).
This requires **physically qualified** kappa_i (e.g. maximal chromophore count and bound on absorption cross section and quantum yield), NOT a finite set of negative assays. There must be no unaccounted chemical dark process, chain reaction or transported photoproduct; otherwise their hazards must be added.

With Phi_j(r_i)= integral I_j(r_i,t)/(h nu) dt, the conditional expected number of off-target changes is at most kappa_i Phi_j(r_i). Since every unintended change requires at least one event:
  P(new incorrect i | any reachable H) <= min(1,kappa_i Phi_j(r_i)).
By conditional expectation and summation,
  c_j <= sum_(i != j) min(1,kappa_i Phi_j(r_i)) + c_dark + c_indirect.
This is a source-physics route to the c parameter in P2's same-scaffold edit drift theorem E[tau] <= D0/(s-c), conditional on earning the actual bounds and a nonzero target-correction s. It is not a measurement or a new probability theorem.

**Illustrative geometric screen**: for 64 addresses on an 8x8 lattice with 20nm pitch, hypothetical Gaussian intensity I(r)/I(0)=exp[-r²/(2sigma²)], sigma=150nm (NOT measured for the paper), the sum of relative exposure at the 63 other sites from a central commanded write is 57.1574. Under a hypothetical uniform per-full-target-dose upper reaction coefficient q0, collateral c <= 57.1574*q0. With hypothetical successful edit s=0.72, the sufficient positive drift requires q0 <0.01260. There is no source evidence that actual q0 meets this gate. With a uniform background illumination fraction f on each other site, add (N-1)*f to the relative sum, so the scaling benefit disappears if f stays fixed. Sequence-selective invading-strand chemistry or actual field-confinement is indispensable at dense spacing.

**Source and prior art:** Liu/Dai et al., *Action-PAINT*, Nature Chemistry 2019 DOI:10.1038/s41557-019-0325-7 (405nm gated CNVK; ~350ms optical feedback; the source reported no independent multi-grid spatial light control). Nakamura/Kawabata/Fujimoto, ChemBioChem 2016 DOI:10.1002/cbic.201600236 (>80% 366nm+sequence-specific invading-strand splitting on its particular chemical system). These do NOT jointly warrant a successful 64-site c. Source verification of on- and off-target bonding must precede scaling, and a finite no-event test cannot rule out rare catalytic photochemical channels.

**Falsification:** If a nearby correct labelled address loses its bond under the command to erase a different incorrect address, measure and charge that rate along with photobleaching, dark chemistry, global 405/366nm exposure, diffusion and specimen destruction. If c>=s under the source, the edit-count theorem has no positive guarantee. A strong ordinary same-instrument optimal controller can use identical dose bounds and may outperform a greedy editor.

Local extended reproducible artifact includes optical_locality.py (deterministic Gaussian point spread response sum) and exact_repair.py; the present GitHub branch also contains the exact rational small-state edit verifier.
