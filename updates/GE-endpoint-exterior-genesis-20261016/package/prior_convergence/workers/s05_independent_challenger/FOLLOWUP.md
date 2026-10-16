# Frontier B continuation: finite-time dark-echo quotient and a loss-contrast resource law

**Status:** a proved, replayed, model-scoped experimental operation; no physical data and no broad novelty claim. The operation recovers a two-state *dark relaxation rate* from terminal survival without estimating the state-dependent loss coefficients. It also gives a finite-count classifier for s04's exact one-pulse aliases under explicitly supplied control and detector bounds. The best same-information likelihood fits the data at least as well; this is a target and acquisition result, not an algorithmic victory over likelihood.

## Operation and exact theorem

Use column probabilities. Let

\[
A=\begin{pmatrix}-a&r\\a&-r\end{pmatrix},\quad
D=\operatorname{diag}(d_1,d_2),\quad M=A-uD,
\qquad a,r,u>0,
\]

where **OFF** evolves under the closed generator `A`, **ON** under the killed generator `M`, and the detector measures total surviving mass `c=(1,1)`. For any initial probability vector `b`, ON durations `t1,t2>=0`, and dark wait `W>=0`, define

\[
Y(W)=c e^{Mt_2}e^{AW}e^{Mt_1}b,\qquad
C(W)=Y(W)-Y(0).
\]

Write `g=a+r` and stationary vector `π=(r,a)^T/g`, with `Π=πc`. Since `e^{AW}=Π+e^{-gW}(I-Π)`,

\[
C(W)=(1-e^{-gW})B,\quad
B=c e^{Mt_2}(\Pi-I)e^{Mt_1}b.
\]

Consequently, whenever `C(W) != 0`, **three finite settings** at dark waits `0,W,2W` give

\[
\boxed{\frac{Y(2W)-Y(0)}{Y(W)-Y(0)}=1+e^{-gW}},\qquad
\boxed{g=-W^{-1}\log\!\left(\frac{Y(2W)-Y(0)}{Y(W)-Y(0)}-1\right)}.
\]

This identity does not require `D`, `u`, `b`, or the gain to be known. A terminal readout `p_j=f+qY(jW)` with a common unknown offset `f` and gain `q>0` has the **same quotient**. The two-state assumption, a truly loss-free OFF phase, common affine readout, fixed ON pulse conditions, and nonzero contrast are essential. For a model with more than two dark modes the contrast is a sum of exponentials; the three-setting formula is then invalid, and a successful fit is not a two-state proof.

In fact the ON exponentials may be replaced by **any fixed unknown linear preparation and probe maps** `P,Q`: `Y(W)=cQe^{AW}Pb` has the same quotient. The ON dose and microscopic loss law need not be calibrated for the exact identity, provided the physical maps `P,Q` are reproduced across all three waits. Their drift, or a different terminal readout after different waits, breaks the cancellation.

The preparation/observation factor is explicit. Let `x=e^{Mt1}b`, `S=cx`, `g=a+r`; then

\[
B=(aS/g-x_2)\,c e^{Mt_2}(e_2-e_1).
\]

Writing `m=tr(M)/2` and `κ=\sqrt{((M_{11}-M_{22})/2)^2+ar}`,

\[
c e^{Mt}(e_2-e_1)
=u(d_1-d_2)e^{mt}\frac{\sinh(\kappa t)}{\kappa}.
\]

Thus the quotient is unavailable at uniform loss (`d1=d2`), zero probe duration, or an unprepared stationary population. With `b=e1,t1=0`, its amplitude is

\[
C(W)=\frac{a}{g}(1-e^{-gW})u(d_1-d_2)
e^{mt_2}\frac{\sinh(\kappa t_2)}{\kappa}.
\]

The s04 one-pulse aliases `H0=(a,r,d1,d2)=(2,1,2,3)` and `H1=(1,1,2,4)` both have the exact ON-only transfer `c(sI-M)^{-1}e1=(s+6)/(s²+8s+14)` at `u=1`, yet the dark-echo quotient is `1+e^{-3W}` versus `1+e^{-2W}`. A finite classifier for these aliases need not use both ON segments: `t1=0` is a valid boundary case (OFF then ON). For a stationary or unknown initial ensemble, a positive preparation pulse may be needed.

