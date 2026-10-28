# Scoped review of the acquired-polynomial curvature implementation

28 October 2026. Reviewed `code/polynomial_curvature.py` and
`code/run_curvature_refinement.py` against
`theory/POLYNOMIAL_CURVATURE_CONTROL.md`, with the existing simplex-law and
hypograph interfaces. This is a scoped implementation review, not an
independent whole-proof audit or a rerun of the main experimental results.
No reviewed implementation file was changed.

## Result

**No invalid mathematical certificate was found on the stated finite,
positive-polynomial input path.** The derivative coefficients, strict
rational matrix checks, reciprocal tangent, DAC preparation and combination
of candidate lower bounds with global upper bounds agree with the proof.
Two reproducible robustness gaps can abort refinement instead of retaining
the already valid hypograph certificate. They do not invalidate certificates
that successfully pass the existing checks.

### Finding 1 — numerical proposal exceptions bypass the rational fallback

**Priority: P2, availability of the promised fallback.** In
`CurvatureLaw.__init__`, the floating conversions, `numpy.linalg.eigvalsh`
and conversion of its proposed bound to a rational occur before the exact
verification loop. An eigensolver exception or nonfinite/overflowing proposal
therefore bypasses the exact Gershgorin fallback altogether.

The review probe replaces `eigvalsh` with a function raising
`numpy.linalg.LinAlgError`; the constructor propagates that exception.
By contrast, replacing the eigenvalue proposal by an incorrect finite zero
does reach the fallback: a polynomial with Hessian diag(2,0) succeeds on
the second exact attempt with mu>2 and positive pivots.

**Correction:** treat numerical eigenvalues only as optional proposals.
If their computation or finite conversion fails, initialize mu directly
from the rational Gershgorin bound plus its strict margin. Preserve every
exact matrix test. A proposal failure must not be converted into acceptance
of an uncertified mu.

### Finding 2 — a nonpositive acquired value aborts instead of using the old bound

**Priority: P2, bounded-error fallback.** `certificate` asserts `p(x)>0`
for both utilities, and the runner requires curvature certificates for both
old and proposed commands in a list comprehension. Thus one unacceptable
polynomial value aborts the complete refinement before the old valid
hypograph certificate can be retained. The numerical compliance proposal
also directly divides by p and has no guarded fallback if it encounters
zero or an unusable iterate.

This situation is compatible with the acquired interval contract. The
saved review probe uses n=1,k=4 and strictly positive node intervals, each
containing the legal constant source J=1. At the legal command x=1/50 the
acquired interpolant is `p(x)=-5071/62500`. Calling even the conductance
certificate raises `AssertionError`. This example has large noise; it does
not assert that the current five saved acquisition cases encounter it.

**Correction:** treat an inadmissible proposal/candidate as an unavailable
curvature improvement and retain the old certificate. Alternatively, the
conductance formula can be evaluated without requiring p(x)>0, while the
compliance formula can use the proof's unsimplified tangent at an
independently positive j0. In either approach, do not replace p by a clipped
value inside the current simplified tangent formula without re-deriving its
constant. Candidate preparation or numerical optimization failure should
also leave the old candidate/certificate available.

## Verified implementation details

- The gradient differences use physical index i+1 against barycentric index
  0 and include k/delta. The Hessian differences include k(k-1)/delta^2,
  the two mixed negative terms and the correct repeated-index multiplicity.
- `positive_definite` performs exact rational Schur elimination on the
  actual Fraction-valued matrices. Rejecting zero pivots is legitimate here:
  the constructor certifies the stronger strict condition and the rational
  Gershgorin fallback adds a positive margin. It does not silently accept
  indefinite matrices or claim that a singular PSD matrix passed.
- On successful verification, the saved pivots correspond to the final
  recorded mu. The numerical eigenvalue is not used as the certificate.
- The compliance scaling is exactly `factor=1/p(x)^2`, including both the
  curvature allowance and E. The base term is -1/p(x), consistent with
  the tangent at j0=p(x). The law is reconstructed from saved J intervals,
  so the raw 3/2 boundary offset is not incorrectly inverted.
- Candidate conversion clips negative finite components, rescales excessive
  total dose, then rounds downward onto DAC20. Exact certification is at
  the resulting command. The fixed DAC20 convention matches the reviewed
  saved-run specification; it is not automatically a generic other-DAC
  interface.
- The runner selects the largest valid candidate lower reward and the
  smallest valid global upper reward. They may originate at different
  commands because every upper bound is global. Keeping the old upper and
  old candidate in these sets makes the successful combined certificate
  no worse than the old certificate.
- Hidden source vectors are accessed for source evaluation only after
  candidates and certificates are chosen. The polynomial derivatives are
  derived from acquired coefficients. No source gradient enters the learner.

## Independent finite review probes

`reviews/curvature_review_checks.py` checks known monomial polynomials at
degrees 2--5, independently of the Bernstein difference formula. It verifies
16 exact values, 32 exact gradient entries and 64 exact Hessian entries,
including boundary points. It exercises one forced finite-eigenvalue
fallback and one out-of-simplex numerical proposal whose actual DAC command
is legal. It also reproduces the two robustness gaps above. Results are in
`reviews/CURVATURE_REVIEW_CHECKS.json`. These checks do not replace the
analytic all-simplex argument, the source-law acquisition proof or the main
run's complete raw-record checks.

## Exact reviewed versions

SHA-256 hashes were recorded before the probes and checked unchanged afterward.

| File | SHA-256 |
|---|---|
| `code/polynomial_curvature.py` | `23b35537913e34726698db6668ed85874736fa401ce874a095b01c3ca445304b` |
| `code/run_curvature_refinement.py` | `8de55ec26918e3e856a76997db2e009b46d4cff7fe082a0f99bbcf0980cfedcd` |
| `code/simplex_law.py` | `2ac69c52818d31b741f165bf6cb50fba5d990f14cd2ae6cedef5b4be1043505d` |
| `code/hypograph_control.py` | `3416567cd6079ef387bed376b5ac46742782fe2a6b96bd2edc8d14c0652294e9` |
| `theory/POLYNOMIAL_CURVATURE_CONTROL.md` | `e8d318191cc34fbc22b5295f1eb8a2254021a3ce3d3aa31558cf8d755306e30d` |

Any subsequent implementation changes need their own versioned review or
appropriate focused check; this note does not silently cover later files.
