# A paid ordinary full-throughput recovery for exact flat mixed encodings

30 October2026. An explicit specialization of random dilation, the flat Petz
map and ordinary known-amplitude amplification. This is a mathematical circuit
construction, not a quantum/source execution, an optimality claim or a new
recovery theorem. Its physical-query bill is quadratic in r, not linear.

## 1. Native input and complete output contract

Fix logical dimension k (k=2 suffices), integer r>=1, and ambient D>=kr.
The native black box is the SAME memoryless CPTP map on every call,

    N(rho)=U(rho tensor I_r/r)U^*,
    U:C^k tensor C^r -> C^D,   U^*U=I.                    (1)

The known inputs are k,r,D and rational target0<epsilon<1. U and its output
subsystem structure are unknown. Arbitrary adaptive/entangled FORWARD calls,
known universal controls, clean known ancillas and protected quantum storage
are allowed. Unknown adjoints, controlled dilations, inverses, input access
to the r-dimensional junk and a quantum switch are NOT given.

The output is one logical system for EVERY already encoded incoming payload,
with arbitrary retained reference. There is no heralded loss/postselection.
For a declared finite number of future payloads, the entire source programme
can be acquired BEFORE they arrive; no original N call is then made online.
Programmes are consumed. This is not an unlimited reusable classical decoder
or an unchanging quantum catalyst.

## 2. Exact flat recovery and its normalization

Write U_j psi=U(psi tensor |j>) and K_j=U_j/sqrt(r). Then

    K_i^*K_j=delta_ij I_k/r,
    N(I_k/k)=Pi/(kr),  Pi=UU^*,
    r N^*(N(rho))=rho.                                 (2)

The CP map rN^* has trace Tr(Pi w) on an arbitrary output w; it is trace
preserving on the occupied support Pi. Add any fixed-output fallback outside
Pi to obtain a mathematical CPTP extension. No unknown Pi gate is inferred.

For ANY r-Kraus Stinespring frame V psi=sum_j |j>K_j psi, define

    T_V w = sqrt(r) sum_j (K_j^* w) tensor |j> .         (3)

T_V^*T_V=Pi, so this is a partial isometry, and tracing its last register
implements the same rN^* on Pi. Changing the Stinespring environment frame
only rotates the discarded register; it does not change the recovery.

The mean inverse S^(-1/2) needed in a generic Petz algorithm is simply
sqrt(kr) times identity ON Pi. It need not be approximated by QSVT or acquired
from output-mean copies. This is an exact use of the promised flat model,
not a transfer to an arbitrary approximately flat or noisy channel.

## 3. The actual forward-query programme supplier

Yoshida--Niwa--Utsumi--Takagi--Murao2512.21260v2 Theorem3 and Lemma6 supply
a known physical offline circuit, from Q parallel native N calls, whose
output has the joint mathematical representation

    E_(V,theta) [P_(V,theta)/k]^tensor Q,
    W_(V,theta)=(e^(i theta)|0>V0+|1>V)/sqrt2,
    P_(V,theta)=W_(V,theta)W_(V,theta)^*.                 (4)

V is ONE random Stinespring frame of N with environment dimension r; theta
is ONE common uniform phase. V0:C^k->C^r tensor C^D is a PUBLIC embedding.
All Q programme copies share the SAME latent V,theta. The circuit need not
reveal either. Its native input preprocessing is allowed under the physical-
query contract, but is not asserted possible from an iid Choi-copy tape alone.
Every programme in (4) costs one original forward query, via this joint
factory, not one free purification or arbitrary controlled unknown gate.

Let

    A_(V,theta)=2P_(V,theta)-I.                          (5)

It is a selfadjoint unitary, and the elementary rank-k projector algebra gives

    A_(V,theta)(|0> V0 psi)=e^(-i theta)|1>V psi.         (6)

The input code |0>V0 C^k is public, so its projection and basis identification
are known controls. The flag in the output of (6) is KNOWN to be1. The r
environment modes are unknown only through their frame, not their dimension.

