# Independent mathematical and physical-model review of frozen R44 and R79

Review date: 27 October 2026. This review concerns the actual frozen arguments in `physics_review_packet/R44` and `physics_review_packet/R79`, with governing scientific inputs in `cases/physical`. It does not treat either snapshot as a final producer endpoint.

**Decision: accept the mathematical results listed below at their stated scalar, rank-one, harmonic, ideal-contact ballistic scope. No substantive correctness blocker was found.** The finite total-spring optimum in R44 has its own necessary fourth moment and global five-root dual; it is not being inferred from the three-moment theorem. One nonblocking convergence-wording clarification for R79 is recorded separately. No frozen source was edited or silently repaired.

## 1. Accepted scope, without policy ranking

All numerical values in this table are for actual backbone mass `m=1`, total mass `M=2`, intercell spring `K=1`, and `theta=1/2`, unless the row explicitly states general resources. The objective omits the shared physical factor `k_B/(2 pi)`.

| Frozen argument | Accepted mathematical statement | Important scope boundary |
|---|---|---|
| Both: target `C_CM<=1/4` | The actual two-unit-mass, spring-4 pendant globally minimizes the full Bose integral over every admitted finite positive internal graph. `J=1.094388522317695923972117822366...`; active spectrum is unique. | Physical topology need not be unique; cancelled dark modes can remain. |
| Both: `C_CM<=1/20`, without a spring-sum cap | The exact infimum is `1.141916025317237323512979800758...`, with effective active trace `A*=3.398130336769495686903715...<4`. No admitted finite network attains it. Positive finite two-branch stars approach it, charging compliance and mass exactly. | The approaching sequences spend unbounded stiffness. The effective heavier backbone is a lower-bound spectrum, not a legal finite attaining cell with actual backbone mass one. |
| R44 `PROOF.md` Section 3 | The rational star with side masses `(1/20,19/20)` and springs `(5,1805/99)` strictly beats the optimized pendant under both `C<=1/20` and total spring sum `<=24`. Its sum is `2300/99`, and its saving is `0.000024495908790882159512...`. | This example alone does not prove optimality; the separate joint-cap proof does. |
| R44 `JOINT_CAP_PROOF.md` | At `C<=1/20` and total positive internal spring sum `<=24`, the exact finite two-pendant star defined by its fifth-edge residual is globally optimal over all admitted finite internal graphs. `J=1.142016098461582733349079543390...`. Two active internal resonances are necessary and sufficient at this point. | This is a finite-budget result, with two binding resource inequalities and three complete nonempty bands. It does not solve the entire joint-budget phase diagram. |
| R44 `FAMILY_PROOF.md` | The universal conditional five-root theorem, nonsingular analytic resource inverse, and an open analytic family of finite global optima near `(C,kappa)=(1/20,24)` are valid. All nine listed neighboring instances have exact interval certificates. | The inverse covers its proper five-root image; coverage of every feasible resource tuple and uniform conditioning are not claimed or proved. |
| R44 `PROOF.md` Section 5 | Uniformly over every admitted finite network at the fixed normalized masses, `J_rigid-J <= 0.398643595583964859020343... C_CM`. This coefficient is the exact sharp small-compliance slope for the unrestricted-stiffness infimum. | The sharp sequence uses `H=C^(-2)`. The approximately `1.05550848` ratio concerns leading savings, both tending to zero, not a 5.55% reduction in total conductance or a fixed-budget device. |
| R79 `PROOF.md` Section 2 | For every fixed positive `K,theta`, `M>m>0`, and finite positive compliance cap, the all-network infimum equals the displayed minimum over two-band parameters `(A,r)` with `B<A<=A0` and `(A-B)/r^2<=dmax`. The minimizing pair and active spectrum are unique. Attainment occurs exactly in the `A*=A0` case; otherwise the positive three-band approximation and nonattainment alternative hold. | This is an implicit exact family/optimization theorem. The plotted or isolated numerical crossing near `C=0.0715548` is not a separately proved complete phase diagram or unique threshold. |
| R79 `PROOF.md` Section 4.2 | Its explicit positive finite star at `C=1/20`, with total internal spring sum `135344623/1943210 = 69.6500239294775...`, has full `J=1.141944111902213589820156529024...` and beats the optimized pendant by `0.000101275639858171896442...`. | The additional stiffness is an output cost. Its larger saving cannot be treated as an equal-stiffness comparison to the R44 cap-24 optimum. |
| R79 `FINITE_STIFFNESS.md` | General-graph feasibility requires `kappa>=1/Cmax`; equality has only one active pendant response. At `Cmax=1/20`, every budget `kappa_max>20` admits a finite positive two-branch star strictly beating the optimized pendant, whereas `kappa_max=20` cannot. The explicit `kappa<20.02` star saves `0.000000182670737317172171...`. | Strict advantage need not remain bounded away from zero as overhead tends to zero. The general optimizing value/order under arbitrary simultaneous caps is not supplied here. |
| R79 `FINITE_STIFFNESS.md` Section 4 | Every fixed finite spring-sum cap has a positive objective gap above the severe-cap trace-escape infimum, even when finite network order is unbounded. | This gives no quantitative gap formula or attainment theorem for every capped resource pair. |

