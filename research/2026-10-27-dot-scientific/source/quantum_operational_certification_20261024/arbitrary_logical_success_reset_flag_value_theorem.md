# Arbitrary logical spectrum: reversible success plus an overlapping reset flag

## Theorem

Let sigma be any finite-dimensional density matrix, V:C3 tensor supp(sigma)->R an isometry, f any unit output vector, and p,q>=0 with p+q=1. Then the actual TP channel

 E(rho)=p V(rho tensor sigma)V*+qTr(rho)|f><f|

has nonnegative normalized-Choi WH3 deficit. Its deficit is zero exactly when p=0, q=0, or f is orthogonal to the ACTUAL success support V(C3 tensor supp(sigma)).

Zero logical eigenvalues must be removed before defining that support: overlap with a formally present but unused logical mode does not make the deficit positive. This theorem includes all nonflat logical spectra and arbitrary coherent flag orientations. It is not the unrestricted two-arbitrary-Kraus-mode theorem: the successful part is required to be REVERSIBLE with a fixed ancillary state sigma.

The proof is an actual shared-resolvent compensation, not concavity in sigma or in Schmidt allocation. Both of those tempting concavities have explicit failures in this family.

## 1. Actual normalized source and supported flag matrix

Apply the output isometry and, if needed, add one orthogonal output direction. In these coordinates the normalized Choi source is

 A=p Phi_(A,R0) tensor sigma_L+q(I_A/3) tensor P_f.

Choose an orthonormal logical eigenbasis of sigma before defining coefficient matrices; sigma is diagonal in all formulas below. This is a basis choice, not a commutation assumption on the flag. Let G be the 3-by-k coefficient matrix of the component of f in the actual success space C3 tensor supp(sigma). Thus ||G||F^2=theta<=1. The outside component has norm sqrt(1-theta). Complex conjugations may enter the INPUT Gram compression, but they leave its determinant equal to the one below. The OUTPUT compression in the fixed antisymmetric frame is exactly (T I3-K)/2.

For t>0 define

 K(t)=G[sigma/(t+sigma)]G*, T(t)=TrK(t).

These are actual source-linked matrices, not arbitrary resolvent variables. They satisfy K>=0 and 0<=T<=1/(1+t), since sigma<=I and ||G||F^2<=1.

The comparison source with the same p,sigma and an orthogonal reset flag has deficit zero exactly, for arbitrary logical rank. Its input, reference and output entropy differences from A are captured by the finite-rank determinant ratios below.

## 2. Common resolvent parameter and exact entropy identity

Assume p,q>0 and put r=q/p, z=t/r. Define

 alpha=1/[2(z+1)], beta=1/[3(3z+1)], gamma=3/(z+3).

In the INPUT determinant integral rescale its spectral variable as s=pt. The actual-to-orthogonal-flag determinant ratio is

 det(I3-beta K(t)).

This follows by a Gram Schur complement of the reset projection: its overlap with the main maxent code is the conjugated G*G/3, and the reset weight is q/3.

In the REFERENCE integral use s=pt/3. Its rank-one determinant ratio is

 1-gamma T(t).

In the UNSCALED OUTPUT L=2N(A) integral use s=2pt/3. The antisymmetric main overlap with the flag is (T I3-K)/2, and the reset weight is2q/3. Its determinant ratio is

 det(I3-alpha(T I3-K)).

The individual compared matrices have equal traces; the affine trace subtractions in the trace-entropy integral therefore cancel. Keeping all three change-of-variable factors gives the exact identity

 Delta(A)=(p/3) integral_0^infinity F(K(t),z) dt,             (1)

 F=2 sum_(i=1)^3 log[1-alpha(T-k_i)]
   -3 sum_(i=1)^3 log(1-beta k_i)-log(1-gamma T),             (2)

where k_i are the eigenvalues of K and sum k_i=T. This agrees with the earlier flat-logical principal-angle formulas but requires neither scalar sigma nor simultaneous diagonalization of sigma and G*G.

The integral is well defined at singular flag orientations. At small t, only the reference logarithm can be unbounded; 1-gamma T>=t/(1+t), so its magnitude is at most log(1+1/t). At infinity K=O(1/t), the linear coefficient below is O(1/z), and all nonlinear terms are O(1/t^4); the total integrand is O(1/t^2). Thus (1) is an ordinary convergent improper integral.

## 3. All nonlinear logarithmic orders are nonnegative

For t>0 all logarithmic arguments are positive. Expanding (2), the order-n coefficient is

 [gamma^n T^n+3beta^n sum_i k_i^n
       -2alpha^n sum_i(T-k_i)^n]/n.

