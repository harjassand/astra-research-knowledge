# Independent audit: finite heterodyne startup admission

## Decision

The proposed startup is mathematically sound in its stated passive, linear, homogeneous thermal model. A real finite heterodyne acceptance disk can turn a mere initial mean bound into an exponential-moment bound on the accepted reference state. The acceptance effect supplies the tail; passive cooling alone does not.

The operator inequality holds for arbitrary initial oscillator–reference correlations and even for inputs with no exponential moment. The finite mean assumption is needed separately to lower-bound availability and to bound a once-only comparison with unwanted startup forces. For many initially correlated buses, the correct normalization uses a global success lower bound from unconditional marginals and a union bound. Multiplying conditional per-bus success probabilities would be unjustified.

I found one small missing step in the first root writeup: the final decision interval needs an exponential-moment propagation bound, rather than a statement about its mean. With the readout port closed, the proposed `.05/g` interval adds less than `6.741e-7` to the log-moment bound. Root has now incorporated this term. The startup perturbation estimate is a **half trace-distance** bound; full trace norm has the extra factor two. The tighter damped-mean comparison added subsequently is also sound; Section 9 audits it.

This audit concerns the construction in `phase8/root/FINITE_STARTUP_ADMISSION.txt`, its numerical implementation in `finite_heterodyne_admission.py`, and the parent’s correlated-array extension. No root file was changed during this audit.

## 1. Physical model and actual finite acceptance

Let `a` be the old oscillator and let `c` be an independent thermal mode of occupation `n_b`. A passive window with surviving intensity `r` has a dilation

\[
a_{\rm ret}=\sqrt r\,a+\sqrt{1-r}\,c,
\qquad
b=-\sqrt{1-r}\,a+\sqrt r\,c.
\]

The collective complementary output `b` includes all loss ports. A normalized measured temporal output mode has the form

\[
s=\sqrt\mu\,b+\sqrt{1-\mu}\,h,
\]

after absorbing an irrelevant phase into the mode definition. Here `h` is an independent thermal mode of the same occupation. This independence follows because all fresh input modes are a product of identical thermal states and hence remain a product in any passive mode basis. The fresh modes orthogonal to the old/retained two-mode subspace are independent of both `a` and `c`.

This is the place where **homogeneous thermal input is used**. Merely bounding each port’s occupation by `n_b`, while permitting unequal temperatures or fresh-mode correlations, does not justify this particular independent-mismatch reduction. A different covariance calculation would be needed in that broader model.

Detector efficiency is represented by a vacuum loss channel of transmissivity `eta_d` before ideal heterodyne. Extra receiver noise is covered only to the extent that the declared detector model or an explicit additional error term covers it.

The hardware accepts a finite ADC disk. For round-to-nearest quadrature step `h_ADC`, the radius uncertainty is `sqrt(2) h_ADC/2`. With the proposed two 16-bit ADCs on `[-16,16]`,

\[
h_{\rm ADC}=1/2048,
\quad
\delta_R=\sqrt2/4096,
\quad
R_\pm=4\pm\delta_R.
\]

Every uncorrupted accepted ADC record lies in the ideal outer disk, and every ideal outcome in the inner disk is accepted. Saturation is an abort, and the acceptance radius is far inside the saturation boundary. Therefore the corresponding effects obey

\[
E_{R_-}\le E_{\rm ADC}\le E_{R_+}.
\]

The actual quantized acceptance set is not exactly rotation invariant. This causes no problem: use the outer ideal disk for the high-moment majorant and the inner ideal disk for availability. There is no need to assert that the ADC instrument itself is phase covariant.

Hardware faults that corrupt the integrator, ADC, saturation handling, register, or comparison are separate physical faults. The operator inclusion describes the uncorrupted declared receiver; it is not an oracle fault flag.

## 2. The heterodyne disk inequality is an operator statement

The ideal heterodyne disk effect is

\[
E_R=\int_{|\beta|\le R}|\beta\rangle\langle\beta|\,\frac{d^2\beta}{\pi}.
\]

For any `c_0>0`,

\[
\mathbf1_{|\beta|\le R}
\le e^{c_0R^2}e^{-c_0|\beta|^2}.
\]

Integrating the coherent-state POVM in the Fock basis gives

