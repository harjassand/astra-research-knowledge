# A realizable exponential finite-noise query obstruction

This is a new mathematical construction, not a claim of literature priority or physical laboratory validation. It strengthens the all-proper-subset obstruction in N854 to arbitrary adaptive controls, under adversarial bounded absolute response noise.

## Statement

For each m≥1 there are 2^m real (m+2)-state plants with the same calibrated rank-one diagonal-control matrix P, the same source b, and the same detector c. Their responses on [0,1]^m are

F_s(u) = product over i of [ε/(ε+u_i) if s_i=0, and u_i/(ε+u_i) if s_i=1],

where ε=m^−2 and s∈{0,1}^m. Every plant is uniformly strictly accretive over the control cube. Matrix norms, inverse norms, condition numbers, source/detector norms, and control strengths are polynomial in m. The unscaled version has P equal to standard basis columns and a common inverse-polynomial dissipation margin; a common polynomial rescaling gives symmetric part ≥I while preserving the functions exactly.

For bounded noise |e(u)|≤η, any randomized algorithm that, on every plant, obtains response at least 1/4 with probability ≥p needs

Q ≥ η(p 2^m − 4)

queries in the worst case. In particular, η=1/16 and p=2/3 give exponential acquisition complexity. The maximum response of every plant is at least 1/2. This is a best-control decision obstruction, not just a failure of a specific calibration schedule. An analogous exponential lower bound holds for predicting every permitted control with uniform additive error less than 1/4.

## 1. Exact diagonal-control realization

Fix s. Introduce formal stage variables x_i and y_i with y_0=1. Impose

(ε+u_i)x_i = ε y_{i−1}.

For s_i=0 set y_i=x_i. For s_i=1 set y_i=y_{i−1}−x_i. Thus y_m=F_s(u) exactly.

Eliminate each y_{i−1} using the preceding x variables. This gives

(A_s+diag(u))x=β_s,

y_m=α_s+γ_s^T x.

Here A_s is lower triangular with diagonal ε and all other entries in {0,±ε}; entries of β_s are 0 or ε; α_s is 0 or 1; entries of γ_s are 0 or ±1. Specifically, one can construct them starting with α=1 and γ=0. At step i, the ith row of A_s is ε e_i^T−ε γ^T and (β_s)_i=εα. Then for bit 0 replace (α,γ) by (0,e_i); for bit 1 replace γ by γ−e_i. The final α,γ give the output coefficients.

This construction is affine in exactly the m independently controlled diagonal entries. There are no controlled off-diagonal couplings and no multiplication of independently applied controls inside the physical matrix.

## 2. Dissipativity proof

Use the same homogeneous recursion with y_0=0, and any vector x. Define d_i=x_i at a bit-1 stage and d_i=y_{i−1}−x_i at a bit-0 stage. In either case y_i=y_{i−1}−d_i. Direct telescoping gives

x^T A_s x = (ε/2)[y_m^2 + sum_i d_i^2].

At bit 1, x_i=d_i. At bit 0, x_i=y_i=−sum_{j≤i}d_j. Consequently ||x||≤m||d||, and

sym(A_s) ≥ δ I,  δ=ε/(2m^2).

Adding diag(u) for u≥0 preserves this bound. Also ||A_s||≤mε, ||β_s||≤ε sqrt(m), and ||γ_s||≤sqrt(m).

## 3. Small common-port realization, with no direct-feedthrough assumption

Embed the stage matrix using two unactuated coordinates:

B_s = [[ε, 0, 0], [−β_s, A_s, 0], [−εα_s, −εγ_s^T, ε]],

P_0 = [0; I_m; 0], b_0=ε e_first, c_0=e_last.

These P_0,b_0,c_0 are identical across all s and have norms at most one. The source equation fixes y_0=1; the middle block implements the stage recursion; the last equation fixes the final state z=y_m. Thus

