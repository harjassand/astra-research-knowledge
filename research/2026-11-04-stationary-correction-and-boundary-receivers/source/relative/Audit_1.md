# Independent audit of weighted Pfaffian interfaces

4 November 2026. Reviewed PROOF.md SHA-256: c46f70d3ed6e5f4960bfb38fa1f5c3279eb4cecb3ad1c85b44d4820b67597b35.

## Verdict

The weighted relative-error theorem, product-field response algorithm, rare same-sign conditioning claim, and joint multiblock stability certificate pass this independent review under their explicit promises. No blocking algebraic or runtime error was found. The crucial positivity is that of the true marginal and its true even moments, not of an empirical reconstructed law or an interpolating model. General-environment efficient contraction, model certification, physical sampling costs, novelty and practical advantage remain unproved.

This report independently checked the reasoning rather than treating the author's numerical tests as proof. Supplementary exact rational checks covered 433 weighted derivative and prefix cases through six spins, including deterministic-support true laws, signed reconstructions, hard pins, non-pairwise Fourier-positive weights, and coupled independent blocks. Tests are internal and are not part of a proof-only package.

## 1. The essential weighted step

For a matching M with endpoint set U, differentiating the Pfaffian Fourier polynomial leaves a uniform law on U times a spin-flipped true marginal on U's complement, with an overall signed spin monomial. Its absolute value is therefore a normalized nonnegative law, even for crossing matchings. A repeated endpoint gives a zero mixed derivative. The sign-flip rule counts selected arcs containing each unselected vertex; crossing signs among selected arcs contribute only an overall sign removed by the absolute value.

Averaging W over U eliminates every Fourier monomial meeting U. Its expectation under the residual spin-flipped marginal is the sum of w_S chi_S E_P x_S over S disjoint from U. True odd moments vanish. All other true moments and all stipulated w_S are nonnegative. Dropping chi_S signs and restoring omitted terms consequently bounds this expectation by Z=E_P W. There is no independence assumption on spins within a block and no division by a small assignment probability.

The weight's pointwise nonnegativity is needed when identifying the expression as a weighted absolute norm. The proof does not require every term after introducing chi to be nonnegative. These two distinct uses of positivity are handled correctly.

The all-Fourier-coefficients condition is sufficient, not necessary. For a single zero-field block, only even coefficients enter this particular argument; odd coefficients could have either sign provided W remains nonnegative. For independent blocks, only monomials having even intersection with every block survive. This observation is not required for, and does not expand, the delivered theorem's chosen cone.

## 2. Taylor expansion, normalization and signed repair

The Pfaffian is multi-affine in pair entries. Nonzero mixed derivatives select matchings, so the exact finite Taylor expansion contains one product of pair errors per matching, with no missing factorial. The weighted derivative bound gives a sum bounded by the product over all pairs of (1+|Delta_ij|), minus one, and hence by exp(D)−1. Derivatives are evaluated only at the true C. No convexity of the space of physical correlation matrices, physicality of C+sDelta, or positivity of p_A is assumed or needed.

Writing eta=exp(D)−1, the partition-ratio estimate and Z_A≥Z(1−eta) follow immediately. Adding and subtracting W P/Z_A gives the stated normalized signed-law bound 2eta/(1−eta). This requires eta<1 as stated.

For signed prefix repair, every reached prefix has positive signed mass. The sum of positive child masses is at least the signed parent mass. Thus each conditional clipping step multiplies the nominal signed-flow ratio by a factor no greater than one; telescoping gives Q(x)≤max(r_A(x),0). With P_W a probability law, this implies TV(Q,P_W)≤||r_A−P_W||_1/2. The improved factor is valid even if many unreachable leaves have negative signed masses. The capped random-bit implementation is a separate perturbation of this ideal Q; its additional error must be added rather than claiming it preserves the pointwise domination exactly. The proof does this correctly.

Because the good estimation event bounds D independently of W, the certificate holds simultaneously for all admitted weights, including weights selected after inspecting the learned data. This does not create an efficient representation or evaluation procedure for arbitrary W.

## 3. Product fields and rare evidence

The one-Pfaffian identity passes its sign and parity checks. For even size, Pf(J)=1, and expansion of Pf(J−D_z A D_z), with the alternating signs in D_z, produces the even-subset generating polynomial F_A(z). Padding with a zero row and column handles odd k without changing it. The identity is algebraic and permits zero and negative evaluation arguments even though admitted product-field parameters are nonnegative.

For a fixed prefix a, indicator expansion contributes 2^−j F_A(a,t_remaining), and its already fixed field factors contribute exactly the displayed product of (1+t_i a_i). No field factor is counted twice. A hard positive pin t_i=1 gives zero mass to its forbidden child exactly; valid reached prefixes still have a positive total child mass. A zero field t_i=0 causes no singularity.

For r positive pins, W is 2^r times the event indicator. Consequently F_C(t)=2^r P(event), and relative error on F_C is exactly relative error on that event probability. The factor 2^r cancels rather than becoming a sample penalty. Under independent spins this event has probability 2^−r, so the claim genuinely reaches exponentially rare evidence under the structural promise. Global spin symmetry gives the all-negative version. The method does not supply the same uniform guarantee for arbitrary mixed-sign assignments.

