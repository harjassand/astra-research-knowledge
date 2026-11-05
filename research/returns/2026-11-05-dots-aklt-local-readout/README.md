# Exact local square-AKLT spin-correlation readout

The supplied, internally reviewed operation estimates a specified infinite-lattice equal-time spin correlation using exact local classical loop samples. It avoids burn-in, an enclosing-volume simulation, finite-box extrapolation, a loop-length cutoff and a separately estimated partition-function denominator. The mathematical guarantee assumes independent ideal fair bits; the reproducible execution uses a seeded pseudorandom generator.

Read the [producer's complete result](package/RESULT.md), [local sampling theorem](package/square_aklt_local_sampler_20261105/LOCAL_SAMPLING_THEOREM.md), [exact construction and physical join](exact-local-operation.md), [executed evidence, audits and costs](evidence-and-costs.md), [original ZIP](original/square_aklt_local_readout_release_20261105.zip), [complete visible update](DOTS_SQUARE_AKLT_LOCAL_READOUT_20261105_RETURN.txt), and [provenance](SOURCES.json). Only the capture header's local ZIP locator is replaced by its equivalent public archive path. No prompt or scientific text is changed.

## Exact physical target

The model is the square-lattice spin-2 AKLT projector Hamiltonian, with unit spin-4 bond-projector coefficients. The target is the pair-correlation limit of expanding open regions with virtual-identity boundary mixtures

```text
sigma_R=V_R I_boundary V_R^dagger / Tr(V_R I_boundary V_R^dagger).
```

This is a selected mixed ground-space boundary state. It is not every pure boundary state or an arbitrary-boundary uniqueness theorem. The operation samples a classical norm-loop gas and computes an observable of this limit; it does not prepare a quantum state, sample its general measurement outcomes, prove a quantum spectral gap, or compute dynamical/static Kubo susceptibility.

## Completed fixed-budget result

For distinct nearest-neighbor sites, the supplied run gives

```text
<S_0 dot S_(1,0)> estimate = -3.559889190566645
Outward-rounded 95% interval = [-3.569890, -3.549889].
```

The [full result JSON](package/square_aklt_local_sampler_20261105/physical_local_infinite_precision001.json) retains exact rational endpoints and half-width 0.009999995258. Coverage at least 95% is a mathematical Monte Carlo statement under the ideal independent-bit interface, rather than a deterministic enclosure or a physical certification of the seeded PRNG.

The budget was fixed before observing sample means: 542,236 complete attempts, seed 2026110501, with 463,946 non-null paths requiring independent local queries. Elapsed producer computation was 722.901 seconds plus 0.106 seconds setup, about 12 minutes 3 seconds on its shared execution host. Capital did not rerun this computation. The largest observed ancestor clan had 35 cylinders and longest observed loop 104 edges; these were observations, not cutoffs.

## Operation and finite confidence

Every routed open path p has activity `a_p=3^(-L_p)(3/5)^r_p`. A rational proposal gives it probability a_p/C, with null output for unused mass. For a non-null path, independently sample the joint accepted loops touching all its vertices and return

```text
X=9 (-1)^parity(i,j) C product_(gamma touching p) delta(p,gamma).
```

Edge overlap makes delta zero; otherwise each shared vertex contributes 3/5. Null paths give 0. Endpoint revisits and self-contacts are retained by the audited activity. For fixed sites the estimator has deterministic range width 9C, where the nearest-neighbor majorant is `C=301805115576299/500964985405440`.

Independent complete attempts give Hoeffding half-width `9C sqrt(log(2/delta)/(2n))`. Rational log/square-root enclosures round outward. The normalized perfect loop draw incorporates the denominator directly. Coupling through one master Poisson process makes sufficiently large open boxes eventually agree on the finite queried clan and source path; bounded convergence identifies the selected thermodynamic pair limit without a boundary extrapolation.

The physical factor 9 applies to distinct spin-2 sites. Same-site `S_i dot S_i` is 6; one cannot reuse the distinct-site formula at i=j. SU(2) invariance makes the same-axis zz correlation one third of the distinct-site dot correlation. The [physical correlator audit](package/independent_audit/PHYSICAL_CORRELATOR_AUDIT.md) checks this join separately.

## Earned consequence and comparison

The technical operation combines an executable exact all-length intersecting-loop oracle, parameter-specific all-loop subcriticality, consistent local Poisson revelation and bounded independent physical readouts. Loop representations, ancestor perfect simulation and physical loop observables are established machinery. Published worm and valence-bond loop Monte Carlo are strong practical comparators; no matched speed advantage over them is demonstrated. The reported 67-fold improvement concerns only this project's earlier global exact implementation on a 32x32 pilot.

The current result and completed local audits govern the operation. Historical global-sampler audits in the bundle describe an earlier implementation that lacked this local interface; their old implementation limitation is not the current status. The [evidence page](evidence-and-costs.md) preserves the earlier statistical anomaly and fixed follow-up rather than hiding them. No historical-priority, practical QMC speed record or civilisation-changing capability is established. Capital ran no source program, numerical replay, new scientific audit or heavy corpus build. Generated current retrieval was not rebuilt.
