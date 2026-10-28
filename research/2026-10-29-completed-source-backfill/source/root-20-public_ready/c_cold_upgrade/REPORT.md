# Task C — global regret from scalar reactions

**Outcome.** Yes, under the separately warranted physical shape, reset and error contracts. An audit at a supplied proposal needs the `n+1` scalar report values at `x` and `x+h_i e_i`. It gives a bound against **every** action in the dose simplex, without learning microscopic coefficients or matrix dimension. The requested synthetic check gives

\[
\sup_{y\ge0,\;\mathbf1^Ty\le1/5}\{G(y)-G(x)\}
\le 0.144409859210197.
\]

This is an outward-rounded bound from the published curvature constants. An elementary dimension-free refinement, proved below, gives the stronger bound `0.142506013134265` from the same three reports. These are certificates of this proposed action, not claims that it is near optimal to an unspecified tolerance.

**Source and acceptance boundary.** All source conclusions here are pinned to public commit `6360a39d9488a041f259181e38c37e638b83c609`. The governing result was discovered as `N1090-matrix-concave-scalar-audit-and-excitation-limits`, rather than supplied as a card ID. I read its current packet, all three cited sources, and the current cost-scope review. Decisive sources are:

- [Shape/finite-difference proof](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/shape/ASTRA_PRO3_MATRIX_CONCAVE_CLASS_AUDIT.md#L13-L77): physical contract and reciprocal intervals at lines 13–37, shape transfer and derivative identity at 39–55, acquisition, finite differences, corrected lower endpoint and simplex certificate at 59–77. SHA-256 `0fbfd812cecf613c61a2b77e77a6feb1eff563ef70de2c8a6136c057e0ebeb8a`.
- [Completed analytic review](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/curator/RESPONSE_PHYSICAL_REVIEW.txt#L42-L69), lines 42–55: the monotonicity correction and exact decreasing-actuator counterexample; lines 57–69: conditional excitation/counting scope and missing execution evidence. SHA-256 `fd3752734939993fc62ab98d64cdd4bdf56fe11a80a665e4d4a5fd3570fcf258`.
- [Current version-bound review](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/knowledge/reviews/A1112-response-and-physical-interfaces-cost-v2.json): `accepted_internally_verified` for the conditional mathematics, corrected finite differences, simplex composition and stated cost scope. Its acceptance does not include the unavailable source-specific numerical archives or physical realization. [Current packet](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/knowledge/current/packets/N1090.json) carries both the monotonicity and acquisition-cost corrections.

The main source's printed Theorem 2 includes `max(-c_i, ...)` in its lower endpoint. Its own proof at line 75 and the current review explicitly restrict this clipping to additional monotone actuation. I **omit** it throughout. Uniform SPD and Loewner concavity do not imply coordinatewise monotonicity: `Q(u)=2-u`, `e=1`, `c=0` already has negative benefit derivative. The source's historical numerical experiment is not used as data for this task.

**Reusable acquisition and proof.** Write

\[
D=\{u\in\mathbb R_+^n:\mathbf1^Tu\le\delta\},\qquad
\operatorname{Reg}_c(x)=\sup_{y\in D}[G_c(y)-G_c(x)].
\]

The supplied input is a feasible `x`, positive steps `h_i` with `sum(x)+h_i<=delta` for each coordinate, a fixed physical source/readout, valid deterministic error `epsilon`, uniform operator-norm caps, and an independently established **joint** Loewner-concavity contract over the whole simplex. The finite differences need C2 regularity on their segments; the source states C2 on a neighborhood. All norms below are Euclidean vector norms or induced matrix 2-norms. The readout identity presupposes fixed nonzero `e`.

1. Prepare/reset the same source at `x` and at each separate `x+h_i e_i`, obtaining one report per point. A perturbation vector containing all the steps is not a substitute for the separate points. Retain the exact doses, source/reset/calibration identity and report error envelope. Already acquired, compatible values at these exact points may be reused; only missing points require new preparations.
2. At every point require `r-epsilon>3/2`, then transform its raw report to

   \[
   [a,b]=\left[\frac1{r+\epsilon-3/2},\frac1{r-\epsilon-3/2}\right].
   \]

   Denote the interval at `x` by `[a_0,b_0]` and at `x+h_i e_i` by `[a_i,b_i]`. If the lower denominator is nonpositive, this particular reciprocal acquisition does not supply a finite upper endpoint; an extra bound or improved readout is needed. No independence or stochastic concentration assumption is used.
3. Supply a sound coordinate curvature cap `M_i` on the corresponding segment. If `||e||` is known, the published choice is

   \[
   M_i^{\rm pub}=\|e\|^2\left(\frac{2L_i^2}{m^3}+\frac{B_i}{m^2}\right).
   \]

   The general question does **not** explicitly supply `||e||`. Therefore directly applying that published numerical formula would add an input. The following elementary deduction removes this issue using the same acquired intervals:

   \[
   \boxed{M_i^{\rm obs}=\left(\frac{2L_i^2}{m^2}+\frac{B_i}{m}\right)
                    \max(b_0,b_i).}
   \]

   This is a segment cap, which suffices for the finite difference; global concavity is still supplied on all of `D`. This refinement is my derivation from the governing proof, not a formula claimed to appear in the packet.
4. Compute the **unclipped** derivative brackets

   \[
   \boxed{\ell_i=\frac{a_0-b_i}{h_i}-c_i,\qquad
   v_i=\frac{b_0-a_i}{h_i}-c_i+\frac{M_i h_i}{2}.}
   \]

5. Return the scalar global certificate

   \[
   \boxed{\operatorname{Reg}_c(x)\le\mathcal B_c(x):=
   \max\left\{-\sum_i x_i\ell_i,\quad
      \max_j\left[(\delta-x_j)v_j-\sum_{i\ne j}x_i\ell_i\right]\right\}.}
   \]

Here is the complete mathematical justification. For any SPD `Q`, completing the square gives

\[
e^TQ^{-1}e=\sup_p(2e^Tp-p^TQp).
\]

For fixed `p`, joint Loewner concavity of `Q(u)` makes the expression on the right convex in `u`; its supremum is convex. Thus `Z` is jointly convex and `G_c=Z(0)-Z-c^Tu` is jointly concave. This rederives the source's inversion/order argument without needing hidden coefficients.

Put `p=Q^{-1}e`. Differentiating yields the source's identities

\[
Z_i=-p^TQ_i p,\qquad
Z_{ii}=2p^TQ_iQ^{-1}Q_i p-p^TQ_{ii}p.
\]

Joint Loewner concavity implies `Q_ii<=0`, so

\[
0\le Z_{ii}\le(2L_i^2/m+B_i)\|p\|^2.
\]

Using `||p||<=||e||/m` proves the published cap. For the dimension-free refinement, instead use

\[
m\|p\|^2\le p^TQp=Z,\qquad
Z_{ii}\le(2L_i^2/m^2+B_i/m)Z.
\]

Convexity along the segment implies `Z(x+t e_i)<=max(Z(x),Z(x+h_i e_i))<=max(b_0,b_i)`. This proves the observed cap using only the supplied physical constants and acquired scalar intervals. Consequently `-M_i<=G_ii<=0` on that segment. Integrating twice gives

\[
\frac{G(x+h_i e_i)-G(x)}{h_i}
\le G_i(x)\le
\frac{G(x+h_i e_i)-G(x)}{h_i}+\frac{M_i h_i}{2}.
\]

The constant `Z(0)` cancels, so the audit does not need a reading at zero. Substituting the reciprocal intervals proves `ell_i<=G_i(x)<=v_i` simultaneously, including adversarially correlated errors. Concavity gives `G(y)-G(x)<=grad G(x)·(y-x)`. A linear function over `D` attains its maximum at `0` or some `delta e_j`; use the lower gradient endpoints for negative coefficients and upper endpoints for nonnegative coefficients. This is exactly the displayed certificate.

The audit consumes `n+1` report values and linear-size arithmetic/storage in the number of controls, with division and comparisons at the required precision. This count excludes the already supplied proposal, independent physical warrant and calibration. A full physical cost must include actual preparations, resets, elapsed time and any proposal/search/refinement calls; it is not zero-cost physical inference. Compute intervals with exact arithmetic or outward rounding. Repeating an adversarial bounded-error report alone does not reduce `epsilon`. At a boundary proposal lacking forward margin, this particular forward-step audit cannot be used without different observations or an independently justified extension.

**Requested synthetic calculation.** The given diagonal entries satisfy `Q>=I`; their first derivative magnitudes are bounded by `(1,2)` and second derivative magnitudes by `(2,4)`. Each diagonal is a concave saturation function, so joint Loewner concavity holds. These facts are verified from the synthetic formula, not inferred from the three readings. Here `||e||^2=2`, hence `M_pub=(8,24)`. Every queried total dose is at most `0.05<0.2`.

For `u=(u_1,u_2)`,

\[
Z(u)=\frac{1+u_1}{1+2u_1}+\frac{1+u_2}{2+4u_2}.
\]

Exact scalar centres, enclosed by the stipulated `epsilon=10^-8`, are:

| Point | Exact report centre `r=R` | Sound reciprocal interval, rounded outward |
|---|---:|---:|
| `(0.02,0.02)` | `667/306` | `[1.471153824510, 1.471153867797]` |
| `(0.03,0.02)` | `35201/16118` | `[1.462082707215, 1.462082749970]` |
| `(0.02,0.03)` | `8819/4042` | `[1.466618265863, 1.466618308883]` |

The actual calculation uses exact rational endpoints, rather than the rounded display table. The published-cap audit produces approximately

\[
\ell=(0.8071074541888162,\;0.4035515628213404),\qquad
v=(0.8471160581479048,\;0.5235601933470202).
\]

The three vertex upper bounds are approximately `(-0.0242131803402031, 0.1444098592101961, 0.0780986857186873)`. Their maximum is the certificate stated above. The new dimension-free cap uses

\[
M^{\rm obs}\approx(5.8846154711871315,17.6538464135613944),\qquad
v^{\rm obs}\approx(0.8365391355038405,0.4918294254148271),
\]

and gives the outward-rounded certificate `0.142506013134265`.

[check.py](producer-workspace/check.py) generated these three centres and implemented the learner calculation with Python `Fraction`. A separate analytic verifier in that file computed the actual synthetic gradient

\[
\nabla G(x)\approx(0.8245562130177515,0.4122781065088757),
\]

checked exact inclusion in both gradient boxes, and checked that each certificate exceeds the exact-gradient tangent upper bound `0.1401745562130178`. For additional calibration only, exact rational bisection on the full-dose edge brackets the actual global regret as approximately `0.09724138445849995` (bracket width below `10^-34`), with optimum near `(0.1883883578467490,0.0116116421532510)`. The global justification is that both partial derivatives stay positive and the edge derivative is strictly decreasing with opposite signs at its endpoints. Neither that gradient nor the optimum is input to the audit. All exact assertions passed. [results.json](producer-workspace/results.json) retains exact fractions and decimal displays. Running `python3 -B check.py` reproduces the check from this directory.

This is a synthetic numerical check under the specified error envelope. No physical source was accessed, reset, calibrated or measured; no real physical acquisition or discovery is claimed.

**Reuse when prices change.** Cache the raw reports/intervals, exact dose points and the physical validity conditions. Since only the linear objective changes,

\[
\ell_i(c')=\ell_i(c)+c_i-c'_i,\qquad
v_i(c')=v_i(c)+c_i-c'_i.
\]

Re-evaluate the same vertex maximum for the same `x`. Both curvature choices and all reports remain reusable if source identity, response units, calibration, reset/reproducibility and the physical/error contracts still hold. The code also checks a concrete reprice to `c'=(1/4,1/10)`: the published-cap certificate becomes at most `0.118409859210197` without any additional report. This certifies that fixed audited proposal; choosing a new proposal may require reports at missing new audit points. Historical acquisition is still paid. Source expiry does not invalidate sound cached interval algebra, but it prevents acquiring missing points.

**What the finite reports cannot establish.** The shape proof is conditional on independently warranted global premises. Finite passive scalar observations do not by themselves establish global Loewner concavity, global derivative/SPD bounds, arbitrary hidden dimension or microscopic coefficients, or continuing source/reset/calibration validity. They can contradict some proposed models; agreement alone does not establish the full physical class. The governing source's lines 110–145 give a specific hidden-threshold indistinguishability/counting construction. I reuse its qualitative mechanism, not its unavailable numerical witness values or a general lower-bound claim.

For a direct synthetic witness for **these three observations**, alter only the first diagonal of the given `Q` by adding

\[
2(u_1-0.03)_+^3.
\]

This is C2, monotone and nonnegative, and vanishes at all three audit points. It preserves `Q>=I` and the same `L=(1,2)`, `B=(2,4)` throughout the dose simplex. Indeed for `t<=0.2`, the new first derivative is `1/(1+t)^2+6(t-0.03)_+^2`. Its extra term is at most `6t^2<=1.2t`, whereas `1-1/(1+t)^2>=2t/(1.2)^2=(25/18)t`, so the derivative remains at most 1 and nonnegative. Its second derivative is `-2/(1+t)^3+12(t-0.03)_+`, lying between `-2` and `12(0.17)-2/(1.2)^3=2383/2700<2`. At `t=0.2` that second derivative is **positive**, so Loewner concavity fails. The original and modified source return exactly the same three noiseless centres despite their different global shape. This elementary task-specific construction is a new check here, not a recovered Astra execution. The assumed separate physical concavity argument is what excludes this alternative.

**Actual retrieval route and exposure.** I read only `TASK_C.txt` from the experiment parent, then the public snapshot's `00_START_HERE.txt` and `knowledge/README.md`. Fast portable `--method content` on the scalar-reaction/global-regret/Loewner-concavity task returned N1090 first; a `structured` cross-check also returned it first. I followed its packet to exact governing sources and verified the stated source SHA-256 values. The adjacent noisy-PSD N1089 result was a candidate, not substituted proof. The misleading point in the applicable source was the printed monotonicity clipping, resolved by the proof and current correction; the historical 510 count is not an audit prerequisite.

The initial general web reader could open the pinned GitHub entry but could not access the deployed library root. Direct public HTTP access and the in-app browser worked. I searched the deployed `knowledge/index.html` for `certify global regret from noisy scalar reactions jointly Loewner concave matrix dose simplex`, observed N1090 first, and opened its compact packet with both current corrections. The page displayed dataset `055d572fc031`; a direct comparison of deployed and snapshot `knowledge/current/manifest.json` found them equal, with full input version `055d572fc03186b88105977483d02360f8fc6016d5edfe7114e3a2c49928bf6d`. No newer live dataset was observed. The live N1090 packet link carried expected SHA-256 `0e3cde0a073a4822a75ad2c0efd2017cdbc4a11f37fe0437272af09faa0e6a1f`.

I attempted optional local `--method agent` once with explicit available physical premises and unavailable monotonicity. It failed with `Agent runtime missing` and directed setup in Python 3.12/3.13 using `knowledge/requirements-agent.txt`. I did not install it or write into the cache: portable content/structured search and deployed web search already supplied the proof. This was a setup limit of the optional ranker, not absent science.

Product context already exposed general Astra evidence/acceptance conventions and unrelated research-topic summaries. It supplied no Task C-specific scalar-audit formula, card ID or fixture result before this retrieval. I did not read memory registries, other chats, experiment protocols/expected scopes, prior study reports or other workers' outputs. Public historical operational text was treated as data. No child agents, paid model calls, hardware operation, publication or cache edits were used. The reused theorem, newly derived dimension-free cap, synthetic verification and remaining physical warrant are distinguished above; no novelty or practical advantage claim follows.
