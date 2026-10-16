# Polynomial compensation across a double characteristic

16 October 2026. Repository reference supplied by the parent task: `astra-positive-memory-20261016`, commit `f80a8f15137575133ad2c9af975513b32e8fa93e`. No Git changes or external writes were made. This folder contains an internally derived theorem candidate and exact finite checks. External mathematical verification and historical priority remain **UNKNOWN**.

The strongest result is a complete polynomial/exponent classification for the degenerate conformal operator, together with a finite compiler for compatible failure sequences. A separate sharp quadratic inequality has both its optimal constant and optimal defect exponent. These results extend the supplied cubic selection rule. They do not settle the fixed-coefficient sharp conformal quasiconvexity inequality.

## Complete classification

Let \(D\phi=(a,b;c,d)\), \(q=\sigma a+d\), \(T_\sigma\phi=(q,c)\), with \(\sigma>0\). Express a homogeneous degree-\(m\) polynomial in \((a,b,c,q)\), and give these variables weights

\[
\operatorname{wt}(b)=0,\quad\operatorname{wt}(a)=1,
\quad\operatorname{wt}(c)=\operatorname{wt}(q)=2.
\]

For \(m\ge3\), \(0<\alpha\le m\), and finite \(1<p,s<\infty\) satisfying
\(\alpha/p+(m-\alpha)/s=1\), the following are equivalent:

1. \(|\langle P(D\phi)\rangle|\le K\|T_\sigma\phi\|_p^\alpha\|D\phi\|_s^{m-\alpha}\) for all periodic compatible maps.
2. The same estimate holds for \(\|P(D\phi)\|_1\).
3. Every monomial of \(P(a,b,c,q-\sigma a)\) has weight at least \(2\alpha\).

Degree two has one exact signed exception: subtract any multiple of the **true** determinant \(aq-\sigma a^2-bc\) before testing the low weights. The absolute criterion has no such exception. Degree one is excluded because every periodic linear gradient integral vanishes.

The statement includes periodic Sobolev maps with \(D\phi\in L^s\), \(T_\sigma\phi\in L^p\), and zero-boundary maps on nonempty bounded domains. Zero-boundary necessity uses periodic tiling, a large smooth cutoff, and isotropic rescaling. No endpoint estimate is asserted.

The analytic ingredient is the supplied mixed-derivative/Hodge estimate \(\|a\|_t^2\lesssim\|T_\sigma\phi\|_p\|D\phi\|_s\), with \(2/t=1/p+1/s\). Hölder interpolation gives an explicit coefficient-dependent constant for every admissible polynomial. Necessity is stronger than a formal kernel test: the exact compatible family has

\[
a_N=N^{-1}\psi_{xy}+N^{-2}F_x,\quad
b_N=\psi_{yy}+N^{-1}F_y,
\]
\[
c_N=-\sigma N^{-2}\psi_{xx}+N^{-3}G_x,\quad
q_N=N^{-2}k,\qquad k=\sigma F_x+G_y,
\]

in base variables \((x,Ny)\). The Hessian of \(\psi\) and the mean-zero scalar \(k\) are independent. The only signed leading cancellation is the classical quadratic Hessian determinant; there are no homogeneous degree-\(m\ge3\) cancellations. A complete elementary Euler-Lagrange jet proof and the quantitative monomial bound are in [CORE_THEOREM_v1.md](CORE_THEOREM_v1.md).

## A sharp quadratic operation

For every periodic \(W^{1,2}\) map,

\[
\boxed{|\langle\sigma a^2+bc\rangle|
\le\sigma^{-1/2}\|T_\sigma\phi\|_2^{3/2}\|D\phi\|_2^{1/2}.}
\]

Both the constant and the defect exponent are optimal. The determinant identity gives \(\sigma\|a\|_2^2\le EM\), while \(\langle\sigma a^2+bc\rangle=\langle aq\rangle\); Cauchy-Schwarz gives the displayed bound. Equality holds for \(g=0\), \(f=f(x)\). With \(\varepsilon=N^{-1}\), \(\theta=x+Ny\), the exact compatible choice

\[
f_N=(-\varepsilon+\varepsilon^2/(2\sigma))\sin\theta,
\quad g_N=(\sigma\varepsilon^2+\varepsilon^3/2)\sin\theta
\]

has defect \(O(\varepsilon^2)\), bounded full gradient, and
\(\langle-(\sigma a_N^2+b_Nc_N)\rangle=\varepsilon^3/2-\varepsilon^4/(4\sigma)\). Therefore every exponent greater than \(3/2\) fails. The absolute estimate for this same quadratic permits only exponent one. This gives an explicit signed-versus-absolute compensation gap with a sharp constant.

## Finite counterexample construction and general operator class

