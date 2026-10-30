# Exact joint conservative composition / phase / connector construction

Status: new internal construction; full boundary forcing not closed.

Use the rank-three network in the preceding obstruction proof. Put N=A+C and, for the connector core phases B=0,1,4, define

    h(0)=0, h(1)=1, h(4)=3, R=N−h(B).

The real connector cycle0→A+B→3A+4B→0 changes(N,B) by(1,1),(2,3),(−3,−4). Therefore it preserves R exactly on the phase cycle0→1→4→0. Conservative A/C reactions also preserve R. This is an actual finite growing shell, not a frozen N approximation.

Let T=R+3 and index its composition by a=A at phase4, C=T−a. The main neutral component contains

* phase4:0≤a≤T;
* phase1:3≤a≤T, with physical A=a−2≥1;
* phase0:3≤a≤T, with physical A=a−3≥0.

The possible phase1 state with physical A=0 is a separate isolated state for this restricted neutral generator and is NOT silently included.

Let sigma_T(a) be the exact conservative fast-shell stationary profile previously constructed. Unnormalized joint invariant weights are

    gamma_4(a)=sigma_T(a),
    gamma_1(a)=24 a(a−1) sigma_T(a), a≥3,
    gamma_0(a)=24 a(a−1)(a−2) sigma_T(a), a≥3.

Indeed the0→1 rate is1, the1→4 rate is a−2, and the4→0 rate is24(a)_3. Thus all three connector fluxes are exactly equal pointwise in the unchanged C coordinate. At phase4, the remaining adjoint is the fast conservative adjoint, which annihilates sigma_T exactly. No rates are averaged and no mixing/time-scale premise enters.

The normalization is of order T³. The fast-shell ratio bounds1/2≤P/Q≤7 imply likelihood-ratio domination of Binomial(T,1/3) by sigma_T, and hence E_sigma[(a)_3]≥(T)_3/27. The matching upper bound is immediate. Therefore the normalized phase0,1,4 masses scale as order1, at most order1/T, and order1/T³ respectively, with corresponding lower bounds obtainable from the same binomial comparison.

## Why the residual level matters
Freezing N leaves the dominant connector cycle hopping between different N levels; dropping those shifts can create adjoint terms of the same order as the purported spectral margin. The residual R keeps this entire neutral connector cycle inside one exact operator.

## Scope: this is not the whole neutral graph
When more B phases are included, additional connector cycles overlap this one. The correct finite-phase tree-degree offsets for the reflected phase graph through B=8 are

    h=[0,1,2,3,3,4,5,5,6].

For example1→2→5→1 is then also residual-level preserving and shares a phase with the first cycle. The three-phase formula above is not an invariant profile of that enlarged joint operator. The larger joint composition/phase shell must be solved as a whole, with all nonzero-R transitions treated as actual external killing/forcing. Fixed-slack tilts using the cruder maximal-source offsets fail in numerical tests; those failures are preserved, not silently discarded.
