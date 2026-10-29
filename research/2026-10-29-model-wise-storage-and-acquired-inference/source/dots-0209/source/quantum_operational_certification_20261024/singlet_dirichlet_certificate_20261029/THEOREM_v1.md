# Model-free present-channel certificate for a high-rate singlet memory
2026-10-29. Root Dirichlet construction, developed here; pending independent review. No novelty claim.

## Interface and theorem
Fix even n≥4, D=2^n, arbitrary chosen product frame V=⊗V_i, and the twisted permutation representation S_ij=V Swap_ij V†. The frame may have been learned from previous data; freeze it before independent validation. Let P be the ENTIRE corresponding spin-zero sector, d0=Catalan(n/2). Pick K=2^floor(log2 d0) and a known isometry E:C^K→P (e.g. previous Dyck/Schur compiler). Let N be ANY CPTP map on the n data qubits, with Kraus K_a. No random-unitary, locality, unitality, excitation-gap or collective-noise model is assumed for N.

Define for every pair
δ_ij=1−Tr[S_ij N†(S_ij)]/D,
q=(1/[2M])Σ_{i<j}δ_ij, M=n(n−1)/2.
Each δ_ij is real and nonnegative, ≤2. Use decoder D_E(X)=E†XE+Tr[(I−EE†)X]|0><0| on C^K. Then the encoded channel Λ=D_E∘N∘Ad_E obeys
1−Fe(Λ) ≤ min{1, (D/(Kn))Σδ_ij}
             = min{1, (D/K)(n−1)q}.
Define C=(D/K)(n−1)=O(n^(5/2)). This is a Bell-loss certificate for a SPECIFIC code/service, not an operator-norm estimate of N or an assertion that all Kraus operators are uniformly near the collective algebra.

## 1. Complete-transposition Dirichlet gap
On the Hilbert space of system matrices with Hilbert–Schmidt inner product, define R(π)X=S_π X S_π† and
L=Σ_{i<j}(I−R((ij))).
Its kernel consists of matrices commuting with every S_π. The orthogonal projection onto this kernel is the group average G(X)=1/n! Σ_π S_π X S_π†. This projection is proof machinery only; no n!-time computation is required by the protocol.

The complete-transposition Laplacian has spectral gap at least n in ANY unitary representation of S_n. Here is the standard character argument, with primary spectrum source below. On the irrep λ⊢n, the class sum of transpositions has eigenvalue
c_λ=Σ_{(r,c)∈λ}(c−r)=1/2 Σ_r λ_r(λ_r−2r+1).
The trivial λ=(n) has c=M. Any nontrivial partition is dominated by (n−1,1), and moving a removable lower-row box to an earlier valid row strictly increases its content sum; therefore c_λ≤c_(n−1,1)=M−n. Consequently L≥n(I−G). Multiplicity of the trivial irrep is handled by G. Negative adjacency eigenvalues do not affect this positive Laplacian bound.

For any matrix A,
||A−G(A)||F²≤(1/n)<A,LA>
=(1/(2n))Σ||[S_ij,A]||F².
Using trace preservation ΣK_a†K_a=I,
Σ_a||[S_ij,K_a]||F²
=2D−2Tr[S_ij Σ_aK_a†S_ijK_a]=2D δ_ij.
Thus Σ_a||K_a−G(K_a)||F²/D≤(1/n)Σδ_ij.

## 2. Why the high-rate code avoids exponential faithful-state loss
Schur–Weyl duality gives G(K_a) in the collective-unitary algebra. Its restriction to the entire spin-zero sector is a scalar α_a, so G(K_a)E=α_a E. This scalar property is crucial: a generic unrelated code need not have it.

Let |Φ_K> be normalized maximally entangled logical/reference input and |Ψ>=(E⊗I)|Φ_K>. Write Δ_a=K_a−G(K_a). For each physical output vector,
(K_a E⊗I)|Φ>=α_a|Ψ>+(Δ_a E⊗I)|Φ>.
The component orthogonal to |Ψ> has squared norm at most ||Δ_a E||F²/K. Since N is trace preserving, the sum of full output squared norms is one. Therefore the physical code-projection Bell loss is bounded by
Σ_a||Δ_a E||F²/K≤(D/K)Σ_a||Δ_a||F²/D.
The fixed-state leakage completion contributes a nonnegative Bell overlap, so the same upper bound holds for 1−Fe(Λ).

