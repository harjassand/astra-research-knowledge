# Sparse internal loads prepare native profiles without learning the kinetics

30 October 2026. Constructed independently by the existing Astra P1
record-geometry role, before receiving a preferred root mechanism.
This changes the task from preserving a native density law to preparing a
specified nonuniform native material. Earlier continuation files are unchanged.

## 1. Result, actual task, and ordinary predecessor

A single-file material contains M hard particles in length N, with
M/N tending to an interior density rho_bar. A sparse set of tagged particles
receives specified opposed forces. The intervening native particles are
unforced. An anchor fixes a laboratory origin; without it, the result is a
material-frame profile with a fluctuating translation.

The construction programs any smooth target density rho_*(x), bounded
away from zero and close packing and with integral rho_bar. With R_N
internal tags, R_N increasing and R_N=o(N), the equilibrium profile error
is O(1/R_N+R_N/N), plus ordinary order-N equilibrium fluctuations.
For a Lipschitz target and R_N=N^(1/3), the largest applied tag force is
O(N^(-1/3)); the total absolute force remains O(1).

The stationary law does not contain the unknown reciprocal kinetic
prefactors. A continuous hard-rod version has a direct polynomial
preparation bound under an actual uniformly elliptic thermal mobility
interface. Preparing and releasing the profile costs order N reversible
work, matching its native excess free energy. Keeping the exact loaded
equilibrium requires no mean ongoing force work. This last statement
does not price absolute thermal back-and-forth work without energy recovery.

The mechanism is ordinary internal piston/pressure control. In particular,
Bénichou, Démery and Poncet explicitly derived the single-file pressure
jump law and the response to several driven probes:
https://arxiv.org/html/1707.06085 and
https://doi.org/10.1103/PhysRevLett.120.070601.
Their pressure interpretation directly precedes this mechanism. Evans's
particle-disordered exclusion solution already supplies the product-gap
stationary representation:
https://arxiv.org/html/cond-mat/9606036.

The constructive addition in this note is an explicit sparse inverse
profile program, with its actual force port, finite preparation and
release ledger, and a direct comparison with boundary and internal
pistons. No priority for a new generic equilibrium-engineering principle
is claimed. Internal pistons given identical forces and access tie the
construction.

## 2. Exact bounded-rate lattice operation

First use a finite model whose actual native calls have bounded rates.
Label the particles 0,...,M-1 in their conserved cyclic order. Let g_i
be the number of holes after particle i; sum_i g_i=H=N-M. Particle 0
may be pinned, in which case g still ranges over all compositions of H.

For i=1,...,M-1, a right step of particle i transfers one hole from g_i
to g_(i-1). Its reverse is the corresponding left step. Give that paired
edge arbitrary unknown reciprocal prefactor c_e(h), bounded between
positive constants. Here h may be a frozen microscopic device variable.
The actually supplied force ratio is

\[
\frac{q_i^+(g,h)}{q_i^-(g-e_i+e_{i-1},h)}
    =e^{F_i}=\frac{w_{i-1}}{w_i},\qquad w_i>0.                 \tag{1}
\]

For example q_i^+=c_e w_(i-1)/w_i and q_i^-=c_e realize this ratio.
At w_(i-1)=w_i the particle retains its ordinary symmetric native rates.
An exponential symmetric load sharing is another valid supplier.
Equation (1) is an actual local-detailed-balance actuator interface.
It is not inferred from an equilibrium distribution or from unmeasured
kinetics. Only particles at changes in w need a nonzero force.

Then the exact conditional stationary law is

\[
\pi_w(g)=Z_H(w)^{-1}\prod_{i=0}^{M-1}w_i^{g_i},
\qquad
Z_H(w)=\sum_{\sum_i n_i=H}\prod_iw_i^{n_i}.                   \tag{2}
\]

