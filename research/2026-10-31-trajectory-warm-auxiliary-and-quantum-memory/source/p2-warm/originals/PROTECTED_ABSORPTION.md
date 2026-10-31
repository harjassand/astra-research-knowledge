# A warm auxiliary system can supply a sharp quantum instrument

Working construction, 31 October 2026. This is the strongest result reached
in the present continuation. `OPERATING_THEORY.md` preserves the preceding
rank-dependent renewal law, full-charge loss theorem, exact nuclear-spin
readout calculation and the initial, stronger orbital-reset requirement.
The theorem here removes that reset requirement when the actual microscopic
instrument has the stronger symmetry specified below.

## Central consequence

An auxiliary system need not be prepared to the target logical accuracy
after every operation. It can remain warm, correlated with retained sources,
and affected by unsuccessful attempts. What is needed is:

1. Every actual fine history preserves the useful quantum information inside
   each retained measured sector.
2. A physical renewal channel supplies an energy drift toward states from
   which the requested outcome has a nonzero probability.
3. Unsuccessful attempts have a bounded energy cost in the same observable.

These conditions yield an exponentially accurate instrument from a cooler
with a **constant nonzero energy floor**. The proof tracks survival and
unnormalized energy together, so it includes the tendency of null results
to select hotter states. A low mean energy asserted only before conditioning
would not suffice.

For two nuclear spins, the construction supplies a singlet-consuming,
triplet-preserving measurement with a physical route back to addressable
particles. Singlet/triplet measurements already have an established
universal computational consumer [1,2]. The new result concerns the physical
instrument and its auxiliary-state requirement, not a new proof of that
universality and not a demonstrated fault-tolerant device.

The finite-tolerance result is exact in its declared scalar model. Raman
scattering, spin-dependent molecular terms, spectator exchange, imperfect
sources and finite control domains remain actual errors. More retries do
not remove those terms.

## 1. Strong microscopic symmetry protects all orbital states

For exactly two identical spin-1/2 fermions,

\[
\mathcal H_2=
(V_0\otimes\mathcal H_+)
\oplus(V_1\otimes\mathcal H_-).
\tag{1}
\]

V_0 is the one-dimensional spin singlet, V_1 the three-dimensional triplet,
and H_+,H_- are the symmetric and antisymmetric spatial/source spaces.
Exchange symmetry here concerns the full orbital wavefunction, not an
assumed single spatial coordinate or one-orbital projection.

Require each actual Hamiltonian and each resolved environmental interaction
to be a scalar on the nuclear spins. Schur's lemma then gives, on the
two-particle branches,

\[
K_h=P_s\otimes F_{s,h}+I_{V_1}\otimes F_{t,h}.
\tag{2}
\]

Every orbital level may be occupied. Motion can exchange entropy with a
source or detector. Neither process can resolve an orientation within V_1.
The F operators can be noncommuting maps on arbitrary retained sources,
including systems initially correlated with the data and a reference.
Here the claim is the joint factorization (2). A record can still steer
pre-existing spin/source correlations by measuring the source. It need not
leave every normalized conditional spin marginal unchanged. For fixed
auxiliary input, no new dependence on triplet orientation is introduced.

This is **strong symmetry of the actual fine instrument**. Covariance of
an averaged channel is weaker: isotropic spin depolarization is covariant
and still destroys triplet information. A spinful environment can absorb
angular momentum even when the total Hamiltonian is rotationally invariant.
Individual atom loss and unwanted p-wave pair loss do not satisfy (2).

The local pair annihilator

\[
\psi_\downarrow(x)\psi_\uparrow(x)
\tag{3}
\]

is a spin singlet and annihilates the **entire** triplet space, not just
triplets in a one-orbital model. A finite-range kernel also works if the
actual kernel is spin singlet. Full molecular hyperfine channels must not
be replaced by that assumption without calculation.

After conclusive singlet consumption, supplying a real fresh singlet gives

\[
(|s\rangle\langle\mathrm{vac}|\otimes G_k)
(|\mathrm{vac}\rangle\langle s|\otimes F_h)
=P_s\otimes G_kF_h.
\tag{4}
\]

Thus the destructive event implements the correct rank-one branch, including
all reference correlations. The triplet cannot be erased and classically
reloaded: preserving a rank-r unknown state through a k-dimensional quantum
bottleneck incurs worst-case half-diamond error at least 1-k/r. The preceding
note proves and saturates this standard Schmidt-number-based bound [3].
For the triplet and no retained quantum memory, the floor is 2/3.

### Continuity with the common-frame construction

A common static classical spin frame still conjugates a complete physical
instrument. Local singlet annihilation is invariant under its SU(2)
determinant. Spin-scalar density forces and detection retain the same
covariance. A finite-range bare pair source is not automatically invariant
under different local frames at its endpoints. Drifting or quantum-controlled
spin rotations remain outside the static-frame theorem. The present
nuclear-spin candidate uses J=0 electronic states to seek the required
scalar physics directly; it does not grant an arbitrary quantum spin
connection or a source reset.

