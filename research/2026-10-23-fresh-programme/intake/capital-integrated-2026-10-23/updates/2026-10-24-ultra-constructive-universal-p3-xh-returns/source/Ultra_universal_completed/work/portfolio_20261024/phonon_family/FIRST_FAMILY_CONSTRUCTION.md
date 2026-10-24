# Owned next construction: attainable spectral families

Saved before waking the four support roles for this continuation. The governing physical_opportunity/PHONON_OPTIMUM.md (99f7440a...) and earlier bytes are unchanged.

## Choice

Turn the isolated certified phonon optimum into an inverse-design theorem: characterize which full passive passband spectra are actually realizable, then show an open mass/stiffness/temperature family has a globally optimal ONE-resonator realization. All results keep the scalar single-backbone harmonic/ideal-ballistic contract. Physical-interface work is separately owned by passive_lag.

## First substantive general derivation

At any positive temperature theta define
g_theta(w)=[w/(2theta)/sinh(w/(2theta))]^2,
h_theta(w)=w g_theta(w),
F_p(w)=h_theta(w)+lambda+2mu w^2.

For lambda<0 and mu>0 the same entire-series coefficient argument as in99f proves F_p has at most three positive roots. Whenever three simple roots b<a<c exist, the full sign-minimizing spectrum is
chi_p=1_[0,b] +1_[a,c].
It has exact moments
A=b^2+c^2-a^2>0,
B=b^2 c^2/a^2>0.

Set arbitrary positive backbone lower-bound mass m0 and
K=m0 A/4,
M=m0 A/B,
M_side=M-m0
=m0 (a^2-b^2)(c^2-a^2)/(b^2 c^2)>0,
k=a^2 m0 M_side/M.
The two-mass pendant cell has q=0 squared frequencies0,a^2 and q=pi squared frequenciesb^2,c^2, so it realizes the sign spectrum exactly with finite positive parameters.

For all competitors with the same K,M and backbone m>=m0, the same two-moment dual proves it is globally optimal. This holds for every strict three-root pair, not only b=1,a=2.

## Why this is an OPEN resource family, not a temperature sweep

Let ell=ln b+ln c-ln a=0.5 ln B. At each root x, implicit differentiation gives
dx=-(d lambda+2x^2 d mu)/F'_p(x).
With endpoint signs epsilon=(+1,-1,+1), F'(x) has the same sign as epsilon. The Jacobian of (ell,A) with respect to (lambda,mu) is
J=-sum_(x=b,a,c) [epsilon_x x/F'_p(x)] u_x u_x^T,
u_x=(1/x,2x)^T.

Every weight is positive, and at least two of the u_x are linearly independent. Thus J is strictly negative definite, so the moment/resource map is locally invertible everywhere in the strict three-root region. The implicit-function/inverse-function theorem gives an open two-parameter set of dimensionless mass/stiffness resources with an exact attained global optimizer. Temperature and mass scaling add their normal physical dimensions.

This calculation needs careful verification of normalization and Jacobian orientation, but no numerical determinant assumption is needed.

## Second desired theorem: complete passive inverse realization

For arbitrary strictly interlacing squared endpoint lists
alpha0=0<beta0<alpha1<beta1<...<alpha_(n-1)<beta_(n-1),
let S=4K and form
q(t)=[prod(t+beta)/prod(t+alpha)-1]/S.
Interlacing should make q a positive Stieltjes sum with a zero-mode pole. Its endpoint moments fix q(t)~1/(m t) at infinity and q(t)~1/(M t) at zero.

Then the reciprocal dynamic mass
R(t)=1/[t q(t)]
should have the positive Foster expansion
R(t)=m+sum_j k_j/(t+nu_j^2),
so side masses M_j=k_j/nu_j^2 and springs k_j are all positive, with sum M_j=M-m.
This would realize every admissible passband union by an actual passive star network, turning necessary spectral moments into a complete attainable-spectrum description rather than an indicator relaxation.

This is a substantive inverse-network construction, but likely overlaps established Stieltjes/Foster/Cauer synthesis; exact prior and theorem scope must be checked. No claim of a newly invented network-synthesis principle.

## Unknowns and next proof target

Can the three-root moment image be characterized globally or shown to cover ALL finite theta, positive K and M>m0? At minimum the analytic Jacobian supplies an open family. A stronger complete result needs global existence/uniqueness and endpoint limits, not numerical parameter sweeps. If general coverage fails, identify the sharp attainable obstruction and build the correct family.

Historical novelty, material realization, full3D performance and mission success remain UNKNOWN/NOT_ACHIEVED.

