# Independent challenge: universal finite-bath compression and capacity floor

Reviewer: `/root/stopping_converse`  
Date: 21 October 2026  
Verdict: **qualified internal mathematical acceptance** of the expurgation, common-normalization, Knill--Laflamme lift, and dimension argument described below. The depth-walk overflow estimate is a separate premise assigned to the root; this review does not certify or repeat that stochastic argument.

The essential implementation qualification is that the inverse-square-root input normalization is an **auxiliary mathematical operation**, not a physical postselected filter. The actual encoder remains an isometry into the expurgated input space. Its distance from the auxiliary normalized projected map is explicitly included in the error.

## 1. Precise inputs to this review

Fix the physical unitary \(V_s\), used repeatedly on the same bath, with \(s\) fixed throughout a coding sequence. Let \(W_n\) be its ordered \(n\)-slot unitary. For even \(n\), use the external input type subspace \(\mathcal T_n\) containing exactly \(n/2\) zero symbols. Its dimension is

\[
D_n=\binom n{n/2}2^{n/2}.
\]

Let \(P_a\) project onto the two-seed Fock vertices of depth at most \(a\), and let \(P_H\) be the corresponding final cutoff. Their ranks are

\[
r=2(2^{a+1}-1),\qquad h=2(2^{H+1}-1).
\]

The premise supplied by the root is that the auxiliary initial bath \(P_a/r\), under the maximally mixed type input, has final overflow probability at most \(\delta\). It follows from the asserted critical-product overflow estimate and the operator domination of the uniform type state by the product state divided by

\[
p_n=\binom n{n/2}/2^n.
\]

No critical-product assumption beyond this average overflow bound is used in the remainder of the proof. In particular, the type distribution and the auxiliary cutoff bath are analytic devices; the physical bath need not be prepared in either a cutoff state or a new horizon-dependent state.

## 2. Expurgation and auxiliary normalization

Define the projected success CP map from the type subspace to all \(n\) external outputs by using the auxiliary bath and keeping only the final bath cutoff. In vertex bases it has Kraus operators

\[
A_{wv}=\frac1{\sqrt r}\langle w|W_n|v\rangle\big|_{\mathcal T_n},
\qquad v\in P_aE,\quad w\in P_HE.
\]

Its number of Kraus operators is at most \(rh\). Let its input failure effect be

\[
L=I_{\mathcal T_n}-\sum_{v,w}A_{wv}^\dagger A_{wv}.
\]

Then \(0\le L\le I\), and the stated overflow premise gives

\[
\operatorname{Tr}L/D_n\le\delta.
\]

Let \(Q\) be the spectral projection of \(L\) onto eigenvalues at most \(2\delta\). Markov's eigenvalue bound gives

\[
\dim Q\ge D_n/2,\qquad 0\le QLQ\le2\delta I_Q.
\]

For \(2\delta<1\), define on \(Q\mathcal T_n\)

\[
R=(I_Q-QLQ)^{-1/2}.
\]

The operators

\[
\widetilde A_{wv}=A_{wv}QR
\]

define a trace-preserving channel with input space \(Q\mathcal T_n\), output space \((\mathbb C^3)^{\otimes n}\), and at most \(k=rh\) Kraus operators. Indeed,

\[
\sum_{v,w}\widetilde A_{wv}^\dagger\widetilde A_{wv}
=R(I_Q-QLQ)R=I_Q.
\]

The normalizer satisfies the exact bound

\[
\eta_R:=\|R-I_Q\|
\le(1-2\delta)^{-1/2}-1.
\]

For \(\delta\le1/4\), one may use the convenient bound \(\eta_R\le2\delta\). This follows from \((1-x)^{-1/2}\le1+x\) on \(0\le x\le1/2\), with \(x=2\delta\).

Neither \(R\) nor the final bath projection is performed on the actual transmission. They only define an auxiliary finite-Kraus channel whose exact code will be used with the unfiltered physical input encoder.

## 3. Unequal input and output dimensions are allowed

The inherited low-Kraus-rank coding argument extends without change to a channel \(\mathcal A:\mathcal B(\mathbb C^{d_{\rm in}})\to\mathcal B(\mathbb C^{d_{\rm out}})\). Its greedy/Tverberg construction concerns only the input-space operator system

\[
\operatorname{span}\{A_i^\dagger A_j\}\subseteq\mathcal B(\mathbb C^{d_{\rm in}}),
\]

which has real Hermitian dimension at most \(k^2\) and contains identity by trace preservation. The input dimension is therefore the \(D\) used in the original proof. The final Knill--Laflamme recovery is defined on the actual output space; equality of input and output dimensions is not needed.

