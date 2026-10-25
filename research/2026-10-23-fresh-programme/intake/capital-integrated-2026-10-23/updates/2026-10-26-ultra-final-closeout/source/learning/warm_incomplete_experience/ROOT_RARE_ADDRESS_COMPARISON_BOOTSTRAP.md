# Exact quadratic acquisition despite a fixed rare set of corrupted addresses

26 October 2026. New root consequence offered to the learning owner's
rare-address robustness construction. Independent whole review pending.
No new source/fixture/observation is executed. This is the same finite
comparison/native-bits interface with an explicit corruption extension;
neither physical noise nor historical six-source guards are inferred.

## 1. The corruption contract and an equivalent cheaper weak label

Keep an unknown quadratic permutation Q:F_2^n->F_2^n and its TRUE chosen-
pair lexicographic comparator C. There is a FIXED set B of native addresses,
with uniform mass epsilon. Every comparison with both endpoints outside B
returns the true C. A comparison touching B may return an arbitrary bit,
even depending causally on the entire past and the current pair. Fresh
future fair bits are not disclosed in advance. No ability to recognize B,
its geometry, or good fibres is supplied. If B itself is chosen in response
to future secret native draws, this proof does not apply.

On the true-prefix branch, the acquired procedure samples exactly uniformly
inside the true current prefix fibre F_y of size N=2^(n-t). A requested
weak-label address x is already supplied. If N>=128, draw K=511 independent
same-prefix Z_i and compare x DIRECTLY with each Z_i. Return the lower-half
label0 when a strict majority of C(x,Z_i) is1, and label1 otherwise.

With a correct comparator, x is below the sample median iff it is below
at least256 of the511 samples. This variant returns1 at median ties;
the older strict-upper label instead returns0 at a tie. Thus the laws
agree away from ties, rather than literally everywhere. The finite-grid
1/N allowance proved below handles this convention correctly. Sorting
the511 samples is unnecessary. It also avoids selecting a corrupted median
address as the sole final comparison. Every one of511 comparisons and all
conditional preparations/rejections are paid.

## 2. A fibre can be arbitrarily bad; only the averaged error is controlled

For a fixed true fibre put delta_y=|B intersect F_y|/N. Its output ranks
r=0,...,N-1 are uniform when x is uniform in that fibre. For a GOOD x of
rank r, one clean random comparison is1 with probability

    p_r=(N-r-1)/N.

At every draw, even under causal arbitrary responses, the conditional
probability of the observed bit1 lies in[p_r-delta_y,p_r+delta_y], clipped
to[0,1]. This uses a fresh uniform Z_i; only its membership in B can change
the answer for good x. Conditional Bernoulli stochastic domination therefore
bounds both majority tails by the corresponding binomial tails. Independence
of the adversary's replies is not required.

Let F_K be the CDF of V~Beta(256,256), extended by0/1 outside[0,1]. The
binomial/median identity and symmetry give, for good x,

    r<N/2: P(error|x)<=F_K((r+1)/N+delta_y),
    r>=N/2: P(error|x)<=1-F_K((r+1)/N-delta_y).         (1)

Bad requested addresses contribute at most delta_y to the average. The
increasing lower-half right Riemann sum exceeds its integral by at most
1/N; the decreasing upper-half right sum is at most its integral. Shifting
the two integrands by delta_y increases their integrals by at most
2delta_y in total. At zero shift their sum is E|V-1/2|. Hence the average
weak-label error within this fibre is at most

    e_y<=1/(2sqrt(K+2))+1/N+3delta_y,                  (2)

because Var(V)=1/[4(K+2)]. This is an AVERAGE over x in the fibre, not a
pointwise rank guarantee. It remains valid if the right side exceeds1.

All true t-prefix fibres have the SAME size. Averaging them with their
actual native weights gives E_y delta_y=epsilon, so for N>=128 the
native-uniform requested-address weak error obeys

    e_t<=1/(2sqrt(513))+1/128+3epsilon.                (3)

Nothing bounds delta_y separately. A selected fibre may lie wholly in B.

## 3. Tiny fibres use the exact old collection, with a different bound

