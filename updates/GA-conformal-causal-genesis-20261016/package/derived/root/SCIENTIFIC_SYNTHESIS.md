# Astra GA: nonlinear conformal calibration, weighted compensation, and causal acquisition

16 October 2026. Inspected main: **f80a8f15137575133ad2c9af975513b32e8fa93e**. Incoming producer mathematics inspected older main **3dde9ce74d829a93388e64032d27351b36dd2221**. Source-preservation commit: **f116469ee41bdc54a155099175b8ce063be98edd**. This report concerns this round's actual inputs and research; previous worker activity is not counted as current deployment.

**Outcome:** substantive restricted mathematics survives reconstruction, including a direct positive conformal Jensen theorem with a rational certificate, a complete weighted polynomial classification, and a precise concentration obstruction. No extraordinary discovery, unrestricted positive-core quasiconvexity theorem, new physical control, or technological superiority has been established. All new high-impact claims remain **source_derived_unreviewed**. Historical priority, external correctness, and physical acquisition are separate unresolved questions.

The strongest positive result is not another finite search. A deepened exact certificate proves conformal Jensen positivity for **every unchanged positive sharp J_r, r>0**, every real background sI, arbitrary periodic W1,4 profiles F,H, and arbitrary periodic W1,4 second potential g. The earlier r1 certificate additionally supplies the explicit bound below. For

    phi=(F(x)+H(y),g(x,y))

obeys

    <J_1(sI+Dphi)-J_1(sI)>
       >= <|Dphi|^4>/256 + s^2 <a^2+c^2+d^2>/128.

The proofs use exact rational positive Gram certificates and nonlinear divergence-free row stresses on this stated infinite-dimensional class. The restriction on the first potential is indispensable to this transfer. The general two-potential sharp problem remains open.

## 1. Actual input, duplicates, and receiving evidence

The source manifest preserves **57 original files**: a 54-file mathematical directory and three pasted files. The two physical pasted files have exactly the same 25,814 bytes and SHA256 `0d2eb67abc8f5f993e4eef13bd257b34be02596a751abafdeb3a56fadb2f965a`. There are **two incoming topical investigations**, not three independent physical/mathematical outputs. The mathematical paste has SHA256 `63c844560cbdb2310aad758dd0e2c78d59130525f803a97c6957fdf1d24f1e47`; the full package report adds derivations and evidence beyond that paste.

The mathematical directory was externally relocated from Downloads into Downloads/Dots during orientation. The preserved originals and initial/observed paths are recorded in `SOURCE_MANIFEST.json`; no agent moved the producer packet. No missing-ZIP question was asked. The supplied package actually contains the earlier calibration and sharp-frontier ZIPs. Their now-available original finite verifiers pass **21, 24, and 10 groups**, respectively, in worker scratch with optimization disabled. All three producer manifests pass at their stated scopes. The embedded calibration report exactly matches the FZ canonical source hash. This closes an original-verifier availability gap; it does not convert a finite replay into an independent analytic proof.

The physical producer's workbook-download failure is an execution-local fact. Previous FZ capital contains nine acquired valid original XLSX files. Their recorded and observed hashes agree; its published source analysis is byte-identical to the archived worker analysis. The current round reads those actual inputs rather than replacing them with a missing-data narrative. Final Figure 2 yields dynamic/static ethane ratio **0.22117569043994356**, versus **0.2214772280049756** from the producer's rounded preprint-v1 values. Both are kept version-specific. Neither is an Astra laboratory observation or an uncertainty interval.

Archived mission prompts, source recommendations, and copied tool transcripts are DATA. The current human request controls actions. Original bytes, prior proofs, concurrent branches, and failed approaches are preserved.

## 2. Direct positive conformal theorem and its decisive certificate

Write Dphi=(a,b;c,d), J_1=H/8+j^2+u j, H=((a-d)^2+(b+c)^2)^2, u=a^2+c^2, j=ad-bc. For the separated first potential, choose

    S_1=-3s^2 b+b^3/2,
    S_2=3s^3+7s^2 a+5s a^2+a^3/2.

