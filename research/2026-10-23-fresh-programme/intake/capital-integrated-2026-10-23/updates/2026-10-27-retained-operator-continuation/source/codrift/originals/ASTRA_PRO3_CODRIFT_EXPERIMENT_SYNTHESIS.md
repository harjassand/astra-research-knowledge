# Astra Pro3 — Joint physical-source and instrument co-drift: task-directed experiment synthesis

27 October 2026. Conditional mathematical research and native Schur-source computations. The programme continues the preceding `ASTRA_PRO3_SELF_CALIBRATING_ACTIVE_INTERFACE.md` and `ASTRA_PRO3_ACQUIRED_PORT_ELIMINATION_AND_ACTIVE_INTERFACES.md` using their stated physical interface rather than substituting an imaginary direct-Hessian oracle. Every reported native acquisition is a configured scalar boundary-reaction calculation. Independent checkers can inspect the source but the acquisition compiler receives only the reported scalar reactions and public contracts.

## 1. What the learner acquires, and what remains supplied

Let `T(t)` be a hidden symmetric positive-definite `r×r` stiffness, `H(t)=T(t)^{-1}`, and let `b=3/2` be a *known stable* boundary baseline. A configurable rank-one shunt commanded with nominal strength `λ>0` and hidden coupling vector `v` has unknown actual gain `κ(t)>0`. Native Schur elimination gives the physical scalar reaction

\[
 y(t,v,\lambda)=b+\frac{\kappa(t)\lambda}{1+\kappa(t)\lambda v^\top H(t)v}.
\]

Using the **observed** reciprocal `z=1/(y-b)` and `x=1/λ`, it becomes

\[
 \boxed{z(t,v,x)=v^\top H(t)v+xh(t)},\quad h(t)=1/\kappa(t).\tag{1}
\]

Previously the source was static while the gain was either static or separately time-calibrated. Here **both drift**. The strongest exact theorem assumes, on a declared operating horizon,

\[
 H(t)=H_0+tH_1,\qquad h(t)=h_0+t h_1,\qquad \tfrac13 I\preceq H(t)\preceq I,\quad h(t)>0.\tag{2}
\]

Affine co-drift, exact source linearity, ability to command the physical shunts, and stability of `b` are **supplied experimental contracts**, not learned merely because a finite fit passes. The learner acquires parameter combinations from actual readings. Code-level prediction of an unmeasured future configuration follows only on the contract's horizon and only for an operation whose controller/source response is specified.

For a fixed coupling `v`, write `q(t)=vᵀH(t)v=q₀+tq₁`. Each reciprocal report is

\[
 z(t,x)=q_0+xh_0+tq_1+txh_1.\tag{3}
\]

All output counts in this note are scalar reactions (one number per configured experiment); the host's matrix inversion, rational arithmetic, and physically charged switches are separate costs. Future source-aware checks are **not** granted to the learner.

## 2. The three-reading task-only acquisition (ABA)

A later scalar scientific task requests `q₀` at target epoch `t=0`; it does not request complete source or gain drift. Take **three distinct-time** readings with times `(-τ,0,+τ)` and reciprocal commanded strengths `(2,1,2)` (nominal strengths `(1/2,1,1/2)`). Then

\[
 z_{-}=q_0-\tau q_1+2(h_0-\tau h_1),\quad
 z_0=q_0+h_0,\quad
 z_{+}=q_0+\tau q_1+2(h_0+\tau h_1).
\]

Consequently

\[
 \boxed{q_0=2z_0-\tfrac12(z_{-}+z_{+})}.\tag{4}
\]

This removes the **physical drift** `q₁`, instrument drift `h₁`, and even the instrument intercept `h₀`, without estimating any of them. An exact native two-hidden-port source check at `τ=1/10` recovered `H₁₁(0)=3/5` with three source calls.

The restricted two-reading lower bound follows because each measurement row lies in the four-dimensional parameterization `(q₀,h₀,q₁,h₁)`. With two distinct times and both positive `x_i`, a functional recovering `q₀` would need coefficients `α_i` satisfying `Σα_i x_i=Σα_i t_i x_i=0`. The 2×2 Vandermonde matrix is invertible, forcing both coefficients zero, contradicting `Σα_i=1`. This also excludes a deterministic adaptive two-reading procedure along an interior-source transcript. Two *simultaneous* readings at the same time with different strengths would suffice, but that is a different experimental interface and does not establish a saving under nonzero switching time.

