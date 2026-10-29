# One tall input, exact receiver and strongest same-input analytic route

30 October 2026. This is a constructed channel-design computation, not measured population data or a device.

## 1. Locked source and objective

The reference and target action labels are

    L = [3/5  1/5],   y=(0,1/2,1).
        [1/5  3/5]
        [1/5  1/5]

Input i is 0 or 1 with uniform prior. The linear design cost is sum_yi K_yi(y-i)^2/2. The budget is c=1/2, entry floor kappa=1/1000. L has three nonproportional output rows, rank2<3, so the previous square inverse is absent. No rows can be merged as proportional likelihood outcomes to give a lossless square experiment. The generic reduction does not need this last observation to be valid.

The source pencil order is6, target order4 and Choi order24. The 3 selfadjoint variable families X,Y,Z retain arbitrary complex references. There are 300 independent real Choi coordinates and6 channel entries; the 28 chosen scalar equality rows have rank28. The constant R block is eliminated during numerical acquisition and rebuilt exactly for qualification.

## 2. Paid proposal, exact repair and result

acquire_general.py compiles the ordinary SDP and uses CVXPY/CLARABEL only to propose K,C and dual multipliers. The numerical proposal is saved before exact repair. A rational roundoff followed by an exact affine correction, supported on an explicitly computed pivot-column set, restores every coefficient equality and stochastic column sum. Mixing by 1/4194304 with the explicit constant baseline makes the rounded certificate strictly positive; that FIRST tested mixture passed exact LDL for both C and R. No target, floor, budget or cost was changed.

CERTIFICATE.json contains the resulting rational K,C,R, multipliers and all failed/successful repair trials (here only that successful primal trial). The certified global cost interval is, outward to the displayed decimals,

    [0.2360470726074909, 0.2360471157316787].

The exact rational gap is less than 4.313e-8. Printed floats in the JSON are diagnostics; the rational strings and exact identities/sign checks govern.

The global lower bound is NOT the numerical solver objective. Let lambda multiply the exact equality rows A v=b and let Y>=0 be a rational repair of the R-PSD dual. For a feasible point,

    objective >= objective + lambda*(A v-b) - Tr(Y R).

Eliminating R=B0(K,c)-Phi_C(A0) leaves a constant, a linear coefficient W_yi of K, and Tr(M C). Exact LDL proves Y>0 and M+delta I>0 with delta=2^-40>=0. The constant identity gives Tr C<=15/2. Therefore Tr(M C)>=-delta*(15/2). The minimum linear K cost over each stochastic column with the SAME floor is exactly

    kappa sum_y W_yi + (1-m kappa) min_y W_yi.

Adding these terms gives the saved rational lower bound. This argument allows nonzero dual residuals and does not trust approximate stationarity or floating eigenvalue signs. receive_general.py recomputes it from SOURCE/CERTIFICATE, rebuilds FULL constant/X/Y/Z coefficient matrices and checks rational LDL. Its generic qualification arithmetic uses no solver; the appended analytic comparator is explicitly gated to this locked source.

## 3. Exact private classical implementation

The returned K has a common per-column denominator D=27670116110564327424=3*2^63. receive_general.py constructs the cumulative integer ticket ranges and checks all12 endpoints/adjacent boundary tickets. IntegerRelease.draw(i,randbits) repeatedly requests a FRESH independent uniform65-bit word, rejects words>=D, and maps the remaining word to the corresponding output range. It realizes the rational K exactly under that explicit ideal-fair-bit contract. Expected bit cost is260/3 per release, and rejection probability per attempt is1/4. Worst-case attempts are unbounded with a geometric tail. No random draws, quantum references or population samples were made in this computation. A PRNG execution or physical entropy source is not automatically an exact private fair-bit implementation.

## 4. Strong ordinary analytic optimum on the SAME source

This binary source is deliberately compared with the full source-aware analytic route, not only an L-output postprocessing LP. Binary inputs imply Q2=I-Q1; spectral calculus reduces the complete-reference Fisher comparison to its scalar t in[0,1] version. Symmetry averaging preserves feasibility and cost. Thus some optimum has

    K = [ tau(1+r)/2    tau(1-r)/2 ],
        [    1-tau        1-tau   ]
        [ tau(1-r)/2    tau(1+r)/2 ]

with 0<=r<1. Put z=(2t-1)^2. The scalar Fisher ratio is

    tau*r^2/(d^2*s) * (s^2-d^2*z)/(1-r^2*z),
    s=4/5, d=2/5.

Its maximum is5 tau r^2 if r<=1/2, and (15/4)tau r^2/(1-r^2) if r>1/2. The first region has cost>=1/4. In the second region the c=1/2 constraint gives tau<=(2/15)(1-r^2)/r^2 and the cost decreases with tau. The best possible improvement over1/4 is therefore the maximum of

    I(r)=(1-r^2)(r-1/2)/(15r^2).

I'(r)=(1-r-r^3)/(15r^3), so its unique maximum is at the unique root r* of r^3+r-1=0 in(1/2,1). The associated tau and every entry meet the SAME 0.001 floor strictly (the exact isolating interval checks it). Hence this is the GLOBAL optimum with the floor, not a relaxed bound or a heldout numerical estimate.

The stdlib receiver isolates r* by100 exact rational bisections and evaluates a rational interval containing

    cost*=0.23604707265357633...

It lies inside the general SDP receiver interval. This ordinary analytic method is faster on this source: its measured after-import arithmetic took0.0003796s, versus0.030606s for the full exact receiver, in addition to the SDP acquisition. There is no speed or generic-incumbent win on this executed example.

For completeness, any channel obtainable by postprocessing L alone has cost at least1/4, even without the information budget or floor. The three L outputs have posterior input-one probabilities1/4,3/4,1/2. Among the allowed actions0,1/2,1 every posterior's minimum squared risk is1/4. This separates the supplied RAW-X design operation from mere output postprocessing, but is not an advantage over the stronger raw-X analytic method just admitted. It does not imply a guessing/decision simulation order.

## 5. Resource boundary

ACQUISITION_COST.json records one numerical solve: compile0.015067s, numerical0.121600s, rational projection setup0.005409s, primal repair/check0.011422s, dual repair/check0.006869s, total after imports0.161659s; imports2.234126s; peak RSS140099584 bytes. The after-import timer includes saved source/proposal/certificate work up to the cost record, but excludes final cost serialization/printing. It is not the cost of mathematical discovery or literature review.

development/RECEIVER_first.json preserves the FIRST stdlib same-input qualification:0.030606s, peak RSS22691840 bytes, zero solver/reference/RNG queries. Its timer starts after module imports and excludes final receipt serialization. The small positive-shift guard correction found by the independent challenger leaves all scientific numbers unchanged. The literal final guarded receiver was then rerun on the SAME source/certificate, taking0.034835s with peak RSS22970368 bytes (ordinary comparator0.0004784s). GUARD_REPLAY.json confirms recursive equality of every scientific payload field after excluding timing/RSS. No source, solver or trajectory was rerun; this extra receiver run pays the actual acceptance-code change.

The unsuccessful earlier tall-obstruction search and its incomplete timing are retained in DEVELOPMENT.md and the original development artifacts. They are not omitted from the full research cost. This source supplies no calibration samples; physical L qualification and raw-X access remain unacquired.