The excluded two-spin example is exact: c=1−rho and opposing hard pins give Z=rho; replacing c by c−delta gives relative partition error delta/rho. An independent rational check with rho=1/10000 and delta=1/100 gives relative error exactly 100. Both true and perturbed two-spin laws in this example can be valid ferromagnetic laws. This disproves an unrestricted extension of the stability inequality, not every possible adaptive learning method for opposing evidence.

## 4. Multiblock composition

Independence refers to the isolated reference laws, before adding W. A mixed derivative of their product factors into per-block derivatives; its absolute law is a product of uniform endpoint factors and spin-flipped true marginal factors. In the Fourier expansion of W, any surviving moment is a product of true block moments. It is zero if one block intersection is odd, and otherwise nonnegative. The same deletion, sign removal and restoration argument therefore gives the joint weighted derivative bound by the true coupled Z.

Expanding jointly in all pair variables proves the exp(D_total)−1 result. One must not instead repeatedly apply a one-block theorem while pretending a signed reconstructed neighboring block induces an admitted environment. The delivered proof avoids that invalid route. It does not assume any partially reconstructed product or contracted environment remains physical or positive.

Arbitrary ferromagnetic connections and hard identifications fit the nonnegative Fourier cone. This is a robustness certificate for their contractions. It is not a polynomial algorithm for evaluating arbitrary compactly represented contractions of signed learned blocks. The only fully supplied contraction/sampling receiver is the product-field case. Absolute physical partition functions further need the isolated bulk normalization factors, which normalized boundary samples do not determine.

## 5. Statistics, arithmetic and sampler runtime

For pair observables taking values in {−1,+1}, the tail bound is 2 exp(−N h²/2), so N≥(2/h²) log(2m/alpha) suffices. With h=epsilon/(32m), D≤epsilon/32; for epsilon≤1 the conservative eta≤epsilon/16 and eta/(1−eta)≤epsilon/15 inequalities hold. Reusing the same samples for all pairs does not invalidate the union bound. Simultaneous block confidence requires the stated union bound across block estimates. Many outputs from the fitted law do not automatically retain a fixed joint TV budget.

The sample cost is O(k^4 epsilon^−2 log(k/alpha)), conditional on iid full-boundary observations and the structural promise. Mixing time, detector noise, unknown ordering, hidden changes of state space, and testing whether a general physical system satisfies the promise are not included.

Empirical correlations have denominator N. Every Pfaffian prefix expression has polynomial degree and polynomial coefficient bit height in k, log N and the rational query bit length. Exact rational Pfaffian evaluation with pivoting has polynomial bit complexity; two evaluations at each of k sampling stages give the stated conservative O(k^4) arithmetic-operation count. Rational activities, rather than binary encodings of an arbitrarily huge real field whose exponential must be written, are the specified input contract.

For a reduced nontrivial rational coin a/b, rejection using ceil(log2 b) bits accepts with probability strictly greater than one half. Deterministic 0/1 cases must be separated, as they are. Capping at R trials changes each transition by at most 2^−R; a union bound over k stages is within the allotted epsilon/4. A positive-mass fallback child ensures later denominators exist. The stated exact capped transition (1−f)a/b+f times the fallback indicator is correct, as is polynomial bit complexity of its evaluator. The k=0,1 cases are separately trivial. Failure of the training event can invalidate accuracy, but does not make the stated high-probability contract false.

## 6. Prior and consequence boundary

The closest specified-model baselines already supply the central exact algebra: [Groeneveld, Boel and Kasteleyn (1978)](https://www.sciencedirect.com/science/article/pii/0378437178902145), [Galashin and Pylyavskyy (2020)](https://arxiv.org/abs/1807.03282), and [Cai and Gorenstein (2014)](https://www.theoryofcomputing.org/articles/v010a007/v010a007.pdf). Their boundary Pfaffian, inverse and matchgate results must not be redescribed as newly obtained by this noise theorem. [Clusel and Fortin (2005)](https://doi.org/10.1088/0305-4470/38/13/003) already develop exact boundary-field partition functions.

General specified ferromagnetic partition-function approximation also has a much stronger established computational baseline: [Jerrum and Sinclair (1993)](https://doi.org/10.1137/0222066). Relative accuracy for exponentially small observables is not by itself unprecedented: [Goldberg and Jerrum (2019)](https://doi.org/10.1145/3337785) provide a multiplicative covariance approximation scheme for specified ferromagnets. Those inputs include a model, whereas the present learner takes passive samples of an unknown hidden block. This difference is real, but does not establish a speed or information advantage over the strongest adaptation of known identities to the same data oracle.

The scoped conclusion is a uniform, noise-tolerant relative interface bound plus an implementable product-field response learner and sampler. It strengthens isolated TV control under an explicit ferromagnetic/Pfaffian promise. Priority for that assembled result remains unresolved, and no experiment or matched end-to-end resource comparison establishes a practical or civilisation-scale advantage. The mathematical audit is favorable; the operational and novelty claims must remain bounded accordingly.
