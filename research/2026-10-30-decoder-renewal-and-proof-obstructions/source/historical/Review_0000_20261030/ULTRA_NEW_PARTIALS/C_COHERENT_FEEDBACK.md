# A literal forward-query coherent-feedback cell

30 October2026. C construction after its independent exterior and
single-spin attempts. Root's separately optimized covariant two-query
comb suggested the missing positive-transpose branch. The circuit and
rational receiver here are explicit; root's floating optimal coefficients
are not used as a source oracle or correctness premise.

## 1. Native model and the actual remaining task

N_U(rho)=U(rho tensor I_r/r)U*, for an unknown isometry
U:C^2 tensor C^r -> C^D, D>=2r. Every forward call draws fresh independent
junk. Controls, Bell preparation and quantum storage are known ideal
operations for this theorem. An arbitrary singly encoded payload may be
entangled with an inaccessible reference. No inverse, source environment,
controlled unknown operation, exposed junk flag or quantum switch exists.

The construction below works at throughput one, with two forward queries
per decoded payload. Its exact rank-two fidelity is low, not a useful
near-perfect decoder. It constructs the physical causal mechanism behind
part of the adaptive gain; it does NOT solve the near-linear-r inverse
problem or establish a scaling law by a small-r example. The all-r
source/kernel formula is exact and exposes that next question.

## 2. The known conditional Pauli isometry

Make a Bell pair between a logical qubit M and input A1; send A1 through
N_U to produce physical B1. Hold M,B1. Upon arrival of the encoded payload
B0, let F01 swap the TWO FULL known physical registers B0,B1, and put
P_s=(I+sF01)/2, s=+1,-1. These are known register operations, not a test of
an unknown microscopic junk index.

Let E be a two-qubit register with orthogonal labels I,X,Z,Y. Define real
J=-iY, and the known isometries

  V_s |psi> = a_s J|psi>|Y>_E
                  + b_s sum_(P=I,X,Z) P|psi>|P>_E,
  a_+=11/14, b_+=5/14,
  a_-=1/97,  b_-=56/97.                                  (1)

Both satisfy a_s^2+3b_s^2=1 exactly. Thus

  W=P_+ tensor V_+ +P_- tensor V_-                         (2)

is an isometry on B0,B1,M. Apply W COHERENTLY and send M, now the new
logical input A2, through a second forward N_U call to obtain B2. Keep E
and all three physical registers. Neither the physical SWAP sector nor
the Pauli label is classically measured/discarded.

This has a short literal known-control implementation. Coherently compute
the SWAP sector into a flag using H--controlled-SWAP--H. Prepare E's
four-dimensional amplitude vector(b_s,b_s,b_s,a_s), controlled by that
flag; apply the known Pauli indexed by E to M; UNCOMPUTE the flag with the
inverse SWAP test. The sector is unchanged by all intervening gates, so
this uncomputation is exact before the second query. The two amplitude
vectors are rational unit vectors. A rational Householder completion is
an explicit known four-dimensional unitary for each; compile the entire
controlled known matrix with its relative phases, not separately unknown
global-phase representatives. Whole-register controlled SWAP costs
O(log D) ordinary controlled elementary gates on a specified qubit
register type. No operation is controlled-N_U.

Tracing E WOULD implement a transpose-depolarizing map on M,

  Lambda_s(rho)=(1-u_s)I/2+u_s rho^T,
  u_s=4b_s^2-1,
  u_+=-24/49,  u_-=3135/9409.                             (3)

Its Choi matrix is(1-u_s)I/2+u_s SWAP, positive iff
-1<=u_s<=1/3. Positive transposition approximation is standard, not a new
primitive. Keeping the Stinespring label coherent is essential here:
classically selecting a random Pauli and erasing the label is a DIFFERENT
controller. A conditional Bell-PHASE dilation only gave u_s<=0 and missed
the positive branch. The earlier failed phase cases are retained.

## 3. Exact state of a finite known output register, with no Schur factory

All physical operations so far are permutations, so the unknown U can be
pushed through them. Work temporarily in the logical/junk input frame.
Start with Phi_(T,A0) tensor Phi_(M,A1) and three maximally mixed junk
carriers. T is the untouched Bell reference used only for analysis.

