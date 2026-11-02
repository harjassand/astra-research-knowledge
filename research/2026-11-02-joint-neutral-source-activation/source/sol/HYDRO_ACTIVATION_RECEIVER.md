# A raw support-activation principle with a complete physical receiver

Author-derived ordinary proof, same sole principal; no independent audit or historical-priority clearance. This is a complete sufficient structural rule, not the unrestricted weak-reversibility theorem. Classical density-dependent martingale estimates and the Filonov/stopped-observation viewpoint are ordinary machinery; the construction below earns the uniform activation data and complete common reward from the raw list.

## 1. Raw hypothesis and conclusion

There are d finite species, with distinguished draining species A. The only total-count-changing reactions are

    0 -> A, rate lambda>0;     A ->0, rate mu A, mu>0.

Every other genuine reaction y->y' preserves N=sum_i x_i, hence |y|=|y'|. Fixed positive rate constants use ordinary falling-factorial mass action. Let m>=2 be the largest internal source degree and R_m its degree-m reactions. Lower-degree conservative reactions are unrestricted.

For each singleton support {i}, perform the following finite closure using ONLY R_m: a reaction whose source support is contained in the current support adds all of its product species. Require that A belongs to this closure for every i. This is a finite raw hypergraph decision, with a witnessing sequence of at most d−1 support-enlarging reactions for each i. It requires pure mX_i sources for non-A singleton starts, followed by possibly mixed cooperative activation; it does not require an ordered source chain, a common reaction anchor, a stationary fiber, or any mixing gap.

Assume the full list is weakly reversible when making the classwise conclusion below. The same argument applies more generally to any closed irreducible class satisfying these raw guards.

**Theorem.** The actual CTMC is nonexplosive. Every irreducible class is positive recurrent, and for its stationary law pi and every r>0,

    E_pi [(1+q(X)) exp(r N(X))]<infinity.                      (H1)

For rational input rates and rational 1<u<t, explicit finite data below acquire a single head H={N<=L} and actual observation episodes satisfying

    E_x[ integral_0^sigma (1+q)u^N ds+V(X_sigma)]<=V(x)−1,    (H2)

where V=t^N outside H and zero on H. Every landing is received at this SAME global value. No statewise stopped expectation is advertised as a computed solver. The raw construction acquires the drift/reward head; a numerical stationary constant would additionally require acquisition of the true finite-head trace.

## 2. A finite quantitative support witness

Let K_m=sum_(R_m) kappa_r, K_lo=sum_(R\R_m) kappa_r, K=K_m+K_lo and k_min=min_(R_m) kappa_r. Set

    T=d+1, L_0=m K_m, b=2^(−ceil(2 L_0 T)),
    delta_0=b/d,
    delta_(j+1)=min(delta_j,k_min delta_j^m b^2), j<d−1,
    delta=delta_(d−1)>0.

