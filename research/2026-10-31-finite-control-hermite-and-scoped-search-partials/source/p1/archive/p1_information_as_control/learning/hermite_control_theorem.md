# A polynomial sensing hierarchy with acquired coefficients and finite control

P1 continuation, 30 October 2026. This is an ordinary construction and proof, not historical-priority clearance. The input distribution and measurement primitives are explicit resources.

## Result and opening

Early information can choose a useful measurement from a nonlinear family with small control dimension, even when its coefficient covariance is isotropic in a much larger space. A concrete Gaussian polynomial family has all of the following properties:

* a two-round experiment uses r+1 scalar observations;
* every fixed q-dimensional linear experiment, including arbitrary mixtures of context and response coordinates, captures at most (p+1)q/M of the target variance;
* M=binom(r+p-1,p), so the separation grows polynomially with r for any fixed p>=2;
* all observations may have independent fixed-variance Gaussian noise: the same r+1 protocol matches the accuracy of observing every one of the r+M coordinates noisily;
* for cubic targets, a bounded 11r-bit control message retains essentially that accuracy;
* M unknown coefficients can be acquired from M function values in a declared feature family, and calibration error enters an exact risk formula;
* generating and applying the dense pattern costs O(M) arithmetic per deployment. There is no arithmetic speedup over reading all coordinates and directly evaluating the target.

The representation is a classical varying-coefficient model and the adaptive operation is conditional projection onto its coefficient vector. The candidate result is the combination of an explicit polynomial family, a lower bound for every mixed fixed linear experiment, finite control, and paid coefficient acquisition. Generic latent-structure discovery is not supplied.

## Family

Fix r>=1 and p>=1. Let A_p be the multi-indices a in N^r with |a|=p, and M=|A_p|=binom(r+p-1,p). Let

`phi_a(u)=prod_i He_{a_i}(u_i)/sqrt(prod_i a_i!)`,

where He_j are probabilists' Hermite polynomials. For standard Gaussian U in R^r, these degree-p features are orthonormal:

`E phi_a(U) phi_b(U)=1{a=b}`.

Independently let V be standard Gaussian in R^M. Given real coefficients c_a, define

`F_c(U,V)=M^(-1/2) sum_a c_a phi_a(U) V_a`.

Its mean is zero and its variance is

`sigma_c^2=M^(-1) sum_a c_a^2`.

When c_a=1 its variance is one and the coefficient vector C(U)=phi(U)/sqrt(M) has covariance I_M/M. It nevertheless lies on the image of an r-parameter polynomial map.

For p=2, M=r(r+1)/2 and the features are

`phi_ii(u)=(u_i^2-1)/sqrt(2)`,

`phi_ij(u)=u_i u_j`, for i<j.

The target has polynomial degree three and belongs purely to third Gaussian chaos. Its ordinary polynomial contains a linear subtraction in V. It is a quadratic form of U with an unknown random matrix supplied by V, together with its trace correction.

## Two-round exact recovery

Observe the r coordinates of U. Form `a(U)=c*phi(U)/sqrt(M)`, where * means coordinatewise product. If a is nonzero, observe the single unit-direction scalar `a(U)^T V/||a(U)||` and multiply by its known norm. If a=0 the output is already zero. Thus r+1 scalar linear observations suffice for exact recovery.

This is not a low-dimensional fixed ridge target. For the cubic family with all c_a nonzero, the only constant translation direction of F is zero. To see this, write such a direction as (h,k). The coefficients of each V_ii in its directional derivative imply h_i=0 for every i; the remaining derivative is sum_a c_a k_a phi_a(U), which vanishes identically only when k=0 by polynomial independence. Hence any fixed linear observation that determines F exactly must span all r+M input dimensions.

## Universal fixed-experiment lower bound

**Theorem.** Every fixed q-scalar linear experiment, with arbitrary directions mixing U and V and an arbitrary nonlinear estimator, has explained variance at most

`min(sigma_c^2, (p+1)||c||_infinity^2 q/M)`.

Its Bayes risk is therefore at least

`sigma_c^2-(p+1)||c||_infinity^2 q/M`.

A negative right side is replaced by zero. Independent randomization of the fixed design cannot improve this bound. For c=1, constant accuracy requires q=Omega(M), whereas the two-round experiment uses r+1 observations.