c_0^T(B_s+P_0 diag(u)P_0^T)^−1 b_0 = F_s(u).

For an arbitrary vector (y_0,x,z), run the same formal stage recursion from that y_0 and put d_i=y_{i−1}−y_i. Telescoping now gives

x^T A_s x − y_0 β_s^T x = (ε/2)[y_m²−y_0²+sum_i d_i²].

Consequently the full quadratic form is exactly

(y_0,x,z)^T B_s (y_0,x,z)
 = (ε/2)[y_0²+z²+(y_m−z)²+sum_i d_i²].

At bit 1, x_i=d_i. At bit 0, x_i=y_0−sum_{j≤i}d_j. Hence ||x||²≤2m y_0²+2m² sum_i d_i², which proves the common bound

sym(B_s+P_0 diag(u)P_0^T) ≥ δ_0 I,
δ_0=ε/[4(m+1)²].

Every entry of B_s has absolute value at most ε, so ||B_s||≤ε(m+2)=O(1/m). The uncontrolled condition number is O(m³). On the entire cube, ||B_s+P_0diag(u)P_0^T||≤1+ε(m+2)=O(1), inverse norm is O(m⁴), and condition number is O(m⁴). No large source or detector amplitude is needed in this unit-actuator version.

For a dimension-independent dissipation margin, let λ=1/δ_0=4m²(m+1)². Use

A'_s=λB_s, P'=2m(m+1)P_0,
b'=2(m+1)e_first, c'=2(m+1)e_last.

Because the product of the new source/detector scalar factors is λε, the response is unchanged. The symmetric part is ≥I, source/detector norms are O(m), actuator norm is O(m²), and the controlled condition number remains O(m⁴). The controlled matrix norm is O(m⁴). All scale factors and coefficients are rational with O(log m) bits. This explicitly charges the polynomial actuator-strength increase needed for a constant dissipation floor; it is not a claim with both unit-strength actuators and constant margin.

The energy identity accounts explicitly for the common source and detector ports.

## 4. Concentration and contrast

All responses are nonnegative and, at every query point,

sum_{s∈{0,1}^m} F_s(u)=1,

because the two gates sum to one coordinatewise. Therefore at most 1/η hypotheses can have F_s(u)>η at any one query, including any interior or fully supported control.

At its binary vertex u=s, a plant has

F_s(s)=(1+ε)^−|s|≥1/2.

The maximum is attained at that vertex because each factor is monotone toward its matching endpoint. Away from the planted corner the product can be exponentially small. No claim is needed that all other binary vertices have exactly zero response: mismatched zero-bits have a small, nonzero leakage, and this is already handled by the sum-to-one argument.

## 5. All-adaptive, randomized bounded-noise lower bound

Use the following fixed, valid noisy oracle for each plant s: return 0 whenever F_s(u)≤η, and return F_s(u) otherwise. Its additive error always lies in [−η,0]. This does not require noise to know future queries or algorithm random bits.

Fix algorithm random bits and follow its all-zero answer path. Each query excludes at most 1/η possible needles. Hence at most Q/η needles can ever cause that run to leave the all-zero path. If it remains on that path, the final proposed control is a fixed point u*, where at most four needles have F_s(u*)≥1/4. Thus, under a uniformly random needle, the success probability is at most

(Q/η+4)/2^m.

Averaging over algorithm randomness leaves this bound unchanged. Uniform success ≥p requires Q≥η(p2^m−4). A constant-regret maximizer (regret strictly less than 1/4) must meet the response threshold, because every optimum is ≥1/2. Minimization is equivalent by changing the common detector sign.

For uniform prediction, distinct plants are separated by at least 1/2 in supremum norm. Given s≠t, select a differing coordinate and let r be whichever of s,t has bit 0 there. At u=r, F_r(r)≥1/2 while the other plant is exactly zero because its bit-1 factor sees u_i=0. Consequently a single prediction function can approximate at most one plant with uniform error ρ<1/4. The same all-zero-path counting yields success probability at most (Q/η+1)/2^m, and therefore

