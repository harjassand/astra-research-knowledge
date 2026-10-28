# A constant-signal physical quadratic episode-length boundary

28 October 2026. **New candidate theorem; independent receiving pending.** Root proposed the unitary-orbit/reset mechanism; this construction strengthens it with a standard Singer difference set and a positive/negative-part initial-state choice. The earlier general-d tiny-signal construction is preserved as `PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH_tiny_signal_initial.md`; its weaker signal caveat is not silently removed. This note is separate from the received rank/core-free short-word modulus theorem. No novelty or total learning-resource advantage is claimed.

## 1. Main statement and sharp interface

For every prime power q, let

    d=q+1,          r=q²+q+1=d(d-1)+1.                    (1)

There are two stationary dimension-d physical HQMMs, differing only in their initial densities, with exactly two common native actions:

1. one **forward** unitary channel, or an explicitly specified weakly depolarizing forward channel;
2. one fixed binary test followed by reset to a common state.

All action/outcome words of total native length at most `r-1` have identical probabilities, including every classical feedback protocol bounded by that length. A word of length r has binary-law TV at least

    3/64      for the unitary action,
    3/128     for the weakly depolarizing action.           (2)

Initial states are at least `I/(2d)`. Both test/reset branches have Choi eigenvalues at least `1/(4d)`. In the depolarizing variant, the forward action also has full Choi floor `1/(2rd)`: **every declared native branch is strictly CP-interior**, with the dimension-dependent margin fully stated.

The library does NOT supply a free inverse, arbitrary hidden-memory gates, coherent control of the actions, a noise flag, or arbitrary hidden-memory measurements. Powers of the forward action cost their actual number of native calls. Knowing a matrix description is not permission to implement its inverse on inaccessible memory. With a free inverse the example can be distinguished quickly; that is a different interface.

Any number of independently reset training episodes, each restricted to at most `r-1` native calls, remains exactly indistinguishable in the two worlds. Thus they cannot uniformly predict the specified r-call binary law with TV error below `3/256` in the depolarizing variant (or below `3/128` in the unitary variant). The statement concerns the necessary **maximum episode length**, not a number-of-shots lower bound or a computational advantage. It applies even if the learner is given both candidate models and only needs to identify the world.

## 2. A standard, constructible perfect cyclic difference set

There exists a set `D={e_0,...,e_(d-1)}` of d residues modulo r whose ordered nonzero differences enumerate every nonzero residue exactly once:

    {e_i-e_j mod r:i!=j} = {1,...,r-1}, with multiplicity1. (3)

This is the standard Singer perfect-difference-set construction, not a new combinatorial claim. A finite-field construction and short proof make the acquisition boundary explicit.

Take the field `F_(q³)`, its subfield `F_q`, and a generator g of the multiplicative group. The quotient `F_(q³)^*/F_q^*` is cyclic of order r. Let D be the exponents modulo r for which

    Tr_(F_(q³)/F_q)(g^e)=0.                               (4)

The trace-zero hyperplane has `q²-1` nonzero vectors, hence `(q²-1)/(q-1)=q+1=d` projective points. For a nonidentity quotient element u, the two linear functionals `Tr(x)` and `Tr(ux)` are independent: a dependence would contradict nondegeneracy of the trace pairing unless u were in `F_q`. Their kernels intersect in one one-dimensional `F_q` subspace, hence exactly one projective point. This is precisely the unique ordered-difference property (3). The trace pairing is nondegenerate because the trace map of this finite separable extension is nonzero, and multiplication by a nonzero field element is bijective.

