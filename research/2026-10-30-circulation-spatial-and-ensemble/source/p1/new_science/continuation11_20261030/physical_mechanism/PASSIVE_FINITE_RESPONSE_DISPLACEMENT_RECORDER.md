# Passive finite-response displacement recording and native-marginal likelihood transfer

30 October 2026. Constructive follow-on by the existing physical-mechanism
role. Earlier alternatives and receiving receipts are unchanged. This is a
second physical-model construction, not a completed electronic reader.

## 1. Result and ordinary mechanism

A passive reciprocal follower avoids the sustaining work of active
backaction cancellation. A weak elastic coupling connects a native
displacement to a damped inertial pointer. Every reaction and thermal-noise
term is retained. The response times remain finite. Its range, preparation,
weak component values and final reader are paid resources.

For $d=N^2$ measured channels on physical horizon $T_N=N^2T$, choose

\[
 g_N^2=H_N/N^2,\qquad H_N\to\infty,\qquad H_N=o(N).
 \tag{1}
\]

The construction gives a physical displacement pointer whose spatial
row-error norm has a full-time tail exponent $N^2H_N$. After marginalizing
the probes, the native path likelihood satisfies

\[
 \log E_0L_N^p,\quad \log E_gL_N^{-p}
 \le C_0N^2+Cp^2H_N^2,\qquad 1<p\le cN/H_N.
 \tag{2}
\]

$L_N=dQ_g/dQ_0$ compares the native marginal with and without the probes,
using the same native initial law. $C_0=0$ under exact canonical preparation.
A native initial density ceiling $e^{C_0N^2}$ is also allowed, but the
initial probes must remain fresh conditional Gaussians. Equation (2)
transfers any supplied native large-deviation principle at speed $N^2$
with unchanged rate. It does not require native mixing or a learned force.

The compared law is the **native marginal**, not the joint record of native
motion and all probe bath noise. The latter comparison exposes an
order-$g$ force and has a much larger likelihood cost. No total-variation
closeness or exact finite-system noninvasiveness is claimed.

Harmonic followers, generalized-Langevin baths and Kalman--Bucy filtering
are ordinary mechanisms. The useful connection here is the simultaneous
physical record accuracy and native-marginal action preservation at the
same volume scale. Historical priority for that conjunction is unestablished.

## 2. Native port and actual reciprocal follower

Take unit native masses, unknown interacting potential $U$, and unknown
fixed frictions in a warranted compact positive interval:

\[
 dX_i=V_i\,dt,\qquad
 dV_i=b_i(X,V)dt+\sqrt{2\gamma_i}\,dB_i,
 \qquad b_i=-\partial_iU-\gamma_iV_i.
 \tag{3}
\]

Assume well-posed nonexplosive dynamics and the canonical law
$\mu\propto e^{-U(X)-|V|^2/2}dX\,dV$. Periodic positions may be lifted to
count physical winding displacement; the winding counter itself need not
be stationary. Hidden native coordinates can be included in the complete
native path. Each measured velocity needs its actual nondegenerate thermal
channel as in (3).

The physical instrument is

\[
 \begin{aligned}
 dX_i&=V_i\,dt,\\
 dV_i&=[b_i(X,V)-gY_i]dt+\sqrt{2\gamma_i}\,dB_i,\\
 dY_i&=(gV_i-P_i)dt,\\
 dP_i&=(Y_i-a_iP_i)dt+\sqrt{2a_i}\,dW_i.
 \end{aligned}
 \tag{4}
\]

$a_i$ lies in a fixed compact positive interval. $B,W$ are independent
Brownian vectors, with genuinely joint independent sources across channels.
Initially $(Y_i,P_i)$ are independent standard Gaussian pairs, independent
of the complete initial native state and any admissible retained old record.
An arbitrary warm correlated probe initialization does not supply this law.

The actual pointer coordinate $U_i^{\rm ptr}$ has
$dU_i^{\rm ptr}=P_i\,dt$. Thus, pathwise,

\[
 g[X_i(t)-X_i(0)]
 =U_i^{\rm ptr}(t)-U_i^{\rm ptr}(0)+Y_i(t)-Y_i(0).
 \tag{5}
\]