Q ≥ η(p 2^m−1)

for uniform prediction at any error ρ<1/4. This holds directly on the 2^m needle family and needs no added zero plant. The packing argument applies directly to the observable response functions.

### Independent Gaussian noise corollary

The obstruction is not limited to adversarial bounded noise. Suppose each query returns F_s(u) plus independent N(0,σ²) noise. Let P_s denote the distribution of the entire adaptive transcript, including algorithm randomness; let P_0 be the reference distribution with zero mean at every query and the same noise. Gaussian likelihoods and the chain rule give

(1/2^m) sum_s KL(P_0 || P_s)
 = (1/(2σ²2^m)) E_0[sum_{j=1}^Q sum_s F_s(u_j)^2]
 ≤ Q/(2σ²2^m),

since sum_s F_s(u)^2≤1 pointwise. Under the reference distribution a proposed action succeeds for at most four plants, so its average success over s is ≤4/2^m. Pinsker's inequality and Jensen's inequality then give actual average success at most

4/2^m + sqrt(Q/(4σ²2^m)).

Thus uniform decision success ≥p requires Q≥4σ²2^m(p−4/2^m)^2 whenever p>4/2^m. For uniform prediction at error <1/4, replace 4 by 1 using pairwise separation. This covers the Gaussian subclass of independent, unbiased, finite-variance noise. It does not establish the same bound for every noise distribution with those properties.

## 6. Scope and qualifications

- The main theorem is for worst-case bounded absolute noise; the separate corollary covers independent mean-zero Gaussian noise. Neither applies to a noiseless exact real-number oracle.
- Noise η may decrease inverse-polynomially with m and the bound remains exponential. If η is exponentially small, this argument does not establish exponential query cost. Precision is an explicitly charged resource.
- The result is worst-case uniform control/prediction. It does not contradict low sample complexity for average prediction under a fixed control distribution: a needle can be statistically negligible there.
- The unknown plant comes from a finite family with only m bits of hidden structure. Small parameter count alone does not give uniform identification under bounded noise.
- Arbitrary adaptive global controls, interior cube points, and unlimited computation are allowed.
- The construction is real, nonreciprocal, strictly accretive and linearly controlled. It does not assert a particular fabrication technology, thermodynamic cost, or experimental source/detector sensitivity.
- The fixed ε gates use polynomially small baseline admittance. Requiring unit actuator norms and a dimension-independent dissipation floor simultaneously is a narrower regime not settled by the scaled construction.
- All coefficients in the ε=m^−2 construction have O(log m)-bit rational descriptions; in the constant-margin scaling sqrt(λ)=2m(m+1) is an integer. Coefficient precision therefore hides no exponential resource.
- No historical priority has been established; see PRIOR_ART.md for the primary-source comparison. The combinatorial query argument is the standard hidden-needle/zero-transcript counting mechanism; the contribution here is its explicit additive-diagonal accretive matrix realization.

## Numerical sanity check

check.py enumerates all binary strings for m=1,...,8, checks the accretivity lower bound and compares the matrix transfer with the product formula at a sampled cube point. Maximum error was 2.22e−16; the minimum eigenvalue-to-proved-bound ratio ranged from 2.0 to 7.72. These are only sanity checks; the identities and bounds above provide the proof.

## 7. Exact readout needs only one query on this promised family

Let p_1,...,p_m be distinct known primes and query u_i=ε/p_i, which always lies in [0,1]. Then

F_s(u) = [product_{i:s_i=0} p_i] / [product_i (p_i+1)].

