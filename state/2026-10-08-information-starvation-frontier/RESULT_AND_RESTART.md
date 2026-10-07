# Suppressed-subclone observability: measurement-starvation exponents and a safety-information frontier

Research checkpoint, 8 October 2026 (Australia/Brisbane).

STATUS: internally derived candidate theorem family and finite numerical diagnostics; NOT externally reviewed, proof-assistant formalized, biologically validated, clinically validated, or priority-cleared. Do not present this checkpoint as an established historical breakthrough. The strongest new content is a measurement-dependent information-starvation law and a safety-observability comparison for rare suppressed subpopulations. The adaptive-therapy O(f0^2) bulk-measurement result itself is inherited recent prior art from Browning et al. (arXiv:2608.18387) and is not claimed here.

No independent subagent service was available in this environment. Adversarial checking consisted of independent literature routes, exact analytic derivations, and separate numerical scaling diagnostics; this is not independent expert review.

## 1. Task and provenance

Goal: search broadly for a high-upside theoretical result with a credible chain from fundamental mechanism to quantitative prediction and experimental capability, giving substantially greater attention than prior Astra runs to biology, cancer, chemistry, materials, engineering, and scientific measurement.

Repository frontier read first:
- 00_START_HERE.txt blob d41f6489f0161ae7ea6ee8d92003e1656de4cafe
- 01_CORE.txt blob 4f84ffebb34d7724e0d6c07ffbbb4ff0c554e282
- agent/RESEARCH_WORKFLOW.txt blob b978a087b48029dcbd227d3320f3d984dcb4adf5
- N33 endotactic permanence blob 03f34609d3695400afec4622c82751d5579cdf64
- N34 reaction certificates blob e8e0fbaf1ded6fd294bfcf91a393a37bffbcf93f
- N35 controlled chemical safety blob 0120db17246ada6ae79da59d46525dcc50f0e404

Repository head observed before writing this checkpoint:
420ee79e9ed7fe1441d12f131f5b8e790e12a692.

Astra mechanisms screened included reaction-network permanence/safety certificates, active causal acquisition under nuisance cancellation, Gaussian information/memory converses, positive-kernel access, and current OpenAI-mathematics-derived capital. No OpenAI release theorem became a load-bearing premise of the final result.

Breadth routes screened in the live literature included adaptive cancer therapy, tumour evolution and resistance, ctDNA measurement limits, causal perturbation/single-cell acquisition, synthetic-cell control, protein energy landscapes, chemistry/catalysis, materials/superconductors, immunology/CAR-T experimental design, regeneration, and safe exploration/control. The cancer observability direction dominated after the first depth cycle because it produced a clean theorem, a current experimental interface, a direct falsifier, and a practical measurement-design consequence.

## 2. Decisive prior-art reset

Browning, Crossley, Murphy, Byrne and Hamis, "Adaptive therapy under parametric, structural, and measurement uncertainty", arXiv:2608.18387v1 (August 2026), prove in their two-population prostate-cancer model that when adaptive therapy keeps the resistant population r=O(f0) on a fixed finite observation window, sensitivity of total burden n=s+r to the resistant growth rate lambda_R is O(r), and the corresponding Fisher-information diagonal scales as O(f0^2). Under a schedule that releases resistance to O(1), the corresponding information is O(1). Their proof uses the rare-population sensitivity and a Gronwall bound on the indirect sensitive-population coupling.

Therefore:
- "successful adaptive therapy hides resistance quadratically from PSA-like aggregate measurements" is PRIOR ART, not a new Astra theorem;
- the remaining question is whether that quadratic starvation is universal or measurement-dependent.

Current biology/measurement motivation:
- 2026 adaptive-therapy reviews explicitly identify dynamic resistant-versus-sensitive composition as a monitoring gap and ctDNA as a major opportunity.
- Gallagher et al., JAMA Oncology 2026, retrospectively validated first-cycle mathematical biomarkers from PSA dynamics in 53 patients, confirming that the bulk-biomarker inference interface is clinically relevant while not resolving clone composition.
- Gamisch, Journal of Liquid Biopsy 2026, integrated 5,238 plasma samples and showed strong finite-molecule limits for low-VAF ctDNA; median input was 5,531 genome equivalents, and fewer than 10% of samples supported any of the studied 95%-detection criteria at 0.01% VAF.

## 3. Candidate theorem A: measurement-starvation pullback law

Let theta be a scalar parameter that acts through a rare subpopulation state r(t;theta). On a fixed finite observation window suppose

r(t;theta)=O(epsilon),
and
partial_theta r(t;theta)=r(t;theta) h(t;theta),

