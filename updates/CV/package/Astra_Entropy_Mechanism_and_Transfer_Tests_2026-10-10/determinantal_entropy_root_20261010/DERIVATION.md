# Determinantal entropy mechanism: root derivation and local gate

10 October 2026. Proposed mechanism, not a global theorem or a novelty claim.

## Target and why it would suffice

For arbitrary independent pure one-mode inputs to a gain-G two-mode squeezer, let rho be one reduced output and tau the thermal state of mean G-1. Investigate det(I+t rho)>=det(I+t tau) for all t>=0. The known Gaussian-channel majorization theorem with vacuum idler does not automatically cover an arbitrary non-Gaussian pure idler.

For every density operator with finite entropy,

S(rho)=integral_0^infinity [log det(I+t rho)-log(1+t)]/t^2 dt.

Indeed for x in [0,1], log(1+tx)-x log(1+t)>=0 by concavity. Its integral divided by t^2 equals -x log x (integration by parts and elementary logarithmic integrals). Tonelli then applies to all eigenvalues. Consequently determinant dominance would imply the pure-product entropy bound. This is a sufficient spectral mechanism, not an assertion that the determinant order holds.

An even stronger sufficient gate is coefficientwise dominance of all elementary symmetric functions e_k(rho). At thermal ratio r=(G-1)/G,

e_k(tau)=G^(-k) r^(k(k-1)/2) / product_{j=1}^k(1-r^j).

At G=2, e_3(tau)=1/21. Since e_3=(1-3 Tr rho^2+2 Tr rho^3)/6, separate upper bounds on integer moments cannot establish this lower bound. The companion flat-rank-three example proves that all integer moment bounds alone are insufficient even for entropy.

## Exact gain-two local test

Take normalized inputs proportional to |0>+epsilon a|m> and |0>+epsilon b|m>, m>=1. Initially take a,b real; complex phases enter only as Re(ab) in the mixed term. The output bipartite amplitude matrix has expansion

D+epsilon(aL+bL^T)+epsilon^2[ab F-(a^2+b^2)D/2]+O(epsilon^3),

where D_n=2^(-(n+1)/2), L_{n+m,n}=sqrt(binomial(n+m,m))*2^(-(n+m+1)/2), and F is diagonal with

F_n=2^(-(n+m+1)/2) P_m(n),
P_m(n)=sum_{j=0}^{min(m,n)} (-1)^(m-j) binomial(m,j) binomial(n,j).

This follows directly from the two lowering/raising disentangling factors of the squeezing unitary; m=1 gives the previously checked (n-1) amplitude and output spectral hole.

Write rho=rho0+epsilon X+epsilon^2 Y. The coefficient of epsilon^2 in e_3 is

Tr[(rho0-I/2)X^2]+Tr[(rho0^2-rho0)Y].

Using sum_n binomial(n+m,m)x^n=(1-x)^(-m-1) and
sum_n P_m(n)x^n=(-1)^m(1-2x)^m/(1-x)^(m+1), it becomes

A_m (|a|^2+|b|^2)+2 C_m Re(ab),

A_m=[(4/7)^m+(2/7)^m+(1/7)^m]/7-[(2/3)^m+(1/3)^m]/3+4/21,
C_m=2^(-m/2) R_m,
R_m=[(4/7)^m+(2/7)^m+(-6/7)^m]/7-[(2/3)^m+(-2/3)^m]/3.

These formulas are a root derivation awaiting the independent finite-epsilon comparison, not a certified global result.

## Sign of the derived Hessian

At m=1, A=C=0 (displacement tangent directions). At m=2, A=88/1323 and C=-A (the common squeezing tangent is zero). At m=3, A=2372/21609 and R=-144/2401, with A^2-2^(-3)R^2>0 exactly.

For every m>=4,
A_m >= 4/21-[(2/3)^4+(1/3)^4]/3,
|C_m| <= (1/4){[(4/7)^4+(2/7)^4+(6/7)^4]/7+(2/3)(2/3)^4}.
The first rational number strictly exceeds the second, checked exactly by check_hessian.py. Monotonicity of the powers proves the bounds uniformly for all m>=4. Thus the derived quadratic form is positive away from the Gaussian tangent modes. Different excitation numbers have disjoint number-shift sectors in the second variation, so no mixed m!=n term survives the diagonal trace.

This passes a local consistency gate. It neither proves global e_3 minimization nor determinant order, and it gives no full arbitrary-mixed-input EPnI. A global channel-specific inequality remains the indispensable step. Numerical survival and local stability do not establish foundational significance or priority.

## Where a global e3 proof must act

For any density spectrum, Tr rho^3 >= (Tr rho^2)^2 by Jensen with probability weights equal to eigenvalues. Therefore e3 >= (1-3u+2u^2)/6, where u=Tr rho^2. At gain two the e3 thermal bound follows automatically for u<=(21-sqrt(161))/28. Only the remaining high-purity region needs channel structure (the two-pure-input purity ceiling is 1/3 via Lieb ambiguity norms and Holder).

In that region the exact missing inequality is Tr rho^3 >= (3/2) Tr rho^2 - 5/14. Quantitative near-Gaussian extremizer control is a possible source of leverage, but no explicit uniform estimate furnishing this inequality has been proved. Local Hessian positivity alone cannot cover all high-purity inputs. Known stability results for Hausdorff-Young/Young must not be silently assumed to have the necessary constants or to imply the specific channel inequality.

Independent finite-epsilon computations using the exact output amplitudes agree with the derived Hessian, including the Gaussian null directions. This is internal numerical corroboration, not external certification or a substitute for the derivation.
