# Ordinary quantum capacity: a constructive regularization equivalence and the unresolved boundary

This is r2's initial independent full attempt for the bounded Sol pilot, 6 November 2026. The common question is **unresolved by this attempt**. I constructed neither the requested total quarter-bit evaluator nor a proof that it cannot exist. The implemented algorithm computes finite-block coherent information and an increasing sequence converging to capacity. Its lack of a stopping certificate is explicit.

The main mathematical deduction here is an exact equivalence: a total quarter-bit evaluator on variable-dimensional rational Choi inputs exists if and only if a sufficient approximation block length can be computed from the input dimension, output dimension and desired error alone. The sufficient block length can be independent of channel coefficients and their bit length. A nonconstructive dimension-only bound already follows from compactness and continuity. Making that bound computable is precisely the missing operation, not a consequence of its existence.

This deduction is not claimed as a new result in the literature. It is a useful complete reduction of the evaluation direction, with its finite operations supplied. It does not close the common question.

## 1. Setup and the equivalence

Let a and b be the channel's input and output dimensions and let C(a,b) be the compact set of all normalized Choi matrices J >= 0, Tr_B J = I_A/a. Define

    A_n(N) = max_rho I_c(rho,N^tensor n),
    f_n(N) = A_n(N)/n,
    L_m(N) = max_{1<=n<=m} f_n(N).

Pure inputs give coherent information zero, so A_n >= 0. Product input states prove superadditivity of A_n. The coding formula gives L_m increasing pointwise to Q.

**Theorem.** The following uniform statements are equivalent.

1. A total algorithm approximates ordinary Q to error 1/4 on every promised-valid finite rational-complex normalized Choi matrix, with dimensions included in its finite input.
2. A total algorithm approximates Q on those inputs to every positive rational error.
3. A total computable function F(a,b,epsilon) returns m such that, for every channel N in C(a,b), including channels whose entries are not computable,

       0 <= Q(N)-L_m(N) <= epsilon.

4. A total computable function G(a,b,epsilon) returns one block length n such that, for every N in C(a,b),

       0 <= Q(N)-f_n(N) <= epsilon.

Only the usual ordinary capacity occurs in this theorem. References used to evaluate coherent information are mathematical purifying references, not physical auxiliary transmission resources.

### 1.1 Fixed error implies arbitrary accuracy, with the full description cost

Given N and epsilon, choose k >= max(1,ceil(1/(4 epsilon))). Form the actual normalized Choi matrix of N^tensor k by tensoring J and rearranging indices into (A^k,B^k) order. Call the supposed quarter-bit evaluator and divide its rational answer by k.

The identity Q(N^tensor k)=kQ(N) follows directly from superadditivity: the subsequence of block lengths divisible by k has the same limiting rate. More explicitly, repeat an arbitrary fixed n0-block input into arbitrarily long multiples of k and pad unused factors by pure states. The reverse inequality follows from the definition of Q.

The new input and output dimensions are a^k and b^k. Its Choi matrix has (ab)^(2k) entries. If each real or imaginary rational component originally has at most ell bits in numerator and denominator, each tensor entry has O(k ell) bits before optional common-denominator consolidation. Forming the tensor input therefore costs at least its explicit output length, O((ab)^(2k) k ell) bits, and polynomial arithmetic overhead per entry. The evaluator's unknown running time on this expanded description must then be paid. This is a finite computability reduction with no efficiency assertion.

### 1.2 A finite rational channel net can be constructed

The channel set is an effectively described compact semialgebraic set. Here is a direct rational net construction, so this step is not an unconstructed acquisition operation.

Write D=ab and J_dep=I_D/D. Choose a rational Hermitian basis H_1,...,H_t for the zero-partial-trace affine directions, where t=a^2(b^2-1). One choice is a Hermitian matrix-unit basis on A tensored with a traceless Hermitian matrix-unit basis on B. Each basis element has operator norm at most one. Every J is J_dep + sum_j c_j H_j, and the coordinate coefficients have a dimension-computable uniform bound |c_j|<=C: invert the finite rational coefficient matrix and use the fact that every entry of a positive trace-one J has modulus at most one.

