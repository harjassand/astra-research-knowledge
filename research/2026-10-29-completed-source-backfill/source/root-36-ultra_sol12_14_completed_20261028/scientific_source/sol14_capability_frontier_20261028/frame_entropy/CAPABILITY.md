# Result and available operation

The qutrit mechanism extends to a dimension-uniform preparation theorem,
and admits a universal rational repair for arbitrary projective 2-designs.
Root whole-read and accepted the proofs at their stated analytic scope.
The exact programs below pass their own integer/rational checks; those
code outputs are distinct from that analytic acceptance.

## Reusable input/output contract

For any supplied weighted rank-one projective 2-design `(w_i,S_i)` in
dimension d>=2, define the new preparation atoms

    sigma_i=[2(d^2-1)S_i+I/d]/(2d^2-1).

For every probability vector p, without further optimization,

    D(sum_i p_i sigma_i || I/d) <= (1/2)D(p||w).

The scalar coefficients have O(log d) bits. Applying them to n exact
projectors costs O(nd^2) field operations. Qualifying the design moments
and reading its matrices are upstream costs, not omitted oracle calls.
The atoms and every output mixture have spectral floor
`I/[d(2d^2-1)]`. The white fraction is explicitly `1/(2d^2-1)`; it changes
the preparation channel and is not free noise tolerance for an unchanged
channel. More generally every `t<=sqrt(1-1/d^2)` qualifies. This threshold
is sharp for the full convex-order mechanism, not proved sharp for
entropy itself. See `UNIVERSAL_NOISE.md`.

For an unmodified design, `PROOF.md` characterizes full score convex order
by the exact hemisphere condition

    sum_i w_i(2<v,S_i v>-1)_+ <=1/d^2 for every unit v.

Pairwise overlap AMPLITUDE at most1/2 is a cheap sufficient certificate.
This receives SICs for d>=3 and complete MUB designs for d>=4, plus
convex mixtures of unitary rotations of qualifying measures. A separate
scalar proof covers the qubit SIC although its convex order fails.
Thus every SIC in every d>=2 satisfies

    S(sum_i p_i S_i)>=H(p)/2,

with equality exactly at uniform weights and point masses. The constant
is sharp for each SIC. This is conditional on a supplied SIC, not a
proof of SIC existence in all dimensions. For uniform redundant designs
on n labels, the correct statement is instead
`S(M)>=H(p)/2+log d-(log n)/2`.

## Actual higher-dimensional receivers

`compile_frames.py` constructs a known d8 Hoggar SIC from the three-qubit
Pauli orbit of `(-1+2i,1,1,1,1,1,1,1)/sqrt12`. Exact Gaussian-integer
arithmetic checks4096 pairs and4096 second-moment components. A separate
d4 complete MUB construction checks400 pairs and256 moments. These are
credited known frames, not new SIC/MUB discoveries.

For64 distinct Hoggar preparation weights (864 followed by a fixed
permutation of1,...,63), rational Newton--Sturm/log certificates enclose

    D(p||uniform)-2D(M||I8/8)=+0.3418397691452384... .

For the SAME source the sharp Harremoes--Topsoe scalar entropy/purity
relaxation gives

    2 Hmin_8(q)-Hmax_64(s)=-0.2792295954104841... .

The frame theorem pays a sign this sharp scalar relaxation does not pay.
This is not superiority to every established entropy argument; our proof
itself uses established transportation, majorization and Gibbs tools.
The actual20-weight d4 MUB source has corrected defect
`+0.2369352873522562...`. Outputs are in `FRAME_RECEIVERS.json`.

Qualification and both exact entropy receivers took about0.233s locally:
0.0364s Hoggar,0.0057s MUB,0.1906s entropy calculations. No eigensolver,
SDP, paid computation or numerical sign premise was used. These are
observed arithmetic costs, not an asymptotic runtime advantage.

## Exact design obstruction and repair

`DESIGN_OBSTRUCTION.md` and `certify_design_obstruction.py` give an
actual48-state weighted qutrit 2-design with radial law Y=2/9,5/6 and
probabilities9/11,2/11. Its hemisphere value at e0 is4/33, exceeding1/9
by1/99. Exact multiquadratic arithmetic qualifies48 rank-one projectors
and all81 moments in about0.0165s. A264-state distinct uniform variant
is proved by finite phase-character sums without a separate264-matrix
execution. The continuous hinge witness also separates this measure from
the weakly closed convex hull of qutrit SIC measures. It is a mechanism
obstruction, not an entropy counterexample.

`certify_noise.py` constructs the48 mixed atoms at t=16/17, checks pure
and mixed moments, and receives ALL preparation weights by the universal
theorem. One supplied source has exact defect
`Din-2Dout=+0.7691812956756565...`. Acquisition plus this control costs
about0.028s; see `NOISE_RECEIVER.json`. At t=19/20 the same design has
a full convex-order hinge violation1/990; no entropy failure is asserted.

The ordinary proof template of generic preparation DPI followed by
convexity of depolarization guarantees1/2 only for t<=1/2. Even its best
state-independent depolarizing factor is at least t^2, so that template
cannot pay1/2 for t>1/sqrt2. The new moment-aware compiler exceeds this
limit in every d>=2. This is a comparator-family limitation, not an
impossibility for every other source-aware entropy argument.

## Proof, cost and claim boundaries

`verify_cut_identities.py` checks the all-variable discriminant,
reciprocal and rational-noise identities in the integer polynomial ring.
Finite dimension scans are not premises. `exact_entropy.py` supplies
elementary interval arithmetic and rational Sturm routines. Rational
interval endpoints, not displayed decimals, govern all finite values.

The entropy duality, projective-design definitions, frame constructions,
entropy/purity envelopes and POVM norm machinery are credited in
`PRIMARY_SCOPE.md`. Historical priority remains UNKNOWN. Quantum memory,
arbitrary operator-valued inputs, WH_d/CLR, physical implementation,
practical speed advantage and civilization-scale leverage are not
established. Root's separate bounded pure-design exponential search
found no counterexample and proves no unrestricted pure-design theorem;
the present noise compiler does not rely on that search.
