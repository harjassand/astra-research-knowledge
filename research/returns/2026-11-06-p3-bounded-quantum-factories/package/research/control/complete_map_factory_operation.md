# Complete-map factories with bounded coherent quantum resources

5 November 2026. This closes the physical composition operation under an
explicit acquired stationary Pauli circuit model. Inputs are the accepted
uniformly mixed bounded-interval ensemble, local inverse theorem and
static-tree history-erasure theorem. Their mathematics is not reproved.
The new operation compiles complete CPTP maps into mixtures of actual noisy
bounded circuits, and uses a fixed all-interval schedule.

## 1. Operation

Let a known N-qubit target admit

    rho_N = E_mu tensor_(A in P_mu) tau_(mu,A),
    |A|<=B,       tau_(mu,A) >= eta I_A/2^|A|,

where P_mu consists of contiguous intervals and B,eta>0 are independent of
N and accuracy epsilon. Fixed-temperature finite-range 1D Gibbs states are
the accepted main source, including noncommuting/nonuniform Hamiltonians.
Here eta is the working floor after finite leaf approximation; decrease the
accepted floor by a fixed factor if necessary.

Under the physical model below there is p_*(B,eta)>0 such that fixed native
fault rate p<p_* permits global trace accuracy epsilon with growing protected
classical computation but these coherent quantum bounds independent of N
and epsilon:

    factory width W <= 3B + fixed interpreter workspace,
    padded factory duration G native ticks,
    data lifetime <= C G ticks,       C=B(B+1)/2.

The data-stage quantum hardware and gate count grow extensively in N, with
potentially enormous fixed factors. Total quantum work also includes all
calibration probes and all physical fair-coin probes used by the classical
algorithm; these counts can grow with requested accuracy. Every preparation,
reset, routing, selection, calibration and release operation is paid. No growing quantum code is used,
including in the controller or acquisition. This is a circuit-model theorem,
not a favorable total-resource or experimentally useful threshold claim.

## 2. Physical model

Use a fixed finite universal native quantum alphabet of bounded arity, plus
reset, discard and constant-size measurement. Basis-preserving NOT/CNOT/
Toffoli and fixed noisy links supply classical computation. If a controlled
alphabet gate is not native, compile its fixed controlled circuit and count
its synthesis error and all its physical gates. Finite synthesis precision
is fixed by B,eta; no analog angle is given inverse-polynomial precision.

Every outgoing native wire is independently followed by the same unknown
stationary one-qubit Pauli channel P. Reset/readout/capture templates are
specified circuits with this noise, not separate unknown SPAM channels.
Stationarity and independent future faults are model assumptions; calibration
estimates parameters and does not certify unrestricted drift. The entirely
classical repetition controller and raw-pool export are constructed in
classical_only_export.md. The corrected controller uses strict repetition-
five blocks, two refresh rounds per EC, and direct fresh physical majority-
five decoder trees for raw export. Its logical fair-coin initialization and
noisy probe-record capture are constructed in that same note; no growing
quantum controller or ideal classical random source is supplied.

Each factory has hardwired bounded quantum ports. All opcodes, enable/phase
flags, within-cell address choices, buffers, switches, ancilla reset, data
idles, transport and release occur inside its specified finite circuit and
acquired map. Wrong controls may apply different gates or multiple gates
within those ports. No requested inactive cell is assumed to be identity,
and no final physical selector is perfect.

The model is synchronous with bounded native slots. Fixed padding includes
admitted timing/control faults and bounded waiting. Unbounded clock
excursions, unmodelled analog pulse drift, or faults acting on distant
unlisted ports lie outside that law. Every comparator must receive the same
timing, topology and routing model. A fixed schedule alone proves nothing
about arbitrary-clock robustness.

One explicit fixed-support realization is a spatially unrolled layered
circuit fabric. Each layer has permanently wired disjoint interval cells;
data indices follow predetermined bounded-length noisy paths between layers
and to final ports. Paths do not depend on the random partition. Pay every
layer cell, transport wire and native link use. An overlapped reused chain
with arbitrary always-on intercell residual couplings is not automatically
an instance. Locality of admitted faults remains essential. Inside a cell,
faults may freely cross an intended **ensemble** cut.

## 3. Complete-channel convex compiler

For k<=B, d=2^k, use normalized Choi matrices

    K_d={J>=0 : Tr_out J=I_d/d},       J0=I_(d^2)/d^2.

The affine tangent space consists of Hermitian X with Tr_out X=0. If
J(F)>=a I, its relative Hilbert-Schmidt ball of radius a lies inside K_d.
Let J(U_j) form an r-net of K_d and let actual channels T_j obey

    ||J(T_j)-J(U_j)||HS<=e.

