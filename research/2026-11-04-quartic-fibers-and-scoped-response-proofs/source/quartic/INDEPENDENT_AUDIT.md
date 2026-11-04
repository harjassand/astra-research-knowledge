# Independent audit: hidden Gaussian quartic compiler

Status: core lemma and successful-certificate reconstruction pass. Full general completeness and polynomial Turing complexity are not established. This audit initially checks the author's equations communicated directly; a final draft check is recorded below when available. No Python was run for this audit.

## 1. Constant-curvature lemma, independently derived

Let V be a real polynomial of degree at most four, globally bounded below. Write V_j for its homogeneous degree-j part and define E={v: D_v V_4=0}. Let C={v: D_v^2 V is constant}.

First V_4 is nonnegative everywhere, by scaling. If v is in C, then D_v^2 V_4=0. Along any affine line parallel to v the polynomial V_4 is affine and globally nonnegative. Its slope must vanish, so D_v V_4=0. Therefore C is contained in E.

Choose any invertible linear coordinates x=A(t,y), with t spanning E. Then V_4 is independent of t. For fixed y, V(A(t,y)) has degree at most three in t and is bounded below. Its homogeneous cubic-in-t term therefore vanishes. Write

V(A(t,y)) = t^T Q(y)t + 2r(y)^T t + s(y).

Q(y) is affine in y, because the quartic part has no t dependence. Boundedness implies Q(y) is positive semidefinite for every y. For each fixed u, u^T Q(y)u is a globally nonnegative affine function of y, hence constant. Polarization shows Q(y)=Q is constant. Thus every v in E has constant second directional derivative, and E=C. Also deg r≤2 and deg s≤4.

If exp(−V) is integrable, Q must be positive definite: any null vector produces, on every fiber y, an exponential of an affine function along that vector, whose integral on the real line diverges whether its slope is zero or not. Tonelli then rules out a finite full integral. This is stronger than mere semidefiniteness and requires integrability, not just boundedness.

Consequently

V(A(t,y))=(t+Q^(−1)r(y))^T Q(t+Q^(−1)r(y))+V_red(y),
V_red=s−r^T Q^(−1)r.

The residual is quartic or lower, bounded below by the same lower bound, and integrable after multiplying by the finite Gaussian fiber integral. The induction hypotheses are preserved.

## 2. What successful recovery actually proves

At each step retain the coordinate map A, Q and r. Conditional on y, sample t with mean −Q^(−1)r(y) and covariance (2Q)^(−1). Reverse all elimination steps. If the final residual is the scalar c, the result is an exact real-arithmetic polynomial triangular circuit applied to independent Gaussian vectors. Its global bijectivity follows step by step: linear coordinates are invertible and each conditional shift is an invertible shear. No local-inverse or Jacobian conjecture is needed.

For the unnormalized integral, each step contributes |det A| π^(k/2)/sqrt(det Q). Therefore Z=e^(−c) times the product of these factors. Omitting nonorthogonal coordinate Jacobians would be an error.

A sound certificate can be checked without deciding boundedness of arbitrary quartics: directly verify every polynomial identity, every Q positive definite, every coordinate map nonsingular, and the terminal scalar. These checks prove normalizability and the transport for that input. However an unsuccessful run is not yet a proof that no other nonlinear Gaussianization exists.

The maximal-kernel greedy rule still needs a distinct theorem if it is claimed to be complete for all potentials admitting some Gaussian-elimination flag. The existence of one available first direction alone does not establish that every maximal-block choice preserves all possible future flags. No counterexample is asserted here; the proof obligation must not be silently skipped.

## 3. Arithmetic versus bit complexity

With an explicitly expanded dense quartic input, each stage uses nullspace computation, coordinate substitution, matrix inversion and degree-four polynomial arithmetic. There are at most n nonempty eliminations, and the number of field operations is polynomial in the dense input size. A transport retained as a circuit has polynomially many operations; fully expanding its inverse can have exponential degree and size.

A polynomial number of rational field operations does not by itself bound the bit lengths of intermediate rational coefficients. A separate height analysis or fraction-free/global representation proof is necessary for a polynomial Turing-time compiler claim. No such bound is credited in this audit.

An unconditional polynomial-time ordinary fixed-point sampler is in fact impossible over the unrestricted accepted class. Consider the integer/rational-coefficient quartic

V_n(x)=1/2[(x_n−4)^2 + Σ_(i<n)(x_i−x_(i+1)^2)^2].

