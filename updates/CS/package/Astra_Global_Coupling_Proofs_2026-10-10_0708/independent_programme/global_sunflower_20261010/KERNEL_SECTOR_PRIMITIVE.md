# A constructive global coupling for full latent-product projection models

Date: 2026-10-10. This is a restricted positive theorem, **not** a solution of the general sunflower problem. The representation assumptions are substantial. Novelty has not been established.

## 1. Native representation and theorem

Let Z_1,...,Z_m be independent uniform finite latent variables. For each of w observed coordinates, specify a subset S_i of the latent variables and an injective recoding h_i of the complete subtuple Z_{S_i}. The observed row is

    X_i = h_i(Z_{S_i}).

The support must be the image of the **entire Cartesian latent product**. Pairwise independence, uniform one-coordinate marginals, or an arbitrary subset of that product does not suffice. Variables with one value can be discarded. Variables appearing in no S_i do not affect the observed distribution.

**Theorem A, binary case.** If all latent variables are uniform bits and A is the w-by-m incidence matrix of the S_i, there is an explicitly samplable coupling Q of three observed rows, each with the original row distribution P, which is supported on sunflowers and satisfies

    Q(x,y,z) <= 4^{rank_R A} P(x)P(y)P(z).

Consequently all Renyi divergence orders, including KL and infinity, are at most rank_R(A) log 4 <= w log 4. If the global observation map is injective, the construction's nonzero likelihood ratio is exactly 4^{rank_R A}.

**Theorem B, arbitrary uniform alphabets.** Under the same full-product and injective-subtuple assumptions, but with arbitrary finite uniform latent alphabets, there is an explicit coupling with

    Q(x,y,z) <= (9/2)^w P(x)P(y)P(z).

Thus the construction accounts simultaneously for alphabet size and deterministic coordinate dependence, without paying total correlation or the number of latent variables.

## 2. Binary kernel-sector construction

Put r=rank_R A and d=m-r. Use rational Gaussian elimination to select d free coordinates in ker_C A. Independently set each free coordinate to one of

    0, 1, omega, omega^2,

uniformly, where omega is a primitive cube root of unity. Solve the pivot coordinates so that Az=0.

Assign type 0 to z_j=0. Otherwise assign type c in {1,2,3} according to which of the three 120-degree sectors centered at 1,omega,omega^2 contains z_j, with deterministic boundary ties. Every sector is contained in a pointed cone. For any row of A, its nonzero z_j cannot all have one type: the sum of nonzero vectors in that pointed cone would be nonzero, contrary to Az=0. Therefore every observed coordinate sees either no nonzero types or at least two different nonzero types.

Independently sample a uniform base bit vector B. At each latent coordinate j, convert its type into the three replicas as follows:

    type 0: (B_j,   B_j,   B_j)
    type 1: (1-B_j, B_j,   B_j)
    type 2: (B_j,   1-B_j, B_j)
    type 3: (B_j,   B_j,   1-B_j).

For each replica, conditioning on the entire type vector leaves a uniform independent bit vector, since the base bits are uniform. Its marginal is exactly the original latent product law.

If an observed subtuple contains only type 0, its three values are all equal. If it contains two distinct nonzero types, every pair of replicas differs in at least one latent bit in that subtuple. Its three values are all distinct. Injective recoding preserves these two allowed cases. Hence every generated triple is globally admissible.

### Exact entropy and pointwise density

The type vector determines every free choice: the four selected complex values have distinct types. Thus it is a one-to-one image of 4^d equally likely free assignments, and has entropy d log 4. The complete latent triple determines both the type vector and the base vector: B_j is the majority bit, and the type identifies the odd replica or the all-equal case. Therefore Q is uniform on

    2^m 4^d = 2^{3m-2r}

latent triples. The independent uniform reference is uniform on 2^{3m} triples. The likelihood ratio is exactly 4^r wherever Q is positive. Pushing forward by the observation map gives the stated pointwise bound, even if the map has irrelevant hidden variables.

This is a global operation: all pivot types depend on a simultaneous kernel solve. It does not glue conditional one-coordinate couplings or assume that their histories coincide.

## 3. Exact arithmetic and implementation cost

Everything can be done in Q(omega). Write z=a+b omega with rational a,b. The three sector scores, multiplied by two, are

    2a-b, 2b-a, -a-b.

Choose a maximum, with a fixed tie order. For nonzero z this maximum is strictly positive. If all nonzero entries in an incidence row receive the same sector, the corresponding real linear functional has positive value on their sum, contradicting its being zero.

