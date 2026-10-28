# Governing sources, prior machinery and implementations

Read selectively on 28 October 2026. The continuation's proofs are ordinary
derivations in the included theory files. These sources identify the retained
contracts and established mathematical/implementation tools; they do not
constitute external validation of the new construction.

## Current Astra sources

Repository revision: `ca9174c0692d6e2ee77a9a1cb3e65573bfeaf9c2`.

- [N1082 current card](https://github.com/harjassand/astra-research-knowledge/blob/ca9174c0692d6e2ee77a9a1cb3e65573bfeaf9c2/frontier/cards/N1082-observable-centered-gram-response-compiler.json).
  Its governing acquisition proof was read directly and is saved as
  `sources/N1082_GOVERNING.md`, SHA-256
  `aebe53e9e530bc6bb3e1f30446ff4f942b9849303e992abaf5222f44a4a6a042`.
  The exact response quotient and rank-one source contract provide the main
  leverage. Generic positive references do not warrant noisy conditioning.
- [N1089 current card](https://github.com/harjassand/astra-research-knowledge/blob/ca9174c0692d6e2ee77a9a1cb3e65573bfeaf9c2/frontier/cards/N1089-task-conditioned-noisy-psd-intervention-certificates.json).
  Its governing task-certificate proof is saved as
  `sources/N1089_GOVERNING.md`, SHA-256
  `9c9ee4a065d977ffaad3e60f43d4403d3efa931ac8323beac3bf6042ed895375`.
  A sound completion family and valid continuous certificate are conditional
  on the actual acquisition being enclosed. Historical producer code and
  named raw results remain unacquired; this continuation does not replay them.
- [N1090 current card](https://github.com/harjassand/astra-research-knowledge/blob/ca9174c0692d6e2ee77a9a1cb3e65573bfeaf9c2/frontier/cards/N1090-matrix-concave-scalar-audit-and-excitation-limits.json).
  The inference subtask read its governing scalar-audit/excitation proof
  directly. Its saved source and reading notes are under `selection/`.

The unchanged prior continuation supplies the unnormalized Schur representation,
dark intervention-order proof, saturation obstruction and previous comparisons.
Its SHA-256 is recorded in `PROVENANCE.json`; all original receiver distinctions
are retained through that archive. Current scoped reviews are not treated as
an independent whole-proof audit.

## Primary approximation and determinant literature

- E. de Klerk, M. Laurent and Z. Sun, *An alternative proof of a PTAS for
  fixed-degree polynomial optimization over the simplex*, Mathematical
  Programming 151 (2015), 433–457; published online in 2014.
  [Primary PDF](https://ir.cwi.nl/pub/23423/23423.pdf).
  Read the grid approximation, Bernstein operator and multinomial arguments.
  They establish the conventional framework against which acquisition count
  and approximation error must be compared. The present source-specific
  energy bound is proved separately in `theory/SIMPLEX_LAW_ACQUISITION.md`.
- E. de Klerk, M. Laurent and P. Parrilo, *A PTAS for the minimization of
  polynomials of fixed degree over the simplex* (2006).
  [Author-hosted PDF](https://www.mit.edu/~parrilo/pubs/files/DeKlerk-Laurent-Parrilo-final.pdf).
  This is earlier conventional grid/Pólya machinery. The retrieved PDF text
  extraction was poor; the 2015 primary paper gives a readable account and
  explicit attribution. No unread step from the 2006 PDF is used in a proof.
- *Multivariate Bernstein polynomials and convexity*, Computer Aided
  Geometric Design (1991).
  [Primary abstract](https://www.sciencedirect.com/science/article/pii/0167839691900316).
  The multivariate operator does not generally preserve convexity. The
  continuation therefore uses concavity of the true energy law and Jensen's
  inequality, and separately verifies curvature of its acquired polynomial.
- A. Kulesza and B. Taskar, *Determinantal Point Processes for Machine
  Learning*, arXiv:1207.6083v4, Sections 2.2–2.4.
  [Primary full text](https://arxiv.org/html/1207.6083v4).
  Positive principal-minor normalization and spectral Bernoulli cardinality
  are classical. The intervention-law error identity, rational truncation
  bound and exact support-cancellation argument are given in full in the new
  theorem, with no detector-noise interpretation imported from the notation.

The inference subtask's `selection/inference_source_notes.md` records further
primary Stieltjes, AAA, moment and network-polynomial sources, together with
the exact scope read. It distinguishes an accessible abstract from a full
article and an inspected implementation from an executed benchmark. Historical
priority for the new bounds has not been established.

## Existing implementations and strong comparison

- [SciPy SLSQP documentation](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html).
  SLSQP was executed only to propose commands from the acquired polynomial.
  The installed version was SciPy 1.17.0 with NumPy 2.3.5; the current online
  page retrieved in this session was version 1.18.0. No version-specific
  feature beyond the established objective/Jacobian/bounds/constraints
  interface was needed. Exact outward certificates do not depend on its
  stopping status or on numerical eigenvalue accuracy.
- Existing baryrat AAA, pyMOR Loewner/parametric AAA, Drake SOS,
  SumOfSquares.jl and recursivenodes implementations were inspected in the
  inference subtask. They were not run or instrumented here. Their sources
  and relevant limitations are recorded in that subtask's source note.

The equally informed conventional comparator receives the same raw intervals,
source warrants and command interface. It may use every proved representation
and certificate here, including the cheaper bound on any given record. Thus it
matches the demonstrated acquisition count. An unverified fit or a weak
single-representation baseline is not treated as the strongest comparator.

All claimed advances are relative to the preserved mission state. Classical
components, ordinary proof correctness, historical originality, end-to-end
measurement cost and a physically useful implementation are separate questions.