## 2. Exponential absorption with a nonzero cooling floor

The following theorem is independent of the atomic architecture. Restrict
the progress calculation to the sector intended to be absorbed. Let E
include all retained sources and orbital variables. Let N>=0 be its energy
or excitation observable, and P a useful low-energy subspace satisfying
N>=I-P.

One cycle consists of a trace-preserving renewal channel C followed by a
physical accepted/unsuccessful instrument. Write F for its unsuccessful
map and A=I-F*(I) for the accepted effect. Assume the **operator** bounds

\[
\begin{aligned}
&0\le A\le I,\qquad PAP\ge p_0P,\qquad p_0>0,\\
&\mathcal C^*(N)\le rN+bI,\qquad 0\le r<1,\\
&\mathcal F^*(N)\le uN+dI,\qquad u,d\ge0.
\end{aligned}
\tag{5}
\]

They apply to the actual source domain after allowed histories. They do
not require a prepared source state, an independently redrawn bath or a
thermal initial orbital distribution. The coefficients must come from the
physical channel, not the name of a cooler.

### 2.1 A sharp effect-to-energy inequality

For every 0<c<p_0,

\[
\boxed{A\ge cI-\beta N,\qquad
\beta=\frac{c(1-c)}{p_0-c}.}
\tag{6}
\]

Proof: write A in P,Q=I-P blocks as [[B,X],[X^dagger,D]]. Positivity and
A<=I give B>=p_0 I, D>=X^dagger B^(-1)X and
XX^dagger<=B(I-B). The Schur complement of
A-cI+beta Q is bounded below by

\[
(\beta-c)I-
cX^\dagger[B(B-cI)]^{-1}X.
\]

The final operator has norm at most c(1-p_0)/(p_0-c), using the preceding
XX^dagger inequality. The chosen beta makes the Schur complement positive.
Replacing Q by N preserves the inequality. The bound is sharp already for
a rank-one effect onto sqrt(p_0)|P>+sqrt(1-p_0)|Q>.

The first derivation used a valid but weaker Young-inequality coefficient.
Keeping A<=I improves the allowable warm floor substantially. Both proofs
and the correction are preserved in the independent audit.

### 2.2 Track survival and energy without renormalizing null histories

For an unnormalized surviving state rho, set

\[
q=\operatorname{tr}\rho,\qquad n=\operatorname{tr}(N\rho).
\]

Applying (5)-(6) gives the positive recurrence

\[
\binom{q'}{n'}\le
M\binom qn,\qquad
M=\begin{pmatrix}
1-c+\beta b&\beta r\\
ub+d&ur
\end{pmatrix}.
\tag{7}
\]

The exact condition rho(M)<1 for this nonnegative two-by-two comparison
matrix is

\[
\boxed{ur<1,\qquad c(1-ur)>\beta(b+rd).}
\tag{8}
\]

A directly usable positive weight is any alpha with

\[
\frac{\beta r}{1-ur}<\alpha<
\frac{c-\beta b}{ub+d},
\]

with the usual limiting interpretation for a zero denominator. Set

\[
\lambda=\max\left\{
1-c+\beta b+\alpha(ub+d),\quad
ur+\frac{\beta r}{\alpha}\right\}<1.
\]

Then

\[
q_k+\alpha n_k\le
\lambda^k(q_0+\alpha n_0).
\tag{9}
\]

Every reference can be included in rho because the hypotheses are operator
inequalities. The retained source evolves throughout C and F. Different
classical histories can use different physical maps if they share this
positive contraction weight and a uniform lambda<1. Individually stable
history-dependent matrices do not by themselves give that guarantee.

There exists some c in the sharp family (6) satisfying (8) precisely when

\[
ur<1,\qquad b+rd<p_0(1-ur).
\tag{10}
\]

This characterizes existence of this certificate. It is not a necessary
condition for every particular physical absorber.

### 2.3 The useful finite tolerance

For a cooler with floor n_infinity,
b=(1-r)n_infinity. If the unsuccessful window has u=1,d=0, condition (10)
becomes simply

\[
\boxed{n_\infty<p_0.}
\tag{11}
\]

The required floor does not shrink with the requested measurement error.
With finite heating d or u>1, taking a longer renewal interval reduces r.
If the physical limiting floor satisfies n_infinity<p_0, finite d and u
can still be accommodated by sufficiently small r. The extra cooling time
and its spin-breaking exposure remain physical costs.

One rational comparison box is

\[
p_0=4/5,\quad r=b=d=1/20,\quad u=1.
\]

Choose c=2/5, beta=3/5, alpha=1/20 and lambda=13/20. Exact arithmetic gives

\[
\boxed{q_k\le(1+E/20)(13/20)^k}
\tag{12}
\]

