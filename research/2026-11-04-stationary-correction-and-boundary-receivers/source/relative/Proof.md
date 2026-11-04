# Uniform response learning and stable composition in ferromagnetic environments

2026-11-04. Status: scoped mathematical construction; independent review is recorded separately in AUDIT.md. No priority, general-inference, or transformative-consequence claim.

## 1. Missing operation and precise scope

Ordinary TV accuracy of an isolated block does not control relative partition errors or its response after rare conditioning. Here we prove a stronger statement for a specific environment cone: nonnegative external weights with nonnegative Fourier coefficients. It includes arbitrary-strength ferromagnetic couplings, consistent nonnegative fields, and hard equality constraints. For product boundary fields we give a complete polynomial-time response learner and sampler from passive data. For general environments we prove a composition/error certificate, NOT an unconditional efficient contraction algorithm.

Let P=p_C be a distribution on k ordered spins, with all odd moments zero and all even moments Pf(C_S). Assume additionally that every even moment is nonnegative. These properties hold for free-boundary, zero-field ferromagnetic planar Ising networks, when the observed spins occur in cyclic order on a single face. The hidden bulk graph and its size need not be known.

We receive iid full-boundary samples from this ISOLATED zero-field distribution, not samples of the block embedded in an unknown environment. Correct ordering, equilibrium sampling, and the model promise are assumptions, not conclusions.

For any antisymmetric A define the signed mass
p_A(x)=2^(-k) sum_(S even) Pf(A_S) x_S,
where x_S=product_(i in S)x_i and Pf(empty)=1. It has total mass one. The empirical pair matrix A=C+Delta need not describe a physical model. Set D=sum_(i<j)|Delta_ij|.

An admitted environment weight W is a nonnegative function on the boundary with Fourier expansion
W(x)=sum_S w_S x_S, with every w_S>=0.
Assume Z=E_P W>0. W need not factor across sites and need not be planar.

## 2. Derivative identity

For a matching M of r disjoint index pairs, let U be its endpoints. Differentiating the Pfaffian expansion gives
partial_M p_C(x)=sigma_M 2^(-2r) x_U p_(C_(U complement))(chi x),
where sigma_M is the crossing sign of the selected pairs and chi_l=(-1)^(number of selected arcs whose interiors contain l). A mixed derivative whose selected pairs share an endpoint is zero.

Proof. In each Pfaffian matching expansion, differentiation retains exactly the terms containing M. Crossings among selected pairs contribute sigma_M. Crossings of a remaining pair with a selected arc occur when exactly one of its endpoints lies inside that arc, giving the product of the indicated chi signs over remaining endpoints. The remaining Fourier expansion is the spin-flipped marginal on the unselected coordinates. This proves the identity. Its remaining marginal is a genuine nonnegative law. In particular ||partial_M p_C||_1=1.

## 3. Weighted derivative domination

For every selected matching M,
sum_x W(x) |partial_M p_C(x)| <= Z.

Proof. The absolute derivative is the product of a uniform law on U and the spin-flipped true marginal on its complement. Averaging W over the uniform U coordinates deletes every Fourier monomial meeting U. Its expectation is therefore
sum_(S disjoint U) w_S chi_S E_P x_S.
Odd moments vanish. All remaining true even moments and w_S are nonnegative. Dropping the signs chi_S and then restoring the missing nonnegative terms bounds the expression by
sum_S w_S E_P x_S=Z.
The left side is nonnegative because W>=0. This argument uses neither independence of boundary spins nor a lower bound on probabilities of individual boundary assignments. QED.

## 4. Relative stability, signed normalization and sampling repair

Exact multilinear Taylor expansion and the derivative bound give
sum_x W(x)|p_A(x)-P(x)| <= Z [exp(D)-1].
Indeed the expansion is indexed by nonempty matchings M, each contributing at most Z product_(e in M)|Delta_e|. Their sum is at most Z(product_e(1+|Delta_e|)-1).

Write eta=exp(D)-1 and Z_A=sum_x W(x)p_A(x). Then
|Z_A/Z-1|<=eta.
If eta<1, Z_A>0 and the normalized signed law r_A(x)=W(x)p_A(x)/Z_A satisfies
||r_A-P_W||_1 <= 2 eta/(1-eta),
where P_W(x)=W(x)P(x)/Z. This follows by adding and subtracting W P/Z_A and using Z_A>=Z(1-eta).

