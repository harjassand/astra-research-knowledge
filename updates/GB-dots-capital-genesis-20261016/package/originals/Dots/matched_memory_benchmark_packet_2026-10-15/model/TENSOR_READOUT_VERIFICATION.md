# Deterministic tensor-contraction fallback: verified algebra and implementation contract

## Result

The proposed tensor-product contraction is correct. It supplies a complete deterministic syndrome-only global recovery without Gaussian elimination or a minimum-surface solver. Keep the component-local box recovery as the primary branch and use this map only as its fixed global fallback. **Using the global contraction alone is a poor decoder:** some single-face faults become logical failures under its fixed seam convention.

Own exact Python checker: `check_tensor_readout.py`; output: `tensor_readout_checks.json`. No authors' code or dependencies were used. No stochastic memory trajectories were run.

## Maps and proof

All chains are over F2. For one periodic length-L factor, vertices v_x and edges e_x have d e_x=v_x+v_(x+1 mod L). Define

- h(v_x)=sum_(r=0)^(x-1) e_r; h(e_x)=0.
- p0(v_x)=1, i0(1)=v_0.
- p1(e_x)=1 if x=L-1 and 0 otherwise; i1(1)=sum_r e_r.
- A=ip, graded by chain degree.

On vertices dh(v_x)=v_x+v_0. For nonseam edges hd(e_x)=e_x; for the seam edge hd(e_(L-1))=sum_(r=0)^(L-2)e_r=e_(L-1)+i1(1). Thus dh+hd=I+A. Also dA=Ad=0, and A acts as identity on the chosen homology representatives.

For the tensor product of four factors use

    H = sum_(j=0)^3 A^(tensor j) tensor h tensor I^(tensor (3-j)),
    P = A tensor A tensor A tensor A.

Over F2 there are no sign distinctions. Cross terms with different-factor differentials cancel in dH+Hd. Remaining terms telescope:

    dH+Hd = sum_j A^j tensor (I+A) tensor I^(3-j) = I+P.

For syndrome z=dE, dz=0 and Pz=PdE=0. Consequently dH(z)=z. This holds for every physical boundary syndrome, including pairs of individually winding components. H is linear, deterministic and depends only on z. Its output is a 2-chain recovery.

For a closed residual C, C+P(C)=dH(C); hence the six coefficients of P(C) determine H2 completely. For orientation ij, its coefficient is XOR of C_ij(x) with x_i=x_j=L-1, summed over the remaining coordinates. Any fixed cuts give the same answer on closed C. These are exactly the six cut tests in the main contract, with cut 0 replaced by seam L-1. H1 vanishes on the total physical syndrome; do not demand it vanish separately on every connected component.

## Literal implementation and expansion-aware cost

Represent a k-cell by (x,sorted active axes). In H's term j, skip a cell if j is active. Every earlier inactive axis is projected to coordinate zero. Every earlier active axis a must have x_a=L-1, or the term is zero; if it survives, expand that axis over all L edge positions. The j coordinate expands over 0,...,x_j-1 and becomes active. Later coordinates are unchanged. XOR each resulting cell into the output.

For a syndrome edge with active axis a:

- j<a: no earlier active axis exists, so at most L-1 output faces.
- j>a: the term survives only at x_a=L-1, but then its i1 expansion contributes L and its h expansion at most L-1, giving L(L-1) faces.

Therefore the naive sparse bound is O(|z| L^2), not automatically O(|z| L). Accounting for the lattice population gives a better uniform global bound. There are six ordered pairs j<a, each with at most L^4 possible input edges; and six j>a pairs with only L^3 surviving seam edges each. At most

    6 L^4 (L-1) + 6 L^3 L (L-1) = 12 L^4 (L-1)

face-toggle operations occur. Thus this direct implementation costs O(L^5) time and O(L^4) output memory. A streamed dense/bit-packed accumulator avoids storing duplicate expansion lists. The Python checker uses sets for clarity and is not a production throughput benchmark. Any stronger sparse bound or prefix-sum optimization needs separate proof/measurement. At L=16 the conservative upper bound is 11,796,480 face toggles per global fallback; at L=32 it is 390,070,272. Frequent global readouts may still be expensive in Python.

Local interval-prism contractions have no periodic i1 loop expansion and remain the preferred ordinary path. Use the literal small-component rule from the main protocol and reserve whole-syndrome H for exceptional large/unliftable cases. Record its invocation and cost separately.

## Critical quality limitation

