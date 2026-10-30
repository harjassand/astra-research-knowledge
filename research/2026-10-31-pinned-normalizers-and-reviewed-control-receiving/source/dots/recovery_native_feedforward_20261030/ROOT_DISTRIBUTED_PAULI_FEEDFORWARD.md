# Protected classical computation to distributed physical logical-Pauli control
30 October 2026. Root construction candidate. Not a whole accepted feedforward or measurement theorem.

## Task and honest input
Input is an internally ENCODED CLASSICAL record z, possibly correlated with a native logical DATA/reference state. In each classical z branch, the source has the admitted native logical/error module and a positive auxiliary/bath state; retained garbage may record z. It must not carry unspecified extra unknown logical information within that branch. The record is protected in the actual received computation code, not an immutable external bit.

The target is a specified logical Pauli P_L(z) on a native Tanner bank. Fix physical Pauli representatives in advance. Their physical component bits c_i^X(z),c_i^Z(z) are explicit Boolean functions, e.g. binary linear combinations of the supplied logical representative matrices. The intended physical P(z)=product_i X_i^(c_i^X) Z_i^(c_i^Z) normalizes the ZERO-reference code; it does not silently implement arbitrary dense syndrome-frame correction.

This is classical feedforward, not a coherent controlled unitary preserving an arbitrary quantum program. Copying and discarding a quantum control would dephase it. The supplied logical measurement interface must earn the classical instrument/retained-branch contract.

## 1. Never decode one master bit and fan it out unprotected
Use the accepted ordinary fault-tolerant processor to compute ALL 2N physical command bits as encoded output symbols while z remains encoded. The circuit has bounded fan-in/fanout and includes the actual copying/arithmetic and ancillas. It may be a reversible classical circuit implemented by the same quantum gate primitives. Conditional on a correct classical z, the ideal outputs are the computational-basis product c(z). Global computation error is chosen exponentially small in N.

Physically de-encode EACH command symbol separately using the accepted actual top-down quantum output decoder and finite qudit-to-qubit port. Its complete joint bad-output law has a fixed small strength p_dec, uniform in concatenation depth. Do not de-encode a single command first and broadcast that exposed bit: one error there would flip the whole logical Pauli with a constant probability.

At the fixed final window, command qubit i controls an actual two-site X or Z operation on native DATA resource i, identity on its tags. Use two fixed layers for X and Z if necessary. All nominal native operations are off in that window as in the reviewed selectable-pulse model. The local command ancillas and all native private idles remain noisy. Each native DATA resource has only a fixed number of command neighbors; no all-bank fanout port is used.

Correct command bits implement P(z) exactly. An arbitrary erroneous command state or bad final gate affects only the corresponding constant-size DATA/controller region. Quantum coherence in bad command outputs is retained in the correctable operator span; it is not modeled as an independent wrong-bit probability.

## 2. Same-circuit output-region accounting
For a DATA region containing its two physical command outputs and final gate locations, use the exact OR majorant

 p_region <=(1+p_dec)^2(1+x)^(c_gate)-1,

where c_gate counts the actual fixed final-location budget and x is its received local fault strength. Hub-only idles have their own fixed-size bound. Same-site operations belong to ONE region, and input/reset/transfer locations must not be double counted. Thus p=max p_region is a fixed small number, not p_dec assumed unchanged.

The full signed expansion, not separate marginal estimates, must give the mixed computation-bad/output-region conjunction. On disjoint location sets the existing sieve provides this and the familiar factor1+b_comp when restricting to computation-good. For M=O(N), the cardinality tail is then bounded by

 b_comp+(1+b_comp) binom(M,K)p^K(1+p)^(M-K),

with actual additional native-cut losses stated separately. Good outputs have at most K=delta N bad regions. Combining their footprints with the already-small live prefix source puts the post-P(z) DATA/controller state in the same warm target logical module. A positive factor repair must be controlled by the actual bad MAP norm or a separately justified gentle bound; correct output labels alone do not establish this.

## 3. Concurrent waiting and the retained-bath seam
DATA remains under native protection while command computation and all higher-level output-decoder stages run. Those stages can take polynomial N time. Arrange the deterministic schedule so a native relaxation interval ends immediately before the final constant physical decode/control window. The command outputs remain encoded until this fixed window; there is no long wait by exposed physical bits.

Two marginal protection claims cannot simply be multiplied, because DATA and z may be correlated and share a bath. ROOT_TNI_CAVITY_RECEIVING.md proposes the exact receiving route: impose the native complete-loss cut in the proof while its nominal memory runs, and apply processor cavities to this SAME CP/TNI joint dynamics. The cut acts in the processor's retained complement, commutes its intended gates, and does not enlarge processor support of weak terms. At the final window the native generators are off, so actual DATA/control boxes are disjoint scheduled gates and use the ordinary full-system cavity expansion.

A precise whole proof can use a time-dependent active-location list: during waiting only processor gate locations are in the circuit expansion, while protected native dynamics is the complementary subsystem; during the final window the now-idle native sites and DATA/control boxes are included. Every cavity projection must isolate its CURRENT active block from all other nominal interactions. Merely declaring the native system an inert reference, or ignoring native trace loss, is invalid. The time-dependent hybrid cavity and its exact fault-class receiving remain explicit proof obligations here.

## 4. Classical branches, logical action and reset safety
The known record source must be block diagonal in its logical classical z, or be replaced by a genuinely received approximate classical instrument. Auxiliary output may depend on z; demanding outcome-independent garbage would be wrong. Within each branch, all good computation/control maps implement the SAME P_L(z) with the native correctable-span identity. A direct-sum positive auxiliary repair can therefore preserve the desired classical feedforward channel, provided its complete branch instrument is actually established. No factor equal to the number of possible z values should appear: use a channel/direct-sum bound, not a union over exponentially many labels.

Discarding local command ancillas after the control is legitimate for this classical target. It must not be advertised as an unknown quantum-program operation. Any raw measurement/control garbage retained as future bath stays in the common model; tracing it for presentation does not make future correlations vanish.

Target DATA is never reset during this operation. Fresh command qubits and temporary processor ancillas use the actual finite reset interface. Nominal helper-DATA gates are off after the final control, and residual couplings must meet the native incident bound. Subsequent native cooling uses the same hardware and strict warm budget, not a clean controller restart.

## 5. Resources and unfinished scope
The Boolean command computation is polynomial in N for supplied logical Pauli matrices. Exponentially small global computation error makes protected overhead polynomial N, potentially huge. Native DATA waits for that actual time; its exponential-in-N horizon is sufficient for fixed polynomial runtimes at sufficiently large N, unlike the unresolved comparison between two exponential rates. Final control has fixed depth and fixed local body/strength. The external fixed schedule remains a resource.

If completed, this would supply a physical INTERNAL logical-Pauli feedforward operation from protected measurement outputs without pristine classical software or a single vulnerable broadcast bit. It would be reusable in encoded teleportation and gate-injection constructions, but does not alone prove those constructions, arbitrary coherent controlled gates, universal native computation, an autonomous scheduler or final external detector reliability. A complete logical measurement instrument and the hybrid waiting/final-window receiving are still required.