for normalized input mean energy at most E. Its cooler floor is 1/19.
This is a rigorous coarse mathematical box, **not a set of assigned tiny
device errors**. The physical calculations below explain which rates and
energy costs would have to supply it or another valid box.

### 2.4 Earn a nonzero accepted effect from local microscopic bounds

The good-subspace probability in (5) need not be assumed from a nominal
cold-state decay rate. Here is a finite-window construction using the same
forward-source reasoning as the earlier local-orbit work. Set hbar=1 in
this paragraph. In the absorbing sector let the actual no-event propagator
obey dot K=(-iH-J/2)K, where J is the total accepted jump-rate operator.
Suppose, throughout the window and on the actual source domain,

\[
0\le J(t)\le j_+I,\qquad PJ(t)P\ge j_-P,\qquad
\|QH(t)P\|\le v,\qquad Q=I-P.
\tag{12a}
\]

Take H_0=PHP+QHQ and its forward unitary U_0. Then U_0 preserves P.
Duhamel's formula, contractivity of K, and bounded off-diagonal coupling
give

\[
\|(K(t)-U_0(t))P\|\le wt,\qquad w=v+j_+/2.
\]

Consequently, for any unit vector in P including any source/reference
state, the norm of the accepted jump amplitude is at least
sqrt(j_-)-sqrt(j_+)wt while this expression is positive. Since
A_T=I-K(T)^\dagger K(T)=integral K(t)^\dagger J(t)K(t)dt,

\[
\boxed{PA_TP\ge p_0(T)P,\qquad
p_0(T)=j_-T-\sqrt{j_-j_+}\,wT^2+\frac{j_+w^2T^3}{3}>0}
\tag{12b}
\]

for 0<T<=sqrt(j_-)/(sqrt(j_+)w). For longer T, the integral of the
positive-part lower amplitude remains a valid saturated lower bound.
The block-diagonal Hamiltonian and its propagator must exist on their
stated domains; the bounded-cross-block hypothesis is the substantive
regularity condition. P must preserve the relevant domain, and the bound
must hold on all forward U_0(t,s)P images, not only the actual no-event
trajectory. No inverse evolution is a control instruction.

A common source Hamiltonian commutes with P and does not enter v. The
source may be fast and may fail to commute with the jump-rate operators.
This does not remove the finite-bandwidth qualification needed to derive
the jump model from a real absorbing reservoir.
The formula above first treats Hamiltonian evolution and accepted loss.
There is a safe extension to unresolved non-accepted jumps L_alpha.
If R=sum L_alpha^\dagger L_alpha<=ell_+ I, use the zero-all-jumps
propagator K_0 generated by -iH-(J+R)/2. The accepted effect dominates
integral K_0^\dagger J K_0 dt: these are the trajectories whose first event
is an accepted loss. The same polynomial lower bound therefore holds with

\[
w=v+(j_++\ell_+)/2.
\tag{12c}
\]

Here I-K_0^\dagger K_0 counts all first events and must not be identified
with accepted loss alone. A finite ell_+ is a real domain qualification.
As a counterexample to omitting it, take P=|0><0|, J=jP, H=0 and an
unobserved scalar orbital jump sqrt(ell)|1><0| into a dark state. Actual
acceptance is j[1-exp(-(j+ell)T)]/(j+ell). At j=T=1, ell=100 it is
approximately 0.00990; the incorrect jump-free polynomial would claim
7/12. Spin opacity does not make motional jumps irrelevant to progress.

For example, a finite molecular form factor gives
J=|f><f| tensor Gamma_E with normalized f and
gamma_- I<=Gamma_E<=gamma_+ I. If P=|phi_0><phi_0| tensor I, then
j_-=gamma_- |<f,phi_0>|^2 and j_+=gamma_+. The unsuccessful energy cost
also depends on ||Nf||, as in section 6. Thus overlap and form-factor
regularity, together with the real ramp/source cross coupling v, supply
both progress and heating qualifications. A contact delta distribution
does not supply these finite bounds.

### 2.5 From absorption to the full quantum instrument

Strong sector opacity is essential here. On the retained triplet the
unsuccessful history remains I_3 tensor a source map. On the singlet the
remaining dilation amplitude has squared norm bounded by q_k on the
energy-constrained input. Accepted singlet histories followed by replacement
already have (4).

First work in the exact scalar model with complete replacement and return
maps. All abort/failure maps must be retained until they are charged in
the explicit error terms below; discarding them would invalidate trace
preservation.

