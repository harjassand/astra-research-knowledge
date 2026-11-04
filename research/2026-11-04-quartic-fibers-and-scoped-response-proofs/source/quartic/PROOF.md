# Exact Gaussian-fiber discovery in bounded-below quartic potentials

Status: exact algebraic theorem with independent mathematical audit; not a novelty claim or a uniform polynomial-bit algorithm claim. The algebraic construction is exact. Polynomial arithmetic-operation complexity is established below; a uniform polynomial bound on intermediate rational bit lengths for unbounded depth is NOT established. Fixed-depth bit complexity and a specifically rounded finite-bit sampling contract are given in sections 4.1–4.2.

## 1. The proposed operation and its scope

Input is the rational coefficient list of a polynomial V:R^n→R of total degree at most four, not a supplied generative map or a supplied sum-of-squares decomposition. The intended output, when the construction succeeds, is an exact sequence of constant-curvature Gaussian integrations, a normalizing integral, and a compositional Gaussian transport. A full successful sequence itself certifies boundedness below and integrability, without separately solving general polynomial positivity.

This is a discovery operation for a restricted integrable family. It is not general nonconvex optimization, generic quartic integration, observational causal identification, or robust recovery from finite noisy data.

## 2. Exact linear discovery theorem

Let V be a real polynomial of degree at most four bounded below on all of R^n. Write V_4 for its homogeneous degree-four component, taking V_4=0 if absent. Define

E(V)={v : D_v^2 V is constant}.

Then

E(V)={v : D_v V_4=0}.

In particular E(V) is a vector space computable by linear algebra from the cubic coefficient vectors of the n partial derivatives of V_4.

Proof of necessity. For v∈E(V), on every line x+tv the polynomial V is at most quadratic in t. Its top homogeneous form V_4 is nonnegative. D_v²V_4=0, so V_4 is affine in t along every such line; a globally nonnegative affine polynomial on the real line is constant. Thus D_vV_4=0.

Proof of sufficiency. Choose any linear coordinates (t,y) with the t-directions spanning S={v:D_vV_4=0}. The quartic part is independent of t. Consequently V has t-degree at most three. For each fixed y, boundedness below eliminates a nonzero homogeneous cubic term in t, so V has t-degree at most two. Write V=tᵀB(y)t+2r(y)ᵀt+s(y). Because no quartic term contains t, B(y) is affine in y. B(y) is positive semidefinite for every y, since otherwise V is unbounded below along a t-ray. An affine symmetric matrix pencil positive semidefinite on all of R^(n−dim S) is constant: for any u, uᵀB(y)u is a globally nonnegative affine function of y, hence constant; polarize in u. Thus B(y)=Q is constant, proving the claim. Necessarily deg r≤2 and deg s≤4.

The argument applies to globally bounded-below, not merely locally positive, potentials. No promise of convexity is used.

## 3. Gaussian elimination and exact certificate

Let columns of K form a rational basis of E(V), complete them with columns of B to an invertible rational matrix T=[K B], and write x=T(t,y). Then

V(T(t,y))=tᵀQ t+2r(y)ᵀt+s(y).

If exp(−V) is integrable over R^n, Q is positive definite. Indeed Q is PSD by the preceding theorem. If u∈ker Q is nonzero, boundedness below forces uᵀr(y)=0 for every y. The potential is then constant along a nonzero full-space direction and its exponential cannot have finite integral.

Define

h(y)=Q^(−1)r(y),
R(y)=s(y)−r(y)ᵀQ^(−1)r(y).

Then V(T(t,y))=(t+h(y))ᵀQ(t+h(y))+R(y), deg R≤4, and R is bounded below because it is the minimum over t. The exact integration identity is

∫ exp(−V(x)) dx = |det T| π^(dim E/2)/sqrt(det Q) ∫ exp(−R(y)) dy.

Conditionally on y, t is Gaussian with mean −h(y) and covariance (2Q)^(−1). Thus recursive success gives an exact generative representation in terms of independent block Gaussians. Implementing Gaussian real numbers and returning finite-bit samples require a separately specified representation/error model.

The executable recognizer need not assume positivity. At each step it computes the proposed kernel from V_4, substitutes coordinates, and explicitly checks the displayed quadratic-in-t identity, constant positive-definite Q, and the residual. Failure is reported rather than interpreted as a positivity verdict. If it reaches a constant c, the identities certify V=c+sum of positive quadratic block forms in an invertible triangular polynomial coordinate change. This proves boundedness below and integrability for that accepted instance.

