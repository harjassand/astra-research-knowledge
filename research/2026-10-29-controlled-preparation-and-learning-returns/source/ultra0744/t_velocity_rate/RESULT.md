# Constructed: normalized iid hard-sphere output at every finite time

The missing rate-dependent operation is a positive conserved-currency lineage.
Use h(v)=a+|v|^2 and g_t=hf_t/(a+e0). A recursively sampled collision partner
is drawn from g_s, the actual |v-w| rate is accepted under an explicit local
clock, and either outgoing particle is selected in proportion to its conserved
h. This makes the transformed evolution genuinely Markov/probability-valued.
Final acceptance a/h returns the physical f_t law, with mean proposal count
(a+e0)/a, exactly two for a=e0.

PROOF.md closes almost-sure termination and finite expected full-tree cost
without assuming a partner-law oracle. An explicit pairwise clock drift pays
the unbounded-rate interface. Initial source support is a source assumption,
not a cutoff on evolved velocities. A fourth-moment calculation gives an
exponential-in-time work bound; no uniform-time efficiency is claimed.

This changes the output contract of the nearest exact ordinary construction:
Fournier's established hard-potential recursion has a random multiplicative
mass, whose second moment is not established there. The constructed output
instead has weight one, so iid bounded tests have ordinary explicit Hoeffding
guarantees. Generic recursion, conserved-quantity weighting and energy packets
are credited prior; historical novelty remains UNKNOWN.

Executed fixed comparison: 12,000 normalized outputs at each t=0,1/4,1, plus
matched exact-ideal weighted recursion and 16 ordinary continuous-time N=5,000
populations. At t=1, normalized output cost 5.541 seconds and 1,342,201 full
partner calls, versus 1.560 seconds and 595,763 calls for the weighted output.
Finite-N Kac simulation was much faster (0.366 seconds for all populations),
with no certified population-bias removal. Full output statistics/counters,
exact algebra controls and source/prior boundaries are preserved.

Scope: a constructive ideal-real model theorem plus binary64 diagnostics.
No device/model acquisition, finite-bit continuous output, historical novelty,
global runtime advantage or late-time efficient solver is claimed. The
Maxwell/linear-rotation constructions remain frozen and are not used as a
hard-sphere moment or Gaussian-smoothing oracle.

Governing files: GENERATOR.md, PROOF.md, CONFIDENCE_OPERATION.md;
implementation hard_sphere.py; controls certify_generator.py and
run_acquisition.py; costs/prior PRIOR_AND_COSTS.md; actual receipts under outputs/.
