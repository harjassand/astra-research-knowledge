P3 — finite-system thermodynamic state preparation, 7 November 2026

Read P3_OPERATIONAL_THERMAL_STATE_20261107_RETURN.txt for the full result,
proofs, input/interface contracts, resource bounds, sources and limitations.

This package emits logical preparation circuits. It does not control any
physical device or commission a source. The independent audits are labelled
binary64; the matrix, probability and angle certificates use exact rational
or outward scalar arithmetic with explicit analytic remainder bounds.

Existing Python dependencies: numpy, scipy, threadpoolctl, matplotlib.
No installation or network access is needed for reproduction.

  python run_construction.py
  python audit_ripple.py
  python certify_observables.py
  python make_figure.py

Compile a different supplied rational collective-spin model:

  python prepare.py EXAMPLE_REQUEST.json --output generated

The request specifies N, beta, rational coefficients of distinct-site
normalized collective Pauli monomials, and a nonempty collective-Z window.
The generic example contains complex Y terms. Finite precision is declared;
an error budget that the arithmetic does not certify is refused.

The compiler samples a sector and multiplicity path, then emits ONE
component circuit. Draw a fresh component for EACH requested independent
thermal-state preparation. Repeating a stored fixed example circuit does
not implement the full Gibbs mixture. The demonstration-seed option is a
reproducible digital example, not a physical independent-randomness promise.

INPUT_MODEL.json contains minimal exact inputs from the authorized obtained
predecessor return, with source-record hashes and its actual uncertainty
and acquisition cost. Reproduction does not require that previous folder
or any held original. No earlier held package is included or reconstructed.

All source code and results are in the package; generated caches and the
working construction notes are omitted. MANIFEST_SHA256.json records the
delivered file hashes. The report distinguishes this finite-dyadic logical
emitter from its arbitrary-precision mathematical algorithm and from native
finite-alphabet synthesis, routing, error correction and hardware execution.
