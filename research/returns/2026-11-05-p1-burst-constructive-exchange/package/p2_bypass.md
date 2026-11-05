# P2 constructive bypass: finite thermal replacement without force identification

5 November 2026. Constructor: exchange_p2_bypass.

## Completed result

The final construction needs **no temporary harmonic pin**. A finite canonical position-pointer instrument, an additive force actuator, and fresh Gaussian dither synthesize exact local thermal momentum replacement on P2's original harmonic hidden-constant-force family. The nominal reset duration is \(6/(5\gamma)\), independent of its slow rate \(\lambda\). The identity holds for arbitrary initial joint laws of source, conserved hidden sector and old classical reference. Second moments are needed for finite expected control cost, not the identity.

Directed interval arithmetic certifies feasibility uniformly over \(0\le k/(M\gamma^2)\le1/4\), including arbitrarily slow original relaxation. This is not one favorable fixture. The root's compensated finite sine mark can then supply the original fixed-strength sine arms. Exact nominal stages compose in a full adaptive campaign. Calibration, arithmetic, range, switching, record erasure, cooling, reuse and model-validity errors remain paid. No universal linear *total* cost or nonlinear optimum is claimed.

Inputs read: P2 return/README/comparators at commit e9bd2054d8e396d82dc89d59b9851f1827fc55ef and its accepted local-thermal theorem at commit 3629d4ca14f495fb6999d2cd9bdd89a2be8c34ba.

## 1. Physical model and access

\[
dx_t=p_t/M\,dt,\quad
dp_t=(-kx_t+F-\gamma p_t+u_t)dt+\sqrt{2\gamma\sigma^2}\,dW_t,
\quad \sigma^2=M/\beta .
\]
The inaccessible \(F\) is constant during reset. P2 has \(F=kdZ\), conserved \(Z=\pm1\), and \(k=M\lambda(\gamma-\lambda)\). Any frozen hidden variable choosing \(F\), with arbitrary reference correlations, is allowed. Coefficients and instrument matrices are calibrated inputs; \(F\) is not.

The additive force port is a real hardware premise. P2 prices such forces, but a formal force variable does not manufacture an actuator. This applies when the declared experimental hardware can produce the finite waveforms after reading a finite meter. It does not apply to a thermostat-plus-passive-observer model excluding force control.

Preparation changes position. The guarantee is independence from the **contemporaneous post-preparation hidden marginal**, not restoration of the earlier hidden state. The reference is classical. Nonlinear/time-varying hidden force, colored-bath error and uncalibrated dynamics require separate bounds.

## 2. General Gaussian replacement theorem

Let \(U\) collect initial source coordinates and constant hidden forces, jointly distributed with any old reference \(R\). Completed observations and the prospective uncontrolled endpoint are
\[
O=GU+\nu,\qquad
\binom{x_T^0}{p_T^0}=HU+\binom{N_x}{N_p}.
\]
The centered noise \((\nu,N_x,N_p)\) is jointly Gaussian, independent of \((U,R)\), and includes actual pointer backaction and bath noise during the later control interval. Observations are completed before that interval.

Write \(h_p\) for the momentum row of \(H\). Choose
\[
G^Tw=h_p^T. \tag{1}
\]
Set \(Z_p=N_p-w^T\nu\), \(V=\operatorname{Var}Z_p\), \(c=\operatorname{Cov}(N_x,Z_p)\). If
\[
r=\sigma^2-V>0, \tag{2}
\]
draw fresh \(D_p\sim N(0,r)\), set \(D_x=-cD_p/r\), and apply a force with endpoint displacement
\[
d=\binom{D_x}{-w^TO+D_p}. \tag{3}
\]
Then
\[
p_T=Z_p+D_p,\qquad x_T=h_xU+N_x+D_x.
\]
All initial-state/force contributions to momentum cancel. Its variance is \(\sigma^2\), and its covariance with the final position noise is \(c-c=0\). Joint Gaussianity implies
\[
\boxed{\mathcal L(p_T,x_T,Z,R)=G_\sigma\otimes
       \mathcal L(x_T,Z,R).} \tag{4}
\]
Every unchanged hidden variable can be included. Initial laws may be non-Gaussian, singular and arbitrarily reference-correlated.

