# Spin-conserving inelastic sorter: algebra audit

This checks the pinned three-site ring plus one internal TLS in the fully unitary two-open-channel-per-lead regime. The claims below assume spin is conserved, both TLS channels are open, and every reflected and transmitted outcome is included. They do not model spin flips or unobserved loss.

## Spin-sector transpose and the unitarity bound

Let $S=S^+$ be the four-channel scattering matrix in contact order $(L0,R0,L1,R1)$, with TLS index $0$ or $1$. In the declared hopping convention, changing $sigma_z=+1$ to $-1$ conjugates the ring flux: $H^-=(H^+)^T$. On-site energies, the real site-3 coupling $\eta\tau_x$, and the diagonal lead self-energy matrix are unchanged by transpose. Thus the full retarded inverse Green matrices and their contact restrictions obey $G^-=(G^+)^T$. The channel broadening matrix $\Gamma$ is real diagonal, so the stated scattering formula gives

\[
S^-=I-i\Gamma^{1/2}(G^+)^T\Gamma^{1/2}=(S^+)^T.
\]

This is a relation between the two spin-conserving sectors; it does not convert either sector into a spin-flip process.

For a ground-TLS input from the left define

\[
T_+=|S_{R0,L0}|^2+|S_{R1,L0}|^2,\qquad
T_-=|S^-_{R0,L0}|^2+|S^-_{R1,L0}|^2
=|S_{L0,R0}|^2+|S_{L0,R1}|^2,
\]

and $T_{\rm avg}=(T_++T_-)/2$, $P_T=(T_+-T_-)/(T_++T_-)$ when the denominator is nonzero. Column unitarity for input $L0$ in the plus sector and row unitarity for output $L0$ in that sector give

\[
T_+=1-|S_{L0,L0}|^2-|S_{L1,L0}|^2,\qquad
T_-=1-|S_{L0,L0}|^2-|S_{L0,L1}|^2.
\]

Consequently

\[
T_+-T_-=|S_{L0,L1}|^2-|S_{L1,L0}|^2.
\]

Define the spin-averaged reflected excitation probability for this ground input by

\[
P_{\rm exc,ref}=\frac12\left(|S^+_{L1,L0}|^2+|S^-_{L1,L0}|^2\right)
=\frac12\left(|S_{L1,L0}|^2+|S_{L0,L1}|^2\right).
\]

Since $T_{\rm avg}|P_T|=|T_+-T_-|/2$, the triangle inequality yields

\[
T_{\rm avg}|P_T|\le P_{\rm exc,ref}.
\]

Let $P_{\rm exc,total}$ be the spin-averaged probability that the outgoing TLS is excited, summing both reflected and transmitted channels for each spin. Then $P_{\rm exc,total}=P_{\rm exc,ref}+P_{\rm exc,trans}$ with $P_{\rm exc,trans}\ge0$, so

\[
T_{\rm avg}|P_T|\le P_{\rm exc,ref}\le P_{\rm exc,total}.
\]

The first inequality depends on using both row and column unitarity and on defining the reflected excitation probability for the same ground-left input, averaged over the two spin sectors.

## Rank-one inelastic block and reflection difference

For fixed spin, let

\[
G_n=\bigl[(E-n\Delta)I-H_\sigma-\Sigma_n\bigr]^{-1},\qquad P_3=|3\rangle\langle3|,
\]

where $\Sigma_n$ acts on contact sites 1 and 2. The full inverse Green operator in TLS order $(0,1)$ has diagonal blocks $G_0^{-1},G_1^{-1}$ and off-diagonal blocks $-\eta P_3$. A rank-one Schur complement gives, with row TLS 1 and column TLS 0,

\[
G_{10}=\frac{\eta G_1P_3G_0}{1-\eta^2(G_0)_{33}(G_1)_{33}}.
\]

The reverse block is $G_{01}=\eta G_0P_3G_1/[1-\eta^2(G_0)_{33}(G_1)_{33}]$. Writing $r_{10}=S_{L1,L0}$ and $r_{01}=S_{L0,L1}$ for plus-spin reflection, the scattering convention gives

\[
r_{10}=-i\sqrt{\Gamma_1\Gamma_0}\,
\frac{\eta (G_1)_{13}(G_0)_{31}}{D},\qquad
r_{01}=-i\sqrt{\Gamma_0\Gamma_1}\,
\frac{\eta (G_0)_{13}(G_1)_{31}}{D},\quad
D=1-\eta^2(G_0)_{33}(G_1)_{33}.
\]

Thus the signed spin transmission difference is the difference of the two inelastic-reflection products:

\[
T_+-T_-=|r_{01}|^2-|r_{10}|^2
=\frac{\Gamma_0\Gamma_1\eta^2}{|D|^2}
\left(|(G_0)_{13}(G_1)_{31}|^2-|(G_1)_{13}(G_0)_{31}|^2\right).
\]

The two products need not agree in a flux-threaded ring. The equality to $T_+-T_-$ is also forced by the row/column unitarity identity above.

## Exact declared-point witness

The executable check `check_spin_scattering.py` uses $E=1/2$, $\Delta=1$, $\phi=\pi/2$, $\eta=2/5$, site energies $(0,3/10,-1/5)$, unit hoppings $1\leftrightarrow2\leftrightarrow3$, and $H_{31}=e^{i\sigma\phi}$. Both kinetic channel energies are $\pm1/2$, hence both channels are open, with $\Gamma_0=\Gamma_1=\sqrt{15}/2$. Exact SymPy arithmetic verifies $S^-=(S^+)^T$, exact unitarity, the rank-one block identity, and the two reflection amplitudes.

With $d=413583083$, the exact probabilities are

\[
|r_{10}|^2=\frac{3000(1489-375\sqrt{15})}{d},\qquad
|r_{01}|^2=\frac{3000(1489+375\sqrt{15})}{d},
\]

so the nonzero flux difference is

\[
T_+-T_-=\frac{2250000\sqrt{15}}{d}>0.
\]

The exact transport values are

\[
T_+=\frac{1125(713843+2000\sqrt{15})}{827166166},\quad
T_-=\frac{1125(713843-2000\sqrt{15})}{827166166},\quad
P_T=\frac{2000\sqrt{15}}{713843}=0.010851078868063\ldots.
\]

The inequality's two sides evaluate to

\[
T_{\rm avg}|P_T|=\frac{1125000\sqrt{15}}{d}=0.0105350205160\ldots,
\quad
P_{\rm exc,ref}=\frac{4467000}{d}=0.0108007319052\ldots,
\quad
P_{\rm exc,total}=\frac{61692000}{d}=0.149164708461\ldots.
\]

The executable exact-arithmetic assertions confirm both inequalities and reproduce the quoted $P_T$ value. This is a finite algebraic witness within the stated spin-conserving, fully unitary model; it does not establish performance outside that scope.