For every n>=2,

 sum_i(T-k_i)^n<=2T^n,
 gamma>=2alpha,
 gamma^n>=4alpha^n.

The first inequality follows by dividing by T and using (1-x)^n<=1-x for x in[0,1], with the T=0 case immediate. Hence every order n>=2 is nonnegative. In particular their sum retains the explicit resource

 F-h(z)T >=(3/2)beta^2 Tr(K^2)>=0,             (3)

where the exact linear coefficient is

 h(z)=gamma+3beta-4alpha
     =4z(z-1)/[(z+3)(3z+1)(z+1)].              (4)

There is no pointwise assertion h>=0; its negative small-resolvent part must be paid by the actual Stieltjes form of T.

## 4. Exact signed-measure compensation of the linear term

The measure h(z)dz/z is negative on(0,1), positive on(1,infinity), and has ZERO total mass:

 integral_0^infinity h(z)dz/z=0.

An exact primitive is

 2log(z+1)-log(z+3)-log(z+1/3),

whose limits at zero and infinity both vanish.

Diagonalize sigma, with positive eigenvalues s_j and nonnegative weights w_j=||G e_j||^2. Then

 T(t)=sum_j w_j s_j/(t+s_j).

For each s_j>0, the multiplier m_j(t)=t s_j/(t+s_j) is strictly increasing. Relative to the signed zero-mass measure h(t/r)dt/t, subtract the constant m_j(r). The product is nonnegative on BOTH sides of r. Therefore

 integral_0^infinity h(t/r) s_j/(t+s_j)dt>=0,                (5)

strictly positive for s_j>0. Summing with weights w_j proves nonnegativity of the integrated linear term. All quantities are integrable, so no unjustified exchange of a divergent signed series is used: subtract the finite linear term first, then apply monotone convergence to the nonnegative nonlinear coefficients.

Equations (1), (3), and (5) prove Delta>=0. If G!=0 on the supported logical space, at least one w_j>0 and the linear integral is strictly positive. Conversely G=0 gives K=0 and exact zero. The p=0 and q=0 cases are respectively reset and reversible encoding, both exact zero. This proves the stated complete equality classification.

## 5. An explicit retained spectral payment

The linear resource can also be evaluated without an integral. Define, by continuous divided differences at x=1/3,1,3,

 J(x)=3 log(x/3)/(x-3)
      +(1/3)log(3x)/(x-1/3)-2log(x)/(x-1), x>0.

The signed-measure proof gives J(x)>0. Direct scalar integration yields

 integral h(t/r) s/(t+s)dt=s J(s/r).

Consequently the actual source satisfies

 Delta(A)>=(p/3)sum_j w_j s_j J(p s_j/q)
             +(p/2)integral beta(t/r)^2 Tr(K(t)^2)dt.       (6)

These resources retain the logical spectrum and flag overlap. They do not by themselves constitute a channel-distance modulus. Section 6 supplies the separate actual mixed-ancilla rotation and adaptive-flag comparison; no inverse-eigenvalue conversion is assumed.

## Scope and provenance

This proof receives the parent's exact shared-resolvent candidate with independent source-factor checking. It extends the audited all-FLAT logical-rank theorem to arbitrary logical spectrum at the VALUE and exact-zero levels. The flat theorem's sharper constant72 remains valid at its own scope. The spectrum-uniform nonflat operational modulus is supplied by the separate metric receiver in Sections 6-7 below. The unrestricted entropy conjecture and arbitrary two Kraus operators with a common reset flag remain open.

## 6. Dimension-free quantitative generalized-erasure reconstruction

The retained linear payment in fact gives a spectrum-independent operational modulus. There is a generalized-erasure channel with the SAME p and the SAME ancillary state sigma such that

 ||E-E_hat||_diamond<=min(2,280sqrt(Delta(E))).   (7)

The constant is independent of logical rank, its smallest eigenvalue, and output dimension. Use one fixed output isometric padding to dimension at least3 rank(sigma)+1 if necessary. The construction is explicit and deterministic.

### 6.1 A paid adaptive overlap

For s>0 put x=s/r, r=q/p. Subtracting the linear signed-measure multiplier's value at z=1 gives the exact nonnegative representation

 integral_0^infinity h(t/r)s/(t+s)dt
 =r x^2/(1+x) integral_0^infinity
   4(z-1)^2/[(z+3)(3z+1)(z+1)(z+x)] dz.

On z in[2,3], the numerator is at least4 and the denominator is at most720(1+x). Therefore

 integral h(t/r)s/(t+s)dt >=r x^2/[180(1+x)^2].

