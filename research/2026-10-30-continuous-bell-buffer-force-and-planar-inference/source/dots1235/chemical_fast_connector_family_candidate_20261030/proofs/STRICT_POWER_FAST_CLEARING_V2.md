# A strict power improvement for uniform fast clearing, without mixing
Status: V2: dependency-reduced personal derivation, under separate review. The uniform block-survival argument is self-contained and does NOT use the earlier fractional-factorial mean bound. Fixed positive fast constants (uniformly over a compact constant-coefficient box) only; arbitrary state-dependent controls are not claimed here.

## Contract and target
Use the homogeneous degree-m conservative fast graph containing all pure mX_i from UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME_V2.md. Let tau be killing at rate c(A)_m on the N-shell, with common catalyst factor temporarily removed. Claim: there are epsilon>0,C<infinity depending only on the finite graph and coefficient bounds such that

    sup_x E_x tau <= C N^(1-m-epsilon)                    (1)

for all sufficiently large N. This is a quantitative stochastic startup estimate, NOT a mixing or metastability assertion.

## 1. Uniform small-time deterministic production along complex paths
The normalized fast ODE z'=b(z) stays in the compact simplex. Every coordinate has total negative drift at most C z_j because any consuming mass-action monomial contains z_j. Choose an initially dominant species i with z_i(0)>=1/k. Then z_i(t)>=e^-C/k on0<=t<=1.

Follow a fixed complex path from mX_i to mA. Every species appearing in the current source complex has already been assigned a bound z_l(t)>=c_l t^(L_l). A newly introduced product species j has y_j=0 at its first introduction, so

    z'_j >= c product_l z_l^(y_l)-C z_j
          >= c' t^(sum_l y_l L_l)-C z_j.

Integration gives z_j(t)>=c'' t^(1+sum_l y_l L_l). Existing lower bounds remain valid. Thus the path eventually gives a lower bound for A. Taking the maximum exponent and minimum constant over finitely many initially dominant species yields

    z_A(t)>=c t^L,  0<t<=1,                              (2)

uniformly over EVERY initial simplex point. L>=1 is a finite integer; the recursion L_new<=m L_max+1 makes it explicitly finite. All constants can be uniform over a fixed positive compact box of constant coefficients.

## 2. Elementary shrinking-time fluid estimate
Run the UNKILLED finite-shell fast chain and set Y_N(t)=X(N^(1-m)t)/N. Its drift b_N satisfies sup|b_N-b|<=C/N by falling-factorial polynomial expansion. The martingale part M_N has

    E sup_(u<=T)|M_N(u)|^2 <= C T/N,  0<T<=1,

by bounded jumps and total rescaled rate O(N), followed by Doob's inequality. The polynomial drift b is uniformly Lipschitz on the compact simplex. Gronwall therefore gives, for the ODE starting at the same x/N,

    P(sup_(u<=T)|Y_N(u)-z(u)|>eta)
       <= C (T/N+T^2/N^2)/eta^2.                          (3)

No long-time limit theorem is imported; all estimates are on a shrinking interval.

Choose

    epsilon=1/[4(mL+1)],   T=N^(-epsilon),
    eta=(c/2)(T/2)^L.

Equations (2)-(3) show that throughout [T/2,T], A in the unkilled chain is at least c' N T^L except with probability

    O(N^(-kappa)),  kappa=1-epsilon(2L-1)>epsilon.

The small deterministic drift error is included in (3) and is smaller than eta for large N.

## 3. Actual killing hazard and uniform block iteration, not assumed absorption
Couple clearing to the unkilled path by an independent unit exponential threshold for its integrated hazard. On the good event above, (A)_m>=c A^m for large N, and the integrated physical hazard over the final half-interval is at least

    c N^(1-m) T * N^m T^(mL)
      =c N T^(mL+1)=c N^(3/4).

Hence, at physical time t_N=N^(1-m-epsilon),

    P_x(tau>t_N)<=C N^(-kappa)+exp(-cN^(3/4)),             (4)

uniformly in the starting composition.

The bound (4) is uniform over EVERY starting composition. For large N its right-hand side p_N is at most1/2. Strong Markov at successive blocks of length t_N therefore gives

    P_x(tau>j t_N)<=p_N^j<=2^(-j),
    E_x tau<=t_N/(1-p_N)<=2t_N.

This proves the strict power gain and exponential survival on that improved scale directly. No prior finite-mean theorem, stationary distribution, factorial-boundary drift, or mixing estimate is needed for restart or finiteness. More precisely survival is bounded by2 exp[-(log2)t/t_N].

## 4. Catalyst and genuinely competing connector events
For fixed B>=q, multiply both fast and killing rates by (B)_q; all times divide by that factor. Before the first connector birth, N,B are fixed and total competing rate is at most C(1+NB). Additional killing/hazard comparison therefore gives

    P(birth before clearing)
       <= C (1+NB) N^(1-m-epsilon)/(B)_q,

in particular O(N^(2-m-epsilon) B^(1-q)) for N>=1,B>=q. These are bounds on actual first competing events, not frozen stationary averages. Small inactive states and B<q remain excluded exactly as in the dependency.

## What is NOT concluded
This does not yet establish the full N-directed phase-return bias after low-B excursions. Output compositions at clearing and their correlation with subsequent connector races must be carried through that construction. The higher-dimensional entropy/interface issue is not declared solved by (1).
