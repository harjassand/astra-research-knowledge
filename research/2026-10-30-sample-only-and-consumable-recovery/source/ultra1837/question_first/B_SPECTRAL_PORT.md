# A paid robust finite-support port for an opaque quantum channel

30October2026. B's positive construction for the question-first pair.
C owns learned approximate recovery/qualification and the uniform small-space
compiler; root independently derives the agnostic competitor principle.
This file proves the source-copy spectral port. No quantum source/gate
execution or practical advantage is claimed.

## 1. Question, inputs and output

Let N be one fixed memoryless CPTP map from known k-dimensional logical
inputs to a known D-dimensional output carrier. Only FORWARD calls are
available, including entangled inputs, and trusted known controls on the
carriers. The controller receives no N-adjoint, isometry, environment,
purification, state matrix, spectrum, eigenbasis or exact-support oracle.
It can acquire independent copies of `A=N(I_k/k)` by actual forward calls.

Given rational `0<a<=1/8`, `0<beta_gap<=1/2`, `0<zeta<=1/2`, the port
chooses ONE finite random rational threshold t and implements an
always-defined CPTP filter approximating

`F_t(rho)=Pi_t N(rho) Pi_t
          direct_sum Tr[(I-Pi_t)N(rho)] |fail><fail|`,
`Pi_t=1_[t,infinity)(A)`.                              (1)

The failure flag is a known orthogonal state. A physical carrier is a
flag qubit plus the D-level output; on failure reset the data register.
The pass branch is NOT dephased in A's eigenbasis.

For every selected t, even bad ones, the ideal F_t has a COMMON support
of rank at most `1/a+1`, independent of the input state, its reference,
and the number of later calls. With probability at least1-beta_gap/4,
the returned finite circuit has FULL diamond distance at most zeta from
F_t on arbitrary source/reference inputs. The circuit and output branch
are physically defined on bad thresholds too; no per-record claim that
the threshold is spectrally good is made.

The same threshold is reused throughout one training/payload batch.
It is not redrawn independently for separate source outputs. The rank
bound is a mathematical property of one actual channel F_t; it is not
an exact-rank assumption on N's noisy outputs.

## 2. No spectral-gap oracle: a finite random threshold

Choose a power of two L satisfying

`8/(a beta_gap)<=L<16/(a beta_gap)`,
`h=a/L`, `g=h/4`, `t_j=a+(j+1/2)h`, j=0,...,L-1.       (2)

Draw j uniformly using exactly log2(L) fresh fair bits. Each t_j is
rational and lies in[a,2a]. The intervals(t_j-g,t_j+g) are disjoint.
Only eigenvalues of A at least a-g>=a/2 can fall in them; there are at
most2/a such eigenvalues, counting multiplicities, since Tr A=1.
Each eigenvalue spoils at most one grid point. Therefore

`Pr[dist(t_j,spec A)<g]<=2/(aL)<=beta_gap/4`.           (3)

Endpoint equality at distance g is allowed. On every remaining grid
point, the whole spectrum is g-separated from the threshold. Also

`g=a/(4L)>beta_gap a^2/64`.                            (4)

This is a distributional guarantee for one finite randomized processor,
not an assumed continuous random number or an eigenvalue observation.

## 3. Dimension-independent controlled copy simulation

Let c be a control qubit, T the target output carrier, and B one fresh
copy of A. Put `K=|1><1|_c tensor SWAP_(T,B)` and
`H=|1><1|_c tensor A_T`. One step of duration u is the physical channel

`Psi_u(X)=Tr_B[e^(-iuK)(X tensor A)e^(iuK)]`.

At u=0 this and `U_u(X)=e^(-iuH)X e^(iuH)` agree. Their first
derivatives also agree, including off-diagonal CONTROL blocks and every
external reference, by the two swap-trace identities. Each conjugation
superoperator's second derivative has diamond norm at most4:
`||ad_K||_diamond<=2||K||<=2`, and similarly for H. Tensoring a fixed
state and tracing it out are CPTP maps of diamond norm1.

The integral Taylor remainder, using unitary-channel norm1 at EVERY real
time, thus gives the non-asymptotic bound

`||Psi_u-U_u||_diamond<=4u^2`.                         (5)

There is no unspecified O(u^3) remainder or exponential-in-time estimate.
Using m fresh A copies at step u=T/m and telescoping gives

`||Psi_(T/m)^m-U_T||_diamond<=4T^2/m`.                 (6)

It works for positive and negative T and controlled evolutions. Every
copy consumes one forward source call on I/k. The copies are not an
accessible purification and are discarded after use.

