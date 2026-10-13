# Controlled-matter audit and restricted synthesis

Capital pin: `097d135f76ebefc49a8e5f28a8363e9ae372c061`.
Date: 13 October 2026. Status: internally reconstructed arguments and exact/floating
synthetic diagnostics, unreviewed. External correctness, priority, specimen-level
validity and technological advantage remain unresolved.

## 1. Disposition and capital fit

The submitted controlled-matter packet is a valuable negative continuation of
N774, not a second demonstrated pump or a manufacturing breakthrough. Preserve
the original independent-ion construction and its direct-force counterexample.
Append the new material-specific qualification, local-basin symmetry restriction,
control-rank nonidentifiability construction, dielectric-retention requirement and
SiC pivot failure. The packet does not establish the missing K-beta control pair.

I read `00_START_HERE.txt`, `agent/COMPOSITION.txt`, `state/CONTINUITY.md`,
`technology/README.md`; the scoped N774/N767/N770/N771 dossiers and gates;
the N774 branch view; N774's integration derivations (direct-force falsifier,
sharp stored-elastic-energy bound and causal/thermodynamic account); the complete
new packet report/script/source ledger and pasted text. N498/N490 dossiers were
checked as context for material-time and committor acquisition limits, not used as
proof premises. No theorem from N767/N770 supplies the new lattice material.

The source archive has seven members, a passing ZIP CRC, and six matching producer
SHA256 pins. The inspected producer script was replayed only in a disposable
copy. Its 24 symmetry fixtures, two synthetic potential cases, 18 damped-loop
quadratures, four PNP modes, continuity check and three hazard doses pass. These
are algebra checks. No atomistic potential, material response or physical
measurement was acquired.

Three additional consequences are derived below: an attainable harmonic-loop
bound in units of damping work; an adaptive endpoint-selectivity certificate
strictly broader than uniform acceleration; and a counterexample to inferring
relative rare endpoint yields from a fixed relative spectral-form approximation.
They refine the decisive acquisition target. They do not close the physical gate.

## 2. What the new source establishes, and what survives

Under ideal bulk D6h, long-wavelength electric-dipole excitation and bilinear
response, the E2g Raman tensor R times an E1u infrared vector P transforms as an
allowed in-plane polar current. E2g x A2u is E2u and cannot supply that bulk polar
current. The angular direction `(cos(2 theta_R-theta_I), sin(2 theta_R-theta_I))`
follows from the stated calibrated representation. It is not a unique mechanism
signature: Raman-modulated direct electromigration has the same tensor symmetry.

For a *whole occupied basin* invariant under C3, its scalar free-energy gradient
cannot have a linear E2g component. This is a necessary local check, not a K-beta
no-go: oriented collective defects can break local symmetry. The independent-ion
two-state mapping cannot be licensed merely by observing an E2g mode.

The packet's synthetic family

    V_sigma(s,Q)=B sin^2(pi s)
      +kappa/2 [(Q1-d cos(pi s))^2
                +(Q2-sigma eta sin^2(pi s))^2]

has well Hessians `diag(2 B pi^2,kappa,kappa)` and relaxed barrier B independent of
eta, while the fixed-control linear response is
`A=diag(2 kappa d,-kappa eta)`. Rank one at eta=0 becomes rank two at nonzero eta.
I checked the envelope logic: at Q=0, the constrained saddle is stationary at
s=1/2; its first derivative under Q is the displayed envelope derivative. With
positive B and sufficiently small d, the constrained reference wells remain
stable. This does not assert identical saddle Hessians or transition prefactors.
It refutes the named information transfer from well phonons plus relaxed barriers
to mode-constrained control rank. A finite-dimensional synthetic path family is
not an atomistic force field or a proof of material attainability.

The damped unequal-frequency area formula is correct for the specified unshaped
ringdown. It bounds no arbitrary shaped protocol. A closed structural area does
not alone predict nonadiabatic correlated ion transport.

