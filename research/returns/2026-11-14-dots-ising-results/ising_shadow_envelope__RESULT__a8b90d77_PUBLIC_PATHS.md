# Periodic walk envelope: a rigorous frozen-shadow counting lemma

This proves the counting component of fluid's intermediate-diagonal bootstrap proposal. The separate actual-wall-to-one-strip pin-lift interface must be established before applying it to the Ising source. No source clock or transition rate is modified.

## 1. Periodic walk
Let v(t) be a nearest-neighbor doubly infinite walk with period T in time and v(t+T)=v(t)+(L,L). In one period it has W west steps, S south steps, L+W east and L+S north steps. Assume W<L. Put b=W+S=(T-2L)/2.

For the half-integer vertical cut j+1/2 define
 U_j=max{y(t):x(t)<=j}, V_j=min{y(t):x(t)>=j+1}.
These extrema are finite, U,V are nondecreasing, and U_(j+L)=U_j+L, V_(j+L)=V_j+L. Each cut has an east crossing, hence U_j>=V_j.

A GOOD cut has no west crossing in the entire lifted walk. Its east crossing is unique, all left visits precede all right visits. For any forward-time interval the net y displacement is at least -S: remove complete periods, each of which adds L, and the remainder has at most S south steps. Therefore U_j-V_j<=S.

For a BAD cut, choose times realizing U_j and V_j. If the left extremum occurs first the same bound S applies. Otherwise the segment from the right extremum to the left extremum has nonpositive net x displacement. It cannot contain a complete time period, because any interval of at least T steps has x displacement at least L-W>0 (complete periods plus a remainder). Thus its y rise is at most the total north count L+S, so U_j-V_j<=L+S.

There are at most W bad cut residues moduloL: every bad residue must be crossed by a west step in the period. Consequently

  sum_(j=0)^(L-1) (U_j-V_j) <= L(W+S)=Lb.

This is an injective geometric envelope estimate, not a count of walk labels or a probabilistic independence assumption.

## 2. Frozen sites within one lattice spacing
Let C be a diagonally periodic pin set in the SAME lifted strip, with every c in C within L-infinity distance1 of this particular walk lift. Define its NW/SE quadrant hull H: a site (j,y) is in H only if some C site lies northwest (x_c<=j,y_c>=y) and some C site lies southeast (x_c>=j,y_c<=y).

The northwest pin gives y<=U_(j+1)+1; the southeast pin gives y>=V_(j-2)-1. Thus the number of hull sites in column j is at most

  U_(j+1)-V_(j-2)+3.

Sum over one period. Monotonicity and diagonal periodicity imply
 sum[U_(j+1)-U_j]=L,
 sum[V_j-V_(j-2)]=2L.
Therefore

  |H per diagonal period| <= Lb+6L.

Using 8L instead of6L is conservative. This pays the vertex-versus-half-integer cut indexing explicitly. One must not apply U,V to ALL horizontal/vertical translates of C at once: then extrema can be infinite. The chosen single-strip lift is essential.

## 3. Conditional bootstrap application
Suppose a finite-transverse-width diagonal strip is bounded by plus sites, and contains frozen sites C as above. Run maximal two-neighbor plus bootstrap on all other sites, in a deterministic queue order. Let M be its final minus set. A free site in M has at least three minus neighbors.

If p in M had no pin northwest, intersect M with the northwest quadrant of p. This set is finite: in that quadrant, both y-x and the strip's transverse width bounds restrict x,y. Maximize y-x there. Its north and west neighbors cannot lie in M, and remain in the same quadrant. The maximizing site is not pinned, contradicting bootstrap stability. The southeast argument is identical with the opposite linear function. Hence M is contained in H and

  |M| <= Lb+6L.

For p=T<2.5L, b<L/4. At L>=24 this guarantees |M|<L²/2, so the reference reaches majority. This is a native monotone ordering (queue additions each have two plus neighbors), but by itself does not prove the source-dependent actual wall's pins satisfy the single-strip hypotheses, that its label remains visible, or that every prefix has the mincut/loop-erasure properties needed by a strong thermal partition bound.

## Scope boundary
The key unproved import for the full Ising construction is: lift the complement of the main physical-plus collar into a strip, and show ALL frozen visited-plaquette pins in that strip belong to the one adjacent collar-walk lift, with no bounded-pocket pins or second unrelated pin band. Existing adaptive visibility arguments suggest this, but a statement about arbitrary pins near an arbitrary torus walk is insufficient. No intermediate-diagonal occupation theorem is asserted solely from this note.

## 4. Frozen initial bounded pockets and perpendicular births

The proof in Section3 only needs the rule that a free site with two PERPENDICULAR plus neighbors may be filled: the extremal witnesses have N/W or S/E neighbors. Opposite-pair births are unnecessary for the hull-majority conclusion.

