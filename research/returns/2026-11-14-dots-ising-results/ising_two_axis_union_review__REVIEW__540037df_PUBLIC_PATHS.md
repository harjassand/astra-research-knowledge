# Independent review: unrestricted-defect two-axis sector

## Reviewed interfaces

At the two large instances R1000 andR10000, the following SIX positive branches cover all original non-target configurations with exactly two actual axial essential physical walls, with NO restriction on contractible filled areas:

1. Actual full plus row/column: existing full-line bound.
2. Actual essential wall p<=2L-8: existing actual-wall bound.
3. Total essential perimeter Pw>=4.6L: nonbacktracking tail permitting arbitrary other walls.
4. In the remaining range, at least one filled contractible area>4R²/3: independent marked large-hole bound.
5. Otherwise every filled area<=4R²/3 and either conservative area-completion condition succeeds: existing GOOD transport.
6. Otherwise both conservative conditions fail: enlarged-cutoff marked-cover/thermal pruning.

Branches may overlap, but only a union upper bound is used. After branches1–3 are removed, both essential lengths exceed2L-8, Pw<4.6L and thus Pw>=4L-16 and each p<2.6L+8. These are precisely the large-hole lower-length condition, the GOOD upper-length condition, and the failed-completion interval (contained in Pw<=4.9L).

The area-admissible geometric schedule is not an assertion that every reference thin collar grows to majority. GOOD is restricted to actual sources whose actual upward path reaches B. The signed-area sufficient condition earns this; overcounting other thermal preimages in its conditional partition is harmless. Frozen bounded right pockets contain no opposite essential wall and retained minus sites are charged to the actual hole count h. Raised area cutoff does not alter this geometry.

For the failed branch, common activities exp(-8P+8A/R), cover tilt12, and optimization over common-column width c are unchanged. The new kernel<2/5 and unmarked pressure<2 are independently certified. This pressure is below the old conservative pressure at both large instances, so retaining the old exponents12599 and125550 is valid. The corrected cyclic interval peeling removes the entire selected projection intersection and cannot repeat a contour.

The large-hole branch uses the global non-target field cap once and ordinary unmarked-loop pressure, not the field-enhanced small-hole activities. Its H threshold and all root/length prefactors are independently certified. This branch is valid regardless of how much area other holes occupy.

## Finite sum

The six negative exponents at R1000 are:
  full line10234; short actual wall3858; NB tail1432; large hole457; GOOD140; failed12599.
At R10000:
  full line105199; short actual wall41368; NB tail14856; large hole6265; GOOD4358; failed125550.

The imported short-wall receipt is stronger than GOOD at both instances. Thus six branches are bounded by6 exp(-140) and6 exp(-4358). Since6<exp(2), the same final exponents138 and4356 are retained. These are original voltage-weighted occupation divided by ZA, not a bound on full mean residence and not a new entrance distribution.

## Topological addendum, separate from exactly-two-axis statement

A wall collection bounding a spin set has an even number of essential resolved cycles. Disjoint essential simple torus cycles have parallel primitive homology. Four or more non-axis cycles force total physical winding perimeter>=8L. Four or more axial cycles with total<5L include a wall shorter than1.25L<=2L-8. Two cycles of primitive Manhattan norm>=3 force total>=6L. Thus the existing global>=5L tail and short-wall result cover these other essential-wall classes. Combining this addendum as an extra union branch requires7<exp(2), not merely the six-branch assertion (both are true).

The genuinely remaining topological classes are no essential walls and exactly two diagonal essential walls. No statement that these have small occupation follows here. Homology is that of ACTUAL walls, never a selected plus seed.

## Executed checks

Independently reran enlarged_certificate.py, raised_pressure.py, axial check.py, good_scalar.py, and north_compute's exact large-hole check.py; all passed. Reviewed the full primitive branch-interface notes and the area-admissible geometry import. This review does not independently reconstruct every earlier actual-wall theorem from scratch, nor establish literature novelty.
