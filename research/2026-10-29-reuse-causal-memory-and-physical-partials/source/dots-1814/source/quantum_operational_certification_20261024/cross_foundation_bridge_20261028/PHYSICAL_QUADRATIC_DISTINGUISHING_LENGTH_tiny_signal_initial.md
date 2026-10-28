# Physical quadratic exact distinguishing length

28 October 2026. **New candidate construction; independent receiving pending.** Root proposed the unitary-orbit/reset mechanism; this note supplies an explicit algebraic family and its complete-word proof. It is separate from the rank/core-free modulus source. No novelty, constant-signal lower bound, sample-complexity advantage or experimental acquisition is claimed.

## Claim and interface

For every `d>=2`, there are two stationary dimension-d physical HQMMs with the **same two native actions**, differing only in their initial density matrices, such that all classical action/outcome words of total length at most

    r-1=d(d-1)

have exactly the same probabilities, while a word of length

    r=d(d-1)+1                                             (1)

distinguishes them. The actions are one deterministic unitary channel and one binary measure-and-reset instrument. Initial states and both test/reset Choi matrices are strictly positive; the unitary branch lies on the CP boundary.

This establishes an `Omega(d²)` worst-case exact experiment-length requirement within the same classical native-word interface as the `O(d²)` short-word theorem. It does not establish a dimension-uniform constant distinguishing advantage. The first nonzero signal can be extremely small and is quantified below.

## 1. Distinct phase-difference modes

Let

    q=2^(d+1),    zeta=exp(2 pi i/q),
    e_j=2^j, j=0,...,d-1,
    U=diag(zeta^(e_j)).                                   (2)

The ordered nonzero differences `e_i-e_j` are all distinct as integers. Indeed, for a positive difference `2^i-2^j=2^j(2^(i-j)-1)`, its 2-adic valuation determines j and its odd part determines i. Their absolute values are less than `2^(d-1)`; the chosen q prevents modular collisions, including between positive and negative differences.

Consequently the set

    Lambda={1} union {lambda_ij=zeta^(e_i-e_j):i!=j}

contains exactly `r=d(d-1)+1` distinct algebraic numbers, closed under complex conjugation. Define

    P(t)=product_(lambda in Lambda)(t-lambda),
    a_lambda=1/P'(lambda).                                (3)

Lagrange interpolation, by comparing the coefficient of `t^(r-1)`, gives

    sum_lambda a_lambda lambda^k = 0,   0<=k<=r-2,
                                  1,   k=r-1.             (4)

P has real coefficients, so `a_conj(lambda)=conj(a_lambda)` and `a_1` is real. Every weight is nonzero.

## 2. An interior effect and a physical traceless witness

Let B be the real symmetric matrix

    B_jj=2j-d+1,      B_ij=1 for i!=j,
    epsilon=1/(8d),  E=I/2+epsilon B.                    (5)

B has trace zero and row absolute sums at most `2(d-1)`. Gershgorin therefore gives

    I/4 <= E <= 3I/4.                                    (6)

Let `b_j=B_jj`, `S=sum_j b_j²>0`. Define a Hermitian matrix Delta by

    Delta_ij=a_(lambda_ij)/epsilon,       i!=j,
    Delta_jj=a_1 b_j/(epsilon S).                        (7)

Its off-diagonals are conjugate paired; its diagonal is real and sums to zero. Thus Delta is Hermitian and traceless. Moreover the diagonal contribution to `Tr(E Delta)` is `a_1`, and each off-diagonal mode contributes its prescribed `a_lambda`. For every integer k>=0,

    Tr[E U^k Delta U^(-k)] = sum_lambda a_lambda lambda^k. (8)

In particular the first `r-1` moments vanish and the next is exactly one. Delta is not zero. Put

    R=||Delta||_F,
    rho_+=I/d+Delta/(2d R),
    rho_-=I/d-Delta/(2d R).                              (9)

These have trace one and eigenvalues at least `1/(2d)`, because `||Delta/R||_op<=1`. All parameters are algebraic, including R. This is an explicit existence description, not free finite-precision laboratory access; cyclotomic degree, gate synthesis, matrix-description precision and readout resolution would have to be paid in an implementation.

## 3. Complete physical native actions

Both models have the identical actions

    a:  Phi_a(X)=UXU†,  one deterministic outcome;

    b:  Phi_(b,1)(X)=Tr(EX) tau,
        Phi_(b,0)(X)=Tr((I-E)X) tau,
        tau=I/d.                                         (10)

The b branch Choi matrices are `E^T tensor tau` and `(I-E)^T tensor tau`. By (6), each is at least `I/(4d)`, and their sum is TP. The a branch is a unitary CP/TP channel of Choi rank one. These are genuine instruments on the full algebra, not signed weighted-automaton transition matrices. The initial state is the only difference between the two models.

## 4. Every shorter action/outcome word is identical

A word with no b action has probability one in both models. If its first b occurs after k uses of a, its first-test probability difference is

    Pr_+(1 after a^k)-Pr_-(1 after a^k)
      = Tr[E U^k(rho_+-rho_-)U^(-k)]
      = (1/(dR)) sum_lambda a_lambda lambda^k.             (11)

It is zero for `k<=r-2`. The complementary outcome has the negative difference and is also equal at those times.

After the first test, **both models and both outcomes** have the same normalized state tau. Every later unitary leaves tau invariant; every later test has the same conditional law and resets to tau again. Thus equality of the first-test probability implies equality of the entire word probability, including all later outcomes. Any word of total length at most `r-1` has its first test after at most `r-2` unitary calls, proving exact indistinguishability through that length. Classical feedback and private randomization cannot evade this: condition on the first test and then apply the same-state continuation argument.

The word `a^(r-1) b` has length r, and (4) gives the nonzero final binary-law TV

    signal_d=1/(dR)>0.                                   (12)

For independent whole-process resets, any adaptive acquisition scheme whose **every episode** is restricted to at most `r-1` native calls also has identical entire training transcript laws in the two worlds. Therefore such training cannot uniformly predict the r-call binary law to error smaller than `signal_d/2`. This is a two-point exact-length obstruction with an explicitly dimension-dependent signal, not a constant-error lower bound. Coherent inter-episode references or extra native actions are outside the stated acquisition interface.

## 5. Prior comparison and diagnostic status

Quadratic quantum-state distinguishing-length upper bounds are established prior art. [Li–Qiu, Theorem 5](https://arxiv.org/pdf/quant-ph/0604085) gives `n_1²+n_2²-1` for quantum sequential machines by bilinearization; later quantum finite-state-machine equivalence work studies the corresponding finite-dimensional span methods, for example [Wang et al.](https://www.pure.ed.ac.uk/ws/portalfiles/portal/481368382/WangEtalJCSS2021EquivalenceCheckingOfQuantum.pdf). This construction is a concrete full-CP/state witness showing the order of the length dependence within the present classical-instrument interface. It is not claimed to be a new or sharp leading-constant theorem in that literature.

The Vandermonde weights can be badly conditioned. Their normalization R is part of the statement, and may make (12) very small. The fact that the test Choi matrices and initial states have clean positive margins does not lower-bound the delayed signal by a universal constant. The unitary action remains exactly on the CP boundary; this does not contradict strict-interior predictive contraction conditions.

`physical_quadratic_length_exact_check.py/.json` verifies the cyclotomic moment identities, conjugation, traceless construction and first nonzero distinguishing signal in small dimensions with exact number-field arithmetic. Its PSD margins follow the explicit rational Gershgorin/Frobenius certificates above. No source calls, samples, solver-based acquisition or hardware execution are involved.
