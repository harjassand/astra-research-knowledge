# Independent whole audit: autonomous radial-gain Gibbs-conditioned MFPT

## Verdict and exact binding

**PASS for the declared autonomous engineered-diffusion theorem/code/receiving conjunction.** No frozen source correction was required. This independently accepts the finite actual mean-hitting-time consumer, not only the preceding theorem and not a reinterpretation of prior capacity or clamped-CDF outputs.

Bindings:

- Manifest `autonomous_radial_mfpt_20261031/FROZEN_SHA256.json`: `d56d3514bff7af7062137347065401df0364823c1223087471f9b036bb73f51e`.
- `receive_mfpt.py`: `607f90e242e47de87d217ca8e19aa16115780eeb10bdfc83a1e3d2dbf915cff0`.
- Current theorem: `ace4c744d82f83c843bee1a0f1602385fbc96ddb3b1913d1b4143d843852a704`.
- `check.py`: `c8b94aa59bc494f5a8b38f3cec37e56c2d306ffc3a66f576bcfe78e61cb1c095`.
- Pinned kinetic backend: `b4b75f4eb063e13a8c4fe49a34af5c55f182df87317a1cde4c0c14b3aefdf8cb`.

All **24 explicit files plus four dependencies** match frozen sizes/hashes. The current proof, code, author tests, arithmetic/cost/scope documentation, inherited raw parser, and source-bound theorem acceptance were inspected. Preserved boundary/citation history and failed CAS-check history are not relabeled current accepted execution. The preceding kinetic archive also matches its recorded 112,784 bytes and SHA256 `2184b8194297af716a12c89267c49dcc52f83b4dfd1377708bb1acd5296c9f2e`.

Accepted output is the **actual autonomous mean time to Y>=1/2 from exact Gibbs conditioned on Y<=-1/2**, or a full-state law with EXACTLY the same (Y,U) pushforward under this separately proved exact kinetic lift. The actual model contains positive radial gain gamma and the mandatory divergence drift. It is not ordinary constant-SPD Langevin, an arbitrary deterministic initial-state mean, an approximate-preparation guarantee, or a physical generator/actuator certificate.

## Executed evidence

The clean copied-tree author suite passed **2,052 assertions**, including all five actual saved cases under literal original tasks. The regenerated report is byte-identical to the frozen report. Wall time was 13.108s, diagnostic only.

The independent suite passed **2,015 assertions**. Coverage includes directed powers and exact Darboux references, exact polynomial resistance integrals, infinite-tail formulas, every separate formula-(9) correction with nonunit beta/kappa, every proof-bearing field, exact resource and total-width boundaries, full original-task recapture of all five cases including work counters, the standalone saved raw/certificate pair, and the ordinary Gaussian comparator. Sampling checks supplement, rather than replace, the all-point inequalities below.

| Fiber dimension | alpha | Exact interval displayed | Total ratio displayed |
|---:|---:|---|---:|
| 64 | 16 | [6654.988857716751, 6870.10383783736] | 1.032323867811014 |
| 128 | 32 | [214677829.3305657, 215693748.79026812] | 1.004732297987503 |
| 256 | 64 | [4.567286514280587e17, 4.5844122742646515e17] | 1.003749657467408 |
| 512 | 128 | [4.19289284446448e36, 4.209577975322795e36] | 1.003979384038002 |

Gamma=512 and beta=kappa=1 are actual declared model parameters. The first target is total ratio1.1; the remaining four target1.01. Exact rational comparisons, not the displays, pass. Both 512-fiber-dimensional inputs (513 full dimensions) give identical exact mean intervals despite coupling/tangent coefficients (20,1) versus (10^100,10^80). Their complete raw hashes remain distinct and received.

Each 512D fiber case reads 523,776 exponent entries, executes 98,306 scalar points, 98,311 integer-power calls and 1,671,295 guarded fixed products. These costs were recaptured and independently reconstructed, not trusted merely because verifier acceptance ignores diagnostic counters.

## 1. Actual generator, gain, global process and initialization

