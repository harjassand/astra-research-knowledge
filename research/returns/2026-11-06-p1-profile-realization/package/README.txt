FINITE GEOMETRY AND PHYSICAL REALIZATION OF COMPLETE MAXIMAL-INFORMATION PROFILES
Astra P1 -- 6 November 2026
Status: UNREVIEWED. Analytic proofs plus finite exact implementation checks.
No independent scientific verification, formal verification, historical priority,
practical advantage, ordinary-capacity algorithm, or completion of the larger
civilisation-scale programme is claimed.

START WITH
  maximal_profile_geometry_and_realization.pdf   (23-page manuscript)
  source_manifest.json                          (governing versions and holds)
  build_validation.json                         (build/check/QA record)
  SHA256SUMS.txt                                (content integrity)

SCIENTIFIC CONTENT
  1. A polynomial exact rational construction of one faithful separable input
     pair and one orientation separating unequal complete maximal-information
     profiles for every nonaffine operator-convex f.
  2. A finite-family affine profile representation and p-1 common scalar probes,
     minimal for the entire affine span of dimension p-1.
  3. An exact physical-realization theorem for signed affine combinations:
     a positive state functional is physically realizable precisely when its
     null space is a two-sided ideal, equivalently when its ACTUAL support
     projection is central in the finite generated algebra.
     The rational compiler returns a CPTP channel or a finite negative-norm /
     null-ideal obstruction that excludes every finite output dimension.
  4. A rational qubit family with a constructive signed interior, a positive
     but nonphysical boundary, and distinctions visible only with references.
     Convexity, closure, minimum complex dimension and paid recovery follow
     under the manuscript's explicit assumptions.

The proof, not the finite tests, supports universal quantifiers. The central
support condition concerns the actual support projection, not its central
carrier. Complete profiles include all finite untouched references. A replacer
retains reference information; its complete profile is not generally zero.

INPUT CONTRACT
  Python 3.12, standard library only, for the compilers and checkers.
  Dense, explicitly supplied rational Choi matrices.
  Choi order is input-major: index (input_index * output_dim + output_index).
  A rational scalar is an integer or a string such as "3/5".
  A complex scalar is [real_part, imaginary_part], with rational components.
  Floating-point JSON numbers are rejected.
  Channel object:
    {"input_dim": a, "output_dim": b, "choi": [[...], ...]}
  See the supplied *_input.json files for fully specified examples.

COMMANDS (run from this unpacked directory)
  python3 compile_witness.py identity_vs_replacer_input.json my_witness.json
  python3 check_certificate.py identity_vs_replacer_input.json my_witness.json my_witness_check.json

  python3 compile_panel.py six_channel_family_input.json my_panel.json
  python3 check_panel.py six_channel_family_input.json my_panel.json my_panel_check.json

  python3 compile_realization.py signed_interior_input.json my_realization.json
  python3 check_realization.py signed_interior_input.json my_realization.json --output my_realization_check.json

INPUT WRAPPERS
  Witness:     {"E": channel, "F": channel}
  Panel:       {"channels": [channel, ...]}
  Realization: {"channels": [channel, ...], "coefficients": ["-1/3", "4/3", ...]}
  Realization coefficients are real rationals summing to 1.

COMPILER OUTCOMES
  different_maximal_profiles:
    states, explicit product decompositions, separating word/phase/orientation,
    exact parameters and a normalized universal margin.
  equal_maximal_profiles:
    finite closure equality result.
  complete_affine_profile_panel:
    affine basis, all relations, reconstruction coefficients, common probes and
    quantitative perturbation certificates.
  realizable:
    exact rational channel, Gram/factorization data and a paid uniform-flag
    heralded implementation.
  not_realizable_negative_norm:
    an explicit polynomial with negative squared norm.
  not_realizable_null_ideal:
    a zero-norm polynomial and a generator whose right product has positive
    squared norm.

VERIFICATION
  python3 test_construction.py
  python3 test_panel.py
  python3 test_realization.py

These test scripts regenerate/overwrite fixtures and their verification reports.
Run them in a working copy if you want to preserve the delivered evidence bytes.
The delivered reports record 8 witness/input-validation cases, 4 panel cases
and 5 realization cases, all passed. Tampered certificates are rejected.
The compilers and checkers share rational arithmetic and helper code: this is
not independent scientific review or independent software implementation.

  exact.py                     exact Q(i), PSD, closure and rational factors
  compile_witness.py            universal separating-state compiler
  check_certificate.py         separating-certificate replay
  compile_panel.py              common affine-panel compiler
  check_panel.py                affine-panel replay
  compile_realization.py        physical channel or obstruction compiler
  check_realization.py          realization/obstruction replay
  test_*.py                    finite regressions and tampering checks

DEPRECATED FAILURE RETAINED
  adaptive_panel_prototype.py is a failed/deprecated adaptive approach. It is
  retained as a useful failure record and is not part of the proven compiler.
  Its coefficient-height feedback is not used to justify termination or cost.

COSTS AND LIMITS
  Polynomial bounds refer to dense rational input dimensions and bit length.
  They are not polynomial bounds in the number of qubits. No free channel
  evaluator, channel-identification oracle, state-preparation oracle, NP-hard
  optimization oracle or exact finite-universal-gate realization is supplied.
  Rational witnesses can have exponentially small observable gaps.
  Exact profile evaluation and input acquisition must be paid separately.
  A heralded success probability p becomes p^n for an n-use successful block.
  Full-block retries cost n/p^n expected uses only when the original input is
  known and resettable; an unknown failed input cannot simply be retried.
  The rational output embedding can be larger than the minimum complex output
  dimension. No polynomial compiler for a minimal rational embedding is claimed.
  Finite-panel coordinates fit promised affine spans; they do not test that an
  arbitrary unknown channel belongs to the span or certify arbitrary noise.
  The closure statements use finite moment coordinates, finite panels and
  pointwise fixed-query convergence, not uniform convergence over all queries.

PRESERVATION / SOURCES
  Governing Astra commit: c6c7966fa8ebdfb5207d2a11b6648ea95c9ecf3e.
  N1690 and corrected N1698 content versions and visible-return hashes are
  recorded in source_manifest.json. Held originals remain unacquired.
  Existing sources, scopes, access/transfer holds and predecessor artifacts
  are preserved. No peer role was messaged or reallocated. Sol remains held;
  Dots remains unmessaged. No new worker, local team or physical experiment.
  Read the manuscript's attribution/source-comparison section before treating
  this construction as new: historical priority is NOT established.
