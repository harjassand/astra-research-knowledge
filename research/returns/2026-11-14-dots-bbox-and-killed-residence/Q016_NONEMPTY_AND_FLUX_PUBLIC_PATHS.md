# Nonempty conditional acquisition and exact source-flux cost

## Nonempty core law without waiting for a rare Gibbs sample

Let Q be the envelope Poisson proposal in source.py, with mean Γ, and let Z=Z_A/w_minus. On compatible nonempty accepted polymer families, the proposal probability is exp(-Λ) times the product of physical activities, where Λ is the sum of actual polymer activities. The event N_envelope=0 implies no retained polymer, so conditioning envelope N>=1 changes every nonempty family's probability by the same factor 1/(1-exp(-Γ)). Therefore `nonempty.py` draws N~Poisson(Γ)|N>=1, thins and rejects incompatible OR empty retained families, and samples exactly μ_A conditional on at least one plus spin.

Its acceptance probability is exp(-Λ)(Z-1)/(1-exp(-Γ)), not exp(-Γ)(Z-1)/(1-exp(-Γ)). Since Λ<=Γ, the latter is a valid lower bound. The n singleton configurations give Z-1>=n exp(-799/25). Consequently acceptance exceeds .30867388 and in particular3/10, proved with rational exponent intervals. Expected attempts <10/3; expected envelope marks per attempt Γ/(1-exp(-Γ))<1.00000006. This conditioning avoids the ~3e7 waiting factor for getting a nonempty unconditional sample. It does NOT condition on a successful rare transition or supply that flux law.

Execution:2000 nonempty draws for each box convention5 and6; all4000 were singleton states. Attempts6472 and6457, respectively. These are genuine conditional samples, not forced individual-polymer thinning tests. Their observed lack of larger components is not a test of the exponentially smaller conditional multi-site tails. `nonempty.json` contains the receipt.

## Exact soft-source flux law and a cost identity

Define q(x)=P_x(tau_B<zeta_A), with q=1 on A∩B; zeta_A is the rate-κ killing clock in core local time. Write μ_A(x)=w(x)/Z_A and p=E_μ q=C/(κ Z_A), using direct source-to-ground edges for A∩B. The outgoing soft-source current distribution is

ν(x)=κ w(x)q(x)/C=μ_A(x)q(x)/p.

Algorithm: draw X~μ_A exactly; run the original physical heatbath dynamics from X until target or soft killing; accept X iff target is first; otherwise restart independently. This samples ν exactly. No committor evaluation is needed. Expected source proposals=1/p=κ Z_A/C.

Let S be a single trial duration, m=E_μ S=N/(κ Z_A). Trial outcome and its duration may be correlated; independence within a trial is NOT needed. Across fresh trials the pairs are iid. By summing E[S_i 1{all earlier trials failed}]=m(1-p)^(i-1), the expected total physical simulation time until acceptance is m/p=N/C=Q. This is exactly the difficult full-duration quantity rather than a cheap source operation. With rate-one-per-site proposal clocks, counting all uniformized proposal events costs nQ in expectation (plus independent source acquisition overhead); exact event-skipping would need a separate computational cost analysis and does not itself change Q.

This is an exact cost characterization of the direct flux-rejection route, not an impossibility theorem for all flux samplers. The fast nonempty core sampler can support stratified experiments but does not bound q or remove this rare-event cost. A useful improvement needs an acquired q-dominating change of measure with controlled likelihood ratios, a Doob-transform construction, or a proven splitting/arrival-law mechanism. None is supplied by this note.

## Governing-model status

Read the bundled exact prompt and completed return, plus independent review. The original prompt explicitly says the completed thermal-core archive was uncollected and to use only its stated interface. The phrase 'r by r rectangles' does not distinguish coordinate span from site count. The later independent review reports uniform diagonal orientation as established but does not reproduce a stronger original definition. Thus both implementation parameters remain explicit: uniform NE/SW augmentation and box_sites=5 or6. No recovered text justifies silently selecting one as original C5. Generic fixed per-plaquette orientations can have degree8, so the six-letter proof must not be claimed for them.