Indeed a right step has probability ratio w_(i-1)/w_i, exactly the
forward/reverse rate ratio. Every marked edge is in detailed balance.
Unknown state-dependent reciprocal conductances are allowed; kinetic
coefficients need not be inferred or identical.

For an unpinned ring include i=0 modulo M and choose

\[
F_i=\log w_{i-1}-\log w_i,\qquad \sum_iF_i=0.                 \tag{3}
\]

There is then a real conservative energy on the fixed-order sector:

\[
E_w(g)=-\sum_i g_i\log w_i
       =-\sum_iF_iX_i+\text{constant}.                       \tag{4}
\]

The lifted positions X_i preserve their order. Adding a complete common
winding does not change (4), because the forces sum to zero. With an
anchor, the origin is fixed and every tag has a bounded positional range.
The anchor's reaction does no displacement work.

This topology is load bearing. If particles can overtake, independently
winding a driven label generally restores a nonzero affinity cycle.
The loaded equilibrium need not survive that changed operation.

### Accessibility and a finite universal waiting bound

With one pinned particle, all remaining positive-rate transitions move
holes along a connected path of M gap sites. Every composition is
accessible. A path between two compositions needs at most
D=H(M-1) one-hole moves. Thus the gap process is irreducible for each h.

If w_min<=w_i<=w_max and q_e>=q_min, then

\[
\pi_{\min}\ge
\binom{H+M-1}{M-1}^{-1}(w_{\min}/w_{\max})^H.                \tag{5}
\]

An elementary canonical-path bound gives

\[
\operatorname{gap}\ge q_{\min}\pi_{\min}/D.                 \tag{6}
\]

For completeness, expand Var_pi f as half the sum of
pi(x)pi(y)[f(x)-f(y)]², telescope along a chosen path of length at most D,
and apply Cauchy--Schwarz. The load of any edge is at most one, while
its conductance is at least q_min pi_min. This proves (6), with a
possibly inessential factor two absorbed by weakening the constant.

Consequently the time

\[
t\ge\frac{D}{q_{\min}\pi_{\min}}
 \left[\frac12\log(1/\pi_{\min})+\log(1/\varepsilon)\right]   \tag{7}
\]

is a conservative uniform total-variation preparation bound, up to a
fixed factor. It is generally exponential in N and is not an efficiency
claim. It does make preparation concrete under this finite-rate interface.
Constant-rate homogeneous zero-range dynamics has much sharper known
diffusive relaxation bounds; Morris's result cannot simply be imported
for arbitrary tilted conductances:
https://arxiv.org/pdf/math/0405161.

All rates can depend on the fixed hidden h without changing (2). Uniform
bounds give the same waiting time conditional on any h and retained old
record. Hidden h is neither reset nor copied. If h instead alters the
conditional equilibrium or is an evolving inaccessible variable, that
is a different supplier and (7) is not asserted for it.

## 3. Explicit inverse profile program

Partition the desired spatial interval [0,1] into R cells of lengths
ell_j. Let M_j be positive integers summing to M, chosen so that

\[
\frac{M_j}{N}\approx\int_{\text{cell }j}\rho_*(x)\,dx,\qquad
\rho_j=\frac{M_j}{N\ell_j}.                                \tag{8}
\]

Place tags at the corresponding cumulative particle labels. There are
M_j gap variables in block j. Assign

\[
w_i=w_j=1-\rho_j
\quad\hbox{for every gap in block }j.                       \tag{9}
\]

Let independent geometric G_i have law
Pr(G_i=n)=(1-w_i)w_i^n. Their expected total is exactly H:

\[
\sum_i E G_i
 =\sum_j M_j\frac{1-\rho_j}{\rho_j}
 =\sum_j(N\ell_j-M_j)=N-M.                                 \tag{10}
\]

Conditioning these variables on sum G_i=H gives exactly (2).
The mean unconditioned physical length of block j is
M_j+sum E G_i=N ell_j. Thus neither a kinetic model nor a fitted
transport coefficient enters the inverse design.

For equal spatial cells and a Lipschitz interior target,