If the signed prefix masses of r_A can be evaluated, it can be converted to a true sampled law Q_W by taking positive parts of the two child masses and normalizing at every prefix. Its error obeys
TV(Q_W,P_W)<=eta/(1-eta).

For completeness, the signed-prefix repair does not assume positivity of r_A. Its root has mass one. Every reached prefix has positive signed mass, so the sum of its positive child masses is positive. Each clipping step only reduces positive flow relative to the signed child/parent ratio; telescoping shows 0<=Q_W<=max(r_A,0) pointwise. Since P_W>=0, (Q_W-P_W)_+ <= (r_A-P_W)_+. Both differences have total mass zero, yielding TV(Q_W,P_W)<=||r_A-P_W||_1/2.

The certificate is uniform over ALL admitted W simultaneously. A good pair-estimation event therefore permits later adaptive selection of the external environment without another statistical union bound. Efficient computation still depends on the representation of W, as distinguished below.

## 5. Which physical environments are covered

A ferromagnetic edge factor can be written as a positive scalar times (1+a x_i x_j), with 0<=a<=1. A nonnegative field similarly gives a positive scalar times (1+t x_i), 0<=t<=1. Products of such factors have nonnegative Fourier coefficients: multiplication combines monomials by symmetric difference, preserving coefficient nonnegativity. Summing hidden environment spins deletes monomials containing those spins and multiplies surviving coefficients by a positive power of two. Thus an arbitrary ferromagnetic environment with nonnegative fields induces an admitted W, regardless of topology, strength, or number of hidden spins. Hard equality is represented by (1+x_i x_j)/2 and is also included.

All fields of the opposite common sign can be handled by a global spin flip of the zero-field block. Arbitrary opposing fields are NOT included.

Nonnegativity of all block spin correlations follows directly from the standard high-temperature expansion of a zero-field ferromagnet: the numerator for a spin-product moment is a sum of nonnegative subgraph weights with the appropriate odd-degree boundary, divided by a positive partition sum. This is established ferromagnetic correlation positivity, not a new correlation inequality.

## 6. Complete product-field response algorithm

For rational t_i in [0,1], let W_t(x)=product_i(1+t_i x_i). This allows t_i=1, which fixes spin i to +1 after normalization. Define
F_A(z)=sum_(S even) Pf(A_S) product_(i in S)z_i.
It is polynomial-time computable by ONE Pfaffian: pad A with a zero row/column if k is odd, use dummy z=1, let J_ij=1 for i<j, and set D_z=diag((-1)^i z_i) in one-based indexing. Then
F_A(z)=Pf(J-D_z A D_z).
The identity follows by the Pfaffian minor expansion and Pf(J_S)=1 for every even S. It holds for arbitrary real z, including mixed signs and zeros.

The response normalization estimate is Z_A=F_A(t). For a prefix a=(a_1,...,a_j), its UNNORMALIZED signed weighted mass is
S_A(a)=2^(-j) [product_(i<=j)(1+t_i a_i)] F_A(a_1,...,a_j,t_(j+1),...,t_k).
This follows from 1[X_i=a_i]=(1+a_i X_i)/2 and evaluating the already fixed field factors. Divide by the positive root F_A(t) if normalized masses are desired; this division cancels in each two-child sampling ratio.

Compute both children, clip their masses below at zero and sample proportionally. Under the good estimation event the root is positive. Every reached prefix is positive, so the conditional denominator is nonzero. Exact rational arithmetic handles t_i=1 and forbidden children with zero mass without taking limits.

For ordinary positive boundary activities lambda_i>=1, use t_i=(lambda_i-1)/(lambda_i+1). The partition ratio for product_i lambda_i^[x_i=+1] is product_i((lambda_i+1)/2) times F_C(t), with the known positive prefactor included. Bit costs charge the rational activity encodings. No claim is made that explicitly writing exp(h) has cost polynomial in the binary encoding of an arbitrarily huge h; the rational activity or rational t encoding is the contract.

### Rare same-sign evidence

