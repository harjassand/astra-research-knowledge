# Calibration of a reusable nonlinear quantum memory

29 October 2026, Australia/Brisbane. New root construction, using a new
generator-row lemma by challenger. Actual independent reviews are separate.
The predecessor kernel theorem remains frozen.

## 1. Principle and scope

A calibrated physical model can control the complete operation of a
persistent nonlinear bosonic memory without resetting it between contacts.
The required stability is a bounded occupation REGION, not a fixed state,
Gaussian dynamics, or a memoryless channel. A fresh independent thermal
contact supplies operation-specific regularity stronger than a bound on
the square of total particle number.

The complete contact error below is uniform in incoming source correlations
and in the number of preceding contacts. It therefore composes linearly
across any finite computation, including actual records, source feedback
and references. The memory can have infinite second number moment.

This changes representation relative to the source-only kernel theorem.
The models share an identified physical canonical oscillator and passive
generator; arbitrary Gram-factorization gauges do not supply that
identification. The SAME retained input state is compared in both models.
Learning an unknown initial state is not implied. This is a mathematical
model-to-computation instrument, not a device error rate or acquired coupler.

## 2. Complete anchored contact

Retain one physical oscillator a. Contact j supplies fresh b_j in thermal
state tau_(n_j), independent of the entire incoming source/a/controller/
reference state and all records. During the finite contact use

    H_j(t)=H_K(t)+A_j(t) S_j(t) sin[sqrt(v_j)(a+a^dagger)]
                                +g_j(t) J_j,
    J_j=i(b_j^dagger a-a^dagger b_j).                    (1)

The real source amplitude has a common pointwise envelope |A_j|<=a_j,
alpha_j=integral a_j<=alpha_bar. S_j is a self-adjoint source/controller
contraction. Source-only complete interventions and actual-record feedback
are allowed through common coherent dilations and that envelope. Common
source-only controls can be put in their own interaction picture. The real
integrable passive waveform g_j is prescribed, not controlled by an incoming
quantum system or a later record within the contact. Paths are strongly
measurable, and the finite chronological controls have these common bounds.

At the end trace b_j permanently. Retain a, source, controller, reference
and actual records. There is no independent reset of a. Later return,
interaction or detector feedback from b_j is outside this contact map.
For finite J the supply is J independent thermal modes, without an infinite
occupied tensor product being interpreted as a vacuum Fock vector.

Both models use the SAME canonical a,b_j, phase convention, passive
generator, physical clock and source program. Uncertain quantities are
v_j, n_j and g_j. Missing passive phases, extra modes or new generators
cannot be absorbed into those parameters without a separate construction.

## 3. A stable first-moment region

All candidates obey

    0<=v_j<=v_max, 0<=n_j<=n_bar,
    |cos Theta_j|<=c_bar<1, Theta_j=integral g_j,
    alpha_j<=alpha_bar.                                 (2)

Choose L_bar>=alpha_bar sqrt(v_max). If

    sqrt(c_bar^2 P_*^2+n_bar)+L_bar<=P_*,                (3)

the class Tr(rho N_a)<=P_*^2 is invariant. Factor out the passive rotation.
The retained output annihilator is a(r)=a cos Theta_j-b_j sin Theta_j.
Fresh thermal independence bounds its initial mean by
cos^2 Theta_j P_*^2+sin^2 Theta_j n_j. In the passive interaction picture
the sine feature has norm sqrt(v_j) and overlap with r equal to
sqrt(v_j)cos[Theta_j-Theta_j(t)]. The closed first-annihilation-row estimate
therefore bounds the output norm by the square root of that mean plus
L_bar. This is the first row of the independently reviewed
../physical/CONCURRENT_THERMAL_MEMORY_INTERFACE.md, with its explicit
CONCURRENT_CONTACT_ASSUMPTIONS.md addendum. Finite-mean inputs follow by
core approximation and lower semicontinuity; no second moment is needed.