### Full proof, including arbitrary mixed observations

Let H=R^r direct-sum R^M be the Gaussian coordinate Hilbert space. Write I_d(T) for the degree-d Gaussian Wick polynomial with symmetric coefficient tensor T, normalized so

`E I_d(T)^2=d! ||T||_F^2`.

For each feature phi_a choose its symmetric order-p kernel A_a in the U subspace. Then

`I_p(A_a)=phi_a(U)`, and `<A_a,A_b>=1{a=b}/p!`.

Let e_a be the corresponding V coordinate, set d=p+1, and define the unsymmetrized tensor

`S=M^(-1/2) sum_a c_a A_a tensor e_a`,

and `T=Sym(S)`. Since U and V are orthogonal Gaussian subspaces, there are no Wick contractions between them, and `I_d(T)=F_c`. The d possible positions of the V factor have disjoint supports, so `d!||T||^2=sigma_c^2`.

The fixed observations determine an orthogonal projection P of rank at most q. Gaussian conditioning projects the Wick kernel in every slot:

`E[F_c | PX]=I_d(P^(tensor d) T)`.

Consequently the explained variance is `d!||P^(tensor d)T||^2`. Projection in every slot commutes with symmetrization, and symmetrization is an orthogonal projection. Hence

`d!||P^(tensor d)T||^2 <= d!||P^(tensor d)S||^2`

`<= d!||(I^(tensor p) tensor P)S||^2`

`=d/M sum_a c_a^2 ||P e_a||^2`

`<=d ||c||_infinity^2 rank(P)/M`.

The second inequality drops contractions on the p U slots. Kernel orthogonality gives the equality. This calculation does not assume that P respects the U/V split. Conditional expectation is the optimal squared-loss estimator, so the bound covers every nonlinear decoder.

The Gaussian Wick-conditioning identity can be checked without importing tensor machinery: condition the generating function `exp(t^T X-||t||^2/2)` on the linear observations and compare coefficients. This gives the projected Wick polynomial term by term.

## Every read noisy

Now every unit-direction observation has independent N(0,s) noise, with finite s>=0, and alpha=1/(1+s). First observe `Y=U+epsilon` and set `W=Y/sqrt(1+s)`. W is standard Gaussian. The Hermite conditional-mean identity is

`E[phi_a(U)|Y]=alpha^(p/2) phi_a(W)`.

Form the posterior coefficient vector

`a_post(Y)=alpha^(p/2) c*phi(W)/sqrt(M)`.

Take one noisy V observation in its normalized direction and return `alpha ||a_post|| Z`. The explained variance is exactly

`alpha E||a_post||^2=alpha^(p+1) sigma_c^2`.

Thus the risk is exactly `(1-alpha^(p+1))sigma_c^2`. This equals the Bayes risk of observing every coordinate of (U,V) once with the same noise variance: the target is pure chaos of degree p+1, so the full Gaussian channel attenuates its explained variance by alpha^(p+1).

### Fixed noisy comparator

Let the fixed sensing matrix L have q unit-norm rows. Put H=L^T L and `P=H(H+sI)^(-1)`. For s>0, P is the covariance of the posterior mean. The conditional Wick-kernel formula gives explained variance

`d! ||(P^(1/2))^(tensor d) T||^2`.

The same contraction argument bounds it by

`d/M sum_a c_a^2 e_a^T P e_a <= d||c||_infinity^2 tr(P)/M`.

The nonzero eigenvalues t_j of H, padded with zeros to q, sum to q. Concavity of t/(s+t) gives `tr(P)<=q/(1+s)=alpha q`. Therefore

`R_fixed,noisy(q)>=sigma_c^2-d||c||_infinity^2 alpha q/M`.

The bound covers repeated and nonorthogonal directions. It is a certified lower bound for the optimal fixed experiment, not a claim that its constant is sharp. No restriction s<=1 is required. At s=0 use the noiseless rank-projection proof.

## Finite control for the cubic family

For p=2, let Q_h,T act coordinatewise by rounding toward zero to a multiple of h and clipping magnitude to T, with T/h an integer. The message contains one of 2T/h+1 indices per coordinate and uses

`B=r ceil(log2(2T/h+1))`

