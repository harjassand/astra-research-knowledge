# A stronger native acquisition theorem: collective stable rank

2026-10-10. This strengthens the minimum-singular-value envelope in CONTINUOUS_CONSTRAINT_AUDIT.md. It remains a mathematical sampler theorem built from classical Gaussian augmentation and rejection sampling; publication novelty is unestablished. The last section closes a finite-output, controlled-accuracy scope for the homogeneous zero-target case.

## 1. Raw-input resource

Let A_1,...,A_m be rational p-by-n matrices, linearly independent in Frobenius inner product. Define

    H_ij = tr(A_i A_j^T),      s(lambda)=lambda^T H lambda=||A_lambda||_F^2.

Assume an integer r>m has been certified such that

    ||A_lambda||_op^2 <= s(lambda)/r   for every lambda.    (SR)

Thus every nonzero combination has stable rank at least r. No minimum singular value, common right inverse, exact radial determinant, or rank-metric coordinate system is assumed.

### Native certificate, without irrational whitening

Compute H and its rational inverse exactly, then

    M_p = sum_ij (H^(-1))_ij A_i A_j^T,
    M_n = sum_ij (H^(-1))_ij A_i^T A_j.

Either rational PSD inequality

    M_p <= I_p/r,                 M_n <= I_n/r             (C)

suffices. Test it by exact rational PSD/LDL methods. One may select the largest successful integer r by monotone binary search over 1,...,min(p,n). Matrix dimensions, rational bit lengths, and every test are charged. This is a polynomial-time sufficient certifier, not a complete recognizer of all spaces satisfying (SR).

Proof: in a conceptual Frobenius-orthonormal basis B_i of the matrix span, Cauchy-Schwarz gives

    ||sum_i u_i B_i v||^2 <= ||u||^2 sum_i ||B_i v||^2
                         <= ||u||^2 ||sum_i B_i^T B_i||_op ||v||^2.

The transposed argument gives the other certificate. The two sums are exactly M_n and M_p; no irrational basis needs to be constructed for verification.

An alternative sufficient certificate is PSD of the block matrix

    (H tensor I_p)/r - [A_i A_j^T]_(i,j).

It is also rational and exact. Evaluating its quadratic form at lambda tensor v proves (SR).

## 2. The spectral-envelope lemma

Let u_j be the nonnegative eigenvalues of A_lambda A_lambda^T. Their sum is s and their maximum is at most s/r. Concavity of log(1+u), on [0,s/r], yields

    log(1+u_j) >= (r u_j/s) log(1+s/r).

Summing, and also using log(1+u)<=u, gives

    r log(1+s/r) <= log det(I+A_lambda A_lambda^T) <= s.

Consequently the homogeneous positive dual density obeys

    exp(-s/2) <= v(lambda)=det(I+A_lambda A_lambda^T)^(-1/2)
                   <= h_r(lambda)=(1+s/r)^(-r/2).          (12)

Unlike a minimum-singular-value envelope, this accommodates angularly varying singular spectra and singular combinations; it requires their mass to be sufficiently spread.

The envelope is natively samplable:

    Z ~ N(0,I_m), V ~ chi-square_(r-m),
    lambda = sqrt(r) H^(-1/2) Z/sqrt(V).                   (13)

Only an ordinary m-by-m Gaussian covariance factorization is needed. Since r is an integer, V is the sum of r-m independent squared standard Gaussians.

## 3. Independent exact sampling and its acceptance

Use (13), accept with probability v/h_r, draw

    X | lambda ~ N(0,(I+A_lambda A_lambda^T)^(-1)),

then draw Y as the Gaussian projected onto ker F(X). This outputs the Gaussian residual-conditioned law F(X)Y=0 from the main audit. Independent trials give independent outputs.

The exact envelope integral is

    B_r = pi^(m/2) r^(m/2) det(H)^(-1/2)
          Gamma((r-m)/2)/Gamma(r/2).

Integrating the lower Gaussian in (12) proves the explicit success bound

    P(success) >= a_(r,m)
      := (2/r)^(m/2) Gamma(r/2)/Gamma((r-m)/2).             (14)

