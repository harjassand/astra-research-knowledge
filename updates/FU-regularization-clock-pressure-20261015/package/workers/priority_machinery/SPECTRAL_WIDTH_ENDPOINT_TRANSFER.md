# Coordinated endpoint theorem with spectral width in place of absolute norm

Date: 2026-10-15. Status: internally reconstructed transfer of the now-coordinated endpoint proof. External correctness and historical priority remain UNKNOWN. This strengthens the subcritical result in `SPECTRAL_WIDTH_TRANSFER.md`; it does not rewrite that earlier proof or claim its prior estimate attained an endpoint.

The source is the coordinated `radial_endpoint_astra/ENDPOINT_PROOF_v1.md`, acquired at SHA-256 `27cc78159b041c0f679dc2372c6eed21e2d1a8ada226ecf5b5e5c6c600c5ad78`, with its moment addendum SHA-256 `16ce40f6c5ac8227850aed26247c18da94ad4a4228f04a1f4eb72951a9eb1a4d`. The parent explicitly coordinated its reading. I read the entire endpoint proof and the addendum. The only changes needed for the transfer are proved below.

Let

\[
\Delta(A)=\sup_{|u|=1}(\sup\sigma A(u)-\inf\sigma A(u))\le D,
\qquad D>0.
\]

For \(0\le\beta\le1\), put

\[
Q(s)=\sqrt{e^2+s^2},\qquad
f_\beta(s)=Q(s)(\log Q(s)+\beta\log\log Q(s))-e,
\]
\[
p_{L,\beta}(x)=Z^{-1}\exp[-(L/D)f_\beta(|x|/L)].
\]

Then the same density regularizes every such bounded self-adjoint tuple, in every Hilbert-space dimension and with arbitrary scalar offsets, whenever

\[
L\ge {400e^3\over\varepsilon}\,m^2(m+1)2^m D.
\tag{1}
\]

The centered relative-error conclusion is the endpoint source's conclusion with effective radius \(D/2\). Its tail is

\[
-\log p_{L,\beta}(x)
={r\over D}(\log r+\beta\log\log r-\log L+o(1)).
\tag{2}
\]

For \(m\ge2\), the leading coefficient \(1/D\) is attained and the largest permitted iterated-log coefficient under the source's pointwise envelope contract is \(\beta=1\). The Pauli pair with amplitude \(D/2\) supplies the same obstruction, including the necessary fixed-offset inequality \(b\le\log(4/D)-1\). The optimal fixed offset is not determined.

## The two changes in the proof

First choose \(a_j=(\sup\sigma A_j+\inf\sigma A_j)/2\) and \(B_j=A_j-a_jI\). Then \(\|B_j\|\le D/2\), and the known numerical-range support argument gives

\[
\operatorname{supp}W_B\subseteq K_B\subseteq[-D/2,D/2]^m.
\tag{3}
\]

Although \(\|B(g)\|\) can exceed \(D|g|/2\), its spectral diameter is at most \(D|g|\). For a self-adjoint \(H\), let \(b\) be the midpoint of its spectral extremes. Scalar translation cancels exactly in every sandwiched exponential derivative:

\[
e^{-H/2}D^k\exp(H)[K_1,\ldots,K_k]e^{-H/2}
=e^{-(H-bI)/2}D^k\exp(H-bI)[K_1,\ldots,K_k]e^{-(H-bI)/2}.
\tag{4}
\]

No derivative of \(b\) is taken: (4) applies to the derivative at a fixed base operator. Lemma 2.1 of the source therefore applies with \(q=\|H-bI\|=\operatorname{diam}\sigma H/2\). At \(H=B(g)\), its coordinate-insertion estimate becomes

\[
\left\|e^{-B(g)/2}\partial_g^\alpha e^{B(g)}e^{-B(g)/2}\right\|
\le2k(k-1)(D/2)^k
{e^{D|g|}\over(1+D|g|/2)^2},\qquad k=|\alpha|\ge2.
\tag{5}
\]

Second, source Lemma 3.1 uses a ball cutoff merely to justify applying the convergent multivariate Taylor series to the compact distribution. Replace it by a smooth cutoff supported in the box \(\{|y_j|<a\}\), equal to one near \(K_B\), with \(D/2<a<\rho\). Taylor convergence in the larger complex polydisc implies uniform convergence of each finite derivative order on this box. The same finite-order-continuity argument therefore works. All coefficient counts and Cauchy bounds are unchanged.

Now set \(\rho=D\) and substitute \(R_{\mathrm{eff}}=D/2\) in source Sections 3-4. Equations (3) and (5) supply precisely the support and moment estimates those sections use. The analytic-potential estimates, \(R_{\mathrm{eff}}/\rho=1/2\), and the two surviving Duhamel denominators give (1) without a \(\sqrt m\) loss.

Normalization also survives. The source's upper norm majorant is replaced, if necessary, by
\(p(x)\exp(\sqrt mD|\nabla V(x)|/2)\), still integrable because the gradient grows logarithmically and the potential is superlinear. Finally \(M_A(x)=M_B(x-a)\), so scalar offsets translate the output and do not change the noise.

This is a geometric strengthening of the endpoint theorem and an exact removal of irrelevant scalar offsets. It does not improve the exponential dependence of the sufficient scale on the number of observables, compile a POVM, or provide a statistical advantage.
