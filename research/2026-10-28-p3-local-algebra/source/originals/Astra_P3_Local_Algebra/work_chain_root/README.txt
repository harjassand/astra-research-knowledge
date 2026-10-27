ASTRA P3: ACQUIRED LOCAL-ALGEBRA COUNTERS

This source distribution contains actual proofs, production programs, raw
inputs, exact outputs, and independent audits. No practical-speed or historical
priority claim is made. Python 3.12 and NumPy were used. Run commands from the
archive root so the adjacent work_* dependency directories remain available.

Strongest all-depth theorem and raw pair compiler
  python3 work_chain_root/acquired_pair_counter.py \
    work_chain_root/contact_field_36_input.json --output count.json

This receives only n and Boolean ANF monomial masks. It acquires the full
chain algebra, affine center, ordinary cubic and compatible quotient
quadratic. Semilinear descent manufactures the hidden binary structure and
two-dimensional blocks. The pair Gaussians have eight joint states. Seven
cubic Artin-Schreier point counts in at most eight field variables and one
binary Gaussian reconstruct the terminal for any number of pairs.

For the precisely certified family, d>=3 and 3 not dividing d, the theorem
is polynomial uniformly in n=b*d*e, including unbounded odd b>=5 and every
depth e. Higher nilpotent cubic coefficients are arbitrary. The quotient
quadratic has unrestricted rank, with height 3h<=e+1. Its support, algebra
and pair decomposition are acquired and verified. Conservative bit bounds
are poly(L,n)+soft-O(d^31) time and poly(L,n)+soft-O(d^20) space, using the
published Lauder-Wan algorithm.

EXECUTION BOUNDARY: this distribution does NOT implement the generic
Lauder-Wan engine. The default pair terminal scans 2^d field coordinates
and reports it. --field-bit-budget bounds d, default 24. The raw 36-bit
example uses 16 coordinates and returns signed count 3997696 and zero count
34361737216. Small-field callback replay is explicitly labeled as replay.

compile_pair_family(poly,n,point_counter=...) calls
point_counter(field_modulus,variable_count,ordinary_polynomial), expecting
the exact number of field points. moment_hypersurface manufactures the actual
degree-three coefficient dictionary. The compiler converts cardinalities
to moments and reconstructs. Seven nontrivial indices are 01,02,10,11,12,20,21.

Broader acquired contact family, with an executed counting backend
  python3 work_chain_root/acquired_contact_counter.py \
    work_chain_root/contact_raw_72_11092.json --output contact_count.json
  python3 work_chain_root/contact_circuit_counter.py \
    work_chain_root/contact_72_bit_circuit.json --output gate_count.json

The raw 72-bit example has module rank 9 and rank-36 quotient noise. Its
signed count is -549755813888; zero count 2361183241159944699904. The actual
gate program has 25678 supplied gates, 8380 output ancestors, 72 original
inputs and 31052 output ANF terms. Gate states do not become independent
counting inputs. Live ANF expansion and its arithmetic are charged in full.

The contact counter acquires the hyperplane, nonsingular transverse polar,
and binary critical kernel dimension kappa, then streams 2^kappa candidates.
Only the origin recurses. A field leaf scans 2^d coordinates and uses Gaussian
elimination for the remaining (b-1)*d bits. No field leaf occurs for e=0 or 2
modulo 3. The one-ray family has kappa=0 for 3 not dividing d at unbounded
module rank. The raw 100-bit case exercises depth 5 -> 2 and rank-40 noise.
The raw 80-bit audit exercises depth 4 -> 1, higher cubic deformations and
rank-20 noise; its field leaf is independently exhausted.

Sharp failures preserved
  HIGHER_RANK_STATIONARY_AUDIT.md in work_stationary_prior_agent proves #P
    hardness with fixed F8, depth two, no noise and full chain centroid.
  pair_divisibility_boundary.py strengthens this to the SAME J-pair residue
    at d=3. Its raw 42/66-bit examples distinguish full residue enumeration
    from critical-chart enumeration; neither is a full ring truth table.
  contact_frontend_failure.json preserves exit 137 in the old all-wire
    frontend. live_circuit_anf.py repairs its storage with backward
    reachability, gate validation, reference counts and release of polynomials.
  Other proofs preserve failures of the infinity test, full-ring contact
    factor, quotient height, nonchain centroids and arbitrary parity constraints.