Multiplying an exact rational readout by the known denominator and testing divisibility by each known prime recovers every bit. Using the first m primes, the controls and rational response have O(m log m) total relevant precision bits. The smallest general separation guaranteed by this encoding is the reciprocal of the denominator, which is exponentially small in m log m. Conversely, its N distinct outputs lie in [0,1], so some pair is separated by at most 1/(N−1); any single-readout decoder that must tolerate arbitrary bounded error uniformly requires an exponentially small absolute error tolerance. Thus exact acquisition and noisy acquisition genuinely differ here. An exponentially small absolute error tolerance is NOT an exponential number of binary precision bits. The finite-noise lower bounds explicitly charge noise or repetition; they do not contradict generic exact-query theorems.

## 8. Extension to the generic plants of the N854 theorem

The unperturbed needle matrices have nongeneric zeros. The preceding results alone are worst-case results for the full admissible plant class. The following perturbation argument moves every needle into the generic subset while preserving exponential noisy-query lower bounds. It uses the finite proper algebraic exceptional sets described in N854; it does not assert uniform conditioning of its inversion formulas.

### 8.1 Stability and the fixed-port genericity map

Use the constant-margin scaled version, denoted A_s, P,b,c, with sym(A_s)≥I. Let B=||b||||c||=4(m+1)². For any real matrix Δ with ||Δ||≤1/2, all u≥0 have

|c^T(A_s+Δ+Pdiag(u)P^T)^−1b − F_s(u)| ≤ 2B||Δ||.

This follows from the resolvent identity and the inverse-norm bounds 1 and 2 for the unperturbed and perturbed accretive matrices. The inequality is uniform over the whole nonnegative control orthant.

For fixed P,b,c, there is no algebraic restriction preventing N854 genericity. Before the common rescaling, write G=A^−1 with coordinates ordered (source, m internal controls, detector). Then

H=G_internal,internal, w=ε G_internal,source,
v^T=G_detector,internal, f0=ε G_detector,source.

These are disjoint entries of G; their coordinate projection has full differential rank. Restricted to invertible G it is a submersion with open image, not necessarily a globally surjective map onto every arbitrary specification of extracted blocks. Matrix inversion is a birational diffeomorphism. When all w_i≠0, passing to (Hbar=diag(w)^−1Hdiag(w), a_i=v_iw_i, f0) is also a submersion onto an open set of reduced coefficients: locally hold w fixed and vary H and v freely. The known input/output and actuator rescalings merely multiply these extraction maps by nonzero constants and does not change this conclusion.

Consequently, pulling back a proper reduced generic-exception polynomial, and clearing inverse/gauge denominators, gives a nonzero polynomial in the full entries of A. It cannot vanish on an open accretive ball. This establishes that an arbitrarily small full-matrix perturbation can satisfy all the source's generic assumptions with the SAME P,b,c.

### 8.2 Rational perturbations and description length

Using the reconstruction and genericity statements in the supplied N854 proof as the source-dependent premises, its bad conditions can be represented by O(m²) polynomials of total degree O(m) each in the physical A entries, after clearing denominators. Reason: each condition uses a singleton, pair, or triple, constant-sized rational operations, and the rational edge involution (H_ij,H_ji)→((a_j/a_i)H_ji,(a_i/a_j)H_ij). Each extracted G entry is an adjugate entry divided by det(A), of degrees at most m+1 and m+2. The finite triple-separation tests use only a constant number of branches per triple. Include w_i≠0, a_i≠0, determinant and reconstruction denominators among the conditions. Thus the product polynomial has total degree T=O(m³). Fixed rational choices such as t1=1/3, t2=2/3, t3=1/2 keep all calibration controls in the permitted cube. For the triple-separation witnesses at t3=1, replace H and a by H/t3 and a/t3; every candidate triple response at the new t3 then equals its original response. Singleton and pair denominator exclusions are nonzero for generic coefficients at any distinct positive t1,t2. This degree bound uses the source's explicit constant-size reconstruction operations rather than a separately expanded list of exceptional polynomials; if that source's genericity premises fail, the unperturbed construction and its noisy lower bounds still stand independently.

