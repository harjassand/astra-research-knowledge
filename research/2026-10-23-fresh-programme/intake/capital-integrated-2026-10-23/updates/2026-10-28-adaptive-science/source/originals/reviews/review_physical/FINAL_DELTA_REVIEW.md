# Warm final-source delta review: R44_final and R79_final

27 October 2026. **Decision: accept the new mathematical claims below at their declared scalar, rank-one, harmonic, ideal-contact ballistic scope. No new substantive correctness blocker was found.** The earlier `REVIEW.md` remains unchanged and its acceptances stand. This is a warm, source-informed follow-up with prior packet/audit exposure, not a blind or fresh review.

I read both final `RESULT.md` files and the new governing proofs and code, inspected the relevant source diffs, and verified hashes of unchanged dependencies and foundations. I did not repeat the earlier passing target, general-infimum, cap-24, nine-point-family, or small-compliance checks. The new certificates were executed only in owned copies under `review_physical/delta_replay`.

## Accepted scientific deltas

| Final source | Accepted addition | Scope retained |
|---|---|---|
| R44 `BOUNDARY_PROOF.md` | The exact feasibility condition is `C_cap*kappa_cap>=1`. Equality forces an active one-pendant response. At `C_cap=1/20`, every spring budget strictly above 20 permits strict finite additional-mode improvement by the displayed mass/spring split. | Arbitrarily small slack gives existence, not a uniform nonzero gain or a common lower bound on added component mass. |
| R44 boundary certificate | The exact rational cell with masses `(1,1/10000,9999/10000)` and springs `(1/100,99980001/4999900)` has `C=1/20`, spring sum `1000300/49999 = 20.006400128002560...`, and full-spectrum saving `5.4891912382394915...e-8` over the optimized spring-20 pendant. | This particular split is not claimed optimal at its own spring sum. |
| R44 extended family | The five additional points at `C=1/20`, `kappa in {20.01,20.1,21,30,100}` have positive finite global two-pendant optima certified by their exact fifth-edge brackets and the previously accepted universal five-root theorem. Together with the earlier nine, fourteen distinct resource points are certified. | The finite list does not establish coverage of every intervening stiffness or a complete global phase diagram. The earlier local analytic-family result remains the source of the open-neighborhood claim. |
| R79 `JOINT_PROOF.md` | At fixed `m=1,M=2,K=1,theta=1/2`, under both `C<=1/20` and total internal spring sum `<=20.02`, the nested-root-defined finite positive two-branch star is globally optimal over every admitted finite positive internal topology. Its active spectrum is unique, and two active internal resonances are necessary and sufficient at this point. | The global result is proved by its own fourth resource moment and five-root certificate. It is not inferred from a three-moment certificate or a failed optimizer. |
| R79 joint certificate | `J_opt` lies in `[1.142045199292380356594718, 1.142045199292393889573449]`, with optimized-pendant saving in `[1.88249677872143150e-7,1.88249691405121882e-7]`. The exact root has finite positive parts and both budgets bind. | Rounded component values or an interval box containing values above 20.02 are not themselves the exact feasible tuning. Feasibility follows from the defining equations and existence proof. |
| R79 `RATIONAL_CELL.md` | The stated rational-decimal positive parts have exact total spring sum `20.0199`, exact `C<1/20`, three completely isolated bands, and full-spectrum saving `[1.83396196008489989e-7,1.83396196008489990e-7]`. | This is a strict feasible near optimum, not the exact transcendental optimizer or a proved manufacturing tolerance region. |

Using the two exact objective enclosures, the rational cell's objective gap above the joint optimum is between `4.853481863653161e-9` and `4.853495396631893e-9`. This makes “near optimal” quantitatively meaningful inside the model. It does not enlarge the physical claim.

## Independent checks of the new arguments

### Feasibility and the small split

For the normalized relative-CM force `f=(-1,m_1,...,m_n)`, the trial displacement with backbone zero and every side coordinate one has `f dot x=1` and energy `x^T L x=kappa_incident`. The compliance Rayleigh inequality gives

`C_CM >= 1/kappa_incident >= 1/kappa_total`.

This is valid on the translation quotient because `sum f=0`. The pendant with spring `1/C_cap` proves sufficiency. At product equality, both resource caps saturate, incident and total spring sums coincide, and Rayleigh equality implies `f` is proportional to `Lx`. Consequently no positive nonincident edge remains and `k_j=kappa_cap*m_j`. All branch natural frequencies coincide and only the aggregate pendant is visible. This confirms the boundary characterization over arbitrary positive graphs, not just the displayed star.

