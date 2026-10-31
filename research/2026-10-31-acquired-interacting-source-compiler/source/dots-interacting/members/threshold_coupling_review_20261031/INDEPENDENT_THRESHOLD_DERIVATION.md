# Independent threshold-coupling derivation (local, not a whole compiler)

Reviewed from the root's inline candidate on 2026-10-31. This is a fresh derivation, not a source-bound receipt for the forthcoming authored file.

## 1. Convention and exact finite generator

The configuration is x in {0,1}^n. Write x^i for its i-th flip, and r_i(x)>0 for the rate OUT of x to x^i. Assume a known strictly positive probability pi with pi_x r_i(x)=pi_(x^i) r_i(x^i). Put psi_x=sqrt(pi_x).

For site i, output bit b, and threshold u, define a jump coherently across contexts z:

L_(i,b,u)=sum_z 1_(u<=r_i(z,b)) |z,b> [sqrt(r_i(z,1-b)/r_i(z,b)) <z,1-b| - <z,b|].

Every jump kills psi by detailed balance. Define L_quant(rho)=sum_(i,b) integral D[L_(i,b,u)](rho) du. This is a finite-dimensional Lindbladian: the integrand is constant between the finitely many distinct rates, so the integral is exactly a finite sum of dissipators with each jump multiplied by the square root of its interval length. There is no continuous-environment oracle assumption.

For each i, the integrated C_i=sum_b integral L†L is block diagonal in context. Its bit block has diagonal entries 2r_i(z,0),2r_i(z,1), and off-diagonal entries -2sqrt(r_i(z,0)r_i(z,1)). Consequently the generator has pure stationary state |psi><psi| without an additional Hamiltonian.

## 2. Pair generator, including signs

Write rho_xy=psi_x psi_y f(x,y). Under this similarity the anticommutator contributes the two independent coordinate generators

r_i(x)[f(x^i,y)-f(x,y)] + r_i(y)[f(x,y^i)-f(x,y)].

If x_i=y_i, the gain term adds

min(r_i(x),r_i(y)) [f(x^i,y^i)-f(x^i,y)-f(x,y^i)+f(x,y)].

If x_i differs from y_i, that gain term is zero because different output bits have separate jump labels. Thus the transformed quantum generator is precisely the backward generator of a classical pair coupling: for equal bits, simultaneous flip at the minimum rate and the two nonnegative excess single rates; for different bits, independent flips. The marginals have the original rates. The diagonal x=y is closed after coalescence, NOT pointwise absorbing: the common configuration continues to move.

The threshold overlap is integral 1_(u<=r)1_(u<=s)du=min(r,s), a positive semidefinite Gram kernel. Replacing it by a geometric mean would in general make the excess rates negative.

In particular diagonal matrix elements evolve under the forward original chain by detailed balance. This also gives exact invariance of the adjoint source-diagonal algebra. Tensoring system/reference operator blocks preserves the identity. A source-diagonal system Hamiltonian and prescribed instruments whose adjoints preserve this algebra, with the specified classical restriction, therefore receive the classical controlled process. Arbitrary coherence-sensitive source interventions are not covered.

## 3. Complete operator return from a coupling tail

Let E_t=exp(t L_quant), P=|psi><psi|, Q=I-P. Run the pair coupling from independent pi-distributed endpoints, and let nu_t(x,y) be its law. Its two marginals remain pi, and it is symmetric under endpoint exchange. The pair-generator formula gives

B_t=E_t†(P), (B_t)_(x,y)=nu_t(x,y)/(psi_x psi_y).

This identity must not be justified by pretending an arbitrary transformed density matrix f is pointwise nonnegative. Complete positivity instead gives 0<=B_t<=I. Pure fixedness gives <psi,B_t psi>=1 and therefore (I-B_t)psi=0.

The positive return operator R_t=E_t†(Q)=I-B_t has trace

Tr R_t=sum_x [pi_x-nu_t(x,x)]/pi_x <= Pr_(pi x pi)(X_t != Y_t)/pi_min.

