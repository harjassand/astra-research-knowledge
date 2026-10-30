# One driven carrier changes the native density through contact

30 October 2026. Complementary construction, Astra P1 / record_geometry.

## 1. Selection result and actual task

A single additional driven hard-core particle can move an extensive native
population and create an order-one native density profile. It needs neither
an extensive controller array nor a force that grows with system size.
The mechanism is the one-dimensional no-passing constraint. It is an
ordinary driven-tracer mechanism, not a new principle.

The construction below adds a useful frozen-kinetics statement: the native
particles may have different unknown symmetric attempt rates. Their exact
stationary law and the common particle velocity remain explicitly soluble.
If the cumulative native resistance homogenizes, the limiting profile is
determined by density and the supplied tracer affinity; the kinetic details
only set the velocity scale.

This alternative does **not** satisfy the stronger task selected by root:
preserve the native bulk density histories while changing physical transport.
It changes the native density itself. Its thermodynamic operating work is
order N on a diffusive observation interval, and preparation is an additional
resource. The profile is relative to the actual tracer position. A uniformly
translated profile must not be reported as a deterministic nonflat
laboratory-frame mean.

## 2. Supplied local operation

There are N lattice sites on a ring, M native particles, one tagged auxiliary
particle, and H=N-M-1 holes. Write n=M+1. Assume H>=1 and M>=1.

The hard-core rule forbids two particles at one site and forbids overtaking.
Label the tracer 0 and the native particles 1,...,M in clockwise order.
Native particle i attempts a jump in either direction at the same frozen rate
c_i, with

\[
0<c_-\le c_i\le c_+<\infty.                                      \tag{1}
\]

Its jump occurs only if the neighboring site is empty. These rates belong to
the particles, not to fixed spatial bonds. They may be unobserved fixed
attributes. The tracer's actual right and left rates are p and q, where

\[
0<q<p<\infty,\qquad F=\log(p/q)>0.                              \tag{2}
\]

For the thermodynamic statements, the supplied port obeys local detailed
balance: a right tracer step receives work F and a left step returns work F
in units of k_B T. An arbitrary actuator with the same coarse jump rates
but hidden futile chemical cycles need not have this work accounting.

The command is a constant local bias. There is no rapid feedback, no copied
microscopic state, no hypothetical second future, and no nonlocal force on
the native particles. Each real successful jump counts as unit physical
displacement of that particular particle. The native and controlled
comparisons contain the same tagged particle; setting p=q removes the bias.
The bath/jump model is a supplied bounded-rate interface, not a derivation
of a particular mechanical device from an equilibrium weight.

## 3. Exact stationary law with unknown frozen native rates

Let g_i be the number of holes immediately clockwise of particle i. Then
g=(g_0,...,g_M) is a composition of H into n parts. A right jump of particle i
moves one hole from gap i to gap i-1, with cyclic indices; a left jump is the
reverse move. Define

\[
S_i=\sum_{j=1}^{i}c_j^{-1},\quad S=S_M,\quad
\mathcal J=\frac{p-q}{1+qS},\quad
w_0=1,\quad w_i=1+\mathcal J S_i.                              \tag{3}
\]

The weights obey

\[
c_i(w_i-w_{i-1})=\mathcal J\quad(1\le i\le M),\qquad
p w_0-qw_M=\mathcal J.                                        \tag{4}
\]

Let

\[
Z_H(w)=\sum_{\substack{g_i\ge0\\\sum_i g_i=H}}\prod_{i=0}^M w_i^{g_i},
\qquad
\pi_H(g)=Z_H(w)^{-1}\prod_{i=0}^M w_i^{g_i}.                    \tag{5}
\]

This is the exact invariant law of the gap process. Adding an independent
uniform tracer position gives the invariant law of the full ring in the
specified cyclic particle-order sector. The finite process is irreducible
within that sector and nonexplosive at the stated positive rates, so this
sector's invariant law is unique. Different conserved cyclic orders are
not silently mixed or reset.

For completeness, set p_i=q_i=c_i for i>=1, p_0=p, q_0=q.
For each gap j the coefficient of the indicator g_j>0 in the stationarity
equation, divided by pi_H(g), is