For any unit tangent direction u, support functions give

    h_conv{J(T_j)}(u) >= h_Kd(u)-(r+e)
                      >= <u,J(F)>+a-r-e.

If r+e<a, separation proves

    F=sum_j w_j T_j,       w_j>=0,       sum_j w_j=1,

with hull margin at least a-r-e. This is complete process equality on all
inputs and references, not merely matching one reset output. The weights
are obtained by finite-dimensional linear feasibility on Choi entries.
Strict margin tolerates finite numerical error. There are no negative
sampling weights, quasiprobability cancellations or postselection.

### Finite library, bounded duration

A k-qubit CPTP map has Stinespring environment dimension at most d^2. Its
unitary dilation therefore needs at most 3k quantum registers, followed by
environment discard. Reset and finite-alphabet unitary synthesis at fixed
accuracy give a computable finite net with maximal word length L(B,a).

Use a padded length-L word over a finite alphabet of gate opcodes and
within-cell locations. A fixed bounded-choice interpreter evaluates an
opcode at each slot and applies the indicated controlled gates on fixed
ports. All tests, controls, buffers and resets are noisy and counted. Invalid
words have a specified default action. There can be R=A_opcode^L words,
while physical duration is only

    G=O(L times fixed within-cell interpreter cost),
    m=O(L log A_opcode) program bits.

It is not an R-way coherent multiplexor, and duration does not grow with R.
The classical LP may retain only a certified net subset. Erroneous opcodes
outside that subset are still included in each actual channel. Every
program word is supplied as a classical mixture rather than a coherent menu
superposition. Any local coherence produced inside an imperfect synthesized
interpreter is included in its bounded workspace and reset after that slot.

Finite gate synthesis is prior machinery: Barenco et al., *Elementary gates
for quantum computation*, https://arxiv.org/abs/quant-ph/9503016 ; Dawson
and Nielsen, *The Solovay-Kitaev algorithm*,
https://arxiv.org/abs/quant-ph/0505030 . Growing precision is in classical
coefficients and calibrated descriptions, not physical pulse precision.

### Final noisy selection is included

The protected classical prefix samples desired word j. Its m raw program
bits come from the classical repetition/raw-pool/tree compiler. Up to its
separate discrepancy, each bit passes through a fresh BSC(r_h), where
r_h=F_P^h(0)<=2s=O(p), independently of old records. Define T_j(P,h) as
the whole channel with those noisy program bits, noisy interpreter, reset,
transport, padded idles and release. It is CPTP even if a wrong word is
executed or microscopic errors join intended blocks.

If G counts primitive stochastic locations and s<=c_s p, coupling to a
fault-free word gives

    ||T_j(P,h)-U_j||diamond <= 2(Gp+m r_h)
                              <= 2(G+2m c_s)p.

This also bounds the Choi Hilbert-Schmidt perturbation e. It is uniform
in h,N,epsilon. A sufficiently small fixed p preserves the fixed hull.

## 4. Fixed all-interval composition

Enumerate intervals of lengths k=1,...,B. Group length-k intervals by start
index modulo k, giving C=B(B+1)/2 disjoint-interval layers. Add singleton
parking cells at uncovered sites in each layer, so every output site is in
exactly one call per layer. For N>=B,

    M <= NB + 2 sum_(k=1)^B k(k-1)=NB+O(B^3),
    and always M<=CN.

For N<B use a single bounded block. Pad all cells to G including root reset,
delivery and release, and include fixed noisy transport in their maps. No
data site has an uncounted idle or wait between layers. Quantum initialization
starts only after growing classical precomputation.

For source sample mu, each actual partition block I has one designated
active occurrence. Every other interval or padding cell has desired map

    D_gamma^tensor |I|,
    D_gamma(X)=(1-gamma)X+gamma Tr(X) I/2.

The active desired map is the replacer R_(omega_I). Active and inactive
maps are **both** compiled into mixtures of the same physical palette.
No noisy enable/disable mask is supposed to implement an ideal cut. The
mutable decision changes classical probabilities, while support and
schedule stay fixed.

Let t_i<C be the number of layers after the active occurrence of site i's
partition block. Choose fixed gamma>0 so that

    ||D_gamma^(t_i)-Id||diamond <= (3/2)C gamma

is inside the accepted product inverse radius for block floor eta. That
theorem gives

    omega_I=(tensor_(i in I) D_gamma^(t_i))^(-1)(tau_I),
    omega_I >= (eta/2) I/2^|I|.