bits. The actuator reconstructs Q(W), forms the M feature weights and their norm, and programs the dense unit-direction measurement. It uses O(M) arithmetic and O(M) model storage.

The feature difference has the exact identity

`||phi(u)-phi(v)||^2=(1/2)||uu^T-vv^T||_F^2`.

Since the quantizer shrinks each coordinate in magnitude, `||Q(u)||<=||u||`. With e=U-Q(U),

`||UU^T-Q(U)Q(U)^T||_F^2 <=4||U||^2||e||^2`.

Write `delta2=E(G-Q(G))^2` and `kappa=E[G^2(G-Q(G))^2]`. Coordinate independence gives

`E||phi(U)-phi(Q(U))||^2/M <=4[kappa+(r-1)delta2]/(r+1)`.

For T>=1, `delta2<=h^2+E[G^2 1{|G|>T}]` and `kappa<=h^2+E[G^4 1{|G|>T}]`, hence the dimension-independent bound

`D_Q := E||phi(U)-phi(Q(U))||^2/M`

`<=4h^2+4 E[G^4 1{|G|>T}]`.

The tail term is exactly `2[(T^3+3T)varphi(T)+3(1-Phi(T))]`. Choosing T=6 and h=0.01 gives D_Q<4.12e-4 with 11r bits. There is no union bound over r coordinates; the claim controls expected target loss, rather than an event on which every coordinate is accurate simultaneously.

For exact c=1, the all-noisy protocol with this quantization has risk exactly

`1-alpha^3+alpha^3 D_Q`.

In particular its controller message scales with r, despite the coefficient covariance being I_M/M. This does not contradict bounds for a genuinely M-dimensional Gaussian coefficient vector: this vector has a different distribution, supported on a nonlinear r-parameter image.

## Acquiring the unknown coefficients from function values

The feature layout and U/V split are promised; c is unknown and may vary over an open bounded subset of R^M. For p=2, use M bounded synthetic input queries:

* For each diagonal feature, query U=0,V=e_ii. The response is `-c_ii/sqrt(2M)`.
* For each off-diagonal feature, query U=e_i+e_j,V=e_ij. The response is `c_ij/sqrt(M)`.

Thus c is recovered with exactly M scalar function evaluations. All these input vectors have norm at most sqrt(3). Fewer than M scalar evaluations cannot identify arbitrary c exactly: every function evaluation is linear in c, and the affine fiber of any adaptive transcript with fewer than M evaluations has positive dimension inside an open coefficient domain.

If each function evaluation has deterministic absolute error at most nu, the diagonal coefficient error is at most sqrt(2M)nu and an off-diagonal error at most sqrt(M)nu. Therefore

`tau_c^2=||c-c_hat||^2/M <=(M+r)nu^2`.

The calibration precision is a paid resource. In particular unit-scale response noise does not automatically yield this small error from one bounded query per coefficient. Repetition, higher-precision evaluation, or another statistically efficient design would need to be charged if that were the access model.

### Exact combined deployment error

Let the actuator use c_hat and the quantized standardized first observations Q(W). Then the deployed decoder has exact true risk

`(1-alpha^3)sigma_c^2`

`+alpha^3 E||c*phi(W)-c_hat*phi(Q(W))||^2/M`.

This follows by expanding the conditional decoder MSE. The true posterior coefficient is alpha times c*phi(W)/sqrt(M), the implemented one is alpha times c_hat*phi(Q(W))/sqrt(M), and the final noisy linear read pays alpha times their squared error. A simple certificate is

`E||c*phi(W)-c_hat*phi(Q(W))||^2/M`

`<= [tau_c+||c_hat||_infinity sqrt(D_Q)]^2`.

This is calibration in a declared finite-dimensional class. It does not infer the layout, certify that an arbitrary unknown function belongs to the class, or discover a hidden nonlinear latent map.

## Full cost and strongest ordinary alternatives

Preparation stores M coefficients and consumes M function-value calls. A dense implementation of every calibration call evaluates M features, so these calls can consume O(M^2) arithmetic in total; the executable ledger reports that work. Per deployment, the controller obtains r context readings and transmits O(r) finite indices. The actuator forms and normalizes M weights and applies one M-coordinate projection, each O(M) work.