Fine observations \(O\) and dither seeds generally remain correlated with \(p_T\). They must be physically isolated/discarded or reset. Equation (4) is not conditional on retained fine \(O\). Their disposal must not leak into later timing/control.

Let \(S=\operatorname{Cov}\nu>0\), \(b=\operatorname{Cov}(\nu,N_p)\). For full-column-rank \(G\), the minimum-variance predictor satisfying (1) is
\[
w=S^{-1}b+S^{-1}G(G^TS^{-1}G)^{-1}
(h_p^T-G^TS^{-1}b). \tag{5}
\]
It minimizes \(\operatorname{Var}N_p-2w^Tb+w^TSw\). Within this fixed two-stage affine feedforward class, initial-mean cancellation is necessary and fresh independent dither cannot reduce variance. Thus \(V_{\min}\le\sigma^2\) is necessary in that class; strict inequality suffices. At equality this zero-data-dependent-position-feedback version also needs residual position covariance zero. More general controllers are not excluded.

## 3. Finite canonical pointers and uniform certificate

Eight independent pointers \((Q_j,P_j)\) have free Hamiltonians \(P_j^2/(2m_{\rm ptr})\). Successive finite boxes couple \(H_{{\rm int},j}=g_j(t)xP_j\). Then \(P_j\) is constant, \(\dot Q_j=P_j/m_{\rm ptr}+g_jx\), and the source receives actual backaction \(-g_jP_j\). All effects are included.

Normalized fixture:
\[
M=\gamma=\sigma=1,\quad 0\le k\le1/4,\quad
\tau_{\rm meter}=1,\quad \Delta=1/8,\quad g=1,\quad m_{\rm ptr}=100,
\]
\[
\operatorname{Var}Q_j=10^{-6},\qquad \operatorname{Var}P_j=10^{-2}. \tag{6}
\]
Read \(O_j=Q_j/(g\Delta)\) at the common meter deadline. The later force interval has \(h=1/5\); nominal total duration is \(6/(5\gamma)\).

Finite matrix exponentials give exact transfer/covariance matrices. A reduced implementation was compared independently with the root's full canonical-pointer matrices to \(10^{-12}\).

| \(k\) | \(V/\sigma^2\) | \(r/\sigma^2\) |
|---:|---:|---:|
| 0 | 0.6234368080 | 0.3765631920 |
| .01 | 0.6232650509 | 0.3767349491 |
| .10 | 0.6217217079 | 0.3782782921 |
| .25 | 0.6191593356 | 0.3808406644 |

The continuum proof covers \([0,1/4]\) by 100 exact decimal intervals. On each, fixed rational midpoint weights receive an exact three-coordinate gain correction satisfying (1); interval inversion verifies rank. This candidate upper-bounds the constrained optimum. Directed interval arithmetic proves
\[
\boxed{\sup_{0\le k\le1/4}V_{\min}(k)/\sigma^2<0.767447<1.} \tag{7}
\]
Independent pointer-position noise guarantees \(S>0\). The \(k=0\) point is a limiting certificate, not a normalizable spatial Gibbs state; every original \(k>0\) member is covered.

Files: p2_general_reset.py, p2_general_reset.json, p2_general_reset_interval.json.

## 4. Actual finite force waveforms

Let \(A=\left(\begin{smallmatrix}0&1\\-k&-1\end{smallmatrix}\right)\), \(B=(0,1)^T\). On the final interval \(h=.2\), use
\[
g_1(s)=\sin^2(2\pi s/h)\ (0\le s\le h/2),\qquad
g_2(s)=\sin^2(2\pi(s-h/2)/h)\ (h/2\le s\le h),
\]
zero elsewhere. Pulses and first derivatives vanish at support boundaries. Define \(L_i=\int_0^h e^{A(h-s)}Bg_i(s)ds\), \(L=(L_1,L_2)\), and coefficients \(v=L^{-1}d\). Then \(u=v_1g_1+v_2g_2\) produces (3) causally, without a delta kick.

