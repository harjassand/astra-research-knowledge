# Ordinary quantum capacity: constructive attempt and exact remaining boundary

Initial independent construction, r3, 6 November 2026.

I did not construct the requested total evaluator or prove that it cannot exist. The full ordinary-capacity question remains unresolved in this attempt. What follows contains complete finite-block algorithms and equivalences, followed by the specific upper-bound and hardness bridges I pursued and could not close. None of the model counterexamples below is claimed to be a family of quantum channels.

The principal representation was computational analysis of the entropy functional, rather than transport of the predecessor's quantum reference. In particular, the finite-block calculation below uses the given channel itself, and charges its full tensor-power matrix. It introduces no assisting channel or shared state.

## 1. A fully rational finite-block procedure

Let a=dim A, b=dim B, and

    a_n(N)=max_rho I_c(rho,N^n),    f_n(N)=a_n(N)/n.

Here and below, a superscript n on a channel denotes its tensor power. Pure input states imply a_n>=0, and a_n<=n log_2 a. Product inputs imply a_{n+m}>=a_n+a_m. Thus f_n converges to Q by Fekete's lemma, although it need not increase with n.

**Proposition 1.** Given a valid normalized rational-complex Choi matrix J, a positive integer n, and a rational eta>0, there is a terminating rational-arithmetic procedure returning [L,U] with

    L <= f_n(N) <= U,    U-L <= eta.

The following is an explicit construction, including singular states. It avoids assuming a rational Stinespring dilation or numerical eigenvalue solver.

### 1.1 Exact entropy intervals

For a rational-complex density matrix X of dimension d, put Y=I-X. The scalar identity

    -x ln x = sum_{k>=1} x(1-x)^k/k

holds on [0,1], including both endpoints by continuity. Consequently

    A_m(X)=sum_{k=1}^m Tr[X Y^k]/k

is rational, and

    A_m(X) <= S_nat(X) <= A_m(X)+d/(m+1).                  (1)

For each eigenvalue x>0, the omitted tail is at most

    (1/(m+1)) sum_{k>m} x(1-x)^k
       = (1-x)^(m+1)/(m+1) <= 1/(m+1).

The zero-eigenvalue tail is zero, so (1) remains valid without a positive spectral gap. Every summand is nonnegative. If the matrix X Y^k becomes exactly zero, the remaining series vanishes exactly.

To convert to bits, use the rational expansion

    ln 2 = 2 sum_{j>=0} 1/[(2j+1) 3^(2j+1)].

After j terms its tail is bounded by

    9 / [4(2j+1)3^(2j+1)].

If ell<=ln 2<=u are such rational bounds, then

    A_m/u <= S(X) <= [A_m+d/(m+1)]/ell.                 (2)

Take m=ceil(8d/epsilon), and make u-ell<=epsilon/(16d). Since ell>=2/3, A_m<=ln d<=d, the interval in (2) has width less than epsilon. All operations, including the stopping test for the logarithm series, are rational and terminate.

### 1.2 No hidden reference resource in the computation

Set d_A=a^n and d_B=b^n. Every physical input state on A^n has a purification u on R A^n with dim R=d_A. For any nonzero vector v with rational-complex coordinates, use the normalized density matrix

    |v><v| / <v|v>.

It has rational-complex entries. The channel output on R B^n also has rational-complex entries, and

    I_c = S(B^n)-S(R B^n).                              (3)

Equation (3) is the usual coherent information: for a pure R A^n input, R B^n has the same nonzero spectrum as the actual complementary output. The reference is used by the mathematical evaluator to represent the input purification; it is not a wire supplied to the communication protocol.

For the normalized Choi convention,

    N(|i><j|)_{kl} = a J_{ik,jl}.

Tensoring these rational output blocks constructs N^n exactly, with the requisite input/output index permutation.

### 1.3 A finite covering with an explicit size

There are D=d_A^2=a^(2n) complex coordinates in u. Round each real and imaginary coordinate of K u to a nearest integer, obtaining a nonzero Gaussian-integer vector v. Its normalized version satisfies

    ||u-v/||v||||_2 <= sqrt(2D)/K.

The trace distance of the corresponding pure states is no larger; channel processing cannot increase it.