with |h| bounded uniformly. Let z=a r be the rare-state signal delivered to a measurement channel p(y|z). Let J_z(z) denote the channel Fisher information for its scalar signal coordinate z.

If, in the relevant small-signal regime,

J_z(z)=Theta(z^(-beta))

and |h| is also bounded below away from zero on a non-negligible observation set, then the Fisher information for theta scales as

J_theta = J_z(z) (partial_theta z)^2 = Theta(epsilon^(2-beta)).

This is the ordinary Fisher-information pullback under a rare-state sensitivity, but its consequence is the useful classification:

- beta=0: fixed-additive-noise / ordinary smooth bulk channel -> quadratic starvation, J_theta=Theta(epsilon^2);
- beta=1: ideal background-free Poisson or binomial molecular counting -> linear starvation, J_theta=Theta(epsilon);
- beta=2: ideal constant-relative-error or log measurement -> no leading starvation, J_theta=Theta(1).

The classification is local and regular. It does not imply that a beta=2 physical assay exists down to arbitrarily small copy number.

## 4. Candidate theorem B: molecular-background phase transition

Condition on N effective independent genome-equivalent opportunities and model a clone-specific molecular measurement by

C | N ~ Binomial(N,p),
p = b + a r,

where a>0 is a known signal conversion and b>=0 is a stable known background term. Let

partial_theta r = r h.

The exact Fisher information is

I_theta
= N (partial_theta p)^2 / [p(1-p)]
= N a^2 r^2 h^2 / [(b+a r)(1-b-a r)].

For low VAF, p<<1,

I_theta approximately N a^2 r^2 h^2 / (b+a r).

Therefore there is a sharp asymptotic crossover around

r_* approximately b/a.

Signal-dominated regime, a r >> b:
I_theta approximately N a r h^2 = Theta(N r).

Background-dominated regime, a r << b:
I_theta approximately N a^2 r^2 h^2 / b = Theta(N r^2).

Thus a clone-specific assay removes one power of information starvation only while the true clone signal dominates its effective background. Below the background floor, the quadratic exponent returns.

The same scaling follows for a Poisson count with intensity lambda=lambda_0+kappa r. If b or lambda_0 is itself unknown and must be estimated, information can only be lower after nuisance projection; the displayed formula is not a free robustness guarantee.

## 5. Candidate theorem C: safety-observability frontier

Use continuous-time observation models with finite information rate.

Assume 0<=r(t)<=r_max and define the cumulative rare-subpopulation exposure

E = integral_0^T r(t) dt.

E is a mathematical risk/exposure proxy, not a clinical safety metric.

### Aggregate fixed-noise observation

Suppose

dY_t = n(t;theta) dt + sigma dW_t

and the rare-state coupling satisfies

|partial_theta n(t;theta)| <= C r(t).

Then

I_bulk
= sigma^(-2) integral (partial_theta n)^2 dt
<= (C^2/sigma^2) integral r^2 dt
<= (C^2/sigma^2) r_max E.

Consequently the Fisher information per unit rare-clone exposure obeys

I_bulk / E <= (C^2/sigma^2) r_max.

As the safety cap r_max tends to zero, aggregate-sensing information per unit rare-clone exposure collapses at least linearly.

### Background-free clone-specific molecular count

Suppose

dN_t has intensity kappa r(t;theta),

and h(t)=partial_theta log r(t) satisfies

0<h_min <= |h(t)| <= h_max

on the relevant observed interval. Then the exact point-process Fisher information is

I_count
= kappa integral r(t) h(t)^2 dt,

so

kappa h_min^2 E
<= I_count
<= kappa h_max^2 E.

There is no additional r_max penalty at fixed E.

### Clone-specific count with additive background

For intensity

lambda(t)=lambda_0+kappa r(t),

I_bg
= integral [kappa^2 r(t)^2 h(t)^2 / (lambda_0+kappa r(t))] dt.

If kappa r_max << lambda_0, then

I_bg
<= (kappa^2 h_max^2/lambda_0) r_max E,

so the aggregate-style r_max starvation returns.

This is the central candidate result: suppression and observability are not in a universal tradeoff. The exponent of the tradeoff is a property of the measurement architecture and its background physics.

## 6. Experimental-design corollary

Under the aggregate leading-order regime in which information is proportional to integral r(t)^2 dt, constrain

0<=r(t)<=r_max,
integral r(t) dt = E,
E<=r_max T.

Then

E^2/T <= integral r^2 dt <= r_max E.

The lower bound is attained by uniform exposure r=E/T; the upper bound by an idealized bang-bang profile at r_max for duration E/r_max and zero otherwise.

