# Physical recovery of unknown mixed encodings after joint dimension compression

2026-10-29. Root construction, independent receiving review pending. This uses established Schur compression and Barnum--Knill reversal as machinery. Historical novelty and a matched lower bound for the complete control model are not established.

## Question and access
An opaque forward CPTP encoder has form N(rho)=V(rho tensor sigma)V†, where the logical input has dimension k, sigma is an UNKNOWN density matrix of dimension at most r (zero eigenvalues allowed), and V embeds a d=kr dimensional space into a known ambient D-dimensional register, D>=d. The input/output registers and trusted known controls are accessible; neither V, sigma, an environment, a source inverse nor a Stinespring unitary is supplied. Calls are memoryless with the same V,sigma. We seek a physical decoder for a later independently encoded unknown payload, including its arbitrary reference.

All source outputs used for training may be stored coherently. This is a substantial paid quantum-memory interface: N training outputs cost at least N logD storage qubits before compression. The decoder may jointly process training and the later payload. It is not a classical-record-only learner or a theorem for arbitrary causal source memory.

## 1. One joint compression, not unrelated per-copy frames
Prepare N normalized Choi programs by sending halves of k-dimensional maximally entangled pairs through N. Retain their references. When N(rho) later arrives, apply the known joint compression C_(D to d)^(N+1) to ALL output registers together, leaving references untouched.

The governing predecessor is Yoshida--Soeda--Murao, Universal construction of decoders from encoding black boxes, arXiv2110.00258, Lemma4/Eqs22--23 (version must be pinned in receiving source receipt). Its CPTP identity, not a product-input statement, is
 C(V^tensor n X V†tensor n)=integral U^tensor n X U†tensor n dU,
for every joint X on d^n and every external reference. It discards the U(D) Schur irrep, retains the symmetric-group irrep, replaces the former with the maximally mixed U(d) irrep and inverses the small-d Schur transform. On the promise only partitions with<=d rows occur; a CPTP default defines other branches.

Apply this identity to the unknown mixed junk inputs. The complete resulting state equals the ensemble obtained by choosing ONE Haar U in U(d) and preparing N independent Choi programs of A_U(rho)=U(rho tensor sigma)U† together with A_U(rho) for the payload. This is a mathematical latent-variable representation; the controller is not handed U and does not generate new queries to A_U. Applying independent compression to separate records would destroy this common-frame correlation and would not justify the construction.

## 2. Elementary finite tomography in the small space
Let h=kd. Measure the normalized Choi state J_U using h² settings: h diagonal projectors, and real/imaginary two-level off-diagonal observables for each unordered pair. Each matrix-entry estimator (off-diagonal means divided by2) has outcome interval length1. With m copies per setting, N=h²m, a union bound gives all real/imaginary entry errors<=e with failure probability<=beta if
 m>=log(2h²/beta)/(2e²).
The raw Hermitian estimate A has operator error<=2he. Affinely repair its trace-preserving marginal:
 B=A-[Tr_output(A)-I_k/k] tensor I_d/d.
The true Choi marginal is I_k/k, and partial-trace norm contraction with dimension factor gives ||B-J_U||op<=a=4he. B has trace1 and the exact correct marginal, but need not be positive.

Define the explicitly faithful Choi matrix
 C=(B+2a I_h)/(1+2ha).
Then C>=a I_h/(1+2ha), has trace1 and marginal I_k/k, hence defines a physical CPTP small-space channel Ahat. Further,
 ||C-J_U||1<=5ha,
 (1/2)||Ahat-A_U||diamond<= (k/2)||C-J_U||1<=10 k h² e=:delta.
These are deliberately conservative bounds. The repair and ridge remove any need for a lower bound on a nonzero eigenvalue of the UNKNOWN sigma. On tomography failure the same formula may not be PSD; the actual implementation checks the exact rational matrix inequality C>=a I_h/[2(1+2ha)] and the exact affine marginal, substituting the completely depolarizing CPTP channel if needed. On the good event the stronger displayed inequality guarantees passage. Use an upward-rational confidence radius and rational matrix arithmetic; exact LDL/principal-minor certification or outward-enclosed eigenvalues suffice. This also guarantees a paid inverse-condition bound on every accepted estimate, including rare statistical failures. A floating eigenvalue sign alone is not a certificate.

