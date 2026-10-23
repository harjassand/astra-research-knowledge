# Binary registry interface audit

Let the ring have $N$ sites (indices modulo $N$), $\sigma_i\in\{-1,+1\}$, and $m_i=m(\sigma_i+\sigma_{i+1})/2$. Assume $m>0$, $0\le J\le hSm^2/2$, and $m<m_c r_h$ so the finite-$h$ calibration applies to every nonzero mismatch $m_i\in\{-m,+m\}$. With $\Delta R_i=R(w_{i+1})-R(w_i)$ it gives
\[
\frac{S}{2h}(\Delta w_i-hm_i)^2+hV(w_i)
\ge \frac{hS m_i^2}{2}+\frac{m_i}{m_c}\Delta R_i.
\]
Adding the binary bond term, the non-corrector baseline is
\[
B_i=\frac{hS m_i^2}{2}-J\sigma_i\sigma_{i+1}
=\begin{cases}
hSm^2/2-J,&\sigma_i=\sigma_{i+1},\\
J,&\sigma_i\ne\sigma_{i+1}.
\end{cases}
\]
It is nonnegative under the stated two-sided range for $J$. The sign restriction $J\ge0$ is needed for unlike bonds.

For periodic $w$ modulo its registry period, $R(w_N)=R(w_0)$ even if its unwrapped winding is any integer multiple of $d$. Summation by parts therefore yields
\[
\sum_i\frac{m_i}{m_c}\Delta R_i
=\frac1{m_c}\sum_i(m_{i-1}-m_i)R(w_i)
\ge-\frac{\|R\|_\infty}{m_c}\operatorname{TV}(m).
\]
Here $\operatorname{TV}(m)=\sum_i|m_i-m_{i-1}|$ and $\operatorname{TV}(\sigma)=\sum_i|\sigma_i-\sigma_{i-1}|$. Since
\[
m_i-m_{i-1}=\frac m2(\sigma_{i+1}-\sigma_{i-1}),
\]
the triangle inequality and an index shift give $\operatorname{TV}(m)\le m\operatorname{TV}(\sigma)$. Thus the exact interface-controlled lower bound is
\[
E\ge \sum_i B_i-\frac{m\|R\|_\infty}{m_c}\operatorname{TV}(\sigma).
\]
If $N_{\rm w}$ is the number of unlike bonds, $\operatorname{TV}(\sigma)=2N_{\rm w}$ and
\[
\sum_i B_i=(hSm^2/2-J)(N-N_{\rm w})+JN_{\rm w}.
\]
In particular at $J=hSm^2/4$, every bond has baseline $hSm^2/4$, so
\[
E\ge \frac{N hSm^2}{4}-\frac{2m\|R\|_\infty}{m_c}N_{\rm w}.
\]
Consequently a negative-energy configuration must have wall fraction
\[
\frac{N_{\rm w}}N>\frac{hS m m_c}{8\|R\|_\infty}.
\]
This is a necessary interface-density condition from the bound, not a sufficient condition or a selected-period result. The mean-zero constraint requires equal numbers of $+$ and $-$ sites (so $N$ is even); it does not change the cyclic summation.

For the proposed six-cell configuration, take $\sigma=(+,+,+,-,-,-)$ and label $w_i$ at the same site used in $V(w_i)$, with edge $i$ running from $w_i$ to $w_{i+1}$. Then
\[
(m_i)_{i=0}^5=(m,m,0,-m,-m,0),\qquad
(w_i)_{i=0}^5=hm(-1,0,1,1,0,-1).
\]
The cyclic differences satisfy $\Delta w_i=hm_i$ on all six bonds, including the wraparound bond. The node-square sum is $\sum_iw_i^2=4h^2m^2$, and $1-\cos x\le x^2/2$ gives
\[
\sum_i hV(w_i)\le 2K h^3m^2,\qquad K=\beta^2V_0.
\]
There are four aligned and two unlike bonds, so $\sum_i\sigma_i\sigma_{i+1}=2$ and the chemical contribution is $-2J$. Therefore
\[
\frac{E}{6h}\le \frac{Kh^2m^2}{3}-\frac{J}{3h}.
\]
At $J=hSm^2/4$ this is $-Sm^2/12+Kh^2m^2/3$, strictly negative when $h/\xi<1/2$ with $\xi=\sqrt{S/K}$. The cosine inequality is global, so no small-$\beta hm$ approximation is needed. This trial is admissible for the mean-zero ring and is lower than, for example, the alternating mean-zero state (whose $m_i=0$, $w_i=0$, and energy is $+6J$ under the displayed convention).

At $J=hSm^2/4$, the same bound is $E\ge NJ-(m\|R\|_\infty/m_c)\operatorname{TV}(\sigma)$. Thus any thermodynamic sequence with $\operatorname{TV}(\sigma)/L\to0$, $L=Nh$, has $\liminf E/L\ge J/h$. A balanced two-domain construction attains this macroscopic limit exactly for the stated ring functional: set $w_i=0$ at every registry minimum and choose the common strain on bond $i$ to be $r_i=Cm_i/(C+D)$. Since $\sum_i m_i=m\sum_i\sigma_i=0$, the integrated common displacement is periodic; the common square vanishes, and each aligned or unlike bond contributes exactly $J$. This is the mechanical relaxation premise behind the reference and requires no extra common-strain-gradient penalty. The six-cell trial's strictly negative energy density therefore beats this macroscopic-sequence bulk limit, as well as the alternating reference, under the displayed parameters; repeating its six-cell pattern preserves that trial density on rings of length $6kh$. It still does not identify a finite-$L$ or thermodynamic global minimizer, or rule out other mixed morphologies.

The sign of the *absolute* energy depends on the chosen additive exchange constant: adding $+J$ per bond shifts all fixed-$N$ states by $NJ$ and leaves the gap $NJ-E$ to the macroscopic reference invariant. So the comparison is the energy gap between admissible states under the same convention, not the sign of an isolated absolute energy. No cyclic indexing error was found.