\[
\|\rho_{\rm step}-\rho_*\|_\infty
\le C(1/R+R/N),\qquad
|F_j|\le C(1/R+R/N).                                      \tag{11}
\]

The first estimate is the cell-average approximation plus count rounding.
The second follows from the bounded derivative of log(1-rho) on the
interior-density interval. The total absolute force is bounded by a
constant times the target's total variation, plus O(R²/N). Selecting
R=N^(1/3) gives O(1) total force and vanishing force per tag. The tag
population itself contributes at most R/N to normalized density if the
tags are additional physical particles rather than selected native ones.

### Equilibrium concentration

All geometric parameters remain in a compact subinterval of (0,1).
Their variances and small exponential moments are uniformly bounded.
A maximal Bernstein bound for their partial sums gives

\[
\Pr\left\{\max_k\left|
  \sum_{i<k}(G_i-EG_i)\right|>\epsilon N\right\}
\le {\rm poly}(N)e^{-c_\epsilon N}.                        \tag{12}
\]

The probability that their total equals its integer mean H is at least
c/sqrt(N). One direct justification is Fourier inversion: the characteristic
functions of the geometric laws have a uniform quadratic expansion near
zero, uniformly bounded third moments, and modulus strictly below one
away from zero. Splitting the integral into the central N^(-1/2) range,
an intermediate Gaussian range and the remaining compact range yields
the uniform local central-limit lower bound.

Conditioning therefore changes the polynomial factor in (12), not its
order-N exponent. Each particle's anchored position is a partial gap sum
plus its hard-core label displacement. If all partial sums differ from
their prescribed means by at most epsilon N, the empirical density differs
in bounded-Lipschitz distance by at most epsilon plus the deterministic
error in (11). Hence

\[
\pi_w\{d_{\rm BL}(\rho_N,\rho_*dx)>
            \epsilon+C(1/R+R/N)\}
\le {\rm poly}(N)e^{-c_\epsilon N}.                        \tag{13}
\]

The number of particles between the tags is actual initial structure.
It must be supplied by counted assembly or by an actual recorded rank
assignment. Selecting an arbitrary collection of unlabeled particles
does not silently supply the M_j. Initial tag positions may be unknown
and are allowed to equilibrate.

### A finite illustrative pattern

At mean density 1/2, four equal spatial cells can alternate density
3/4 and 1/4. The corresponding label fractions alternate 3/8 and 1/8.
The w values alternate 1/4 and 3/4, and the tag forces alternate
+log 3 and -log 3. Four loaded tags, or three internal tags and the
anchor reaction, produce two separated dense bands and two dilute bands.
The actual native particles form the bands; they are not reclassified
auxiliary current or a measured-field overlay.

## 4. Literal continuous pressure supplier and a polynomial preparation bound

The same operation has a direct ordinary mechanical realization. Consider
unit-length hard rods in a fixed one-dimensional channel of length N,
with one anchored rod, no passing, and a thermal fluid. Native rods have
no applied body force. Selected tagged rods receive constant forces F_i.
The unknown reciprocal mobility may contain configuration-dependent
hydrodynamic interactions.

Write x_i=X_i-i for the free-space ordered coordinates. Their convex
domain is

\[
\mathcal C=\{0\le x_1\le\cdots\le x_{M-1}\le H\}.
\]

For positive numbers p_i define the actual potential

\[
E_p(g)=\sum_i p_i g_i,\qquad
F_i=p_i-p_{i-1}.                                         \tag{14}
\]

Here F_i=P_right-P_left is the force balancing the two gas pressures.
The positional equilibrium is proportional to exp(-E_p) on the gap
simplex. It is the law of independent exponential gaps with rates p_i,
conditioned on their sum H. Choose, in block j,

\[
p_i=p_j=\frac{\rho_j}{1-\rho_j}.                           \tag{15}
\]