One may construct the fields by irreducible polynomials, find a primitive element by exact finite search, and enumerate (4). These finite algebraic costs are real and paid. For orientation, the trace construction is documented in [Herron, Section 1.4 and Proposition 2.1](https://arxiv.org/pdf/2502.09536), crediting [Singer's 1938 theorem](https://doi.org/10.1090/S0002-9947-1938-1501951-4). The proof here states exactly the property used; no unidentified signed-automaton witness is imported.

Set

    zeta=exp(2 pi i/r),      u_i=zeta^(e_i),
    U=diag(u_i).                                           (5)

All entries are algebraic. By (3), the adjoint modes `u_i conjugate(u_j)`, `i!=j`, together with 1 are **all r-th roots of unity**, once each.

## 3. Interior effect and a bounded trace-norm delayed witness

Let

    b_j=2j-d+1,       S=sum_j b_j²=d(d²-1)/3,
    B_jj=b_j,        B_ij=1 for i!=j,
    epsilon=1/(8d),  E=I/2+epsilon B,
    Delta=[u u†-I+diag(b_j/S)]/(r epsilon).              (6)

B is real symmetric and traceless, with each row absolute sum at most `2(d-1)`. Therefore

    I/4 <= E <= 3I/4.                                     (7)

Delta is Hermitian and traceless. Its diagonal is `b_j/(r epsilon S)` and its off-diagonal entry is `u_i conjugate(u_j)/(r epsilon)`. Consequently

    Tr[E U^k Delta U^(-k)]
       =(1/r)[1+sum_(i!=j)(u_i conjugate(u_j))^(k+1)]
       =(1/r)sum_(ell=0)^(r-1) zeta^(ell(k+1))
       =0,       k=0,...,r-2,
        1,       k=r-1.                                  (8)

These are exact finite-root sums. No nearly singular Vandermonde inversion is needed in this family.

Write `T=||Delta||_1`. Because `|b_j|/S<1`, the diagonal matrix `-I+diag(b_j/S)` is negative definite and has trace norm d. Also `||u u†||_1=d`. The triangle inequality gives

    0<T <= 2d/(r epsilon)=16d²/r.                        (9)

Let `Delta_+` and `Delta_-` be its positive and negative parts. They are PSD and each has trace `T/2`, since Delta is traceless. Define the two initial densities

    tau=I/d,
    rho_+=tau/2+Delta_+/T,
    rho_-=tau/2+Delta_-/T.                              (10)

Both have trace one and are at least `I/(2d)`. Their difference is `Delta/T`. Their algebraic spectral descriptions are finite; an actual preparation/compiler would have to pay the corresponding precision and gate costs. For the lower bound only their physical existence is used.

The essential improvement over the earlier tiny-signal construction is (9)-(10): using a trace-norm positive/negative decomposition, rather than centering a Frobenius-normalized witness symmetrically around `I/d`, preserves a constant late signal. Indeed

    1/T >= r/(16d²) >= 3/64,       d>=2.                 (11)

## 4. Common complete physical actions

The unitary variant uses a one-outcome native action

    a: Phi_a(X)=UXU†.

The strictly-interior variant instead uses the one-outcome channel

    a: Psi_a(X)=(1-beta)UXU†+beta Tr(X)tau,
    beta=1/(2r).                                         (12)

No classical record reveals which part of the mixture occurred. Its unnormalized Choi matrix is

    (1-beta)|U>><<U| + (beta/d) I_(d²),

so its Choi floor is `beta/d=1/(2rd)` and the channel is exactly TP.

Both variants use the same fixed binary action

    b,1: Phi_(b,1)(X)=Tr(EX)tau,
    b,0: Phi_(b,0)(X)=Tr((I-E)X)tau.                    (13)

Their Choi matrices are `E^T tensor tau` and `(I-E)^T tensor tau`; (7) proves the floor `1/(4d)`, and their sum is TP. Thus all states and instruments are actual full-algebra quantum objects. Both worlds differ only in (10).

On traceless Delta, (12) obeys

    Psi_a^k(Delta)=(1-beta)^k U^k Delta U^(-k),            (14)

because tau is invariant under U. Thus depolarization preserves every exact zero in (8).

## 5. Full short-word and adaptive-episode indistinguishability

A word containing only a has probability one in both worlds. If its first b occurs after k forward calls, the difference of its first outcome-1 probabilities is

    [Tr(E Phi_a^k Delta)]/T

in the unitary variant, or `(1-beta)^k` times that expression in the depolarizing variant. It vanishes exactly for `k<=r-2`. Outcome0 has the opposite difference and is also equal.

After that first b, **both outcomes and both worlds have the identical normalized state tau**. Every later forward channel leaves tau invariant, and all later test branches have identical conditional laws and reset again. Hence matching the first test proves equality of the complete word, not just its final marginal. Every word of total length at most `r-1` tests first after at most `r-2` forward calls, establishing the claim for all such words.

This argument also covers arbitrary bounded-length classical feedback episodes: before the first test the forward outcomes are deterministic, and private random choices cannot depend on the hidden world; at the first test the outcome laws agree; afterward the physical states are identical. Stopping, retaining the whole classical record and randomizing the episode policy do not change this conclusion.

For independently reset acquisition episodes, condition on the entire previous training record. The next chosen short episode again has the same conditional law in both worlds. Induction gives equality of the whole training record law, even for adaptive selection of episodes and any finite number of reset attempts. There is no hidden postselection advantage: every selected short record event has the same probability in both worlds. The statement does not cover extra coherent/quantum access beyond this declared classical native library.

## 6. First signal, constant-error consequence and dimension order

The word `a^(r-1) b` has length r. Its binary-law TV is exactly

    v_d=1/T                                      (unitary),
    v_d=(1-1/(2r))^(r-1)/T                       (interior). (15)

Bernoulli's inequality gives `(1-1/(2r))^(r-1)>1/2`; using (11), the interior signal is at least `3/128`, while the unitary signal is at least `3/64`. These are honest dimension-uniform positive constants on the prime-power sequence. The forward Choi margin in (12) shrinks as `Theta(d^-3)`; no dimension-independent mixing margin is being granted.

An estimator based only on shorter reset episodes has the same output distribution in both worlds. By the triangle inequality, at least one world has expected TV prediction error at least `v_d/2` for the specified r-call binary law. For a deterministic guaranteed-error output, simultaneous error below `v_d/2` in both worlds is impossible. This is the stated constant-error episode-length obstruction, not a lower bound against longer calls, richer controls or arbitrary coherent testers.

A fixed pre-call abort clock changes this comparison: the particular distinguishing word survives with probability `gamma^r`, so its full clocked-record TV is `gamma^r v_d`, not `v_d`. There is no dimension-uniform constant-risk lower bound for a fixed positive abort probability inferred here. A clock of order `1/r` can retain constant survival but pays expected duration of order r. Likewise a learner allowed occasional longer episodes is not covered by the strict maximum-length premise.

For any supplied dimension bound `D_max>=3`, choose a power of two `q<=D_max-1` maximal and take actual dimension `d=q+1<=D_max`. Then `q>(D_max-1)/2` and `r=q²+q+1` is of order `D_max²`. The source already lies in the promised dimension class; no padding argument or uncharged extra state is needed. Thus the worst-case quadratic native experiment-length order holds for all large supplied dimension bounds, not only a sparse sequence of exact dimensions.

## 7. Comparison and verification status

The `O(d²)` exact short-word upper is established prior quantum-automata linear algebra. [Li–Qiu, Theorem 5](https://arxiv.org/pdf/quant-ph/0604085) gives `n_1²+n_2²-1` for quantum sequential machines; the received short-word modulus theorem combines that conventional finite-dimensional principle with a paid semialgebraic stability procedure. Singer difference sets and their Fourier cancellation are also established mathematics. This note makes a concrete physical, full-record, constant-signal resource boundary in the declared forward/test-reset interface; it does not claim priority or a new universal quantum-automata theorem without further literature review.

The earlier all-d power-of-two phase construction supplied only a possibly tiny late signal. It remains valid but is strictly weaker for constant-error claims; it is retained as explicit history. The new construction pays a different arithmetic choice and initial-state preparation, and proves its signal rather than presuming it.

`physical_quadratic_length_exact_check.py/.json` constructs finite fields and verifies difference sets, exact cyclotomic root-sum moments, trace-norm/PSD bounds, and the fixed CP instruments. Approximate numerical state displays are distinguished from exact algebraic certificates. There are no source calls, episode samples, RNG calls or physical executions. Independent review is pending; the separate received modulus receipt does not receive this lower-bound construction automatically.
