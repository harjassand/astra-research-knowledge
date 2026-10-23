# Standard-form entropy gates: order domination and finite-mixture identity

Scope: primary-source pinning for (i) the normal-functional bound \(\omega\leq\phi/p\Rightarrow D(\omega\|\phi)\leq\log(1/p)\), and (ii) the finite ensemble / Donald identity. No claim about recovery or repetition is made here.

## General von Neumann algebra and order gate

Use the standard Araki relative entropy convention \(D(\rho\|\sigma)\), with first argument the state being distinguished and second argument the reference. Hiai, *Quantum \(f\)-divergences in von Neumann algebras I: Standard \(f\)-divergences*, arXiv:1805.02050, is a primary source for all normal positive functionals on an arbitrary von Neumann algebra (not just finite algebras): §2.1 gives the standard form and unique natural-cone representatives for every normal positive functional; Definition 2.1 defines \(S_f\); \(S_{t\log t}(\rho\|\sigma)\) is the usual relative entropy (Example 3.6); Proposition 2.3(3)–(4) gives joint homogeneity and direct-sum additivity; Theorem 4.1(iv) gives data processing for normal unital positive Schwarz maps. Corollary 4.2(1) gives

\[
D(\rho\|\sigma)\geq \sigma(1) f\!\left(\frac{\rho(1)}{\sigma(1)}\right),\qquad f(t)=t\log t,
\]
with equality for proportional nonzero functionals. In particular, for a normal state \(\omega\) and \(0<p\leq1\), \(D(\omega\|p\omega)=\log(1/p)\).

The order bound follows directly, including nonfaithful states. For \(0<p<1\), write \(\phi=p\omega+(1-p)\nu\), where \(\nu=(\phi-p\omega)/(1-p)\) is a normal state. In \(M\oplus M\), set
\[
\Upsilon=\omega\oplus0,\qquad \Xi=p\omega\oplus(1-p)\nu.
\]
By direct-sum additivity and the proportional-state equality, \(D(\Upsilon\|\Xi)=\log(1/p)\). Apply data processing to the diagonal unital normal *-homomorphism \(\iota:M\to M\oplus M\), \(x\mapsto x\oplus x\). Its pullbacks are \(\Upsilon\circ\iota=\omega\) and \(\Xi\circ\iota=\phi\); hence
\[
D(\omega\|\phi)\leq\log(1/p).
\]
For \(p=1\), order and normalization force \(\omega=\phi\). This argument requires no density operator, finite trace, or faithful state, and has no support-regularization limit. It is a derivation from the cited Hiai properties, rather than a separately named theorem in that paper.

**Pins:** Hiai §2.1 and Definition 2.1; Proposition 2.3(3)–(4); Example 3.6; Theorem 4.1(iv); Corollary 4.2(1). Primary source: [arXiv:1805.02050](https://arxiv.org/abs/1805.02050).

## Finite ensemble identity

Petz, *Relative entropy in quantum information theory* (1999), Theorem 1.1(1e), states for positive functionals \(\omega_i\) on a C*-algebra and \(\omega=\sum_i\omega_i\):
\[
S(\omega,\phi)+\sum_i S(\omega_i,\omega)=\sum_i S(\omega_i,\phi).
\]
The chapter says this property is from references [2] and [4]; [4] is M. J. Donald, “Relative Hamiltonians which are not bounded from above,” *J. Funct. Anal.* 91 (1990), 143–173. Petz’s statement is explicit and covers the required algebraic setting, while the accessible source copy is an expository chapter, not Donald’s original proof. I could not inspect Donald’s full paper text; ScienceDirect exposed only the abstract/metadata in this pass. Therefore the exact identity is pinned to Petz’s theorem statement and attribution, but the original Donald proof is **not independently audited here**.

For normalized normal states \(\rho_i\), positive weights \(p_i\), and \(\bar\rho=\sum_i p_i\rho_i\), this yields the familiar version
\[
\sum_i p_iD(\rho_i\|\sigma)
= D(\bar\rho\|\sigma)+\sum_i p_iD(\rho_i\|\bar\rho),
\]
whenever the displayed quantities are finite. One detail matters when substituting \(\omega_i=p_i\rho_i\): the relative entropy of positive, unnormalized functionals is not homogeneous in only its first argument. Hiai’s Definition 2.1 and Eq. (2.7) imply
\[
S(p_i\rho_i\|\eta)=p_iD(\rho_i\|\eta)+p_i\log p_i
\]
for normalized \(\eta\). The same \(\sum_i p_i\log p_i\) appears on both sides of Petz’s (1e) and cancels; joint homogeneity applies to \(S(p_i\rho_i\|p_i\bar\rho)\). Do not silently use joint homogeneity with only the first argument scaled. Avoid subtracting extended infinities; invoke the formula in the finite-value regime used by the argument.

Petz’s chapter: [PDF](https://www.maphysto.dk/publications/MPS-misc/1999/16.pdf), a 114-page proceedings booklet; the chapter begins at PDF p. 83 (printed p. 83), and §1, Theorem 1.1(1e) is on PDF pp. 83–84. The statement is in the theorem on printed p. 83; the attribution is printed p. 84, and the Donald reference is printed p. 87. Donald original: [DOI record](https://doi.org/10.1016/0022-1236(90)90050-U).
