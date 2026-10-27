# Mean-dominant reference scores and full commuting anchored filter order

Status: independently PASS; see `mean_dominant_commuting_filter_order_independent_audit.md`. Self-contained polynomial/SOS certificate and actual-source checks freshly replayed. No noncommuting filter order is asserted.

## 1. Actual score theorem

Let

psi=sqrt(r)|00>+sqrt(u)|11>+sqrt(v)|22>,
X=|psi><psi|+I3 tensor diag(a,b,c),

with r>0,u,v,a,b,c>=0. Let Q0 be the derivative of the homogeneous WH3 deficit under reference congruence by diag(sqrt(1+epsilon),1,1) at epsilon=0. This scales BOTH the distinguished main weight r and reset weight a.

**Claim:** Q0>=0 whenever 2r>=u+v.

In particular every largest-Schmidt-weight reference coordinate has nonnegative score, for arbitrary aligned reset weights. Scores in smaller coordinates are not claimed positive.

The exact acquired source formula is

Q0=r integral_0^infinity s/(a+s)^2
 g1(r/(a+s),u/(b+s),v/(c+s)) ds,                     (1)

g1(x,y,z)=-3/(3+x)-1/(1+x+y+z)
          +2/(2+x+y)+2/(2+x+z).

It follows either from the exact correlated3 by3 and output2 by2 blocks in `largest_schmidt_reference_score_finite_order_interface.md`, or directly from the reference entropy-gradient formula and Sherman-Morrison. Singular reset endpoints are received by xlogx continuity.

## 2. Pointwise companion balancing gives a scalar Stieltjes bath

At fixed x and y+z, reciprocal convexity gives

g1(x,y,z)>=g1(x,m,m), m=(y+z)/2.

Indeed only the last two reciprocal terms change. Thus the actual score is bounded below by the same integral with

m(s)=(1/2)[u/(b+s)+v/(c+s)].

This is a positive scalar Stieltjes bath of total mass M0=(u+v)/2<=r. The balanced kernel factors exactly:

g1(x,m,m)=2(1-m)(x+3m)/[(x+3)(x+m+2)(x+2m+1)].       (2)

If m(s)<=1 throughout s>0, the lower integral is pointwise nonnegative. Otherwise m has a unique crossing theta>0 with m(theta)=1. Homogeneous scaling of every mass by1/theta sets this crossing to1 without changing the sign. In these normalized variables r>=M0>=1.

Write the bath as m(z)=sum_j w_j/(B_j+z), with sum_j w_j/(B_j+1)=1. The tilted weights nu_j=w_j/(B_j+1) form a probability distribution on B_j>=0. Its mean is

M=E_nu B=M0-1<=r-1.

The proof below allows any finite such bath; the actual qutrit source uses at most two atoms.

## 3. Sharp harmonic-effective-bath derivative bound

Define

ell(z)=E_nu[1/(B+z)], beta(z)=ell(z)^-1-z.

Then m(z)=1+(1-z)ell(z)=(beta(z)+1)/(beta(z)+z). Jensen gives0<=beta<=M. Differentiation gives

beta'=E_nu[(B+z)^-2]/ell^2-1>=0.

The sharp upper bound is

beta'<=beta(M-beta)/(zM)                             (3)

when M>0; for M=0 the bath is concentrated at0 and beta'=0. To prove(3), Cauchy-Schwarz yields

[1-z ell]^2=[E B/(B+z)]^2
 <=M E[B/(B+z)^2]=M[ell-z E(B+z)^-2].

Substitute ell=1/(beta+z) and rearrange. Since the bound increases in M at fixed beta and M<=r-1,

0<=beta'<=beta(r-1-beta)/[z(r-1)].                    (4)

For r=1, necessarily M=beta=0 and the derivative is0. This mean constraint is essential: cruder variance bounds do not receive the ratio derivative.

## 4. A zero-area ratio and its two derivative endpoints

Let

q1(z)=4(z-1)/[(z+1)(z+3)(3z+1)], integral_0^infinity q1(z)dz=0.

For x=r/(a+z) and m=(beta+1)/(beta+z), the balanced density divided by q1 equals the removable rational function

R(z,a,beta,r)=
 r z(z+1)(z+3)(3z+1)(3a beta+3a+beta r+3beta z+r z+3z)
 /{2(3a+r+3z)
 [3a beta+a z+2a+beta r+3beta z+r z+z^2+2z]
 [3a beta+2a z+a+beta r+3beta z+r z+2z^2+z]}.

Thus the balanced score is the integral of R(z,a,beta(z),r) q1(z), up to the positive homogeneous scale removed earlier.

The total derivative is R_z+beta' R_beta. It is affine in beta'. By(4), it suffices to receive BOTH endpoints

R_z>=0,
R_z+[beta(r-1-beta)/(z(r-1))]R_beta>=0.              (5)

Set r=beta+1+k, k>=0. The self-contained checker `mean_dominant_reference_score_stieltjes_certificate.py` acquires R from(2) and proves(5) with exact polynomial arithmetic:

* The first endpoint, after multiplication by its explicitly positive denominator, has662 monomials, all positive coefficients.
* The second endpoint numerator has850 monomials, with only the two negative terms -82 beta k z^3-4 beta k z^4. Subtract

  42 z^2(beta-kz)^2+2 z^4(beta-k)^2

  from that numerator. The remainder has848 monomials, every coefficient positive (minimum2). This is an exact sum-of-squares plus positive-coefficient certificate, not a floating sign check.

Denominators are positive for z>0 and r>1. The r=1 case has beta=0 and is received by the first endpoint. Therefore the actual composite ratio R(z,a,beta(z),r) is nondecreasing.

Since q1 is negative below1 and positive above1, subtracting the constant R(1) times its zero integral gives

integral R(z)q1(z)dz=integral [R(z)-R(1)]q1(z)dz>=0.

The ratio is finite at the crossing and at infinity. The original source integrals and the baseline are integrable, so this centering is legitimate. Together with Section2 this proves the mean-dominant score theorem.

## 5. Full commuting anchored filter order

Let X0=3d Phi3+I3 tensor A, d>0,A>=0, and let Z be any invertible reference filter satisfying[A,Z*Z]=0. Put kappa=lambda_min(Z*Z). Then

D[(I3 tensor Z)X0(I3 tensor Z*)]>=kappa D(X0).        (6)

A reference unitary in the polar decomposition of Z does not affect the deficit. Simultaneously diagonalize A and K=Z*Z using matched physical/reference covariance. The filtered source has main weights h_i=d k_i and reset weights a_i k_i.

Order k1>=k2>=k3=kappa. Lower k1 to k2, keeping the other two fixed. The changing main coordinate is largest, hence satisfies the mean-dominant condition; its reference derivative is Q1/k1>=0. Therefore lowering it cannot increase the deficit. Next lower the tied pair k1=k2 together to k3. Both changing coordinates are largest, so the sum of their reference derivatives is nonnegative. At the endpoint the source is kappa X0, whose deficit is kappa D(X0) by homogeneity. This proves(6).

Singular filters follow by K+epsilon I and continuity, giving the corresponding value bound with kappa=0. The all-reset d=0 case is identically0.

This is a finite, throughput-charged comparison for ALL commuting reset/filter pairs, not merely one eigenaxis. It is not monotonicity along every arbitrary filter path, and no statement for[A,Z*Z]!=0 follows from the proof. The separately normalized entropy deficit need not be monotone.
