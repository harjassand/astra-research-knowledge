# Finite clamped-energy receiving: exact arithmetic, costs, limitations

The theorem is a model reduction, not a new CIR algorithm. The executable's
actual numerical task is narrower: a finite externally clamped protocol, an
exact positive initial state, a terminal energy threshold, and a requested
ABSOLUTE width of its probability interval. Autonomous first-passage is not
computed. Full-state actuation, measurement, and model-membership acquisition
are not performed. They are not hidden inside a zero-cost oracle.

## Receiving interface and acquisition

The raw input is a complete energy polynomial and an actual generator program
`complete_pair_gradient` with a rational nonnegative tangent weight. The program
is the tensor/drift specification, not a few samples from a physical device.
Every monomial coefficient is strictly positive, all exponents are even, the
common total degree is 2 or 4, and every coordinate has a pure degree-p term.
Zero terms must be omitted, and duplicate terms are rejected. The consumer
acquires p, alpha=m/p, a coercivity constant, exact initial U(z0), and whether
the complete-pair tensor is SPD off the origin. It checks alpha>=1. The scalar
CDF backend further requires integer alpha; this is an implementation restriction,
not a mathematical restriction of the exact kinetic projection theorem.

Raw scanning costs O(S m) exponent entries, plus exact rational arithmetic for
coefficients and initial energy. Hashing scans the full raw program again. The
initial evaluation only multiplies nonzero monomial supports, at most p factors
per term, but locating them still reads all exponent entries. The complete-pair
operator is represented by formula (3) of the proof, NOT expanded into m^2
records. This is legitimate succinct input syntax, not a claim to have acquired
an arbitrary supplied matrix in less than its input length.

The protocol is supplied externally to both producer and verifier, as exact
rational (clamped y,duration) pairs. The temperature, kappa, threshold, tolerances
and resource budgets also come from the external original task. A submitted
certificate cannot relax them. The verifier recomputes raw acquisition and every
scalar integral-free calculation. It strictly binds types, model hash, actual
acquisition, exact protocol parameters, exact endpoints, scope, and exclusions.
Timing, work counters, and float displays are explicitly non-proof metadata.

## Outward fixed-point exponential

At scale S=2^P, nonnegative intervals are integer pairs. Every product is rounded
down/up after division by S; multiplication by a nonnegative rational uses floor/
ceiling integer division. For exp(-x), x>=0, reduce x=r*2^s with 0<r<=1/2.
Compute a positive Taylor sum for exp(r) with outward arithmetic. Once the next
term's upper endpoint is <=1/S, the complete remaining tail is <=2/S because
all subsequent term ratios are <=1/2. Invert the positive interval, then square
s times with directed rounding. All endpoints enclose the exact exponential;
no floating transcendental library participates in a certificate.

This routine is incomplete at fixed precision. Tiny positive quantities may
receive lower endpoint zero. In particular a zero lower Poisson seed or scale B
causes UNKNOWN rather than an unbounded search. There is no claim that P=256
suffices for every valid task. The caller may supply a larger finite precision.
Scaling/Taylor iterations and arithmetic operations have explicit budgets.

## Exact CDF enclosure

The scalar law is noncentral Gamma, equivalently noncentral chi-square. E and B
are propagated by directed interval operations. With terminal u0 and q fixed,

    lambda in [Elo*u0/Bhi, Ehi*u0/Blo],
    x      in [q/Bhi, q/Blo].

The Gamma-Poisson CDF is decreasing in lambda and increasing in x. The first
claim follows by coupling Poisson(lambda2)=Poisson(lambda1)+an independent
nonnegative Poisson increment, then adding independent exponential variables
to Gamma(alpha+N); the second is monotonicity of a CDF. Thus using the opposite
corners of this rectangle is sound even though E and B are correlated.

At a fixed corner, initialize w0=exp(-lambda), t0=exp(-x), and propagate
w_(n+1)=w_n*lambda/(n+1), t_(k+1)=t_k*x/(k+1) outward. The integer-shape Gamma
CDF is 1-sum_(k<alpha+n)t_k. Clip each enclosure to [0,1], sum nonnegative
products w_n*GammaCDF, and bound the entire omitted mixture by

    tail <= 1 - (lower bound on sum of retained Poisson weights).

Stop only when this tail is <= requested_width/8. Each corner's rounding and
truncation are included. Finally check the full combined probability interval
has width <= the externally requested tolerance. A resource exhaustion or
failure of this final conjunction returns UNKNOWN. No sampled normal number,
empirical convergence heuristic, or unchecked special-function call is used.

For two corners and n retained terms, scalar arithmetic is O(alpha+n) plus the
exponential work and protocol length; n can grow with noncentrality. Precision
and integer lengths matter. This is not a uniform constant-cost sampler or a
relative rare-probability bound. Arithmetic costs do not scale with an unknown
angular partition, number of angular transitions, or tangent mixing rate.

## Budgets and exactness boundaries

All external budget integers are strict positive integers, excluding bool and
float aliases; exact task rationals are Fraction objects with capped bit lengths.
The raw canonical rational parser rejects malformed, aliased, and oversized
strings. Input term count, dimension, exponent entries, total coefficient bits,
initial-state bits, and protocol segments are separately bounded. The raw
initial-energy Fraction arithmetic has conservative product/addition prechecks.

The fixed engine guards every product against `max_integer_bits` and counts
arithmetic operations before them. `largest_guarded_product_bits` is only this
tracked product proxy, NOT total peak process memory or every transient
addition/division bit length. Some positive additions can add a bit. The code
never advertises this counter as a strict all-intermediate memory bound.
Every loop has a separately finite bound. The script's Python runtime and input
serialization are ordinary paid work, not an ideal unit-cost real-RAM claim.

No denied source transfers, external writes, or physical operations were used.
All primary comparisons were bounded web reads. Existing accepted archives and
sources remain unchanged. The preliminary theorem's omitted positive-coefficient
words are preserved in EXACT_KINETIC_LIFT_BEFORE_GRAMMAR_CORRECTION.md; executable
acquisition already required positive coefficients before the wording repair.