\[
E_R\le
\frac{e^{c_0R^2}}{1+c_0}
\left(\frac1{1+c_0}\right)^n.
\tag{1}
\]

This is a positive-operator inequality, not a bound on coherent states alone. Consequently it remains true when tensored with any reference, including a reference entangled with the old oscillator.

Normal ordering gives `q^n = :exp[-(1-q)n]:`. Pulling (1) through detector inefficiency replaces the no-click strength by

\[
\eta_0=\eta_d\frac{c_0}{1+c_0}.
\]

Tracing the independent thermal mismatch mode `h` yields

\[
\operatorname{Tr}_h\left[
\sigma_{n_b}(h)
:e^{-\eta_0s^\dagger s}:
\right]
=A:e^{-\eta b^\dagger b}:,
\]

where

\[
A=\frac1{1+\eta_0(1-\mu)n_b},
\qquad
\eta=\frac{\eta_0\mu}{1+\eta_0(1-\mu)n_b}.
\tag{2}
\]

The word “no-click” names an algebraic normal-ordered majorant. The physical instrument remains the heterodyne disk, with no photon counter or replacement measurement introduced.

## 3. Exact tilted accepted-map calculation

Set

\[
t=e^\theta-1,
\quad
u=rt-\eta(1-r),
\quad
v=\sqrt{r(1-r)}(t+\eta),
\quad
w=(1-r)t-\eta r.
\]

The retained moment and the output acceptance effect commute because they act on different output modes. Thus the positive majorant is valid after multiplication by the retained moment. The joint normal-ordered exponent in the input modes is

\[
:\exp\{u a^\dagger a+v(a^\dagger c+c^\dagger a)+w c^\dagger c\}:.
\]

The thermal `P`-representation Gaussian integral over `c` gives

\[
\frac1{1-n_bw}
:\exp\left[\left(u+\frac{n_bv^2}{1-n_bw}\right)a^\dagger a\right]:,
\]

provided `1-n_b w>0`. The determinant identity

\[
uw-v^2=-t\eta
\]

then gives the proposed formula:

\[
\mathcal A_{\rm acc}^{*}(e^{\theta n_{\rm ret}})
\le
K\left[1+\frac{u+n_bt\eta}{1-n_bw}\right]^{n_{\rm old}},
\tag{3}
\]

\[
K=\frac{e^{c_0R_+^2}}{1+c_0}\frac{A}{1-n_bw}.
\tag{4}
\]

The signs of `u,w` and the positive cross term in `v` are correct for the beamsplitter convention above. The square root in `v` covers the complete product `r(1-r)`.

Under

\[
n_bt<1,
\qquad
t(r+n_b\eta)\le\eta(1-r),
\tag{5}
\]

the base in (3) lies between zero and one. The denominator is positive because `w<=t`. Nonnegativity follows also directly from `u+n_bv^2/(1-n_bw)>=u>=-eta(1-r)>=-1`. Therefore

\[
\boxed{\mathcal A_{\rm acc}^{*}(e^{\theta n_{\rm ret}})\le K I.}
\tag{6}
\]

Equation (6) is the decisive admission result. For any normalized old oscillator–reference state, even with an infinite initial exponential moment,

\[
\operatorname{Tr}[(e^{\theta n_{\rm ret}}\otimes I_R)
(\mathcal A_{\rm acc}\otimes\operatorname{id}_R)(\rho_{aR})]
\le K.
\]

These unbounded-observable inequalities can be interpreted first as quadratic-form inequalities on finite-energy vectors and then extended by positivity/monotone convergence. No physical number cutoff is used.

After coarse-grained acceptance with probability `p_acc>0`, the normalized bound is `K/p_acc`. This is a bound on the accepted ensemble, including arbitrary correlations with the reference. It is not a uniform bound on every normalized rare raw heterodyne branch.

## 4. Uniform parameter margin and finite filter

For the proposed `theta=.8`, `c_0=1`, `n_b<=.1`, and `eta_d>=.5`, the fixed constant temporal filter has a conservative lower bound

\[
\mu_{\min}=0.49866298647\ldots.
\]

