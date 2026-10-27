# Two coherent reversible modes with an arbitrary overlapping reset flag

## Whole-class theorem

Let V:C3 tensor C2 -> R be an isometry, let f be ANY unit vector of R, and 0<=p<=1. The actual TP channel

 E(rho)=p V(rho tensor I2/2)V*+(1-p)Tr(rho)|f><f|

has nonnegative WH3 Choi deficit. The reset flag need not be orthogonal to the success code, and its component inside that code may be entangled between qutrit and logical coordinates. This is a genuinely coupled TWO-mode family, not a convex combination argument using one-mode entropy positivity.

Put theta=||V*f||^2. Its deficit is zero exactly when p=0, p=1, or theta=0. Thus within this class the exact zero cases are reset, reversible mixed-logical encoding, or orthogonally heralded generalized erasure. No assertion for unequal logical weights or arbitrary two Kraus operators is made.

## 1. Actual source and symmetry reduction

A reference isometry reduces to the normalized Choi state

 A=p Phi_(A,R0) tensor I_L/2
   +q (I_A/3) tensor |f><f|, q=1-p.

The success reference is R0 tensor L of dimension6. At most one additional reference direction is needed for the outside component of f. Write

 f=sqrt(theta)g+sqrt(1-theta)f_perp,

where g is a unit vector in C3 tensor C2. For theta>0, physical covariance paired with the conjugate success-reference qutrit unitary, and the flat logical I2/2 symmetry, put

 g=sqrt(lambda)|0,0>+sqrt(1-lambda)|1,1>, 0<=lambda<=1.

This is an exact unitary equivalence, not an entropy pinching. Phases of the single outside vector are immaterial.

## 2. Exact principal-angle spectra

Write f2(S,P) for trace entropy of a positive 2x2 matrix with trace S and determinant P, with continuous zero endpoints. Set

 a=p/2, b=q/3, c=pq/18,
 Sin=a+b, Aout=p/3, Bout=2q/3, Sout=Aout+Bout,
 r=p/6.

The source is a weighted sum a Pmain+b Qflag of projections of ranks2 and3. The nonzero eigenvalues of Pmain Qflag Pmain are theta lambda/3 and theta(1-lambda)/3. Therefore the source entropy is

 f(A)=f2(Sin,c(3-theta lambda))
      +f2(Sin,c(3-theta+theta lambda))+f(b).       (1)

The unscaled output L=2N(A) is Aout Pminus+Bout Qflag, where Pminus=P_antisym(A,R0) tensor I_L has rank6. The compressed overlap Qflag Pminus Qflag has eigenvalues

 theta(1-lambda)/2, theta lambda/2, theta/2.

Indeed its physical qutrit matrix is theta(I-rho_g,R0)/2. Thus

 f(L)=f2(Sout,2c(2-theta+theta lambda))
      +f2(Sout,2c(2-theta lambda))
      +f2(Sout,2c(2-theta))+3f(Aout).             (2)

These weighted-projection formulas can be verified by diagonalizing the principal-angle 2x2 spans; a pair of weights a,b and overlap z has trace a+b and determinant ab(1-z). The unmatched projection directions contribute the displayed spectator eigenvalues.

The reference state is r P_success+q|f><f|. Its entropy is

 f(R)=5f(r)+f2(r+q,rq(1-theta)),                 (3)

independent of lambda. Hence the exact deficit is f(A)+f(R)-f(L)+kappa, with kappa=log(4/3). All spectra are actual source spectra, including the factor two on the output.

## 3. Paid concavity in the flag's Schmidt allocation

For p,q>0 the determinants in (1)-(2) are positive, even at theta or lambda endpoints. The fixed-trace determinant Hessian is

 partial_P^2 f2(S,P)=integral_0^infinity ds/(s^2+Ss+P)^2.

Let Pin,1 and Pin,2 be the denominator polynomials from (1), and Pout,1 and Pout,2 the lambda-dependent ones from (2). Directly,

 2Pin,1(s)-Pout,1(s)
 =s^2+(2p/3)s+2c(1+theta-2theta lambda)>=0,

 2Pin,2(s)-Pout,2(s)
 =s^2+(2p/3)s+2c(1-theta+2theta lambda)>=0.        (4)

Thus 1/Pin,j^2<=4/Pout,j^2 pointwise. Because the input determinant slopes are +/-c theta and the output slopes are +/-2c theta,

 partial_lambda^2 Delta
 =c^2 theta^2 integral_0^infinity
   [1/Pin,1^2+1/Pin,2^2-4/Pout,1^2-4/Pout,2^2] ds
 <=0.                                          (5)

It is strictly negative when p,q,theta>0, since (4) is strict for s>0. Consequently the minimum over lambda occurs at an endpoint. This is an exact source-compatible Schmidt-allocation comparison, not generic concavity of the entropy deficit in the channel or in its Kraus weights.

## 4. Endpoint receiving by one coherent star plus an orthogonal mode

At lambda=0 or1 the inside flag component is a PRODUCT between success qutrit and logical coordinate. The other logical mode is reference-orthogonal both to f and to the first mode. The source therefore splits into two actual orthogonal reference blocks:

 (p/2)Phi3+q(I3/3) tensor P_f,
 and (p/2)Phi3.

The first is an arbitrary-overlap coherent star, paid by the whole-star theorem; the second has zero deficit. Direct reference-sum additivity gives nonnegative endpoint deficit. Equation (5) then proves the whole-class value theorem.

