# Independent receiving review: random encoder with learned physical decoder

**Decision: ACCEPT the Petz construction and, by explicit composition with the
separately received SDP bridge, its coefficient-one variant.** This receipt binds
the original governing draft together with the finite-seed/encoding-cost addendum.
The exact-design theorem and the bounded-bit physical implementation have different
budgets, stated below.

Reviewed 2026-10-29 by `producer-workspace/review_history_program_bounds`.
Governing source SHA-256:
`feb0656708176fe2ee04ab762e7fc0165894385e0c49f77be250d5cc44e1a2bb`.
Originals were preserved; dependency receipts and source copies are hash-bound.

## 1. Received operational theorem

The source N:D->Dout is a fixed memoryless CPTP map, chosen independently of a fresh
encoder seed, with supplied Kraus-rank bound r. D=2^n, k=2^ell<=D, k>=2. The
controller can prepare and encode logical training states and has the unknown
logical payload **before source encoding**. It has trusted paid endpoint controls
and protected coherent storage. It does not receive a source Kraus list,
Stinespring unitary, complement, inverse, or unknown controlled-source oracle.

Define `A = r sqrt(k/D)`. Under exact uniform Clifford selection, seed-averaged
entanglement infidelity of the learned code is at most

- Petz: `2A+3delta+beta+gamma`;
- received standard SDP variant: `A+2delta+zeta+beta+gamma`.

Apply an independent uniform logical Pauli before the known encoder, its inverse
after logical decoding, and retire the key. For the reduced logical channel the
same quantities bound half-diamond distance to identity, capped at 1. With the
bounded seed sampler, add `eta_seed` to either bound:

`Petz: halfdiamond <= min(1,2A+3delta+beta+gamma+eta_seed)`;

`SDP:  halfdiamond <= min(1,A+2delta+zeta+beta+gamma+eta_seed)`.

Here gamma is the TOTAL implementation budget, including all repeated encoders,
endpoint pads, preparations, compression and physical recovery. The ideal padded
reference channel is exactly Pauli; imperfect physical pads need not leave the
actual channel exactly Pauli, but their charged hybrid error preserves the bound.
All randomness is averaged for the stated reduced-channel target. No per-seed,
per-training-record, released-key, or arbitrary source-memory guarantee is inferred.

## 2. Independent centered second-moment derivation

Let T=N^c be a mathematical complement of output dimension at most r. It is not
an algorithmic oracle. For code columns e_i, let
`J=(id_k tensor T E)(Omega_k)` and `tau=T(P/k)`, P=EE^dagger. Put
`Delta=J-(I_k/k) tensor tau`. Uhlmann supplies a CPTP decoder achieving at least
the squared fidelity of those two states. The root-fidelity/trace inequalities
therefore give `F_opt>=1-||Delta||_1` (the negative lower-bound range is harmless).
The argument allows rectangular N and arbitrary ancillary enlargement of a
mathematical decoding isometry.

Write `a=Tr[T(I_D)^2]`, `b=Tr[N(I_D)^2]`. Define three scalar Haar moments:

`S=(a+b)/(D(D+1))`,
`O=(b-a/D)/(D^2-1)`,
`H=(a-b/D)/(D^2-1)`.

They respectively arise from equal columns, distinct off-diagonal column pairs,
and distinct diagonal column pairs. Swap contraction with a Stinespring isometry
identifies the second channel invariant as b; no equal input/output dimension is
required. Direct expansion gives

`E Tr J^2 = S/k + (k-1) O/k`,
`E Tr tau^2 = S/k + (k-1) H/k`.

Since `||Delta||_2^2=Tr J^2-Tr tau^2/k`, subtraction gives exactly

`E||Delta||_2^2 = (k^2-1)/(k^2(D^2-1)) * (b-a/D)`.

For k<=D, its coefficient of b is at most 1/D^2, so the expression is <=b/D^2.
The environment dimension bounds rank Delta by kr. Jensen and the Schatten
inequality yield `E(1-F_opt)<=sqrt(kr b)/D`.
Each Kraus K_a is a contraction because sum K_a^dagger K_a=I; hence
`N(I)<=r I`, `Tr N(I)=D`, and `b<=rD`. This proves `E(1-F_opt)<=r sqrt(k/D)`.

The scalar squared norm is a quadratic polynomial in P. Explicitly, with
`W_ab=K_a^dagger K_b`, it equals

`sum_ab Tr(P W_ab P W_ba)/k^2
 - sum_ab Tr(P W_ab)Tr(P W_ba)/k^3`.

Thus it is degree (2,2) in U. An exact unitary 2-design suffices for the moment;
Jensen is applied afterward to its finite distribution. One does NOT assume that
the nonlinear optimized fidelity itself is a degree-two polynomial.

