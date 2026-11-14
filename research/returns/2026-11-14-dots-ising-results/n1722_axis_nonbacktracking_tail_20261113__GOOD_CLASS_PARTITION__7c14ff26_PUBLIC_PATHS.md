# Paid nonbacktracking partition for a canonical wide-wall success class

## Status
The partition calculation, finite receipts, and geometric implication from the conservative area condition have been independently reviewed by fluid and GKP. This is not a frozen-package addition. TWO_AXIS_SECTOR.md states the resulting restricted sector closure, not the full exit theorem.

## The important distinction
Fix an actual axial wall gamma and its deterministic geometry-only right-only bootstrap, followed by straight columns UP TO A SAFE PERIODIC-PIN CUTOFF. This reference order need not reach majority from its thin reference collar alone. Define GOOD sources as those whose ACTUAL upward path reaches the original B before the cutoff. Such sources have valid target-ending paths. Extra source plus bits cause skips as before.

In the congestion estimate, all erased-bit assignments may still be summed: some of those overcounted assignments would not be GOOD, but a positive overcount only raises the bound. Therefore uniform completion from the thin reference is unnecessary. The geometric schedule, local pin preservation, essential connected conditional pins and the prefix minimum-cut gaps are necessary.

For p<=2.6L+8, transverse collar width is at most.8L+6, leaving a proper safe strip at the stated finite sizes. During reference bootstrap the mincut gap is0; during permitted straight prefixes it is at most2. The moving reference perimeter obeys m<=p+2. Frozen-region cancellation and per-prefix fixed auxiliary triangulation are exactly those in the reviewed short-wall theorem, provided the safe cutoff keeps their geometric premises.

## Nonbacktracking one-/three-loop bound
Use rho13/4, v3/2 and the exact rational axis-walk certificate in RESULT.md. Let z=rho exp(-8), A=100nq^4/(1-q), q3exp(-8), and

    b_NB=200n v^(-L) z^L/(1-z).

The fixed gamma forces every other essential contour to have the same axial homology. After removing contractible loops with connected essential pins, their total length obeys the actual pinned minimum-cut floor. Therefore the earlier ONE-versus-at-least-THREE split now gives

    J <= exp(A+8m) *
      [200n v^(-L) z^max(L,ceil(m-2))/(1-z)
       + b_NB^3 exp(b_NB)/6].

This is a bound on all thermal preimages, not just on one path's energy. With p<=2.6L+8, the >=3-loop term after reference multiplication is below1 at all four finite instances: its logarithm is at most

    3 log(201n)+81-.878L < 0.

The ONE-loop term yields

    J <=402n exp(16) rho^p v^(-L) exp(A).

Actual visible labels and coordinate-current cuts give the same bound N_GOOD<=4nL J C_kappa. The conditional scalar receipts are VACUOUS at R80 and R200, but give

    R1000: N_GOOD/ZA <=exp(-140),
    R10000: N_GOOD/ZA <=exp(-4358).

No unsupported positive claim is made at the first two instances.

## Remaining coverage implication
To combine with failed-both-area pruning, the independently reviewed AREA_ADMISSIBLE_COMPLETION.md proves that the geometric swept template contains at least its signed-area clean-completion volume minus the actual interior hole count, with correct pin padding. If that conservative count reaches majority, the actual source is GOOD. Merely observing a small energy barrier does not prove this implication. Large holes, other homologies and other topologies remain separate unless explicitly controlled elsewhere.