For R44's new split, `H=epsilon*v` and `k=(1-epsilon)^2/(C-epsilon/v)` preserve compliance exactly. The cost derivative at zero is

`v-2*k0+k0^2/v=(v-k0)^2/v=64` at `v=100,k0=20`.

The new squared eigenvalues have first-order shifts `epsilon*v^2*G0(v)` and `epsilon*v^2*Gpi(v)`. This follows from the Schur complement: the extra mass-normalized diagonal is exactly `v`, its coupling is `-v*sqrt(epsilon)`, and the old block changes smoothly by `O(epsilon)`. The old roots and the new root are separated at zero. Thus the width expansion has a controlled `O(epsilon^2)` remainder. At `v=100`, `G0=1/75`, giving the exact positive width coefficient `gamma=80/213`.

The old positive edges are zeros of the fitted three-moment dual. Their first-order contributions to the integral of that dual vanish. Exact log, trace and compliance matching then gives `J'(0)=gamma*R1(10)<0`. I independently differentiated the complete finite characteristic-polynomial spectra and their direct Bose integrals; the result agrees with `-0.0005490208372578455244908...`, while the spring derivative equals 64. The positive finite rational member independently reproduces the stated gain. The proof of strict improvement for every positive slack is therefore justified; a negative fitted multiplier by itself is not being treated as a construction.

### R79's new finite global optimum

The graph-wide stiffness resource remains essential. For all normalized admitted graphs,

`E=trace(Dpi^2-D0^2)=16+8*kappa_incident <= 16+8*kappa_total`.

The stated cap implies `E<=4404/25=176.16`. The candidate is a positive star, so total and incident costs coincide. Its endpoint formulas preserve the other three resources exactly: trace 4, logarithmic product 2, and inverse endpoint sum `21/40`, equivalently `C=1/20`.

I separately simplified the candidate cost. With `A=4-delta`, the same denominator `den` used to define `t`, and `B=2H/(H+delta)`, it is

`kappa = [(A-B)^2/den + delta*(H-4+delta)]/4`.

This agrees with `t+H-c`. I checked the displayed partial-derivative formulas by differentiation of the defining rational functions. Their interval signs, the opposite stiffness residual signs at the broad delta endpoints, and exclusion of zero denominators give one continuous differentiable `delta(H)` throughout the H bracket. Positive `kappa_H` makes that branch decrease, so its endpoint isolations bound every intervening delta. The two fifth-edge residual signs are evaluated on this exact-cost branch, not at independently rounded pairs. Thus the nested IVT construction really supplies a simultaneous exact-budget and five-edge object.

The cubic interpolation coefficients are correct. For the entire function `Q=F*sinh^2(w)/w^2`, I checked the coefficient shifts and the exceptional low indices. The exact signs for even indices `0..17`, together with the inserted positive cubic, give five variations. For `n>=18`, division by `d_(n-2)>0` gives

`b + 4a/U_n + 16lambda/V_n + 64nu/Z_n`.

Here `lambda>0`, `a<0`, `nu<0`, and the certified lower bound obtained by dropping lambda is positive. The negative terms increase toward zero with n. Therefore the entire infinite tail is positive. The previously audited convergent-series Descartes lemma applies, and the five distinct prescribed roots exhaust the positive roots with multiplicity. This certifies the whole frequency axis and all three bands.

The dual difference is correctly signed:

`J-J* = integral R(chi-chi*) - nu*DeltaW - (b/4)*DeltaE >=0`,

because `nu<0`, `DeltaW>=0`, `b>0`, and `DeltaE<=0`. All differences converge near zero and infinity for finite connected spectra. Equality forces the same active spectrum. Any second nested root in the isolating box would have the same proper certificate, budgets and spectrum, hence the same high-band start and width. The asserted local root uniqueness follows without assuming it in the existence construction.

Independent 90-digit reconstruction gives

`delta=0.005773477588268574504105907852...`,

`H=73.338463669231653669647467607215...`,

`J=1.142045199292387123084083548537...`.

The positive reciprocal-response inverse, original mass-normalized endpoint matrices, CM response, complete bands and spring sum agree with the certificate. The direct partials are approximately `kappa_delta=3.47007762893651` and `kappa_H=0.000974158694706`, consistent with the branch argument. These floating reconstructions support implementation; they do not replace the exact nested-root and whole-axis proofs.

### Explicit rational cell and extended certificates

