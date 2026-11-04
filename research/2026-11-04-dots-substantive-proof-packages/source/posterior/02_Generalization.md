# Conditional inference: extending the obstruction to general varying-field Ising

Date: 2026-11-04. Status: independently audited as a scoped reduction, with unit-edge and probability-estimation clarifications incorporated. Depends on POSTERIOR_OBSTRUCTION.md. No novelty claim. All complexity implications concern polynomial-time randomized approximation, not an unconditional impossibility theorem.

## Lemma: cubic regularization with polynomial encoded weights

A general finite simple ferromagnetic Ising graph with positive rational activities can be approximated to prescribed TV error on its original spins by a simple cubic ferromagnetic Ising graph of polynomial size and polynomial weight bit length. Its partition can likewise be approximated after explicit known factors are removed.

Delete any original edges with beta_e=1 first; they do not affect weights or the partition function. For each vertex v of degree d>=1, replace it by a path of d copies, one for each original incident edge. Put its activity lambda_v on the first copy, and activity 1 on all other copies. Attach each original incident edge to its assigned copy. The resulting maximum degree is three. A degree-zero vertex is kept. Give every path edge a large interaction B. Let a configuration be aligned if each path is constant.

An aligned configuration corresponds uniquely to an original configuration and has exactly its weight multiplied by B^h, where h is the number of path edges. For any configuration of first-copy representatives, compare all other copy assignments with the aligned assignment. Their vertex-field weights agree, because fields occur only on the representatives. If an assignment is unaligned, at least one strong path edge disagrees and its relative strong-edge weight is at most B^-1. The ratio of external interaction weights is at most Q=product_(original e) beta_e. If N is the number of path copies, there are at most 2^N assignments. Consequently Z_unaligned/Z_aligned <= 2^N Q/B. Choose B>=2^N Q/delta, a rational number with polynomial bit length. Projecting first copies is delta-close to the original distribution; the partition after division by B^h has relative error at most delta.

To make the maximum-degree-three graph cubic, first ensure an even number of vertices by adding one isolated activity-1 vertex if necessary. This adds an explicit partition factor 2. There is then an even number of degree deficits because sum_v(3-deg v)=3N-2m is even. Pair the deficits arbitrarily. For each pair introduce a separate K4 with one edge ab removed. The vertices a,b have degree two; attach them respectively to the two deficit incidences. All new vertices and original vertices then have degree three. The graph remains simple, even if the two deficits belonged to the same original vertex. All added vertices have activity 1.

If all new edges have interaction exactly 1, the added spins are independent and contribute a known factor 2^(number of added vertices); the original marginal is unchanged. Replace all such unit interactions by 1+tau, choosing tau so the number of added edges times tau is at most the allocated error. Every configuration weight is multiplied by a factor between 1 and (1+tau)^(number of added edges), controlling both partition and TV error. The resulting graph is simple, cubic, strictly ferromagnetic, with arbitrary positive rational activities and polynomial encoding size.

Together with POSTERIOR_OBSTRUCTION.md, a uniform polynomial-time sampler for arbitrary observations in accepted zero-field positive cubic tensor networks would give a uniform polynomial-time sampler for GENERAL varying-field ferromagnetic Ising, at any inverse-polynomial target accuracy.

## From such a sampler to a counting scheme

This implication does not assume that sampling is automatically equivalent to counting without a reduction. The varying-field Ising family is closed under pinning: fixing a spin deletes that vertex and multiplies adjacent unary activities by positive rational interaction ratios, while retaining ferromagnetic edge interactions. Encoding lengths grow only additively.

At each of n stages, use the hypothetical sampler on the current pinned instance to estimate the two probabilities of one remaining spin to additive error a=O(epsilon/n), with failure probability O(delta/n). Use complementary empirical frequencies (estimate one probability and take one minus it for the other) and choose a spin value with estimated probability at least 1/2. On simultaneous accuracy, its true conditional probability is at least 1/2-a, hence at least 1/3. A fresh estimate of that chosen probability to additive a yields relative error O(epsilon/n). Clip the estimate below at 1/4, or output a flagged failure if that threshold is violated. On the simultaneous accuracy event and a<=1/12, the chosen true probability is at least 5/12 and the fresh estimate at least 1/3, so this convention does not change the success case; it prevents division by zero on an already-budgeted failure event. The sampling TV error is allocated below a, and independent runs plus Hoeffding give polynomial sample count. The selected sequence yields an assignment s* with probability equal to the product of these conditional probabilities. Therefore
Z = w(s*) / product_(stages i) Pr[s*_i | earlier selected spins].
All factors are bounded away from zero by the selection rule, so the estimated product and resulting partition value have relative error O(epsilon). The union-bound failure probability is O(delta), with constants chosen for requested tolerances. Original assignment weight w(s*) is exactly computable from rational inputs. This is an FPRAS.

## Consequence and limitation

Goldberg and Jerrum proved that general varying-field ferromagnetic Ising counting is approximation-equivalent to #BIS:
https://www.cs.ox.ac.uk/people/leslieann.goldberg/papers/ising.pdf

Consequently the hypothetical unrestricted posterior sampler described above would imply an FPRAS for #BIS. This does not prove that such a sampler is impossible. It shows why the unconditional compiler cannot honestly be advertised as solving unrestricted Bayesian inference merely because its raw input tensors are positive and its unconditioned latent fields are zero. The barrier is a known approximate-counting frontier, not a new complexity separation.

This reduction also does not rule out efficient inference for particular observation patterns, average-case evidence, approximate methods with weaker guarantees, bounded-width graphs, or residual componentwise consistent fields.