Linear one-carrier continuity and Poisson coupling give, for a nonzero Fourier
mode, decay rate `D_chem k^2+sigma/epsilon` (with the stated anisotropic conversion
when needed). The target-derived 10 nm/one hour/90 percent requirement is
`2.9266809905e-5 /s`; neutral diffusion alone requires
`D_chem<=7.4133695525e-23 m^2/s`. This is a homogeneous constitutive-model result,
not a no-go for traps, compensation, reactions or stable phases. Uniform drift
does not write a composition pattern. Retention needs a specified captured
endpoint, mass/charge balance and a reverse-process account.

N774's full leading phase-odd direct-force false positive remains valid. New bulk
angular signatures do not remove it. A new source notice should strengthen the
specimen acquisition gate rather than withdraw the conditional mathematics.
N767/N770's measured-response-before-device strategy is a useful *workflow*
analogy; its negative-real-admittance equations and material parameters do not
transfer into ionic pumping.

## 3. Sharp harmonic-loop bound on the accessible control subspace

This consequence combines N774's geometric coefficient with the new packet's
dynamic susceptibility and explicit damping cost. Assume:

* small harmonic physical coordinates `Q(t)=Re(q exp(-i omega t))` at omega>0;
* real site and directional-path derivatives g,h, so `u-u0=g^T Q`, `v=h^T Q`;
* the same one-pole independent-ion model as N774, with
  `chi=p0(1-p0)` and `R=lambda^2/(lambda^2+omega^2)`;
* a passive real symmetric positive-definite damping matrix Gamma, in consistent
  mass-weighted coordinates; and a periodic host response without uncharged
  initial stored-energy release.

Let

    H=(g h^T-h g^T)/(2i),
    A=[g^T;h^T],
    S(q)=Im[(g^T q)^* (h^T q)]=q^* H q.

The oriented area in (u,v) is pi S(q). N774's leading contribution odd under
reversal of that trajectory is

    Delta x_odd=-(pi a/2) beta^2 chi R S(q).                 (1)

Finite-rate even terms, calibrated direct forcing and other mechanisms are not
included in (1). In particular, a total observed current cannot be substituted
for this selected contribution.

The damping loss per cycle and mean damping power are exactly

    W_damp=integral_0^(2pi/omega) dot Q^T Gamma dot Q dt
           =pi omega q^* Gamma q,
    P_damp=W_damp omega/(2pi)
           =omega^2 q^* Gamma q/2.                        (2)

Define `M_Gamma=A Gamma^-1 A^T`. Then

    |S(q)| <= (1/2) sqrt(det M_Gamma) q^* Gamma q,

and hence

    |Delta x_odd|
      <= [a beta^2 chi R/(4 omega)] sqrt(det M_Gamma) W_damp.
                                                               (3)

Proof. Conjugating H by Gamma^-1/2 gives a rank-at-most-two Hermitian matrix built
from real vectors b=Gamma^-1/2 g and d=Gamma^-1/2 h. On their plane its nonzero
eigenvalues are
`+/- sqrt((b^T b)(d^T d)-(b^T d)^2)/2`.
The Rayleigh quotient is bounded by their magnitude, which equals
`sqrt(det M_Gamma)/2`. Equations (1) and (2) prove (3). Its coefficient is attained
by corresponding complex eigenvectors in the unrestricted harmonic subspace.

Actual optical drives access a smaller subspace. At a fixed omega write

    q=C(omega) f,
    C=[K-omega^2 I-i omega Gamma]^-1 B,
    G=C^* Gamma C,  H_C=C^* H C.

B maps the independently controllable force amplitudes into the physical
coordinates. Assume dependent zero-response columns have been removed and G>0.
Then the *exact mathematical interval* of accessible area per damping work is

    S/W_damp in [lambda_min,lambda_max]/(pi omega),
    lambda_min/max=eigenvalue extrema of
       G^-1/2 H_C G^-1/2.                                 (4)

Proof. Substitution makes the ratio a generalized Hermitian Rayleigh quotient.
Its endpoint eigenvectors attain the extrema, and continuous interpolation of
unit vectors spans the interval. Thus

    |Delta x_odd| <= [a beta^2 chi R/(2 omega)]
                    max(|lambda_min|,|lambda_max|) W_damp. (5)

