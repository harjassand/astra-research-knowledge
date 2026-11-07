# Independent hostile audit: local physical refresh rather than lifetime simulation

7 November 2026, Brisbane. Independent initial report, frozen before peer exchange.
Author role: hostile mathematical auditor. No peers' new constructions were read.

## Governing capital and exact scope

I read `AGENTS.md`, `outputs/RESEARCH_TO_PUBLICATION_WORKFLOW.md`, the established
`outputs/PROTECTED_QUANTUM_PROCESSING_RESEARCH_DOSSIER.md` (SHA-256
`b94faadf5e396a54566414b0889bb45286080a47512701f032795c8e10fb8c00`), and
`work/protected-quantum-processing-20261107/principal/THERMAL_SERVICE_THEOREM.md`
(SHA-256 `bb4e12ae7cc82ed68f94d4b162f6c9a85e08671fd88b805a510ee47058666b40`).
The cwd is not itself a Git repository. The earlier dossier records its own
underlying source-repository revision; that fact is not a current-checkout claim.

The audited capital supplies a stabilizer DATA family of distance at least
delta*n, bounded-body/incidence integer syndrome energy U, bounded-support local
updates, and at least kappa*U strictly decreasing labels at low linear energy.
For the two-sector energy specialization every low-energy syndrome has a
canonical Pauli repair of weight at most C0*U. The full canonical module, including
off-diagonal syndrome operators and arbitrary retained bath/reference coefficients,
is logically neutral for every local leg retained below a strict cutoff u_c*n.
Selected code-preserving gates and the restricted encoded-port construction remain
capital at their stated assumptions. Neither their engineered GKSL primitive nor
their isolated stochastic staging is silently promoted into microscopic hardware.

## Strongest positive result in this independent investigation

**PROVED abstract compiler, conditional physical use.** A constant-accuracy,
reference-safe refresh of a *constant-size* local system into a full-rank thermal
state can be converted into an exact positive sparse-fault model. Together with
finite-temperature local exchange collisions, this supports a direct discrete
cooling theorem with exponential logical protection under a genuine sparse joint
fault law. Its precision requirements are fixed constants, independent of service
duration and code size. No exponentially accurate global simulation is required.

The decisive missing physical operation is narrower than “simulate Davies for all
times”: provide repeated local refreshes and local control modules with a **joint
no-return/CP-minorization contract**, or prove an equally strong local replacement.
Correct reset marginals, fixed-point fidelity, and a whole-memory reduced-state
approximation do not provide that contract. I give counterexamples below.

## 1. Counterexample: exact thermal marginals can give a logical error floor

Let L=P1*...*Pw be a nontrivial logical Pauli supported on w physical qubits of a
stabilizer code. Give its control ancillas the correlated state

    omega_A=(1-p)|0^w><0^w|+p|1^w><1^w|.

Every ancilla has exactly the same finite-temperature qubit Gibbs marginal
diag(1-p,p), for beta*Delta=log((1-p)/p). Apply the local controlled-Pj from ancilla
j to DATA j, then discard the ancillas. The resulting encoded channel is

    E=(1-p)id+p Ad_L.

For a logical Bell input and an anticommuting logical test its half-diamond error
from identity is p. Both branches have exactly zero syndrome energy. All control
operations are local and every ancilla marginal is the promised Gibbs state.
The all-subset fault probability is p, rather than p^w. A GHZ purification gives
the same obstruction with a retained quantum environment.

**Consequences.** Independent reset fidelity cannot be inferred from one-ancilla
tomography. Even exact thermal marginals plus zero DATA energy do not certify a
writer's logical content or protect a long computation. Reusing a common reset
bath without a joint bound can realize this failure. This does not invalidate a
primitive whose fresh-output/no-return or sparse joint law is explicitly assumed.

## 2. Counterexample: fixed points and local tests do not establish storage

The preceding logical-Pauli channel fixes the exact Gibbs state of every
syndrome-only Hamiltonian, since that Gibbs state is maximally mixed on logical
degrees of freedom. It can nevertheless corrupt a logical Bell state in one step.
On a distance-d code, all observables supported on fewer than d qubits have the
same expectation on every logical code state. Consequently agreement on all
bounded local physical observables, or even an exact Gibbs fixed point, cannot
replace reference-uniform logical-channel control. A fixed-point preparation
theorem must not be called a logical-storage theorem.

A first-moment promise is also insufficient. The mixture of a low-energy state
and an energy v*n state with weights 1-epsilon and epsilon has mean energy
epsilon*v*n and a constant probability epsilon outside every cutoff below v*n.
It need not have an exponentially small energy tail. A hard support promise or an
exponential-moment gap, with its constants, is genuinely stronger. The first
moment alone gives at most Markov's constant tail bound.

