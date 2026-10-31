# Dimension-free decaying kernel from an acquired power-contraction certificate

31 October 2026. Constructive operator lemma, pending independent review. This is a direct application of established block-encoding, uniform singular-value amplification and LCU tools, not a novelty claim or a complete reservoir-process compiler.

## 1. Interface and claim

Let A act on a finite-dimensional encoded register, with ||A|| <= 1. An actual normalization-one block encoding U_A, its inverse and controlled versions are acquired. Their implementation costs are paid separately. Let P be an orthogonal projector reducing A, and Q=I-P. A controlled reflection about P is acquired. A certified integer m>=1 satisfies

    ||A^m Q|| <= 1/4.

The certificate and access are inputs, not inferred from a small spectral radius or a Markov mixing assertion in an unspecified norm. The system dimension is not enumerated. Define

    q=2^(-1/m), a=1-q, a'=a/2,
    F(t)=(1/2) exp(a't) exp[t(A-I)] Q,    t>=0.

For 0<epsilon<1/4 there is a normalization-one block encoding of F(t) with operator error <=epsilon and resource cost polynomial in m, log(1/epsilon), the finite input-bit length of t and the supplied oracle costs, uniformly in t. An explicit oracle-query upper bound below is O(m ell log((ell+1)/epsilon)+m), where ell=ceil(log_2(16/epsilon)); additional source arithmetic is polynomial in m and ell. No inverse output norm is included: this is a block encoding, not guaranteed preparation of F(t)|v>/||F(t)|v>||.

The statement also applies coherently to a finite binary t register. Arithmetic, branching, state preparation and their inverses must then be controlled coherently. It is not a free continuous-real-input oracle. A real t approximated by a binary value within h changes F by at most 3h, as shown below.

## 2. Exact algebra and a uniform norm bound

Reduction gives AQ=QA and hence A^n Q=(AQ)^n Q. Set

    B=2 A^m Q,    ||B||<=1/2.

For n=km+r, 0<=r<m,

    A^n Q = 2^(-k) B^k A^r Q.

The k=0 case means A^r Q; Q is still required, including n=0. Expanding the exponential yields

    F(t) = sum_(n>=0) w_n(t) B^k A^r Q,
    w_n(t) = exp(-a't) Pr[Poi(qt)=n] 2^(r/m-1).

Indeed q^n=2^(-k-r/m), and a'+q=1-a'. Every weight is nonnegative and

    sum_n w_n(t) <= exp(-a't) <= 1.

All selected operator products are contractions, so ||F(t)||<=exp(-a't). This argument uses ordinary matrix products, not a mistaken substitution of singular-value powers for nonnormal matrix powers.

For m>=1, setting x=(log 2)/m gives 1-exp(-x)>=x/2 and log 2>=1/2, so

    a' >= 1/(8m).

Also F'(t)=(A-I+a'I)F(t), and therefore ||F'(t)||<=3 for t>=0. A finite-bit time approximation incurs at most 3|Delta t| in operator norm. This bound does not grow with t.

## 3. Fully finite time and power caps

Use the integer quantities

    ell=ceil(log_2(16/epsilon)),
    T_*=8m ell,
    K=2(T_*+ell),
    J=floor(K/m).

If the binary input t>=T_*, return an exact zero block. Its error is <=exp(-ell)<=2^(-ell)<=epsilon/16. This is a reversible comparison, not evaluation of a huge exponential.

For 0<=t<T_*, the Poisson mean mu=qt is at most T_*. Since E 2^N=exp(mu) for N~Poi(mu),

    Pr[N>K] <= exp(T_*) 2^(-K) <= exp(-ell) <= epsilon/16.

Here log 2>=1/2 suffices. Deleting all terms n>K therefore incurs at most epsilon/16 in operator norm. The explicit caps are K=O(m ell) and J=O(ell). No large-rate path or system-basis enumeration is hidden in this truncation.

## 4. Acquiring B is an approximate singular-value operation

A block encoding of C=A^m Q uses m applications of U_A and one encoding of Q, with fresh product ancillas. The encoding of Q is the two-term LCU of I and the acquired reflection 2P-I with opposite sign. Products use fresh ancillary blocks so their top block is the product of the top blocks.

Because all singular values of C are <=1/4, standard uniform singular-value amplification, with amplification factor 2 and a fixed slack interval larger than [0,1/4], constructs a unitary whose top block B_tilde satisfies

    ||B_tilde-2C|| <= eta_B,
    ||B_tilde|| <= 1,

using O(log(1/eta_B)) calls to the block encoding of C and its inverse, and polynomial classical phase-generation/finite-precision work. For instance the approximating bounded odd polynomial is required to approximate 2x on [0,1/4], with a constant gap before its saturation region. The usual efficient uniform-amplification construction supplies this polynomial and QSVT phases.

This is NOT exact amplification of an arbitrary continuum of singular values by a finite circuit. The approximation is part of the error ledger. Since B is a contraction and B_tilde is the block of a unitary,

    ||B_tilde^k-B^k|| <= k eta_B.

Choose eta_B=epsilon/[64(J+1)]. The averaged error over all retained powers is then <=epsilon/64.

Access precision convention: the clean oracle model treats U_A and the projector reflection as exact supplied unitaries. In a gate implementation, approximate these unitaries in operator norm so the sum of errors over every forward/inverse/controlled use is <=epsilon/64. This is an explicit unitary-synthesis promise, not an assertion that an arbitrary fixed noisy block encoding can be refined. If only a fixed block error is supplied, its robustness must be charged using an appropriate QSVT perturbation theorem; this note does not silently replace that input by exact access.

## 5. Actual SELECT circuit and normalization one

For the retained index n compute k=floor(n/m), r=n mod m reversibly. Apply Q, then r copies of A, then k copies of B_tilde, all by ordinary block-encoding products. Implement the variable counts by fixed loops of m-1 and J conditional calls. Give every product factor fresh ancillas. Inactive slots apply identity. All loop flags and arithmetic are uncomputed; no success measurement is made between factors.

The resulting selected top block is B_tilde^k A^r Q. Unused product ancillas may remain in failure spaces; they are part of the global block encoding, not silently reset. The circuit has at most

    J O(log(1/eta_B)) (m U_A calls + one Q call)
      + (m-1) U_A calls + one Q call.

Controlled versions are charged. There is no enumeration of system vectors or sectors.

Prepare an index state with amplitudes sqrt(w_n) for n=0,...,K, and a residual arm of probability 1-sum_(n<=K)w_n. On the residual arm SELECT is a zero contraction, implemented by flipping an extra success flag. PREPARE-dagger SELECT PREPARE has exactly the desired truncated weighted sum in its top block. It already has normalization one. No amplification of a lone nonunitary output and no postselection are needed.

## 6. Finite arithmetic and an acquired Poisson-weight source

On the active branch all arguments t,qt are bounded by T_*=O(m ell). Each w_n is an elementary computable real. The n=0 and t=0 branches are explicit; for positive mu one can evaluate

    log w_n = -a't-mu+n log(mu)-log(n!)+(r/m-1)log 2.

Factorials involve only n<=K=O(m ell). Exact integer factorials and interval logarithms thus have polynomial bit cost. Exponentials with an exponent below the output precision threshold may be bounded by an interval near zero rather than evaluated relatively. Standard rational interval series with range reduction give b-bit absolute intervals in polynomial(m,ell,b,input bits) time; no tiny endpoint probability is inverted.

For each n compute a nonnegative dyadic lower bound wbar_n<=w_n with deficit <=2^(-b). Choose b so

    (K+1) 2^(-b) <= epsilon^2/2^18.

Set the residual dyadic probability to exactly 1-sum wbar_n. It is nonnegative. The L1 difference of the complete probability vectors, including the residual arm, is at most twice the deficit. Consequently the Euclidean distance of their square-root amplitude vectors is at most the square root of that L1 bound. PREPARE and UNPREPARE then change the weighted contraction by at most twice this state-vector distance, less than epsilon/64 with the displayed budget.

An explicit finite source circuit can prepare these K+2 dyadic probabilities by a binary tree of prefix sums and conditional rotations. All nonzero sums are >=2^(-b), so division and square-root/angle arithmetic need only polynomially many bits; zero sums have a separate deterministic branch. There are O(K) rotations. Synthesize their total operator error <=epsilon/64. This source is deliberately not optimized: O(K) data and polynomial(K,b) reversible arithmetic suffice. It does not enumerate an exponentially large physical state space.

For coherent binary t, compute all these dyadic lower bounds and prefix sums reversibly, apply the controlled preparation, then uncompute the work. Approximation bounds hold uniformly in each t block, hence in operator norm for a superposition of t values. PREPARE and its adjoint use the same deterministic arithmetic. This requires no random classical Poisson oracle and no quantum-access promise to an unexplained table.

## 7. Error and resource ledger

Allocate epsilon/16 to the large-time zero branch and epsilon/16 to the active Poisson tail; epsilon/64 each to B-power error, probability-vector approximation, preparation synthesis and primitive unitary synthesis. Reserve another epsilon/16 for optional time rounding h<=epsilon/48. The sum is strictly below epsilon; budgets can be loosened without changing complexity.

The maximum number of A-oracle calls is

    O(m ell log((ell+1)/epsilon)+m).

Reflection, controlled-comparison, arithmetic, workspace and rotation costs are polynomial in m, ell and input-bit lengths. Actual U_A/reflection costs multiply their respective query counts. Product ancilla workspace is polynomial in the same parameters times the supplied encoding workspace. There is no implicit promise of logarithmic dependence on m: constructing A^m is paid directly. Huge t costs its finite input length, not t, after the threshold comparison. In a coherent implementation the worst-case active branch cost is paid.

An application wanting a normalized output state still pays success probability ||F(t)v||^2 and the relevant inverse-norm/amplification costs. An application wanting a complete CP instrument must construct its other Kraus branches and normalize the whole isometry. Neither follows from this block-encoding lemma alone.

## 8. Strong ordinary contour comparator from the SAME certificate

The certificate also yields a useful resolvent bound for an established alternative. Put C=AQ on the whole register, so C^m=A^mQ and ||C||<=1. On the circle |z|=q,

    (zI-C)^(-1)
      = [sum_(r=0)^(m-1) C^r z^(-r-1)]
        [I-C^m z^(-m)]^(-1).

Since q^(-m)=2 and ||C^m||<=1/4, the second inverse has norm <=2; each term in the first sum is <=q^(-m)=2. Therefore

    ||(zI-C)^(-1)|| <= 4m.

The contour encloses the spectrum because rho(C)<=4^(-1/m)<q. For

    f_t(z)=(1/2) exp[-(1-a')t+tz],

we have max_|z|=q |f_t(z)| <= (1/2)exp(-a't), and max |f'_t(z)| <=1/(2 e a')=O(m), uniformly in t. Also f_t(C)Q=F(t).

Thus this same acquisition certificate supplies dimension-free polynomial bounds for an ordinary contour-integral/QSVT-resolvent/LCU route. Its initial block normalization can scale polynomially in m and then be reduced using uniform singular-value amplification with slack. Indeed ||exp[t(A-I)]||<=1 by its positive Poisson expansion, so ||F(t)||<=min((1/2)exp(a't),exp(-a't))<=1/sqrt(2), uniformly in t. This supplies fixed slack without any diagonalization. This paragraph is an explicit comparator route, not a separately audited optimized gate theorem. It already defeats any inference that efficient nonnormal functional calculus is absent from the literature.

## 9. Primary-source scope and exclusions

[Gilyén, Su, Low and Wiebe](https://arxiv.org/abs/1806.01838) supply QSVT, uniform amplification, multiplication/LCU and related standard primitives. Here QSVT scales singular values only to obtain approximately 2A^mQ; subsequent powers are actual matrix products. We do not apply a scalar exponential to singular values and call it exp(tA).

[Jiang and An, 2026](https://arxiv.org/html/2601.11959v1) analyze contour-integral quantum eigenvalue transformation for nonnormal matrices. Their parameters include contour function bounds, contour length and resolvent norm; they explicitly discuss asymptotically stable ODE fast forwarding. The bounds in Section 8 instantiate the relevant analytic parameters from an algorithmic power certificate. Their normalized-output state task and this absolute-error operator task must not be conflated.

[Li and An, 2026](https://arxiv.org/html/2608.25822v1) describe T-independent LCHS-based solvers under strict logarithmic-norm dissipation and discuss contour alternatives beyond that premise. [An, Onwunta and Yang](https://quantum-journal.org/papers/q-2026-01-27-1986/) give dissipative history/final-state fast-forwarding results. These are strong ordinary alternatives; this note makes no novelty or optimality claim.

[Apers and Sarlette](https://arxiv.org/abs/1804.02321) fast-forward reversible Markov-chain discriminants. Their discriminant is not automatically a given nonreversible transition operator in the required Hilbert norm. Likewise, total-variation mixing or coupling of a random-map chain does not automatically supply the stated block encoding and operator-norm power certificate.


## 10. What this closes and what it does not

If a source realization actually supplies A, the reflectable reducing P and a polynomial m certificate, this construction replaces a dense exponential-kernel call by a dimension-free acquired operator circuit with absolute error. It does not acquire those inputs, prove a random-map physical realization, price a jump stack, or close a retained-memory complete-isometry process. It is not evidence that a new general learning operation or a civilisation-scale capability has been obtained. Its immediate value is a concrete, checkable interface improvement in a larger construction.

A sharp premise limitation: the D-dimensional nilpotent unilateral shift S has ||S||=1 and spectrum {0}, but ||S^j||=1 for every j<D. With P=0 its first power certificate at threshold 1/4 therefore requires m>=D. A constant eigenvalue gap does not give a polynomial-register-size m for a nonnormal operator. The acquired power/survival certificate, not spectral stability alone, carries this resource improvement.