\[
\frac{p_{j+1}w_{j+1}+q_jw_{j-1}}{w_j}-(p_j+q_{j+1})=0.         \tag{6}
\]

Equation (6) follows by subtracting the two neighboring constant-current
identities p_iw_i-q_iw_{i-1}=\mathcal J. This proves stationarity directly;
it does not infer it from visible equilibrium statistics.

Put t_H=Z_{H-1}/Z_H. Removing one hole from gap i gives

\[
\pi_H(g_i>0)=w_i t_H.                                         \tag{7}
\]

Consequently every particle, including every native particle, has the same
stationary mean physical velocity

\[
v_N=p_i\pi_H(g_i>0)-q_i\pi_H(g_{i-1}>0)
   =\mathcal J t_H.                                          \tag{8}
\]

This is an equality of actual displacements. It is not a redefinition of the
native current as an auxiliary current.

### 3.1 Uniform finite-size capacity

No limit theorem is needed to show that the force is transmitted to an
extensive native population. Counting every hole once yields

\[
H Z_H
=\sum_{\sum g_i=H-1}\left(\prod_iw_i^{g_i}\right)
  \sum_i w_i(g_i+1).
\]

Therefore

\[
\frac{H}{w_{\max}(H+n-1)}
\le t_H\le
\frac{H}{w_{\min}(H+n-1)}.                                    \tag{9}
\]

Here w_min=1 and

\[
w_{\max}=\frac{1+pS}{1+qS}<p/q.
\]

For n/N bounded away from zero and one, (1), (3), and (9) give

\[
v_N=\Theta(N^{-1}),\qquad Mv_N=\Theta(1),                       \tag{10}
\]

with constants uniform over all frozen arrays satisfying (1). Thus a single
bounded-rate auxiliary supplies a nonvanishing mean total native current.
The tracer moves only order N on physical time N^2; the M native particles
together move order N^2.

## 4. Kinetically robust macroscopic profile

An exact spatial profile requires more than the bounds (1). Assume
n/N -> rho in (0,1) and a deterministic, quenched resistance limit

\[
\sup_{0\le u\le1}
\left|\frac1M S_{\lfloor uM\rfloor}-\bar r\,u\right|
\longrightarrow0,\qquad 0<\bar r<\infty.                      \tag{11}
\]

For example, fixed homogeneous rates c give bar r=1/c. Frozen stationary
ergodic rates with a suitable resistance law of large numbers are another
supplier; the present statement is pointwise for arrays satisfying (11).
For arbitrary arrays satisfying only (1), the exact finite formulas remain
valid, but a universal spatial profile is not asserted.

Write k=e^F-1. From (3),

\[
w_{\lfloor uM\rfloor}\longrightarrow 1+ku
\]

uniformly. There is a unique t in (0,e^{-F}) solving

\[
\int_0^1\frac{du}{1-t(1+ku)}=\frac1\rho,
\quad\hbox{equivalently}\quad
\frac{\log[(1-t)/(1-e^F t)]}{kt}=\frac1\rho.                    \tag{12}
\]

The left side is continuous and strictly increasing from 1 to infinity.
Since 1/rho>1, existence and uniqueness follow.

The physical macroscopic coordinate, measured clockwise from the tracer,
of particle with label fraction u is

\[
x(u)=\rho\int_0^u\frac{dv}{1-t(1+kv)}.
\]

Consequently the native density profile converges in probability to

\[
\rho_F(x)=(1-t)e^{-\lambda x},\qquad
\lambda=\frac{kt}{\rho},\qquad 0<x<1.                          \tag{13}
\]

It has mean rho and a discontinuity at the tracer:

\[
\rho_F(0+)=1-t,\quad \rho_F(1-)=1-e^F t,\quad
\frac{1-\rho_F(1-)}{1-\rho_F(0+)}=e^F.                         \tag{14}
\]

The one auxiliary contributes mass 1/N, so it does not change this native
density limit. The mean velocity satisfies

\[
Nv_N\longrightarrow \bar v=\frac{\lambda}{\bar r}.              \tag{15}
\]

The profile shape is independent of the individual c_i and even of a
bounded positive common prefactor multiplying both p and q. Those kinetics
affect the time scale, through bar r, rather than the limiting profile.

