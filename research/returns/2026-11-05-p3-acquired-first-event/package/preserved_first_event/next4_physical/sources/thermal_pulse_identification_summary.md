# A finite common thermal pulse identifies an observable hidden linear diffusion

This independent [complete construction](package/companions/thermal_pulse/heat_pulse_identification.txt) adds a **different physical port** to the earlier [force-only nonidentifiability model](../2026-11-05-p2-tracial-acquisition/active-port-nonidentifiability.md). In a certified finite-dimensional observable all-even OU class, a calibrated common diffusion-scaling pulse permits drift/diffusion identification up to similarity and native stationary entropy inference. It does not contradict the unchanged force-only indistinguishability result or extract hidden work.

## Model, physical reach and finite pulse

The native system is `dX=A X dt+sqrt(2D)dW`, scalar output `Y=CX`, Hurwitz A, positive D and known finite order n, with all coordinates even under time reversal. The added actuator implements `D -> (1+u(t))D` while leaving drift, mobility and sensor coupling fixed to paid tolerance. It must reach **all** native noise contributions in the declared model. Global thermal reach, bath equilibration/memory, controller energy and a complete model order are substantial premises, not consequences of one sensor or one scalar knob. Unheated active noise, invisible modes or temperature-dependent drift change the claim.

Use `u(t)=eta sin^2(pi t/h)` over a finite duration h, returning to baseline with zero endpoint slope. Peak is eta and slew is `eta pi/h`. For `L_A(Z)=AZ+ZA^T`, `omega=2pi/h`, hot-minus-control end covariance is

```text
S=T_A(D)=2eta integral_0^h sin^2(pi s/h) exp(As)D exp(A^T s)ds,
T_A=eta omega^2[exp(h L_A)-I][L_A(L_A^2+omega^2 I)]^-1.
```

This map is invertible on symmetric matrices for every Hurwitz A, including defective/nonnormal cases; the chosen raised-cosine Laplace transfer has no zero at its spectrum. No arbitrary-pulse version is asserted. At bounded slew, a short pulse has signal of order h squared; a very long pulse can lose its covariance signal before readout. Conditioning and timing remain actual costs.

## Scalar readings and unknown-drift reconstruction

A finite post-pulse observation stack has hot/control raw second-moment difference `V=O S O^T`, where rows of O are `C exp(At_j)`. Future native process noise cancels in expectation. Fixed finite detector bins replace C by `C_b=C(exp(Ab)-I)/(bA)` and preserve observability in the stated stable model. Assignment-invariant independent electronics can cancel in mean while increasing variance; equal noise marginals do not suffice if heat-dependent cross-correlations change.

Known A,C give `S=O^dagger V(O^dagger)^T`, with diffusion error amplified by `1/[s_min(T_A)s_min(O)^2]`. With unknown A and sensor gain, use n+1 equally spaced readings and a supplied anti-alias bound `|Im lambda(A)|<pi/Delta`. Consecutive covariance blocks H0,H1 give `F'=H1 H0^-1`, `A'=Log(F')/Delta`, `S'=H0`, then invert `T_A'` and solve the stationary Lyapunov equation. This identifies A,D,Sigma up to similarity; native entropy production

```text
Q=A Sigma+D,
sigma=Tr[Q^T D^-1 Q Sigma^-1]
```

is similarity-invariant. Scalar sensor gain is absorbed in that representation. Invertibility, observability, matrix-log/Stein/Lyapunov conditioning and certified finite precision are paid. A finite-dimensional complete model and native frequency bound cannot be inferred by overlooking weak extra modes or aliases.

## One operating specimen, statistics and full bill

Fresh randomized hot/control assignment each cycle isolates the contrast from an arbitrary correlated current state. Martingale moment estimation works along one continuously operating specimen without hidden reset, independent trajectories or relaxation between cycles. A certified fourth-moment bound, or separately prepared native stationarity, controls finite-sample exposure. Statistical independence of trajectories is not manufactured from one correlated record.

M cycles cost `M[h+n Delta+b+latency]` physical time, M assignment bits, `M(n+1)` readings, `O((n+1)^2)` accumulators and `O(M(n+1)^2)` arithmetic. Ordinary offline reconstruction uses `O(n^3)` arithmetic and `O(n^2)` storage at fixed precision; optional dense condition certification can be much larger. Detector ADC range/bits, clipping probability, finite response, timestamps, waveform/drift/diffusion bias and heat-tagged pickup all have explicit budgets. More samples do not remove a calibration floor. An expectation-only bias bound needs a confidence conversion or a stronger conditional/pathwise contract.

Heating a bath with heat capacity C_bath changes stored energy by approximately `C_bath T0 eta` at each hot pulse, before leaks, source work and controller losses; expected hot pulses are M/2. Native sigma is the modeled device's unperturbed dissipation, not the thermostat/controller's total losses. No uniform cheap global thermostat is supplied, and no efficiency advantage over equally informed covariance/noise-identification or stochastic-realization methods is proved.

The [original simulator](package/companions/thermal_pulse/heat_pulse_demo.py) and [recorded execution](package/companions/thermal_pulse/heat_pulse_execution.json) use one million simulated cycles. True native entropy is 20.25, empirical reconstruction about 21.07724758 and tagged-moment error `.01014736`; the conservative 95% moment radius `.13477982` is **not** a certificate of that displayed point accuracy. A separate calculated known-A/C budget of 208,600,580 cycles for diffusion error 0.1 was not executed. Full unknown-A confidence pays further conditioning. This is simulation/algebra, not physical thermal hardware or a new Capital rerun. [Original package, sources and status](SOURCES.json).