For R79's rational cell, I independently formed the physical mass and stiffness matrices with exact Fractions and computed `det(tI-Mass^(-1)L)` by a generic determinant. Both characteristic polynomials agree with the specialized coefficients used for root isolation. The three disjoint cubic sign brackets exhaust all beta roots, and the exact quadratic gives the alpha roots. Positivity and strict interlacing include the highest optical band. Direct all-band quadrature agrees with `J=1.142045204145875753226610...`. The exact compliance fraction and both strict resource margins match the report; the spring margin is exactly `1/10000`.

For R44, the extended candidates inherit the earlier accepted global conditional theorem only after their own exact root existence and proper multiplier signs are verified. I replayed all five new certificates and independently reconstructed the two extreme new budgets, 20.01 and 100, including full positive stars and direct all-band quadrature. Their values match the new enclosures. The five points remain individual certified optima; they do not prove an interval of global resource-image coverage.

The interval-library change uses recursive halving and squaring for positive exponential arguments above 16. Each step preserves inclusion because the enclosed exponential is positive; halving terminates in the already audited Taylor regime. This legitimately extends the old limited argument domain. The cap-100 high-band endpoint is about 24.7944, so its integral calls need exponential arguments near 49.6. The larger domain is relevant to the new certificate. Earlier certificates stayed inside the previous supported range; no earlier mathematical error is repaired by this extension. The generic `components` extraction is a refactor of the same exact positive-star construction.

## Repairs, preserved failures, and remaining limits

1. The earlier nonblocking R79 wording issue is now repaired in the frozen final `FINITE_STIFFNESS.md`: the convergence statement explicitly says `L1`. No theorem changes and the original audit remains preserved.
2. R79 `explore.py` now filters nonpositive inverse-moment denominators and candidates whose proposed high band does not follow the low bands. The earlier script could print infeasible exploratory values; those values cannot be counted as realized positive networks. The new `EXPLORATION_NOTE.md` explicitly preserves that failure. The accepted earlier theorem only used sufficiently large H, and each accepted finite example had its own positivity/interlacing certificate, so this diagnostic repair does not invalidate those accepted results.
3. No new substantive error or required repair was found in the accepted final mathematical proofs or certificates. The earlier R79 statement that an exact jointly charged point remained open is superseded at cap 20.02 by its new proof; the general arbitrary-resource joint frontier remains open. The earlier R44 cap-24 result and analytic local family remain accepted unchanged.

All gains are small normalized model effects. Neither a finite list of exact optima nor a scalar root certificate establishes a practical thermal device, individual displacement/strain limits, connector mass, vector-mode behavior, finite-contact performance, anharmonic robustness, historical novelty, or an advantage over the equally informed conventional design class. The unbounded-stiffness escape infimum remains nonattained by finite cells. None of these separate open physical or historical questions is imposed as a new condition on mathematical acceptance.

## Evidence, provenance, and exposure

Executed new producer scripts: R44 `certify_boundary_split.py` and `construct_joint_extended.py`; R79 `joint_certify.py`, `rational_cell.py`, and `joint_network_check.py`. Every assertion passed, and all five generated named outputs are byte-identical to their frozen final counterparts. Exact replay details are in `delta_replay_comparison.json`; copied-code hashes are in `delta_replay_manifest.json`. Unchanged foundations/dependencies and the new scientific inputs are recorded in `delta_source_manifest.json`.

`independent_delta_checks.py` imports no producer module and reruns no earlier check suite. Its exact rational polynomial/margin checks and independent 90-digit reconstruction are retained in `independent_delta_checks.json` and `.log`. These artifacts supply meaningful independent checks of the new costs, splitting derivative, extended family endpoints, nested optimum and rational realization.

The review intentionally carries forward prior scientific source/audit exposure described in the original report. Final result and reproduction notes additionally expose the producers' stated internal review conclusions; those labels were not used as substitutes for argument checking. I did not open the new helper audit reports. `R79_final/SOURCE_NOTE.md` contains the opaque local provenance label `p47`; I observed that literal label, did not access such a directory, and have no policy/forecast mapping for it. This is recorded as an actual provenance-label exposure, not concealed as full blindness.

No memory files, programme chats, Dots, dispatcher/admission/policy/action/forecast files, live producer directories, or policy assignment mappings were consulted. No thread messages, new chats, goals, automations, or subagents were created. No external research was needed. This is a substantive warm internal mathematical/model audit, not a fresh blind audit, formal proof-assistant verification, experiment, or historical-priority clearance.
