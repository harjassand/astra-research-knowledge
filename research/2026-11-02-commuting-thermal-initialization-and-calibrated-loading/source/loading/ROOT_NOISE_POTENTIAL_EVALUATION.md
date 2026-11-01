# Root explicit finite computation of the signed-noise log potential

1 November2026. Algorithmic supplement to the calibrated terminal-noise candidate. Cluster convergence/tails are separate analytic premises; this note avoids hiding an exp(L log L) enumeration cost.

Let G be the bounded-degree physical-fault overlap graph, and define for any finite fault-label subset A
 Z_A(t;s)=sum_{E subset A} t^|E| [product_{i in E}(-r_i)] exp[-beta(Energy(s+d_E)-Energy(s))].
It has constant term1 and degree at most |A|. It is the exact signed error-island partition function restricted to A with all fault weights scaled by t. Let ell_A(t;s) denote its FORMAL Taylor logarithm, computable to degree L by polynomial arithmetic (e.g. solve ell'_A=Z'_A/Z_A with constant-term division). No real logarithm of a possibly negative numerical truncation is required.

For each connected nonempty support S in G, set
 Psi_S(t;s)=sum_{A subset S} (-1)^(|S|-|A|) ell_A(t;s).
Möbius inversion on supports gives ell_V=sum_{S subset V} Psi_S. If S is disconnected, Z_A factors over G-components and the alternating sum cancels, so Psi_S=0. Every monomial of Taylor degree k uses at most k distinct fault labels; therefore Psi_S has no coefficient below degree |S|. Consequently the full degree-L Taylor logarithm is obtained exactly by summing Psi_S over connected S with |S|<=L, truncated to degree L, and evaluating t=1.

This also includes repeated polymers/fault labels in logarithmic clusters: their Taylor multiplicity contributes to degree k, while Möbius inversion groups them by their distinct support. It is not a naive enumeration of all partitions of k.

For a given S, generating all Z_A from subsets E costs at most sum_{A subset S}2^|A|=3^|S| times polynomial work in L and local energy evaluation. Computing all formal logarithms and the alternating sum adds 2^|S| poly(L). Connected S can be enumerated in N exp(O(L)) time on bounded-degree G. Total work is therefore N exp(O(L)) poly(L), which is polynomial in N/epsilon when L=O(log(N/epsilon)) with fixed constants. Local energy increments inspect only the bounded set of checks touched by S. All coefficients use known coupling/rate values with charged numerical precision.

If the analytic cluster bound controls the absolute total-degree tail by N C exp(-aL), this computed potential differs uniformly from the exact real log Z_V(1;s) by that amount. Analytic continuation/zero-freeness, not the formal logarithm computation alone, supplies positivity and identifies that logarithm branch. Its exponential convergence slack must also absorb the polynomial and exponential error amplification from finite coefficient arithmetic; O(poly(L)+log(N/epsilon)) precision bits suffice when explicit operation-count and coefficient bounds are used.

Thus polynomial positive sampling of the preimage does not require an unproved efficient enumeration of connected polymer MULTISETS. The established algorithmic cluster-expansion literature provides stronger implementations; this is a direct conservative fallback for the actual error-island polynomial.