The apparatus reads the pointer. The residual $Y$ bounds the error but is
not measured or subtracted. No copied microscopic state or hypothetical
second future is involved.

One mechanical realization has actual spring energy

\[
 {1\over2}[Y_i(0)+g(X_i-X_i(0))
                -(U_i^{\rm ptr}-U_i^{\rm ptr}(0))]^2
\]

and pointer kinetic energy $P_i^2/2$. The native reaction is $-gY_i$, the
pointer force is $+Y_i$, and a real damper supplies both $-a_iP_i$ and its
thermal noise. A displacement transformer or gear realizes the ratio $g$.
Equivalently, use $Q_i=U_i^{\rm ptr}/g$: the actual pointer mass, spring
stiffness and drag are $g^2,g^2,a_ig^2$. No ratio transformer is then needed,
but the small mass, large thermal velocity and spatial range become explicit.
Fixed response poles do not mean fixed fabrication cost or fixed travel.

The offset is a local spring preparation and a latched pointer origin.
Fresh relative thermal preparation is an initial resource, not a conclusion
from later invariance. For a periodic native coordinate, a winding linkage
or register must retain actual turns rather than only a phase modulo one
turn. Locality here is the interaction graph between a native port and its
own auxiliary; physical space, range and finite-component realization are
not inferred from the graph.

## 3. Passive circuit with the same reaction, and a real memory boundary

An ordinary capacitor in parallel with a series inductor--resistor branch,
inserted as a burden in a native current channel, realizes the reaction core.
In normalized thermal units choose

\[
 C=g^{-2},\qquad L=g^2,\qquad R=ag^2.
 \tag{6}
\]

Let native current be $V$, branch current be $\dot Q=P/g$, and capacitor
charge be $X-Q=Y/g$. Kirchhoff's law gives $\dot Y=gV-P$. The actual
capacitor voltage is $gY$, and the branch inductance, resistance and Johnson
noise give the last equation in (4). The driving-point impedance is

\[
 Z_g(s)=g^2\,{s+a\over s^2+as+1}.
 \tag{7}
\]

Its poles have finite response rates and its real part is nonnegative.
Its DC resistance is $ag^2$; its thermal voltage noise is the
fluctuation-dissipation noise of this same impedance. A noiseless resistor
would be a different supplier. There is no unilateral gain or cancellation
source hidden in (6).

The reaction circuit is not automatically a permanent charge register.
Total charge crossed through an inductor is not determined by instantaneous
current. An actual coulombmeter, storage element or mechanical pointer must
record that integrated branch motion. A new storage capacitor changes the
impedance and must be included. The mechanical free pointer makes the
storage coordinate explicit, at the cost of its range and final reader.
An ideal magnetic transformer likewise cannot be assumed to transmit an
unbounded DC history without a flux and saturation budget.

Equation (6) avoids such an ideal transformer in the reaction network, but
requires growing capacitance and decreasing inductance/resistance. Real
losses, tolerances, leakage, bandwidth and saturation remain properties of
the actual components. This is a physical finite-response model, not an
assertion that this asymptotic family can be built at fixed cost.

## 4. Energy and stationary law

The reaction core energy is

\[
 E=U(X)+|V|^2/2+|Y|^2/2+|P|^2/2.
 \tag{8}
\]

Both reciprocal pairs cancel in its differential: $-gY\cdot V+gV\cdot Y=0$
and $-Y\cdot P+P\cdot Y=0$. With
$\Gamma=\operatorname{diag}\gamma_i$ and $A_d=\operatorname{diag}a_i$,

\[
 \begin{aligned}
 dE={}&[-V^T\Gamma V-P^TA_dP
                 +\operatorname{tr}\Gamma+\operatorname{tr}A_d]dt\\
 &+V^T\sqrt{2\Gamma}\,dB+P^T\sqrt{2A_d}\,dW.
 \end{aligned}
 \tag{9}
\]

No powered unilateral term appears. The conservative drift is divergence
free and preserves (8); each thermal velocity generator preserves its
Gaussian. Consequently

\[
 \pi_g=\mu\otimes\mathcal N(0,I_d)_Y
                   \otimes\mathcal N(0,I_d)_P
 \tag{10}
\]

