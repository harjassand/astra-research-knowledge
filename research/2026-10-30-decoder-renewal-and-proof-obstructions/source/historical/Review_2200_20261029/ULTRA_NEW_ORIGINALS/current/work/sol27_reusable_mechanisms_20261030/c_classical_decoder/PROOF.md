# A classically stored logical Pauli decoder from local calibration records

30 October 2026. C's completed restricted operation. Ordinary product
tomography, Bell/StateHSP learning and symplectic synthesis are credited;
this is not a new generic Clifford-learning or noise-threshold claim.
The actual finite execution is computational, not a laboratory experiment.

## 1. Source and consequence

A fixed memoryless CPTP source N maps q logical qubits to n physical
qubits. Training access consists ONLY of fresh Bell-input programs
J=(id_R tensor N)(Phi_(2^q)), plus known controls/measurements. The
unknown late payload is already encoded by the same N, may be entangled
with an inaccessible reference, and is not available or retried during
calibration. No unknown U, junk description, environment, adjoint,
controlled N or classical model is supplied to the receiver.

For efficient candidate discovery, the STRUCTURAL promise is an ideal
mixed Clifford encoding N0(rho)=U(rho tensor sigma)U*, with arbitrary
sigma, for which the physical images of the2q logical X/Z generators
lie in supplied patches S_a of size at most w. For example, a warranted
depth-d geometric Clifford circuit and known logical input positions
give its native causal neighborhoods. This is not an inference from a
preview or from finitely many records. Unknown support of weight w would
instead require a choose(n,w) search; this is not silently replaced by
a supplied small neighborhood.

The ACTUAL N may contain coherent or dissipative calibration error. The
quality theorem below does not assume N0 exists: it uses fresh measured
correlations of actual N. The structural/noise promise only ensures a
high-quality frame can be found at the declared cost. Bell preparation,
measurement calibration, independent shots and known-gate accuracy are
separate operational requirements, not acquired hardware facts.

Output: a finite CLASSICAL list of known Clifford gates and an output
wire set. Apply that circuit to each late payload, retain q wires, discard
the rest. All source calls precede payload arrival. There is no protected
quantum program, program refresh, generic Schur/RDS factory or online
source-call latency in the returned decoder.

## 2. Actual-channel frame theorem

Let O_(X_j),O_(Z_j) be signed physical Hermitian Paulis whose binary
symplectic commutation matrix is exactly that of the q logical X/Z pairs.
Suppose a known Clifford D maps them respectively to positive X_j,Z_j
on the chosen output wires. Define

    R_D(w)=Tr_other D w D*,
    S_(X_j)=X_(R_j) tensor O_(X_j),
    S_(Z_j)=Z_(R_j) tensor O_(Z_j),
    d_a=Tr J (I-S_a)/2.

All S_a commute. The full Bell projector on reference and decoded wires
is the product of their2q positive-eigenspace projectors. Therefore

    1-Fe(R_D N)<=sum_a d_a,                           (1)
    halfdiamond(R_D N,id_(2^q))<=2^q sqrt(sum_a d_a).  (2)

This is a whole-channel/all-reference statement, not average decoded
bit correctness. Fe is the squared normalized Bell overlap. There is
no pure-junk, exact-support or conditional reference-marginal assumption.

High correlations can themselves force the exact algebra: two
anticommuting Hermitian Paulis A,B obey <A>^2+<B>^2<=1. If every signed
<S_a> exceeds1/sqrt2, all S_a must commute, and the physical O_a have
exactly the logical symplectic matrix. The implementation nevertheless
checks that matrix exactly and refuses incompatible candidates; no
noisy commutator estimate or inferred exact span is needed.

## 3. Literal physical circuit, with its cost