Fix rational 0<eta<=1/2, put lambda=eta/(8a), and replace an arbitrary J by

    J_lambda=(1-lambda)J+lambda J_dep.

Its smallest eigenvalue is at least lambda/D. Round its coefficients to a rational grid of mesh h=lambda/(D t), increasing the finite coordinate box by one mesh point at its boundary. The operator error is at most t h/2=lambda/(2D), so the rounded matrix remains positive. Partial trace is exact by the basis choice. The trace-norm rounding error is at most lambda/2, and mixing contributed at most 2lambda.

For normalized Choi matrices, the diamond norm obeys

    ||N-M||_diamond <= a ||J_N-J_M||_1.

Consequently the rounded channel is within 5a lambda/2 < eta in diamond norm. Enumerate the finite coefficient grid and retain precisely the positive semidefinite matrices; exact rational principal minors give a terminating validity test. The resulting valid rational channels form the required eta-net. Its cardinality is at most (2 ceil((C+h)/h)+1)^t. For b=1 the channel set is a singleton and Q=0.

Thus calling an evaluator at every point of this net involves only promised-valid rational inputs. The construction does not require a capacity oracle to acquire the net.

### 1.3 The same effective continuity bound holds before and after regularization

The Leung–Smith entropy telescoping argument gives, when ||N-M||_diamond<=eta<=1/2,

    |f_n(N)-f_n(M)| <= omega_b(eta),
    |L_m(N)-L_m(M)| <= omega_b(eta),
    |Q(N)-Q(M)| <= omega_b(eta),
    omega_b(eta)=8 eta log_2 b+4 h_2(eta).