is invariant exactly. In the stationary experiment the mean stored probe
energy is $d$ and its mean net bath heat is zero. The unwrapped pointer's
memory coordinate is not asserted to be stationary or to have free range.

If $d\nu/d\mu\le e^{C_0d}$ and probes are fresh, the joint path law has
the same ceiling relative to the stationary experiment. That allows the
estimates below; it does not assert zero transient heat for a warm start.

Probe preparation, engagement, manufacture, thermal-source capacity, pointer
range, readout, communication and retirement/reset remain resources. The
passive balance does not bound the complete apparatus budget by $O(d)$.
It removes the continuously powered cancellation term, not every cost of
obtaining a usable recorded number.

### A loaded free-native example with an explicit heat bill

For free native coordinates under constant actual force $f_i=F_i/N$, the
linear velocity/reaction process has stationary means

\[
 \overline V_i={f_i\over\gamma_i+a_i g^2},\qquad
 \overline P_i=g\overline V_i,\qquad
 \overline Y_i=a_i g\overline V_i.
 \tag{10a}
\]

Its stationary covariance remains the identity. The actual source work
rate is $f_i\overline V_i$, and the two excess heat rates are
$\gamma_i\overline V_i^2$ in the native bath and
$a_i g^2\overline V_i^2$ in the pointer bath. These sum exactly to the source
work; equilibrium noise exchange has not been mistaken for extra load work.
On time $N^2T$,

\[
 E W_{\rm native}=T\sum_{i=1}^{N^2}
                     {F_i^2\over\gamma_i+a_i g^2}=O(N^2),
\]

\[
 E Q_{\rm pointer}^{\rm excess}
   =g^2T\sum_{i=1}^{N^2}
                  {a_iF_i^2\over(\gamma_i+a_i g^2)^2}=O(H_N)
 \tag{10b}
\]

for bounded $F_i$. Exact stationary preparation gives these equalities;
switching on the load from the centered canonical preparation introduces
only fixed-response mean transients. The instrument's finite native
mobility change is $O(g^2)$ and its displacement pointer remains real.
This example has neither a continuously powered cancellation source nor
the large active compensation bill. It does not extend the generic
likelihood theorem to all driven interacting native systems: those still
need the kinetic-moment premise stated in Section 8. Final readout and
hardware costs are not included in (10b).

## 5. Filtering the probe in the complete native path filtration

Conditioning on the complete probe path would give a quadratic Girsanov
cost $dg^2T_N=H_NN^2$, which is too large. The needed comparison instead
integrates out the hidden probe.

For one channel define

\[
 Z=\binom YP,\quad e=\binom10,\quad
 A=\begin{pmatrix}0&-1\\1&-a\end{pmatrix},\quad
 b_a=\binom0{\sqrt{2a}}.
 \tag{11}
\]

Then $dZ=(AZ+geV)dt+b_a\,dW$. In the complete native mechanical path,

\[
 dR=dV-b_i(X,V)dt=-g e^TZdt+\sqrt{2\gamma_i}\,dB.
 \tag{12}
\]

The unknown native force in this equation is a proof parameter; neither
recorder nor controller evaluates it. $V$ is an observed adapted input to
the hidden linear equation. Given that input, the hidden conditional law
is Gaussian. Equivalently, the initial native state and residual $R$
determine the native path by its well-posed equation, so the usual
linear-Gaussian filter with an observed input applies despite nonlinear
native interactions.

Write $m_i=E_g[Z_i\mid\mathcal F_t^{\rm native}]$. Its deterministic
conditional covariance obeys

\[
 \dot S_i=AS_i+S_iA^T+b_ab_a^T
        -{g^2\over2\gamma_i}S_iee^TS_i,
 \qquad S_i(0)=I_2.
 \tag{13}
\]

Since $A+A^T+b_ab_a^T=0$, Riccati comparison with the uncontrolled solution
gives $0\le S_i\le I_2$. Independent hidden sources give block-diagonal
covariance across channels; native interactions enter as observed inputs.
The filter is

\[
 dm_i=(Am_i+geV_i)dt
       -{gS_ie\over2\gamma_i}[dR_i+g e^Tm_i\,dt],
 \qquad m_i(0)=0.
 \tag{14}
\]

