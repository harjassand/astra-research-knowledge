# Constructive witnesses and the full double-characteristic pencil class

Status: separately derived extensions, unreviewed. These extend `CORE_THEOREM_v1.md`. Finite exact checks below support algebra only; they are not a substitute for a separate mathematical audit. Priority and external verification are UNKNOWN.

## A. A finite signed witness compiler

Let \(R(a,b,c,q)\) be a nonzero homogeneous degree-\(m\) polynomial, \(m\ge2\), and suppose

\[
\langle R(\psi_{xy},\psi_{yy},-\sigma\psi_{xx},k)\rangle
\]

is not identically zero on periodic \(\psi\) and mean-zero \(k\). For \(m\ge3\), the core null-polynomial lemma guarantees this for every nonzero \(R\). For \(m=2\), exclude the span of \(-\sigma a^2-bc\).

There are witnesses \(\psi,k\) made from a combined total of at most \(m\) cosine modes, with integer cosine amplitudes in \(\{1,\ldots,m+1\}\), and with every frequency coordinate of absolute value at most \(5(m-1)\). They can be found by a finite exhaustive algorithm. Rational \(\sigma>0\) and rational coefficients give entirely exact rational arithmetic.

**Proof and construction.** Let \(\mathcal R\) be the symmetric polarization of \(R\), normalized by \(R(v)=\mathcal R(v,\ldots,v)\). A Hessian cosine of frequency \(\nu=(\nu_x,\nu_y)\) contributes the vector

\[
H(\nu)=(-\nu_x\nu_y,-\nu_y^2,\sigma\nu_x^2,0),
\]

whereas an independent scalar cosine contributes \(Q=(0,0,0,1)\). Fourier expansion of any nonzero signed average shows that for some assignment \(V_i\in\{H(\nu_i),Q\}\), with \(\sum_i\nu_i=0\),

\[
B(\nu_1,\ldots,\nu_{m-1})
=m!\,\mathcal R(V_1,\ldots,V_m)\ne0,
\qquad\nu_m=-\sum_{i<m}\nu_i.
\]

For each fixed assignment, \(B\) is a polynomial in the \(2(m-1)\) frequency coordinates. Each coordinate appears only in its own slot and the final slot. Both slots have degree at most two in it. Thus its degree in each coordinate is at most four. A nonzero such polynomial cannot vanish on the full product grid

\[
\nu_i\in\{1,2,3,4,5\}^2,\qquad 1\le i<m. \tag{1}
\]

Search this grid and the \(2^m\) assignments to find a nonzero \(B\). Since every component of the first \(m-1\) frequencies is positive and the final frequency is the negative of their sum, the only sign choices satisfying \(\sum_i\epsilon_i\nu_i=0\), with \(\epsilon_i\in\{-1,1\}\), are all plus and all minus. Indeed, if the last sign is plus, positivity forces every earlier sign to be plus; reverse all signs for the other case. Therefore

\[
\left\langle\prod_{i=1}^m\cos(\nu_i\cdot x)\right\rangle=2^{1-m}. \tag{2}
\]

Put each cosine into \(\psi\) or \(k\) according to its assignment, initially with separate amplitudes \(t_i\). The signed average is a homogeneous degree-\(m\) polynomial \(J(t_1,\ldots,t_m)\), and the coefficient of \(t_1\cdots t_m\) is exactly \(2^{1-m}B\ne0\). Repeated frequencies do not invalidate this coefficient identity: the amplitudes remain independent labels before evaluation. Since the degree of \(J\) in each amplitude is at most \(m\), the product grid \(t_i\in\{1,\ldots,m+1\}\) contains a point with nonzero signed average. This proves the claim.

No absent nonresonance assumption is used: positivity of (1) is precisely what excludes every other sign resonance. The argument deliberately uses five frequency values and \(m+1\) amplitude values; smaller universal grids are not asserted.

### Cost and exact divergence certificate

At most

\[
2^m5^{2(m-1)}
\]

resonance tests and then at most \((m+1)^m\) amplitude tests suffice. A resonance coefficient can be evaluated by

\[
m!\mathcal R(v_1,\ldots,v_m)
=\sum_{S\subseteq\{1,\ldots,m\}}(-1)^{m-|S|}
 R\left(\sum_{i\in S}v_i\right),
\]

using \(2^m\) polynomial evaluations. If \(D\le\binom{m+3}{3}\) is the number of monomials, direct evaluation gives an upper bound of order \(mD\,4^m5^{2(m-1)}\) rational arithmetic operations for the resonance stage. The amplitude stage can use exact Laurent polynomial multiplication; a deliberately crude finite bound is \(O(Dm(2m)^{m+1}(m+1)^m)\) rational operations if every factor has at most \(2m\) frequencies and products are expanded without collecting repeated terms. These bounds are exponential, not an efficiency claim. Bit costs depend additionally on the input rational coefficient lengths; no unit-cost rational arithmetic claim is made.