A comparison ideal singlet branch can include a single input-independent
CP completion of the missing weight. Let B_k be the actual accepted and
replaced map and N_k the final no-event map. Define the comparison singlet
output as B_k(P_s rho P_s)+R_s N_k(P_s rho P_s), with a fixed CPTP output
embedding R_s; define its triplet output as N_k(P_t rho P_t), including the
matched return map. Original instrument completeness makes this comparison
trace preserving. It is logical identity inside each measured sector
jointly with an allowed source channel, not identity return of the source.
No bounded inverse, input-dependent completion or physical source reset is
used. The wrong-label weight costs q_k and the remaining singlet/triplet
cross block costs at most sqrt(q_k). Therefore

\[
\epsilon_{\rm ST,E}\le\sqrt{q_k}+q_k
+\epsilon_{\rm number}
+\epsilon_{\rm replacement}
+p_{\rm return\ timeout}
+\epsilon_{\rm physical}.
\tag{13}
\]

The first term cannot generally be replaced by q_k. Even the scalar model
has exact half-diamond error sqrt(q)/(2-sqrt(q)). Reporting a timeout as an
explicit abort instead has a linear tail cost when early branches and the
eventual completion are matched; labeling an unresolved coherent branch
as triplet is the reason for the square root in (13).

No individual normalized null history is asserted to remain cold. Some
can be very hot. Equations (7)-(9) bound their complete joint weight and
their chance of delaying the operation. That is the distinction which
allows the theorem to cover arbitrary retained-source correlations.

## 3. Full orbital protection creates an addressability problem

Higher orbitals let two triplet atoms occupy the same physical port in
different modes. Spin opacity does not put them back into two usable ports.
The earlier one-orbital Pauli argument cannot simply be reused here.

The replacement below earns a return mechanism in an admitted one-dimensional
trap. Transverse excitation is excluded by a real confinement/domain
condition. Arbitrary three-dimensional orbitals require additional mixing
and cooling; independent two-phonon coolers preserve several relative
parities and are not a complete repair.

## 4. A physical two-force cooler for the retained pair

Merge the selected pair in a scalar harmonic longitudinal trap. On the
triplet, neglecting the separately budgeted non-scalar molecular corrections,
the spatial state is an antisymmetric two-fermion state. Let a and b denote
centre-of-mass and relative annihilation operators. Put

\[
Q=a^2+b^2,\qquad N=N_a+N_b.
\]

The two source operators needed are actual density moments:

\[
\sum_i x_i\ \longrightarrow\ a+a^\dagger,
\qquad
\sum_i x_i^2\ \longrightarrow\ Q+Q^\dagger+2N+2.
\tag{14}
\]

A cavity mode at nonzero intensity gradient supplies the first force. A
separate mode at an extremum supplies the quadratic force. Driving their
red one- and two-phonon sidebands, with independent output reservoirs or
justified frequency separation, yields the established optical mechanisms
behind

\[
\mathcal L_-=\gamma_1\mathcal D[a]+\gamma_2\mathcal D[Q].
\tag{15}
\]

Linear cavity cooling and quadratic two-phonon cooling are established
methods [4-6]. The pair construction uses them together to remove a dark
relative-motion obstruction while preserving the spin irrep. It does not
assume access to a logical spin operator as an actuator.

Linear force alone cannot cool relative motion. Quadratic force alone has
additional dark superpositions. Together their common kernel is

\[
|0_a\rangle\otimes\operatorname{span}(|0_b\rangle,|1_b\rangle).
\tag{16}
\]

Exchange parity selects the unique odd target |0_a,1_b> for every triplet
orientation. The spin-one factor remains untouched.

### 4.1 An energy-decay proof, not just a dark-state assertion

On odd relative parity the following global ideal-generator inequality
holds:

\[
\boxed{N_a+Q^\dagger Q\ge\tfrac14(N-1).}
\tag{17}
\]

At fixed total number n, set x=<N_a>,
A=<N_b(N_b-1)> and B=<N_a(N_a-1)>. Then
A-B=(n-1)(n-2x), A+B<=n(n-1). If x>=(n-1)/4 the result is immediate.
Otherwise

\[
\|Q\psi\|^2\ge(\sqrt A-\sqrt B)^2
\ge\frac{(n-1)(n-2x)^2}{2n}
\ge\frac{n-1}{2}.
\]

All terms preserve total number, so the blockwise argument proves (17).
It gives

\[
\mathcal L_-^*(N-1)
\le-\tfrac14\min(\gamma_1,2\gamma_2)(N-1).
\tag{18}
\]

The even relative sector has the conservative counterpart
N_a+Q^dagger Q>=N/8, with unique |0_a,0_b> target in the noninteracting
model. Background singlet interactions change the actual even-sector
cooling rates/domain and must enter its qualification; they do not break
spin opacity merely by being scalar.

### 4.2 Finite sideband heating gives the required nonzero floor

Include blue channels gamma_1+ D[a^dagger] and gamma_2+ D[Q^dagger], with
red rates gamma_1-,gamma_2-. Since [Q,Q^dagger]=4(N+1), define

