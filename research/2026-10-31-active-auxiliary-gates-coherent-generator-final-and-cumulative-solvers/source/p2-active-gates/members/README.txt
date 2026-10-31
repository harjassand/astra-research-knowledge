ASTRA: COHERENT GATES WITH ACTIVE, UNPREPARED QUANTUM AUXILIARIES
31 October 2026

Start with MAIN_THEOREM.txt in this directory.

Earned scope
------------
1. A common accretive quantum transition amplitude plus a decay outlet gives
   uniform bright/excited contraction without a source-Hamiltonian norm or
   gain-derivative bound.
2. An explicit moving dark-space construction yields a full retained-channel
   gate bound of order 1/T, including all emission histories.  The proof allows
   arbitrary initial code/source/reference correlations.
3. Real tripod loops give Householder gates.  A specified two-body pair-star
   gives controlled-Z.  A fully explicit established realification compiles
   Clifford+T computations using one extra rebit and h+3c+10t loops, before
   routing and physical preparation/readout costs.
4. An architecture-specific lower bound shows that inverse-error time cannot
   be removed for fixed coupling/decay, absorbing flags and the star-only
   control graph.
5. A same-tripod coherent-source resonance leaves 70.21% leakage as T grows;
   loss removes that failure in the stated finite model.  Separate positive
   leg gains can still destroy the common dark subspace.
6. A complete optical-manifold calculation distinguishes scalar light shifts
   from information-carrying emissions.  A separate exact degenerate-complement
   subsystem permits actively excited/scattering optical auxiliaries.

Not earned
----------
A qualified microscopic pair coupler; a complete laboratory operating window;
arbitrary helper/loading states; a universal physical encoding of an unknown
complex input using real controls alone; a fault-tolerance threshold; a practical
advantage over equally informed established methods; historical priority.

Files
-----
  dissipative_transport/MAIN_THEOREM.txt
    Central proofs, explicit contracts, costs, comparisons and limitations.
  dissipative_transport/finite_time_gate_checks.py
    Rapidly switching quantum sources, complete code/source operator bounds,
    and a separate-positive-leg-gain failure.
  gate_mechanism/INDEPENDENT_GATE_AUDIT.txt
    Complementary mathematical audit, same-hardware resonance, lower bound.
  gate_mechanism/*_checks.py and *_counterexample.py / *_comparison.py
    Ordinary finite-source diagnostics and their JSON results.
  exchange_protection/HOLONOMY_CONSTRUCTION.txt
    Explicit local/pair transitions, real geometric gates and microscopic gap.
  exchange_protection/REAL_COMPILER.txt
    Realification, fixed ray bank, routing and initialization costs.
  exchange_protection/holonomy_compiler.py and rebit_compiler.py
    Pair-subspace and circuit checks, with JSON results.
  physical_window/COMMON_MODE_TRIPOD_INTERFACE.txt
    Common-mode Maxwell field construction, full angular closure, fine jumps,
    physical return diagnostic, exact static subsystem and optical limitations.
  physical_window/atomic_closure_checks.py
    All angular identities and an optional complete 12-level/source Lindblad
    diagnostic.  Its Choi-state distances are not diamond-norm certificates.
  inherited/OUTPUT_MODE_THEOREM.md
    The user's original compact handoff, preserved byte-for-byte.
  ASSESSMENT.txt and SHA256SUMS.json
    Review scope and reproducible package contents.

Reproduction
------------
Python with NumPy and SciPy is sufficient.  This run used NumPy 2.3.5,
SciPy 1.17.0.  All programs use only local files and fixed example seeds.
From the extracted package root:

  python dissipative_transport/finite_time_gate_checks.py
  python gate_mechanism/positive_gap_counterexample.py
  python gate_mechanism/dissipative_bright_checks.py
  python gate_mechanism/tripod_resonance_comparison.py
  python exchange_protection/holonomy_compiler.py
  python exchange_protection/rebit_compiler.py
  python physical_window/atomic_closure_checks.py --full

The last command includes the larger optical diagnostic.  Its current complete
results are already included.  Numerical results use ordinary floating point,
with no certified interval enclosures.  The general claims rest on the written
proofs; finite replay does not establish a microscopic device or novelty.

Continuity
----------
Earlier readout, warm absorption, return, complete-manifold cancellation,
triplet-tensor and unobserved-history corrections are preserved at their exact
scope.  This package does not overwrite or promote them into a device claim.
No repository integration or external publication was performed.
