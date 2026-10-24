# Named-port weak-plane gate: exact audit

Scope: the frame/control construction in Sections 1–2 of
NAMED_PORT_WEAK_PLANE_OPERATION.txt. I did not audit its population,
death, or completed-channel estimates.

Let \(F=[C,D]\) be the broad mathematical frame, with frame rows
\[
F_c=(n^{-1},-z/(n\sigma))I,\qquad
F_a=(A/n,(1-z)A/(n\sigma))I,\qquad
F_e=E F_c X.
\]
The last identity is exact: the e entries of C and D are respectively
\(E/n\,X\) and \(-zE/(n\sigma)X\). All row coefficients are real.
The broad normal correction is \(i jQJQ\), where
\(J=(|a\rangle\langle e|-|e\rangle\langle a|)\otimes X\).
Writing \(Q_{aa}=q_aI,Q_{ee}=q_eI,Q_{ae}=qX\) gives
\((QJQ)_{ae}=(q_aq_e-q^2)X=:\chi X\).
Thus \(j=-r_{ae}/\chi\) cancels the whole broad a-e block exactly;
\(\chi=1-O(\beta^2)\) is uniformly bounded away from zero.

The c-e block of the frame generator can be evaluated without a
remainder estimate. From \(F_e=EF_cX\), the first two terms in
\[
H_0=iF'F^\dagger-iFF'^\dagger-iF(F^\dagger F')F^\dagger
\]
give \(-iE'\|F_c\|^2X\), and the last term vanishes because
\(F_c(F^\dagger F')F_c^\dagger=0\) for the real vector \(F_c\) and
skew-adjoint \(F^\dagger F'\). Since \(P_{cc}=\|F_c\|^2I\),
\[
(H_0)_{ce}=-iE'P_{cc}X.
\]
The normal correction contributes exactly
\((QJQ)_{ce}=-P_{ca}X\). To see the cancellation of its E-dependent
terms, use \(Q_{ca}=-P_{ca}\), \(Q_{ee}=I-E^2P_{cc}\),
\(Q_{ce}=-EP_{cc}X\), and \(Q_{ae}=-EP_{ac}X\), with
\(P_{ac}=P_{ca}\) real. Then
\(Q_{ca}XQ_{ee}-Q_{ce}XQ_{ae}=-P_{ca}X\).
Consequently the accepted broad Hamiltonian has
\[
\bar H_{ce}=i r_{ce}X,\qquad r_{ce}=-E'P_{cc}-jP_{ca}.
\]

Here is the endpoint factorization, including the contribution from
the a-e normal cancellation. Put \(\theta=a_0/\beta=h^4\) and
\(\sigma=\beta f\,s_h(f)\), where \(s_h\) is smooth, positive, and
\(1+O(\beta^2)\). The row coefficients have the forms
\[
F_c=(u_c(f),\,\beta f\,v_c(f)),\qquad
F_a=(a_0f^2u_a(f),\,\theta f\,v_a(f)),
\]
with all displayed scalar functions and their needed derivatives
uniformly bounded and smooth. The frame connection entry \(k\) in
\(F^\dagger F'=\begin{psmallmatrix}0&k\\-k&0\end{psmallmatrix}\otimes I\)
is \(k=\beta f'\,k_h(f)\) with \(k_h\) uniformly smooth and bounded.
The exact formula
\[
(H_0)_{ac}=i r_{ac},\quad
r_{ac}=F_a'F_c^\dagger-F_aF_c'^\dagger-F_a(F^\dagger F')F_c^\dagger
\]
therefore has \(r_{ac}=a_0 f f' R_h(f)\), with \(R_h\) uniformly smooth
and bounded: each term contains \(f f'\), using the row forms above.
Likewise \(P_{ac}=a_0 f^2 S_h(f)\). The exact row relation gives
\[
(H_0)_{ae}=(E H_0{}_{ac}-iE'P_{ac})X
=i(E r_{ac}-E'P_{ac})X,
\]
so \(r_{ae}=a_0e_0 f^3 f'\,\widetilde R_h(f)\). Since
\(\chi^{-1}\) is uniformly smooth and bounded, the normal-correction
coefficient \(j=-r_{ae}/\chi\) has the same factor and bound. Finally
\(P_{ca}=a_0f^2 S_h(f)\) and \(P_{cc}\) is smooth and bounded, so
\[
r_{ce}=e_0 f f'\,\widehat R_h(f)
\]
for a uniformly smooth bounded \(\widehat R_h\). In particular the
factorization is for the broad Hamiltonian *after* its normal a-e
cancellation, not just for \(H_0\).

For \(B=\beta f\), the quotient extends smoothly:
\[
v=-\frac{r_{ce}}{B\delta}
=-\frac{e_0}{\beta\delta}f'\widehat R_h(f).
\]
The specified bump is flat at both endpoints, so \(v\) and its endpoint
limits are smooth and flat. Differentiating the exact expression gives
\[
|v|=O\!\left(\frac{e_0}{\beta\delta}\right),\qquad
|\dot v|=O\!\left(\frac{e_0}{\beta\delta^2}\right)
\quad(s=t/\delta).
\]
The triangle has norm bounded by \(C|v|\); its s-derivative has the
same \(O(e_0/(\beta\delta))\) bound because \(B,E\) and their s
derivatives are bounded. Thus
\(\|N\|=O(e_0/(\beta\delta))=O(h^3)\) and
\(\|\dot N\|=O(e_0/(\beta\delta^2))=O(h)\).
Together with the broad \(\bar H\) bounds this keeps total control norm
\(O(h^2)\) and slew \(O(1)\).

The total named-port audit is exact:
\[
(H_{\rm named})_{ce}=i(r_{ce}/\delta+vB)X=0,\qquad
(H_{\rm named})_{ae}=0.
\]
There is no dead coupling. The remaining added triangle edges are
c-b and b-e; the permitted a,b,c control graph is complete, so any
a-b entry of \(\bar H\) is allowed. The algebraic annihilation identities
also check directly:
\[
NC=0,\qquad ND=-\frac{i vB}{n\sigma}(eX-Ec),\qquad
C^\dagger ND=D^\dagger ND=0.
\]
Hence \(F^\dagger NF=0\), but \(ND\ne0\) generally: the correction
preserves the code column and does not transport the whole first-error
plane. No obstruction was found in this bounded exact gate. Later
channel/reset estimates remain outside scope.