The author's diagnostic instead subtracts the fixed marginal T(I/D). Its distinct
moment is `(kD-1)/(kD(D^2-1))*(b-a/D)`, which the independent algebra also verifies.
The code and supporting MOMENT_AND_PRIOR note are correctly labeled; that weaker
fixed-marginal diagnostic is not a numerical proof of the centered formula.

## 3. Established predecessors, not a new random-coding law

[Klesse, quant-ph/0701102v2](https://arxiv.org/pdf/quant-ph/0701102v2), section 4.2,
equations (27)–(28), already gives the Haar-code average bound
`1-sqrt(kr)||N(I/D)||_2`. Its stated notation uses a common system space. The
rectangular extension here is independently justified by the trace/moment algebra
above, rather than attributed verbatim to the paper.

[Dankert–Cleve–Emerson–Livine, quant-ph/0606161v2](https://arxiv.org/pdf/quant-ph/0606161v2),
Theorem 1, directly establishes the uniform Clifford 2-design property.
[Koenig–Smolin, arXiv:1406.2170v1](https://arxiv.org/pdf/1406.2170v1), equation (1),
the integer-index construction, and its circuit-synthesis discussion establish
finite Clifford indexing and polynomial classical/circuit costs. These are
primary algorithm dependencies; no new Clifford design/compiler claim is received.

## 4. Transfer to an actual learned decoder

For a fixed seed, A_U=N E_U has output support inside the span of the at most r
Kraus images of its k-dimensional input, hence rank A_U(I/k)<=kr. The received
low-support theorem therefore applies with d=min(Dout,kr). Its mathematical
common-compression gauge is a separate random variable from the public encoder U;
there is no requirement to know or identify that gauge or the original N.

All training Choi outputs and the later payload must enter **one common joint
compression batch**. Conditional on its mathematical gauge, the training data
have the required IID channel law and are independent of the payload reference.
The earlier received theorem already accounts for this reference-safe identity.
Fresh training normally accompanies each new service payload; this is not a
reusable classical decoder acting on arbitrarily many future original-Dout
outputs. The known encoder circuit description can be reused, but its physical
execution is paid on each source input.

Let f_U=F_opt(A_U). The Petz dependency gives actual fidelity at least
`f_U^2-3delta-beta-gamma_learner` uniformly for each fixed seed. Because
`f_U^2>=1-2(1-f_U)`, averaging gives the claimed factor 2. The distinct accepted
SDP receipt gives `f_U-2delta-zeta-beta-gamma_learner`, so its composition gives
factor 1. No encoder optimization, generic solver execution, or supplied source
matrix is introduced by this argument.

Dependencies actually received and read:

- low-support recovery receipt `cc35fde93df42844fcc49ddc76c83303c8c84439984a8a22b317ceec2acf9b64`;
- uniform common-design compiler receipt `a048f5cd386c519e13cf2a6369c57947197170acd82f3ce31d8654dec6e98ca7`;
- optional standard SDP receipt `78bd023a542622c81c56a8a725c5586989b3e2c801adc850a5b2f6551c13690e`.

The last receipt did not itself accept random-code corollaries. This review
receives the simple composition; it does not independently repeat or enlarge the
SDP proof. The Petz result remains independent of that optional dependency.

## 5. Logical padding and access boundary

For any fixed whole logical training-and-decoding channel C, independent private
logical Pauli conjugation produces
`C_twirl = average_P Ad(P^dagger) C Ad(P)`.
Entanglement fidelity at I/k is invariant under each such conjugation. The twirled
Choi state is diagonal in the orthonormal Pauli-Bell basis. Its identity weight is
F_e, and the other weights sum to 1-F_e. The channel-distance triangle inequality
gives half-diamond <=1-F_e; the maximally entangled input attains it, proving
**equality**. This works for k=2^ell, not only a single qubit.

Padding is on the LOGICAL payload before E_U and before the opaque source. One
cannot silently add it when the only available input is an already-noisy encoded
payload from the earlier decoder-only problem. The key must be independent of
the base learner, not used to change its training rule, and its final register is
retired for the claimed reduced target.

A precise counterexample illustrates the key boundary: for logical
`V=cos(pi/6)I+i sin(pi/6)Z`, F_e=3/4. The retired-key twirl has identity error 1/4;
with the pad key retained, a Bell input already witnesses joint trace distance
1/2. Thus the linear released-key claim is false even for an elementary channel.

## 6. Finite seed and complete resource accounting

The addendum fixes the only receiving clarification requested. The Clifford order
modulo phase is
`G=2^(n^2+2n) product_(j=1)^n(4^j-1)`, with b=ceil(log2 G)=O(n^2).
A b-bit integer is accepted if it is below G, with probability p>1/2. Exact
uncapped rejection is uniform and has expected bit cost b/p<2b, but has no
worst-case finite bit cap. G has an odd factor, so bounded fair bits cannot
realize this uniform law exactly without a failure branch.

Cap at R attempts and choose a fixed fallback encoder on all-rejection. Each valid
integer has success probability `(1-(1-p)^R)/G`; hence the successful seed remains
exactly uniform. The total distribution is within `(1-p)^R<=2^-R` in total
variation of uniform. Seed-dependent physical learner channels remain CPTP, so
this changes reduced half-diamond distance and entanglement fidelity by at most
eta_seed. The cap uses bR bits, with R chosen by an exact integer comparison to
meet the target. This is independent of the already paid design-compiler
randomness inside the decoder.

Propagate `d'=max(4,2^ceil(log2 d))` through ALL tomography budgets and set the
common-design order to N_train(d',...)+1. If Dout<d', use the received direct
Dout=O(d) branch. The accepted uniform compiler supplies one full-reference joint
batch error budget, not independent per-slot error assumptions. Its mathematical
gate/bit cost is polynomial in batch size,d,log Dout,log(1/error), with enormous
constants. It supersedes the earlier fixed-d enumeration step only through its
own separate received construction.

There are N_train+1 source queries and N_train+1 physical O(n^2)-size encoder
executions, plus O(log k) padding gates and 2 log2 k private bits per payload.
A sufficient hybrid allocation has
`gamma >= gamma_learner+(N_train+1)epsilon_encoder+epsilon_prepad+epsilon_postpad`
plus the declared preparation/routing allowances. Dividing a finite total error
budget among a polynomially bounded number of known gates costs only the
corresponding logarithmic precision overhead. Protected output storage is at
least N_train ceil(log2 Dout) qubits, plus references/work/payload/carriers.

For example, to target total error epsilon in (0,1), the Petz branch can require
`D>=16 k r^2/epsilon^2`, then take delta=epsilon/24 and
beta=gamma=eta_seed=epsilon/8. The coding term is at most epsilon/2 and the
remaining terms at most epsilon/2. The SDP branch can instead use
`D>=4 k r^2/epsilon^2`, delta=epsilon/20 and
zeta=beta=gamma=eta_seed=epsilon/10. These are sufficient schedules, not optimized
constants. k remains a dimension: polynomial dependence on k is exponential in
the logical qubit count log2 k. This is not efficient high-rate decoding.

## 7. Independent tests, and what was not executed

The independent program verifies symbolically both second-moment formulas. It
also exactly enumerates the 30 rank-2 two-qubit Clifford code projectors
`(I +/- P)/2`, P nonidentity two-qubit Pauli, proving
`average(P tensor P)=7 I/30+SWAP/15`. Exact rational/complex-rational tests then
check the centered formula on partial trace, rotated nonunital amplitude damping,
random-unitary dephasing, rectangular erasure, and a complex unitary channel.
This is a nontrivial code-orbit test, not a claimed implementation of the full
Clifford sampler.

Twelve independent complex logical channels in dimensions 2,4,8 confirm Pauli
Bell diagonality, fidelity preservation, and equality between the Bell-input
trace lower bound and the Pauli-channel diamond upper bound. Twenty exact group
order/seed-rejection cases verify cap probabilities and conditional uniformity.
Exact scalar checks cover the squared-fidelity averaging step. All tests pass.
The author's five 1000-Haar-sample oracle-model benchmark rows replay identically.

The author benchmark uses unavailable source Kraus matrices to compute an
exact-model Petz decoder. It is correctly labeled as an oracle benchmark, NOT
execution of the opaque learner, native Clifford sampler, SDP solver or full
quantum circuit. No hardware, runtime advantage or practical superiority is
certified by those numbers.

## 8. Essential scope boundaries

For a fixed source tracing out the last qubit of D=2048 and k=r=2, a Clifford
that swaps the logical carrier into that discarded qubit has F_opt=1/4, although
the seed-averaged optimal infidelity bound is 1/16. The claim is not per-code.
If the source is instead allowed to choose
`N_U=Tr_first_qubit o Ad(U^dagger)` after seeing the seed, EVERY code is erased
with rank-two noise. This directly violates the incorrectly applied average
bound, demonstrating that source-before-seed is load-bearing.

No unrestricted source adaptation/memory, noisy untrusted buffers, released-key
joint guarantee, free seed selection/validation, extra-payload reuse, efficient
high-rate code, quantum-capacity theorem, rank-free claim, historical novelty or
competitive hardware advantage is received. Established random coding and
physical/optimized recovery are explicitly acknowledged predecessors.
