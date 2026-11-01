# Independent whole review: mixed-degree geometric dilation

## Verdict and frozen scope

**PASS** for the main geometric-dilation capacity sandwich, the genuine geometry-only counterexample, and the standalone exact raw producer/receiver. No source correction was required. This is separate from the earlier homogeneous, exact-mobility-range and finite-Jensen acceptances. In particular no angular-independent exact parallel endpoint or exact open attainable range is inherited.

I read the complete main proof, failure proof, executable, author tests, README, costs and source-scope record. All twelve files bound in `FROZEN_SHA256.json` were checked unchanged. Core bindings:

- freeze: `03e9781f38afc9d25aa022024a3bfa5b1184a682475bc7c03a38862b5b554d5f`;
- `PROOF_CANDIDATE.md`: `9a18d02f3c47a15c2f9d0b4c6b1fa5710cc4247fdb166430e80654b57fc22a3e`;
- `GEOMETRY_ALONE_FAILURE.md`: `b72d86c7d03a6306910cfe3ad8f2b6a15d5efd914a4a8fb2792a6c9c37e07e1b`;
- `receive_dilation.py`: `d760c77b7efaa81bdb3ee424fd818359840d1da767fba4398c177a63f93bf4e8`;
- `check.py`: `f3b31e882ee4fa17813d4106a5a2313b944e634341255aa20f51a8d6f1091e51`;
- `results.json`: `229fe3757b6a7bb625e2658fe050cfdafea683904a8598f2f4914af83650daf5`;
- `check_results.json`: `94528578cd3a937a498393acc81a50bf30a11eb4df8a454fd84d1e9377fda2dd`;
- `RECEIVING_AND_COSTS.md`: `bdcafacda6db053576b50e8770c08e907d82ff60faeaa82c6e0c9e5a213b47ad`;
- `SOURCES_AND_SCOPE.md`: `a3c1f23a68169dde90cc8d91177e7b7d5436d13d43e2c216300b683d53417ac0`.

The code is Python-standard-library-only, with no predecessor source dependency. Original sources, saved certificates/timings and earlier archives were not mutated. Immutable candidate/pending headers are retained; this later source-bound receipt supplies acceptance at the stated scope.

## 1. Spatial cancellation and actual model

The physical potential is F(y,z)=U(s(y)z), not v(y) times one homogeneous energy, with s=1+kappa(1-y^2)^2. The change of variables x=s z gives the exact conditional partition s^-m Z_beta, where Z_beta is the entire unknown mixed-energy integral. It need not be a power of beta. Thus q=s^-m is independent of energy coefficients and beta, but the capacity itself retains the explicit1/beta Dirichlet factor.

The model family consists of every fixed finite constant SPD transverse M, unit longitudinal mobility, zero cross mobility and the matching reversible drift/noise. The scalar trial has no transverse gradient; dropping the nonnegative transverse energy supplies the lower fixed-fiber inequality. Neither step requires identifying M. This is a quantified mathematical family, not physical membership learned from polynomial coefficients.

The basins are the actual full fibers at y=+/-1/2. Weighted H1 slicing/traces and truncation to[0,1] give the stated condenser variational class, with either orientation of the0/1 labels equivalent by h->1-h. The projected y drift generally depends on z. No Markov projection, angular equilibration, arbitrary-state passage-time equivalence or sampler is assumed.

## 2. Jensen, beta and the radial comparison

For s0=1+kappa, F0=U(s0z) and R_z=integral_slab exp(beta F_y)dy, define

    S(z)=integral_slab exp[beta(F_y-F0)]dy.

Then integral dz/R_z = Z0 E_rho0[1/S], where Z0=s0^-m Z_beta and rho0 is proportional to exp(-beta F0). In particular

    E_rho0 exp[beta(F_y-F0)]
       = Z0^-1 integral exp[-beta(2F0-F_y)]dz.

This sign and the beta factor are correct; the expectation is not with respect to an untempered or differently normalized fiber.

