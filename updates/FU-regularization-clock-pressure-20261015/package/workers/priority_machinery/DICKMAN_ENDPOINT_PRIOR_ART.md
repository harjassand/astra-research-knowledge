# The supplied Pauli noise already has the critical Dickman tail

Date: 2026-10-15. Status: exact primary-source comparison and internally derived postconvolution consequence. Historical priority of the universal tuple theorem and sharp quantum obstruction remains UNKNOWN.

## Original primary theorem actually acquired

W. Vervaat, *Success epochs in Bernoulli trials (with applications in number theory)*, Mathematical Centre Tracts 42 (1972), [CWI original full text](https://ir.cwi.nl/pub/19565/19565A.pdf), SHA-256 `ce030b5e2331116d9cb5575300aae06942c335cd0dea3aa350712f0066f427dd`. This is a 173-page scanned monograph. PDF pages 97–102, printed pages 90–95, were rendered and visually read. The extracted text is empty; the image files are the read receipt. This is not a conclusion from a search snippet or a later citation.

Theorem 4.7.7 gives, for every alpha>0,

\[
D_\alpha=\sum_{k\ge1}\prod_{j=1}^k U_j^{1/\alpha},\qquad
\mathbb E e^{zD_\alpha}
=\exp\!\left[\alpha\int_0^1{e^{zu}-1\over u}\,du\right],
\]

its absolutely continuous density q_alpha, its convolution semigroup, and its eventual decrease. Lemma 4.7.9, printed pp. 94–95, states the more precise expansion whose consequence is

\[
-\log q_\alpha(t)
=t\bigl(\log t+\log\log t-1-\log\alpha+o(1)\bigr).
\tag{1}
\]

Its proof explicitly extends de Bruijn's alpha=1 argument. Iksanov–Iksanov's [2026 primary manuscript](https://arxiv.org/pdf/2604.14396v2), PDF p.5 Eq.(8), also states this expansion and routes it to Vervaat. The acquired 2026 PDF has SHA-256 `d3000a925681f0bc3b253d3af3ee2ffa8348601981c3c41eabe5516d7c7d4022`; its internal arXiv stamp says 8 August 2026, although search metadata showed an earlier v2 date. The byte pin is the identification used here. Hensley's 1986 convolution-powers paper was located, but its requested publisher PDF returned 403 and is not a theorem premise.

## Exact consequence for the supplied noise

The supplied DATA, lines 597–652, defines D=D_(1/2), B a fair Bernoulli, U uniform, omega uniform on the two-sphere, and

\[
Z=S\omega,\qquad S=1+2(D+BU).
\]

The supplied algebra identifies this as scalar noise regularizing the Pauli triple. That transform identity was not separately reaudited here. Conditional on that identity, the following tail conclusions are unconditional calculations from the actual scalar law.

Put t=(r-1)/2. For r>3 the density of S is

\[
f_S(r)={1\over4}q_{1/2}(t)
+{1\over4}\int_0^1q_{1/2}(t-u)\,du.
\]

Since q_(1/2) is decreasing for t>1,

\[
\tfrac12q_{1/2}(t)\le f_S(r)\le\tfrac12q_{1/2}(t-1).
\]

Applying (1) at both endpoints and using alpha=1/2 gives

\[
-\log f_S(r)
={r\over2}(\log r+\log\log r-1+o(1)).
\]

The Lebesgue density of Z is p(x)=f_S(|x|)/(4 pi |x|^2). The radial Jacobian costs O(log r), so

\[
\boxed{-\log p(x)={r\over2}
  (\log r+\log\log r-1+o(1)).}
\tag{2}
\]

Thus the special Pauli noise already attains leading coefficient 1/2 and iterated-log coefficient 1. The shape r(log r+loglog r) is classical Dickman asymptotics, and is not itself a new discovery. For the scaled tuple R sigma, scale Z by R to obtain

\[
-\log p_R(x)={r\over2R}
(\log r+\log\log r-1-\log R+o(1)).
\tag{3}
\]

This does not attain the new necessary fixed-offset bound b<=log(2/R)-1; its offset is smaller by log 2. No optimal-offset claim follows.

## Smooth radial endpoint noise also follows for this particular tuple

Let G_sigma be any nondegenerate centered isotropic Gaussian density and put p_tilde=p*G_sigma. If W*p is positive, associativity and positive postconvolution give W*p_tilde>=0. The new density is radial, smooth, everywhere positive, and has every exponential moment. All its derivatives are exponentially weighted integrable, since they are p*(derivatives of G_sigma).

Gaussian postconvolution preserves the full expansion (2), including its constant -1. Here is a direct proof that does not assume p is bounded near its spherical singularity. Write h(r)=(r/2)(log r+loglog r-1). Fix eta in (1/2,1). For |z|<=r^eta,

\[
h(|x-z|)=h(r)+O(r^\eta\log r)=h(r)+o(r),
\]

and the error in (2) is uniformly o(r) on this annulus. Hence this part of the convolution is at most exp[-h(r)+o(r)]. On |z|>r^eta, split the Gaussian exponent in two to get

\[
\int_{|z|>r^\eta}p(x-z)G_\sigma(z)\,dz
\le C_\sigma e^{-r^{2\eta}/(4\sigma^2)}\int p(x-z)\,dz
=C_\sigma e^{-r^{2\eta}/(4\sigma^2)}.
\]

This is negligible compared with exp[-h(r)+o(r)]. The integral on |z|<=1 supplies the matching lower bound exp[-h(r)+o(r)] times a fixed positive Gaussian mass. Consequently -log p_tilde(x)=h(r)+o(r).

This removes nonsmoothness as a meaningful distinction for *existence of smooth radial endpoint noise for the Pauli triple*. It does not prove strict log-concavity, a uniform construction for every bounded tuple, a common scale depending only on m,R, or the universal tilted-moment obstruction. Those are separate statements and retain their own correctness and priority obligations.