For one face f, contraction identity gives

    f + H(df) = P(f) + dH(f).

P(f) is the full coordinate logical sheet iff both active-coordinate positions of f equal L-1. Consequently a global-H-only decoder declares logical failure for 6L^2 of the 6L^4 possible single-face faults. This is a distance-one readout defect, not poor memory dynamics. The checker verifies the residual parity relation on every basis face. At zero initial error, noise in those locations alone creates an initial decoded-failure hazard 6 lambda_X L^2 under this global-only decoder.

The component-local branch avoids this for isolated face errors when L>8. At L<=8, its strict L/8 criterion sends them to fallback; those sizes are therefore unsuitable for treating this particular combined decoder as a meaningful protected-memory benchmark. L>=16 is a reasonable implementation starting range, not proof that the asymptotic theorem applies there. The source's sufficiently-large compatible-size hypothesis remains separate.

The fallback is a valid full quantum syndrome recovery but not minimum-weight, maximum-likelihood, or a canonical intrinsic logical-memory test. Its large-component failures must be interpreted as decoder-specific. This removes the algebraic completeness obstruction, not all performance interpretation issues.

## Exact finite verification

For each L=2,3,4 the checker exhausts every basis 0-, 1-, and 2-cell and asserts dH+Hd=I+P and d²=0. It additionally checks dH(df)=df on every basis face. By F2 linearity these checks establish the finite-lattice identity for all chains in these degrees at each tested L, not merely sampled syndromes.

It checks every cube boundary has zero six-bit homology, all six fundamental logical sheets return the six unit vectors, cut-position invariance on those sheets, and a wrapped-strip syndrome with two individually nonbounding components. All tests pass. The universal proof above, rather than finite testing, covers arbitrary L.

Counts by L:
- L=2: 16 vertices, 64 edges, 96 faces, 64 cube boundaries, 6 logical sheets.
- L=3: 81 vertices, 324 edges, 486 faces, 324 cube boundaries, 6 logical sheets.
- L=4: 256 vertices, 1024 edges, 1536 faces, 1024 cube boundaries, 6 logical sheets.

## Updated execution gate

Global GF2 elimination and MILP are no longer prerequisites. Implement local syndrome-component prism filling plus this fixed global contraction, verify dD(s)=s and all six homology invariants, and keep the same complete D for every compared memory kernel. The next authorized simulation can then report complete finite-T decoder-specific outcomes at L>=16, together with local/fallback rates, rather than requiring unresolved readout categories solely because a global solve was unavailable. Resource/time caps and alternative implementation errors can still produce explicitly unresolved trials.

## Separable dense implementation: O(L^4) route verified

The O(L^5) bound above describes literal basis expansion, not the best implementation. A separately written standard-library dense implementation applies the tensor operators as axis transforms and avoids expansion:

- On a vertex axis, ip XOR-reduces the line into coordinate 0, zeroing its other entries.
- On an edge axis, ip reads coordinate L-1 and broadcasts that bit to all coordinates.
- h on a vertex axis produces output edge at r equal to XOR of input vertices x>r; compute by one reverse cumulative parity pass. The seam output r=L-1 is zero.

For each input edge orientation k and j != k, apply the appropriate ip transformations on axes ell<j, then h on j; XOR into output face orientation {k,j}. There are exactly 12 terms, each at most four axis passes. Each pass has L^3 lines of length L and O(L^4) work. Fixed-dimensional total time and storage are therefore O(L^4), including all ip expansions. The implementation streams intermediates and uses six output and four input orientation arrays plus bounded scratch arrays. Python list storage has substantial constant overhead; this is a scaling claim, not a hardware cost claim.

`check_dense_tensor_readout.py` compares this implementation against the independent literal-expansion homotopy on EVERY basis edge at L=2,3,4: 64, 324, 1024 comparisons respectively, all PASS. Linearity then gives agreement for every syndrome at those sizes. A seeded L=16 algebra test constructs 2,000 random face proposals, forms their boundary (7,754 edges), and verifies dH(z)=z; output contains 37,308 faces. This test also PASSed, taking approximately 0.39 seconds including construction/readout/boundary verification in this environment. This was an algebra test, not a noise/correction trajectory, Monte Carlo lifetime estimate, or production throughput benchmark. Results are saved in `dense_tensor_readout_checks.json`.

The O(L^4) separable implementation is now the preferred complete fallback route. All warnings about global-H-only logical defects and preserving the component-local primary decoder still apply.