To implement (5), expend fresh copies of P/k in ordinary partial-SWAP density
matrix exponentiation at time pi*k. The ideal result exp(-i pi P)=-A differs
only by a GLOBAL minus sign in an uncontrolled call. If a controlled call is
ever used, a KNOWN Z on the control pays the relative minus sign. Negative
time uses a reversed known partial-SWAP, fresh programme and the same latent
frame; no noisy reduced channel is inverted. A full-diamond error bound is

    error <= 4(pi*k)^2 / s                              (7)

using s fresh programmes per requested reflection. This conservative bound
is supplied by the already established finite collision/DME proof; it also
follows by second-order one-collision expansion and channel telescoping.

The reflection supplier and all later algorithms are analyzed conditional
on ONE V,theta, then averaged. Averaging each programme independently first
would destroy the native inverse signal and is explicitly not this circuit.

## 4. Literal base block; its amplitude is1/r

Prepare the PUBLIC maximally entangled state

    |Phi_r>_(E E')=r^(-1/2) sum_j |j>_E |j>_(E'),

put the flag in KNOWN state1, adjoin the received B payload, apply (5), and
project onto the known input code |0>V0 C^k. Keep the decoded k-dimensional
code coordinate and E'. This is a block of a known-format unitary circuit,
not a physically postselected output in the final algorithm. Its block is

    B_(V,theta)=(e^(i theta)/r) T_V.                    (8)

Indeed the inverse Stinespring code block is e^(i theta)V^*, and the normalized
environment pair contributes1/sqrt(r); comparing with (3) supplies the other
1/sqrt(r). Thus

    B^*B=Pi/r^2.                                       (9)

It is ZERO on Pi-perp. There is no arbitrary off-support successful block.
The output flag1 in (6) lets us seed only r environment modes. Treating the
reflection as a generic2r-environment dilation would unnecessarily replace
the amplitude1/r by1/(sqrt2*r).

All projectors used for amplification are KNOWN ancilla/code projectors.
The initial projector is arbitrary B tensor the known ancillary seed; the
success projector is the public |0>V0 code, the dilution flag and free E'.
Neither is the unknown physical Pi. For k=2, binary padding identifies the
public code coordinate with a logical qubit plus zero workspace. For another
fixed k, public register padding/permutations and unitary extensions on unused
basis states provide the same implementation; their known costs are paid.

## 5. A fully explicit all-r amplification schedule

For every r>=1, set

    theta_r=pi/(4r+2),   lambda_r=r sin(theta_r),
    j=r,                M=2r+1.                        (10)

Here0<lambda_r<1, because pi<4. Adjoin a known dilution ancilla whose success
amplitude is lambda_r. The resulting base block is

    e^(i theta) sin(theta_r) T_V.                       (11)

Use j ordinary Grover/oblivious-amplification iterations and the base call,
with reflections about the two known projectors just described. There are
exactly M=2r+1 calls to (5) or its inverse; the inverse is the SAME reflection.
For every vector in Pi, the two-projector amplitude-amplification plane has
initial angle theta_r. The final success amplitude is exactly

    sin((2r+1)theta_r)=sin(pi/2)=1.                     (12)

The failed component is zero. The overall output phase e^(i theta) is common
to the logical input and disappears at channel level. Equations(9)--(12)
hold for superpositions and arbitrary references: they are a partial-isometry
block identity, not an average success statement for selected test states.

The whole executed unitary/ancilla/discard circuit is CPTP on EVERY B input.
On Pi it is exactly the isometry T_V, up to a global phase. On Pi-perp it has
some physical fallback action, which is allowed and requires no unknown
support measurement. After discarding E' it is the same exact inverse rN^*
for every latent V,theta. Composed with N it is identity, at FULL throughput.