For m=2k,

    a_(r,m) = product_(j=1)^k (1-2j/r)
            >= 1 - m(m+2)/(4r).                          (15)

Thus r=Omega(m^2) suffices for a dimension-independent number of independent trials. The bound depends on r, not on a hidden normalizing constant. Per-trial work is polynomial matrix formation/factorization plus ordinary normal generation.

For odd m, (14) still applies. If M=2 ceil(m/2)<r, a_(r,m)>=a_(r,M): writing the reciprocal as E[(r/V_0)^(m/2)] with V_0~chi-square_r, Lyapunov's moment inequality and Jensen show that it is nondecreasing in m. Hence the next-even bound is valid.

### Affine offsets and nonlinear targets

For the affine density v_c(lambda) in the main audit, let D_ij=c_i^T c_j. Since the affine exponent is between -||c_lambda||^2/2 and 0,

    exp[-lambda^T(H+D)lambda/2] <= v_c(lambda) <= h_r(lambda).

Therefore a lower success bound before the nonlinear correction is

    a_(r,m) sqrt[det H / det(H+D)].                        (16)

If g(x)=F(x)h(x) with a verified ||h(x)||^2<=beta, the final nonlinear correction costs at most exp(beta/2) expected trials. More generally it suffices to verify g^T(FF^T)^(-1)g<=beta. Merely giving an arbitrary target circuit does not verify this condition.

These formulas explicitly separate a natively acquired matrix-space resource, affine displacement cost, and nonlinear likelihood cost.

## 4. Growing examples that are not radial Wishart cases

Take m Frobenius-orthogonal N-by-N real signed orthogonal matrices P_i. For example, select distinct real Pauli/Weyl matrices, tensor products of I, X, Z, XZ, where

    X=[[0,1],[1,0]],        Z=[[1,0],[0,-1]].

Put A_i=P_i. Direct exact checks give

    H=N I_m,
    M_p=M_n=(m/N) I_N.

Thus the raw-input certificate returns every integer r<=N/m. With N=Omega(m^3), (14)-(15) imply constant acceptance while m and both variable dimensions grow. This is a resource-rich regime; it is not arbitrary dense constraint solving.

The matrices need not commute or form an orthogonal design. For N=64, choose

    P_1=I, P_2=X on the first tensor bit,
    P_3=Z on the first bit, P_4=X on the second bit.

The first-bit X and Z do not commute. At two dual vectors with equal squared norm,

    lambda=(1,0,0,0):      det(I+A_lambda A_lambda^T)=2^64,
    lambda=(3/5,4/5,0,0):  det(I+A_lambda A_lambda^T)=(1924/625)^32.

These determinants differ, so the dual law is angularly nonradial. For lambda=(1,1,0,0), A_lambda has rank 32; no full-rank-orthogonal-design identity is present. The certificate r=16 nevertheless gives exact lower acceptance 21/32. This N=64 example verifies the ideal-envelope theorem only: r=16 does not satisfy the finite-output theorem's sufficient r>=4(m+1)^2=100. For the same four matrices repeated across extra tensor bits, N=512 gives r=128, meets that theorem, and has exact success lower bound 1953/2048. The multiprecision sampler itself has not been implemented or benchmarked.

Common orthogonal transformations A_i -> U A_i V^T preserve H and conjugate M_p,M_n. Dense rational Householder U,V therefore produce dense coefficient matrices with the same natively recovered certificate. The acquisition does not need to recover those transformations.

verify_stable_rank.py and STABLE_RANK_EXACT_CHECKS.json verify the Gram matrices, native certificate, noncommutation, singular combination, nonradial determinant, rational squared acceptance, and exact lower bounds using integer/rational arithmetic.

These are examples of the theorem, not a claim that the matrices or their operator inequalities are new. A targeted source search found Gaussian determinant-cancellation MCMC and the classical Wishart, coarea and Gaussian-conditioning ingredients, but no precise antecedent for (12)-(16). Failure to locate one is not publication-novelty evidence.

## 5. Closure under subspace restrictions has an explicit charge