Let L_a=ceil(log_2 a), L_b=ceil(log_2 b), C=L_a+2L_b, and delta=eta/2. If C=0 the capacity is zero. Otherwise choose

    t = min{1/4, delta/(2C), (delta/12)^2},
    K = ceil(2D/t).                                     (4)

The elementary entropy-continuity bound gives, for trace distance <=t,

    |I_c(u)-I_c(v)|/n
       <= t(log_2 a+2log_2 b)+2h_2(t)/n
       <= t C+6 sqrt(t) <= delta.                       (5)

Here h_2(t)<=3 sqrt(t) is sufficient. For example, -t ln t<=sqrt(t), -(1-t)ln(1-t)<=t<=sqrt(t), and ln 2>2/3 establish that bound. The more precise constants are irrelevant to termination.

Enumerate every nonzero Gaussian-integer vector whose 2D real coordinates lie in [-K,K]. There are exactly

    G=(2K+1)^(2D)-1                                    (6)

candidates. For each candidate, compute (3) with each entropy interval of width at most n eta/8. Let l_v,u_v be the resulting coherent-information bounds. Then

    L=max{0,max_v l_v/n},
    U=min{L_a,max_v u_v/n+eta/2}

contain f_n. Their width is at most 3eta/4. This proves Proposition 1.

The code in finite_block.py implements the rational entropy intervals, rational-complex channel action, tensor products, grid plan, and exhaustive finite-block procedure. The exhaustive covering is deliberately not executed in the default checks.

### 1.4 Costs actually charged

The dense Choi matrix for N^n has (ab)^(2n) rational-complex entries. An entry is obtained from n input entries, so its individual bit length is bounded effectively in n and the input bit length, with index normalization included.

Each candidate requires density matrices of dimensions b^n and (ab)^n. The entropy series needs at most

    m_X=ceil(64 dim(X)/(n eta))

matrix multiplications under the above precision choice. A naive dense multiplication uses O(dim(X)^3) rational scalar operations. Common denominators bound all intermediate bit lengths effectively; the extra sum over 1/k can, for example, be placed over m!, of bit length O(m log m). No unit-cost assumption about arbitrarily large rationals is required.

The dominant enumeration count is (6), not polynomial time. Even for a=b=2,n=1,eta=1/4, (4) gives t=1/9216, K=73728 and G=147457^8-1, which lies between 2^136 and 2^144. Running nine small candidate checks is not execution of that optimizer.

**Corollary.** Q is uniformly lower semicomputable on the promised input class. At stage s, compute intervals for f_1,...,f_s to width 2^-s and take the running maximum of all lower endpoints and zero. This is a monotone rational sequence converging to Q. Every stage terminates; a stage certified to be within 1/4 of Q has not been identified.

## 2. The exact operation an evaluator would supply

**Proposition 2.** The following statements are equivalent for the stated varying-dimensional explicit rational input class.

1. A total rational 1/4-bit evaluator for Q exists.
2. A total arbitrary-precision rational evaluator for Q exists.
3. There is a total computable b(J,epsilon) such that

       Q(N)-f_{b(J,epsilon)}(N) < epsilon.

4. There is a total computable B(L,epsilon), depending only on the input description length L and epsilon, such that every valid J of length <=L satisfies

       0 <= Q(N)-f_m(N) <= epsilon     for every m>=B(L,epsilon).

**Proof.** The tensor-power identity gives

    Q(N^k)=k Q(N).

It follows directly from the regularized formula, by restricting Fekete's limit to multiples of k; it does not assert additivity for different channels. Applying the 1/4 evaluator to the fully expanded rational matrix of N^k, then dividing by k, gives error <=1/(4k). This proves 1=>2. The expanded input has (ab)^(2k) entries; that acquisition/description cost is part of this reduction.

For 2=>3, compute q with |q-Q|<=epsilon/4. Sequentially compute certified lower bounds l_n for f_n to precision epsilon/8, and stop at an n with

    l_n > q-epsilon/2.                                 (7)

Such an n exists because the right side is at most Q-epsilon/4 and sup_n f_n=Q. At the returned n,

    Q-f_n < Q-q+epsilon/2 <= 3epsilon/4.