Let v_s be the known vector obtained by applying V_s to M, regarding its
new output as A2. Its reference indices are(T,E), dimension8, and its
logical indices(A0,A1,A2) have dimension8. Define

  v_A=(v_+ +v_-)/2,
  v_B=SWAP_(A0,A1)(v_+ -v_-)/2.                           (4)

In the input frame, W has exactly the two terms v_A tensor I_junk and
v_B tensor SWAP_(junk0,junk1). Every component in(4) is rational; the two
initial Bell amplitudes contribute1/2, not an untracked square root.

For pi in S3, let P_pi permute the logical carriers, let c(pi) be its
cycle count, and put f=(01). The EXACT partial permutation moment on T,E
after the second query is

  M_pi = sum_(s,t in{A,B}) r^[c(f^[s!=t] pi)-3]
          Tr_(A0,A1,A2)(|v_s><v_t| P_pi).                  (5)

This follows by tracing the maximally mixed junk permutation; it does not
assume unknown logical states are Gaussian, diagonal or reset. It holds
for every U and every ambient D>=2r, not just Haar-drawn U.

Here is a finite known physical channel producing exactly the relational
state used by the receiver. Prepare a six-level group register G in a
uniform superposition over S3, controlled-permute B0,B1,B2 by pi, invert
the classical group label, and discard all three physical carriers. The
result, including T for analysis, is

  Omega_(T,E,G)= (1/6)sum_(pi in S3) M_pi tensor L(pi^-1),  (6)

where L is the LEFT regular representation. Indeed the off-diagonal
group entry(g,h) after label inversion is M_(h g^-1)/6. This is a
positive trace-one state because it is the output of the displayed
channel. No unknown support projector, generic large-dimensional Schur
transform or spectrum is supplied. Coherent finite-group permutations
are ordinary representation machinery; the ancilla has only six basis
states for this cell and each controlled permutation uses O(log D) gates.

The final accessible input is E tensor G, dimension24; T is untouched
and inaccessible to the receiver. A fixed known CPTP map24->2 completes
the controller. An unused padded group label is assigned a reset branch
in a physical qubit-register completion, so this remains CPTP even off
the exact six-level support.

## 4. Actual final decoder certificate

`coherent_pauli_feedback.py` implements(1),(4)--(6) using Fraction
arithmetic. It used one floating48-by48 Choi SDP ONLY to propose the
final known24->2 map at r=2. It then rounds the symmetric proposal to
2^-28, adds2^-18 I, verifies strict positivity by EXACT LDL, scales by
131073/131072, and adds the known |0><0| output channel for the positive
trace deficit. That deficit is positive by exact diagonal dominance;
all576 trace-preserving matrix entries are checked as rationals.

`COHERENT_FEEDBACK_DECODER.json` is the resulting rational unnormalized
Choi matrix. Its positive Choi factor gives an ordinary finite known
Stinespring circuit, with no source calls or unknown model in that
factorization. Padding and known-unitary synthesis error must be paid.
The exact objective, not the floating solver value, is

  Fe=55716029295809/123760695281664
      =.4501916312687661.                                 (7)

This is an exact feasible circuit value, not a certified global optimum.
All source-U dependence vanished in the actual physical channel, so(7)
holds for EVERY flat rank-two source, not only on Haar average. No
source, quantum circuit or physical experiment was executed. The actual
computation was rational contraction/certificate arithmetic plus one
small final-decoder proposal. Parent's larger adaptive/parallel floating
comb results are comparisons, not imported rigorous upper certificates.

## 5. A physical all-input conversion using only allowed interventions

Let Lambda_U denote the logical composite of this ENTIRE two-query
controller, including its source queries, on N_U's payload. Every physical
operation is permutation-covariant and the physical carriers are all
discarded, so Lambda_U is ONE common logical channel Lambda independent
of U. This is a stronger statement than equality of Bell fidelities.

Draw a known logical Pauli P uniformly from four choices. Preapply P
before EACH of the two forward source queries, and postapply P* on the
decoded logical qubit. The changed query source is N'=N_U composed AdP,
another flat encoder. The singly encoded payload is exactly
N_U(rho)=N'(P* rho P); no operation on an unknown code is needed. Therefore
the realized composite is

  (1/4)sum_P Ad(P*) composed Lambda composed Ad(P),