\[
k_0=\tfrac14\min\{\gamma_{1-}-\gamma_{1+},
2(\gamma_{2-}-\gamma_{2+})\},
\quad k=k_0-8\gamma_{2+},
\quad h=\gamma_{1+}+16\gamma_{2+}.
\]

For E=N-1 and k>0,

\[
\mathcal L^*E\le-kE+hI,
\qquad
\mathcal C_t^*E\le e^{-kt}E+
\frac hk(1-e^{-kt})I.
\tag{19}
\]

Actual recoil heating adds to h; source-induced multiplicative heating
reduces the net k. The even-sector formula uses its 1/8 coefficient and
constant gamma_1+ +8 gamma_2+. Equation (19) is the required adjoint drift,
uniform over references and initial orbital states in the model. It does
not assume an initially thermal distribution.

For a cavity population linewidth kappa, the familiar resolved-sideband
blue/red ratio for an m-phonon transition is approximately
[kappa/(4m omega)]^2. This gives a physical route to k>0. It does not make
the recoil term or the quadratic coupling inexpensive.

At an antinode, with atomic detuning Delta, single-atom coupling g_0,
intracavity population n_c and eta_LD=k_L x_zpf,

\[
G_2\simeq\frac{g_0^2}{\Delta}\sqrt{n_c}\eta_{\rm LD}^2,
\qquad \gamma_{2-}\simeq\frac{4G_2^2}{\kappa}.
\tag{20}
\]

For the two atoms, the free-space Rayleigh rate is approximately
R_pair=2 Gamma g_0^2 n_c/Delta^2. With
C=4g_0^2/(kappa Gamma),

\[
\boxed{\frac{R_{\rm pair}}{\gamma_{2-}}
\simeq\frac{2}{C\eta_{\rm LD}^4}.}
\tag{21}
\]

This is a substantive cost. Two-phonon cooling is slower in the Lamb-Dicke
parameter, and its free-space recoil can dominate without sufficient
cooperativity. Nuclear Raman is a fraction zeta of that rate in the
admitted far-detuned model. At fixed power, more detuning slows cooling;
holding G_2 fixed requires n_c proportional to Delta^2. The photon source,
power, AC shifts, saturation and finite electronic spectrum are included
resources. No arbitrary initial quantum state of those drive lasers is
asserted to give the same cooler.

The merged pair requires its full two-atom optical response. The scalar
single-atom hyperfine resolvent does not by itself justify replacing that
response by a sum of independent atomic polarizabilities near contact.
Molecular and collective electronic channels of the cooling fields must
also enter the spin-breaking remainder and the force/heating bounds.
This is part of the same unresolved microscopic join as the absorbing
field; the cavity model is not a completed material-specific qualification.

The ideal oscillator coercivity is global. Its physical derivation from
the standing-wave cavity is a finite Lamb-Dicke and electronic-domain
approximation. Validity of that approximation over the actual moment/tail
envelope must be supplied. Strong scalar symmetry continues to protect
spin outside the linearized motional model, but its cooling progress need
not remain the one predicted by (19).

## 5. Returning two usable particles without measuring their spin

The odd target |0_a,1_b> is the Slater determinant filling the lowest two
one-particle orbitals. Split the scalar trap into two wells while preserving
a gap from that occupied two-dimensional subspace to the unoccupied modes.
Any unitary inside the filled subspace contributes only its determinant
phase. The exponentially small final splitting between its two occupied
modes is therefore not the adiabatic bottleneck.

At the endpoint, that occupied subspace must actually approximate the span
of one localized orbital at each output port. It then contains one particle
per port. Gap bounds, ramp speed, localization tails and source-force noise
are real properties of the potential path, not consequences of Schur's lemma.

With finite cooling floor, use finite cool/split intervals and scalar
occupancy heralding. Stop on one particle at each port. On failure, merge
and try again. All these actual histories act as identity on the triplet
orientation; an unsuccessful spatial return has not measured its qubit.
The same theorem (5)-(10) applies to this return instrument, now using the
odd spatial target as P and including the real rejected-ramp energy cost.
Finite caps produce an explicit return-abort probability.

For the combined measurement, vacuum is the conclusive singlet branch and
receives a fresh singlet. Two-particle one-per-port is the usable retained
branch. Single-particle events are faults, not valid triplet outputs.
Presence tests can be done after separation so the established single-atom
scalar fluorescence calculation is not silently extrapolated to an
overlapping radiating pair. Any needed number discrimination beyond presence
must be supplied by the detector's actual rates and charge domain.

### Physical source and detection

The ground-state 171Yb weak-drive pi-polarized detector has exact admitted
hyperfine-resolvent jumps L_0 proportional to I and Raman jumps proportional
to sigma_+ and sigma_-; the full formulas are in `OPERATING_THEORY.md`.
Rayleigh recoil can change orbital progress, while Raman changes spin.
Counting accuracy, dark counts, collection efficiency, optical power and
readout duration are separately charged. The prior scalar-effect identities
are used at their actual hypotheses, not merely at the level of outcome
probabilities.