## 4. Arithmetic complexity and unresolved bit issue

Dense quartics in n variables contain O(n^4) coefficients. At most n stages occur. Derivatives, nullspaces, rational coordinate changes of fixed degree, positive-definiteness tests by exact LDL elimination, polynomial multiplication of bounded degree and square completion use a polynomial number of rational arithmetic operations. All transformations are stored compositionally; the expanded inverse transport can have exponentially large degree and is not expanded.

This is NOT yet a polynomial Turing-time theorem. Each rational operation can increase the bit lengths of intermediate coefficients. The algorithm runs in polynomial time in n and the largest intermediate numerator/denominator bit length H encountered, with an explicit polynomial-size list of polynomial identities at that height. No proof here bounds H polynomially in the original coefficient encoding. Exact rational operations must not be treated as unit-cost in a claimed bit-complexity result.

Output magnitude is an independent issue. For

V_n(x)=sum_(i<n)(x_i−x_(i+1)^2)^2+(x_n−2)^2,

the minimizing point has x_n=2 and x_1=2^(2^(n−1)). A conventional explicit rational approximation of that coordinate to fixed absolute error already requires exponentially many bits. This minimizer statement alone is not a sampling lower bound. A stronger example is W_n(x)=1/2[(x_n−4)^2+sum_(i<n)(x_i−x_(i+1)^2)^2]. Its exact sampler has X_n=4+Z_n and X_i=X_(i+1)^2+Z_i with independent standard Gaussians. With probability at least 0.49, X_n≥4 and successively every Z_i≥−a²/2 whenever the preceding coordinate is at least a. Starting a_0=4, a_(j+1)=a_j²/2 gives a_j=2^(2^j+1). The failure probabilities are bounded by a summable sequence beginning at Pr[Z<−8]<10^(−14), so X_1≥2^(2^(n−1)+1) with constant probability. Therefore explicit fixed-point output at constant absolute resolution requires exponentially many bits with constant probability. This does not rule out a succinct circuit or floating relative-error output. The original V_n has partition function π^(n/2); the standard-normal version W_n has partition function (2π)^(n/2). Both compositional samplers have only n Gaussian/shear stages. A succinct arithmetic-circuit or floating-point representation changes the output contract and must be stated, not silently substituted.

### 4.1 Fixed-depth bit-complexity corollary

For each fixed d, the exact compiler restricted to runs with at most d nonempty maximal-block stages has polynomial Turing complexity in the dense rational input size. The polynomial degree may depend on d; this is not a uniform polynomial bound for d up to n.

Use rational nullspace bases and inverses obtained by fraction-free elimination or ratios of minors, not arbitrary long arithmetic circuits. If current coefficients have numerator and denominator bit length at most H, clearing the O(n^4) coefficient denominators costs O(n^4 H) bits. Each relevant minor has size at most n, so its determinant height is polynomial in n and H by the determinant expansion bound. A degree-four linear substitution uses products of at most four basis entries; matrix inversion uses bounded-size determinant ratios; square completion uses quadratic polynomials and one inverse matrix. Directly taking common denominators over the polynomially many coefficients shows that, for absolute constants C,c,

H_next+1 ≤ C(n+1)^c(H+log(n+1)+1).

The same bound covers stored coordinate and curvature matrices. Induction yields H_max ≤ (C(n+1)^c)^d(H_input+log(n+1)+1). Polynomially many integer operations on these heights give a bound (n+1)^(O(d)) times a polynomial in input height, with fixed universal arithmetic exponents. Hence bounded-depth full recovery has a genuine exact bit-complexity guarantee.

### 4.2 A finite-bit sampler with an explicit output contract

The target here is the distribution of coordinatewise nearest-grid rounding of X to spacing Delta=2^(−p), where p is a nonnegative integer. It is not the continuous law in total variation. Given a successful compiled certificate of depth d and maximum rational height H, there is a worst-case finite-bit sampler whose rounded output has total-variation error at most epsilon, with complexity polynomial in n, p, H, log(1/epsilon), and 2^d. In particular fixed depth gives polynomial complexity in the original dense input size, p and log(1/epsilon). This is an output-sensitive consequence of the certificate, not an extension to unbounded-depth ordinary outputs.