The exact identity is

    J_1(sI+Dphi)-2s^4 = 5s^3 a + S_1 c+S_2 d+G.

Two rational Gram blocks, of dimensions eight and five, represent G on all ten gradient quadratic monomials and sa,sc,sd. Exact rational LDL/Sylvester checks prove both blocks exceed I/128. Therefore

    G >= [M4+s^2(a^2+c^2+d^2)]/128,

where M4 sums the squares of all ten gradient quadratic monomials and satisfies M4>=|Dphi|^4/2. Here a depends only on x and b only on y, so div S=0 and <S·Dg>=0. Also <a>=0. Integration and strong W1,4 approximation establish the theorem for arbitrary g, arbitrary amplitudes/concentration, and every real s. The exact matrix identity and rational positivity are algebraic certificates; the stress cancellation/density argument is analytic. Both obligations were reconstructed separately.

Decisive files: `workers/ga_sharp_invention/BASE_PROOF.md`, `BASE_CERTIFICATE.json`, `QUANTITATIVE_ADDENDUM.md`, `REPORT.md`, and the separately written `workers/ga_nonlinear_stress_audit/AUDIT.md` with its Fraction-based independent algebra checker. A universal result is not inferred from their agreement.

For a general smooth first potential, the same pointwise certificate remains true but

    div S=[4s^2+10s f_x+3|Df|^2/2] f_xy.

The lost stress pairing is the exact remaining operation. Bounding or replacing it without destroying the quartic budget would advance the full conformal problem. Setting it to zero, imposing separation silently, or estimating its norm with an unsupported sharp constant would not. Derivative-only row stresses that are divergence-free for every f reduce to affine cofactor stresses; a general repair needs an additional nonlocal or otherwise richer operation.

Close prior art matters. Harris–Kirchheim–Lin's triangular-support laminate theorem already supplies qualitative Jensen positivity for either single-profile axis case through fixed matrix transformations. The two-profile class above can have full affine gradient span, so that specific triangular-support theorem does not apply. This is a scope comparison, not historical priority clearance or proof that no broader predecessor exists. Classical SOS and nonlinear calibration are not claimed as new subjects.

### Sustained continuation: one exact certificate for every r>0

The successful r1 construction justified a dedicated further worker and a second audit turn, rather than stopping at that subsidiary theorem. The all-r stress is

    S_1=-(r+2)s^2 b+7r b^3/[6(r+2)],
    S_2=(r+2)s^3+(5r/2+2)s^2 a+7r s a^2/4
                                      +r(4r+3)a^3/[12(r+2)].

Subtract J_r(sI)=(r+2)(r+3)s^4/6, the first-row tangent (r+2)(2r+3)s^3 a/3, and S·Dg to define G_r. A single exact identity gives

    (r+2)G_r = z0^T Q0 z0 + r z1^T Q1 z1,

with fixed rational positive definite matrices Q0,Q1 of sizes10 and16. The z vectors are explicit polynomials in r,a,b,c,d,s. Independent Fraction arithmetic reconstructs every one of the62 nonzero polynomial coefficients and all four exact positive LDL blocks, without sampling r. Since r>0 and r+2>0, this proves G_r>=0 for all real entries and every positive parameter. The same separated-coordinate null pairing and density proof then establishes the all-r conformal theorem.

The full quantitative statement, exact shifted-matrix floor and any additional stress-conservation examples are in `workers/ga_parametric_stress_genesis/REPORT.md`, `ALL_R_THEOREM_PROOF.txt`, and `workers/ga_nonlinear_stress_audit/ALL_R_AUDIT.md`. The earlier r1 bound remains a separate, stronger r1 certificate. A one-phase nonseparated Lipschitz example is not promoted as a new qualitative class: fixed transformations already put its gradient measure in the classical triangular-support setting. A general stress-conservation hypothesis is also retained explicitly, not assumed for arbitrary first potentials.

The natural first attempt failed near r=0; its negative pointwise residual is preserved as a refuted stress ansatz, not a compatible Jensen counterexample. A broader stress choice matching the determinant-square r0 limit produced the exact all-r certificate. This is a concrete case where further inference changed the mathematical mechanism and expanded a surviving theorem. It remains internal research, with historical originality and external validation unresolved.

