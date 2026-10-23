# Joint-rail companion audit

## Assumptions and local error bound

Index each cell by (i\in\mathbb Z), with cell algebra (A_i\otimes B_i). The input is the product state
\[
\tau=\bigotimes_i(\tau_{A_i}\otimes\tau_{B_i}),\qquad
\tau_{A_i}\succeq a_* I,\quad \tau_{B_i}\succeq b_* I,
\]
and write (p=a_*b_*>0). Thus on any union \(\Gamma\) of (m\) cells,
\[
\tau_\Gamma\succeq p^m I_\Gamma.
\]
The evolution \(\Omega\) is a trace-preserving *-automorphism with strict cell radius \(R\); in particular it sends each onsite projector to a projector. No factorization of \(\Omega\), its output, or its action between the A and B rails is assumed. The input product structure is used only for the stated eigenvalue floor (and the optional conditional refinement below).

Let \(P_A\) and \(P_B\) be the rank-one onsite label projectors. Define the reference projectors
\[
P_A^{\rm ref}=P_{A,i-1},\qquad P_B^{\rm ref}=P_{B,i},
\]
and \(Q_A=\Omega(P_{A_i})\), \(Q_B=\Omega(P_{B_i})\). The **joint**, unnormalized copy-mismatch terms are
\[
e_A^{\rm joint}=\operatorname{Tr}\tau\,P_A^{\rm ref}(I-Q_A)P_A^{\rm ref},\qquad
e_B^{\rm joint}=\operatorname{Tr}\tau\,P_B^{\rm ref}(I-Q_B)P_B^{\rm ref}.
\]
These expressions retain any correlations created by the full joint \(\Omega\).
Each trace involving \(\tau\) is shorthand for the trace against its reduced density matrix on the displayed finite support union.

For A, \(Q_A\) is supported on cells \([i-R,i+R]\); adjoining the reference cell \(i-1\) gives
\[
\Gamma_A(i)=[i-\max(R,1),i+R],\qquad
m_A=R+\max(R,1)+1.
\]
For B, the reference is already at \(i\), so
\[
\Gamma_B(i)=[i-R,i+R],\qquad m_B=2R+1.
\]
The separate \(\max(R,1)\) in the A expression handles the edge case \(R=0\): A's comparison still spans cells \(i-1,i\), while B's spans only cell \(i\).

On either union write \(P=P_X^{\rm ref}\), \(Q=Q_X\), and \(m=m_X\). Since \(P,Q\) are projections and \(\tau_\Gamma\succeq p^m I\),
\[
e_X^{\rm joint}\ge p^m\operatorname{Tr}\bigl(P(I-Q)P\bigr).
\]
The reference and transported projectors have equal rank on the union: the local normalized trace is preserved by \(\Omega\), and both projectors have trace \(1/d_A\) (respectively \(1/d_B\)). In the finite matrix algebra of the union, equal normalized trace means equal rank. For equal-rank projections,
\[
\|Q-P\|_{\rm op}^2=\|P(I-Q)P\|_{\rm op}
\le \operatorname{Tr}\bigl(P(I-Q)P\bigr).
\]
Thus the main operator-norm conclusion is valid with no \(\sqrt 2\) loss:
\[
\|Q_A-P_A^{\rm ref}\|_{\rm op}
\le\sqrt{\frac{e_A^{\rm joint}}{p^{m_A}}},\qquad
\|Q_B-P_B^{\rm ref}\|_{\rm op}
\le\sqrt{\frac{e_B^{\rm joint}}{p^{m_B}}}.
\]
The one-sided operator leakage has the same norm for equal-rank projections. Separately, the one-sided Hilbert-Schmidt leakage also satisfies
\[
\left\|(I-Q_A)P_A^{\rm ref}\right\|_2
\le\sqrt{\frac{e_A^{\rm joint}}{p^{m_A}}},\qquad
\left\|(I-Q_B)P_B^{\rm ref}\right\|_2
\le\sqrt{\frac{e_B^{\rm joint}}{p^{m_B}}}.
\]