Complete rank-three production entry point
  python3 work_chain_root/acquired_quotient_counter.py \
    work_chain_root/quotient_raw_72_8112.json --output count.json

This receives only n and Boolean ANF monomial masks. It acquires the chain
algebra and binary coordinates, fits an ordinary homogeneous ternary cubic
plus quotient quadratic, recovers the affine center, and counts all critical
rays by exact Gaussian elimination. The example has 72 original bits,
rank-36 compatible quadratic noise, and three singular rays. Its signed
count is 4260607557632, zero count 2361183243565126385664.

Actual gate-program entry point
  python3 work_chain_root/quotient_circuit_counter.py \
    work_chain_root/quotient_72_bit_circuit.json --output gate_count.json
The input has 72 independent bits and 4888 internal gates. Its output is
identical to the previous raw input. No gate state becomes an independent bit.

Adaptive counting
  Add --residual-bit-budget 24 to acquired_quotient_counter.py to acquire the
  minimum admissible quotient height and permit ONE explicitly budgeted
  residual enumeration. Every enumerated point is recorded. This mode is not
  labeled polynomial when that residual dimension grows. The executed
  adaptive_quotient_checks.py regenerates three saved examples, including
  original dimensions 36 and 63 with only a 9-bit residual.

Representation and theorem scope
  A = F_(2^d)[t]/t^e is acquired, not supplied. For d>=3 the rank-three raw
  fitter is complete on translated homogeneous cubic phases with unit XYZ
  coefficient and an arbitrary binary quadratic on the first h ring digits.
  The default polynomial range is 3h<=e+1. The quadratic rank is unrestricted.
  Nonzero projective critical directions are acquired by small binary systems.
  Only the origin recurses. The minimum-height extension is also exact.

Rank-three finite-field execution boundary
  Depths e=0 or 2 modulo 3 never invoke field enumeration. Depth 1 modulo 3
  can reach a finite-field leaf; the built-in fallback enumerates at most
  24 bits by default and explicitly reports doing so. A general exact
  finite-field callback can replace it. Lauder-Wan gives the theoretical
  polynomial-time backend through W^2+W+H=0, but this package does NOT
  implement that generic backend. field_leaf_compiler.py manufactures and
  certifies the four-variable reduction. laurent_field_counter.py implements
  an actual finite Dwork specialization for bounded Laurent/Hesse phases.

Other completed production mechanisms
  work_chain_root/stationary_chain_counter.py : smooth residue shortcut,
    including small residue fields and mandatory unused-layer checks.
  work_ring_count_agent/rank_five_stationary.py : raw fixed-module-rank smooth
    compiler, executed on rank-five examples; no depth-one fallback is hidden.
  work_chain_root/acquired_chain_counter.py : complementary split-ring base
    plus global rank-r defect, automatically tries applicable Gabidulin,
    selfadjoint-field, and nilpotent recovery routes; streams 2^r leaves.
  work_chain_root/acquired_product_counter.py : acquired primitive components
    with retained global quadratic glue.

Reproducing selected checks
  python3 work_chain_root/contact_field_checks.py
  python3 work_stationary_prior_agent/acquired_pair_terminal_checks.py
  python3 work_composite_review_agent/eight_state_audit.py
  python3 work_chain_root/pair_divisibility_boundary.py
  python3 work_chain_root/live_circuit_checks.py
  python3 work_chain_root/quotient_counter_checks.py
  python3 work_chain_root/quotient_homogeneous_compiler.py
  python3 work_chain_root/adaptive_quotient_checks.py
  python3 work_stationary_prior_agent/weighted_homogeneous_checks.py
  python3 work_composite_review_agent/weighted_ray_fit_audit.py
  python3 work_ring_count_agent/rank_five_stationary.py --checks

Some exhaustive suites evaluate hundreds of millions of assignments across
small cases; their JSON outputs are already included. Larger coefficient-only
checks are explicitly distinguished from complete raw acquisition. The proof
PDF/TeX states original description size, input count, arithmetic/reconstruction
costs, prior methods, and preserved failures. The raw general-circuit problem,
unrestricted parity constraints, arbitrary nonchain centroids, and arbitrary
nonhomogeneous perturbations are not solved by these constructions.

Earlier network work is in work_preserved_network. The three recovered
latest task-directed files are unchanged with their original receipt. The
older exact/noise-aware 510-reaction Gram source was not recovered; the
preservation note explicitly records that gap.