The exact-rational control also shows that naively treating two different-time calibration readings as contemporaneous yields `q̂₀−q₀=7/150≈0.0466667` on the acquired fixture, despite every raw reaction being exactly evaluated.

## 3. Four-reading recovery of both affine drift trajectories (ABBA)

Use **four sequential readings** at `t=(-3τ,-τ,+τ,+3τ)` and `x=(2,1,1,2)`, where the physical strength pattern is A–B–B–A. Set

\[
 A_0=\tfrac12(z_{-3}+z_{+3}),\quad B_0=\tfrac12(z_{-1}+z_{+1}),
\]
\[
 A_1=(z_{+3}-z_{-3})/(6\tau),\quad B_1=(z_{+1}-z_{-1})/(2\tau).
\]

Then the entire affine source and instrument trajectory for this configuration is acquired:

\[
 \boxed{q_0=2B_0-A_0,\quad q_1=2B_1-A_1,\quad h_0=A_0-B_0,\quad h_1=A_1-B_1.}\tag{5}
\]

Every right-hand quantity is computed from real native scalar reports. No separate grounded gain-calibration experiment is hidden. The proof is substitution into (3), where symmetric averages cancel odd time terms and symmetric differences recover the odd coefficients. The four rows are full rank for `τ>0`, so four calls are necessary to identify **all four** scalar-trajectory coefficients over an open class, including adaptive deterministic plans.

## 4. Complete `r`-port affine co-drift source: `2(d+1)` calls

Put `d=r(r+1)/2`. There are `d+1` unknown coefficients in each time epoch (`vech H₀,h₀`) and (`vech H₁,h₁`), so **`2(d+1)`** independent real parameters. Each configured scalar reciprocal observation is a linear row

\[
 a(t,v,x)=(c(v),x,t c(v),tx),\quad c(v)=\operatorname{vech}_{\rm sym}(vv^\top).
\]

A full-rank design identifies them all; fewer scalar reports cannot identify the complete trajectories over an interior source class. Along any fixed adaptive transcript, the chosen rows are fixed and have a nonzero null direction if fewer than `2(d+1)` reports have been returned; a small perturbation keeps both hidden positive source trajectories and gain trajectories admissible while preserving the entire transcript.

**Achievability with distinct timestamps:** perform `d+1` independent settings near a negative time and `d+1` corresponding settings near a positive time, perturbing their timestamps to make them strictly distinct. At coincident ideal clusters the design matrix factors into two invertible blocks; its determinant remains nonzero under sufficiently small timestamp perturbations. This is an existence construction that explicitly pays source calls, rather than assuming that `d+1` settings can be performed simultaneously.

**Executed `r=2` control:** eight separate scalar Schur reactions at rational times `-0.30,-0.29,-0.28,-0.27,+0.27,+0.28,+0.29,+0.30` gave a nonzero rational design determinant `10556001/25000000`. The learner reconstructed all eight coefficients of `(H₀,h₀,H₁,h₁)` exactly. Then **24 newly specified scalar shunt reactions and 12 later symmetric/nonsymmetric feedback equilibria** were computed correctly from retention with **zero further learner source calls** (36 separately charged, source-aware checker evaluations). The controller operates in the stipulated stable range, and a downstream controller does not become a free native action merely because its formula is known.

These are full-identification costs. The three-call `q₀` and the gain-free contrast below have different, narrower future-task coverage and should not be conflated with full tomography.

## 5. Joint physical and sensor curvature: sharp protocol-specific minimax error

Affine drift is brittle. Replace exact affineness for one probe by the weaker, independently supplied local class

\[
 |q''(t)|\le B_q,\qquad |h''(t)|\le B_h,
\]

with **adversarial error at most `ε` in each reciprocal report `z`**. The next two bounds apply to the specified original protocols, not to arbitrary alternative schedules.

For the three-call ABA estimator, Peano-kernel integration or the symmetric Taylor remainder gives

\[
 \boxed{\mathcal E_{\rm ABA}=\tau^2(B_q/2+B_h)+3\epsilon.}\tag{6}
\]

