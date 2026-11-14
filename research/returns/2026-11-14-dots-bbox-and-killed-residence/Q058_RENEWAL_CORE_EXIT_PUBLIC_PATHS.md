# Hard-source renewal: a rigorously rare departure, not a bounded mean

Let a be all-minus, B first majority, λ_a=n/(1+exp31.96), and ν the uniform singleton law after leaving a. Write τ=τ_{a∪B}. Standard regenerative occupation, or Green-function reversibility, gives

N*/w(a)=1+λ_a E_ν τ,
C*/w(a)=λ_a P_ν(τ_B<τ_a).

These formulas refer to the hard-source capacity and numerator, not the original soft-source quantities.

## Occupation inside the acquired box18 core
Let A18 be the explicit core sampled by CompactPerimeterCore. Its exact normalizer satisfies Z18/w(a)≤exp Γ, Γ<7.948e−7. Since the hard equilibrium potential h_a lies in[0,1],

λ_a E_ν[integral until τ of 1_{X_t in A18\{a}} dt]
 = sum_{x in A18\{a}} w(x)h_a(x)/w(a)
 ≤expΓ−1.

Thus all core excursion occupation contributes less than8e−7 to the normalized numerator. The remaining issue is occupation OUTSIDE A18, not the common quick singleton extinction.

## New constructive exit-probability bound
A first A18 exit is an addition at a gate; deletions cannot increase component boxes. The newly connected augmented plus component S has a consistent lift in[-18,18]^2 around the gate: each old box18 component touching it has a neighbor at coordinate offsets at most1 and side spans at most17. The union's width in each coordinate is≤37<L, so winding is impossible. Since S exits box18, at least one side width is≥19. Augmented connectivity implies every intermediate row/column is occupied, hence its PHYSICAL perimeter P≥2(width+height)≥40.

For any such S, area/P≤37/4, so E(S)=8P−.04 area≥7.63P. The perimeter coding used in perimeter_core.py extends to this37-wide lifted box with the SAME128-letter alphabet: 16-bit headers encode each cycle's initial cell offset in[-36,36]^2 and its side, requiring73²·4=21,316<65,536 labels. Four symbols per cycle suffice; cycles have length≥4. Canonical root translations contribute n. Therefore the weighted sum of eligible components is at most

T = n sum_{P≥40}(128 exp(−7.63))^P.

This sums even impossible perimeters and codes, harmlessly. No execution of the box37 decoder is claimed; the header/code extension is a counting injection.

Remove S from the post-addition configuration. The remaining configuration Y is in A18, because it consists of unaffected old components. It is augmented-nonadjacent to S. For the old X and new X'=Y∪S, native detailed balance gives

w(X) q(X,X') = w(X') q(X',X) ≤ w(Y)w(S)/w(a).

The pair(Y,S,gate) must retain a gate multiplicity: a component S can have up to |S|≤1369 possible deleted gates. Therefore the total stationary outward flux satisfies

Flux(A18,A18^c)/Z18 ≤1369 T.

This explicit gate factor is essential; omitting it would incorrectly identify different boundary edges with one component.

The expected number of outward crossings in one singleton excursion is bounded by Flux/(λ_a w(a)), since h_a≤1. In particular,

P_ν(exit A18 before hitting a or B) ≤ (Z18/w(a))·1369 T/λ_a.

For a simple rational certificate use128 exp(−7.63)<1/15, giving T≤n·15^−40/(1−1/15). This is conservative and independently checkable by a finite Taylor lower bound for exp7.63.

## Limitation that remains decisive
A very small exit probability does NOT bound the mean occupation after exit. The rare escaped excursions may be extremely long. A completed numerator theorem needs a paid conditional duration/return estimate, or an unbiased tail-reward method with controlled work and variance. Capped singleton runs cannot substitute for it. This result isolates where the missing mean-duration work resides; it is not a first-passage solution.
