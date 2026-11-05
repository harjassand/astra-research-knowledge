# Complete noisy thermal-register operation

Research construction, 5 November 2026. All distances below are half diamond
distance, or its induced adaptive-process distinguishing distance with arbitrary
logical references and retained external classical records. Constants are not
optimized. The accepted source compiler and passive bath theorem are inputs;
the new interfaces, precompensation and stopping-time bridge are proved in this
package. No nonequilibrium Davies basin is assumed.

## 1. Concrete model and the theorem

The physical memory has N qubits, a commuting Pauli stabilizer Hamiltonian with
positive bounded couplings, and the accepted decoder frame. Its valid syndrome
space is L. The equilibrium syndrome law is

    pi(s) = Z^{-1} exp(-sum_a lambda_a s_a),   lambda_a = beta J_a.

The history compiler has bounded degree and alphabet, additive coercivity, and
an instability witness of size L_*(N) >= c_* N^eta. At the chosen sufficiently
low fixed temperature, the strengthened Peierls tail below is available. The
specified local Pauli Davies bath has total syndrome jump rate at most C Gamma N.
Rates depend on the syndrome, not on the logical density matrix. These are the
accepted physical-class hypotheses, not consequences of active fault tolerance.

The chosen complete commissioning model uses the same unknown stationary
one-qubit Pauli channel Lambda at every specified outgoing primitive wire.
Preparation, reset, readout and record capture are known templates whose only
unknown fault parameters are those of Lambda. Faults at distinct locations are
independent. A broader class of known independent Pauli laws is sufficient for
the circuit lemmas, but the calibration proof does not identify arbitrary
independently unknown SPAM or gate-dependent maps.

The active architecture supplies noisy bounded-arity gates, noisy preparation,
measurement, discard and idle, and paid nonlocal links of specified duration,
error and cost. Constant-size bottom-code cells couple locally to the memory.
Coupler isolation and switching are paid native access with the stated fault
law. All arithmetic and decoding use the same noisy protected code. No ideal
encoder, decoder, classical controller, output selector or readout port is used.

There is a sufficient p_*>0 independent of N, the requested hold horizon and
interior accuracy such that, for p<p_*, the operation below has

    d_process <= C n_raw p + epsilon_total
                 + C [R N q + Gamma N T] b_N,

    q <= C_0 p,       b_N <= C_1 exp(-c N^eta).

Here n_raw counts external unknown raw entries and raw deliveries. Internal
decode/work/reload does not pay that original raw-input floor again. R bounds
the number of offered source/access opportunities; rejected or selectively
considered source candidates also count. In the basic sequential operation R
is, up to a fixed factor, the number of actual writes and reads.

For each offered source j, a deterministic cap T_j bounds that source's
intrinsic passive time, and T=sum_j T_j. A policy may read or abandon a source
adaptively, but cannot freely select a favorable candidate and then assign its
selected syndrome an equilibrium marginal. If only a pathwise total exposure
cap T_actual is known across at most J candidates/resets, the conservative
bound uses sum_j T_j <= J T_actual. A sharper adaptive-allocation theorem is
not asserted here.

The error epsilon_total includes source approximation, protected execution,
tree coupling, numerical sampling, parameter uncertainty and acquisition
failure. A finite commissioned source stream has one joint total-variation
budget, paid once. Each new physical preparation, candidate, refresh, decoder,
reset and occupied location is still charged.

## 2. Compiled active boundary

The same-code construction is in endpoint_route/same_code_controller_bridge.md.
Use Aharonov-Ben-Or's measurement-free scheme and a fixed sufficient CSS base.
The displayed conservative choice has parameters [[2047,1,>=63]]. The finite
gadget constants A and g are charged; no practical numerical threshold is
inferred. With a=binom(A,2), recursive bad-fault tags obey

    p_(r+1) <= a p_r^2,       sum_r p_r <= 2p  (ap<=1/2).

