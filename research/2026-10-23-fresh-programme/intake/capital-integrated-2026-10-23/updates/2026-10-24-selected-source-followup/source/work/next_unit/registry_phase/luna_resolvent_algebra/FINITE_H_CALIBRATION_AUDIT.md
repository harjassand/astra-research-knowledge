# Finite-spacing calibration audit

For the stated edge energy
\[
E_i=\frac{S}{2h}(\Delta-hm)^2+hV(w),\qquad \Delta=w'-w,
\]
let $q=\sqrt{2SV}$, $R'=q-Sm_c$, and $r=|m|/m_c$. Since $q$ is globally Lipschitz with constant $L_q$, $R'$ is globally Lipschitz and for every real $\Delta$ (not only small hops)
\[
|R(w+\Delta)-R(w)-R'(w)\Delta|\le \frac{L_q}{2}\Delta^2.
\]
Writing this Taylor remainder as $e$, the $-Sm\Delta$ term cancels against $-(m/m_c)R'\Delta$ because $R'=q-Sm_c$. Thus
\[
E_i-\frac{hSm^2}{2}-\frac{m}{m_c}\Delta R
\ge \frac{S-hrL_q}{2h}\Delta^2+hV-\frac{m}{m_c}q\Delta.
\]
Set $S_{\rm eff}=S-hrL_q$. If $S_{\rm eff}>0$, completing the square gives
\[
\frac{S_{\rm eff}}{2h}\left(\Delta-\frac{h(m/m_c)q}{S_{\rm eff}}\right)^2
+hV\left(1-\frac{r^2S}{S_{\rm eff}}\right).
\]
Both terms are nonnegative when $S_{\rm eff}\ge r^2S$, equivalently
\[
r^2+\nu_h r\le1,\qquad \nu_h=\frac{hL_q}{S}.
\]
The allowed interval is $0\le r\le r_h$, with
\[
r_h=\frac{\sqrt{\nu_h^2+4}-\nu_h}{2}.
\]
This also guarantees $S_{\rm eff}\ge r^2S$ and strict $S_{\rm eff}>0$ (at $r=0$, $S_{\rm eff}=S$). The calibration inequality is therefore exact for every edge increment, including arbitrarily many registry periods; it is a sufficient discrete bound, not a claim of the exact discrete commensurate-incommensurate threshold.

For the cosine registry, $q=2\sqrt{SV_0}|\sin(\pi w/d)|$ is globally Lipschitz with $L_q=\beta\sqrt{SV_0}$ despite its cusps. Since $m_c=(4/\pi)\sqrt{V_0/S}$ and $\beta d=2\pi$, $\nu_h=(\pi^2/2)(h m_c/d)$. The root relation $r_h^2+\nu_h r_h=1$ then gives $h m_c r_h=(2d/\pi^2)\nu_h r_h<2d/\pi^2<d/2$. This is a useful whole-period-hop check: in the certified mismatch band, a hop $\Delta=nd$ from a registry minimum cannot beat the locked baseline; the global Taylor proof already covers it without this separate check.

For variable cell mismatch $m_i=\alpha\phi_i$, choose a smooth cutoff $0\le\chi\le1$ equal to one wherever $f(\phi)=a\phi^2/2+b\phi^4/4<0$ and supported in $|\alpha\phi|<m_c r_h$. Existence requires the strict margin $|\alpha|\sqrt{-2a/b}<m_c r_h$ when $a<0$; retain $a+S\alpha^2>0$ as in the continuum argument. Then $f+\chi S\alpha^2\phi^2/2\ge0$, and edgewise $E_i\ge\chi_i E_i$ permits the calibrated inequality wherever $\chi_i\ne0$. Put
\[
A_i=A(\phi_i),\qquad A(\phi)=\frac{\alpha\phi\chi(\phi)}{m_c}.
\]
On a periodic ring, with $\Delta R_i=R(w_{i+1})-R(w_i)$,
\[
\sum_i A_i\Delta R_i=\sum_i(A_{i-1}-A_i)R(w_i)
\ge-\|R\|_\infty\|A'\|_\infty\sum_i|\phi_i-\phi_{i-1}|.
\]
The reindexing is valid for an unwrapped $w$ with any integer winding because $R(w+nd)=R(w)$; periodic $\phi$ gives $A_N=A_0$. Consequently the periodic lattice functional obeys
\[
F_h\ge \frac{\kappa}{2h}\sum_i|\phi_{i+1}-\phi_i|^2
-C_h\sum_i|\phi_{i+1}-\phi_i|,
\qquad C_h=\|R\|_\infty\|A'\|_\infty.
\]
No small-hop, zero-winding, or no-phase-slip assumption enters. A noninteger endpoint mismatch or open/free ends leave a boundary term. The regularity is sufficient: $q$ is Lipschitz, $R\in C^1$ with bounded derivative, and the discrete telescoping uses only values of $R$, not derivatives at its cusps. The cutoff support, inherited onsite inequality, and periodic/integer-registry boundary condition are the substantive premises.