The bound is uniform in n and m. The first bound applies the same fixed-input output-entropy estimate to S(B^n) and S(RB^n) and then takes maxima; the input purifying reference can have dimension a^n. The remaining bounds follow by finite maxima and the pointwise limit. These are the quantitative ingredients in [Leung and Smith, Corollary 14 and its proof](https://arxiv.org/html/0810.4931).

For a fully rational search, at eta=2^-s use

    omega_b(eta) <= 2^-s(8 ceil(log_2 b)+4s+8),

because h_2(2^-s)<=2^-s(s+2). The right side tends effectively to zero.

### 1.4 Building a uniform cutoff from an evaluator

Assume statement 2, fix a,b,epsilon, and choose the above net with omega_b(eta)<=epsilon/16. At every net channel M call the evaluator with error epsilon/16, obtaining v_M. For m=1,2,... compute w_(m,M) with

    |w_(m,M)-L_m(M)| <= epsilon/16

using the complete finite-block algorithm in Section 2. Stop at the first m for which, at every net point,

    v_M-w_(m,M) < epsilon/2.

This is a strict rational test on a known finite list. It eventually passes, since L_m(M) tends to Q(M) and the limiting discrepancy is at most epsilon/8. At that m,

    Q(M)-L_m(M) < 5epsilon/8

on the net. Moving an arbitrary channel to a net point costs at most two continuity errors, so

    Q(N)-L_m(N) < 3epsilon/4 < epsilon.

This constructs F solely from a,b,epsilon and the hypothesized evaluator. There is no hidden oracle in the net or fixed-block routines. The sole hypothetical component is the capacity evaluator itself.

### 1.5 The other implications

If F exists, compute m=F(a,b,epsilon/2) and approximate L_m(N) to error epsilon/2. The resulting rational number approximates Q to error epsilon. All optimizations are finite and supplied below.

To pass from F to one block, take n=lcm(1,...,m), or the larger computable n=m!. Every j<=m divides n, so superadditivity implies f_n>=f_j and hence f_n>=L_m. Conversely, if G exists, L_G>=f_G. This proves the equivalence.

The cost of computing F from an evaluator includes the full channel-net acquisition, all amplified evaluator calls, every increasing finite-block search through its stopping m, and the extremely large state nets. No bound for these costs is asserted. In particular, this equivalence is not itself an evaluator: it supplies no F independently of the unknown evaluator.

### 1.6 What compactness alone really supplies

Each L_m is continuous, L_m increases to continuous Q, and C(a,b) is compact. An elementary finite-cover proof, equivalently Dini's theorem, therefore guarantees that for every fixed a,b,epsilon some finite sufficient m exists uniformly over channels.

This proves existence of each integer separately. It does not produce a computable map (a,b,epsilon)->m. The constructive argument in 1.4 shows exactly how a capacity evaluator would make that existence effective, rather than assuming an effective Dini theorem can manufacture its own limit evaluator.

For fixed a,b and a fixed error, that integer could be hardcoded nonuniformly into some finite program. A single uniform program for all dimensions and errors cannot hardcode an arbitrary countable table. This is why the varying-dimension contract in the common question matters.

## 2. Supplied finite-block engine

[finite_block.py](finite_block.py) implements the following total finite calculation. It accepts rational-complex channel matrix-unit images, or constructs them from the promised-valid normalized Choi matrix. No complementary-channel factorization or irrational square root is required.

For block n, use a pure input on R A^n with dim R=a^n. A nonzero vector of Gaussian integers w defines the exactly rational density |w><w|/<w|w>. On this purification,

    I_c(rho_A,N^n)=S(B^n)-S(RB^n).

Both output density matrices are rational complex when J is rational complex. Thus the true entropy-exchange term is evaluated through the actual channel, not through an independently chosen environment.

### 2.1 Certified rational entropy without a numerical eigenvalue oracle

For 0<=x<=1,

    -x ln x = sum_(k>=1) x(1-x)^k/k,
    0 <= -x ln x - sum_(k=1)^m x(1-x)^k/k <= 1/(m+1).

The remainder bound follows by replacing 1/k by 1/(m+1) and summing the geometric series; at x=0 it follows by continuity. For a D-dimensional density matrix X, exact rational matrix multiplication gives

    P_m(X)=sum_(k=1)^m Tr[X(I-X)^k]/k,
    P_m(X) <= S_nats(X) <= P_m(X)+D/(m+1).

Certified rational bounds for ln 2 come from

    ln2=2 sum_(j>=0) 3^(-2j-1)/(2j+1).

After j=0,...,l-1 the positive tail is at most

    9 / [4(2l+1)3^(2l+1)].

Dividing the entropy bounds by the corresponding upper/lower logarithm bounds yields a certified rational interval. The implementation chooses m=ceil(4D/tau) and sufficient l to obtain interval width at most tau. Rank-deficient outputs and zero eigenvalues require no special numerical regularization.

### 2.2 A complete finite state net and its size

Let L=a^(2n) be the number of complex purification amplitudes. Round the 2L real coordinates of a unit vector to multiples of 1/M, then normalize. If M>=sqrt(2L)/delta and delta<=1/2, the resulting pure-state trace distance is at most delta. Integer coordinates in [-M,M] therefore supply a finite net of size

    (2M+1)^(2L)-1.

Contractivity and the entropy continuity inequality give coherent-information error at most

    delta [ceil(log_2 b^n)+ceil(log_2 (ab)^n)] +2h_2(delta).

The entropy inequality is the usual sharp finite-dimensional continuity bound of [Audenaert](https://arxiv.org/abs/quant-ph/0610146). Choosing delta=2^-s turns the last display into the rational bound used in the executable:

    2^-s [ceil(log_2 b^n)+ceil(log_2 (ab)^n)+2s+4].

The code chooses this at most half its requested block error, evaluates every candidate to an entropy-interval error using the remaining half, and takes maxima. Both the finite upper bound on A_n and a certified lower bound are produced. The exhaustive nontrivial search is implemented, but was not executed in this run.

As an actual size example, its one-use qubit-to-qubit net for block error 1/4 has **31,145,186,800,345,706,772,049,920 candidates**. That is a dimension/precision cost, not evidence that no faster algorithm exists.

For each candidate, the two entropy matrices have dimensions b^n and (ab)^n. The larger polynomial degree is O((ab)^n/tau), using O(degree * (ab)^(3n)) rational arithmetic operations with dense multiplication, plus the exact channel action. Rational numerator and denominator bit lengths increase with polynomial degree and the full input denominator length; no unit-cost real arithmetic is assumed. One can consolidate each rational matrix to a common denominator before the powers: a conservative bit bound after degree m is O(m D^2 ell_out + m log m + m log D), where D is that entropy-matrix dimension and ell_out bounds its entry descriptions.

`capacity_lower_bounds` performs successively refined complete finite-block searches, retaining the largest certified rational lower bound. Every yielded stage terminates and the sequence increases to Q. It contains no stopping certificate for the desired global quarter-bit error.

### 2.3 Executed checks and limits

`python3 finite_block.py` ran successfully under the already installed SymPy 1.14.0. [checks.json](checks.json) records eleven checks, completing in about 1.47 seconds of script wall time:

- exact entropy brackets for a pure state, a maximally mixed qubit, a rank-deficient four-level state and a complex pure state;
- rational normalized-Choi positivity/trace preservation/reconstruction and coherent-information brackets at five qubit erasure probabilities, compared with the independent exact value 1-2p for maximally mixed input;
- exact tensor-channel construction with a complex phase channel;
- one actually executed complete state-net enumeration in the degenerate one-dimensional case.

The nontrivial complete qubit state net was only counted. These are implementation checks for supplied finite operations. They do not establish capacity computability, noncomputability, a convergence rate or a physical communication advantage. The complete-net generator is not presented as a practical numerical method.

## 3. The noncomputability direction was pursued at the actual resource boundary

I read the governing quantified statement of accepted N675, including the bounded entropy defect, the computable witness margin and its tensor amplification. Its correctness and internal dependencies were accepted as instructed, without a new audit. Its reference dimension is finite for every witness, but has no supplied computable bound. The theorem compares arbitrary faithful state pairs with no equal-reference-marginal restriction.

I also read the available full visible originals of N1677 and N1680 and the in-place N684 extraction. No unavailable PDF or ZIP was fetched or recovered. Their completed assisted and stationary-catalyst results were credited at their stated scopes.

The useful no-case structure is complete environmental order, which survives tensoring self-complementary helpers and forces zero ordinary capacity. The yes case has a computable complete entropy/Holevo advantage before paying an arbitrarily large symmetric helper. N684's fixed-qubit half-erasure compilation preserves positivity at zero logical rate; the helper block length depends on a finite witness dimension and accuracy. Hence its positive ordinary rate has no supplied computable lower bound. N1680's paid sequential source construction moves the unknown dimension into a boundary cost, but retains a signed extensive history correction with no adequate lower bound.

I tried to eliminate the large-reference charge by preparing a state on a small Alice system and a large Bob reference using only a small purifying wire. Every individual state rho_AR indeed has a purification with Schmidt rank at most dim A, so Bob can locally generate its large R from a small purifying partner. This does **not** transfer the entropy advantage of a pair of states at no cost. The required local channel or discarded purifier is state dependent; combining letters into one larger purification makes the discarded system retain letter-dependent correlations. In an actual half-erasure dilation the receiver/environment see the complete delivered purification in the corresponding branch. Replacing that purification by only R changes the true complementary output. I obtained no inequality preserving the receiver-minus-environment advantage through this replacement.

The same defect appears in a convex-split/state-splitting attempt: bounded communication can coexist with consuming an unbounded shared entangled resource. N1680 already explicitly supplies that observation for its repaired source. Checking Bob's maximally mixed local reservoir marginal is not exact joint catalyst return.

I further considered repeated weak source interactions with a finite memory. The ordinary input can have arbitrarily large virtual memory without that memory entering the channel description, which is allowed. However, physical future outputs are a lossy channel of that memory, not the untouched reference in N675. A mixing estimate on the retained memory does not reverse this loss, and a finite-dimensional input/output wire does not give both complementary parties an untouched quantum reference. No positive-fraction lower bound on the signed history correction was constructed. A claimed generic telescoping or a paid bounded wire alone would therefore repeat an explicitly identified predecessor failure.

These are failed constructions, not exclusions of every possible construction. In particular, I have no global impossibility theorem for a mixed shield-preserving catalytic transition.

## 4. Why the available hardness and asymptotic facts do not resolve the equivalence

The governing [Bhattacharyya–Mehta–Zhao v3](https://arxiv.org/html/2601.22471v3) passages distinguish succinct-circuit QMA hardness of a constant-gap ordinary-capacity promise from their restricted maximally-entangled-assisted, one-shot, zero-error classical undecidability result. Expanding circuits to explicit matrices changes size, and neither assertion rules out unrestricted terminating computation on explicit Choi matrices.

[Cubitt et al.](https://doi.org/10.1038/ncomms7739) rule out a universal fixed detection block. This does not rule out a computable approximation block F(a,b,epsilon) as in Section 1. Their construction can require growing channel dimensions and arbitrarily small rates.

The regularized Rényi characterization in [Cheng and Tomamichel](https://arxiv.org/html/2609.08998) compares Rényi order with order one uniformly over block size, and yields a strong converse above Q. Its optimized Rényi block quantities are themselves superadditive and regularized. The argument supplies no independently computable upper sequence converging to Q. Substituting a stabilized channel divergence can change the optimization and must not be treated as the same quantity.

Public searches also exposed the existing [Hirche channel-order paper](https://arxiv.org/html/2610.03706) and [Zhu–Wang private-capacity activation paper](https://arxiv.org/html/2609.10520). Their restricted structural and activation examples were considered, not imported as a general evaluator or quantitative transfer from N675. This was incidental public-source exposure, not exposure to another pilot constructor's developing result.

An elementary countermodel explains the logical gap without claiming to model actual channels. For program e, define c_e=2^-t if it first halts at step t, and c_e=0 if it never halts. The function (e,epsilon)->c_e is computable to error epsilon by simulating only ceil(log_2(1/epsilon)) steps. Yet c_e=0 is coRE-complete. The block sequence

    a_n(e)=n 2^-t if e halts at t<=n, and 0 otherwise

is uniformly computable and superadditive, and a_n/n increases to c_e. Its first positive block is unbounded. Thus undecidable zero testing and unbounded detection blocks can coexist with a total approximation algorithm. This only refutes that inference pattern; it proves no assertion about ordinary Q.

## 5. Remaining central operation and actual resource use

The evaluator route requires an independently constructed computable F(a,b,epsilon), or any converging certified upper approximation from which such an F follows. This attempt supplies the finite optimizations and effective channel nets, but not F.

The hardness route requires a finite rational channel, computable without a witness dimension, whose ordinary capacity is zero in the nonhalting case and at least a computable positive g(instance) in the halting case. Tensor amplification could then be selected from actual instance data. Accepted N675 and the available predecessor interfaces do not by themselves supply that ordinary rate lower bound, and this attempt has not constructed it.

Acquisition used read-only local exact originals and ordinary public web reads/searches. There were nine web tool requests, containing fourteen search queries plus direct governing-source reads/finds. No inaccessible predecessor attachment was retried; no installation, paid/API service, physical experiment, outreach, shared-source write or descendant agent was used. All new files are in this r2 directory. SymPy was already installed; eleven finite checks were actually run. Scientific work time and model use are governed by the lead's bounded pilot; the script's measured runtime is not a claim about reasoning compute.

No quarter-bit answer can honestly be produced for a general input from the supplied program. The full common question remains unresolved, despite the completed equivalence and finite-block construction.