Adjacent-level interfaces are actual simulations of finite code circuits.
Their input-independent bad tags have probability <=g p_r, uniformly on the
allowed correctable input subspace. The final raw-to-code boundary has O(p)
logical noise and arbitrarily small protected-code leakage. Disjoint code-to-
raw descents produce local-stochastic classical error pools of strength O(p),
even with correlated incoming gauges.

For each quantum output prepare a fresh independent encoded Bell resource,
perform the logical Bell transform on the data and one resource half, fan out
the resulting logical Z bits into protected pools, and discard the consumed
systems. Do not apply old coherent controls to the surviving Bell half B.

The static-tree theorem couples each possibly correlated raw control pool to
a reference tree with exact leaves only in the proof. The real tree has noisy
leaves, wires and voters. For q_c,e,v<=s<=0.01,

    u_(ell+1) <= v+3(u_ell+e)^2,
    d_(ell+1) <= [3v+6(u_ell+e)] d_ell,
    d_L <= q_c (21s)^L.

Its reference error is a computable independent binary symmetric channel of
strength O(p). Mixed local-stochastic bounds prove the coupling uniformly over
old quantum references and classical records. Each depth-L tree uses 3^L
leaves, hence polynomial inverse-accuracy overhead. Native CNOT, CNOT, Toffoli
voters are complement covariant under every fixed Pauli bit-fault pattern.

B waits and descends independently. Its raw arrival and the two classical
roots occur at the same prescribed clock. Always-scheduled CNOT and controlled-Z
gates apply the terminal byproduct. The uniform Bell outcome naturally twirls
the independent B-side channel E_i:

    K_i = Q_terminal,i Q_tree,i (1/4) sum_b P_b^{-1} E_i P_b.

Thus the comparison output channel is a product of exact O(p)-weak Pauli
channels. All fine Bell/pool histories are discarded/reset at paid cost;
arbitrary pre-existing external records remain. Good events are never globally
conditioned on. Hybrid replacements retain the full independent fault laws.

The product-boundary statement is useful for any protected quantum circuit,
not solely for this memory. Unknown raw entry and final raw delivery retain
their separate O(p) floors.

## 3. Positive source and compensated writing

The complete proof and explicit sufficient thresholds are in
inverse_noise_theorem.md. For each product Pauli boundary channel K_i define
its action as a syndrome convolution. At fixed bounded incidence and positive
bounded temperature parameters, sufficiently small q makes every law

    mu_I = (product_(i in I) K_i^{-1}) pi

strictly positive. The inverse exists but is not a positive channel on arbitrary
states. Positivity is proved specifically for the thermal target family, using
a signed connected-noise polymer expansion. It is uniform in N and in the
global syndrome constraints.

The accepted history gas acquires weak soft interactions. A deletion bound
and the mixed local-influence estimate yield a rapidly mixing context-dependent
single-polymer heat bath. Connected-subset logarithm evaluation, truncation,
mixing, numerical precision and random bits all have explicit polynomial cost.
There is no exponentially costly global density-ratio rejection step.

Sample s~mu_all before the unknown logical input is needed. Through actual
protected circuits prepare the decoder-frame state V_s rho V_s^*. Export it
with the product boundary compiler. For any ordered endpoint-noise prefix J,

    K_J mu_all = mu_(complement J).

Every prefix has an instability probability bounded by

    b_(0,N) = B x_0^{L_*(N)}/(1-x_0),      0<x_0<1.

An elementary physical Pauli has identity logical action on a stable syndrome.
The chance of any nonidentity logical endpoint action is therefore at most
C N q b_(0,N). At the end, the syndrome marginal for each fixed offered source
is exactly pi in the comparison. The sampling and metrology errors add once by
channel contractivity. Holding starts in the specified law without physically
equilibrating the whole memory.

### Actual retained-seed extension

The retained preparation seed is distributed as mu_all, not as pi. It can be
correlated with the unknown logical input and its reference. The comparison
keeps this same seed, the same private endpoint fault labels, the same final
syndrome s'=s+delta(F), and the same external record law. It removes only a rare
nonidentity logical action. It does not replace the actual seed by an
independently labelled Gibbs sample. The syndrome marginal suffices for the
intrinsic-time coupling because bath jump rates are logical-state independent.