For impulse response \((h_x,h_p)^T=e^{As}B\), on \(0\le s\le.2\), \(0\le k\le.25\),
\[
h_p(s)\ge1-s-ks^2/2\ge.795,\quad
(h_x/h_p)'=1+h_x/h_p+k(h_x/h_p)^2\ge1.
\]
Early pulses have a larger position/momentum ratio. Integration gives
\[
\det L\ge.795^2h^3/32=0.00015800625>0. \tag{8}
\]
Checked determinants are about \(0.0002263\).

The squared-force action is \(\int u^2ds=(3h/16)(v_1^2+v_2^2)\). For P2's initial hard fixture at \(D_0=1\), its expected value is about \(224\)–\(233\) normalized units, corresponding to Girsanov action \(56\)–\(58\). These are substantive control costs, not joules or an energy optimum. Meter preparation/cooling/records are additional. Gaussian amplitudes require finite peak clipping and an explicit overflow allowance.

## 5. Force information remains small

The two source sectors differ by drift \(2kd\). All meter couplings and feedback forces are common adapted functions of available records and fresh randomness, so cancel from that drift difference. The full augmented-path Girsanov information remains
\[
D(\mathsf P_+^t\Vert\mathsf P_-^t)
=\frac{4D_0\lambda}{\gamma}
+2D_0\lambda(1-\lambda/\gamma)^2t. \tag{9}
\]
Fresh ancillary states are sector-independent, and partial records cannot increase distinguishability.

At the fixed reset time \(O(1/\gamma)\), information is \(O(D_0\lambda/\gamma)\to0\) as \(\lambda\to0\), while (4) is exact. Thus replacement does not force hidden-sign identification. A noisy predictor cancels input-dependent mean contributions and the controller shapes the remaining noise. P2's inference bound cannot be promoted to an intervention lower bound under this admitted hardware. Its entropy composition and restricted independent-timing theorem remain valid.

## 6. Original sine arms and adaptive endpoint

The root independently constructs a finite loaded meter \(Y=p_{\rm trigger}+\xi\), with Gaussian \(\xi\) independent of initial state/reference and final source noise at a common deadline. Gain constraints and endpoint-noise orthogonality include physical backaction.

For
\[
a_v(Y)=\tfrac12[1+\eta e^{v/(2\sigma^2)}\sin(Y/\sigma)],
\]
the bound \(\eta e^{v/(2\sigma^2)}\le1\) makes this a probability and Gaussian convolution gives
\[
E[a_v(p+\xi)\mid p]=[1+\eta\sin(p/\sigma)]/2.
\]
Endpoint independence makes this a joint identity. The arm is withheld to the fixed deadline; temporary fine data is isolated/discarded.

Combined with (4), this supplies the original \(q_\pm=[1\pm\eta\sin(p/\sigma)]G_\sigma\), followed by actual common loaded-meter and future-response dynamics. A second meter is paid. Its feasibility in the original soft-spring range must be checked; a pinned fixture alone is insufficient.

If \(K\) denotes reset after discarded workspace is removed, \(CK=K\). Exact resets/marks therefore compose under arbitrary common adaptive future kernels, each process following its own history. The next reset must again satisfy the affine/frozen-force contract. Nominal fixed physical meter noise is not itself an accumulating approximation term. Finite implementation errors remain.

## 7. Reference-inclusive calibration formula

For an imperfect endpoint
\[
p=B\theta+N_p,\qquad x=H\theta+N_x,
\]
with independent centered Gaussian noise covariance
\(\left(\begin{smallmatrix}V_x&c\\c&V_p\end{smallmatrix}\right)\), \(V_x>0\), \(V_p-c^2/V_x>0\), and \(\theta\) containing all initial variables/reference, the exact augmented local replacement divergence is
\[
J_{\rm aug}=\frac12\left[
\frac{E(B\theta)^2}{\sigma^2}
+\frac{V_p}{\sigma^2}-1
-\log\frac{V_p-c^2/V_x}{\sigma^2}\right]. \tag{10}
\]
Retaining fewer initial variables only lowers the required divergence.

Near \(B=0,V_p=\sigma^2,c=0\), the expression is quadratic in mean-gain, relative-variance and cross-covariance errors, with constants depending on input moments and covariance margins. Under uniform moments, coefficient accuracy \(O(\epsilon/\sqrt n)\) suffices for an \(O(\epsilon^2)\) campaign KL budget.

