# Continuation: coherent expander records and the remaining capacity operation

The whole common question remains unresolved. I did not construct a total ordinary-capacity evaluator or a computable-gap ordinary-channel halting reduction in this continuation. The initial rational finite-block evaluator and cutoff-equivalence proof remain intact.

I read the lead's exact `ENVIRONMENT_ENTROPY_EXCESS_OBSTRUCTION.md` at this natural completed boundary. No other constructor's developing output was read. The transfer changed the test I applied to a mixer route: a positive asymptotic rate may coexist with an unknown finite boundary scale, so an effective boundary estimate must not be silently imported. The argument below constructs an actual stationary ordinary-input family that makes this distinction explicit, including the entire coherent eight-dimensional mixer record.

## 1. An exact fixed-alphabet counterexample to a uniform mixer/history cutoff

**Statement.** There is one fixed rational eight-dimensional full-erasure channel N and a family of finite stationary ordinary input processes with the following properties.

- The retained input memory is maximally mixed and is updated by a degree-eight quantum expander with a dimension-independent Hilbert--Schmidt contraction at most 5 sqrt(2)/8<9/10.
- The entire coherent Kraus register of that expander is emitted as the physical channel input. It reaches N's true environment intact.
- For each fixed memory dimension D, the environment entropy rate is zero and its entropy excess is at most 2 log_2 D.
- For every blocklength n there is a computably selectable finite D and one of these stationary processes for which

\[
e_E(n)\ge 2n\log_2(10/9)-1.
\tag{1}
\]

Thus even with a fixed physical alphabet, a fixed eight-unitary degree, tracial stationarity, and a fixed strict memory contraction, there is no sublinear environment-excess envelope uniform over the unknown memory dimension. This is a theorem about a proposed history estimate. The fixed channel N has Q=0 and is itself easily computable; (1) is not a quantum-capacity noncomputability theorem.

### The actual process

For each odd D>=3, take the Gross--Eisert quantum Margulis channel

\[
\Phi_D(X)=\frac18\sum_{j=1}^8 U_j XU_j^*,
\quad \|\Phi_D(X)\|_2\le\lambda\|X\|_2
\quad (\operatorname{Tr}X=0),
\]

with lambda=5 sqrt(2)/8. The original construction supplies eight explicit unitaries and their inverses in every odd dimension. Their entries are algebraic roots of unity and discrete Fourier entries. Only this original expander theorem is imported; the entropy argument below is separate.

Use the isometry

\[
V_D:M\longrightarrow F\otimes M,
\qquad V_D=\frac1{\sqrt8}\sum_{j=1}^8|j\rangle_F\otimes U_j,
\tag{2}
\]

and initialize M in I_D/D. Repeated applications of (2), retaining M and emitting F, give consistent stationary states rho_(F^n). Stationarity follows from Phi_D(I_D/D)=I_D/D. Every physical input has dimension eight. There is no discarded mixer label in this construction.

The fixed channel N:A=C^8->B=C is

\[
N(X)=\operatorname{Tr}(X)|0\rangle\langle0|,
\qquad N^c(X)=X.
\]

Its actual isometry sends |j>_A to |0>_B|j>_E. Its normalized Choi matrix is I_8/8 (with a one-dimensional output), so the physical channel has a finite rational description independent of D. The actual environment state is rho_(F^n).

### Its entropy rate and finite-block entropy

Purify the initial memory by R=C^D. After n uses of (2), the state on R F^n M is pure and its RM marginal is

\[
\tau_n=(\operatorname{id}_R\otimes\Phi_D^n)(\Phi_D^{\rm Bell}).
\tag{3}
\]

Consequently

\[
S(F^n)=S(\tau_n)\le 2\log_2D.
\tag{4}
\]

For each fixed D this proves h_E=0, and hence e_E(n)=S(F^n). The degree-eight record has been retained coherently, not measured and replaced by a classical trajectory.

Choose a Hilbert--Schmidt orthonormal Hermitian operator basis {G_alpha} on M, with G_0=I/sqrt(D) and all other elements traceless. Expanding the Bell state gives

\[
\operatorname{Tr}(\tau_n^2)
=\frac1{D^2}\sum_\alpha\|\Phi_D^n(G_\alpha)\|_2^2
\le\frac1{D^2}+
\left(1-\frac1{D^2}\right)\lambda^{2n}.
\tag{5}
\]

