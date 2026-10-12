# Point Coulomb: the energy pair state and an exact echo-word test

13 October 2026. Internal mathematical working state. The microscopic-to-Landau limit on $t=N\tau/\log N$ is **not proved**. The statements below distinguish exact $N$-body identities, an isolated two-body calculation, and a prescribed-field Fourier test. No diffusion is inserted into the physical particle dynamics.

## 1. Exact energy-weighted pair identity

Use the unit three-torus, the zero-mean periodic Green function $G(x)=c/|x|+O(1)$ near zero ($c>0$), and $F=-\nabla G$. The Hamiltonian is

\[
 H_N=\sum_{i=1}^N\frac{|v_i|^2}{2}+\frac1N\sum_{i<j}G(x_i-x_j),
 \qquad \dot v_i=\frac1N\sum_{j\ne i}F(x_i-x_j).
\]

Let $f_{1,N}$ and $f_{2,N}$ be the *probability* marginals of a symmetric law and $C_{2,N}=f_{2,N}-f_{1,N}^{\otimes2}$. Translation-invariant initial data remain translation invariant; hence $f_{1,N}(x,v)=m_N(v)$. Since $G$ has zero spatial mean, the product contribution to potential energy vanishes. Writing $K_N=\frac12\int |v|^2 f_{1,N}$, we have the exact identity

\[
 \frac{\mathbb E H_N}{N}=K_N(t)+\Phi_N(t),\qquad
 \Phi_N(t)=\frac{N-1}{2N}\int G(x-x')\,C_{2,N}(t,dz\,dz'). \tag{1}
\]

For homogeneous iid initial positions and velocities, $C_{2,N}(0)=0$, so $K_N(t)-K_N(0)=-\Phi_N(t)$. Thus convergence of the *second moments* to a homogeneous Landau/Balescu-Lenard law (which conserves kinetic energy) requires $\Phi_N(t)\to0$ along the claimed scaling. Weak convergence of the one-particle law without uniform integrability of $|v|^2$ does not by itself imply this condition. The signed scalar $\Phi_N$ can also conceal cancellation between spatial scales.

The exact weak first BBGKY equation for a velocity test $\varphi$ is

