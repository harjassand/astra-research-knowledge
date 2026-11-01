# Uniform autonomous survival receiver: review notes (not a final receipt)

Input manifest: 51bf3b23073d2b85727d36d94a9191a26b8dd4d2d0faaca4cab78152e437b4e7.
All 13 explicit files and 8 dependency bindings have been verified and copied.
Copied author suite passed 3,809 checks, actual four saved cases and byte-identical
check_results.json; shell timing 10.071 s diagnostic.
Independent whole suite is still running; its absence of results is not PASS.

Analytic/source review completed: root proof 2414f104 remains the bound source;
its zero-resolvent/source-current normalization and initial-law comparison are
sound. Corollary e20a54e8 pays the midpoint-rate penalty 3/16 times relative rate
width. Finite interval arithmetic uses the actual current-expression upper bound,
not just an arbitrary mean upper bound. Runtime code pins the three inherited
code dependencies transitively; root/corollary proof texts are package-manifest
bindings and certified identities, not runtime re-proved text. No newer trial or
well-current source is substituted.

Shared max_operations applies to guarded fixed products, not all Fraction or
Python operations. Two inherited roots and one wrapper root have separate bit
and call accounting. Display, seconds and work fields are intentionally not proof
inputs. Verification recomputes using original external controls before comparing
proof records. Original-task times are strict nonnegative Fractions; external
resource inputs are strict positive ints, excluding bool and subclasses.

513-dimensional frozen output: k_star ~2.384062482990607e-37;
epsilon ~0.004780005556792939;
rho ~1.973778717895864e-24;
initial comparison ~1.4049123523912124e-12;
rate uncertainty ~0.00014566836832336988;
total KS ~0.004925673926521221.
This is uniform absolute CDF error, not a relative extreme-tail or unbounded-moment
bound. Full Gibbs|A and the actual constant-SPD model remain required.
