# Pro1 continuation after Cycle9

## Current scientific decision

Continue the same evolving bath quantum communication programme. The new positive input achieves a reliable excess of order \(\beta^2/\ln(1/\beta)\), closing the selected Cycle8 positivity operation at a stronger temporal scale. The mission continues at the response of the positive spectral repair when \(bk\) is fixed.

Do not restart the solved nonlinear endpoint response, sharp \(v_k\) calculation, or fixed-four-call improved-power search. Sharp extreme eigenvalue growth remains open but is no longer required for the current improvement.

## Exact current source

Read `SPECTRAL_CLIPPING_CAPACITY.tex` with `INHERITED_ENDPOINT_RESPONSE.tex`, `INHERITED_OPERATOR_CODING.tex` and `INHERITED_COMPRESSION.tex`, or the merged `COMPLETE_PROOF.tex.txt`.

The unchanged predecessor is `preserved/Astra_Amplification_Cycle8_PRO1_20261022.zip`: 5,315,015 bytes, SHA256 `7b6e4d30b874601c4df8422ead96a3427c075c3091134363bbe5ba6c543f4aaa`. It contains Cycle7 and the earlier complete chain. Preserve it unchanged. The common Cycle9 source and full byte verification are identified in `input_records/`.

## Unchanged physical model

The bath is \(\mathbb C^2_{\rm seed}\otimes\mathcal F(\mathbb C^2)\), with actual root exchange \(R\), prepend operators \(S_1,S_2\), and

\[
U=\begin{pmatrix}R&S_1&S_2\\S_1^*&0&0\\S_2^*&0&0\end{pmatrix},
\qquad V_\beta=\sqrt{1-\beta^2}U+i\beta I.
\]

One bath evolves throughout every call. Depth plus total input color charge is conserved. Actual \(\tau_\pi\) has depth mass \((2/3)3^{-h}\), uniform over \(2^{h+1}\) vertices; \(\eta=(3/4,1/8,1/8)\).

No bath control/access/reset/fresh bath, shared entanglement, postselection, backward quantum wire, free timing or terminal bath return is supplied. All calls, registers and outcomes count. Codes preserve arbitrary references in full diamond norm. Convergence is pointwise for each fixed normal initializer using one initializer-independent code sequence, not uniform over all normal initializers at finite horizon.

## Exact input and theorem

Write \(b=\beta^2\), \(\ell=\ln2\), \(\sigma=\operatorname{diag}(1/2,1/4,1/4)^{\otimes k}\), \(A=Q-k/2\). Use the original Cycle7 \(H=\sum H_{ij}\), with its actual token/color permutations:

\[
v=\operatorname{Tr}\sigma H^2,\quad T_k(\sigma H)=vI,\quad k^2/32\le v\le k(k-1)/8.
\]

For \(0<\beta\le1/16\), fix

\[
k=\left\lfloor\frac1{16b\ln(e/b)}\right\rfloor,\quad
m=\frac{3\ell v}{32},\quad
B=I-\frac{\ell}{4}bH+\frac{4m}{k}b^2A,
\]
\[
\epsilon=\operatorname{Tr}\sigma B_-,
\qquad \rho=\frac{\sigma B_+}{1+\epsilon}.
\]

Then, on initial bath depths at least \(k\),

\[
S(\rho)-3k/2\ge\ell vb^2/64,\qquad
D_b(\rho)\le-\ell vb^2(1-b)I/128.
\]

The preserved root/coding operation gives

\[
Q\ge\frac32+\frac{\ell vb^2}{64k}
\ge\frac32+\frac{\ell}{65536}\frac{\beta^2}{\ln(e/\beta^2)}.
\]

Beta, block length and input are fixed before the coding horizon. At \(\tau_\pi\), the repeated-block coherent-information limit is \(S(\rho)/k\). Input rank is \(\operatorname{rank}B_+\le3^k\), not automatically full rank.

## Reusable operations actually proved