The equality uses orthogonality of the first tensor factors; the bound uses unitality on G_0 and the contracted traceless sector. Von Neumann entropy is at least order-two Renyi entropy, so

\[
S(F^n)\ge-
\log_2\left[D^{-2}+(1-D^{-2})\lambda^{2n}\right].
\tag{6}
\]

For a given n, choose the least odd D>=max{3,(10/9)^n}. This is a finite integer computable by rational arithmetic. Since lambda<9/10, the bracket in (6) is at most 2(9/10)^(2n), proving (1). The coefficient is

\[
2\log_2(10/9)=0.3040061868\ldots.
\]

In particular, for any proposed envelope b(n) with b(n)/n->0, some large n and the explicitly selectable D above violate e_E(n)<=b(n). No computability assumption on b is needed for this failure of uniformity.

The same construction also has exponential decay of fixed local correlations. For a Hermitian one-site observable O with norm at most one, its transfer insertion sends the stationary density matrix into the order interval [-I/D,I/D], and the adjoint insertion sends I into [-I,I]. Their centered Hilbert--Schmidt norms are at most 2/sqrt(D) and 2 sqrt(D), respectively. The intervening traceless transfer contracts by lambda per step. Thus two centered one-site observables at separation t have covariance magnitude at most 4 lambda^(t-1), independently of D. Even this finite-observable statement does not restore a uniform entropy-history estimate.

### What this supplies and what it does not

This matches the lead's distinction at the level of an actual coherent encoder, rather than only a logical hard-family obstruction. For each D, the boundary scale is finite and its dependence on D is known. If D were given, it would not be mysterious or noncomputable. What fails is removing D from a uniform estimate while retaining only the fixed degree, fixed physical dimension and fixed spectral gap.

The entire example has zero bulk input entropy rate. More generally, a deterministic finite-memory isometric emitter has S(input block)<=2 log D, and |I_c(input block,N^n)|<=S(input block). It therefore cannot, on its own, yield the positive capacity gap needed for the common question. Fresh control randomness and an actual receiver/environment rate asymmetry would still have to be constructed. The example does not provide that asymmetry, and the unknown history remainder in the supplied N1680 source is not given a favorable sign by (5).

An attempted full negative proof could validly keep a finite D-dependent boundary while proving a positive bulk rate. The theorem above neither excludes such a proof nor supplies its missing positive rate.

## 2. A new primary evaluator result was checked with its exact stabilization

I examined Schmitt--Sutter, *The regularized channel Renyi divergence is continuous*, arXiv:2609.29885v1, especially their definition (7) and Corollary 4.1. The corollary gives a terminating evaluator for the **stabilized** regularized channel relative entropy by combining finite lower witnesses with computable upper bounds at Renyi orders above one. This is stronger than invoking a strong converse alone: the computable upper sequence is an additional operation.

It does not directly evaluate the ordinary-capacity representation

\[
Q(N)=\underline D^{\rm reg}
(\operatorname{id}_R\otimes N\;\|\;
\mathcal R_R^{I}\otimes N),
\qquad \dim R=a=\dim A,
\]

because that identity uses **unstabilized** divergence. In fact the stabilization discrepancy can be calculated exactly at every order, rather than left as a possible technical gap.

Let E=id_R tensor N and F=R_R^I tensor N, and permit an external untouched stabilizing register Z. On an input omega_(ZRA), their outputs are

\[
\tau_{ZRB},\qquad I_R\otimes\tau_{ZB}.
\]

Every state tau_(RC) with dim R=a obeys

\[
\tau_{RC}\preceq a I_R\otimes\tau_C.
\tag{7}
\]

For pure states (7) follows from Cauchy--Schwarz in a Schmidt decomposition with at most a terms. Convex combination proves it for mixed states. Hence max-relative entropy, and every sandwiched Renyi divergence of order alpha>=1, is at most log_2 a on the displayed channel pair.

Take an independent Bell state on RZ and an arbitrary state on A. This attains log_2 a, regardless of N. It follows that

\[
D_\alpha(E\|F)=\log_2 a,
\qquad D_\alpha^{\rm reg}(E\|F)=\log_2 a
\quad(\alpha\ge1).
\tag{8}
\]

With a normalized maximally mixed replacer, the value is 2 log_2 a, and subtracting the normalization shift recovers (8). One can therefore apply the new stabilized-divergence algorithm, pay its exact input and precision costs, and still obtain a quantity independent of the original channel. An identity channel and a full-erasure channel of the same input dimension have different Q and the same values in (8).

