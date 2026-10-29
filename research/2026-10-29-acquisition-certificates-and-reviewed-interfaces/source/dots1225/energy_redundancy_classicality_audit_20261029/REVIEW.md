# Independent mathematical receiving review: energy, broadcast redundancy, and classical reconstruction

2026-10-29. Reviewer: review_finite_quantum_sampler. Verdict: PASS at the stated existence/resource scope. Source originals preserved; their hashes match AUTHOR_FREEZE.json. No historical novelty, optimality, efficient compiler, experimental broadcaster, acquired Stinespring access, or practical advantage is accepted by this receipt.

## Received result and contract
For the family of energy-bounded density operators, a single full-domain normal CPTP binary broadcaster has both marginal errors at most b in half trace norm on that family. Its full-domain nature is essential: the repeated channels are defined off the promised family. A fixed nonnegative Hamiltonian with finite-rank finite-energy projectors and a known zero-energy reset state is assumed. Under these hypotheses, the common finite-outcome entanglement-breaking reconstruction error satisfies

 e <= min(1, ell b + 2[sqrt(E/R)+E/R] + d(R)^2/2^ell).

This is a bound on familywise reconstruction, not a diamond-norm approximation to the identity on all energy-constrained reference-entangled inputs. The de Finetti intermediate approximation is in diamond norm, but the supplied broadcast premise is not.

## Load-bearing proof checks
### 1. Cutoff is trace preserving, not postselection
Let P=P_R, Q=I-P, omega0=|0><0| and p=Tr Qrho. The map C(rho)=P rho P+p omega0 is CPTP and takes values in P. Since H is nonnegative and H>=R Q as a quadratic-form inequality, p<=E/R. Purification followed by projection gives ||rho-P rho P||_1<=2 sqrt(p); adding the positive reset term costs p in trace norm. Hence T(rho,C rho)<=sqrt(p)+p/2<=delta_R. The expression can be capped at one. No normalization by 1-p or measurement of energy within P is performed.

A coherent near-tail example makes a merely linear-in-p replacement invalid: with a low-energy vector orthogonal to the reset vector and a high-energy vector, the pure superposition sqrt(1-p)|low>+sqrt(p)|high> has cutoff distance [p+sqrt(4p-3p^2)]/2, asymptotic to sqrt(p). The submitted square-root term is necessary for this proof route.

### 2. Tree iteration does not require invariant promises
For a leaf sequence S_j=T_(i_j)...T_(i_1), define a_j=T(S_j rho,rho). Contractivity and the broadcast guarantee on the ORIGINAL rho imply

 a_j <= T(T_(i_j) S_(j-1)rho,T_(i_j)rho)+T(T_(i_j)rho,rho) <= a_(j-1)+b.

Thus a_ell<=ell b even when every intermediate state is outside the family or has enormous energy. No bound is invoked on T_i at those intermediate states. The full tree may have arbitrary output correlations. Permutation averaging is a CPTP channel and its common marginal is the convex average of leaf channels, so the same bound survives.

### 3. Input replacement costs one delta, not an unproved energy bound
Let S denote the averaged leaf marginal before cutoff and rho_R=C rho. The finite-dimensional tree marginal is F^(1)=C S restricted to P. Then

 T(F^(1)(rho_R),rho_R)
 <= T(C S C rho,C S rho)+T(C S rho,C rho)
 <= T(C rho,rho)+T(S rho,rho)
 <= delta_R+ell b.

This is the decisive input-telescoping step. Its second comparison contracts BOTH the broadcast output and its target. There is no independent assumption about the energy of S rho, no output-tail union bound over K leaves, and no hidden K delta_R penalty.

### 4. Primary channel theorem and finite outcomes
Inspected primary: Chiribella, arXiv:1010.1875v4, https://arxiv.org/pdf/1010.1875v4, Section 2.1, Theorems 4–5 and proof, pages 10–11. Theorem 5 applies to permutation-invariant broadcast outputs, not just symmetric-subspace support. Its one-output channel bound is full diamond norm 2d^2/K, independent of input dimension. Therefore the received half-diamond d^2/K is correctly normalized. Its proof uses a symmetric purification lift; this is mathematical existence, not access to a hidden environment.

