# What a computation must retain, and what its apparatus may consume

The subsequent construction in `PROTECTED_ABSORPTION.md` is the principal
result of this continuation. It shows why the near-pure orbital reset
requirement in Section 7 below can be replaced by a constant-floor progress
condition when strong microscopic sector opacity holds on the full orbital
space. This note preserves the preceding derivations and costs.

Working research, 31 October 2026. This is a continuation of the common-frame
construction in `../p2_transport/DERIVATION.md`. That construction, its
one-resonance full-charge theorem, microscopic recentering, source-algebra
obstruction and complete instrument remain intact. Equation (1) in that file
has had a missing displayed plus sign restored; its mathematics and executable
calculation have not otherwise been changed.

## Result and choice of mechanism

The strongest completed change here is a **branch-dependent quantum-memory
law**, used to build a singlet/triplet instrument with actual pair consumption.
A conclusive rank-one singlet branch need not return the original particles.
A real singlet source can replace them. The triplet branch retains a
three-dimensional quantum state and cannot be replaced using a classical label.
The law has a tight quantitative version: if an arbitrary rank-r sector must
pass through a retained quantum system of dimension k<r, even unlimited
classical records leave worst-case half-diamond error at least 1-k/r.

The physical construction is local singlet pair loss, one finite loss window,
spin-preserving presence detection at separated ports, and conditional fresh
singlet supply. A full charge-star contraction, retaining both double
occupations and noncommuting retained source operators, replaces thousands of
discrete capture/readout/return windows. Its optical realization is examined
using one candidate species throughout: ground-electronic-state 171Yb.

The construction is a conditional complete-instrument result, not a device
window. The microscopic audit makes this distinction consequential. A
declared 100-kHz double-well model permits the desired loss rate well below its
orbital gap, yet the conservative complete window accumulates approximately
0.57% nuclear Raman exposure before readout, cooling, source replacement or
holding. Its approximately 119-nm two-well potential is not furnished by
naming an ordinary optical tweezer.

Renewal cannot be ignored. The scalar Rayleigh detector heats motion. A
direct audit of a published one-upper-level optical cooling Hamiltonian
finds an undressed electronic mode; increasing that drive does not remove
its hyperfine interaction. Established scalar cavity sideband cooling is a
constructive replacement. It supplies an energy-contraction model with
explicit cooperativity, recoil, optical-power, geometry and holding costs.
The resulting repeated-use theorem controls **weighted joint histories**,
not the temperature of every arbitrarily selected rare trajectory.

All new derivations retain working status. No exhaustive novelty claim is
made. The constituent ideas of state preparation after a rank-one
measurement, quantum-memory dimension witnesses, lossy Hubbard physics,
nuclear-spin qubits, cavity cooling and singlet-only computational
universality are credited below. The additions are their explicit
instrument/resource composition, the source-uniform full-charge bound,
quantitative failure witnesses and the ensuing physical corrections.

Throughout, epsilon denotes one half of the diamond norm of the difference
of complete, trace-preserving instruments, including classical outcome and
abort flags. A restricted energy/input domain is stated where needed.

## 1. A tight law for renewal after a measured outcome

### 1.1 The exact rank-one construction

Let A be a measured pair, E all retained apparatus and sources, and R any
reference or rest of the computation. The initial state on AER is arbitrary.
For the singlet |s>, suppose the actual destructive fine histories are

\[
J_h=|\mathrm{vac}\rangle\langle s|\otimes F_h.
\tag{1}
\]

Supply a real source with accepted loading histories

\[
R_k=|s\rangle\langle\mathrm{vac}|\otimes G_k.
\]

The composition is exactly

\[
R_kJ_h=P_s\otimes G_kF_h.
\tag{2}
\]

No unknown quantum information in the rest of the computation is erased.
Indeed, P_s rho P_s = |s><s| tensor rho_ER^(s). Different source histories
can steer pre-existing E/R correlations; equation (2) preserves the complete
joint instrument, not a fictitious independently reset E. Replacement may
use different particles and a new motional wavepacket, provided those are
the admitted output ports and physical singlet of the next operation.

This does not supply a singlet source, a lower loading rate, orbital cooling
or spare particles. Those are constructed and charged in Sections 5-7.
Ordinary one-particle loss before a conclusive singlet projection does not
have (1).

### 1.2 What a classical label cannot preserve

Let an accepted sector P have rank r. Require the identity quantum channel
on that sector, including a reference maximally entangled with it. Suppose
the operation erases the original carriers and retains at most a k-dimensional
quantum system, alongside any classical record. All other systems carrying
the input state are inaccessible to recovery. For k<r,

\[
\boxed{\frac12\|\mathcal R\mathcal E-\mathrm{id}_r\|_\diamond
\ge 1-\frac{k}{r}.}
\tag{3}
\]

Proof: after the bottleneck, every pure branch has Schmidt rank at most k
across accessible memory versus the reference. Subsequent local decoding and
classical mixing leave Schmidt number at most k. Its overlap with the
maximally entangled r-dimensional state is at most k/r, by Cauchy-Schwarz on
the k Schmidt coefficients. The two-outcome test onto that maximally
entangled state gives trace distance at least 1-k/r. This also bounds the
diamond distance.

