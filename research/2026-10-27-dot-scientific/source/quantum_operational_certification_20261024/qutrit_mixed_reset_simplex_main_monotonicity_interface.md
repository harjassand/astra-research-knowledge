# Qutrit mixed reset: exact simplex and main-weight derivative interface

Research interface, not a positivity theorem. Prior notes inspected include white_product_noise_matrix_stieltjes_receiver.md, product_noise_low_rank_value_compression.md and rank_one_main_arbitrary_bath_entropy_theorem.md. The latter is a different balanced source family and does not directly receive this channel.

For E(rho)=p rho+q Tr(rho)tau, matched covariance diagonalizes tau. Put a=p/3, b_i=q tau_i/3 and use homogeneous deficit, allowing a,b_i>=0 independently. If f(M)=Tr M logM and J_m is the all-ones m-by-m matrix, exact physical spectral cancellation gives

 D(a,b)=f(diag(b)+a J3)+3 sum_i f(b_i+a/3)
        -2 sum_(i<j) f(diag(b_i,b_j)+(a/2)J2).             (1)

This is exactly the actual WH3 deficit, with all normalization constants canceled. The source has the displayed3x3 block and two copies of every b_i; the output has the displayed three2x2 blocks and one copy of every b_i; its reference eigenvalues are a+3b_i. These facts prove(1), including continuous singular endpoints.

## Candidate main-weight monotonicity

D(0,b)=0. For positive b_i,

 partial_a D=<1|log(diag(b)+aJ3)|1>+sum_i log(b_i+a/3)
             -sum_(i<j)<1|log(diag(b_i,b_j)+(a/2)J2)|1>.  (2)

A proof that(2)>=0 for every a,b would prove the entire requested simplex class without twirl monotonicity or noise concavity.1000 bounded log-scale tests found no failure, but this is NOT a theorem. The exact direct physical/source derivation is the useful object.

Let x_i(s)=1/(s+b_i), S=sum_i x_i, S_ij=x_i+x_j. Sherman–Morrison gives an alternative exact integrated representation

 partial_a D=a integral_0^infinity [S^2/(1+aS)
       +(1/3)sum_i x_i^2/(1+a x_i/3)
       -(1/2)sum_(i<j) S_ij^2/(1+a S_ij/2)]ds.           (3)

Its integrand is NOT pointwise nonnegative. At x_i=x, the bracket divided by x^2 is9/(1+3ax)+1/(1+ax/3)-6/(1+ax), which is negative for ax=10. A separate success-baseline-canceling rescaling of source/output/reference integration variables also has both signs. These failures exclude the simplest pointwise payment, not integrated monotonicity.

## White-noise stationary reduction candidate

The existing exact white-product formula has

 D(a,b)=integral_0^infinity F(m_1(s),m_2(s),m_3(s))ds,
 m_i(s)=a/(s+b_i),
 F=2 sum_i log(1+(g-m_i)/2)-log(1+g)-3sum_i log(1+m_i/3),
 g=sum_i m_i.

Adding common noise b_i->b_i+t shifts the integral lower endpoint, so

 d/dt D(a,b+t1)=-F(m(t)).                                (4)

If F(m(s)) could be proved to have at most one sign change, from negative to positive, then no interior common-noise minimum would occur. This would reduce full-rank noise to the rank<=2 boundary or the zero limit at infinite common noise. The boundary would STILL require receiving; no whole theorem is asserted by this reduction alone.

For a=6, expF-1 has positive denominator and numerator

 H(s)=product_(i<j)[(s+b_i)(s+b_j)+3(2s+b_i+b_j)]^2
   -[product_i(s+b_i)+6 sum_(i<j)(s+b_i)(s+b_j)]
      *product_i(s+b_i+2)^3.                              (5)

Leading powers12 and11 cancel; H has degree10. Its highest four coefficients are polynomials in b_i with nonnegative coefficients. The lower coefficients have both signs. A bounded5000-case coefficient diagnostic found at most one Descartes sign variation, but no universal certificate has been established. Ordered-noise substitution b=(x,x+y,x+y+z) does NOT make all relevant coefficients nonnegative. The root geometry is generally complex, so real-rootedness is also unavailable.

The positivity question and the monotonicity candidate remain genuinely unresolved here. Numerical evidence must not be promoted to the missing integrated sign argument.