Source selection based on retained seed values is handled by the union over
all offered source paths and their caps. No equilibrium assertion conditional
on selection or a rare retained record is used.

## 4. Passive path and actual noisy reading

For a fixed offered source, compare the actual bath with a path that keeps the
same syndrome jumps but deletes its rare nonidentity logical jumps. The
accepted unstable-set estimate gives

    Pr[logical bath discrepancy before intrinsic time T_j]
       <= C Gamma N T_j b_(0,N).

This is a statement about the whole path and permits a logical read time to be
chosen from retained records. It is not an equilibrium-preparation assumption.

Reading begins with simultaneous local capture into actual protected encoder
interfaces. Private protected Pauli seeds and the same tree regenerators twirl
each input boundary to an independent product Pauli channel J_i. Their
preparation occurs while the memory continues its counted passive hold. If
quantum controllers were unavailable during a blackout, this preparation
starts after their return; its delay is included in T_j. No raw memory output
waits unprotected for a growing classical computation. The protected decoder
then computes the actual decoder-frame recovery from all captured qubits.

For a deterministic read time, prefixes J_I pi have the forward version of the
same cluster bounds and hence instability <=b_(0,N). But a stopping-time
syndrome can be biased. The next lemma supplies the required replacement.

### Anytime-read lemma

Presample the private independent Pauli labels F_i of a fixed read template.
For this F define A_F as the union of syndrome sets for which a nonidentity
read-noise prefix would encounter an unstable input. The forward-prefix bound
and a union over at most N rare nonidentity labels give

    E_F pi(A_F) <= C N q b_(0,N).

For every set A, a stationary continuous-time syndrome chain of maximum total
jump rate C Gamma N satisfies

    Pr_pi[exists t in [0,T_j] : S_t in A]
       <= (1+C Gamma N T_j) pi(A).

Proof: charge initial membership pi(A), then count entries into A. Stationarity
equates incoming and outgoing flux; the latter is at most C Gamma N pi(A).
Integrate over the interval. No independence between the stopping rule and
the existing records is needed for this whole-interval event bound.

Average this inequality over F, which is independent of the offered source's
bath path. Then every allowed stopping-time read has logical discrepancy

    <= C N q (1+Gamma N T_j) b_(0,N).

Fine read-twirl seeds and interface transcripts are discarded as specified by
the product-noise compiler. External input references and pre-existing records
are retained in the comparison. The theorem is unconditional joint process
distance; conditioning on a rare record has its ordinary inverse-acceptance
probability cost.

## 5. Campaign, useful access and slack

After reading, perform any specified protected logical circuit, measurements
and classical feedforward. Final raw delivery is an actual descent to the local
port. For reuse, keep the logical state protected, prepare a fresh compensated
source and reload. The decoded old background is consumed. This new noisy
reuse operation is distinct from the previously accepted syndrome-preserving
access theorem, which remains valid at its own scope.

Sum all uniform circuit/source/metrology hybrid errors, all offered write
events, the passive-path events and the anytime-read events. With deterministic
per-source caps summing to T this gives the transparent bound

    d_process <= C n_raw p + epsilon_total
                 + C [R N q + Gamma N T(1+Nq)] b_(0,N).

To obtain the theorem's simpler displayed form, choose any fixed x_1 with
x_0<x_1<1 and set b_N=B x_1^{L_*(N)}/(1-x_1). Writing
a_*=c_* log(x_1/x_0)>0,

    sup_(N>=1) N exp(-a_* N^eta)
       <= max{1, [1/(e a_* eta)]^{1/eta}}.

Consequently (1+Nq)b_(0,N)<=C b_N with an explicit finite constant. This
constant can be enormous when eta is small; the notation does not make it a
practical estimate. Under only a total pathwise exposure bound, replace the
allocated T by the conservative J T_actual unless a stronger allocation proof
is supplied. Candidate rejection/reset opportunities are charged as above.

## 6. Acquisition, deployment and unavoidable raw error