The tensor is `gamma zz^T/(p^2 U)+T`, with T tangent and the correct reversible divergence drift. The inherited pointwise closure, with its radial terms multiplied by the ACTUAL gamma, gives

    dY=-v'(Y)u dt+sqrt(2/beta)dW,
    du=gamma(alpha/beta-v(Y)u)dt+sqrt(2gamma u/beta)dB.

Longitudinal mobility remains one; changing gamma is not a free global time reparametrization. Tangent noise/drift annihilate every function of U, without mixing assumptions. For W=1+y^2+(1+2kappa/gamma)u,

    GW <= [2+(gamma+2kappa)alpha]/beta-gamma u.

The stopped coercive Lyapunov argument excludes infinity escape. The adapted energy rescaling and clock `gamma*exp(gamma integral v)/beta` give the same squared-Bessel dimension2alpha. Thus alpha>=1 excludes origin hitting; the finite consumer chooses the stronger integer alpha>=4. At zero the inherited boundary is inaccessible/no-killing (entrance in the stated Feller classification), not an artificial absorbing boundary. Positive tangent weight earns full SPD only off this unvisited origin; weight zero remains a valid rank-one case.

The reversible projected density is rho=q*pi_y, with q=v^-alpha and pi_y Gamma(alpha,rate beta v). The unknown angular partition is not evaluated. Exact all-start projection permits a singular-in-angle lift only when its (Y,U) initial pushforward is EXACTLY rho restricted to A and normalized. This permission is specific to the engineered closed model. A fixed ray is not a universal replacement for full Gibbs initialization in another kinetic model.

The program's e1 evaluation is correctly renamed an **algebraic energy probe**, not the physical initial state. Its observable initial law is an explicit fixed part of the authenticated contract. No symbolic law was secretly replaced by that witness, a point start or a sampler output. Small total-variation preparation error alone does not control the unbounded hitting-time mean; no such claim is accepted.

## 2. Zero-resolvent/source join: why this is genuinely an MFPT

On Omega={y<b}, use the killed reversible form

    E(h)=beta^-1 integral rho [h_y^2+gamma u h_u^2],

with zero target trace and the actual no-killing origin interface. At lambda>0, the killed Markov resolvent identity gives

    <1_A,R_lambda 1_Omega>
      = integral_A rho E_x[integral_0^tau_B exp(-lambda t)dt].

Sources A and S have finite L2 norm because rho has finite total mass. The ordinary variational identity for Q_f(lambda)=<f,R_lambda f> has the correct negative energy and negative lambda||h||^2 terms. Positivity and resolvent Cauchy give `0<=Q_AS<=sqrt(Q_A Q_S)`. No bounded inverse at zero, spectral gap, finite mean or Poisson minimizer is assumed.