### 4.1 Proof of the profile limit

Choose t_N<1/w_max so that independent geometric variables G_i with

\[
\Pr(G_i=a)=(1-t_Nw_i)(t_Nw_i)^a,\qquad a\ge0,
\]

have total mean H. Conditional on their sum being H, their joint law is
exactly (5). Uniform convergence of the weights and monotonicity show
t_N -> t from (12). Since t<e^{-F}, all geometric parameters eventually lie
in a fixed compact subset of (0,1).

Uniform exponential moments give exponential concentration of all partial
sums on the scale N. Conditioning on the total does not destroy this:
the triangular-array local central limit estimate gives
Pr(sum G_i=H)=Theta(N^{-1/2}). It follows directly by Fourier inversion:
the product characteristic function decays as
exp[-cN sin^2(theta/2)], while its small-theta expansion has variance Theta(N)
and uniformly bounded third moments. Dividing the concentration bounds by
this polynomial conditioning probability still tends to zero exponentially.

Thus the cumulative physical positions converge uniformly to x(u).
The derivative dx/du=rho/[1-t(1+ku)] is positive and bounded, so inversion
gives (13). The same local central limit estimate at H-1 and H yields

\[
t_H=t_N
\frac{\Pr(\sum_iG_i=H-1)}{\Pr(\sum_iG_i=H)}
\longrightarrow t,
\]

which proves (15). This proves a stationary profile and stationary mean
velocity, not a mixing-time theorem from an arbitrary unprepared state.

### 4.2 A concrete target

Choose F=log 2, t=1/4, and

\[
\rho=\frac{1}{4\log(3/2)}.
\]

Then

\[
\rho_F(x)=\frac34(2/3)^x,\qquad
\bar v=\frac{\log(3/2)}{\bar r},\qquad
\rho\bar v=\frac{1}{4\bar r}.                                 \tag{16}
\]

The native density decreases from 3/4 immediately ahead of the tracer to
1/2 immediately behind it. The steady mean native total current tends to
1/(4 bar r). No native hopping coefficient is measured by the controller.

## 5. Work, preparation, and the actual record

Let X_0(s) be the tracer's unwrapped displacement and
B_nat(s)=sum_{i=1}^M [X_i(s)-X_i(0)] the true native total displacement.
Under the stationary law, exactly

\[
\mathbb E B_{\rm nat}(s)=Mv_Ns,\qquad
\mathbb E W(s)=Fv_Ns.                                        \tag{17}
\]

For physical time s=N^2 T, (15) gives

\[
\frac{\mathbb E B_{\rm nat}(N^2T)}{N^2}
\longrightarrow \rho\bar v T,\qquad
\frac{\mathbb E W(N^2T)}{N}
\longrightarrow F\bar v T>0.                                 \tag{18}
\]

The equality for work counts the actual signed work of the tracer port.
At stationarity it also equals entropy production in units of k_B:
all native edges have forward/reverse rate ratio one, and the only
nonzero cycle affinity is F. The system-probability contribution to
stationary entropy production cancels by stationarity.

This does not price a chemical apparatus with futile cycles or no recovery
on reverse steps. In particular, absolute supplied energy per attempted
or successful step can be of order N^2 even though the reversible port's
mean net work is order N. Native and tracer jump activity, confinement,
fabrication, initialization, sensing and operation time remain resources.
There are O(N^3) native attempt events and O(N^2) tracer attempts on the
diffusive interval at the bounded-rate interface.

The stationary law is not supplied for free. A preparation can wait for
the finite irreducible process to converge, but its mixing time and work
must be charged. Equations (17)--(18) are stationary service costs; they
do not prove that a controller starting with a flat unprepared native
population reaches this state by a particular multiple of N^2.
An exact positional sampler/placer would be a stronger operation.
The homogeneous driven-tracer hydrodynamic literature provides a separate
transient route under its actual initial-law hypotheses; it is not silently
extended here to arbitrary frozen arrays.

The displayed profile is relative to the tracer. In the full stationary
law the tracer position is uniform, so the laboratory mean density is flat.
A typical macroscopic configuration nevertheless has the nonflat profile
(13) at a random translation. Retaining the actual tracer position makes
the density control visible. Pinning the profile at a prescribed laboratory
location needs another operation; it does not follow from a coordinate
change.