This rules out that particular substitution. It does not exclude adapting the upper-bound machinery to the required unstabilized quantity. I did not construct such an adaptation; doing so would be a substantive solution, not an already supplied theorem.

## 3. Fixed helper activation was checked without discarding its dimension cost

Public discovery also found the October v3 of Zhu--Wang, *Quantum incapacity from observable shadows*, arXiv:2607.24693v3. Its stated universal fixed-qutrit activation theorem initially looked relevant: P(M)>0 implies Q(M tensor Lambda)>0.

The governing construction uses a d-dimensional single-excitation code over **d calls** of the qutrit helper, obtains a dephased erasure with q=eta=1/4, and combines it with some finite private-code block. Their Section 5 explicitly retains the potentially large block and auxiliary dimension. This supplies positivity, not a computable uniform ordinary-rate margin for the accepted N675 hard family. I found no justified way to remove that denominator. The source was read as a primary construction; a newer abstract's use of “every” was not treated as a quantitative rate theorem.

The older Wu--Wang private-channel amplification source, arXiv:2510.04527v2, was also inspected. Its helper bounds depend on shield dimensions and parameters; its separate claimed private/quantum separation invokes the spin-alignment conjecture. None of those conditions was imported into the common question.

## 4. Execution and actual resources

`quantum_expander_history.py` constructs the eight Margulis unitaries using already installed NumPy 2.5.3. No package was installed. Its D=3,5,7 checks used floating-point arithmetic to inspect unitarity, the retained-memory contraction, Choi-power purity, and equality of emitted-record and two-boundary entropies. The run completed in about 0.37 seconds of tool wall time. The largest tested emitted record had dimension 64; the largest two-boundary matrix had dimension 49. The observed contraction values were approximately 0.576, 0.666 and 0.722, below the imported bound 0.884. These are convention checks; (4)--(6) and the original expander theorem prove the general statement.

An earlier classical expander/color-record prototype is retained in `expander_history.py` and `expander_fixture_results.txt`. Its small exhaustive fixture inspected 512 colorings and 512 label words and completed in about 1.05 seconds. It is not needed for the sharper coherent-record proof above and is not claimed as the common-question solution.

For a general memory D, (2) needs a local D-dimensional memory, its explicit eight algebraic unitaries, one initial tracial state, and an eight-dimensional emitted register per step. Dense generation of one n-block state costs exponentially in n through its 8^n physical dimension; the smaller two-boundary formula (3) has dimension D^2 and can be evaluated by n applications of the explicit map on D^2 operator basis elements. The selected D in (1) grows at least as (10/9)^n. These source-generation costs are real; they are not a channel-input description cost for the fixed erasure channel and are not supplied to a capacity evaluator as free data.

No large-D family, encoded Turing-machine channel, ordinary positive rate gap, or total capacity upper evaluator was executed. No goal, automation, subagent, service, physical experiment, shared-file edit or source-transfer bypass was performed. The original held PDF/ZIP packages remain unavailable and unused.

Primary governing passages:

- Gross--Eisert, [arXiv:0710.0651v2](https://arxiv.org/pdf/0710.0651), Section 1.2, Observation 1 and the explicit implementation in Section 3: the degree-eight Margulis expander and its dimension-independent contraction.
- Schmitt--Sutter, [arXiv:2609.29885v1](https://arxiv.org/html/2609.29885v1), definition (7), Corollary 4.1 and its proof: stabilized divergence and the extra computable upper sequence.
- Zhu--Mao--Fang--Wang, [arXiv:2509.15106v2](https://arxiv.org/html/2509.15106), Section 4.5, equations (137)--(142): the ordinary-capacity identity is unstabilized.
- Zhu--Wang, [arXiv:2607.24693v3](https://arxiv.org/html/2607.24693v3), Section 4, equation (13), and Section 5: single-excitation helper dimension/call cost and existential activation scope.
- Wu--Wang, [arXiv:2510.04527v2](https://arxiv.org/html/2510.04527): dimension-dependent privacy amplification and the separately stated spin-alignment assumption.

The lead's transferred environment-excess argument is used as a method constraint at its stated conditional scope. The accepted N675 theorem and completed predecessors are not re-audited or weakened. The final missing operations remain those in the initial construction: a recursive ordinary-channel cutoff for a positive solution, or a physically constructed ordinary rate gap for a negative solution. The bounded second turn did not resolve them.