This is a required precision, not acquired calibration. Actual excitation, observations, confidence, drift and exposure costs remain to be supplied. An \(O(n/\epsilon^2)\) calibration calendar requires an independently established fast identification experiment; it does not follow from (10).

## 8. Useful response duration

The unpinned harmonic source converts the sine-arm momentum contrast into
\[
\Delta E[x(t)-x(0)]
=2\eta\sigma e^{-1/2}
\frac{e^{-\lambda t}-e^{-(\gamma-\lambda)t}}
{M(\gamma-2\lambda)}. \tag{11}
\]
At \(t=1/\gamma\), the gain tends to \((1-e^{-1})/(M\gamma)\) as \(\lambda\to0\), and equals \(e^{-1/2}/(M\gamma)\) at critical damping. A nonvanishing useful response takes \(O(1/\gamma)\), not \(O(1/\lambda)\).

Use an increment rather than absolute position. In the hard fixture, the hidden-force/initial-position contribution to this short increment is \(O(\sqrt\lambda)\), while useful contrast and thermal/readout variance are order one in normalized units.

Equation (11) is the bare ideal response. Actual marking/readout latency and backaction belong in the declared loaded response or a separately proved comparison. It is not an instantaneous disturbance-free meter. Private randomized force probes can be cheaper for this linear mean-response task. That ordinary comparator is admitted; the replacement interface earns a stronger endpoint through arbitrary later physical experiments/decisions.

## 9. Resources and implementation qualifications

**Range and coarse centering.** P2's original position width grows as \(\lambda^{-1/2}\). A coarse latched center \(C\) can define a differential sensor via \(g(x-C)P\), leaving source backaction \(-gP\) unchanged. The relative coordinate sees unknown constant force \(F-kC\). Fixed MSE on \(x-C\) avoids multiplying numerical gain errors by a huge absolute coordinate. Centering needs a real sensor, offset range, memory and calibration. If locating/translating a port costs \(\lambda^{-1/2}\) time/hardware, it remains charged. The \(1.2/\gamma\) figure begins only once the required local port is ready.

**Preparation and classical regime.** One equilibrium realization of (6) uses mass \(100M\), trapping stiffness \(100M\gamma^2\), and pointer temperature \(10^{-4}\) times source temperature. Alternative squeezed/nonequilibrium preparations have their own work and uncertainty. Eight fresh pointers per reset and a further finite set for marking are not free. The phase-space standard-deviation product is \(10^{-4}k_BT/\gamma\); a classical realization requires this action scale comfortably above \(\hbar/2\). Initial pointer spread and independent final ADC error may share the position-noise budget after decoupling, but their actual joint realization must be supplied.

**Switches and bandwidth.** Force pulses are finite C1 functions. Meter coupling in the certificate uses finite rectangular boxes: finite amplitude does not certify finite slew. Strict slack and uniform gain rank permit sufficiently small smooth ramps with recomputed matrices by continuity. An explicit admissible finite-slew meter-ramp certificate has not been executed in this note. Supply it or retain a separately justified switching-error allowance; do not promote ideal steps to an acquired finite-bandwidth device.

**Peak clipping.** Gaussian feedback and dither have unbounded mathematical support. With only second moments, controlling \(n\)-trial overflow by \(\delta\) can require range \(O(\sqrt{n/\delta})\); justified sub-Gaussian envelopes improve this to \(O(\sqrt{\log(n/\delta)})\). These are different premises. Force range, maximum slew and any hardware saturation remain paid.

**Energy.** The reported \(\int u^2\) is an action/control resource. Mechanical work is \(\int up/M\). Driver energy requires actual impedance/efficiency; refrigeration, occupied hardware and memory reset add costs. No Landauer-optimality or energy-minimum claim is made.

**Finite precision and randomization.** Use finite ADC ranges/bits, arithmetic, random bits and waveform synthesis. Discrete Gaussian approximations do not have small raw TV to a continuous Gaussian. Couple ideal/quantized seeds and compare their physical force channels: Girsanov prices squared waveform mismatch divided by \(4\gamma\sigma^2\). Mean-square command error \(O(\epsilon^2/n)\) per trial is sufficient for that campaign KL contribution, but an arbitrarily precise analog actuator is not provided for free.