**Clock-matched acquisition.** All three arms can be read at the same final time `t1+t2+2W`: after the final ON segment of arm `j`, append an OFF idle of duration `(2-j)W`. Closed OFF evolution preserves total survival. This equalizes assay age without changing the identity. Randomization/interleaving and an independent dose monitor remain needed to bound arm-specific drift. The control timing, OFF leakage, affine detector stability, independent resets, and state-insensitive terminal readout are **acquisition requirements**, not inferred from the algebra or from synthetic counts.

## Finite-sample certificate for the quotient

Run `N` independent Bernoulli terminal-survival trials per arm and let `p̂_j` be the three observed frequencies. For confidence level `1-α`, set

\[
\epsilon_N=\sqrt{\frac{\log(6/\alpha)}{2N}}.
\]

Hoeffding and a union bound give `|p̂_j-p_j|<=epsilon_N` for all three arms with probability at least `1-α`. Each empirical difference `Ĉ_j=p̂_j-p̂_0` is then within `2epsilon_N` of the true contrast. If the two empirical differences have the same established sign, `|Ĉ_1|>2epsilon_N`, and the following interval lies strictly in `(1,2)`, then

\[
R\in\left[
\frac{|\widehat C_2|-2\epsilon_N}{|\widehat C_1|+2\epsilon_N},
\frac{|\widehat C_2|+2\epsilon_N}{|\widehat C_1|-2\epsilon_N}
\right]=[R_-,R_+],
\quad
g\in\left[-\frac{\log(R_+-1)}{W},
            -\frac{\log(R_--1)}{W}\right].
\]

Otherwise the output is **UNKNOWN**. The interval covers under the stated independent Bernoulli and common-affine-readout assumptions; it does not diagnose model misspecification. In the synthetic alias replay with `t1=0,t2=0.31,W=0.525,q=0.8`, `N=10,000,000` *per arm* (30 million total) and seed `8749`, the 95% Hoeffding intervals are `[2.574,3.627]` for true `g=3` and `[1.734,2.254]` for true `g=2`. These are **synthetic** demonstrations, not physical feasibility or measured confidence intervals.

The count is substantial because the observed first-wait contrasts are only about `−0.0392` and `−0.0482` after gain. More efficient likelihood intervals are possible; three Bernoulli means with unknown baseline, amplitude, and `g` form a saturated three-parameter model. When the sample proportions are feasible, the quotient estimator is exactly its maximum-likelihood fit, so there is no claim that quotient estimation outperforms the strongest same-information likelihood incumbent.

Three points alone cannot validate the assumed two-state OFF model, because the fit is saturated. A **held-out fourth wait** has the exact prediction `p_3=p_0+(p_1-p_0)(1+z+z²)` with `z=(p_2-p_0)/(p_1-p_0)-1`, again independent of common affine readout. A failed fourth-wait confidence check rules out the fixed two-state/constant-readout combination; a pass is limited evidence and does not prove that microscopic model.

## Finite-time classifier with explicit drift margins

A much cheaper task is to distinguish the **specified** s04 aliases. Use an ON-only reference of duration `t=0.275` (padded with OFF to the same final clock) and an OFF-then-ON assay with dark wait `W=2`. Both have the same ON time. Assume the ON dose of *each* arm is independently in `[0.995,1.005]`; reference detection gain `q_R>=0.75`; and the echo/reference gain ratio is in `[0.995,1.005]`. Assume no unknown additive readout offset for this two-arm classifier. These are externally supplied or independently monitored control guarantees.

The Feynman–Kac path formula makes survival monotone decreasing in ON dose, so endpoint evaluation gives rigorous ratio enclosures without assuming the arms share exactly the same dose:

| World | Nominal reference `Y_R` | Nominal echo `Y_E` | Allowed physical `Y_E/Y_R` |
|---|---:|---:|---:|
| `H0` | 0.546093 | 0.483671 | `[0.879864,0.891564]` |
| `H1` | 0.546093 | 0.453947 | `[0.825646,0.836921]` |

After the gain-ratio uncertainty, `H0` has observed echo/reference ratio at least `L=0.8754643`, while `H1` has ratio at most `U=0.8411058`. The gap is `G=L-U=0.0343585`. Set `θ=(L+U)/2=0.8582851`; for `N` trials **in each arm** classify by the sign of `T=p̂_E-θ p̂_R`. The reference survival is at least `R_min=0.5444526`, so under either world the true mean of `T` has the correct sign with magnitude at least `q_min R_min G/2`. Hoeffding yields

