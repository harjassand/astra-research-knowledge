# Known bounded-history stochastic programs: a concrete acquired interface

31 October 2026. Concrete corollary candidate receiving the reviewed pure-return compiler. This is simulation of a KNOWN program, not learning an unknown source, a practical speedup claim, or a claim of novelty.

## 1. Exact forward convention and acquired channel

Let n>=1. Histories x=(x_1,...,x_n) are ordered OLDEST TO NEWEST. At each event of a rate-lambda Poisson clock, discard x_1, shift left, and append a fresh fair bit b:

    x -> (x_2,...,x_n,b).

Define the quantum channel by the Stinespring isometry

    W_hist |x_1,...,x_n>
      = |x_1>_environment tensor |x_2,...,x_n> tensor |+>.

This is an actual circuit: prepare one fresh |+>, permute the n+1 wires so the discarded bit enters the private environment, and retain the new n-bit source. An O(n)-SWAP implementation and its controlled inverse suffice; wire relabeling may reduce costs but is not required. No old bit is irreversibly erased. All 2^n binary encodings are valid.

For a diagonal observable D_f=sum_x f(x)|x><x|,

    W_hist^dagger(I tensor D_f)W_hist
      = diag_x [(1/2)sum_(b=0,1)f(x_2,...,x_n,b)].

Thus the diagonal Heisenberg restriction is EXACTLY the stated forward shift/drop-oldest/append-fair transition. It is not silently identified with the opposite shift or the time reversal of an unrelated random-map convention.

The fixed pure source is psi_hist=|+>^tensor n and the fixed environment vector is c_hist=|+>. They cost n and one Hadamards. Reflection about psi_hist is implemented by Hadamards, a computational all-zero phase reflection, and inverse Hadamards, with polynomial/O(n) elementary logical cost under standard ancillary conventions.

After n applications, every old source bit has been transferred to an environment:

    Phi_hist^n(rho)=Tr(rho)|psi_hist><psi_hist|.

This identity is completely positive and remains true with an arbitrary retained reference. Therefore (Phi_hist^dagger)^n Q=0. The acquired return horizon is m=n, with no mixing estimate, stationary amplitude oracle or 2^n state table. The overlap A_hist=(<+| tensor I)W_hist satisfies A_hist^n=P_hist, giving the matching power certificate exactly.

## 2. Acquired nonlinear output and centering

For every history x let B_x be a Hermitian system operator. The input must supply an ACTUAL reversible controlled block-encoding circuit for

    B_hist=sum_x |x><x| tensor B_x,

with known normalization b and real implementation cost. A classical program that merely prints matrix entries does not automatically supply this interface. Known polynomial-size Boolean/arithmetic/gate-selection programs do qualify when their reversible evaluation and the selected operator implementation are explicitly paid. No table of all 2^n B_x is needed.

If the uniform mean 2^(-n)sum_x B_x is known to vanish, this is already centered. Otherwise mean subtraction is NOT free. A separate centered physical model adds one sign bit sigma, refreshed independently fair at the SAME Poisson events. Set

    Phi=Reset_|+> on sign tensor Phi_hist,
    psi=|+>_sign tensor psi_hist,
    K=Z_sign tensor B_hist.