The exact sampler is X_n=4+Z_n, X_i=X_(i+1)^2+Z_i with independent standard Gaussians. With probability 1/2, X_n≥4. Set a_0=4, a_(j+1)=a_j^2/2, so a_j=2^(2^j+1). Conditional on reaching a_j, failure to reach a_(j+1) has probability at most Φ(−a_j^2/2). A union bound over j gives total failure below 10^(−14), uniformly in n: the first threshold is 8, and subsequent thresholds increase doubly exponentially. Hence X_1≥2^(2^(n−1)+1) with probability greater than 0.49. Merely writing its integer part requires Ω(2^n) bits in ordinary positional fixed-point representation.

This does not exclude compressed arithmetic circuits, floating-point relative accuracy, bounded parameter regimes, or output-sensitive algorithms. Such output conventions must be named. Also a finite-bit output distribution is discrete and cannot be close in total variation to an absolutely continuous target. A rounded target or another explicitly defined approximation metric is required.

## 4. Strong established comparators and actual scope

- Carlini, *Reducing the number of variables of a polynomial* (2005/06), https://arxiv.org/abs/math/0507531: essential-variable reduction via linear dependence of first derivatives is established. Applying the derivative nullspace to V_4 is not itself a new algebraic operation.
- Welch, Zhang and Uhler, *Identifiability Guarantees for Causal Disentanglement from Purely Observational Data* (2024), https://arxiv.org/abs/2410.23620 and https://arxiv.org/html/2410.23620v2: unknown linear mixing of additive-Gaussian causal models, layer-wise recovery, directional score-Hessian criteria and quadratic optimization. This is the closest acquired hidden-coordinate comparator. Their statistical input/assumptions and the proposed exact dense-coefficient quartic input differ; neither should be substituted for the other.
- Pagani et al., *An n-dimensional Rosenbrock distribution for Markov chain Monte Carlo testing*, https://arxiv.org/abs/1903.09556 and https://doi.org/10.1111/sjos.12532: quartic conditional-Gaussian constructions already have direct independent sampling and known normalization. Sampling a supplied triangular quadratic model is not new.
- Dinh, Krueger and Bengio, *NICE* (2014), https://arxiv.org/abs/1410.8516: invertible additive coupling, simple Jacobians, and ancestral sampling are established normalizing-flow operations.

The potentially useful deliverable is a coefficient-only exact recognition/certification procedure based on a bounded-below quartic lemma, with explicit reconstruction. No claim of novelty, practical learning from noisy samples, generic quartic sampling, polynomial fixed-point sampling, or broad scientific transformation follows from the current proof.

## 5. Additional physical/statistical assumptions

Exact cancellation of homogeneous coefficients and exact kernel ranks are fragile under perturbations. A learned approximate potential needs a singular-value separation, positive-precision margin, tail control, and an error theorem before this can be called a robust inference/sampling method. An arbitrarily small positive quartic perturbation can remove every exact Gaussian direction. Failure of an exact rank test is not evidence that approximate sampling is hard, and success under ideal coefficients does not establish sample-efficient recovery of those coefficients.

## 6. Draft check and resolved narrow-class completeness

I read the author's substantive PROOF.md, sections 1–6, on 2026-11-04. Its section 5 supplies an additional invariant that resolves the preceding completeness concern for the specified lowering-flag class. This is not a completeness theorem for all polynomial Gaussianizations or every conceivable integration flag.

Write V=c+||q_0+Lx+L b(x,x)||², where L is invertible and b is symmetric bilinear, with a full flag F_j satisfying b(F_j,R^n)⊆F_(j−1). Such an invariant holds for a triangular quadratic map, survives invertible linear changes of input, and is unchanged by invertible output transformations absorbed into L.

For A={v:b(v,w)=0 for all w}, the quartic derivative kernel is exactly A. Indeed a sum of squared real polynomials constant on every line parallel to v forces each polynomial in that sum to be constant along those lines. Equivalently, its highest nonconstant coefficient would contribute a strictly positive highest even power. Since L is invertible, this proves the asserted annihilator identity.

Choose x=Kt+By with im K=A. All quadratic terms are independent of t. Let P be the orthogonal projector onto (LA)^perp. Completing the Gaussian square yields

V_red(y)=c+||P(q_0+LB y+L b(By,By))||².

The map M=PLB from the input complement to (LA)^perp is invertible: PLB y=0 implies By belongs to A, and therefore y=0. Dimensions agree. Its normalized quadratic map M^(−1)PL b(By,By) is the product b induced on the quotient by A, in the chosen complementary coordinates. The reason is PL kills LA, so adding an element of A to any representative does not change the class. A is an annihilator ideal.