These are accepted internal mathematical results, not merely unverified candidates. Historical priority, a material specimen, performance in vector or anharmonic models, and a practical device advantage are distinct questions not established by the packets or this review. None is imposed as a prerequisite for accepting the mathematical statements above.

## 2. Independently checked load-bearing facts

### Physical moments and full bands

For a connected cell, the unique translation vector has squared overlap `1/M` with the backbone force vector. The determinant lemma then gives

`prod(t+beta)/prod(t+alpha) = 1 + S q(t)`,

where `q(t)=1/(M t)+tau+O(t)` and `tau=(ms/M)^2 C_CM`. Its zero-frequency residue, logarithmic derivative at zero, and high-frequency trace yield respectively

`prod beta/prod_(alpha>0) alpha = S/M`,

`sum 1/beta - sum_(alpha>0) 1/alpha = M/S + (ms^2/M) C_CM`,

`sum(beta-alpha)=S/m`.

Thus the sign and factor in the negative-cubic moment are correct. At the normalized resources, `D=integral(chi_rigid-chi)/w^3=C_CM/4`, not its negative. Rank-one interlacing gives disjoint interiors and `0<=chi<=1`; all acoustic and optical bands therefore enter the same scalar objective. Dark eigenvalues cancel in the determinant ratio and contribute zero interval width, not an omitted conducting channel.

The static response identity is also sound: contracting `D(q)x=w` with the translation vector forces the backbone-force contraction to zero, leaving the same relative-CM compliance as `D0` on its translation-free space. This is an aggregate static readout and a Gibbs variance lower bound. It does not become a cap on every internal displacement or strain.

The independent script additionally constructs a connected four-mass graph with positive nonincident springs and non-proportional incident stiffnesses. Exact rational characteristic polynomials, a grounded static solve, and matrix traces verify all three resource identities and `E=16+8*kappa_incident`. This explicitly distinguishes incident from total stiffness without relying on a star-only calculation.

### Three-moment entire-series certificate

I checked the convergent Laurent-series Descartes argument, including zero coefficients, multiplicities and arbitrary positive compact intervals. Multiplying by a monomial and differentiating removes a coefficient-sign variation; Rolle gives the required zero bound. Local uniform differentiation is available for these entire functions. This is a whole-axis proof, not a frequency-grid extrapolation.

For R44's convention,

`F=w^3 g + lambda w^2 + 2 mu w^4 - eta`,

the normalized even coefficients are `B1=lambda-eta/3` and, for `n>=2`,

`Bn=lambda+mu*n*(2n-1)-4eta/[(2n+2)(2n+1)]`.

When `mu>0, eta>0`, they strictly increase to a positive tail. When `mu=0, lambda>0, eta>0`, they again increase to a positive tail. The negative constant and single positive cubic term give at most three sign variations. Three prescribed distinct endpoints exhaust the positive zeros with multiplicity, forcing the complete required alternating sign pattern. R79's convention is equivalent with `a=2mu` and `nu=-eta`; its scaled proof correctly handles arbitrary temperature and arbitrary log-multiplier sign in the proper quadrant.

For `R=F/w^3`, the normalized dual identity is

`J-J* = integral R(chi-chi*) - mu*(T-T*) - eta*(D-D*)`.

The compliance cap has the correct inequality sign. At zero trace multiplier, the trace resource truly drops out. This is why an effective trace below four can be a sharp lower bound without becoming an attaining physical network.

### Positive inverse and optimized comparator

Strict endpoint interlacing makes all residues of `q(t)` positive. Between adjacent poles, its derivative is negative and there is one simple zero. The reciprocal decomposition `1/[t q(t)]` has positive residues `rho_j=1/[-sigma_j q'(-sigma_j)]`, giving actual springs `rho_j` and side masses `rho_j/sigma_j`. Its value at zero fixes total mass, and its high-frequency limit fixes backbone mass. This supplies physical positive finite networks, rather than a relaxed indicator accepted without realization.

I independently reconstructed the displayed stars and both endpoint matrices, solved the rational response inverses, and integrated each complete band directly with 90-digit arithmetic. The resulting resources, components and conductances agree with the exact certificates. Those numerical reconstructions check implementation; the positive-residue argument and exact intervals carry the realization/sign claims.