This can be much smaller than the unrestricted bound (3). Both signs of the area
are attainable iff `lambda_min<0<lambda_max`. A zero extremum permits zero area,
not both nonzero orientations. If field-amplitude, phase, Raman-force or damage
constraints exclude an eigenvector, (4) is an upper envelope, not an attainment
claim. Raman force is ordinarily quadratic in optical field; no arbitrary complex
f is supplied for free.

### One drive can enclose a loop yet cannot reverse it by global phase

Take dimensionless `K=diag(1,4)`, `Gamma=diag(.2,.3)`, `B=(1,1)^T`, omega=1.5,
g=(1,0), h=(0,1). There is one force channel. For a unit force, the measured-form
linear response yields `S=-.20156012167744` and `W_damp=1.00332585158538`.
Multiplying f by any phase only multiplies S by |f|^2, so the area has one fixed
sign. The two modes' different phase lags create the loop. The number of drive
channels is therefore not the rank of the real trajectory; conversely, a nonzero
loop does not establish independently reversible control.

This is a synthetic exact linear-system construction, numerically evaluated.
It is compatible with N774's narrower claim that rank-one *in-phase instantaneous*
responses have zero leading geometric area. The new source already avoids a
universal rank-one no-go; do not introduce one in the intake.

### Cost and acquisition limits

W_damp is energy dissipated in the selected passive host coordinates, not total
wall-input energy. Mode preparation, optical conversion, parasitic absorption,
ion/control backaction, direct electrical work, heating removal, contacts and
postprocessing remain charged. Initial ringdown energy must be paid. The bound
does not describe an active fueled gain medium such as N767/N770. If G is singular,
a pseudoinverse cannot silently remove directions whose area or cross terms have
zero recorded cost; additional cost or an exact range restriction is required.

At fixed P_damp, equations (2)-(3) give

    |Delta x_odd| <= [pi a beta^2 chi R/(2 omega^2)]
                      sqrt(det M_Gamma) P_damp.

This apparent low-frequency divergence is not a free advantage: maintaining
fixed power drives coordinate amplitudes as 1/omega and eventually exits the
small-control and damage domain. At fixed work per cycle the mean speed is
`omega |Delta x|/(2pi)`; at fixed power a different optimization results. No
frequency optimum survives without an acquired amplitude/field/thermal budget.

The decisive experimentally useful object is therefore the *same-specimen*
frequency-dependent pair `(H_C,G)`, with uncertainties and legal forcing set,
together with a validated transport model. Phonon peaks alone determine neither
matrix. Generalized Rayleigh optimization and thermodynamic friction metrics are
established mathematics/prior art; the new item is this restricted consequence
for the N774 acquisition contract, not an invented general control theory.

## 4. Endpoint selectivity is controlled by a committor, not by a clock

The source proves a well-mixed common-hazard statement. The following extension
allows arbitrary finite spatial/configurational networks and adaptive controls.
It identifies exactly which acceleration directions can never change eventual
capture yield, even when their kinetics are very different.

Let a finite configuration set contain disjoint absorbing target T and unwanted
sink B; all other states are transient. For a baseline CTMC generator L0, let
q(x)=P_x(hit T before B), so `q=1` on T, `q=0` on B and `L0 q=0` inside.
Assume this *configuration-level* q is acquired or certified, not merely guessed
from a projection or a thermal mobility number.

Consider any nonexplosive controlled CTMC with bounded, predictable legal rates
L_t, potentially chosen from the full past history. Define tau as first arrival
in T union B. If every legal control obeys

    L_t q=0 in every transient state,                      (6)

then `q(X_(t min tau))` is a bounded martingale. Consequently at every finite time

    P(already captured in T by t)
      + sum_x transient P(X_t=x,t<tau) q(x)=E[q(X0)].       (7)

If tau<infinity almost surely, bounded convergence gives

    P(eventually captured in T)=E[q(X0)]                   (8)

