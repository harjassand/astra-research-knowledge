NEAR-HARMONIC MECHANICAL COMPILER -- RESEARCH PACKAGE
6 November 2026

The mathematical operation constructed here takes an explicitly finite
Fourier vector field on a torus and compiles its clock extension into
classical natural mechanics q'=p, p'=-grad V(q), with V globally as close
in Hessian to |q|^2/2 as a supplied tolerance requires. Declared Fourier
observables become exact quadratic position readouts.

What is included

  THEOREM_AND_ALGORITHM.txt
    Full input/output theorem, Fourier contraction, effective constants,
    global potential, projection algorithm, derivative evaluator and
    bit-cost contract.

  CONSEQUENCES_AND_SOURCE_INTERFACE.txt
    Explicit composition with a published polynomial-ODE simulator;
    compactification and convergent latch; undecidable promised limits
    in a fixed near-harmonic natural system; positive-curvature, Cesaro
    and discounted-response deductions; time/precision/access limits.

  compiler.py
    Exact Gaussian-rational Fourier implementation of the free frame,
    inverse, fixed point, finite-precision evaluator and smallness
    certificate. It does not implement the full ambient potential
    evaluator described in the theorem.

  verify.py
    Reproducible exact finite checks using only the Python standard
    library. Run from this directory: python3 verify.py
    This regenerates results.json and EXAMPLE_CERTIFICATE.json, including
    a variable runtime field. Regeneration consequently changes their
    archived hashes.

  results.json
    Recorded finite test results, including a certified C^4 error less
    than 2^(-512) for the embedding correction on the worked example.

  EXAMPLE_CERTIFICATE.json
    Complete rational certificate for d=1, Y(x)=sin(x), eta=1/4.
    The construction chooses epsilon=2^(-178), configuration dimension
    12, and Hessian error at most 1/8. The slowdown 2^178 is a
    sufficient conservative certificate, not a necessary lower bound.

  SOURCES_AND_PROVENANCE.txt
    Pinned Astra sources and their actual provisional scope, primary
    references, Zenodo search record, attribution, and work limits.

  CHECKPOINT.json
    Active task status and the four unchanged SAT predecessors.

  MANIFEST.json
    SHA256 hashes and sizes of all other package files.

Recorded verification

  Free-frame interpolation identities: 702
  Gunther product and sign identities: 6
  Picard ball/residual checks: 4
  Fixed quadratic readout checks: 32
  Geodesic shear metric identities: 3
  Finite-precision C^4 evaluation: 1

The final finite-precision example retained 88 nonzero Fourier coefficients
after two rounded iterations. The a posteriori C^4 error certificate is
at most 2^(-517), stronger than the requested 2^(-512).

These tests check explicit algebra, signs, arithmetic and a finite
implementation. The proof supplies the all-input mathematical statements;
finite tests alone do not. The proof has not received independent review
or proof-assistant verification.

Credit and conclusion

The geometric architecture comes from provisional Astra N1226; the
compactification/latch comes from N716, checked here under the published
simulator interface. Gunther/Yang, Tao, and the polynomial-simulation
literature are credited. No claim of priority is made.

The demonstrated consequences concern exact simulation and the limits of
general long-time prediction. The package does not establish a practical
predictive advantage or a civilization-scale capability. SAT remains
unresolved and inactive as the current allocation, with its predecessors
preserved at their original scopes.
