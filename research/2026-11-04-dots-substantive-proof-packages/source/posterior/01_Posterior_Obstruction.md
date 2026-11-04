# A conditioning obstruction for the positive latent compiler

Date: 2026-11-04. Status: independently derived reduction; independent adversarial review found the scoped construction and bounds valid. This proof makes no priority claim. It distinguishes unconditional generation from unrestricted posterior inference.

## Proposition

Every ferromagnetic Ising model with arbitrary positive rational vertex activities on a finite simple cubic graph can, to any prescribed total-variation accuracy, be realized as the projection of the conditional original-variable/latent distribution of a strictly positive rational cubic tensor network accepted by the zero-field branch of the compiler. The conditioning fixes a matching of original edge bits. The construction and all raw tensor bit lengths are polynomial in target input length and logarithmic inverse accuracy.

Thus the efficient unconditional sampler does not by itself resolve arbitrary opposing-field posterior inference. This proposition alone is a reduction for cubic target graphs, not a proved complexity classification of that restricted target family.

## Construction

Let H have n vertices and 3n/2 edges, interactions beta_e>1, activities lambda_v>0, with weight
w(s)=product_e beta_e^[s_u=s_v] product_v lambda_v^[s_v=1].
Take two copies of H. In each copy replace every edge uv by the path
u -- p_(u,e) -- p_(v,e) -- v.
Join each port p_(v,e) to its corresponding port in the other copy by an additional edge. The resulting graph is simple and cubic. These new cross-copy edges form a matching on all ports.

Use a positive symmetric two-column factor
F(a)=[[a,1],[1,a]], a>1,
at both endpoints of every edge (the parameter can depend on that edge). At each vertex form its raw tensor by summing the two products of its three incident factor columns, with equal mixture coefficients. All raw entries are positive rationals, and all factor matrices are invertible. The tensor has nonzero hyperdeterminant: it is an invertible three-leg image of the two-term diagonal tensor. Column normalization leaves equal mixture coefficients. Every hidden edge Gram matrix is
[[a^2+1,2a],[2a,a^2+1]],
so the unconditional hidden model has zero fields and ferromagnetic interaction (a^2+1)/(2a). It is therefore accepted by the existing compiler.

Choose a large common parameter R on each core-to-port edge. Write B=(R^2+1)/(2R) for the resulting strong interaction.
On the middle edge p_(u,e)--p_(v,e), select a rational a_e>1 so that (a_e^2+1)/(2a_e) approximates the desired beta_e to allocated logarithmic error. This is possible in polynomial bit complexity by approximating beta_e+sqrt(beta_e^2-1). The case beta_e=1, if needed, can first be replaced by a nearby value greater than one with controlled global error.

For each vertex choose three nonunit positive rational port activities f_(v,e) whose product is lambda_v. If lambda_v!=1 use lambda_v,2,1/2. If lambda_v=1 use 2,2,1/4. On each matching edge choose a=max(f,1/f)>1. Observe its original edge bit to be 1 when f>1, and 0 when f<1. The conditional endpoint factor is respectively (1,a) or (a,1), up to a positive scalar. Thus the observation imposes the activity f at that port in BOTH copies.

After all matching-edge observations, the two hidden copies are independent. Each has zero-field core spins, port activities f, strong core-to-port interactions B, and target-approximating middle interactions.

## Strong contraction under opposing fields, without misusing the consistent-field lemma

For one conditional copy let E be the event that every port equals its associated core spin. Conditional on E, summing no further variables is necessary: the core model is exactly the target model with its slightly approximated middle interactions, because product_(ports at v) f_(v,e)=lambda_v.

A crude bound suffices to make E overwhelmingly likely with polynomial ENCODING length. There are k=3n ports. For any core assignment s, map every port assignment y to the aligned assignment y*(s). If y violates at least one alignment, the ratio of its strong-edge weight to the aligned weight is at most B^-1. The port-field ratio is at most
P=product_ports max(f,1/f),
and the middle-edge ratio at most
Q=product_e beta'_e,
where beta'_e are the actually realized rational interactions. Therefore
w(s,y)/w(s,y*(s)) <= P Q / B
for every unaligned y. Summing at most 2^k assignments per s gives
Z_(not E)/Z_E <= 2^k P Q / B.
Choose rational R >= 2^(k+1) P Q / delta. Since B>=R/2, this ratio is at most delta. The bit length of R is O(k+log P+log Q+log(1/delta)), polynomial in the encoded target instance and precision. This uses large numerical interactions, but not exponentially long input descriptions.

Consequently the core marginal differs by at most delta in total variation from the target with approximated interactions. Give that initial interaction approximation a separate delta budget; its per-configuration logarithmic error sums over edges, so the total error remains O(delta).

Any epsilon-accurate sampler for the conditioned source distribution, followed by projection to one copy's core spins, would therefore sample the target within epsilon+O(delta). The same conclusion holds for a sampler returning ONLY original edge bits. Complete its output with the fixed evidence bits. Conditional on this full original assignment x, latent vertex spins are independent with probabilities proportional to c_v(s) product_(e incident v) B_(v,e)(x_e,s). This is a positive local reverse kernel, obtained by factoring q(s|x). Draw each hidden spin through this kernel and then project the cores. For the constructed rational factors the probabilities are rational with polynomial bit length; approximate/capped coins add only their allocated TV error. Markov-kernel contraction ensures that an epsilon-TV original posterior sample becomes an epsilon-TV joint/latent sample before coin error. Thus no inaccessible hidden-state oracle is assumed.

## Exact posterior recognition rule

For evidence x_e=b_e on an edge subset A, delete those hidden interactions. In the labels and positive symmetrization of the original compiler, the residual vertex activity is
lambda'_v = lambda_v product_(e in A incident v) [ B_(v,e)(b_e,1) / ( B_(v,e)(b_e,0) r_(v,e) ) ].
This follows directly from the residual spin-zero weight c_v(0) product_(observed e)B_(v,e)(b_e,0) product_(unobserved e)r_(v,e)^-1 and analogous spin-one weight.

The residual graph remains ferromagnetic. If the lambda'_v are componentwise consistent, the same sampler/counting proof applies, with all observation likelihood constants recorded. This can handle exponentially rare but certified evidence without rejection sampling. If they are inconsistent, the unconditional theorem gives no guarantee; alternative methods may still work.

The positive conditional kernel for unobserved original edges is unchanged once residual hidden spins are sampled. For observed original bits, the output is their fixed evidence value. Exact positive likelihood factors must be retained if estimating the evidence probability through a ratio of partition functions.

## Established comparison

Goldberg and Jerrum's general varying-field ferromagnetic partition problem is approximation-equivalent to #BIS: https://www.cs.ox.ac.uk/people/leslieann.goldberg/papers/ising.pdf . The present proposition does not assume that their result automatically holds on the cubic restricted target family, and does not claim an impossibility theorem for sampling. Its justified conclusion is that the acquired unconditional representation does not preserve its consistent-field certificate under arbitrary observations. This is an explicit boundary of the compiler, not a new Ising algorithm or a novelty claim.