Therefore, at the same integrated rare-clone exposure, aggregate sensing can gain an information factor as large as

r_max / (E/T)

by concentrating a permitted diagnostic excursion near the cap.

For an ideal background-free molecular counter with constant h, leading information is proportional only to E, so this concentration advantage disappears.

This is an experimental-design statement, not a treatment recommendation. Real tumour risk need not be linear in E, the state r(t) is not directly actuated, switching has dynamical costs, and any in-vivo use requires a genuine biological safety model. The clean first test is preclinical: controlled mixtures, organoids, bioreactors, or xenografts.

## 7. Resource lower-bound interpretation

For nearby parameter values theta and theta+delta, local KL divergence is approximately

KL approximately (1/2) I_theta delta^2.

Hence keeping a fixed local distinguishability or precision as epsilon decreases requires, up to model-dependent constants:

- bulk fixed-noise observation budget scaling as epsilon^(-2);
- ideal background-free clone-specific molecular opportunities scaling as epsilon^(-1);
- background-dominated molecular measurement returning to epsilon^(-2).

This should be read as local asymptotic information scaling, not as a complete minimax theorem.

Finite molecule input imposes an additional hard physical floor. For a background-free single-locus Poisson model with N_GE genome equivalents and clone VAF f, the probability of observing at least one mutant molecule is

1-exp(-N_GE f).

Requiring 95% probability gives

N_GE >= -log(0.05)/f approximately 2.996/f.

Examples:
- f=0.1% -> at least about 2,996 GE;
- f=0.01% -> at least about 29,958 GE;
- f=0.001% -> at least about 299,573 GE.

Gamisch's reported median clinical input of 5,531 GE makes the last two regimes strongly input-limited for a single locus even before technical losses and stronger evidentiary thresholds.

## 8. Falsifiable preclinical prediction

Use a two-population sensitive/resistant system with a known clone-specific barcode or resistance mutation. Maintain comparable total burden under containment/adaptive control while sweeping the resistant fraction across as broad a range as experimentally feasible. Collect in parallel:

1. a bulk-burden measurement;
2. clone-specific ddPCR or UMI-based sequencing;
3. effective unique genome-equivalent input and assay background.

Fit the same resistant-growth or transition parameter from each stream.

Predictions:
- aggregate/bulk observed information has log-log slope approximately 2 versus resistant fraction while the rare-state sensitivity is O(r);
- clone-specific molecular information has slope approximately 1 above the background crossover;
- it returns toward slope 2 below the effective background;
- when N_GE f << 1, typical samples become zero-dominated even if expected Fisher information is formally nonzero;
- for matched integrated rare-clone exposure E, a short cap-limited diagnostic excursion helps aggregate sensing much more than signal-dominated direct molecular counting.

A result inconsistent with these slopes after charging actual molecule input, background, and model sensitivity would falsify the proposed mechanism in that experimental system.

## 9. Finite diagnostic

See scaling_check.py and scaling_check_results.json beside this file.

Representative two-population logistic-competition ODE with fixed treatment; resistant initial fraction epsilon varied from 1e-5 to 1e-1. Finite differences were taken with respect to the resistant growth-rate parameter.

Fitted low-epsilon log-log exponents:
- fixed-noise total-burden Fisher information: 1.9997928626;
- background-free resistant Poisson count: 0.9997980468;
- ideal log/relative observation: -0.0001774270.

Independent analytic rare-signal process f(t)=epsilon exp(theta t):
- zero-background Poisson count exponent: 1.0000;
- with background b=1e-4, low-epsilon exponent: 1.9987089902;
- same model at high epsilon: 1.0026191607.

These diagnostics only confirm the asymptotic algebra for the chosen models. They do not validate tumour biology, ctDNA shedding, or clinical usefulness.

## 10. Biological and statistical failure modes

The result must not be promoted from model theorem to biological efficacy without addressing:

- ctDNA VAF is not automatically proportional to resistant-cell fraction: shedding, spatial structure, copy number, apoptosis, vascular access, tumour burden, and clonal hematopoiesis can distort the map;
- assay background may drift rather than remain stable;
- overdispersion, serial correlation, sample-processing loss, and stochastic tumour dynamics can reduce information;
- if theta also changes an abundant sensitive compartment directly, rare-state starvation can disappear;
- if the observation horizon grows like log(1/epsilon) until the resistant clone becomes O(1), the fixed-window exponents change;
- adaptive switching times can have nonsmooth parameter sensitivities at event collisions;
- below the one-molecule regime, expected Fisher information can be a poor description of a typical realization; exact detection probabilities or Bayesian posteriors should be used;
- E=integral r dt is a mathematical exposure proxy, not metastasis risk, toxicity, or patient safety.