Initial bounded components of the artificial8-complement of D may be retained with their arbitrary actual bits, rather than physically filled. Each such pocket lies in H(D): vertical north/south rays from its sites first meet D, since the pocket is bounded and its physical-neighbor boundary is D. Moreover H(D) has exactly the same monotone envelopes as D. Indeed y<=U_D(x) and y>=V_D(x) for a hull site, and monotonicity shows that adding such sites cannot raise any U or lower any V. Therefore treating every initial bounded pocket site as unavailable does NOT enlarge the thickened-walk envelope or its Lb+6L bound.

This is a geometric area statement, not a free change to the source. Actual pocket bits stay fixed. For the conditional weight ratio, their terms cancel only if the processed essential component has no physical adjacency to them; distinct initial8-complement components supply that separation. Their algebraic replacement by plus in numerator and denominator belongs to the inherited pin-cancellation argument, not to the native dynamics.

## 5. Prefix minimum-cut lemma for a two-neighbor reference order

Fix initial plus set D and any reference additions v1,...,vk, each with at least two physical neighbors in D or among EARLIER additions. Fix all other spins minus (or retain any additional fixed plus boundary that was included in the reference test). At a prefix F, the all-plus assignment on F minimizes physical perimeter over all assignments on F.

Proof: any alternative removes some T subset F. Remove those vertices in reverse reference order. At removal, every earlier plus neighbor that justified the original birth is still present: earlier T vertices have not yet been removed. Therefore the removed vertex has at least two plus neighbors and its removal changes perimeter by 2k_plus-4>=0. Sum these nonnegative increments. This is an exact native-graph statement, with no planar/topological assumptions. A positive uniform field also favors the all-plus reference.

Consequently the total wall length of any conditional thermal preimage is at least the total reference wall length (gap0) for an all-two-neighbor order. This does NOT imply that the essential-wall length alone has that lower bound: contractible walls may carry part of the excess. A connected-essential-pin or alternative paid decomposition is still required before inserting this fact into a one-essential-loop partition estimate.

## 6. Final integrated diagonal review

Read the final SINGLE_PIN_BAND, CONSTRUCTION, CONNECTED_MINUS_REPAIR and PAID_PARTITION notes in `ising_intermediate_diagonal_20261113`. The previously flagged single-pin-copy premise is now supplied explicitly: a main-plus lift cannot carry independent homology because it would cross the actual wall/minus collar; its copies are NN separators. The connected left8 pin trace is locally attached to its own separator and cannot cross an intervening one. Thus the chosen right strip contains only the next copy's left pin band. Initial bounded pockets project into the same periodic envelope, not an additional copy of its area.

The connected-minus ordering retains frozen initial pockets and the essential pin band. Any newly detached component is contractible: two essential minus components would contradict the retained NN-connected essential plus set. The transverse gate functional permits recursive removal of a pin-free pocket before its articulation gate, preserving8-connectivity at each accepted step. This supplies the connected pin sets needed for thermal loop erasure, not merely the majority-size bound.

Independently checked the paid partition:
- Every compatible preimage has perimeter at least the all-plus prefix by Section5. After contractible pin-free loops are erased, the same bound applies to ESSENTIAL moving perimeter.
- Other moving essential cycles are an odd number of parallel diagonal loops, each length at least2L.
- One-loop and at-least-three-loop bounds use the certified diagonal nonbacktracking witness; all unmarked contractible pressure remains paid.
- Visible actual diagonal label count is at mostL, since each uses at least2L of at most2n physical disagreement edges. Both endpoint ratios and n coordinate cuts give804 n² L, matching the scalar.
- The negligible three-loop contribution uses b0<1 and exp(b0)/6<1; its absorption into the common402n factor is safe since rho/2>1.
- The original optimized-capacity receipts are imported without changing source, core, cutoff, r, clock, target or voltage.

Reran final paid_scalar.py and union_receipt.py successfully. Paid intermediate exponents are48,441,3197,34696; union with the arbitrary-defect total-diagonal-perimeter tail gives47,219,1302,13567 at R80,200,1000,10000.

Final verdict: no new gap found in the integrated exactly-two-actual-diagonal-wall sector proof under the inherited adaptive physical-plus/digital-separation lemmas. This is a broad source-sector occupation estimate, NOT full residence closure. No-essential-wall states remain outside it; the whole no-essential class contains the core and cannot itself have exponentially small occupation. No novelty or civilization-level consequence is established by this review.

Executed order diagnostic: order_check.py found140 actual nongeodesic diagonal cases on8x8;2097 reference births, all preserving essential-minus8-connectivity, no stalls. Initial bounded components were frozen, not filled or counted as plus. This supports the interface but is not used in place of its proof.