Their unconditioned means then satisfy exactly the same length constraint
(10). The partial-sum proof gives (13) with exponential in place of
geometric gaps. Here conditioning on the exact sum uses its density,
not a positive-probability event. That density at its mean is at least
c/sqrt(N) by the continuous local central limit argument. For a partial
sum of fewer than M variables, the remaining sum has density at most
p_max, since convolution cannot increase the largest single exponential
density. Its conditional tail is therefore at most C sqrt(N) times
the unconditional Bernstein tail. The final partial sum is fixed by
the constraint. This proves the continuous version of (13).
This is the ordinary hard-rod pressure law, in units
k_B T=rod length=1. Tonks's primary phase-integral/equation-of-state
paper is https://doi.org/10.1103/PhysRev.50.955; the pressure balance for
driven single-file probes is explicitly developed by Bénichou et al.
The lattice and continuous equations of state are different and have
not been interchanged.

One possible force port is a prescribed signed buoyant load on each
tag in a vertical channel, while the native particles are neutrally
buoyant. A common change in the imposed body field can ramp all loads
together. This is an ideal hard-rod/thermal-fluid model: actual extra
electrostatic, magnetic, surface or fluid interactions must be included
if a different selective-force implementation introduces them. A tag's
material coupling encodes the force; a scalar field control alone cannot
reprogram an arbitrary new profile without changing those couplings.

For a precise receiving theorem assume the actually executed positional
generator, conditional on frozen h, is

\[
L_{\lambda,h}f
 =e^{\lambda E_p}\nabla\!\cdot
   (e^{-\lambda E_p}\mathsf M_h(x,\lambda)\nabla f),\qquad
\mathsf M_h\succeq m_- I,\quad m_->0,                      \tag{16}
\]

with reflecting no-flux boundaries and well-posed dynamics. Symmetric
mobility and its thermal drift/noise are part of this supplier. The
controller does not estimate the matrix. A nonequilibrium friction
law or a noiseless damper would not have (16).

Let D be the diameter of C; D²<=H²(M-1). The gap is bounded uniformly
over all linear tag forces and all h by

\[
\operatorname{gap}(L_{\lambda,h})
 \ge\frac{2m_-}{eD^2}.                                   \tag{17}
\]

Proof: add q(x)=|x-x_0|²/D² to the linear potential. The resulting
measure has Hessian at least 2I/D² on the convex domain, and hence
Poincaré constant at most D²/2 by the Brascamp--Lieb inequality.
Approximate the hard reflecting walls by convex barriers if needed.
Since 0<=q<=1, the ratio between the original and auxiliary densities
has oscillation factor at most e. Comparing variances by minimizing
over their additive constant gives a Poincaré constant at most eD²/2
for the original measure. The actual Dirichlet form dominates
m_- times the Euclidean gradient form. This proves (17).

For a supplied initial density ceiling B relative to the desired loaded
equilibrium,

\[
\|\nu e^{tL_{\lambda,h}}-\pi_\lambda\|_{\rm TV}
\le\tfrac12\sqrt{B-1}\,
   \exp[-2m_-t/(eD^2)].                                  \tag{18}
\]

If the native initial law has ceiling B_0 relative to the unloaded
canonical law, then B<=B_0 exp(osc E_p), and osc E_p=O(N) for the
interior-profile class. Thus a uniform preparation time is

\[
t=O\!\left(N^3[N+\log B_0+\log(1/\varepsilon)]/m_-\right).
                                                               \tag{19}
\]

This is polynomial and deliberately conservative, not a sharp relaxation
claim. It applies to the continuous thermal interface (16). It has not
been transferred to the earlier bounded-rate lattice chain or to a
finite-bandwidth inertial apparatus. The actual diffusivity lower bound,
thermal bath, source initialization and wall/link forces remain resources.

## 5. Actual preparation, holding, and release work

The loaded profile contains order-N native free energy. Sparse hardware
does not make that resource disappear.

