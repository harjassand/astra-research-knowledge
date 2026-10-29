# Random encoder plus a learned physical decoder for unknown low-Kraus-rank noise

2026-10-29. Root construction/transfer; independent review pending. Random-code decoupling is established prior machinery, not a new coding law. The new operational obligation is constructing the decoder from opaque forward queries.

## 1. Source and encoder access
Let a FIXED memoryless CPTP source N:L(C^D)->L(C^Dout) have Kraus rank at most r. The source map is chosen independently of the fresh encoder seed. The controller can prepare known code inputs and trusted endpoint controls, but does not know source Kraus matrices, an environment, inverse, or Stinespring unitary.

Take D=2^n and logical k=2^ell<=D, k>=2. Choose a uniformly random Clifford unitary U on n qubits (an exact unitary2-design), and define the KNOWN encoder E_U|psi>=U(|psi> tensor |0>^(n-ell)). Uniform Clifford sampling and circuit synthesis have standard finite polynomial-size constructions. All n carrier qubits, code preparation, private logical padding and storage are paid. The source may be arbitrary coherent/nonunital low-rank noise, but cannot adversarially select a new map after seeing U.

## 2. Established random-code performance, with a direct moment derivation
For mathematical analysis only choose Kraus matrices K_a, a<=r, and the complementary channel T=N^c. Let P=E_U E_U†, J_RE the normalized Choi state of T E_U, and tau_E=T(P/k). Define Delta=J_RE-I_k/k tensor tau_E. Uhlmann's theorem and the trace-distance/fidelity inequalities imply existence of a decoder with
 Fopt(N E_U)>=1-||Delta||1.
No complementary-channel access is used by the algorithm.

Set a=Tr[T(I_D)^2], b=Tr[N(I_D)^2]. The exact unitary second-moment identity gives
 E_U ||Delta||2²=[(k²-1)/(k²(D²-1))](b-a/D)<=b/D².
The rank is at mostkr, so Jensen/Cauchy--Schwarz gives
 E_U[1-Fopt(N E_U)]<=sqrt(kr)||N(I_D/D)||2<=r sqrt(k/D)=:A.
The last inequality follows from N(I_D)<=r I_Dout and trace N(I_D)=D. Both estimates hold for an exact2-design because the squared-norm expression is quadratic in the code projector. The fixed environment-marginal comparison used in check_random_code_moment.py gives a slightly weaker but independently diagnostic moment; it is not substituted for the above identity.

Klesse, quant-ph/0701102v2, Sec4.2/Eq28, already proves the Haar average bound sqrt(kr)||N(I/D)||2. The present algebra fixes normalizations and the exact2-design transfer; it does not claim priority for random coding, decoupling, capacity lower bounds, or efficient Clifford generation.

## 3. Acquire the missing decoder
For each fixed public seed U, the restricted channel A_U=N E_U has output support rank at mostkr, since its Kraus images span at mostkr dimensions. It can therefore be trained by the received joint-support-compression/learned physical recovery algorithm, with d=min(Dout,kr), adjusted to the received power-of-two padding.

Training queries prepare logical Choi halves, apply the known E_U, and invoke the original opaque source. Store their outputs. The later payload is encoded with the same E_U; it is jointly compressed with training outputs and physically decoded. This returns a logical k-dimensional state, not a classical reconstruction of the D-dimensional noise. No global encoder optimizer is required: code choice is randomized and decoder construction is in the small compressed space.

The received optimization-free Petz learner gives, for each fixed code, actual entanglement fidelity at leastFopt(A_U)^2-tau, where tau=3delta+beta+gamma. Averaging over the independent encoder seed yields
 F_e(complete learned-code protocol)>=1-2A-tau.
A separately received standard known-small-channel SDP decoder may improve this to1-A-(2delta+zeta+beta+gamma); its actual receiving status must remain separate from the Petz version.

## 4. Actual endpoint padding gives a linear identity-error bound
Here the controller has access to the logical payload BEFORE encoding, unlike a decoder-only task in which an already-encoded unknown state simply arrives. Apply a fresh uniform logical Pauli BEFORE E_U, apply its inverse AFTER the learned logical decoder, and retire the key. This physically Pauli-twirls the entire logical input-output channel. Entanglement fidelity is unchanged, and for a Pauli channel half-diamond distance to identity is exactly its total nonidentity Pauli probability1-F_e. Consequently the reduced decoded channel obeys
 halfdiamond(Decoded,id_k)<=min(1,2r sqrt(k/D)+3delta+beta+gamma)
for the Petz learner, with all randomness averaged and implementation allowances included. The SDP variant has the corresponding coefficient1 and its own received error budget.

The key is not released as part of a stronger joint-output target. Without pre-encoding payload access, this padding cannot be silently inserted into the decoder-only theorem. Without key retirement, a linear joint-output guarantee can fail. The independent model-free guard can provide its separately received accepted-memory-filter statement; this section itself is a reduced-channel IID/oblivious-source coding theorem.

## 5. What this makes possible and what it does not
This gives an actual random ENCODER plus learned physical RECOVERY construction for an arbitrary unknown fixed low-Kraus-rank source, rather than assuming the useful code/frame has already been supplied. A sufficient dimensional regime for a small error is D large compared withkr²/error², together with the paid training/implementation budgets. No classical description of the complete source/environment is reconstructed.

Training query count depends polynomially on logical dimensionk, rankboundr and inverse accuracy, not on ambientD orDout. With the received finite-design compiler, the theoretical known-control/bit cost is polynomial in these parameters and logD/logDout, with very large constants. Protected quantum training storage still scales with the number of stored output qubits. No native circuit or full learner was executed here.

For fixed small logical dimension this is a meaningful asymptotic resource statement. Taking k comparable toD can give a high-rate EXISTENCE bound, but the learner is polynomial in k, hence exponential in logk; efficient high-rate many-logical-qubit coding is NOT proved. Low Kraus rank is restrictive: extensive/full-rank junk or memoryful noise can violate it, and the accepted rank barrier prevents a rank-free universal claim.

The guarantee is an average over a fresh encoder seed for a fixed source, not a worst-case guarantee for every code. Fresh whole-algorithm Bell validation can select seeds using its own soundness/availability budget, but is not an uncharged part of this theorem. Source noise that can adapt to the chosen encoder is outside the random-coding premise. Unknown noise during trusted gates/buffers, practical overhead, strong conventional comparisons, and historical novelty of the complete transfer remain open.

## 6. Reproduction and primary interfaces
check_random_code_moment.py samples Haar codes for a fixed partial-trace source, verifies the moment numerically, and computes exact-model Petz fidelity ONLY as an oracle benchmark. It does not supply unavailable matrices to the actual learner, execute a Clifford sampler, or demonstrate a hardware gain.

Primary sources read/retrieved: Klesse quant-ph/0701102v2 (random-code performance); Dankert--Cleve--Emerson--Livine quant-ph/0606161 / PRA80,012304 (Clifford2-design); Koenig--Smolin arXiv1406.2170 (efficient uniform Clifford selection). Learned-recovery, uniform compiler, padding/guard and optional SDP performance remain governed by their exact Astra source/receipt versions.
