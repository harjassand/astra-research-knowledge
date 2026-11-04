# A complete planar receiver for learned ferromagnetic interfaces

2026-11-04. Status: scoped receiver construction; independent review is recorded in PLANAR_RECEIVER_AUDIT.md. Depends on the weighted stability theorem in PROOF.md; that theorem is not modified here. Established matchgate synthesis and FKT are explicitly used, not claimed as new algorithms.

## 1. Input/output contract

There are B isolated unknown zero-field ferromagnetic planar Ising blocks. Block b has k_b ordered boundary spins lying on one face and an empirical pair matrix A_b, obtained from independent isolated-block snapshots. Let C_b be its unknown true pair matrix and D_total=sum_b sum_(i<j)|A_(b,ij)-C_(b,ij)|. The structural promise and boundary order are supplied, not tested.

The assembly is a SUPPLIED PLANAR FACTOR-GRAPH EMBEDDING in a disk. Each block is a node with its k_b ports in the measured cyclic order. Distinct block ports initially correspond to distinct spin variables. Known environment spins and ferromagnetic pair factors (1+a_e x_u x_v), with rational 0<=a_e<=1, connect the ports and environment spins. All environment spins have zero field. Choose K distinct output spins with probe legs on the outer boundary of this same disk, in supplied cyclic order. Boundary fields are allowed only on these cofacial outputs, through product_i(1+t_i x_i), rational 0<=t_i<=1.

The algorithm computes a relative partition-normalization estimate and produces a normalized sampler/evaluator for the K output spins under those fields. Runtime is polynomial in total interface size, known assembly size, field/coupling bit lengths and requested accuracy; it does not depend on unknown internal block volumes. Its guarantee uses D_total and the weighted stability theorem. It does NOT sample arbitrary internal assembly spins, allow general interior fields, or efficiently contract arbitrary nonplanar assemblies.

Use a uniform baseline measure for each explicit environment spin. If physical convention instead sums it with unnormalized counting measure, multiply by the known factor 2 per such spin. Unknown isolated block partition factors are not learned; all outputs are relative to their product.

## 2. Exact Fourier contraction, including normalization

For each block, write its signed law as
q_b(x_b)=2^(-k_b) sum_(S even) Pf((A_b)_S) x_S.
Expand every known edge factor as 1+a_e x_u x_v. Averaging all spin variables under their uniform baselines retains exactly the even total powers at every spin. Therefore the assembly's relative signed partition is the ordinary binary tensor contraction with the following signatures:

1. At block b, F_b(s)=Pf((A_b)_support(s)) for even support and zero for odd support.
2. At a spin vertex, an even-parity signature on its incident Fourier indices, including its block index if any, its edge indices, and one output probe if designated.
3. At an environment edge, the two-leg signature E_e(0,0)=1, E_e(1,1)=a_e, and E_e(0,1)=E_e(1,0)=0.

There is NO omitted factor of 2: the 2^(-k_b) factors in the block laws and the uniform baseline factors at environment spins exactly cancel the sums over spins when enforcing parity. The contraction with all probe indices zero equals the signed partition Z_A(0). The open probe tensor has zero entries on odd total probe parity, because every constituent signature has even parity.

## 3. Closing output fields without non-matchgate unary factors

Individual unary field vectors (1,z_i) have mixed parity and must not simply be assumed matchgates. Instead close all K probe legs at once with
H_z(s)=1[|s| even] product_i z_i^(s_i).
Because the open network has only even total probe parity, this gives exactly the same value as the product of the unary vectors, for ANY rational z_i, positive or negative.

The signature H_z is itself a principal-Pfaffian signature: take the antisymmetric matrix L with L_ij=z_i z_j for i<j. For every even S, Pf(L_S)=product_(i in S)z_i, since Pf(J_S)=1 for the all-upper-ones antisymmetric matrix J. Thus H_z is an even matchgate signature. Add its realizing disk in the common outer face and join its ports in reverse boundary order, as required for planar gluing. Its Boolean values are symmetric under simultaneous permutation of the z labels, so the reversal causes no physical sign change.

