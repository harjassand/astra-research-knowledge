# Details that close the source and count costs

These are author-derived supplements to `COMPILER_PROOF.md`, not an independent audit. All approximation norms below are absolute operator norms. The input is the finite classical passive matrix pair `(H,E)` together with actual controlled system circuits. No relative access to an exponentially small number is assumed.

## Small-matrix arithmetic uniformly over coherent times

Write `p=ceil(log2(1/zeta))` for the desired one-particle accuracy, and let `s=ceil(log2(max(1,2RT)))`. Compute `exp(At/2^s)` by its Taylor series on a norm-bounded disk, to error at most `zeta/(100*2^s)`. The number of Taylor terms and arithmetic bits are polynomial in `p+s`, matrix dimension and input length. Square `s` times. At each step the exact target is a contraction. If the error before a square is `e`, the error after it is at most `2e+e^2`, plus the arithmetic error. Allocating the same geometric guard precision to each square gives final error `O(zeta)`. In particular, this computation takes `O(log(1+RT))` small-matrix multiplications, not `RT` time slices. It does not diagonalize a nonnormal matrix or invert `F(t)`.

The computed rational matrix `Fhat` has norm at most `1+zeta` from the certified absolute bound. Divide it by `1+2zeta` to get a genuine contraction `Fc`; then `||Fc-F||=O(zeta)`. This mathematical scaling is specified by the certified error bound, not by an approximate numerical test of contractivity.

The Julia unitary of `Fc` requires the positive square roots of `X=I-Fc Fc^dagger` and `Y=I-Fc^dagger Fc`. Regularize each by `zeta^2 I`. The square-root change is at most `zeta`. Newton's matrix iteration starting at a scalar multiple of the identity approximates the regularized square root in `O(poly(p))` steps. All eigenvalues lie in `[zeta^2,2]`; matrix inverses therefore require polynomially many **bits** in `p`, although their numerical condition number can be a power of `1/zeta`. Ordinary finite-dimensional rational matrix inversion with pivoting is polynomial in dimension and bit length. The regularization avoids an eigenvector-gap or positive-eigenvalue promise. Allocating polynomially smaller arithmetic errors at every iteration gives total square-root error `O(zeta)`.

Compute a Givens/phase QR decomposition of the resulting approximate `2M`-dimensional unitary. A vector component below a threshold `zeta/poly(M)` can be omitted at its absolute norm cost; otherwise division, square root and angle evaluation use polynomially many guard bits. Normalizing the columns or taking the nearby polar unitary, also with the preceding regularized arithmetic, gives an actual product of `O(M^2)` two-mode unitaries within `poly(M) zeta` of the exact Julia unitary. Degenerate singular values do not require identifying eigenvectors. A different choice of angles at a vanishing pivot changes only a correspondingly small residual; its arbitrary unitary completion is retained, not discarded.

Each arithmetic algorithm can be made reversible by retaining its finite operation trace and then uncomputing it after the angles have controlled their gates. Its gate and workspace costs are polynomial in `(M,p,log(1+RT),input bits)`, uniformly for every finite time word in a coherent register. Finite precision branches are deterministic functions of that word, so this is an actual coherent circuit rather than classical preprocessing of exponentially many durations. Matrix arithmetic costs are paid each time it is invoked.

## The binary Fock gate cost is not hidden in this arithmetic

For a two-mode mixing gate, use binary occupation registers and the Hamiltonian

    Hphi = exp(i phi) b_i^dagger b_j + exp(-i phi) b_j^dagger b_i.

Within intended total occupation at most `K` it is two-sparse with computable weights `sqrt[(n_i+1)n_j]`, normalization at most `2(K+1)`, and a bounded evolution angle. The row map and weights take polynomial time in `log K` and requested precision. A standard block-encoding Hamiltonian simulation therefore costs `O~(K)` elementary queries and polynomial arithmetic gates per query; a segmented Taylor construction gives the same deliberately nonoptimal conclusion. On the unused states of the individual register box one can use the explicitly bounded truncated ladder Hamiltonian, also of norm `O(K)`. Its behavior outside the intended total-number space need not equal an oscillator.

Phase gates `exp(i theta n_j)` are obtained by controlled binary rotations. For a coherently computed angle, expand its finite word into controlled fixed-angle gates, allocating the total gate-synthesis error over the word. This adds polynomial logarithmic overhead. The algorithm never computes a Fock permanent or stores `K` distinguishable particles. The permanents in the test program are solely small-instance definitions used to verify the signal block.

## CDF preparation, tiny prefixes and division

For either cumulative distribution `J` or `W`, one reversible finite-matrix evaluation supplies the mass of any addressed dyadic interval. At depth `b`, prepare the next bit by the normalized masses of its two child intervals. Thus a `B`-bit clock uses `B` coherent prefix evaluations and finite rotations, rather than a list of `2^B` probabilities.

If a prefix has total probability below `xi=eta^2/(100 B 2^B)`, choose any conditional rotation there. There are at most `2^B` prefixes at a given depth, so the sum of affected probabilities is at most `eta^2/(100B)` at that depth. For the state-error bound, select only the **first** such prefix on each path. These selected subtrees are disjoint; their ancestor rotations are unchanged. The squared difference between the two states within a subtree is at most four times its original mass. Summing the disjoint masses over depths therefore gives a squared state error `O(eta^2)`, without a triangle-inequality loss of `sqrt(B)`. On the remaining prefixes, compute masses with absolute error `O(xi eta^2/B^2)` and rotation angles to `O(eta/B)`. Division then has an explicitly positive denominator at least a constant times `xi`. Its bit length is `O(B+log(B/eta))`. Certified absolute mass errors distinguish masses above `2xi` from those below `xi`; changing the threshold by a constant covers the indeterminate strip. Clip negative finite errors and normalize each two-child vector before rotating; this always prepares an actual normalized state. The rotation-synthesis errors are added in ordinary circuit norm over the `B` levels. These operations hold uniformly over a coherent duration.