Let P,Q have orthonormal columns and delete a,b dimensions respectively. For A'_lambda=P^T A_lambda Q, put d=a+b. The deleted row and column energies satisfy

    ||A'_lambda||_F^2 >= ||A_lambda||_F^2 - d ||A_lambda||_op^2
                      >= (1-d/r)||A_lambda||_F^2,
    ||A'_lambda||_op^2 <= ||A_lambda||_op^2.

Hence, if d<r,

    ||A'_lambda||_op^2 <= ||A'_lambda||_F^2/(r-d).          (17)

The reciprocal stable-rank budget loses at most a+b. Full Gaussian conditioning onto homogeneous subspaces has the correct standard Gaussian prior in orthonormal coordinates, so the sampler's structural family is preserved. To retain constant acceptance require the residual r-d still be Omega(m^2).

Affine restriction adds explicit offsets. Nonlinear graph restriction Dy=h(x) changes both the residual target and the Gaussian prior by exp(-||D^+h(x)||^2/2), even when D has orthonormal rows. Neither that factor nor the new target energy is automatically free. Arbitrary variable identification can also destroy the one-sided affine structure. No unrestricted closure theorem is asserted.

## 6. Inverse-determinant moments: a precision-control resource

For an integer k>=1 with r>km, introduce k copies of the positive dual. Their combined precision matrix is

    I + sum_(ell=1)^k A_(lambda_ell) A_(lambda_ell)^T.

Its nonidentity part has trace S=sum_ell lambda_ell^T H lambda_ell and operator norm at most S/r. The same envelope in dimension km yields

    E_X det(F(X)F(X)^T)^(-k/2)
       <= det(H)^(-k/2) C_(r,km),
    C_(r,d)=(r/2)^(d/2) Gamma((r-d)/2)/Gamma(r/2).          (18)

For k=2,

    C_(r,2m)=product_(j=1)^m (1-2j/r)^(-1).               (19)

Let pi_0 be the tilted x law. Since its normalizer is at least det H^(-1/2), its density versus the standard Gaussian has squared L2 norm at most C_(r,2m). Therefore, for every measurable event E,

    pi_0(E) <= sqrt[C_(r,2m) P_Gaussian(E)].               (20)

This transfers small-probability conditioning failures under the prior to the actual sampled x law. It avoids an unspecified nonzero-minor oracle.

## 7. A finite-output controlled-accuracy theorem (homogeneous zero target)

### Scope and metric

Assume rational homogeneous inputs, g=c=0, a native certificate M_p<=I/r, and

    r >= 4(m+1)^2.

Given rational 0<epsilon<1, there is a finite-random-bit algorithm outputting rational (x_hat,y_hat) such that

    W_1(Law(x_hat,y_hat), pi_0_joint) <= epsilon,
    ||F(x_hat)y_hat|| <= epsilon                         (21)

(the latter can be enforced for every output). Its running time and number of random bits are polynomial in total rational input bit length, dimensions, and log(1/epsilon), using ordinary multiprecision arithmetic. This is a controlled finite approximation, not exact finite-bit equality conditioning or total variation to a continuous law.

The transpose-only certificate gives the same conclusion by swapping x and y in this homogeneous zero-target case. This section does not claim the same bit theorem for arbitrary computable nonlinear targets; a quantitative evaluation/modulus-of-continuity assumption would be needed.

### Explicit ingredients of the construction and proof

1. **Constant ideal success and finite moments.** Equations (14)-(15), with the next-even bound, give success at least 1/2. Equation (19) and -log(1-u)<=u/(1-u) give

       C_(r,2m) <= exp[m(m+1)/(r-2m)] < 2.

   Under the exact target, conditional Gaussian covariance domination gives

       E||X||^2 <= p,    E||Y||^2 <= n.                    (22)

   The accepted dual variable is followed by X|lambda with covariance at most I, so its mixture has the first bound directly. The second inequality uses Y=P_ker Z with fresh standard Gaussian Z. The L2 estimate remains needed for the singular-value event, not for these moments.

