> **CORRECTED AUDIT (2026-10-08):** The finite-quotient and periodic-point arguments below remain valid. The claim that Formanek excludes characteristic-two torsion-free hyperbolic witnesses is not established by its cited sources, and the assertion that h_sup=0 might allow infinite-positive-Rokhlin free ergodic actions conflicts with Seward Corollary 7.7. See [CORRECTED_AUDIT.md](CORRECTED_AUDIT.md).

# Additional algebraic-dynamical audits of the Bernoulli kernel
2026-10-08. Companion to RESEARCH.md. Proven solely from ab=1 != ba in F_q[G] with G infinite; no group197 source correctness assumed.

## Periodic-point theorem
Define A=T_a, B=T_b, C=I-BA=T_{1-ba}; K=im C=ker A and Y=ker C=im B on X=F_q^G, as in the main note. Let N be any finite-index NORMAL subgroup, Q=G/N. Then the N-periodic configuration space X^N is canonically F_q^Q, finite dimensional over F_q, and invariant under A,B,C. On X^N, AB=I; finite dimensionality implies BA=I there too, hence C=0 on X^N. Therefore:
- K intersect X^N = {0}.
- X^N is contained in Y, despite Y being a PROPER closed G-invariant subgroup of X.
Every point x with finite G-orbit is N-periodic for the finite-index normal core N of its stabilizer. Therefore K has NO nonzero periodic points, and Y contains EVERY periodic point of the full shift X. This is an exact obstruction to K being a nontrivial FULL SHIFT as a topological G-system: a nontrivial full shift always has nonzero constant periodic points. The absence of periodic points beyond zero does NOT distinguish measure isomorphism: such points are Haar-null in infinite Bernoulli shifts.

## Group-ring finite-quotient invisibility
For each epimorphism phi:G->Q to a finite group Q, the images phi_*(a),phi_*(b) in the finite-dimensional algebra F_q[Q] satisfy phi_*(a)phi_*(b)=1; hence phi_*(b)phi_*(a)=1 and phi_*(r)=0 for r=1-ba. In particular no finite quotient detects the nontrivial idempotent r.

Stronger uniform residual-kernel consequence: let S=supp(r). Suppose every distinct s,t in S could be separated in SOME finite group quotient phi_{s,t}:G->Q_{s,t}. Their finite direct product supplies a finite image in which the images of ALL elements of S are distinct, so the nonzero finite sum r pushes forward to a nonzero group-ring element; contradiction. Hence there is a single pair s!=t in S whose images coincide under EVERY finite-group homomorphism of G, so s^{-1}t is a specified-in-principle nonidentity element of the finite residual intersection of all finite-index normal subgroups. The actual support S/pair was not acquired from the original graph construction.

This recovers a strong algebraic form of nonresidual finiteness from the finite-support inverse witness, without assuming nonsoficity theorems or any hyperbolicity.

## Failure of naïve classification transfers
- On every finite quotient, the defect r vanishes even though it is nonzero in F_q[G]. Consequently all finite-quotient dynamics will incorrectly show BA=I; a periodic-orbit / finite-cover experiment cannot verify non-direct-finiteness. This is a failure mode for computational model checking.
- The periodic-point and topological fixed-point obstructions are categorical/topological only. They do NOT prove Haar K is not measurably Bernoulli.
- Neither the perfect Haar product X= X x K nor the finite-quotient invisibility of K implies the entropy supremum is zero or that nontrivial Bernoulli shifts are measurably isomorphic.

## Adversarial source alignment
Formanek/Bartels-Lueck-Reich already exclude any torsion-free hyperbolic ab=1 !=ba witness (main note). The family197 candidate's hyperbolic upgrade must therefore break at a source graph/disk/topology premise; do not use finite quotient checks to select which.

## Next check
Once explicit a,b over a concrete presented family197 group are available, calculate S=supp(1-ba), finite-window projection ranks for Y=im T_b, and candidate s^-1 t in finite residual. The raw source proof currently supplies abstract finite sums but not a finitely instantiated example; no numerical support cardinality or finitely presented word pair is claimed.

## 2026 structural-ergodic-theory significance (prior-art check)
Tim Austin, ICM 2026, *Some Recent Developments in Structural Ergodic Theory*, https://epubs.siam.org/doi/full/10.1137/25M1805564 , Question 3.1 explicitly asks whether there exists a countable group for which Rokhlin entropy is identically zero. Under the hypothesis that *all* nontrivial Bernoulli shifts of a given infinite group G are measure isomorphic, Seward's finite-base min formula plus infinite-base theorem (main RESEARCH.md Theorem C) imply NO free ergodic pmp action of G has positive Rokhlin entropy, so the full-collapse outcome would supply an explicit witness to this independent major open question (within the free-ergodic interface). Conversely family197 group-ring failure alone supplies only a finite h_sup bound, not an explicit group with universally zero entropy. This distinction narrows significance and guards against overclaiming a solution of Austin's question.