## 3. Counterexample: state norm cannot silently become a scalable channel norm

For dimension D define the two Werner-Holevo channels

    Phi_+(X)=(Tr(X)I+X^T)/(D+1),
    Phi_-(X)=(Tr(X)I-X^T)/(D-1).

For every state rho, their trace-norm output difference is at most 4/(D+1)
(equality on pure states). On a maximally entangled reference input, their outputs
are normalized projectors onto the symmetric and antisymmetric subspaces, and
are perfectly distinguishable. Their diamond distance is therefore 2.
Finite-dimensional norm equivalence has a dimension-dependent cost. This is why
a reference extension is harmless for a fixed-size reset qubit, while treating an
n-qubit memory as one finite system can hide an exponential factor.

## 4. Local refresh minorization lemma

Let R be a CPTP channel on a d-dimensional local module and let

    R_tau(X)=tau Tr(X),  lambda_min(tau)=t_min>0.

If ||R-R_tau||_diamond<=epsilon and p=d*epsilon/t_min<1, then

    R=(1-p)R_tau+p R_bad

for an exactly CPTP R_bad. This is a positive channel decomposition, valid on all
inputs entangled with arbitrary references; it is not a conditional-state or
average-fidelity statement.

**Proof.** Use normalized Choi matrices. J(R_tau)=I/d tensor tau, whose minimum
eigenvalue is t_min/d, and ||J(R)-J(R_tau)||_infinity<=epsilon. Thus
J(R)>=J(R_tau)-epsilon*I>=(1-p)J(R_tau). The difference is CP and has trace-scaling
p, giving the asserted normalized CPTP residual. The bound is conservative. QED.

Applying local channels with this decomposition gives independent Bernoulli
bookkeeping flags even if the actual channels vary deterministically in time:
the branch probabilities are p independently of the input, because every residual
is TP. Independent fresh local environments make the channels genuinely local.
A common returned bath needs the analogous inequality on the *full joint map*;
the lemma on the reduced local map alone does not supply it.

### A legitimate, limited use of Merkli's uniform-in-time theorem

Primary source: Marco Merkli, *Dynamics of Open Quantum Systems II, Markovian
Approximation*, arXiv:2105.00023v2, Theorem 1.1, equations (1.26)-(1.30), and its
spin-Boson specialization Proposition 1.3. It **does** prove an O(|lambda|^(1/4))
uniform-in-time reduced-dynamics approximation for fixed finite dimension, subject
to its form-factor, effective-coupling and resonance assumptions. Its initial
reservoir state is thermal and product with the system (equation (1.14)). Its
constants and admissible coupling are model dependent; Proposition 1.2 explicitly
displays temperature and resonance-data dependence. No size/control uniformity is
imported for the whole code family.

For an isolated reset qubit with fixed nonzero gap Delta and G=sigma_x, choose an
admissible smooth form factor nonzero at Delta. The two-level Davies semigroup is
primitive and has Gibbs state tau. The local dimension is two, so converting the
source's superoperator estimate to diamond norm costs a fixed factor. Its reset
channel obeys, for suitable fixed constants,

    ||R_t-R_tau||_diamond
       <=C_local |lambda|^(1/4)+C_mix exp(-g_local lambda^2 t).

For any fixed target p_reset>0 choose a sufficiently small **fixed** lambda and a
sufficiently long **fixed** reset duration so that the right side is below
p_reset*lambda_min(tau)/2. The lemma then supplies a positive reset-fault
decomposition at rate p_reset. Both choices may be astronomically impractical,
but neither depends on n or the exponentially long service duration.

**Mandatory applicability boundary.** This application needs a fresh independent
thermal reservoir segment for each reset, isolated from DATA and all old returned
bath modes. Repeating a theorem about a product initial reservoir does not prove
that a reused finite bath is refreshed. One-use thermal qubit tapes with SWAP
resets give a simpler exact microscopic alternative, but consume charged fresh
thermal tokens. An infinite continuum reservoir per refresh is an idealized
physical resource, not a finite-resource laboratory implementation.

## 5. Explicit finite-temperature local exchange module

For a catalog Pauli P and positive energy change d, set A=P Pi_d, so
[JU,A]=Jd A, A^dagger=P Pi_-d. Take one ancilla with gap Jd, thermal excited
probability q_d=(1+exp(beta Jd))^(-1), and interaction

    V=A tensor |0><1|+A^dagger tensor |1><0|.

It has bounded full support (including the check-read neighborhood) and commutes
with H_DATA+H_anc. At interaction angle pi/2 the |0> ancilla branch performs the
deterministic local lowering channel

    C_down(rho)=(I-Pi_-d)rho(I-Pi_-d)
                   +A^dagger rho A,

