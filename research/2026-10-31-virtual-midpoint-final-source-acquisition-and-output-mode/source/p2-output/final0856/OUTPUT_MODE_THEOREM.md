# Reliable sector readout through an unprepared linear receiver

Research construction, 31 October 2026. The new results below are working
theorems for their stated models, with proofs and ordinary executable checks.
They are not a device qualification or a claim of priority over the literature.
The earlier warm-absorption, return, local-orbit and actual-history results are
preserved; this construction changes the readout interface.

## 1. Physical question and result

Can a useful quantum measurement be repeated while its receiver and retained
gain source remain unprepared, without learning the gain's quantum dynamics?

There are two constructive answers in this note.

1. For a calibrated finite passive linear receiver, a measured output temporal
   mode can eliminate every unknown initial receiver operator. Positive bounded
   operator gain then gives a uniform measurement bound, even when that gain
   does not commute with the source Hamiltonian. Stable receiver networks with
   nonzero DC response have exponentially improving label accuracy with time.
2. With only a coarse linewidth interval, a resonant receiver of bounded mean
   energy can instead use delayed boxcar integration. Its complete duration is
   logarithmic in requested inverse error and initial energy. This is ordinary
   dissipative settling, augmented by a quantum-gain and correlated-history
   guarantee. It does not require purification or a reset of the gain source.

The exact-cancellation result covers arbitrary initial receiver states. The
coarse-calibration result needs an energy bound. Both require a physical
sector-scalar interaction, fresh input field, actual output collection and
measurement, and the stated receiver dynamics. An operator-valued fluctuating
receiver pole is different from an operator-valued force amplitude.

## 2. Model and meanings of protection

Let the retained data have an involution

\[
 W=P_+-P_-,\qquad W^2=I.
\]

Either eigenspace may have arbitrary dimension. The rest of the retained system
is a source E and a bosonic receiver. Initially they may be arbitrarily
correlated with the data and an external reference. The newly incident field
on each observation interval is independent of all of them and of the actual
past record. Its state is vacuum or a specified Markov thermal Gaussian state.

The resonant one-mode model, with hbar=1, is

\[
 H=H_E(t)+W\otimes G_E(t)\otimes(a+a^\dagger),\qquad
 0<g_- I\le G_E(t)\le g_+I,
\]

\[
 da=-\frac\kappa2a\,dt-iWG_E\,dt-\sqrt\kappa\,dB_{\rm in},
 \qquad dB_{\rm out}=dB_{\rm in}+\sqrt\kappa a\,dt.
\]

The Langevin equation is notation for a unitary system-field dilation, not an
assumption that the quantum gain is a classical stochastic number. Source
dynamics, including its noncommutation with G, is retained. For finite-dimensional
E, bounded sufficiently regular G and the usual linear receiver dilation give
the core setting. Extensions to unbounded sources require self-adjointness,
common-domain/propagator and approximation-limit conditions. The mathematical
bound contains no norm of H_E.

Every actual Hamiltonian, output coupling and measurement operation must act as
the identity on the data multiplicity inside each W sector. Equivalently, every
fine measurement operator has the structure

\[
 K_r=P_+\otimes V_{r,+}+P_-\otimes V_{r,-}.                 \tag{1}
\]

Commuting with W is insufficient. For example Z1+Z2 commutes with two-spin SWAP
but rotates the triplet. Conversely, (1) permits arbitrary source/receiver
evolution and its correlations. Fine records can steer pre-existing data-source
correlations. It is incorrect to claim an unchanged conditional data marginal
for every fine record merely from (1).

The reusable target is a coarse two-outcome projective instrument, with a
possibly outcome-dependent CPTP source channel and identity action on each
retained data sector. Source restoration is not part of that target.

The mathematical input-output conventions are standard Gardiner-Collett
theory. The new construction combines them with constrained temporal filtering
and the positive-operator transport principle. The latter is explicit in the
accessible Astra N1419 source cited at the end.

## 3. Exact removal of a resonator's initial quantum operator

Put a0=kappa/2, z=exp(-a0 T), and define

\[
 V=T-\frac4\kappa\tanh\frac{\kappa T}{4},\qquad
 w(t)=\frac{1-2e^{-a_0t}/(1+z)}{\sqrt V}.                 \tag{2}
\]

For every T>0, V>0 and

\[
 \int_0^T w^2dt=1,\quad
 \int_0^T w(t)e^{-a_0t}dt=0,\quad
 \int_0^T w(t)dt=\sqrt V.                                \tag{3}
\]

This is the normalized orthogonal projection of the constant function away
from the unknown cavity transient. It is an ordinary linear receiver filter.

First turn off the logical force only as a mathematical interaction-picture
construction. Denote the resulting free passive dynamics by a_f and b_out,f.
The final output mode

\[
 B=\int_0^T w(t)b_{{\rm out},f}(t)dt
   =-\int_0^T w(T-t)b_{\rm in}(t)dt                      \tag{4}
\]