a Pauli channel with the SAME Bell fidelity. Its all-input/reference
halfdiamond distance from identity is exactly1-Fe. Thus the twirled
rank-two cell has throughput one and exact certified bound

  halfdiamond <=68044665985855/123760695281664
               =.5498083687312339.                       (8)

This is not a generic fidelity-to-diamond assertion: it uses the exact
flat source family and known INTERVENTIONS on every fresh logical query.
The Pauli seed is INTERNAL and discarded after its correction; an exposed
seed-conditioned output channel is not the averaged twirl. The seed can
be chosen when the first offline programme is prepared. Fresh independent
seeds, junk and programme registers are consumed for later payloads; the
same seed is not silently reused to claim a product-channel guarantee.
It is also not a useful near-perfect decoder. A known gate/error budget
adds by an ordinary CPTP hybrid; an unknown noisy gate threshold or a
drifting source is not inferred. The twirl uses two fair classical bits;
it does not expose a hidden junk flag.

## 6. The SAME controller is an exact all-r family

Neither the rational amplitudes in(1), the group-kernel channel(6), nor
the saved final24->2 decoder depends on r or D. Every step is a physical
CPTP map for ALL r>=1 and D>=2r. This remains true for D=2, where S3 has a
nonfaithful representation: it follows from the explicit controlled-
permutation circuit and the globally CPTP final decoder, not from
extrapolating positivity in one faithful representation.

In(5), c(pi) can only be1,2,3. Hence the exact output and its fidelity
have degree at most two in1/r. `receive_feedback_family.py` derives those
three symbolic coefficients from the SAME saved decoder and circuit,
without another source/model case or solve. It rechecks exact positivity
and all576 trace-preservation entries of that fixed decoder. The result is

  Fe(r)=1/4
       +157722669488099/[495042781126656 r]
       +40484174315045/[247521390563328 r^2].               (9)

The constant coefficient is EXACTLY1/4. The physical Pauli-twirled cell's
all-input/reference halfdiamond error is exactly1-Fe(r). This is a
dimension-independent CONTROLLER FAMILY, not a uniform-quality inverse:
Fe(r) tends to1/4 at large rank. A quantum programme is consumed and new
source calls are still required for each payload. There is no free
classically learned reusable inverse of the unknown U.

For comparison, root's independently derived one-query optimum is
Fe_1(r)=(1+1/r)/4. Equation(9) is strictly larger for every r>=1, but it
uses TWO queries. This does not establish a per-query advantage or an
all-r advantage over the best TWO-query parallel strategy. The retained
rank-two comparison uses root's separate exact all-parallel dual, not a
generalization from a numerical table. Its source/model scope is stated
in C_COMPARISON.md.

## 7. Costs and the next actual scientific gate

Two new N_U calls are consumed per arbitrary payload, plus its original
encoding call if total source use includes that preparation. The first
Bell query can precede the payload, requiring protection of one physical
carrier plus one qubit until arrival; alternatively both calls are online.
The second call is intrinsically ONLINE after the payload interacts with
the first programme. The unknown payload must remain coherent across that
source latency and the known O(log D) controlled-permutation circuit.
The peak physical history is three D-level carriers; E has two qubits
and G needs three padded qubits. The final known decoder has fixed
dimension, independent of D. Known-control compilation/readout/reset and
source holding costs remain physical obligations, not acquired facts.

N1104's fresh-known-probe-to-Choi retry reduction does not apply to query2:
its input is now entangled with retained UNKNOWN physical memory and the
payload. A failed postselected simulation would damage that joint state
and cannot be retried from a known classical specification. The general
linear collision lower and separate iid-Choi quadratic lower remain
unchanged; no contradiction or new general query lower follows.

The construction replaces an abstract comb coefficient by a small native
coherent interaction and a finite receiver. It does not yet turn a
growing number of such cells into a near-perfect inverse at O(r) queries:
discarding old history or the Pauli label changes the channel, and a
failed branch is not a paid restoring draw. The remaining gate is an
all-orders coherent-history recurrence/controller with a proved error
bound and paid source latency. Iterating Bell fidelities as if they were
independent successes, cloning the payload, or assuming an exact Markov
reset would erase that gate rather than solve it.
