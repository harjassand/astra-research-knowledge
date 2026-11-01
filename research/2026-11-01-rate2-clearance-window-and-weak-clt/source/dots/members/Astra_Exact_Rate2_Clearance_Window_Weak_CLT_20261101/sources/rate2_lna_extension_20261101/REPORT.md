# Ordinary full-network LNA: a stronger baseline, with a sharp domain warning

**Result first.** The conventional full-network linear-noise approximation (LNA) yields clearance-time variance estimates **0.70434, 1.36608, 2.62568** for N=100, 1,000, 10,000. These are useful ordinary heuristic competitors, not fitted to the SSA or proposed clock. But its intermediate fixed-time covariance becomes physically impossible: a B-coordinate variance exceeds an elementary exact-chain upper bound by factors **3.85, 744, 142,259**. A final delta-method timing estimate can remain useful despite that failure; it cannot thereby become a certified physical-state or first-passage law.

This is a separate extension. All 355 hashes in the existing frozen pilot still pass. No new SSA samples, external sources, installations or interventions were used.

## Construction and approximation boundary

Use exactly the previous twelve stoichiometric channels and coefficients, including CD→AE=2, with deterministic initial mean m(0)=(0,N,1,1,0) and **C(0)=0** because initial counts are fixed. No Poisson initial covariance is inserted.

The ordinary mass-action rates use **a²**, not the CTMC's A(A−1). With reaction vectors ν_r, deterministic drift f=Σν_r a_r, Jacobian J=Df and Q=Σa_r ν_rν_rᵀ, integrate

    m' = f(m),
    C' = J(m) C + C J(m)ᵀ + Q(m).

All five mean coordinates and all 25 covariance entries are integrated. This is the ordinary chemical-LNA/linearized diffusion prescription; no controlled system-size expansion through this low-count boundary is established here. It is neither an exact moment equation nor a claim that the stochastic mean follows m. In particular E[A(A−1)]≠E[A]², and simply extending a(a−1) to 0<a<1 would give negative “rates.” No such extension was used.

Stop the deterministic mean at its first total-count crossing of **floor(15(N+2)/16)**. Let T be that deterministic time, g=(1,1,1,1,1), and d=gᵀf(m(T))=1−a(T). The conventional transverse first-passage delta method is

    tau − T ≈ −gᵀξ(T)/d,
    Var_LNA(tau) = gᵀ C(T) g / d².

The slopes are about −19.847, −207.399, −2082.287, so division is not near a tangency at these targets. This local Gaussian/delta-method approximation is **not** a first-passage theorem for the actual chain.

## Comparison without fitting

The original prespecified main SSA samples are reused, with sample variance computed using denominator M−1. The supplied candidate variance is **0.5682 N^0.2**; that coefficient is an input from a separate deterministic-candidate calculation, not an actual-chain CLT premise.

| N | Existing SSA paths | SSA sample variance | Full-network LNA variance | Candidate variance 0.5682 N^0.2 |
|---:|---:|---:|---:|---:|
| 100 | 64 | 1.28854 | 0.70434 | 1.42725 |
| 1,000 | 64 | 1.50366 | 1.36608 | 2.26204 |
| 10,000 | 16 | 3.56466 | 2.62568 | 3.58510 |

Corresponding standard deviations:

| N | SSA sample SD | LNA SD | Candidate SD |
|---:|---:|---:|---:|
| 100 | 1.13514 | 0.83925 | 1.19468 |
| 1,000 | 1.22624 | 1.16879 | 1.50401 |
| 10,000 | 1.88803 | 1.62039 | 1.89344 |

LNA variances divided by N^0.2 are 0.28040, 0.34314, 0.41614. These three points do not establish the large-N limit of the ordinary LNA coefficient, nor exclude the possibility that it tends toward the supplied candidate coefficient. A new coefficient/solver claim must compare with that ordinary limit, not merely with a deterministic point clock.

Ordinary LNA is descriptively closer to the observed variance at N=1,000; the candidate is closer at N=100 and N=10,000. **The striking N=10,000 candidate agreement is only 16 samples and does not validate a CLT, finite-N error, tails or a Gaussian law.** No confidence interval for the true variance is asserted. In particular a chi-squared interval assuming normal clearance times would assume part of what needs checking.

The centering also remains different: LNA is centered at ordinary deterministic times 2.45338, 3.71483, 6.23440, not at the observed SSA means. The candidate point remains 2.77960, 4.40538, 6.98205. No empirical recentering or variance fitting was done. A naive untruncated Gaussian LNA time law even assigns negative-time mass about 0.00173, 0.000741 and 0.0000597; it was not silently clipped or renamed a certified CDF.

