# Quantum physical-frame challenge: completed construction

The root's strict-noise fixed-frame mechanism survives this independent
mechanism assessment at its explicitly scoped abstract interface. I have
not audited the root's moving generator or conferred novelty/hardware status.
The useful additions are a quantitative exact-frame cost obstruction, a
stated-error cost repair, and two exact processes showing why an averaged
noise channel is insufficient physical acquisition.

## Constructed results

1. **Universal physical-frame size, qubits.** Let
   lambda=[1-3/(2c-1)^2]/4. Any fixed list of M physical product vertices
   containing every noisy pure two-qubit output satisfies
   M>=ceil[1/(2lambda)]. A local Cartesian N-by-N frame therefore has
   N>=ceil(sqrt(ceil[1/(2lambda)])).
   A rotated Bell output's partial-transpose minimum gives the constraint;
   one physical product vertex can satisfy it on at most2lambda Haar
   fraction of rotations. The bound allows mixed factors and arbitrary
   non-Cartesian product lists.

2. **Endpoint and input-size scope.** At c0, every vertex covers a Haar-null
   set, giving an independent universal physical-frame obstruction.
   This requires the all-pure-output range, or a pure product initialization
   plus dense control; {I/2 tensor I/2} is otherwise a trivial invariant
   frame. A dyadic c_B just above c0 has an O(B)-bit description but forces
   M=Omega(2^B). At B=32 the exact lower bound exceeds15.4billion vertices.
   This is not a lower bound against arbitrary HMMs, nonphysical vertices,
   continuous/adaptive frames, or entangled-block simulators.

3. **Accuracy-driven repair.** Trace-distance tolerance epsilon replaces
   lambda by lambda+epsilon in the lower bound (when their sum<1/4).
   More constructively, for L local noise uses, set
   Delta=min[s/2,4epsilon/(3L)], s'=s-Delta, c'=(1+1/s')/2.
   Exact Pauli half-diamond distance bounds the reference circuit's output
   error by3LDelta/4<=epsilon. Its rational margin
   lambda'=(1-3s'^2)/4>=min[3/16,epsilon/(2L)] is independent of the tiny
   input gap. A rational fidelity-net tolerance lambda'/2 fits the parent's
   qubit containment condition. The script outputs exact plans, **not**
   frames or measured performance. The samples are exact for the modified
   reference and approximate for the original target.

4. **Noise-output flags.** For every rational c>c0 and eta>0, a five-outcome
   local Pauli instrument erases to exactly Phi_c but has entangled flagged
   branches after an entirely rational entangling gate. No feedback is
   required for the obstruction. With known local Pauli corrections, the
   both-flagged union has probability eta^2 and negative subnormalized
   partial-transpose witness -12eta^2/25. Eta=.01 costs10000 expected
   heralding attempts. Full flags correct every unknown input, which is
   established environment-assisted correction, not a new device.
   The root explicitly excludes these noise-output flags.

5. **Unobserved classical noise memory.** Draw a Pauli once and use it
   twice. Each isolated use has exactly the same Phi_c channel, but the
   two-use unknown-input map is identity. An arbitrary ideal U followed
   by noise, then identity followed by the repeated noise, yields exactly U.
   Cost: two operation calls, a four-valued error label per active qubit,
   a phase clock, and environment retention/reset acquisition. A single
   |0> two-call Z diagnostic distinguishes this model from fresh noise by
   a mean gap greater than2/3 for every c>c0. It can falsify this specific
   memory, not certify unrestricted arbitrary-depth freshness.

6. **Exact sampling cost.** Ordinary LP/Caratheodory sparsity limits one
   two-qudit trace-preserving column to d^4 output vertices, even if the
   complete frame is enormous. Ordinary exact binary-interval sampling
   then needs at most ceil(log2(r-1))+2 expected fair bits for support r,
   with tail Pr[B>k]<=(r-1)2^-k. Non-dyadic probabilities preclude a bounded
   worst-case fair-bit count. The included sampler checks exact probability
   mass through depth64, not empirical Monte Carlo.

Full derivations: [PROOF.md](PROOF.md).
Exact matrix/process/cost results: [RESULTS.json](RESULTS.json).
Serialized rational instrument: [INSTRUMENT.json](INSTRUMENT.json).
Stated-error reference plans: [ACCURACY_RESULTS.json](ACCURACY_RESULTS.json).
Sampler checks: [SAMPLER_RESULTS.json](SAMPLER_RESULTS.json).

## Strong ordinary comparators and decision

Harrow–Nielsen2003 III.2–III.3 already supplies stated-error
separability-preserving circuit simulation, including bounded qudit gates
and16-term qubit decompositions. Lami–Huber2016 Thm7 already supplies the EA
threshold. Okay2026 Def13/Thm16/Lem17/Cor19 already supplies branchwise
convex-preservation-to-stochastic-kernel and adaptive exact Born sampling.
Gregoratti–Werner2002/2003 already characterizes environment-assisted
random-unitary correction. Xuetal2013 already experimentally realizes
correlation revival under a classical random-unitary environment, with a
different physical model. These sources were personally read at the
sections/version scope recorded in SOURCE_RECEIPT.json.

The parent result should therefore stay a fixed local **physical** rational
frame/strict-threshold/interface theorem, with exact computation and sampling
costs. It is not a new generic positive simulator or tractability class.
The two process constructions are decisive boundary witnesses; their core
physical principles are established prior.

The next consequential transfer is an acquired conditional noise instrument
and multi-time error budget, together with a full-cycle implementation
comparison against an equally informed adaptive separable-state sampler.
An isolated average noise fit, a vertex count, or a kernel identity cannot
supply that acquisition or an advantage. No such physical/full-cycle
advantage was achieved here.

All mathematical code uses stdlib Fraction/isqrt and small matrices.
The four unknown-input process cases completed in approximately0.27seconds.
No large frame was allocated. All three scripts passed; all original frozen
research folders remain untouched. These new derivations await independent
review; this report does not mark them audited.