For the four-call ABBA estimate of the reference-time `q₀`, write it as `2 average(z at ±τ) − average(z at ±3τ)`. The `q` error kernel is everywhere nonpositive, with integrated absolute area `7τ²/2`; the `h` error kernel is nonpositive, with area `8τ²`. The measurement decoder has absolute coefficient sum three. Thus

\[
 \boxed{\mathcal E_{\rm ABBA}=\tau^2(7B_q/2+8B_h)+3\epsilon.}\tag{7}
\]

**Sharpness, not just an error-propagation formula.** Take center `q_c=3/5`, `h_c=4/5`, bounded curvature constants `B_q=1/40`, `B_h=1/50`, and reciprocal noise `ε=1/10000`. For either fixed protocol, let `E` be the claimed radius and set source pairs

\[
 q_{\pm}(t)=q_c\pm(E+B_qt^2/2),\quad
 h_{\pm}(t)=h_c\pm(d_h+B_ht^2/2).
\]

For ABA, `d_h = -2ε − τ²(B_q/2+B_h)`; for ABBA, `d_h = -2ε − τ²(4B_q+17B_h/2)`. Direct rational substitution verifies that **both** positive physical sources' true reciprocal reactions lie within exactly `ε` of *the same reported values* at every protocol time, while the requested center-time `q₀` values differ by `2E`. This holds with full positive hidden 2×2 blocks `diag(q(t),2/3)` and positive gain throughout the declared test domain. Therefore no estimator—including nonlinear adaptive postprocessing of the same fixed observation schedule—can guarantee error less than `E`. The simple linear decoder attains the upper bound.

The executed sharp radii were `129/40000 = 0.003225` for ABA with `τ=3/10`, and `111/40000 = 0.002775` for ABBA with `τ=1/10`; both schedules span `[-0.3,+0.3]`. These numerical values compare distinct protocols and capabilities, not globally optimized equal-intervention methods.

**Raw instrument error is separate.** If the native reaction has bounded absolute error `η`, and all physically possible exact reciprocal responses satisfy `0<z<=Z` with `η Z<1`, then

\[
 |\widehat z-z|\le\eta Z^2/(1-\eta Z).\tag{8}
\]

This is a justified worst-case transformation from raw sensor error into the reciprocal-error contract. It may not be minimax tight for the original raw sensor model, so (6)–(7) must not be relabelled sharp *raw-reaction* minimax rates. An exact-rational example with `η=10⁻⁶` and `Z=14/5` was verified.

## 6. Precision-aware timing/strength compiler

For general four-call symmetric schedules `(-R,-u,+u,+R)` with outer reciprocal strength `x_A`, inner reciprocal strength `x_B`, define

\[
 \alpha_A=\frac{x_B}{x_B-x_A},\qquad
 \alpha_B=-\frac{x_A}{x_B-x_A}.
\]

The estimator is `α_A average(z_outer) + α_B average(z_inner)`. It cancels unknown constant and linear time terms in both `q` and `h`. Its **exact sharp curvature kernel norms** for given time and gains are

\[
 C_q=\int_0^R|\alpha_A(R-s)+\alpha_B(u-s)_+|\,ds,\quad
 C_h=\frac{|\alpha_A x_A|}{2}(R^2-u^2).\tag{9}
\]

For an instrument supplying only bounded raw reaction error `η`, use the public `Z(x)=1+0.9x` (from source spectra and `3/4<=h<=9/10`), and set `E(x)=ηZ(x)^2/(1−ηZ(x))`. A sound, source-oblivious acquisition objective is

\[
 \mathcal U=B_q C_q+B_h C_h+|\alpha_A|E(x_A)+|\alpha_B|E(x_B).\tag{10}
\]

This is a rigorously certified **upper bound**, not globally sharp raw-error minimax. Search the public finite catalogue, including hardware constraints, *before* querying the source. All design comparisons and sign-change integrals are rational; independent verification recomputes the Peano areas by a different geometric formula.

**Executed design:** `R=3/10`, minimum adjacent time separation `1/20`, strengths drawn from `[1/2,3/4,1,5/4,3/2,2,3,4]`, `Bq=1/40`, `Bh=1/50`, raw `η=10⁻⁶`, and total nominal strength cost at most seven for four calls. Among **288** eligible designs, the canonical ABBA `(λ_A,λ_B,u)=(1/2,1,1/10)` has `U≈0.002490060`. At the *same* total nominal strength `3`, choosing `u=1/4` instead gives `U≈0.001127560` (2.21× reduction). Allowing total strength `7`, `(λ_A,λ_B,u)=(1/2,3,1/10)` gives `U≈0.000488596` (5.10× reduction versus canonical). Catalogue optimality is exact; continuous-source/hardware and overall amortized-resource optimality are not claimed.