The event is (sigma,x)->(sigma',x_2,...,x_n,b), where sigma',b are independent fair bits. This is a different specified model, not a faithful centering of arbitrary unsigned noise. It has exact PKP=0 because <+|Z|+>=0. The sign reset is acquired by transferring the old sign to a private environment and inserting |+>. There are n+1 source qubits and two fresh event-output qubits; the return identity Phi^n=Reset_psi and m=n remain exact. The environment coefficient state is |+>|+>, with no likelihood/partition-function operation.

## 3. A fully explicit noncommuting benchmark with H_sys=0

Let f,g:{0,1}^n->{0,1} be supplied polynomial-size reversible Boolean circuits and use a single system qubit. Define

    B_x=(b/sqrt(2))[(-1)^f(x) X+(-1)^g(x) Z].

Each B_x/b is a Hermitian unitary. Its normalization-b encoding is directly acquired: conjugate the fixed Hadamard (X+Z)/sqrt(2) by Z^f X^g, and uncompute f,g. This costs the actual two Boolean computations, their inverses and a constant number of selected single-qubit gates. Different history values need not commute. For example f(x)=x_1 and g(x)=0 gives two noncommuting values.

Take H_sys=0 and the explicit refreshed-sign model. This avoids attributing pre-existing difficult closed-system evolution to the source compiler. The example does not prove classical hardness: simple f,g can have much smaller ordinary representations, and no lower bound is claimed for arbitrary compressed classical methods.

## 4. Received capability and all costs

From the stationary source preparation psi, the reviewed base receiver applies with m=n. Its exact diagonal-algebra argument gives the entire accessible system process of the stated classical history/sign program under prescribed system instruments, arbitrary retained references and their output records. The source and artificial dark-emission records stay private; intermediate source memory is retained rather than reset.

The overhead is polynomial in

    n, 1+b^2T+alpha0 T+p, input/register bit lengths,
    log(2+lambda T), log(1/epsilon),

with actual history-output, source, reflection, H_sys and control implementation costs paid. It is not polynomial in 2^n or inverse stationary probability. The physical source's finite-rate corrections are retained; no white-noise or instantaneous-reset limit is substituted. Observable estimation, tomography and repeated execution costs are additional and may introduce inverse-accuracy dependence even though channel-compilation precision costs are logarithmic.

Source: `PURE_RETURN_FULL_FINITE_BIT_RECEIVING.md`, SHA256 `1a097458af52e4b89746b2f5e38e8ba4ea9f8a835db731daef39b8e9ea71e032`; whole independent review SHA256 `62b766cb45cd243c2e0c75402a8f91aa311c940436d2d2c739b4d3e2b705962f`. The independently reviewed grouped-Poisson operator kernel is a subordinate acquired operation, not a separate physical-model assumption.

The separate arbitrary-source/joint-control addendum has now passed whole review: final source SHA256 `39cfffcb2c38bf13da46a380760a994787caada7ecc99f43cc93e6953fc95069`, independent receipt SHA256 `3d48ca120041a8a0dd37da86b5b5a08c40e9d16b10fa643e29e4c4e31ca798ef`. Its larger cap, positive normalization padding and both-branch fixed-window schedule are binding when used. It permits the full quantum-source task and, with the additional algebra check below, meaningful classical label observations. It does not supply public path access. The construction is limited to programs whose state really is the last n iid bits (and explicit sign refresh); an arbitrary n-bit state machine need not reset in n steps.

### Prescribed public label snapshots and feedback

Let D be the algebra of system-valued source-diagonal operators, sum_x |x><x| tensor O_x, including the sign label if present. The adjoint source channel preserves D by Section 1, and the commutator with source-diagonal K and system-only H0 preserves D. Therefore the adjoint semigroup restricted to D is precisely the corresponding classical-history/system evolution.

At a prescribed time, a projective source LABEL measurement and its retained classical record also preserves this algebra in the Heisenberg picture. So do classical stochastic label updates and label-dependent system instruments, provided the FULL outcome-retaining instrument has this adjoint preservation property. Preserving only the unconditional channel while exposing an arbitrary coherence-sensitive outcome is not enough. Backward composition of the restricted semigroups and these instruments proves equality of their entire accessible joint output law, not just a single-time marginal.

Thus up to p prescribed source snapshots and such feedback operations may be PUBLIC, with their actual implementation/record costs and the enlarged count budget paid. The internal dark-emission color, time, component and seed records remain PRIVATE: they are not the physical source-event path. Arbitrary coherent source interventions remain legitimate only as the separately defined quantum-source task, not as the same classical noise model.

A nonstationary initial classical history law can be acquired by sampling its actual known sampler and preparing the resulting computational basis state. There is no need to prepare sqrt(pi_0) amplitudes. A correlated classical-history/system initial ensemble is likewise allowed if its joint sampling/conditional system preparation is acquired and paid. The source need not physically start in psi; psi is still needed as an efficiently known reflection state inside the compiler.

The reviewed addendum can sharpen the execution envelope to near-linear in 1+b^2T+alpha0 T+p times a fixed polynomial in n and logarithmic rate/precision/input factors, with the actual query/consumer costs retained. Its low-rate per-window Poisson repair is essential to that refinement. If p itself scales with lambda T, the observation/output cost can restore a linear-rate dependence. Neither this statement nor the compiler outputs all microscopic physical source events for free.

## 5. Strong ordinary comparators and a precise limit

**Direct trajectories already use n bits, not 2^n.** Simulating every physical event takes expected lambda T source updates and actual system evolution/control work. A state-space density solver may enumerate 2^n histories, but it is not the strongest baseline. The claimed interface improvement is avoiding the high-rate loop for the coupled controlled process, not compressing an ordinary n-bit memory by calling its state count exponential.

**Source endpoints alone are easy.** After k events, if k<n the final history is the original suffix followed by k fresh bits; if k>=n it is n fresh bits. One can sample the capped count using probabilities for k=0,...,n-1 and a residual arm, then draw at most n bits. Thus endpoint sampling need not visit every event. That observation does not automatically reproduce the system's chronologically ordered noncommuting B(history) evolution. Neither does it establish a lower bound against a better ordinary path-functional algorithm.

**Process tensors already retain reusable memory and controls.** [OQuPy](https://arxiv.org/abs/2406.16650) provides reusable process-tensor machinery for non-Markovian system dynamics. [Jørgensen and Pollock](https://arxiv.org/abs/1902.00315) exploit causal tensor-network structure for non-Markovian path integrals and multitime correlations. These are genuine retained-knowledge/retained-memory alternatives, not methods forced to restart from scratch after every control. Their costs depend on the particular acquired/compressed process representation; this note proves no general rank or runtime lower bound against them.

**Dense exact and elimination routes remain relevant.** For small n/system dimension, a full joint generator and high-precision dense exponential may be simpler. At fixed error and very rapid lambda, a justified effective model can be preferable. Known special B functions can admit direct algebraic or low-bond descriptions. No practical crossover or universal advantage follows from the corollary.

The concrete result is an acquired program-to-interface map for known bounded-history colored-noise outputs, including nonlinear history functions and noncommuting system values. It is not acquisition from raw samples, not a universal generative-program theorem, and not evidence of a new general learning operation.
