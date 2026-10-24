# One-cavity matched transfer: time and intrinsic-loss bounds

## Model and selected-mode meaning

A single passive Markov cavity couples to one designated traveling port at a controllable external rate \(\kappa_e(t)\), with \(0\leq\kappa_e(t)\leq\kappa_{\max}\). Capture and release occur in separate, nonoverlapping intervals. The capture input envelope and release output envelope are each normalized in temporal-mode \(L^2\). We optimize the mode overlap (equivalently, the one-particle energy-transfer probability) for this cavity and port. This quantity \(\eta\) is not a state fidelity: fidelity also depends on the encoded input, thermal/noise channels, and the rest of the output modes. The bounds below assume no additional coherent path, active recovery, or repeated transfer attempt.

## No intrinsic loss: exact rate-area law

For capture on \([0,T_H]\), the cavity amplitude at the end is
\[
a(T_H)=\int_0^{T_H}\sqrt{\kappa_e(t)}
\exp\!\left[-\tfrac12\int_t^{T_H}\kappa_e(s)\,ds\right]f(t)\,dt .
\]
For unit-norm \(f\), Cauchy–Schwarz is tight for the matched envelope proportional to the displayed kernel. The maximum capture probability is therefore
\[
\eta_H=\int_0^{T_H}\kappa_e(t)
  e^{-\int_t^{T_H}\kappa_e(s)ds}\,dt
=1-e^{-K_H},\qquad K_H=\int_0^{T_H}\kappa_e(t)dt.
\]
The last equality follows by differentiating \(e^{-\int_t^{T_H}\kappa_e}\) with respect to \(t\). Release from a unit cavity amplitude has optimally captured output-mode probability
\[
\eta_C=\int_0^{T_C}\kappa_e(t)e^{-\int_0^t\kappa_e(s)ds}dt
=1-e^{-K_C}.
\]
With no loss between the two legs, their selected-mode probabilities multiply:
\[
\eta=(1-e^{-K_H})(1-e^{-K_C}).
\]

For fixed \(K_H+K_C=K\), the function \(x\mapsto\log(1-e^{-x})\) is strictly concave, so
\[
(1-e^{-K_H})(1-e^{-K_C})
\leq (1-e^{-K/2})^2,
\]
with equality exactly at \(K_H=K_C=K/2\). Since \(K_H+K_C\leq\kappa_{\max}(T_H+T_C)\), any target \(\eta\geq\eta_0\) requires
\[
T_H+T_C\geq
\frac{-2\log(1-\sqrt{\eta_0})}{\kappa_{\max}}.
\]
Equality is attained by equal rate areas and \(\kappa_e=\kappa_{\max}\) throughout each leg. Thus finite rise/fall ramps or any submaximal-rate portions can only increase the required open time. For example, \(\eta_0=0.9\) requires at least \(5.94/\kappa_{\max}\) total open time (approximately).

## Constant intrinsic loss

Now include an unobserved intrinsic decay rate \(\kappa_i>0\) during each leg. The optimized capture probability is
\[
\eta_H=\int_0^{T_H}\kappa_e(t)
 e^{-\int_t^{T_H}(\kappa_e(s)+\kappa_i)ds}dt.
\]
Put \(A(t)=e^{-\int_t^{T_H}(\kappa_e+\kappa_i)}\), so
\(dA=(\kappa_e+\kappa_i)A\,dt\). Then
\[
\eta_H=\int_0^{T_H}\frac{\kappa_e}{\kappa_e+\kappa_i}\,dA
\leq \frac{\kappa_{\max}}{\kappa_{\max}+\kappa_i}
        [A(T_H)-A(0)]
\leq \frac{\kappa_{\max}}{\kappa_{\max}+\kappa_i}.
\]
Similarly, for release set \(B(t)=e^{-\int_0^t(\kappa_e+\kappa_i)}\). Since \(-dB=(\kappa_e+\kappa_i)Bdt\),
\[
\eta_C=\int_0^{T_C}\frac{\kappa_e}{\kappa_e+\kappa_i}(-dB)
\leq\frac{\kappa_{\max}}{\kappa_{\max}+\kappa_i}.
\]
Consequently the sequential selected-mode energy-transfer probability obeys
\[
\eta\leq
\left(\frac{\kappa_{\max}}{\kappa_{\max}+\kappa_i}\right)^2,
\]
regardless of pulse duration or envelope shaping. A storage gap \(\Delta\) with the same intrinsic decay contributes the further survival factor \(e^{-\kappa_i\Delta}\). The ceiling is a branching-loss bound: at every instant, at most the fraction \(\kappa_{\max}/(\kappa_{\max}+\kappa_i)\) of cavity decay can exit through the designated port.

## Scalar checks and scope

For constant external rate \(\kappa\) over duration \(T\), the no-loss leg integral is exactly \(1-e^{-\kappa T}\). With intrinsic loss it is
\[
\int_0^T\kappa e^{-(\kappa+\kappa_i)u}du
=\frac{\kappa}{\kappa+\kappa_i}
 (1-e^{-(\kappa+\kappa_i)T}),
\]
which approaches the claimed branching ceiling as \(T\to\infty\). These formulas refer to the norm of the map from one normalized input temporal mode to the memory, or from the memory to one normalized output temporal mode. They do not establish preservation of arbitrary states against thermal noise, nor a universal quantum-state fidelity.
