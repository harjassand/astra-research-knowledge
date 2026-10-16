# Constructive witnesses and general pencils: corrected version 2

16 October 2026. This version supersedes `EXTENSIONS_v1.md`, which is preserved internally. Two audit qualifications are incorporated: repeated same-source cosine modes are grouped before amplitudes are selected; periodic transfer under an arbitrary real coordinate change is proved by compact-support localization rather than asserted to be immediate. This remains internally derived and unreviewed externally. Historical priority is UNKNOWN.

## A. Finite bounded-frequency signed witnesses

Let \(R(a,b,c,q)\) be homogeneous of degree \(m\ge2\), and suppose its average under
\((a,b,c,q)=(\psi_{xy},\psi_{yy},-\sigma\psi_{xx},k)\) is not identically zero for periodic \(\psi\) and mean-zero \(k\). This holds for every nonzero \(R\) when \(m\ge3\); at degree two the excluded null span is \(-\sigma a^2-bc\).

Then there is a nonzero signed witness using a combined total of at most \(m\) distinct same-source cosine modes, with every cosine amplitude an integer between one and \(m+1\), and every frequency coordinate of absolute value at most \(5(m-1)\). A mode of \(\psi\) and a mode of \(k\) are distinct sources even when their cosine frequencies coincide. Rational \(\sigma>0\) and rational input coefficients make the finite search exactly rational.

Let \(\mathcal R\) be the symmetric polarization, normalized by \(R(v)=\mathcal R(v,\ldots,v)\). Hessian and independent-scalar modes contribute respectively

\[
H(\nu)=(-\nu_x\nu_y,-\nu_y^2,\sigma\nu_x^2,0),
\qquad Q=(0,0,0,1).
\]

Fourier expansion of a nonzero average implies that, for some assignment of these two types to \(m\) labelled slots and frequencies summing to zero,

\[
B(\nu_1,\ldots,\nu_{m-1})
=m!\mathcal R(V_1,\ldots,V_m)\ne0,
\qquad \nu_m=-\sum_{i<m}\nu_i.
\]

For a fixed type assignment, \(B\) is a polynomial of degree at most four in each independent frequency coordinate: a coordinate appears in its own slot and the final slot, with degree at most two in each. Thus a nonzero \(B\) is detected on

\[
\nu_i\in\{1,2,3,4,5\}^2\quad(1\le i<m). \tag{1}
\]

Every component of the first \(m-1\) frequencies is positive. Consequently the only sign resonances \(\sum\epsilon_i\nu_i=0\), with \(\epsilon_i=\pm1\), are all plus and all minus. If the final sign is plus, the positive sum of the earlier frequencies forces every earlier sign to be plus; the other case reverses all signs. Therefore the product of all \(m\) cosines has average \(2^{1-m}\).

Give the labelled cosine slots independent amplitudes \(t_i\), assigning each to \(\psi\) or \(k\). Their integral \(J(t)\) is a homogeneous degree-\(m\) polynomial with nonzero coefficient \(2^{1-m}B\) at \(t_1\cdots t_m\).

**Group before choosing amplitudes.** Identify \(\nu\) and \(-\nu\) as the same cosine frequency, and merge repeated frequencies within each source. There are \(h\le m\) groups. The labelled polynomial is exactly the grouped polynomial evaluated at the sum of amplitudes within each group. Hence the grouped polynomial is nonzero: otherwise the labelled polynomial would vanish identically. Its degree in each of the \(h\) group amplitudes is at most \(m\), so evaluating the grid \(\{1,\ldots,m+1\}^h\) finds a nonzero value. This proves the claimed **merged-mode** amplitude bound; selecting amplitudes before merging would not have proved it.

### Cost and quantitative failure

The search needs at most \(2^m5^{2(m-1)}\) resonance tests and then at most \((m+1)^h\le(m+1)^m\) amplitude tests. One resonance coefficient costs \(2^m\) polynomial evaluations via

\[
m!\mathcal R(v_1,\ldots,v_m)
=\sum_{S\subseteq\{1,\ldots,m\}}(-1)^{m-|S|}
R\left(\sum_{i\in S}v_i\right).
\]

For at most \(D\le\binom{m+3}{3}\) monomials, a direct upper bound is \(O(mD4^m5^{2(m-1)})\) rational arithmetic operations in the resonance stage. Expanding Fourier products without collecting terms gives a crude finite amplitude-stage bound \(O(Dm(2m)^{m+1}(m+1)^m)\). Input rational bit lengths are an additional cost. These are exponential bounds, not an efficient algorithm claim.

Apply the construction to the first forbidden weighted part \(P_j\), and use the exact compatible family in the core theorem. Solving \(\Delta\chi=k\), \(F=\chi_x/\sigma\), \(G=\chi_y\) preserves rational Fourier coefficients. Exact integration yields

\[
\langle P(D\phi_N)\rangle=\sum_{\ell=j}^{3m}I_\ell N^{-\ell},
\qquad I_j\ne0.
\]

