# Independent review: exact activity-query lower bound
31 October 2026. Reviewer: independent internal mathematical review.

## Source and verdict
PASS. I read the complete actual source
graded_reservoir_consequence_audit_20261031/EXACT_ACTIVITY_QUERY_LOWER_BOUND_CANDIDATE.md,
5,305 bytes, SHA-256 dd9648df785e7a22fbdd7ec7452a20f383ae86d6d97d4d6bd87e2b562652abb0,
and independently verified its byte count and hash.

This establishes a worst-case oracle lower bound linear in accumulated activity for the stated family. It does not establish practical advantage, historical novelty, an optimal upper-bound polynomial or a general lower bound against methods given the unknown bits for free.

## 1. Access model and block acquisition
A_x maps |j,b> to |j+1,b xor x_j> for j<N and vanishes at the endpoint. It is a norm-one partial permutation. A reversible cyclic increment on the padded clock, a bit-oracle operation and a known j<N success flag give an exact contraction block with O(1) bit queries. Controlled versions and inverses have the same constant query overhead; standard compute/uncompute can pay any required control construction.

The projector is part of a unitary block construction, not a successful postselection assumption. Dummy clock values can have explicitly known oracle values. The ordinary clock arithmetic does not reveal the unknown bit table. Every bit-dependent preprocessing or compilation query must be included in the total count, as the source explicitly requires.

## 2. Why the physical process is a renewal clock
The private reservoir is specifically HARD-CORE. From a ground-bath clock state |j,b,0>, the Hamiltonian connects only to |j+1,b xor x_j,1>. Its adjoint connects back. A further raising operation on bath state1 vanishes. This two-state isolation would fail for an unrestricted bosonic ladder, and no such extension is claimed.

In that pair the unnormalized amplitudes obey u'=-gv, v'=gu-2lambda v. The jump density is 4lambda v^2 for J=2sqrt(lambda)a. For positive g and lambda, both no-jump amplitudes decay to zero, so eventual absorption probability is one.

Each physical jump leaves the next pure clock/parity state with bath vacuum. The next two-state problem has the same g and lambda, regardless of x. Strong Markov renewal therefore gives independent identically distributed waiting times up to clock N. At N the bath-vacuum state is absorbing.

## 3. Exact mean, with no elimination limit
Integrating the three identities displayed in the source gives
integral v^2=1/(4lambda),
integral uv=1/(2g),
integral u^2=1/(4lambda)+lambda/g^2.
The integrability follows directly from the stable two-by-two amplitude generator. Their sum is the survival integral
m=1/(2lambda)+lambda/g^2=1/(2lambda)+1/Gamma.

Thus E S_N=Nm. Markov's inequality at T=4Nm implies probability at least3/4 of having completed all N emissions. This is an exact finite-rate result, not an adiabatic waiting-time approximation.

Clock N can also be occupied coherently before the last emission. Its associated parity is already the full input parity, so ignoring this contribution only weakens the completion bound. No bath observation is needed by the reduction.

## 4. Success and trace-norm constants
Measure clock and parity. On clock N the parity is correct. On all other outcomes use an independent fair coin. Since clock N has probability at least3/4, exact success is at least7/8 for every input bitstring.

A trace-norm error at most1/4 in the accessible final state changes any measurement probability by at most1/8. Hence the simulator followed by this measurement and fallback computes parity with success at least3/4. The source uses trace norm consistently; no missing factor of two occurs.

## 5. Query reduction
For Q standard bit-oracle queries, output-sign expectation is a multilinear polynomial of degree at most2Q in y_i=(-1)^{x_i}. This holds also for adaptive measurements/randomness after purification or averaging. Success at least3/4 means p(y) product_i y_i>=1/2 pointwise.

Averaging over uniform independent signs forces a nonzero degree-N Fourier coefficient. If degree(p)<N, that coefficient is zero. Therefore Q>=N/2. This is the ordinary polynomial-method parity argument, credited to Beals, Buhrman, Cleve, Mosca and de Wolf; the primary source is https://arxiv.org/abs/quant-ph/9802049 .

Replacing each supplied coupling-block call by its O(1)-query bit-oracle implementation converts any claimed uniform simulator into such a parity algorithm. All other supplied operations are input-independent. Consequently the total worst-case number of coupling/access queries, including acquisition and compilation, is Omega(N).

With lambda>=Gamma,
Gamma T=4N(1+Gamma/(2lambda)) lies in [4N,6N].
Therefore the bound is Omega(Gamma T). The microscopic damping rate may be much larger than Gamma, so this is genuinely an obstruction to removing useful accumulated activity, not a claim that runtime must be linear in damping.

## 6. Exact scope
The construction has one private lossy qubit, O(log N) system clock qubits, one parity bit, H_f=0 and no external interventions. A final-state-only simulation guarantee already suffices; a stronger controlled-process guarantee necessarily includes it.

The result is an oracle lower bound for a growing family, not a computational lower bound for a fixed explicit small matrix. Reading the entire bitstring or reusing previously acquired information must pay that acquisition once; it cannot be declared free to defeat the access-model conclusion.

No match to the compiler's higher polynomial dependence, optimal precision scaling, practical crossover, superiority over every ordinary solver or literature novelty is inferred. The hard-core restriction, constant-error convention and total query accounting are essential to the accepted statement.