Input is the explicit incidence matrix plus evaluable recodings. No listing of the exponentially large row family is needed. A fraction-free rational elimination gives a kernel description in polynomial bit complexity in w and m: the matrix entries are 0 or 1, and the relevant minors have polynomial bit length by the determinant bound. Each sample uses d two-bit choices, a linear kernel evaluation, exact rational comparisons, m independent base bits, and evaluation of the supplied recodings. The latter cost depends on how the recodings are represented and is not hidden as a free oracle. The output size is at least the size needed to write the three observed rows.

The included verifier uses Fraction arithmetic for modest examples. The polynomial bit-complexity claim concerns standard fraction-free elimination, not an unanalysed floating-point optimizer.

## 4. Uniform latent alphabets of any size

Call a latent variable nonbinary when it has q_j>=3 values. For each observed coordinate containing a nonbinary latent variable, choose one such variable; let J be the union of choices. If t coordinates contain any nonbinary variable, |J|<=t.

For j in J, draw a uniform ordered triple of pairwise distinct values. Each marginal is uniform, and its likelihood ratio against three independent uniform values is

    q_j^2 / [(q_j-1)(q_j-2)] <= 9/2.

Every observed coordinate containing a nonbinary variable contains one selected member of J, so its three subtuples are automatically pairwise distinct. There are w-t remaining coordinates, all depending only on binary latent variables. Apply Theorem A to their incidence matrix. Nonselected nonbinary variables can be sampled independently across all replicas. Binary variables not appearing in the remaining matrix are free columns and are automatically sampled independently by the kernel construction.

The product likelihood ratio is at most

    (9/2)^{|J|} 4^{rank A_remaining} <= (9/2)^w.

Again push forward through the injective subtuple recodings. This proves Theorem B.

## 5. Sunflower-free consequence and a direct witness

If the observed full-product support is sunflower-free, no effective latent variable can have three values: varying that variable alone produces a sunflower. Thus all effective variables are binary. Each is seen somewhere, so the global observation is injective and the family has 2^m rows.

Theorem A and the fact that only diagonal triples are admissible give 2m log 2 <= rank(A) log 4, hence m<=rank(A)<=w and

    |F| <= 2^w.

There is also a simpler deterministic witness when m>w. Any nonzero real dependence among the incidence columns has both positive and negative coefficients, since the columns are nonzero and nonnegative. The union of supports of its positive columns equals the union for its negative columns. Starting from a fixed binary latent row, flip the positive-column variables to make a second row and the negative-column variables to make a third. Each observed coordinate contains neither flip group or both; therefore its three values are all equal or all distinct. The three rows are distinct.

The rank condition is only necessary for sunflower-freeness; it is not sufficient. For example, three latent bits observed in their three two-bit pairs have a full-rank incidence matrix yet contain sunflowers.

## 6. A precise barrier to acquiring this representation by a large subfamily

For two observed coordinates, split latent variables into those seen only on the left, only on the right, and on both. A full-product model with injective recodings is exactly a bipartite graph whose nonempty components are vertex-disjoint complete bipartite graphs: shared latent values index components, and private values index their two sides.

Take the point-line incidence graph of a finite projective plane of order q. It has v=q^2+q+1 vertices on each side and v(q+1) edges, and is C4-free. Every complete bipartite subgraph is therefore a star (including a single edge). Any vertex-disjoint union of such subgraphs has at most 2v edges, since a star's edge count is smaller than its vertex count and at most 2v total vertices are available. Thus a subfamily with the required two-coordinate representation retains at most

    2/(q+1)

of all rows. This tends to zero at fixed observed rank two.

Accordingly, a universal constant^{-w} retained-mass acquisition theorem for this exact class is false on arbitrary families. The incidence graph has many sunflowers; this does not refute acquisition specifically on sunflower-free families, the coupling goal for arbitrary families, or any exponential sunflower bound. It does show why the supplied representation must not be treated as a routine preprocessing step.

## 7. Boundaries of extension

Injectivity is essential in the proof: a noninjective recoding may turn three distinct latent subtuples into exactly two equal observed symbols. Arbitrary linear maps over F_2 are therefore outside the theorem. For an additive code specified by maps L_i:F_2^m -> F_2^{r_i}, the corresponding unresolved gate is to find a two-dimensional W on which every L_i has rank zero or two, never one. Equivalently, u,v,u+v must have the same block support. The real/complex kernel proof above does not establish that finite-field assertion.

Neither bounded-ambiguity acquisition for general rows nor a constant-cost reduction of arbitrary additive maps to coordinate projections is proved here. The positive primitive is useful evidence, but these are necessary missing steps before claiming a general mechanism.