An ordinary method that reads all coordinates and directly evaluates the quadratic form also costs O(M) arithmetic. A native quadratic-energy or direct-target oracle is an ordinary stronger access primitive and can subsume the final projection. If implementing the projection requires exporting all M coordinates first, there is no acquisition advantage. No practical total-cost speedup follows from the scalar-read separation alone.

The meaningful resource distinction is whether the source supports a programmed aggregate with compact incoming control while retaining its M coordinate values locally. The theorem supplies a structured control example and a strong fixed-experiment lower bound, not a claim that such a physical interface has been implemented or discovered.

## Primary-source comparison and novelty status

Hastie and Tibshirani, Varying-Coefficient Models (JRSS B, 1993), was read from the author's public copy. It explicitly defines regressions linear in some variables with coefficient functions depending on other variables, including polynomial bases and vector-valued modifiers. Its Section 3 also explains why unrestricted coefficient functions require additional assumptions for estimation. The conditional-linear representation here is an instance of that established framework:

https://hastie.su.domains/public/Papers/VaryingCoefficients.pdf

Wasilkowski and Wozniakowski, Can adaption help on the average? (1984), concerns linear target problems under orthogonally invariant laws, including Gaussian laws. Its primary abstract was checked in the preceding continuation. The present target is nonlinear in the joint (U,V) input, so the linear no-adaptation theorem does not apply:

https://link.springer.com/article/10.1007/BF01410103

Hillar and Lim, Most tensor problems are NP-hard (JACM, 2013), establishes broad hardness of multilinear/tensor analogues of matrix tasks; its primary abstract was read for the discarded generic-structure-discovery opening. This is a reason not to replace earned feature layout with a supposed universal efficient tensor-discovery oracle; it is not being cited as a direct proof of the sensing theorem:

https://arxiv.org/abs/0911.1393

Targeted searches did not identify this exact Hermite sensing/control hierarchy. Historical priority remains unresolved. Gaussian conditioning, Wick/Hermite expansion, varying coefficients, polynomial feature maps and aligned linear measurement are established machinery. The construction and fixed-experiment bound above are proved directly and do not depend on a novelty claim.

## Executable evidence

`check_hermite_fixed.py` checks degrees p=1,2,3. It passed 102 arbitrary mixed noiseless designs, 306 arbitrary mixed noisy designs and 27 independent cubic conditional-moment integrations. The latter use four-point tensor Gaussian quadrature, which integrates squared cubic conditional predictors exactly in exact arithmetic. The largest discrepancy was below 8e-16. The fixed bound was also reconstructed independently by the adaptive_structure agent.

`learn_quantized_cubic.py` acquires genuinely hidden continuous coefficients in [0.9,1.1] through the declared scalar function-value interface. It implements the 11-bit-per-coordinate control message by actual bit packing and decoding, generates dense actuator weights, simulates all noisy reads, and charges the dense projection. It uses a separate ground-truth scorer only for validation. Its fixed-experiment lower bound grants the comparator the true coefficients, making it stronger than an equally calibrated comparison.

The largest executed instance used r=64 and M=2080. Preparation consumed 2080 function evaluations, 4,326,400 materialized feature entries, and 8,652,800 dense target products. The prepared coefficient array occupies 16,640 bytes. Each deployment used 65 noisy scalar reads, an 88-byte (704-bit) packed control message, 2080 generated weights and 2080 dense projection multiplications. Over 8192 independently simulated inputs, measured MSE was 0.02975957 with estimated standard error 0.00048888; the exact prediction from the acquired model and Gaussian quantizer-bin moments was 0.02968988. Full 2144-coordinate noisy observation has risk 0.02959527. Every fixed 65-read unit-direction experiment has risk at least 0.89399625 by the proved mixed-design bound.

These values establish agreement between the formulas and the executable protocol. They do not establish a runtime win. Preparation and deployment timings in the JSON include implementation and validation details and are not used as speedup evidence. The learned model is saved in `learned_cubic_model.npz`; exact parameters, counts and uncertainties are in `learn_quantized_cubic_results.json`.

The companion `cubic_structure_hardness.md` proves that finding even one globally affine direction of a general supplied cubic is NP-hard, with an inverse-polynomial directional-curvature gap. That result explains why the known feature layout above is a substantive promise rather than a generic factorization algorithm.
