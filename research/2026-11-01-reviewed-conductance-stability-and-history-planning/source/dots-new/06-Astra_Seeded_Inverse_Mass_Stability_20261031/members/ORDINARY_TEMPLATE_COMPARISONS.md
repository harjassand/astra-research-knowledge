# Ordinary Lyapunov templates: earned comparisons, not a novelty claim

The main theorem gives the ordinary Foster machinery full credit. These comparisons
concern precise templates on the **same raw network**, not the capabilities of every
tier, sampled-time, excursion, fluid, or decomposition argument.

## Positive linear mass and its exponential

For `V(x)=v dot x+constant` with all v_i>0, at `(A,B,C)=(0,0,n)` all internal and
death rates vanish, and `LV=lambda v_A>0`. Thus no negative-constant Foster drift
outside a finite set is possible for this template. Similarly for
`W=exp(v dot x)`, `LW/W=lambda(exp(v_A)-1)>0` on that ray. This is why the successful
inverse correction needs a separately paid extinction-face patch.

Constructive LP-based stochastic stability frameworks using positive linear Foster
functions are established prior work. Gupta, Briat and Khammash (2014) explicitly
describe that approach and distinguish it from computational quadratic functions:
[primary PLOS article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003669).
The publisher's complete HTML was accessed 2026-10-31. The preceding direct generator
calculation, not a claim that the paper has no other extensions, is our template
exclusion. Efficient raw-network LP acquisition itself is not novel here.

## Standard chemical entropy: explicit failure on the cubic interior

Let `f(z)=z log z-z+1` with its continuous value at zero, and
`V=f(A)+f(B)+f(C)`. At `(n,n,n)`, every conservative jump has nonnegative V increment:
the starting point minimizes V on its total-count hyperplane by convexity. The
channel `A+B+C -> A+2C` has rate `alpha3 n^3` and V increment

    f(n-1)+f(n+1)-2f(n) >= 1/(n+1), n>=2.

For the inequality integrate `f''(z)=1/z` against the triangular second-difference
kernel, whose area is one. Immigration has nonnegative increment, and the death
contribution is bounded below by `-mu n log n`. Hence

    LV(n,n,n) >= alpha3 n^3/(n+1)-mu n log n >0

eventually. In particular this V cannot furnish even a negative-constant Foster
inequality outside a finite set. This failure is exact finite-count cubic noise, not
a simulation or a deterministic fluid conclusion.

The same conclusion holds for every fixed reference vector q>0 in the standard
pseudo-Helmholtz family

    V_q(x)=sum_i [x_i log(x_i/q_i)-x_i+q_i].

For rational q, choose x=nq integer. The gradient is `(log n)1`, so every conservative
jump cancels the first-order term and has a nonnegative convex remainder. The one
channel above contributes at least `c_q n^2`, since its rate is proportional to n^3
and its Hessian along that bounded jump is bounded below by a positive multiple of
1/n. Core contributions are bounded below by `-C_q n log n`.

For arbitrary real q>0, simultaneous rational approximation supplies integer n_k
and integer vectors x_k with `n_k->infinity` and `delta_k=x_k-n_k q->0`. This elementary
torus recurrence follows from pigeonholing the fractional parts of `j q`; in the
rational case exact multiples already suffice. At x_k,

    grad V_q(x_k)=(log n_k)1+O(||delta_k||/n_k).

The internal mean jump rate has magnitude O(n_k^3) and is conservative, so the entire
signed first-order contribution is O(||delta_k|| n_k^2). Each convex remainder is
nonnegative, while the displayed positive-rate channel contributes at least
`c_q n_k^2`. For large k the first-order error is less than half that contribution.
The core is again only O(n_k log n_k) in magnitude. Thus `LV_q(x_k)>0` eventually.

This is a template obstruction; weighted sums, nonsmooth repairs, sampled-time
entropy, or compositions with other functions are not excluded. In particular the
main inverse-mass certificate is an ordinary composition-sensitive repair, not an
argument that classical Lyapunov theory fails.

## Product form and sampled-time comparisons

The independent `SEEDED_STAR_BASELINE.md` retains the successful easy inverse-A
baseline and product-Poisson compatible control. For the hard non-complex-balanced
fixture, the main theorem gives a direct incompatible complex-balance calculation.
Neither calculation excludes all non-Poisson product forms or conditional laws.

The exact three-layer no-go applies to **one-step geometric drift** for arbitrary
normlike F(A,N). It does not apply to a sampled-time Foster inequality or to a
multi-event mechanism that remembers the mediator. The present certificate avoids
having to posit such an episode law by an exact inverse-mass drift estimate.

## Access accounting

A fresh primary-source search was used to check ordinary constructive comparators.
No historically denied Wisconsin, gated PMC, or denied ScienceDirect full text was
retried or fetched through an alternate route. Some such links appeared automatically
in search results; no new access attempt was made to them.

One optional new comparator URL,
`https://escholarship.org/uc/item/61h8m00p`, returned HTTP 429 on its first open. It
was not retried or fetched elsewhere. That access remains **uncompleted**; no proof
or theorem detail is attributed to that unavailable source. The construction, exact
tests, and independent audit do not depend on it. The PLOS publisher access succeeded.