## 7. New operation: gain-free signed scientific contrast during co-drift

Let the later question request `vᵀH(0)v−wᵀH(0)w` rather than an entire hidden response. With the **same fixed nominal strength**, take `v` at `−τ,+τ` and `w` at `0`. Under affine source and gain drift,

\[
 \boxed{L=(z(-\tau,v,x)+z(+\tau,v,x))/2-z(0,w,x).}\tag{11}
\]

The shared `h₀,h₁` cancel, as does the physical response slope along `v`. This **three-call gain-free** procedure recovers `H₁₁(0)−H₂₂(0)=−1/15` exactly for the native 2-port control, without ever estimating `h₀` or `h₁`. With only two measurements at distinct times, cancellation of two independent gain nuisance coefficients `h₀,h₁` again forces both decoder weights to zero; hence three are necessary for nonzero contrasts under this interface. This is task-specific acquisition once the contrast is requested, not universal free transfer to unforeseen contrasts.

## 8. New physical operation: identifying one-step intervention-induced source change

The earlier proofs require that configuring a shunt does **not** change the hidden physical source within a measurement. A stronger, explicitly causal but still supplied contract permits the *previous* shunt setting to change the next response:

\[
 H(t;w)=H_0+tH_1+\beta w e_1e_1^\top,\qquad h(t)=h_0+t h_1,
\]

where `w` is the *known nominal strength of the immediately preceding intervention*, `w=0` before any prior shunt, and `β` is an unknown carryover coefficient. The current reaction is evaluated by **native Schur elimination using this modified hidden stiffness**. It is not computed by feeding an assumed `H` vector oracle into the learner.

For `v=e₁`, each reciprocal reading becomes the linear regression row

\[
 z_i=q_0+t_i q_1+x_i h_0+t_i x_i h_1+\beta w_{i-1}.\tag{12}
\]

This is now a **five-parameter** model. I constructed a five-reading plan at five different times with previous-strength histories actually generated by the earlier interventions. Its design determinant is `-3/64`, and it exactly recovers `(q₀,q₁,h₀,h₁,β)` with native experimental calls. Four calls are insufficient for full parameter recovery on any interior source family: every fixed four-row adaptive transcript has a null direction, and a small perturbation retains source spectra, gain positivity, and the same observations.

**Executed:** `β=1/100` was acquired from five scalar configured experiments. Eighteen later source configurations, specified only after acquisition and involving three new times, three new preceding-action strengths and two new current strengths, were predicted exactly from the retention; independent source-aware checks used the physical network model and did not furnish the learner with extra readings. The future experimental *interventions* themselves remain physically paid; the zero refers only to further **learning/acquisition** calls. Ignoring the memory term and running the old four-call ABBA decoder would misidentify `q₀` by exactly `1/100`.

**Causal-model limitation:** an alternative source with additional nonlinear history term

\[
 \delta w(w-1/2)(w-2)e_1e_1^\top,\qquad\delta=1/100,
\]

returns exactly the same five original native reactions because only histories `w∈{0,1/2,2}` were observed. For a new preceding strength `w=1`, the hidden quadratic response differs by `-1/200`, and a purposefully added preparation intervention plus one source reading distinguishes the two alternatives (raw reaction separation `20/8381`). Thus the finite five-call success does not infer absence of nonlinear or longer-lasting actuation memory. An actual apparatus needs tested intervention-history and recovery-time contracts.

## 9. Decisive failures: finite fits cannot justify source or instrument drift contracts

**Changing physical source despite an exact four-call fit.** The smooth analytic function

\[
 P(t)=(1-t^2/\tau^2)(1-t^2/(9\tau^2))
\]

vanishes at all four ABBA acquisition times but satisfies `P(0)=1`. Two sources with `H₁₁^±(t)=H₁₁^{\rm affine}(t)±P(t)/100`, identical gains and identical other coefficients are strictly positive and return every *same* historical configured reaction exactly, yet differ at target time `0` by `0.02`. This imposes a worst-case radius `0.01` when the affine source law is withdrawn. They need not both obey the earlier tight curvature bounds; those are a separate, explicitly stated source class.