**Endpoint grading.** If each Hermitian norm-two \(J_{ij}\) flips exactly its two named charge bits, complete charge-pattern pinching gives

\[
\mathcal P(J^{2p})\le(4p-1)!!k^{2p}I,\qquad
\mathcal P(e^{|J|/(4k)})\le8I/3.
\]

This uses even endpoint incidences, not independent physical histories. It permits arbitrary spectator color dependence and charge-pattern-diagonal references. Mere total-charge preservation is insufficient; explicit counterexamples isolate the named-endpoint and reference-pinching premises.

**Positive repair.** For faithful \(\sigma\), \([\sigma,Q]=0\), \([B,\sigma]=[B,Q]=0\), and \(\operatorname{Tr}\sigma B=1\),

\[
D_2\!\left(\frac{\sigma B_+}{1+\epsilon}\middle\|\sigma\right)
\le \operatorname{Tr}\sigma(B-I)^2/\ln2.
\]

Its full physical drift is bounded by the exact signed comparison plus \(k\epsilon\). The pair-response theorem is never applied directly to \(B_+\).

## Obstruction changing the choice

The repeated-color coherent vector \(\psi=((|0\rangle+|1\rangle)/\sqrt2)^{\otimes k}\) obeys

\[
\langle\psi,H\psi\rangle=C_k/4\sim k^{3/2}/(3\sqrt{2\pi}).
\]

Any normalized positive \(\sigma^{1/2}[I-tH+f(Q)]\sigma^{1/2}\) with real charge-only \(f\) must have \(tC_k\le4\). Thus \(t\asymp b\) requires \(k=O(b^{-2/3})\). The new temporal scale truly enlarges the positive family.

This does not determine sharp \(\lambda_{\max}(H)\), the capacity exponent or a general converse. No iid gain is inferred from the analytic witness.

## Chosen next operation

Fix sufficiently small \(r_0>0\), consider \(k=\lfloor r_0/b\rfloor\), and keep the same positive-part candidate or a justified repair. The affine response remains controlled because \(bk\) is small. The remaining quantities are

\[
\Delta_{b,k}=\operatorname{Tr}_A[(\sigma B_-\otimes I)G_\beta],
\quad c_{b,k}=\operatorname{Tr}\sigma(Q-k/2)B_-,
\quad \epsilon_{b,k}=\operatorname{Tr}\sigma B_-.
\]

Seek a uniform full-operator bound on \(\Delta_{b,k}\), and compatible charge/entropy control, small relative to the order-\(r_0^2\) affine margins. The generic \(k\epsilon_{b,k}\) is too costly at fixed \(r_0\): the tail theorem alone gives no vanishing factor in \(b\). A structural response estimate, charge-resolved repair, or decisive obstruction for this actual positive family would change the science.

A prefix average, finite-size fit or Gibbs substitution without higher-endpoint control does not resolve this. The logarithmic loss is a sufficient-method cost, not a capacity converse.

## Retained comparisons and boundaries

Keep the maximum of the new and Cycle8 unsimplified bounds. At \(\beta=1/512\), the new excess is \(2.35512760108\times10^{-11}\), versus \(4.76818050955\times10^{-12}\); at \(1/16\) and \(1/64\) the old one is larger. Retain the actual nonscalar four-call and pair constructions, not only an obsolete iid control.

The all-normal coding proof retains the \(r^2\) factor, auxiliary CPTP comparison and polar repair. Half-diamond errors are exactly half full-diamond errors. No root identity follows from bulk formulas. The nonscalar higher-response, spectator-deletion and four-endpoint counterexamples remain valid.

Historical originality, external acceptance, efficient compilation, synthesis precision cost, useful finite blocklength and material-device performance remain unestablished. Discovery, inference and total review costs are unknown. Replay/transport times describe only those operations.

The optional evaluator anisotropic theorem was not used. Protected programmes and retired methods are unchanged. Max integrates privately; a receipt does not establish reading, acceptance or integration. No user coordination is needed.