All exact finite identities hold for each fixed rate array. They therefore
allow an arbitrary old record that selects such an array, provided the
conditional initial law and the complete future generator are the ones
specified. A record that also selects a nonstationary initial gap state
does not warrant the conditional stationary expectations (17). Mixtures
of arbitrary conditional laws cannot be replaced by the stationary law
without an additional preparation estimate.

## 6. A resource boundary for creating native density structure

Here is the appropriate scope for an extensive-work obstruction. It is
an isothermal free-energy statement at a specified equilibrium reference,
not a universal prohibition on sparse control.

Start the unbiased native system in its canonical uniform equilibrium.
Include the auxiliary, controller, memory and retained record in the
thermodynamic state. Suppose their total initial excess free energy is
o(N), the final Hamiltonian/reference is restored, and all work sources
and information reservoirs are included. Local detailed balance gives

\[
\beta\mathbb EW
\ge D(P_T\Vert\Pi_{\rm eq})-D(P_0\Vert\Pi_{\rm eq}).             \tag{19}
\]

One direct proof writes the relative-entropy balance as
dD/ds=beta times mean work rate minus nonnegative entropy production,
including the usual reference-free-energy term during a changing
Hamiltonian. With equal initial and final reference Hamiltonians that
term vanishes upon integration.

If the final native profile, possibly relative to a retained tracer
position, concentrates near a deterministic rho_*(x) of mean rho, then
the canonical equilibrium counting bound yields

\[
\liminf_{N\to\infty}\frac1N D(P_T\Vert\Pi_{\rm eq})
\ge \mathcal V(\rho_*)
:=\int_0^1\left[
\rho_*\log\frac{\rho_*}{\rho}
(1-\rho_*)\log\frac{1-\rho_*}{1-\rho}\right]dx.                 \tag{20}
\]

For a concise derivation, partition the ring into a fixed number of blocks,
count equilibrium configurations at the prescribed block densities by
binomial coefficients, and use Stirling's formula. Under the target law
the corresponding event has probability tending to one. The binary
relative-entropy inequality

\[
D(P\Vert Q)\ge P(A)\log(1/Q(A))-\log2
\]

then gives the block version of (20); refine the partition. Conditioning on
an unbiased tracer position or allowing N possible translations changes
the counting exponent by at most log N. It does not remove the order-N
cost of a nonflat profile.

For every nonconstant profile, mathcal V>0. In the explicit example (16),
with lambda=log(3/2), binary Pinsker gives the positive lower bound

\[
\mathcal V(\rho_F)\ge 2\int_0^1(\rho_F-\rho)^2dx
=\frac{5\lambda-2}{16\lambda^2}>0.                            \tag{21}
\]

Thus o(N) total work plus o(N) supplied free energy cannot prepare this
profile from the specified equilibrium. A small number of carriers can
transmit the force; their number does not eliminate the extensive native
free-energy requirement.

Equation (19) requires honest accounting of preparation and old information.
An initially correlated old record can supply mutual information; a
metastable native state can supply stored free energy; an uncharged chemical
source can supply work. Those are additional resources rather than
counterexamples to (19). Likewise, a passive gate changing the *relaxation*
of an already nonflat profile does not create the free energy in (20).
Phase selection in a different equilibrium system is outside the canonical
exclusion reference used here.

## 7. Strong ordinary comparisons and priority

### 7.1 Driven tracer