For each nonnegative homogeneous component of degree d<=p, concavity of t^(d/p) gives2-r^d >=(2-r^p)^(d/p), where r=s/s0<=1. Multiplying by that component and summing proves

    2U(s0z)-U(sz) >= U(s0(2-r^p)^(1/p)z).

A SECOND spatial change of variables, not an energy-Gamma identity, yields E S <= integral(2-r^p)^(-m/p)dy. Jensen gives E[1/S]>=1/E S. The moments are legitimate: positive components earn radial monotonicity, so 1/R_z is bounded by the integrable exp[-beta U(s_min z)]; the positive Tonelli integrals and comparison bound also make E S finite. Coercivity makes Z_beta positive and finite.

Dividing by the actual basin mass Z_beta MA/Z leaves the lower denominator

    s0^m integral(2-(s/s0)^p)^(-m/p)dy
      = integral[s0^(2p)/(2s0^p-s^p)]^(m/p)dy = R_plus.

The final bounds1/(beta MA R_plus) and1/(beta MA R0) therefore have exactly the claimed normalization. No residual s0 power or unknown partition is missing. The scalar proof objects need not be sampled or implemented as normalized densities.

## 3. Organizing condition versus acquired grammar

For smooth U, f(t)=U(t^(1/p)x) satisfies

    f''(t)=[D^2U-pDU](t^(1/p)x)/(p^2t^2).

Thus a global pDU-D^2U>=0 certificate gives radial p-concavity. If U>=0 globally, such a concave ray function cannot have a negative derivative, since its supporting tangent would eventually become negative. This earns DU>=0. Coercivity/integrability remains a separate condition. The degree8 example in the proof has pDU-D^2U=12x^2-16x^4+12x^6>=0 and U>=3x^2/4+x^8, as claimed.

This broader criterion is THEOREM-ONLY here. The executable never assumes a global polynomial-positivity oracle, supplied useful basis or arbitrary SOS decomposition. It acquires only a positive diagonal quadratic component plus nonnegative quartic monomials. Negative components can be admissible to the organizing theorem yet correctly return UNKNOWN under this sufficient finder. One must not erase the radial condition after recognizing geometric partition cancellation.

## 4. Conservative full diffusion and physical tail