2. **A native small-singular-value bound.** Put F_bar=H^(-1/2)F. For each fixed unit u, Q=||F_bar(X)^T u||^2 is a weighted chi-square with mean 1 and every weight at most 1/r. The Chernoff bound, with t=r(1/a-1)/2, is

       P(Q<=a) <= [a exp(1-a)]^(r/2),   0<a<1.           (23)

   Also ||F_bar(x)||_op<=||x||/sqrt r follows from M_p<=I/r. On ||X||<=L, cover the unit sphere by a sqrt(t)/(2L/sqrt r)-net. If sigma_min(F_bar)^2<=t, some net point has Q<=(9/4)t. For 0<t<=min(4/9,L^2/r),

       P[sigma_min(F_bar)^2<=t, ||X||<=L]
         <= (5L/sqrt r)^m (9e/4)^(r/2) t^((r-m)/2).       (24)

   Equation (20) bounds the tilted probability by the square root of twice the right-hand side of (24). Choose t so the Gaussian right-hand side is at most (eta/T)^2/2; then the tilted probability is at most eta/T. In particular, selecting t=2^(-q) to meet this requirement needs

       q=O(r + m log(1+L) + log(T/eta)),                  (25)

   with a larger universal constant if necessary. Thus the required lower-singular-value cutoff has only polynomially many bits. If a larger q is chosen, validity is preserved.

3. **Cap trials and truncate primitive seeds.** Set T=ceil(log_2(1/eta)); the ideal probability of failing to accept by T is at most eta. There are at most T(m+r+p+n) normal seeds and T acceptance uniforms. Choose a normal cutoff L_0 with 2 T(m+r+p+n)exp(-L_0^2/2)<=eta. In (13), V contains at least one squared normal, so

       P(V<v_0) <= P(|Z_1|<sqrt(v_0)) <= sqrt(2/pi) sqrt(v_0).

   Choose a dyadic v_0<=eta^2/(4T^2), making all small-V events together at most eta. These cutoffs have polynomial bit length. On their complement, lambda is bounded by an explicit product of ||H^(-1/2)||, sqrt(rm), L_0 and v_0^(-1/2). Each candidate x has norm at most sqrt(p)L_0 because its precision is at least I. This supplies L in (24). Union bounds over T accepted candidates charge the small-singular-value events using (24), with the desired eta/T budget.

4. **Rational input supplies spectral height bounds.** Positive definiteness of the rational Gram matrix H and elementary determinant/entry bounds give

       2^(-poly(input bit length)) <= lambda_min(H)
         <= lambda_max(H) <= 2^(poly(input bit length)).

   These bounds can also be explicitly computed from det H and an entry-norm upper bound. On the good event from (24),

       lambda_min(FF^T) >= lambda_min(H) t.

   All linear solves, LDL/Cholesky factors, square roots and projection operations used by the ideal sampler are therefore evaluated on bounded arguments a polynomial number of bits away from their singularities. Their derivatives and ordinary numerical error-amplification factors are bounded by 2^(poly(input length, dimensions, log(1/eta))). Standard interval arithmetic with that many guard bits certifies any specified exponentially small absolute error. Cholesky of I+A_lambda A_lambda^T has no small eigenvalue; only the final fiber projection requires (24).

   For the integer-r homogeneous zero-target sampler there is a useful exact simplification. At a rational approximate dual vector, the squared acceptance probability is

       a(lambda)^2=(1+s(lambda)/r)^r / det(I+A_lambda A_lambda^T).

   This is rational and lies in [0,1]. It can be computed and compared with the square of a dyadic uniform exactly. There is no need for a potentially cancellation-prone log-determinant/exponential evaluation. Powers and determinants have polynomial bit length because r is at most the input matrix dimensions. Since |sqrt(u)-sqrt(v)|<=sqrt(|u-v|) on [0,1], an O(zeta^2) perturbation bound on the rational squared ratio suffices for O(zeta) error in acceptance probability.