A fresh-pair factory fills one real orbital from a qualified cold Fermi
source, isolates it, splits it and accepts only a presence record at both
outputs. Double filling of one orbital is uniquely a singlet. A classical
splitter with p in [1/4,3/4] has separation probability at least 3/8,
conditional on double filling. Operator-controlled splitting requires its
actual two-particle bound instead. Source preparation, rejected loads,
finite particle capacity and waiting-data errors remain in the operation.

## 6. Earn the unsuccessful window's energy cost

A sink can heat the surviving branch. In particular, u=1,d=0 does not
follow merely because accepted events remove particles.

For an explicit smooth local no-loss rate j(x)>=0 and relative kinetic
energy p^2/(2mu),

\[
-\tfrac12\{j,p^2\}=-p j p+\frac{\hbar^2}{2}j''.
\tag{22}
\]

In a scalar harmonic trap, N=H_osc/(hbar omega)-1/2 consequently has the
safe adjoint bound

\[
\mathcal L_{\rm no}^*N\le
\left[\frac{\|j\|}{2}
+\frac{\hbar\|j''\|}{4\mu\omega}\right]I.
\tag{23}
\]

For duration T this supplies u=1 and d=T times that actual curvature
coefficient, before adding drive/ramp terms. A literal delta-function loss
does not satisfy it. A molecular Franck-Condon kernel is generally nonlocal
and needs its corresponding form calculation. For a bounded rank-one
effect Gamma|f><f| with f in the domain of N, the anticommutator energy
term is bounded by Gamma||Nf||; finite molecular range therefore enters the
actual d rather than being discarded.

For general controls, an operator-form inequality
i[H,N]+sum_j D[L_j]^*(N)<=hN+kI integrates to an explicit u,d. A common
source Hamiltonian acting only on E commutes with N and drops out; spatial
force or form-factor bounds remain. This is the appropriate use of the
earlier local-regularity principle. It does not equate finite orbital energy
with arbitrarily high momentum regularity.

## 7. Reuse across computations, rather than only one successful call

The survival-energy theorem controls tails and occupied work in the sector
intended to absorb. For a fixed cycle time tau and input energy E,

\[
\mathbb E[\hbox{number of active cycles}]
\le\frac{1+\alpha E}{1-\lambda}.
\tag{24}
\]

This is the absorbing-sector hitting-time bound, or the corresponding
occupied-apparatus work bound when the loss is not monitored. It is not the
wall-time bound for a complete singlet/triplet measurement: a surviving
triplet needs the full k-cycle cap. If no actual event detector supplies an
early stop, the controller and optical sources also run for that full cap,
even after an unobserved loss. A final number readout can avoid repeated
readout overhead, but does not grant observed early stopping. Holding costs
on all waiting data are charged for the actual elapsed schedule.

It also bounds retained output energy when the actual accepted map has
G*(N_out)<=u_A N+d_A I. If G follows cooling, its contribution at cycle j
is at most

\[
(u_A b+d_A)q_j+u_A r n_j.
\]

Summing gives a finite, explicit bound

\[
E_{\rm out}\le
\begin{pmatrix}u_A b+d_A&u_A r\end{pmatrix}
(I-M)^{-1}\binom{q_0}{n_0}.
\tag{25}
\]

For stopped branches, subsequent holding work must be added. The accepted
source/return detector must supply u_A,d_A; a sharp fictitious spatial
projection is not a physical energy bound.

Equation (25) bounds the accepted absorbing branch, not by itself the
complete measurement output. For a triplet whose no-event window obeys
F_t^*N<=u_t N+d_t I, the full cap instead gives

\[
n_{t,k}\le (u_t r)^k n_{t,0}
+(u_tb+d_t)q_t\sum_{\ell=0}^{k-1}(u_t r)^\ell .
\tag{25a}
\]

Use the appropriate nonnegative excitation observable in each sector:
N_osc in the even harmonic sector, N_osc-1 in the odd sector. The r,b
appearing in (25a) mean a bound actually valid for that triplet observable;
separate r_t,b_t may replace them. The singlet floor cannot simply be
reused for a different energy origin or a different physical cooling map.

Add the actual return map's energy cost, replacement, the unresolved
singlet tail and any holding after early events. The singlet tail's
unnormalized energy is bounded by (9). A common finite envelope follows
when these actual maps have affine energy bounds; u_t r<1 supplies a
uniform triplet envelope as the cap changes. Without that condition, a
particular finite cap still has (25a), but increasing the cap may increase
the required cooling cost.

A finite returned energy alone does not imply a uniform bound over
infinitely many calls: its coefficient of incoming energy could exceed
one. Supply a fixed scalar cooling interval while the particles are parked
in separate addressable traps. If the complete output bound assembled
above is E_out<=K_0+K_1 E_in and that parked cooler has contraction r_p
and floor E_p, then