For completeness, the full Hilbert-Schmidt difference obeys
\[
\|Q_X-P_X^{\rm ref}\|_2^2
=2\left\|(I-Q_X)P_X^{\rm ref}\right\|_2^2,
\]
and therefore has the separate bound
\[
\|Q_A-P_A^{\rm ref}\|_2\le\sqrt{2e_A^{\rm joint}/p^{m_A}},\quad
\|Q_B-P_B^{\rm ref}\|_2\le\sqrt{2e_B^{\rm joint}/p^{m_B}}.
\]
This Hilbert-Schmidt factor does not weaken the main operator-norm result.

## Conditional errors

Let \(q_A=\operatorname{Tr}(\tau_{A_{i-1}}P_A)\) and \(q_B=\operatorname{Tr}(\tau_{B_i}P_B)\). If a reported error is conditioned on the copied input label, set \(\epsilon_X=e_X^{\rm joint}/q_X\); then the unconditional theorem gives \(\|Q_X-P_X^{\rm ref}\|_{\rm op}^2\le q_X\epsilon_X/p^{m_X}\) and \(\|(I-Q_X)P_X^{\rm ref}\|_2^2\le q_X\epsilon_X/p^{m_X}\). Under the product-input assumption above, compression to the reference-label subspace gives the sharper floors
\[
P_A^{\rm ref}\tau_{\Gamma_A}P_A^{\rm ref}\succeq q_A b_*p^{m_A-1}P_A^{\rm ref},\qquad
P_B^{\rm ref}\tau_{\Gamma_B}P_B^{\rm ref}\succeq q_B a_*p^{m_B-1}P_B^{\rm ref}.
\]
Thus the conditional form can be sharpened to
\[
\|Q_A-P_A^{\rm ref}\|_{\rm op}^2,\ \|(I-Q_A)P_A^{\rm ref}\|_2^2
\le\frac{\epsilon_A}{b_*p^{m_A-1}},\qquad
\|Q_B-P_B^{\rm ref}\|_{\rm op}^2,\ \|(I-Q_B)P_B^{\rm ref}\|_2^2
\le\frac{\epsilon_B}{a_*p^{m_B-1}}.
\]
The basic theorem uses the joint, unnormalized \(e_X^{\rm joint}\) and requires no conditional normalization.

## Radius and preparation windows

The reference map has radius one, so \(\alpha=\sigma^{-1}\Omega\) has radius at most
\[
r=R+1.
\]
The frozen core is \(T=[-r,5r-1]\), of length \(6r\). For every \(i\in T\), the A comparison needs \([i-\max(R,1),i+R]\); the B comparison needs \([i-R,i+R]\), which is contained in that A-expanded window. Taking the union over the core sites gives exactly
\[
U=[-r-\max(R,1),\,5r-1+R],\qquad |U|=6r+R+\max(R,1).
\]
For \(R=0\), this is \([-2,4]\), seven cells; for \(R\ge1\), it is \([-2R-1,6R+4]\), or \(8R+6\) cells.

The density floor is applied to the physical input \(\tau_U\) once, on the actual support union of each mismatch observable. Rewriting the comparison with \(\alpha\) by applying \(\sigma^{-1}\) to observables does not insert another input state or another factor of \(p\). The uniform local floors are preserved under the reference shift. In particular, no additional “\(\alpha\)-input density floor” or fictitious extra support enlargement belongs in these estimates.

## Scope

The local projector argument requires \(\Omega\) to map projections to projections and preserve the local trace, as a QCA automorphism does. A general non-unitary channel need not preserve projection rank, so the equal-rank identity for the two-sided Hilbert-Schmidt difference would require a separate hypothesis or replacement bound. The joint mismatch formulas themselves make no rail-factorization assumption.