## 3. Complete weighted polynomial operation

For fixed sigma>0 define T_sigma phi=(q,c), q=sigma a+d. This first-order operator has rank two off its characteristic axis and rank one on it. In adapted polynomial coordinates (a,b,c,q), give b weight0, a weight1, and c,q weight2. Let j(P) be the smallest weight remaining after exact coefficient cancellation.

For every nonzero homogeneous polynomial P of degree m>=3, finite 1<p,s<infinity, and 0<alpha<=m with

    alpha/p+(m-alpha)/s=1,

the following are equivalent:

    |<P(Dphi)>| <= K ||T_sigma phi||_p^alpha ||Dphi||_s^(m-alpha),
    ||P(Dphi)||_1 <= K' ||T_sigma phi||_p^alpha ||Dphi||_s^(m-alpha),
    j(P)>=2alpha.

For degree two, the absolute criterion is the same; the signed criterion must be taken modulo the **full true gradient determinant**, aq-sigma a^2-bc. Degree one and Lebesgue endpoints are excluded from this statement.

The sufficiency proof is classical mixed-derivative interpolation, Hodge decomposition, and Hölder with explicit allocations. Necessity uses actual compatible two-scale maps with

    (a,b,c,q)=(N^-1 psi_xy+O(N^-2), psi_yy+O(N^-1),
                -sigma N^-2 psi_xx+O(N^-3), N^-2 k),

where k is an independently chosen mean-zero scalar. The leading signed functional cannot vanish for a nonzero degree>=3 polynomial: the elementary Hessian Euler–Lagrange calculation leaves only affine functions and the degree-two determinant. Testing only plane waves or q=0 would miss some illegal polynomials. The necessary sequences are uniformly bounded compatible gradients, not independently prescribed matrix distributions.

This provides a finite algebraic admission/exclusion operation. For rational sigma and polynomial coefficients, the separately checked bounded-frequency witness construction gives explicit compatible counterexamples to inadmissible exponents. Its exhaustive construction has exponential arithmetic cost; no solver speedup or optimal constant is claimed. Real double-characteristic 2x2 pencils with a rank-one characteristic line reduce to this Jordan model, with fixed transformation conditioning and transformed domains/lattices charged. Revised compiler/lattice qualifications are retained in versioned extensions and their audit.

Root's `STRICT_WEIGHT_COMPACTNESS_THEOREM.md` strengthens the distinction: under bounded full-gradient Ls norm, uniformly integrable |Dphi|^s, and nonzero defect tending to zero, universal signed/absolute little-o at power alpha holds **exactly when j(P)>2alpha**. Interpolation retains a positive power of ||(a,c,q)||_s, which vanishes by Vitali. Equality is a real nonvanishing boundary, witnessed by uniformly bounded compatible maps. A distinct worker audited this proof.

The incoming cubic case is m3, alpha1, p2,s4: two forbidden coefficients give an 18-dimensional finite-bound space; five forbidden coefficients give a 15-dimensional little-o space. Two independent cubic investigations reconstruct the latter. For the target C_r, the weighted order is three. Its optimal defect power3/2 is attained with an **L6**, rather than L4, receiving norm. That stronger exponent does not solve the sharp L4 problem.

These precise characterizations are new internal derivations relative to the inspected Astra records. Their ingredients are classical, and historical originality is UNKNOWN. Ball–Currie–Olver already proves the Hessian null-Lagrangian classification and uses polarization/resonance. Müller's 1998/2000 work already gives cubic compensation for a different rank-varying constraint with the same L4/L2 scaling. The full primary proofs were read, rather than relying on abstracts. No broad invention of compensation beyond constant rank is asserted.

## 4. What concentration actually requires, and what it does not provide

For the unchanged positive quartic, fix r>0 and set A_r=1, t=sqrt(Q_r)>0. Both construction and independent audit prove

    |C_r|/t <= K_r[(M t)^(1/3)
                         +(integral_{|Dphi|>M}|Dphi|^4)^(1/4)],  M t<=1.