The derivation uses only the central plateau of the output impulse response. All omitted ramp contributions have nonnegative projection on a fixed phase direction because the phase excursion is at most `Delta_max T`. The plateau integrand is bounded using the largest total damping in the exponential and the smallest read-port coupling in the numerator. No filter adapted to an unknown pole is required.

The actual overlap is the squared old-output coefficient divided by `1-r`; discarding that denominator is conservative since `1-r<=1`.

Ignoring intrinsic damping gives the looser but independently verified bound

\[
r\le e^{-3.996\times.7}=0.06098056940\ldots.
\]

Including intrinsic damping, as in root’s calculation, improves this to `0.06097617896`. From (2), the uniform effective strength is

\[
\eta\ge0.12312259872\ldots.
\]

The contraction threshold in (5) can be written

\[
r\le\frac{\eta(1-n_bt)}{t+\eta}.
\]

Its conservative value is `0.08010405720`, appreciably above the retained-intensity bound. With the looser `r` above, the old-number base in (3) is `0.97087950749`.

Do not assume that the largest `r`, which is adverse for contraction, also maximizes the prefactor. A simple fully uniform bound avoids this issue:

\[
K\le\frac{e^{c_0R_+^2}}{(1+c_0)(1-n_bt)},
\]

so

\[
\log K\le15.44035504433\ldots.
\tag{7}
\]

For a single module with efficiency fixed at `.5`, the earlier Markov availability estimate near `.89` is valid. For the broader declared efficiency interval `[.5,1]`, the availability bound must use efficiency one. Root’s corrected single-module mean envelope `1.37130330390` gives second moment `2.47130330390` and availability at least `0.84551687570`; consequently `log M_.8<=15.60816219575` at the end of the measurement window. These are model bounds, not measured performance figures.

## 5. Correlated arrays: global normalization without independence

Let each bus have a local accepted map `A_i`, and assume the startup couplings and fresh fields are local across buses. Initial bus states may be arbitrarily entangled with one another and with a reference. Shared unknown classical parameters are also allowed when all inequalities hold uniformly in those parameters.

For a particular retained bus `i`,

\[
\mathcal A_{\rm all}^{*}(e^{\theta n_i}\otimes I_{\ne i})
=\mathcal A_i^*(e^{\theta n_i})
\otimes_{j\ne i}\mathcal A_j^*(I)
\le K I,
\tag{8}
\]

because all other acceptance effects are at most the identity. This proves the unnormalized per-bus moment bound for the all-accepted branch without any factorization assumption on the initial state.

Availability needs a separate global bound. After precooling with surviving intensity `r_0`, the complete channel from one original oscillator to its selected detected mode is phase insensitive, with initial intensity coefficient `a_i<=r_0` and added thermal photon number `N_i<=n_b`. It admits the exact decomposition

\[
\text{pure loss with }\tau_i=a_i/G_i
\quad\text{followed by quantum-limited amplification with }G_i=1+N_i.
\tag{9}
\]

The output mean is `G_i tau_i n+(G_i-1)=a_i n+N_i`, and the Gaussian covariances also agree. This is a channel identity, used only to prove a bound; it is not a proposed implementation.

For Fock input `n`, no initial photons survive the pure-loss part with probability `(1-tau_i)^n`. Conditional on that component, the amplifier produces a thermal state of mean `G_i-1`. Its ideal heterodyne radius has tail `exp(-R_-^2/G_i)`. Bounding the remaining component by one gives

\[
\begin{aligned}
p_{i,\rm abort}(n)
&\le(1-\tau_i)^n e^{-R_-^2/G_i}
+[1-(1-\tau_i)^n]\\
&\le e^{-R_-^2/G_i}+n\tau_i\\
&\le e^{-R_-^2/(1+n_b)}+nr_0.
\end{aligned}
\tag{10}
\]

The radial ideal effect pulled through a phase-covariant channel is diagonal in the original Fock basis. Initial number coherences therefore do not affect this marginal probability. The actual ADC abort probability is bounded by the ideal inner-disk abort probability, so exact rotation invariance of the ADC acceptance set is unnecessary.

Averaging (10) and applying the ordinary union bound gives

\[
\boxed{
p_{\rm all}\ge1-m e^{-R_-^2/(1+n_b)}
-r_0\sum_i\langle n_i\rangle.
}
\tag{11}
\]