contains no a(0) operator. This cancels the whole initial quantum mode, not
only its mean amplitude. B is canonical. Its quadrature
Y=i(B^dagger-B) has a Gaussian marginal of variance

\[
 v=2n_b+1.                                               \tag{5}
\]

Fresh field input makes this marginal independent of every initial retained
system and of each actual preceding history. A Gaussian *unconditional*
marginal without that freshness condition would not be enough: correlating the
data sector with the sign of an initially Gaussian pointer can double a tail
probability. Vacuum purity implies factorization; a mixed thermal marginal by
itself does not.

Equation (4) does not assert that the driven output equals a Gaussian variable
plus an independent quantum gain. A different argument is needed for that case.

## 4. Quantum gain: a transport proof rather than a random-displacement ansatz

The free commutator with the selected future output mode is

\[
 [a_f(t),B^\dagger]=\sqrt\kappa\,k(t),\qquad
 k(t)=\int_t^T w(u)e^{-a_0(u-t)}du
 =\frac{(1-e^{-a_0t})(1-e^{-a_0(T-t)})}
 {a_0(1+z)\sqrt V}\ge0.                                  \tag{6}
\]

Write a_f(t)=sqrt(kappa) k(t) B+a_perp(t), where a_perp commutes with B and
B^dagger. With X=B+B^dagger, [X,Y]=2i. In the Y representation X=2i partial_Y.
In a fixed data sector s=+/-1 the interaction-picture Hamiltonian is

\[
 H_s(t)=s\sqrt\kappa k(t)G_E(t)X+V_s(Y,t),               \tag{7}
\]

where V_s is Hermitian and local in Y. It contains H_E and every complement
mode. It can be unbounded subject to the stated domain conditions. Its local
action changes neither probability density nor the associated current.

If rho(y,t) is the pointer density after tracing the internal components,

\[
 \partial_t\rho+\partial_y j_s=0,\qquad
 j_s=-2s\sqrt\kappa k(t)\langle\psi(y)|G_E(t)|\psi(y)\rangle.
                                                               \tag{8}
\]

For s=+, every component's velocity is at most -2 sqrt(kappa) k g_-.
A moving-boundary flux comparison therefore gives

\[
 \Pr(Y_T\ge0\mid s=+)\le\Pr(Y_0\ge\mu_-),\qquad
 \mu_-=2\sqrt\kappa g_-\int_0^Tk(t)dt
       =4g_-\sqrt{V/\kappa}.                              \tag{9}
\]

The negative sector obeys the reflected inequality. Consequently

\[
 \boxed{p_{\rm wrong}\le Q(\mu_-/\sqrt v)},\qquad
 Q(x)=\frac1{\sqrt{2\pi}}\int_x^\infty e^{-u^2/2}du.       \tag{10}
\]

The bound is an operator effect bound on all initial source/receiver/reference
states, because it holds for every such state. Rapid noncommuting source
evolution changes the internal components in (8) but cannot reverse the
qualified current. No frozen-source approximation or inverse evolution is used.

A common source-only force F_E, with ||F_E||<=f<g_-, is allowed by replacing
the gain interval with [g_--f,g_++f]. Indeed, in sector s the directed force
is G_E+sF_E, which has those bounds even when F_E and G_E do not commute.
This charges a bounded unwanted drive rather than supposing exact cancellation.
If the permitted force can vanish or change sign, the uniform discriminator can
fail; positivity is an actual interaction qualification.

A known nonnegative switching envelope u(t) is handled by replacing g_- and
g_+ inside the transport integrals with u(t)g_- and u(t)g_+. Turn-on, turn-off
and collection tails must be included in the physical duration; the constant-
force formulas are not a claim that a zero-time experimental ramp is available.

For a constant classical gain g, the stronger exact Gaussian effect identity is

\[
 E_y=\sum_{s=\pm}P_s\frac{e^{-(y+s\mu)^2/(2v)}}{\sqrt{2\pi v}}
       \otimes I_{\rm initial\ receiver},\quad
 \mu=4g\sqrt{V/\kappa}.                                  \tag{11}
\]

For an operator-valued gain, (11) generally fails. Use (1) and (10), not an
invented scalar fine effect.

Detection efficiency eta with an independent vacuum loss port gives the same
argument on a larger pointer: replace the standardized shift by
sqrt(eta) mu/sqrt(1+2 eta n_b). Other known Gaussian amplifier noise adds its
variance. Unknown offsets, gain asymmetry and nonlinear detection require their
own bounds. Digital postprocessing cannot undo photons that already disturbed
a logical state through a nonscalar interaction.

## 5. Known dispersive shifts and the indispensable negative-kernel correction

Suppose sector s has a fixed scalar receiver pole

\[
 \lambda_s=\kappa/2+i\delta_s.
\]