For the normalized loss direction, the convolution is omitted when `J(t)<=M eta^2`: its already explicit multiplier `sqrt(J/M)` makes the signal error at most `eta`. Otherwise the retained time cells have a lower-bounded mass. Since `|(E^dagger F)'|_F <= R |E^dagger F|_F`, the norm at a cell representative is at least its RMS norm times `exp(-R Delta)`. A retained prefix/cell and finite `B` therefore supply an absolute lower bound on the norm to be divided by. The required bits are polynomial in `B,log R,log(1/eta)` and input lengths. In the direct jump term, omit a branch of relative coefficient `beta0/w<=eta`; when retained outside the initial strip, its coefficient and the lower bound on `w` provide the same guarantee. The small strips and omitted branches are allocated explicit isometry-error budgets.

## Robust amplification from a signal-block error

Let the ideal rectangular signal block be `c V`, where `V^dagger V=I` and `c=sin(theta)`, with `(2qA+1)theta=pi/2`. Suppose the actual acquired block `X` differs by `d` in norm. The singular values of `X` differ from `c` by at most `d`. Its polar isometry differs from `V` by `O(d/c)` when `d<c/2`. Odd oblivious Grover amplification has good singular-value polynomial

    p(x)=sin[(2qA+1) arcsin(x)].

On `[-1,1]`, its derivative is at most `(2qA+1)^2` (it is a signed odd Chebyshev polynomial). Thus its good block differs from `V` by `O(qA^2 d + d/c)`. Since the amplified full circuit is unitary, the norm of the unwanted output is bounded by the square root of a constant times this good-block error. This argument uses only the acquired signal block and its adjoint; it does not assume a close or supplied unitary completion. Choosing base signal errors as a sufficiently small fourth power of the allocated final isometry error, divided by a polynomial in `A0`, is more than sufficient. All resulting precision costs stay logarithmic in inverse error.

## The emitted-count factorial inequality

Let `rho_c` be the unnormalized finite-cutoff density matrix conditional on `c` actual emitted photons, and set `X=N+c` in that sector. The free number-preserving Hamiltonian commutes with every function of `X`. A physical jump decreases `N` by one and increases `c` by one, so its entire Lindblad contribution to `E[g(X)]` cancels, including the no-jump anticommutator. No Poisson assumption about jump times is made.

For `F_k(x)=(x)_k`, the finite-difference identity is

    F_k(x+1)-F_k(x)=k F_{k-1}(x).

In an occupation basis, one normalized creation direction raises total `N` by one with coefficient at most `sqrt(N+1)<=sqrt(X+1)`. The identity

    (X+1)_k = (X+1)(X)_{k-1}

therefore gives, by weighted Cauchy-Schwarz over occupation, system, reference and count labels,

    |sum_c tr[rho_c Q a^dagger(g) (N+c)_{k-1}]|
      <= ||Q|| ||g|| sqrt(M_k M_{k-1}),
    M_k=E[(N+C)_k].

Missing raising transitions at the top cutoff only reduce this inequality. Apply it separately to each bounded coupling term and sum. It follows that

    dM_k/dt <= 2k a sqrt(M_k M_{k-1}).

Regularize a zero moment before dividing by its square root. Starting from vacuum and zero emitted count, induction integrates to `M_k(t)<=(at)^(2k)`. Expanding `exp(sX)` into nonnegative falling-factorial terms gives the stated MGF for all `s>=0`. A finite-`K` process has bounded jump rate, hence no finite-time explosion. Alternatively, prove the moment bound for a stopped count and take a monotone limit.

System-only instruments preserve these unconditional bounds, including their outcome labels and references; the argument never conditions on a rare observed outcome. The tail comparison is made against the exact process with a classical private jump record, so freezing an event of probability `p` costs at most `2p` in complete channel norm. It does not require a square-root probability estimate for a coherent public output field.

## Composing the actual operation

Each complete first-event circuit has a local isometry error that includes clock embedding, source arithmetic, Dyson tail, Gaussian gates and amplification leakage. Its induced channel error is at most twice that error. Compare the implemented capped process backwards against exact first-event instruments; CPTP continuation cannot enlarge a preceding error. This yields at most `S` local costs. The exact count-tail bound, charged tiny remaining windows, and actual prescribed system instruments complete the comparison. Rounding a private event time changes the exact continuation by at most `O(v+KR)` times the time error. Hence resolving it requires logarithmically many additional time bits.

Round `H` Hermitian and keep the loss supplied as a rounded factor `E`, forming the damping matrix from that factor. Then CP is preserved. On the finite cutoff, coefficient perturbations in the generator have norm bounded by a polynomial in `K,||E||,h,q_j` times their absolute entry errors. Contractive Duhamel multiplies this by `T`, so the precision requirement is logarithmic in `R,T,1/epsilon`, not a separate rate-dependent number of gates. The spectrum and infinite-Fock errors are received separately from the frozen first-stage derivation.

These details support a constructive polynomial upper bound. They do not supply an optimized fault-tolerant circuit, independent proof review or a practical runtime advantage.
