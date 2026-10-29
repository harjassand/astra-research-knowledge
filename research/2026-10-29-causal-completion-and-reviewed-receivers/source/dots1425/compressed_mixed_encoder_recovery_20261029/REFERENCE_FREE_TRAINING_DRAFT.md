# Reference-free training inputs for the jointly compressed physical decoder

2026-10-29. Root operational extension, receiving review pending. Removes the need to bring logical Choi-reference halves to the decoder, not the need for coherent output storage.

## Fixed prepare-and-measure experiment
The sender/controller can prepare the following known logical k-dimensional states:
 |i><i| for each i;
 rho_(ij,R,±)=(|i>±|j>)(<i|±<j|)/2;
 rho_(ij,I,±)=(|i>±i|j>)(<i|∓i<j|)/2,
for i<j. There are2k²-k input settings. Keep only their classical labels. Send repeated preparations through the opaque channel (or through the chosen known encoder followed by the physical noise source). The decoder stores the quantum OUTPUTS; it needs no entangled training reference and no joint sender/receiver Bell measurement.

After the later encoded payload arrives, jointly compress ALL training outputs and the payload. Reference-joint compression applies to these nonidentical known inputs as well: conditional on one common latent U, each training group contains independent outputs of A_U applied to its specified logical preparation. The decoder may now perform ordinary finite process tomography in dimensiond using those labels. Independent compression of separate groups would not provide this common U and is not substituted.

## Explicit matrix reconstruction
Let S_i=A_U(|i><i|), and let Y_R=S_(R,+)-S_(R,-), Y_I=S_(I,+)-S_(I,-). Then
 A_U(|i><j|)=(Y_R+iY_I)/2,
 A_U(|j><i|)=A_U(|i><j|)†.
Together with the diagonal outputs this reconstructs the normalized Choi estimate used by the already received rational repair/Petz or standard SDP decoder. No environment or original-D channel tomography is performed.

Estimate each output density matrix with the same d² diagonal/real/imaginary two-level settings. If every real/imaginary output entry has error<=e0, each reconstructed normalized-Choi entry has component error<=2e0/k. Thus set e0=ke/2 to meet the old entry bounde. With M=(2k²-k)d² measurement settings and m repetitions per setting,
 m>=log(2M/beta)/(2e0²)
ensures all entries meet the requirement with probability>=1-beta. The exact-integer alternative chooses L minimal with2^L>=2M/beta and m=ceil[L/(2e0²)]. Training calls are N=M m. These conservative bounds are not a claim that this measurement scheme is sample-optimal.

On arbitrary statistical outcomes, reconstruct a Hermitian estimate using conjugate block pairs, then apply the received exact marginal repair, positive ridge and certified fallback. The physical learned decoder and its fidelity/implementation bounds are unchanged after substituting this new N into the joint-compression and design orders. All preparations, compressed-output measurements and finite arithmetic are known operations with charged synthesis.

## Remote interface and limitations
For a spatially separated sender and decoder, known training preparations and their classical labels suffice. No preshared entanglement or noiseless QUANTUM link carrying training reference halves is assumed. The large quantum source outputs must still be stored coherently at the decoder and processed jointly with the later payload; the classical labels/code seed must be supplied through a declared classical channel. This is not free classical communication or a claim about one-way capacity without an interface contract.

Endpoint Pauli randomization, if used for a linear reduced-channel identity bound, additionally requires the sender to control the payload before encoding and the decoder to receive/use the key under the stated privacy/retirement boundary. Reference-free TRAINING does not remove those separate resources. The decoder-only already-encoded-payload theorem cannot insert a new input pad retroactively.

As before, the learned small matrix belongs to this common jointly compressed batch. It is not a reusable original-D classical decoder for arbitrary future outputs. Source stationarity/memorylessness governs the learning guarantee; the separately received finite guard supplies only its own model-free accepted-operation soundness against causal memory.
