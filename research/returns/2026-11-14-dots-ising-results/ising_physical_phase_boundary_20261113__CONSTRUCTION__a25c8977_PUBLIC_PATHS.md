# Actual physical phase boundary with a visible label

Coordinated candidate: fluid owns adaptive physical encoding and visibility/geometry; quantum owns the final mixed-partition bound; GKP independently reviews right-only growth. This document states the interfaces explicitly. It does NOT identify auxiliary triangulation with the original fixed core definition.

## 1. Deterministic physical-plus resolution
For each physical plaquette with corners a,b,c,d in cyclic order, choose the a-c diagonal unless both a,c are plus and the plaquette is not all plus; in that case choose b-d. All auxiliary diagonal couplings remain ZERO. Thus no selected diagonal in a mixed plaquette is plus-plus.

This is only a canonical decomposition of the physical disagreement edges. It changes neither the Hamiltonian, native transition rates, original core A, soft clock, nor voltage. At checkerboards it resolves around physical nearest-neighbor plus components, rather than joining diagonal-only plus components.

Let gamma be a noncontractible cycle in this auxiliary wall decomposition, oriented with plus on its right. Its physical length is p. For the intended quantitative family require p<=L+R at L=8R; this forces axial homology. All other spins of the actual source remain arbitrary.

## 2. Physically connected plus collar and its perimeter
Let D be the plus endpoints of the augmented edges crossed by gamma. Inside a visited triangle the two plus endpoints are equal or joined by the triangle's third edge. If that third edge were a plus-plus diagonal, the plaquette would be mixed with a selected plus-plus diagonal, excluded by construction. Therefore the plus endpoint walk uses only PHYSICAL nearest-neighbor steps (and stationary steps). It is homotopic to gamma, so D is NN-connected and contains a physical winding cycle.

The weighted triangular turn identity yields exactly p physical steps in this closed plus-side walk: its diagonal-step count is zero and the essential turn sum is zero. Equivalently apply the general collar lemma reviewed by quantum. The underlying connected NN graph contains a cycle, hence internal NN edges >= vertices. Consequently P(D)<=2|D|<=2p. Repeated walk steps do not invalidate this argument; distinct vertices are at most step occurrences.

The minus endpoint walk is8-connected and essential. On the narrow lift cylinder it lies on the opposite side of the NN winding plus collar. Its entire trace therefore belongs to the left8-minus component of the artificial complement of D, after orienting the two sides consistently. This uses digital planar separation, not an assertion about the actual arbitrary exterior spins.

## 3. Right-only monotone construction
Use GKP's independently reviewed right-only two-neighbor bootstrap: freeze the artificial left8-minus component of D, and add eligible sites on the other side up to xmax(D). The turning argument forces completion of the rightmost column while preserving every edge of the left wall. Then grow consecutive columns to the right until first B.

All reference additions have at least two plus neighbors during bootstrap, so P(reference)<=P(D). Later partial columns add at most2 perimeter edges. The physical length of gamma remains p; hence all OTHER reference walls together have length at most p+2.

A wall of length p and axial displacement L has horizontal span at most(p-L)/2, plus at most constant collar padding. With p<=L+R this is much smaller than L/2. The bootstrap and subsequent half-band sweep therefore fit in a proper lifted strip; periodic copies of frozen collars are not encountered before majority. Actual extra plus spins merely cause skips, and every path stops at its first actual B visit.

## 4. Why the adaptive label remains visible
Pinning only triangle vertices is insufficient to justify a state-dependent diagonal rule without discussion of the fourth bit. Here all vertices of every plaquette visited by gamma remain unchanged:

- Main plus endpoints are in D and never changed.
- Minus vertices lie in the left8 component and never changed.
- An extra plus vertex not on the main plus endpoint walk can occur only as the opposite plus corner of a checkerboard. Geometrically this vertex is outside D and shares a plaquette with the true minus collar, so it lies in the artificially frozen left8 component. Its ACTUAL plus value is retained, not overwritten.

Thus recomputing the deterministic physical-plus resolution at any path endpoint gives the SAME gamma as an actual closed wall component. No other wall can merge into a fully retained closed component. At a fixed endpoint there are at most2n/L=2L noncontractible physical wall cycles, since all physical disagreement edges together have length at most2n. Canonical root choice avoids duplicate root labels.

## 5. Conditional partition: freeze the label's encoding, not the model
For a fixed edge and visible label gamma, the geometric order and processed prefix are determined. Unprocessed source spins are physically readable at the endpoint; only processed bits are summed. Boundary monotonicity may replace unknown exterior spins by minus for a weight-ratio upper bound, preserving D and the crossed-triangle pins.

During this conditional estimate choose ONE fixed auxiliary triangulation extending gamma's local choices. Do NOT recompute the adaptive rule separately for every reconstructed thermal source. The fixed local crossed-triangle vertices keep gamma an exact cycle; arbitrary choices elsewhere merely encode the same physical energy. There is no2^n triangulation label sum.

Drop the nonpositive field ratio on the original prefix. Remove gamma's unchanged length p. All remaining wall sets have at least one other noncontractible wall of physical length>=L (their total mod2 homology must cancel gamma). Reference remaining length<=p+2. Hence the same positive full-wall-set calculation gives the proposed per-endpoint bound

 J_p = exp(4theta) exp[2theta(p-L)]
       *100n 3^L/(1-q) *exp[100n q^4/(1-q)], q=3exp(-2theta).

All islands and other winding walls remain in the pressure factor. The original coordinate-current lemma then bounds the entire source family by4nL J_(L+R) C_kappa, provided the geometry/visibility interfaces above are accepted. This is a pointwise fiber sum, not a Gibbs-source-current substitution.

## 6. Executed diagnostics
check.py exhaustively enumerated all65536 spin states on4x4. Across39872 noncontractible adaptive wall cases, every plus collar was physically NN-connected and winding, and P(D)<=2p always held.

pinned_closure.py additionally pinned ALL vertices of ALL visited plaquettes. Across20480 short axial cases p<=L+2, native two-neighbor closure had ZERO failures to acquire a full plus line. This directly contrasts with the fixed-resolution counterexamples; it does not erase those valid counterexamples for the different construction.

## Honest scope
The source family consists of actual physical-plus-resolution winding walls of bounded p. It is not all winding under the original augmented connectivity, not every non-target configuration, and not a total residence theorem. The original core/capacity remain exactly unchanged. Final quantitative receipts and a separate review of the collar-side/visibility topology are still required before promoting this candidate to the delivered theorem package.