The homogeneous Lambda model is identified with noisy experiments. Use
opposite-sign preparations and let m_t be half their difference in recorded
polarization after t idle locations. A fixed affine capture offset cancels:

    m_t=A lambda_axis^t,        lambda_axis=m_1/m_0.

Three axes determine Lambda. All templates, including capture, depend only on
this same Lambda. Effective endpoint channels can be sampled with a protected
quantum simulation of the explicit resource/decoder/descent template: retain
the unconditional decoded syndrome marginal and reinsert the known Bell pair
inside the simulated target. No ideal physical step is inserted into the
unknown-input operation. Recursive decoder circuit cost is polynomial in the
explicit template size, with fixed base-code tables charged.

For lambda_a=beta J_a, selectively isolate the actual bounded-support check
coupler, expose it to the stipulated bath with known lower relaxation gap,
and measure its syndrome through the noisy capture template. Its mean is
c_a+a_a(1-2r_a), with r_a=(1+exp(lambda_a))^{-1}. Compute c_a,a_a from the same
calibrated Lambda; subtract and debias. The sufficient per-check sample count
is O(exp(2lambda_max) eta_lambda^{-2} log(m/delta)). Taking eta_lambda=O(epsilon/m)
retains a polynomial but potentially huge total bill. Physical component error
stays fixed while statistical and numerical precision improve.

Metrology compares actual and estimated forward channels on the valid state
prepared for the estimated channel. It does not multiply parameter error by
an extensive inverse-channel norm. Calibration failure and source-law error
remain explicit. Selective coupler isolation is real extra fabrication/access,
not supplied by global switching. Stable independence, commuting fabrication,
and the bath law remain model assumptions; finite trials cannot certify them
against arbitrary future drift.

The exact depolarizing raw-cut boundary is

    inf_R (1/2)||D_b R D_a-id||_diamond = (3/4)(a+b-ab),
    D_a(rho)=(1-a)rho+a I Tr(rho)/2.

Its proof and attaining identity channel are in endpoint_and_refresh.md. This
explains the O(p) raw port term for unknown reference-entangled inputs and
outputs. Internal encoded work reaches arbitrary epsilon. Release and
reacquisition through new raw cuts count anew.

## 7. Common-bath separation from every noninteracting hold

Fix independent isotropic local XYZ couplings and the unobserved Davies law

    g_beta(omega)=2 nu/(1+exp(-beta omega)),
    [H,P_omega]=-omega P_omega.

It obeys detailed balance and g_beta<=2nu, so the accepted interacting-memory
holding theorem applies within this same specified bath class. No jump record
or purifying environment is supplied to the controller. All information-
carrying quantum helpers undergo the declared holding channel; classical
pre-hold records and fresh decoding ancillas are allowed.

For any noninteracting static Hamiltonian H=sum_i H_i, diagonalize each H_i.
Isotropy preserves the XYZ bath under this rotation. If its gap is Delta, the
two transverse couplings give downward/upward rates 2g_beta(Delta) and
2g_beta(-Delta), whose sum is 4nu. They damp coherence at 2nu. The longitudinal
zero-frequency coupling adds coherence damping 2nu. Thus, up to a known local
Hamiltonian unitary, the exact one-site channel is

    E_(i,t)(rho)=lambda rho+(1-lambda) tau_i Tr(rho),
    lambda=exp(-4nu t),

where tau_i is that site's Gibbs state. For lambda<=1/2 it has the symmetric
two-output extension

    B_i(rho)=lambda rho_A tensor tau_(i,B)
             +lambda tau_(i,A) tensor rho_B
             +(1-2lambda) tau_(i,A) tensor tau_(i,B) Tr(rho).

Each term is completely positive, and the weights sum to one. Both marginals
are E_(i,t). Tensor these extensions, precompose any encoder, copy its retained
classical record into both branches, and apply the allowed decoder separately
to each branch. The resulting reference/output state is symmetrically
extendible to two proposed outputs. This holds even if encoding and decoding
are ideal and arbitrarily expensive.

