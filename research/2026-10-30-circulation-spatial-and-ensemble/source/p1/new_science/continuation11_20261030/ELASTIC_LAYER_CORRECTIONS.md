# Binding clarifications of the elastic-layer proof

30 October 2026. The actual record-geometry receiving check identified two
points in `ELASTIC_CARRIER_LAYER_AND_DENSITY_LAW.md` (reviewed input SHA
begins `7f3ecd1fcc7a`). Preserve that input and its review; use this note with
the theorem. Neither point changes the joint concentration construction.

## 1. Use the norm event to pass to the continuous path

The time-grid argument after (11) must apply (9) directly to
`||u||>epsilon N²`, not just to the weaker density event (10). At all grid
times the norm is then small. The relative-velocity bound between grid times
makes its supremum small, and the deterministic inequality (7) holds for
**every** collection of row translations C_y(s). A small density error at
grid times alone would not exclude cancellation between rows which a later
translation could destroy. The existing norm concentration supplies the
needed stronger event with exactly the same exponent.

## 2. Finite-force cutoff for general stiffness

On a link sublevel kappa V<=H_* for V(1+z)=z²/[2(1-z²)], the all-regime
bounds are

\[
 1-|z|\ge {\kappa\over 2(\kappa+2H_*)},\qquad
 |\kappa V'|\le\sqrt{2\kappa H_*}
                     (1+2H_*/\kappa)^{3/2},
\]

and

\[
 \kappa V''\le4\kappa(1+2H_*/\kappa)^3.
\]

The simpler clearance c kappa/H_* and force C H_*²/kappa in the initial
note require kappa<=C H_*. They are valid for the concrete intended choice
kappa_N=log(N+2), H_*=C N²log N. The general ideal density theorem only
needs kappa_N->infinity; a polynomial finite-force realization separately
requires a polynomial stiffness choice and the displayed range and
derivative. For the concrete logarithmic stiffness the worst-case required
derivative is of order N^6 log N and the corresponding unit-mass frequency
bound is of order N^3 sqrt(log N). These conservative rare-tail ranges are
much larger than the near-equilibrium frequency sqrt(log N).

This qualification is physically material. Small-amplitude spring
characterization does not warrant the volume-scale rare-event claim. No
claim of modest apparatus bandwidth follows from slowly growing typical
stiffness.

## 3. Joint thermal sources and potential scope

The thermal coordinates entering different carriers, different rows and
different periods are jointly independent standard Gaussians, conditional
on the full past available before their introduction. Independent scalar
marginals are insufficient. This is the actual product-source supplier used
for invariance of the joint relative Gibbs law and the spatial vector noise
bound. Sharing one fresh scalar between all rows would invalidate the latter.

The explicit force/derivative envelope above applies to the displayed
rational link potential. An unknown homogeneous strongly convex potential
still supplies the ideal concentration theorem under its stated bounds;
its finite-force realization needs its own sublevel force and derivative
envelope. It does not inherit the rational potential's envelope from convexity.