This uses unconditional marginal probabilities. Arbitrary initial cross-bus correlations cause no difficulty, and there is no multiplication of conditioned success rates.

With `m=217`, initial means at most `100`, and `3.3/g` precooling including the stated ramps, an independently conservative calculation that omits intrinsic cooling yields

| Quantity | Conservative bound |
|---|---:|
| `r_0` | `2.79633759150e-6` |
| Summed vacuum/thermal abort contribution | `0.000104843032` |
| Summed initial-energy abort contribution | `0.060680525736` |
| Global success probability | `>=0.939214631233` |
| Conditional per-bus log moment | `<=15.503066295958` |

Including intrinsic damping gives root’s slightly stronger success bound `0.939232650673` and log moment `15.503047110496`. Equation (8) is divided by this one global success probability. It is not divided by a product of per-bus lower bounds.

The argument also implies an unnormalized total exponential-moment bound `K^m`, but it does not imply that normalized accepted buses or their tail events are independent. A downstream proof needing simultaneous tail control must retain correlations and use a justified union or joint operator bound.

Parallel timing requires actual parallel receivers and integrators. A shared sequential detector must pay the resulting waiting and noise. The `1.2/g` standalone precooling example and the `3.3/g` array example are different protocols; their availability and calendars must not be combined.

## 6. Finite decision latency

For a subsequent force-free passive thermal interval with surviving intensity `r_f`,

\[
\mathcal E_{r_f}^*(e^{\theta n})
=\frac1{1-n_b(1-r_f)t}
\left[1+\frac{r_ft}{1-n_b(1-r_f)t}\right]^n.
\]

When `n_b t<1`, the number base is at most `e^theta`. Hence

\[
M_{\rm after}\le
\frac{M_{\rm before}}{1-n_b(1-r_f)t}.
\tag{12}
\]

For the `.05/g` decision slot with the readout port off and intrinsic rate at most `1.1e-4 g`, the additional log cost is at most

\[
-\log[1-.1(1-e^{-1.1\times10^{-4}\times.05})(e^{.8}-1)]
<6.741\times10^{-7}.
\]

This is sufficient to close the original small omission. Any actual continued read-port opening or additional waiting can be substituted into (12). Unwanted drive during the slot is included in the once-only physical comparison below.

## 7. Once-only startup comparison under continuing physical noise

Take the comparison startup to use the same actual passive coefficients, thermal fields, receiver and ADC, but zero unwanted force. This does not require knowing those coefficients operationally. They label a comparison experiment in the proof.

For a perturbation

\[
\Delta H(t)=a^\dagger F(t)+aF(t)^\dagger,
\qquad \|F(t)\|\le u(t),
\]

where the bounded controller operator commutes with the oscillator in the interaction definition, a purification-vector Duhamel bound gives

\[
\epsilon_{\rm start}\le
\sum_i\int u_i(t)
[\sqrt{E_i(t)}+\sqrt{E_i(t)+1}]\,dt.
\tag{13}
\]

Here `epsilon_start` bounds **half trace distance** for the complete startup output, with all reference systems and accept/abort records retained. A corresponding bound on full trace norm is twice (13). One may use a suitable reference-prefix mean envelope, or an independently established actual-prefix envelope. The declared `E_i(t)<=100` is loose but sufficient for the stated weak force and passive damping.

The startup comparison requires only first moments because the perturbation is linear in `a,a†`. Other unbounded perturbations need their own energy-constrained comparison argument; they are not automatically covered by (13).

Let `P` be the actual entire startup instrument, `Q` its comparison, and `F_future` the actual subsequent computation, including loading useful data only on acceptance. Then

\[
\tfrac12\|\mathsf F_{\rm future}\mathsf P(\rho)
-\mathsf F_{\rm future}\mathsf Q(\rho)\|_1
\le\epsilon_{\rm start}.
\tag{14}
\]

The future experiment starts from the reference’s accepted state for the moment proof. A small trace distance is **not** used to infer that the actual accepted state has a finite exponential moment; such an inference would be false in general.

If the final statement conditions on successful startup, the comparison must include normalization. With `p_ref>epsilon_start`, the root’s conservative conditional bound

\[
\frac{2\epsilon_{\rm start}}{p_{\rm ref}-\epsilon_{\rm start}}
\tag{15}
\]

