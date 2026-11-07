THERMAL LOCAL RESPONSE HORIZON — 2026-11-07

Main result
  At fixed inverse temperature, fixed transition band, fixed accuracy and
  confidence, the optimal independent-Gaussian scalar imaginary-time reading
  cost has log M = Theta(T log T). A matching finite record construction is
  supplied. Local gapped nearest-neighbor spin chains attain the lower bound
  despite identical full spectra and all partition functions.

Read REPORT.md for the question, exact access model, complete proofs,
representation, bit costs, acquisition and calibration conditions, and limits.

Files
  thermal_horizon.py
    Exact rational thermal-weight construction, finite Jacobi encoding,
    certified elementary functions, finite acquisition schedule, polynomial
    record compiler/evaluator, and charged finite-stream processor.
  validate_horizon.py
    Replays exact finite checks and independent floating full-spin diagnostics.
    Core calculations use the standard library; full-spin diagnostics use
    already installed NumPy. No network or physical instrument is called.
  VALIDATION.json
    Executed results. Huge mathematical acquisition budgets were NOT executed.
  EXPLICIT_PAIR_n7_uniform.json
    Eight-site main-family example with polynomial endpoint-weight floors.
  EXPLICIT_PAIR_n8.json
    Nine-site binomial-background variant, retaining its stronger hopping floor.
  ENDPOINT.json
    Current question, completion scope, access distinctions, unresolved targets.
  SOURCE_SCOPE.json
    Governing original versions and primary credits.
  FAILURE_OBJECTS.json
    The invalid unweighted thermal-lift shortcut and its exact scope.
  PREDECESSORS.json
    Prior archives and byte-preservation checks.
  SHA256SUMS.txt
    Integrity manifest for the other archive members.

Reproduce
  python3 validate_horizon.py

Use the main explicit constructor
  from thermal_horizon import construct_pair
  pair = construct_pair(7, background="uniform")

Encoding
  Fractions in JSON are exact strings. The field squared_hoppings stores b_i^2;
  the hopping in H is its POSITIVE square root. This is an explicitly declared
  finite algebraic encoding, not a claim that all hopping coefficients are
  rational. The exact common spectrum is preserved.

Access
  The lower bound concerns an unknown source accessed through specified scalar
  observations. It does not apply when its actual Hamiltonian coefficients
  are supplied. No experimental measurement channel is constructed.

Predecessors
  Exact QUBO and the full 2D physical nucleation predictor remain unresolved.
  Earlier scientific scopes and resource holds are unchanged.