For either model let E be its displayed potential, pi_0 the unloaded
canonical law, and pi_lambda proportional to exp(-lambda E) pi_0.
Keep the same hard-core sector, anchor and physical labels. A constant
loaded force has exact displacement-work identity

\[
W_{\rm motion}(0,t)
 =\sum_i F_i[X_i(t)-X_i(0)]=E(g(0))-E(g(t)).                \tag{20}
\]

At the loaded equilibrium its mean is zero over every fixed interval.
Its absolute variation need not vanish. A rectifying actuator that
pays for every forward or backward motion is not the regenerative
force port represented by (20). Anchoring bounds each tag's travel
and makes its finite energy capacity explicit; an unanchored realization
needs a real way to share or store opposing winding work.

For the reversible preparation ledger, change the physical potential
from 0 to E quasistatically. An ideal parameter quench back to zero has
the two mean contributions below. Do not double count force work and
field-energy work. Pathwise,

\[
W_{\rm motion}=-\int\lambda\,dE
 =-\Delta(\lambda E)+\int E\,d\lambda.                    \tag{20a}
\]

For a complete lambda=0 to lambda=0 cycle, the actual net force work
equals the parameter-work ledger. Boundary energy must be retained for
an incomplete cycle. A literal zero-time change is not granted as a
device operation; a finite-duration replacement is proved below.

\[
W_{\rm on}^{\rm rev}=-\log E_{\pi_0}e^{-E},\qquad
W_{\rm off}=-E_{\pi_1}E.
\]

Their sum is exactly

\[
W_{\rm prepare+release}^{\rm rev}
  =D(\pi_1\|\pi_0).                                      \tag{21}
\]

The final bare native system has law pi_1, but is no longer stationary
after release. Allowing it to relax dissipates that free energy; an
appropriate reversible reverse protocol can recover it. Invariance of
the loaded system is not a claim of a permanently unloaded gradient.

A finite loading schedule makes the preparation concrete. Use J steps
lambda_j=j/J. At each step change lambda at the current configuration,
then wait long enough for the actual law to be within delta of
pi_(lambda_j). Apply (7) for the finite-rate model, or (18) for the
continuous model. During each parameter change, count E delta_lambda.
Since

\[
\frac{d}{d\lambda}E_{\pi_\lambda}E
   =-\operatorname{Var}_{\pi_\lambda}E\le0,
\]

the excess of the left Riemann sum over the reversible integral is at
most osc(E)/J=O(N/J). Imperfect equilibration adds at most O(N delta)
to the entire mean work, including the final release. Thus

\[
E W_{\rm complete}
 =D(\pi_1\|\pi_0)+O(N/J+N\delta),                           \tag{22}
\]

in the ideal final-quench limit. A one-time preparation of pi_0 is still
required; its cost is not erased by (22). The source is a real
Hamiltonian/load port with paid engagement and energy recovery, not an
ideal probability reweighting.

### Fixed-duration release, without a global position clamp

There is an especially useful actual release for the smooth sparse
program. Since R=N^(1/3) and |F_j|=O(1/R),

\[
\sum_j F_j^2=O(1/R).                                      \tag{22a}
\]

Keep the actual mobility matrix unchanged as the force is turned off,
and assume also M_h<=m_+ I. Smoothly lower lambda from one to zero over
a fixed physical interval tau. Compare this actual law with the
mathematical reference that keeps lambda=1, both started from pi_1.
Their diffusion and reflection interface is identical. The change in
drift is (1-lambda) M_h grad E. Girsanov therefore gives

\[
D(Q_{\rm off}\|Q_{\rm hold})
\le\frac{m_+\tau}{4}\sum_jF_j^2=O(\tau/R).                 \tag{22b}
\]

The same estimate holds for the bounded-rate lattice supplier
q_i^+=c_e exp(lambda F_i), q_i^-=c_e with unchanged reciprocal c_e:
the standard jump likelihood has per-edge relative entropy bounded
by C F_i², and only the tags change rates. Mere knowledge of the
forward/reverse ratios, without this actual compatibility of the
force operations, would not supply either path comparison.

