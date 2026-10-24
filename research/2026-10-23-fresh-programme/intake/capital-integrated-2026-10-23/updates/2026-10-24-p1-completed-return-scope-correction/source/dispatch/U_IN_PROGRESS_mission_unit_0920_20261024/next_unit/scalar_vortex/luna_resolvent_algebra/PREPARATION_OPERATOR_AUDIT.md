# Finite-cutoff preparation operator audit

This checks the spectral and adiabatic gates in Sections 4.1–4.3 of `REAL_SCALAR_PREPARATION_AND_LOCAL_VORTEX_PAIR.md`. The useful protocol convention is
\[
\widehat H_s^R=H_0+\chi_R(W_s-2),
\]
so the path starts at exactly $H_0$. This is the ideal $H_s-2$ with the same energy-origin shift; the unshifted path $H_0+2+\chi_R(W_s-2)$ has identical gaps and states but starts at $H_0+2$.

For $m=a-b^2/4>0$,
\[
P_s=(1-s)+sP=(1-s)+sm+s[(x+b/2)^2+y^2]
\]
is bounded below by $\min(1,m)>0$. Direct use of
\[
H_0(Qe^{-r^2/2})=e^{-r^2/2}(-\tfrac12\Delta Q+(x,y)\cdot\nabla Q+Q)
\]
with $Q=P_s$ gives $H_s(P_s e^{-r^2/2})=3P_s e^{-r^2/2}$. The positive profile is therefore the simple ground state, by positivity improvement for the scalar Schrödinger semigroup; $H_s$ has compact resolvent since $W_s$ is bounded and $H_0$ is confining.

The multiplier claims at $s=0$ need the distinction made in the source: $W_s\to W_0=2$ pointwise and strongly as bounded multipliers, but not in multiplier norm. Uniform spatial derivative bounds do hold. For $s>0$ set $X=\sqrt{s}(x,y)$; then
\[
W_s=\frac{2+2sa+\sqrt{s}\,bX_1}{1-s+sa+|X|^2+\sqrt{s}\,bX_1}.
\]
The denominator is $(1-s)+sm+|X+\sqrt{s}(b/2,0)|^2$, bounded below by $\min(1,m)$. Its shifted quadratic form controls $1+|X|^2$ uniformly, while the numerator is affine in $X$ with uniformly bounded coefficients. All $X$ derivatives of this quotient are uniformly bounded, and $\partial_x^\alpha=s^{|\alpha|/2}\partial_X^\alpha$; the $s=0$ multiplier is constant. This proves uniform $x$-derivative bounds of every fixed order. Pointwise continuity plus the uniform zeroth-order bound gives strong multiplier continuity.

That strong continuity upgrades to norm-resolvent continuity: in the resolvent identity, $W_t-W_s$ is uniformly bounded and strongly tends to zero, while $(H_s+i)^{-1}$ is compact. The compact-times-strong lemma makes the relevant product norm-small. The ground eigenvalue is exactly $3$ for every $s$ and simple; the next eigenvalue is continuous, so its positive gap has a positive minimum on $[0,1]$.

For the cutoff, the difference from $H_s-2$ is $(\chi_R-1)(W_s-2)$ and is supported on $r>R$. Uniform boundedness of $W_s$ and the quadratic form of $H_s$ give
\[
\|r(H_s+i)^{-1}\|\le C,\qquad
\|\mathbf1_{r>R}(H_s-2+i)^{-1}\|\le C/R,
\]
uniformly in $s$; a fixed spectral-parameter shift only changes the constant. Hence the cutoff resolvents converge in norm uniformly in $s$. There is no additional low-energy branch: all cutoff operators have a common lower bound, and norm-resolvent convergence (or min–max) preserves the rank-one cluster in a fixed bounded interval containing the ideal ground energy $1$ but no excited spectrum, uniformly in $s$. For sufficiently large $R$, the cutoff ground is simple and uniformly gapped. Its positive normalized vector converges in $L^2$ to the ideal one at $s=1$.

The asserted convergence in each fixed $D(H_0^k)$ also follows. The cutoff potentials and their spatial derivatives are uniformly bounded for $R\ge1$. The eigen-equation first bounds $H_0\phi_s^R$; commuting $H_0$ through the smooth bounded potential inductively bounds every fixed $H_0^k\phi_s^R$, uniformly in $s,R$. Interpolating this bound with the $L^2$ convergence yields convergence in each lower fixed graph norm. Constants need not be uniform in $k$ and the finite-$R$ adiabatic constants may depend on $R$.

For fixed finite $R$, $s\mapsto\widehat H_s^R$ is smooth in operator norm with common domain $D(H_0)$; its $s$ derivatives are compactly supported smooth multipliers. The uniform gap gives a smooth real normalized ground $\phi_s^R$, with $\langle\phi_s^R,\partial_s\phi_s^R\rangle=0$. Put
\[
B_s=\mathcal R_s^R\partial_s\phi_s^R,
\quad (\widehat H_s^R-\lambda_s^R)B_s=\partial_s\phi_s^R.
\]
For $\Psi=e^{-i\int^t\lambda_s^Rdt}(\phi_s^R+i\dot s B_s)$, the order-$\dot s$ terms cancel with this sign, and the residual is exactly
\[
(i\partial_t-\widehat H_s^R)\Psi
=-e^{-i\int^t\lambda_s^Rdt}\bigl(\ddot s B_s+\dot s^{\,2}\partial_sB_s\bigr).
\]
With $s(t)=\sigma(t/T)$, smooth and flat at both endpoints, $B_s,\partial_sB_s$ are bounded in any fixed graph norm for fixed $R$, so this residual is $O_{R,k}(T^{-2})$. Flatness makes the correction vanish at the two endpoints.

Finally let $A_s=\widehat H_s^R+c\ge1$. Smooth bounded multipliers with the required spatial derivatives act boundedly on each fixed $D(H_0^k)$, and these graph norms are uniformly equivalent to $\|A_s^k\cdot\|$ for fixed $R,k$. For the exact homogeneous evolution the instantaneous Hamiltonian commutes with $A_s^k$, leaving
\[
\left|\frac d{dt}\|A_s^k\psi\|^2\right|
\le C_{R,k}|\dot s|\|A_s^k\psi\|^2.
\]
Since $\int_0^T|\dot s|dt=1$, the graph propagator is uniformly bounded in $T$. Duhamel applied to the $O(T^{-2})$ residual over duration $T$ gives endpoint error $O_{R,k}(T^{-1})$. This argument is valid for the finite smooth cutoff family, not the uncut path at $s=0$; it establishes finite-time linear acquisition at the stated model scope, with no uniform-in-$R$ rate claimed.