5. **Couple finite seeds and acceptance decisions.** Generate normal seeds from uniformly random dyadic intervals and evaluate the inverse normal CDF to certified precision, discarding endpoint-tail intervals already charged above. On the truncated interval the inverse derivative is explicitly bounded; normal CDF evaluation on a bounded interval uses the convergent exponential/erf series with polynomially many terms and bisection. Square roots likewise admit polynomial-time precision algorithms on the bounded domains in step 4. Thus the finite seeds can be coupled to exact Gaussian seeds with arbitrarily small, explicitly bounded coordinate error using polynomially many bits.

   Evaluate each acceptance probability and uniform to absolute error at most zeta. Away from a 2zeta interval around the ideal threshold the decision agrees. Conditionally on all other ideal variables, the independent acceptance uniform falls in that interval with probability at most 4zeta. Taking zeta<=eta/(4T) adds at most eta to the disagreement probability. Arithmetic precision also controls propagation of the seed errors into those probabilities, using step 4. Use separated cutoffs rather than asserting that their boundaries have small probability: analyze the good seed event |Z|<=L_0 while the implementation permits 2L_0; analyze V>=v_0 while it permits v_0/2; and analyze the ideal S(x)>=4tH while the implementation checks S(x_hat)>=2tH by an exact rational PSD/LDL test. Choose the x approximation finely enough that ||H^(-1/2)[S(x_hat)-S(x)]H^(-1/2)||_op<=t on the analyzed good event. The ideal 4t margin then implies the rational check passes with at least a t margin. Apply (24) with 4t when allocating its bad-event budget. With sufficiently small certified numerical error, every analyzed good event passes the corresponding implementation check. If a check cannot be certified it may safely fall back, and that event is contained in the already charged larger bad set. This removes any unproved cutoff-boundary probability assumption.

6. **Output clipping, fallback and Wasserstein control.** If the cap or a certified cutoff fails, output (0,0). Otherwise round the computed pair to rational coordinates within a prescribed small Euclidean error and clip to an explicit ball of radius R_out=O(sqrt(p+n)L_0+1). Independently check the rational residual ||F(x_hat)y_hat||^2<=epsilon^2. If it fails, output (0,0), which exactly satisfies the homogeneous target. On the good coupling event, choose the rounding error small enough using the known coefficient norm and R_out that the residual check passes and the Euclidean output error is at most epsilon/2.

   Let eta_total be the sum of the finitely many bad-event bounds, at most a universal constant times eta after the preceding allocations. By (22), the expected coupling distance on the bad event is at most

       sqrt[(p+n) eta_total] + R_out eta_total.

   Select eta by successive dyadic halving until this explicit quantity is at most epsilon/2. Because T and L_0 grow only logarithmically in 1/eta, the required log(1/eta) is polynomial in the stated input parameters. This proves (21). There is no unknown density normalizer or mixing-time parameter in the choice.

The construction is deliberately conservative and not an optimized implementation. The supplied scripts verify the algebraic examples, not this full multiprecision sampler. The theorem establishes existence and a charged finite-precision route in the stated homogeneous scope; implementation quality and practical speed remain untested.

## 8. What this changes, and what it does not

The stable-rank theorem genuinely improves acquisition beyond the exposed Wishart/orthogonal-design cases and beyond the earlier minimum-singular-value certificate. Its raw-input verifier is invariant under common orthogonal coordinate changes, and it applies to dense noncommuting matrix spans. The finite-output theorem avoids an ideal-real-only claim in a carefully bounded homogeneous scope.

It is still a resource-conditioned sampler, with a strong collective stable-rank surplus relative to the number of constraints. General nonlinear composition, arbitrary target energies, generic surface-area sampling, and unrestricted matrix spaces are not solved. The Gaussian identity, the auxiliary determinant cancellation, Student-t generation and rejection mechanism are classical; the exact scope/antecedents of the combined acquisition and precision theorem need broader literature and independent proof review before any novelty claim.

## Primary-source context

See the fuller source audit in CONTINUOUS_CONSTRAINT_AUDIT.md. Key checked antecedents are [Ellam et al., determinant-free Gaussian-field MCMC](https://arxiv.org/abs/1709.03312), [Hubbard, Gaussian auxiliary-field transformations](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.3.77), [Diaconis–Holmes–Shahshahani, manifold conditioning](https://arxiv.org/abs/1206.6913), [Zappa–Holmes-Cerfon–Goodman, manifold MCMC](https://arxiv.org/abs/1702.08446), and [Sawyer, Wishart density and sampling](https://www.math.wustl.edu/~sawyer/hmhandouts/Wishart.pdf). These establish the classical ingredients. The targeted searches do not settle historical novelty of the combined stable-rank acquisition theorem.