Proof. Write the compiled transport as X=F(G), with n independent standard Gaussian inputs. Rational LDL factorizations of each Q implement the required Gaussian covariance using rational matrices and square roots of positive rationals. On a latent cube ||g||_infinity≤G_0+1, interval evaluation of the degree-two block shears supplies bounds R≥1 for ||F(g)||_infinity and L≥1 for its infinity-norm Lipschitz constant. The logarithms of R and L are bounded by 2^d times a polynomial in n,H,log(G_0+2): each block obeys a magnitude bound B_next≤2^poly(n,H)(1+B²+G_0), and differentiation obeys the corresponding product bound. Positive rational square roots and all finite operations can be enclosed by rational intervals to any requested precision using polynomial bit work. The same operation bounds ensure that evaluating F to a chosen absolute coordinate error requires only polynomial work in the listed quantities and the requested precision.

Choose integer G_0=ceil(log_2(64n/epsilon))+1. A Gaussian union bound makes the probability outside this cube less than epsilon/16. The density of X is globally at most

M = e^(−c)/Z = product sqrt(det Q) / [pi^(n/2) product |det T|].

A rational upper bound M_0≥max(1,M) with log M_0 polynomial in n,H follows from determinant numerator/denominator bounds (using pi≥1). Set N_grid=ceil((2R+2)/Delta)+2. Inside [-R−1,R+1]^n, the union of delta-neighborhoods of all rounding hyperplanes has volume at most

2 delta n N_grid (2R+2)^(n−1).

Choose a positive rational delta≤min(1/4,Delta/8) making M_0 times that volume at most epsilon/16. Its reciprocal has bit length polynomial in n,H,p,log(1/epsilon),log R. Choose latent approximation tolerance eta≤delta/(4L). Couple the finite-precision Gaussian generation to exact Gaussian inputs within eta in infinity norm with failure probability at most epsilon/8, and evaluate F with absolute coordinate error at most delta/2. Except on the tail, generation-failure and rounding-boundary events, both outputs round to exactly the same grid point. The coupling inequality therefore gives TV error below epsilon (with substantial slack).

For completeness, the required Gaussian coupling can be implemented without an infinite-time primitive. Generate uniform proposals on [-G_0,G_0] and accept with probability exp(−y²/2). Acceptance is at least 1/(2G_0). Cap each coordinate at B=ceil(2G_0 log(64n/epsilon)) proposals; total cap failure is at most epsilon/64. Generate uniform proposal and acceptance variables to b dyadic bits. Since |d exp(−y²/2)/dy|≤1, coupling these variables to exact uniforms changes any acceptance decision with probability at most O((G_0+1)2^(−b)) per proposal, while proposal locations differ by at most 2G_0 2^(−b). Choose b to make the union of decision discrepancies at most epsilon/64 and location error at most eta. Evaluate the exponential threshold within 2^(−b) using range-reduced Taylor series or another rigorously rounded elementary-function algorithm. The truncated-normal tail contributes at most epsilon/16. The caps give worst-case polynomial runtime; deterministic zero fallback is used only on the charged failure event. All these precision choices have logarithmic dependence on 1/eta and 1/epsilon.

The symbolic normalizer remains the exact expression from section 3. A log-normalizer can be approximated to stated absolute precision. Writing an ordinary positional rational approximation of an exponentially tiny Z is a different output contract and is not asserted to have polynomial length.

## 5. Completeness under an explicit lowering-flag promise

Suppose the raw potential admits an unknown representation

V(x)=c+||q_0+Lx+L b(x,x)||²,

where L:R^n→R^n is invertible, b:R^n×R^n→R^n is symmetric bilinear, and a full flag 0=F_0⊂F_1⊂...⊂F_n=R^n satisfies

b(F_j,R^n)⊆F_(j−1).

None of L, b, q_0, or the flag is supplied. This class includes triangular quadratic Gaussian residual maps, their invertible linear input changes, and arbitrary invertible output changes absorbed into L. The flag gives a triangular polynomial automorphism x↦x+b(x,x), and therefore V is bounded below and integrable.

Let A={v:b(v,w)=0 for every w}. The quartic part is V_4(x)=||L b(x,x)||², and its translation kernel equals A. One inclusion is immediate. For the other, if the sum of real polynomial squares is constant along every v-line, every component L b(x+tv,x+tv) must itself be constant in t: otherwise the highest nonzero t-degree among the components contributes a positive coefficient at twice that degree to the sum. Differentiating gives b(x,v)=0 for all x.

A is an annihilator ideal and contains F_1. Choose x=Kt+By, where im K=A and B is any complement. With P the orthogonal projection onto (LA)^perp, Gaussian square completion yields

V_red(y)=c+||P(q_0+LB y+L b(By,By))||².

