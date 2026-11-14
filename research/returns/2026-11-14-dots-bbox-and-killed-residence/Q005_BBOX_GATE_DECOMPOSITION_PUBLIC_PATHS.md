# Constructive bbox gate decomposition: slow birth versus energetic merger

Status: deterministic geometric/energy lemma for ordinary plus components in a common contractible lift. Not a completed R200 global capacity bound. Existing delivered contour bounds use augmented filled domains and cannot be substituted without proving the matching geometry interfaces.

Let s(C)=w(C)+h(C), with a unique shortest lifted bounding rectangle. On the square Ising graph E(C)=8P(C)−t|C|, t=.04. Since P(C)≥2s and |C|≤wh≤s²/4,

 E(C)≥f(s):=16s−.01s².

For s≤H=800 this function is increasing and concave. The perimeter inequality requires connected ordinary plus components; filled domains require their matching contour convention. Distinct ordinary components have additive energy.

## Isolated gate
If adding one spin extends the bbox of just one old component, it has at most one neighbor in that component. If attached to no other old component, total k≤1. Reason: in an extended coordinate direction the new outer row/column was empty, leaving at most the inward neighbor. Hence ΔE=32−16k−t≥16−t. Native heatbath rate is at most exp(−15.96), NOT merely1. This statement excludes cyclic interval ambiguity, winding and merger gates.

## Merger gate
Suppose one new site joins r≥2 distinct ordinary components in a common lift. Their union with the site has bbox semiperimeter at most sum_i s_i+2: the coordinate projections of each component and the joining site form a connected family of intervals, so their union span is at most the sum of their lengths plus one in each coordinate.

If the new bbox exceeds H, then sum_i s_i>H−2. If every old component has s_i≤H and s_i≥2, monotonicity and concavity give

 E_old(affected components) ≥ f(H−2r)+(r−1)f(2),

for 2r≤H. This follows by first lowering the total to H−2 and then concentrating all available semiperimeter into one component while every other component remains at its minimum2. Real discrete geometry can only increase the bound.

At H800, t.04:
- r2: lower energy6431.80.
- r3:6463.56.
- r4:6495.24.

The continuous droplet saddle f(800)=6400. The r2 merger has at least31.8 additional energy, while an isolated outer-row birth incurs15.96. Thus the obvious fast k2 merger does NOT automatically erase the slow-birth advantage at the level of bare energy. Extra components can energetically pay for their faster transition.

## Global costs still unpaid
1. Entropy: sum exp(−E) over all shapes, placements, thermal backgrounds and merger configurations. Energy minima alone are not probability bounds.
2. Original source uses augmented plus connectivity and filled domains, not ordinary component boxes. Its at-most-eight affected outer-domain decomposition must be translated, not assumed.
3. Winding changes and torus shortest-interval ambiguity.
4. The complete majority target contains disconnected configurations; a target override or separate tilt bound remains essential.
5. R200 old trial's normalized source and reservoir terms remain unchanged unless explicitly re-established.

Promising next precise task: derive a marked multi-contour generating bound with separate r1 slow-birth and r≥2 energetic-merger sectors. Existing delivered magnetic polygon moments may control shape entropy, but their area/perimeter constraints must be replaced by compatible bbox or span constraints. No numerical e16 global improvement is claimed.

## Primary machinery consulted
Bovier, den Hollander, Spitoni, Homogeneous nucleation for Glauber and Kawasaki dynamics in large volumes at low temperatures: https://arxiv.org/abs/0806.0755 . Their potential-theoretic asymptotic result motivates critical-gate decomposition; it is not a finite-parameter certificate for this construction.
