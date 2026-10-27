# Astra Pro3 — total slow-band acquisition, sparse causal probes, and a nonlinear-model falsifier

**27 October 2026.** Exact mathematical work and executed software-source experiments. This continuation begins with the archived gap-free spectral-memory research. The mathematical ingredients—Hausdorff moment duality, Gauss–Radau/Lobatto quadrature, orthogonal polynomials, Markov inequalities and factorial intervention contrasts—are classical. The research objective is to compile actual native observations into future operational guarantees, with explicit distinctions between acquired data, supplied physical assumptions and model-aware independent checks.

## 1. Source and observation interface

The supplied source class is an unknown positive, finite spectral measure on `[0,1)` with impulse moments

\[
  g_j=\int x^j\,d\mu(x).
\]

Linearity, time invariance, positive spectral representation, synchronized sham/treated source preparation and calibrated reciprocal boundary responses are **premises**, not properties acquired merely from successful data fitting. The existing four-port Schur instrument has the native scalar reaction

\[
 R_t=\frac32+\frac1{q_t+h_t/(1+u_t)},\qquad
 q_t=q_t^{(0)}+\sum_{j<t}g_j u_{t-1-j}.
\]

A pulse of amplitude `δ=1/5` at time zero, matched against an otherwise identical sham trial at the same time `t=j+1`, gives

\[
 g_j=\frac1\delta\left[\frac1{R_{t,\mathrm{pulse}}-3/2}-\frac1{R_{t,\mathrm{sham}}-3/2}\right].
\]

Thus each independently obtained impulse coefficient costs two native scalar reaction readings, one active pulse, a matched preparation/reset and a wait to the selected time. The actually tested source is an unknown-to-the-learner continuum of modes, uniform on `[0,3/4]`, so its checker-only moments are `(3/4)^j/(j+1)`. This source formula is **never** used by the new data-only noisy certificate selector or the sparse-task inference procedure. It is used by the independent source simulator and proof verifier. Exact-response and bounded-error readout scenarios are alternatives; they are not silently conflated.

The target is the *total* mass in the near-nondecaying band,

\[
 W_b(\mu)=\mu([b,1)),\qquad b=7/8.
\]

The old endpoint-Christoffel calculation bounded only mass at one specified decay factor. It did **not** bound `W_b`. This distinction motivates the present construction.

## 2. Conditional exact slow-band theorem from finitely many moments

Suppose the learner has exact moments `m_0,...,m_D` of a nonnegative measure on `[0,1)`, and choose rational `0<b<1`. Write `L(x^j)=m_j`. The following data-only tests and formulas yield a sharp upper bound for `W_b` when their positive-quadrature conditions pass.

**Even degree `D=2n`.** Compute the monic degree-`n` polynomial `p_n` from

\[
 L((b-x)x^k p_n(x))=0,\qquad k=0,\ldots,n-1.
\]

Require the modified moment Gram matrix `G=(b m_{i+j}-m_{i+j+1})_{i,j<n}` to be positive definite and `p_n` to have `n` simple roots strictly in `(0,b)`. Construct

\[
 Q_{2n}(x)=\frac{p_n(x)^2}{p_n(b)^2}.
\]

**Odd degree `D=2n+1`.** Obtain the monic polynomial from

\[
 L(x(b-x)x^k p_n(x))=0,\qquad k=0,\ldots,n-1.
\]

Require the corresponding Gram matrix to be positive definite, all roots in `(0,b)`, and the computed endpoint weight at zero to be nonnegative. Construct

\[
 Q_{2n+1}(x)=\frac{x p_n(x)^2}{b p_n(b)^2}.
\]

**Theorem (sharp total-band certificate).** Under these checkable conditions and positive quadrature weights, every compatible positive spectral source satisfies

\[
 \boxed{ W_b(\mu)\le L(Q_D)=\sum_{j=0}^{D}[x^j]Q_D\;m_j }. \tag{1}
\]

The upper bound is **attained** by a strictly stable finite atomic source sharing every acquired moment. For even `D` its nodes are the roots of `p_n` and `b` (Gauss–Radau); for odd `D` they are `0`, the roots of `p_n`, and `b` (Gauss–Lobatto). In the executed moment records every prerequisite passed through `D=11`, with all matrix leading minors and root counts checked exactly.