Under $Q_g$, $dI_i=(dR_i+g e^Tm_i dt)/\sqrt{2\gamma_i}$ is a native-filtration
innovation Brownian motion. The filter then has stable drift $A$,
observed input $geV_i$, and Brownian coefficient $O(g)$.

Under $Q_0$, evaluate the same functional of the native path. Here
$dR_i=\sqrt{2\gamma_i}\,dB_i$, so

\[
 dm_i=\left(A-{g^2\over2\gamma_i}S_iee^T\right)m_i\,dt
              +geV_i\,dt-{gS_ie\over\sqrt{2\gamma_i}}dB_i.
 \tag{15}
\]

The family $A$ is uniformly exponentially stable for the warranted compact
interval of $a_i$. The time-dependent perturbation in (15) is $O(g^2)$.
Variation of constants and Gronwall therefore give uniform exponential
stability for all sufficiently small $g$. No individual eigenvalue bound is
substituted for this uniform transition-matrix estimate.

Under either native law, therefore,

\[
 m=g\mathcal T[V]+gG,
 \qquad \int_0^{T_N}|m|^2dt
       \le Cg^2\int_0^{T_N}(|V|^2+|G|^2)dt.
 \tag{16}
\]

$\mathcal T$ is a deterministic stable convolution with bounded
$L^2$-operator norm. $G$ is a Gaussian convolution of the corresponding
native-filtration Brownian vector, with covariance bounded by $CI_{2d}$
at every time. $G$ and $V$ need not be independent.

## 6. Two-sided likelihood moments without a native mixing rate

In its own filtration the passive native law has drift $b_i-ge^Tm_i$,
with the same diffusion coefficient as the reference. Set

\[
 u_i=-{g\over\sqrt{2\gamma_i}}e^Tm_i,
 \qquad \mathcal A_T=\int_0^{T_N}|u|^2dt.
\]

Equation (16) yields

\[
 \mathcal A_T\le Cg^4\int_0^{T_N}(|V|^2+|G|^2)dt.
 \tag{17}
\]

Under the stationary version of either law, $V(t)$ has a standard Gaussian
marginal. The warm-start path ceiling preserves a useful exponential
bound. Jensen in time gives, for small enough $qg^4T_N$,