For N<=64 retain the original capped exact collection of all N native
addresses in F_y. Sort them using a bounded comparison algorithm, and
label x by its rank in the collected list (x is one of those addresses).
No extra threshold comparison is necessary. The label is exact whenever
F_y contains NO bad address. On a contaminated fibre any answer is allowed
in this analysis. Since there are2^t equally weighted fibres and each
contaminated fibre contains at least one of the epsilon2^n bad addresses,

    native mass of contaminated fibres<=N epsilon<=64epsilon.

Thus the ideal complete-collection weak-label error satisfies

    e_t<=64epsilon,                                   (4)

without identifying or rejecting contaminated fibres. Collection timeout
is its original separately charged UNKNOWN event. Sorting at most64
objects takes at most64ceil(log2 64)=384 comparisons even if replies are
inconsistent: a finite mergesort still terminates. It need only be correct
when the entire fibre is clean, where every reply is a true total order.

## 4. Close the SAME local-correction acquisition loop

For the explicit constant epsilon<=1/4096, both(3) and(4) are STRICTLY
below1/32. For(3), use1/(2sqrt513)<1/45 and
1/128+3/4096=35/4096, with1/45+35/4096<1/32. For(4),64/4096=1/64.

For any requested interpolation point x_0, the seven nonempty vertices of
a fresh random three-direction additive cube are each native-uniform.
The third additive difference of every quadratic coordinate is zero, so
the XOR of their true labels is the true label at x_0. A union bound gives

    P[one corrected label wrong | any preceding causal history]
         <=7/32<1/4.                                 (5)

The seven vertices need not be independent. The fixed B may contain x_0;
the algebra still reconstructs its true polynomial value from the random
vertices. The sampler used in this ideal argument is the TRUE acquired-
prefix sampler, so no wrong learned conditional law has been smuggled into
the calculation.

Repeating with fresh cube and preparation tapes yields conditional trial
error probability at most1/4 at every repetition. If corrupted replies
are history dependent, Bernoulli domination/martingale Hoeffding replaces
an unjustified independence claim. An odd R-fold majority still has error
at most exp(-R/8). Interpolate each coordinate at0,e_i,e_i+e_j as before.

The same ideal-TRUE-prefix coupling, exact small-fibre collection caps,
conditional proposal caps and finite all-branch scan guards therefore give
actual correct completion with probability at least

    1-delta_a-eta_1-eta_2,

using the original R,M,S/error allocations. Corrupted replies do not change
the address filters or the true-prefix acceptance probability: those use
the already acquired coordinate CODE. The algorithms agree with their ideal
true-prefix versions until an acquired-coordinate error or actual cap.
This is a joint completion/error guarantee, not confidence conditional
on a selectively returned result.

All weak labels now take at most511 comparisons, including tiny fibres.
Consequently the conservative logical comparison ceiling improves to

    7*511*n*D_n*R=3577 n D_n R,
    D_n=1+n+binom(n,2).                                (6)

The number of conditional preparations, rejected proposals and bit/code/
linear-algebra costs still uses the full old M,S bounds. Global or
prefix-dependent acquired affine checkpoints give the same successful-run
2^g or2^g_cond factors. The explicit internal-confidence wrapper
epsilon_fail=delta2^-n (DISTINCT from the address-corruption mass epsilon)
also gives its bounded-error expected-work guarantee from the unchanged
all-branch2^n cap. No worst-context structure parameter is inferred cheaply.

## 5. Boundaries and strongest comparator

This is exact acquisition of the promised underlying quadratic permutation
despite this particular global bad-address channel. It assumes no noisy
or finite-precision source beyond that declared channel. Corruption on
otherwise good pairs, source changes, failures of uniform conditional
preparation, leaked future bits, arbitrary model classes or separately
unbounded source/physical latency require different analysis.

The method supplies no pointwise good-fibre guarantee. Its protection is
the native-uniform marginal of random correction vertices, the balanced
true-prefix law, and a separate contaminated-small-fibre mass bound. A
same-evidence ordinary retaining/local-correction implementation can use
all these choices. Boolean local correction, noisy comparison learning,
robust ranks and affine conditional decoders are strong established
ancestors; priority and practical advantage have not been established.
No source calls were executed for this theorem, and the historical six
expired-source guards remain absent.