**Proof.** All zeros of `p_n` lie below `b`. For `x>=b`, `|x-c_i|>=|b-c_i|` for every root, so `Q_D(x)>=1`; for `x<b`, `Q_D(x)>=0`. This gives (1) without approximations. The positive quadrature rule reproduces every polynomial through degree `D`: divide it by `(x-b)p_n(x)` in the even case, or by `x(x-b)p_n(x)` in the odd case. The quotient has degree at most `n-1`, so the associated modified orthogonality eliminates its integral, while the remainder is reconstructed exactly by its values at the proposed nodes. The node weights are positive by the stated modified Gram positivity and endpoint-weight checks. The resulting atomic source places weight `L(Q_D)` at `b`, since `Q_D(b)=1` and it vanishes at all other nodes. This proves matching primal and dual certificates and full sharpness over the stated observation class. The theorem is conditional: a candidate whose node or weight checks fail returns **UNKNOWN** and must not be called sharp.

### Four-moment witness and independently checked extension

From four native impulse coefficients,

\[
 (m_0,m_1,m_2,m_3)=(1,3/8,3/16,27/256),
\]

we obtain

\[
 Q_3(x)=\frac{32x(12x-5)^2}{847},\qquad W_{7/8}\le 6/77.
\]

The exact matching source is

\[
 \mu_* = \frac{13}{70}\delta_0+\frac{81}{110}\delta_{5/12}+\frac6{77}\delta_{7/8}.
\]

It has all decay factors strictly below one, shares the four observations exactly, and has total near-unit mass `6/77`. The resulting upper bound is about `0.077922`, despite the independent continuum source's **true** slow-band mass being zero. The learner cannot infer that zero from the early data.

| Number of exact acquired moments | Additional native scalar reactions beyond four moments | **Sharp** upper bound on entire slow-band mass |
|---:|---:|---:|
| 4 | 0 | `6/77` = 0.0779221 |
| 5 | 2 | `36/1073` = 0.0335508 |
| 7 | 6 | `2916/401521` = 0.00726238 |
| 9 | 10 | `46656/30268025` = 0.00154143 |
| 11 | 14 | `46656/144887849` = 0.000322015 |
| 12 | 16 | `839808/5560520833` = 0.000151030 |

The simulator actually acquired all twelve coefficients using **24 scalar Schur reactions**; each two-reaction pair is recorded. The independent verifier reconstructed strictly positive quadrature sources for degrees 2–5 and checked all higher rational dual/Gram/root conditions. These numbers are not merely fitted numerical estimates.

## 3. Noise-aware certificates: why increasing degree may stop helping

In a second readout model, each reported **reciprocal** Schur response is within `10^-8` of its true value. Thus each recovered moment has a deterministic error bound `η=10^-7`, with arbitrary error correlation. The synthetic sensor's actual error was 100 times below its advertised limit.

Every polynomial `q(x)` which is pointwise nonnegative below `b` and at least one above `b` gives the **valid noise-aware bound**

\[
 W_b(\mu)\le \sum_{j=0}^D q_j\widehat m_j
                 +\sum_{j=0}^D|q_j|\eta_j. \tag{2}
\]

This is true even if `q` is chosen adaptively from the reported data, provided its **global** polynomial inequalities are actually checked. The noisy learner independently proposes its quadrature polynomial from its *reported centers*, not from the hidden exact source moments. It rejects a proposal whose modified moment matrix or root conditions fail. **Rejection of a noisy proposal is not rejection of the source class.** Existing certified bounds remain available.

The failure is concrete. After eight additional moments, the exact bounds continue to improve, but the coefficients in the dual polynomial magnify the stipulated error boxes:

| Total moments | Sharp bound if readings were exact | Obtained data-only noisy certificate |
|---:|---:|---:|
| 7 | 0.00726238 | 0.00731053 |
| 8 | 0.00349951 | 0.00364304 |
| 9 | 0.00154143 | **0.00206719** |
| 10 | 0.00073065 | 0.00229327 |
| 11 | 0.00032201 | 0.00700330 |
| 12 | 0.00015103 | no admissible quadrature proposal; retain older certificate |

