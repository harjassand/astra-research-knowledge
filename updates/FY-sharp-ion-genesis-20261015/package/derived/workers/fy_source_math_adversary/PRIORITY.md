# Bounded primary-source priority comparison

Date: 2026-10-15. Historical priority of the precise sharp family,
ambient nonexposure theorem, or nonspectrahedral target-cone corollary is
UNKNOWN. The comparisons below establish method ancestry and receiving
hypotheses. They are not a complete search of mathematical literature.
Acquired bytes, exact versions, SHA-256 hashes and URLs are recorded in
`sources/ACQUISITION_RECEIPTS.json`.

1. **Giuseppe Bruno and Federico Pasqualotto, Quasiconvexity for the
   Dacorogna-Marcellini Energy, arXiv:2608.06367v1.**
   I acquired the author HTML and read Theorem 2, the heat criterion,
   exact-two-form argument and Appendix A. Their quartic equivalence
   requires both left and right SO(2) invariance. The relative-energy heat
   argument and exact-form cancellation are established there, as is
   separating a sharp generator from a determinant-square remainder.
   The supplied J_r has only the required left invariance: at r!=1 its
   rank-one values at e11 and e12 differ by beta_r; at r=1 its expansion
   still contains `(u-v)j/2`. Consequently the theorem does not apply
   directly to any of the sharp branches. Existing pinned FW proofs also
   exclude specifically stated linear-orbit positive-sum transfers, but
   that does not exclude every analytic consequence of earlier literature.
   [Primary paper](https://arxiv.org/html/2608.06367v1).

2. **Tim Netzer, Daniel Plaumann and Markus Schweighofer, Exposed Faces
   of Semidefinitely Representable Sets, SIAM J. Optim. 20 (2010).**
   I acquired the author-hosted original PDF and visually inspected
   printed pp.3-4. Theorem 2.3 records the Ramana-Goldman kernel
   characterization and exposure of every spectrahedral face. This is
   the precise classical obstruction needed for the incoming direct-LMI
   conclusion. `PROOFS.md` supplies an elementary kernel argument
   independently, including affine offsets and singular pencils. No new
   general theorem about spectrahedra is claimed. The original
   Ramana-Goldman DOI failed to open through the web tool; its 1995 full
   original proof was not acquired in this audit.
   [Primary research paper](https://www.math.uni-konstanz.de/~schweigh/publications/exposed.pdf).

3. **Christoph Hanselka and Rainer Sinn, Positive Semidefinite
   Univariate Matrix Polynomials, arXiv:1707.08261v1.**
   I acquired the original PDF, inspected its introduction and visually
   checked Corollary 2.8 and proof on printed p.9. Its polynomial-matrix
   factorization includes degenerate matrices. Applying it to the
   four-by-four quadratic matrix pencil, followed by the elementary
   degree bound in `PROOFS.md`, gives the eight-by-eight lift. This
   confirms rather than removes the distinction between direct LMIs and
   projections. Calderon's 1973 two-by-n biquadratic SOS theorem is
   another established route; only its primary publisher abstract was
   inspected in this audit, not its original three-page proof.
   [Hanselka-Sinn](https://arxiv.org/abs/1707.08261),
   [Calderon publisher record](https://www.sciencedirect.com/science/article/pii/0024379573900529).

4. **James Renegar, Hyperbolic Programs, and Their Derivative
   Relaxations, original 2004 technical-report version.**
   I acquired the author-posted original preprint and visually inspected
   Theorem 23 and its proof on printed pp.14-15. Every boundary face of a
   closed hyperbolicity cone is exposed. The additional audit corollary
   that K is not itself such a cone follows directly from the inherited
   nonexposed ray. Renegar's result supplies the implication, not a
   historical priority clearance for this particular K.
   [Original preprint](https://optimization-online.org/wp-content/uploads/2004/03/844.pdf).

5. **Current public openai/math catalogue.**
   The GitHub API resolved main to
   `1581d4cbdd69a0faf34b2089614fe2a814316a6a`, and I acquired the raw
   overview at that exact pin. The bounded catalogue search acquired no
   theorem for the present invariant ROC cone or its QC frontier. Entry
   095 concerns other hyperbolicity cones, and links both no-lift claims
   and a separate explicit-lift example. Those are producer statements
   about different mathematical objects, not applicable premises for K.
   No such no-lift transfer can hold here because the explicit acoustic
   lift already exists. The current pin equals the catalogue pin used in
   preceding PR #100; this audit does not find new catalogue capital.
   I did not fully audit those unrelated manuscript proofs.
   [Pinned primary repository overview](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/overview.tex).

Targeted public searches combined rank-one convexity, quartics, left
invariance, nine coefficients, nonexposed rays and spectrahedrality.
Their exact queries and acquisition limits are recorded in
`SEARCH_LOG.json`. No matching prior proof was acquired. Empty or unrelated
search results do not establish an absence theorem. The pinned earlier
FW priority audit acquired a wider collection of classical variational
papers and recorded remaining C4/symmetry qualifications. I read that
existing audit as historical capital, not as a replacement for the primary
comparisons above or as independent external review.

The appropriate provenance is therefore:

- Negative sharp QC, 3/1250 coercivity, full ambient nonexposure and the
  exact finite lift are inherited pinned capital.
- Direct nonspectrahedrality is an explicitly articulated consequence
  of inherited nonexposure plus classical facial geometry.
- Non-hyperbolicity in the nine coefficient variables is an additional
  immediate audit deduction using classical facial geometry.
- Historical-first status, correctness review external to this agent
  system, sharp positive-branch QC, and general planar Morrey remain
  unresolved.
