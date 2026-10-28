# A support-aware rational completion for a fixed decoder effect

28 October 2026. Author lemma, independent receiving pending. This is a finite exact-CPTP repair for the fixed-effect optimization route, not a globally moving-effect optimization theorem. It uses only known rational matrices and approximation bits, never an unknown source support or free whitening oracle.

Let A be a rational Hermitian effect on k dimensions, D=I-A, and suppose a mathematical candidate C=[[A,B],[B*,D]]>=0 has already been specified through the fixed-effect slice. Its partial trace is I. We turn a certified absolute approximation to B into an EXACT rational feasible Choi matrix without changing A or adding a constant replacement-cost floor.

## 1. Known supports and a paid arithmetic eigenvalue bound

Let Q_den>=1 be a common positive integer denominator for the real and imaginary entries of A and D. Both support projectors P_A,P_D are exactly rational: take a rational column basis V for each range by Gaussian elimination and form V(V*V)^(-1)V*. No support of an unknown quantum source is acquired.

Every positive eigenvalue of A or D is at least mu=Q_den^(-k). Indeed, for rank r>0 the product of its r positive eigenvalues is the r-th elementary symmetric coefficient, a sum of r by r principal minors. Multiplied by Q_den^r this is a positive integer: Hermitian Gaussian-integer determinants are real integers. The product is therefore at least Q_den^(-r). Since all eigenvalues are at most1, every positive eigenvalue is at least that product and hence at least mu. Rank zero gives a trivial cross-block support. The bit length of mu is polynomial in the known rational input length; no physical gap promise is added.

## 2. Exact rational feasible output

Choose rational0<t<=1/4. Obtain a rational Btilde with certified Frobenius error ||Btilde-B||F<=e, where e<=t mu/4. Define

    B_fin=(1-t) P_A Btilde P_D,
    C_fin=[[A,B_fin],[B_fin*,D]].

This is exactly rational and exactly CPTP. Block positivity of C gives B=sqrt(A) K sqrt(D) for a contraction K, with B=P_A B P_D. On the positive supports,

    ||A^(-1/2) B_fin D^(-1/2)||
       <=1-t+e/mu<=1-3t/4<1.

The zero supports vanish exactly. The block-factorization criterion proves PSD; it may also be certified by exact rational PSD arithmetic. The partial trace remains A+D=I exactly. This is not a TNI substitute or a positive-completion inference from unrelated data.

Since ||B||F<=sqrt(k),

    ||C_fin-C||F<=sqrt(2)(t sqrt(k)+e)<=2t sqrt(k).       (1)

The stipulated error and PSD certificates are required; an uncertified approximation uses a declared feasible fallback. Required absolute accuracy e costs O(log(1/t)+k log Q_den) bits, not a reciprocal-e number of source samples.

## 3. Positive cost and numerator transfer

Suppose u(C)=m0+Tr(W C), m0>0, W>=0, and N(C)=||c+L(C)||², with known rational coefficients. Choose rational a>=||L||op² and w>=||W||F², put B_num=1+||c||²+2k a, and require

    t<=min{1/4, m0/(1200 B_num), m0/[400k(1+w)]}.        (2)

A qubit-output decoder has0<=C<=2I and Tr C=k, hence ||C||F<=sqrt(2k). Equation(1) gives a root-numerator displacement at most2t sqrt(k a). Since N(C)<=2B_num and t<=1,

    |N(C_fin)-N(C)|<=6 B_num t<=m0/200,
    |u(C_fin)-u(C)|<=2t sqrt(k w)<=m0/400.              (3)

Both costs are at least m0 because both Choi matrices are feasible and W is PSD. Therefore

    N(C_fin)/u(C_fin)
       >=[N(C)/u(C)-1/200]/(1+1/400)
       >=0.99 N(C)/u(C)-0.01.                         (4)

Unlike the received fixed-shrink counterexample, t is a known precision parameter adapted to the positive cost floor. Small t costs arithmetic bits, not retries or new source calls. A is unchanged, including its exact zero and one eigenspaces.

## 4. Exact scope

This removes the support-alignment/rational-output concern AFTER a fixed-effect mathematical candidate and a certified approximation to its cross block have been computed. It does not grant that approximation as a quantum query. Square roots and polar frames are functions of KNOWN matrices; a full canonical optimization implementation still needs its numerical residual-to-cost/numerator transfer recorded. Globally moving A is untouched.

The rational eigenvalue floor is a finite-input arithmetic bound, not a favorable unknown-source spectral floor. No current source-acquisition exponent changes.