Thus the search terminates if the evaluator is supplied.

For a full tail modulus, first acquire a block b with f_b>=Q-epsilon/2. Write m=kb+r,0<=r<b. Superadditivity and a_r>=0 give

    f_m >= kb f_b/m,
    Q-f_m <= b log_2 a/m+epsilon/2.

Therefore every

    m >= max{b,ceil(2b L_a/epsilon)}                    (8)

has error <=epsilon. Rational Choi validity is decidable by exact finite linear algebra: the trace constraints are rational equalities, and PSD can be decided by principal minors or exact elimination. There are finitely many descriptions of length <=L. Enumerate the valid ones and run the just-constructed total modulus procedure on all of them. Their maximum is a computable B(L,epsilon). Invalid inputs need not be sent to an algorithm whose promise excludes them. This proves 3=>4 with no uniform running-time estimate assumed.

Finally, 4 or 3 together with Proposition 1 approximates Q: choose epsilon=1/8, compute the indicated finite-block value to error <=1/8, and obtain a rational 1/4 approximation. Thus 4=>1 and 3=>1. QED.

This is an equivalence, not a construction of b or B. It sharpens the missing operation: a total evaluator would supply a computable sufficient finite block, even if its own implementation never uses coherent-information block enumeration. Conversely, proving only that one natural cutoff proposal fails would not disprove the evaluator.

## 3. Why continuity and compactness did not complete that operation