The images (F_j+A)/A give a lowering flag in the quotient. Deleting repetitions is legitimate: dimensions increase by at most one, and the first index at which a new dimension appears maps into the preceding distinct image. Thus whenever the quotient is nonzero it has a nonzero annihilator. This proves that maximal-block elimination succeeds recursively for this invariant class. Constants q_0 cause no problem.

The cleanest theorem states this invariant class directly and notes that triangular quadratic maps are included. It need not assert a separate classification of all nonlinear Gaussianizable quartics. The proof does not recover a uniquely meaningful causal graph: it recovers one correct Gaussian transport.

Draft verdict: sections 2–4 check algebraically, with coordinate determinants and covariance conventions correct. Section 5's quotient construction passes for the explicit lowering-flag promise as detailed above. The remaining polynomial coefficient-height question is explicitly left open in the draft and must remain so absent a new proof. The draft appropriately avoids claiming a practical finite-bit exact sampler or robustness to noisy coefficient estimates. My constant-probability output-size example strengthens its minimizer-only illustration; a large minimizer alone would not establish a sampler output lower bound.

## 7. Exact recognition is discontinuous even when the target law is close

Take V_0(x,y)=x²+(y−x²)² and V_epsilon=V_0+epsilon y⁴ for epsilon>0. The unperturbed compiler succeeds. The perturbed leading form is x⁴+epsilon y⁴, whose directional derivative kernel is zero, so the exact compiler stops immediately for every positive epsilon.

Nevertheless the probability laws are close quantitatively. Under p_0, X and Z are independent N(0,1/2) and Y=X²+Z. Thus E_0[Y⁴]=105/16+9/4+3/4=153/16. Set w=exp(−epsilon Y⁴) and a=E_0 w. Since p_0=a p_epsilon+(1−a)r for a probability density r, TV(p_0,p_epsilon)≤1−a≤epsilon E_0 Y⁴=153 epsilon/16. Hence arbitrarily small total-variation perturbations can destroy every exact fiber. This does not refute the exact theorem; it demonstrates why an approximate-recognition/sampling theorem would be a genuinely separate capability.

## 8. Final revision audit: fixed depth and rounded outputs

Reviewed PROOF.md SHA256 `4ccf075981c93b856d683a7d38c290341a861315fbae868de6bce3cfc64aff63` on 2026-11-04. The earlier normalizer ambiguity has been corrected: the unscaled squared-residual chain has Z=pi^(n/2), whereas its one-half-scaled standard-normal counterpart has Z=(2pi)^(n/2).

Sections4.1–4.2 add a valid, materially narrower positive complexity result. Using minors/fraction-free rational linear algebra and direct fixed-degree substitutions, one stage has coefficient-height bound H_next+1≤poly(n)(H+log(n+1)+1). A fixed number d of maximal-block eliminations therefore gives polynomial Turing complexity in original rational input size, with polynomial degree allowed to depend on d. This does not establish the unrestricted d≤n coefficient-height claim.

The rounded-output sampler also passes. Its target is coordinatewise nearest-grid rounding of the exact continuous sample, not continuous-law total variation. Standard-normal transport is implemented with rational LDL factors and approximated positive rational square roots. On a bounded latent cube, magnitude and Lipschitz bounds have logarithms at most2^d poly(n,H,log G). The stated global density bound is correct because the successful global transport attains min V=c. The expanded-output-cube rounding-slab volume bound safely bounds the probability of boundary crossing. All required evaluation and Gaussian precisions have polynomial bit length in n,H,p,log(1/epsilon),2^d.

The capped rejection implementation is sufficient: for G≥1, the integral of exp(−y²/2) over [−G,G] exceeds1, so its uniform-proposal acceptance probability is at least1/(2G). The stated cap gives the charged small failure probability. Coupled dyadic uniforms alter decisions only near acceptance thresholds; the derivative bound at most1 and the union over polynomially many proposals justify the precision choice. Location error, elementary exponential evaluation, tail clipping and deterministic fallback are separately accounted for. Gaussian covariance square-root errors are included in evaluating the full transport, not silently treated as exact rational coefficients.

Thus the final claim supported here is: exact coefficient-to-transport recovery under the lowering-flag promise; polynomial arithmetic complexity generally; polynomial Turing compilation and polynomial Turing sampling of a specified rounded target at fixed elimination depth. The earlier warning against unrestricted fixed-point output and the discontinuity example remain applicable. This final section supersedes any blanket reading of the initial draft-stage statements as denying all finite-bit sampling guarantees.