An exact invariant region is

    v_max=21/10, alpha_bar=1/100, n_bar=1/10000,
    c_bar=1/10, L_bar=29/2000, P_*=1/40.                 (4)

Here L_bar^2>=v_max alpha_bar^2 and the left side of (3) is at most
2481/100000<1/40. The angle interval |Theta_j-pi/2|<=1/10 supplies the
cosine bound. These are sufficient conditions, not physical limitations.

For N=N_a+N_b set

    P_0=sqrt(P_*^2+n_bar), P_bar=P_0+L_bar,
    C_bar=P_bar+sqrt(P_bar^2+1).                         (5)

Throughout every contact, <N(t)><=P_bar^2. Passive rotation preserves total
N; the first-row theorem applies to the bounded sine with rotating feature
norm sqrt(v_j). These are unconditional complete-state expectations, not
conditional expectations after division by a rare outcome probability.
The bounds are uniform over admitted controls and all contact replacements.

## 4. The generator row instead of the total-number graph

Fresh thermal independence gives exactly, on any input purification,

    ||J psi_in||^2=(2n+1)<N_a>+n.                        (6)

The anomalous thermal moments vanish, while the cross terms in J^2 are
n<N_a+1> and (n+1)<N_a>. Thus (6) holds with finite <N_a> even when
<N_a^2> is infinite. Source/reference correlations are unrestricted.

For X_a=a+a^dagger and X_b=b+b^dagger,

    [J,A S sin(sqrt(v)X_a)]
               =i A sqrt(v) S X_b cos(sqrt(v)X_a).       (7)

The passive generator commutes with itself; X_b commutes with the cosine.
Equation (5) gives ||X_b psi(t)||<=C_bar. Row Duhamel yields

    ||J psi(t)||<=Gamma_bar,
    Gamma_bar=sqrt((2n_bar+1)P_*^2+n_bar)+L_bar C_bar.     (8)

The common domain is D(J) intersect D(sqrt(N)), not D(N). It is preserved
by the passive group and source-only isometries. Weyl displacements in
the a direction preserve it because their J commutator is linear in X_b
and their first-number row has a bounded displacement term. Finite-sector
vectors are a common core since J commutes with N. In the passive
interaction picture the Weyl direction rotates in the two-mode plane;
its J commutator remains a field row bounded by the first-number graph
norm. A graph-space Volterra construction for the integrably bounded sine
then identifies the graph solution with the Hilbert-space propagator.
The separate ../challenger/THERMAL_CONTACT_FIRST_MOMENT_SENSITIVITY.md
gives the domain details (SHA256
5c10503d7254a2af09eedc0780a2c653618e67b6a518ea16f2b2fd91aa3d678b).

The valid but coarser inequality ||J psi||<=||N psi|| needs a second
number moment. Equation (8) controls the actual uncertain operation and
avoids that requirement. Earlier second-moment machinery remains useful
for generators whose action genuinely requires it.

## 5. Complete one-contact sensitivity

Let E_(v,g,n) retain everything except outgoing b, and d=||rho-sigma||_1/2.
Uniformly on <N_a><=P_*^2, including arbitrary references,

    d(E_(v,g,n)(rho),E_(vhat,ghat,nhat)(rho))
       <=min(1,epsilon_v+epsilon_g+epsilon_n),           (9)

where all intermediate candidates stay in (2), and

    epsilon_v=alpha_bar |sqrt(v)-sqrt(vhat)| C_bar,
    epsilon_g=Gamma_bar integral |g(t)-ghat(t)|dt,
    epsilon_n=|n-nhat|/[1+max(n,nhat)].                  (10)

Spectral calculus on the same X_a gives
||[sin(sqrt(v)X_a)-sin(sqrt(vhat)X_a)]psi||
<=|sqrt(v)-sqrt(vhat)| ||X_a psi||<=|sqrt(v)-sqrt(vhat)| C_bar.
Complete Duhamel and the source envelope prove epsilon_v without a sine
linearization or Fock cutoff. Linear dependence on |v-vhat| additionally
requires a positive lower bound on v; the sqrt(v) estimate holds at zero.