The physical z derivative includes the chain-rule factor s. Defining D=z.grad_z F=sum_d d s^d U_d>=0 gives F_y=(s'/s)D. For each fixed SPD M, the coercive Lyapunov function

    V_M=1+y^2+(1+kappa)z^T M^-1 z

has drift -2[y s'/s+1+kappa]D plus diffusion trace2[1+(1+kappa)m]/beta. Since y s'>=-kappa and s>=1, the bracket is at least1. Smooth local coefficients and this stopped Lyapunov bound establish nonexplosion. Finite Gibbs mass and constant block mobility with the matching noise/drift give the reversible Dirichlet process. No uniform relaxation modulus as M becomes singular/large is asserted, and the analytical inverse M is not executed.

For y>=T>1, s>=kappa y^4(1-T^-2)^2, so the explicit tail is

    kappa^-m(1-T^-2)^(-2m) T^(1-4m)/(4m-1).

It is finite already at physical m=1. This exponent is NOT the maximum energy degree p or m/p. The scalar program uses exactly this rational tail. No reflecting boundary or physical finite box replaces the full process.

## 5. Genuine geometry-only failure

The companion U_R(x)=(x^2-R^2)^2 has the SAME q=s^-1 for every R, while its negative quadratic component violates the radial premise. The obstruction is not a missing normalizer or invalid diffusion.

The constants c1=8065/4096 and c2=7121/4096 correctly bound s on the stated center/edge intervals. With t*=2/(c1^2+c2^2) and A=(c1^2-c2^2)/(c1^2+c2^2), either z^2>=t*R^2 forces the center energy above A^2R^4 or the complementary case forces it on the edge interval. Each usable interval has length at least1/8. Hence the compact z portion contributes at most32R exp(-A^2R^4) to integral1/R_z.

For |z|>2R, the quartic bound and convex tangent at2R give the tail exp(-9R^4)/(9R^3). The normalizer lower bound follows from |x-R|<=1/(4R), where |x^2-R^2|<=9/16, producing Z_R>=exp(-81/256)/(2R). With R0=443/240, their ratio gives the stated exponentially vanishing upper bound on k_parallel/k_free.

For each fixed R the fixed-fiber committor has exact parallel longitudinal energy. Its normalized-integral derivative obeys a polynomial-in-z bound by2 sup_y|F_z| on the compact slab; exp(-F) has a uniform quartic tail there. Its transverse energy is finite and matching boundary values give a global H1 extension. Thus adding gamma times that finite energy and letting gamma down to zero transfers the obstruction to SMALL BUT STRICTLY POSITIVE finite transverse mobility. No singular admitted diffusion is used.

The global process also checks: D=4(sz)^2[(sz)^2-R^2]>=-R^4. Writing t=y^2, y s'/s=4t(t-1)/(t^2-2t+2) lies in[-1,6]; the corresponding polynomial inequalities are5t^2-6t+2>=0 and2t^2-8t+12>0. With the chosen quadratic Lyapunov function the bracket lies in[1,8], giving LV<=16R^4+6. Fiber coercivity and q~y^-4 give finite Gibbs mass. Therefore the counterexample genuinely proves that geometric marginal knowledge alone cannot give the asserted positive universal relative lower bound.

## 6. Entire raw acquisition, not selected-coefficient recognition

The producer strictly scans the complete supplied coefficient dictionary in actual physical coordinates, with dimension, monomial, exponent-entry, individual and total coefficient-bit budgets. It checks strict integer exponent vectors, canonical rational coefficients, duplicate/zero terms and allowed total degree.

The degree-two part must have positive pure diagonals in all but one coordinate. That unique absent coordinate is acquired as y. The y^2/base ratio for one transverse quadratic term is -4kappa/(1+kappa); the code derives t and requires0<t<1. It reconstructs U2, U4, all signs and q_min, then constructs and compares EVERY coefficient of s^2 U2+s^4 U4 through total degree20. Other degree/sign/axis terms are not omitted merely because the Hessian looked favorable.

Pure quadratic inputs are admitted with p=2. With any nonzero quartic component p=4; quartic diagonals need not all be positive because U2 alone gives U>=q_min||z||^2. Positive mixed quartics may be nonconvex, as the stated Hessian example demonstrates. A rotated/non-diagonal quadratic form, negative component or unsupported raw basis can soundly be UNKNOWN. No coefficient positivity or coordinate-learning oracle is hidden.

The hash includes dimension and the canonical full polynomial; exact reordering does not change the model. Changing graph/coefficients must still pass full acquisition even when scalar outer bounds are identical. The old exact homogeneous angular-independent parallel endpoint does not follow from this parser or this proof.

## 7. Exact arithmetic, total budgets and requested width

At rational y, q=s^-m and R0's integrand s^m are rational. For R_plus the code forms s0^(2p)/(2s0^p-s^p), then reduces m/p by gcd BEFORE selecting rational, square-root or fourth-root arithmetic. Integer division and nested isqrt give outward dyadic bounds, with exact equality detection. Negative rational exponents for q/tail are handled exactly.

All profiles are positive. On the half slab, s decreases and the denominator2s0^p-s^p increases; R_plus's integrand is decreasing and at least s^m by the stated squared-difference identity. Endpoint Darboux sums thus have the correct orientation. q is integrated on separately monotone[1/2,1] and geometric[1,2],[2,4],... pieces; both resistances are doubled half-slab integrals. The explicit infinite tail is added only to the mass upper endpoint.

Every integrand type has a separately counted cache key, sharing only profile arithmetic. All attempted-refinement cached values count against one evaluation cap. The preliminary necessary final-grid count is correct for the dyadic cutoff: q contributes(J+1)N+1 points and the two resistances each N+1, total(J+3)N+3. Extra seed points are additionally charged by the actual cache guard. The seed must resolve positively; cutoff/grid/precision and evaluation budgets bound termination.

Power/root-shift guards run before their expensive exponentiations. They do not cap all low-degree profile arithmetic, accumulated Fraction sums, final reciprocals or serialization; those actual costs and the limited largest-power diagnostic are documented. Python's exact string limit returns UNKNOWN rather than a rounded proof field.

Refinement checks a numerical product ratio for all three positive integrals. The final exact endpoints are[1/(beta U_M U_plus),1/(beta L_M L0)], with their TOTAL ratio separately compared against the external request. Structural slack can force UNKNOWN despite arbitrarily fine arithmetic. No unbounded accuracy-forcing loop or fixed factor masquerading as the requested total width is present.

The verifier recomputes from ORIGINAL raw input and external task, recursively binds all acquisition fields except seconds, model/family/task scope and all twelve endpoints, and rejects bool/float aliases. Optional displays, timing and reported work counts are not proof-bearing or authenticated. The result is a universal fixed-SPD family OUTER enclosure; actual membership, exact parallel endpoint equality, inverse mobility and experimental calibration are explicitly not supplied.

## 8. Executed independent checks and preservation

All author scripts were run in `producer-workspace/dilation_review_20261031`, not the frozen directory. The complete **3,936 author assertions** passed, including ACTUAL recomputation of all nine saved certificates and the additional nonfirst-axis saved raw fixture. The regenerated report is byte-identical to the frozen one.

I separately implemented **1,183 exact checks**: reduced rational/square/fourth-root enclosures including negative powers; independent exact rational Darboux references where m/p is integral; physical-m tail identities independent of p; both constant-shifted radial-well raw representations rejected; barrier dichotomy at963 exact test points; nonfirst-axis/coefficient acquisition; exact total-evaluation and requested-width boundary tests; recursive task/model/acquisition aliases; all six interval endpoint corruptions; missing scope and exact input-entry/bit budget saturation.

Unique artifacts in `audit_control_agent_20261031_2027/`:

- `check_control_audit.py`: `eefb6f3f8c1f4a2b1c70475f8c56c58941495ae6d5ceaf85ee7ef3023cc567a8`;
- `independent_control_results.json`: `5e65a2732a222a17b722d9198b8fe3613792a1da5ee410a704dd1e57ee7b14ff`;
- `author_replay_results.json`: `94528578cd3a937a498393acc81a50bf30a11eb4df8a454fd84d1e9377fda2dd`.

The independent script runs beside a COPY of receive_dilation.py and prints its results. Author scripts regenerate report files, so reproduce them in a copied directory. Tests supplement the proof, not certify all infinite-dimensional variational/process premises by themselves.

## 9. Finite consequence, costs and comparisons

The513D mixed chain has11,767 raw monomials and6,036,471 exponent entries actually scanned. It pays262,147 distinct scalar evaluations, N65536, cutoff2,2688-bit precision and largest observed powered numerator/denominator35,841bits. The exact family outer interval displays approximately[2.413067788904625e-152,2.429308909946876e-152], ratio1.006730486859<1.01. The report's roughly93-second producer timing is diagnostic, not a controlled speed comparison or total audit cost; verification here genuinely repeated the computation.

This is finite known-model geometric prediction without evaluating the mixed U partition, not an assumption that all mixed-degree fibers are homogeneous. Equal outer answers after acquisition do not imply equal actual rates or parallel endpoints. The organizing condition supplies information beyond q alone, as the failure proof shows.

Spatial Jacobians, Dirichlet/Thomson, fixed-fiber Cauchy, Jensen and radial concavity are ordinary primitives. Equally informed ordinary methods with the same proof can reproduce the result. Existing fixed-channel, soft-channel, capacity and sampled variational methods remain strong comparators. I have not promoted the bounded bibliography into an exhaustive historical search or independently re-read every newly cited primary paper in this audit. No new external action was required. There is no new priority, generic positivity, physical/hardware, MFPT, sampler or general complexity-separation claim.

**Conclusion:** the new geometric proof, its nontrivial scope obstruction and the standalone raw-input/finite-arithmetic receiving conjunction are sound at the frozen scope. All prior accepted source families and all current frozen originals remain unchanged.
