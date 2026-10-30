# Replacement for the failed freezing step: exact growing-shell profile

Status: internal derivation, awaiting audit. This constructs and compares the actual infinite family of conservative-shell profiles in the obstruction network. It is not a global recurrence proof.

Consider its fast A,C chain at fixed N=A+C≥3 and fixed B≥4. The common factor(B)_4 changes time only. Write a=A,c=N−a. The chain is birth–death in a, with

    birth_a=c[6(c−1)(c−2)+a(c−1)+7a(a−1)],
    death_(a+1)=(a+1)[12(c−1)(c−2)+a(c−1)+a(a−1)].

Thus an exact positive stationary profile is

    w_N(a)=binom(N,a) product_(j=0)^(a−1) P_N(j)/Q_N(j),
    sigma_N(a)=w_N(a)/Z_N,
    P_N(j)=6(c−1)(c−2)+j(c−1)+7j(j−1),
    Q_N(j)=12(c−1)(c−2)+j(c−1)+j(j−1), c=N−j.

All factors are positive for N≥3 and0≤j≤N−1. The fast adjoint annihilates sigma_N EXACTLY, including population boundaries. This is not a frozen deterministic equilibrium or a time-scale separation assumption.

## A uniform neighboring-shell comparison
Let X=(c−1)(c−2),Y=j(c−1),Z=j(j−1), all nonnegative. Then

    1/2 ≤ P_N(j)/Q_N(j) ≤7.

Also X+Y+Z≥(N−2)²/2, hence both P_N,Q_N≥(N−2)²/2. At fixed j,

    P_(N+1)(j)−P_N(j)=12(c−1)+j≤12N,
    Q_(N+1)(j)−Q_N(j)=24(c−1)+j≤24N.

For N≥3 these imply

    1≤P_(N+1)/P_N≤1+216/N,
    1≤Q_(N+1)/Q_N≤1+432/N.

There are at most N product factors. Therefore, for0≤a≤N,

    e^(−432) (N+1)/(N+1−a)
      ≤ w_(N+1)(a)/w_N(a)
      ≤ e^216 (N+1)/(N+1−a).

Combining with the exact birth–death ratio on shell N+1 gives analogous bounds

    (e^(−432)/2) (N+1)/(a+1)
      ≤ w_(N+1)(a+1)/w_N(a)
      ≤ 7e^216 (N+1)/(a+1).

These very loose constants are finite and independent of N,a. No spectral-gap or global endpoint-comparability hypothesis is used.

For normalization, the first inequality gives Z_(N+1)≥e^(−432) Z_N. For an upper bound, split shell N+1 at its midpoint: for a≤(N+1)/2 compare by adding C to state a on shell N; for a>(N+1)/2 compare by adding A to state a−1. The displayed ratios are then≤2e^216 or14e^216. Summing yields

    e^(−432) ≤ Z_(N+1)/Z_N ≤16e^216.

Hence normalized profiles sigma_N obey the same form of neighboring-shell bounds, with different fixed constants. Adding one particle changes a profile by at most a fixed constant times (N+1)/(a+1) or (N+1)/(c+1), and by a bounded factor on every compact interior composition interval.

## What this changes
The frozen phase matrix had a positive eigenvalue for every fixed fugacity tilt, because it discarded real conservative redistribution of unbounded A,C. The exact sigma_N removes that spurious fast growth identically. It also earns the missing forcing-sensitive neighboring-shell comparison directly, despite exponentially different weights at distant points on a shell. The earlier resolvent endpoint obstruction does not prohibit such a local comparison.

The full connector reactions move between N and B levels, and their adjoint action on sigma_N times a radial/phase envelope must still be controlled pointwise. The comparison constants above alone do not settle that global assembly, and no averaging of connector rates is performed. Extending this mechanism to arbitrary multidimensional conservative faces remains a separate hard problem.
