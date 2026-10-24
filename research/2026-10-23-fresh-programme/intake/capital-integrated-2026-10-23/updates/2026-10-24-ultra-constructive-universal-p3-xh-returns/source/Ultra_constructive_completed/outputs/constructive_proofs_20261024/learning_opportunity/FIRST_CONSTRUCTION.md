# Independent first construction: a comparator can acquire its own conditional sampler

Saved before support-agent exposure. Author-owned question and construction, 24 October 2026. Internal mathematical candidate; proof, priority and consequential capability require separate review.

## Question and input/output contract

An opaque comparison oracle orders all n-bit objects by the unknown integer whose bits are Q(x). Can we acquire an exact compact rank decoder, inverse and uniform conditional sampler without being supplied the hidden affine coordinates, a significance flag, fibre sampler, or a table of ranks?

Promise: Q:F_2^n -> F_2^n is a bijection; each coordinate is a Boolean polynomial of degree at most two. Let B_i(u,v)=Q_i(u+v)+Q_i(u)+Q_i(v)+Q_i(0) be its alternating polar form. The *joint polar rank* is

    b(Q) = codim intersection_i rad(B_i).

The class promise is b(Q)<=b. n and an upper bound b are supplied. Q, B_i, their joint radical, rank labels, output bits, affine hiding maps and conditional samplers are not supplied. The only data operation is C(x,y)=1{rank Q(x)<rank Q(y)}, with exact equality x=y handled locally. All comparisons, input bits, randomness, fibre preparation, linear algebra, storage and verification are charged. Exact class recognition against arbitrary orderings is not claimed.

Goal: with failure probability delta, acquire all Q_i exactly on every input, then compile Q, Q^{-1}, and exact uniform sampling from every prefix fibre. This is a promised-class theorem, not representation-free general learning.

## Load-bearing operation: an acquired prefix samples its own fibres

Suppose t leading coordinates F=(Q_1,...,Q_t) have been acquired exactly. Compute each polar matrix and the common radical L_t by Gaussian elimination. Its codimension r_t is at most b. Choose a complement R_t:F_2^{r_t}->F_2^n. On L_t,

    F(R_t z+v)=F(R_t z)+A_t v,

where A_t(v)=F(v)+F(0) is linear. This follows from B_i(R_t z,v)=0 for every v in L_t. For a desired prefix y, enumerate all 2^{r_t} core values z and solve

    A_t v=y+F(R_t z),  v in L_t.

Every feasible z has the same number 2^{dim L_t-rank A_t} of solutions. Pick a feasible z uniformly, then pick a solution uniformly from its affine linear solution space. This is an exact uniform prefix sampler, acquired from earlier learned output coordinates. It needs neither rare-prefix rejection nor hidden input coordinates. Since Q is bijective, every t-bit prefix is feasible and has exactly 2^{n-t} preimages.

The same operation with t=n gives the unique inverse input. The exponential is in the acquired joint polar rank r_t, not in t or n.

## Acquiring the next coordinate from its own conditional median

For any queried x, use the acquired prefix sampler to draw K=2m+1 independent uniformly distributed Y_j from {y:F(y)=F(x)}. Sort them by the original comparator and choose their median M. Define an approximate bit label

    L_t(x)=1{x is above M in the oracle order}.

Conditional on F(x), the unknown suffix rank is uniform on a set of size 2^{n-t}. Its next bit changes at the exact median. For an independent uniform x, the averaged label error is bounded by the expected distance between the sample-median quantile and one half, with a finite-grid correction. One conservative bound to be proved/checked is

    P[L_t(X)!=Q_{t+1}(X)] <= 1/(2 sqrt(K+2)) + 1/2^{n-t}.

For short suffixes, enumerate the fibre exactly and use an exact lower/upper half threshold, eliminating the grid correction. Sorting all K points is unnecessary: linear-comparison median selection suffices. All operations remain paid. Prefixes are computed from learned polynomials, not revealed by the oracle.

## Turning an averaged approximate label into an exact polynomial

For any quadratic Boolean f and three independent uniform offsets a,b,c,

    xor_{S subset {a,b,c}} f(x+sum S)=0.

Consequently the xor of the seven nonempty-vertex labels estimates f(x). Each nonempty vertex is marginally uniform, even though the seven are dependent. A union bound gives error at most 7e when the approximate label's averaged error is e. Fresh offsets and fresh median experiments make repeats independent conditional on previously learned exact coordinates. With K a sufficiently large absolute constant and exact enumeration for short fibres, 7e<1/4. Majority repetition then recovers each requested f(x) with exponentially small error.

Values at 0, e_i and e_i+e_j determine the entire quadratic ANF. There are D_n=1+n+binom(n,2) such values. Apply self-correction to each of these n D_n coordinate requests, with O(log(n D_n/delta)) repetitions. Conditional on no previous acquisition error, the next stage satisfies the same guarantee. A union bound gives exact acquisition of every Q_i with probability at least 1-delta.

## Candidate theorem and resource scale

After repairing the finite-grid median bound explicitly, the construction gives O(n^3 log(n/delta)) comparator calls up to a large absolute K/selection constant; the fibre operation costs poly(n)2^b field operations per sampled object. More precisely, comparison acquisition is O(n D_n K log(n D_n/delta)), polynomial in n and log(1/delta), with runtime/memory additionally exponential in b. It is not polynomial for arbitrary joint polar rank. Acquired ANF storage is O(n^3) bits. Oracle input transmission is 2n bits per un-cached comparison; teacher computation is not free. A real bit implementation uses exact F_2 arithmetic and finite random bits for exact uniform affine-space sampling; uniform feasible-core choice uses charged rejection for non-power-of-two counts.

This is a *bootstrap*: acquired prefix -> acquired joint polar radical and exact conditional sampler -> next coordinate acquisition. No one grants the sampler needed to learn later bits. The operation is stronger than learning a fixed model using supplied features, but it is restricted to a supplied algebraic promise.

## Nontrivial family beyond an affine-hidden complete scalar flag

Take the cube map z->z^3 on F_8, written in any F_2 basis, direct-product it with n-3 identity coordinates, then hide input/output by independently chosen invertible affine maps. Squaring in F_8 is linear, so cube is quadratic, and gcd(3,7)=1 makes it a permutation. The three-bit cube has no nonzero affine output combination: each Tr(a z^3), a!=0, has a nonzero quadratic polar form. Thus no invertible affine input/output change makes its first output coordinate affine, whereas an affine-hidden scalar triangular decoder has an affine first coordinate. This claim will be verified exactly rather than assumed from the family description. Its joint polar rank is three, independent of n.

## Strongest comparators and scientific meaning

Relevant archive governing construction: N780, COMPARISON_DECODER_THEOREM.txt and RECOGNITION_AND_NOISE.md. That construction acquires a complete hidden triangular flag; it cannot automatically be applied to the unflagged cube family above. Published comparators include low-degree polynomial self-correction, Boolean function learning, lexicographic preference elicitation, active ranking and algebraic learning. Each may use every acquired prefix and the same conditional sampler. No practical or query advantage is asserted before comparing against the strongest such construction. Full sorting costs O(n 2^n) comparisons and O(2^n) rank storage; it may win on every executable small test despite worse asymptotic class scaling.

The intended foundation is exact operational representation acquisition: a learner builds the experiment needed to acquire its next representation coordinate. It is not general intelligence, autonomous invention of its model class, cheap certification of that class, a speedup over all equally informed learners, or civilisation-level success. The potential consequence is a rigorously costed route from opaque order judgments to reusable nonlinear state and new conditional experiments; removing the bounded-core/class promise is a major open barrier.