The bound is tight for unrestricted encoding/decoding. Let P_U range over
Haar-random rank-k projectors and use the continuous instrument with Kraus
density sqrt(r/k) P_U. Store its k-dimensional output and the classical U,
then embed it back. The averaged channel is

\[
\Lambda_k(\rho)=a\rho+(1-a)\frac{I}{r}\operatorname{tr}\rho,
\qquad a=\frac{kr-1}{r^2-1}.
\tag{4}
\]

Its normalized Choi overlap is k/r and its half-diamond distance from the
identity is 1-k/r. This is a mathematical saturation argument, not a claim
that the random projector instrument is available in the present apparatus.
The Schmidt-number argument is standard quantum-information machinery [1].

Consequences for the actual task:

| Sector to preserve | Dimension | Error floor if only a classical label survives |
|---|---:|---:|
| Singlet | 1 | 0; an actual fresh singlet suffices |
| One two-qubit parity sector | 2 | at least 1/2 |
| Triplet | 3 | at least 2/3 |

If an accessible reservoir secretly retains the unknown state, it counts as
quantum memory in (3). Restoring its visible controls does not erase that
resource. If only a logical subsystem is required, replace r by the
dimension of that logical subsystem, but prove that the future operation
stack does not need the erased correlations. A gauge label cannot simply be
declared disposable when future contacts use it.

### 1.3 Why consuming every branch would lose the computational resource

Starting from a product of singlet bonds, successful destructive singlet
projections alone merely contract paths of singlet tensors. Projecting two
members of different bonds swaps entanglement to the two remaining endpoints;
projecting the endpoints of one bond removes that bond. Products of bonds
remain products of bonds. This does not furnish the full singlet/triplet
computational model.

In particular, replacing a triplet outcome by its classical label is not a
shortcut to the published universal consumer. That consumer uses coherent
triplet branches as actual operations [2,3]. The present mechanism retains
those branches and consumes only the rank-one singlet branch.

## 2. The native sink and a full-charge contraction

### 2.1 Derive the spin selection from fermions

Admit one physical orbital at each of two ports a,b. Use spin-independent
hopping and local loss operators

\[
H_{\rm hop}=-\sum_\sigma
(c^\dagger_{a\sigma}c_{b\sigma}\otimes B+\mathrm{h.c.}),
\qquad L_j=\sqrt{\Gamma_j}\,c_{j\downarrow}c_{j\uparrow}.
\tag{5}
\]

Keep all six two-fermion states: three separated triplets, separated singlet
S, and both doubles D_a,D_b. In this complete admitted space, hopping and
local pair loss annihilate every separated triplet. Hopping couples S to
the doubles with sqrt(2) times the single-particle contact.

All density interactions, assisted hopping, double-to-double pair hopping
and source dependence remain in the three-dimensional singlet charge block.
Every loss history therefore has the factor <s|, while the complete triplet
instrument is identity on its three spin directions tensor a source map.

The Lindblad notation is not a microscopic source proof. One possible
dilation is a fresh empty continuum of escaping pair products coupled to
c_down c_up. Smooth spectral density across the admitted conditional
transition energies, negligible re-entry and short reservoir correlation
time are required for a constant Markov rate. This continuum is an additional
prepared resource, distinct from the arbitrary retained source E.

The dissipative Hubbard experiment [4] gives an actual native pair-loss
precedent in 173Yb, but in the metastable 3P0 state. We do not borrow its
rates for the ground-state 171Yb detector. The latter candidate instead uses
optical photoassociation with the actual molecular channels in [5].

### 2.2 Source-valued amplitudes, with no bath inverse

In a forward common-source interaction picture let the no-loss amplitudes
obey, with hbar=1,

\[
\begin{aligned}
\dot s&=-iT_a^\dagger a-iT_b^\dagger b,\\
\dot a&=-iT_as-i\Delta a-iKb-\Gamma_a a/2,\\
\dot b&=-iT_bs-iK^\dagger a-iH_b b-\Gamma_b b/2.
\end{aligned}
\tag{6}
\]

The vectors may include any reference. Require, on all admitted source
histories,

\[
a_- I\le\Re T_a\le a_+I,\quad \|T_b\|\le b_+,
\quad\|\Delta\|\le\delta,\quad\|K\|\le\kappa.
\]

Both loss rates have strictly positive lower bounds and finite upper bounds.
There is no mathematical bandwidth bound on the common source or H_b.
The imaginary part of T_a does not enter the Lyapunov estimate; well-defined
common operator domains and propagators are still required.

Set N=||s||^2+||a||^2+||b||^2 and

\[
V=N+c\operatorname{Im}\langle s,a\rangle,\qquad0<c<2.
\]

Direct differentiation cancels the common generator. The only cross term
involving H_b is absent because V couples S to D_a only. The resulting
quadratic lower bound for -dot V is the matrix