\[
 \begin{aligned}
 E e^{Cqg^4\int_0^{T_N}|V|^2dt}
 &\le {1\over T_N}\int_0^{T_N}
              E e^{Cqg^4T_N|V(t)|^2}dt\\
 &\le e^{C_0d}(1-C' qg^4T_N)^{-d/2}.
 \end{aligned}
 \tag{18}
\]

The same estimate applies to $G$ with its uniformly bounded Gaussian
covariance. Cauchy--Schwarz combines the two without assuming independence.
For either $Q_0$ or $Q_g$,

\[
 \log E e^{q\mathcal A_T}
 \le C_0'd+Cq,d g^4T_N,
 \qquad qg^4T_N\le c.
 \tag{19}
\]

Only single-time canonical velocity moments, stable probe response and the
actual initial ceiling were used. Native temporal correlations can remain
arbitrarily slow.

The exponential-integrability case needed for the drift change holds, and
the native-marginal likelihood is

\[
 L={dQ_g\over dQ_0}
  =\exp\left(\int u\cdot dB-\tfrac12\mathcal A_T\right).
 \tag{20}
\]

For $p>1$, write $L^p$ as the square root of the exponential local martingale
with integrand $2pu$, times $e^{(p^2-p/2)\mathcal A_T}$. Cauchy--Schwarz,
the nonnegative exponential-supermartingale bound and (19) give

\[
 \log E_0L^p\le C_0'd+Cp^2dg^4T_N,
 \qquad p^2g^4T_N\le c.
 \tag{21}
\]

Under $Q_g$, the inverse density uses $-u$ against its innovation Brownian
motion. The same estimate holds for $E_gL^{-p}$, because (19) holds under
that law too. The physical and filtered equations have the same uniquely
specified native marginal; the change of measure is not defining a
different apparatus.

More explicitly, measure identification can start from the actual passive
law: (19) makes the reverse exponential a true martingale under $Q_g$.
After that change of measure the native drift is exactly $b$ and its
diffusion and initial law are unchanged. Weak uniqueness of the original
native equation identifies the resulting native law with $Q_0$. Taking
the reciprocal density gives (20), without requiring a separate
uniqueness theorem for a hypothetical apparatus with a Volterra force.

Since $dg^4T_N=O(H_N^2)$ and $g^4T_N=O(H_N^2/N^2)$, this proves (2).
Taking $p_N\asymp\sqrt{N/H_N}$ gives

\[
 {1\over p_NN^2}
 \max\{\log E_0L^{p_N},\log E_gL^{-p_N}\}\to0.
 \tag{22}
\]

Two-sided Hölder inequalities then transfer every supplied native
speed-$N^2$ LDP, including exponential tightness, with unchanged rate for
any measurable native path observable to which that LDP applies. This
does not establish an LDP for an arbitrary unknown potential. It also
does not give total-variation closeness; $H_N^2$ can diverge.

Unknown fixed classes can be treated conditionally with uniform constants.
A mixture retains the likelihood bound by first comparing the matched
joint class/native law and then projecting. Its native rate, if one exists,
is still the rate of the actual mixture, not an averaged class coefficient.

## 7. Full-time row precision and the correct controller interface

Partition the actual fixed channels into $N$ groups $\mathcal R_y$ of $N$
channels. Define

\[
 \eta_y(t)={1\over N^2}\sum_{i\in\mathcal R_y}
 \left[{U_i^{\rm ptr}(N^2t)-U_i^{\rm ptr}(0)\over g}
              -(X_i(N^2t)-X_i(0))\right].
 \tag{23}
\]

This is the difference of two row sums of $Y$, divided by $gN^2$.
At any fixed stationary time, those row sums have joint Gaussian covariance
$NI_N$. Different times need not be jointly Gaussian: a triangle bound on
their individual norm tails suffices. Consequently

\[
 P_g\left\{\left({1\over N}\sum_y\eta_y(t)^2\right)^{1/2}
                  >\varepsilon\right\}
 \le e^{C_0d+CN-c\varepsilon^2N^2H_N}.
 \tag{24}
\]

For full time use a unit physical-time grid and $\dot Y=gV-P$. On each
interval, the squared norm of the vector of row increments is at most
the integral of the squared norm of the row vector $\sum(gV_i-P_i)$.
At each stationary time this derivative vector is Gaussian with covariance
$N(1+g^2)I_N$. Jensen's exponential estimate on that integral and a union
over $O(N^2)$ intervals preserve the exponent. The warm path ceiling is
then imposed once. Thus

\[
 \boxed{
 P_g\left\{\sup_{t\le T}
    \left({1\over N}\sum_y\eta_y(t)^2\right)^{1/2}
                   >\varepsilon\right\}
 \le\operatorname{poly}(N)e^{C_0d+CN-c\varepsilon^2N^2H_N}.}
 \tag{25}
\]

Choose $H_N/K_N^2\to\infty$ for a joint row-norm envelope $C/K_N$ with
super-volume failure. $H_N=\log(N+2)$ and
$K_N=\log\log(N+e^e)$ are compatible with (1).

The older maximum-row requirement is not supplied: its scalar exponent
at $C/K_N$ is only $NH_N/K_N^2$, not $N^2H_N/K_N^2$. A receiver must use
the joint norm in (25) and a separate large scalar threshold for its force
cap. At the cap scale $Na_N/K_N$, $a_N=N^{-1/4}$, the same row calculation
gives

\[
 \operatorname{poly}(N)
 \exp[C_0d-cN^{5/2}H_N/K_N^2],
 \tag{26}
\]

which is super-volume for the concrete parameters. The full-time argument
also applies to this scalar threshold.

## 8. Port, record and physical limits

The groups in (23) must be actual current channels. Fixed electrical
branches or fixed particle lanes provide literal grouping. A tagged
particle's horizontal displacement is not its Eulerian row current when
it crosses between rows. Actual local attribution or spatially resolved
ports are then needed. The filter does not create them.

This supplier also does not arise automatically from a finite menu of
hidden jump operations. It needs a continuous displacement port, reciprocal
force access and the underdamped thermal channel in (3). It has not been
constructed for exclusion jumps by renaming their counts. The earlier
spatial exclusion example and this mechanical recording supplier remain
different interfaces unless explicitly connected.

The final pointer reader must supply its actual response, noise, resolution,
timestamps and backaction. Equation (25) bounds intrinsic follower error,
not arbitrary added electronic, optical or mechanical readout error.
Reader forces must be included in (4) or separately controlled. A physical
pointer is stronger than an unexplained integral symbol, but is not by
itself a complete digital counter, communication network or reliable
instrument.

The conversion factor $g$ in the displayed count must be the actual known
or sufficiently calibrated transduction scale. Positive bounded unknown
frictions require no kinetic estimation, but an unknown fixed fractional
gain error does not disappear when a displacement is divided by a nominal
$g$. The receiving program must pay the required relative gain accuracy and
whole-protocol confidence. Channelwise known gains comparable to $g_N$ can
be handled with weighted sums; an uncharacterized gain is a different
readout interface.

Range is also real. In direct mechanical coordinates the thermal offset is
$1/g=N/\sqrt H$. In a free diffusive native example the normalized pointer
excursion on time $N^2$ is typically $O(\sqrt H)$. An arbitrary unknown
system needs an actual displacement bound. Canonical velocity marginals
alone give a conservative polynomial bound: Jensen on $\int V_i dt$
allows a native displacement cutoff $N^3\ell_N$ with super-volume failure
for $\ell_N\to\infty$, and pointer range $N^2\sqrt H\,\ell_N$.
This is a capacity obligation, not an efficient apparatus claim. A winding
register must physically retain its number of turns.

Conditional statements require the initial native ceiling and fresh probe
Gaussians conditional on the old record. Arbitrary correlated probe
initialization breaks the exact filter. The native marginal comparison
does not preserve that law after arbitrary postselection on future probe
records. Exposing complete probe noise exposes the order-$g$ force and
invalidates the small-marginal-cost inference. For a controller using only
the macroscopic pointer estimate, (25) is the appropriate error input to
a subsequent joint pushforward argument.

No weak-load or driven Gibbs assertion has been imported silently. The
likelihood proof uses a stationary canonical reference or its specified
warm initial ceiling. Nonstationary driving needs its own uniform
exponential kinetic-moment bound or a separate tilt argument. The exact
passive equations and count identity remain true, but that alone is not
the driven LDP proof.

## 9. Primary predecessors actually consulted

R. Zwanzig, *Nonlinear generalized Langevin equations*, J. Stat. Phys. 9,
215--220 (1973), DOI <https://doi.org/10.1007/BF01008729>; actual PDF:
<https://courses.physics.ucsd.edu/2020/Fall/physics210b/Zwanzig1973_NonlinearGeneralizedLangevinEq.pdf>.
The quadratic bath, exact elimination for an arbitrary nonlinear native
force, and fluctuation-dissipation relation were read. Harmonic bath
elimination is a direct predecessor, not the new part claimed here.

R. E. Kalman and R. S. Bucy, *New Results in Linear Filtering and Prediction
Theory*, J. Basic Eng. 83, 95--108 (1961), DOI
<https://doi.org/10.1115/1.3658902>; actual PDF:
<https://people.duke.edu/~hpgavin/SystemID/References/KalmanBucy-ASME-JBE-1961.pdf>.
The actual setup, white-noise observation assumptions and covariance/filter
framework were read. Later targeted retrieval of the detailed sections
timed out. The specific observed-input Riccati and likelihood arguments
needed here are displayed above rather than attributed to an unread section.

H. Nyquist, *Thermal Agitation of Electric Charge in Conductors*, Phys.
Rev. 32, 110 (1928), DOI <https://doi.org/10.1103/PhysRev.32.110>.
The primary publisher abstract and indexed original-paper extract with
$4RkT$ voltage noise and its impedance-network extension were read. Full
retrieval of the PDF at
<https://123.physics.ucdavis.edu/johnson_files/nyquist_1928.pdf> timed out;
no claim relies on having retrieved that entire article.

The ordinary passive follower is a stronger comparison than an ideal active
cancellation circuit with unpriced unilateral gain. It trades small burden
for pointer uncertainty and range, then uses collective precision. The
finite native system does change. The proved useful statement is that its
native-marginal likelihood cost is negligible at the volume scale while its
physically generated pointer record is accurate on that same scale.