Now take the lowest weighted component \(R=P_j\) of an inadmissible polynomial, and use the exact compatible family (3) of the core theorem. With the cosine data above, solve \(\Delta\chi=k\), \(F=\chi_x/\sigma\), \(G=\chi_y\). All Fourier coefficients remain rational. Exact integration gives a rational polynomial

\[
\langle P(D\phi_N)\rangle=\sum_{\ell=j}^{3m}I_\ell N^{-\ell},\qquad I_j\ne0. \tag{3}
\]

Let \(S=\sum_{\ell>j}|I_\ell|\), and choose
\(N\ge\max\{1,\lceil2S/|I_j|\rceil\}\). Then the numerator is at least \(|I_j|N^{-j}/2\). Fourier coefficient sums give explicit constants \(M_0,E_0\) with

\[
\|D\phi_N\|_s\le M_0,\qquad
\|T_\sigma\phi_N\|_p\le E_0N^{-2}
\]

for every finite \(p,s\). Consequently, at any excluded power \(\alpha>j/2\), the ratio is at least

\[
\frac{|I_j|}{2E_0^\alpha M_0^{m-\alpha}}N^{2\alpha-j}. \tag{4}
\]

This is an explicit quantitative failure sequence. It also gives a witness for the quadratic signed theorem after subtracting the true gradient determinant first. It does not compute the best constant in any admissible estimate.

## B. Every nontrivial two-by-two double-characteristic pencil

Let \(\mathcal L\) be a real constant-coefficient first-order operator on two potentials in the plane. Suppose its symbol satisfies

\[
\det L(\xi)=\gamma\ell(\xi)^2,\qquad\gamma\ne0,
\]

for a nonzero real linear form \(\ell\), and suppose \(L(\xi)\) has rank one for every nonzero \(\xi\) with \(\ell(\xi)=0\). Then invertible real changes of physical coordinates, potential components, and output components transform it to

\[
\begin{pmatrix}\partial_x&\partial_y\\0&\partial_x\end{pmatrix}. \tag{5}
\]

Thus the core theorem classifies polynomial estimates for this entire operator class in the corresponding adapted gradient coordinates. Multiplicative constants change only by finite norms of the fixed invertible transformations and their inverses. The determinant exception remains a true gradient determinant, multiplied by a nonzero constant.

**Proof.** Choose covector coordinates with \(\ell=\xi_x\), and write \(L(\xi)=A\xi_x+B\xi_y\). Then \(A\) is invertible. Set \(N=A^{-1}B\). Dividing the determinant identity by \(\det A=\gamma\) gives

\[
\det(\xi_x I+\xi_yN)=\xi_x^2.
\]

Hence \(\operatorname{tr}N=\det N=0\), so Cayley-Hamilton gives \(N^2=0\). The rank assumption gives \(N\ne0\). Choose \(v\) with \(u=Nv\ne0\); then \(Nu=0\), and \((u,v)\) is a basis. If \(S\) has columns \((u,v)\), then

\[
S^{-1}NS=\begin{pmatrix}0&1\\0&0\end{pmatrix},
\qquad
S^{-1}A^{-1}L(\xi)S
=\begin{pmatrix}\xi_x&\xi_y\\0&\xi_x\end{pmatrix}.
\]

This proves (5). For periodic functions, a general real coordinate change carries the torus to its transformed lattice; it need not preserve the standard integer torus. The statement is immediate on the transformed torus, and for compactly supported/zero-boundary maps on the transformed domain. No assertion about integer torus automorphisms is smuggled in. For a purely rational pencil, an adapted rational construction is available when its characteristic form and chosen vectors are rational; the algebraic operator equivalence itself allows arbitrary real coefficients.

This pencil reduction is elementary Jordan theory. It is not a new operator normal-form theorem. The result here is the transfer of the complete nonlinear weighted polynomial estimate, with the same explicit exclusions and null-Lagrangian qualification.

## C. Finite replay

Run `python3 weighted_jet_verify.py`. It uses explicit runtime checks, not Python `assert`. It checks the null-polynomial algebra through degree eight, weighted monomial dimensions, target cubic weights, six exact compatible witness sequences, and one nontrivial pencil conjugation fixture. It writes `VERIFICATION_RECEIPT.json`.

The six witnesses include a cubic and a quartic whose leading restrictions vanish on every single plane wave; they nevertheless have nonzero multimode compatible averages. Another witness requires an independent leading \(q\), so setting \(q=0\) throughout would miss it. These cases are why the construction adds something beyond testing only the formal kernel or a rank-one curve.