\[
Q=\begin{pmatrix}
ca_-&-c(\delta+\Gamma_{a,\max}/2)/2&-c\kappa/2\\
-c(\delta+\Gamma_{a,\max}/2)/2&\Gamma_{a,\min}-ca_+&-cb_+/2\\
-c\kappa/2&-cb_+/2&\Gamma_{b,\min}
\end{pmatrix}.
\tag{7}
\]

Since (1-c/2)N<=V<=(1+c/2)N, Q>=mI>0 proves

\[
\|U_{\rm no}(T)\|^2\le
\frac{1+c/2}{1-c/2}\exp[-mT/(1+c/2)].
\tag{8}
\]

Small positive c always works for finite displayed bounds, positive a_- and
both positive loss rates. No source derivative or reversed evolution is
used. This is the dissipative analogue of retaining the complete charge
star in the previous one-resonance theorem.

A rational example is

\[
gI\le\Re T_a\le2gI,\quad\|T_b\|\le2g,
\quad\delta,\kappa\le g,\quad\Gamma_a=\Gamma_b=2g.
\]

At c=1/4 the leading principal minors of Q/g-(9/50)I are
7/100, 299/10000 and 13793/1000000. Thus

\[
\boxed{q(T):=\|U_{\rm no}(T)\|^2
\le\frac97 e^{-4gT/25}.}
\tag{9}
\]

The exact rational certificate is in `detector/pair_loss_check.py`. Dense
matrix examples verify its derivative inequality with noncommuting and
rapid common sources, but are not its proof.

### 2.3 Physical qualifications that the proof does not remove

The unbounded-H_b freedom is mathematical. A real finite-width molecular
sink still needs spectral support for every transition admitted by the
physical domain. Both doubles need a sink: an undamped, arbitrarily detuned
off-target state can trap amplitude. Extremely strong loss is not optimal;
the familiar Zeno limit slows transfer as g^2/Gamma.

Accretivity is a coarse operator promise. It is not established by a few
prepared calibration shots. Classical source control with a stronger known
model may admit a much faster ordinary optimized or adiabatic operation.
Equation (9) is a robust sufficient schedule, not a lower bound on duration.

## 3. A correct quantum instrument requires the survivor amplitude

After one finite loss window, turn off contact and interrogate atom presence.
Loss/no-loss records in the outgoing particle reservoir are orthogonal.
After tracing those products, the state has no coherence between total
occupancy zero and two. No-loss S/T coherence, however, remains inside the
two-particle sector.

The no-loss branch has the form

\[
K_T=P_t\otimes U_t+A_TP_s,\qquad\|A_T\|\le a=\sqrt{q(T)}.
\tag{10}
\]

All conclusive loss histories, after actual replacement, have form (2).
Stack their source operators in W. Completeness gives
W^dagger W=I-A_T^dagger A_T on the singlet input source. The polar comparison
V=W(I-A_T^dagger A_T)^(-1/2) is an analytical isometry, not a physical
inverse source operation. Its distance from W is at most
1-sqrt(1-a^2).

For input singlet weight p, the off-diagonal no-loss contribution has
half-trace norm at most a sqrt(p(1-p)); its remaining singlet weight costs
at most a^2 p/2. The loss-branch normalization costs at most
[1-sqrt(1-a^2)]p. Hence the safe reference-uniform bound

\[
\epsilon_{\rm intrinsic}\le a+a^2
\tag{11}
\]

for a<=1. Surviving doubles and any fixed completion of their output are
included in this bound; no projected return is inserted.

### An exact witness and formula

For a scalar ideal absorber, K_s=sqrt(1-q)P_s and
K_t=P_t+sqrt(q)P_s, the full answer is sharper:

\[
\boxed{\epsilon_{\rm scalar}=
\frac{\sqrt q}{2-\sqrt q}.}
\tag{12}
\]

For a pure input with singlet weight x, including a reference, the relevant
two-dimensional subspace gives

\[
D(x)=\tfrac12\left[qx+
\sqrt{q^2x^2+4qx(1-x)}\right].
\]

The maximum is attained at x=1/(2-sqrt(q)) and equals (12). Convexity and
purification cover all mixed/reference inputs. In particular, q=10^-6 gives
instrument error 0.000500250125..., not 10^-6. This calculation directly
excludes a label-only error analysis.

### Why number-classification error can now be linear

The actual escaping-product record has already removed 0/2 charge coherence.
For an ideal spin-scalar detector with uniformly bounded misclassification
eta on each allowed occupancy block, relabeling the same fine physical
histories costs at most eta in the joint instrument. The detector may alter
motion or retained sources; those maps remain in the comparison.

This does not contradict the earlier sqrt(eta) bound for general coherent
charge inputs. The new physical domain has earned block diagonality. It
does not grant spin opacity to a detector whose photons distinguish nuclear
states. Raman histories are actual additional errors.

## 4. Microscopic nuclear-spin readout, including its cost

Ground-state 171Yb has I=1/2 and J=0. For zero field and pi-polarized weak
excitation to J=1, write the excited hyperfine Hamiltonian as A I dot J.
In each accessible m_F=+/-1/2 block it is

\[
H_{\rm hf}=\begin{pmatrix}0&A/\sqrt2\\A/\sqrt2&-A/2\end{pmatrix}.
\]

