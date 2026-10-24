# Section 6 check: product beam and thermal TLS

This is a row/column unitarity audit of Section 6 in `LOCAL_UNITARY_SPIN_SORTING_AND_RESET.md`. It uses its labels and fixed-total-energy scattering matrix; it does not alter the central note or redo its scattering witness.

Let $U=S_+(E)$ and label $a=L0$, $b=R0$, $c=L1$, $d=R1$. Define $F_1(E)=(T_{+,1}-T_{-,1})/2$ for incident TLS mode 1 from the left, at the same total energy $E$ used to define $F_0(E)$ for incident mode 0. Column $c$ unitarity gives

\[
T_{+,1}=|U_{bc}|^2+|U_{dc}|^2=1-|U_{ac}|^2-|U_{cc}|^2.
\]

Using $S_-=U^T$, transmission for spin minus and incident mode 1 is

\[
T_{-,1}=|U_{cb}|^2+|U_{cd}|^2=1-|U_{ca}|^2-|U_{cc}|^2,
\]

where the last equality is row $c$ unitarity. Thus

\[
F_1(E)=\frac{|U_{ca}|^2-|U_{ac}|^2}{2}=-F_0(E),
\]

because Section 4 gives $F_0(E)=(|U_{ac}|^2-|U_{ca}|^2)/2$. The sign and the equality require both the sector transpose relation and complete row/column unitarity at that energy.

For a product input with electron kinetic energy $K$ and thermal mode probability $p_\beta$ in mode 1, branch 0 has total energy $K$ and branch 1 has total energy $K+\Delta$. The mixture flux is therefore

\[
F_\beta(K)=(1-p_\beta)F_0(K)+p_\beta F_1(K+\Delta)
=(1-p_\beta)F_0(K)-p_\beta F_0(K+\Delta).
\]

Replacing this by $(1-2p_\beta)F_0(E)$ would silently correlate the electron kinetic energy with the TLS branch to hold total energy fixed; it does not describe the product preparation.

For the declared witness, both channels remain open for $K\in(1/4,3/4)$: the relevant kinetic energies $K-\Delta,K,K+\Delta$ lie in $(-2,2)$. Since the open-channel scattering matrix is regular, $F_0$ is continuous there. At $K_*=1/2$, the earlier exact witness gives

\[
F_*=F_0(K_*)=\frac{1125000\sqrt{15}}{413583083}>0.
\]

Continuity gives an open neighborhood $I\Subset(1/4,3/4)$ on which $F_0(K)>3F_*/4$. Choose any normalized smooth bump $h$ compactly supported in $I$; this is a genuine finite-width packet, with no width or minimum bandwidth asserted. Stationarity and orthogonality of distinct total-energy sectors give

\[
F_{\mathrm{packet},\beta}=\int |h(K)|^2\bigl[(1-p_\beta)F_0(K)-p_\beta F_0(K+\Delta)\bigr],dK.
\]

Since $|F_0(E)|\le1$ and $0<F_*\le1$, the sufficient condition $p_\beta<F_*/8$ yields

\[
F_{\mathrm{packet},\beta}
>\frac{3F_*}{4}-p_\beta\left(1+\frac{3F_*}{4}\right)
>\frac{17F_*}{32}>\frac{F_*}{2}>0.
\]

For $p_\beta=(1+e^{\beta\Delta})^{-1}$ this condition is $\beta\Delta>\log(8/F_*-1)\simeq6.6312$. It is a conservative sufficient dimensionless thermal margin, not a Kelvin-temperature or useful operating-window claim. The finite-band conclusion is existential by continuity; the support width is not quantitatively specified.
