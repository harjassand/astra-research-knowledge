# Initial response, finite damage and transferable proof information

This parent construction independently tests the interaction branch's question. It is exact scalar-network/positive-operator mathematics, not a continuum-fracture or component-qualification claim. Star–triangle equivalence and convexity are established principles; external novelty of these particular constructions is not asserted.

## A matched local-law counterexample

Place three protected unit host springs between prescribed external coordinates and three internal ports. One hidden network is a Y with three unit spokes to an internal center. The other is a triangle with each edge stiffness1/3. Their full intact external Dirichlet-to-Neumann matrices are exactly equal: diagonal1/3 and off-diagonal−1/6. Thus every initial linear boundary loading has identical response and energy, not only two selected compliance entries.

Damage may delete any subset of the three hidden springs, paying the **same local rule** `Gamma_e=c_e/2` in both networks (unit critical-extension parameter). Host springs remain protected. This does not freely assign different toughness to obtain the result. Hidden material budget/topology is not assumed separately observed or equal.

For external displacement `(t,-t,0)`, intact energy is `t^2/2` in both. Exact elimination of all internal variables and all seven nonempty damage sets gives first global energetic thresholds

`t^2 = 4/3` for Y, versus `t^2 = 2/3` for the triangle.

At `t=1`, Y has no energetically favorable allowed break set, while the triangle does. The entire initial port response therefore does not determine this finite-damage decision, even with a matched local fracture-cost law and the same finite interacting host. `exact_network.py` uses only Fraction arithmetic and independently constructs the Schur response and every damaged minimum. Its full results are `EXACT_NETWORK.json` (.0021s). The claim does not transfer to homogeneous 3D penny cracks, prescribed internal topology, separately known material budget, or additional dynamic/nonlinear observations. Dirichlet control avoids an infinite dead-load release from complete disconnection; force-control transfer requires a coercive residual load path.

## What additional information does transfer

Suppose each admissible finite damage state d has release

`G_d(p)=p^T R_d p/2`, with `R_d>=0`, and cost `Gamma_d>=0`.

Under displacement control, linear elastic softening gives `R_d=Lambda_0-Lambda_d`; under coercive force control the corresponding form is the compliance increase. **Supply** proof information that the same intact state obeys `G_d(p_j)<=Gamma_d` for every admitted damage d and every proof load p_j. This quantified global energy information is stronger than observing an undamaged bulk loading curve.

For any `p=sum_j c_j p_j` with `sum|c_j|<=1`, the triangle inequality for the seminorm `||R_d^(1/2)p||` gives `G_d(p)<=Gamma_d` for every d. Thus the absolute convex hull of the proof loads is universally safe under these premises, regardless of interaction details. If a service point is outside that hull, a separating functional v gives an operator counterexample `R=epsilon vv^T`, `Gamma=epsilon/2`: all proof inequalities hold after normalizing `|v.p_j|<=1`, but the service inequality fails. This sharpness is for the unrestricted PSD release-form class, not a realization theorem for every crack geometry or matched local material law.

The homogeneous premise matters. With fixed bias/residual stress, balanced-hull transfer can fail: `G(p)=(p-1)^2` passes a proof at+1 but fails at−1 for a cost below4. If each biased release is convex, the ordinary convex hull of proof loads still transfers by Jensen. For an admitted PSD augmented form in `(p,1)`, applying the previous seminorm proof and restricting the last coordinate to1 gives precisely that ordinary convex hull: coefficients summing to1 with absolute sum at most1 must be nonnegative.

No physical proof stability, unchanged microstructure, fracture energies or safe loading envelope was acquired. Small compliance error alone cannot supply these quantified energy inequalities or a local-K bound. The useful next question is which experimentally obtainable stability information can support a finite service certificate without importing the conclusion as a premise. That acquisition problem remains open here.
