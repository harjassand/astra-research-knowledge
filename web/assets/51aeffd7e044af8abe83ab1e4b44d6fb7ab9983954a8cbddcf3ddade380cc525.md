# HF space-simulation addendum

Frozen research follow-on, 2026-10-08. The first research ZIP is unchanged.

## Scientific result

The previous space-simulation proof gate is now internally closed within an explicitly specified model: fixed Rossman/GKPS BGS terms with bounded comprehension, standard HF Card, and unary/binary input with at least two atoms. One fixed binary-vocabulary two-dimensional FO+H interpretation program simulates such a term program with maximum state universe polynomial in input size plus peak live hereditary closure, independently of unrestricted finite runtime.

The new reduction transfers the prior explicit-model exponential maximum-state lower bound to this precise fixed-term HF model, conditional on that separate lower bound and its stated inputs. It does not provide an unrestricted computational-space lower bound, a P-versus-NP result, or a theorem about every model merely polynomial-time equivalent to CPT. Historical novelty is unverified. There is no formal certification or external expert review. The proof has undergone separate mathematical reconstruction and independent AI audits, with exact finite semantic controls.

## Contents

- space_simulation/HISTORY_INDEPENDENT_HF_SPACE_SIMULATION.md: complete simulation and conditional corollary
- space_simulation/DIMENSION_AND_BINARY_COMPILER_AUDIT.md: explicit resettable binary/2D compiler
- space_simulation/NEGATIVE_CONTROLS.md: boundaries and failure examples
- space_simulation_audit/INDEPENDENT_AUDIT.md: independent complete proof audit
- space_simulation_audit/BLIND_RECONSTRUCTION.md: independently reconstructed route, recorded before reading the proposed proof
- Three standalone Python scripts and their exact JSON results
- SHA256SUMS.json: hashes of every other packaged file

## Verification

The tests cover 117,448 canonical descriptor equality comparisons, 1,318 garbage-collection cases, 6,000 dynamic-reserve phases, 262,405 exhaustive quotient/incidence cases, six tagged-product cases, and 1,171,875 independent raw-descriptor equality comparisons. All final checks passed. Tests concern finite semantic mechanisms; they are not generated-FO execution or an asymptotic proof certificate.

Run the scripts with Python 3; only the standard library is used. Each writes its JSON result beside itself.

## Scope details

The resource measure is the peak over the native run, not the instantaneous current state. The reserve may retain the largest cardinality needed so far, but grows only polynomially in that peak. Input size must be at least two for parameter-free marker creation. The simultaneous binary/2D initialization does not silently encode arbitrary raw high-arity inputs. Powerset, choice, succinct integer primitives and other machine instructions are outside the proved syntax.