The one-pendant comparator is optimized. The supplied whole-family theorem establishes one stationary global minimum and increasing objective above it. Its `k*=2.729088...` is below both required lower bounds `k>=4` and `k>=20`; consequently the relevant pendant choices are exactly 4 and 20, including when a common feasible upper spring budget is added. The target all-network certificate independently confirms the spring-4 choice.

### General infimum reduction and trace escape

For R79's two-dimensional minimum, all feasible degenerating boundaries tend to the rigid-chain objective, while a finite feasible member lies strictly below it. A compact strict sublevel set therefore gives an interior-in-`A>B,r>0` minimizer. The two resource constraint gradients are independent: `d[(A-B)/r^2]/dr` is nonzero there. KKT legitimately produces `a>=0,nu<=0` and complementary slackness. The three endpoint zeros exclude the remaining wrong multiplier quadrant; the `nu=0` case reduces to the supplied two-moment theorem. The whole-axis dual then proves globality and uniqueness over the spectral relaxation. This reasoning is not assuming that a local optimizer is globally correct.

Both explicit approximation mechanisms preserve original mass, trace, log moment and compliance. R79's compensating high band has fixed squared width `delta=A0-A*`; the moment formula for `t_H` has a positive denominator for sufficiently large `H` and tends to the required finite low spectrum. R44's hard branch has fixed positive mass and spring tending to infinity, with the other spring adjusted to keep compliance exact. Their simple finite roots converge, the high optical band moves to infinity, and its complete Bose tail vanishes. Equality in the lower bound would force trace `A*<A0`, proving nonattainment. The omitted trace is escaping to high frequency; it is not supplied by dark modes or free rigid mass.

### Fourth moment and the finite cap-24 optimum

For any normalized physical graph, direct expansion of `trace[(D0+4e_b e_b^T)^2-D0^2]` gives

`E=integral 4w^3 chi=16+8(D0)_bb=16+8*kappa_incident`.

Since total spring sum is at least incident sum, total `<=24` implies `E<=208`. The candidate is a star with total/incident sum exactly 24, so its relaxation resource equals the actual budget.

The cap-24 candidate's fifth-edge residual has rigorous opposite signs at the given rational `h` endpoints. Component positivity, strict interlacing, `nu_stiffness>0`, and `eta_compliance>0` are enclosed throughout the bracket. The entire-function coefficients, including the exceptional `n=1,2` terms, are correct. The candidate-specific `B1,...,B14` signs and positive derivative tail give exactly five sign variations. Five distinct edge roots therefore exhaust all positive roots. The expanded dual difference is

`J-J* = integral R(chi-chi*) - nu_stiffness*(E-E*) - eta_compliance*(D-D*) >=0`.

This proves the claimed finite global optimum under both caps for all finite internal topologies. One pendant cannot supply its three nonempty active intervals. I also checked the stronger general five-root bound in `FAMILY_PROOF.md`: the even-coefficient extension has

`B'''(x)=nu*(96x-72)+192eta*((2x+1)^(-4)-(2x+2)^(-4))>0` for `x>=3`.

The tail has at most three sign variations and an eventual positive sign; insertion of the prefix and the cubic gives at most five overall. The root/resource Jacobian is a strictly negative definite weighted Gram matrix. Four distinct vectors `(1/x,2x,4x^3,-x^-3)` span four dimensions by a cubic-polynomial argument. Thus the inverse-function and open-family conclusions are justified beyond the nine numerical instances. No global resource-image coverage follows merely from this local result.

### Uniform and limiting resource statements

R44's exact supporting dual has one simple root at `sqrt(2)` and one exactly double root at the certified `r0`. The three-zero bound counted with multiplicity excludes every other positive zero. Its negative set is the rigid acoustic interval, yielding `J_rigid-J<=eta0*C/4` uniformly in finite order and retuning. The displayed legal small-`C` star has soft side mass `b=C r0^2+O(C^2)`, hard spring `C^-2`, and exactly charged compliance. Expanding the finite characteristic polynomials gives the reported first-order acoustic deficit and optical width. Their difference has coefficient `eta0/4`; the high band contributes `o(C)`. This proves sharpness of the all-network small-compliance slope, while its stiffness diverges.

R79's feasibility inequality follows directly from weighted Cauchy-Schwarz at the backbone and the static energy identity. Equality forces all spring cost to be incident, equal static branch displacements and `k_j/m_j` constant; all additional side modes are dark. The branch-splitting variation is smooth at zero width, with exact moment derivatives cancelling. Its negative derivative is `R0(8)/16`; the stiffness derivative is exactly `255/128`. The strict-above-20 onset is therefore proved for every positive budget overhead, not inferred just from the negative pendant multiplier.

For a fixed finite stiffness cap, the severe-cap dual gap forces weighted local `L1` convergence to the trace-deficient optimizer. A uniform `E` bound controls the high trace tail by `E/(2R^2)`; `chi<=1` controls the low tail by `epsilon^2`. These imply convergence of total trace to `A*<4`, a contradiction. Arbitrarily many high bands do not evade this argument.