## 3. Actual Petz operation from a learned classical matrix
Compute Kraus matrices K_l of Ahat from its known positive Choi matrix. Put S=Ahat(I_k/k)>0 and implement the ordinary CPTP recovery with Kraus operators
 L_l=(1/sqrt k) K_l† S^(-1/2).
Indeed sum_l L_l†L_l=I_d. This is an actual Stinespring/measurement-and-discard quantum operation, NOT a virtual expectation-value estimator. The adjoints here are adjoints of CLASSICALLY COMPUTED small matrices, not an oracle for the original unknown N†. The ridge gives S>=k a I_d/(1+2ha), so inverse conditioning is explicitly bounded by chosen finite precision rather than the unknown junk spectrum. A finite known dilation and synthesis error must be charged.

For every latent U, A_U has a perfect mathematical recovery Tr_junk(U† · U). It need not be known to the algorithm. Its entanglement fidelity on Ahat is>=1-delta. Barnum--Knill, arXivquant-ph/0004088v2 (18Jan2026), Theorem3/Eq13 with the single-state ensemble{I_k/k}, gives the above transpose/Petz recovery fidelity on Ahat at least(1-delta)^2. The singleton automatically meets the commuting-ensemble condition. Contractivity then implies its actual entanglement fidelity on A_U is at least1-3delta.

The standard normalized-Choi bound therefore gives actual half-diamond recovery error at most k sqrt(3delta), uniformly in U on the tomography-good event. Averaging the failed estimation event contributes at mostbeta. If the full joint compression/compiler/decoder synthesis has half-diamond errorgamma, the final physical decoded channel obeys
 (1/2)||decoded-id_k||diamond <= k sqrt(3delta)+beta+gamma.
Global optimizer optimality is entirely unnecessary. There is no recovery SDP in this construction.

## 4. Resources and what is uniform
For desired epsilon choose, for example, delta=epsilon²/(12k²), beta=epsilon/4 and gamma=epsilon/4. The bound is then<=epsilon. Set e=delta/(10kh²), and use the integer m above. Training queries are explicitly
 N=h² ceil[50 k² h^4 log(2h²/beta)/delta²].
One additional source use encodes the payload. This very loose polynomial in k,r,1/epsilon is independent of D and of min_nonzero_eigenvalue(sigma). It is not a useful practical cost claim.

Large-D compression must carry its actual control implementation. A corrected high-dimensional Schur compiler (arXiv2509.22640), or the controlled-permutation/symmetric-group-Fourier multiplicity channel, supplies only poly(logD) dependence. Preparing the small-d irrep maximally mixed state cannot be treated as a free oracle. For FIXED k,r, direct finite GT-pattern enumeration has overhead at most(N+2)^{d(d-1)/2}; combined with known small-d Schur circuits this is polynomial in N and logD, with exponent depending on d. A uniform polynomial-in-r gate claim is not made without a separate efficient preparation theorem. Records, references, padding/routing, classical matrix processing, and the protected compressed payload during tomography/decoder preparation are paid.

## 5. Evidence and strongest alternatives
check_physical_petz.py executes finite-outcome tomography by multinomial sampling and constructs the actual CPTP Petz Kraus operation for the SMALL compressed k2,r2 model. It checks TP, actual entanglement fidelity, the Barnum--Knill competitor inequality and distance bound, including junk eigenvalue10^-8. It does NOT execute the giant joint large-D compression or a physical device. Its conservative ridge causes poor low-budget performance; no small-budget advantage is claimed.

Pure-isometry universal inversion is already known, and the joint compression identity is borrowed explicitly. The proposed transfer is to unknown mixed correctable encodings, with a gap-free physical learned recovery in the small latent space. A public-flag independent-Weyl-key mixed encoder gives a strong rank-dependent acquisition lower bound; no r-independent extension is possible. A classical learner given only measured large-D training records, and an equally equipped quantum learner using the same compression, are different comparators. No generic environment-free recovery exclusivity, unconditional capacity or fault-tolerance claim follows.

The promise already supplies existence of a correctable logical subsystem but NOT its decoder, frame, junk spectrum or an accessible purification. The construction aims to acquire the missing decoder. Its usefulness outside exact mixed-isometry structure, physical quantum-memory cost, best rank dependence and historical novelty remain open.

