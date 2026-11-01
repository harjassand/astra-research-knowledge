# Actual consumer, cost ledger, and retained alternatives

Status: author construction, not independently accepted. Frozen predecessors are
not dependencies of this standalone standard-library consumer and remain unchanged.

## What was supplied, acquired, and left unknown

The predictive task is full-fiber equilibrium conductance cap_mu,M(A,B)/mu(A),
A={x_axis<=-1/2}, B={x_axis>=1/2}, beta>0. Input is the COMPLETE sparse polynomial
in the actual physical axes, not s, U, a reaction coordinate, a partition value,
conditional sampler, committor, kinetic matrix, or already-factorized expression.

The sufficient finder acquires the unique absent aligned coordinate in the
positive diagonal quadratic Hessian; derives kappa from one y^2/base quadratic
coefficient ratio; reconstructs U2 and U4; checks every sign and every monomial
of the full F=s^2 U2+s^4 U4 identity. U>=q_min||z||^2 is acquired. Generic rotated,
non-diagonal-quadratic, negative-component, or unsupported-degree inputs can
return UNKNOWN. This is deliberate scope, not a hardness claim or a failed proof
that those inputs lack useful structure. No numerical optimizer proposes a basis.
The basins are acquired from this grammar, not arbitrary user-prespecified sets.

The numerical output universally quantifies over finite CONSTANT SPD transverse
M, with longitudinal mobility1, zero cross mobility, and matching reversible
noise/drift. This is a mathematical family receiving interface; a raw polynomial
cannot authenticate an actual physical apparatus or its kinetic membership.
The source binds that scope explicitly. No actual M is read or estimated.

The detailed quadratic/quartic coefficients are acquired to validate the raw
model, but never used in the scalar integrals after admission. For fixed m,kappa,
beta,p4, ALL admitted U have the SAME certified outer interval for every declared
M. The unknown Z_beta, angular conditional law, internal mixing rates, interaction
graph, and all interaction strengths disappear from this specified prediction.
They do NOT disappear from the actual committor or exact parallel endpoint.

## Executed cases (unit beta,kappa; genuinely mixed, nonconvex graph energy)

Fixtures have U=sum_i(z_i^2+z_i^4)+20 sum_chain z_i^2 z_j^2. The two-coordinate
Hessian at z=(1,1) has eigenvalue 2+12-2*20=-26, so the admitted class is not merely
convex Gaussian or convex perturbations. Every fixture is expanded before calling
certify; expanded exponent vectors are fully scanned and bound. m is fiber dimension,
and n=m+1 is physical diffusion dimension.

| m | Raw monomials | Full interval ratio | Distinct scalar evaluations | Producer seconds observed |
|---:|---:|---:|---:|---:|
|1|14|1.034559810975|1,795|0.026|
|2|37|1.058198337048|2,563|0.054|
|3|60|1.081896511647|2,563|0.037|
|4|83|1.102634245708|2,051|0.032|
|16|359|1.169389474016|8,195|0.133|
|64|1,463|1.058480893962|16,387|0.386|
|128|2,935|1.031354559898|16,387|0.679|
|256|5,879|1.014307904863|65,539|7.873|
|512|11,767|1.006730486859|262,147|93.164|

The 513D full interval is approximately
[2.413067788904625e-152,2.429308909946876e-152]. Its exact rational endpoints and
requested TOTAL ratio101/100 are in results.json; displays/timing are not proofs.
The raw input contains 6,036,471 exponent entries. Here N=65,536 per monotone
segment, T=2, precision2,688bits, largest observed powered numerator/denominator
35,841bits, and numerical product ratio1.000972657733. The remaining full width
is structural sandwich slack. The actual author receiving run recomputes every
saved certificate including this one, paying the scalar and raw scan costs AGAIN.
Fixture generation has separate observed timing in results.json, not hidden in
an oracle. Saved small fixture uses nonfirst axis2 and its certificate is replayed.

## Exact arithmetic, termination, and receiving

Every scalar point is bounded at scale2^P using exact integers. q and R0 use
rational powers; Rplus uses rational powers with exponent m/p reduced by gcd
BEFORE selecting a root. Thus divisible dimensions get ordinary rational arithmetic
rather than artificial fourth-root work. The other possible roots are square or
fourth roots from isqrt. If a=x^n and root degree d, floor-root of
floor(a_num*2^(dP)/a_den) gives an outward lower endpoint; equality is checked
exactly and otherwise the upper endpoint is one unit larger.

q is monotone on [.5,1] and on [1,infinity); each geometric tail segment [2^j,2^(j+1)]
is treated separately. R0 and Rplus decrease on [0,.5], and symmetry doubles their
bounds. Endpoint Darboux sums, not floating quadrature, provide enclosures. The
remaining infinite tail is an exact rational analytic upper bound. No finite box
is substituted for the physical process. All scalar point types have separate
caches and count against one distinct-evaluation cap; intermediate refinements
are also counted, not merely the final grid.

