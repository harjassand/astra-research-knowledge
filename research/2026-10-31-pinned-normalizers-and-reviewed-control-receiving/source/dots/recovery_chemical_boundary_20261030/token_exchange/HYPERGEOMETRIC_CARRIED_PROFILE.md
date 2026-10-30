# An exact dilution-aware carried profile for productive uniform resets

30 October 2026. New local candidate. This solves the incoming-profile seam for a specified productive-reset module, not for arbitrary C/Y disturbances or a whole raw network.

## Model and profile

Fix an integer offset ell>=1. There are n persistent labels, C source and Y=n-C working. A working label has rank0,...,L; rank0 is target, count A. Each source enters at rate gamma and becomes a working rank-L label. At that same event, with probability Y/(Y+ell), select an old working identity uniformly and reset its rank to L; otherwise reset none. Equivalently sample one of Y+ell slots, ell of which are null. Thus a particular old target is lost with probability1/(Y+ell). Working labels progress toward rank0 at allocated rate q, with any additional safe working moves allowed. There are no other adverse events, births or deletions before the killing mark. Kill at rate kappa(A)_m, n sufficiently large. Assume nonexplosion and valid localized Dynkin calculus in this exact common clock.

The offset can represent additional null/protected slots, but no physical realization is being assumed. The exact law, especially its uniform reset, must be acquired before use.

For s>0 define

    Phi_s(A,Y;n)=E (1+H)^(-s),
    H~Hypergeom(N=n+ell-1, marked=A, draws=Y+ell-1).

This is well-defined for0<=A<=Y<=n and ell>=1, with the natural degenerate convention when N=0. At Y=n it equals f_s(A). Write

    mu=A(Y+ell-1)/(n+ell-1).

Uniformly in n,A,Y,

    f_s(mu)<=Phi_s(A,Y;n)<=C_s f_s(mu).              (C)

## Exact harmonicity, not a heuristic dilution correction

Suppress working progress and run source entries until C=0. For j distinct initially-target identities, survival through a growth step at working size r has probability1-j/(r+ell). Multiplying from r=Y to n-1 gives

    E[(H_final)_j]=(A)_j (Y+ell-1)_j/(n+ell-1)_j.

These are exactly the factorial moments of the displayed hypergeometric variable and determine its finite-support distribution. Therefore Phi_s is the actual terminal f_s value function of the pure entry/reset chain. Its entry generator is EXACTLY zero. In particular A(Y+ell-1) is an entry/reset martingale; the profile pays its finite-population fluctuations rather than merely taking the inverse of that martingale.

Increasing A at fixed Y decreases Phi_s by coupling the marked set. Consequently working progress and safe rank decreases have nonpositive Phi_s drift. The full un-killed process has

    L Phi_s<=0.                                    (H)

The killed process may be extended past its Cox mark for optional stopping. Equation(H) yields incoming Phi preservation at deterministic times and at the actual pre-kill state.

## Proof of comparability(C)

The hypergeometric mean is mu. Convexity of f_s gives the lower bound. For the upper bound, sampling without replacement from N weights (A equal to exp(-theta), the others1) gives

    E exp(-theta H)
       <=[1-(A/N)(1-exp(-theta))]^(Y+ell-1)
       <=exp[-mu(1-exp(-theta))].

For completeness, the first inequality is the elementary-symmetric mean inequality: at fixed sum of nonnegative weights, averaging any pair increases every elementary symmetric polynomial because only their nonnegative-coefficient product term changes. Repeated averaging proves its maximum occurs at equal weights. No independence of sampled identities is asserted.

Take theta=log2 and apply Markov to H<=mu/2 to obtain exp(-c mu). Split E f_s(H) there to get (C). Degenerate N=0 or mu=0 is immediate. In particular

    Phi_s^2<=Phi_(2s)<=C_s Phi_s^2,                 (S)

the first inequality by Jensen and the second by(C).

## Actual killing-time scale

