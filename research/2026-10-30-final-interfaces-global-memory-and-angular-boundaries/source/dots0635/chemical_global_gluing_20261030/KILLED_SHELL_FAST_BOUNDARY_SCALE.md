# An actual boundary-layer absorption bound, not an assumed mixing scale

Status: new internal derivation, awaiting audit. For the killed growing shell Q_N in KILLED_SHELL_GREEN_COMPARISON.md, the crude polynomial bound can be replaced by

    sup_a E_a[tau_kill] ≤ C N^(−9/4)

for all sufficiently large N. This is an absorption bound, not a spectral-mixing claim.

Write b_N(a),d_N(a) for the exact conservative birth/death rates and k(a)=(a)_3 for killing. There exist fixed epsilon,c,C>0 such that

    b_N(a)+d_N(a)≤C N³ for all a,
    b_N(a)−d_N(a)≥c N³ for0≤a≤epsilon N

for all large N. The second assertion follows directly from the displayed homogeneous leading drift: at a/N=0 it is strictly positive, and falling-factorial corrections are O(N²) uniformly.

Put s=N^(3/4) and W_N(a)=(a+s)^(−3). Its first two derivatives satisfy

    W'=-3(a+s)^(-4), W''=12(a+s)^(-5).

Taylor's theorem for the jumps±1 gives

    Q_N W_N ≤(b_N−d_N)W_N'
             +C N³/(a+s)^5−(a)_3/(a+s)^3,

with adjusted fixed constants and all large N.

For a≤epsilon N, the first term is negative and absorbs the Taylor remainder because a+s→infinity. If a≤s it is bounded above by a fixed negative constant since N³/s⁴=1. If s<a≤epsilon N, the killing term is bounded below in magnitude by a fixed positive constant. For a≥epsilon N, the absolute fast-motion contribution is O(1/N), while (a)_3/(a+s)^3 tends uniformly to1. Hence Q_N W_N≤−c0<0 uniformly over the entire shell.

Applying the finite killed-chain Dynkin formula to W_N/c0 gives

    E_a[tau_kill]≤W_N(a)/c0≤C N^(−9/4).

In particular G_N(i,i)≤C N^(−9/4). The additional rate6 killing used in the neighboring-shell comparison therefore changes every Green entry by a factor between[1+C N^(−9/4)]^(-1) and1, rather than the earlier coarse N^12 factor. The shifted neighboring-shell Green comparison can consequently use a fixed polynomial exponent4 (up to harmless enlargements of constants), coming from the explicit forest-rate products alone.

The mesoscopic scale a~N^(3/4) was DERIVED by balancing A-creation at rate N³ against accumulated clearing hazard a³. It is not a supplied fast-equilibration assumption. The same calculation suggests the exponent D²/(D+1) for a degree-D one-dimensional conservative chain with positive drift away from a=0 and killing(a)_D, but that broader statement is not used here.

This bound still does not establish compatible forcing across the full N,B dynamics. It does show that the frozen-composition instability can be replaced by a concrete, rapidly absorbing stochastic boundary layer with controlled local Green comparisons.
