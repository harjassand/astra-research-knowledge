# A globally optimal finite-temperature passive resonator cell

Owned construction: physical_opportunity_fresh. Internal mathematical result, pending independent review. Historical novelty and physical material performance remain UNKNOWN.

## 1. Exact physical model and resource contract

An infinite periodic one-dimensional harmonic material has exactly one scalar backbone coordinate per unit cell. That backbone coordinate, of positive mass m, is connected to its counterpart in adjacent cells by a positive spring K. Any finite connected passive internal network of additional positive point masses and positive linear springs can attach within the cell. Total cell mass is M, fixed. Arbitrary topology, arbitrarily many optical modes, arbitrarily large internal stiffness and arbitrary dark modes are allowed to the comparator. No active element, damping, reservoir, negative stiffness or extra intercell bond is supplied.

Mass-normalize the cell. For q in [0,pi],
D(q)=D0+s(q) v v^T,  s(q)=4K sin^2(q/2),
where D0 is PSD, has the unique rigid-translation nullvector z normalized to unit length, ||v||^2=1/m, and (z^T v)^2=1/M.

There is a fixed positive lower bound m>=m_min on the backbone mass. In the explicit example m_min=1. This avoids the singular massless-backbone trick. M and K are identical for every competitor. Static long-wave stiffness is K, and acoustic speed (for fixed cell spacing a) is a sqrt(K/M), identical to the rigid-mass chain.

Transport is ideal-contact harmonic BALLISTIC thermal conductance of this infinite periodic spectrum, with unit transmission in each pass band. It is not diffusive conductivity, finite-contact conductance, full 3D thermal conductivity, electronic transport, or a room-temperature material claim. Internal connector mass, finite specific modulus, physical atomic geometry, disorder and anharmonicity require a separate realization calculation. All finite masses in the declared network are included.

Let theta=k_B T/hbar. Apart from the factor k_B/(2pi), conductance is
J_theta = integral_0^infinity g_theta(omega) chi(omega) domega,
g_theta(omega)=[omega/(2theta)/sinh(omega/(2theta))]^2,
where chi is the union-of-pass-bands indicator. The explicit construction uses theta=1/2 in the chosen frequency unit.

## 2. Two exact spectral resource identities

Write alpha_j=lambda_j(D0), beta_j=lambda_j(D0+4Kvv^T), ordered increasingly. Here alpha_0=0, alpha_j>0 for j>0, beta_j>0.

Rank-one interlacing yields
alpha_j <= beta_j <= alpha_(j+1)
for j below the final mode. Each eigenvalue branch increases continuously with s, so the pass bands are [sqrt(alpha_j),sqrt(beta_j)] with disjoint interiors. Zero-width dark bands do not affect the integrals.

First resource identity, from the trace:
integral 2omega chi(omega) domega
= sum_j(beta_j-alpha_j)
=4K/m.                                                   (T)

Second resource identity, from the determinant lemma:
prod_j(t+beta_j)/prod_j(t+alpha_j)
=1+4K v^T(D0+tI)^(-1)v.
As t tends to zero, the null translation mode gives
v^T(D0+tI)^(-1)v=1/(M t)+O(1).
Therefore
prod_j beta_j / prod_(j>0) alpha_j = 4K/M.
Put Omega_r=2sqrt(K/M), the rigid-total-mass comparator cutoff. Taking logs of the endpoint product gives the convergent regularized identity
integral_0^infinity [chi(omega)-1_[0,Omega_r](omega)]/omega domega=0.  (L)

No approximate density of states or acoustic-only truncation appears. The full optical spectrum is charged.

## 3. Classical limit benchmark

The total pass-band width is
W=Tr sqrt(D0+4Kvv^T)-Tr sqrt(D0).
For t>0 let q(t)=v^T(D0+tI)^(-1)v>=1/(M t). The scalar square-root/log determinant integral gives
W=(1/(2pi)) integral_0^infinity t^(-1/2) log[1+4K q(t)]dt
 >= (1/(2pi)) integral t^(-1/2) log[1+4K/(M t)]dt
 =2sqrt(K/M)=Omega_r.                                    (C)

The rigidly locked total mass saturates the infimum. Thus generic internal resonances do not improve the high-temperature classical ballistic conductance at the same M,K. An attractive acoustic gap alone is insufficient evidence.

## 4. Positive finite-temperature design and scalar dual

Set theta=1/2, so
g(omega)=(omega/sinh omega)^2,
h(omega)=omega g(omega)=omega^3/sinh^2 omega.

Define exact positive constants
h1=1/sinh^2(1),
h2=8/sinh^2(2),
mu=(h1-h2)/6 >0,
lambda=-(4h1-h2)/3 <0.