Finite-precision inversion is classical and retains the earned local floor
and condition-number slack. Its residual is budgeted. No global inverse
is formed.

After the active replacement of I, no later active replacement touches it,
because the active intervals partition the chain. All later maps are product
depolarizers, even when their interval crosses several partition blocks.
Their restriction to I is tensor_i D_gamma^(t_i), yielding tau_I exactly.
Every site is replaced once, so arbitrary initial data-reference
correlations are erased. Conditional on mu, the whole desired circuit is
the replacer for tensor_I tau_I. Averaging mu gives the replacer for rho_N.

This is the missing composition operation: an inactive **physical branch**
can entangle across a cut, while its complete compiled mixture is the needed
product channel on arbitrary input. State-only palette inversion would not
have established this.

## 5. Fixed threshold and its unfavorable constants

For d=2^k,

    J(R_omega)>=(eta/2)J0,
    J(D_gamma^tensor k)>=gamma^k J0>=gamma^B J0.

The second inequality follows from the one-qubit Choi matrix
(1-gamma)|Phi><Phi|+gamma I/4. Put

    mu=min(eta/2,gamma^B),        a=mu/4^B.

Every desired map has Choi floor at least a. Choose net radius r<=a/4
and its fixed interpreter, then choose p_* below the classical threshold,
the tree small-noise bound, and

    2(G+2m c_s)p_* <= a/4.

Thus r+e<=a/2 uniformly in N and epsilon. The factors gamma^B, 4^B, G
and m remain explicit fixed constants. They can make p_* unusably small.
A positive constant theorem is not an engineering threshold estimate.

## 6. Acquisition without quantum fault tolerance

The unknown homogeneous Pauli law has three independent parameters. Use
the accepted opposite-sign idle-contrast protocol on each Pauli axis, with
constant-size quantum probes and classical-only protected record capture:

    m_t=A_axis lambda_axis^t,       lambda_axis=m_1/m_0.

Stable noisy preparation, measurement and capture response enter A_axis;
opposite signs cancel additive offsets. Its magnitude is bounded below
at small p. Hoeffding estimation gives parameter accuracy zeta with
O(zeta^-2 log(1/delta_acq)) trials per axis. All accumulation, reset,
routing and classical protection costs count. There is no ideal record
import or protected quantum tomography simulator.

Given estimated P, evaluate each bounded T_j(P,h) by ordinary classical
matrix/channel simulation. Matrix dimension and circuit length are constants
in B,eta, though immense. The growing reference tree is summarized by the
finite scalar recursion r_h=F_P^h(0), using certified finite precision.
The control note proves the uniform sensitivity

    |r_h(P)-r_h(P')| <= g_F TV(P,P')/(1-alpha).

Consequently, for L_cal=2[G+m g_F/(1-alpha)],

    ||T_j(P,h)-T_j(P',h)||diamond <= L_cal TV(P,P').

Acquire zeta=O(epsilon/(M L_cal)). A sufficient constant-coherence probe
count is

    O((M L_cal/epsilon)^2 log(1/delta_acq)),

before separately counted protected classical processing. It does not need
an extra factor equal to the number of nodes in a regenerator tree. Project
estimates onto the physical Pauli simplex in an admitted compact domain;
a strict hardware margin and confidence intervals make this certified under
the model. No finite experiment certifies arbitrary future drift or iid
noise against all alternatives.

For digitally specified target H, there is no fabricated holding Hamiltonian
to learn, no need for individually isolatable check couplers, and no Davies
bath. If the target is instead an unknown physically fabricated H, a separate
compatible Hamiltonian-acquisition operation is still required. The earlier
memory's acquisition assumptions are neither inherited nor removed for that
different task by this digital-source theorem.

## 7. Finite bits, process error and records

The local LP dimension and menu size are fixed at B,eta. Finite-precision
channel descriptions and rational mixture weights with certified residuals
suffice. A fully elementary fallback enumerates a fine rational probability
grid until interval arithmetic certifies a small Choi residual. Hull
inclusion guarantees termination. The fixed-dimensional conversion

    ||Phi-Psi||diamond <= d ||J(Phi-Psi)||_1
                       <= d^2 ||J(Phi-Psi)||HS

turns it into a process error. Rational random selection uses binary uniform
integers and capped rejection with an explicit tail budget. No ideal real-
valued physical selector or varying analog gate precision appears.