This is the ordinary sample-based Hamiltonian-simulation/DME mechanism,
not a new simulation claim. Kimmel etal.1608.00281 AppendixC/Theorem20
explicitly treats controlled DME. Go etal.2412.02134v3 identifies a gap in
the older asymptotic upper-bound argument and gives non-asymptotic
diamond bounds. Equations(5)-(6) are included to pay this exact controlled
primitive without relying on that old remainder assertion.

## 4. Coherent thresholding, not an eigenvalue measurement

Use phase estimation on `U=exp(pi i A)`, whose normalized eigenphases
are lambda/2 in[0,1/2]. Choose a power of two P=2^m with

`P>=256/g`, `P<512/g`.                                (7)

Interpret a phase code y/P in[-1/4,3/4) by subtracting1 when y/P>=3/4.
The estimate of lambda is twice that number. Comparing it with rational
t is finite integer arithmetic. There is no pi-dependent comparison.

The elementary phase-estimation kernel obeys

`Pr[y]<=1/[4P^2 dist_circle(lambda/2,y/P)^2]`.

The lattice tail beyond normalized error g/8 has probability<1/16:
P(g/8)>=32, and bounding at most four grid points in every unit annulus
gives `sum_(j>=31)1/j^2<=1/30<1/16`. If this error does not occur, the
threshold classification is correct at every g-separated eigenvalue.

Repeat the coherent phase-estimation circuit r times into distinct phase
registers, where r is an odd integer with

`2^(-r)<=zeta^2/128`.                                 (8)

For one eigenvector, the virtual measured codes are independent, and a
majority of wrong classification bits has probability at most
`2^r(1/16)^(r/2)=2^(-r)`. Compute their majority into ONE binary flag,
then UNCOMPUTE EVERY phase-estimation register before measuring the flag.
Discard only the (almost reset) work and use that binary pass/fail flag.

For each eigenvector, the resulting ideal finite-QPE isometry differs
from the exact flag isometry by norm at most sqrt(2*2^-r). Orthogonality
of data eigenvectors makes this an operator-norm bound for arbitrary
superpositions and arbitrary references. Its FULL channel diamond error
is at most `2sqrt(2*2^-r)<=zeta/4`.

Measuring/discarding the full phase record would destroy retained
coherences and would NOT implement(1). Coherent flagging and uncomputation
are load-bearing. The later failure reset is an ordinary CPTP map, so
it cannot increase this diamond error.

## 5. Literal source-copy and gate costs

Forward plus inverse QPE uses2rm controlled evolution calls. A call of
index j has absolute time `T_j=pi 2^j`, j=0,...,m-1, occurring2r times.
Implement it with

`n_j=ceil[384 r(P-1)2^j/zeta]` fresh copies of A.        (9)

Since pi^2<16, (6) gives that call FULL diamond error at most
`zeta 2^j/[6r(P-1)]`. Summing every forward/inverse call gives at most
zeta/3. The total number of A copies per filter is bounded by

`C_filter<=2rm+768 r^2(P-1)^2/zeta`.                  (10)

This is polynomial in1/a,1/beta_gap,1/zeta and their logarithms. It is
independent of D as a SOURCE-CALL count, not as a physical-storage cost.

A controlled partial swap is an elementary reflection exponential:
compute the eigenvalue of the global register-SWAP into an ancilla,
apply its one-qubit phase rotation, and uncompute. Global SWAP uses
O(log D) elementary controlled swaps on a padded register. Negative
times use the same circuit with opposite angle. All rotations and QFT
phases have computable finite specifications. Approximate the known
finite circuit with total FULL diamond synthesis error<=zeta/3; its gate
count is polynomial in log D, C_filter, rm, the input bit length and
log(1/zeta). This is a trusted circuit-control assumption, not a local
spatial hardware implementation.

The remaining zeta/12 pays finite preparation of I/k over ALL program
copies. Let `Cmax=ceil[2rm+768r^2(P-1)^2/zeta]`. To generate one label,
draw ceil(log2 k) fair bits and accept values<k. Cap this at hprep trials,
then output label0 on failure. Choose the finite integer hprep so

`2^(1-hprep)<=zeta/(12 Cmax)`.                         (10a)

The chance of exhausting the cap is at most2^-hprep. The resulting
logical mixed input has FULL trace distance at most2^(1-hprep) from I/k;
N cannot increase that distance. Hybrid substitution over at most Cmax
A-program copies therefore costs at most zeta/12 PER filter, not a
free preparation error per copy. Across Q filters it costs at most
Q zeta/12, and the same rule includes any separately added validation
uses. Each label uses a deterministic finite number of fair-word
draws, but exactly one source call; no source trial is spent on rejected
classical integers. Gate/work cost is polynomial in hprep and log k.
The complete full-diamond budget is now
`zeta/4+zeta/3+zeta/3+zeta/12=zeta`.