\[
E_{j+1}\le r_pK_1E_j+
r_pK_0+(1-r_p)E_p+D_{\rm idle}.
\tag{26}
\]

Choosing a real finite interval with r_pK_1<1 supplies an invariant energy
envelope. Isolated single-atom scalar cavity cooling has no unresolved
two-particle relative mode; all required directions still need force
geometry. Its source, photons and duration count. Again, the floor need
only support the progress inequalities, not vanish with logical error.

The complete finite adaptive computation obeys a joint-channel hybrid
bound obtained by adding (13), readout/source/ramp errors, explicit aborts
and the actual holding contributions. To see why only physical energy
envelopes are needed, let Phi_j be actual globally defined channels and
Psi_j the input-independent comparison instruments. Then

\[
\Phi_m\cdots\Phi_1-\Psi_m\cdots\Psi_1
=\sum_{j=1}^m\Psi_m\cdots\Psi_{j+1}
(\Phi_j-\Psi_j)\Phi_{j-1}\cdots\Phi_1 .
\tag{27}
\]

Each local difference acts on an actual physical prefix. The comparison
suffix is only used for trace-norm contraction. Thus its artificial CP
completion need not satisfy a fictitious cold-state condition. Include
all adaptive records, retained sources and references in the joint channel.
There is no physical reset of the retained quantum source between calls.
Weighted histories, rather than a claim of uniformly cold rare conditional
states, provide the composition guarantee.
At fixed nonzero nuclear-spin errors, arbitrarily long reliable computation
still requires a genuine error-correction layer with its own operations.

## 8. The microscopic join changes when the atoms are merged

The merged trap removes the need for the earlier stationary approximately
119-nm double-well profile at 100-kHz confinement. It also removes the
small spatial overlap which had suppressed unwanted triplet p-wave contact.
Both changes must enter the comparison.

Using the same 171Yb photoassociation data [7,8], an isotropic harmonic
100-kHz model with a specified nominal cold-singlet loss rate
Gamma=0.01 omega gives:

| Quantity | Conditional merged-trap diagnostic |
|---|---:|
| Orbital length | 24.31 nm |
| Pair-loss rate | 6283/s |
| PA intensity | 1.714 mW/cm^2 |
| Nominal cold loss time for q=10^-6 | 2.199 ms |
| Two-atom atomic Raman hazard | 4.46e-4 |
| Known-four-line p-wave loss hazard | at most 8.35e-4 |
| Centered coherent triplet norm budget from those lines | at most 0.02367 |

The cold-time line assumes a stable cold state with q=exp(-Gamma T); it is
not the warm-cycle duration predicted by (7), and not a certified
full-Franck-Condon progress bound. This isotropic cold diagnostic also does
not supply the transverse stability required by the one-dimensional
return construction. The molecular line list is incomplete.
The coherent entry is a conservative sufficient bound after removing a
scalar; it is not a demonstrated error or a lower bound. It nevertheless
shows why the faster nominal singlet rate does not establish a better full
instrument. Merging makes the non-scalar molecular operator the leading
quantified concern in this comparison.

No RF decoupling, polarization cancellation or spin-transparent molecular
intermediate is silently supplied. Such a repair could be worthwhile, but
would have to include its physical control path and all decay branches.
The full trapped molecular matrix, energy injection, escaping-product
fraction and non-scalar remainder over the reachable orbital envelope are
the specific remaining physical calculation. A gas loss coefficient alone
does not qualify them.

## 9. Prior machinery and useful failures retained

* The full-charge one-resonance theorem remains a useful good-subspace
  progress mechanism. Its new two-loss-channel Lyapunov version is in the
  preceding note, with a rational source-uniform exponential certificate.
* The common static frame, microscopic recentering, scalar-source versus
  quantum-spin-source distinction and correlated-history composition are
  preserved. Neither symmetry averaging nor an abstract logical algebra
  supplies the actual spin-transparent interaction.
* The attempted one-upper-level electronic dressing cooler leaves an
  undressed mode with a finite hyperfine coupling. Its exact eight-state
  counterexample is preserved; it is not used as a renewal operation.
* Cooling every orbital to the logical error target was unnecessarily
  strong under (2). It remains necessary to pay an appropriate orbital
  error when the physical instrument is protected only inside one band.
* Screened geometric dilution supplies useful smooth matrix-element and
  detector-rate scaling, but not the Coulomb high-momentum domain, metallic
  heat renewal or noncollective spin-noise control. Those failed inferences
  are retained separately.
* Brokered optical networks have a stronger demonstrated operation stack
  today [9]. Their disposable Bell resources can implement an exact parity
  instrument. Their source rates, cooling and memory holding must be
  counted too. The exact renewal dephasing law g=r_source/(r_source+Gamma)
  shows why source purification alone does not protect waiting data.