These terms may be large; they need not be discarded as a perturbation. Form the
real span S of Re exp(-lambda_s t) and Im exp(-lambda_s t) for the finitely many
known poles, remove redundant functions, and set

\[
 w_0=1-\mathsf P_S1,\quad V=\|w_0\|_2^2=\int w_0dt,
 \quad w=w_0/\sqrt V.                                    \tag{12}
\]

One real filter cancels both initial quadratures for every sector. The free
input modes B_s can differ between sectors; they are proof coordinates for the
same physically measured homodyne statistic, not conditional hardware choices.
Each is a fresh canonical Gaussian mode.

Define k_s(t)=int_t^T w(u)exp[-lambda_s(u-t)]du and beta_s=Re k_s. With this
definition the correct commutator is

\[
 [a_{f,s}(t),B_s^\dagger]=\sqrt\kappa\,k_s(t)^* .          \tag{13}
\]

Thus the pointer force is sqrt(kappa) beta_s G X_s. The imaginary component
gives +sqrt(kappa) Im(k_s) G Y_s, a local potential. The conjugation matters to
the decomposition but leaves the real transport coefficient unchanged.

For beta_s of either sign, its guaranteed integrated displacement is

\[
 \mu_s=2\sqrt\kappa\int_0^T
       [g_-\beta_s^+(t)-g_+\beta_s^-(t)]dt.              \tag{14}
\]

If min_s mu_s>0, (10) holds with that minimum. The upper gain bound is needed:
on an adverse piece of the response kernel the source may select its largest
allowed gain.

### A failed shortcut

One cannot generally demand beta_s>=0 when delta_s is nonzero while cancelling
both initial quadratures. If k=u+iv, then k'=lambda k-w and k(0)=k(T)=0.
The imaginary equation gives

\[
 \delta_s\int_0^T e^{-\kappa t/2}u(t)dt=0.
\]

For nonzero delta, u>=0 would force u=0. Negative pieces are therefore a
structural feature of this exact annihilator, not numerical noise.

### Why the correction remains finite

The cancellation identity gives

\[
 \int_0^T\beta_sdt=\operatorname{Re}(1/\lambda_s)\sqrt V.  \tag{15}
\]

For each fixed finite set of stable poles, V=T-O(1), and
int beta_s^- dt=O(T^-1/2). To see this, write w0=1-v_T.
The finite Gram matrix for the independent transient functions is bounded
below by its positive value at any T0>0, while each function and its integral
decays exponentially. Therefore ||v_T||_1 is uniformly bounded for T>=T0.
The step-response kernel from 1 differs from its positive DC limit only in a
terminal region of bounded integral. Convolution with v_T also has bounded
L1 norm. Division by sqrt(V) proves the assertion.

Hence

\[
 \mu_s\ge 2\sqrt\kappa\left[
 g_-\operatorname{Re}(1/\lambda_s)\sqrt V
 -(g_+-g_-)B_s/\sqrt V\right],                           \tag{16}
\]

with a finite constant B_s independent of T. A fixed gain interval therefore
permits exponentially decreasing label error without gain-source freezing.

## 6. A finite interacting receiver network

The same proof applies beyond one oscillator. Let a be an M-mode vector with

\[
 da=Aa\,dt-i\ell WG_E\,dt-C^\dagger d\mathbf B_{\rm in},
 \quad A=-iK-C^\dagger C/2,
\]

where K is Hermitian and all loss ports are included. Select an observed output
row C_o. Assume A is stable with ||exp(At)||<=M0 exp(-alpha t). The interaction
Hamiltonian is WG_E(ell^dagger a+a^dagger ell). All fresh input ports are vacuum
or have the same known thermal occupation; general known covariances can be
handled separately but are not assumed identical without qualification.

Use the real nuisance span generated by the real and imaginary parts of
(C_o exp(At))_j. Define w0,V,w as in (12). With
B=exp(i phi) int w b_out,f, every initial receiver mode disappears and

\[
 c(t):=[\mathbf a_f(t),B^\dagger]
 =e^{-i\phi}\int_t^T w(u)e^{A^\dagger(u-t)}C_o^\dagger du,
 \quad\beta(t)=\operatorname{Re}[\ell^\dagger c(t)].       \tag{17}
\]

Choose a constant local-oscillator phase so that the DC response

\[
 \chi=\operatorname{Re}[-e^{-i\phi}\ell^\dagger
                   (A^\dagger)^{-1}C_o^\dagger]>0.        \tag{18}
\]

This is possible exactly when that complex response is nonzero. The pointer
Hamiltonian is WG[beta X-Im(ell^dagger c)Y] plus a local complement potential.
Therefore

\[
 \int\beta dt=\chi\sqrt V,\qquad
 \mu=2\int[g_-\beta^+-g_+\beta^-]dt.                     \tag{19}
\]

Let L0=sup_(T>=T0)||projection_S(1)||_1, which is finite by the Gram argument.
An explicit conservative constant is