**Temporary records and reuse.** Fine observations/dither seeds are correlated with the output and must be isolated/discarded or reset on a fixed/padded schedule. Retaining them breaks (4). Reuse requires actual pointer/cold-bath reinitialization time or \(n\) fresh sets with disposal. Retained arms/outcomes require protection and remain in the reference. Sensor reinitialization, record reset reliability, cooling and physical isolation all remain in the bill.

A faithful calendar is
\[
T_{\rm cal}+\sum_{j=1}^n[
T_{{\rm locate/center},j}
+T_{{\rm pointer\,prep/reset},j}
+1.2/\gamma
+T_{{\rm arm\,mark},j}
+T_{{\rm response},j}
+T_{{\rm disposal/logic},j}],
\]
plus retries, overflows, deadlines and record collection. The nominal reset stage is constant per round; total cost need not be.

## 10. Existing methods and priority boundary

The strongest ordinary method here is Gaussian estimation with finite-time covariance/feedback control. Equation (5) is constrained least squares; endpoint force synthesis is controllability. No novelty is claimed for those components. The earned bridge is the complete old-reference-preserving replacement, including unknown force, actual backaction, covariance repair, causal force timing and record disposal.

Andersen velocity resampling is a valid competitor when physical rewrite/collision access is available. Here the reset is synthesized from sensing plus additive force rather than assumed as a simulation instruction. A full same-access priority comparison remains necessary.

Primary precedents retrieved:
- Martínez et al., *Engineered swift equilibration of a Brownian particle*, Nature Physics 12, 843–846 (2016), https://doi.org/10.1038/nphys3758 and https://arxiv.org/abs/1512.07821 .
- Gómez-Marín, Schmiedl and Seifert, *Optimal protocols for minimal work processes in underdamped stochastic thermodynamics*, J. Chem. Phys. 129, 024114 (2008), https://arxiv.org/abs/0803.0269 and https://doi.org/10.1063/1.2948948 . Its ideal optimal boundary impulses are not silently used here.
- Li, Quan and Tu, *Shortcuts to isothermality and nonequilibrium work relations*, Phys. Rev. E 96, 012144 (2017), https://arxiv.org/abs/1608.07757 and https://doi.org/10.1103/PhysRevE.96.012144 .
- *Optimal Control of Underdamped Systems: An Analytic Approach*, J. Stat. Phys. (2024), https://doi.org/10.1007/s10955-024-03320-w . Primary abstract describes Gaussian endpoint-control machinery using Lyapunov equations. Full theorem-level applicability remains to be compared.

Root retrieval refs: turn147search0, turn147academia38, turn148academia7, turn148search8, turn147search2, turn147academia39, turn148search6. Root must open these before citing them itself.

## 11. Preserved optional pin alternative

The earlier route adds a spring \(K\) at coarse center \(C\), with \(\omega^2=(k+K)/M\ge\gamma^2\). For \(c=(F+KC)/(k+K)\) and \(U_0=(\sqrt{\beta(k+K)}(x_0-c),p_0/\sigma)\),
\[
J(t)\le2e^{-\gamma t}(E\|U_0\|^2+1),\qquad t\ge\log(8)/\gamma.
\]
The proof mixes exact Gaussian kernels and needs no center-information entropy charge. At full damped-oscillator periods,
\[
p_t=ap_0+\sigma\sqrt{1-a^2}\xi_p
\]
with independent position noise and no force contribution. Feedback/dither completes a reset; separate pin files certify it. This requires extra curvature control, removed by the final no-pin construction. The centered switch-on work is \(K E(x-C)^2/2\); remote fixed centering would instead pay the growing absolute range.

## 12. Files, verification and limits

Final construction:
- p2_general_reset.py
- p2_general_reset.json
- p2_general_reset_interval.json

Earlier pin route:
- p2_reset_probe.py
- p2_reset_probe.json
- p2_reset_interval.json

Run in this directory:

    python3 p2_general_reset.py
    python3 p2_general_reset.py --interval --pieces 100
    python3 p2_reset_probe.py
    python3 p2_reset_probe.py --interval

NumPy/SciPy check finite gains, covariances and pulses. mpmath directed intervals certify the continuum variance margin. There were zero physical trials.