Put z=Delta+i Gamma/2 and D=(z-A/2)(z+A). The exact two-by-two resolvent
within this admitted optical model gives

\[
r_0=\frac{z+A/2}{D},\qquad r_1=\frac{A/\sqrt2}{D},
\]

\[
L_0=\sqrt\Gamma\frac\Omega2r_0I,
\quad L_+=\sqrt\Gamma\frac\Omega2r_1|\downarrow\rangle\langle\uparrow|,
\quad L_-=\sqrt\Gamma\frac\Omega2r_1|\uparrow\rangle\langle\downarrow|.
\tag{13}
\]

The light shift and sum of no-photon attenuation terms are scalar. All
elastic Rayleigh records therefore preserve nuclear-spin coherence, including
references. The nonzero Raman rate is explicit:

\[
\zeta:=\frac{R_R}{R_0}
=\frac{A^2}{2[(\Delta+A/2)^2+(\Gamma/2)^2]}.
\tag{14}
\]

This is an extension of the far-detuned scalar-effect analysis in [6], not
an exact statement about all electronic levels, magnetic fields or laser
states. Weak excitation, the finite optical manifold, polarization, source
linewidth and field uniformity remain physical conditions. Spatial recoil
multiplies the scalar jump by a motional operator; it is harmless to spin
but not free for subsequent orbital admission.

For separate presence tests at both ports, collection efficiency eta_c and
duration t give the simple bound

\[
\epsilon_{\rm read}\le
2e^{-\eta_cR_0t}+2R_Rt+2dt+\epsilon_{\rm optical,other},
\tag{15}
\]

where d bounds dark-count/false-vacuum hazards under the stated count rule.
One-atom outputs are explicit loss flags. Hardware which only distinguishes
zero from nonzero total occupancy cannot silently certify two atoms.

At large detuning, R_0 approximately Gamma Omega^2/(4 Delta^2). For
L=log(2/epsilon_count), t approximately 4L Delta^2/(eta_c Gamma Omega^2),
while the two-atom Raman contribution is approximately L A^2/(eta_c Delta^2).
If the retained computation has an independent half-diamond error rate r_h,
then at fixed maximum Omega

\[
\mathcal B_R+\mathcal B_h\simeq
\frac L{\eta_c}\left[
\frac{A^2}{\Delta^2}+
\frac{4r_h\Delta^2}{\Gamma\Omega_{\max}^2}\right],
\]

and minimization of this model expression gives

\[
\Delta_{\rm opt}^2=|A|\Omega_{\max}\sqrt{\Gamma/(4r_h)},
\qquad
(\mathcal B_R+\mathcal B_h)_{\rm min}
=\frac{4L|A|}{\eta_c\Omega_{\max}}\sqrt{r_h/\Gamma}.
\tag{16}
\]

Here the B terms are sufficient error-budget contributions in this
explicit simplified rate model. Minimizing them is not a lower bound on
the actual error of this detector or of every possible detector. If the optimum
violates weak excitation, electronic-level separation or trap constraints,
it is unavailable. Increasing detuning alone does not make readout
arbitrarily reliable at fixed power and holding noise. A cavity or a different
readout is allowed to improve this trade, and must receive the same source
information in a comparison.

## 5. A real source can exploit rank one too

The singlet factory need not assume a repulsive 171Yb Hubbard interaction.
Admit one bound orbital of an isolated source trap, fill it from a cold
unpolarized Fermi reservoir, isolate it, then split it with a spin-independent
path. Accept only a spin-preserving presence record at both separated
outputs. A doubly filled single orbital is the unique singlet by fermion
antisymmetry.

For a classical noninteracting splitter,
c_sigma^dagger maps to sqrt(p)a_sigma^dagger+sqrt(1-p)b_sigma^dagger. The
one-at-each-output term has weight 2p(1-p) and is exactly S. A coarse box
p in [1/4,3/4] yields acceptance at least 3/8, conditional on double filling.
No fine 50/50 calibration is necessary. With retained operator-valued
controllers, this product expression is not automatic; a full two-particle
transfer bound is required instead.

The source note supplies the actual filling-rate model and its reverse
escape, finite particle capacity, higher-band contamination and false-herald
terms. In particular, if bad loading probability is b and good acceptance
is at least a, the conditional contamination can scale as b/a. A small raw
loading error is not its accepted error. Existing cold 171Yb reservoirs [7,8]
are physical precedents, not measurements of this proposed factory's yield.

A capped factory with per-attempt progress at least p_F and duration T_F
has failure weight at most (1-p_F)^m after m attempts. Its supply rate,
all rejected preparations, readout, cooling and routing count. Offline
factories and buffering can reduce the time during which data wait, but
add apparatus and storage. They are not free consequences of (2).

## 6. A decisive cooling failure, and a supplied alternative

### 6.1 Strong dressing does not repair a missing coupling rank

The single-upper-level Hamiltonian written in Eq. 50 of [6] couples the
electronic x combination of m_J=+1,-1 to one upper J=0 state. It has rank
one. The orthogonal electronic y mode and m_J=0=z remain undressed.
Projecting the actual hyperfine operator into that two-dimensional kernel
gives

