# A supplied mixed-alphabet extension of the additive coupling

Date: 2026-10-10. Natural logarithms throughout.

## 1. Input class and status

Let X be uniform on F_2^m. Independently let Z_j be uniform on explicitly supplied finite alphabets A_j. For observed coordinates i=1,...,w, the input supplies

* binary linear maps L_i on X;
* subsets S_i of the latent alphabet indices;
* injective, evaluable recodings h_i of the complete tuples (L_i X, (Z_j)_{j in S_i}).

The observed row is

    Y_i = h_i(L_i X, (Z_j)_{j in S_i}).

The support is the image of the **full** independent latent product. The statement below does not hold merely from pairwise independence or from partial product support. The recodings must be injective on their realized tuple domains. The representation is input, not an oracle assumed obtainable from arbitrary rows.

This is a closure construction using the additive result in `../additive_projection_gate_20261010/structural_worker.md` and its counting/sampling extension, together with the selected-latent-variable argument in KERNEL_SECTOR_PRIMITIVE.md. The binary-only combination is just another additive binary code and is not an enlarged class. Arbitrary nonbinary alphabet cardinalities do enlarge that supplied input class. No separate novelty claim is made for this closure operation.

## 2. Coupling theorem

There is a sunflower-supported coupling Q of three copies of the observed row law P satisfying

    Q(y_1,y_2,y_3) <= 16^w P(y_1) P(y_2) P(y_3).    (1)

Consequently every Renyi divergence order, including KL and infinity, is at most w log 16.

To construct it, discard one-point latent variables and absorb two-point latent variables into the binary vector X. Let t be the number of observed coordinates that contain a latent variable of alphabet size at least three. For each of those coordinates choose one such variable, and let J be the union of the choices; |J|<=t.

For each j in J, sample a uniform ordered triple of distinct alphabet elements. Its three marginals are uniform and its likelihood ratio against three independent uniform values is

    |A_j|^2 / [(|A_j|-1)(|A_j|-2)] <= 9/2.

Every one of the t covered observed tuples is now all distinct, regardless of all other latent values. Every nonselected nonbinary variable can therefore be sampled independently in the three replicas.

There remain k=w-t coordinates. Their observed tuples depend only on the binary vector by linear maps. Apply the additive difference coupling to these k maps. Any common kernel can be quotiented out, or equivalently left as independent unused binary directions. The additive theorem and the good-plane count give a coupling of uniform binary replicas with pointwise density at most 16^k, under which every remaining observed block is all equal or all distinct.

For clarity, this additive coupling can be realized by sampling independent uniform binary differences u,v, conditioned on

    for each remaining i, (L_i u,L_i v) is (0,0)
    or consists of two distinct nonzero values,

then taking an independent uniform base a and outputting a,a+u,a+v. Its conditioning event has probability at least 16^(-k). Translation by the independent base makes each replica uniform. The three replicas recover a,u,v, so the nonzero density is exactly the reciprocal of that acceptance probability. The quotient version proves the same claim when the maps have a nontrivial joint kernel.

Independence between the binary and nonbinary parts gives total latent density at most

    (9/2)^{|J|} 16^k <= 16^w.

Injective recoding preserves all-equal/all-distinct tuples. Pushing forward the pointwise likelihood bound proves (1), even if some latent variables are globally unobserved.

## 3. Access and computational cost

Required input is the explicit binary matrices, explicit latent alphabet samplers/encodings, the subsets S_i, and native evaluation procedures for h_i. The algorithm does not list the exponentially large observed family.

Uniform ordered distinct triples from an alphabet of size q are obtainable by sampling three distinct indices; standard exact integer sampling has expected polynomial bit cost in log q. This presumes those indices can be converted into the supplied alphabet elements at the stated input evaluation cost.

The binary part has an exact rejection sampler with expected at most 16^k trials, each using random binary vectors and matrix-vector products. Thus it is fixed-parameter exponential in the observed width and polynomial in the explicit matrix input size, rather than polynomial in w. The additive worker also supplies a 5^k-term exact inclusion-exclusion/prefix-count sampler; its own record gives the arithmetic and bit-complexity details. No polynomial-in-width general additive sampler is asserted here. The final recoding evaluation and output-writing costs are additional explicit costs.

## 4. Unresolved global step

The construction relies on a native supplied representation and full latent support. It does not yield a representation-acquisition algorithm for arbitrary set families, and the fixed-width projective-plane obstruction rejects the simplest large-subfamily or low-information-mixture acquisition versions. The global three-petal logarithmic-loss barrier remains unresolved by this investigation.

