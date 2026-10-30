# A continuous nonlinear material that receives the passive-metered spatial program

30 October 2026. Root's next construction. This supplies a concrete source
connection for the passive native recorder and the metered elastic carrier,
rather than identifying either with a two-dimensional exclusion sensor.
The physical-mechanism proof and root metered-cell proof are dependencies.
Their original exact versions and actual reviews remain preserved.

## 1. Actual native material and the consequence

There are N fixed horizontal rows, each with N underdamped native particles
on a circle of circumference N. Let X_y be the vector of lifted positions,
V_y their velocities, and let the actual unknown smooth potential satisfy

\[
 U_N(X_1+c_1\mathbf1,\ldots,X_N+c_N\mathbf1)=U_N(X_1,\ldots,X_N)
                                                               \tag{1}
\]

for independent row translations. The potential can be nonharmonic and can
couple relative coordinates in different rows. Its actual interactions,
spatial range and force bounds belong to the native material; (1) does not
grant an instantaneous nonlocal force. A local row potential is a concrete
subclass. Arbitrary forces between particles in different translating rows
do not satisfy (1) automatically.

Each row has an unknown common friction gamma_y in a fixed positive bounded
interval. Its independent thermal sources and actual force port obey

\[
 dX_{y,l}=V_{y,l}ds,\quad
 dV_{y,l}=(-\partial_{y,l}U_N-\gamma_yV_{y,l}+F_y(s/N²)/N)ds
                                   +\sqrt{2\gamma_y}\,dB_{y,l}.
                                                               \tag{2}
\]

The native load F_y is prescribed, bounded and sufficiently regular on
macroscopic time. It may be selected by an admissible old record. A later
native forcing policy that observes hidden probe noise is not included.
All compared native experiments have the same load and initial law.
Start with a warranted canonical native law, or the stated native warm
ceiling, and fresh independent Gaussian passive probes. Producing the
canonical law of an unknown interaction is a separate preparation resource.

The goal is an actual composite shear-current law while preserving the
native density/current **large-deviation law at speed N²**. Unlike the
isolated native source in the original theorem, passive measurement here
changes finite-system native paths. The same-rate assertion is the earned
comparison; it is not microscopic identity or a full-record TV result.

## 2. The source bound is exact despite nonlinear relative dynamics

Define P_y=sum_l V_{y,l}, A_y=sum_l[X_{y,l}(s)-X_{y,l}(0)]. Equation (1)
cancels every relative force, so under the unmetered reference,

\[
 dP_y=(-\gamma_yP_y+F_y(s/N²))ds+\sqrt{2\gamma_yN}\,dB_y,
 \qquad dA_y=P_y ds.                                        \tag{3}
\]

Therefore the true integrated current has the exact decomposition

\[
 A_y(s)+\frac{P_y(s)-P_y(0)}{\gamma_y}
   =\int_0^s\frac{F_y(u/N²)}{\gamma_y}du
                            +\sqrt{2N/\gamma_y}\,B_y(s).    \tag{4}
\]

The proof does not treat instantaneous P_y as a uniformly bounded current
drift. At s=N²t, the corrected h_y=A_y/N² has bounded drift and Brownian
bracket 2/(gamma_y N). Its endpoint correction has Gaussian scale N^(-3/2).
Uniform OU stability and a time-mesh estimate imply

\[
 \Pr\{\max_y\sup_{t\le T}
 |[P_y(N²t)-P_y(0)]/(\gamma_yN²)|>C/K_N\}
 \le\operatorname{poly}(N)
                    \exp[C_0N²-cN³/K_N²].                  \tag{5}
\]

The same estimate holds for a bounded prescribed load from the centered
initializer: its aggregate mean is O(1). Initial warm density changes only
the indicated prefactor. No native mixing rate enters (3)--(5).

Apply the actual smoothing S_N and specified nonlinear psi to the corrected
current for the analytic comparison. Bounded derivatives make its drift
bounded and its vector bracket O(1/N); Ito's trace correction is O(1/N).
Its continuous martingale satisfies the directional sub-Gaussian bound
without the bounded-jump cutoff. Replacing corrected by actual h changes
the target by at most a constant times (5), by the Schur bound on S_N and
the Lipschitz bound on psi. The actual controller never observes or
subtracts P_y/gamma_y. This proves the needed source receiver for the main
joint tracking argument.

## 3. The passive native meter also receives the loaded experiment

Attach the physical follower of `PASSIVE_FINITE_RESPONSE_DISPLACEMENT_RECORDER.md`
to each native coordinate, with common g_N and common a_y within each row.
The extra native force is -g_N Y_{y,l}; its actual pointer velocity is
P^{ptr}_{y,l}, with
dY=(g_N V-P^{ptr})ds and dP^{ptr}=(Y-a_yP^{ptr})ds+sqrt(2a_y)dW.
All bath sources are joint independent at their stated ports. Choose
g_N²=H_N/N², H_N=log(N+2), and K_N=log log(N+e^e).

The rowwise relative system remains autonomous: uniform load disappears
under the mean-zero projection. Its invariant law is the canonical native
relative law times independent Gaussian relative probe coordinates. The
three aggregate coordinates (native velocity, extension, pointer velocity)
have a stable linear Gaussian equation, driven by the O(1) total row load.
The corresponding per-particle mean is O(1/N), uniformly over physical
time. Stability follows at g=0 from the native friction and the damped
probe oscillator, and persists uniformly for sufficiently small g.