Let
F(omega)=h(omega)+lambda+2mu omega^2.
By construction F(1)=F(2)=0. Also F(4)<0<F(5), so there is a third root c in (4,5). Numerically,
lambda=-0.762690668386891023868323685448...,
mu=0.0193145037102902787301674481588...,
c=4.259874009292292484341159056875....

The crucial global sign assertion is
F<0 exactly on (0,1) union (2,c),
F>0 on (1,2) union (c,infinity).                          (S)

### All-frequency proof of (S), without a sampled sign claim

Multiplication by the positive factor sinh^2(omega)/omega^2 preserves every positive root and sign. The resulting entire function is
Q(omega)=lambda+omega+sum_(n>=1) a_n omega^(2n),
a_n=c_n[2mu+4lambda/((2n+2)(2n+1))],
c_n=2^(2n-1)/(2n)! >0.

Because lambda<0 and mu>0, the bracket increases strictly with n and tends to 2mu>0. Hence the even coefficient signs change at most once, from negative to positive. Here the first three a_n are negative and a_n>0 for n>=4.

Q'' therefore also has coefficients negative through n=3 and positive from n=4. Divide Q'' by omega^6. Each negative term has a negative exponent, so its derivative is positive; every positive term has a nonnegative exponent, so its derivative is nonnegative. The convergent series permits termwise differentiation on every positive compact interval. Thus Q''/omega^6 is strictly increasing and has at most one positive zero. Rolle's theorem implies Q' has at most two positive zeros and Q at most three. The already established distinct roots 1,2,c exhaust them and are simple (an extra multiplicity would force another derivative zero). Since Q(0)=lambda<0 and Q is positive for sufficiently large omega, (S) follows.

The signs lambda<0<mu and F(4)<0<F(5) can be checked by elementary exponential bounds; the script evaluates them with 70-digit Decimal arithmetic. The proof does not use finite sampling to exclude further roots.

## 5. Exact passive two-mass realization

Choose the following finite positive resources:
m_min=m=1,
K=(c^2-3)/4,
M=4-12/c^2,
M_side=M-1=3-12/c^2,
k=4 M_side/M.

Numerically:
K=3.7866316437609973,
M=3.3387164232022783,
M_side=2.3387164232022783,
k=2.8019347878118195.

The backbone mass 1 connects to adjacent backbone masses by K. A single side mass M_side attaches by k. In mass-normalized coordinates
D0=k[[1,-1/sqrt(M_side)],[-1/sqrt(M_side),1/M_side]].

At q=0 the squared eigenfrequencies are 0 and 4.
At q=pi they are 1 and c^2:
the trace is c^2+1, and the determinant is c^2.
Thus the exact pass bands are [0,1] union [2,c].
The equally massive rigid comparator has cutoff Omega_r=c/2.

All masses and stiffnesses are finite, with order-one ratios. The construction uses neither vanishing backbone mass nor unbounded internal frequency.

## 6. Global optimality, including backbone-mass reallocation

Let chi_* be these two bands. Consider ANY finite passive connected internal cell satisfying the same K,M and backbone mass m>=1. It may use more resonators, rearrange internal topology, lock all mass to the backbone, or choose arbitrary internal stiffness.

Define
r(omega)=g(omega)+lambda/omega+2mu omega=F(omega)/omega.
By (S), chi_*=1 exactly where r<0. Hence pointwise
r(omega)[chi(omega)-chi_*(omega)] >=0.

The logarithmic resource identity (L) cancels lambda. The trace identity gives
integral 2omega[chi-chi_*]domega=4K/m-4K<=0.
Therefore
J(chi)-J(chi_*)
= integral r(chi-chi_*)domega - mu[4K/m-4K]
>=0.                                                       (OPT)

The divergence of lambda/omega near zero is harmless: both spectra have a nonzero acoustic interval and their indicator difference vanishes near zero. Every finite competitor has bounded frequency support.

This proves a globally optimal, explicitly synthesized primitive for the entire declared passive single-backbone class, rather than merely a local search or a comparison to one unoptimized mass-in-mass cell. Equality requires m=1 and the same bands except sets of measure zero, since mu>0 and the sign is strict off the three endpoints.

## 7. Actual calculated benefit and strongest comparison scope

For ideal contacts:
J_*=integral_0^1 g + integral_2^c g =1.133319342823405,
J_rigid=integral_0^(c/2) g =1.440176577374174.
Thus J_*/J_rigid=0.786930825447633, a 21.3069% reduction in this finite-T harmonic ballistic contract.

This is consistent with the classical obstruction:
W_*=c-1=3.259874009292292,
W_rigid=c/2=2.129937004646146.
At high T the constructed cell is worse. At T tending to zero, both have the same single-channel conductance quantum to leading order. The advantage is a finite quantum thermal window, paid by a compensating optical band above the most useful thermal frequencies.

A monotone Riemann lower bound independently gives J_rigid-J_*>0.30685. The precise quadrature values are diagnostics of the displayed exact construction, not the proof of global optimality.

