# Exact ordered-fault sampler

`exact_sampler.py` consumes the producer's graph, parameters, U, J limbs, and
capped internal distance array. It checks source/array hashes in the manifest,
reconstructs the exact root normalizer, and verifies equality with Z_exact.
It does not independently certify the supersolution or shortest-path table;
those are separate certificate/audit obligations. No fixed pilot is authorized
until those checks and the sampler review pass.

## Law implemented

The sampler holds an ordered list of oriented fault edges and a set of their
underlying IDs. It does not select clean routes or mark their vertices visited.
Repeating an underlying edge kills immediately, including reverse traversal.
A shared endpoint is allowed. This bounds the number of distinct sampled faults
by the graph edge count; there is no finite-length truncation bias.

The initial weight of (x,y,e) has integer numerator

    (q_num[e] << (cost[e] + dlmax - dl[x])) * U[y,(cost[e]-dl[x]) mod N]

at denominator 2^(qden+Q+dlmax). At internal state (v,r), draw uniformly from
[0, U[v,r] * 2^(qden+D)). Place the exact terminal numerator
2^(Q+qden+D-dr[v]-((r-dr[v]) mod N)) first. Remaining buckets for x have weight
J[x,(r-dist[v,x]) mod N] * 2^(D-dist[v,x]). The rest is null. Right states have
only terminal and null. This implementation explicitly restricts N=D=64,
qden=64 and checks that the terminal exponent is nonnegative for every relevant
state/residue. The current producer uses Q=56, read from metadata.

After selecting x, independently select its outgoing edge with exact integer
weight (q_num[e] << cost[e]) * U[y,(r-dist[v,x]+cost[e]) mod N]. Only internal
fault starts are allowed here; left-ending and right-starting orientations are
excluded. Distances lower-bound clean gaps and do not condition any edge.

Update the true score at every fault and at termination. Reject a negative
terminal score, and use fair bits to thin by 2^(-(S-(S mod N))) otherwise.
Generate independent q_num/2^64 noise on every graph edge, discard the tuple-edge
draws, and force those edges to 1. Ask the fixed CircuitModel for its canonical
left-to-right residual path; recover its orientation and retain only edges
where E=1. Accept only exact equality to the proposed ordered oriented tuple.
The independent finite audit establishes that each accepted E has mass P(E)/Z.

## Certified floating endpoint selection

All decisions refer to the original arbitrary-precision integer uniform draw.
Floating arithmetic only proposes a candidate endpoint bucket.

Let u=2^-53, n be the number of internal vertices, and J be a nonnegative
128-bit integer represented by its two uint64 limbs. The conversion

    float(J_lo) + 2^64 * float(J_hi)

has relative error at most gamma_2 = 2u/(1-2u). Scaling by 2^(D-d), 0<=d<=D=64,
is exact in binary64. Each positive mass is >=1 and <2^192, so it is normal and
finite; zero is exact. With n<=2^20, the total is <2^212 and is finite. The code
checks the limb types, n bound, distance range, D, and float finiteness. NumPy
cumsum sums nonnegative binary64 numbers. Every prefix has relative error at
most gamma_(n+1), allowing conversion and at most n-1 additions.

Let A_k be an exact prefix and F_k its computed floating prefix. Let F_n be the
computed final total, which is itself rounded, not an exact total. With
kappa=gamma_(n+1), positivity gives

    abs(A_k-F_k) <= kappa*A_k <= kappa*A_n
                    <= kappa/(1-kappa)*F_n
                    < 2(n+1)u*F_n.

The implementation uses E=nextafter(16(n+1)u*F_n,+infinity). The coefficient is
exactly representable and the multiplication is rounded once; nextafter makes
E at least its real product. This is a deliberately loose error enclosure.
The extra slack is not a claim of faster convergence or model accuracy.

For proposed bucket k, form an upper bound for its preceding exact prefix as
ceil(nextafter(F_(k-1)+E,+infinity)), and a lower bound for its ending exact
prefix as floor(nextafter(F_k-E,-infinity)). Certify only when

    upper_preceding <= original_integer_draw < lower_ending.

The empty preceding prefix is exactly zero. A null candidate needs only the
left inequality. Addition/subtraction are explicitly rounded outward before
conversion to Python integers. Candidate search uses float(draw), but its
rounding cannot affect validity: incorrect or ambiguous candidates fail the
exact-integer enclosure check. On ambiguity, compute arbitrary-precision
integer prefixes directly and use the same unchanged draw. The fallback
introduces neither approximation error nor additional random draws.

Only one O(n) temporary CDF is held. J_float is O(n*N); there is no
vertex-by-residue-by-target CDF table or unbounded cache. `--force-exact-prefixes`
allows differential tests against the integer implementation.

## Statistical and model scope

A fixed number of independent ideal-bit trials gives a Bernoulli indicator
with success probability P_q(failure)/Z. The 99.9% fixed-shot Clopper-Pearson
interval uses exactly checked outward dyadic endpoints, multiplies by exact Z,
and expands by the supplied exact conversion-TV bound to cover the stated
input probabilities. It is not a sequential/optional-stopping interval.
The point estimate is for the rounded q model; the interval includes the input
conversion error. Distances, table slack, null killing and score folding do not
introduce additional bias if the certificates hold.

Python random.Random is a deterministic Mersenne Twister generator. Its output
is reproducible, not ideal random bits and not proof of physical IID behavior.
The executable's exact-law and confidence claims are conditional on replacing
that source with ideal independent bits. The bit counter reports requested
bits, not cryptographic entropy or consumed hardware entropy. Uniform integer
rejection, score-thinning bits, unused tuple-edge noise, and noise generation
are all counted. Time includes separate setup, sampling and confidence phases;
peak RSS is the whole process, while static_array_bytes is only listed NumPy
arrays, not Python structures, decoder allocations or transient working memory.

Scope is the frozen circuit graph, independent-edge noise model, costs,
canonical path selector and exact decoder implementation. It does not establish
hardware failure rates, correlated-noise validity, arbitrary decoder behavior,
novelty, or speed against unmeasured competitors. Any comparison must retain
matching model, confidence, setup/resource accounting, and PRNG caveats.