For the passive term the Hamiltonian difference is (g-ghat)J. The common
graph construction permits differentiating U_g(T,t)U_ghat(t,0), and (8)
supplies its integrable bound. Source-only isometries commute with the
rows and can be inserted at their actual times. Purified-vector difference
bounds complete half trace distance; outgoing partial trace is contractive.

For the thermal term set q=n/(1+n), r=m/(1+m), n<=m. Couple geometric
waiting times using common uniform trials. Both continue if U<=q and
both stop if U>r; their first disagreement has total probability
sum_(k>=0)q^k(r-q)=(r-q)/(1-q)=(m-n)/(1+m). This bounds the total variation
of the diagonal thermal inputs. Tensoring a common retained correlated
state and applying the contact cannot increase that distance.

For both thermal means at most one there is a stronger exact conventional
choice: epsilon_n=|n-nhat|/[(1+n)(1+nhat)]. Only the vacuum probability
decreases with n in that range, so its deficit is the complete total
variation. The generic expression (10) is retained for arbitrary thermal
means; using it in the cold numerical example is a stated sufficient bound.

For a supplied common pulse g_theta=theta u, u>=0, integral u=1, the
waveform term is |theta-thetahat| Gamma_bar. Certified delivery L1 error
zeta adds Gamma_bar zeta. Equal endpoint area alone does not supply a
common shape; the counterexample below shows why this datum is essential.

## 6. Composition through persistent memory

Keep the exact retained a/source/controller/reference/record state at
every boundary. For every finite J contacts, channel telescoping gives

    d(E_J ... E_1(rho), Ehat_J ... Ehat_1(rho))
                  <=min(1,sum_(j=1)^J epsilon_j).       (11)

Each local replacement is evaluated on an admitted prefix. Invariance
(3) controls its incoming memory; every later common complete operation
is contractive. All full-contact replacement hybrids stay in the region.
The source can remain on throughout the passive contacts and source
feedback can depend on actual earlier records. The passive pulse family
and common pointwise envelopes remain those supplied in (1).

The coefficient is independent of J because the contact restores the
moment REGION. It does not restore a particular state or erase the old
memory's influence on the source. Equation (11) includes the retained
oscillator in its output; it is not a product of reduced reset-gate maps.
It gives no bound on normalized outcomes selected with small probability.
It is a linear sufficient workload comparison, not a duration-uniform
total error or a threshold theorem.

A simultaneous parameter confidence event covers all admitted source
programs selected after calibration. A new program in the same declared
physical/control family requires no new bath fit. On that event (11) is
deterministic. Acquisition failure probability is separate; an unconditional
acquisition-and-deployment comparison may add it once. Structural promises
are not certified from finite data by either the event or (11).

If rho_actual is epsilon_pre close to an identified rho_0 in the region,
the deployment-to-prediction comparison is explicitly

    d(E_actual(rho_actual), Ehat(rho_0))
               <=epsilon_pre+sum_j epsilon_j.            (11a)

First apply contractivity under E_actual, then compare the two maps on
rho_0. Comparing BOTH maps on the same off-region rho_actual instead costs
2 epsilon_pre by this argument. Trace closeness alone does not imply a
moment bound on rho_actual; (11a) does not need one. Any additional local
physical-error allowance must apply to the hybrid inputs where it is used.
Unknown heating, loss, controls, readout and reset are not automatically
covered by the model-parameter budget. This preparation-target precision
was required by the actual independent conventional_solver review.

## 7. Strict reach beyond a second-moment input condition

For r=P_*^2 take a number-diagonal memory with

    p_(4^k)=r 8^(-k), k=1,2,...,   p_0=1-r/7.           (12)

The probabilities sum to one and <N_a>=r sum_(k>=1)2^(-k)=r, while
<N_a^2>=r sum_(k>=1)2^k is infinite. The old N-graph bound gives no finite
passive-error allowance here, but (6)-(11) still apply. At each contact,
fresh thermal independence supplies the J-row input bound from the finite
retained mean alone. For a fixed-frequency oscillator the state has finite
mean energy and divergent second energy moment. This is a change in what
the representation controls, not a physical-resource claim about preparing
that particular state.

