# Kinetic-blind torque metrology: ordinary construction and predecessor correction

30 October 2026. Independently selected complementary round-10 task, preserved before redirecting to the composite-carrier current governor. No new metrology principle or practical advantage is claimed.

## Outcome

An actual finite-time, Gibbs-prepared torque experiment has a sign likelihood independent of its hidden reciprocal kinetics. The likelihood supports finite-sample and anytime inference. A finite-bandwidth encoder can acquire the full work displacement with a nonaccumulating endpoint error. The complete operation nevertheless pays for baseline preparation, signal isolation, thermal calibration, sensing and time.

The ordinary incumbent already supplies the core principle. Crooks gives the path-reversal machinery; Hayashi et al., PRL 104, 218103 (2010), explicitly use fluctuation statistics for torque measurement; Shirts et al., PRL 91, 140601 (2003), derive the fluctuation-relation logistic likelihood and discuss fitting its slope. This candidate therefore did not establish a new scientific principle. The useful preserved result is the physical and statistical scope, including a force/flow counterexample.

## 1. Actual experiment

Use calibrated thermal units k_B T=1. A mechanical rotor theta on the circle, velocity v and inertia tau is coupled to hidden equilibrium coordinates z and perhaps an arbitrary frozen class h. Its complete baseline energy is E_h and its warranted preparation is mu_h proportional to exp(-E_h). The class h need not reset or mix.

For trial i choose its duration T_i from the previous completed record, before inspecting the new initial state. Make the actual baseline preparation conditional on that old record and h. Apply the unknown constant torque F through its actual native force port, and record

\[
J_i=\int_0^{T_i}v_tdt.
\]

This is the full unwrapped displacement, including fractional turns and all reaction motion. The work is F J_i. No other active hidden source, temperature difference or unmeasured driving is included. The force-off initializer and its preparation/reset/replacement costs are real resources. An arbitrary old driven state cannot replace it. A time-reversal-odd field would require its actual reversed experiment; the self-reversed construction below excludes one.

## 2. Exact nuisance cancellation

For a microscopic path omega and its physical reversal R omega, local detailed balance gives

\[
\frac{P_F(d\omega\mid x_0,h)}{P_F(dR\omega\mid\Theta x_T,h)}
=\exp[-(E_h(x_T)-E_h(x_0))+FJ(\omega)].
\]

The actual initial Gibbs weights cancel the energy endpoints, so

\[
\frac{\mathbb P_{F,h}(d\omega)}{\mathbb P_{F,h}(dR\omega)}=e^{FJ(\omega)},
\qquad P_{F,h}(dj)=e^{Fj}P_{F,h}(-dj).                 \tag{1}
\]

No final equilibration is needed. This compares the forward ensemble with reversed paths assigned the same baseline initial density, not with an ensemble initialized at the actual driven final marginal.

For a continuous-time jump model the proof is explicit. Require reciprocal rates

\[
q_F(x,y)/q_F(y,x)=e^{-[E_h(y)-E_h(x)]+F d(x,y)},
\quad d(y,x)=-d(x,y).
\]

Jump-rate products telescope in energy. Reversal preserves the occupation time of every state, so escape-rate integrals cancel. Unknown symmetric activities, even if force-dependent, cancel. The baseline weights cancel the remaining energy difference. For an underdamped rotor the same identity is the microscopic reversibility relation of a Hamiltonian system with matched same-temperature Langevin thermostats and torque in its angular momentum equation. Its observed angular process need not be Markovian.

Every frozen h has the same multiplier e^{Fj}. An arbitrary posterior mixture over h therefore preserves (1). What is required after an old record is the actual conditional baseline law given h. Invariance alone does not prepare it.

## 3. Logistic inference and completed-trial stopping

For A=|J|>0 and S=sign J, (1) gives

\[
\Pr_F(S=+1\mid A=a,\text{old record})=(1+e^{-Fa})^{-1}. \tag{2}
\]

The magnitude distribution can contain arbitrary nuisance kinetics. Define

\[
\ell_n(F)=\sum_{i\le n}\{FJ_i/2-\log\cosh(FJ_i/2)\}.   \tag{3}
\]

Choose any fixed prior measure nu on a permitted candidate interval. A finite discrete mixture is sufficient. The conditional likelihood-ratio mixture