\[
P_dH_{\rm hf}P_d=A I_xJ_x,\qquad
\|P_dH_{\rm hf}P_d\|=|A|/2.
\tag{17}
\]

This term survives infinite dressing strength. In the full eight-state
calculation, an initial |m_J=0,up> has m_J=0 population approximately
7.6e-12 at t=pi/|A| for drive/A=1000. The limiting population is zero,
not one. The two alleged independently dressed electronic branches share
one upper state; they cannot be treated as independent two-level systems.

This counterexample addresses the printed Hamiltonian's isolation claim.
It does not refute the scalar off-resonant readout or optical cooling in
general. The original large-magnetic-field cooling method [9] has a genuine
different physical mechanism and its own field/coherence costs.

Two independent J=0 upper levels, coupled to x and y separately, repair
the rank. Their ideal closed-Hamiltonian dressed doublet is

\[
D(v)=|e_z\rangle v-
\sum_{j=x,y}|u_j\rangle G_j^{-1}
\langle e_j|H_{\rm hf}|e_z\rangle v,
\]

\[
D^\dagger D=\left[1+\frac{A^2}{4}
(|G_x|^{-2}+|G_y|^{-2})\right]I.
\tag{18}
\]

For I=1/2 this is an exactly isometric logical doublet after normalization.
NIST lists actual 6s7s and 6s8s singlet J=0 Yb levels [10]. That level
existence does not supply transition strengths, upper-state decay routing,
sideband excitation, laser isolation or a cooling cycle. We therefore
preserve (18) as a repair candidate and do not use it in the completed
renewal budget.

### 6.2 Cavity cooling uses a different entropy outlet

Established cavity sideband cooling [11,12] uses photon escape from a
resonator to remove motional energy. For far-detuned pi-polarized light on
the same admitted 171Yb ground manifold, the leading optical polarizability
is scalar by (13). Thus its force and desired cavity output can act on
motion without learning the nuclear spin. Raman scattering remains a
separate finite error, with ratio (14).

For a standard dispersive standing-wave model, let kappa be the cavity
**photon population** linewidth, Gamma the atomic population linewidth,
g_0 the antinode atom-cavity coupling, Delta_a the atomic detuning, n_c the
coherent intracavity occupation and eta_LD=k x_zpf. Around a maximum-gradient
position kx_0=pi/4,

\[
U_0\simeq g_0^2/\Delta_a,\qquad
G=U_0\sqrt{n_c}\eta_{\rm LD},\qquad
R_0\simeq\frac{\Gamma g_0^2n_c}{2\Delta_a^2}.
\tag{19}
\]

The linearized scalar interaction is hbar G(d+d^dagger)(b+b^dagger).
With red cavity detuning Delta_c=-omega,

\[
A_-=\frac{4G^2}{\kappa},\qquad
A_+=\frac{G^2\kappa}{(\kappa/2)^2+4\omega^2},\qquad
\gamma_c=A_--A_+.
\tag{20}
\]

Free-space recoil adds a nonnegative heating rate
H_rec=alpha_rec eta_LD^2 R_0, where alpha_rec is determined by the actual
emission and drive geometry. It must not be silently set to zero. Then

\[
\bar n_\infty=\frac{A_++H_{\rm rec}}{\gamma_c},\qquad
\bar n(t)=e^{-\gamma_ct}\bar n(0)
+(1-e^{-\gamma_ct})\bar n_\infty.
\tag{21}
\]

Defining C=4g_0^2/(kappa Gamma), the resolved-sideband limit gives

\[
\frac{R_0}{A_-}=\frac1{2C\eta_{\rm LD}^2},\qquad
\bar n_\infty\simeq
\left(\frac{\kappa}{4\omega}\right)^2+
\frac{\alpha_{\rm rec}}{2C}.
\tag{22}
\]

These relations derive a finite cooling floor from actual source parameters.
For a chosen cooling time, the nuclear Raman contribution per exposed atom
is at most R_R t. More detuning decreases that fraction, but reduces the
cooling rate at fixed power. Maintaining G requires increasing n_c as
Delta_a^2; optical power, trap shifts and saturation remain real resources.

Equations (19)-(22) are the dispersive, weak-coupling, Lamb-Dicke model, not
the full atomic/motional continuum. They require small electronic excitation,
G sufficiently below the cavity relaxation scale for rate elimination,
stable detuning, valid trap potentials and motion localized in the specified
geometry. The primary treatments retain interference and diffusion terms
when these simple limits are insufficient. Their linewidth conventions
differ; the population-linewidth convention above is fixed explicitly.

One force direction does not cool three arbitrary motional modes. The
actual routing/cavity/pump arrangement must address each required axis;
sequentially cooling isolated atoms with appropriate non-collinear forces
is one supplied model construction. A collective cavity force on several
atoms can leave relative modes dark. Arbitrary uninitialized cavity/source
states are also not supplied: the driven steady-state source and fresh
optical output reservoir are part of this replacement apparatus.

## 7. What remains reliable over repeated uses

### 7.1 A reference-uniform energy renewal law

For an admitted scalar cooler let N be total motional excitation and suppose
its complete adjoint channel obeys

