# A rigorous physical-time inclusive fault-insertion contract

2026-10-29. This is a constructive retained-bath / nonunitary-noise contract for the **actual physical evolution**, with its completed-reset record retained. It is not yet a proof that an autonomous quantum code corrects the resulting faults. The missing conversion is identified exactly below.

## Model and locations

Work on the actual data+controller+bath Hilbert space, not an effective eliminated generator. Let L_0(t) be the clean guarded-channel generator plus arbitrary bath-only evolution. The noise is

    N(t)=sum_e [-i h_e(t), .] + sum_a D[M_a(t)].

Every h_e is bounded, with bounded system support but possibly a common retained bath. Every M_a has bounded system support and is bounded. Allow time dependence and arbitrary system-bath initial correlations. Infinite-dimensional baths require existence of the joint propagators; use an interaction picture or finite approximants for unbounded bath-only dynamics. No bath reset is used.

Partition physical time into deterministic slabs of length T. Partition the local noise terms among fixed spatial anchors, with each anchor's terms supported in a fixed-radius system neighborhood. A physical-time fault location j=(anchor, slab) denotes its assigned noise generator N_j(t), zero outside that slab. Assign each term exactly once, rather than counting one insertion as multiple locations. Define

    epsilon_j=integral ||N_j(t)||_diamond dt
              <= integral [2 sum_e ||h_e(t)|| +2 sum_a ||M_a(t)||^2] dt.

The diamond norm is on the full augmented system-bath map (and arbitrary reference), not a reduced-system Markov approximation. Assume epsilon_j<=eta T. The clean generator need not be small, have a spectral gap, mix, or be independent among clocks.

Crucial physical condition: multiplying any selected N_j by any number z_j in [0,1], while keeping all other terms fixed, leaves a legitimate CPTP generator. This holds for the Hamiltonian and added-Lindblad model above. It need not hold for arbitrary signed differences of calibrated generators; the root defect theorem's broader perturbation class is not silently inherited.

## Inclusive fault map and theorem

For a finite selected set S of physical-time locations, let E(z_S) be the full physical propagator over the experiment, with all unselected noise present at full strength and selected N_j multiplied by z_j. Define

    F(S)=sum_{A subset S} (-1)^(|S|-|A|) E(1_A).

Then

    ||F(S)||_diamond <= product_{j in S} epsilon_j <= (eta T)^|S|.    (2)

In a formal Dyson expansion around L_0, F(S) is exactly the sum of paths having at least one noise insertion from every specified location in S, with arbitrarily many additional insertions anywhere. Thus (2) is the standard *inclusive* coherent fault-path currency, not a claim that fault paths are probabilities or independent. It is uniform in total volume and runtime outside the selected locations.

### Proof

The multivariate fundamental theorem of calculus gives

    F(S)=integral_[0,1]^|S| (product_j partial_zj) E(z) dz.

Duhamel's formula expresses the mixed derivative as a sum over all temporal orderings of |S| inserted maps N_j(t_j), with the interpolated full propagator between consecutive insertions. Every intervening propagator is CPTP and has diamond norm one, because all z are in [0,1]. Apply submultiplicativity to each integrand. The time-ordering simplices, summed over permutations, partition the product integration domain (coincident-time boundaries have measure zero). Therefore the bound is precisely

    integral product_j ||N_j(t_j)||_diamond dt_j
      = product_j epsilon_j.

No factor growing with total number of unmarked locations appears. Summing the absolute values of the entire Dyson expansion instead would introduce such a factor and lose the threshold-compatible bound. The CPTP interpolation is what avoids that mistake.

## Completed channels and their real order are retained

The same theorem applies to the joint output consisting of physical quantum state plus the full classical **downward-reset time/location record**, with Kraus labels either retained or summed. This follows by taking the ordinary quantum-jump instrument of the fixed clean downward resets and adding a classical record register. For every z, the summed record instrument is CPTP. The Duhamel argument inserts N_j on the physical state while preserving already-produced records; its norm bound is unchanged. Finite time bins followed by refinement give the continuous record version.

Consequently the contract does not replace the actual correlated clock history by iid clocks, average progress, or a nominal synchronous gate order. On the zero-noise clean invariant sector, the root intertwiner says the recorded channels implement their exact completed-channel order. After insertions, the physical state and the actual records remain the objects bounded by (2), even if the state leaves that sector. Trace out the bath only at the end if desired; contractivity preserves (2).

Restricting to a particular event in the classical record is a trace-nonincreasing CP postprocessing and cannot increase the bound. **Renormalizing by that event's probability can increase the bound arbitrarily.** Thus (2) is not a uniform conditional-noise theorem for each realized clock schedule.

## What this establishes, and the single remaining semantic obstruction

Equation (2) already accommodates bounded local Hamiltonian noise with a retained, common bath and bounded local nonunitary noise. It supplies the honest physical-time fault-insertion representation the controller results were missing. A bounded-depth physical-to-abstract frame preserves bounded support up to a constant radius, and preserves Hamiltonian operator norms.

However, a physical-time insertion is not automatically a single faulty **completed data channel**. It can leave a corrupted controller whose later resets enact wrong channels, while eligibility delays can allow extensive storage damage. The interval counterexample in DATA_EXPOSURE_COUNTEREXAMPLE.md proves that discarding physical-time extent and charging only successful-update indices is unsound even for independent Poisson clocks.

To invoke a standard circuit/exRec theorem one still needs a deterministic correctness statement: for every physical fault cluster satisfying a stated geometry (and every allowed clock record), all data outside a bounded, charged neighborhood follow the intended fault-tolerant channel circuit, including entry/exit of corrupted controller sectors. Or one must prove an autonomous decoder threshold directly for (2) plus the actual clock instrument. Neither statement is obtained from equal-time B flags, single-clock liveness, or the joint no-emission bound. In particular, the record instrument itself may correlate an unmarked data update with a remote marked clock fault through a long eligibility dependency cone.

This is a precise partial bridge, not a claimed quantum-memory threshold. It isolates the unresolved task as fault **semantics and correction**, rather than the existence of a retained-bath, nonunitary physical-time fault expansion.

## Standard comparison

The norm-and-Duhamel mechanism is conventional, not claimed novel: compare Terhal–Burkard, https://arxiv.org/abs/quant-ph/0402104, and Aliferis–Gottesman–Preskill, https://arxiv.org/abs/quant-ph/0504218. Its useful specialization here is to the full guarded-clock CPTP dynamics and its completed-reset record, without eliminating controllers or resetting the environment.
