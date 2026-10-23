# Audit of the live Hilbert–Schmidt multiplier, Eqs. (3)–(6)

## Verdict

The estimates (3)–(6) are algebraically valid in the stated fixed finite
live space. They require exactly the declared charge structure: after
excluding \(a,e\), every live sector has \(Z\)-charge \(0\) or \(-1\);
\(P_eH_cP_a=0\); \(H_c\) is Hermitian with operator norm at most \(B\);
and the only dissipators during the live evolution are the Hermitian
dephaser \(\kappa\mathcal D[Z]\) and terminal \(e\)-loss. The constant in
(5) follows with the displayed factors. The bound is independent of
controller dimension and run duration.

## Block equations

For \(U=X_{aa}\), \(Y=X_{ea}\), and blocks
\(A=(H_c)_{aa}\), \(E=(H_c)_{ee}\), \(C=(H_c)_{eQ}\),
\(F=(H_c)_{aQ}\), the Hamiltonian \(e,a\) block is exactly \(gI\);
there is no \(H_c\) contribution to it. Direct block multiplication gives
\[
 \dot Y=-igU+igX_{ee}-iEY+iYA-iCX_{Qa}
          +iX_{eQ}F^\dagger-\lambda Y,\qquad
 \lambda=(\kappa+\gamma)/2,
\]
and
\[
 \dot U=-i[A,U]-ig(Y-Y^\dagger)-iFX_{Qa}+iX_{aQ}F^\dagger.
\]
The dephasing coefficient on \(Y=X_{ea}\) is \(-\kappa/2\), because the
\(e,a\) charge difference is one; terminal loss contributes
\(-\gamma/2\). The \(aa\) block has no direct dephasing or loss.

Positivity and \(\operatorname{Tr}X\le1\) imply \(0\le X\le I\),
\(\|X\|_2\le1\), \(\|Y\|_2\le e:=\|P_eX\|_2\), and
\(\|X_{ee}\|_2,\|X_{eQ}\|_2\le e\). The charge differences from \(a\)
to every sector in \(Q\), and from \(a\) to \(e\), have magnitude at
least one, so \(\|X_{Qa}\|_2,\|X_{aQ}\|_2,\|X_{ae}\|_2\le
z:=\|[Z,X]\|_2\). Compression does not increase the operator norm of
\(H_c\), hence \(\|A\|,\|E\|,\|C\|,\|F\|\le B\). These facts give
\[
 \|R_Y\|_2\le(u+3B+\lambda)e+Bz,\qquad
 \|R_U\|_2\le2ue+2Bz,
\]
as in (3).

## Multiplier derivative and constants

For \(m=2\operatorname{Im}\operatorname{Tr}(Y^\dagger U)\), the leading
terms from \((-igU)^\dagger U\) give \(2g\|U\|_2^2\). The aa-commutator
term is bounded by
\(2\|Y\|_2\|[A,U]\|_2\le4Be\|U\|_2\). The \(R_Y\) and \(R_U\) terms
contribute, respectively,
\[
 2(u+3B+\lambda)e\|U\|_2+2Bz\|U\|_2
 \quad\text{and}\quad
 4ue^2+4Bez.
\]
Combining the \(e\|U\|\) terms yields coefficient
\(2(u+5B+\lambda)=2K_1\), proving (4).

The opening states \(|m|\le1\) without showing the sharper block estimate
needed for that constant. It is valid: block orthogonality gives
\(\|X\|_2^2\ge\|U\|_2^2+2\|Y\|_2^2\), so
\[
 |m|\le2\|Y\|_2\|U\|_2
 \le\|U\|_2^2+\|Y\|_2^2
 \le\|X\|_2^2\le1.
\]
Thus \(|m(T)-m(0)|\le2\), as used in (5).

The exact energy identity (2) gives
\(\int e^2\le1/(2\gamma)\) and \(\int z^2\le1/\kappa\).
For \(J=\int\|U\|_2^2\), integrating (4), using \(g\ge\ell\), gives
\[
 J\le\frac1\ell+\frac{A_0}{\ell}\sqrt J
        +\frac{u}{\gamma\ell}
        +\frac{2B}{\ell\sqrt{2\gamma\kappa}},
 \qquad
 A_0=\frac{K_1}{\sqrt{2\gamma}}+\frac{B}{\sqrt\kappa}.
\]
Young's inequality in the form
\((A_0/\ell)\sqrt J\le J/2+A_0^2/(2\ell^2)\) yields the displayed
bracket in (5). Finally the three off-aa blocks in the \(a\)-row,
\(X_{ae},X_{aQ}\), are disjoint entries of \([Z,X]\) with charge
difference at least one. Hence
\(\|P_aX\|_2^2\le\|U\|_2^2+\|[Z,X]\|_2^2\). Integrating proves (6)
with \(C_a=J_{\max}+1/\kappa\), exactly as stated.

## Scope

This audit verifies the multiplier step only. It depends on the fixed
coherent-controller dimension and the original unital dephaser/terminal-loss
energy identity; additional nonunital reset baths or extra charge sectors
would require a new estimate.