Pinsker and stationarity of the held reference imply that the entire
release path law, and in particular its final state, differ by at most
C sqrt(tau/R). With a delta-accurate prepared start, the final error
is at most delta+C sqrt(tau/R). No position sensor or all-particle clamp
is used. A fixed-duration smooth force ramp has finite temporal
bandwidth; it is not an instantaneous intervention.

Because osc E=O(N), replacing the ideal removal by this actual ramp
changes its mean parameter work by at most
C N[delta+sqrt(tau/R)]. Thus the full executed protocol satisfies

\[
E W_{\rm complete}
=D(\pi_1\|\pi_0)
 +O\!\left(\frac NJ+N\delta+N\sqrt{\tau/R}\right),\qquad
\|\nu_{\rm final}-\pi_1\|_{\rm TV}
\le\delta+C\sqrt{\tau/R}.                                 \tag{22c}
\]

For fixed tau and R,J tending to infinity this attains the order-N
free-energy cost with o(N) excess. Unknown fixed reciprocal kinetics
are retained. The release statement compares actual laws, not a
copied microscopic specimen. A fixed number of order-one force tags
does not have (22a); its ideal release requires a sufficiently fast
actual ramp or an independently warranted holding operation.

The nominal loading increments can also be replaced by smooth ramps
of the same fixed duration tau. Their maximum force difference from
the preceding held equilibrium is F/J, so the same calculation bounds
their path error by C sqrt(tau)/(J sqrt(R)). Summing the resulting
work errors adds only O(N sqrt(tau)/(J sqrt(R))) to (22c).
After each ramp apply the stated finite waiting bound. For bounded
initial densities, the forward equation for the density relative to
pi_lambda shows that its ceiling grows by at most
exp(osc(E) times the total variation of lambda). Thus a ceiling
B_0 exp(CN) suffices for all the monotone loading stages, not a
fresh unsupported initializer at every step. This supplies a wholly
finite schedule at the fixed-mobility or fixed-prefactor interface.

For the lattice program, conditioning independent geometric gaps changes
their entropy by only o(N). One does not need a coordinatewise
equivalence-of-ensembles assertion for this step: the bounded-coefficient
weighted sum sum_i G_i log w_i concentrates on the scale sqrt(N log N),
and the conditioning costs only a polynomial factor. Its conditional
mean differs by o(N), while log Pr(sum G_i=H)=O(log N).
The exponential-gap argument uses the corresponding density bound.
Consequently

\[
\frac1N D(\pi_1\|\pi_0)\longrightarrow
\int_0^1\!\left[
 \rho_*\log\frac{\rho_*}{\bar\rho}
 +(1-\rho_*)\log\frac{1-\rho_*}{1-\bar\rho}
\right]dx.                                                \tag{23}
\]

For the continuous unit-rod program the corresponding expression is

\[
\int_0^1 f_{\rm rod}(\rho_*(x))\,dx-f_{\rm rod}(\bar\rho),
\qquad
f_{\rm rod}(\rho)=\rho\log\frac{\rho}{1-\rho}-\rho.           \tag{24}
\]

Both are strictly positive for a nonconstant profile. The four-band
example costs asymptotically 0.1308120359 N in the lattice model and
(log 3)N/4=0.2746530722 N in the continuous rod model.

For an isothermal cyclic controller with all auxiliary free energies and
records included, the nonequilibrium free-energy inequality gives the
matching lower bound W>=D(pi_1||pi_0). A prepared battery, chosen label
order, measured microstate or unreset information memory must appear
in that ledger. Equation (22) does not derive a total device-energy
advantage from an ideal net force-work calculation.

