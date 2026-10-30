# Active occupation comparison with a fast siphon — full local proof
Status: personally checked derivation, not independently reviewed. Separate from all frozen family proofs.

Fix d>=2, m>=2, and a finite strongly connected homogeneous degree-m complex graph. Every complex contains A. The graph contains mA and A+(m-1)X_i for each i!=A, and each latter source has an edge whose product has more A. All rate constants and the clearing coefficient are fixed positive. Write Q_N for its mass-action generator on total-count shell N. Add clearing hazard k_D(A)_m and optional competing hazard u+vA, where 0<=u,v<=C_0. Let tau be the first killing event of any kind and, for active starts A>=1, define

    T_N(x)=E_x tau,    U_N(x)=E_x int_0^tau A_s ds.

For all sufficiently large N, uniformly in x with A>=1 and in the bounded competitors,

    T_N(x)<=C log(N+1)/N^(m-1),
    T_N(x)<=C log(N+1) N^-gamma U_N(x),
    gamma=(m-1)/(2m).

In addition, uniformly in these x and competitors, the probability that clearing is the first killing tends to one and U_N(x)>=cN^{-(m-1)}. The last two statements require only that u,v are bounded, not bounded below. No assertion is made for A=0.

## 1. Pointwise logarithmic drift
For an enabled reaction, its A-jump j has |j|<=m-1, and A+j>=1 since its product contains A. Thus |log(A+j)-log A|<=C_m/A. The total reaction rate is <=C A N^(m-1), giving |Q_N log A|<=CN^(m-1).

If A<=epsilon N, a reservoir coordinate is >=(1-epsilon)N/(d-1). For large N its designated source is enabled, with rate >=c A N^(m-1). Its positive logarithmic jump is >=c'/A. Thus one positive contribution is >=c''N^(m-1).

An A-decreasing reaction must have at least two A in its source (all products contain A). For source A-degree a>=2, its absolute negative log contribution is <=C A^(a-1)N^(m-a)<=C A N^(m-2). Summing and choosing fixed epsilon sufficiently small yields

    Q_N log A>=cN^(m-1) whenever 1<=A<=epsilon N.  (L)

These estimates include disabled reactions and small A without replacing factorial propensities by powers on the lower-bound side.

## 2. Uniform killed-time bound, without recurrence assumption
On the finite shell define W(x)=2log(N+1)-log A. It satisfies log(N+1)<=W<=2log(N+1). For the killed generator K=Q_N-[k_D(A)_m+u+vA], (L) gives KW<=-cN^(m-1) when A<=epsilon N. When A>epsilon N, Q_N W<=CN^(m-1), whereas k_D(A)_m W>=c'N^m log(N+1). Consequently KW<=-cN^(m-1) throughout the active shell for large N.

Apply the finite-state stopped Dynkin formula up to tau wedge t, assigning W=0 at the cemetery. Positivity of W gives E(tau wedge t)<=W(x)/(cN^(m-1)). Monotone convergence proves the first bound and finite killing time; neither irreducibility nor a prior mean-time estimate is needed.

## 3. Mesoscopic hit before killing
Put K_N=floor(N^gamma), gamma=(m-1)/(2m), and consider the UNKILLED fast chain from 1<=A<=K_N. Let sigma be its first hit of A>=K_N. Before sigma, (L) applies. The stopped bounded function log A has values between0 and log(K_N+m), so Dynkin localization gives

    E sigma <=C log(N+1)/N^(m-1).

Indeed this bound follows first for sigma wedge t, hence forces sigma finite. Before sigma the total killing hazard is at most C(K_N^m+K_N+1). Couple killing with its integrated hazard along the unkilled path. Then

    P(tau<=sigma)<=C K_N^m E sigma
                    <=C N^{-(m-1)/2}log(N+1)=o(1).      (H)

At sigma, A lies in [K_N,K_N+m].

## 4. Occupation earned at the mesoscopic hit
Start with A in [K_N-m,K_N+m], for N large. Stop the unkilled path when A leaves [K_N/2,2K_N]. Before that exit its total jump intensity is <=C K_N N^(m-1). Let t_N=c_0/N^(m-1). Since every jump changes A by at most m-1, exiting the interval requires at least c_1K_N jumps for a constant c_1>0. The expected stopped number of jumps by t_N is <=C c_0K_N; Markov's inequality therefore bounds exit probability by C'c_0. Choose c_0 so it is <=1/4.

The integrated killing hazard before the same exit or t_N is <=C(K_N^m+K_N+1)t_N=o(1), deterministically. Hence with probability at least1/2, the actual killed chain remains alive in this interval for all of [0,t_N]. On this event its A-occupation is at least (K_N/2)t_N, proving

    U_N(x)>=cK_N/N^(m-1) whenever |A-K_N|<=m.          (D)

By (H), strong Markov at the mesoscopic hit extends (D), with a smaller constant, to every start 1<=A<=K_N. Combined with section2 this proves T_N/U_N<=C log(N+1)/K_N for those starts.

## 5. Starts above the mesoscopic level
For A>K_N, stop the actual killed chain at killing or its first entrance into A<=K_N. Prior to this stop, occupation is at least K_N times elapsed time. At an entrance the chain has A in [K_N-m,K_N], and sections3–4 apply. Let R_N=C log(N+1)/K_N, chosen also >=1/K_N. Strong Markov and the pointwise bound at the entrance give

    T_pre+E[1_entrance T_N(X_entrance)]
      <=R_N {U_pre+E[1_entrance U_N(X_entrance)]}.

This is exactly T_N(x)<=R_N U_N(x), including paths killed before entrance.

## 6. Clearing probability and opportunity lower bound
The clearing compensator gives E int_0^tau k_D(A_s)_m ds=P(clearing first)<=1. Since A^m<=C[(A)_m+1], Holder's inequality on the occupation measure yields

    U_N <= C T_N^((m-1)/m)(1+T_N)^(1/m)=o(1).

The competing-event probability is u T_N+v U_N=o(1), uniformly for bounded u,v. Thus P(clearing first)>=1/2 for large N. Finally (A)_m<=N^(m-1)A implies

    1/2 <= k_D E int_0^tau (A_s)_m ds
        <= k_D N^(m-1) U_N,

giving U_N>=cN^{-(m-1)}.

## 7. Actual catalyst restoration
At fixed B>=q, divide physical time by the common fast/clearing factor (B)_q: normalized competitors are u=k_I/(B)_q and v=k_T B/(B)_q, uniformly bounded for all B>=q. Thus the lemma applies uniformly in B. Both physical T and U are their normalized versions divided by (B)_q, so their ratio is unchanged. At the fixed section B=q the constants absorb this factor.

For finite small N, the lemma's asymptotic claims are not asserted. Any state enabling a fast source can follow a directed complex path to mA, then clear with positive probability. Finite-state killing arguments apply on active classes. Inactive A>=1 states can occur at small N and require physical connector treatment. At large N, every A>=1 state enables either mA or a source A+(m-1)X_i; A=0 remains a genuine fast siphon and requires actual immigration.
