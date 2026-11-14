# Single-band lift interface for diagonal collar closure

This records the digital-topology interface under independent review. The adaptive actual-wall plus4/minus8 conventions are essential.

1. The main plus collar D is physically NN-connected and contains a diagonal essential NN cycle. It cannot contain any independent-homology NN cycle: such a plus cycle would intersect the actual essential minus8 collar of gamma, impossible for disjoint NN-plus/8-minus sets on the torus. Thus its lift components are periodic under(L,L), and distinct translates by(L,0) are disjoint NN components.

2. In the diagonal cylinder, these lift components are ordered essential NN separators. The complement has the essential8-connected strips between adjacent copies, as well as possible bounded pockets. Select the growth strip immediately RIGHT of D0, bounded on its other side by D1=D0+(L,0).

3. Every unavailable visited-plaquette vertex outside main D is in the essential LEFT8 side of its own D copy. This includes all actual minus endpoints and every extra fourth-corner plus pin: the latter connects by an8-step inside the visited plaquette to the minus collar, without entering D. The entire unavailable pin band is8-connected and essential.

4. A pin band on the left of Dk belongs to the immediate-left strip, not a strip beyond another copy. It is locally attached across an actual wall edge to Dk, and an8-connected set cannot cross an intervening essential NN separator. Being essential, it cannot be confined to a bounded pocket. Therefore the chosen right strip of D0 contains only the pin band associated with D1. It contains no pin band from D0 or another translate.

5. Every pin in this one band is a vertex of a plaquette incident to the main trace D1, hence within L-infinity distance1 of that trace. The trace-hull bound can therefore use ONE periodic trace. Using both D0 and D1 as pin sources would incorrectly produce an O(n) hull even in the geodesic case.

Initial bounded complement pockets are retained, not filled natively. Their vertices lie in the NW/SE hull of their enclosing D copy. On projection to the torus, all translated copies of that hull coincide, so these pockets and the remaining right strip are contained in ONE projected thickened hull, not the sum of separate area bounds. The projected area is no larger than the lifted per-period area, even if there is overlap.

This interface invokes standard NN/8 digital separation, but does not replace it with ordinary planar same-connectivity separation. All auxiliary contour choices remain those of the actual physical-plus encoding; no new source class is introduced.