A positive operator has norm at most its trace. Hence, for a uniform coupling-tail bound epsilon(t),

0<=E_t†(Q)<=min(1,epsilon(t)/pi_min) Q.

This is an operator inequality and thus controls arbitrary source states entangled with a reference. An exponential coupling tail yields a return time logarithmic in 1/pi_min, but does not by itself provide an efficient circuit, stationary-state preparation, or centered coupling implementation.

## 4. Local implementation burden

If each rate depends on at most k listed neighboring bits, explicitly sort the at most 2^k context rates separately for each i,b. Consecutive endpoints define at most 2^k threshold intervals. Each resulting jump acts only on the site and its context, and is a diagonal-context-controlled two-dimensional rank-one operator. Its entries are acquired square roots of rate ratios times interval length. For an enabled context, interval length <= r_i(z,b), so its squared local norm is at most r_i(z,b)+r_i(z,1-b), avoiding a spurious inverse-small-rate norm blowup. Arithmetic precision and the supplied rate representation still must be paid.

This gives finitely many explicitly local jumps, with count O(n 2^k) and polynomial cost in the explicit local tables and their bit precision, not a polynomial promise for arbitrary succinct exponentially large rate tables. A complete jump-stack block encoding or full first-event compiler remains a separate receiving obligation.

## 5. Decisive prior comparison

Temme and Wocjan, Quantum 9, 1951 (2025), arXiv:2504.02651v2, is the central primary comparator. Its Eq. (57) supplies the stationary-weighted inverse-map Kraus construction; Lemma 16 supplies coupling-tail/pi_min return; Theorem 20 requires acquired image/preimage, probability, and stationary-ratio computation. The generic reverse-map/return mechanism must be credited to this work. The present explicit threshold Lindbladian is to be assessed as a continuous-time local specialization, not a first coupling-to-qsample method. This comparison does not assert that their efficient-implementation hypotheses follow from forward sampling alone.

Primary full body inspected: https://arxiv.org/html/2504.02651v2

## Verdict

The inline local algebra and operator return claim are sound with the above rate convention and closed-diagonal precision. No whole compiler or new originality claim is accepted by this note. Await the actual authored source for byte-bound review.

## 6. Exact uniformization identification (independent derivation)

The comparison can be strengthened beyond analogous convergence bounds. For each finite threshold interval alpha=(i,b,l), define the deterministic map f_alpha that flips a configuration's bit b to 1-b exactly when its context passes that threshold; it leaves every other configuration unchanged. Let Delta_alpha be the interval length and R=sum_alpha Delta_alpha. Define its weighted inverse-map operator

T_alpha=sum_x sqrt(pi_x/pi_(f_alpha(x))) |x><f_alpha(x)|.

It obeys T_alpha=I+J_alpha, where sqrt(Delta_alpha) J_alpha is exactly the interval jump from Section 1. The classical chain obtained by selecting alpha with probability Delta_alpha/R has transition matrix I+Q_classical/R, and is reversible. The weighted inverse-map channel is Phi=R^-1 sum_alpha Delta_alpha T_alpha (.) T_alpha†, with the denominator here R (not a rate at an individual configuration).

Put S=sum_alpha Delta_alpha J_alpha. Directly, S has diagonal -sum_i r_i(x), and flip entries sqrt(r_i(x)r_i(x^i)), so S=S†. Trace preservation of Phi gives 2S+C=0, C=sum_alpha Delta_alpha J_alpha†J_alpha. Expanding R(Phi-I) consequently gives exactly sum_alpha Delta_alpha D[J_alpha].

Thus the threshold generator is an exact continuous-time uniformization of the existing weighted grand-coupling channel construction, not only a generator with similar estimates. This algebra also identifies why detailed balance eliminates an extra current Hamiltonian. Efficient retained-process high-rate simulation remains separate from constructing this lift, but the lift itself should not be presented as a new mechanism.