Let \(S=\sum_{\ell>j}|I_\ell|\). For \(N\ge\max\{1,\lceil2S/|I_j|\rceil\}\), the numerator is at least \(|I_j|N^{-j}/2\). Fourier coefficient sums give explicit bounds \(M\le M_0\), \(E\le E_0N^{-2}\). At \(\alpha>j/2\), the ratio is therefore at least

\[
\frac{|I_j|}{2E_0^\alpha M_0^{m-\alpha}}N^{2\alpha-j}.
\]

At degree two first subtract the true gradient determinant as required by the signed classification. This compiler does not find the best admissible estimate constant.

## B. Full real two-by-two double-characteristic class

Let \(\mathcal L\) have a real two-by-two first-order homogeneous symbol with

\[
\det L(\xi)=\gamma\ell(\xi)^2,\qquad\gamma\ne0,
\]

where \(\ell\) is nonzero, and assume rank one at every nonzero characteristic covector. Choose adapted covector coordinates with \(\ell=\xi_x\), so \(L=A\xi_x+B\xi_y\) with \(A\) invertible. Then \(N=A^{-1}B\) has zero trace and determinant, hence \(N^2=0\), while the rank assumption gives \(N\ne0\). Choose \(v\) with \(u=Nv\ne0\), and let \(S=(u,v)\). Directly,

\[
S^{-1}A^{-1}L(\xi)S
=\begin{pmatrix}\xi_x&\xi_y\\0&\xi_x\end{pmatrix}. \tag{2}
\]

Thus every such pencil is equivalent to the canonical operator by invertible changes of physical coordinates, potential components, and output components. This is classical Jordan algebra. The consequence is transfer of the complete nonlinear polynomial classification.

### Spatial norms and arbitrary lattices

Write the physical coordinate change as \(y=Cx\), and the potential change as \(\phi(x)=S\psi(Cx)\). Then

\[
D_x\phi=S(D_y\psi)C,
\quad P'(B)=P(SBC),
\quad dx=|\det C|^{-1}dy.
\]

The fixed invertible output transformation gives equivalent defect norms. In the unnormalized integral estimate the Jacobian on the left is \(|\det C|^{-1}\); on the right its exponent is
\(-\alpha/p-(m-\alpha)/s=-1\). These factors cancel. The remaining norm constants are controlled by the fixed invertible matrices and their inverses. The determinant exception remains a nonzero scalar multiple of the true gradient determinant, since \(\det(SBC)=\det S\det C\det B\).

A real coordinate change carries the original lattice \(\Gamma\) to \(C\Gamma\), generally a skew lattice. To pass from the compact-support theorem to periodic maps on **any** lattice, take a periodic smooth map \(\psi\), multiply it by a fixed nonnegative cutoff \(\eta(y/R)\), and apply the compact estimate. The added gradient/defect terms are \(O(R^{-1})\), since the periodic potential is bounded. Periodic averaging as \(R\to\infty\) gives

\[
|\langle P(D\psi)\rangle_\Gamma|
\le K\frac{(\int|\eta|^p)^{\alpha/p}
             (\int|\eta|^s)^{(m-\alpha)/s}}
            {\int\eta^m}
\|T\psi\|_{L^p(\Gamma)}^\alpha
\|D\psi\|_{L^s(\Gamma)}^{m-\alpha}, \tag{3}
\]

with normalized cell norms. The powers of \(R\) cancel by the same exponent balance. The cutoff quotient is a finite fixed constant, independent of \(\psi\). The analogous argument proves the absolute bound. This establishes sufficiency on an arbitrary lattice without assuming an integer torus automorphism or an unproved mixed-derivative estimate on an irrational lattice.

Conversely, the core necessity fields can first be localized into a compact ball (core proof), then rescaled into the interior of any fundamental cell and extended periodically. The cell normalization factors cancel by the exponent balance. Their divergent ratios survive. Hence the same algebraic criterion is necessary on every lattice. Alternatively, use the transformed compact-domain theorem directly for zero-boundary maps. No sharp numerical constant is transferred through the cutoff quotient.

For rational input pencils a rational adapted reduction is available if the characteristic form and basis choices are rational. The abstract equivalence (2) permits arbitrary real coefficients; an exact rational witness compiler is asserted only after a rational reduction with rational polynomial data.

## C. Replay boundary

`weighted_jet_verify.py` and `VERIFICATION_RECEIPT.json` now implement the grouped-mode version. They preserve the exact row curls and determinant-null averages and independently check a nontrivial Jordan fixture. The earlier compiler and receipt are retained as `_v1` files for internal audit history. Full primary-source PDFs, extracted texts, page images, and superseded extension artifacts are excluded by the publication allowlist.

The algebra replay is finite. The all-degree Fourier interpolation argument, localization limits, and operator-class transfer remain written mathematical proofs requiring external review. This result does not supply the unchanged sharp conformal quasiconvexity bound or historical-priority clearance.