for *every* adaptive control satisfying (6). No finite mean time is needed for
this equality. A control that freezes uncaptured defects permanently fails the
completion premise; its unfinished mass must stay in (7).

Proof. The stopped Dynkin compensator is
`q(X_(t min tau))-q(X0)-integral_0^(t min tau)(L_s q)(X_s)ds`.
Bounded rates/finite state make its finite-time expectation zero. Under (6) the
integral vanishes. Splitting the expectation into target, bad and transient states
gives (7); bounded convergence under eventual absorption gives (8).

An important sufficient subclass is state-dependent clock control:

    k^u_xy(t)=a_x(t,history) k^0_xy, a_x>=0.

All outgoing destination ratios from each state are unchanged and
`L^u q=a_x L0 q=0`. This is strictly broader than a single global mobility
multiplier. Even nonexponential waiting-time modifications preserve the eventual
endpoint assertion if the embedded destination probabilities remain fixed and
absorption eventually occurs. Ionic memory alone is not an escape; a changed
destination law or a changed physical endpoint is required.

Condition (6) is broader still: different edge ratios can cancel on this selected
objective. For the synthetic chain with states (0,1,2,T,B),

    L0: 0->1,B at rates1,1; 1->0,2 at1,1; 2->1,T at1,1,
    L1: 0->2,B at1,2; 1->T,B at1,1; 2->0,T at1,2,

both have q=(1/4,1/2,3/4,1,0), although L1 is no row scaling of L0.
Any adaptive switching preserving these generators' scope has the same eventual
target yield, provided absorption completes. This is an objective-specific
condition, analogous in purpose to N771's `M lambda0=0`; its proof is independent
of the chemical adjoint model and no Jacobian/interface theorem is imported.

### Finite-pulse conditional selectivity can change under a uniform clock

Use two transient states x0,x1 with

    x0 -> T at rate1; x0 -> x1 at rate1; x1 -> B at rate1,

starting at x0. Let s be integrated global mobility dose and z=exp(-s). Then

    P(T by s)=(1-z^2)/2,
    P(B by s)=(1-z)^2/2,
    P(T | captured by s)=(1+z)/2.                          (9)

At s=log2 the conditional good fraction is 3/4; at s=log4 it is 5/8. Both have
eventual good fraction 1/2. The correction from still-unreacted x0 is z^2/2, and
`P(T by s)+z^2/2=1/2` exactly. Speeding the same path dynamics can therefore alter
a finite-pulse conditional yield without changing ultimate destination choice.
The source's invariant finite-pulse conditional fraction is valid for its stated
one-transient-state, common-hazard model; do not extend that part to every network.
Conversely, this example does not invalidate its source theorem.

### A residual certificate and a necessary control target

For general controls, still at finite time,

    E[q(X_(t min tau))]-E[q(X0)]
      =E[integral_0^(t min tau) (L_s q)(X_s) ds].           (10)

Thus it is enough to acquire an *objective-specific generator residual*
`e_s(x)=(L_s q)(x)`, rather than reconstruct every rate to arbitrary accuracy.
This acquisition can still be hard: the true state includes collective defects,
charges, history or hidden coordinates wherever a Markov description requires
them. A projected q or projected generator without a certified closure is not a
legal replacement.

If every legal control has L^u q<=0, the stopped process is a supermartingale and
no adaptive protocol can exceed the baseline eventual target probability. For
|L^u q|<=delta and finite E[tau], equation (10) yields

    |P_u(T)-E[q(X0)]|<=delta E_u[tau].                    (11)

Units are probability/time for delta. The stopping-time moment must be acquired;
it is not supplied by observation of a fast local mode. A certified nonnegative
duration potential v, zero at sinks and with every legal `L^u v<=-1`, supplies
`E_u[tau]<=E[v(X0)]` by the same stopped argument. This can make (11) usable
without complete path sampling, provided v and its generator inequalities are
actually checked. No rare-event relative-error claim follows from additive (11).