One explicit finite asymptotic choice is R=N^(1/3), J=N^(1/6),
delta=N^(-1/6), and fixed ramp duration tau=1. The continuous source
then gives total loading/waiting time O(N^(25/6)/m_-), up to constants
and harmless logarithms, order-N ideal work with O(N^(5/6)) excess,
and final total-variation error O(N^(-1/6)). Actual clocks, reversible
source operation, force precision and tag assembly remain paid.
The full-state error is a finite-tolerance statement; it is not a
superexponential approximation of the loaded microscopic measure.

## 6. What sparse internal access buys, and what it does not

Two exterior pistons with no internal body forces or partitions leave
a single connected equilibrium chamber at constant pressure, hence
constant bulk density for either strictly monotone equation of state.
They cannot hold the four-band example in a stationary zero-current
state. R internal loads supply pressure jumps at R material labels,
giving R independently allocated spatial regions subject to the total
mass and length constraints.

This is a scope statement about static equilibrium holding. It is not
a prohibition on time-dependent boundary control, reservoirs, active
bulk chemistry, or a supplied spatial force field.

The strongest ordinary comparator is R internal pistons or semipermeable
partitions with the same conserved particle counts and force access.
Those devices obey exactly the same pressure balances and realize the
same profile, work and preparation operation. Calling the selected
particles tags does not improve on that mechanism. Sparse tags can be
a small physical realization of internal pistons in a single-file
channel; they are not a new thermodynamic resource.

Position-clamped internal pistons are a stronger port. If their locations
partition space into cells of maximum diameter 1/R and each cell has its
prescribed particle count, the coarse density error is O(1/R) for every
allowed microscopic configuration, even before local equilibration.
Their force range, positioning work, thermal confinement and feedback or
mechanical lock must then be paid. This alternative may dominate the
pressure-controlled preparation for a coarse target; it was not omitted
to make the present construction appear uniquely capable.

Without an anchor the equilibrium is uniform under common translations.
The profile is meaningful relative to the retained origin tag. A
nonflat laboratory mean cannot be claimed by silently fixing that random
origin after the experiment. An actual anchor, external trap, or correctly
retained material-frame readout supplies the missing reference.

## 7. Precision, old records, and genuine limitations

The controller learns no unknown kinetic rates, but the applied force
ratios or continuous loads must be real and known. In the anchored lattice
model, force errors e_j accumulate in log w: a sufficient coarse-profile
condition is max_k |sum_(j<=k)e_j|=o(1). The crude bound
max|e_j|<=epsilon gives a possible R epsilon cumulative error.
For a free ring, a nonzero sum of force errors also introduces a true
nonequilibrium affinity. A common potential/load construction that keeps
the forces exact differences prevents that cycle error, but is an
additional actual construction.

An O(delta) error in log w gives O(delta) macroscopic profile error on
the interior class. It does not give microscopic total-variation error
O(delta) independent of N. Canonical free-energy and information errors
can be order N delta².

The bounds can hold jointly with a retained old record when the actual
initial ceilings, frozen kinetic class, rate or mobility lower bounds,
and future thermal laws hold conditional on that record. Initial records
may identify the tags and counts. They do not grant a free canonical
baseline, arbitrary postselection, or a hidden-state reset.

After release, a bound on the joint actual positional/hidden-class law
also bounds every later genuine observable record under the same
unloaded physical dynamics and record-selected policy, by contraction
of total variation through that actual future kernel. Its reference
starts from the prepared pi_1 and then genuinely relaxes. It is not
the stationary loaded reference. No statement conditions on a newly
retained microscopic preparation log or an unbounded precision work
measurement without rechecking the stated initial-information interface.

The useful working result is therefore concrete: a programmed sparse set
of internal loads can create a specified bulk native material without
identifying its reciprocal kinetics. The continuous version has an
explicit conservative polynomial waiting bound and an order-N reversible
preparation/release ledger. It changes the native state and loses the
earlier density-preservation task. Its core is already the physics of
internal pistons and single-file pressure, so this is a strong ordinary
alternative, not a claimed civilisation-changing discovery by itself.