For p,q,theta>0 the endpoint star has D=qI3/3 nonzero, a coherent center vector of squared norm p theta/6>0, and remaining leaf physical bath (p/6)(I-theta P_u), of rank at least two. The established coherent-star equality classification therefore makes the endpoint deficit strictly positive. All intermediate lambda values are then strictly positive as well. If theta=0, the reset is orthogonally flagged from the reversible rank-two main and the deficit is exactly zero. If p=0 or1, reset or reversible-code equality applies directly. This proves the full stated zero classification.

## What is and is not acquired

This receives arbitrary two-mode flag orientation for a FLAT logical success state I2/2, including generic rank-two projected center coupling and Choi rank five. It does not expose hidden Kraus labels as measured outcomes, replace reference-qubit noise by physical-qubit noise, or extend by convexly mixing unequal-weight mode cases. The arbitrary two-coherent-mode/shared-flag value problem remains open.

## 5. Explicit global generalized-erasure capability

The same whole-class proof is quantitative. There exists an actual generalized-erasure channel with the SAME success probability p and flat logical success state I2/2 such that

 ||E-E_hat||_diamond<=min(2,72sqrt(Delta(E))).    (6)

Use a fixed output isometric padding to dimension at least seven when required; no outcome is postselected. At a Schmidt-allocation endpoint, the affected star has trace tau=q+p/2, normalized parameters

 t=p theta/(6tau), a=q/(3tau), x=p/(6tau).

The audited scalar coherent-star payment Delta>=3t ax/4 and homogeneity give

 Delta(E)>=p^2 q theta/(144 tau^2)
          >=min(p,q)^2 theta/576.              (7)

For the last inequality, if p<=q then q>=1/2 and tau<=1; if q<=p then p>=1/2 and q<=1. These give the displayed deliberately weaker common constant. Concavity in lambda transfers the endpoint lower bound to the entire class.

There are two direct, actual-channel comparisons:

* Keep V and replace f by its normalized projection onto the orthogonal complement of the success code. This costs exactly 2q sqrt(theta) in diamond norm. At theta=1 choose any orthogonal flag in the padded output, giving the same bound.
* Keep f and replace V by the polar isometry of (I-P_f)V. Its five unchanged singular directions need no rotation; the remaining principal angle has sine sqrt(theta). A polar completion at theta=1 uses the padded outside direction. Thus ||V-W||<=sqrt(2theta), and the reversible success channel changes by at most 2sqrt2 p sqrt(theta) in diamond norm, with reset unchanged.

Choose the smaller bound. It is at most 2sqrt2 min(p,q)sqrt(theta), which by (7) is at most48sqrt2 sqrt(Delta)<72sqrt(Delta). The p=0, q=0 and theta=0 endpoints are exact and need no division.

The ideal flag/code measurement can be applied to the ACTUAL channel. Diamond data processing gives the same bound for the joint heralded instrument, with ideal successful map p id3 after discarding the logical ancilla. If zeta denotes the error and p>zeta, each normalized successful output, including entangled inputs, is within 2zeta/p of the input. This is conditional state error with an explicit success denominator, not uniform recovery near reset. The code/flag constructions require access to the channel parameters, not an entropy measurement alone.

## 6. The square-root structure exponent is sharp

Take p=q=1/2 and the actual flag family

 f_theta=sqrt(theta)|0,0>+sqrt(1-theta)f_perp,

so lambda=1. The exact spectral formulas give

 Delta(E_theta)=(2/15)log(9/8)theta+O(theta^2).   (8)

Here ell(x,y)=(log x-log y)/(x-y)=integral_0^infinity ds/((s+x)(s+y)), with ell(x,x)=1/x; these arguments are eigenvalues, not trace/determinant coordinates. Differentiating at theta=0 gives c[ell(p/2,q/3)+3ell(p/6,q)-4ell(p/3,2q/3)], c=pq/18, which reduces to the coefficient in (8).

Every generalized-erasure Choi state F (even with arbitrary logical success eigenweights and arbitrary output isometry) commutes with I3 tensor its own reference marginal R_F. For the actual A_theta, between x=|physical1,reference0,logical0> and y=|physical1,f_perp>,

 <x|[A_theta,I3 tensor R_theta]|y>
 =-(pq/18)sqrt(theta(1-theta)).                 (9)

The main maximally entangled modes contribute zero to this entry; it comes from [q I3/3 tensor P_f,p I3 tensor P_success/6]. The two-coordinate compression gives commutator trace norm at least pq sqrt(theta(1-theta))/9. The elementary Lipschitz commutator bound used in the one-mode sharpness proof is at most4||A_theta-F||_1. Therefore

 ||A_theta-F||_1 >=(pq/36)sqrt(theta(1-theta)).   (10)

The same lower bound applies to channel diamond distance. Equations (8)-(10) exclude any structure-approximation exponent larger than1/2, even when the target is allowed an arbitrary mixed logical success state. The constant72 is not claimed optimal.

## Subsequent receiving

The flat-logical-rank extension is proved in `flat_logical_success_arbitrary_flag_uniform_theorem.md`, with the same dimension-free72sqrt(Delta) capability for every finite flat logical rank. The fully arbitrary logical spectrum is now received by `arbitrary_logical_success_reset_flag_value_theorem.md` through a different shared-resolvent compensation, with uniform280sqrt(Delta). The unequal-weight Schmidt-concavity failure remains valid; the new proof does not reuse that false premise.