In the sigma eigenbasis define

 e^2=sum_j ||G e_j||^2 [p s_j/(q+p s_j)]^2.

Equation (1) and the nonnegative nonlinear resource imply

 Delta(E)>=q e^2/540.                           (8)

No inverse eigenvalue or entropy-whitening operation is involved.

### 6.2 Mixed-ancilla rank-one code-rotation estimate

Let h be any unit output vector, theta_h its success-code overlap, and g its normalized projected domain vector when theta_h>0. Let W be the polar isometry of (I-P_h)V, completed using the padded outside direction when theta_h=1. Then D=W-V has rank one,

 D=|d><g|, ||d||^2=2(1-sqrt(1-theta_h))<=2theta_h.

For an arbitrary pure input entangled with a reference R of dimension at most three, write rho=|psi><psi|_(R,A) tensor sigma. The operator (I_R tensor D)rho has rank at most three, and

 ||(I_R tensor D)rho||_2^2
 =||d||^2 Tr[(rho_A tensor sigma^2)P_g]
 <=2 Tr[sigma^2 rho_h],

where rho_h is the unnormalized logical reduced matrix of the projected h. The last inequality uses rho_A<=I and incorporates theta_h into rho_h. Hence the rank bound gives trace norm at most sqrt6 sqrt(Tr sigma^2 rho_h). The exact telescoping identity

 W rho W*-V rho V*=D rho W*+V rho D*

gives the actual reversible-success channel bound

 ||V(. tensor sigma)V*-W(. tensor sigma)W*||_diamond
 <=2sqrt6 sqrt(Tr sigma^2 rho_h).               (9)

The bound is dimension-free because the reference rank is the INPUT dimension three, not the logical rank. It is not a pure-ancilla substitution or a free exposure of Kraus labels.

### 6.3 Adaptive flag and actual comparison channel

For p,q>0 form the UNNORMALIZED output vector

 h_raw=f_out+V vec[G diag(q/(q+p s_j))],

where the coefficient notation means filtering the logical columns of the projected flag matrix G. Then ||f-h_raw||=e.

If ||h_raw||>=1/2, normalize h_hat=h_raw/||h_raw||. The reset pure-state trace distance is at most2e: the sine of the angle between f and span(h_raw) is bounded by the norm of the particular residual f-h_raw. Thus changing the reset flag costs at most2q e.

Rotate the success code away from h_hat as in (9). Its weighted logical mass satisfies EXACTLY

 Tr[sigma^2 rho_(h_hat)]
 =(q/p)^2 e^2/||h_raw||^2.

The success-channel cost is consequently at most4sqrt6 q e. The final channel has success isometry W, ancillary sigma, and reset flag h_hat orthogonal to ran W. The total comparison cost is at most(2+4sqrt6)q e.

If ||h_raw||<1/2, then e>1/2 by the triangle inequality. Instead keep V and move the original reset flag to any unit vector outside its code. This costs at most2q<=4q e and is also covered by the same common bound.

Using (8) and q<=1, the total cost is at most

 (2+4sqrt6)sqrt540 sqrt(Delta)<280sqrt(Delta).

For an elementary numerical bound, sqrt6<49/20 and sqrt540<93/4 give the coefficient less than5487/20<275<280. The p=0, q=0 and zero-overlap endpoints are exact, without divisions. The universal channel distance bound two supplies the cap in (7).

## 7. Actual heralded access, sharpness, and remaining frontier

The final orthogonal code/flag measurement and logical-ancilla discard can be applied to the ORIGINAL channel. Diamond data processing gives the same error zeta=min(2,280sqrt(Delta)) for its joint heralded instrument. Its successful CP map differs from p id3 by at most zeta, including arbitrary entangled inputs. If p>zeta, normalized successful outputs have statewise trace error at most2zeta/p. No uniform conditional recovery is claimed near reset, and no proof path or adaptive filter is claimed to be a physical preprocessing of an unknown channel. The construction requires source/channel parameter access.

The flat k=2 example already gives a generalized-erasure distance lower bound of order sqrt(Delta), even when the target logical spectrum is unrestricted. Thus the exponent in (7) is sharp; no optimal constant is asserted.

The resulting whole class is reversible success with an INPUT-INDEPENDENT reset probability q. It is broader in logical spectrum/rank than the flat theorem but does not contain arbitrary K0,K1 or arbitrary nonscalar reset effect F. That nonreversible-success / input-dependent-failure class, and the unrestricted WH3 entropy problem, remain open.