\[
P(\text{wrong sign}\mid H_j)
\leq \exp\!\left(
-\frac{N q_{\min}^2 R_{\min}^2 G^2}{2(1+\theta^2)}
\right).
\]

`N=52,861` per arm, `105,722` independently reset preparations total, makes the bound at most 0.05 **for each specified world**. At nominal gain `0.8` and exact dose `1`, seeded binomial draws had `T=+0.01219` under `H0` and `T=−0.01193` under `H1`, correctly classifying both. This count is an upper bound for the specified two-hypothesis decision, not a cost to identify all four physical parameters or a universal unknown-system guarantee. Assay clock time per preparation is `2.275` model time units; those units have no supplied physical conversion.

The **matched same-information incumbent** is a joint binomial profile likelihood that fits both arm counts under each hypothesis' drift/dose probability envelope. The replay implements this, with profile log-likelihood differences `+25.04` and `−23.71` on the same two seeded outcomes, again correctly choosing each world. In 300 seeded repetitions per world, the threshold and profile likelihood errors were respectively `44/43` for `H0` and `43/43` for `H1` at `N=3000`; `10/10` and `9/10` at `N=10000`; and `0/0` for both at `N=30000`. The likelihood envelope relaxes some physical correlations, so a fully constrained likelihood fit may improve further. The threshold's contribution is its explicit worst-case control-margin certificate, not empirical superiority.

The finite durations matter. If the same two aliases are probed in the vanishing-duration regime with `t1=0`, dark wait `W=h`, and ON time `t2=h`, exact Taylor expansion gives `Y_H0(h,h)-Y_H1(h,h)=h^3+O(h^4)` while each survival probability is `1-2h+O(h^2)`. The single-trial Bernoulli KL is therefore `h^5/4+O(h^6)`. Any fixed-power classifier restricted to these shrinking settings needs `N=Ω(h^-5)` resets. Extracting the mixed derivative at zero is an expensive acquisition choice; the finite `W=2,t=0.275` assay avoids that small-duration penalty. This statement is local to these two worlds and this shrinking-setting family, not a universal lower bound over finite pulse timings.

## Near-uniform-loss resource law (any finite hidden state count)

There is a sharp obstruction that explains the finite-count cost and applies well beyond two states. Let `A` be **any** closed finite-state Markov generator, `b` any probability initial condition, `u(t)>=0` any ON waveform, and every unknown state loss satisfy `d_i in [d−δ,d+δ]` with `0<δ<=d/6`. Let `U=∫u(t)dt`. Feynman–Kac gives

\[
S_{A,D,u}(T)=E_b\exp\!\left(-\int_0^T u(t)d_{X_t}\,dt\right),
\qquad
e^{-(d+\delta)U}\leq S_{A,D,u}(T)\leq e^{-(d-\delta)U}.
\]

Hence **any two worlds** satisfying this same loss band, even with different hidden generators and initial states, have terminal-survival Bernoulli laws obeying

\[
D_{\rm KL}(P\Vert Q)
\leq \frac{(e^{-(d-\delta)U}-e^{-(d+\delta)U})^2}
{e^{-(d+\delta)U}(1-e^{-(d-\delta)U})}
\leq16(\delta/d)^2,
\]

uniformly over **all nonnegative doses** `U` (interpret `U=0` by continuity). To check the constant, put `r=δ/d<=1/6` and `x=dU`. The middle fraction equals `e^{-(1-3r)x}(1-e^{-2rx})²/(1-e^{-(1-r)x})`. Bound its numerator by `4r²x²e^{-x/2}` and denominator below by `(1-e^{-5/6})min(x,1)`; splitting at `x=1` and maximizing `x²e^{-x/2}` at `x=4` gives `<16r²`.

For an adaptive sequence of `N` **independently reset terminal-survival Bernoulli assays**, the chain rule still bounds transcript KL by `16N(δ/d)²`, since each chosen waveform obeys the same bound conditional on the previous results. Pinsker gives total variation at most `sqrt(8N)δ/d`. To classify two worlds with at least `2/3` success in each, total variation must be at least `1/3`, so

\[
\boxed{N\geq \frac1{72}(d/\delta)^2}.
\]

The constant is loose; the **quadratic scaling** is the consequential point. Increasing dose to order `1/δ` makes the loss exponent difference order one but drives survival below `e^{-(d-δ)/δ}`, a rare-event cost. The bound excludes kill-time trajectories, state-resolved measurements, controls that themselves alter `A`, and nonreset correlated samples. It also requires an independently known upper band `δ` to predict the difficulty; terminal survival alone does not grant that band.