Taking the minimum of all accepted historical certificates ensures that acquiring more information **cannot worsen the retained guarantee** merely because an optimizer proposes a worse procedure. This is not a new minimax noisy-moment theorem: a stronger semidefinite or set-membership optimizer with the same evidence could do better.

## 4. Inventing a better native experiment: one late impulse pair

For any positive source, measuring just one late coefficient `m_H` yields

\[
 \boxed{W_b(\mu)\le \frac{\widehat m_H+\eta_H}{b^H}},\tag{3}
\]

because `x^H>=b^H` on the entire slow band. The measurement is a **native lag-`H` matched Schur experiment**: one pulse, two scalar reaction readings, and `H+1` units of elapsed experiment time. No intermediate impulse coefficients are measured or assumed.

The executed source gave these finite-noise bounds:

| Newly measured lag | Certified total slow-band upper bound |
|---:|---:|
| 8 | 0.03237331 |
| 16 | 0.00499432 |
| 32 | 0.00022554 |
| 48 | 0.00007324 |
| 64 | 0.00051542 |

**Trade-off.** For a later scientific requirement `W_{7/8}<=0.01`, acquiring the consecutive moments `m_4,m_5,m_6` needs six additional scalar reactions, three active pulses and maximum lag wait `7`, and succeeds for the executed source. A predeclared one-shot lag-16 design instead succeeds with two additional scalar reactions, one active pulse and wait `17`. A capped schedule lag 8 then 16 uses four reactions and succeeds at the second. The long-lag method uses less sensor bandwidth but more time; it is **not** a universal guarantee of success. On an equally compatible source with genuine slow-band mass greater than the threshold it must reject the target.

Past lag 48 the fixed absolute sensor-error floor dominates the decaying true response, demonstrating that longer measurement is not always more informative. Exact waiting time, resets, actuation and readout precision must therefore enter the compiler's objective.

### A sparse polynomial combines old knowledge with one late reading

After the old `m_0..m_3` and new `m_16` are actually observed, a future mass query needs no further source call. I solved a numerical grid LP in the five-dimensional polynomial span

\[
 \operatorname{span}\{1,x,x^2,x^3,x^{16}\},
\]

rounded its proposal to dyadic rationals, and **independently certified the final exact polynomial** by real-root counting: it has no zeros and is positive on `[0,7/8]`, and `q-1` has no zeros and is positive on `[7/8,1]`. Therefore the entire real continuum, not merely the numerical optimization grid, satisfies the proof obligations. The uncertainty charge in (2) uses only the five acquired moments.

Its achieved guaranteed bound was **0.00419523**, versus **0.00499432** from the late coefficient alone—about a 16% reduction in band-mass bound from *no additional experimental readings*. The LP has no role in correctness after the exact root and rational moment certificates pass. This sparse certificate is not claimed sharp over the five-coordinate joint consistency set.

### An indistinguishable-source experiment, not merely a bound

The exact four-moment atomic witness from §2 and the continuum checker source give **identical first eight native Schur reactions**. At lag 16 their impulse coefficients differ by approximately `0.00861108`. A new native pair therefore distinguishes the two mechanisms. For the slow atomic source, the near-band mass is still `6/77`; its late reading correctly fails the `0.01` admission condition. Thus the successful result on the continuum source does not depend on pretending that all compatible sources are benign.

## 5. A separate falsification operation: nonlinear memory hidden from *all* single-pulse measurements

The strongest remaining epistemic assumption is that measured impulse coefficients describe **linear** causal superposition. No number of single-pulse tests alone establishes that assumption.

I constructed a four-port source that changes the internal response law to

\[
 q_t=q_t^{(0)}+\sum_{j<t} g_j u_{t-1-j}
       +\beta u_{t-1}u_{t-2} +\gamma u_{t-1}u_{t-2}u_{t-3},
\]

with the obvious omission of terms before their first causal time. The linear source (`β=γ=0`), pair-interacting source (`β=1/10, γ=0`) and cubic source (`β=1/10, γ=1/50`) produce **exactly the same Schur reactions for every single-pulse history**, at any waiting time. All early positive moments and band-mass calculations thus remain consistent even when the linear superposition premise is false.

At time `t=2`, use synchronized factorial conditions `00`, `10`, `01`, `11`, with each active pulse of amplitude `δ=1/5`. The first two raw reactions (`00` and `10`) were already retained at this time by the ordinary impulse-acquisition record. Two **new** native scalar readings complete the experiment. On the reciprocal-reaction scale,