For a concrete selective perturbation, add only edge1->T at rate1 to L0. The new
q is (3/8,3/4,7/8,1,0), the old-q residual is 1/2 at state1 and zero elsewhere,
and the exact yield corrections are (1/8,1/4,1/8). This shows a route that *can*
change selectivity: increase a transition toward a higher-committor state rather
than merely reparameterizing time. No actual SiC optical/charge cycle doing this
has been identified.

Detailed balance alone does not preserve endpoint selectivity. In the un-killed
five-node line B--0--1--2--T, all baseline symmetric edge rates are1. Raising only
0<->1 symmetrically to3 preserves uniform equilibrium of that closed chain but
changes its first-hit committor to (3/10,2/5,7/10) on (0,1,2). Killing B,T defines
the repair question; its boundary-value problem differs from equilibrium.

These statements are applications of standard committor, Dynkin and stochastic
control reasoning. They are not claims to have invented transition-path theory,
time changes or supermartingale certificates.

## 5. A 97-percent quadratic-form band does not certify relative rare repair yield

This root-proposed family was independently reconstructed as a precise generic
transfer falsifier. It does not assert that the spectral-matching source claimed
the false transfer.

Take an undirected unit-weight line x0,...,x_(n-1),T. Connect *every* transient xi
also to B by a unit edge. Stop at first T or B. In the modified graph multiply
only each failure edge xi--B by c in (0,1), leaving path and target edges alone.
Let Q1,Qc be the positive Dirichlet Laplacians on transient states. Edgewise
positive-semidefinite decomposition immediately gives

    c Q1 <= Qc <= Q1.                                    (12)

All baseline edge weights are1; all modified weights are c or1. Moreover

    c I <= Qc <= (c+4) I.                                (13)

The lower bound follows from the failure-edge term cI. For the upper bound, the
remaining path/target matrix is tridiagonal with first diagonal1, subsequent
diagonals2, offdiagonal -1; Gershgorin puts its spectrum below4. Thus the
Dirichlet condition number is at most (c+4)/c independently of n.

Nevertheless the relative target probability from x0 grows without bound as n
increases. Define u0=1,u1=1+c and

    u_(j+1)=(2+c)u_j-u_(j-1).

The committor equations have `h_i=u_i/u_n`, hence

    h0(c)=1/u_n(c).                                      (14)

Proof: the x0 equation is `(1+c)h0=h1`; the interior equations are
`(2+c)h_i=h_(i-1)+h_(i+1)`, with h_n=1 at T. The recurrence and boundary value
determine the unique solution.

The characteristic roots are

    lambda_+/- (c)=[2+c +/- sqrt(c^2+4c)]/2.

They obey `0<lambda_-<1+c<lambda_+`, and

    u_n=A_c lambda_+^n+B_c lambda_-^n,
    A_c=(1+c-lambda_-)/(lambda_+-lambda_-)>0,
    B_c=(lambda_+-(1+c))/(lambda_+-lambda_-)>0.

Since lambda_+(c) is strictly increasing in c,

    h0(c)/h0(1) ~ (A_1/A_c)[lambda_+(1)/lambda_+(c)]^n -> infinity.

For c=.97, (12) is a fixed 97-percent form band and (13) is a uniform conditioning
bound, yet there is no dimension-independent relative capture guarantee. The
baseline target is exponentially rare; additive absolute errors can stay tiny.
This does not refute absolute-error bounds or an explicitly supplied rare-yield
relative certificate. The mechanism is accumulation along a long absorbing
branch, not hidden exponentially large microscopic rates.

This joins the new spectral and controlled-matter work at a genuine obstruction:
a broad operator/spectral approximation can fail to preserve the consequential
rare endpoint. The repair is an acquired committor-weighted residual or comparable
relative endpoint certificate, not simply a tighter-looking global norm. That
repair's acquisition cost and rare-event conditioning remain open.

### Realization by the submitted matching law in its kinetic scope

