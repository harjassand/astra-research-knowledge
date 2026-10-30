# Independent audit: fast killed-shell boundary scale

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical audit only.

## Verdict

The uniform mean-absorption bound C N^(-9/4) passes. All regions and endpoint terms are controlled, with no mixing or averaging assumption. Its improvement of the new-killing correction and the shifted Green-comparison exponent to D=4 is valid.

## Drift and Taylor estimate

For the exact shell rates, the leading drift at a/N=0 is 6N³. The degree-three leading polynomial is continuous in a/N, while falling-factorial corrections are uniformly O(N²) over 0≤a≤N. Thus fixed epsilon,c>0 give b_N−d_N≥cN³ for a≤epsilon N and all sufficiently large N. The total rate bound b_N+d_N≤CN³ is uniform over the shell.

Set s=N^(3/4) and W(a)=(a+s)^−3, with W(cemetery)=0. For shifts ±1, the second derivative at all intermediate points is at most C/(a+s)^5 once s≥2. At a=0 the death rate is zero; at a=N the birth rate is zero, so no actual out-of-shell state value is used. Taylor's inequality and the exact killing term give

    Q_N W≤−3(b_N−d_N)/(a+s)^4
             +CN³/(a+s)^5−(a)_3/(a+s)^3.

There is no approximation to the killing term.

## Uniform three-region argument

Eventually s<epsilon N.

1. For 0≤a≤s, the negative drift term has magnitude at least 3cN³/(2s)^4=3c/16. The Taylor remainder relative to this drift is at most C/[3c(a+s)]≤C/(3cs), tending uniformly to zero. Absorb half the drift. Killing is nonpositive.

2. For s<a≤epsilon N, the same relative bound makes the entire fast-motion contribution nonpositive. Also

       (a)_3/(a+s)^3
          ≥(1−1/a)(1−2/a)/8≥1/32

   for all sufficiently large N. Thus killing alone supplies a uniform negative bound in this region.

3. For a≥epsilon N, |(b_N−d_N)W'|≤C/N and the Taylor remainder is O(N^−2). Meanwhile

       (a)_3/(a+s)^3
         =[(1−1/a)(1−2/a)]/[1+s/a]^3 →1

   uniformly, because s/a≤epsilon^−1 N^−1/4→0. The exact generator is therefore uniformly negative here too.

Taking the minimum of the three eventual margins proves Q_N W≤−c0 with fixed c0>0 on every shell state.

## Dynkin and Green consequences

Apply Dynkin's formula up to t∧tau_kill, with cemetery value zero. Nonnegativity of the surviving terminal value gives

    c0 E_a[t∧tau_kill]≤W(a).

Each fixed-N killed chain is finite with finite rates, so this stopping argument is legitimate without an explosion issue. Monotone convergence gives

    E_a[tau_kill]≤W(a)/c0≤N^−9/4/c0.

This proves absorption directly; it does not assume it from a mixing estimate. Every Green diagonal is bounded by its row sum, hence G_N(i,i)≤C N^−9/4. The previously audited rank-one killing inequality then gives

    G_N/(1+6G_N(2,2))≤G_N^(+kill6)≤G_N.

Its relative loss is at most 1+O(N^−9/4), uniformly over all entries. Combining with the independently checked O(N^4) positive-forest comparison yields two-sided shifted Green bounds with exponent D=4 after enlarging a fixed constant to include finitely many smaller N.

## Scope

The result concerns killing by the specified clearing reaction with the common (B)_4 factor removed. Restoring that positive factor rescales physical absorption times by its reciprocal. No conclusion about conservative mixing, full connector feedback, or global recurrence follows. The suggested degree-D generalization is not required for this audit.

Reviewed source SHA-256: `6a11586481401f3f66dcd68b5f7916a768b212e91ea46b4cf04c3f1008131f6c`.