The linear map M=PLB from the complementary input space to (LA)^perp is invertible. Indeed PLB y=0 implies By∈A; complementarity gives y=0, and the dimensions agree. Identify (LA)^perp isometrically with R^(n−dim A) for this existence argument. Then the normalized quadratic map is

b_red(y,z)=M^(−1)PL b(By,Bz).

It is exactly the product induced by b on the quotient R^n/A. The projector PL kills LA and b(A,R^n)=0, so this quotient description is independent of representatives. The images (F_j+A)/A form a lowering flag in the quotient. Their dimensions rise by at most one; deleting repeated images preserves the lowering property, because at the first index of a new image the product lands in the preceding distinct image.

Every nonzero quotient therefore has a nonzero annihilator. Induction proves that the raw-potential maximal-kernel algorithm succeeds until dimension zero, regardless of the rational complements chosen by the implementation. The isometric coordinates used to justify the induction need not be computed: the implementation works entirely with raw rational residual potentials and rational linear algebra.

This is completeness for the displayed invariant class, not a classification of all polynomial Gaussianizations. Strong nilpotency and linear triangularization of a supplied polynomial map are classical; the missing interface considered here is recovery directly from V.

## 6. Strongest current baselines and limitations

- Welch, Zhang, Uhler, Identifiability Guarantees for Causal Disentanglement from Purely Observational Data, NeurIPS 2024, arXiv:2410.23620. Their directionally nonlinear Gaussian causal model under linear mixing is recovered layerwise using constant directional Hessians; the practical direction search is a QCQP. This already supplies the conceptual causal-layer criterion. Our restricted algebraic proposal takes exact quartic coefficients, not noisy samples, and replaces that direction search by a linear kernel. It establishes no stronger causal identifiability. https://arxiv.org/abs/2410.23620
- Rolland et al., SCORE, ICML 2022, recovers nonlinear Gaussian causal order from score Hessians in observed coordinates. https://proceedings.mlr.press/v162/rolland22a.html
- van den Essen and Hubbers, Polynomial maps with strongly nilpotent Jacobian matrix and the Jacobian conjecture (1996), gives the classical equivalence between strong nilpotency and linear triangularizability for the supplied map. https://www.sciencedirect.com/science/article/pii/002437959500095X
- Hybrid Rosenbrock densities already have conditional Gaussian structure, exact normalizers and direct independent sampling when the representation is known: arXiv:1903.09556, DOI 10.1111/sjos.12532. This source was identified by the independent reviewer; exact scope is being checked.
- NICE additive-coupling normalizing flows already exploit known invertible triangular changes of variables: arXiv:1410.8516. Transport inversion and sampling after the map is known are not the proposed missing operation.

- Carlini, Reducing the number of variables of a polynomial (2005/06), arXiv:math/0507531, supplies the classical essential-variable reduction through first derivatives. The linear nullspace operation itself is not new; the proposed bridge is from that kernel for V_4 to exact Gaussian fibers of V and recursive compilation. https://arxiv.org/abs/math/0507531

The potential distinction is exact coefficient-to-transport recovery on this narrow quartic family. Novelty, uniform polynomial bit complexity, stability to coefficient error, data acquisition cost, and a real scientific workload advantage remain unestablished. No claim that this is a civilization-changing result is warranted.

## 7. Finite exact checks

The internal test_elimination.py checks twelve rational potentials of dimensions 2 through 5, generated from quadratic triangular residuals followed by integer unimodular coordinate mixing. Only the expanded raw potential is supplied to the elimination routine. Every stage checks the exact square-completion identity, constant positive-definite curvature and degree≤4 of the residual. All cases terminate at constant zero, and the product of determinant factors agrees exactly with the known Gaussian normalizer. These tests check implementation and examples, not the general completeness or bit-complexity proof. Code is not part of any proof-only deliverable.

## 8. Robustness boundary

For V_0=x²+(y−x²)² the compiler succeeds; for V_epsilon=V_0+epsilon y⁴ with any epsilon>0, the top form x⁴+epsilon y⁴ has zero translation kernel, so it stops immediately. Yet the normalized laws obey TV(p_0,p_epsilon)≤153 epsilon/16. Indeed under p_0, X,Z are independent N(0,1/2), Y=X²+Z, and E Y⁴=153/16. With w=exp(−epsilon Y⁴), a=E w, the identity p_0=a p_epsilon+(1−a)r for a probability law r gives TV≤1−a≤epsilon E Y⁴. Thus exact recognition is discontinuous even for arbitrarily close laws. Approximate transport recovery is a separate unsolved operation, not supplied by this exact result.