The root identified a stronger interface; I reopened the spectral packet's
`RESEARCH_NOTE.md`, lines27-108 and154-216, and reconstructed it. Work in the
single-particle sector with eta=1. Replace the common bad vertex by n separate
leaves B_i, one attached to each x_i, and let B denote their union. The same
Dirichlet equations and committor hold because all B_i have boundary value0.
There are2n+1 graph vertices. Set the *single global* diagonal operator to
D(B_i)=2 and D=0 on all transient vertices and T.
Choose squared hopping amplitudes1/2 on path/target edges and2 on failure edges.
In the source's slow time tau=epsilon^2 t, the oracle rate
`2|T_xy|^2 gamma_*/(gamma_*^2+Delta^2)` is1 on every edge: gamma_*=1 on zero-detuning
path edges and2 on failure edges. Thus no independent fictitious linewidth
assignment or inconsistent edge detuning table is needed.

The actual common normal-inverse-Gaussian law has

    gamma_M(Delta)=[8 sqrt(225+16 Delta^2)-95]/25.

At Delta=0 it is1. At Delta=2 it is41/25 because sqrt289=17. Therefore all failure
edges have the exact rate ratio

    c=4(41/25)/[(41/25)^2+4]=4100/4181<1,

while path edges remain at ratio1. Equations(12)-(14) apply with this *actual*
matching c, and the relative rare endpoint ratio again diverges. Its phase noise
is the same globally CPTP construction; the global D has only the two stated
energy levels. Hopping amplitudes and detunings stay bounded per edge.

This is a mathematical first-hit functional of the source's finite kinetic graph.
It does not provide an irreversible quantum absorber or retention operation.
Such physical capture/readout can change linewidths and needs an added interface.
The leaf construction has maximum degree3 and uniform bounds `||D||=2` and
`||T||<=2sqrt2` by the Hermitian row-sum bound. No growing high-degree hub or
exponentially large microscopic rate is needed. Source reduction is nevertheless
fixed-finite-volume epsilon->0, not a relative first-hit guarantee at finite
epsilon uniformly in n. No exchange of long-time, weak-hopping and size limits is
made. The source itself explicitly
excludes arbitrary first-passage monotonicity (line193), so its capacity and
transport-form theorem is preserved. The refuted claim is a tempting stronger
transfer to relative endpoint selectivity, not the submitted theorem.

## 6. Primary-source audit and comparator update

The source access ledger is `PRIMARY_ACCESS.json`. The following are primary
source observations, not measurements performed in this run.