\[
 B_0=\|\ell\|M_0\|C_o\|
               (\alpha^{-2}+L_0/\alpha).
\]

Indeed, the step-response tail has integrated deviation at most
||ell|| M0 ||C_o||/alpha²; the projected correction has integral at most
||ell|| M0 ||C_o|| L0/alpha. Thus

\[
 \int\beta^-dt\le B_0/\sqrt V,\quad V=T-O(1),\qquad
 \boxed{\mu\ge2g_-\chi\sqrt V
                -2(g_+-g_-)B_0/\sqrt V.}                \tag{20}
\]

Every fixed finite passive stable receiver with nonzero DC transduction admits
this readout. Its internal oscillators can interact, be arbitrarily populated,
and retain correlations with the computation. The calibrated object is the
observable transient space; a microscopic reconstruction of every source or an
internal realization is unnecessary. Existing linear-system identification is
relevant to obtaining that space, and its acquisition cost must be counted.

For several sector-dependent networks, one common physical homodyne phase must
make every relevant DC response positive. Nonzero individual responses do not
by themselves guarantee this common phase. A known finite family can be included
in the nuisance span. Dark/unstable modes, nonlinearities, operator-controlled
poles, and unknown continua are outside the stated finite-network result.

## 7. Coarse calibration: settling without purification

Exact annihilation is not the only way to make a reusable instrument. This
second result uses an unknown static resonant linewidth

\[
 0<\kappa_-\le\kappa\le\kappa_+
\]

and an initial receiver mean occupation at most E. Its state and correlations
are otherwise arbitrary. The positive quantum force remains on throughout
[0,t0+L]. Discard the output over [0,t0] and integrate with w=1/sqrt(L) over
[t0,t0+L]. This requires neither an exact pole nor a fitted signed waveform.
Resonance and the correct force/homodyne quadrature remain separate supplied
control qualifications; a coarse linewidth promise does not establish them.

The free measured mode now contains an initial receiver component:

\[
 B=\zeta a(0)+B_{\rm fresh},\qquad
 \zeta=\frac{2e^{-\kappa t_0/2}(1-e^{-\kappa L/2})}
                  {\sqrt{\kappa L}}.                    \tag{21}
\]

B is canonical and the fresh part has quadrature variance (1-zeta²)v. Its
response kernel remains nonnegative. Consequently the same transport argument
holds even though B is initially correlated with the source: G_E commutes with
B as an operator, and the proof only requires an upper bound on B's initial tail.

The minimum shift is

\[
 \mu_\kappa=4g_-\sqrt{L/\kappa}
 \left[1-\frac{2e^{-\kappa t_0/2}(1-e^{-\kappa L/2})}
                 {\kappa L}\right].                    \tag{22}
\]

Conservative, box-uniform quantities are

\[
 \mu_0=4g_-\sqrt{L/\kappa_+}
       \left[1-\frac{2e^{-\kappa_-t_0/2}}{\kappa_-L}\right],
 \qquad \zeta_{\max}^2=\frac{4e^{-\kappa_-t_0}}{\kappa_-L}.
                                                               \tag{23}
\]

For a single oscillator of mean occupation E, any quadrature has second moment
at most

\[
 V_E=2E+1+2\sqrt{E(E+1)}.                                 \tag{24}
\]

This follows from |<a²>|<=sqrt(E(E+1)). The old receiver quadrature and fresh
field quadrature commute. For any 0<r<mu0 their initial tail therefore obeys a
union bound, leading to

\[
 \boxed{p_{\rm wrong}\le
 Q\!\left(\frac{\mu_0-r}{\sqrt v}\right)
 +\frac{\zeta_{\max}^2V_E}{r^2}.}                         \tag{25}
\]

This bound applies to the sum of the two sector error probabilities on the
whole input state. It does not require a mean-energy bound separately after
conditioning on an unlikely sector or record. The corresponding instrument
bound is energy-constrained, rather than an unconstrained diamond norm.

For a desired label bound p in (0,1), an explicit feasible sizing is

\[
 L\ge\max\left\{\frac4{\kappa_-},
     \frac{2\kappa_+v}{g_-^2}\log\frac1p\right\},
 \quad r=g_-\sqrt{L/\kappa_+},
\]

\[
 t_0\ge\frac1{\kappa_-}
 \left[\log\frac{8\kappa_+V_E}
 {p\kappa_-g_-^2L^2}\right]_+.                           \tag{26}
\]

Then mu0>=2r, and each term of (25) is at most p/2. In particular

\[
 T=t_0+L=O(\log(1/p)+\log(1+E))                          \tag{27}
\]

for fixed coarse receiver, gain and input-noise bounds. The source can keep
evolving noncommutatively during both intervals. The receiver need not approach
a pure state: thermal input and the continuing force may keep it populated.
The discarded interval is a real duration, not free preprocessing. Conventional
settling and integration can use precisely the same new guarantee.