The resulting closed binary contraction equals
Z_A(z)=sum_(all spins) [product_b q_b(x_b)] [uniform environment baselines] [product_e(1+a_e x_u x_v)] [product_(outputs i)(1+z_i x_i)].
This is an algebraic identity even for signed empirical block laws and mixed-sign probe z. The physical error certificate is applied only to the admitted nonnegative query fields t, not to every intermediate z used to calculate prefixes.

## 4. Why every gate has a polynomial-size rational planar realization

For an antisymmetric r by r rational matrix M, the signature s -> Pf(M_support(s)) is matchgate-realizable with O(r^4) graph vertices and rational weights. The explicit established construction is Cai and Gorenstein, *Matchgates Revisited*, Theorem 5.1 and Section 5 (2014): start with weighted complete-graph Pfaffians and replace crossings by constant-size signed crossover gadgets. Its signature convention uses deleted vertices; attaching one unit-weight leaf at each external node complements the bits and converts that convention to support(s). No approximation or physical positivity is needed. Weights are matrix entries and fixed constants, so encoding lengths remain polynomial.

Even parity at an r-leg spin vertex is the special case M=J. The edge signature is the r=2 case M_12=a_e. The closing signature is M_ij=z_i z_j. Replacing every factor node by its planar realizing disk preserves the supplied global planar embedding. The crossover signs INSIDE synthesized gates are required algebraic signs; they are not ordinary nonnegative physical interactions and must not be dropped.

Let H be the number of vertices in the synthesized planar matching graph. A conservative bound is
H=O(sum_b k_b^4 + sum_(spin vertices v) d_v^4 + |E_environment| + K^4),
where d_v counts all incident Fourier legs including probes. Thus H is polynomial in the supplied assembly/interface description. The algorithm constructs these graphs from O(r^2) matrix entries, not from an explicitly enumerated 2^r signature table.

## 5. Joining matchgates and fixing the global Pfaffian sign

Join two external matchgate vertices by a unit-weight edge along each factor-graph wire. A global perfect matching either uses that bridge (both endpoints are externally matched, corresponding to bit 1 at both signatures) or does not (both are matched inside their gates, bit 0). Hence the perfect-matching sum is exactly the desired equality contraction of the signatures, with no extra summation prefactor.

A planar Pfaffian orientation computes this weighted perfect-matching sum by one Pfaffian, up to the known global orientation/ordering sign. Signed and zero edge weights do not invalidate the combinatorial identity. The sign can be calibrated on the same fixed topology at A_b=0, a_e=0 and z=0: only the all-zero Fourier assignment survives, so the contraction is exactly 1. The orientation depends on topology, not weights. Keep zero-weight edges in the synthesis topology for this calibration. Alternatively the usual explicit FKT sign convention can be used.

This paragraph is a specified-model application of established FKT, not a new counting method.

## 6. Output prefixes and an actual sampler

For a prefix u=(u_1,...,u_j) of the output spins, its unnormalized signed weighted marginal is
S_A(u)=2^(-j) [product_(i<=j)(1+t_i u_i)] Z_A(u_1,...,u_j,t_(j+1),...,t_K).
The identity follows by substituting the fixed field factors and inserting (1+u_i x_i)/2 for each observed spin. It holds after summing all internal spins. Thus every prefix needed by the signed-flow sampler is computed by the explicit planar Pfaffian receiver above.

If the signed root Z_A(t) is nonpositive, return a fixed fallback output/value; this cannot happen on the good training event. Normalize by Z_A(t), or cancel that common positive denominator in every child ratio. Take positive parts of child masses and sample proportionally. For 0<epsilon<=1 and K>0, handle zero/one probabilities deterministically, cap each nontrivial rational-coin rejection after R=ceil(log2(4K/epsilon))+1 trials, and choose a positive-mass child on cap exceedance. The extra TV error is at most epsilon/4 by a union bound. For K=0 the output is the unique empty assignment and no coin calls are needed; the partition query is still computed. This is exactly the rigorously analyzed repair in PROOF.md, now with a complete contraction oracle rather than an assumed one.