## 8. Finite calibration anchor and a useful failure

For g_theta=theta u with a known common shape, calibrate with a in vacuum
and the SAME stationary independent thermal b supply. The source sine is
excluded or separately bounded during the calibration transit. Physical
canonical a, its phase, and selective scaled Weyl control are supplied.
Weyl calls occur outside the passive pulse, with no frozen-field assumption
during a finite contact.

Put f=sqrt(v)e_a, q=lambda^2 v, c=cos theta. A single local controlled
Weyl probe has real mean u_0=exp(-q/2). Two interleaved words, one local
Weyl before the common passive contact and one after it, have real means

    z_+=exp[-q(1+c+n(1-c^2))],
    z_-=exp[-q(1-c+n(1-c^2))].                          (13)

The inverse assumes q=lambda^2 v>0, and finite-interval inference must
certify a strictly positive lower endpoint for q. At v=0 all three means
equal one, leaving theta and n unidentifiable. This restriction concerns
acquisition; the deterministic comparison (9) itself allows v=0.

The passive unitary acts on BOTH Ramsey branches. Pull the second Weyl
back through it and use the initial Gaussian characteristic function.
This proves (13) without requiring a vacuum supply for b. The three
scalar means identify

    q=-2 log u_0, v=q/lambda^2,
    c=(log z_--log z_+)/(2q),
    theta=arccos c,
    n=[-(log z_++log z_-)/(2q)-1]/(1-c^2).               (14)

A near-swap prior fixes the arccos branch and keeps 1-c^2 away from zero.
Independent starts, fixed-design confidence rules, known control/readout
accuracy and stationary parameters are needed for the statistical transfer.
Repeatable thermal marginals alone do not imply independent episodes.
The selective complementary sine/cosine compiler and field-argument
scaling are extra resources; scaling a sine pulse's duration is insufficient.

The separate anchor construction supplies interval inversion and resource
analysis. Small n is a difference of log visibilities, so stable inversion
does not eliminate absolute-precision shot cost. A trusted zero/nonzero
occupation detector is a stronger conventional thermal estimator but an
additional interface. Neither is inferred from the old six-table count
fixture, which belongs to a different plant. No old counts are reused as
new data.

### Equal endpoint area does not identify concurrent memory dynamics

Start a,b in vacuum and put the source in S=+1. Use the SAME nonzero source
pulse in a middle time interval. One passive waveform performs a full swap
before that interval; another performs it afterward. Both areas are pi/2
and all three calibration means (13) agree. The source pulse and its timing
are identical.

The first retained output is
exp[-i alpha sin(sqrt(v)(a+a^dagger))]|0>; the second is |0>, since the
excited mode has departed. They differ for every v>0 and alpha!=0: the
Gaussian spectral measure has positive density, and the phase
exp[-i alpha sin(sqrt(v)X)] is not almost everywhere constant. Its vacuum
expectation therefore has modulus strictly below one. The first output's
mean is exactly v alpha^2[1+exp(-2v)]/2>0; the second has zero mean.
Both chronologies can use finite smooth pulses with disjoint supports.
The source marginal in this example is unchanged.

This failure identifies missing waveform information, not a physical
limit on concurrent control. Endpoint calibration needs a declared pulse
family or a separate path-error contract to certify the memory operation.

## 9. Consequence and remaining physical scope

The theorem permits reuse of a finite calibrated nonlinear model across
adaptive computations, including the retained memory state itself.
Stabilizing first moments suffice for the declared passive-parameter
uncertainty; nonlinear dynamics and occupied correlated memory are allowed.
Known Duhamel, Gaussian-characteristic and channel-composition methods are
used where strongest. No generic process-learning or hardware advantage is
claimed.

