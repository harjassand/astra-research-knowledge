# Independent first-principles route: what survives the kill-test

Date: 5 November 2026. No other researchers' new tournament proposals were read.
The parent supplied a geometric cut challenge after the independent permutation
construction; that challenge is attributed explicitly below.

## Selection assessment

The initially derived target is **rejected as a new foundational opening**.
Private permutation converts an oblivious bounded-size error support into a
local-stochastic logical support law, but this is established private coding and
interleaving. More seriously, it does not make the required computation physically
possible in a local medium whose damaged sites disconnect communication.

The strongest remaining question on this route is:

> What is the attainable joint space, physical-time, initialization and fault-budget
> law for reference-preserving fault-tolerant quantum computation when BOTH quantum
> operations and classical decoding/control are geometrically local, noisy and
> propagation-limited?

A completed answer would turn an abstract correlated-noise fault-tolerance theorem
into an actual computing operation, or sharply delimit which noise and geometry
contracts permit that operation. This consequence is stronger than proving a new
correlation-tolerance statement alone, which current primary work already provides.
However, the concrete progress here consists of exact obstructions and a diagnostic
for a missing compiler operation, not an attained new fault-tolerant architecture.
I therefore do not recommend this as the winning selection if another independent
route has a comparable consequence and an actual constructive central opening.

## Opening derived before literature search

The full derivation is preserved in derivation_before_search.md. For an arbitrary
bad-site set F of size m fixed before a uniform private permutation Pi, every
prescribed k-role set S obeys

  P(Pi(S) subset F) = (m)_k/(N)_k <= (m/N)^k.

For an n-role code block correcting alpha n faults, alpha>epsilon=m/N, the block
failure bound is exp[-n D(alpha||epsilon)]. This has a real information-order
requirement. A fault field reacting to Pi can target a chosen logical block.
An expected fault-density bound alone is insufficient: a complete-system fault
with probability epsilon has the same mean density and defeats the k-th power law.

This mechanism trades an independence premise for private assignment and a
nonreactivity premise. It does not make either premise experimentally automatic.
The exact bound is spatial within one round. Reusing a fixed permutation does
not make repeated faults independent over time; repeated-round claims need the
fresh conditional private-assignment contract stated in the original derivation.

## Geometry obstruction (parent challenge, independently checked)

Consider a synchronous nearest-neighbor circuit on an L^d grid. A wall of sites
of thickness comparable to the interaction range and cardinality O(L^(d-1))
separates left from right. Reset all wall sites after every gate layer. Because
no site participates in more than one gate per layer, information cannot traverse
the wall before it is erased. In a periodic domain use two walls. The corrupted
fraction is O(1/L), tending to zero.

Fresh input introduced on one side cannot influence a required output on the
other. A private permutation of role labels does not repair this severed channel.
Pre-shared entanglement cannot transmit a fresh message without communication.
Placing the input on both sides beforehand would change the preparation contract.
Allowing long-range couplers or an unaffected external communication path changes
the physical resource contract. The wall argument concerns permanent adversarial
resets, not dilute stochastic bursts that may leave alternative paths in time.

Thus a global small fault fraction is not a sufficient physical noise contract
for fixed-dimensional local computation. Fault geometry or protected/nonlocal
connectivity has to enter the theorem.

## Finite-speed opening: a usable quantum channel needs the control record

Let a fresh unknown qubit A, possibly maximally entangled with an inaccessible
reference R, arrive at one endpoint. Require its state to be transferred to a
physical output B at distance L. The initial hardware state may contain any
input-independent pre-shared entanglement. Every quantum and classical signal
has propagation speed at most v.

For t<L/v there is no causal A-to-B channel. The induced map from A to B is a
replacement map rho -> sigma_B Tr rho. For such a map,

  (1/2) || id_2 - replacement_sigma ||_diamond >= 3/4.

Proof: twirl sigma over single-qubit unitaries. Convexity and unitary invariance
show the maximally mixed replacement minimizes distance. Applying identity and
complete depolarization to one half of a Bell pair gives Phi_RB and I_RB/4.
Their difference has eigenvalues 3/4,-1/4,-1/4,-1/4, so trace distance is 3/4.
The completely depolarizing channel attains that half-diamond value.

An instantaneous mathematical Pauli-frame update does not yield the required
physical channel until the necessary classical information has arrived. This is
ordinary no-signalling with the operational output interface made explicit, not
a claim of newly discovered causality.

For a uniform reassignment of N=L^d existing data roles, expected total Manhattan
transport distance is exactly

  N d (L^2-1)/(3L).

