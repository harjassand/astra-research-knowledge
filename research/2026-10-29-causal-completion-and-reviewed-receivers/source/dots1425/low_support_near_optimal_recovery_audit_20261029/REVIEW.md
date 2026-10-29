# Independent review: arbitrary low-support physical recovery

2026-10-29. Reviewer `producer-workspace/review_history_program_bounds`.

**ACCEPT the squared-entanglement-fidelity near-optimal recovery theorem at the stated memoryless, low-output-support, coherent-training scope.** Perfect correctability and the mixed-isometry structure are not needed for this extension. The corrected finite tomography/physical-Petz construction and reference-joint compression/compiler receipts remain load-bearing dependencies.

The accepted statement is

`F_e(I_k/k, M_N) >= F_opt(N)^2 - 3delta - beta - gamma`,

where M_N is the entire one-payload recovered channel, including its fresh training queries, joint compression, measurement/feedforward and physical recovery. This is not diamond-near-optimality, approximation of the true source's Petz map, or an unconditional guarantee of recovery close to identity.

## 1. Support factorization is a complete channel identity

Let `S=N(I_k/k)` and P be its support projector. For every input density matrix rho, `rho<=I_k`, hence `N(rho)<=k S` and its output is supported on P. For an arbitrary positive unnormalized input, the same argument uses the additional trace factor. An equivalent direct Kraus proof is stronger in presentation: `S=(1/k)sum_l K_l K_l†` implies `(I-P)K_l=0` for every l. Thus **all** channel Kraus images lie in the support, including for entangled/reference inputs.

Choose any isometry V from C^d into C^D whose image contains P, padding the support when needed. Then `F(X)=V† N(X)V` is CP and trace preserving, and `N=Ad(V) composed with F` as a linear channel identity. Neither V nor F must be accessible to the controller. If a Kraus-rank upper bound s is supplied, one may choose `d=min(D,ks)` because the union of s Kraus images has dimension at most ks. This is the precise reading of the source's shorthand: not every smaller d is automatically a valid support bound.

No requirement `d>=k` is needed. For example a replacement channel may have d=1 while k>1. The compression, h=kd tomography and rectangular Petz construction all remain meaningful; their attainable fidelity will simply reflect irreversible loss.

## 2. Joint compression and conditional statistics still apply

Apply the accepted reference-joint compression identity to the factorization `N=Ad(V) F`, on all training outputs and the one later payload. It yields one common latent U and the small channel `A_U=Ad(U) F`. This does not query V on arbitrary inputs, learn a purification, or create new access to A_U.

Conditional on U, the prepared training Choi programs are IID and independent of the unknown payload/reference. The earlier finite Hoeffding bound, rational trace-preserving repair, positive ridge, strict acceptance test, physical fallback and corrected all-accepted inverse-condition bound therefore apply without modification. They never used perfect correctability. In particular the trained surrogate is faithful by construction even when `F(I/k)` has zero or arbitrarily small eigenvalues.

For a training record t the likelihood `p(t|U)` is payload-independent. Subsequent recovery acts on the small payload channel, and averaging the actual `(U,t)` mixture gives a well-defined CPTP recovered channel M_N. No claim of independent latent frames or high-probability accuracy for every observed t is needed.

## 3. The optimum benchmark is unchanged

Any physical decoder R from D to k restricts to the small CPTP decoder `R composed with Ad(V)`. Conversely any small decoder Q extends physically to D by

`Q_ext(X)=Q(V† X V)+Tr[(I-VV†)X] tau`,

for a fixed output state tau. The two terms form a CPTP channel and agree with Q on every source output. The support measurement/unknown V used in this extension is only a mathematical witness, not an operation supplied to the algorithm. Applying the same reasoning to the known-in-the-proof output unitary U establishes

`F_opt(N)=F_opt(F)=F_opt(A_U)`.

Finite-dimensional CPTP decoder sets are compact and the entanglement-fidelity objective is continuous, so an optimizer exists; alternatively an arbitrarily close competitor would suffice. No optimizer or recovery SDP is executed. For a fixed N, the complete training-assisted procedure itself induces a CPTP map from the payload output to the logical output, since its training state is independent of that payload. Thus comparison with the ordinary physical-decoder optimum is appropriate despite using queries to learn the channel.

## 4. Fidelity transfer and exact scope