## 8. The full instrument and actual-history composition

For the exact-filter theorem, the wrong-outcome effects are bounded by pI on
the whole retained auxiliary space. Let V_(r,alpha,s) be the physical coarse
outcome r and unobserved fine Kraus operators restricted to sector s.
Define a valid ideal comparison instrument by

\[
 \mathcal I_s(\rho)=\sum_{r,\alpha}
 (P_s\otimes V_{r,\alpha,s})\rho
 (P_s\otimes V_{r,\alpha,s})^\dagger,                    \tag{28}
\]

and report label s. This comparison is input-independent and completely
positive. Summing over s is trace preserving. Its auxiliary evolution is the
actual sector-conditioned channel, including all physical fine outcomes; it
does not demand a bath inverse, normalization depending on an input state,
or restoration of the receiver/source.

Relabeling the wrong diagonal output mass costs at most p in half trace norm.
For the off-diagonal sector blocks, Cauchy-Schwarz gives
sum_r ||C_r||_1 <= sqrt(p), including an arbitrary external reference.
Therefore

\[
 \frac12\|\mathcal M-\mathcal I\|_\diamond
 \le p+\sqrt p.                                          \tag{29}
\]

The same proof gives (29) on the input energy-constrained set for (25), using
the total wrong mass rather than a false operator inequality on all energies.
Thus a full-instrument tolerance epsilon can use p=O(epsilon²). A tiny label
error alone is never identified with the full instrument distance.

For a sequence of actual operations, telescope with actual prefixes and ideal
CPTP suffixes:

\[
 \mathcal M_n\cdots\mathcal M_1-
 \mathcal I_n\cdots\mathcal I_1
 =\sum_j\mathcal I_n\cdots\mathcal I_{j+1}
   (\mathcal M_j-\mathcal I_j)
   \mathcal M_{j-1}\cdots\mathcal M_1.                    \tag{30}
\]

The ideal future channels need not generate qualified physical source states.
Every error estimate is evaluated on a real preceding history. Adaptive
classical records can be included as registers. Fresh incident field per window
is required; retained source and receiver states are never assumed independent
between windows. With uniform per-window epsilon_j, the bound is sum epsilon_j,
plus actual gate/loading/holding/model errors.

### Warm energy envelope

For the one-mode model, N=a^dagger a obeys

\[
 \frac{d}{dt}\langle N\rangle
 \le-\kappa\langle N\rangle+\kappa n_b
       +2g_+\sqrt{\langle N\rangle}
 \le-\frac\kappa2\langle N\rangle+\kappa n_b+
             \frac{2g_+^2}{\kappa}.                      \tag{31}
\]

For fixed kappa the invariant mean-energy ceiling is therefore
max{E_initial,2n_b+4g_+²/kappa²}. On the coarse interval use kappa_- in the
floor. Departed-output homodyne does not change the nonselective retained mean
energy. Particular rare conditional histories can be hotter; they cannot be
given the averaged ceiling as a pathwise claim.

Actual weighted histories still suffice. In (25), V_E is increasing and
concave in E, and sqrt(p) is concave in p. Average energy and actual-prefix
telescoping therefore control the probability-weighted error budget for a
fixed schedule. Adaptive heating, intervening gates and loading add their real
energy injections. Arbitrary source energy, long-term maintenance of g_-, or
the ability to switch other noncommuting logical gates is not supplied by (31).

With vacuum input and the one-port convention, the mean emitted photon count is
\(\kappa\int_0^T\langle N(t)\rangle dt\), bounded by \(\kappa E_{\max}T\)
when that mean-energy envelope applies. Detector inefficiency, source pump
power, local-oscillator power and electronic processing are additional costs;
an emitted-photon bound does not determine the full electrical/optical work.
For thermal input one must distinguish incident flux from excess emitted flux.
Both intervals in the settling construction contribute physical exposure and
source work, including the part whose detector record is discarded.

For an actual implementation, the instrument budget has the form
\(p+\sqrt p+\epsilon_{\rm physical}+\epsilon_{\rm loading/gates/holding}\).
A Hamiltonian remainder R contributes a sufficient bound of order
\(\int\|R(t)\|dt/\hbar\) on its admitted domain, with escape and unobserved
jump histories accounted for separately. Longer observation lowers p but can
increase these physical terms. Their conservative sum is not a measured error
floor, and the ideal limit p to zero does not establish a device accuracy limit.

For a stable finite network, a positive Lyapunov matrix P satisfying
A^dagger P+PA=-I yields a similar affine drift for a^dagger P a. The bounded
force contributes at most 2g_+||P ell||sqrt(<N>), and all loss-input heating
must be included. This provides a route to a finite mean-energy envelope,
not a claim that every nonlinear network has one.

## 9. Finite precision, finite bandwidth and the useful failures