A bisection must transport Theta(N) roles over O(L^(d-1)) bounded-capacity edges
with high probability. Hence latency is Omega(L), even though the abstract
permutation can be specified compactly. Any proposed fast architecture must pay
transport or nonlocal hardware, rather than a relabeling in its analysis.

## Waiting is part of the noise process

A compiler cannot simply insert a long passive wait and keep a per-step fault
threshold unchanged. If a stabilizer-encoded block has distance d_code and no intermediate
syndrome extraction during a wait of tau physical steps, an adversary allowed f
site corruptions per step can enact a weight-d_code logical operator whenever
f*tau >= d_code. Split that operator across disjoint batches at successive steps;
its final action is a logical error invisible to the final syndrome.

This is not a no-go for active protection while decoding. Ongoing syndrome
extraction and a valid delayed-frame protocol can change the conclusion. That
active, causally local, fault-tolerant control operation is precisely what must
be supplied. An asserted error map per abstract layer is insufficient on its own.

## Strongest primary comparators checked

1. Adam Smith, *Scrambling Adversarial Errors Using Few Random Bits, Optimal
   Information Reconciliation, and Better Private Codes*, SODA 2007, 395-404;
   IACR ePrint 2006/020. The primary abstract explicitly uses t-wise independent
   random permutations to handle adversarial errors with efficient private coding.
   This defeats a novelty claim for the permutation core derived above.
   https://eprint.iacr.org/2006/020
   https://pure.psu.edu/en/publications/scrambling-adversarial-errors-using-few-random-bits-optimal-infor/

2. Shin Ho Choe and Robert Koenig, *How to Fault-Tolerantly Realize Any Quantum
   Circuit with Local Operations*, PRX Quantum 6, 010357 (24 March 2025).
   Their local quantum compiler has constant quantum-depth overhead and polynomial
   hardware overhead under local stochastic noise. The 3D architecture uses
   O(n^(3/2) log^3 n) qubits; the quasi-2D one O(n^2 log^3 n). The paper explicitly
   excludes extra classical processing from quantum depth, assumes error-free
   classical processing, and leaves fault tolerance including the resulting waits
   as future work (PDF p. 3, and definition on pp. 9-10). This is an explicit author-
   stated limitation, not an inferred defect in the published theorem.
   https://journals.aps.org/prxquantum/pdf/10.1103/PRXQuantum.6.010357

3. Nikolas P. Breuckmann, Louis Golowich and Umesh Vazirani, *Fault-Tolerant Quantum
   Computation with Adversarial Errors*, arXiv:2608.16857v2, 30 September 2026.
   Theorem 1.1 gives physical qudit count at most logical_N^(5+eta), subpolynomial
   time overhead, and tolerance of N/2^(O(sqrt(log N))) arbitrary physical-qudit
   corruptions per time step. Errors can be coherent, global and non-Markovian.
   The theorem explicitly assumes free noiseless classical computation and encoded
   input. It is therefore a strong comparator to any broad claim that correlation
   tolerance is the missing discovery; it is not by itself a complete finite-speed
   local physical controller. The authors also identify the classical-decoding
   assumption as a concern for their proposed quantum-PCP connection.
   https://arxiv.org/html/2608.16857v2

## Why the two fault-tolerance papers are not automatically composable here

The quantum-local compiler is proved to preserve a local-stochastic error law.
The newer theorem permits adversarial supports subject to a per-layer cardinality
bound. A physical time dilation and a stochastic-to-adversarial substitution need
new proofs. Both works' classical side processing must be realized under the
physical noise and communication budget. An abstract efficient decoder or a
claimed bounded error spread does not establish those conditions.

The input and output handoffs also need explicit error allowances. An adversary
permitted to erase a single unencoded unknown input before it is encoded can
irreversibly destroy it. Arbitrary fidelity does not follow merely from protecting
the later circuit. A trusted or quantitatively bounded source/handoff interface,
or an already encoded input, is a substantive premise.

## Central operation that remains

Construct a composable local gadget with finite-rate classical syndrome transport,
active quantum protection during all decoder latency, and a proved transformation
of the allowed physical fault field into the base code's admissible errors.
Charge the gadget's own registers, reset channels, communication, decoding energy,
and source/output interfaces. Establish a matching geometry/fault-budget lower
bound under the same interface. This is a genuine question, but the present
route has not yet constructed that gadget and does not claim that the new
architecture exists with a specified strong asymptotic resource law.

## Decision for the selection round

Preserve the exact permutation calculation, the geometry and causal obstructions,
and the primary-source scope findings. Do not present them as the requested new
foundational discovery. They provide a useful rejection test for overbroad
correlation-based proposals and a concrete harder operation, but a winning
selection needs further constructive work or a stronger competing route.