## 11. Routes demoted rather than discarded

### Stochastic safety certificates for tumour control
Astra N33-N35 provide a strong mathematical route from reaction-network inward-drift certificates to exponentially small finite-horizon exit probability. However, cancer control-barrier methods and tumour-control CRN models already exist, so "apply a barrier certificate to cancer" is not by itself frontier-breaking. The stronger future composition is to maximize information subject to an N35-style high-probability preclinical safety certificate.

### Compressed causal perturbation design
Astra's causal-inference scout derives nuisance-canceling covariance contrasts that can recover an unknown latent linear DAG under strongly separating clamps and dense invariant confounding/noise. This remains interesting, but logarithmic strongly separating intervention designs and 2026 latent causal-representation results already cover important portions of the headline. The remaining dense-noise extension needs a dedicated priority audit and a biologically plausible perturbation service.

### Protein, chemistry, materials, cell engineering
Current 2026 literature revealed high-upside empirical frontiers, including large-scale protein energy-landscape measurements and accelerated superconducting/material searches, but this run did not derive a theorem with a comparably clean novel interface. These are retained as breadth leads, not promoted over the present result.

## 12. Novelty status

Targeted current-literature searches found:
- the O(f0^2) aggregate adaptive-therapy starvation theorem in Browning et al.;
- general safe optimal experimental design / dual-control ideas;
- established Poisson finite-molecule ctDNA detection limits;
- extensive ctDNA monitoring and adaptive-therapy motivation.

They did NOT surface, in the searched material, the exact combined statement:
1. a measurement-channel starvation exponent for a suppressed rare clone;
2. an explicit linear-to-quadratic clone-specific molecular crossover caused by assay background;
3. the fixed-exposure safety-observability inequality comparing aggregate and direct clone-specific sensing.

This is a search finding, NOT a priority certificate. The mathematics is elementary enough that equivalent results may exist under different terminology in statistical sensing, rare-event estimation, epidemiology, ecology, or control. External specialist review is required before claiming novelty.

## 13. Strongest next attacks

1. Replace local Fisher-information claims with finite-separation Le Cam or Hellinger minimax lower bounds, including nuisance background and correlated bulk noise.
2. Extend the safety-observability theorem to hybrid feedback policies with event-triggered switching and stochastic rare-population dynamics.
3. Derive the exponent for realistic VAF ratios with random cfDNA denominator, variable shedding, multi-locus panels, and overdispersion.
4. Test whether existing prostate adaptive-therapy datasets have paired or banked ctDNA sufficient for a retrospective slope/crossover analysis.
5. Combine Astra N35 with information maximization to obtain a certified informative preclinical pulse: maximize information while preserving an explicit finite-horizon stochastic exit bound.
6. Conduct a specialist priority review spanning adaptive therapy, liquid-biopsy statistics, stochastic control, rare-event inference, and optimal experimental design.

## 14. Core external sources

- Browning AP, Crossley RM, Murphy RJ, Byrne H, Hamis S. Adaptive therapy under parametric, structural, and measurement uncertainty. arXiv:2608.18387v1, 2026.
- Gallagher K et al. Mathematical Biomarkers of Adaptive Therapy Outcomes in Prostate Cancer. JAMA Oncology. Published online 6 Aug 2026. doi:10.1001/jamaoncol.2026.2781.
- Wu J, Strobl MAR, Scott JG. Adaptive therapy and its challenges. Evolution, Medicine, and Public Health. 2026;14(1):1-3. doi:10.1093/emph/eoag010.
- Gamisch A. Molecular sampling limits of ctDNA detection in clinical plasma samples. Journal of Liquid Biopsy. 2026;13:100480. doi:10.1016/j.jlb.2026.100480.

## Restart instruction

Do not rediscover the O(f0^2) bulk result: treat Browning Proposition 1 as inherited prior art.

Start from Theorems A-C above. First audit the continuous-time likelihood formulas and prove a finite-separation information lower bound. Then stress-test the ctDNA map using realistic nuisance structure. In parallel, perform specialist prior-art search for "information starvation", "rare-state observability", "Fisher information under suppression/containment", and background-limited molecular sensing. Only after that decide whether the result is a paper-level theorem, a general principle worth naming, or a useful but elementary corollary.

The highest-upside escalation is the certified safe-probing composition: combine a genuine stochastic safety certificate with a theorem showing the maximum information obtainable before a rare resistant population violates the safe set.