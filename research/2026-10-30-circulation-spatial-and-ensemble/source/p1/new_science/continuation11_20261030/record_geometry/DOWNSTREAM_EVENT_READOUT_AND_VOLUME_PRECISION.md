# Downstream native-event readout: exact source preservation and a volume-scale loss boundary

30 October 2026. Complementary constructive opportunity, record_geometry.

## 1. The actual stronger port

An existing outgoing record can be measured after it has left the native
system. This is a useful ordinary alternative to contacting the native
positions with a new reciprocal sensor. It is not a claim that every
particle hop already emits an accessible record.

Assume the actual native dynamics has local marked events. An event carries
its physical row and horizontal displacement sign, and already emits a
distinguishable outgoing quantum or other physical signal with that mark.
The emission is part of the reference dynamics. The outgoing channel is
strictly one way: changes of its downstream load do not change the native
input, Hamiltonian, transition rates or noise. Native and deployment use
the same source and channel; only the downstream record is used to drive
the isolated auxiliary apparatus.

The native state may contain arbitrary hidden memory. Conditional on that
state and the full past, the total intensity of the relevant unit events
is at most Lambda N^2. No native jump rate is learned. A single event
affects at most a fixed number of local current components.

This port can preserve the source exactly. The ordinary physical precedent
is cascaded quantum input--output theory. With source A, receiver B,
source operator L_A, receiver operator L_B, and

\[
H_{\rm cas}=\frac{L_B^\dagger L_A-L_A^\dagger L_B}{2i},
\]

the cascade generator is

\[
\mathcal L\rho
=-i[H_A+H_B+H_{\rm cas},\rho]+\mathcal D[L_A+L_B]\rho.
                                                               \tag{1}
\]

Here D[L]rho=L rho L^dagger-{L^dagger L,rho}/2. For any observable O_A
on the source, the cross terms in the dissipator are

\[
\tfrac12[L_A^\dagger,O_A]L_B
+\tfrac12L_B^\dagger[O_A,L_A].
\]

They cancel i[H_cas,O_A] exactly. Thus

\[
\mathcal L^\dagger(O_A\otimes I_B)
=(\mathcal L_A^\dagger O_A)\otimes I_B.                        \tag{2}
\]

The reduced source evolution is autonomous for every initial joint state.
Repeating this argument between source interventions preserves its
operational multitime statistics. A finite propagation delay does not
create upstream influence in an actually one-way field channel; equation
(1) is the usual zero-delay Markov representation.

For a classical marked native jump process, outgoing record states identify
the actual jump marks and the complete native path law is unchanged.
For a general coherent quantum plant, an arbitrary hypothetical classical
trajectory is not inferred from a Lindblad generator; an operational record
or a commuting pointer-state interface must be specified.

Detection loss downstream does not by itself disturb the source. Reflection,
reciprocal impedance changes, incoming thermal radiation or active probing
are different physical interfaces. A circulator or matched-load cascade
must be supplied, not inferred from the existence of light emission.

## 2. Exact counting model and spatial normalization

Use N rows and physical observation time T_N=N^2 T. Let B_y(s) be the
true total horizontal native displacement in row y by time s. Every unit
event has increment d_j in {-1,+1} and a row label y_j.

Suppose a downstream detector retains the event with independent probability
eta_N, conditional on the complete native path, with eta_N>=eta_0>0.
The fresh detection decisions are independent of the old record and
native future conditional on their actual supplied initial interface.
Write delta_N=1-eta_N.

For known efficiency define

\[
\widehat B_y(s)=\eta_N^{-1}
\sum_{\substack{j:t_j\le s\\y_j=y}}\xi_j d_j,\qquad
E_y(s)=\widehat B_y(s)-B_y(s),\qquad
\xi_j\sim{\rm Bernoulli}(\eta_N).                             \tag{3}
\]

This is an estimator of true displacement, not a reassignment of a lost
event's physical current. The row field is B_y/N^2; its spatial L^1
measurement error is

\[
\mathcal E_N=\sup_{s\le T_N}N^{-3}\sum_y|E_y(s)|.               \tag{4}
\]

The same proof permits row-dependent known efficiencies whose common
minimum is bounded away from zero and whose maximum loss tends to zero.
Native event times and intensities need not be independent, stationary,
reversible or known.