Consider the leading deterministic field F(z)=sum_(R_m) kappa_r z^y(y'−y) on the unit simplex. Its solutions exist globally and remain on that compact simplex. For each coordinate, consumption requires that coordinate in the source, so

    dot z_i>=−L_0 z_i.

At least one initial coordinate is >=1/d and therefore stays >=b/d throughout [0,T]. Follow its acquired support witness. Once every input species of the next witness reaction is >=delta_j, its newly produced species obeys dot z_k>=k_min delta_j^m−L_0 z_k. Over one unit interval, followed by persistence to T, it is >=k_min delta_j^m b^2. Existing activated coordinates retain their earlier lower bounds. At most d−1 enlargements are needed. Consequently, UNIFORMLY over EVERY initial composition on the simplex,

    z_A(s)>=delta,                d<=s<=d+1=T.              (H3)

This is actual finite-time support activation, not eventual permanence or convergence to an equilibrium. It includes every initial face and arbitrary ratios among all hidden populations.

## 3. A finite-N probability bound, not an infinite-rate premise

Start the physical chain at total count n>=m. Observe it for the deterministic physical interval

    tau_n=T n^(1−m).

Set Z_n(s)=X(s n^(1−m))/n. Let z(s) solve the leading ODE from X(0)/n. Stop estimates if the physical total exceeds 2n. Count conservation implies PATHWISE

    N(v)<=n+I(v),              I a rate-lambda Poisson driver.

Thus nonexplosion already follows: finite N sublevels have bounded genuine rates, and I has finitely many jumps on every finite physical interval.

On the stopped box define the rational bounds

    L_F=m^2 2^m K_m,
    C_E=m^3 3^(m−1)K_m+m 2^(m−1)K_lo+lambda+2mu,
    Q=2^m K+lambda+2mu.

L_F bounds the leading field's infinity-norm Lipschitz constant on [0,2]^d. The falling-factorial product differs from its leading monomial by at most m^2 3^(m−1)/n; after its coordinate jump factor, the leading drift error is bounded by the first term of C_E/n. All lower-degree conservative drift and port drift contribute the other terms. Therefore the scaled drift differs from F by at most C_E/n.

Each scaled martingale coordinate has jumps <=m/n and predictable quadratic variation <=m^2 Q T/n. Put

    b_F=2^(−ceil(2 L_F T)), a=delta b_F/4,
    gamma=a^2/[4(m^2 Q T+m a)].

The compensated-Poisson exponential martingale, using e^v−1−v<=v^2 for |v|<=1, gives

    P(sup_(s<=T)|M_i(s)|>=a)<=2 exp(−gamma n).              (H4)

For completeness choose the exponential parameter eta=n a/[2(m^2QT+ma)], so eta m/n<=1/2. Its variance price is at most eta^2 m^2QT/n, and the resulting exponent is at most −gamma n. Apply both signs and the maximal inequality. No stationary phase or independent-cohort assertion is involved.

If

    n>=4 C_E T/(delta b_F),                                 (H5)

Gronwall gives sup_(s<=T)|Z_n(s)−z(s)|_infty<=delta/2 whenever the martingale bound holds and the box is not exited. The exit probability is at most exp(lambda T)2^(−n). Combining with (H3), there is an event G_n with

    A(v)>=delta n/2 on [d n^(1−m),T n^(1−m)],
    P(G_n^c)<=C_P exp(−c n),                                (H6)
    C_P=2d+2^ceil(2lambda T), c=min(gamma,1/2).

Every quantity is acquired from the raw list. This finite-N estimate is the required uniform control; no homogenization limit has been inserted in its place.

## 4. All actual outputs at one total-count value

Write Delta_t=1−1/t. On G_n the genuine death hazard satisfies

    mu integral_0^tau_n A(v)dv >= h_n,
    h_n=(mu delta/2)n^(2−m).

Use independent unit Poisson drivers Y_+,Y_- for immigration and death. Exactly N(tau_n)=n+I−D. On G_n, D=Y_-(mu integral A)>=Y_-(h_n). This is a PATHWISE bound, not survival-conditioned independence. Hence

    E t^(N(tau_n)−n)
      <=exp[lambda tau_n(t−1)−Delta_t h_n]
        +exp[lambda tau_n(t^2−1)/2] sqrt(P(G_n^c)).           (H7)

The first expectation factors only after the event is dropped; the two raw Poisson drivers are independent. The second term is Cauchy–Schwarz with the exact immigration MGF. Thus every adverse path and actual landing is included.

Let b_t=Delta_t mu delta/4, eta=min(b_t,1)/2. If n>=4lambda T t/(mu delta), the first term is <=1−eta n^(2−m). Bound the second by C_t exp(−c n/2), where

    C_t=ceil(sqrt C_P) 2^ceil(lambda T(t^2−1)).

For p=m−2, choose additionally

    n>=max((4p/c)^2,8 C_t/(c eta),1).

Then p log n<=c n/4 and exp(−c n/4)<=4/(cn), making the second term <=(eta/2)n^(2−m). Therefore, with a_out=eta/2,

    E t^N(tau_n)<= [1−a_out n^(2−m)] t^n.                  (H8)

For m>2 the per-observation contraction is polynomially small. Its PHYSICAL interval is also shrinking, and no positive uniform mixing gap is needed or claimed.

## 5. The whole physical occupation and genuine activity are paid

Fix 1<u<t and let I*=I(tau_n). Along the ENTIRE actual interval, including G_n^c,

    N(v)<=n+I*,
    1+q(X(v))<=(1+lambda+mu+K)(n+I*)^m.

For n>=1, n+I*<=n(1+I*), and I* is stochastically bounded by Pois(lambda T). With S the Stirling numbers of the second kind, define the acquired bound

    C_u=2^ceil(2lambda T(u−1))
           sum_(ell=0)^m S(m+1,ell+1)(lambda T u)^ell,
    C_occ=T(1+lambda+mu+K) C_u.

The exact Poisson factorial-tilt identity proves

    E integral_0^tau_n (1+q(X(v)))u^N(v)dv
         <=C_occ n u^n.                                    (H9)

The 1 term pays residence and the q term pays GENUINE reaction activity. No whole-interval cost is replaced by a terminal output or by a fictitious fast clock.

Let zeta=1−u/t. The sufficient rational requirements

    n>=(2(m−1)/zeta)^2,
    n>=4 C_occ/(zeta a_out)

make (H9) at most half (H8)'s negative output margin. Indeed n^(m−1)(u/t)^n<=exp(−zeta n/2) beyond the first threshold. Finally

    n>=ceil sqrt[2 m!/(a_out Delta_t^m)]

makes the residual margin at least one, since t^n>=exp(Delta_t n)>=(Delta_t n)^m/m!. Choose L above all these acquired thresholds and (H5), n>=m, and the output thresholds of Section4. This establishes (H2) for complete observation intervals. Early absorption at H removes only nonnegative future reward and terminal value, so preserves the inequality.

## 6. Whole return consequence and the numerical boundary

Repeat the actual observation intervals until H. The nonnegative potential plus accumulated physical F reward is a supermartingale, and each outside-head interval has residual at least one. Finite-stage expectations are legitimate by N(v)<=n+I(v) and the Poisson exponential moments. Thus H is reached after finitely many observation intervals with finite expected entire F reward. Sampling cannot accumulate in finite physical time: on any such time interval N is pathwise bounded, so the positive lengths T N^(1−m) have a positive lower bound. No artificial resetting or control was applied.

Every head state has finitely many genuine successors and a finite initial holding reward. Outside-head successors have hitting reward at most t^(L+1). On an actual closed irreducible class, the finite head trace is irreducible and its return count has a finite geometric block bound. Closing its real excursions proves finite positive physical return reward. Regeneration yields (H1). Weak reversibility supplies closedness of the actual classes; it is not used as a substitute for the activation/occupation estimates.

The constructor below acquires raw support witnesses, rational activation/concentration data and L. Its exact large integers are stored with hexadecimal tags rather than silently failing decimal conversion. It does NOT acquire or evaluate the finite-head trace's stationary normalizing constant. The theorem may use this proved finite existential ingredient, while a numerical stationary-moment solver would have to acquire it.

## 7. Scope of the new operation

The useful global operation is uniform finite-time SERVICE CREATION from every initial support, followed by a paid observation at the SAME total-count potential. Arbitrarily many unpinned inventories and all of their feedback evolve during the interval. A finite raw support closure, not a favorable receiving law, earns the activation bound. The method is distinct from averaging a conservative core through an infinite-rate limit.

The restriction is substantial. If some large hidden singleton support cannot produce A in the leading density system, the proof supplies no activation bound: finite immigration seeds and sublinear activation-debt layers can then govern the clock. The accepted N1621 rate-2 model and N1421 A-catalytic families illustrate why those cases cannot be erased by this criterion. General weakly reversible recurrence, and general one-port conservative-core stability without the support condition, remain unresolved here.