Completed: general Gaussian replacement theorem; causal finite meter/force construction; strict uniform feasibility on P2's original stiffness family; C1 force invertibility/action checks; exact separation from hidden-force inference; reference-inclusive endpoint calibration formula.

Unfinished: actual calibration acquisition/drift guarantees; executed finite-slew meter-switch certificate; actual hardware; optimal total resource law; universal nonlinear intervention law.

## 13. Stronger endpoint: prepare the original sine arms directly

This extension implements the original non-Gaussian arms without the second compensated marking meter. It uses the same finite pointer block, a shorter finite force window, and explicitly prepared non-Gaussian randomness. The random arm is withheld from the external controller until the intervention endpoint.

Use the notation of the reset theorem. Let
\[
R_p=N_p-w^T\nu,\quad V=\operatorname{Var}R_p,
\quad q=\operatorname{Cov}(\nu,R_p)=b-Sw,
\quad c=\operatorname{Cov}(N_x,R_p).
\]
Choose a position feedback vector \(s\) satisfying
\[
s^Tq=-c.
\]
The endpoint displacement in position is now \(s^TO\), so
\[
x_T=(h_x+s^TG)U+N_x+s^T\nu.
\]
The Gaussian noise \(N_x+s^T\nu\) is independent of \(R_p\). Both are independent of the arbitrary initial state and old reference.

Set \(r=\sigma^2-V>0\), and choose a fresh fair arm \(A\in\{-1,+1\}\). Conditional on the arm draw an independent scalar \(D\) with density
\[
d\mapsto G_r(d)\left[1+A\alpha\sin\left(\frac{\sigma d}{r}\right)\right],
\qquad \alpha=\eta\exp\left(\frac{V}{2r}\right)\le1.
\]
Drive the endpoint displacement
\[
(\Delta x,\Delta p)=(s^TO,-w^TO+D)
\]
using the finite two-pulse actuator. Then \(p_T=R_p+D\). A Gaussian convolution gives
\[
\mathcal L(p_T\mid A)=G_{\sigma^2}(p)
 [1+A\eta\sin(p/\sigma)]=q_A(p).
\]
For example, conditional on the sum \(R_p+D=p\), the Gaussian part of \(D\) has mean \(rp/\sigma^2\) and variance \(Vr/\sigma^2\). The sine attenuation is therefore \(e^{-V/(2r)}\), exactly canceled by \(\alpha\).

Consequently the complete endpoint identity is
\[
\mathcal L(A,p_T,x_T,Z,R)
=\tfrac12 q_A(p_T)\,\mathcal L(x_T,Z,R).
\]
The hidden marginal on the right is common to the two arms. It is the contemporaneous prepared marginal, not the initial spatial marginal. No inference of \(F\) or \(Z\) occurs. The initial law may be non-Gaussian and depend arbitrarily on the old adaptive history.

### Avoiding a position-range cost hidden in the feedback

A generic choice \(s\propto q\) changes position by a multiple of \(x_0\), which on P2's fixture can cost \(1/k\) in expected actuator action. This is unnecessary. Impose additionally
\[
s^TG_x=0,
\]
where \(G_x\) is the initial-position column. Only the first and last pointer readouts are needed for this correction: solve
\[
\begin{pmatrix}G_{0x}&G_{7x}\\q_0&q_7\end{pmatrix}
\begin{pmatrix}s_0\\s_7\end{pmatrix}
=\begin{pmatrix}0\\-c\end{pmatrix},
\]
and set the other six entries to zero. This leaves bounded gains on initial momentum and force and eliminates the divergent absolute-position displacement. It does not remove the meter's absolute position range; differential centering still has the preparation costs already listed.

### Uniform certificate and duration