This module satisfies PRODUCTIVE_POOL_FORCING: source entries grow Y, each working label's adverse participation is gamma C/(Y+ell)<=gamma C/(1+Y), and each entry resets at most one existing worker. Let

    alpha=m/((L+1)m+1),   T_n=C n^-alpha.

Here is the stopped argument rather than an automatic deterministic-time import. Use the first third of a block to obtain Y>=c nT_n (or retain the already-large working pool). Select c nT_n workers. During the next third their adverse participation is bounded by B/T_n, while their product-forcing damping is a fixed constant. At time2T_n/3 there are J>=c nT_n^(L+1) target identities, except with probability exp[-c nT_n^(L+1)].

For a final interval of length epsilon T_n, with fixed epsilon<=1/3 sufficiently small, the cohort touch-count mgf uses per-label bound B/T_n and proves that at least J/2 remain target throughout, except with probability exp(-cJ). The integrated kill hazard is then at least

    c epsilon T_n J^m >= c' C^((L+1)m+1).

Choose C large first, then n large; conditional survival through a block is <=1/2 uniformly over all starting pool/rank configurations. Since n stays fixed, block restarting gives E tau^j<=C_j n^(-j alpha) and a square-root survival integral of order n^-alpha. Finite small n requires n>=m for kill availability and can be handled separately; no assertion is made for n<m with no immigration.

For the version with exact one-step progress and no additional safe moves, the time POWER is also sharp from the all-source initial state. Ignore resets and use the same independent source-entry and per-label progress clocks; this reference process dominates actual target ranks. A reference label reaches target by time t with probability at most gamma q^L t^(L+1)/(L+1)!, and the n reference labels are independent. Hence P(tau<=t)<=C n^m t^((L+1)m+1) by the actual kill compensator and reference factorial moment. Taking a small constant times n^-alpha gives the matching lower moment scale. This asserts only the population power, not a leading constant or global chemical optimality.

## Graded Green with the correct incoming profile

Using(H),(S), Cauchy-Schwarz and the actual survival tail gives

    E integral_0^tau Phi_s(A_t,Y_t;n)dt
       <=C_s n^-alpha Phi_s(A_0,Y_0;n).

Since Phi_s>=f_s(A), the same bound holds with actual f_s(A_t) as the integrand. Optional stopping of(H) yields terminal carried preservation. If the actual kill removes at most m targets, then

    E f_s(A_out)<=C_s Phi_s(A_0,Y_0;n).

A carried output with its updated population n'=n-d,Y'=Y-d,A'=A-d,0<=d<=m, is also bounded by a constant times the incoming Phi_s at the pre-kill state. Indeed if A<2m its pre-kill mu is bounded; otherwise A-d>=A/2 and Y-d+ell-1>=(Y+ell-1)/2, while the normalization denominator decreases. Thus mu_out>=mu_pre/4. Apply(C). This is preservation, NOT a population-small carried-output reset.

Finally, the actual kill compensator bounds P(A_(tau-)<=K)<=C K^m n^-alpha. Combine terminal grade2s preservation with(S) and split at K to obtain

    E f_(s+p)(A_out)
       <=C_(s,p) n^[-alpha p/(2p+m)] Phi_s(A_0,Y_0;n).

This is a genuine actual-A output reset relative to a dilution-aware incoming profile. It does not substitute f_s(A_0) for Phi_s(A_0,Y_0;n); PRODUCTIVE_POOL_PROFILE_OBSTRUCTION proves that substitution can fail.

## What remains open

The module's uniform-reset law and monotone source consumption are exact assumptions. General bounded-batch C/Y disturbances, working-to-source returns, seed deletions, immigration, arbitrary face metadata and physical-clock conversion are not covered by this carried theorem. In particular Phi_s at a kill output need NOT have a population-small factor: the working pool may still be too small relative to n. A full signed section would need to carry this resource variable through subsequent cycles, not declare its old scalar feedback norm small. No global recurrence or raw compiler extension follows merely from this local construction.