\[
\mathcal C^*(N)\le rN+bI,\qquad0<r<1.
\tag{23}
\]

For (21), r=e^(-gamma_c t) and b=(1-r) n_infinity, summed over modes.
Equation (23) holds on all inputs and therefore with arbitrary reference
correlations; in a finite Fock cutoff, the omitted upper raising transition
only strengthens this particular energy inequality.

Suppose one routed use of gates, readout and waiting adds at most D in the
corresponding energy inequality. Repeating use then cooling gives

\[
M_{j+1}\le r(M_j+D)+b,
\qquad M_* =\frac{rD+b}{1-r}.
\tag{24}
\]

An initial M_0<=M_* remains inside this **mean-energy envelope** for every
number of uses. The constants D,r,b need the actual ramps, recoil and
heating model. This is a renewable domain, not an assumption of a freshly
prepared auxiliary on each gate.

### 7.2 Converting energy to a full operation guarantee

Let |0> be the unique admitted motional ground state and p the excited
weight after cooling. Since N>=I-|0><0|, p<=M. For an arbitrary joint state
rho_MR, comparison with |0><0| tensor tr_M rho gives

\[
\frac12\|\rho_{MR}-|0\rangle\langle0|\otimes\rho_R\|_1
\le\sqrt p+\frac p2\le\sqrt M+\frac M2.
\tag{25}
\]

Proof: first compare rho with its ground-ground block using the gentle
projection bound, then supply the missing positive R marginal of trace p.
This proof is a comparison argument, not an inserted energy measurement.

The square root cannot generally be replaced by p. An input
sqrt(1-p)|0,0_R>+sqrt(p)|1,1_R> has distance
[p+sqrt(4p-3p^2)]/2. If a **real** spin-independent operation has first
removed ground/excited coherence, the distance is exactly p. An assumed
projection or an uncharged random trap wait cannot supply that improvement.
In particular, with an arbitrary evolving correlated source, averaging
different wait times need not dephase the joint state: source frequencies
can cancel the motional phase. The completed cavity budget uses (25).

If the coarse physical record h reweights energy, apply these statements
to its unnormalized joint output, sum over h, and use Cauchy-Schwarz:
sum_h p_h sqrt(M_h)<=sqrt(sum_h p_h M_h). Thus the averaged envelope bounds
the full classical/quantum instrument without asserting that every rare
normalized history is cold. A conditional re-selection requires its own
acceptance denominator or an actual energy flag.

### 7.3 Complete operation and correlated-history composition

A conservative single-call bound is

\[
\begin{aligned}
\epsilon_{\rm call}\le{}& a+a^2
+\epsilon_{\rm presence}
+\epsilon_{\rm source}\\
&+\epsilon_{\rm orbital\ renewal}
+\epsilon_{\rm ramps,routing}
+\epsilon_{\rm bad\ molecular}\\
&+\epsilon_{\rm unwanted\ exchange}
+\epsilon_{\rm storage}
+p_{\rm abort}.
\end{aligned}
\tag{26}
\]

Here source and orbital renewal refer to actually supplied preparations,
not reconstruction of the retained source E. Every incident unwanted
coupling on the real admitted and leakage states is included in the
appropriate physical term. Scalar exchange between the wrong computational
particles is still a logical operation, just as in the prior common-frame
construction. Nuclear magnetic gradients and quantum-controlled rotations
are not made harmless by the J=0 label.

For L adaptive useful calls, a joint-channel hybrid bound sums these call
errors and the actual branch-weighted holding/abort contributions. No
independent retained bath is inserted between calls. Source-uniform loss
bounds and the cooler's actual source qualifications must hold on the
reachable histories or their violating weight must be explicitly charged.
At fixed nonzero imperfections this is a finite-accuracy, finite-computation
result. It is not a threshold theorem or unlimited accuracy through retries.

The full time is

\[
T_{\rm call}=T_{\rm route}+T_{\rm ramp}+T_{\rm loss}
+T_{\rm count}+T_{\rm cool}+T_{\rm fresh\ pair\ wait}
+T_{\rm output\ route}.
\tag{27}
\]

Stopping the active pair's work does not stop holding errors on the rest of
the register. Source renewal is paid only on the branches that use it, but
the data waiting for it remain physical.

## 8. A microscopic test of the prospective operating region

The PA audit supplies an actual local model rather than an assigned small
residual. For a weak resonant optical Feshbach transition with optical length
ell and a normalized orbital phi,

\[
\Gamma_D\simeq\frac{16\pi\hbar\ell}{m}\int|\phi|^4,
\quad\hbox{or}\quad
\Gamma_D=4\sqrt{2/\pi}\,\omega\ell/l
\tag{28}
\]

for an isotropic Gaussian with l=sqrt(hbar/(m omega)). The same real
molecular resolvent supplies both loss and coherent shifts. Missing excited
channels, returning products and the escaping-pair fraction are not hidden
inside Gamma_D.

The concrete scalar trap V(x)/(hbar omega)=1/2(|x|/l-2.45)^2 has, in a
converged finite-grid calculation,

