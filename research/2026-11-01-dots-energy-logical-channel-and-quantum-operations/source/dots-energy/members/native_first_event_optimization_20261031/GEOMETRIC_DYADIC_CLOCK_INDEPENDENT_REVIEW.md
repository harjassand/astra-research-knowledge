# Independent review: fixed-window and coherent dyadic clocks

## Scope and source binding

I read both complete author bodies and checked their clock laws, coherent realization, and receiving errors separately from the frozen whole compiler and numerical ledgers.

Fixed-window source: `FIXED_WINDOW_GEOMETRIC_CLOCK_BINDING.md`, SHA-256 `16335629791a1bfa6368171f39182fde71b61d957c87e2af0c26188684809500`.

Coherent conditional final source: `COHERENT_DYADIC_TRUNCATED_CLOCK.md`, SHA-256 `71a7d3ecb1cf66fb759a4048d7af027ef80dd2f75a9395baf62e181e724ed13a`. I read the final precision and zero-input edits and independently verified this final hash. The initial complete body was `COHERENT_DYADIC_TRUNCATED_CLOCK.md`, SHA-256 `b157bea103f4b1e68b96b5778ffe3d1778e2736a939af93d4a062e8e0f6e60ad`; the subsequent primary implementation paragraph was read at `729375406727eab9e1598f269bc29e5920dfec9e4c74d836b121ed4d4abb910c`.

Verdict: local mathematical PASS with the explicit real-polynomial QSVT and precision convention below. These are acquired alternative clock operations, not a whole integration, executed gate backend, resource advantage, or amendment of any frozen ledger.

## 1. Fixed-window product clock

For M=2^B, z=exp(-q tau/M), the product identity product_j(1+z^(2^j))=(1-z^M)/(1-z) proves the claimed independent-bit law exactly. Its probabilities are integrated exponential-bin masses, not a pointwise approximation to the density. The q=0 and B=0 limits are well defined. Reflection implements an increasing exponential. A separate tail flag of mass exp(-q tau) produces an uncensored exponential censored at the classical window; its unknown time is irrelevant to comparisons with thresholds no larger than that window.

All these angles depend only on the fixed classical rate/window and the bit index. A circuit can prepare the bits with actual controlled rotations and retain every seed for reversal. Nonpositive-exponential evaluation and squared-probability clipping tolerances suffice for operator-norm angle accuracy. The construction does not prepare a conditional exponential at an arbitrary coherent duration for free. Adaptive recompilation after a private physical event-time measurement is permitted in the received simulator, with its actual arithmetic cost charged.

## 2. Outer bins and the physical clock

For the three-exponential proposal, component labels remain orthogonal private Kraus coordinates and every component uses the same normalized block JK0(t)/sqrt(w_total(t)). This condition is essential. The exact integrated bin weights admit a mathematical embedding into the continuous Kraus environment by adjoining the exact conditional time within each bin. Embedding the finite bin vector with that conditional density preserves its norm. The midpoint differs by at most Delta/2.

Consequently the normalized block derivative gives an L2/Stinespring error at most Lout Delta/2, because total proposal mass divided by A^2 is at most one. The exact continuation channel changes by at most Lphys Delta/2. Neither conclusion asserts TV closeness of continuous and discrete timestamps. The proposed mesh budget pays both errors. Finite component weights, angle synthesis, and actual midpoint arithmetic are separately charged.

This removes outer inverse-uniform endpoint-strip costs for this replacement only. The physical short-window rule survives. An old inner source with endpoint floors cannot silently inherit their removal; the separately reviewed stable hierarchical source supplies the zero-duration limits needed to avoid those floors.

## 3. Sequential QQ clocks

Independent unconditioned exponential waits, censored only at the fixed call window and compared with the coherent remaining residence, give exactly the ordinary conditional-residence Poisson law before discretization. There is no division by the probability of an event before that residence. With at most K total accepted virtual insertions and at most K+1 residences, 2K+2 allocated waiting draws safely include the final stopping draw. Overflow selects the zero word; it is not restarted until success. Unused draws and reversible history remain available for unpreparation.

Under the conditional-bin coupling, matching wait errors accumulate linearly. A fresh exact wait has density at most q conditional on the entire preceding history. Thus each changed stop decision costs at most a constant times q times the inherited remaining-time error plus its bin width. Summing over the capped path yields O(q(K+1)^2(Delta_QQ+h_off)). On matching paths, chronological mark positions change by O((K+1)(Delta_QQ+h_off)), and telescoping the actual word gives the stated O([Hs+mu(alpha_H+1)](K+1)^2(Delta_QQ+h_off)) norm error.

At a rounded zero residence, the exact probability of a missing QQ mark is at most q times its small exact duration. Equality is treated as a zero interval in the fixed boundary order, not as license to interchange noncommuting boundary operators. Fresh numerical rotation errors are summed in circuit operator norm over the fixed number of uses. These facts justify the mesh choices up to the stated conservative constant subdivisions. They remove sorting and coherent exponential/logarithm evaluation from these QQ waiting clocks only.

## 4. Coherent dyadic truncation