For a subset H of r spins, set t_i=1 on H and zero elsewhere. Then F_C(t)=2^r P[X_i=+1 for every i in H]. The proposed estimate gives RELATIVE accuracy eta for this event probability, and the repaired sampler approximates its conditional law, without a 1/P[event] sample factor. Such events can have probability 2^-r, for example under independent unbiased spins. All-minus evidence follows by global spin flip. Mixed-sign evidence is excluded.

## 7. Samples and exact bit complexity

For k>=2 let m=binom(k,2), 0<epsilon<=1 and 0<alpha<1. Choose h=epsilon/(32m), and estimate all pair moments by empirical averages from
N >= (2/h^2) log(2m/alpha)
independent full-boundary snapshots. Hoeffding and a union bound imply simultaneous pair error at most h with probability at least 1-alpha. Hence D<=epsilon/32 and eta<=epsilon/16. The normalization relative error is at most epsilon/16; the ideal repaired sampler TV error eta/(1-eta) is at most epsilon/15. These guarantees hold uniformly for every rational t in [0,1]^k and every admitted W for the abstract stability certificate.

Thus N=O(k^4 epsilon^-2 log(k/alpha)). The k=0,1 cases are trivial because the isolated law is respectively a point mass or the uniform single spin. The guarantee is per learned distribution, not a promise that arbitrarily many outputs jointly remain epsilon-close without the usual product-law accumulation.

Let B be the maximum bit length of the rational query t_i. Empirical A entries have denominator N. Weighted Pfaffian prefix masses have numerator and denominator bit lengths polynomial in k, log N and B, by the degree bound and determinant/Pfaffian coefficient height bounds. Fraction-free or exact rational Pfaffian elimination is polynomial bit time, with pivoting and zero-pivot handling. Computing two prefixes at each step uses O(k^4) rational arithmetic operations conservatively. It does not enumerate 2^k spin assignments.

Handle conditional probabilities 0 and 1 deterministically. For a nontrivial reduced rational coin a/b, use unbiased-bit rejection with success probability greater than 1/2 per trial. Cap at R=ceil(log2(4k/epsilon))+1 trials; on cap choose a fixed child with positive signed weighted mass. This keeps all subsequent denominators valid and changes the distribution by at most epsilon/4 in TV, by a union bound. Its worst-case bit runtime is polynomial. The actual capped law has an exact evaluator: with f=(1-b/2^ceil(log2 b))^R its bit probability is (1-f)a/b+f times the indicator for the designated fallback bit. Multiplying the k transition probabilities remains polynomial bit time.

If the training event fails, the algorithm may detect a nonpositive root and return a fixed fallback distribution/value. Accuracy is claimed only on the stated 1-alpha event. No physical sampling/decorrelation cost is hidden in the iid oracle assumption.

## 8. Multiple independently learned blocks: a genuine compositional certificate

Let P_b=p_(C_b) be independent isolated boundary laws of several blocks, each satisfying the Pfaffian and nonnegative-moment assumptions. Their boundary variables are initially distinct. Let W on their union be any admitted environment weight, possibly introducing ferromagnetic connections, hard identifications or additional integrated environment spins. Write
Z=sum_x W(x) product_b P_b(x_b)>0.
For noisy matrices A_b=C_b+Delta_b, put D_total=sum_b sum_(i<j)|Delta_(b,ij)| and Q_signed(x)=product_b p_(A_b)(x_b). Then
sum_x W(x)|Q_signed(x)-product_b P_b(x_b)| <= Z [exp(D_total)-1].
Consequently the same relative-normalization and normalized signed-law bounds hold with D_total.

Proof. Expand jointly in all pair variables of all blocks. A nonzero mixed derivative selects a matching inside each block. Its absolute value is a product of uniform laws on the selected endpoints and spin-flipped true marginal laws elsewhere. Expand W in its nonnegative Fourier coefficients. Terms meeting removed endpoints vanish; odd intersections with a block vanish; every surviving product of true block moments is nonnegative. Discarding flip signs and restoring removed nonnegative terms bounds the weighted derivative norm by Z. Summing the joint Taylor expansion gives the claimed exponential bound. This proof does not assume positivity of any INTERMEDIATE or reconstructed block law. QED.

