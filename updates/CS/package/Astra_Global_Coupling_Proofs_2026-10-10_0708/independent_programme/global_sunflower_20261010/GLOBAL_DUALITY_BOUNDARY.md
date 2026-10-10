# Exact global entropy duality: a known independence theorem and its consequence

Date: 2026-10-10. Natural logarithms throughout.

## Status and attribution

This note closes a logical issue in the global coupling proposal. A uniform O(w) marginal-preserving entropy bound is exactly equivalent to an exponential sunflower independence bound, rather than a strictly stronger hypothesis. The underlying polynomial theorem is **known**, not a new primitive: Samuel Rota Bulò and Marcello Pelillo, *A generalization of the Motzkin–Straus theorem to hypergraphs*, Optimization Letters 3 (2009), 287–295, Theorem 3, specialized to k=3 and tau=1/6.

Primary author-hosted paper: https://www.dsi.unive.it/~pelillo/papers/OL09.pdf

DOI: https://doi.org/10.1007/s11590-008-0108-3

The source was read on 2026-10-10 after independently deriving the cubic specialization. Its Lemma 2 already contains the same second-derivative and third-derivative argument. No priority claim is made for the specialization or for optimization based on it. The entropy conclusion below is a direct application of finite entropy duality.

## 1. The cubic minimum

Let H be any finite 3-uniform hypergraph on V and let alpha(H) be its independence number. Define

    Phi_H(x) = sum_i x_i^3 + 6 sum_{ijk in H} x_i x_j x_k,
    x_i >= 0, sum_i x_i = 1.

Then

    min_x Phi_H(x) = alpha(H)^(-2).                 (1)

For completeness, here is a short self-contained proof of this specialization. A uniform distribution on a maximum independent set gives equality in the upper bound. Let x minimize Phi_H, and suppose an edge {i,j,k} lies in its positive support. The first derivative vanishes in every direction tangent to this support, and the Hessian is nonnegative on such directions. For a pair i,j write

    R_ij = sum_{l outside {i,j,k}: {i,j,l} in H} x_l.

The Hessian curvature along e_i-e_j is

    6(x_i+x_j-2x_k-2R_ij).

The analogous three pair curvatures are nonnegative, but their sum is

    -12(R_ij+R_jk+R_ki) <= 0.

Consequently every R is zero and every pair curvature is zero, which also gives x_i=x_j=x_k. For a direction supported on these three vertices with d_i+d_j+d_k=0, the first and second order terms vanish. Its cubic coefficient is

    d_i^3+d_j^3+d_k^3+6d_i d_j d_k = 9d_i d_j d_k.

Taking d=(1,1,-2) gives a strictly negative change for sufficiently small positive displacement, a contradiction. Thus the support is independent. If its size is s, convexity gives sum_i x_i^3 >= 1/s^2 >= 1/alpha(H)^2. This proves (1).

## 2. Exact entropy interpretation

Permit the ordered triples consisting of an edge of H in any order, together with all diagonal triples. Denote this relation by R_H. For a probability distribution P on V, let

    I_H(P) = min_Q D(Q || P^3),

where Q is supported on R_H and each of its three marginals is P. Diagonal Q is always feasible. Restricting first to the support S of P, the finite entropy dual is

    I_H(P) = sup_{u>0, sum u=1}
             [-3 D(P||u) - log Phi_{H[S]}(u)].       (2)

One common dual potential suffices by averaging the three potentials and using permutation symmetry and convexity of log-partition. Strong duality follows from a relative-interior feasible coupling: give every allowed triple sufficiently small positive mass and complete the identical marginal deficits with diagonal mass.

Combining (1) and (2) gives

    I_H(P) <= 2 log alpha(H[S]) <= 2 log alpha(H).

Conversely, take P uniform on a maximum independent set. Only diagonal triples are then permitted, so I_H(P)=2 log alpha(H). Therefore

    sup_P I_H(P) = 2 log alpha(H).                  (3)

For the hypergraph whose edges are nontrivial three-petal sunflowers among distinct rows of a partite family F, relation R_H is exactly global coordinatewise validity. Indeed a triple with exactly two equal rows fails at any coordinate distinguishing the remaining row. Thus (3) applies without an extra repeated-row case.

## 3. What this does and does not buy

An exponential independence bound would automatically supply the all-distributions global KL coupling bound. Conversely the latter applied to a uniform sunflower-free family gives the independence bound. Hence simply optimizing the cubic or defining the entropy capacity is an equivalent reformulation of the original global obstruction.

The dual also makes the acquisition issue concrete. Once a scaling u is acquired, rejection from u^3 produces the entropy-optimal relation-supported coupling, with acceptance Phi_H(u). A C^(-w) acceptance guarantee for every u is exactly the missing exponential independence bound by (1). The one-coordinate acceptance estimate cannot be multiplied through arbitrary row correlations.

No polynomial-time global acquisition algorithm is claimed. The hypergraph can have cubic size in the explicit row count; evaluating all allowed triples can require O(|F|^3 w) elementary coordinate comparisons. General polynomial minimization in (1) includes maximum hypergraph independence, so its exact optimization cannot be treated as a free preprocessing oracle. The first/second/third derivative argument characterizes minima; it is not a proved efficient route to the global optimum.