1. **An unknown continuum of poles cannot be annihilated exactly.** If a
   nonzero finite-duration w canceled exp(-lambda t) for an open interval of
   lambdas, its analytic Laplace transform would vanish identically. Exact
   all-state cancellation therefore needs known finite receiver structure.
   Equation (25) is a constructive alternative using a finite energy bound.
2. **Small pole mismatch is not uniformly small on unbounded receiver energy.**
   A residual coefficient zeta a(0) can be amplified by an arbitrary coherent
   displacement. In the executable, changing kappa from 1 to 1.01 leaves a
   coefficient about -0.004085 for the T=8 nominal annihilator. The statement
   is a continuity obstruction on an unbounded domain, not a physical error
   floor. Actual energy/tail bounds restore finite tolerances.
3. **An operator gain is not an operator pole.** A term W D_E a^dagger a with
   noncommuting source dynamics changes the receiver's free mode decomposition.
   It cannot be absorbed into a fixed finite collection of scalar poles merely
   by bounding the eigenvalues of D_E. A conservative finite-domain norm
   estimate is proportional to integral ||D_E|| N_domain dt, with its domain
   tails charged. That sufficient bound is not an impossibility theorem.
4. **Fresh field is an entropy resource.** A colored/reused field conditioned
   by the previous record need not provide the Gaussian conditional tail.
   White-noise, passive-line and detector assumptions require qualification.
5. **The rotating-frame Hamiltonian is a physical claim.** Real couplers have
   higher levels, finite bandwidth, counterrotating terms and source-dependent
   corrections. The theorem's lack of ||H_E|| does not establish a microscopic
   approximation uniformly for arbitrary source transition frequencies. Bounds
   on the local orbit of the actually coupled source operators, or direct
   microscopic propagator estimates, are required where those approximations
   are used. A large unrelated reservoir bandwidth need not be charged, but a
   resonant omitted source term cannot be called harmless.
   A first-moment energy bound suffices for (25), but does not by itself bound
   every higher-power microscopic correction, such as a Kerr term proportional
   to N squared. Such corrections require their actual higher moments, an
   invariant finite domain, or a tail argument. Detector saturation and output
   bandwidth also impose physical domains even when an ideal filter cancels an
   arbitrarily large initial operator exactly.
6. **A shared sum-of-Z force is not parity readout.** Resolving Z1+Z2 resolves
   states within the even parity sector. A native parity coupling, a genuinely
   sector-scalar exchange measurement, or actual coherent parity-mapping gates
   are needed. Their errors and times cannot be omitted.
7. **Readout reuse does not supply arbitrary gate reuse.** A residual Z a^dagger a
   coupling can be harmless during Z readout and harmful during an X rotation.
   The retained energy envelope does not replace a physical switch, an earned
   robust gate, or a bound on the entire gate interval.
8. **Finite prepared-state calibration does not certify an arbitrary-source
   lower bound.** Two gains can agree on every accessed source subspace and
   differ on an unvisited orthogonal subspace, with one having a dark zero-gain
   state there. The data are identical on those preparations. A uniform g_-
   therefore needs a structural operator argument or a justified accessible
   source domain in addition to statistical calibration. This theorem reduces
   the required information; it does not obtain that information by naming it.

## 10. Microscopic interfaces and equally informed comparisons

### Longitudinal superconducting readout

Didier, Bourassa and Blais proposed modulated longitudinal readout. Touzard et
al. implemented a pumped Josephson interaction with an output port, phase-
sensitive amplifier and digital weighting. Their effective model includes both
the desired conditional displacement and a residual dispersive pole:

\[
 H_{\rm eff}/\hbar=-\alpha q^{\dagger2}q^2/2
 +\zeta(t)(q^\dagger q-1/2)(c+c^\dagger)
 -\chi q^\dagger q\,c^\dagger c.                          \tag{32}
\]

Within its two-level domain, known scalar chi belongs in the finite-pole
construction, not in an arbitrarily assigned tiny error. The experiment reports
kappa=(100 ns)^-1, chi/2pi about 100 kHz, and a 750 ns readout plus 120 ns
depletion example. Its reported discrimination, assignment and QND metrics
are distinct. Calibration used 3x10^5 prepared-state trajectories. These facts
identify an actual operation stack; none certifies an arbitrary quantum gain
source, arbitrary receiver occupation or zero spectator coupling.

The new filter can augment this existing apparatus. Loading/preparation of the
data or measurement ancilla, pump generation, fresh incoming modes, amplifier
and oscillator phase stability, detector bandwidth, digitization, residual
couplings and subsequent gate isolation remain costs. A dedicated receiver
or a complete spectator-error sum is necessary. No numerical performance gain
over that experiment is inferred from the dimensionless checks below.

### Exchange and full-triplet readout