\[
t/(\hbar\omega)=0.00346017,
\qquad\Delta_{\rm orb}/(\hbar\omega)=0.956431.
\]

Taking g=sqrt(2)t/hbar and Gamma=2g gives Gamma/omega=0.00978684. At
omega/(2pi)=100 kHz, the selected 2009 molecular-line model gives

| Quantity | Model result |
|---|---:|
| Orbital length | 24.31 nm |
| Site separation | 119.13 nm |
| Pair-loss rate | 6149/s |
| PA intensity | 1.680 mW/cm^2 |
| Per-atom Rayleigh rate | 0.16084/s |
| Per-atom Raman rate | 0.09933/s |
| Sufficient loss window for q=10^-6 | 28.59 ms |
| Two-atom Raman exposure in that window | 0.005680 |

The intensity and molecular data are model inputs from [5]; the hyperfine
value used for the atomic correction is from [13]. No precision enclosure
for the continuum/grid approximation is claimed. The theoretical and
measured molecular-line positions differ and are not mixed to assert a
spectral gap.

The loss window obeys Gamma T=12.5 log(9/(7q)). The nominally small atomic
hazard per unit Gamma therefore becomes relevant over a complete measurement.
This sufficient bound alone does not establish that the physical device must
incur that exposure. An equally informed conventional controller may exploit
a tighter source box, nominal dynamics or ordinary coherent transfer.

The p-wave contact was also calculated from the actual orthonormal band
orbitals, using the Wronskian w_L' w_R-w_L w_R'. Its geometry factor is
2.4620e-4, 3.35 times the naive separated-Gaussian estimate. Four published
nearby molecular lines give a small conditional diagnostic after this
suppression, but the list is not a complete wrong-sector spectrum. Neither
the orbital gap nor those four lines certify the full molecular instrument.

Most decisively, the selected 119-nm double-well profile is an admitted
Hamiltonian, not an earned optical source. Tightening the trap improves the
atomic-loss ratio but makes that geometry and finite molecular range more
problematic. Lowering laser intensity does not improve the Raman/loss ratio
because both scale linearly with intensity. Thus no joint physical window
is claimed from this table.

## 9. Comparators receive the same useful machinery

### Existing singlet, spin/charge and optical-Feshbach operations

The published singlet/triplet computation results [2,3] already supply the
universal consumer. Conventional spin-to-charge conversion can use better
calibrated coherent or adiabatic control when that information is available.
The earlier charge-return compiler preserves particles and works with a
different retained-source promise. The present loss construction needs a
new sink, fresh atoms and motional renewal; its one-window count establishes
no speed advantage by itself.

Ordinary optical-Feshbach exchange gates receive the same optical lengths,
trap control, cooling and improved source knowledge. They deliberately
operate at a different loss/phase tradeoff. The new complete-instrument
guarantee concerns resonant singlet consumption and reference-preserving
replacement, not a discovery of the PA selection rule.

### A stronger demonstrated optical operation stack

Broker/client networks prepare a Bell resource on disposable interfaces
before contacting retained data [14]. A Bell pair ab, CNOT A->a and CNOT
B->b, followed by Z outcomes x,y, has Kraus operator
P_(x xor y)/sqrt(2). It preserves both parity sectors, including references.
The complete construction and exact Pauli-resource-error formulas are in
`alternative/ALTERNATIVE.md`.

Main and colleagues' mixed-species ion experiment is a substantially stronger
physical operation-stack benchmark than isolated component fidelities [15].
It demonstrated repeatable teleported entangling gates. Its source schedule
included frequent recooling; the reported effective Bell rate was 9.7/s and
complete teleported CZ average gate fidelity 86.1(9)%. Those are original
experimental metrics, not diamond-norm certifications or predictions for our
parity protocol.

An exact waiting-law obstruction applies to this comparator and our fresh
singlet factory alike. If each source interval preserves a retained sector
coherence by lambda and succeeds with probability p, then at success

\[
g=\mathbb E[\lambda^N]=\frac{p\lambda}{1-(1-p)\lambda}.
\]

For independent Poisson production rate r and Markov coherence decay Gamma,

\[
g=\frac r{r+\Gamma},\qquad
\epsilon_{\rm hold}=\frac{\Gamma}{2(r+\Gamma)}.
\tag{29}
\]

After k repeated renewals, that coherence is g^k in this model. Ideal
purification requiring n serial raw pairs gives g<= [r/(r+Gamma)]^n before
its gate times or failures. Better resource fidelity alone can therefore
erase the unknown quantum information while it waits. Multiplexing,
protected storage and correction are real improvements, with real hardware.

### Why geometric dilution was not selected as the complete answer

The accompanying screening audit derives an L^-2 clock shared by smooth
screened matrix elements and an appropriately cooled SET rate model. It
also finds the limitations of extending that clock to a device:

* The screened Coulomb cusp persists. In strict two dimensions its q^-6
  momentum tail invalidates a naive sixth-moment bound [16]. Finite
  low-energy expectation is not a cubic-SOC norm certificate.
* Coulomb energy divided by orbital gap approaches a constant; dilation
  does not supply one-band admission.