Consequently, under both metered and unmetered native laws, the full
velocity field is a canonical Gaussian marginal plus a deterministic mean
of squared norm O(1). Under a native warm initializer the path density
ceiling is imposed once. In particular the kinetic exponential-moment
bound used in the passive recorder's two-sided likelihood proof holds
uniformly for this prescribed weak load. The observation equation simply
subtracts the same known functional native load along with the native
force; the recorder does not compute either subtraction.

This supplies the previously separate driven moment premise. The same
native-marginal comparison therefore transfers every warranted native
speed-N² LDP under the actual load, with unchanged rate. Fresh conditional
Gaussian probes remain essential; arbitrary conditioning on their future
readouts does not retain this likelihood statement.

## 4. Receiving the actual pointer-controlled auxiliary layer

Use the extensive elastic carrier layer, with the actual four-coordinate
finite cell in `METERED_FINITE_CELL_AND_SPATIAL_ERROR.md`. Its native and
auxiliary pointer readings supply their respective integrated displacements.
The native pointer group is a fixed row, so its attribution is literal.
Every auxiliary charged displacement, including during the bath phase,
is counted by its physical pointer up to the endpoint-extension error.

The intrinsic normalized pointer errors obey a joint spatial norm bound
with exponent N²H_N and a separate cap-tail bound with exponent
N^(5/2)H_N/K_N². Since H_N/K_N²->infinity, their joint C/K_N envelope is
super-volume, although the old maximum-row envelope is not. Extra final
reader, timestamp, evaluation and delivery errors must satisfy the actual
joint-error/cap contract, and deterministic bias must be O(1/K_N) to retain
the displayed order-volume carrier work. No per-device calibration event
of fixed probability is promoted to an unconditional rare-law guarantee.

The receiving proof has three distinct steps. First apply (3)--(5) to the
ideal current governor on the unmetered native path. Second transfer that
super-volume event through the native-marginal likelihood comparison,
extending only by the independent auxiliary primitive sources. Third compare
the actual pointer-driven governor with that ideal governor on the same
native path and auxiliary primitives. The deterministic stable-loop
convolution bounds the extra joint observation error; its tiny state-
corrector difference is absorbed as described in the metered-cell note.
This does not condition a source martingale on successful future readings
or pretend that the full probe-record likelihood has the small marginal cost.

If the unmetered native path has a good volume-speed LDP with actual rate I,
the measured composite consequently has the physical pushforward rate of

\[
 (\rho,W)\longmapsto
 \left(\rho+1,
 W+[\psi(y,t,(S h)(y,t))-h(y,t)]e_x\right),\qquad
 h=\int_0^1W_x\,dx.                                        \tag{6}
\]

The auxiliary current can be retained as its actual displayed field. The
native density-path rate is unchanged after accounting for the added
charged background. This assertion is for fixed-row continuous materials;
it does not supply a passive reader for the original two-dimensional
exclusion example. A native LDP is not proved for every unknown potential.
Independent free row particles provide a concrete receiving subclass; the
source and measurement comparisons allow nonlinear relative potentials
whenever their own actual native LDP is warranted.

## 5. Sustained load and the work that is actually counted

For a constant native row load F_y/N, the metered aggregate mean velocities
relax to

\[
 \overline V_{y,l}=\frac{F_y}{N(\gamma_y+a_yg_N²)},\quad
 \overline P^{ptr}_{y,l}=g_N\overline V_{y,l},\quad
 \overline Y_{y,l}=a_yg_N\overline V_{y,l}.                   \tag{7}
\]

This result does not depend on the nonlinear relative potential. Centered
canonical initialization is sufficient: the mean transient lasts O(1)
physical time, uniformly in N. On horizon N²T, actual native source work is

\[
 EW_{native}=TN\sum_y\frac{F_y²}{\gamma_y+a_yg_N²}+O(1)
                  =O(N²),                                \tag{8}
\]

and the probe bath's excess loaded heat is

\[
 EQ_{probe}^{excess}
 =TNg_N²\sum_y\frac{a_yF_y²}{(\gamma_y+a_yg_N²)²}+O(1)
                  =O(H_N).                               \tag{9}
\]

The stationary covariance contribution is thermal equilibrium exchange,
not an uncounted active drive. The equality with the stated bounded
transient uses the exact canonical relative initializer; a warm initial
state has its own excess energy and heat. Equations (8)--(9) therefore
do not assert that arbitrary nonequilibrium preparation is free.

The controlled auxiliary layer retains its O(N²+NK_N) signed mean force-work
bound, with its actual metered-cell mobility. The passive native follower
has no continuously powered cancellation channel. This removes the N^6
input-work failure of the rejected active recorder model at the reaction
core. It does not establish an O(N²) total instrument budget: charged-
layer preparation, growing stiffness and rare-tail force range, fresh-bath
capacity, pointer manufacture/range, readers, communication, clocking,
logical reliability and retirement remain in the complete ledger.

## 6. Scientific decision and remaining boundary

The completed mechanism is the conjunction of a physical stiff transport
layer, passive displacement memory, native-marginal action preservation and
a controller that asks for the joint precision the apparatus naturally
supplies. The ordinary governor and ordinary follower are available to an
equally informed controller. Their use is part of the contribution rather
than a claimed computational separation.

The reason this construction is stronger than another ring fixture is that
it specifies how a nonlinear material can be measured and coupled while
retaining its volume-scale law, with no native mixing or force identification
needed in the metrology proof. It remains a theoretical architecture with
an explicit reader/reliability boundary. Actual pointer export can disturb
the probe; its force/noise must be included before a complete physical
capability is claimed. Arbitrary spatial circulation, finite-system
noninvasiveness, full microscopic record preservation, a practical speedup,
historical priority and a total-work advantage remain unestablished.