\[
 Z_{11}-Z_{10}-Z_{01}+Z_{00}=\beta\delta^2=1/250.
\]

The compiler acquired `β=1/10` and, using only the twelve already purchased impulse coefficients and this interaction estimate, exactly predicted eight newly specified multi-pulse source reactions. No new learner source calls were made for those questions; independent physical-source calls used by the checker remain separate.

A source with an additional cubic interaction gives *all the same earlier readings*, including the factorial four-point test, but differs under a genuinely overlapping triple pulse by `1/6250` in reciprocal response. This is a decisive counterexample: even successful pairwise interaction testing cannot prove the absence of higher-order memory. The appropriate next intervention is a triple-overlap factorial test, or an explicit UNKNOWN if unavailable. With reciprocal error ≤`10^-8` per response, the four-reading contrast certifies `β` to error ≤`10^-6`, regardless of error correlation. Any later predictions must propagate that bound and other unmeasured interaction terms.

## 6. What is acquired and what remains supplied

The learner acquires actual finite scalar Schur histories, mathematically certified compatibility families, exact or noisy upper bounds on the **total** slow spectral band, and executable extra experiments that address later tasks. It also acquires a test that falsifies the linear superposition model when nonlinear pulse interactions are present.

It does **not** acquire the positive spectral representation, prove time invariance, guarantee matched resets in a real apparatus, discover an unobserved uniform decay ceiling or certify infinite-horizon gain. The bounded slow-band mass does not bound the DC gain: if even a tiny permitted mass sits at `x` arbitrarily close to 1, its contribution `w/(1-x)` remains unbounded. A nonzero slow-band certificate is therefore useful for finite-time exposure decisions, not a proof of indefinitely stable operation.

The equally informed alternatives include classical Gauss–Radau/Markov–Stieltjes truncated-moment solvers, semidefinite moment relaxations, Lipschitz/robust statistics and ordinary nonlinear system identification. They can copy the construction and tie or improve it. There is no claim of new quadrature mathematics, exclusive agent superiority, device feasibility, or newly discovered physical law.

The strongest next research attack is a physically realizable, independently calibrated **band-selective sensor** with a proven time–precision–actuation trade-off, alongside intervention tests that distinguish genuinely linear positive spectral memory from higher-order and nonstationary source effects. Such an interface could yield useful slow-mode certification without ever assuming a finite spectral order.

## 7. Executed artifacts and verification

- `acquired_spectral_memory.py`: preserved exact native Schur instrument dependency, copied from the preceding verified experiment.
- `band_risk_compiler.py` and `band_risk_results.json`: actual 24-native-reading acquisition, every degree-1–11 exact quadrature certificate and observed noisy certificates.
- `long_lag_probes.py` and `long_lag_results.json`: long-lag native reaction experiments and honest time/bandwidth trade-off.
- `sparse_shaped_certificate.py` and `sparse_shaped_results.json`: sparse new-task dual, optimization proposal, dyadic rounding, exact continuum nonnegativity certificates.
- `slow_source_discrimination.py` and `slow_source_discrimination_results.json`: exact indistinguishable historical raw reactions followed by a distinguishing late experiment.
- `intervention_nonlinearity_guard.py` and `nonlinearity_guard_results.json`: native factorial acquisition and nonlinear superposition counterexamples.
- `independent_verify_band.py` and `independent_verification_results.json`: independent exact audit (220 successful checks) reconstructing the numerical claims without invoking the producer scripts.

All results files are actual executed outputs, not placeholders. The raw native reactions, added source calls, independent checker operations, rational coefficients, and mathematical premise boundaries are preserved. The archive is generated locally for handback and is not automatically committed to the Astra repository.

**Classical background:** NIST Digital Library of Mathematical Functions, [§3.5 Gaussian quadrature](https://dlmf.nist.gov/3.5); explicit [Chebyshev–Markov–Stieltjes inequalities](https://link.springer.com/article/10.1186/s13660-015-0709-1); Shohat & Tamarkin, [*The Problem of Moments*](https://doi.org/10.1090/surv/001). These are antecedents and comparators, not priority evidence for this software integration.