is safe. Keeping abort as an explicit output instead gives the simpler whole-experiment bound (14).

For the intentionally loose whole-calendar mean envelope and `u=1e-7 g`, the preliminary 217-bus calculation had half trace-distance cost about `0.00180559`, and the corresponding conservative conditional comparison was about `0.00385223`. The improved damped-mean calculation in Section 9 reduces these to `0.00038686034` and `0.00082411903`. The resulting global startup error is paid once, not once per gate, but it must remain visible in a claimed end-to-end accuracy budget. Independence must not be invoked to turn it into a product of per-bus probabilities.

Detector, switch, and classical-control faults need their own actual map-distance or valid jump-intensity bounds, including shared fault support. The construction specifies one finite attempt before useful input. An eventual-success retry protocol would need its own elapsed-time and correlated-noise accounting.

## 8. Scientific scope

The startup is a useful constructive admission primitive: it closes the gap between a physically modest initial mean assumption and the exponential moment needed by the later unbounded-bus proof. It permits arbitrary initial oscillator/reference correlations in the accepted-map theorem and arbitrary initial cross-bus correlations in the array availability bound.

It does not provide unconditional availability for arbitrary unbounded initial energy, uniform quality of every normalized raw record, a measured detector specification, or an advantage over conventional mechanisms supplied with the same receiver and physical resources. The finite dirty-qubit and ordinary fault-tolerant comparators remain relevant. The justified gain is a concrete physical preparation and whole-history interface under a stated model.

## 9. Addendum: tighter damped-mean startup comparison

The amended `finite_heterodyne_admission.py` uses an elementary analytic mean envelope and is sound. Write `s=.14`, `E_0=100`, ramp duration `h=.1/g`, and

\[
k_{\rm flat}=3.99609g-10^{-5}g.
\]

Young’s inequality bounds the force term so that throughout the flat plateau

\[
\dot E\le-k_{\rm flat}(E-s).
\]

The value `s=.14` is also above the sufficient stationary mean for the intrinsic-only interval and every intermediate ramp value. The ratio giving that stationary mean is linear-fractional in the ramp amplitude, so checking both endpoints suffices. Consequently an envelope above `s` remains nonincreasing throughout the remaining passive calendar, despite the allowed residual force.

Ignore cooling during the first ramp and let `F=T_pre-2h` be the precooling plateau. On the plateau,

\[
E(t)\le s+(E_0-s)e^{-k_{\rm flat}t}.
\]

The pointwise bound

\[
\sqrt{E(t)}+\sqrt{E(t)+1}
\le\sqrt s+\sqrt{s+1}
+2\sqrt{E_0-s}\,e^{-k_{\rm flat}t/2}
\]

therefore yields the integral bound

\[
\begin{aligned}
I_{\rm start}\le{}&
h(\sqrt{E_0}+\sqrt{E_0+1})
+F(\sqrt s+\sqrt{s+1})\\
&+\frac{4\sqrt{E_0-s}}{k_{\rm flat}}
(1-e^{-k_{\rm flat}F/2})\\
&+(h+T_{\rm obs}+T_{\rm final})
(\sqrt{E_{\rm end}}+\sqrt{E_{\rm end}+1}),
\end{aligned}
\]

where `E_end=s+(E_0-s) exp(-k_flat F)`. The final term deliberately ignores further cooling while bounding the closing ramp, the entire observation, and decision latency. Their mean cannot rise above this envelope because it remains above `s`.

For `T_pre=3.3/g`, `T_obs=.8/g`, and `T_final=.05/g`, the code evaluates

\[
gI_{\rm start}\le17.82766538177.
\]

Thus the 217-bus once-only half trace-distance contribution is

\[
\epsilon_{\rm start}\le217\times10^{-7}\times17.82766538177
=0.000386860338785,
\]

and the conservative conditioned comparison is `0.000824119025227`. This tightening is a uniform mean-based Duhamel estimate, with no independence assumption or inference of an actual high moment from trace distance.

The amended finalization cost is `6.74045885e-7` in log moment. Including it gives the 217-bus accepted reference bound `log M_.8<=15.50304778455`. The finite decision-slot gap identified in Section 6 is therefore closed.
