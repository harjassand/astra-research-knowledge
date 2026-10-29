# Bounded random bits, precision and ordinary-call interface
2026-10-29. Additive to frozen governing proof.

## Efficient approximate Haar twirl
The exact polynomial quadrature is a valid ideal finite construction, but its table need not be built. For each SO3 factor draw three independent b-bit uniform integers and use midpoint grids for alpha,gamma in[0,2pi) and z=cos(beta) in[-1,1]. This requires6b fair bits for A,B, with no rejection loop. Couple each grid draw to a continuous uniform draw in its cell. Put h=2^-b. Then angular errors in alpha,gamma are at most pi h, while |z-z'|<=h.

For beta,beta'∈[0,pi], |cos beta-cos beta'|>=2 sin²(|beta-beta'|/2)>=2|beta-beta'|²/pi². Thus |beta-beta'|<=pi sqrt(h/2). Telescoping the three known Euler rotation matrices gives ||A-A'||op,||B-B'||op<9sqrt(h). The nine-dimensional label action O=A tensor B consequently differs by at most18sqrt(h) in operator norm.

A unitary channel's half-diamond distance is at most the operator-norm difference of its unitaries. Thus N independent label transformations contribute at most18N sqrt(h). For qubit rotations corresponding to A and A', half-diamond is exactly half the SO3 operator-norm difference; the two corrective payload gates contribute at most9sqrt(h). Contractivity through the fixed estimator/measurement channel gives a total twirling error at most
 (18N+9)2^(-b/2) <=32(N+1)2^(-b/2).
This does NOT require the estimator to be continuous: the perturbed quantum input goes through the same fixed estimator channel, and the known corrective gates are compared separately. Choose an even b=2 ceil(log2(32(N+1)/delta_twirl)) to make this at most delta_twirl. Integer comparisons can select b without a logarithm oracle. Exact irrational grid rotations remain ideal known controls; their finite implementation is charged next.

## Explicit precision budget
Let tau_label bound the half-diamond error of each implemented nine-dimensional grid-label rotation; tau_measure bound each measurement implementation; tau_process bound the whole classical-outcome-controlled estimated gate map relative to the specified exact estimator; and tau_gate bound each of the two corrective qubit rotations. The finite implemented averaged gate has half-diamond error at most
 432/(m g_L²) +32(N+1)2^(-b/2)
 +N(tau_label+tau_measure)+tau_process+2tau_gate.
All quantities are upper budgets, not inferred from floating residuals. Known arithmetic/synthesis precision and routing must realize them. The finite estimator acts on finitely many rational count tuples, in fixed matrix dimension9; a specified deterministic tie rule is required. No free exact real computation or native hardware implementation is asserted. A separately acquired contamination-confidence failure probability is added as an additional bad-branch weight.

## Finite source-call cap without readiness bias
In the stated IID family the minus-flag probability is q=(8+eta)/18>=4/9. Waiting flags are independent of the normalized retained IID records, so conditioning on acquiring N records by a cap does not bias their normalized joint state. Expected calls are at most9N/4. Cap one fresh acquisition attempt at L=ceil(9N/2) ordinary calls. Markov gives abort probability at most1/2. Discard incomplete records/statistics and retry from fresh IID uses at most r times; total call cap rL, abort<=2^-r. A successful batch feeds exactly the same estimator-state law as above. This readiness statement fails for arbitrary source memory; it is not imported from marginal flag frequencies alone.
