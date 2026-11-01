# Independent whole review: original constant-SPD Gibbs-conditioned MFPT

DRAFT — numerical/model acceptance is established; final cost-wording disposition is being recorded separately before freezing this receipt.

## Established result and scope

The frozen mathematical proof, raw-model parser, directed finite arithmetic and original-task receiver pass at their stated ordinary constant-SPD, quartic, EXACT FULL Gibbs|A mean-hitting-time scope. All 3,678 author tests replayed, all six saved cases were genuinely recomputed, and the report is byte-identical. Independently implemented checks passed1,958 assertions, including least-diagonal and least-pure-coefficient acquisition, root rounding, irrational constants, complete formula-(12) propagation, absolute-time scaling, all proof-field attacks and original-task recapture.

The source manifest initially received is `1f2c424f1d1ea9f1c1d9b68b03d0cd8dfa1cce4966a934f1be48f253aaba3aa9`; it binds15 explicit files and4 dependencies. The main implementation is `7c3a732589bec0aa4240c3970c84be2079421343f791ce68b2e4e92bd65b81ca`, and theorem is `bf9e83e1f39f25758dc02b10a06d06a955b98e61de172f633ba5d4f341a7d8e0`. No candidate code correction is needed.

One cost sentence in the original frozen arithmetic document is too broad: “These root costs are explicit and independent of angular dimension.” Only the number of root invocations is fixed at two. Nonsquare-root operands use2P scaling, and P=max(192,alpha*(bits(kappa)+2)+128) can grow with dimension. The independent exact witness in `root_cost_witness.json` reports386 versus1538 operand-bound bits for the same root argument at m16 versusm512. This is not a numerical defect or a lower bound on all possible algorithms; it is a correction to this implementation's cost description. The literal dimension-independent bit-cost claim is not accepted.

## Actual executed finite outputs

All cases use beta=kappa=d_min=1. Exact rational comparisons, not the displays, establish the reported targets.

| Fiber m | Actual mobility floor | Mean interval displayed | Total ratio displayed |
|---:|---:|---|---:|
|512|1|[4.19289284446448e36, 5.27036476987163e36]|1.2569757838742874|
|64|64|[6654.988857716751, 6999.720487971243]|1.0518004819579463|
|128|64|[214677829.3305657, 216084459.45972905]|1.0065522841066061|
|256|64|[4.567286514280587e17, 4.5880730112929184e17]|1.0045511699227405|
|512|64|[4.19289284446448e36, 4.212934895560057e36]|1.004780005556793|

The sixth case has m512, coupling10^100 and diagonal mobility(64,128,...,32768), rather than coupling20 and64I. Its exact outer interval matches the fifth because their acquired d_min and mu agree. This is NOT equality of their actual means or dynamics. Both models have distinct complete raw hashes. Each m512 case reads1,023 energy terms and523,776 exponent entries; isotropic mobility contributes one additional value, whereas the diagonal case reads all512 values.

The original M=I case is retained with its requested1.3 target. A requested1.01 is actually refused. There is no silent replacement of ordinary mobility by64I and no use of the earlier gamma512 gain. The author replay took16.799s wall and the independent suite14.825s, diagnostic timings only.

## Theorem-to-code join: full state, not a reused kinetic quotient

The already separate source-bound theorem receipt is `audit_constant_spd_mfpt_theorem_20261031_2239/THEOREM_REVIEW.md`, SHA256 `e5a7c357b9b52c9c1e2d39b1d9636a0e102f6d4c5359b75c5fca5b22ed211b9f`. Its6,175 exact theorem checks and all-point reasoning remain applicable to the unchanged main theorem. The whole implementation join was inspected anew rather than accepted merely from that receipt.

