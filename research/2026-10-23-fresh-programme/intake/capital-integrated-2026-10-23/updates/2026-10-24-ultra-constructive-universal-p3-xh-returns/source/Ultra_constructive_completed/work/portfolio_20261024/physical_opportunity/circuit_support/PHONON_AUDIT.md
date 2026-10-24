# Audit: rank-one phonon bandwidth bound and finite-temperature optimum

## Verdict

The rank-one total-bandwidth bound is correct, with the stated constant, for a connected scalar spring cell whose only intercell element is one spring $K$ attached to a backbone mass $m_b$. The finite-temperature dual construction also passes: at one dimensionless temperature it gives a globally minimizing spectrum over all finite passive cells with fixed total mass and intercell spring, and any backbone mass $m_b\ge1$, provided the internal cell is connected and has no on-site pinning. A one-side-mass cell with $m_b=1$ realizes the minimizer exactly; the same certificate includes the rigid mass-on-backbone chain.

This is an exact harmonic-model result, not a measured thermal-conductance reduction. The global optimization does not charge a separate budget for internal spring stiffness or fabrication. It also excludes contacts, disorder, anharmonic scattering, additional intercell links, and multiple coupled polarizations. The mass-matched rigid-backbone chain is included as the endpoint $m_b=M_{\rm tot}$ of the globally optimized class.

## Rank-one bandwidth theorem

Write the mass-normalized Bloch matrix as

$$
D(q)=D_0+s(q)vv^T,\qquad s(q)=4K\sin^2(q/2),\qquad 0\le s\le4K,
$$

where $D_0\succeq0$, $D_0z=0$, $\|z\|=1$, and for one connected cell the nullspace is spanned by the rigid translation $z$. If the backbone mass is $m$, then $v=e_b/\sqrt m$, so

$$
|z^Tv|^2=1/M_{\rm tot},\qquad \|v\|^2=1/m.
$$

The $j$th eigenvalue is nondecreasing in $s$. Rank-one interlacing gives
$\lambda_j(D_0)\le\lambda_j(D_0+svv^T)\le\lambda_{j+1}(D_0)$ for $j<n$. Thus the $j$th passband is the interval
$[\alpha_j,\beta_j]=[\sqrt{\lambda_j(D_0)},\sqrt{\lambda_j(D_0+4Kvv^T)}]$, and different bands have disjoint interiors. Its total width is

$$
W=\sum_j(\beta_j-\alpha_j)
=\operatorname{Tr}\sqrt{D_0+4Kvv^T}-\operatorname{Tr}\sqrt{D_0}.
$$

For $t>0$, let $q(t)=v^T(D_0+tI)^{-1}v$. The resolvent projection onto the translational zero mode gives $q(t)\ge |z^Tv|^2/t=1/(M_{\rm tot}t)$. The scalar identity
$\sqrt{x}=\pi^{-1}\int_0^\infty t^{-1/2}x/(x+t)\,dt$ and the rank-one determinant lemma yield

$$
W=\frac1{2\pi}\int_0^\infty t^{-1/2}\log(1+4Kq(t))\,dt
\ge\frac1{2\pi}\int_0^\infty t^{-1/2}\log\!\left(1+\frac{4K}{M_{\rm tot}t}\right)dt
=2\sqrt{K/M_{\rm tot}}.
$$

For the last integral, set $t=(4K/M_{\rm tot})x^2$ and use
$\int_0^\infty\log(1+x^{-2})dx=\pi$. The trace-square-root formula follows by integrating by parts; the boundary terms vanish because the logarithm grows only logarithmically at zero and is $O(t^{-1})$ at infinity.

The constant is sharp: take a connected internal spring network and scale all its internal stiffnesses to infinity. All internal frequencies diverge, the cell moves rigidly, and the only finite passband tends to the comparator band of a mass $M_{\rm tot}$ on the backbone, with width $2\sqrt{K/M_{\rm tot}}$. The general bound is
$W\ge2\sqrt K\,\|P_{\ker D_0}v\|$; the positive translational overlap is essential. If the update is orthogonal to every zero mode, this argument gives no positive bound. Extra internal zero modes, on-site pinning, or extra intercell links also invalidate the fixed product identity used below.

