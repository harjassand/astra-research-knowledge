# Completed substantive review of the observation-factory extension

Root read the full pinned N1073 governing proof, the complete new
`PROOF_EXTENSION.md`, and all used operation/factory/lazy code. The extension is
accepted at its stated mathematical and reference-runtime scope. This supersedes
pending-review labels in the worker's frozen handoff and verifier output; it
does not confer novelty, physical acquisition or practical advantage.

Governing pin:e1e2272165c8548326c31bb11817c28f871d21e9. Governing proof SHA256:
33007e1215fd91118e35be36b07b50ea3096b936b3c33c8e519b058d50ad4eb9.
Extension proof SHA256:7313f49d8f638dee659c726231e8205700288a6b4ac6da76a76e696f7b94eb0d.
This review uses the source's already-classical input and private-record contract;
it does not reaudit the old generic LP simplex implementation.

## Accepted construction and boundaries

1. For known rational L with distinct columns and strictly positive K, finite
   empirical classification followed by exact confusion-matrix inversion can
   simulate K without raw input. The positivity/norm argument and resource
   accounting are valid; no uniform polynomial-in-alphabet/bit-length claim.
   The particular source needs just two cheap calls. Root independently checked
   every rational output, one-call feasible certificate and common-part cost.
2. A fixed hard cheap-call budget under open stationary calibration uncertainty
   forces the common-part raw bound. The multinomial Bernstein uniqueness
   argument is sound and explicitly does not apply to unbounded stopping.
3. The corrected Bernstein envelopes nest on four-adic degrees. Root separately
   derived the hypergeometric variance cancellation and remainder estimates.
   The displayed M2/M3 bounds, rational radii and starting degree are conservative
   and valid. Constant envelope width gives the exact1385.96875 expected cheap
   calls. The naive implementation's bit-cost defect is not a theorem against
   all factories.
4. Predrawing terminal degree and using its conditional stop coin telescopes
   correctly. The lazy near-half interval is a conservative exact bound; fallback
   continues the same uniform prefix. It does not allocate exponentially large
   denominators on ordinary paths. With the positive margin at TV radius1/600,
   costly exact elevations are exponentially rare. Polynomial exact arithmetic
   and E[N log^c N]<infinity establish finite expected internal bit work. This is
   not a measured expected physical cost or a worst-case resource bound.
5. Exact robustness to arbitrary finite-prefix perturbations is different from
   stationary unknown calibration. Root independently derived, and the worker
   checked, the multi-affine conditional-output argument. Even any positive
   total drift budget forces raw probability>=11/40 in this source family.
   Common-part splitting attains it. The overlap result at radius>=1/4 is a
   minimax statement; it is not a pointwise lower bound for every distinct
   stationary channel outside the overlap witness.
6. The102-call ordinary comparator has output TV<=1e-6, including predictable
   drift within separated per-call bias bounds. Root independently certified
   the rational exponential bound. The101 value fails this particular Hoeffding
   certificate, not a lower bound on all approximate algorithms.

The factory requires one persistent classical X and independent cheap draws
with a fixed unknown channel during each invocation. Private cheap records,
degree, flags and memory are discarded. Marginal Y equality is not equivalence
of arbitrary disclosed transcripts; cq composition keeps only the registers
specified by the source contract. Quantum-coherent input, state-changing cheap
reads, free parameter access and unbounded input lifetime are not manufactured.
For many outputs ordinary one-read caching is an available comparator.

## Actual runtime review and verification

Root preserved the worker's frozen files and created `runtime/` as the reviewed
copy. One callback-boundary correction converts equality indicators to Python
integers before adding them: numpy integer callbacks otherwise produce numpy
booleans whose addition can lose the count of two zero records. All nine such
callback words now give the exact intended weights. No mathematical rule changed.

All three supplied verifiers were rerun in this root-owned runtime and passed.
Their output JSONs remain here, with roughly .013s,.058s,.191s recorded core
verification times. Root also independently reconstructed the source channel
identities and the102-call bound in `independent_checks.py`. Finite diagnostics
support implementation scope; the reviewed arguments establish the general
claims under ideal iid/unbiased-bit promises. Seeded PRNG samples do not certify
ideal randomness or a physical proxy service.

Reviewed code hashes are in `RUNTIME_REVIEW_RECEIPT.json`; factory.py and
factory_lazy.py match the worker core exactly, and operation.py has only the
typed-callback correction. Historical priority, real proxy acquisition,
complete-resource advantage and civilisation-level capability remain UNKNOWN
or NOT_ACHIEVED. Established garbling, Bernstein factories, concentration and
common-part coupling receive the same observations and costs.