## 3. A sharp sufficient condition for volume-speed readout

There are constants depending only on eta_0, Lambda and T such that

\[
\Pr\{\mathcal E_N>\epsilon\}
\le 2^{N+1}
\exp\left[-c\min\left\{
\frac{\epsilon^2N^2}{\delta_N},\ \epsilon N^3
\right\}\right].                                            \tag{5}
\]

When delta_N=0 the detection error is identically zero. In particular,
delta_N->0 implies

\[
\limsup_{N\to\infty}N^{-2}\log
\Pr\{\mathcal E_N>\epsilon\}=-\infty.                          \tag{6}
\]

Proof: for any fixed sign vector v in {-1,+1}^N, the scalar error
M_v=sum_y v_y E_y is a martingale in the actual native/detector filtration.
At one native event its increment is v_y d (xi/eta_N-1).
It has conditional mean zero, uniformly bounded magnitude, and conditional
second moment delta_N/eta_N. For theta in a fixed bounded interval,

\[
\log\mathbb E[e^{\theta v_yd(\xi/\eta_N-1)}\mid{\rm past,event}]
\le C\delta_N\theta^2.
\]

The intensity bound and an exponential-martingale maximal inequality
therefore give

\[
\Pr\{\sup_{s\le T_N}M_v(s)>x\}
\le \exp\left[-c\,\frac{x^2}{\delta_N N^4+x}\right].
\]

Set x=epsilon N^3 and union over the 2^N sign vectors. Since
sum |E_y|=max_v sum v_y E_y, this proves (5). The sign-vector entropy is
only order N and is negligible at the actual volume speed N^2.

This is the joint spatial estimate. Individual row convergence in
probability would not supply the required conclusion.

### 3.1 Unknown efficiency: an unweighted robust route

Exact efficiency calibration is unnecessary if the probability of losing
each native mark is conditionally at most delta_N and

\[
N\delta_N\longrightarrow0.                                  \tag{7}
\]

Use the raw observed signed counts. Their total absolute row error is
bounded by the number of lost events over the whole observation horizon.
Conditional loss decisions with the stated bound give the usual Poisson
domination with mean at most Lambda T delta_N N^4. Chernoff's inequality
at epsilon N^3 gives

\[
\Pr\{\mathcal E_N>\epsilon\}
\le
\exp\left[-\epsilon N^3
\left\{\log\frac{\epsilon}{\Lambda T N\delta_N}-1\right\}\right]
                                                               \tag{8}
\]

for all sufficiently large N. This is superexponential at speed N^2.
Independent per-photon absorption clocks provide the required conditional
loss bound; a correlated common-mode detector failure does not.

The stronger loss target (7) costs only a constant-factor increase in
length in the distributed-absorber construction below. It avoids
pretending that a finite-confidence efficiency estimate is an exact
physical calibration.

## 4. Actual finite delay and response

Suppose an emitted mark is either recorded or lost within D_N=o(N)
physical time. At time s, the discrepancy from assigning each detected
mark its exact emission time is bounded in total absolute row count by
the number of native events in [s-D_N,s].

At total conditional intensity Lambda N^2, covering sliding windows by
O(N^2) deterministic windows gives