* A fixed added amplifier noise floor can make readout time grow as L^4.
  A thin conducting screen has a different noise scaling from bulk metal.
* Fixed-thickness island electron-phonon cooling is insufficient to renew
  the detector on the proposed L^2 clock without an additional heat path.
* Noncollective nuclear fields can accumulate more strongly as the cycle
  slows.

These are failed sufficient routes, not proofs that the original dressed
spin construction is impossible. A full dressed Coulomb/scattering
calculation may distinguish harmless resonance renormalization from true
within-sector disturbance more sharply than a raw unbounded-operator norm.

## 10. What has been earned, and what remains physical

The completed capability is a source-qualified singlet/triplet instrument
whose accepted singlet branch is renewable by particle replacement, with a
tight law explaining why the same trick cannot erase the triplet. Its
uniform progress proof keeps both charge paths and arbitrary common forward
source evolution. Actual molecular, detector and cooling mechanisms are
connected to their relevant rates and domains, and repeated use has an
explicit energy and joint-history analysis.

The remaining device bridge is narrower and testable in a physical model:
an actually generated trap must have its complete trapped Franck-Condon
matrix, loss-product branching, wrong-sector molecular spectrum, source
noise and all-mode cooling/readout rates computed together. The current
numbers do not establish that bridge. The next improvement should reduce
the whole operation's Raman/holding exposure or replace that molecular
interface; adding more blind repetitions is not a solution at fixed rates.

## Executable work

Run from the workspace, without network access:

    OPENBLAS_NUM_THREADS=1 python p2_operating/renewal_check.py
    OPENBLAS_NUM_THREADS=1 python p2_operating/detector/pair_loss_check.py
    OPENBLAS_NUM_THREADS=1 python p2_operating/detector/cooling_rank_check.py
    OPENBLAS_NUM_THREADS=1 python p2_operating/scaling_audit/scaling_checks.py
    OPENBLAS_NUM_THREADS=1 python p2_operating/scaling_audit/pa_checks.py
    OPENBLAS_NUM_THREADS=1 python p2_operating/alternative/verify_alternative.py

The root script checks the singlet replacement Kraus identity, tight
memory-dimension channel, exact scalar absorber instrument norm, cooling
population-versus-coherence distinction, adjoint energy inequality,
repeated-use envelope and cavity/detector resource relations. The physical
audits preserve their model parameters and approximation limits. Exact
rational certificates are identified separately from floating matrix and
grid consistency checks.

## Primary sources

1. Terhal and Horodecki, Schmidt number for density matrices,
   https://doi.org/10.1103/PhysRevA.61.040301 ; https://arxiv.org/abs/quant-ph/9911117
2. Freedman, Hastings, Shokrian Zini, Symmetry Protected Quantum Computation,
   https://arxiv.org/abs/2105.04649
3. Rudolph and Virmani, The two-qubit singlet/triplet measurement is universal
   for quantum computing given only maximally-mixed initial states,
   https://arxiv.org/abs/2107.03239 ; https://doi.org/10.1038/s41467-023-43481-y
4. Dynamics of Ultracold Quantum Gases in the Dissipative Fermi-Hubbard Model,
   https://arxiv.org/abs/1805.11853
5. Reichenbach, Julienne and Deutsch, Controlling nuclear spin exchange via
   optical Feshbach resonances in 171Yb, https://arxiv.org/abs/0905.4556
6. Coherence Preserving Leakage Detection and Cooling in Alkaline Earth Atoms,
   https://arxiv.org/abs/2410.23430
7. Realization of a SU(2) x SU(6) system of fermions in a cold atomic gas,
   https://arxiv.org/abs/1005.3670
8. Degenerate Bose-Fermi mixtures of rubidium and ytterbium,
   https://arxiv.org/abs/1506.08705
9. Reichenbach and Deutsch, Sideband Cooling while Preserving Coherences in
   the Nuclear Spin State in Group-II-like Atoms,
   https://doi.org/10.1103/PhysRevLett.99.123001
10. NIST, Energy Levels of Neutral Ytterbium,
    https://physics.nist.gov/PhysRefData/Handbook/Tables/ytterbiumtable5.htm
11. Zippilli and Morigi, Mechanical effects of optical resonators on driven
    trapped atoms: Ground state cooling in a high finesse cavity,
    https://arxiv.org/abs/quant-ph/0508075
12. Cooling the motion of a trapped atom with a cavity field,
    https://arxiv.org/abs/1208.5942
13. Intercombination line frequencies in 171Yb validated with the clock
    transition, https://arxiv.org/abs/2303.08421
14. Benjamin et al., brokered graph-state architecture,
    https://arxiv.org/abs/quant-ph/0509209
15. Main et al., Distributed quantum computing across an optical network
    link, https://arxiv.org/abs/2407.00835 ;
    https://doi.org/10.1038/s41586-024-08404-x
16. Hofmann, Barth and Zwerger, Short-distance properties of Coulomb systems,
    https://arxiv.org/abs/1304.2891

Supporting primary methods and complete derivations are linked in the
detector, alternative and scaling-audit notes. No outreach or external
write was performed; all research retrieval was read-only.