The actual capped sampler has a polynomial-time evaluator by multiplying its explicit rational transition probabilities, including each capped-coin fallback probability.

## 7. Error guarantee under the physical query

Let R=product_b P_b times the uniform environment-spin measure. Let W_t be the product of the nonnegative ferromagnetic edge factors and the nonnegative output-field factors. It has nonnegative Fourier coefficients. Apply the multiblock theorem of PROOF.md:
||W_t(product_b q_b-product_b P_b)||_1 <= Z_true(t) eta,
where eta=exp(D_total)-1.

Marginalizing all internal spins cannot increase this weighted L1 error. Therefore
|Z_A(t)/Z_true(t)-1|<=eta,
and if eta<1, normalized signed output marginals are within 2eta/(1-eta) in L1 of the true output law. Positive-flow repair gives TV error at most eta/(1-eta), plus the budgeted capped-coin error.

This guarantee does not require any reconstructed block to be a nonnegative distribution. It also does not require an efficient sampler for the unknown internal block models. It does require the original independent-block model promises and correctly calibrated physical edge factors.

## 8. Statistical and bit cost

Let 0<epsilon<=1, 0<alpha<1 and M=sum_b binom(k_b,2). For M=0, all isolated block boundary laws are known uniform zero/one-spin laws and no training is needed. For M>0, estimate every pair within h=epsilon/(32M). A sufficient number of independent full-boundary snapshots PER nontrivial block is
N>=2 h^(-2) log(2M/alpha).
A union bound gives D_total<=epsilon/32 with confidence at least 1-alpha. Thus eta<=epsilon/16 and the repaired output law has O(epsilon) TV error, with room for the explicit coin budget. The total snapshot count across blocks is at most B N. This conservative bound is polynomial in the total number of observed interface pairs and does not hide bulk decorrelation/measurement costs. Blocks of arity zero or one have known uniform zero-field laws and need no pair estimates.

All empirical entries, environment activities and query fields are rational. Matchgate synthesis uses only these entries, their simple products and fixed constants. The global Pfaffian has polynomial degree in a polynomial number H of rational weights. Clearing denominators and standard determinant/Pfaffian height bounds give polynomial output bit length; exact fraction-free or rational elimination has polynomial bit runtime, even under severe cancellation. Each response query uses one such Pfaffian; output sampling uses at most 2K such queries. No exponential characteristic-zero field extension, near-zero numerical-sign oracle, or real-RAM assumption is used.

For each fixed learned summary, the guarantees hold simultaneously over all admitted planar assemblies and boundary-field queries whose pair-error budget remains the same. The cost for a particular assembly still charges its full known graph/interface description and rational bit lengths. This is not an efficient search over assembly designs. If a learned summary is reused for several independent block instances, its pair-error budget must be counted once per occurrence; reusing training data does not eliminate accumulation of systematic approximation error.

## 9. Strongest comparison and remaining limits

The contraction receiver is established planar matchgate/FKT machinery: Cai and Gorenstein, *Matchgates Revisited*, Theory of Computing 10 (2014), Theorem 5.1, https://www.theoryofcomputing.org/articles/v010a007/v010a007.pdf . Galashin–Pylyavskyy exact boundary reconstruction and classical Ising boundary-field response methods are also prior, as documented in PROOF.md.

What the combined proof adds as an input/output contract is a noisy-data, hidden-volume-independent assembly interface with controlled RELATIVE response and output-law error, despite signed empirical intermediates. It does not introduce a new exact planar solver. Whether this precise robust learning/assembly guarantee is new is unestablished; an ordinary algorithm supplied the same data may exploit the same mechanism.

The complete receiver is limited to supplied planar assembly embeddings, cofacial outputs/fields, and the stated zero-field isolated-block model. Nonplanar contraction, arbitrary interior fields, model certification, absolute bulk free energies and production performance remain outside the theorem. No physical deployment or civilisation-scale advantage is established.