* [Minami et al., PRL124,147401](https://link.aps.org/accepted/10.1103/PhysRevLett.124.147401):
  accepted-manuscript text verifies Na-beta THz-current prior art, polarity,
  approximately50kV/cm threshold, approximately2pA maximum and fitted enhancement62.
  Na does not acquire K response. This strengthens N774's direct-force comparator.
* [Negi et al., PRB109,134105](https://arxiv.org/html/2309.14678v2):
  full author text verifies K-beta spacegroup194, the .72eV vacancy/.08eV collective
  interstitial barriers and their lower-bound/static scope. Beta-double-prime data
  cannot be borrowed as K-beta rates.
* [Colomban and Lucazeau, JCP72,1213](https://pubs.aip.org/aip/jcp/article/72/2/1213/218449/Vibrational-study-of-and-conduction-mechanism-in):
  primary abstract supports low-frequency cation modes and E2g assignment. Full
  K-specific eigenvectors, linewidths and a matched excited-mode pair were not
  acquired. Framework linewidths cannot be relabelled as that pair's damping.
* [Li et al., arXiv2610.05941v1](https://arxiv.org/html/2610.05941v1):
  full preprint verifies field-responsive AgCrSe2 simulations with separate drive
  and transport probe, collective barriers and Langevin thermostat. Probe-work
  density1.0625e17W/m^3 follows from reported sigma and field, not total drive work.
  This is driven-mobility simulation, not retained unbiased writing.
* [Karsthof et al., arXiv2111.01011v1](https://arxiv.org/html/2111.01011v1) and
  [Coutinho et al., PRB103,L180102](https://arxiv.org/html/2105.04209v1):
  primary text supports the carbon-injection task and distinguishes low-barrier
  interstitial rotation from1.8/2.2eV translation. A soft rotation does not produce
  a cell-to-cell transport cycle; electronic trap depths are not laser thresholds.
* [Rahman et al., APL Electronic Devices1,036103](https://pubs.aip.org/aip/aed/article/1/3/036103/3351973/Repeated-rejuvenation-of-SiC-MOSFETs-for):
  full primary HTML supports a two-device electrical-recovery comparator using
  current pulses. Functional recovery does not itself identify carbon-vacancy
  annihilation. The first PDF fetch succeeded only at metadata level; subsequent
  PDF/direct-download attempts failed; HTML then supplied the primary text.

A stronger **2026 comparator omitted by the submitted packet** was found:
[Chavda et al., Cold annealing..., doi10.1063/5.0304589](https://pubs.aip.org/aip/aed/article-pdf/doi/10.1063/5.0304589/20912243/016116_1_5.0304589.pdf),
published20February2026. Primary PDF text reports98–100percent electrical recovery
after Co60 damage with active cooling and estimated junction near20C. It explicitly
distinguishes oxide/interface charge damage from substantial bulk carbon-vacancy
creation. Its reported10V drain bias and7–10A current imply70–100W, whereas adjacent
text calls dissipation below48W. This is an unresolved internal numerical account,
not a reason to discard the electrical observations or claim carbon-vacancy repair.
Concurrent V,I and junction/cooling data are needed for a matched energy comparison.

The proposed low-temperature selective SiC vacancy repair must therefore beat
strong electrical comparators while establishing a *different microscopic
endpoint*, not merely be called nonthermal. No qualified new route was found.

Prior-art context was also checked: embedded jump chains/time changes (Lalley's
CTMC notes), E/Vanden-Eijnden transition-path committors, quantitative
supermartingale certificates, and Sivak/Crooks thermodynamic friction metrics.
These prevent novelty promotion of the underlying methods. This was not an
exhaustive literature or patent search.

## 7. Decisive next gates and reproducibility

For K-beta, first acquire a phase/stoichiometry/defect-qualified same-specimen
response: legal complex force map C, damping/work G, constrained collective
well/path derivatives g,h, full direct-field trajectories and uncertainties.
Precompute several phase/polarization/frequency predictions, including the
forbidden bulk channel and structural/direct-force alternatives. Validate the
correlated kinetic interface independently of fitting the driven current.
Electrical detection should be paired with a calibrated translation/tracer assay.
The predicted mixed displacement must exceed its actual sensitivity floor.

For retained repair, specify the desired and competing endpoints and acquire a
configuration-level committor or an independently certified superharmonic bound.
Test whether candidate controls have a positive relevant residual L^u q, and
charge its acquisition and exposure. Distinguish changed eventual yield from
changed finite-time completion. Test reverse transformation, sink capacity,
damage, addressing, throughput and total energy per *retained useful endpoint*.

Stop or pivot if only clock acceleration is available, if full-field baselines
explain the measured transport, or if no retained endpoint has a favorable
matched comparison. These are bounded acquisition experiments, not justification
to scale manufacturing claims or enlarge assumed amplitudes.

`derive_checks.py` contains an independent exact Fraction solver for 27 row-clock
scalings, shared/nonshared committors, residual corrections, a symmetric-edge
counterexample and the finite-pulse censoring fixture. It also checks the rare
capture recurrence against eight exact direct linear solves. Floating tests check
240 random harmonic controls,36 unrestricted endpoint/determinant identities,
24 restricted extrema and a one-channel loop. `derived_checks.json` is the result.
These diagnostics are not interval certification or physical validation.

Run from this folder with one BLAS thread:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      /Users/harjas/Documents/Codex/2026-10-13/new-chat/work/research-venv/bin/python derive_checks.py

Producer replay: `independent_replay.json`. All new mathematics is separately
identified from immutable producer files in `replay/astra_controlled_matter_audit/`.
No capital files, original attachments, Git history or checkpoints were modified
by this audit.
