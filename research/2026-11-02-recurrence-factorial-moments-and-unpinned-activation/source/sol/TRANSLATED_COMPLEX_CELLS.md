# Exact finite cells, with their acquisition and limitation

Same author and scope as this stage. These facts are mathematical constructions, not a general recurrence theorem.

Use raw mass-action propensities q_e(x)=kappa_e x!/(x-y_e)!, interpreted as zero unless x>=y_e. For a linkage class C_l and an integer residual z>=0, form the COMPLETE translated cell

    S_(l,z)={z+y:y in C_l},

with all its complex-graph edges. The full generator is exactly the sum of these cell generators. A physical edge x->x+y'−y has the unique residual z=x−y for that raw reaction. Parallel edges remain separate or their rates are added.

## A reference acquired from the finite raw graph

For every raw edge choose a finite directed return path in its strongly connected linkage class. Add one unit of flow around that edge followed by its return path. Summing these cycles gives strictly positive integer coefficients kappa0_e, with equal total incoming and outgoing flow at EVERY complex. This is a constructive finite operation on the supplied graph.

Let mu0(x)=1/x!. On each reference cell,

    mu0(z+y) q0_e(z+y) = kappa0_e/z!.

Complex flow balance therefore proves stationarity of mu0 restricted to that cell. More generally EVERY FINITE UNION OF COMPLETE CELLS has exactly mu0 restricted to each communicating component as a stationary measure. Cell overlaps do not spoil the identity. Selecting arbitrary individual edges would spoil it. This is an exact acquisition, rather than a supplied stationary fiber or mixing assumption.

For the original rates let

    a=min_e kappa_e/kappa0_e,    b=max_e kappa_e/kappa0_e.

On a finite irreducible union with m distinct states, the directed matrix-tree formula compares each rooted tree weight by factors a^(m−1), b^(m−1). Hence its normalized original stationary law pi obeys

    (a/b)^(m−1) mu0(x)/mu0(y)
      <= pi(x)/pi(y)
      <= (b/a)^(m−1) mu0(x)/mu0(y).                 (1)

The same comparison holds with aggregate rates: every aggregate edge ratio remains in [a,b]. No spectral-gap lower bound is used.

A SINGLE linkage cell admits an even sharper exact profile. If rho>0 is the finite complex-graph stationary vector for rates kappa, then

    pi_(l,z)(z+y) proportional to rho_y/(z+y)!,

because its flux is rho_y kappa_e/z!. The factors rho_y are fixed; they do not depend on the large residual z. This does not supply a common profile on overlapping cells: one physical state can play different complex roles in different cells.

## Turning an actual deletion word into a uniformly finite cell

Take any fixed enabled deletion word at basis state b. At each prefix state x and fired edge y->y', include its ENTIRE translated linkage cell with residual x−y. The finite union contains the whole actual word and its reverse communication paths. Translating this union by w>=0 preserves every edge and its mass-action rates. Its shape and cardinality m are independent of w.

Apply (1) to the start b+w and the terminal b−delta+w. If delta_i>=1 and the i-th initial count is comparable to total size N, then

    pi_cell(start)/pi_cell(terminal) <= C/N,

with an explicitly acquired constant C=(b/a)^(m−1) (using different letters for the rate bound and basis state where necessary). This is a true, uniform preference for the lower factorial-energy endpoint inside an acquired constant-size cell, including multiple changing inventories and nonconstant landing roles.

Combining this construction with `COORDINATE_DELETION.md` gives finitely many cell templates with an inward endpoint preference on every actual infinite communication class outside its finite head. This avoids ANY neighboring-profile transport law.

## The remaining whole-process operation

The selected finite cell generator omits other actual translated cells meeting its states. Its stationary law, endpoint odds, holding times and return law cannot be assigned to the full process. The missing operation is a global comparison or Lyapunov construction that retains ALL those overlapping competitors. The original/reference ratio bound in (1) is exponential in the number of states if applied to a growing global truncation, so it does not prove tightness. No uniform mixing or boundary oracle is silently substituted for this step.