up to irrelevant Kraus phases; the |1> branch is a local CPTP raising channel.
Consequently the actual finite-temperature channel is

    C_beta=(1-q_d)C_down+q_d C_up.

This equality is on the full quantum module, not just diagonal states. The energy
exchange is exactly balanced by the ancilla, with finite gap and finite collision
duration. Reference entanglement is retained. The full Hamiltonian can remain on:
its free evolution commutes with the interaction and only changes syndrome phase.
The outgoing thermal mode must not return uncharged.

A finite-temperature reset fault at rate p_reset combines with q_d as a local
fault rate at most q_d+p_reset. Since d>=1, q_d<=exp(-beta J). This is a fixed
nonzero-temperature construction; it does not pretend that resetting to a pure
ground state is exact in finite time.

## 6. Constant coherent calibration errors: a constructive robustification

Diamond closeness to an ideal unitary **alone** does not imply a positive mixture
with that unitary: its Choi matrix has rank one. The same issue can affect an
ideal lowering channel. Do not make this inference for imperfect gates.

There is a direct finite-dimensional repair when each local module has a fresh
environment. Deliberately smooth its ideal channel C_down with a small complete
depolarization probability r>0 on its full q-qubit patch Q:

    C_ref=(1-r)C_down+r D_Q,   dim(Q)=D_Q.

If the actual module is delta-close in diamond norm to C_ref, then its normalized
Choi matrix has the same minorization argument with minimum reference eigenvalue
at least r/D_Q^2. Thus it contains C_ref with coefficient at least
1-D_Q^2 delta/r. It contains C_down as an exact CP branch with weight at least

    (1-r)(1-D_Q^2 delta/r).

All remaining branches are local CPTP faults. Their total rate is at most
r+D_Q^2 delta/r. Fix r and delta small constants below the eventual fault margin.
No exponentially accurate calibration is needed. A fixed fractional overrotation
does not shrink with pulse duration; its actual integrated channel error must
satisfy this constant bound. This argument needs **local channels**, not merely a
reduced map with an uncontrolled shared returning bath. Intentional smoothing is
ordinary channel-cone reasoning, not a new physical phenomenon or a priority claim.

## 7. Direct noisy-sweep theorem, avoiding lifetime simulation entirely

Assume a stabilizer family with the capital's distance, low-energy global repair
and density of lowering moves. Make one sweep through all L<=c*n local
energy-resolved labels in a fixed order, applying the ground lowering channel at
each good location. Every local fault acts on at most q_f DATA qubits and any
retained bath B. There is a positive fault instrument satisfying, uniformly on the
full module and references,

    sum_(F contains A) W_F^*(I)<=p^|A| I

for every subset A of locations in the sweep. The complete joint dynamics are
CPTP. This can be earned from the local fresh-environment decomposition above;
it is also a valid broader assumption for correlated faults. Marginal rates do
not suffice.

Let D_f bound the energy increase of one fault; let R be a fixed upper bound on
the number of local decreasing-label predicates whose truth can be changed by
one successful lowering move or one fault. Full read supports and all gate cones
are included. Such R exists by bounded support/incidence. Enlarge it by one.
Choose a=min(1/2,kappa/(2R)) and b=D_f+1. For every input energy eigen-syndrome and
every scalar syndrome path in a branch with f faults,

    U_end<=(1-a) U_start+b*f,
    max_(within sweep) U<=U_start+D_f*f.                  (S)

**Proof.** Mark the >=kappa*U_start active labels at sweep start. Each marked label
either executes a successful decrease when visited, is itself faulty, or has had
its predicate changed by an earlier successful decrease/fault. At most R marked
labels can be charged to any such operation. If S is the number of successful
decreases, kappa*U_start<=R(S+f). Every success lowers integer energy at least one,
whereas every fault raises it at most D_f. This proves the stronger coefficient
1-kappa/R when nonnegative, and hence (S) with the conservative a above. Ideal
ground-channel Kraus legs map one syndrome to one syndrome. A faulty local leg
expands into DATA Paulis with arbitrary bath coefficients, each changing only its
bounded neighborhood. The same path bound therefore proves an **operator support
inclusion** for arbitrary coherent inputs; it is not an assertion of a classical
fault history for a coherent superposition. QED.

Choose constants u_s,f_*>0 with

    b*f_*<a*u_s,
    u_s+D_f*f_*<u_c,
    2*C0*u_c<delta

and strict margins. Good branches with f<=f_*n return support U<=u_s*n and never
leave the full canonical safe module. On every such local leg the operation is
identity on logical information. The complete good sweep is therefore
id_L tensor K_GB for a CP/TNI map on the actual gauge/bath module. No gauge/bath
independence or normalization is used. A warmer admitted input below u_c*n cools
to u_s*n after a fixed number of sweeps if f_* is reduced and the same
intermediate-energy margins are reserved.