The error budget is additive across blocks before exponentiation. Simultaneous empirical confidence follows by a union bound over all estimated block pairs. This is a stable contraction certificate in the ferromagnetic environment cone. It is not yet a uniform efficient algorithm for arbitrary compactly described W: evaluating its signed prefix contractions can itself be difficult. Product fields are completely implemented above; a separately justified tractable contraction receiver can use the same certificate. No general nonplanar signed contraction or arbitrary-environment sampling algorithm is inferred.

## 9. Why the restriction matters

Take two spins with zero-field ferromagnetic correlation c=1-rho, 0<rho<1, and W=(1+x_1)(1-x_2). Then Z=1-c=rho. Changing c to c-delta changes Z by delta, so the relative error is delta/rho, unbounded as rho tends to zero at fixed delta. This W has a negative even Fourier coefficient and lies outside the admitted cone. It proves that the same unconditional uniform relative bound cannot hold for arbitrary opposing-field environments. It does not prove impossibility of inference for any individual excluded model.

## 10. Primary comparison and consequence boundary

Boundary Pfaffian formulas, exact inversion and exact Pfaffian response evaluation are established: Groeneveld, Boel and Kasteleyn, Physica A 93 (1978), https://www.sciencedirect.com/science/article/pii/0378437178902145 ; Galashin and Pylyavskyy, Duke Mathematical Journal 169 (2020), https://arxiv.org/abs/1807.03282 . Ferromagnetic correlation positivity is also classical; it was proved directly above from the nonnegative expansion rather than treated as a new mechanism.

Known Pfaffian samplers and matchgate algorithms remain the appropriate specified-model comparators: Edelman, Jeong and Schaub (2026), https://arxiv.org/abs/2605.01202 ; Cai and Gorenstein, *Matchgates Revisited*, Theory of Computing 10 (2014), https://www.theoryofcomputing.org/articles/v010a007/v010a007.pdf . The contribution claimed by this proof contract is not those algebraic operations. It is the uniform, noise-tolerant RELATIVE interface guarantee and signed-law repair, with a complete finite-sample product-field response learner. Priority for that assembled guarantee has not been established.

This operation strictly strengthens isolated TV learning: it controls an explicit class of arbitrarily strong interventions and simultaneous ferromagnetic compositions, including exponentially rare same-sign evidence. Nevertheless, it does not certify the structural promise, supply iid physical data, reconstruct bulk physics, compute absolute block free energies, solve arbitrary compact-environment contractions, or establish a practical/civilisation-scale advantage. Absolute composite partition values additionally require the isolated block normalization factors, which passive normalized samples do not identify. The learned ratio is relative to the product of those unknown isolated normalizations.


### Stronger specified-model comparators

Jerrum and Sinclair (1993), https://doi.org/10.1137/0222066 , already give polynomial randomized approximation for specified ferromagnetic Ising partition functions. The present data oracle is an unknown hidden bulk observed through iid boundary snapshots. The multiblock certificate is not a new general ferromagnetic counting algorithm.

Clusel and Fortin, *1D action and partition function for the 2D Ising model with boundary magnetic field*, Journal of Physics A 38 (2005), 2849–2871, https://arxiv.org/abs/cond-mat/0408657 and https://doi.org/10.1088/0305-4470/38/13/003 , explicitly develop exact boundary-field partition functions. Thus boundary-field Pfaffian response evaluation itself is established, including contexts more general than the consistent-field noise guarantee here.

Goldberg and Jerrum, *Approximating Pairwise Correlations in the Ising Model*, ACM Transactions on Computation Theory 11 (2019), Article 23, https://arxiv.org/abs/1810.05830 and https://doi.org/10.1145/3337785 , give multiplicative covariance approximation for specified ferromagnets even when the covariance is exponentially small. Relative accuracy for an exponentially small observable alone is therefore not a novelty claim.

The narrower interface established here is uniform relative prediction and response sampling from a single noisy boundary-data summary, with no specified hidden graph, and a multiblock perturbation certificate for a stated environment cone. An ordinary algorithm given the same empirical correlations may be able to exploit the same identities and bounds. No comparison has established that this construction beats the strongest such adapted method.