## 3. Errors, necessary clarification, and unproved promotions

**Substantive mathematical errors found: none in the accepted scopes above.** This conclusion follows from reading the complete governing proofs, code inspection, exact replay, and independent reconstruction; it is not inferred from prior packet audit labels or successful execution alone.

**Nonblocking wording clarification:** R79 `FINITE_STIFFNESS.md` Section 4 says the indicators converge on compact frequency intervals away from the zero endpoints without naming the convergence mode. The proved statement is local `L1` (equivalently the required weighted `L1` there). Whole-sequence pointwise convergence is not implied by the dual-gap estimate. Replace that phrase with “converges in `L1` on every compact subinterval of `(0,infinity)` separated from the three zeros.” The ensuing trace argument already needs only this statement, so no theorem or numerical result changes. This clarification was also explicitly identified in the frozen `helper/FINITE_BUDGET_AUDIT.md`; it is not presented as a new undisclosed producer error. The frozen originals remain untouched.

There is no mathematical blocker to the accepted statements. The following remain unproved and must not be promoted from them:

- A complete simultaneous compliance/spring-sum optimum and active-order classification at every feasible resource tuple.
- Global uniqueness of the displayed numerical fixed-trace transition or an entire phase diagram inferred from continuation/grid evidence.
- Attainment of the unrestricted-stiffness escape infimum by a finite network, or achievement of its sharp slope at a common fixed stiffness budget.
- Unique physical topology from unique active spectrum; a bound on every local displacement from a CM-compliance cap.
- Historical novelty, fabrication feasibility, robustness, realistic material advantage, or a method advantage over an equally informed conventional Foster/Stieltjes designer.

These are scope boundaries or separately open questions, not retroactive failures of the proved constrained mathematical results. A substantive internal audit is sufficient to accept those results at their actual scope; no external validation condition is added here.

## 4. Replays and independent artifacts

All writes and executions were confined to `review_physical`. Unmodified Python copies were placed under `review_physical/replay/{R44,R79}`. Executed producer scripts:

- R44: `helper/certify_dual.py`, `certify_finite_network.py`, `certify_envelope.py`, `certify_joint_cap.py`, `construct_joint_family.py`, and `check_asymptotic.py`.
- R79: `certify.py` and `network_check.py`.

Every assertion passed. The eight regenerated named outputs are byte-identical to their frozen counterparts, including the nine-point family certificate. `replay_comparison.json` records the comparisons. This establishes replay fidelity, while the analytic review above establishes the relevant argument scope.

I inspected outward rounding, signed reciprocal division, integer-square-root bounds, Taylor/geometric exponential remainders, alternating Machin-pi bounds, and the full positive Bose-tail series. No omitted optical tail or unchecked sign region was found in the exact numerical certificates. Proposing brackets with `mpmath` is separated correctly from the exact existence/sign enclosures.

`independent_checks.py` imports no producer module. It contains exact `Fraction` matrix/characteristic-polynomial checks and symbolic coefficient checks, plus independent 90-digit mass-normalized eigensystems and direct quadrature. `independent_checks.json` and `independent_checks.log` retain its outputs. It independently reproduces the target optimum, both kinds of severe-cap finite stars, the cap-24 candidate, the common escape infimum, the branch-splitting derivatives, and the sharp small-compliance diagnostics. Its floating diagnostics are explicitly not substituted for interval proofs or the analytic universal root bounds.

`replay_manifest.json` records copied-code provenance. `source_manifest.json` records hashes for the governing scientific proof/evidence files used. No scientific producer source was changed.

## 5. Exposure and limitations of review independence

I was given neutral packet identifiers R44 and R79 and the scientific review task. I did not read memory files, programme chats, Dots, dispatchers, admissions, orchestration policies, action files, early forecasts, live producer directories, snapshot metadata, or policy assignments. No user or producer thread was messaged; no chat, goal, automation, or subagent was created. No external sources were required for these self-contained mathematical claims.

The runtime instructions automatically included a broad historical memory summary. I did not consult or rely on it, and no specific study policy assignment was exposed by it. The frozen scientific inputs themselves mention earlier internal reviews and helper provenance. I read the actual helper proof and certificate arguments; after independently checking the main mathematics, I also read R79's existing finite-budget audit and result notes. Thus this review was blind to orchestration labels and forecasts, but not blind to the existence or stated conclusions of prior scientific audits inside the allowed packet. The convergence-wording clarification above is explicitly attributed accordingly.

This is a substantive internal mathematical/model audit, not a formal proof-assistant verification, historical-priority search, experiment, or audit of any later extension. The fixed scalar single-link harmonic ideal-contact model and its omitted physical costs remain the exact boundary of the accepted science.