For a qubit reference R and candidate outputs A,B, the sum of Bell projectors
Phi_RA tensor I_B + Phi_RB tensor I_A has operator norm 3/2. Equal marginals
therefore have Bell fidelity <=3/4. Bell-projector measurement then gives

    (1/2)||decoded channel-id||_diamond >=1/4
    whenever t>=log(2)/(4nu).

This bound is independent of N, all one-site energy gaps and beta. It is a
sufficient constant-time obstruction, not a claim of an optimized threshold
over every product channel. At H=0, the local channel is depolarizing and is
entanglement breaking for t>=log(3)/(4nu); the corresponding error lower bound
is 1/2. An explicit three-axis measure/prepare representation proves that
stronger H=0 statement.

The interacting register, with sufficiently small fixed p and large N, can
retain an unknown entangled qubit to error below 1/4 across a much longer
interval with no active quantum correction. Static interactions and the bath
remain present, and classical record maintenance may still cost energy. This
is not a universal power-outage memory. A monitored bath, a protected quantum
side memory, interacting autonomous correction or a different spectral law
changes the hypotheses. A competitor given the same passive hardware may use
the same operation.

## 8. Resource and broader consequences

Ordinary active correction receives the same controls, precision, ports,
cooling, metrology, reset, switching and routing. Fixed-noise active storage
already exists; the contribution is compatibility with the specified thermal
hold and the independent boundary compiler. Modern qLDPC interfaces and
autonomous correction are included as strong, scoped comparators in the
report. No general quantum-memory lower bound is inferred from another bath
or access model.

Charge all of

    E_fabrication + E_acquisition + E_commissioning + E_access + E_reset
      + integral(P_static + P_cooling + P_records + P_active) dt,

as well as total quantum and classical occupied spacetime, critical-path
active duration, nonlocal link costs and every fresh source/pool. The static
trees add polynomial inverse-accuracy overhead; ordinary FT polylogarithmic
overhead applies to this enlarged workload. Nonlocal active links are an
explicit paid architecture assumption, not a proved finite-speed 3D layout.

For fixed chosen designs, E_P=A_P+T P_P and E_A=A_A+T P_A. A favorable crossover
requires the corresponding price inequality; when P_A>P_P it is
T>(A_P-A_A)/(P_A-P_P), with the usual sign cases. No actual prices or universal
thermodynamic gate cost are supplied by a gate-count theorem. The published
BDL constants and sufficient witness exponent are severe and remain in this
comparison. A sufficient size certificate is not a lower bound on the best
possible performance of the physical family.

For the full Gibbs state, take the logical subsystem maximally mixed. Logical
Paulis are then immaterial, so exact compensation gives the full target Gibbs
state, with only the implementation/metrology/source epsilon in the actual
operation. No unknown raw-input floor is required for that known mixed-state
task. The same proof does not upgrade a pure coherent TFD at a fixed noisy raw
output port.

The inverse-noise note also proves, for the same logical density matrix in
every syndrome sector,

    D(mu||pi) <=128 w d N q^2 exp(w lambda_max),
    Delta F=beta^{-1} D(mu||pi).

This state-function bound is not the work consumed by the sampler or a
reversible-work protocol. The exact one-bit inverse
mu(1)=(r-p)/(1-2p), r=(1+exp(lambda))^{-1}, is positive iff p<=r. Thus the
fixed-noise neighborhood cannot persist uniformly to zero temperature.

## 9. Preservation and verification

The predecessor archive is included byte for byte. Its once-paid source,
intrinsic-time process coupling, paid syndrome-preserving access, coherent TFD,
central-sector construction and earlier independent physical classes remain
at their accepted scopes. Named actual-check sampler obstructions are not
promoted to general sampling hardness.

Five executable suites check finite inverse laws/prefixes, the soft sampler,
the noisy-tree coupling identities, reference-entangled Bell refresh, raw-cut
algebra and the common-bath broadcasting identities. They do not certify a
device, an asymptotic lifetime by simulation, a practical threshold, or the
declared physical noise model. The mathematical proofs carry those conditional
infinite-family conclusions at the explicit model scope above.