This is the ordinary known-amplitude-amplification mechanism. The public
dilution avoids a ceiling decision involving an almost-integer transcendental
angle and gives a literal uniform schedule, not a search over pulse counts.
The stronger pure endpoint r=1 can instead use the exact four-forward-query
qubit-isometry inversion of2401.10137v3 Section3.3/Corollary6, with queries
INTERLEAVED online. That ordinary endpoint is admitted; it does not supply
an inverse of the mixed source when r>1.

## 6. Finite precision and original-source bill

Choose a full-channel error budget epsilon. Allocate epsilon/2 to all sample-
programmed reflection calls and epsilon/2 to the programme factory and known
controller synthesis. Each of M calls receives full-diamond error at most
epsilon/(2M). By (7), it suffices to choose

    s=ceil[8*pi^2*k^2*M/epsilon],
    Q=M*s=O(k^2*r^2/epsilon).                           (13)

Use the rational upper pi<22/7 for an exact integer ceiling. All Q native
queries can occur OFFLINE; this includes calls used to acquire the reflected
programme and its common random frame. After the factory has run, source
calls during a payload are ZERO. The payload nevertheless remains coherent
during Q partial-SWAP collisions and the known amplification/controller gates.
Offline acquisition does not eliminate online gate depth or protected storage.

The amplitudes in the public env-Bell preparation and lambda_r rotation are
known computable numbers, not oracles. For example lambda_r lies between1/2
and pi/4; inverse-trig conditioning for its rotation is uniformly bounded.
Taylor/Machin or directed elementary-function routines to
poly(log r,log(1/epsilon)) bits and ordinary known-unitary synthesis suffice.
Divide the controller error allowance over its actual finite gate count.
Known inverse/preparation circuits are reversed normally; only their uses of
the unknown reflection are separately supplied by fresh programmes.

The source factory uses Schur transforms and known representation controls.
The fixed-rank large-GT enumeration shortcut is NOT used: the previously paid
highest-weight/small-Schur/common-finite-Haar port gives polynomial cost in
Q,r,k and logD, with its precision cost charged. The programme store alone
has Q registers of O(logD+logr) qubits; factory representation workspace is
additional polynomial workspace, not free. Retention must protect all these
quantum programmes. Each requested recovered payload consumes its own finite
store; there is no unlimited reuse claim.

For T future payloads with a single JOINT stream-error budget epsilon, apply
the same construction to M_T=T(2r+1) reflection calls, yielding the conservative
Q_T=O(k^2*T^2*r^2/epsilon) joint offline bill. Alternatively acquire independent
per-payload programme batches with per-use error epsilon/T, giving the same
order. If epsilon is instead per-use accuracy, the independent-batch total
is T*O(k^2*r^2/epsilon). The ideal recovered channel is the SAME identity in
every latent frame, so averaging programmes or entangling payloads does not
invalidate the hybrid stream bound. Programme stores/finite gates are consumed
and paid; a family of arbitrarily many later payloads is not obtained free.

## 7. Actual scientific boundary

This completes an ordinary arbitrary-payload, reference-safe, full-throughput
recovery under the exact flat promise using ONLY forward physical N queries,
with all original calls paid offline. It improves the needlessly generic
inverse-mean/filter precision apparatus for this class. It does NOT remove
the quadratic-r programme acquisition cost of this supplier and is not a
linear-r active-query theorem. N1104's physical-query Omega(r) and iid-Choi-
copy Omega(r^2) distinctions remain intact; neither is promoted to a matching
physical-query lower bound here. A sharper active comb/representation that
bypasses the quadratic query-to-reflection lift remains a real open operation.

The primary's Theorem13 Petz application has the opposite dimension-ratio
condition (minimum Kraus rank=input/output dimension) and is NOT directly
invoked for (1). Sections3--5 above supply the missing correct composition.
Isometry inversion does not magically purify a mixed payload; RDS does not
retroactively attach its lost environment to a previously encoded payload.
Virtual inverses/quasiprobabilities that recover only expectation values are
not arbitrary quantum-payload recovery. A quantum switch is nowhere used.