Let ζ>0 be the desired uniform output perturbation and put ρ=min{1/2,ζ/(2B)}. Choose an integer K>T. Perturb every matrix entry independently from the grid

{0, ρ/(nK), 2ρ/(nK), ..., (K−1)ρ/(nK)}, n=m+2.

Every such Δ has operator norm at most ρ. The product exceptional polynomial remains nonzero under this affine substitution, so the elementary finite-grid polynomial bound gives at least one grid choice for which it is nonzero. This is an existence argument; it does not assume a free robust way to validate genericity in a physical experiment. With rational ζ of O(m+log m) bits, all perturbed matrix coefficients have O(m+log m) bits. For fixed or inverse-polynomial noise, one may take ζ≤1/(64·2^m), so the bit cost remains polynomial even though the perturbation is exponentially small. The perturbations retain accretivity ≥I/2 and polynomial norms/condition numbers.

### 8.3 Noisy lower bounds survive

Write the perturbed responses as F̃_s, with sup_u|F̃_s(u)−F_s(u)|≤ζ. Take ζ≤min{η/4,1/16,1/sqrt(N)}, N=2^m.

For bounded noise, use an oracle returning zero when the ORIGINAL F_s(u)≤η/2, and otherwise returning F̃_s(u). This is valid because |F̃_s(u)|≤η/2+ζ≤η at the zeroed points. Every zero-path query exposes at most 2/η plants. At any fixed final control, F̃_s(u)≥1/4 implies F_s(u)≥1/4−ζ≥1/8, so at most eight plants succeed. Hence

Q ≥ (η/2)(pN−8)

is necessary for decision success p at threshold 1/4. Every perturbed optimum is at least 1/2−ζ≥7/16, so this remains a nontrivial constant-accuracy decision task.

Pairwise sup-norm separation is at least 1/2−2ζ. Uniform prediction with error strictly below 1/4−ζ can fit at most one perturbed plant, giving Q≥(η/2)(pN−1). In particular, any fixed error below 3/16 is covered by ζ≤1/16.

For independent Gaussian noise,

sum_s F̃_s(u)^2 ≤ 2 sum_s F_s(u)^2 + 2Nζ² ≤ 4.

The same KL argument therefore gives average decision success at most 8/N+sqrt(Q/(σ²N)), so Q≥σ²N(max{p−8/N,0})². For uniform prediction in the separated-error regime replace 8/N with 1/N.

This generic extension proves that exact generic identifiability does not imply uniform noisy acquisition efficiency, even within the generic set. The deliberately tiny perturbations can make N854's algebraic inversion conditions extremely poorly separated; no lower bound on those separations is supplied or implied.

## 9. Adaptive precision and inverse-variance measurement budgets

The Gaussian result also permits query-dependent noise precision. At query t, let the algorithm choose both u_t and σ_t>0 from its past observations, with a fresh independent Gaussian error of conditional variance σ_t². Suppose every transcript obeys a total inverse-variance budget V=sum_t σ_t^−2. The chain rule under the same zero-mean reference gives average KL at most V/(2N), since sum_s F_s(u_t)²≤1 at each chosen control. Therefore success is at most

K/N + sqrt(V/(4N)),

where K=4 for the response-threshold decision and K=1 for uniform prediction. Necessarily V≥4N(max{p−K/N,0})². This also permits an adaptive stopping time whenever the budget bound holds pathwise and the usual finite-transcript or limiting KL argument applies.

If a stated measurement interface charges time or exposure proportionally to inverse variance, as in ideal independent white-noise averaging at fixed spectral density, this yields an exponential total measurement-time/exposure bound even when a query may be made arbitrarily precise. This is a conditional measurement-interface statement, not a universal physical law connecting precision to energy or time. The perturbed generic family inherits the same conclusion with the constant-factor loss from sum_s F̃_s²≤4.
