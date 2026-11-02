# Root construction: temporal excursion gas

Status: proof strategy, NOT an established expansion or memory theorem. 2026-11-01.

## Exact algebra personally checked
The accompanying root_seed_clock.py uses the actual five-qubit CSS seed with four weight-three checks and four qutrit clocks. For every one of 324 oriented clock edges, controlled-prefix conjugation produces exactly a scalar sign times either identity or the full corresponding stabilizer. Residual is exactly zero in real integer matrix arithmetic. Sixteen 81-dimensional ancillary Hamiltonians include the full spectrum, not a projected vacuum. At beta=2 and fixed leading singleton coefficient -0.5, increasing Delta from20 to1000 moves singleton coefficients from approximately(-.285,-.340) to(-.475,-.483), and largest multi-check coefficient decreases from .0214 to .00124. Finite checks do not establish uniform convergence or a family theorem.

## Constructive route to missing lemma
Use Duhamel worldlines of clocks, not expansion in beta*t. Divide every clock history which visits zero into maximal excursions from zero back to zero. Each excursion is a temporal rod with duration l and weight t^k exp(-Delta*l), carrying its sequence of intermediate nonzero clock positions. Clock path revisits within the nonzero subspace are resummed by its adjacency propagator, bounded by exp(C*t*l). At least two hops are required for a nontrivial excursion. Its duration moments are consequently controlled by t^2/(Delta-C*t) and t^2/(Delta-C*t)^2.

The controlled-Pauli dressing signs factor over pairs of neighboring clocks: their commutation exponents are bilinear functions of prefix Pauli labels. Signs associated with two rods can differ from1 only when their time intervals overlap. Same-clock rods are hard core. Therefore a candidate exact signed continuum polymer gas has pair factors in {+1,-1,0}, Mayer factor bounded by2, and finite spatial interaction degree. The integral of starts of a neighboring rod which overlaps a fixed rod is bounded by l+l'. This suggests a Kotecky–Preiss majorant proportional to Delta*l plus a small endpoint charge, with smallness t^2/Delta^2 rather than beta*t. It must be written explicitly and checked; no convergence is asserted yet.

A rod winding once around a K-cycle carries syndrome sign s_a and needs at least K hops. Its zero-temperature integrated weight per unit time starts at 2*t^K/Delta^(K-1). Any cluster with syndrome dependence needs at least one winding rod; shared-data interactions cannot manufacture flux from contractible paths. Additional excursions/steps yield higher orders, provided the charged cluster expansion is uniform.

Worldlines that never visit zero require a separate wrapping-rod sector. Their total imaginary-time length is beta, energy penalty Delta, and internal motion at most C*t. They should contribute exp[-beta*(Delta-C*t)] times local factors. Treating all clocks as initially zero would silently discard these thermal defects and is forbidden.

## Essential checks before claiming theorem
1. Exact rod counting on a time circle, including histories with multiple choices of zero crossing, avoids overcounting and boundary factors.
2. Pairwise sign factorization for the globally ordered controlled-Pauli gauge, including winding phases and reverse hops.
3. Explicit KP inequality for signed continuum rods; length and endpoint charges must control both overlap contributions.
4. Uniform Fourier/support locality of the flux-dependent log partition function, not only an extensive norm error.
5. Leading winding coefficient with finite-beta boundary correction and calibrated onsite self-energy; thermal wrapping terms explicitly charged.
6. Translate local flux perturbations into the actual decoder crossing-witness ratio. A global partition-function approximation is insufficient.
7. A Davies bath theorem would be a model-specific consequence. Generic physical noise or arbitrary calibration perturbations remain separate.

## Consequence gate
If established at fixed Delta/t and beta, with constants independent of volume, the construction could replace bounded-many-body thermal checks by bounded-dimensional native two-body interactions without demanding that every auxiliary spin be in its ground state. This is the intended capability. Ground-band gadget simulation alone is not enough. Compare strongest hopping gadgets and nonperturbative Ocko–Yoshida shielding before assigning novelty.

## Sharper provisional KP estimate
For a nonwrapping rod with k>=2 hops and duration l, summing its internal nonzero-position walks gives an absolute density bound A(l)<=2*t^2*exp[-(Delta-2*t)*l] (two choices of initial neighbor; end-hop bound may require an extra constant). With a(l)=a0+b*l, neighboring-rod start integration is at most l+l'. Thus a fixed rod sees at most

  C*D*exp(a0)*t^2*[l/(Delta-2*t-b)+1/(Delta-2*t-b)^2].

Choose a0=C0*D*(t/Delta)^2 and b=C0*D*t^2/Delta, with C0 large and t/Delta small. This can close the KP inequality, unlike the crude beta*t expansion. An exponential spatial-support weight can be inserted by multiplying the constant per rod; bounded degree suffices.

A first-return excursion on a K-cycle avoiding0 in its interior has winding either0,+1,-1, never multiple full windings. A winding rod therefore supplies exactly one syndrome sign, and its minimal path contains K hops. Its infinite-line time integral is 2*t^K/Delta^(K-1). Extra path detours have at least two extra hops. Cluster corrections involving at least one winding rod cost the small overlap norm O(D*r^2). This suggests a relative O(r^2) weighted-local correction to the target coefficient, beyond the conservative O(r) earlier bound.

A clock history never hitting0 is a wrap rod occupying the whole imaginary-time circle. Its unconstrained trace weight is bounded by (K-1)*exp[-beta*(Delta-2*t)]. It has no closing-edge winding flux itself. Its interaction with ordinary rods must be included in the KP sum: ordinary rods see at most this exponentially small activity, while a wrapping rod sees O(beta*t^2/Delta) ordinary-rod activity, absorbable in its length charge. Multiple wrap rods interact through the same bounded-degree signs. This is a proposed exact treatment, pending an explicit time-circle measure and audit.

Important subtlety: the interaction sign is not simply a function of interval overlap; it depends on ordered hop events and prefix labels inside both rods. The modulus bound still only uses overlap. A proof must retain full rod trajectories as polymer labels rather than replacing them by durations alone.
