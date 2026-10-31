# Independent mathematical review: parallel frozen-fiber capacity

## Verdict and exact source scope

PASS for the stated full-fiber equilibrium capacity/mass theorem. I read the entire `PARALLEL_CHANNEL_CANDIDATE.md`, SHA-256 `05eee3b87028cd70a43d65de2a34abe0e0ab4c52213d1b490ce74bbeae8f18f4`, and checked all normalization, sign, integrability and contraction steps. No source was modified.

This receipt does not accept the finite arithmetic wrapper, its 77-test suite, or the raw quartic engine merely by reference. They require their own source-bound receiving reviews. The previously reviewed homogeneous polynomial theorem supplies a sufficient global-process premise for that grammar; this broader p>0 statement still explicitly requires an actual conservative reversible diffusion and finite positive fiber partition.

The optional asymptotic source has a separate review note. Primary comparison scope is discussed below, without a historical novelty claim.

## 1. Fixed-fiber Cauchy is a valid full-process lower bound

For an admissible committor test h, the full-fiber basins fix h(-b,z)=1 and h(b,z)=0 for almost every z. On each such fiber, weighted Cauchy gives

    1 <= [integral |h_y|^2 exp(-beta vU)dy]
          [integral exp(beta vU)dy].

Therefore discarding the nonnegative transverse-gradient part of the full Dirichlet energy gives a lower bound, not an unjustified reduced-process equality. Infimizing over h preserves it. Smooth approximants and local Sobolev slicing/Fubini give the same assertion in the Dirichlet-form domain; full-fiber boundary traces are essential. This argument would not automatically receive arbitrary basin shapes.

With R(t)=integral_{-1/2}^{1/2} exp(v(y)t)dy and the full Gibbs normalizer Z,

    cap_mu(A,B) >= (beta Z)^(-1) integral dz / R(beta U(z)).

Since the slab has length one and v>=v_min>0 there,

    0<1/R(beta U)<=exp(-beta v_min U).

Thus the transverse integral is finite. It is positive as well. The reciprocal inequality and the slab-length factor are correct. For a different slab length the corresponding constant could not be silently dropped.

Equivalently a divergence-free current can run in the y direction with its z-dependent intensity proportional to 1/R(beta U(z)); its optimized parallel resistance gives the same bound. This current and its unknown normalization are analytic witnesses, not operations required of the proposed scalar output procedure.

## 2. Homogeneous pushforward and cancellation

Let alpha=m/p>0 and V_U=vol{U<=1}. Homogeneity gives vol{U<=s}=V_U s^alpha for s>0. Finite positive Z_U implies finite positive V_U, and

    Z_U=Gamma(alpha+1)V_U.

Consequently the pushforward of Lebesgue measure under beta U is

    (Z_U beta^(-alpha)/Gamma(alpha)) t^(alpha-1)dt.

The factor is correct: differentiating V_U s^alpha supplies alpha, and Gamma(alpha+1)=alpha Gamma(alpha). Positivity allows this identity by measure pushforward without an angular parameterization or differentiating level sets. A coarea regularity/oracle assumption is not hiding in the argument.

The actual basin mass satisfies

    Z mu(A)=Z_U beta^(-alpha) MA,

because v is globally even and the full density is exactly exp(-beta vU)/Z. The angular partition cancels and leaves precisely

    k_parallel = [beta MA Gamma(alpha)]^(-1)
                    integral_0^infinity t^(alpha-1)/R(t)dt.

Near zero the integrand is O(t^(alpha-1)); at infinity it is bounded by t^(alpha-1) exp(-v_min t). Both are integrable. Global normalizability separately requires 4m>p since q=v^(-alpha) has tail order |y|^(-4alpha). The original polynomial Lyapunov argument handles nonexplosion in the received smooth quartic family. The theorem does not infer diffusion existence from finite Z_U alone for every conceivable nonsmooth homogeneous U.

## 3. Gamma expectation and Jensen

Set a=1+kappa, Delta=a-v and S(t)=integral exp(-t Delta)dy. With T Gamma(shape alpha, rate a),

    integral t^(alpha-1)/R(t)dt / Gamma(alpha)
       =a^(-alpha) E[1/S(T)].

Since R0=a^alpha I_minus, division by k_free gives exactly

    k_parallel/k_free=I_minus E[1/S(T)].