The process is ordinary Langevin with constant finite SPD transverse M, unit longitudinal mobility and zero cross mobility. Its proper Lyapunov function with K=1+kappa/p has

    LV=2(1+Km)/beta-2[yv'+Kp v]U <=2(1+Km)/beta-2pU.

This earns nonexplosion; there is no singular origin, engineered divergence field or squared-Bessel boundary requirement. The finite Gibbs law and local elliptic reversible form are the actual full-state process.

Homogeneous scaling gives q=v^-alpha and pi_y proportional to(beta v)^alpha exp(-beta vU). The constructed current is

    j_f=J_f pi_y (1,-v'z/(p v)),  J_f(y)=integral_-infinity^y qf.

Its full-z continuity identity follows from z.grad U=pU. Weighted Cauchy uses the actual inverse M, not1/(gamma u), and gives

    Q_f<=D_f=beta integral J_f^2/q [1+d(y)],
    d(y)=(v'/(pv))^2 E_pi_y[z^T M^-1 z].

M>=mu I, acquired coercivity, virial E U=alpha/(beta v), and concavity of t^(2/p) give the stated moment upper bound. No energy Markov closure, angular sampler, conditional mixing rate, committor or Poisson solution is assumed.

The killed discounted-resolvent identity, A/S source split and positive-resolvent Cauchy first earn finiteness and then the actual mean:

    M_A T_A=Q_A+Q_AS,
    L_A/M_A <=T_A <=(1+M_S/M_A)D_A/M_A.

The scalar trial is justified by extended-energy truncation, not an assumed L2 zero-inverse. Full infinite tails of J_A^2/q decay as x^(2-4alpha), while the full-z correction decays as x^(-2-8/p). The initial full conditional Gibbs law matters in these full-state source identities. Matching only the energy marginal or choosing a ray is not enough; the implementation explicitly rejects such altered initialization claims.

For quartics, c=d_min/m yields C=alpha/[8mu sqrt(beta d_min)]. The separate slab integration-by-parts estimate and global basin estimate are

    C_s=kappa/[2mu sqrt(beta d_min) a^(3/2)],
    D_max=4alpha max(kappa,1)/[mu sqrt(beta d_min)].

The finite outer formula is exactly

    low=beta M R,
    high=(1+a^-alpha/M)*{
      beta M R(1+C_s)+beta(1+D_max)[M S0+Wfar/M]}.

Every positive basin-tail and cross-source correction is retained. One-basin mass and full-slab resistance have the correct factors. The lower endpoint's coincidence with reciprocal scalar conductance does not make the upper/source argument capacity inversion. The actual model and mean remain different from earlier radial-gain and clamped-CDF services.

## Complete input, minimum mobility and coercivity

The public producer validates all external budget types before use, then accepts only exact constant-isotropic or constant-diagonal mobility syntax. Every diagonal entry is parsed canonically, strictly positive, and scanned before its exact minimum is acquired. An invented larger floor, unsupported dense matrix, mixed syntax, missing/negative last entry, radial-gain field or wrong dimension is rejected. The theorem's dense-SPD scope does not become an unimplemented dense-matrix parser.

The full quartic energy list is checked through the pinned energy parser: every exponent, coefficient, degree, sign, duplicate and pure coercive term. p must actually equal4 and alpha=m/4 must be an integer at least4. The smallest pure coefficient and mobility entry need not be the first or the e1 probe; independent tests put both minima last and recover exactly d_min=1/7 and mu=7/11. Coercivity then equals d_min/m, not an inferred convexity constant.

A synthetic zero tangent program and e1 are used only to reuse that parser. The acquisition removes tangent-weight, off-origin-SPD and initial-energy claims, renames the witness as an algebraic probe, records SPD EVERYWHERE for the actual constant matrix, and overwrites the model description and complete raw hash. No synthetic program is mistaken for actual dynamics or physical preparation.

Energy plus mobility coefficient bits are charged to one aggregate limit, with individual rational/string and input-size caps also enforced. Boundary tests pass at the exact total and refuse one below it. Initial law is fixed by the authenticated observable contract, not a raw field that an untrusted certificate can choose.

## Directed roots, integrals and total-width arithmetic

The inherited scalar routine is imported through two verified source hashes, and only its ordinary M/R integration and arithmetic are reused. The old model, gamma, initialization and mean formula are not inherited. An isolated harmless backend-byte alteration was actually tested and refused before import; original and clean replay trees were untouched.

For a positive rational q, the new root routine first detects perfect rational squares by exact numerator/denominator isqrt and equality. It returns the exact root in that case. Otherwise it forms floor(q*2^(2P)), takes its integer square root, adds1 and divides by2^P. Since floor(sqrt(floor x))=floor(sqrt x), this is a valid strict upper root within one dyadic unit of the true root. Tests use exact squared inequalities, values immediately above/below dyadic squares, tiny/huge perfect rational squares and exact operand-budget boundaries. No floating root is used.

Argument and scaled-shift bit limits precede the large operations. C_s uses the upper root of1/(beta*d_min*a^3), and D_max uses the upper root of1/(beta*d_min), with positive coefficients. Independent squared comparisons directly verify both factors for nonunit/nonsquare beta,kappa,d_min and diagonal mu. Monotonic propagation then uses Mhi,Rhi in positive numerator terms and Mlo in denominators. Independent formula reconstruction checks every resulting component and the cross multiplier.

M is integrated on separately monotone[1/2,1] and dyadic tail pieces; R is twice the decreasing half-slab integral. Directed powers and endpoint Darboux sums are outward. The entire remaining mass is bounded by

    T/(4alpha-1) * [kappa(T^2-1)^2]^(-alpha),

with its power rounded upward. Positive seed, cutoff, grid, point, operation and precision limits are finite. Analytical near/far source bounds replace—not assume—an inner cumulative-mass oracle.

The numerical M/R product width is checked first; the complete MFPT total ratio is checked afterward. Early failure of the current factor is a sufficient-bound refusal, not a physical impossibility. Actual mobility is never optimized behind the task. Exact equality at a total-ratio request passes; a stricter target refuses even after numerical tolerance is met.

Two useful independent scaling checks distinguish beta, mu and d_min rather than merely comparing saved numbers. Multiplying every quartic coefficient by9 and dividing mobility by3 preserves the interval, consistently with transverse coordinate scaling. Taking beta9 and mobility divided by3 multiplies both exact time endpoints by9. These checks pass and would expose misplaced temperature or mobility factors.

## Paid work and receiving semantics

For saved T=2^J and N>=128, all seed and prior-refinement points lie on the final nested grid, giving `(J+2)N+2` paid scalar points. There are J tail powers plus three correction powers. Each integer exponent alpha costs `1+2*(popcount(alpha)+floor(log2(alpha)))` guarded products including rational conversion. Thus m512 uses98,306 points,98,310 power calls and1,671,270 products, plus two separately counted root invocations. The independent ledger reproduces all six actual cases.

This is not a unit-cost real-RAM claim. Root bit cost, scalar-product bit cost, low-degree Fractions, raw storage/hashing, monotone sums, final rational arithmetic, serialization and repeated verification are real work. Product/root maximum-bit counters are limited proxies, not total peak memory or every intermediate. `max_operations` caps the stated guarded fixed products; it is not advertised here as counting all Python work or the separate fixed number of isqrt operations. Fixed precision, root/integral budget exhaustion and serialization can honestly return Unknown.

Receiving recomputes the entire raw/scalar operation from the ORIGINAL external task. It type-strictly binds task, acquired model/coercivity/minimum mobility, full generator, exact FULL Gibbs initial law, observable, exclusions, all constants/corrections, source multiplier, N/T/P, tail, total ratio and exact endpoints. Independent attacks cover every proof-bearing field, all terminal endpoints, weaker initialization substitutions and valid changed mobility. All six case tasks were reconstructed literally, not accepted from a certificate's chosen task. The standalone small raw case was also replayed with its literal README task.

Timing, work counters, display floats and additional outer certificate fields remain non-proof metadata. The independent replay directly recaptured work instead of misreading verifier PASS as authentication of arbitrary diagnostics. This is a Python callable interface, not a hostile-stream service; unsupported argument signatures are ordinary API errors, not false mathematical admissions.

## Zero-gap note, ordinary comparators and excluded future claims

The frozen zero-gap observation is sound. For h_R(y,z)=psi(-y/R) supported far inside the left tail,

    ||h_R||^2 ~ R^(1-4alpha),
    E(h_R) ~ beta^-1 R^(-1-4alpha).

The fiber derivative vanishes for every constant SPD M. These admissible zero-target-trace tests have killed Rayleigh quotients of order R^-2, so the killed spectral bottom is zero. When alpha>1/4, the squared mean is negligible relative to the norm, giving zero global Poincare gap as well. Fiber cutoffs justify form approximation. This demonstrates why a finite source-specific mean does not supply a bounded global inverse. It is not promoted to additional survival, exponential-moment, median or arbitrary-initial-state claims.

The source ledger retains strong direct exit-time/resolvent and spectral-gap alternatives; the mathematical proof here is self-contained. This whole review does not claim a new exhaustive priority search or independently reopen every recorded primary retrieval. Ordinary Poisson/current methods supplied the same explicit derivation reproduce this certificate. The Gaussian radial special case, full elliptic PDE/barrier solvers, simulations and averaging methods receive identical model/initial-law information. No universal runtime victory or historical novelty is accepted.

No physical parameters, generator, full Gibbs sampler, weighted initialization error, apparatus or mobility change was acquired or implemented. No source retry, laboratory/chemical/biological operation, outreach, publication or purchase occurred. The future uniform-survival lemma is OUTSIDE this freeze and this acceptance. Earlier radial, kinetic, conductance and theorem-only receipts retain their original scopes.