The input restriction and local cutoff produce a genuine finite-dimensional symmetric channel on a d-dimensional input and d-dimensional receivers, so the theorem's hypotheses apply. To see finite outcomes directly, take the normalized Choi matrix of its one-output EB approximation. It is a separable density operator on d by d, hence a finite convex combination of product pure states (at most d^4 terms by elementary finite-dimensional convexity). The preserved input marginal I/d makes the resulting effects M_i=d p_i |a_i^*><a_i^*| sum exactly to I. Thus this is a trace-preserving measure-and-prepare channel, not a separable operator with a mismatched marginal. Pulling the effects back through C* preserves positivity and their sum I on the full Hilbert space. Embedding the finite output does not change trace norm.

Adding the de Finetti distance and T(rho_R,rho)<=delta_R proves the received inequality. A constant-output finite-outcome channel separately guarantees e<=1.

## Spectral-growth consequence and edge cases
With R=16E/b^2, E>0 and 0<b<1, 2delta_R=b/2+b^2/8<=5b/8. For ell=ceil(log2[d(R)^2/b]), the de Finetti term is at most b and ell b is at most b[2log2 d(R)+log2(1/b)+1]. Their constants sum to 21/8 as claimed. Substituting d(R)<=A(1+R)^s gives the fixed-envelope b log(1/b) law and rearranging gives the displayed necessary exponential energy bound.

This statement must keep A,s and the Hamiltonian fixed. Enlarging ground degeneracy, mode number, or volume can invalidate a formerly claimed uniform envelope. For E=0 the family is in the finite ground sector. For broadcast infimum b_2=0, the rigorous order is: fix R and ell, take achievable b down to zero; then let ell increase; finally let R increase. Equivalently choose achievable b depending on ell so ell b goes to zero. This establishes infimum e=0 only, not an attained exact finite-outcome EB map. The submitted wording is valid with this explicit reading of arbitrarily small slack.

## Evidence independently executed
1. Verified every AUTHOR_FREEZE.json hash before checking.
2. Replayed the author's actual qubit cloner tree and oscillator checks in the review folder, leaving original files untouched. Its full depth-three tree and resource tables reproduced.
3. Independently checked 511 exact rational stochastic leaf paths through depth eight, with a legitimate classical broadcast extension and an explicitly nonclosed singleton family. Both path telescoping and cutoff-input comparison hold exactly.
4. Tested coherent pure-state tails from 10^-12 to 0.9 against their exact distance formula and the gentle bound. The smallest-tail ratio to the bound is essentially one, exposing the square-root obstruction.
5. Checked cutoff/depth-rounding constants on 20 broad energy/error combinations. Large resource expressions are arithmetic evaluations, not simulations of exponentially many observers.

The general proof is analytical; these finite tests are diagnostics, not substitutes for the primary channel theorem.

## Scope, scientific value, and unresolved obligations
This removes a real logical obstacle: no intermediate energy conservation, family closure, uncorrelated clones, or access to source dilation is needed to derive a common classical reconstruction from low-error binary broadcasting plus a fixed low-energy state count. It does not supply the broadcaster, an efficient implementation of the EB approximation, or a physical origin of redundant records. Noncommuting prepared outputs are allowed; no orthogonal pointer-basis conclusion follows. The K-1 broadcaster calls in the proof tree and potentially enormous collective measurement are not cheap devices. Strong equally informed conventional EB strategies are within the comparison class, not ruled out.

Sharpness, the optimal dependence on the spectral envelope, historical novelty, and any transfer to experimental quantum Darwinism remain open. Separate sharpness examples must receive independent checking before being attached to this verdict. Astra historical claims in the source are contextual only and were not independently re-audited here.