Competitors with multiple independent intercell connections, nonlocal intercell links, disorder/localization, added contact resistance, nonlinear/dissipative elements or alternative cell-spacing/material-strength contracts are outside OPT. They may outperform this class. A competent comparison at full material/device scale must admit these and count their complete costs. Known local-resonance thermal suppression is prior art; the particular global two-moment optimum/duality has not yet received a complete novelty audit.

## 8. Physical realization and consequence boundary

The enabling result is a resource-constrained attainable-spectrum optimization: exact mass/stiffness moments, a constructive global dual, and a finite primitive that wins in the correct finite-temperature transport output. Its possible role is designing passive phononic/thermoelectric/cryogenic links with minimal optical-spectrum waste; no application is established.

The point-mass/spring model treats bonds as massless force laws. For atomic lattices these are harmonic interatomic Hessians; for architected continuum materials, beam/neck/support mass and internal modes must be included. A rod of length a, modulus E and density rho has mass at least K a^2/(E/rho), so K cannot be held fixed while taking a finite-length physical backbone mass to zero. Actual specific-modulus, volume, strength and scattering constraints could shrink or eliminate the ideal margin. The theorem's fixed positive m_min contract preserves this unknown rather than hiding it.

No equipment operation, new specimen, hardware thermal measurement, diffusive conductivity reduction or unchanged electronic power factor was acquired in this construction. Primary nanophononic experiments establish their own systems only.

## Reproduction
Run python3 phonon_optimum.py. It saves phonon_optimum.json, reconstructs the two mass-normalized matrices and both spectral identities, evaluates the exact constants/root, checks all-band Bose integrals and the monotone improvement bound. Scalar sign samples are diagnostics; Sections 4 and 6 contain the global proof.


## 9. Exact rational endpoint and benefit certificate

phonon_dual_exact_certificate.py verifies the sign premises with exact Fraction arithmetic. For rational x>=0 and N=80,
L_N(x)=sum_(j=0)^N x^j/j! < exp(x)
< L_N(x)+[x^(N+1)/(N+1)!]/[1-x/(N+2)],
because the remaining Taylor-term ratios are bounded by x/(N+2)<1.

For E=exp(2omega)>1,
h(omega)=4omega^3/[E+1/E-2],
and its denominator is strictly increasing in E. The rational exponential enclosures therefore produce rational h,lambda,mu,F and coefficient enclosures. The actual exact assertions establish:
lambda<0<mu;
F(4)<-0.05869<0;
F(5)>0.22573>0;
F(17/4)<0<F(427/100);
the n=3 even-coefficient bracket is below -0.01584, and n=4 is above0.00473.

The exact script also uses monotone right/left Riemann bounds with 32 subintervals, enlarging the optical-loss interval from [c/2,c] to [17/8,427/100]. It proves
J_rigid-J_* >0.29034279485998>0
using rational arithmetic only. The sharper21.3069% numerical value remains a quadrature evaluation; strict positive benefit does not depend on quadrature or Decimal sign rounding.

Q and all its derivative series converge uniformly on positive compact intervals because they are products of polynomials and the entire sinh^2 series. The Q''/omega^6 derivative argument is thus valid on every positive compact interval and covers the whole positive axis by exhaustion.

The coefficient/sign and strict-improvement outputs are saved in phonon_dual_exact_certificate.json. Printed decimal representations of extremely narrow rational enclosures are rounded for display; the asserted signs use the exact underlying fractions.

## 10. Governing primary ancestry

The transport/scattering phenomenon is established prior art. Davis and Hussein's primary model of nanopillared silicon predicts lowered thermal conductivity through local-resonance hybridization, despite additional optical modes: [PRL112,055505(2014)](https://doi.org/10.1103/PhysRevLett.112.055505), [author preprint](https://arxiv.org/abs/1304.6070). Its thermal conductivity calculation is not the ideal ballistic fixed-resource theorem here.

Chien et al. explicitly count the total pass-band width in the classical intrinsic harmonic conductance and distinguish it from end-reservoir/contact transport: [PRE95,012137(2017)](https://doi.org/10.1103/PhysRevE.95.012137), [primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC5473347/). Their dimerized-chain model is a different intercell topology, so its detailed formula is not an imported premise for OPT.

Actual localized-resonance materials and electronic/thermal measurements exist in their own regimes: [Spann et al., Advanced Materials35(2023), DOI10.1002/adma.202209779, NIST primary record](https://www.nist.gov/publications/semiconductor-thermal-and-electrical-properties-decoupled-localized-phonon-resonances). These are mechanism ancestry and strong material comparators; they do not validate the present ideal cell or establish priority of its constrained optimum.

The source notes in sources_support/PHONON_SOURCES.md retain matched/unmatched mass, stiffness, geometry and readout scopes.