\[
 \frac d{dt}\langle\varphi,f_{1,N}\rangle
 =\frac{N-1}{N}\int F(x-x')\cdot\nabla\varphi(v)
 C_{2,N}(dz\,dz'). \tag{2}
\]

For $\varphi=|v|^2/2$, exchange symmetry turns (2) into

\[
 \dot K_N=\frac{N-1}{2N}\mathbb E[(v_1-v_2)\cdot F(x_1-x_2)]
 =-\dot\Phi_N. \tag{3}
\]

The $G$-weighted pair correlation measures available interaction energy. It does **not** bound the force term in (2): $F/G\asymp1/|x|$ near zero. Nor does the signed energy current in (3) control all test functions, since grazing deflections can change momentum directions while exchanging little pair kinetic energy. A kinetic closure also needs force history or impulse covariance, with its tensor structure.

## 2. Exact close-pair scale and smooth dimer obstruction

Let $\rho=N(x_1-x_2)$ in a local chart around zero and define the locally finite measure

\[
 \langle\psi,\mu_N(t)\rangle
  =(N-1)\mathbb E\,\psi(N(x_1-x_2),v_1,v_2),
 \qquad \psi\in C_c(\{\rho\ne0\}\times\mathbb R^6). \tag{4}
\]

The prefactor counts close partners per tagged particle. For a smooth cutoff $\chi_R$ supported in $|\rho|\le R$, the *exact* close-pair contribution to potential energy per particle is

\[
 U_{N,R}=\frac1{2N}\int G(\rho/N)\chi_R(\rho)\,d\mu_N. \tag{5}
\]

If $\mu_N$ has a locally convergent $1/|\rho|$-weighted limit, then $U_{N,R}\to(c/2)\int\chi_R(\rho)|\rho|^{-1}d\mu$. This convergence is not automatic from ordinary weak convergence because of the singular weight.

Put $s=Nt$ and $u=v_1-v_2$. Direct differentiation of (4) gives the exact fast-time weak equation

\[
 \begin{split}
 \frac d{ds}\langle\psi,\mu_N\rangle={}&
 \left\langle u\cdot\nabla_\rho\psi
 +\frac{F(\rho/N)}{N^2}\cdot(\nabla_{v_1}-\nabla_{v_2})\psi,
 \mu_N\right\rangle+\mathcal R_N(\psi),\\
 \mathcal R_N(\psi)={}&\frac{N-1}{N^2}\sum_{j=3}^N
 \mathbb E\left[(F_{1j}\cdot\nabla_{v_1}+F_{2j}\cdot\nabla_{v_2})
 \psi(Nr_{12},v_1,v_2)\right]. \tag{6}
 \end{split}
\]

On compact sets away from $\rho=0$, $F(\rho/N)/N^2\to c\rho/|\rho|^3$. The term $\mathcal R_N$ is the exact three-particle and external-field obligation; it cannot be dropped by a two-particle energy bound. If it vanishes on a fast layer, the limiting relative flow is $\rho'=u,\ u'=2c\rho/|\rho|^3$, conserving $|u|^2/4+c/|\rho|$. The local energy balance also has a flux through $|\rho|=R$ when the cutoff is used.

For iid uniform positions, at $s=0$ and fixed $R$,

\[
 \mu_N(B_R\times\mathbb R^6)=O(R^3/N^2),\qquad
 \int_{|\rho|\le R}\frac{c}{|\rho|}d\mu_N=O(R^2/N^2). \tag{7}
\]

For a uniformly random matching into dimers at separation $b/N$, the matched pair has probability $1/(N-1)$, so $\mu_N(0)$ converges to one unit of mass on $\rho=bn,\ v_1=v_2=V$, with $n$ uniform on the sphere and $V$ the shared Gaussian. At the same time, $\|C_{2,N}(0)\|_{\rm TV}\le2/(N-1)$, with the total-variation-norm convention, while $\Phi_N(0)\to c/(2b)$. The force-weighted variation is of order $N$.

There is a smooth version with the *same exact one-particle Gaussian*. Independently for each matched pair, take a uniform torus center, a uniform spherical direction $n$, and a smooth radial variable $B_N$ supported in $(b-\eta_N,b+\eta_N)$, where $\eta_N\downarrow0$. Place the particles at center $\pm B_Nn/(2N)$. Let $V\sim\mathcal N(0,\Sigma-\epsilon_N^2I)$ and independent $\xi_1,\xi_2\sim\mathcal N(0,\epsilon_N^2I)$, with $\epsilon_N\downarrow0$ and $\epsilon_N^2<\lambda_{\min}(\Sigma)$, and give them velocities $V+\xi_1,V+\xi_2$. Randomly match the labels. Every particle then has exactly the spatially uniform $\mathcal N(0,\Sigma)$ one-particle law, and the full $N$-particle law has a smooth density for each $N$. The pair relative velocity converges to zero, so the fast-layer limit below is unchanged.

Here is the isolation proof for a uniformly tagged matched pair. Choose $1/3<\alpha<1/2$ and $\delta>0$ with $\delta+2\alpha<1$. Since $G\in L^1(\mathbb T^3)$, the Gaussian kinetic energy and the absolute potential energy of matched and unmatched pairs give

\[
 \mathbb E\left[\sum_i\frac{|v_i(0)|^2}{2}
       +\frac1N\sum_{i<j}|G(r_{ij}(0))|\right]=O(N). \tag{8}
\]

Thus $|H_N|=O_P(N^{1+\delta})$. Because $G$ is bounded below, energy conservation gives $\sum_i|v_i(t)|^2/2=O_P(N^{1+\delta})$ uniformly in time. The maximum speed is consequently $O_P(N^{(1+\delta)/2})$, so every particle moves at most $O_P(N^{(\delta-1)/2})=o_P(N^{-\alpha})$ during $0\le t\le S/N$. Other pair centers begin within $N^{-\alpha}$ of the tagged center with probability $O(N^{1-3\alpha})=o(1)$; outside that event, all external particles remain at distance at least a fixed multiple of $N^{-\alpha}$ through the fast layer. Their total physical acceleration on either tagged particle is at most $C N^{2\alpha}$, and its impulse over $S/N$ is $O(N^{2\alpha-1})=o(1)$. In $s=Nt$ variables the tagged pair therefore obeys $\rho'=u,\ u'=2c\rho/|\rho|^3+o_P(1)$ on $[0,S]$. The limiting repulsive trajectory starts at $|\rho|=b>0$, stays away from zero, and remains bounded on $[0,S]$; ordinary ODE stability closes the estimate. In particular, $v_1=V+q(s)n+o_P(1)$ and $v_2=V-q(s)n+o_P(1)$, with

\[
 \rho=b(1+y^2),\quad
 q=\sqrt{c/b}\,y/\sqrt{1+y^2},\quad
 s=\frac{b^{3/2}}{2\sqrt c}
 [y\sqrt{1+y^2}+\operatorname{arsinh}y]. \tag{9}
\]

The limiting tagged velocity law has Fourier transform $e^{-\xi^T\Sigma\xi/2}\operatorname{sinc}(q(s)|\xi|)$ and kinetic energy above its initial Gaussian by $q(s)^2/2=c(1/b-1/|\rho(s)|)/2$. Weak convergence of the actual tagged law gives at least the lower bound $\liminf_N K_N(s/N)\ge K_N(0)+q(s)^2/2$; equality of finite-$N$ second moments would need a separate uniform-integrability argument. The bounded Fourier observable already differs by order one. This proves that unweighted fixed-tag chaos is insufficient for a restart theorem; the construction is correlated and is **not** a counterexample to the iid kinetic limit.

Even for iid data, (7) only initializes the close-pair state. Controlling its creation and transport up to $N/\log N$ physical time, and coupling it to all larger impact-parameter scales, remain open. A scalar energy ledger is necessary for the dimer obstruction but cannot supply the Landau tensor.

## 3. Exact two-body scattering logarithm and its limited implication

For the isolated repulsive potential $c/(Nr)$ in $\mathbb R^3$, incoming relative speed $g>0$, impact parameter $b$, and $a=2c/(Ng^2)$, Rutherford scattering gives $\theta=2\arctan(a/b)$. The change in one particle's velocity has transverse and longitudinal components

\[
 |\Delta v_\perp|=\frac{gab}{b^2+a^2},\qquad
 \Delta v_\parallel=-\frac{ga^2}{b^2+a^2}. \tag{10}
\]

If one *additionally* uses the independent-encounter flux $Ng\,2\pi b\,db$, azimuthal averaging gives the following exact scattering-level covariance rate for impacts $0<b<B$:

\[
 \begin{split}
 \mathsf C_N^{\perp}(g,B)
 &=\frac{4\pi c^2}{Ng}J(B/a)P_{\hat g},\\
 \mathsf C_N^{\parallel}(g,B)
 &=\frac{4\pi c^2}{Ng}\frac{B^2}{B^2+a^2}\hat g\hat g^T,\\
 J(z)&=\frac12\left[\log(1+z^2)+\frac1{1+z^2}-1\right]
 =\log z-\frac12+o(1). \tag{11}
 \end{split}
\]

Thus the transverse rate is $(4\pi c^2/g)(\log N/N)P_{\hat g}+O_g(1/N)$ for fixed $B$, whereas the longitudinal rate and strong impacts $b=O(a)$ are $O_g(1/N)$. This pins the candidate grazing scale $\nu_N=\log N/N$ and separates strong-pair energy from the logarithmic weak-scattering budget. In the actual $N$-body plasma, the independent-encounter flux, temporal decorrelation, dielectric response, and error accumulated over $N/\log N$ time are unproved. Equation (11) is not a stochastic or molecular derivation.

## 4. Enhanced damping test with all echo vertices retained

This is an exact calculation for the diagnostic equation $\partial_t h+v\partial_xh+E(x,t)\partial_v h=\nu\partial_v^2h$. It is **not** the microscopic plasma equation: $\nu$ is inserted only to test a proposed damping argument. With $\widehat h_k(\eta)=\int e^{-i\eta v}h_k(v)dv$, each free leg obeys

\[
 (\partial_t-k\partial_\eta)\widehat h_k=-\nu\eta^2\widehat h_k,
 \qquad \eta'(t)=-k,
 \qquad \text{damping}=e^{-\nu\int\eta(t)^2dt}. \tag{12}
\]

A field Fourier mode $p$ taking $k-p\to k$ contributes the *actual* Duhamel factor $-i\eta(t_j)E_p(t_j)$ at the interaction time $t_j$. For equal alternating legs $k,-k,k,-k,\ldots$, equal length $\Delta$, even leg count $r$, and observed terminal density $\eta(T)=0$, the boundary frequencies alternate $0,-k\Delta,0,-k\Delta,\ldots,0$. Therefore every second interaction factor is zero. The tempting damping estimate $\nu k^2T^3/(3r^2)=O(1)$ at $r\asymp T\asymp\nu^{-1}$ describes a **vanishing** word in this geometry.

A shifted path removes the zeros. Take $r$ even main legs of length $\Delta$ with $k_j=(-1)^j k$, followed by a final $+k$ leg of length $\Delta/2$. Observe density at $T=(r+1/2)\Delta$. Backward transport fixes the initial velocity frequency $\eta(0)=k\Delta/2$; at the $r$ interactions $t_j=j\Delta$,

\[
 \eta(t_j)=(-1)^j k\Delta/2,
 \qquad |p_j|=|k_j-k_{j-1}|=2|k|. \tag{13}
\]

For a Gaussian initial velocity profile of variance $\sigma^2$, and prescribed temporal impulse amplitudes $A_j=\int E_{p_j}(t)dt$ tending to delta pulses at $t_j$, the *specified ordered word coefficient* in the observed density has exact magnitude

\[
 |\rho_{k,\mathrm{word}}(T)|
 =\exp[-\sigma^2 k^2\Delta^2/8]
 \exp\left[-\nu k^2\Delta^3\left(\frac r{12}+\frac1{24}\right)\right]
 \left(\frac{|k|\Delta}{2}\right)^r\prod_{j=1}^r|A_j|. \tag{14}
\]

The damping exponent follows by integrating a triangle from $+k\Delta/2$ to $-k\Delta/2$ on each main leg, and the final half triangle to zero. If $T=\nu^{-1}$ and $r\sim\nu^{-1}$, then $\Delta\to1$ and the exponent tends $k^2/12$: enhanced damping alone does not suppress this arbitrarily long *geometric path*. But (14) retains the $r$ force amplitudes and $r$ velocity derivatives. For example, unit delta impulses and $k=1$ give the factor $2^{-r}$. With Poisson normalization $\widehat E_p=-ip|p|^{-2}\rho_p$, one has $|E_{\pm2k}(t)|=|\rho_{\pm2k}(t)|/(2|k|)$. A self-consistent echo therefore needs a sustained, correctly phased sequence of non-negligible charge modes; (14) does not construct it. Replacing those factors by one would manufacture an obstruction.

The remaining decisive task is to bound the **sum of weighted nonlinear histories** generated by iid particle dynamics (including their field response and microscopic pair state) on $T=N/\log N$. A free diffusion semigroup estimate, even an enhanced one, is insufficient by itself; the prescribed-field example also does not disprove the microscopic limit.