**Physical source stays affine but instrument drift is quadratic.** The same original ABBA record is also compatible with an alternative `H'=H+δ e₁e₁ᵀ` together with

\[
 h'(t)=h(t)-17\delta/16+\delta t^2/(16\tau^2),\quad \delta=1/100.
\]

The four reaction reports are identical and all source parameters remain positive. The target source response differs by `δ` at `t=0`. A **fifth freshly paid measurement** at `t=0` breaks this particular disguise; its raw scalar reaction difference is exactly `5/15673≈0.000319`. Independent raw error less than half that separation can reject the false affine-gain source in this control. Passing any finite test still cannot certify unrestricted gain stability or absence of intervention-induced backaction.

**Instrument intervention changes the source.** The reciprocal identity only describes a fixed underlying hidden matrix *during a configured measurement*. If the matrix itself depends arbitrarily on shunt choice, a reparameterization of the hidden response and configuration-induced perturbation can preserve every accessible reading. That is a genuine missing physical contract, not a recoverable source parameter under the present proof. Hardware switching time, heating, contact hysteresis, and wear are not charged by the synthetic model and must be explicitly tested for actual implementation.

## 10. Comparison with the strongest same-information alternative and scientific status

An equally informed classical retaining system-identification algorithm can apply the reciprocal transform, polynomial time regression, counterbalanced experiments, optimal-recovery Peano kernels, interval arithmetic and linear algebra to achieve **the same procedures and error bounds**. ABA/ABBA counterbalancing and drift checks have established experimental-design ancestry; the NIST engineering statistics handbook warns that time-confounded measurement order can obscure process drift (https://itl.nist.gov/div898/handbook/pmd/section4/pmd443.htm). This note makes no priority claim for the component mathematics or for experimental reversal designs.

The original new mechanism is a **task-to-native-experiment compiler over co-drifting scientific and measurement parameters**, with explicit distinction among: acquiring one requested physical invariant (3 calls), acquiring two complete scalar drift trajectories (4 calls), acquiring an entire hidden multiport model at all future times inside its declared affine horizon (`2(d+1)` calls), selecting observation times/strengths for robust precision, and rejecting incompatible physical source contracts when fresh evidence supports rejection.

The next substantive question is how to **acquire a physically justified contract about source backaction and gain drift without assuming their functional form**, with randomized negative controls, extended intervention-history probes, and falsifiable recovery-time restrictions. The conditional first-order carryover construction above is an initial executable mechanism, not the resolution of this general question. A finite fit is not a proof of global regularity. No experimental hardware, new physical law, general intelligent-science breakthrough, or architecture advantage has been established.

## 11. Actual executable research

Files in this same directory:

- `codrift_primitives.py`: independent full-network Schur source and rational helpers.
- `affine_codrift_acquisition.py` and its `_results.json`: ABA, ABBA, eight-call full affine tomography at distinct times, matching ambiguity witness, 24 later new reactions and 12 later controllers.
- `curvature_and_no_go.py` and its `_results.json`: matched sharp ABA/ABBA error and source-pair witnesses, raw-reaction error conversion, analytic nonaffine impossibility.
- `task_quotient_and_falsifier.py` and its `_results.json`: gain-free contrast, naive static calibration failure, instrument-curvature ambiguity and fifth-call falsifier.
- `robust_time_design.py` and its `_results.json`: exact-rational 288-plan time/strength search.
- `causal_backaction_acquisition.py` and its `_results.json`: five-call intervention-memory acquisition, 18 new history-dependent reactions, biased old decoder and nonlinear-carryover indistinguishable source.
- `verify_codrift.py` and `independent_verification_results.json`: source and future-equilibrium checks using whole-matrix inversion rather than imported producer code, independent sharp witness checks and different Peano-kernel integration geometry, including all 288 catalogue comparisons.
- `clean_replay.py` and `clean_replay_results.json`: isolated subprocess execution and byte-for-byte comparison of results.
- `SHA256_MANIFEST.json`: preserved hashes of proof, code and results.

No historical sandbox path is referenced as a current output. No change has been made to the Astra knowledge repository.