The Gamma rate, rather than scale, convention matters and is correct. Tonelli and the Gamma Laplace transform give E S(T)=I_plus. Jensen for x ->1/x gives E[1/S]>=1/E[S]. The expectation is finite: S(t)>=exp(-Delta_max t), and Delta_max<a. The intermediate lower ratio is I_minus/I_plus; both scalar integrals are positive.

The Gamma variable is a proof device for a scalar integral identity. The final explicit-factor algorithm need not sample it, evaluate Gamma, calculate Z_U or numerically integrate k_parallel. This is not a hidden fiber-preparation or conditional-mixing operation.

## 4. Uniform slab contraction

On |y|<=1/2,

    Delta(y)=kappa y^2(2-y^2),
    d=Delta_max/a=7 kappa/[16(1+kappa)].

Choose eta^2=7/[8(1+d)], which lies strictly between zero and one. For y!=0,

    Delta(eta y)/Delta(y)
      =eta^2(2-eta^2 y^2)/(2-y^2)
      <=(8/7)eta^2=1/(1+d)
      <=1/(1+Delta(y)/a).

At zero the undivided inequality is immediate. Subtracting from one gives

    1-Delta(eta y)/a >=1/(1+Delta(y)/a).

Raising positive terms to alpha>0 preserves the inequality. Restricting I_minus to the smaller physical slab and changing variables supplies the factor eta, yielding I_minus>=eta I_plus. The omitted part of the integral is nonnegative, so the inequality direction is correct.

Thus

    k_free/C_parallel <=cap_mu(A,B)/mu(A)<=k_free,
    C_parallel^2=(16+23 kappa)/(14(1+kappa)).

The upper bound is the ordinary y-only Dirichlet trial. For unit kappa the constant is sqrt(39/28); uniformly over positive kappa it is at most sqrt(23/14). This bound is independent of beta, alpha and the numerical coercivity constant. It is not claimed sharp for kappa tending to zero, and kappa=0 would fail the global longitudinal confinement premise.

The same k_free applies to all admitted angular U with fixed m,p,kappa,beta, so the ratio of any two true conductances is at most C_parallel, not its square. The conclusion concerns this equilibrium full-fiber conductance only. It does not guarantee equilibration from arbitrary starting points, fast angular mixing, Markovian projected paths or bounded passage times from a particular state.

## 5. Checks and relation to the radial construction

I reran `check_contraction.py` in a temporary directory containing the exact bound source, leaving its saved JSON untouched. All 62,730 rational pointwise checks passed. They check the finite contraction algebra, not the Sobolev/coarea/global-process proof, which was reviewed separately above.

This parallel bound can be stronger than the earlier radial-transport estimate without invalidating it. The two analytical trial constructions retain different information. The stated advantage in unit parameters, and removal of dependence on a numeric coercivity constant once existence is acquired, follow from the present proof. No blanket dominance over every possible sharper radial or other trial-current bound is inferred.

## 6. Strong ordinary primary comparisons

I read `SOURCES_AND_COMPARISONS.md`, SHA-256 `c4a97e3c4d769c078f7110b77822f9cc8688af3785574a8a4529105e47d127cc`, and directly inspected the relevant primary texts:

- Mangeat--Guerin--Dean, arXiv:1710.02699v2, Section VII, equations 98--103, derive a hard-channel effective-diffusivity lower bound from the unobstructed common channel. Their problem and observable are not this soft-potential basin capacity. It is a substantive prior channel-retention comparator, not merely trajectory simulation. https://arxiv.org/pdf/1710.02699
- Loper--Zhou--Geman, arXiv:1811.00205v2, introduction and Theorem 2, use local capacities under an explicit flatness condition to approximate small-target hitting probabilities, distinguishing these from passage-time information. It establishes relevant prior capacity-based avoidance of long direct simulations, not the precise current full-fiber multiplicative theorem. https://arxiv.org/pdf/1811.00205

The elementary common-channel-style estimate R(t)<=exp(a t) gives ratio R0/a^alpha=I_minus, which is only order alpha^(-1/2) at fixed kappa. The present proof retains all energy channels before comparison. This comparison does not prove that all stronger prior variational methods fail to give the same bound. Exact historical matching and practical significance remain open.

No denied source was retried; no held-domain application or physical operation was undertaken. Ordinary Cauchy, Dirichlet/Thomson, homogeneous scaling, Gamma transforms and Jensen are credited. This receipt accepts the mathematical conjunction and its explicitly limited consequence, not a new general algorithmic or physical claim.