For two retained electron spins with spin-independent tunnelling and Coulomb
interaction, exchange has H_ex=J S1.S2=(J/2)SWAP-J/4. A genuine scalar exchange
modulation can therefore furnish the W=SWAP force while preserving all three
triplet orientations. Spin-rotation symmetry must hold over the admitted
charge/orbital domain, not only in a selected S--T0 calculation.

Bottcher et al. demonstrated parametric longitudinal coupling of a double-dot
spin qubit to a high-impedance resonator. Their effective force and dispersive
terms both arise from exchange curvature J''; that apparatus does not establish
full-triplet readout. A concrete charge-source warning is

\[
 J(\epsilon)=\frac{\epsilon+\sqrt{\epsilon^2+4t_c^2}}2,
 \quad J''(\epsilon)=\frac{2t_c^2}{(\epsilon^2+4t_c^2)^{3/2}}>0.
\]

Putting epsilon=epsilon0+xi tau_z with source Hamiltonian Omega tau_x gives a
positive noncommuting curvature gain. But the same curvature generally gives
an operator-valued receiver pole. The positive gain alone consequently does
not close the physical theorem's hypotheses. Charge-gap elimination, unwanted
exchange, gradient fields, spin-orbit terms, loading, isolation and return all
need their own finite-domain bounds.

### Ordinary receiver methods get the same information

For a known empty resonant receiver and constant g, the ordinary optimum matched
filter has signal norm squared

\[
 B(T)=T-\frac4\kappa(1-e^{-\kappa T/2})
        +\frac1\kappa(1-e^{-\kappa T}).                   \tag{33}
\]

The dirty-state annihilator has V(T) from (2), giving an amplitude-SNR ratio
sqrt(V/B). It tends to 1/2 for short T and to one for long T. At long times,
B=T-3/kappa+o(1), whereas V=T-4/kappa+o(1). Exact rejection has a real sensitivity
cost. Ordinary depletion or passive settling can be faster or cheaper when the
initial state and model are known. Conversely, both methods may adopt this
quantum-gain guarantee. Pole identification, coarse source bounds and model
qualification are never counted as acquired just by stating them.

Coherent hot-bus gates are also established machinery. Closing a known
phase-space trajectory does not automatically close one generated by a
noncommuting unknown gain. Readout is the consequence proved here, not a
coherent gate or coherent choice among programs.

## 11. Why the molecular route was not promoted into a device window

The paired audits in molecular/MOLECULAR_AUDIT.md and
pair_response/DERIVATION.md retain the full excited-atom label, electronic
J=1 and both nuclear spins. They correct two tempting truncations.
The 24-state calculation is complete within that declared atomic manifold;
it is not the full molecular electronic/vibrational spectrum.

For a fixed molecular axis z and real polarization x, the complete 24-state
response is nuclear-spin scalar through moments 0,1,2. The next moment contains
a triplet tensor with non-scalar norm 5 A_hf² |J_d|/6. Omitting the intermediate
electronic-antisymmetric nuclear-singlet sector incorrectly produces an earlier
Delta^-3 anisotropy. The required identity is
P F² P=(PFP)²+PF(I-P)FP.

Warm orbital motion adds A_hf[B,K]/Delta^4. An explicit two-configuration
48-state model gives [B,K]=-(3J_d k/2) sigma_y^(orb) I_tot,y. It preserves the
singlet/triplet label while entangling triplet information with motion. Thus
single-atom scalar response and a correct pair label do not prove pair opacity.
That witness admits two different interatomic axes. It is not an unavoidable
term in an exactly fixed-axis one-dimensional model. Establishing that narrower
contact domain is itself physical work; low transverse occupation alone does
not establish it. The fixed-axis pair tensor already survives separately.

Complete Franck-Condon closure also cancels the useful 1/Delta free-to-bound
amplitude between orthogonal entrance and final ground states. Useful transfer
starts as <f|(H_e-H_g)|i>/Delta². Combining isolated-level association strength
with complete-manifold cancellation is inconsistent. In the fixed-vacuum-
Stokes bad-cavity limit, useful absorption and the surviving spin disturbance
can both scale as Delta^-4; their ratio then stops improving with detuning.
Two independent classical Raman beams change that comparison and incur their
own power, recoil, holding and dissipative-outlet costs.

Final molecular parity supplies a real singlet-selective successful channel,
but unobserved optical histories and odd rotational molecular outputs still
need qualification. The complete-manifold pump/Stokes columns are generally
rank two, so an isolated-level STIRAP dark vector is not an exact full-manifold
dark vector. These are model-specific failures, not universal loss floors.

A source-unit correction is retained: Kitagawa et al. report the 171Yb ground
scattering length as -0.15(19) nm, not -0.15 Bohr radii. Earlier cold optical-loss
numbers do not thereby become warm one-dimensional cycle bounds. No earlier
conservative disturbance upper bound is called a measured error floor.

## 12. Executable evidence and its limits

Run `python p2_interface/output_mode_checks.py` from the workspace root with
NumPy and SciPy. It writes output_mode_results.json and checks:

- exact resonant filter normalization, zero startup operator coefficient,
  time-reversed fresh mode and nonnegative response;
- complete wrong-outcome effect matrices for a two-level quantum gain source,
  including noncommuting source frequencies up to 200 in kappa=1 units;
- common real filters for two known dispersive poles, the negative-kernel
  correction, and an actual noncommuting-source propagation with that kernel;
- a two-mode interacting receiver, including a slowly decaying mode;
- a pole-mismatch witness and equally informed empty-receiver comparison;
- feasible coarse-linewidth schedules from the analytic tail bound.

For kappa=1, delta=+/-0.0625, G in [0.3,0.5], fresh vacuum, the exact-pole
label bounds are about 2.73e-5 at T=20 and 1.49e-11 at T=40. These are label
bounds, not device errors or full-instrument bounds.

For only kappa in [0.8,1.2], G in [0.3,0.5], initial E<=10 and fresh vacuum,
one numerical feasible schedule from (25) has t0=24.0575 and L=22.3198,
total T=46.3773, label bound approximately 1e-6 and instrument half-distance
bound approximately 0.001001. The optimizer supplies a feasible witness, not a
certified global optimum. The complete waiting time is included.

All numerical results are ordinary floating-point diagnostics without certified
rounding enclosures. In the constant-source Fourier test, the finite pointer
quadrature produces a roughly 1.3e-5 discrepancy at a true tail of about 0.00729;
it is explicitly allowed as quadrature error, not evidence against or a numerical
certificate of the analytic inequality. Source effect completeness is checked
independently. The mathematical claims rest on the identities and current proof.
The source propagation uses an exact finite sequence of alternating rotations
and translations. The inequality applies to that sequence itself; the check is
not a certified convergence study of a high-frequency continuous Hamiltonian.

The molecular audit programs preserve the full matrices, omitted-sector
correction, warm commutator, closure sum and failed dark-state/polarization
routes separately.

## 13. Sources and continuity

- Astra N1419, read at commit
  `ceaef853be46099e0e3446d0778160f26ef962fe` in
  `harjassand/astra-research-knowledge`. Accessible governing source:
  [FINAL_NATIVE_PREFIX.txt](https://github.com/harjassand/astra-research-knowledge/blob/ceaef853be46099e0e3446d0778160f26ef962fe/research/2026-10-30-continuous-bell-buffer-force-and-planar-inference/source/p2/FINAL_NATIVE_PREFIX.txt).
  This supplies the positive operator-force support principle and full
  sector-instrument distinction. It is distinct from the earlier signed-spin
  native handles. Missing original raw derivations were not presumed available.
- Gardiner and Collett, [PRA 31, 3761 (1985)](https://doi.org/10.1103/PhysRevA.31.3761),
  input-output quantum stochastic dynamics.
- Didier, Bourassa and Blais,
  [PRL 115, 203601 (2015)](https://doi.org/10.1103/PhysRevLett.115.203601),
  modulated longitudinal readout proposal.
- Touzard et al., [PRL 122, 080502 (2019)](https://doi.org/10.1103/PhysRevLett.122.080502),
  [accessible accepted paper](https://link.aps.org/accepted/10.1103/PhysRevLett.122.080502),
  actual pumped conditional-displacement readout and detector stack.
- Bottcher et al., [Nature Communications 13, 4773 (2022)](https://doi.org/10.1038/s41467-022-32236-w),
  [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC9378792/),
  measured longitudinal spin-resonator coupling with simultaneous dispersive term.
- Levitt and Guta, [PRA 95, 033825 (2017)](https://doi.org/10.1103/PhysRevA.95.033825),
  quantum linear-system identification and observable transfer functions.
- Gambetta et al., [PRA 76, 012325 (2007)](https://doi.org/10.1103/PhysRevA.76.012325),
  ordinary optimal QND readout filtering and relaxation tradeoffs.
- Reiter and Sorensen, [PRA 85, 032111 (2012)](https://arxiv.org/abs/1112.2806),
  separate effective Hamiltonian and each physical decay operator.
- Kampschulte and Hecker Denschlag,
  [Cavity-controlled ultracold chemistry](https://arxiv.org/abs/1803.10004),
  real association/output machinery in its selected cold-state model.
- Kitagawa et al., [PRA 77, 012719 (2008)](https://arxiv.org/abs/0708.0752),
  ground molecular spectroscopy and the corrected scattering-length unit.

The substantive new combination is the quantum-gain transport theorem for a
measured output mode, its signed-kernel extension to interacting receivers, and
the coarse-calibration energy/history guarantee. Linear filtering, passive
settling, longitudinal hardware and the prior positive-force principle receive
their existing credit. The remaining physical calculation is to qualify an
actual source/coupler/receiver over one common energy domain, especially any
source-dependent pole and noncommuting gate intervals. It is not legitimate to
declare a device window by choosing those residuals numerically small.
