# Independent audit: structural fast-collar degrees and physical-shift corollary

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review. Reviewed UNIFORM_FAST_COLLAR_DEGREE_THEOREM.md and the added physical-shift section of MAJORITY_INSERTION_UNIFORM_GREEN.md.

## Verdict

The structural theorem passes under its explicit repeated-row hypotheses. It removes the need for separate two-row/three-row degree fixtures in the hard network for each fixed K and offset vector. The new macroscopic physical fixed-C/fixed-A corollaries also pass. They correct the scope of the earlier “not a fixed-C shift” summary: a fixed-C comparison is now earned when BOTH queried A counts are at least epsilon R, with constants depending on epsilon. No uniform epsilon-to-zero or near-identity conclusion follows.

## 1. Row-local low-phase elimination

Low phases have no horizontal transitions, so their eliminated block is confined to one row. Each induced fast-to-fast or fast-to-killing rate equals a sum of initial fast-to-low rates multiplied by probabilities of the corresponding low-chain exit. These probabilities lie in [0,1]. Consequently an induced rate cannot have larger asymptotic degree than the total initial fast-to-low rate, whose degree is at most D. A nonzero induced rate is positive rational and has a well-defined leading power. Since supports and original degrees repeat from row to row, its support and degree also repeat; different positive row coefficients do not change degrees. Fast horizontal degree-D edges are untouched.

This argument justifies the degree cap without assuming a phase mixing rate or diagonal dominance of a signed expansion.

## 2. Determinant and exact Green degree

After eliminating low phases, every outgoing edge has degree at most D. There are n=w|F| fast states. The killed determinant has degree at most Dn by its positive forest expansion. Orienting every phase's horizontal line toward one exterior collar boundary gives an admissible forest using n degree-D edges, so the degree is exactly Dn.

For an inverse entry G(a,b), every numerator forest has n−1 edges and contains the unique directed a-to-b path. Its total cost, defined by summing D minus edge degree, is at least the shortest path cost. Thus its degree is at most D(n−1)−dist(a,b).

The matching lower bound is valid. Choose a shortest simple a-to-b path. In each phase line, remove the selected path vertices and partition all remaining vertices into horizontal intervals. Orient each interval toward a path endpoint or an exterior boundary root. Every added edge has degree D. Such an interval cannot create a cycle: once it hits the selected path it follows that path to b, and the selected path never returns to a vertex outside itself. Intervals directed to the exterior terminate there. This completes the required two-root forest with a in the b-tree. Hence

    deg G(a,b)=−D−dist(a,b).

If a-to-b reachability fails, the inverse entry is zero instead.

Because horizontal motion has zero cost in both directions, any finite phase path can be realized at one row and followed by a horizontal move to the destination row. Conversely projection of any state path onto phase changes has at least the shortest phase cost. Therefore dist(a,b)=dist_phase(phase(a),phase(b)), independently of row positions and collar width w.

## 3. Boundary interface formulas

An entrance and an exterior horizontal exit each have degree D. Inserting the Green degree between them yields D−dist_phase(i,j), exactly as stated. For actual killing, the exit factor instead has degree d_j,*, producing d_j,*−dist_phase(i,j), maximized over possible killing phases. This is the displayed minimum-cost formula. The minimum is over phases with a NONZERO actual killing edge; if there are none, no actual killing rate is created by the Schur complement. Boundary exits used to ground the determinant are not silently counted as actual killing in this formula.

Self-return excursions are discarded. Existing direct retained phase edges do not spoil the result: their supports and degrees already match under insertion, and adding them to comparable Schur-generated rates preserves comparison. Every nonzero leading coefficient is built from positive finite forest/Schur expressions and is continuous and strictly positive on compact macroscopic cut intervals. Thus matching degrees genuinely gives constant-factor comparison. Constants may depend on w and phase width; only degrees/support are width-independent here.

## 4. Hard-network application for arbitrary fixed K and offsets

For K≥4, the low phases B=0,1,2,3 have no horizontal moves. Repeated immigration reaches B=4 or encounters a residual-changing kill, proving low-block transience. At every fast phase B≥4, both conservative composition directions have degree three and strictly positive interior leading coefficients. Other rates have degrees 0,1,3 and phase changes leave C unchanged. Arbitrary fixed offsets change which phase edges preserve residual, but not these structural statements. The hypotheses therefore hold for every fixed K≥4 and fixed integer offset vector, without relying on the three original fixtures.

## 5. Macroscopic physical shifts

For 0<epsilon≤1, A_x,A_y≥epsilon R gives C_x,C_y≤(1−epsilon)R+max_j h_j. A cut near (1−epsilon/2)R is above both queries by order R, so both lie safely below the removed rows and insertion fixes their C coordinates. The cut fraction remains in a fixed compact subset of (0,1), allowing the proven uniform comparison with an epsilon-dependent constant. The resulting map increases A by exactly one at both queried states.

Similarly, if both C counts exceed epsilon R, a cut near epsilon R/2 lies below them and insertion increases C by one while leaving A fixed. The comparison excludes the removed rows automatically because the separation is macroscopic. It does not cover two query states that cannot share either macroscopic-coordinate condition, nor provide control as epsilon tends to zero.

## Scope retained

This establishes exact joint killed-kernel transport and its stated macroscopic physical-shift special cases. Constant comparison is not 1+O(1/R); mesoscopic sectors, residual-changing excursions, forcing compatibility, and global feedback remain unresolved.

Reviewed hashes:
163b061869648683439a7ef6d4452f82708e397fa74de3128130b431c067f0d0  producer-workspace/UNIFORM_FAST_COLLAR_DEGREE_THEOREM.md
a09cafccf791899a448ced6a585457a66a2da17433f81bba2674a6fd3600ecb9  producer-workspace/MAJORITY_INSERTION_UNIFORM_GREEN.md
