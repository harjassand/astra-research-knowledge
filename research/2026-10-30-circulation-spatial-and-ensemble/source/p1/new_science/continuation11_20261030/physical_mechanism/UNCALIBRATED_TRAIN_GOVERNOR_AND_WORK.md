# Ordinary delayed governor at an actual extensive carrier port

30 October 2026. Constructive comparison requested after root selected the
stronger task of retaining native bulk histories. This note supplies the
ordinary controller and its true work bill. Root owns the material train and
the proof that its relative density stays a fixed uniform offset. Those
supplier conclusions are not assumed to follow from the current equation
alone.

The governing mechanism is established accumulated-error feedback. Brandes,
*Feedback control of quantum transport*, Phys. Rev. Lett. **105**, 060602
(2010), [primary paper](https://arxiv.org/pdf/1005.0018), and Wagner et al.,
*Strong suppression of shot noise in a feedback-controlled single-electron transistor*, Nature Nanotechnology **12**,
218–222 (2017), [primary paper](https://arxiv.org/pdf/1602.05466), were read in
round 10. They directly precede current-error regulation. The contribution
here is an explicit same-port work and delay comparison, not a new controller.

## 1. Exact port and actual task

Suppose an isolated physical carrier train has actual total displacement $A$
and the center-of-mass force port

\[
 dA_t=N\mu f_tdt+\sqrt{2N\mu}\,dW_t,\qquad
 \mu\in[\mu_-,\mu_+],\quad \mu_->0.                       \tag{1}
\]

The fixed device mobility is unknown. The control never estimates it. The
actual force $f_t$ acts on every one of the $N$ charges, so its mechanical
source work is

\[
 W_f=\int f_t\,dA_t.                                     \tag{2}
\]

Internal reciprocal pair forces may cancel from (1), but their energy,
preparation and relative motion remain in the actual supplier. A train with
different drag coefficients or missing bath/force reciprocity does not inherit
(1) merely from having many particles.

Let the desired actual auxiliary displacement $Z$, supplied by the native
history/evaluator, satisfy

\[
 dZ_t=b_tdt+dM_t^Z,\qquad |b_t|\le b_*,\qquad
 d\langle M^Z\rangle_t\le C Ndt,                         \tag{3}
\]

with jumps bounded by a constant. The native branch is autonomous and the
train bath is fresh and independent of its future innovations. Thus the error
$E=A-Z$ has a martingale noise with bracket bounded by (C'Ndt). The drift
$b_t$ may be nonlinear and history dependent; no generator fitting is used.

Constant-force fields are actual per-step forces. A fixed total loop EMF does
not silently become the uniformly applied $f_t$ in (1).

## 2. One-block-old integral feedback without mobility calibration

Use physical blocks of length $\Delta_N$, with

\[
 1\ll K_N\ll N,
 \qquad K_N\Delta_N/N^2\to0.                             \tag{4}
\]

For the conservative communication delay $\Delta_N=O(N\log N)$, it is enough
that $K_N\log N/N\to0$. Set the initial counting origins to $A_0=Z_0=0$,
$E_{-1}=E_0=0$. This chooses a displacement origin and does not reset a hidden
physical state. During block $m$, hold

\[
 f_m=-\operatorname{clip}\left({K_N\over N^3}E_{m-1},
                              -{K_N\over N},{K_N\over N}\right),
 \qquad E_m=E(m\Delta_N).                                \tag{5}
\]

The command uses a complete old epoch, allowing a genuinely finite collection,
computation and broadcast delay. It is not an instantaneous global sensor.
The true (unknown) gain is $g=\mu K_N/N^2$.

Before clipping, with $h=g\Delta_N$, the exact sampled recursion is

\[
 E_{m+1}=E_m-hE_{m-1}-\int_{m\Delta_N}^{(m+1)\Delta_N}b_sds+\xi_m,
 \quad E[\xi_m\mid\mathcal F_{m\Delta_N}]=0,
 \quad E[\xi_m^2\mid\mathcal F_{m\Delta_N}]\le C N\Delta_N.
                                                               \tag{6}
\]

For $h<1/8$, put $r_\pm=(1\pm\sqrt{1-4h})/2$. The impulse response

\[
 G_j={r_+^{j+1}-r_-^{j+1}\over r_+-r_-}
\]

is positive and satisfies, uniformly over the mobility interval,

\[
 \sup_jG_j\le C,\qquad \sum_jG_j=1/h,\qquad
 \sum_jG_j^2\le C/h.                                    \tag{7}
\]

The drift convolution is bounded pointwise by $b_*\Delta_N/h$; the martingale
convolution has variance at most $CN\Delta_N/h$. Hence the linear surrogate
satisfies

\[
 \sup_mE E_m^2\le C\left({b_*^2N^4\over K_N^2}
                           +{N^3\over K_N}\right).       \tag{8}
\]

This conclusion does not require $b_t$ to be deterministic: its convolution
has a deterministic absolute bound. In particular a mean load of order one
requires an error $O(N^2/K_N)$, while the fluctuation width is
$O(N^{3/2}/\sqrt{K_N})$.

## 3. Clipping and whole-time macroscopic tracking

Apply the bounded-jump martingale exponential inequality to the deterministic
weighted innovations in (6). Their predictable variance is $O(N^3/K_N)$,
and their jumps remain bounded by a constant because $\sup G_j\le C$.
For every fixed $\varepsilon>0$, the sampled error therefore obeys

\[
 \Pr\left[\max_{m\Delta_N\le N^2T}|E_m|>\varepsilon N^2\right]
 \le \operatorname{poly}(N)\exp[-c_\varepsilon K_NN]       \tag{9}
\]

for sufficiently large $N$. The bounded drift is smaller than the threshold
because $K_N\to\infty$. The same estimate at the clipping threshold
$N^2$ bounds the first disagreement between the executed controller and its
linear surrogate. A stopped comparison is necessary here; after clipping the
linear convolution is not asserted to represent the actual process.

Within each block the force drift is at most $\mu_+K_N\Delta_N=o(N^2)$, and
the noise bracket is $O(N\Delta_N)$. Another maximal martingale bound gives
superexponentially small order-$N^2$ deviations over a block. A union over
the polynomial number of blocks yields

\[
 \limsup_{N\to\infty}N^{-1}\log
 \Pr\left[\sup_{t\le N^2T}|A_t-Z_t|>\varepsilon N^2\right]=-\infty.
                                                               \tag{10}
\]

The martingale exponential premise for (9) is its actual bounded jump/rate or
bounded continuous-bracket interface. A quadratic-variation expectation alone
would not justify this tail estimate. Equation (3) specifies a predictable
bracket bound, not just its mean.

## 4. Actual work: order $N$ load plus order $K_N$ noise

For piecewise constant, predictable held commands, the physical work (2) has
the exact expectation

\[
 EW_f=N\mu E\int_0^{N^2T}f_t^2dt.                        \tag{11}
\]

The stochastic integral has zero mean. A torque switch at a fixed position
does not perform displacement work. Electronics/field-source switching costs
are not thereby zero; they are outside the mechanical work identity.

On the event before clipping, substitute (8) and (5). The resulting bound is

\[
 EW_f\le C_T(b_*^2N+K_N)+o(1).                           \tag{12}
\]

On the clipping event the total work compensator is at most $C K_N^2N$;
multiplying by the probability from the stopped comparison makes its
contribution negligible. Thus (12) is a bound for the actual clipped execution,
not only the unbounded linear surrogate. When $b_*=0$, the mean fluctuation
work is $O(K_N)=o(N)$.

For any other predictable controller with this same force/noise port,

\[
 EW_f\ge {\big(E[A_{N^2T}-A_0]\big)^2\over N\mu N^2T}.    \tag{13}
\]

This is Cauchy–Schwarz using $EA=N\mu E\int fdt$. A sustained mean current
$EA=vN^2T+o(N^2)$, $v\ne0$, therefore needs at least
$v^2NT/\mu+o(N)$ operating work. A known constant drive attains the bound if
$\mu$ and $v$ are supplied; the uncalibrated governor attains its order while
also regulating the realized native-history target. This is the ordinary
work-efficient comparator at the extensive carrier port.

### A literal opposing load

If a separate actual load torque is $\ell=-L/N$, $L>0$, replace (1) by

\[
 dA=N\mu(f+\ell)dt+\sqrt{2N\mu}\,dW.
\]

Its bounded order-one drift can be absorbed into (3). Let $u=f+\ell$. The
drive source and load then obey the exact mean ledger

\[
 EW_{\rm drive}=N\mu E\int u^2dt-\ell EA,
 \qquad EW_{\rm out}=-\ell EA.                           \tag{14}
\]

The difference is the nonnegative viscous contribution. Both useful output
and source input are order $N$ for an order-one sustained current on $N^2$
time. Thus this port is capable of actual load delivery as well as compensating
a counted native displacement. It does not produce load work for free from
the bath.

## 5. Precision, old records and what is not supplied here

If an actual synchronized old-epoch observation has error at most $\eta_N$,
the added convolution is bounded by $h\eta_N\sum G_j=\eta_N$. Its extra
mechanical work bound is

\[
 C K_N^2\eta_N^2/N^3.                                    \tag{15}
\]

For the load budget $O(N)$, it suffices that
$\eta_N=O(N^2/K_N)$. For the finer noise budget $O(K_N)$, it suffices that
$\eta_N=O(N^{3/2}/\sqrt{K_N})$. Tracking at speed $N$ additionally requires
the actual whole-horizon readout-failure probability to be superexponentially
small on that scale. A fixed calibration confidence does not provide it.

One cannot replace a common timestamp by arbitrary asynchronous latest counts.
Every force is chosen from the complete retained past record; future bath
increments are not available to the controller. The delayed-force work proof
holds with the entire sensor/controller log retained. It does not condition
on a rare future bath realization or erase the information and power bill of
acquiring (A-Z).

The exact aggregate force port, paid local synchronized sensing, evaluator,
communication, repeated native-event processing, train preparation and the
uniform-offset density theorem are separate actual resources. This note does
not infer any of them from the existence of a formal center-of-mass variable.
Its role in selection is to show that once that material port is genuinely
supplied, ordinary uncalibrated delayed feedback already obtains the desired
order of operating work and a full macroscopic tracking guarantee.