On a tomography-good pair `(U,t)`, the learned model Ahat satisfies `halfdiamond(Ahat,A_U)<=delta`. Let `f=F_opt(N)`. The unknown optimal competitor on A_U has entanglement fidelity at least `max(0,f-delta)` on Ahat. The already received Barnum–Knill singleton theorem therefore gives learned Petz fidelity at least `max(0,f-delta)^2` on Ahat. Its Kraus map is physical on the entire small output space, so transfer back to A_U costs at most another delta.

For `0<=delta<=1`,

`max(0,f-delta)^2-delta >= f²-3delta`.

If delta<=f, the difference between the two sides is `delta(2-2f+delta)>=0`. If delta>f, the lower target is nonpositive (and the direct scalar inequality also holds). This proves the per-good-pair bound without assuming f is close to1.

Bad estimation events have total probability at most beta and still produce CPTP outputs. Since entanglement fidelity is a test probability in[0,1], averaging costs at most beta. Full reference-safe implementation error gamma changes that test probability by at most gamma. The claimed global bound follows.

The consequence `1-F_e <=2(1-f)+3delta+beta+gamma` is valid because `1-f²<=2(1-f)`. It is a weaker consequence, not a literal equivalence to the squared-fidelity statement. If f is independently known to be close to1, normalized-Choi inequalities additionally give an identity half-diamond bound

`halfdiamond(M_N,id)<=k sqrt(1-f²+3delta+beta+gamma)`

when the radicand is useful, capped at1. Without such a benchmark promise, the theorem does not undo irreversible damage or assert high recovered fidelity.

**Important metric distinction:** the construction approximates the channel's behavior by a faithful surrogate and uses that surrogate's physical Petz decoder. It does not prove diamond approximation to the original channel's Petz map, whose operator behavior on tiny-support directions can be spectrally sensitive. Its gap-free conclusion concerns recovery quality in entanglement fidelity. Comparisons with spectral-cost bounds for a stronger Petz-map implementation task must preserve that distinction.

## 5. Finite resources and predecessor scope

The base h=kd tomography schedule has a forward-query budget polynomial in k,d,1/delta and log(1/beta), independent of ambient D and unknown spectral gaps. Its corrected all-accepted inverse bound, physical Stinespring synthesis, rational feasibility test and fallback remain required. The received compiler is polynomial in batch size and log D only for fixed d, with explicitly paid d-dependent GT enumeration; no uniform polynomial-in-d gate bound is imported here.

All training outputs/references must remain coherent until the payload arrives; compression is joint and the small payload is protected during learning/compilation. Normally a new payload needs a new joint training batch. No reusable original-D decoder, source-memory/drift robustness, unbudgeted control errors, practical storage advantage, or positive communication rate is established.

This is not a first physical or first forward-channel-only Petz claim. [Utsumi et al.,2509.03619v3, Section2.4.3](https://arxiv.org/html/2509.03619v3) explicitly presents Petz implementation without a supplied source Stinespring unitary. [Yoshida et al.,2512.21260v2](https://arxiv.org/abs/2512.21260v2) presents random dilation constructions and related applications. These predecessors were checked at the cited scope; this receipt does not establish a strict complexity separation or historical novelty over them. The candidate contribution being received mathematically is the intrinsic-output-support compression and regularized learned-recovery composition at its stated quality metric.

## 6. Independent checks

`independent_checks.py` verifies10,201 exact scalar fidelity inequalities; four arbitrary low-support channel factorizations including d<k; physical decoder restriction and off-support extension in both directions; and16 lossy-channel benchmark cases with analytic optima. No SDP is used.

For qubit Pauli channels, twirling a recovery preserves its objective, reducing it to a probability mixture of Pauli corrections; hence `F_opt=max_i p_i`. The exact Petz fidelity is `sum_i p_i²`, and the ridge-learned fidelity is checked against its analytic rational expression. For classical grouping channels `|i><i| -> |f(i)><f(i)|` with d nonempty groups, any decoder has `F_e<=d/k²`, achieved by choosing one input label per group. Tests include d=1 replacement, d<k irreversible grouping, and d=k complete dephasing, all rotated by unknown-output unitaries in the fixtures. Random non-benchmark recoveries are labeled only as witnesses, not numerical global optima.

All analytical and matrix tests pass. The maximum TP residual in the analytic optimum fixtures is about1.58e-15. These are finite diagnostics of the theorem, not hardware execution, certified arbitrary-channel optimization, or a large-batch compression run. The source and all dependent receipts are preserved and hash-bound separately.