Known zero ancillas and Clifford preparations are exact in the ideal
circuit model; other trusted preparation errors must be divided over
their complete declared use count as well.
An error in the source's ACTUAL N is not an implementation error here:
N is the opaque channel being learned. Source drift/memory between calls
would violate the model and is not repaired by these estimates.

## 6. Effective rank and loss, without exact support

Let A have eigenvalues in decreasing order. Suppose only that

`sum_(j>d0)lambda_j(A)<=tau`.                         (11)

For ANY threshold from(2), its mean rejection probability is

`t_loss=Tr[(I-Pi_t)A]<=tau+2d0 a`.                    (12)

The first d0 discarded eigenvalues each weigh at most2a; the rest sum
to at most tau. This is elementary KyFan bookkeeping, not a spectral-gap
or ground-state approximation. The port is defined without this promise;
the promise only supplies a useful loss estimate.

For any logical input/reference state, its output marginal satisfies
`N(rho_logical)<=k A`, since rho_logical<=I_k. Consequently projection
failure is at most `k t_loss`, and gentle projection followed by a flag
provides the conservative arbitrary-reference FULL diamond bound

`||F_t-N||_diamond<=2sqrt(k t_loss)+k t_loss`          (13)

after embedding N into the pass carrier. This bound is capped by2. C
and root derive a stronger Bell-fidelity recovery bound using average
loss directly, so(13) is a control, not the preferred decoder noise floor.

If N is half-diamond eta-close to a rank-d0 mixed-isometry source N0,
then(11) holds with tau<=eta: use the support projector of N0(I/k) and
the variational trace-distance bound. The current broader operation can
instead assume effective rank and approximate recoverability separately;
it does not require any exact N0. Root owns that agnostic theorem.

## 7. Why training noise does not cost Q times eta

Let Q be the finite total number of filtered training/payload uses in a
batch. Conditional on ONE selected threshold, F_t is an actual fixed
CPTP channel with support rank<=1/a+1. Joint reference-preserving Schur
compression applies to this F_t itself, with a mathematically unknown
isometry padding its common support. It does not compare its Q training
programs to ideal programs of N0.

Choose zeta<=Gamma/Q for the filter implementation. Any complete causal
composition of those Q filters differs from the ideal F_t composition
in FULL diamond norm by at most Gamma on good thresholds. The random
bad-threshold contribution is at most2(beta_gap/4). All averaged branches
are CPTP. Thus physical source noise remains inside the learned target
F_t, while only the chosen numerical IMPLEMENTATION precision costs Q.
No bad eigenvalue event is silently postselected away.

Total source calls for this port are at most
`Q(1+C_filter)` plus any separately declared loss-validation trials.
With zeta=Gamma/Q, the dominant dependence is quadratic in Q, polynomial
in1/Gamma and1/g, and logarithmic in synthesis precision. Samples are
fresh for every partial-swap step. Protected storage still includes all
training/payload output carriers, O(Q log(2D)) qubits plus logical
references and compression work. A program sample can be streamed and
discarded one at a time; no claim of an ambient-free classical memory is
made. This is one-batch service, not a reusable streaming decoder.

## 8. Optional acquisition of the actual loss

The ideal t_loss is directly the binary failure probability when filtering
A. Conditional on a good threshold, an actual implemented-filter failure
mean differs by at most zeta/2. For fresh independent validation copies,
ordinary Hoeffding with

`V>=log(2/beta_val)/(2nu^2)`

therefore gives `t_loss<=hat_t+nu+zeta/2` except with probability beta_val.
Each validation trial pays one A preparation AND its own C_filter copies.
The chosen total-call and implementation budgets must include V before
launching the experiment; there is no free loss-estimation oracle.
This is an ideal-source/circuit confidence statement, not executed data.

## 9. Imports and current limits

Controlled copy simulation and QPE are established mechanisms; see the
primary arXiv1608.00281 AppendixC/Theorem20, and the non-asymptotic update
arXiv2412.02134v3. No new general DME algorithm is claimed. The retained
joint-compression incumbent is N1291 at pinned Git revision
85048ae0abfe1c1ac932afb7d233993c3553df2a; its full governing proof and
completed review were read after the first question/mechanism was formed.
Its exact mixed-isometry condition is replaced here by an actual filtered
channel, but its fixed-rank GT enumeration cannot be treated as uniformly
polynomial when1/a grows. C and root pay that uniform-port issue separately.

This file does not prove the learned decoder theorem by itself, execute
the quantum processor, acquire a physical source/noise/calibration, prove
optimal costs, or establish historical novelty. It proves the specific
missing source-copy/common-support interface with finite resources.
