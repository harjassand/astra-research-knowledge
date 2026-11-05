# Exact local birth and lazy-time primitives

These primitives support the query-local ancestor sampler. They do not by themselves prove that adaptively overlapping Poisson regions are explored consistently. That separate argument belongs to the ancestor engine and its audits.

## 1. Local loop birth measure

Let Lambda0 = 4 total/den be the raw torus-rooted proposal majorant inherited from the verified closed-loop oracle. For a finite nonempty vertex query K, use the dominating proposal rate

    Lambda_K = (3/2) Lambda0 |K|.

Choose a root uniformly in K, an initial direction uniformly among four directions, and follow the same rational finite-memory torus bridge. Reject nonphysical closure aliases, repeated physical edges and, when specified, exits from the open physical box. For a returned routed loop gamma let k_K(gamma) count its cyclic visits to K, including multiplicity at self-contact vertices. Accept with probability

    (3/5)^(r_true-r_memory) / k_K(gamma).

There is no 3/(2L) factor in this local oracle. The factor 3/2 has moved into its proposal rate; the old length denominator is replaced by the query visit count.

For each rooted oriented encoding, prefix/transition/stopping probabilities telescope to

    3^(-L) (3/5)^r_memory / (Lambda0 |K|).

The final correction changes this to 3^(-L)(3/5)^r_true/(Lambda0 |K| k_K). There are exactly 2 k_K oriented rooted encodings whose root lies in K. Multiplying their summed probability by Lambda_K gives

    3^(1-L) (3/5)^r_true = w_gamma.

This is precisely the desired birth intensity of every unoriented routed loop meeting K. Shared-vertex multiplicity matters: replacing k_K by the number of distinct query vertices visited would overcount self-contacting loops.

The all-length finite-memory certificate supplies the raw proposal's finite total mass and almost-sure termination on Z². The torus is only a finite-state proposal majorant, not a physical boundary condition. The oracle has no imposed path-length cutoff.

Numerically,

    (3/2) Lambda0 = 66455976045001 / 166988328468480
                 = 0.3979677900515361.

Implementation: `local_birth_oracle.py`, class `LocalLoopBirthSampler(seed=0)`.

- `.rate(K)` returns the exact rational Lambda_K, deduplicating K.
- `.propose(K, box=None)` returns a canonical routed loop or null.
- `box=None` means Z². `(width,height)` is the usual open rectangle starting at zero. `(xmin,xmax,ymin,ymax)` specifies half-open coordinate limits.
- Query vertices must lie in a specified finite box. Empty K has zero rate and null output.

## 2. Exact exponential times

Represent an independent Exp(1) random variable as E=-log U, with U uniform on (0,1) and its binary expansion revealed lazily. After b bits have integer prefix p,

    p/2^b <= U <= (p+1)/2^b.

The zero lower endpoint is refined until positive, almost surely after finitely many bits. For rational x>0, find an integer k and rational y in [1,2) with x=2^k y. Then

    log x = k log 2 + log y.

For z=(y-1)/(y+1), 0<=z<=1/3, the first N terms

    L_N(y) = 2 sum_{j=0}^{N-1} z^(2j+1)/(2j+1)

give the rigorous rational enclosure

    L_N(y) <= log y
             <= L_N(y) + 2 z^(2N+1)/((2N+1)(1-z²)).

The same formula at y=2 bounds log2. Multiplication by negative k reverses the two log2 endpoints. Monotonicity of log converts uniform bounds to exponential bounds:

    -upper_log(U_upper) <= E <= -lower_log(U_lower).

Refinement doubles both revealed bits and series terms. New intervals are intersected with prior intervals. Their widths tend to zero almost surely. Arbitrary endpoint values are not held in a global cache; only log2 enclosures use a bounded cache. Each exponential atom retains its own enclosures while it is live.

Every event time is represented symbolically as a rational constant plus a finite rational linear combination of independent exponential atoms. Addition and subtraction preserve shared atom identity and cancel coefficients exactly. To compare two times, subtract their expressions. A symbolically constant result is compared exactly. Otherwise, refine rational intervals until the difference has a definite sign.

A nonzero rational linear combination of independent continuous exponential variables has no atom at zero. Countably many adaptively selected rational coefficient patterns preserve this almost-sure statement. Hence every nontrivial comparison terminates almost surely. There is no floating ordering, fixed precision threshold, or finite iteration cutoff.

Implementation: `exact_lazy_time.py`.

- `ZERO` or `ExactTime.zero()` is time zero.
- `exponential_time(rng)` returns an independent atom as an ExactTime.
- `t.plus_exp(rng)` and `t.minus_exp(rng)` add/subtract fresh independent Exp(1) atoms.
- `t + u`, `t - u`, and rational scaling retain exact atom reuse.
- `.compare(other)` returns -1/0/1; comparison operators use that same exact mechanism.
- `.bounds(level)` returns rigorous rational lower/upper endpoints.

As throughout the sampler, ideal independent fair bits specify mathematical exactness. Python PRNG runs are reproducible diagnostics rather than physical-randomness certificates.

## 3. Independent normalization and time tests

`verify_local_primitives.py` independently enumerates every even physical edge subset as a GF(2) sum of elementary face boundaries. This exhausts the cycle space of each simply connected rectangular grid. At each degree-four vertex it enumerates all three pairings, traces their routed components and collects all loop types. It then follows the actual implemented prefix and bridge transition probabilities, rather than simply assigning the intended activity.

Results in `primitive_checks.json`:

- 3×3: all 20 routed configurations,17 loop types,224 rooted oriented encodings, maximum loop length8.
- 4×4: all 1504 routed configurations,793 loop types,21288 rooted oriented encodings, maximum loop length20.
- For every loop and four different query sets in each box, proposal probability times local rate equals its intended activity exactly as a Fraction. Query sets include one corner, one interior vertex, two opposite corners and the whole box.
- 801 log-bound/time-ordering tests against 200-decimal-digit arithmetic.
- 80 exponential atoms enclosed correctly at three refinement levels.
- A deliberately near-tied pair forces refinement beyond the initial 32 uniform bits.
- Symbolic cancellation of reused atoms is exact.

Complete 4×4 enumeration is a strong implementation check, not a proof covering all physical sizes. The telescoping/counting argument above supplies that proof. High-precision comparisons similarly test the code; the rational enclosure and continuity argument supplies exactness.

## Reproduce

    python square_aklt_local_sampler_20261105/verify_local_primitives.py
    python square_aklt_local_sampler_20261105/benchmark_primitives.py