For rational \(\sigma\) and rational coefficients, every inadmissible polynomial has a signed failure witness built from at most \(m\) cosine modes of coordinate frequency at most \(5(m-1)\). The compiler polarizes the first forbidden weighted part. Its resonance polynomial has degree at most four in every independent frequency coordinate, so a five-point positive grid detects it. Positivity ensures only the all-plus and all-minus sign resonances survive. A further \((m+1)\)-point amplitude grid produces a nonzero exact average.

The declared worst case is \(2^m5^{2(m-1)}\) resonance tests and then \((m+1)^m\) amplitude tests, with exponential rational arithmetic cost. Repeated same-source cosine modes are grouped before amplitudes are selected, so the merged-mode amplitudes really are at most \(m+1\). Coefficient bit lengths remain an additional cost. The resulting exact average is a polynomial in \(N^{-1}\), yielding an explicit ratio lower bound \(cN^{2\alpha-j}\) above the allowed exponent. [EXTENSIONS_v2.md](EXTENSIONS_v2.md) contains the corrected separate proof, cost accounting, and audit boundaries; superseded v1 is preserved internally.

The same file shows that every real two-by-two first-order pencil with \(\det L(\xi)=\gamma\ell(\xi)^2\), \(\gamma\ne0\), and rank one on its nonzero characteristic covectors reduces to this operator by invertible coordinate/component changes. This is an elementary Jordan reduction; the transferred weighted classification is the consequence. General coordinate changes carry a torus to a transformed lattice. The corrected proof transfers through compact-support estimates, large cutoffs, periodic averaging, and the exact cancellation of norm Jacobian factors. No standard integer torus automorphism is assumed.

## Exact replay and examples

Run `python3 weighted_jet_verify.py`. The replay passed exact null-polynomial linear constraints through degree eight, weighted dimension counts, target cubic weights, six compatible Fourier witnesses, and a nontrivial pencil conjugation. It uses runtime checks rather than Python `assert` and writes [VERIFICATION_RECEIPT.json](VERIFICATION_RECEIPT.json).

At \(\sigma=2\), selected exact signed averages are:

| Polynomial | Compatible average | Why the witness matters |
|---|---:|---|
| \(ab^2\) | \(-3/N\) | Forbidden first jet |
| \((2a^2+bc)b\) | \(7/N^2\) | Its leading restriction vanishes on every single plane wave |
| \(qb^2\) | \(1/(4N^2)\) | Requires an independent leading \(q\); a \(q=0\) test misses it |
| Target \(C_1\) | \(3/N^3+12/N^5\) | Optimal weighted power \(3/2\) |
| \((2a^2+bc)^2\) | \(19/N^4\) | Another single-plane-wave-invisible obstruction |

The finite replay does not verify analytic interpolation, the all-degree necessity proof, optimal constants beyond the explicit quadratic argument, or historical originality. `PUBLICATION_ALLOWLIST.json` explicitly permits only current reports, code, and provenance/verification receipts; downloaded full source PDFs, extracted full texts, page images, and superseded artifacts remain internal and excluded.

## Prior mathematics and the remaining sharp obligation

The planar Hessian null-polynomial structure is explicitly prior mathematics: Ball–Currie–Olver's Theorems 3.4 and 4.1 classify higher-order null Lagrangians, and Example 4.10(c), p.155, gives exactly affine terms plus the scalar planar Hessian determinant. Their proof also uses polarized resonances. We read those primary sections and visually checked the example; neither the null lemma nor Fourier polarization is presented as invented here. [Primary paper](https://www-users.cse.umn.edu/~olver/e_/bco.pdf).

Müller's Lemma 2 gives a signed cubic defect estimate for a different nonconstant-rank axis constraint, proved by conic frequency splitting. Its proof and corollary were read in full, with the main lemma visually checked. It is a substantive predecessor, not merely an abstract analogy. It does not state the present weighted classification; this difference does not establish priority. [Primary preprint](https://files-www.mis.mpg.de/mpi-typo3/preprints/1998/preprint1998_19.pdf).

Guerra–Raiţă's systematic theory assumes constant rank; the present Jordan symbol drops rank, so that framework cannot simply be substituted as a proof of the whole theorem. Its higher-order null-Lagrangian discussion does explain the classical necessity machinery. [Primary paper, Sections 1 and 5](https://arxiv.org/html/1909.03923).

The complete result is therefore a useful specialized assembly of classical interpolation, null-Lagrangian theory, Jordan algebra, and finite polynomial interpolation. No irreducibly new general analytic machinery or externally established novelty emerged. The precise combined classification and bounded-frequency compiler would need a broader priority search before any originality claim.

The target cubic \(C_r\) has lowest weight three, yielding the optimal exponent estimate \(\|C_r(D\phi)\|_1\lesssim_r\|T_{r+1}\phi\|_2^{3/2}\|D\phi\|_6^{3/2}\). Its receiving norm is \(L^6\). The required sharp conformal inequality uses the unchanged \(L^4\)-scale quartic energy and the exact threshold one. Neither that threshold nor concentration control is supplied here. The fixed-coefficient conformal and general planar quasiconvexity obligations remain open in this report.