\[
\mathcal E_n(F)=\int e^{\ell_n(F')-\ell_n(F)}\nu(dF')    \tag{4}
\]

is a nonnegative martingale at the true F across completed prepared trials: each factor has conditional mean one, including after conditioning on the new magnitude. Thus

\[
\Pr_F(\exists n:\mathcal E_n(F)>1/\alpha)\le\alpha.
\]

The sets C_n={F: E_n(F)<=1/alpha}, or their running intersection, are anytime confidence intervals because ell_n is concave. Durations may depend on past completed records if each subsequent conditional experiment again satisfies (1). This permits stopping across trials. It does not validate an arbitrary state-dependent stopping time within a trial.

The coverage is averaged over complete prepared trials. Conditioning on a particular fresh initial angle or future bath/encoder history can destroy (2). Such records can be retained, but cannot silently become conditioning variables for the within-trial sign likelihood. Their use in future design is allowed only with the next full conditional initialization.

For a known force range |F|<=F_max and simultaneous sensing errors |Jhat_i-J_i|<=eta_i, each summand in (3) has displacement derivative bounded by F_max. Therefore, on the good sensing event,

\[
e^{-2F_{\max}\sum_i\eta_i}\widehat{\mathcal E}_n(F)
\le\mathcal E_n(F).                                    \tag{5}
\]

If the sensing event has failure probability delta, rejecting only when the left side exceeds 1/alpha gives coverage at least 1-alpha-delta. One does not condition the fluctuation theorem on that good event. Fixed nonzero resolution is not automatically harmless over indefinitely many trials.

## 4. A finite-bandwidth rotor encoder

For the physical momentum equation assume actual warranted bounds

\[
dv_t=\tau^{-1}[-r_t v_t+b_t]dt+\tau^{-1}\sqrt{2r_t}\,dW_t,
\quad r_-\le r_t\le r_+,
\quad |b_t|\le B=F_{\max}+L,                             \tag{6}
\]

where L bounds the rotor's conservative torque, including its interaction with hidden equilibrium coordinates. The bounds do not identify r_t or the hidden dynamics. The initial v is the actual Gibbs N(0,1/tau).

Let V(v)=exp(tau v^2/4). Its generator satisfies

\[
LV/V\le-r_-v^2/4+B|v|/2+r_+/(2\tau).
\]

Put

\[
v_c=\max\{4B/r_-,\sqrt{4r_+/(\tau r_-)}\},\quad
C=B^2/(4r_-)+r_+/(2\tau),\quad K=C e^{\tau v_c^2/4}.
\]

Outside |v|<=v_c the displayed polynomial is nonpositive, and inside it LV<=K. Optional stopping of Dynkin's formula at the first speed V_* therefore proves

\[
\Pr(\sup_{t\le T}|v_t|\ge V_*)
\le(\sqrt2+KT)e^{-\tau V_*^2/4}.                        \tag{7}
\]

This is uniform over the stipulated hidden kinetics. Choose V_* from a paid trial failure budget delta_i. Read the angular coordinate modulo 2pi at a fixed interval Delta satisfying

\[
V_*\Delta+2\zeta<\pi,
\]

with actual angular error at most zeta at every read. Nearest-neighbor phase unwrapping is then correct on the certified speed event. The full sum telescopes, so

\[
|\widehat J-J|\le2\zeta,                               \tag{8}
\]

independently of the number of reads. The error does not accumulate one radius per read. The preparation, angular calibration, finite read duration, read failure budget and detector backaction remain supplied measurement resources. This is not a claim that an arbitrary native observation port has them.

For any finite chosen set of trials, the number of reads is finite and scales as the sum of T_i V_*, with V_* of order sqrt(log((1+T_i)/delta_i)) for fixed physical bounds. Summable delta_i permit the anytime procedure. These are mathematical finite-bandwidth bounds; Gaussian velocity still has unbounded support, and a fixed uncharged saturation probability is not eliminated.

## 5. Uniform finite precision is attainable under the actual bounds

This paragraph supplies a deadline rather than merely a confidence interval that might never shrink. The constants are deliberately conservative, not a practical performance claim.

Take a fixed duration

\[
T\le\min\{\tau/(1024r_+),\sqrt\tau/(16B)\},\quad c=T/\sqrt\tau.
\]

Given initial |v_0| between 1/sqrt(tau) and 2/sqrt(tau), the martingale in the integral form of (6) has probability at least one half of staying below 1/(16 sqrt(tau)): Doob's L2 inequality uses its quadratic variation at most 2r_+T/tau^2. Gronwall then bounds sup|v_t-v_0| by 1/(4 sqrt(tau)). Thus

\[
\Pr\{3c/4\le|J|\le9c/4\mid\text{old record}\}
\ge p_0=\Phi(2)-\Phi(1)>0.                             \tag{9}
\]

Let w(a) be an even-magnitude weight: zero below c/4 or above 3c, one on [c/2,5c/2], linearly interpolated on the two remaining intervals. Its Lipschitz constant is 4/c. The weighted score is

\[
\psi_F(j)=w(|j|)j/(1+e^{Fj}).
\]

By (2), its conditional expectation at the true F is zero. It lies in [-3c,3c]. Since F_max c<=1/16, its displacement Lipschitz constant is at most 14 throughout the permitted force interval.

If every displacement error is at most eta<=c/4, each event in (9) produces a measured magnitude in [c/2,5c/2]. A conditional Hoeffding bound gives at least p_0 n/2 such events except with probability exp(-n p_0^2/2). On this event the negative derivative of the measured weighted score is at least n p_0 c_1/2, where

\[
c_1=c^2/[16\cosh^2(5F_{\max}c/4)].
\]

Let Fhat maximize the measured weighted concave log likelihood on [-F_max,F_max]. A martingale Hoeffding bound on the true score and the Lipschitz sensing bound imply, with probability at least 1-alpha_1-alpha_2-delta,

\[
|\widehat F-F|\le
\frac{2}{p_0c_1}\left[
3\sqrt2 c\sqrt{\log(2/\alpha_1)/n}+14\eta\right],         \tag{10}
\]

provided n>=2 log(1/alpha_2)/p_0^2. Clipping the maximizer to the force interval preserves the bound, including at its boundary.

For target error epsilon it is enough to choose

\[
\eta\le\min\{c/4,\epsilon p_0c_1/56\},\qquad
n\ge\frac{288c^2}{\epsilon^2p_0^2c_1^2}\log(2/\alpha_1)
\]

and the previous event-count bound. Equations (7)-(8) supply eta at a finite read rate. This is a complete finite task under the stated preparation and physical bounds. It may be very expensive: n scales at least as the inverse square of the short trial duration, while preparation is repeated n times. No hidden favorable relaxation rate or free retained bit pays that bill.

## 6. Work and information

The conditional Fisher information is

\[
\mathcal I(F\mid A=a)=a^2/[4\cosh^2(Fa/2)].
\]

For x=|F|a/2, the conditional mean dimensionless work is 2x tanh x. Since 2x<=sinh(2x),

\[
F^2\mathbb E\mathcal I(F\mid A)\le\tfrac12\mathbb E[FJ]. \tag{11}
\]

Longer directed runs can make negative signs rare rather than improving the conditional experiment. This is an accounting for these sign data, not a new universal thermodynamic uncertainty theorem. If Gaussian dynamics are actually known, ordinary mean/variance or full dynamical likelihood methods can use additional information and beat the robust conditional-sign method.

## 7. Force versus reported flow

Take independent Gaussian native displacements U_a with mean m_a f_a T and variance 2m_a T. Merely reporting J=(U_1+U_2)/2 gives a fluctuation-ratio slope

\[
2(m_1f_1+m_2f_2)/(m_1+m_2),                             \tag{12}
\]

which contains the unknown kinetics. Actual work was f_1U_1+f_2U_2.

With a real two-sided reciprocal transformer, output J_1=J_2=J and internal efforts e_a=(f_1+f_2)/2 instead give mean J=(m_1+m_2)(f_1+f_2)T/4 and variance J=(m_1+m_2)T/2. The slope is exactly f_1+f_2 because output work is now (f_1+f_2)J. The original internal carrier currents remain different. This is a concrete metrological implication of the force/flow distinction.

## 8. Decisive failures

- A two-state device with rates a exp(plus or minus F/2), initialized uniformly, obeys (1). Initialized in its driven stationary law, its finite-time probabilities of net current +1 and -1 are equal. The same slope estimator then reports zero despite nonzero F.
- At F=0, conditioning that device on fresh initial state 0 excludes negative net current. An unconditional baseline theorem is not a conditional guarantee for that label.
- A hidden active source G with perfectly tied current K=J changes the path ratio to exp((F+G)J). Only the sum is identifiable. Unknown equilibrium kinetics and unknown active work are different uncertainties.
- A state-selected first-passage duration need not preserve path reversal. It cannot replace the fixed-duration trial without accounting for its holding-time and endpoint selection.
- Integer winding alone omits the endpoint fractional displacement and hence part of torque work.
- Temperature, coordinate scale, force isolation and the baseline source cannot be inferred from the fluctuation ratio itself.

## Sources and status

Crooks, PRE 60, 2721 (1999), actual primary paper read, especially microscopic reversibility and finite-time work ensembles: https://arxiv.org/pdf/cond-mat/9901352 .

Shirts, Bair, Hooker and Pande, PRL 91, 140601 (2003), actual four-page primary paper read; it explicitly removes the unknown continuous work distribution by logistic conditioning and discusses fitting the slope: https://www2.stat.duke.edu/homeweb/scs/Courses/Stat376/Papers/NormConstants/FreeEnergy/ShirtsPandeMLEPhysRevLett2003.pdf .

Hayashi, Ueno, Iino and Noji, PRL 104, 218103 (2010), actual publisher abstract read; primary PDF unavailable through the tool. It is a direct torque-measurement predecessor. No experimental numerical claim or biological procedure is used: https://doi.org/10.1103/PhysRevLett.104.218103 .

The construction and estimates here were derived explicitly. They have not received an independent review or apparatus validation. No new fixture was needed. The candidate's main principle was preempted, so the role redirected to the composite-carrier feedback task rather than claiming a metrology discovery.