Calibration starts, selective controls, known passive pulse family, native
canonical ports, thermal independence and permanent departure remain
physical resources. Each execution contact consumes a fresh thermal mode
after calibration. A solver must retain the correlated state and supply
its own numerical allowance. Preparation, model comparison, statistical
failure, physical noise and total workload error remain distinct. The
old baseline continuum certificate does not transfer to this architecture.

## 10. Exact executed conditional example

The standalone `reusable_memory_certificate.py` uses integer square-root
enclosures and Fraction arithmetic. For (4) it certifies

    Gamma_bar <= 0.042041255959648729.

A compatible nominal model is vhat=2, thetahat=pi/2, nhat=1/20000.
If supplied calibration intervals certify

    |sqrt(v)-sqrt(vhat)|<=1/100000,
    |theta-thetahat|<=1/10000,
    |n-nhat|<=1/1000000,

then 1,000 contacts of source action at most 1/100 each have complete
retained-output model-comparison distance at most

    0.005308353946532403.                               (15)

This is conditional on those intervals, the known common waveform and
all structural premises. They are not measurements and were not acquired
by the predecessor six-table fixture. The bill includes 1,000 fresh thermal
modes and total source action at most 10; source/control/record storage and
actual delivery time remain additional resources. A small comparison
allowance is not a workload success probability.

The executable independently checks 36 exact thermal geometric distances,
the heavy-tail partial sums through k=64 and their finite J-row bound, and
a quantitative equal-area counterexample. For v=1/16, alpha=1/100, its
one-photon amplitude in the excited retained state obeys

    |<1|exp[-i alpha sin(sqrt(v)X)]|0>|
       >=alpha sqrt(v)-(alpha+alpha^3)v^(3/2)/2
        =309999/128000000=0.0024218671875.

Here X has unit Gaussian vacuum variance and <1|f(X)|0>=E[X f(X)]. The
global cubic sine remainder and E[X^4]=3 prove the inequality. The output
half trace distance from vacuum is at least this orthogonal amplitude.
Thus the same endpoint calibration permits observably different retained
outputs when waveform ordering is not supplied. No nonlinear trajectory
solver or truncated Fock dynamics is used in this certificate.

## 11. Strong conventional comparison

Energy-constrained channel continuity is established machinery, not an
invention of this tranche. Shirokov and Holevo, arXiv:1812.07447, relate
continuity/differentiability to the generator; their Proposition 1 supplies
linear continuity when the relevant constrained generator is bounded.
Becker and Datta, arXiv:1810.00863, develop fractional energy-constrained
norms and attenuator/amplifier examples. Becker, Datta, Lami and Rouze,
arXiv:2006.06659, compare different Hamiltonians under energy constraints;
their supplementary Example 6 even includes a full sine oscillator coupling
when comparing bounded spontaneous-emission noise. These primary sources
were read at those precise statements and models.

Pure-loss calibration and constrained comparison are also established:
Nair, Phys. Rev. Lett.121,230801(2018), arXiv:1804.02211, treats beam-splitter
loss sensing and energy-constrained channel fidelity. For a source-off
passive contact an exact conventional Gaussian-channel calculation should
be used wherever stronger. The novelty sought here is narrower: acquire
and propagate an operation-specific generator-row contract while a full
nonlinear source remains active, stabilize it across reuse, and connect a
physically anchored finite calibration to the complete retained-memory
instrument. An equally informed conventional approach can use this same
proof and inverse. No statistical or computational superiority follows.

The most direct general comparator is van Luijk, *Energy-Limited Quantum
Dynamics*, Commun. Math. Phys.406,120(2025),
https://doi.org/10.1007/s00220-025-05282-w, Proposition 5.1 and Lemma 5.2.
It gives energy-constrained Duhamel comparison along energy-gain bounds.
The new restricted-input J row is compatible with that framework: it uses
fresh-product structure instead of asserting that an arbitrary quadratic
generator is bounded by sqrt(N). Its source-reading record is saved in
../challenger/THERMAL_CONTACT_SOURCE_COMPARISON.md.