The scaling is attained, up to model-class constants, by the finite-time echo target. For `D=diag(d,d+δ)`, `b=e1`, `u=1`, `t1=0`, and `t2=W=1/d`, write `α=a/(a+r)` and `γ=(a+r)/d`. Uniformly for `α>=α0>0` and `γ` in a compact subinterval of `(0,∞)`, the exact formula above yields

\[
C(W)=-\alpha e^{-1}\frac{(1-e^{-\gamma})^2}{\gamma}
\frac{\delta}{d}+O((\delta/d)^2),
\qquad R=1+e^{-\gamma}.
\]

Thus `N=O((d/δ)^2 ε^{-2} log(1/β))` suffices for a fixed accuracy `ε` in `γ` at failure probability `β`, provided the common detector gain has a positive lower bound. The near-uniform lower bound and this target-specific upper bound match in **sample exponent**, though constants may be poor and no throughput advantage over likelihood follows. If `γ` tends to zero, the wait must grow on the order of `1/g`; the fixed-clock constant deteriorates. A detector gain tending to zero or contrast vanishing also defeats a uniform finite budget. This is the precise supply/acquisition boundary.

## Closest predecessors and novelty assessment

- [Sontag, Wang, and Megretski, *Input Classes for Identifiability of Bilinear Systems* (2009)](https://www.sontaglab.org/FTPDIR/sontag_wang_megretski_inputs_tac_54_195_207.pdf) already establishes foundational input-class results for generic bilinear systems; multiple pulse widths are sufficient in their setting while simpler classes are not. We do not claim generic pulse identifiability.
- [Sattar, Jedra, Fazel, and Dean, *Finite Sample Identification of Partially Observed Bilinear Dynamical Systems* (2025)](https://proceedings.mlr.press/v283/sattar25a.html) gives finite-sample identification theory for partially observed bilinear dynamics. Our Bernoulli terminal-survival and uncalibrated one-channel loss constraints differ, but broad finite-sample bilinear-ID novelty is unavailable.
- [Hua and Sarkar, *Matrix Pencil Method for Estimating Parameters of Exponentially Damped/Undamped Sinusoids in Noise* (1990)](https://escholarship.org/uc/item/2n45r2z5) already covers exponential-rate extraction as a mature signal-processing idea. The `0,W,2W` quotient is a one-mode exponential fit, not a new general spectral algorithm.
- [Harville et al., *Cryogenic Ion Kinetics and Thermodynamics in a Temperature Controlled, Radiofrequency Ion Trap* (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12525174/) already extract two-isomer exchange kinetics using selective bleaching and a stronger isomer-specific probe. It is a serious *physical* incumbent, and our aggregate-survival-only design has no demonstrated advantage over it. [Offenberg et al. (2008/2009)](https://arxiv.org/abs/0810.5097) separately demonstrate continuous parent-ion photodestruction, but not the combined unchanged-`A` loss-echo interface.
- [Red-fluorescent-protein pulsed photodegradation/recovery experiment (2011)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3175071/) and [optically modulated fluorescence dark-state recovery (2015)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4724789/) show dark waits and pulsed recovery are established experimental motifs. Their observables and microscopic dynamics do **not** validate this killed-CTMC total-survival interface.

The defensible contribution is the **specific conservation-padded, calibration-cancelled terminal-survival quotient coupled to an explicit drift-robust count budget and a matching near-uniform-loss resource exponent**. It is mathematically exact and useful as a test design; originality beyond the combination is unproved and likely limited by classical pump-probe and exponential-fitting prior art. It does not achieve a new foundational operation under the campaign's highest novelty gate. Further pursuit should require a real apparatus with measured OFF leakage/dose/readout drift, and a same-information likelihood comparison on its data.

## Replay and artifact boundaries

Run `python3 dark_echo.py` in this directory. The script writes [FOLLOWUP_RESULTS.json](FOLLOWUP_RESULTS.json) and verifies 100 random exact quotient identities (maximum numerical discrepancy below `1e-12`), the exact one-pulse alias equality on a finite time grid, the endpoint drift margins, seeded Bernoulli counts, the profile-likelihood incumbent, and the finite-count confidence intervals. This is an executable **synthetic discriminator** and algebra check, not a wet-lab experiment or independent novelty review.