Conventional controllers and existing singlet, cavity and optical methods
receive the same available source knowledge, improved readout and cooling
machinery in these comparisons. A count of pulses, photons or attempted
windows alone establishes no advantage.

## 10. Completed consequence and practical limit

The organising law is now stronger than a short pulse or a single qualified
measurement. **Within-sector protection can make auxiliary-state accuracy
a progress requirement instead of a logical-accuracy requirement.** The
survival-energy theorem proves this even when null histories select hot
states and retained sources remain correlated. The paired linear/quadratic
cooler and filled-subspace splitting supply a concrete return mechanism
in a declared physical domain.

What has not been proved is that the 171Yb molecular, cavity, trap, detector
and source parameters jointly satisfy a useful complete-device error
budget. The warm-auxiliary law reduces the required cooling purity; it does
not cancel molecular anisotropy or Raman events. The best next physical
improvement is therefore the actual spin-transparent absorbing interface
or a different native sink, evaluated over the whole reusable cycle.

## Proof and executable preservation

* `protected_absorption_check.py` and its JSON output verify the exact
  rational progress certificate, full multi-orbital singlet-loss darkness,
  a hot triplet double-occupancy witness, the microscopic accepted-effect
  bound with a fast noncommuting retained source, and a complete finite CP
  cooling/absorption model with a retained noncommuting source.
* `alternative/ABSORBING_ENERGY_AUDIT.md` independently proves the sharp
  effect bound, recurrence, determinant condition and instrument-norm
  conversion; its executable tests the sharp cases and CP channels.
* `detector/ORBITAL_OPACITY_AUDIT.md` proves the global ideal oscillator
  coercivity, nonzero heating floor, occupied-subspace return and finite-range
  no-loss energy bound. Its executable checks fixed-number blocks through
  total number 100; the analytical proof, not the cutoff, is the theorem.
* `OPERATING_THEORY.md`, the detector notes and PA/screening audits preserve
  the earlier successful components and failed shortcuts.

The root CP example carries the same two-state source through all cycles,
with noncommuting source terms of strengths 20 and 3 in its dimensionless
units. Its computed unsuccessful-filter heating coefficient is 0.15514;
it is measured from the actual model operator, not set to zero. The
certified comparison rate for that example is 0.86067 per cycle. These
floating-point checks are not interval certifications of a physical box.

## Primary methods consulted

1. Freedman, Hastings, Shokrian Zini, Symmetry Protected Quantum Computation:
   https://arxiv.org/abs/2105.04649
2. Rudolph and Virmani, universal singlet/triplet measurement computation:
   https://arxiv.org/abs/2107.03239 ; https://doi.org/10.1038/s41467-023-43481-y
3. Terhal and Horodecki, Schmidt number for density matrices:
   https://doi.org/10.1103/PhysRevA.61.040301
4. Zippilli and Morigi, cavity cooling and the full force/diffusion model:
   https://arxiv.org/abs/quant-ph/0508075
5. Cooling the motion of a trapped atom with a cavity field:
   https://arxiv.org/abs/1208.5942
6. Nunnenkamp, Borkje, Harris and Girvin, Cooling and squeezing via quadratic
   optomechanical coupling: https://doi.org/10.1103/PhysRevA.82.021806 ;
   https://arxiv.org/abs/1004.2510
7. Reichenbach, Julienne and Deutsch, Controlling nuclear spin exchange via
   optical Feshbach resonances in 171Yb: https://arxiv.org/abs/0905.4556
8. Goyal, Reichenbach and Deutsch, p-Wave Optical Feshbach Resonances in
   171Yb: https://arxiv.org/abs/1010.0465
9. Main et al., Distributed quantum computing across an optical network link:
   https://doi.org/10.1038/s41586-024-08404-x ; https://arxiv.org/abs/2407.00835
10. Burgarth and Giovannetti, The Generalized Lyapunov Theorem and its
    Application to Quantum Channels:
    https://doi.org/10.1088/1367-2630/9/5/150 ;
    https://arxiv.org/abs/quant-ph/0605197
11. Chia, Paterek and Kwek, Hitting statistics from quantum jumps:
    https://doi.org/10.22331/q-2017-07-21-19 ;
    https://arxiv.org/abs/1608.05510

Readout and the one-upper-level cooling audit use the actual Hamiltonians
in https://arxiv.org/abs/2410.23430. Their conclusions are separated: the
off-resonant scalar readout survives; the stated single-upper-level
large-drive isolation does not follow from its printed Hamiltonian.

No exhaustive priority claim is made for the new working synthesis.
Lyapunov methods for quantum channels and quantum-jump hitting statistics
already exist [10,11]. The working addition here is the explicit coarse
survival/energy certificate, its sharp effect inequality, full
sector-instrument conversion and the physical warm-auxiliary return
construction. It is not a claim to invent those general methods.