For N>=1, l=ceil(log2 N) and M=2^l give N<=M<2N. Preparing the first l geometric bits with a fixed angle list and testing m<N has success

P_N=(sum_{m<N}z^m)/(sum_{m<M}z^m)>=N/M>=1/2.

The inequality follows from decreasing nonnegative weights. Conditional on that test, the accepted state has exactly the integrated bin probabilities of an exponential conditioned on [0,Nh]. N remains in the output, so different N labels remain orthogonal even when the normalized clock states overlap. The proposal is a genuinely acquired rectangular block with singular values sqrt(P_N), uniformly bounded below by 1/sqrt(2).

Left endpoints stay on the common grid and are within h of the exact conditional time. Reflection gives the increasing law with the same displacement bound, including allowed endpoint values. N=0 must be dispatched by the caller's explicit limiting-bridge convention, not by normalizing a zero-probability event. Invalid integer padding must likewise be excluded or flagged; it is not part of the admitted singular interval.

## 5. Bounded polynomial and actual polar preparation

For c_k=binom(2k,k)/4^k, p_m(x)=x sum_{k=0}^m c_k(1-x^2)^k is odd of degree 2m+1. Its nonnegative partial series lies between zero and one on [0,1]; oddness gives absolute bound one on [-1,1]. For x>=1/sqrt(2), the missing series is at most 2^-m. The proposed m therefore gives O(eta^2) good-amplitude error. Scaling by 1-eta^2/256 preserves a strict global margin without changing that conclusion.

A bounded real polynomial is not automatically the exact response of a single bare phase sequence. The appropriate established receiver is rectangular real-polynomial singular-value transformation with its extra real-part signal ancilla, prepared and projected in |+>, and the two controlled conjugate phase sequences. Its projected block is the real polynomial at normalization one. This is the convention used here. The input clean-seed projector and output accepted-clock projector are explicitly computable, and the proposal and inverse are known circuits.

I freshly inspected Gilyen--Su--Low--Wiebe, Corollaries 10 and 18, for this real-polynomial convention and constructive phase acquisition: https://arxiv.org/html/1806.01838 . I also inspected Haah, Section 4.3, for bounded-precision product decomposition: https://arxiv.org/html/1806.10236v4 . These are ordinary primary components, not new phase synthesis.

Binding precision: classical polynomial/phase factorization must approximate the target GOOD polynomial to O(eta^2), not merely O(eta). This ensures its ideal coherent failure amplitude stays O(eta). Subsequent elementary unitary/phase synthesis is budgeted in total circuit operator norm O(eta), using actual capped circuit length. Approximating only the good polynomial to O(eta) would in general permit O(sqrt(eta)) failure and is not the claimed source accuracy. The stronger preprocessing tolerance costs only a constant factor in log(1/eta).

The polar direction on each singular vector is exactly the normalized accepted clock state. A good-amplitude deficit O(eta^2) gives failure norm O(eta) by unitarity; different N columns remain orthogonal. Hence the full source-isometry bound is uniform for coherent N and arbitrary external references, without a sqrt(Nmax) factor. Actual proposal rotation and signal-phase errors are charged by unitary telescoping, not by a claim that scalar polynomial derivatives control changing singular vectors.

The rational coefficient list has polynomial degree and bit length; its conversion and finite phase preprocessing are paid. The resulting O(log(1/eta)) proposal-call bound and polynomial-in-bit-length preprocessing are sound. The product preparation has O(Bmax) controlled rotations plus actual leading-bit, comparison, and uncomputation circuits. No range-sized table, exact-real phase oracle, or conditional-acceptance P_N evaluation is required.

## 6. Receiving boundaries and checks

Replacing a truncated exponential inside the existing hierarchical source still requires the acquired atom/mixture probabilities, acceptance arithmetic where applicable, grid compatibility, and the full chronological word error argument. This source alone does not remove all coherent arithmetic from the simulator. Each source-isometry error is divided across the actual capped uses; SELECT is zero on failure and all seeds remain until reversal. Outer Kraus-coordinate errors continue to use the L2 comparison, unlike inner selected-word average estimates.

The fixed-window clocks need no amplification and should not pay the conditional-clock cost. The coherent dyadic alternative pays logarithmically many cheap proposals rather than the earlier three proposals plus scalar conditional-acceptance arithmetic. Which is cheaper requires an integrated receiving ledger with all phase acquisition, rotations, comparisons, and arithmetic costs. Neither proposal counts nor this mathematical proof are a hardware-gate benchmark.

As nonproof sanity checks, I independently verified product-bin identities for B=0,...,7 and five rate-grid scales (maximum discrepancy 1.12e-16), and the polynomial bound/tail at 29,029 grid points. These checks do not implement the QSVT phase backend and do not substitute for the algebra above. Frozen earlier sources and ledgers remain unchanged.

## Final binding

The author explicitly incorporated the requested eta^2/1000 good-polynomial factorization tolerance, O(eta) total actual circuit synthesis error, and controlled exclusion of N=0 from the polar block in the final 71a7d3ec source. I read those final edits. No clock law, numerical ledger, or whole-compiler source was silently altered by this receipt. The two exact source hashes named above are the binding versions.