If |C_r|/t stays above a fixed positive constant, a selected amplitude band of order t^-1 carries a fixed quartic-energy fraction on a set whose total measure is comparable to t^4=Q_r^2. Normalized versus physical measure is specified in the proofs. The estimate even localizes the essential concentration to the first-column components (a,c), rather than assuming every component must be uniformly integrable.

The sharp ratio supremum Gamma_r agrees for square-periodic maps, compactly supported maps, and W1,4_0 maps on every nonempty bounded planar open domain. Periodic-to-compact transfer uses a large tiled region and a bounded-width cutoff; zero extension alone does not prove that direction.

Disjoint rescaled copies of a compact template retain its ratio while converging to any prescribed weak energy measure, with the concentration scale chosen sufficiently small to fit the selected centers and boundary distances. Equal copies on a refining grid can have a diffuse Lebesgue limit and no nonzero norm-preserving spatial translation/dilation profile. Even extremizing templates can be put into such a cloud. Thus a finite spatial-profile argument cannot simply be assumed. This does not rule out selecting and independently amplifying an individual small-energy copy, nor does it prove nonquasiconvexity.

The producer's exact P1 ratio0.68544 exceeds2/3 but is weaker than FZ's existing exact0.693155 bound. It is a distinct valid compatible example, not a new sharp lower-bound advance. Its canonical heat-stress contraction counterexample rules out that specified stress estimate, not all nonlocal stresses. Neither the new concentration theory nor finite searches locates Gamma_r relative to one.

## 5. Physical causal result and the correct acquisition decision

Freshly acquired Lim–Hulsey–Yan JACS Au2021 primary text already proposes a short negative Pd/C surface sweep followed by a roughly100-fold longer positive reaction interval. Its tentative mechanism and dynamic-to-open-circuit experiment do not identify Xu's carrier or execute the same-positive-hold randomized test. They do stop generic prepare-then-react novelty.

The root's exact switched-state theorem adds a useful information limit. Normalize static positive ethane rate to one, negative rate to beta>=0, and let the observed periodic mean be rho over h positive and d negative seconds. If D=h+d beta-(h+d)rho lies between0 andh, bounded positive stable models with

    z'=-mu z, b=1-z                 during positive hold,
    z'=lambda(1-z), b=beta          during negative hold

can match both static endpoints and the exact periodic mean for a continuum of positive mu,lambda. As mu decreases, both the isolated-pulse and conditioned-next-pulse common-hold contrasts tend to zero over every fixed hold, while conditioning cycles diverge. Other finite parameters produce large isolated-pulse effects. All formulas and observation restrictions are in `CAUSAL_IDENTIFIABILITY_THEOREM.md`; a separate analytic audit and24 numerical diagnostics corroborate the construction.

This is a countermodel to an inference, not a fit to the actual electrode or a new physical mechanism. It does not reproduce uninspected timed records, current, spectroscopy, or measured conditioning transients. It shows why cycle aggregates cannot supply a minimum single-pulse response or a finite washout horizon. Fixed10-second nulls in both proposed interventions do not exclude every accumulated-state model without a measured dynamics bound.

The next acquisition should combine randomized isolated and periodically conditioned interventions with recorded conditioning, withdrawal and recovery over increasing horizons; equal actual interfacial and reactive exposure; fresh-carbon fate with complete chase and missing-label bounds; net useful ethylene output; and complete paid conditioning/read/reset work. Existing workbooks do not jointly supply this observation. Spectroscopy on a different foil, slow400-second holds, different feed and hundreds-of-ohms contact cannot be substituted for productive0.1-second mixed-feed dynamics. The acquired1-second current record is not optimum0.1-second energy or measured H uptake.

Decision: preserve the measured published whole-system response, **STOP generic pulse-preparation novelty**, and **HOLD causal/technology promotion pending the specified acquired observation**. Do not allocate another speculative electronic-carrier construction on the same aggregates. No experiment or external author communication was performed.

## 6. Research investments and methodology evidence