\[
\Pr\left\{\sup_{s\le T_N}
\#\{{\rm events\ in}\ [s-D_N,s]\}>\epsilon N^3\right\}
\le \exp[-\omega(N^2)].                                     \tag{9}
\]

Indeed the mean count of a covering window is
O(N^2(D_N+1))=o(N^3), and its Poisson Chernoff exponent is of order
N^3 log[N/(D_N+1)], apart from the polynomial covering factor.
No gradient telescoping or asynchronous cancellation is used.

A finite-response linear pulse integrator can also be included at its
actual additive-charge interface:

\[
\tau\,dr=-r\,ds+dD,\qquad dC=r\,ds,\qquad C=D-\tau r
\]

with zero initial filter state. For fixed tau, a recent O(log N) window bounds the
filtered residual; the older contribution is exponentially attenuated.
A polynomial full-horizon count envelope handles the old tail.
Thus pulse overlap need not imply dead time for an actually linear,
nonsaturating integrator. This does not establish such linearity for
an arbitrary photodetector or eliminate electronic noise.

Common held sampling times, subsequent collection, and actuator commands
remain the actual communication contract. A downstream latency O(log N)
can be absorbed into the measurement envelope before the separate O(N)
collection delay. The theorem does not silently identify stale counts
at different times with one synchronized snapshot.

## 5. Fixed loss fails, even for a perfectly unchanged source

Take N^2 independent native walkers, each with independent positive and
negative physical jumps at rate lambda/2. The positions can be on the
horizontal circles. Total signed displacement over time N^2 T is
B=P_+-P_-, where P_+ and P_- are independent Poisson variables of mean
lambda T N^4/2. This is a conservative actual-particle example with a
bounded local jump rate and an exactly unchanged native source.

With fixed eta<1, split each sign into independent detected D_+,D_- and
missed M_+,M_- streams. The inverse-efficiency estimator's error is

\[
E=\frac{\delta}{\eta}(D_+-D_-)-(M_+-M_-).
\]

Its exact moment generating function gives

\[
\begin{split}
\frac1{N^2}\log\mathbb E e^{\theta E/N}
={}&\lambda T N^2\left[
\eta\{\cosh(\delta\theta/(\eta N))-1\}
+\delta\{\cosh(\theta/N)-1\}\right]\\
\longrightarrow{}&\frac{\lambda T\delta}{2\eta}\theta^2.
\end{split}                                                   \tag{10}
\]

Thus the volume-speed error rate is finite:

\[
I_{\rm error}(e)=\frac{\eta e^2}{2\lambda T\delta}.             \tag{11}
\]

The error vanishes on the typical macroscopic scale, but is not
superexponentially negligible at speed N^2. Substituting such a record
into a controller can change the rare current law.

There is also an estimator-independent obstruction within this actual
count-only interface: event times, signs and row labels are retained,
while emitter positions are not observed. Conditional on that entire
detected record, the missed
signed current M=M_+-M_- remains independent with its symmetric Skellam
law. Any estimator based only on the detected record and independent
receiver randomness has an error M-a for a conditional scalar a.
If a>=0, the event M<-epsilon N^3 forces a large error; if a<0, use
M>epsilon N^3. Hence every such estimator has failure probability at least
one missed-current tail. That tail has finite volume-speed exponent

\[
\lim_{N\to\infty}N^{-2}\log
\Pr\{M>\epsilon N^3\}
=-\frac{\epsilon^2}{2\lambda T\delta}.                        \tag{12}
\]

This follows directly from its Poisson moment generating function and
the quadratic moderate-deviation limit. The obstruction is not confined
to the unbiased estimator. Extra native-position measurements or another
record channel would be additional physical information and are not ruled
out by this claim.

## 6. A finite-rate ordinary receiver, and exactly where it can fail

A concrete ideal receiver class is a one-way transmission line of length
L_N and propagation speed v. Each marked signal is absorbed into a counted
channel at a fixed rate gamma per unit travel time. Every absorption
produces the corresponding unit charge in a local integrating counter.
The absorber is linear and unsaturated over its declared range. If there
is no unrecorded competing loss, independent absorption clocks give

\[
\delta_N=e^{-\gamma L_N/v},\qquad D_N=L_N/v.                   \tag{13}
\]

With a known lower bound gamma>=gamma_min>0, choose

\[
L_N=\frac{a v}{\gamma_{\min}}\log N,\qquad a>1.
\]

Then delta_N<=N^{-a}, D_N=O(log N), and the raw-count route (7)--(9)
works without measuring gamma or any native rate. Absorption itself has
fixed local response rate; the increased reliability is purchased by
channel length and absorbing material. The native source is still
unchanged at the assumed one-way port.

This does not prove that an arbitrary detector has zero unrecorded loss.
If counted absorption occurs at rate gamma_d and unrecorded parasitic
loss at rate gamma_l, the actual efficiency is

\[
\eta_N=
\frac{\gamma_d}{\gamma_d+\gamma_l}
\left[1-e^{-(\gamma_d+\gamma_l)L_N/v}\right].                  \tag{14}
\]

Fixed positive gamma_l/gamma_d creates a nonzero loss floor however long
the receiver is. One must reduce this ratio, increase the counted
absorption response, or collect the formerly lost channel.
For calibrated estimation, vanishing ratio is enough. For the robust
raw-count construction at the worst-case intensity interface, a ratio
o(1/N) is sufficient together with a sufficiently small exit probability.

Repeating ordinary destructive detectors is not automatically a repair.
An undetected photon already absorbed by an inefficient detector is gone;
later detectors cannot recover it. A nondestructive repeated record,
independently accessible loss channels, or redundant emitted marks is a
different supplier. Adding redundant emission at the source is not
authorized merely by the original native generator.

### 6.1 Counter range, noise and clocks remain actual resources

The proof assumes that a counted absorption creates a known unit counter
increment. Finite response can be treated as in Section 4, but saturation,
dead time, dark counts and electronic integration noise are not silently
discarded. A polynomial full-horizon count range can be chosen with
superexponential overflow probability from the native intensity bound.
The physical linear dynamic range and storage capacity must still be
supplied; a logarithmic digital word length alone does not establish them.

Independent centered unit counter errors of total intensity q_N N^2
satisfy the same estimate as (5) with delta_N replaced by delta_N+q_N.
Thus q_N->0 is sufficient. An unknown directed error rate instead needs
its accumulated bias controlled; a safe worst-case condition is Nq_N->0.
Fixed additive detector noise can have the same finite-rate obstruction
as fixed missed-event noise.

If finite calibration is used, its coverage event is part of the
end-to-end statement. A fixed failure probability does not establish an
unconditional volume-speed rare-event law. One needs a conditional-on-
coverage result or failure probability exp[-omega(N^2)] with paid trials.
The known lower absorption bound in the raw-count construction is a
supplied physical bound, not a result inferred from a stationary
equilibrium weight.

## 7. Power, hardware and preparation bill

For a fixed-energy emitted quantum E_gamma and nonvanishing native
activity, the source emits Theta(N^4) quanta over physical time N^2.
Its emitted energy throughput is Theta(E_gamma N^4), and average optical
power is Theta(E_gamma N^2). The absorber receives almost all of this
energy in the high-efficiency construction. Whether it is dissipated or
recovered depends on a further actual energy port.

This is a throughput statement, not a universal lower bound on externally
supplied measurement work: an already radiative native system may already
pay the emission bill in the reference. If the native process does not
already emit the marks, installing a pumped emitter introduces new
kinetics and an energy source. Its compatibility with the native law
must be established separately.

There are O(N^2) local marked channels, each with O(log N) propagation and
absorber length in (13), plus their counter range and readout hardware.
This is O(N^2 log N) channel material at fixed cross section. Routing it
without creating an unintended spatial shortcut or return path is an
actual layout condition. The additional delay is O(log N); subsequent
global collection still has finite propagation time.

Any nonzero standby power per unit absorber length accumulates another
O(N^4 log N) energy scale over the observation interval. No standby,
clocking, conversion, logical reliability, source retirement or fabrication
cost has been made free. This readout can be attractive when a suitable
native output stream already exists. It does not automatically beat the
root mechanical recorder's resource budget for a nonradiative medium.

Independent unread source records are used only at their actual interface.
A common-mode receiver outage or a correlated source preparation cannot
be replaced by independent scalar efficiencies. Conditioning on an old
record is allowed if the complete future source/detection conditions
remain valid under that conditioning.

## 8. Small upstream imperfections require a separate quantitative supplier

Exact one-way propagation gives exact source autonomy. A physical isolator
with merely small backscatter is not automatically covered.

One useful sufficient rare-law comparison can be proved if the full
microscopic native jump rates, on the same marked support and with the
same initial law, actually obey

\[
q'_e(s)=q_e(s)(1+d_e(s)),\qquad |d_e(s)|\le b_N<1/2,
\qquad \sum_e q_e(s)\le\Lambda N^2.                           \tag{15}
\]

The coefficients may depend on hidden state and complete past. The
likelihood-ratio exponential for time N^2 T has, when p b_N<=1,

\[
\log\mathbb E_P Z^p\le C p^2 b_N^2 N^4,
\]

and the reverse comparison has the same form. If

\[
Nb_N\longrightarrow0,                                      \tag{16}
\]

choose p_N->infinity with p_N(Nb_N)^2->0. Holder's inequality in both
directions then shows that every sequence of events has the same
finite volume-speed logarithmic exponents under P and P', and is
superexponential under one law if and only if it is under the other.
The moment contribution divided by N^2 tends to zero, while the Holder
power tends to one. This does not assert that the difference of the two
logarithms divided by N^2 vanishes for arbitrarily superexponential events.

This preserves volume-scale rates, not literal equality of finite-N
path laws or small total variation of every microscopic record.
It also requires the full conditional rate comparison (15), not only
similar observed means. A new transition channel with zero reference
rate falls outside it.

The 1/N directional scale is physically relevant. For symmetric native
walkers or exclusion, a relative right/left bias of order c/N produces an
order-one macroscopic drift on diffusive time. Thus a generic
backaction estimate that is only O(1/N) can change the targeted current
law. Reciprocal perturbations may admit weaker conditions, but their
symmetry would be an additional proved structure.

## 9. Scope against a reciprocal local probe

For a native coordinate X and sensor S with constant-mobility Hamiltonian
coupling V(X,S), demanding unchanged native forces for every actual sensor
state gives partial_X V=0 after any state-independent native offset has
been removed. Then V cannot provide X-dependent sensor forces.
An active compensation, a nonreciprocal port, or a changed native law is
needed in that elementary mechanical class. This explains why the
downstream cascade is a genuinely stronger operation.

This is not a no-go from detailed balance alone. A reversible finite-state
example has a native bit X flipping independently at rate one and a sensor
bit S flipping symmetrically at rate c_X. The product uniform law is
reversible, X is autonomous, and the sensor's activity record carries
information about X. Supplying those kinetic couplings physically is a
separate task; an equilibrium distribution alone does not supply them.
The example prevents a blanket extension of the mechanical reciprocity
argument to all possible kinetic sensors.

## 10. Primary comparison and status

The direct ordinary predecessors are C. W. Gardiner,
[Driving a quantum system with the output field from another driven
quantum system, PRL 70 (1993), 2269](https://doi.org/10.1103/PhysRevLett.70.2269),
and H. J. Carmichael,
[Quantum trajectory theory for cascaded open systems, PRL 70 (1993),
2273](https://doi.org/10.1103/PhysRevLett.70.2273).
Their primary publication abstracts were checked early. A later attempt
to obtain full PDFs was not completed after search-tool availability
changed. The cancellation (1)--(2) and all counting/precision bounds above
are reconstructed explicitly here; no unexamined detector model from
those papers is imported.

Realistic photodetection has its own established literature, including
[Quantum Trajectories for Realistic Photodetection I: General Formalism,
arXiv:quant-ph/0206125](https://arxiv.org/abs/quant-ph/0206125).
Only its primary indexed abstract was inspected; it is not a supplier
certificate for (13). No priority claim for downstream noninvasive
measurement is made.

The completed connection is specific: a source with an already available
one-way marked output admits actual downstream readout preserving its
law; vanishing loss gives the required joint spatial rare-event precision.
Fixed loss cannot be repaired by a better estimator using only that same
record in the Poisson counterexample. A finite-rate long absorber closes
the construction only at the declared no-unrecorded-loss, unsaturated
counting interface, with paid length, energy throughput and storage.
These premises are the precise remaining physical suppliers.

This connection does not produce independent thermal preparations for
the elastic auxiliary layer. Those source and initialization premises
remain separate. Nor does an abstract native jump generator supply
emitted photons, and an emitted-jump port does not measure a general
continuous native displacement. These are distinct actual sensing
interfaces, including in comparison with root's compensated mechanical
recorder.

The stronger constructive follow-up
TAGGED_POSITION_MARKS_REMOVE_FIXED_LOSS_FLOOR.md proves that fixed
efficiency can suffice for row-confined particles when detected signals
also give particle identity and wrapped position. Short-arc reconstruction
recovers missed-run current except for geometrically long runs, whose
joint effect is superexponentially negligible at volume speed. Its extra
information and causal merging costs are explicit. It must not be
confused with an estimator on the count-only record of Section 5.