For fixed a,b, the set of channels is compact. Each finite-block f_n is continuous, and Q is continuous with an explicit channel-distance modulus. The latter is the established finite-output-dimension continuity theorem of [Leung and Smith](https://arxiv.org/abs/0810.4931).

Thus F_m=max_{n<=m} f_n is an increasing sequence of continuous functions on this compact set with continuous limit Q. Dini's theorem gives a uniform finite m at each fixed accuracy and dimension. It does not supply a procedure computing m from a,b and the accuracy.

There is a precise logical obstruction to making that step on continuity grounds alone. Let M_e be an effective enumeration of machines, indexed by e>=0. Put

    c_e=2^(-e-1),  r_e=2^(-e-3),
    beta_e(x)=max{0,r_e-|x-c_e|},      0<=x<=1.

The supports are disjoint. Define

    g_n(x)=max({0} union {beta_e(x): e<=n and M_e halts within n steps}).

Each g_n is a rational piecewise-linear, effectively computable, 1-Lipschitz function. The sequence increases. Its limit g is also 1-Lipschitz, including at the accumulation point zero. But

    g(c_e)=r_e if M_e halts, and zero otherwise.

An arbitrary-precision evaluator for g would decide halting by evaluating at c_e to error r_e/4. Nevertheless Dini's theorem applies and gives uniform convergence nonconstructively. One can even use the single fixed rational point construction g_n(x)=Omega_n x(1-x), where Omega_n increases effectively to a noncomputable left-c.e. real: a known common Lipschitz modulus for the approximants and limit still does not yield a convergence modulus.

This example is not a quantum-capacity noncomputability proof. It establishes exactly which information the compactness argument fails to provide. It does not exclude additional quantum-channel structure from providing it.

## 4. The strong-converse bridge, tested without a hidden stopping rule

The primary 2026 source [Beigi and Tomamichel](https://arxiv.org/html/2609.11771v1) states exponential fidelity decay above ordinary Q. Its Section 5 uses the weak converse and a code-conversion argument. The capacity is the rate threshold appearing in that conclusion; the theorem does not offer a finite test certifying that a proposed rate is above Q.

The following countermodel makes this distinction exact, while retaining concatenation-like supermultiplicativity. For the above g_n, set

    A_n(x)=n g_n(x),
    F_n(x,R)=2^(-n max{0,R-g_n(x)}).

Since g_n increases,

    A_{n+m} >= A_n+A_m,
    F_{n+m}(x,R) >= F_n(x,R) F_m(x,R).                  (9)

If R<g(x), F_n(x,R)=1 for all sufficiently large n. If R>g(x), then for every n,

    F_n(x,R) <= 2^(-n(R-g(x))).                         (10)

Thus this effectively specified model has a perfectly sharp operational threshold g, a known exponent depending only on the gap, no unknown onset in its strong converse, uniformly continuous finite-block rates and limit, and the concatenation inequality (9). Its capacity remains noncomputable. Scaling A_n and g by an integer k also provides the exact analogue of tensor amplification. Taking k_e=1/r_e converts the zero-versus-r_e halting promise to zero versus one, making a fixed 1/4 evaluator impossible in this model.

Again this is not a physical channel construction. It rules out the abstract inference from those properties to an evaluator. The missing ingredient is effective achievability convergence or a separate upper certificate, not a stronger numerical exponent in (10).

## 5. Direct hardness and helper-removal routes considered

I read the quantified N675 entropy-defect statement and its computable margin. It concerns the unrestricted finite untouched reference and generic variable-dimensional rational POVMs. Its accepted status is retained. Its channel-order or assisted-capacity consequence is not an ordinary-capacity rate gap by itself.

I also read the supplied available N1677/N1680 visible originals, preserving their ordinary/assisted distinction and their unavailable-package hold. I did not attempt to retrieve their held packages or reprove the accepted N675 theorem.

The route considered was to encode the unknown reference as a long stationary input memory, paying its startup only once. It still needs an ordinary entropy-rate inequality after replacing the untouched memory by actual past/future outputs. I found no way to make that replacement lossless. Arbitrarily many repeated marginals with a single quantum memory are not free: noncommuting correlations can fail shareability, while a separable hidden-variable extension can let the histories learn the hidden label and remove an extensive local advantage. These observations do not constitute a general impossibility theorem for stationary encoders.

An attempted source-independent substitute was a fixed low-dimensional zero-capacity helper. [Zhu and Wang, v3](https://arxiv.org/html/2607.24693v3) gives a fixed qutrit activator for every positive-private-capacity partner. Its actual single-excitation construction uses d helper copies to simulate a d-dimensional dephased erasure, with d equal to a sum of ranks of private code states (S6.2-S6.3). Its implication is positive capacity, and its charged finite-block rate can depend on that unknown code dimension. It therefore does not supply a computable ordinary rate from N675's arbitrary-reference margin. I did not assume positive unassisted private capacity for the N675 family.

The regularized-divergence evaluator in [Schmitt and Sutter](https://arxiv.org/html/2609.29885v1) is explicitly for stabilized channel divergences (their Eq. 7). The coherent-information identity uses an unstabilized comparison. Replacing it with full stabilization admits an independent purifying reference and changes the value. This source does not close Proposition 2's missing operation. Its result is credited at its actual scope.

The QMA-hardness result in [Bhattacharyya, Mehta and Zhao, v3](https://arxiv.org/html/2601.22471v3) uses succinct circuits and is compatible with a terminating unbounded-time evaluator; its distinct undecidability theorem uses a restricted zero-error assisted classical resource. I did not turn either into an ordinary noncomputability claim.

## 6. Executed evidence and present outcome

`python3 finite_block.py > checks.json` completed successfully using the existing Python standard library. Nine physical candidate evaluations have exact rational intervals containing the analytic value: the identity, dephasing, half-erasure and complete-erasure channels on a qubit with maximally mixed and pure inputs, plus an identity-channel purification with an imaginary coordinate. Complements enter through (3), rather than a separately selected environment. There were also 3,136 finite countermodel inequality checks; their general validity rests on the algebraic proof (9)-(10), not those fixtures.

The fully exhaustive finite-block optimizer was not run: its explicit one-block qubit grid already has more than 2^136 candidates. No large unknown strategy, quantum helper, physical experiment, package installation, service, billing or external contact was acquired or used.

The construction gives a complete computable lower sequence and an exact equivalence between the desired evaluator and a computable sufficient block bound. The continuity and strong-converse routes do not supply that bound. The direct reduction route did not construct a fixed ordinary rate gap. Thus the full required boundary is still UNRESOLVED in this attempt; no global hardness or total evaluator is claimed.

Context: I read the common brief, workspace operating instructions, relevant memory registry entries, governing N675 passages and the two allowed predecessor visible responses. I deliberately accessed no other pilot constructor's or the lead's developing scientific output. Public primary-source discovery was available, and memory exposure was present, so this was not a blind construction. Files written were restricted to r3.