Since K>d0/2 and d0~2^n/[sqrt(π)(n/2)^(3/2)], D/K=O(n^(3/2)), not exponential. Rare spectator failures can still catastrophically damage particular untwirled logical states; the theorem does not deny this. They have small weight in the high-dimensional maximally entangled code input.

## 3. Reference-complete service by an actual retired-key logical Pauli twirl
For k=log2K, choose fresh uniform independent 2k-bit key z, apply logical Pauli P_z before E, and P_z† after D_E. Delete/retire the key after decoding, with no later adversarial access. The averaged implemented logical channel is
Λ_tw(ρ)=1/K² Σ_z P_z†Λ(P_zρP_z†)P_z.
The key must be independent of source bath, calibration and input; N must be the same linear channel independent of the key except through its input. Do not claim the bound conditioned on a disclosed key or for a keyed joint output.

The twirl makes the normalized Choi matrix Bell diagonal, preserving its identity-Bell coefficient Fe(Λ). Equivalently Λ_tw=Σ_z p_z Ad_Pz with p_0=Fe(Λ). A maximally entangled input gives half trace distance 1−p_0. Conversely, convexity and half diamond distance ≤1 between any two channels give half diamond distance ≤Σ_{z≠0}p_z. Hence EXACTLY
(1/2)||Λ_tw−id||diamond=1−Fe(Λ)≤Cq.
This is a physical modification of the service, not an inference that untwirled worst-case error equals Bell loss. It uses O(k) logical Pauli gates before/after the code and 2k private random bits per service, plus erasure of the key. Gate/key/privacy costs are real. Unknown-bath cross-service reuse is not licensed by this one-channel result.

## 4. Positive physical symmetry test
Prepare data maximally mixed I_D/D, using independent fair classical bits and computational-basis product preparations, and a fresh isolated ancilla |+>. Choose a pair uniformly. Apply controlled-S_ij (ancilla1 branch), apply N to data only, apply the SAME controlled-S_ij, then measure ancilla X. The minus probability is
q_ij=(1−Tr[S_ij N(S_ij)]/D)/2=δ_ij/2.
The equality Tr[S N(S)]=Tr[S N†(S)] follows from the adjoint pairing. The off-diagonal ancilla block after the sequence is N(S)S/(2D), proving the formula even for NONUNITAL N. Averaging the random pair yields q.

Each trial uses one complete N call, two local controlled twisted-SWAP operations, one isolated ancilla held coherent through N, n product preparations and one ancilla readout. Twisted swap is local on the chosen pair, compiled from known local rotations and SWAP; its controlled version requires actual coherent control (e.g. controlled rotations plus Fredkin decomposition). Random-pair routing is an additional O(n) SWAP overhead on a simple line, unless geometry supplies direct pair access. No source controlled-N, bath reversal, environment tomography or full code execution is required during this test. The ancilla must not couple unintentionally to N/bath. A dephasing/noisy flag does not automatically certify data quality.

Full product tomography is an alternative signed estimator but is not the positive low-error test analyzed here. The latter is a stronger boundary-control interface than the previous ordinary Pauli discovery probes.

## 5. Confidence and actual execution errors
Assume validation trials independently realize the same N with the same reset/preparation interface. Conditional on any frozen learned frame, m random-pair trials are iid Bernoulli(q). If r failures occur, let q_U be the exact one-sided binomial upper confidence limit solving
Σ_{j=0}^r binom(m,j) q_U^j(1−q_U)^(m−j)=β
for r<m (q_U=1 if r=m). Then with probability ≥1−β the twirled service has half diamond error ≤min(1,Cq_U). If no failures occur, q_U=1−β^(1/m)≤log(1/β)/m. Thus zero-defect acceptance at error ε costs m≥C log(1/β)/ε, i.e. O(n^(5/2) ε^(−1) log(1/β)) full-channel calls. Nonzero defects can be accepted only when their confidence upper bound is sufficiently small; no forced acceptance of an arbitrary source is claimed.

