# Independent review: fixed-alternative randomized local-probe obstruction

**PASS, theorem-only**, at the explicit unit-longitudinal interface `diag(1,M)` with fixed finite constant SPD M. Source: `RANDOMIZED_LOCAL_PROBE_OBSTRUCTION_ROOT.md`, SHA-256 `b24a7775dd2403233f771cf1ec19e79138bb1a85939a71fa72cc162a8afaf47c`. This is a separate source-bound acceptance, not an amendment to the author's three-file theorem freeze and not code acceptance.

## Claim and quantifiers

For a randomized adaptive local-value/finite-jet procedure terminating almost surely on the nominal F0, let q be its probability of reporting a strictly positive lower conductance bound on F0. For every epsilon>0 there exists one fixed smooth alternative F1 (chosen using the algorithm's distribution, not its realized random seed) on which the reported lower bound is false with probability at least q-epsilon. The alternative is of the form F0+A b(y), supported in a relatively compact open subinterval of the slab. This supplies exactly the statistical scope absent from the transcript-dependent H construction.

The proof is correct. Standard measurability of the procedure/query/output random variables is understood.

1. Almost-sure finite termination gives a deterministic K0 with P(N>K0)<epsilon/3; no expectation bound is needed. Padding missing queries outside the slab is harmless.
2. Continuity from below for the events {reported lower bound>=1/n} gives a deterministic L>0 with probability at least q-epsilon/3. No quantitative lower threshold is assumed in advance.
3. Translate an interval of length h inside a fixed interval with compact closure in the slab. For every fixed query coordinate, the translation measure of hits is at most h. Integrating over algorithm randomness and union-bounding the first K0 nominal queries gives mean hit probability at most K0*h/(translation-range length). Choosing h small makes this less than epsilon/3. Therefore at least one FIXED interval I has that small hit probability. Neither query densities, independence, bounded query derivatives, nor a uniform stopping-time bound are used.
4. Couple the nominal and alternative algorithms with the same random seed. Outside I the two potentials and ALL finite jets agree. On the nominal event {N<=K0, no hit among first K0}, induction makes every alternative query and the stopped output identical. Intersecting with the lower-bound event leaves probability at least q-epsilon, uniformly over the future amplitude A.
5. Choose a smooth nonnegative b supported in I with b>=1 on an interval I0 of positive length. The scalar trial whose derivative is 1/|I0| on I0 has unnormalized energy at most

       exp(-beta A)/(beta |I0|^2)
         * integral_(I0 x R^m) exp(-beta F0).

   Its transverse derivative is zero. The unnormalized basin mass stays EXACTLY unchanged. Therefore the actual rate tends to zero as A grows; choose one fixed finite A for which it is below L. The same fixed F_A now witnesses the stated failure probability. No post-seed selection of a potential occurs.

## Full global process

The inherited nominal s/U construction supplies a coercive quadratic Lyapunov function V=1+y^2+K_L z^T M^-1 z with bounded-above LV. The number K_L is unrelated to the query cutoff K0. Adding A b(y) changes LV by -2Ay b'(y), a bounded function because b is smooth and compactly supported in y. Thus every fixed finite-A alternative is nonexplosive. F_A>=F0 gives finite Gibbs mass, basins and mobility/noise remain unchanged, and the conservative reversible Dirichlet capacity is legitimate. Narrow support may make derivatives enormous but finite; the unrestricted model class explicitly permits that.

## Useful coverage corollary

If one procedure has false-lower-bound probability at most alpha for EVERY model in this compact-bump alternative class (as part of a claimed uniform coverage guarantee), then necessarily

    P_F0(reported lower bound>0) <= alpha.

Otherwise choose epsilon<q-alpha and the fixed alternative above contradicts the uniform guarantee. This is a valid fixed-input probabilistic no-free-lunch statement, not merely pathwise transcript compatibility. A procedure reporting UNKNOWN is not contradicted.

## Boundaries

The procedure is granted finitely many local values/finite jets and must terminate almost surely on F0. No claim is made for interval/global oracles, symbolic coefficient access, trajectory observations, equilibrium samples, fixed finite-dimensional model classes, uniformly bounded derivatives, or a fixed polynomial degree. No arbitrary-error rejection probability or finite number of evaluations is inferred for the separate exact coefficient receiver.

The opening's earlier ambiguity about general longitudinal mobility was corrected before this acceptance. The phrase "compact open slab interval" is read in the standard intended sense "an open interval whose closure is compactly contained in the slab"; choosing such an interval is trivial and the proof does not require a nonempty interval literally both open and compact in R. No further correction is mathematically needed.

No executable was run for this measure/variational argument; its verification consists of the explicit probability coupling, exact Dirichlet trial bound, and global Lyapunov calculation above. Original artifacts were not edited by this reviewer.