Actual deployment: **12 gpt-6.1-sol workers at max**, plus **one gpt-6-luna worker at max** for metadata/schema preparation. The independent initial roles covered analytic audit, sharp construction, polynomial operation, concentration, primary historical machinery/OpenAI Math proofs, physical evidence, original replay, weighted adversary, cubic UI adversary, concentration adversary, nonlinear-stress adversary, and a parametric stress continuation. Assignments were complementary and the audits were initially isolated. Root derived the strict-weight compactness extension and the physical countermodel, read decisive proofs and compared the receiving hypotheses.

`WORKER_DEPLOYMENT.json` records actual dispatch arguments and follow-up count. Aggregate tokens, money, pure inference time, immutable model versions and peak concurrency are unavailable, not estimated from elapsed time. A Luna renderer initially collided with the already preserved source manifest; root review caught this before application and the corrected create-only renderer preserves it. This is a tooling review observation, not a model comparison.

Observed compounding: the new packet closes a prior verifier-availability gap; prior acquired workbooks resolve a new run's local download failure; the incoming cubic criterion leads to a full degree/power classification and a strict compactness hierarchy; a different nonlinear stress representation proves a larger exact QC subclass. Observed limits: stronger L6 estimates do not close the L4 budget; concentration can preserve every unresolved ratio; more finite examples can be weaker than existing examples; a real periodic effect can leave the needed causal operation unmeasured.

These observations support the value of retaining exact scientific capital and changing representations. They do not establish Astra's epistemic-closure hypothesis, prompting superiority, or a causal benefit from a particular model/budget. No matched workflow experiment was performed. The current round is descriptive evidence, not a controlled test.

## 7. Precise highest-value continuations

1. Continue the nonlinear calibration only where it supplies new control of the general mixed stress source. Prove a nonlocal stress correction with the exact quartic budget, or provide a genuinely compatible negative Jensen field. The finite classification and restricted theorem are not permission to claim unrestricted QC.
2. Seek scope-matched external mathematical review and closest priority for the weighted characterization, bounded-frequency construction, strict compactness theorem and two-profile calibration. Classical general tools are credited; absence of an exact match in a bounded search is not novelty clearance.
3. Preserve the concentration cloud as a decisive test of any proposed compactness/profile proof. A valid approach must retain fine-scale distributions or justify an additional selection operation. Any Lp regularity promise must be explicitly acquired or proved for the receiving class.
4. Redirect the Pd branch to empirical acquisition with measured conditioning/recovery horizons and accountable fresh-feed useful output. Reopen mechanism invention when that observation supplies an independently manipulable state or a discriminating erasure/rescue test.
5. Preserve any parametric stress construction or failure at its exact parameter and algebraic scope. A negative pointwise residual outside the separable-compatible transfer is not a QC counterexample.

## 8. Integration and unresolved repository boundary

The source snapshots, separately attributed proofs/audits, exact certificates, failures, provenance and handoffs are integrated through new GA records and new routes N885–N888. Historical cards/source bytes remain unchanged. Reciprocal material updates are appended as scoped notices; they do not rewrite old evidence status. Transfers distinguish compatible interfaces, incompatible receiving norms and explicit refuted inferences.

The existing checkpoint publisher has inherited malformed records. A fresh handoff is validated individually outside the immutable checkpoint tree; repository-wide publication remains blocked if those same records fail. No ancestry is invented and no unrelated inherited repair is attempted. The actual checked commit, public PR/merge, source-hash reconciliation, access validation, technology/workflow checks and any blocker are recorded separately in the final integration receipt. A successful Git operation is not scientific proof.

Current draft PRs84,85,87,88 retain conflicting histories; PR88 overlaps older N822 activity whose canonical science already entered through later FR/PR89. Draft95 has594 added paths and no exact GA card-ID overlap, but its whole scientific intake has not been cleared. It is left independent rather than merged merely because Git reports mergeable. Recent merged101/102 supply the receiving mathematics/data used above. Fresh head/path checks are preserved in the integration preparation report.

The complete decisive proofs are under `package/derived/root` and `package/derived/workers`; originals are under `package/originals`. The final user response provides immutable GitHub permalinks after verified integration. External downloaded fulltexts, cloned repositories and native datasets remain segregated outside the authored publication selection.