Retain the eight-pointer meter of duration \(1/\gamma\), and use a force window \(1/(10\gamma)\). In normalized units the constrained-optimal fixtures have \(V=0.415866\) at \(k=0\) and \(0.414636\) at \(k=1/4\). For the original sine family at the chosen fixed nonvanishing strength \(\eta=1/2\), this gives \(\alpha\approx0.714\). The sufficient threshold is
\[
V/\sigma^2\le \frac{2\log 2}{1+2\log 2}\approx0.58094.
\]
The new interval certificate covers every \(k\in[0,1/4]\) with 100 exact decimal intervals. It constructs exactly mean-correct weights from each interval's fixed rational midpoint weights and a three-coordinate gain correction, then certifies
\[
V/\sigma^2\le0.550222391,\quad
\alpha\le0.921744982<1,
\]
and the two-coordinate correction determinant is at most \(-0.114997617\). Thus the complete original sine-arm intervention is feasible uniformly in a nominal meter-plus-force window \(11/(10\gamma)\). The interval construction uses its published piecewise rational candidate weights; the displayed point fixtures use the constrained optimum. Both satisfy the same endpoint theorem. The certificate is not a physical experiment.

The C1 actuator proof applies unchanged with the shorter window. Force action is much larger than in the Gaussian-reset version: the point fixtures with \(D_0=1\) give \(E\int u^2dt\) about 13,531 at \(k=0\), rising to 23,694 at \(k=1/4\), normalized \(M=\gamma=\sigma=1\). The corresponding Girsanov actions are about 3,383–5,924. These figures omit apparatus preparation and are not mechanical work. They remain finite as \(\lambda\downarrow0\), but no energy superiority is claimed. A longer-window optimized protocol or the Gaussian reset followed by compensated marking may cost substantially less.

### Randomness, reuse and campaign scope

The tilted density can be generated by rejection from \(G_r\), with acceptance probability \(1/(1+\alpha)\). Across fair arms the dither marginal is exactly \(G_r\); its conditional mean is \(A\eta\sigma e^{-1/2}\), and its conditional second moment is \(r\). The actuator-cost calculation includes that dither second moment. A finite number of precomputed attempts gives a declared failure probability; all launches use a common deadline. Gaussian generation, acceptance arithmetic, finite ranges and disposal of correlated registers require the same explicit accounting as the Gaussian reset. The time bound does not include their preparation time.

The endpoint identity composes through arbitrary future adaptive experiments and old histories within the affine constant-force source class, after the fine pointer records and private random seed are isolated or reset. It is the original two-arm campaign interface within this class, not a claim about all nonlinear Hamiltonians. Smoothing the meter's switch edges, acquiring calibration, and maintaining recycled cold pointers remain separate implementation obligations.

Files: `p2_direct_sine_arm.py`, `p2_direct_sine_arm.json`, `p2_direct_sine_arm_interval.json`. Reproduce with `python3 p2_direct_sine_arm.py` and `python3 p2_direct_sine_arm.py --interval --pieces 100`.

## 14. Stronger existing-method comparison

Chen, Georgiou and Pavon, *Steering state statistics with output feedback* (2015), https://arxiv.org/pdf/1504.00874 , DOI https://doi.org/10.1109/CDC.2015.7403244 , is the strongest directly relevant comparator located. Its Theorem 1 establishes finite-energy output-feedback steering between specified Gaussian endpoint distributions when the target covariance strictly exceeds the Kalman estimation-error covariance. The model assumes known Gaussian initial statistics, a controllable observable linear plant and continuous observations with independent Wiener measurement noise. The broad variance-floor mechanism and Gaussian steering are therefore established control machinery. The specific bridge here is cancellation uniform over arbitrary initial references and a constant unknown force, explicit finite canonical-pointer backaction, and the exact original non-Gaussian two-arm endpoint. Those details are not established by directly invoking that theorem. This comparison limits any novelty claim: the contribution is a concrete physical-instrument/application theorem and inference–intervention separation, not the discovery of covariance steering. Primary full-text retrieval: `turn187view0`; root must open it before using its citation.

## 15. Smooth meter completed

`p2_c1_meter_completion.md` supersedes the earlier unresolved meter-switch entry. Every pointer coupling now has explicit C1 cubic smoothstep edges, peak1 and maximum slew96 in normalized units. Exact finite matrix exponentials and a new100-piece directed interval certificate prove the original sine-arm operation uniformly over the complete stiffness interval: residual variance at most0.542831311 and required dither amplitude at most0.905327083. No impulsive meter switch remains. The separate note gives the exact lifted operation, independent full-state validation, and the still-required readout/ADC latency and recycling qualifications. This improvement does not change the finite calibration, hardware preparation or total-cost limitations.