[Ayyer, Ann. Inst. H. Poincare D 10 (2023), 687--713,
arXiv:2001.02425](https://arxiv.org/pdf/2001.02425) gives the exact
stationary factorization, currents and scaled tracer-frame profile for
homogeneous native rates. Its Section 2 explicitly identifies the
zero-range mapping as established machinery. This is a direct predecessor,
not merely an analogy. The finite frozen-rate calculation above is a
useful extension of that ordinary traffic-equation solution, with no
priority claim.

[Lobaskin and Evans, Driven Tracers in a One-Dimensional Periodic Hard-Core
Lattice Gas, arXiv:2002.02841](https://arxiv.org/pdf/2002.02841) studies
actual driven tracers and their influence on the native density and current.
It explicitly identifies no passing as the source of long-range coupling.
The model there includes totally asymmetric tracers; the present finite-F
work accounting instead keeps both p and q strictly positive.

[Landim, Olla and Volchan, Communications in Mathematical Physics 192
(1998), 287--307](https://doi.org/10.1007/s002200050300) proves a diffusive
law of large numbers for an infinite-line driven tracer via an
inhomogeneous zero-range hydrodynamic equation. The primary abstract was
checked; its complete hypotheses were not imported into a finite-ring
transient theorem here.

### 7.2 An ordinary direct contact actuator can be simpler

[Bodineau, Derrida and Lebowitz, A Diffusive System Driven by a Battery
or by a Smoothly Varying Field, J. Stat. Phys. 140 (2010), 648--675,
arXiv:1003.5838](https://arxiv.org/pdf/1003.5838) studies one asymmetric
bond on the native ring. This local stationary battery produces a
nonflat laboratory-frame density and current of order 1/N per bond.
Its bulk density equation remains heat, with nonlinear boundary matching
at the battery. This is a stronger direct actuator on native transitions;
it needs no mobile auxiliary and avoids the random profile origin.
It also changes native density histories and pays a nonzero affinity.
The source's hydrodynamic and fluctuation statements are credited to that
model, not promoted to a theorem for unknown hidden kinetics.

### 7.3 Passive sparse barriers refute a broader sparsity claim

[Franco, Goncalves and Neumann, Ann. Inst. H. Poincare B 49 (2013),
402--427, arXiv:1010.4769](https://arxiv.org/pdf/1010.4769) proves the
critical slow-bond transition for symmetric exclusion. A finite number of
bonds with rates N^{-beta} are invisible to the diffusive density law
when beta<1; beta=1 yields a membrane law; beta>1 blocks macroscopic
passage. Thus one local passive kinetic change can affect an extensive
density field, but its resistance must scale with N.

An elementary exact current comparison makes the resource transparent.
On an exclusion chain coupled to fixed boundary densities, stationary
native current is

\[
J=\frac{\rho_L-\rho_R}{\sum_e c_e^{-1}},
\]

with boundary contact resistances included. The expectation closure
E[eta_i(1-eta_j)-eta_j(1-eta_i)]=E eta_i-E eta_j makes this identity exact.
Changing R=o(N) uniformly bounded resistances changes the total resistance
by only o(N); adding resistance Theta(N/R) at each of R sites can change
the order-one macroscopic conductance. For periodic cells of length
L=N/R, native rate c and one gate rate c/(1+lambda L), the mean resistance
per site is exactly (1+lambda)/c. The usual homogenized diffusivity is
c/(1+lambda) if the cells become microscopically fine.

That periodic homogenization is an ordinary resistor/hydrodynamic
comparator; no full path LDP for it is proved here. An Arrhenius gate would
need a transition-state barrier of order log(N/R). Specifying that barrier
does not by itself establish an unknown physical attempt prefactor.
Actual gate conductance, assembly, holding and barrier-preparation costs
must be warranted. Reversibility removes housekeeping entropy production,
not the apparatus bill.

### 7.4 Thermodynamic principle

[Esposito and Van den Broeck, EPL 95 (2011), 40004,
arXiv:1104.5165](https://arxiv.org/abs/1104.5165) supplies the ordinary
nonequilibrium free-energy inequality underlying (19). Equations
(20)--(21) specialize it to the actual native-profile target. No new second
law is proposed.

## 8. What this construction settles

Sparse local contact is sufficient for genuine native density control in a
one-dimensional no-passing medium. It uses a specific topology and a paid
affinity. In the solved frozen-rate class, unknown kinetic coefficients do
not prevent a macroscopic response and need not be identified to prescribe
the limiting profile when resistance homogenizes.

The construction does not preserve native density histories, prepare its
stationary law for free, generalize to overtaking carriers, or establish
cheap control of arbitrary hidden reciprocal dynamics. A direct native
battery is a strong ordinary competitor at an explicitly stronger port.
The sharper remaining opportunity is a physical operation that changes
transport while preserving the native density-path task at comparable
total resources.


