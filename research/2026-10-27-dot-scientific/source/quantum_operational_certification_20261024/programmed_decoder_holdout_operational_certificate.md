# Model-free holdout validation of the actual programmed recovery instrument

Status: new exact finite-confidence certificate, pending independent receipt. This validates a LOW-DIMENSIONAL effective instrument, not the high-dimensional channel model, entropy deficit, or an adversarial public transcript.

## 1. What is fixed and trusted

Fix any one programmed decoder BEFORE validation, including its tuning parameters, gate circuit, training-ensemble distribution and finite number n_train of consumed channel calls per data attempt. It may be the labelled receiver already received, but its assumed isometry-plus-reset model need NOT be true for this certificate. For every attempt the circuit is nevertheless a legitimate CP instrument, with accepted qutrit output and an erasure flag.

Assume the underlying channel is fixed and memoryless on all training, holdout and subsequent data calls, with trusted qutrit preparation, known receiver output interface and trusted low-dimensional measurements/gates. Use fresh independent program batches, discard their labels/randomness, and prepare the data/reference independently of training. These assumptions define a fixed averaged effective qutrit-to-(qutrit+erasure) channel even when the underlying physical output dimension is arbitrarily large. No future guarantee is made for hidden memory, drift, adversarial transcript-conditioned inputs or untrusted devices.

## 2. Six known input states suffice for an assisted-rate certificate

Fix an input qubit embedding W:C2->C3. On each HOLDOUT attempt choose uniformly one of the six Pauli eigenstates |psi>. Encode it by W and send it through the original channel using one fresh programmed-decoder batch. At the recipient, project the accepted qutrit output onto ranW and decode by W*. Treat every other outcome as rejection. If accepted, measure the projector |psi><psi|, using its known classical preparation label.

Record A=1 for acceptance and0 otherwise. Record B=1 for acceptance AND the matching-projector outcome, and0 otherwise. Thus0<=B<=A<=1. Let S2 be the actual subnormalized qubit CP map induced by this ENTIRE fixed procedure, averaged over discarded program randomness. Its subnormalized Choi state C=(id2 tensor S2)(Phi2) has
 z=TrC=E[A], w=<Phi2|C|Phi2>.
The six-state2-design identity gives EXACTLY
 f=E[B]=(z+2w)/3.                                      (1)
It is valid for arbitrary trace-nonincreasing S2; input-independent acceptance is NOT assumed.

For a preselected number N of independent attempts and confidence parameter0<delta<1, set
 h=sqrt[log(4/delta)/(2N)],
 zL=hat z-h, zU=hat z+h, fL=hat f-h.
Hoeffding and a union bound give, with probability at least1-delta, simultaneous zL<=z<=zU and f>=fL. Correlation of A and B on one attempt is harmless. Adaptive repeated peeking or selecting among candidates using the same holdout requires a separate valid confidence allocation and is not included.

If the observed certificate satisfies
 zL>0 and fL>=7zU/8,                                    (2)
then (1) guarantees w/z>=13/16. This is a statement about the actual effective instrument, irrespective of whether the proposed isometry/reset/entropy model was correct.

## 3. A charged operational consequence

For future data attempts the sender prepares a qubit Bell pair and directly encodes its sent half into W. There is no sender projection or extra2/3 loss. Fresh program batches and IID channel calls give independent identical accepted Bell states C/z, with probability z>=zL. Bilateral qubit Pauli twirling makes them Bell diagonal while preserving their singlet fraction. Their entropy is at most that of(13/16,1/16,1/16,1/16). The previously received iid hashing theorem therefore gives at least
 h0=[13log2(13)-48]/16>0
entangled qubit pairs per accepted pair.

With confidence at least1-delta, the asymptotic TWO-WAY-ASSISTED entanglement rate per TOTAL original channel use is at least
 zL h0/(n_train+1).                                    (3)
The N holdout attempts themselves cost N(n_train+1) original channel calls and their quantum storage/gates; any prior candidate construction or exploration is additional. For a finite subsequent block of L attempts the denominator is(N+L)(n_train+1), before any further preparation costs. Formula(3) is asymptotic with fixed holdout overhead; it is not a finite-block hashing guarantee. Recipient herald flags precede forward hashing, so the overall protocol uses two-way classical communication.

The certificate also witnesses that the original channel is not entanglement breaking: local programming/preparation/decoding independent of the data cannot create entanglement with the sender's retained Bell half through an EB channel. Training outputs may be quantum program resources but are independent of that fresh Bell pair and are prepared from classically labelled unentangled inputs in the labelled model.

For recovery rather than distillation, input/output Pauli twirling of S2 makes its acceptance probability constant z and its normalized accepted channel a Pauli channel. The certified singlet fraction F gives exact diamond distance2(1-F) to the identity for that Pauli channel. Thus a stronger observed version of(2) can validate a more accurate heralded recovery channel without identifying the large physical output.

## 4. The structural promises guarantee discovery, not validity

For the source-unknown learned receiver's sufficient regime, choose zeta=p0/180 and assume epsilon<=p²/120. The already acquired complete error eta<=a/10, a=p/9, implies
 z>=p0/10 and F>=9/11.
Then f-7z/8=z[(1+2F)/3-7/8]>=z/264>=p0/2640.
On the simultaneous concentration event, fL>=f-2h and zU<=z+2h. Therefore (2) holds whenever h<=p0/9900. For example,
 N>=ceil[9900² log(4/delta)/(2p0²)]
is a sufficient, deliberately conservative discovery budget. It is independent of raw output dimension but can be enormous. This promise-based pass guarantee is logically separate from the model-free validity of any observed certificate(2).

## 5. Optional twelve-state qutrit non-EB witness

For the unprojected accepted qutrit CP map, use the twelve qutrit2-design inputs from the labelled-training construction and matching qutrit projectors. Then f3=(z3+3w3)/4. The same Hoeffding bounds certify a non-EB accepted operation whenever f3,L>z3,U/2, since then w3>z3/3. This weaker witness need not meet the qubit hashing threshold. Failure of either certificate proves neither EB nor absence of assisted capacity.

## Comparison scope

Any equally informed fixed generic decoder may be subjected to the SAME low-dimensional holdout protocol. The certificate is not a claim that the signed-Choi learner is statistically or computationally optimal. Its advantage here is that the proved structural promises supply a concrete candidate guaranteed to pass with finite charged resources. The validation guarantee itself does not silently inherit those promises or certify them.