Positive typed budgets bound dimension, monomials, coefficient bits, total input
coefficient bits, exponent entries, grid, total scalar evaluations, cutoff,
precision, and guarded high-degree powers/root shifts. The high-power bound is
checked BEFORE those exponentiations. It is NOT a whole-program intermediate-bit
budget: low-degree profile arithmetic, rational integral accumulation, final
reciprocals and serialization have their ordinary finite costs. The reported
max_power_integer_bits is only the largest powered numerator/denominator proxy,
not peak process memory or every arithmetic intermediate. No timing is certified.
Python exact string digit limits can return UNKNOWN, not silently round a value.

A positive lower seed is checked before any tail loop, and fixed cutoff/grid/
evaluation budgets ensure finite termination. Numerical refinement stops at the
requested numerical product tolerance. The requested TOTAL full-rate width is
then checked exactly; failure is UNKNOWN. Increasing numerical precision cannot
remove a genuine Rplus/R0 gap. This is a limitation of the sandwich, not a
physical accuracy floor or an impossibility for stronger methods.

The verifier reruns raw acquisition and scalar certification with the EXTERNALLY
supplied task, rather than trusting certificate-supplied budgets/tolerance. Strict
recursive typed equality binds all acquisition fields except observed seconds,
all model/family/task scope, and every exact interval endpoint. Booleans/floats
cannot impersonate integer metadata. Float displays, timing, and reported work
counters are explicitly diagnostic; corrupting them cannot change the received
mathematical claim. No saved output is trusted as an execution oracle.

## Complexity and why rare conductance itself does not force rare-event work

For fixed maximum energy degree4 the factorization search is a bounded scan,
not a general SOS or basis-learning problem. Let R be supplied terms, n dimension,
B input bit size, N final grid, J=log2T and P fixed-point precision. Scanning and
canonical hashing pay O(R n) exponent visits; constructing the full identity pays
O(R n) entries up to a fixed degree-dependent factor, plus exact rational arithmetic
and sorting O(R log R) keys of length n. Explicit parsed/coefficient/output sizes
are bounded by admitted inputs and the recorded budgets. No free sparse-coordinate
oracle is assumed; full vectors are actually traversed.

At most O(N(J+3)) distinct scalar evaluations are required by a completed final
grid, plus the bounded seed and any non-nested points. Scalar powers have exponents
O(m), with base bit lengths O(B+logN+logT); powering is ordinary binary exponentiation.
Squared/fourth roots and integer division have bit complexity polynomial in their
recorded operand length; accumulated integer sums add O(logN+logJ) bits before
rational interval scaling. Rational products/reciprocals and serialization are
also polynomial in these finite operand lengths. This gives a polynomial ledger
in ACTUAL admitted m,B,P,N,J, not a blanket polynomial guarantee in requested
accuracy for all parameter regimes. Coercivity does not enter numerical width;
kappa and intrinsic profile slack can still make targets/budgets fail.

For the demonstrated fixed kappa1 family, logarithms of the rare rate grow with m,
while our paid precision and power sizes grow on that scale; there is no loop
waiting for an event of probability about10^-152. This does not prove asymptotic
optimal complexity or defeat an equally informed analytic/variational solver.

## Strong ordinary retaining comparisons

1. **Exact spatial Jacobian/free-energy reduction.** This already gives q=s^-m and
   the scalar upper k_free for arbitrary integrable U. It is the starting point,
   not a novelty claim. However, q alone cannot certify a positive relative full-
   rate lower bound: GEOMETRY_ALONE_FAILURE gives a smooth coercive radial-double-
   well family with identical q and arbitrarily small slow-M rates.
2. **Dirichlet/Thomson and fixed-fiber Cauchy.** These are ordinary primitives.
   A solver supplied the SAME radial p-concavity proof can produce exactly this
   result; no proprietary algorithmic separation is claimed. The newly derived
   comparison plus receiving chain should not be counted as an independent
   pre-existing method merely because those primitives are ordinary.
3. **Earlier homogeneous capability.** For F=v(y)U_hom(z) the exact parallel
   endpoint cancels by energy coarea and an exact open mobility range is known
   in our earlier accepted construction. Mixed U is generally not separable as
   one v times U; that exact endpoint theorem is NOT transferred. The present
   outer prediction uses a different spatial/Jensen comparison and loses exact
   endpoint universality. Pure quadratic inputs are explicitly recognized with
   the tighter actual degree p2, not forced through the mixed p4 bound.
4. **Sample-based committor/profile methods.** Equilibrium/reweighted sampling,
   profile optimization and rare-event acceleration are strong ordinary options;
   blind brute-force crossing is not the only comparator. Those methods can use
   structure when available. Here no equilibrium samples or conditional mixing
   oracle are supplied, and no angular partition is evaluated. Conditional slow
   mixing itself is not an obstacle to this particular variational prediction.
5. **Full elliptic PDE/fiber variational solvers.** Retained: they may tighten the
   intrinsic sandwich, obtain actual rates for a known M or solve out-of-grammar
   models. Their acquisition/discretization/verification cost is not dismissed;
   no exponential worst-case lower bound or formal hardness separation is asserted.

Located primary comparisons are cited in SOURCES_AND_SCOPE.md. Historical priority
of the radial p-concavity conductance theorem remains unresolved after bounded
retrieval. No scientific importance score, experimental validation, arbitrary-start
MFPT claim, physical implementation, or general hidden-dynamics reconstruction is
inferred from this mathematical consumer.