Applied here, it yields an isometric outer encoder

\[
C:\mathbb C^K\longrightarrow Q\mathcal T_n,
\qquad
K\ge\left\lceil\frac{\dim Q}{k^4}\right\rceil
\ge\frac{D_n}{2(rh)^4}.
\]

The actual physical encoder is **\(C\)**. It is not the generally nonisometric map \(RC\).

The resulting code satisfies Knill--Laflamme simultaneously for all \(\widetilde A_{wv}\). If desired, take an exact recovery isometry \(D\), retaining all of its syndrome systems. Its extension from the correctable subspace to the full output space can always be made isometric by enlarging the finite syndrome space.

## 4. Why one auxiliary code works coherently for every initial cutoff bath

Because the KL conditions hold for the entire error family indexed by **both** initial and final bath coordinates, the recovery can be chosen so that

\[
D\widetilde A_{wv}C|\psi\rangle
=|\psi\rangle\otimes|s_{wv}\rangle.
\]

The syndrome vectors have the KL Gram matrix; they need not be orthogonal. Multiplying by \(\sqrt r\), reinserting the final bath vectors, and superposing the initial bath coordinates gives an exact operator identity

\[
(D\otimes I_E)(I\otimes P_H)
W_n(RC\otimes I_{P_aE})
=I_{\rm logical}\otimes Z,
\]

where

\[
Z|v\rangle=\sqrt r\sum_w|s_{wv}\rangle\otimes|w\rangle.
\]

This is a coherent identity on \(\mathbb C^K\otimes P_aE\), not merely a statement for the maximally mixed auxiliary bath. It therefore covers coherent superpositions of initial vertices and correlations with any inert bath purifier. No factor of \(r\) is lost in passing from a mixed initializer to this coherent identity; the \(\sqrt r\) is retained explicitly in \(Z\), whose normalization is not assumed.

An exact code for only the separate diagonal-initializer channels, with unrelated recoveries or unrelated KL matrices, would not justify this step. The auxiliary mixture's single Kraus family and its cross-index KL conditions are precisely what provide the needed common recovery.

## 5. Uniform joint failure bound

On \(Q\mathcal T_n\otimes P_aE\), let

\[
F=(Q\otimes P_a)W_n^\dagger(I\otimes(I-P_H))W_n(Q\otimes P_a).
\]

This is the positive failure effect for the true, unnormalized physical block. Taking the partial trace over the initial bath gives exactly

\[
\operatorname{Tr}_E F=rQLQ.
\]

For every positive operator \(F\) on a tensor product whose second factor has dimension \(r\),

\[
F\le r\,(\operatorname{Tr}_E F)\otimes I_E.
\]

A direct proof writes a vector as \(\xi=\sum_i\xi_i\otimes|i\rangle\). Positivity of the block matrix gives
\(|\langle\xi_i,F_{ij}\xi_j\rangle|\le\sqrt{\langle\xi_i,F_{ii}\xi_i\rangle\langle\xi_j,F_{jj}\xi_j\rangle}\).
Summing and applying Cauchy--Schwarz bounds the quadratic form by \(r\sum_i\langle\xi_i,F_{ii}\xi_i\rangle\), which is at most the quadratic form of \(r(\operatorname{Tr}_E F)\otimes I_E\).

Consequently,

\[
\|F\|\le r\|\operatorname{Tr}_EF\|
\le2r^2\delta.
\]

Thus, uniformly over every input in \(Q\) and every possibly coherent cutoff bath,

\[
\|(I\otimes(I-P_H))W_n(C\otimes I_{P_aE})\|
\le r\sqrt{2\delta}.
\]

The \(r^2\) in the probability bound and \(r\) in the amplitude bound are legitimate. Replacing them by a smaller factor without another argument would not follow from expurgation of the auxiliary average alone. Their actual growth is harmless for the proposed cutoffs.

## 6. Physical recovery, polar normalization, and complete error

The true recovered joint map

\[
H=(D\otimes I_E)W_n(C\otimes I_{P_aE})
\]

is an isometry. Compare it with the exact normalized projected factorization. Projection failure contributes at most \(r\sqrt{2\delta}\); replacing \(RC\) by \(C\) contributes at most \(\eta_R\), since \(D\), the projection, and \(W_n\) are contractions. Therefore

\[
\|H-I\otimes Z\|\le\varepsilon_n,
\qquad
\varepsilon_n=r\sqrt{2\delta}+(1-2\delta)^{-1/2}-1.
\]

For \(\varepsilon_n<1\), the same isometry/polar argument as in the earlier lower-stability review gives an isometry \(Z_0\) on \(P_aE\) with