In the classical, ideal ballistic limit the intrinsic conductance is proportional to total propagating bandwidth. Chien et al. give $\kappa_0=k_B\Omega/(2\pi)$ and explicitly define $\Omega$ as the sum of band widths ([primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC5473347/), Eq. 34). That establishes the bandwidth-to-classical-conductance relation, not the rank-one inequality above. The quantum harmonic transport/NEGF framework is developed by Dhar and Roy ([primary article](https://doi.org/10.1007/s10955-006-9235-3)). I did not find the exact rank-one lower bound in this bounded source check; this is not a priority or novelty claim.

## Spectral moment identities

Let $\chi(\omega)=\sum_j\mathbf1_{[\alpha_j,\beta_j]}(\omega)$, the number of propagating branches at frequency $\omega$. With a connected internal cell, $\alpha_1=0$ and $\alpha_j>0$ for $j\ge2$. Two identities constrain every such spectrum. The first depends on the competitor's backbone mass; the second depends only on fixed $K$ and total mass.

First,

$$
\int_0^\infty 2\omega\chi(\omega)d\omega
=\sum_j(\beta_j^2-\alpha_j^2)
=\operatorname{Tr}(D_0+4Kvv^T)-\operatorname{Tr}D_0
=4K/m_b.
$$

Second, define $\Omega_r=2\sqrt{K/M_{\rm tot}}$. The determinant lemma at the singular endpoint gives

$$
\det(D_0+4Kvv^T)=4K|z^Tv|^2\det{}'(D_0)
=\frac{4K}{M_{\rm tot}}\prod_{j\ge2}\alpha_j^2,
$$

where $\det{}'(D_0)=\prod_{j\ge2}\alpha_j^2$. Hence

$$
\frac{\prod_j\beta_j}{\prod_{j\ge2}\alpha_j}=\Omega_r,
\qquad
\int_0^\infty\frac{\chi(\omega)-\mathbf1_{[0,\Omega_r]}(\omega)}{\omega}\,d\omega=0.
$$

The corresponding squared-eigenvalue endpoint product is $\prod_j\beta_j^2/\prod_{j\ge2}\alpha_j^2=4K/M_{\rm tot}=\Omega_r^2$; the displayed frequency-endpoint product is its square root. The last integral is understood as a common lower-cutoff limit; the acoustic divergence cancels. This logarithmic moment is fixed by $K$ and $M_{\rm tot}$, not by the backbone mass or the number or topology of internal springs.

## Exact finite-temperature dual construction

At $\theta=k_BT/\hbar=1/2$ in a chosen frequency unit, the Landauer weight per ideal propagating channel is, up to the common factor $k_B/(2\pi)$,

$$
g(\omega)=\left(\frac{\omega}{\sinh\omega}\right)^2.
$$

Set $h(\omega)=\omega g(\omega)=\omega^3/\sinh^2\omega$, and choose

$$
\mu=\frac{h(1)-h(2)}6=0.0193145037103\ldots,
\qquad
\lambda=-\frac{4h(1)-h(2)}3=-0.762690668387\ldots.
$$

Then $F(\omega)=h(\omega)+\lambda+2\mu\omega^2$ vanishes at 1 and 2. The signs are

$$
F(0)=\lambda<0,\quad F(3/2)>0,\quad F(4)<0,\quad F(5)>0,
$$

with numerical values $F(3/2)\approx0.0686282$, $F(4)\approx-0.0586905$, and $F(5)\approx0.225737$. Therefore there is a third root $c\in(4,5)$, numerically $c\approx4.25987400929$.

The sign pattern is global, not inferred from a grid. For $\omega>0$, $F$ has the same sign as

$$
Q(\omega)=\frac{F(\omega)\sinh^2\omega}{\omega^2}
=\lambda+\omega+\sum_{n\ge1} c_n d_n\omega^{2n},
\quad c_n=\frac{2^{2n-1}}{(2n)!},\quad
 d_n=2\mu+\frac{4\lambda}{(2n+2)(2n+1)}.
$$

Here $d_n$ increases strictly from
$d_1=-(h(1)+2h(2))/9<0$ to $2\mu>0$, so the coefficients of $Q''$, as a power series in $x=\omega^2$, change sign once from negative to positive. Divide that series by $x^{n_0-1}$, where $n_0$ is the first positive-coefficient index. Every negative lower-power term and every positive higher-power term then has positive derivative, so the quotient is strictly increasing on $x>0$; $Q''$ has at most one positive zero. Rolle's theorem gives at most three distinct positive zeros for $Q$. The roots 1, 2, and $c$ are therefore all the positive roots, and the listed signs imply

$$
\chi_*(\omega)=\mathbf1_{[0,1]}(\omega)+\mathbf1_{[2,c]}(\omega)
=\mathbf1_{\{F<0\}}(\omega)\quad\text{a.e.}
$$

For any feasible passive spectrum $\chi$, the two moment constraints imply

$$
\int g(\chi-\chi_*)d\omega
=\int\left(g+2\mu\omega+\frac{\lambda}{\omega}\right)(\chi-\chi_*)d\omega
=\int\frac{F(\omega)}{\omega}(\chi-\chi_*)d\omega\ge0.
$$

The inequality holds pointwise because $\chi_*=1$ where $F<0$ and $\chi_*=0$ where $F>0$. Near zero, both physical spectra contain an acoustic interval, so the common-cutoff interpretation of the logarithmic moment makes the difference integral finite. For a competitor with backbone mass $m_b\ge1$, the exact trace moment is $4K/m_b\le4K$, while the candidate with $m_b=1$ has trace moment $4K$. Thus
$$
J(\chi)-J(\chi_*)=\int r(\chi-\chi_*)d\omega-\mu\left(\frac{4K}{m_b}-4K\right)\ge0.
$$
Both terms are nonnegative: the first by the pointwise sign certificate and the second because $\mu>0$ and $m_b\ge1$. This proves a global minimum over the whole fixed-$(K,M_{\rm tot})$ passive-cell class with the stated lower bound on backbone mass, not merely a local or numerically sampled optimum. It also holds over the larger relaxed class $0\le\chi\le1$ with the same two moment relations.

### Attaining cell

Take a backbone mass $m=1$ and one side mass $M_s$, joined by an internal spring $k$. For $s=4K\sin^2(q/2)$, the squared frequencies $\rho=\omega^2$ solve

$$
mM_s\rho^2-[M_s s+k(m+M_s)]\rho+sk=0.
$$

Choose

$$
K=\frac{c^2-3}{4},\qquad
M_{\rm tot}=4-\frac{12}{c^2},\qquad
M_s=3-\frac{12}{c^2},\qquad
k=\frac{4M_s}{M_{\rm tot}}.
$$

All are positive and finite because $4<c<5$. At $s=0$, the roots are 0 and 4; at $s=4K=c^2-3$, the roots are 1 and $c^2$. Monotonicity in $s$ therefore gives exactly the bands $[0,1]$ and $[2,c]$, realizing $\chi_*$. Numerically these parameters are $K\approx3.78663164$, $M_{\rm tot}\approx3.33871642$, $M_s\approx2.33871642$, and $k\approx2.80193479$; units are dimensionless and must be scaled to any proposed physical frequency and mass.

As a separate conventional comparator, the rigidly bound mass-$M_{\rm tot}$ chain with the same $K$ has one band $[0,\Omega_r]=[0,c/2]$. Direct quadrature of the ideal Landauer weight gives $I_*=\int g\chi_*\approx1.13331934$ and $I_{\rm rigid}=\int_0^{c/2}g\approx1.44017658$, ratio $0.78693$. The rigid chain is also covered by the global certificate: it has the same $K$ and total mass and backbone mass $m_b=M_{\rm tot}\ge1$. More generally the optimum covers every internal topology and every backbone-mass allocation satisfying $1\le m_b\le M_{\rm tot}$.

## Scope and physical gate

The finite-temperature optimum is for **intrinsic ideal ballistic transport**: each propagating branch has unit transmission and the reservoirs are matched so that contact reflection is absent. It is not the conductance of a finite sample with arbitrary leads. Chien et al. explicitly find that boundary reservoirs can produce large contact-dependent departures from the intrinsic conductance even for lattices with identical bulk bands ([primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC5473347/), §§III–IV). No physical material, fabrication route, finite-length transmission, anharmonic lifetime, or matched internal-stiffness cost was acquired here. The mathematical result identifies an exactly optimal spectrum in a sharply stated passive class; practical thermal benefit remains unestablished.