Keep the inherited efficient mixed-block sampler's numerical convention
separate from independent finite-bit complexity. The latter is closed in
../architecture/finite_bit_decomposition_fallback.md: compute a dense Gibbs
matrix to certified finite precision, enumerate rational positive block
nets and all bounded interval partitions, solve a rational convex LP, and
sample the resulting weights. This can cost exp[O_B(N^2+N log(1/epsilon))]
or worse once solver overhead is included. It is computability closure,
not a near-linear or practical source. Block-state grids refine with epsilon
but preserve a fixed floor; therefore the **same** fixed quantum palette
works by changing only classical weights.

Using trace distance for states, a conservative error budget is

    error <= epsilon_source + delta_prefix + delta_tree + delta_acq
             + M(epsilon_LP + epsilon_leaf + L_cal zeta)
             + epsilon_sampling.

Allocate fractions of epsilon to these terms. Use per-call diamond residuals
and forward telescoping of CPTP channels. There is no inverse-channel norm
on the full N-qubit system. All local comparisons are complete process
comparisons, so arbitrary external references and old records can remain.

New fine partition, palette, opcode and tree records correlate with the
prepared state. For a record-free Gibbs output, erase/discard them at cost.
Reset growing scratch locally in parallel after its last use; reset raw
roots, opcodes and flags inside each padded G-tick factory, with all data
idles during that reset/release included. There is no long post-preparation
erasure wait. A replacement reset followed by fresh noise exactly removes
old information; no perfect surviving zero is necessary. If records are
retained, report the actual cq extension instead of claiming that its
conditional quantum state is Gibbs.

Under stationary reuse, component acquisition can be paid once. Across many
runs, the full discrepancy is bounded by the acquisition failure probability
plus the sum of fresh source/control/interface budgets. Old records may
remain throughout: fresh fault locations and paid history erasure earn the
reference maps. Uniform sensitivity controls all uses of the common learned
parameters; conditioning on a fortunate calibration record is unnecessary.

## 8. Full resource ledger and consequence

At fixed B,eta, the coherent quantum DATA schedule has C layers, M<=CN calls,
W bounded coherent registers per call, and G bounded native ticks. Its
spacetime, native gates, reset and transport cost is O(M G W), including
delivery and environment reset. This is the data stage, not total quantum
activity. Let Q_acq be the actual number of constant-size calibration probes
and Q_coin the actual number of noisy |+>/Z fair-bit probes consumed by the
source, coefficient sampling, capped rejection and all other classical
randomness. The implemented logical coin uses one raw fair seed followed by
complement-covariant classical encoding and a final high-level EC, so each
such seed is included in Q_coin. A variant using 5^j independent raw coins
per encoded coin must charge all 5^j probes instead. Neither convention is
an ideal free classical entropy source.

With G_acq and G_coin the complete bounded quantum reset/preparation/readout
costs per probe, total quantum work and spacetime include

    O(M G W + G_acq Q_acq + G_coin Q_coin).

Probe-record capture, coin encoding, protected storage and computation have
additional classical costs. A reusable bounded probe/coin module suffices
before output initialization, preserving bounded coherent width and lifetime
while its total work and elapsed time grow. All probe cooling and resets
are paid. An unrolled fixed data fabric costs O(N) hardware
times C,G,W-dependent factors. A reused physical layout needs its actual
switching/noise law included before claiming the same accounting.

Classical cost includes source computation, every local channel simulation
and LP, rational sampling, parameter acquisition counters, strict repetition-
five protection, and M m 3^h raw-leaf exports with physical five-ary decoder
trees. Growing routing,
storage and synchronization occur before quantum initialization and remain
paid. Total elapsed time is the whole classical preparation time plus CG;
total spacetime includes growing classical memories/links and all probes.

Charge every gate, cooling step, reset, pulse, data transfer and fabrication
assumption under the specified apparatus cost model. Any thermodynamic
erasure claim includes extensive information/heat expenditure; bounded
coherence alone yields no energy advantage. The fixed-port topology,
programming verification, native synchronization and acquired stationary
primitive law are real resources rather than free physical conclusions.

The broad earned conclusion is that known interacting mixed states in this
class need no coherent quantum processor or quantum error-correcting block
whose size or lifetime grows with global accuracy. Growing reliable
classical control plus fixed noisy quantum cells suffice in one specified
model. Complete-map interiors resolve actual noisy composition across
random ensemble cuts, which an ideal block source or positive state inverse
alone does not do. No favorable total-resource comparison with ordinary
fault-tolerant preparation or qLDPC interfaces follows; they receive the
same controls, acquisition, cooling, routing, timing and target access.
The generic sufficient constants may defeat any engineering benefit while
the foundational bounded-coherence conclusion remains.

The guarantee is at the specified physical release time. Protecting the
delivered state for an additional growing hold interval is a separate
operation and does not follow from bounded preparation time.