\[
\|Z-Z_0\|\le\varepsilon_n,
\qquad
\|H-I\otimes Z_0\|\le2\varepsilon_n.
\]

After tracing all nonlogical outputs, the physical decoded channel for every initial bath supported on \(P_aE\) has **full** diamond error

\[
\boxed{\|\Lambda_{n,\sigma}-\mathrm{id}_K\|_\diamond
\le4\varepsilon_n.}
\]

This is a uniform statement on the entire initial cutoff subspace, including coherent bath states. It does not require physical access to the bath or a projection outcome. No transmission branch is discarded or credited conditionally.

## 7. Cutoff growth and the asymptotic rate

Take the proposed sequences

\[
a_n=\lfloor n^{1/4}\rfloor,\qquad
H_n=a_n+\lceil n^{3/4}\rceil,
\qquad
\delta_n\le\frac{4e^{-\sqrt n/8}}{p_n}.
\]

The elementary central-binomial bound gives \(p_n\ge1/(n+1)\). Consequently

\[
\delta_n\le4(n+1)e^{-\sqrt n/8},
\qquad
r_n\sqrt{2\delta_n}
\le2^{a_n+2}\sqrt{8(n+1)}e^{-\sqrt n/16}\longrightarrow0.
\]

Also \(\eta_R=O(\delta_n)\), so \(\varepsilon_n\to0\). This explicitly checks that the universal coherent-bath lift's factors of \(r_n\) do not defeat the given overflow estimate.

For the dimensions,

\[
D_n\ge\frac{2^{3n/2}}{n+1},\qquad
\log_2 k_n\le a_n+H_n+4=o(n).
\]

Hence

\[
\log_2K_n
\ge\frac32n-\log_2(n+1)-1-4(a_n+H_n+4),
\]

and \(\liminf\log_2K_n/n\ge3/2\). The coding argument has unequal input/output dimensions, but the correct input dimension \(\dim Q\ge D_n/2\) is used throughout; the full \(3^n\) output dimension is not mistakenly substituted for the type-space input dimension.

## 8. One sequence for every fixed normal bath initializer

The encoder \(C_n\) and decoder \(D_n\) depend on the fixed device, the deterministic cutoff sequence, and the auxiliary average channel. They do **not** depend on the actual bath initializer \(\tau\).

For any fixed normal density \(\tau\), let

\[
q_n=\operatorname{Tr}(P_{a_n}\tau),\qquad
\tau_n=P_{a_n}\tau P_{a_n}/q_n.
\]

Normality and increasing finite vertex cutoffs give \(q_n\to1\). Projecting and normalizing a purification yields

\[
\tfrac12\|\tau-\tau_n\|_1\le\sqrt{1-q_n}.
\]

For the same physical code and decoder, initial-bath trace distance bounds the full diamond distance between the resulting logical channels by \(\|\tau-\tau_n\|_1\): tensor an arbitrary logical reference and use contractivity of the complete physical operation. Therefore

\[
\boxed{
\|\Lambda_{n,\tau}-\mathrm{id}_{K_n}\|_\diamond
\le4\varepsilon_n+2\sqrt{1-q_n}\longrightarrow0.
}
\]

The factor two is explicit because this is a full diamond norm and the cutoff approximation was stated in half trace distance. The same single sequence of codes succeeds for every **fixed** normal initializer. The claim is pointwise in \(\tau\); it is not a convergence bound uniform over all normal densities at each \(n\), and it does not cover a physical initializer adversarially changed with the horizon.

## 9. Conclusion and boundaries

Conditional on the root's stated critical-product overflow estimate, this completes a valid unassisted capacity floor of \(3/2\) qubits per counted forward use for each fixed \(V_s\), with one code sequence for all fixed normal initializers. It is stronger than the earlier small-perturbation lower-continuity argument and does not require bath resets.

The bath cutoff, projected channel, auxiliary maximally mixed initializer, and inverse-square-root normalizer are proof constructions, not physical operations. The actual operation is the isometric encoder \(C_n\), the unchanged closed device for all \(n\) calls, and one receiver decoder \(D_n\), with all outputs retained in the dilation. The theorem claims approximate logical recovery, not terminal or all-use bath return. It is an existence proof using inherited exact coding machinery, not an efficient circuit compiler or a practical finite-size device proposal.

No additional code replay was needed to check this operator argument. The independent activity here was the proof of the common-recovery lift, the positive-block inequality, the normalization/error accounting, and the unequal-dimension coding check. The random-walk premise and historical priority remain separate obligations.