If each actual test's minus probability differs from the ideal by at most b_test, use q≤q_U+b_test. Such a bound follows from a separately justified complete test-circuit half-diamond error budget; it cannot be inferred from the witness alone. Add actual service implementation half-diamond error b_service after multiplying the witness uncertainty:
service error≤min(1,C(q_U+b_test)+b_service).
Thus local test calibration bias must be O(ε/C); this stringent precision is a real scaling cost. Approximate frame acquisition itself needs no separate hidden-noise-model bound here: any exactly specified compiled frame defines a candidate code, tested directly. Differences between specified and physical gates must be paid.

For a T-step memory process, N may be the entire reset-to-readout CPTP channel N_T, with arbitrary retained bath memory WITHIN the trial. Then each witness trial costs T primitive source uses and holds the ancilla through the whole horizon. The certificate applies to this tested channel/horizon/interface, not to all future times or adversarial future bath states. Validation samples without the required cross-trial reset are not iid; this theorem makes no stationary extrapolation from them. The separately reviewed fixed-joint-algebra theorem remains the source of uniform-in-time protection.

## 6. Strong conventional baselines and limitations
A full encoded-Bell preparation and Bell projection directly measures Fe with better O(ε^(−1) log1/β) low-error shot count, but holds k protected reference qubits and runs the full compiler/decoder.

A stronger no-reference alternative prepares a random logical Clifford (exact state 2-design) applied to |0>, runs encode→N→decode, reverses the Clifford, and measures all-zero survival. Its average survival is Favg=(K Fe+1)/(K+1). Its positive failure probability directly certifies Bell loss, again without the C=O(n^(5/2)) witness penalty. It needs executing full logical randomized-state synthesis AND the actual encoder/decoder on every validation call. When those controls are already affordable, it is a better statistical comparator. We do not claim superiority over it.

The symmetry witness's specific capability is certifying a candidate high-rate compiled code using only maximally mixed physical data and local controlled-swap boundary operations, before executing the heavy code compiler on every calibration shot. It trades many more shots and stringent ancilla/control calibration for that reduced calibration circuit. Whether this is practical depends on hardware; no advantage measured.

This is a SUFFICIENT certificate, not complete learning or optimal decoding. A channel may be perfect on the chosen singlet code and wildly noncollective outside it, producing a large witness and false rejection. No generic efficient discovery for arbitrary noise is supplied. Pairwise model fitting alone still does not certify the present channel: the new positive full-array autocorrelation test is essential. No historical novelty claim has been established.

## Sources and checks
* Konstantinova–Kravchuk, Spectrum of the Transposition graph, arXiv:2204.03153v1, https://arxiv.org/html/2204.03153 , Theorem1 and partition eigenvalue formula (full source checked 2026-10-29). Complete-graph largest adjacency eigenvalue n(n−1)/2, second n(n−3)/2, hence Laplacian gap n. Our application is its unitary conjugation representation; no star/Aldous conjecture is needed.
* Graydon–Skanes-Norman–Wallman, Designing Stochastic Channels, https://arxiv.org/abs/2201.07156 (2022), primary comparator navigation for twirling and infidelity/diamond equality. The Pauli-specific equality used above is proved here directly, not imported without conventions.
* Existing compiler source: Bacon–Chuang–Harrow, https://arxiv.org/html/quant-ph/0407082v4 ; qubit sequential CG/path construction. Prior reviewed folder unknown_collective_noise_encoder_20261029 supplies the candidate encoder and its control/precision caveats; no old noise promise is imported into this certificate.

`check_v1.py/.json` verifies n=4,6 arbitrary coherent and nonunital channels, a local phase mixture, and rare code reflection. It numerically checks exact Kraus commutator identities, group-average Poincare bound, code Bell-loss bound, completed decoder, actual ancilla interference, and Pauli-twirled Choi diagonality/equality. Group averaging is used only for small-instance tests. No hardware result or large-n gate synthesis is claimed.