The bad mass is bounded by

    delta_sweep<=binom(ceil(c*n),ceil(f_*n)) p^ceil(f_*n)
       <=exp[-f_*n log(f_*/(e*c*p))+O(1)].

This is exponentially small when p<f_*/(e*c). The TNI lost-mass argument from the
capital yields reference-safe logical error O(K*delta_sweep) for K sweeps.
Code-preserving bounded-depth gates can be inserted with their full endpoint
spread/fault margins and a fixed restoring number of sweeps. Gate programs and
clocks must obey the same genuine local fault contract. An unprotected global
enable bit causing n wrong gates with constant probability is excluded by an
explicit counterexample, not silently accepted as local noise.

**Status.** The sweep combinatorics, module support and sparse-fault theorem are
proved at the stated assumptions. Integrating every retained coherent bath
Hamiltonian from the earlier GKSL model into the new positive discrete fault law
is **not proved here**. Neither an arbitrary diamond-small reduced reset error nor
the word “thermal” supplies such an integration. This is a powered local
measurement-free correction mechanism, with an explicit physical collision model,
not a new passive material and not a complete quantum-computer demonstration.

## 8. Predecessors, physical costs and exact remaining work

Hong--Guo--Lucas, arXiv:2403.10599v3, Section 4 and Appendix E.2-E.3, already provides
finite-depth measurement-free Gibbs sampling with ancilla resets, and analyzes
incoherent Pauli/control/reset faults by modified local rates. Their equations
(85)-(89) specify pure resets and a controlled local sampler; (90)-(99) concern
Pauli errors and rate repair. Thus local measurement-free cooling is established
capital in the literature. The present direct density/sweep argument avoids
requiring exact detailed balance under perturbations, but no historical novelty
claim has been established.

Ong--Parameswaran--Placke--Hahn, arXiv:2605.03011v2, linked by the arXiv primary
record to DOI 10.1103/25wc-17zy, has a physical resettable-ancilla protocol and
Theorem 1's fixed-point error bound (equation (41)). Its bound contains the
rescaled mixing time and structural parameters. Section III initializes and
resets ancillas to a product pure state each cycle. It must not be represented as
having proved finite-temperature imperfect resets or logical storage. The source
itself distinguishes heuristic mixing-time behavior from a general theorem.

Costs that must remain in any final claim:

* One-use thermal tokens: O(n*K) total local tokens/interactions for K sweeps;
  O(n) active local hardware can suffice with replenishment, but total bath
  throughput and preparation are charged. A finite precharged tape has
  O(n*K) physical cells, which is exponential when K is exponential in n.
* Recycled thermalizers need an actual no-return/renewal theorem. A closed finite
  bath has recurrence and finite entropy capacity; it cannot be treated as an
  infinite perfect reset source for free.
* Bounded-incidence patches can be colored into a fixed number of disjoint layers.
  Parallel constant-duration sweeps require truly compatible local channels and
  the charged local clocks/switches. Sequential common-bath modules cost O(n)
  duration per sweep. Either option is explicit; bounded degree is not a
  three-dimensional bounded-density layout theorem.
* Reset duration, bath coupling, finite gaps, peak exchange/control strengths,
  deliberate smoothing, calibration bounds and local classical schedule hardware
  have possibly huge fixed constants. Finite gate duration is paid; shortening a
  pulse does not remove fractional calibration errors.
* Protected encoded WRITE/READ needs the earlier compatible isolated staging
  theorem or a newly proved common-bath gateway. Bare unknown inputs and outputs
  retain their fixed-noise endpoint floors.
* Every active/autonomous comparator receives these same reset tokens, controls,
  routing, calibration, clocks and protected ports. The construction has no
  demonstrated total-space, total-work, net-heat or practical advantage.

The strongest next attack is the full joint local-refresh contract with a
recyclable physical bath, or a direct coherent-noise cooling-cycle drift proof.
These are sharper missing operations than global exponential-accuracy Markov
simulation, and the positive compiler shows why such simulation is not necessary.

## Source pins and preservation

Primary sources were read online and cached only under
`../auditor/sources/`: Merkli 2105.00023v2, Ong 2605.03011v2 and HGL 2403.10599v3.
Source URLs are respectively `https://arxiv.org/html/2105.00023v2`,
`https://arxiv.org/html/2605.03011v2`, and
`https://arxiv.org/html/2403.10599v3`. No published files, website checkout, or
external user artifact was changed. This initial report is to remain immutable
after its hash is communicated; corrections belong in follow-up notes.