## A physically decisive fixed-time covariance warning

For the actual chain, each coordinate satisfies

    B(t) ≤ S(t) ≤ N+2+I(t),  I(t) ~ Poisson(t).

Consequently, at every fixed deterministic t,

    Var B(t) ≤ E[B(t)²] ≤ (N+2+t)²+t.

This is a loose exact bound requiring no LNA. Dense diagnostics of the **tighter BDF** LNA trajectory give:

| N | Diagnostic time | LNA B variance | Exact-chain second-moment ceiling | Ratio |
|---:|---:|---:|---:|---:|
| 100 | 2.04391 | 4.1681×10^4 | 1.0827×10^4 | 3.85 |
| 1,000 | 3.40838 | 7.5174×10^8 | 1.0108×10^6 | 744 |
| 10,000 | 5.94101 | 1.42485×10^13 | 1.00159×10^8 | 142,259 |

At the last point the deterministic B mean is about 3,918, while its LNA SD is about **3.77 million**, although the whole initial population was 10,002. An independent Radau integration to that same time agrees on B variance to **1.98×10^−8 relative**. The giant transient is therefore not explained by the observed solver discrepancy.

Interpretation: the fixed-time linearized Gaussian perturbation has left a physically small-fluctuation regime through the rapid transition. This is a clear failure of its *state-covariance approximation* in that region. It does **not**, by itself, prove that the final scalar delta-method timing variance is useless or asymptotically wrong: passage times can admit a useful phase description when fixed-time linearized state fluctuations do not. That distinction is exactly what a controlled boundary-aware clock construction would have to establish, rather than assume.

## Solver checks, domain defects and full additional cost

The predeclared primary pass used BDF and Radau at rtol=1e−8, atol=1e−10, plus BDF at rtol=1e−10, atol=1e−12, for each N, with physical horizon 200. All nine integrations reached their deterministic targets. An analytic full 30-variable Jacobian was checked on 90 finite-difference columns, with maximum scaled discrepancy 3.12e−9. Independent reaction formulas and the identities Σf=1−a and gᵀQg=1+a were also checked.

Maximum time-variance discrepancies across the three settings were 1.62e−7, 9.06e−7 and 2.95e−6; **Radau versus tighter BDF agrees within 6.41e−8**. Their deterministic crossing times agree with the original ordinary ODE within 1.03e−9. These are numerical consistency checks, not interval-certified error bounds.

Mean species remained nonnegative at solver nodes and dense sampled times. No rate clipping, mean projection or covariance PSD projection was applied. Symmetrization was used only to inspect eigenvalues. The loose N=10,000 BDF run had an intermediate minimum covariance eigenvalue **−8,869**, or **−7.25e−10 relative** to the large local covariance scale. That defect is retained, not described as a PSD pass. Radau and tighter BDF showed no sampled negative eigenvalues. Absolute covariance asymmetry reached 0.00195 at the enormous transient scale. Internal Newton stages and rejected-step counts are not separately exposed; their computational work is included in solver counters and timing. Sampled diagnostics are not validated all-time enclosures.

The PSD defect prompted a bounded, explicitly separate diagnostic extension: three tighter-BDF reruns with 10,001 dense time samples, then one independent Radau recheck of the extreme N=10,000 transient. Their purpose was to check validity, not to alter or fit the variance estimates. In total **13 numerical integrations**, **zero new SSA events**, **zero failed/unfinished solver runs**, with the one loose-BDF PSD quality defect retained:

- Primary nine solves, startup and validation: **9.253 s** launch-inclusive; full initial controller **9.259 s**.
- Three domain diagnostic solves, startup and checks: **4.762 s**.
- Targeted Radau peak recheck including startup: **2.357 s**.
- All three numerical process-tree launches: **16.372 s**, **21.440 CPU s**, peak reported child/descendant RSS **93,980 KiB**. CPU can exceed wall due to library threading. Do not add nested controller/child clocks twice.

All preparation/validation computations, refinements and diagnostics are included in these numerical process costs; source inspection, code/report authoring and shell inspection are not claimed as algorithm throughput or measured all-session CPU. Final hash/CSV checks have a separate receipt. No compiler, installation or new simulation was needed for this extension. The local machine and packages are the original pilot's shared container; timings are not portable complexity claims.

## What remains to earn

Ordinary methods already supply both a deterministic timing point and an inexpensive *heuristic timing spread*. A candidate clock variance is not by itself a new computational capability. The useful additional result would justify actual-chain first-passage fluctuations through the boundary and rapid transition, quantify finite-N error where the ordinary Gaussian state approximation is physically invalid, and preserve the requested exit/occupation information at lower matched-error total cost. The present experiment neither supplies nor rules out that result.