pauli_compiler.py represents i^p X^x Z^z by two n-bit integers and p mod4.
Hermitian Y has p=1. Multiplication adds2 z.dot(x') to phase. H swaps
x,z and adds2xz; S adds x and toggles z; SDG subtracts x; CNOT toggles
x_target by x_control and z_control by z_target with no RAW-phase shift.
These are exact Pauli identities, including complex signs.

For each pair, fixing all earlier output wires:

1. Map its Z representative to a single positive Z by local H/SDG,
   a pivot SWAP, CNOTs into the pivot, and a possible sign-fixing X.
2. Its X representative then has X or Y at that pivot. Local SDG/H
   turns its other factors into X; CNOTs out of the pivot remove them.
   A possible Z fixes its sign while leaving the Z representative fixed.
3. All remaining pairs commute with this pair and therefore have no
   support on the now locked wire. Continue.

The code checks the entire supplied symplectic matrix, then the exact
images of all supplied signed generators. If W is the union of supports
and destinations, the emitted gate count is O(q W); for2q patches each
of size w this can be O(q^2 w), NOT automatically O(qw). Classical
updating of2q rows and full-n integer/scanning costs are additional.

route_line replaces a remote CNOT by moving its control through known
adjacent SWAPs, applying the adjacent CNOT, and restoring the swaps.
A SWAP uses3 adjacent CNOTs. Unknown intermediate junk is allowed:
the identity holds on ALL input states. General line-routing distance
is charged; no expander or arbitrary all-to-all edge is called geometric
locality. The executed q=1 source below needs only5 already-neighbor
gates. All2n Pauli-generator routing identities are checked exactly.

## 4. Find candidates with ordinary local measurements

For one requested reference generator P_a and its supplied patch S_a,
measure P_a on R and each of the3^w product X/Y/Z basis patterns on S_a,
m fresh programs per pattern. All outcomes, including parity failures,
are recorded; no postselection or exact-sample-span assumption occurs.
The counts are a2^(w+1)-outcome histogram for each pattern.

A weight-t physical candidate Pauli Q is covered by3^(w-t) patterns.
Ignoring the irrelevant measured sites gives m3^(w-t) independent +/-1
samples, all with mean Tr J(P_a tensor Q). An integer Walsh transform
of each histogram obtains all compatible correlations. There are
M<=2q4^w candidates across the requested generators, so Hoeffding gives

    Pr(any absolute correlation error>a)
       <=2M exp(-m a^2/2).                           (3)

With exact ideal Clifford access, each reference group contains its
true correlation-one logical image, regardless of mixed junk. If those
true images have actual signed correlations at least1-2e0, choosing
the largest absolute empirical correlation in each group gives
d_a<=e0+a on event(3). Once e0+a<(1-1/sqrt2)/2, the algebra is canonical
automatically; the exact compiler check is still performed.

No gap separating the junk's exact from near stabilizers is supplied.
A near-stabilizing junk factor may change the chosen frame, but (1)
tests the actual frame's error. Local tomography is an ordinary strong
method already supplying this discovery step; no algorithmic novelty
or advantage over it is claimed.

## 5. Fresh validation, uncertainty and liveness

Freeze the candidate signs and circuit BEFORE validation. For each a,
measure S_a directly on m_v fresh independent programs. A minus outcome
is Bernoulli with probability d_a. If phat=k_bad/m_v and ell>0, set

    h=ell/m_v,
    u=min(1,phat+h+sqrt(h^2+2h phat)).                (4)

The binomial lower-tail inequality
Pr(phat<d-sqrt(2d ell/m_v))<=exp(-ell), inverted algebraically, proves
Pr(d>u)<=exp(-ell). The code rounds the square root UP using integer
square root and a2^-40 grid. Union over2q fresh tests is valid conditional
on all discovery data. Combine (1)--(2) with sum u; it does NOT require
that the discovery model was right. Acceptance requires sum u<=tau.

For completeness, the operation has a paid uniform high-yield choice:
take a<=tau/(8q), suppose e0<=tau/(8q), and choose m from(3). Then
each selected d<=tau/(4q). If m_v>=1024q ell/tau, an upper-tail Bernstein
bound gives phat<=5tau/(16q), except probability exp(-ell). Substituting
in(4) gives u<tau/(2q), hence acceptance and Bell error<=tau. Discovery
cost is exactly2q3^w m, validation2q m_v. No repeat-until-success on a
payload occurs. The default finite experiment uses its stated fixed
budget and actual admission; it is NOT claimed to instantiate this
worst-case high-yield choice for every arbitrary sigma/noise level.

This pays the ordinary favorable O(tau^-1 log(1/delta)) validation regime
instead of silently imposing an additive-Hoeffding tau^-2 test. The
discovery phase can still cost tau^-2 under this simple ordinary method.

If the measured joint observable differs from S_a in operator norm by
b_a, add b_a/2 to u. A locally factorized bounded readout with per-rung
observable errors b_i gives b_a<=sum_i b_i by tensor telescoping. These
are acquired-calibration obligations, not empirical numbers inferred
from ideal known-control simulation. The actual finite packet assumes
ideal known measurements; its unknown calibration noise is IN N.

The statistical statement is joint: probability of returning a decoder
that violates its bound is at most the declared failure budget. It is
not conditional confidence after an arbitrarily low-yield acceptance.
For the SAME fixed N, each good learned circuit works on arbitrary
future inputs/references. T uses cost at most T times its one-use diamond
bound; drift and unbounded reuse performance are not granted.

## 6. Native calibration classes which do not grow with n

If U is a known-geometry finite-depth Clifford but its gates are unknown,
the promised logical images are supported in their native light cones.
Under actual finite-depth LOCAL CPTP gate errors, telescoping in the
backward causal cone bounds each desired observable's change by the sum
of the FULL local gate diamond errors in that cone. Gates outside the
cone do not affect the observable. This needs a warranted local circuit
composition, not an unknown shared reservoir or a global near-Gibbs
assumption. It allows arbitrary sigma, including entanglement/magic.

A useful explicit subclass is post-encoding product unitaries E_i plus
single-site depolarization with Pauli attenuation mu_i. For an ideal
positive Bell stabilizer S with physical support T, let
b=sum_(i in T)||E_i-I|| and g=product_(i in T)mu_i. Purifying the ideal
program, S|psi>=|psi>, and

    ||P_minus E_T|psi>||^2<=||(E_T-I)|psi>||^2<=b^2.

Thus its actual correlation is at least g(1-2b^2). Only the support
enters; error on the rest of n sites is not summed into a global
trace-distance premise. This is a visibility/yield bound, not an input
needed by the actual-channel validation theorem.

Actual decoder gates also need a contract. If their full-channel
implementation errors sum to g_err, add g_err/2 to(2). The compiler's
logical circuit correctness does not acquire noisy native gates,
detectors, routing hardware or a fault-tolerance threshold.

### A separately warranted all-input local-noise port

Root's `root_classical_decoder/SCALABLE_FRAME_AND_RIGIDITY.md` Section6
proves the ideal Pauli-channel rigidity statement. Its use here needs
only a DECODER-RELEVANT channel bound, not a global128-site error budget.
Let W include every wire of the net decoder D, and suppose the separate
warrant is

    Delta_W >= halfdiamond(Tr_barW N, Tr_barW N0).

Then R_D=R_W Tr_barW, and the actual versus ideal correlations of the
selected Bell Paulis differ by at most2Delta_W. If each certified actual
signed correlation exceeds2Delta_W, every ideal correlation is nonzero.
Conjugating each selected physical Pauli through the ideal Clifford
forces its input logical label to equal its reference label: otherwise
Bell orthogonality makes that correlation zero. The residual junk Pauli
generators commute because the physical and logical symplectic forms
match. Consequently R_D N0 is a Pauli-diagonal CPTP map, hence a Pauli
channel. Its halfdiamond error is exactly1-Fe(R_D N0). Contractivity and
the Bell-measurement fidelity difference then give

    halfdiamond(R_D N,id)<=1-Fe(R_D N)+2Delta_W.       (5)

For a POST-encoding product noise E=product_i E_i,
Tr_barW E=(E_W)Tr_barW, so Delta_W<=sum_(i in W)
halfdiamond(E_i,id). A warranted finite-depth local noisy circuit gives
a corresponding backward-cone telescoping bound. Correlated nonlocal
noise is not admitted by this argument. The selected finite circuit
uses only three adjacent physical wires; error at other outputs need
not enter this EXTRA relevant-channel premise, even with entangled junk.

This can avoid the generic2^q sqrt(error) conversion only when its local
all-input calibration premise is actually supplied. Good Bell records
alone do not supply Delta_W. Equation(5) is NOT used to tighten the
executed QUALIFIED_DECODER.json; its generic.1834 bound is preserved.

## 7. The exact finite computational acquisition

source_acquire.py instantiates n=128,q=1, a warranted5-site radius-two
patch, and an opaque Clifford encoding with TWO nearest-neighbor
ENTANGLING layers interspersed with local H/S layers. This is not total
gate depth two. Its
518 unknown Clifford gates are not read by the receiver. The junk is a
global1024-gate Clifford of127 full-rank mixed magic qubits with Bloch
(2/5,2/5,2/5), so it is neither pure junk nor a Pauli-noisy pure stabilizer
input. Unknown actual output calibration includes a coherent Z rotation
with tan(theta/2)=1/100 and depolarizing Pauli attenuation499/500 at
EVERY physical output site.

The backend computes EXACT rational local Born laws by Heisenberg
contractions, never materializing a2^128 density matrix. It draws
995328 discovery and131072 disjoint validation records using63-bit
rounded categorical tickets. A seeded PCG64 run is only a numerical
application; it does not itself warrant independent ideal variates or
the quantum device model. Ideal fair-ticket law error is explicitly
bounded, summed over all records, by

    15309/2251799813685248 + 1/70368744177664.

The declared ideal-law total statistical failure bound is
4098*(3/8)^16<.001, using e>8/3; the rounded-law bound adds the displayed
TV quantity. These confidence contracts are not claims about PCG64.

The strict receiver reads only the contract and declared measurement
counts/request. It neither imports source_acquire nor reads its unknown
U, sigma, probabilities or TRUTH_AUDIT. Integer histogram processing
selects signed physical Pauli pairs. The stored/qualified controller is

    H64, CX(64,63), SDG63, H62, CX(63,62),

then retain output wire63 and discard the other127 wires. All256
generator conjugations verify the routing exactly. The final validator
RECOMPILES and embeds the circuit from its validated signed pair, so an
unrelated/stale DECODER file cannot inherit its qualification.
The implemented record format and CLI are explicitly q=1, whereas the
mathematical frame theorem and compiler allow general q. The CLI checks
positive budgets, the exact reference order, source/request identities,
count shapes and the discovery concentration premise before reporting
the displayed joint risk.

Results from actual records:

    Bell fidelity >=272566541459/274877906944
                  =.9915913013501267,
    general all-input halfdiamond <=.18339791329162836.

The exact hidden-source audit (not supplied to the learner) gives
Fe=49825264870270499/50010000500000000=.9963060262371023. The generic
diamond bound is deliberately much looser; no1% all-input claim follows.
There are NO later source calls or quantum program memories. Physical
source preparation/measurement/controller admission remains NOT_ACQUIRED.
