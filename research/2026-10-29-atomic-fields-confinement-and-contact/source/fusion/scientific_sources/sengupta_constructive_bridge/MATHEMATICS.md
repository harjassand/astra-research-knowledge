# Source-specific axis and action criterion

Source: [Sengupta et al., arXiv:2610.28466v1](https://arxiv.org/html/2610.28466v1), printed Jacobi profiles and Appendix A maps. The established near-axis omnigenity condition is not new: see [Plunk, Landreman and Helander (2019)](https://arxiv.org/abs/1909.08919). This calculation applies it to these exact families and quantifies the resulting action defect. Exact omnigenity is not necessary for useful approximate or iso-action confinement.

The printed axes have u=u0,v=v0, since both transverse potential components vanish at the profile turning points. Write a=sinh(u0),b=sinh(v0). The paraboloidal axis is

\[
\gamma=(a\cos\zeta-b\sin\zeta,
 a\sin\zeta-b\cos\zeta,ab+\tfrac12\sin2\zeta).
\]

Direct differentiation gives (gamma'×gamma'')_z=a²−b² and

\[
|\gamma'|^2=(1+a^2)(1+b^2)-(ab-\sin2\zeta)^2,
\quad \min|\gamma'|^2=\min\{(a-b)^2,(a+b)^2\}.
\]

Full-circuit regularity excludes a=±b, so this particular axis has nowhere-zero curvature. This implication is not true for generic regular curves.

For the ellipsoidal web, at fixed R=(u0+v0)/4,S=(u0−v0)/4,

\[
\gamma=(A\,\mathrm{sn}\,t,B\,\mathrm{cn}\,t,C\,\mathrm{dn}\,t),
\quad t=\zeta/2+K_t/2,
\]

where the functions have parameter 1−g, g=m_g, and
A=cn(R|g)dn(S|g)/sn(R|g), B=dn(R|g)cn(S|g)/sn(R|g), C=sn(S|g)/sn(R|g).
The z component of gamma'×gamma'' is −AB dn³(t)/8. If A=0, the tangent vanishes at sn(t)=0; if B=0, it vanishes at cn(t)=0. Regularity therefore requires AB≠0 and again excludes curvature zeros.

# Axis strength cannot be constant

On either printed axis, put tau=kappa*zeta+delta, k²=m, d=dn(tau|1−m). Jacobi addition identities give

\[
 A_0=\mathrm{sn}(K+i\tau|m)+\mathrm{sn}(K+i(K'+\tau)|m)
 ={1\over d}+{d\over k},\qquad B_a=A_0/\sqrt{D_a}.
\]

All these axis profiles are meromorphic in complex zeta. A constant real B_a would imply the meromorphic identity A_0²=C²D_a. This is impossible when D_a has a simple complex zero, since a meromorphic square has only even-order zeros and poles.

For the regular paraboloidal axis, P=sqrt((1+a²)(1+b²))>|ab|+1. Its D_a=P²−(ab−sin2zeta)² vanishes when sin2zeta=ab±P, values outside [−1,1]. These roots have cos2zeta≠0 and are simple.

For the ellipsoidal axis let lambda=sn(R|g)^−2>1,nu=g sn²(S|g)∈[0,g),mu=dn²(t|1−g). Then

\[
D_a={(\lambda-\mu)(\mu-\nu)\over4},\qquad
(\partial_t\mu)^2=4\mu(1-\mu)(\mu-g).
\]

The elliptic function mu attains lambda in the complex plane, where its derivative is nonzero because lambda>1. Thus D_a again has a simple zero. The argument actually excludes any meromorphic replacement A_0 on the same regular constant-u,v axis. An unprinted Gardner construction is covered only if those axis and meromorphic-profile premises survive; no complete Gardner audit is asserted here.

Nonconstant analytic B_a has mirror minima. In vacuum, curl(B)=0 implies grad(B²/2)=(B·grad)B, so at an on-axis strength extremum

\[
\nabla_\perp B=B_a\,\boldsymbol\kappa.
\]

Since curvature is nonzero, the first transverse variation of each well bottom is nonzero. A nondegenerate tube cross-section spans the normal plane, so its first-order well-bottom strength cannot be independent of poloidal phase. This excludes exact near-axis omnigenity in the printed families, consistent with established QI/QS restrictions. It is not a practical confinement no-go.

For an isolated nondegenerate well of depth Delta=B_m−B_min, the full bounce action has leading form 2pi sqrt(mu_mag)*Delta/sqrt(B_ss). Its transverse gradient is dominated by −2pi sqrt(mu_mag)*grad(B_min)/sqrt(B_ss) as Delta→0. It is therefore nonzero at the axis for sufficiently deep trapped particles. Continuity excludes compact action contours inside some sufficiently small section neighborhood. The statement permits larger/off-axis iso-action contours and does not demonstrate global particle loss.

# Ellipsoidal half-period bound

This is a quantitative restriction, not just an exactness test. The profile satisfies A_0(tau+K')=A_0(tau). Period matching kappa=N K'/(2K_t) makes A_0 invariant under zeta→zeta+2K_t for every printed integer N and phase. The geometry then has mu→g/mu. Constant B_a would require D(mu)=D(g/mu), whereas

\[
D(\mu)-D(g/\mu)=-{(\mu^2-g)[\mu^2-(\lambda+\nu)\mu+g]\over4\mu^2}
\]

is not identically zero.

For 0<g<1/4, choose the paired values mu=1/2 and 2g. Put S=lambda+nu>1,p=lambda*nu>=0. Then

\[
{D(1/2)\over D(2g)}={S/2-1/4-p\over2gS-4g^2-p}
\ge {1\over8g(1-2g)}.
\]

To verify the inequality, the numerator exceeds the denominator: at S=1 their difference is (1/2−2g)² and it increases with S. The ratio consequently increases with p. At p=0 it also increases with S, so its lower bound is attained in the relaxed limit S=1,p=0. Because A_0 is identical at the paired phases,

\[
{B_{a,\max}\over B_{a,\min}}\ge[8g(1-2g)]^{-1/2}.
\]

At the printed low-g example g=(3−2sqrt(2))², the bound is 2.12413740856. This does not identify the parameters of the paper's separate N=3 trapped iso-action demonstration, and it does not prove poor confinement: good QI fields can deliberately have strong mirror variation.

# Actual reference well/action data

For the reference paraboloidal member, v0=delta=0,N=1,K'/K=5/2 and u0=acosh(sqrt(5)sech(2pi/5)). A stationary minimum is at zeta=1.11960950303 with B_min=10.4475912372,B_ss=42.4382736619 and curvature 1.65294053928. The eight located symmetry-related axis minima have a nonzero first-order coefficient, as recorded in `elliptic_checks_and_limits.json`.

Set d=dn(tau|1−m),T=1−(1−k)sn²(tau|1−m). The source flux-label Hessian at the axis is diagonal:

\[
H_{uu}=\kappa_f^2(1-m)T/d^2,\qquad H_{vv}=\kappa_f^2(1-m)T/k.
\]

With R=sinh(u0),P=cosh(u0),D=P²−sin²(2zeta), the relative transverse gradient is

\[
\partial_u\log B=-PR/D,\qquad
\partial_v\log B=-R\sin2\zeta/D.
\]

The relative half-spread of the well bottom on a small flux section is

\[
S_w\sqrt{\Delta\psi}+O(\Delta\psi),\quad
S_w=\sqrt{2\,(\nabla_{uv}\log B)^T H^{-1}(\nabla_{uv}\log B)}.
\]

The reference minima have S_w=0.413553099 or 0.529367296. At the less severe class, integrating actual source field lines to both mirror events at B_m=1.01B_min gives actions 0.0324041892 and 0.0397022105 for opposite offsets on the exact same surface DeltaPsi=5.7599965e−6. The axis action is 0.0360351616: full spread 20.2525%. Physical half-span is 0.000992109 source length units. Source cd is even, so the opposite offsets have identical flux labels exactly; this is not a mismatch of launch surfaces.

The normalized directional action derivative converges to−42.1913 at this finite depth. Its product with mirror depth approaches S_w as depth is reduced:0.430887,0.421913,0.417666,0.415183,0.414366 at depths 2%,1%,0.5%,0.2%,0.1%. The deep-well limit is 0.413553. Mirror-event/solver refinement changes actions by at most 3.1e−9 of the axis action in the tested cases. These finite action integrals are numerical, not interval-certified and not a drift-closure theorem.

There are real parameter tradeoffs. For v0=delta=0,N=1 and R=sinh(u0),

\[
\kappa_{\min}={R\over1+R^2},\quad
\kappa_{\max}={\sqrt{R^2+4}\over R^2},\quad
\iota={\mathrm{sech}(\pi K/K')\over\sqrt{1+R^2}}.
\]

At fixed positive iota, R<=sqrt(iota^−2−1). Letting R grow to reduce curvature drives transform to zero. Letting R→0 permits small curvature in some phases, but maximum curvature diverges and the maximum radius of a circular normal tube is at most R²/sqrt(R²+4). An arbitrarily thin/strongly shaped tube is not a matched finite-volume repair. These circular-tube statements do not exclude arbitrary cross-section shapes.

# A complete reference tube and the surviving current interface

This closes a geometric prerequisite without presuming the sampled tube is complete. Write x=kappa(u−u0),y=kappa v,U=cd(x|m),V=1/(k cd(y|m)). On |x|,|y|<K, U∈(0,1],V>=1/k. From the printed psi formula, psi_U<0 and psi_V>0. Holding V=1/k gives psi>=1/k−U; holding U=1 gives psi>=1/k−1/(kV). Thus

\[
\psi-\psi_a\le q<1\quad\Longrightarrow\quad
U,\mathrm{cd}(y|m)\ge1-q.
\]

Each phase section has a unique minimum at x=y=0 and strictly increases along every ray away from it. Its profile-box boundaries have psi−psi_a>=1. Hence every 0<q<1 level is a smooth closed oval before considering web regularity.

For the reference q=1/4, `certify_reference_tube.py` uses outward AGM elliptic-integral bounds to enclose the exact modulus root in m∈[0.00619,0.00620]. Jacobi amplitude obeys sqrt(1−m)<=am'(x)<=1, which gives cd(x|m)<=cos(sqrt(1−m)x)/sqrt(1−m) for x<pi/2. At x=.731 the upper bound is<.748344<.75. Therefore |x|,|y|<.731. The same interval calculation gives

\[
u-|v|>0.00325081,\qquad D>1.15053\times10^{-5}
\]

throughout the complete tube. Profile denominators stay nonzero and Re sn(K+x+i tau)>0; hence A>0 and B is analytic and nonvanishing there.

The web is globally injective on u>|v|. Put p=sinh(u)−sinh(v)>0,q=sinh(u)+sinh(v)>0,t=zeta−pi/4, X_+=(x_cart+y_cart)/sqrt(2),X_-=(x_cart−y_cart)/sqrt(2). Then

\[
X_+=p\cos t,\quad X_-=-q\sin t,\quad
z_{cart}=(q^2-p^2)/4+1/2-\sin^2t.
\]

At a shared image with nonzero X_+,X_-, w=sin²t is the unique solution in(0,1) of

\[
z_{cart}={X_-^2\over4w}-{X_+^2\over4(1-w)}+1/2-w.
\]

The right derivative is strictly negative. This recovers p,q and the signs of sin(t),cos(t), hence u,v,t uniquely. If one X component is zero, w is necessarily0 or1 because p,q>0, and the remaining equations still give uniqueness. Both components cannot vanish. The local Jacobian is nonzero because P D>0. Compact closed reference tubes are therefore globally embedded.

The ordinary external-current interface survives on any of these regular nested surfaces: K=−n×B/mu0 gives the exact source field inside and zero outside. The source harmonic potential has toroidal circulation C=4pi N_profile/(kappa k). Its phase modulo C is a smooth primitive circle map on a flux torus, with nonvanishing tangential gradient B. Its level sets are closed current loops; discretization carries I=C B_*L_*/(mu0 n_coils) per loop. This follows without closed magnetic field lines or rational transform. It is ordinary current-potential theory applied to this exact field. No quantitative finite-coil field/topology error, packing, finite conductor or engineering advantage is acquired in this new family.

# Constructive fixed-transform parameter test

The printed v0=delta=0,N=1 subfamily has sigma=pi K/K' and cosh(u0)=sech(sigma)/iota. Fix iota=1/sqrt(5), vary sigma, and retain all located well minima and a minimum barrier of twice the tested 1% mirror depth. This changes the exact source field; it does not remove any of the frozen finite-orbit launches.

Physical size is matched. If H is the axis label Hessian, the near-axis volume coefficient is

\[
V(\Delta\psi)=2\pi\Delta\psi\int_0^{2\pi}{P D\over\sqrt{\det H}}d\zeta+O(\Delta\psi^2).
\]

Here |det(DX)|=PD; the actual paraboloidal determinant is negative. Axis length is L_a=4sqrt(1+R²) E(1/(1+R²)). We fix V/L_a³=pi*1e−8, corresponding to effective minor radius/L_a=1e−4. The initial near-axis matching is then corrected using actual finite tube-volume quadrature and radial roots of the exact label, rather than retaining an arbitrary DeltaPsi.

A candidate at the exact rational sigma=1.34452 has m≈.0103247538853,u0≈.424728052953,kappa≈2.34265695666. It preserves exact iota=1/sqrt(5). A separate outward AGM/elementary certificate proves its entire DeltaPsi<=1e−5 tube is regular and embedded, with u−|v|>.4208006 and D>.1879283. The actual matched tube uses DeltaPsi=1.88806161e−6; reference uses2.53626517e−6. Volume target/refinement discrepancies are below 6.1e−9 numerically.

At1% well depth, actual mirror-to-mirror integrations retain all eight located classes and stay between their original adjacent axis maxima. The worst relative half-action spread is .08611450 for reference and .04557686 for candidate, ratio.52925877. The full spreads are 17.2229% and 9.11537%. No global critical-point enumeration or global optimization theorem is claimed.

This improvement is costly. Minimum relative axis-well barrier falls .0978955→.0200005; the near-axis elongation diagnostic increases 3.56486→4.77552; normalized maximum axis curvature increases 31.3727→53.7346. A 25-point scan plus the reference, with the reference barrier floor restored, finds no improvement over the reference. This is a scoped control, not a no-improvement proof.

The first attempted parameter result is retained. Its critical-point brackets missed a near-endpoint minimum and it lacked a mirror-barrier guard. The final code shifts endpoint brackets, applies barrier and post-rounding guards, and verifies actual mirror events. The initial result is not an admitted gain.

The tube here is deliberately tiny to calibrate the action derivative and the parameter mechanism. No claim covers broad finite-radius passing/trapped confinement or repair of the original four diagnostic-tube crossings. The latter were crossings of psi−psi_axis=.2 while source regularity still held, not demonstrated global losses. Larger or shifted action contours remain a live repair; a limited six-start magnetic-strength critical-point search found no accepted interior stationary well in its tested boxes, and is retained as a failed local search rather than a no-go theorem.

# Exact label-tangency replay

The source first integral is also checked algebraically rather than inferred from finite residuals. With s=sn(tau|1−m),c=cn(tau|1−m),d=dn(tau|1−m),D1=c²+mU²s²,D2=c²+mV²s², Jacobi addition gives

\[
b={U_u sc\over\kappa_fD1},\quad e={V_v sc\over\kappa_fD2},\quad
A=d(U/D1+V/D2).
\]

Writing L_U=partial_U log(psi),L_V=partial_V log(psi), the metric cross terms vanish because L_U/D2+L_V/D1=0. The remaining B·grad(psi) numerator vanishes using U_u²/kappa_f²=(1−U²)(1−mU²),V_v²/kappa_f²=(V²−1)(mV²−1), and d²=1−(1−m)s². `web_and_label_identities.py` verifies the complete rational identity, in addition to the web inverse and axis Hessian identities.

The candidate tube bound uses the sharper elementary comparison: cd(x|m)=cos(theta), theta'=sqrt(1−m cos²(theta))>=sqrt(1−m). Thus cd(x|m)<=cos(sqrt(1−m)x) before the first zero. At x=.0046 the interval upper bound is below .99999, proving all DeltaPsi<=1e−5 candidate sections stay in the certified profile box.

For an isotropic launch at a well minimum, the fraction confined to that isolated well is sqrt(delta_barrier/(1+delta_barrier)), from conservation of energy/magnetic moment. It changes .29861 to .14003 in the parameter test. This is not the overall confined phase-space fraction; higher-depth trajectories may enter a larger well class.
