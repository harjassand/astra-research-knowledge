# A forced-shell replacement: polynomial neighboring Green comparison

Status: new working proof, awaiting audit. This is for the conservative birth–death shell in the demonstrated rank-three obstruction, not arbitrary-dimensional shells.

Let Q_N be its fast A,C birth–death generator on a=0,...,N, with common(B)_4 time factor removed, and ADD genuine killing k(a)=(a)_3 corresponding to the clearing connector. N≥4. Let G_N=(−Q_N)^−1. Every state can reach killing by at most three A-increasing steps followed by clearing, so Q_N is transient. The earlier bounded-path argument gives ||G_N||_infinity≤C N^12: all rates are≤C N³, every nonzero rate is≥a fixed positive constant, and a killing path has length≤4. No mixing estimate is assumed.

## Adding C: compare common indices exactly
Compare shell N+1 with shell N at the same A index a. Eliminate the new endpoint a=N+1 from Q_(N+1) by a Schur complement. That endpoint has equal death and killing rates(N+1)_3. Thus on the old states0,...,N the effective chain has the N+1 birth/death rates, unchanged killings except at a=N, where an extra killing b_(N+1)(N)/2=7N(N−1)/2 is added.

The positive-transition graph on old states is unchanged. At each old a<N,

    b_(N+1)(a)/b_N(a)
      =[(c+1)/c] [P_(N+1)(a)/P_N(a)], c=N−a,

and the second ratio lies between1 and1+C/N by the already proved polynomial bounds. Death-rate ratios lie between1 and1+C/N (their remaining quadratic factor obeys the same uniform lower bound). Endpoint killing changes by1+7/[2(N−2)]=1+O(1/N). All other killing rates are unchanged.

The rooted-forest formulas for det(−Q) and every Green cofactor have POSITIVE coefficients in transition/killing rates. In each forest every vertex chooses at most one outgoing edge. Therefore every individual forest-weight ratio is between1 and

    L_N ≤ C0 product_(c=1)^N(1+1/c) (1+C1/N)^(N+1)
        ≤C2(N+1).

The same finite forest supports occur in both matrices. Taking ratios of numerator and denominator gives, for all old indices a,b,

    [C2(N+1)]^(−1) ≤ G_(N+1)(a,b)/G_N(a,b) ≤C2(N+1).

Here the restricted Green block of the original N+1 chain equals the inverse Schur complement, exactly. This is an entrywise neighboring-shell estimate, not a bound inferred from the inverse norm.

## Adding A: shifted-index comparison, including the new killing site
Compare G_(N+1)(a+1,b+1) with G_N(a,b). Eliminate endpoint A=0 of the N+1 chain. It has no killing and returns to A=1 with probability1, so the Schur complement only removes the excursion/return self-loop. On the shifted old index set, birth-rate ratios have form1+O(1/N); death-rate ratios include(a+1)/a times1+O(1/N); existing killing ratios for a≥3 are(a+1)/(a−2). Products of these per-vertex factors are bounded by a fixed power of N. All are bounded below by1; the finite quadratic factors are handled as in the preceding comparison.

There is one genuinely new killing rate: at old index a=2, the shifted killing is6 while the original was0. First add this killing to Q_N. The rank-one resolvent identity and the Markov Green inequality

    G(a,2)G(2,b)≤G(a,b)G(2,2)

show that adding rate6 reduces any Green entry by at most a factor1+6G(2,2)≤1+C N^12. (The Green inequality follows by considering paths that hit2 before accumulating occupation at b.) After this addition, the two positive forest supports agree, and the remaining rate ratios have polynomial product bounds.

Hence for some fixed constants C,D,

    C^(−1) N^(−D) ≤ G_(N+1)(a+1,b+1)/G_N(a,b) ≤C N^D

uniformly in0≤a,b≤N. No exponential pointwise comparison is imported, and no conservative-shell stationary law is used to establish transience.

## Scope
This constructs the comparison needed for a genuinely KILLED conservative shell, improving on the stationary profile that failed under connector forcing. It still does not solve the full network: connector jumps couple different N and B levels, forcing profiles must be chosen compatibly, and these coarse polynomial bounds may be insufficient to absorb all coupled fluxes with a summable radial envelope. A general growing-shell theorem in higher dimensions remains unproved.