For J_f(y)=integral_-infinity^y q f and w=-(v'/v)u, the current `j_f=J_f*pi_y*(1,w)` has divergence rho f because

    partial_y pi_y + partial_u(w pi_y)=0.

The inverse transverse form coefficient is **1/(gamma u)**. Weighted Cauchy therefore yields

    Q_f <= D_f = beta integral J_f^2/q [1+K(y)],
    K=alpha v'^2/(beta gamma v^3).

The conditional moment used is E_pi u=alpha/(beta v). This earns precisely the beta/gamma factors; replacing gamma u by an ordinary constant transverse mobility here would be invalid.

Scalar trials with h'=-beta J_f/q give `L_f=beta integral J_f^2/q <= Q_f`. The tail trial grows quadratically and may fail to be L2 near alpha=1, but truncating values, then taking compact y/u cutoffs and removing lambda in the proper order, yields the lower bound in the extended finite-energy sense. At alpha=1, an origin logarithmic cutoff has vanishing energy; no impossible positive-capacity zero cutoff is assumed. Current upper bounds extend from a compact core by form closure.

For y<-b, J_S=0; on the slab J_A=M_A and J_S<=M_S. Therefore `D_S<=(M_S/M_A)^2 D_A`. Finite D_A and D_S bound both diagonal resolvent limits and their cross limit. Only THEN monotone convergence earns

    M_A T_A=Q_A+Q_AS<infinity,
    L_A/M_A <= T_A <= (1+M_S/M_A)D_A/M_A.

The occupation cross term is retained, not discarded. A capacity formula does not supply this source identity. The lower endpoint later happens to coincide with reciprocal scalar free-energy conductance, but is proved as one positive slab contribution to a Poisson source energy, not asserted equal to the full mean.

## 3. Full tails and every constant of formula (9)

For x=-y in the left basin, M(x)=integral_x^infinity v^-alpha. Then M(x)^2/q(x)=O(x^(2-4alpha)), while K(x)=O(x^-6). The source currents have finite energy for alpha>3/4. This is a full infinite-domain statement, not a finite reflecting box, and the received lift/backend satisfy stronger hypotheses.

For integer alpha>=4, set b=1/2, d=1/alpha, a=1+9kappa/16 and c=v(1+d). On [b,1], v<=a; on [1,1+d], v<=c<=a; throughout [b,1+d], |v'|<=4kappa. With M(x)<=M, these give

    S0=(1-b)a^alpha+d*c^alpha,
    S1=(1+d-b)16kappa^2 a^(alpha-3).

No negative exponent is used to reverse the near-basin inequality. On x>1, v is convex and increasing, hence

    M(x)<=v(x)^(1-alpha)/[(alpha-1)v'(x)].

Using v'>=8kappa(x-1), v>=1, and alpha>=4 yields the complete far bounds

    integral_(1+d)^infinity M(x)^2 v(x)^alpha <= Wfar,
    Wfar=1/[64kappa^2(alpha-1)^2 d],
    integral_(1+d)^infinity M(x)^2 v'^2 v^(alpha-3)
      <=M/(alpha-1)^2.

Thus no nested cumulative-mass oracle is smuggled into the finite consumer.

The slab uses a separate, stronger estimate. On [0,b], W=v^alpha decreases, and

    K W <= [4kappa/(beta gamma a^2)] y(-W').

Integration by parts and evenness give integral_slab K W <=4kappa R/(beta gamma a^2). This estimate is not misapplied to the basin. M_S<=a^-alpha then gives exactly

    T_low=beta M R,
    T_high=(1+a^-alpha/M) * {
      beta M R[1+4kappa/(beta gamma a^2)]
      +beta M S0+beta Wfar/M
      +(alpha/gamma)M S1+alpha/[gamma(alpha-1)^2] }.

There is one left basin and one complete slab, with no missing factor2. The radial corrections have no extra beta. At unit beta,kappa and gamma512, the slab overhead is exactly0.0032. All nonzero basin/source corrections remain explicit and strictly positive in the tested certificates.

## 4. Complete raw acquisition and finite arithmetic

The raw schema binds complete homogeneous positive degree2/4 energy, complete-pair tangent generator and a canonical positive radial gain. Dimension is checked before allocating the witness vector. The accepted backend scans every exponent/coefficient, rejects duplicates, missing pure coercivity, wrong degree/sign, malformed rationals and BOOL/float aliases, and supplies the exact coercivity certificate. Its hash is checked before import; the new full raw hash includes gamma. An arbitrary matrix, rotated basis, initial-law field or different physical kinetic program is not silently admitted.

Only M=int_(1/2)^infinity v^-alpha and R=int_slab v^alpha require quadrature. Outward dyadic rational conversion plus directed binary powers encloses each integrand. Endpoint Darboux sums split q at its turning point1 and use the decreasing half-slab resistance. The internal integration interface explicitly rejects crossing the monotonicity join. Independent exact rational Darboux references and direct polynomial integration of v^alpha verify all relevant regions and every saved resistance.

For T>1, the complete remaining mass is bounded by

    T/(4alpha-1) * [kappa(T^2-1)^2]^(-alpha).

The power is evaluated outward above. A positive lower seed is required before cutoff search. Cutoff/grid/precision, total points and fixed-operation limits are finite. Actual cache accounting includes seed and prior-refinement points. At saved T=2^J and N>=128, all nested earlier/seed points belong to the final grids, giving exactly `(J+2)N+2` cached points. There are J tail powers plus four correction powers. A power n>0 costs `1+2*(popcount(n)+floor(log2(n)))` guarded products, including rational conversion; this independently reproduces every saved work ledger.

The numerical test first requires Mhi*Rhi <=(1+quad_relative)Mlo*Rlo. It then separately rounds a^alpha,c^alpha,a^(alpha-3),a^-alpha outward, uses Mhi for numerator terms and Mlo for reciprocal terms, and applies the full source multiplier. Finally it checks the **TOTAL** high/low against the original external request. Numerical tolerance does not erase transport/source slack. Exact equality at a requested total ratio passes; a stricter ratio refuses.

The early transport-factor gate is sound for this sufficient formula: every other correction is positive, so a factor already at or above the target cannot meet it. This does not prove a physical accuracy floor, and gamma is neither optimized nor altered behind the user's task.

## 5. Resource and receiver boundaries

All external budget integers are type-checked before use, and exact task rationals are strict positive Fraction values with bit caps. Raw energy coefficient totals exclude separately bounded tangent/gain fields; no all-input-bit counter is claimed. The initial witness arithmetic uses conservative rational prechecks. The inherited fixed engine guards products before executing them and counts the work, including constants/tails.

`largest_guarded_product_bits` is not an all-intermediate or peak-memory cap. Monotone sums, ordinary low-degree Fraction calculations, final reciprocals, products of interval endpoints and serialization have paid finite costs beyond that proxy. Exact serialization can return Unknown; optional floats may be null. No float determines an endpoint or acceptance. Unsupported grammar, finite-resource exhaustion, fixed-precision failure and unmet sufficient total width are honest refusals, not proof of unidentifiability.

Receiving recomputes from the original raw model and external task, then type-strictly binds dependency, task, complete acquisition, exact generator, observable, initial law, proof method, exclusions, every source/tail/near correction and constant, N,T,P, total ratio and every mass/resistance/mean endpoint. Independent attacks cover every one of these fields. Valid changed gamma or changed angular input cannot reuse an old certificate even if some scalar answer would coincide.

Timing/work/display fields and additional outer fields remain explicitly unauthenticated metadata. The independent run recaptured work rather than interpreting verification as authentication of submitted diagnostics. This is a Python callable, not a hostile-stream service; ordinary signature errors outside its callable contract are not false mathematical successes. The internal `acquire` helper expects its named budget dictionary; the user-facing supported whole consumer is `certify/verify` with the declared task signature.

## 6. Fair alternatives and precise nonclaims

An ordinary variational/Poisson-current implementation given this same explicit current reproduces these bounds. Ordinary Gaussian radial reduction gets the same exact scalar operation at matched alpha and actual kinetics; this is independently tested. Verified two-dimensional Poisson/barrier solvers receive the same model, initialization, gamma and certificates. No formal performance separation, priority result or new general CIR/variational primitive is inferred.

The source-bound theorem receipt already records the corrected inaccessible boundary terminology and the failed bibliography retrieval. This whole audit requires no new retrieval or denied-source retry: every mathematical step used is supplied and independently reasoned. No physical model inference, angular Gibbs preparation, fixed-ray apparatus, energy readout, controller, finite-bit weighted initialization guarantee, autonomous finite-time CDF, laboratory operation, publication, outreach or purchase occurred.

The requested constant-SPD extension is a DIFFERENT full-state theorem/model. It receives its own separate theorem-only review; neither its code nor any future numerical result inherits this radial-gain acceptance.

## Preservation and reproducibility

All work is in `audit_autonomous_mfpt_whole_20261031_2234/`. Run `python -B check.py` from its clean `autonomous_radial_mfpt_20261031/` subdirectory to replay the author suite, or `python -B independent_audit.py` from this receipt directory. The pinned backend is copied at its required source-relative sibling path. Original frozen sources/results/history and previous archive are unchanged.

`hash_verification.json`, `prior_archive_preservation.json`, `final_input_recheck.json`, author replay logs/report, independent test/results and this review are separately bound by `AUDIT_SHA256.json`. No operational failure or unresolved blocker occurred in this audit.

**Conclusion:** this package earns an exact finite outer interval for a genuinely autonomous, finite Gibbs-conditioned hitting-time mean under its declared positive-radial-gain engineered diffusion, with all global tails, source cross terms and numerical costs paid. It does not earn arbitrary-start latency, original constant-SPD dynamics, or approximate physical preparation.
