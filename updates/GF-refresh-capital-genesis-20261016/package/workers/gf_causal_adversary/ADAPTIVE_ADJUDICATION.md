# Independent adjudication of the adaptive and mean-action claims

Author: `gf_causal_adversary`. Date: 2026-10-16. Requested by root after completion of the fixed-schedule audit.

**Disposition: both main mathematical claims are sound under their distinct explicit interfaces.** I found one misleading singleton mean-hazard remark, supplied an exact finite counterexample, and verified that the author corrected the remark in `ADAPTIVE_PRODUCT_THEOREM.md`. That correction does not change either main proof. This adjudication was derived from the two proof files without reading their producer test results or relying on agreement. It establishes no external validation or historical novelty. Root separately identified a close primary prior for the mean-action constant/weak-loop construction; that exact primary-model comparison belongs to the assigned primary reader and is not settled by this correctness review.

## 1. Keep the three contracts separate

| Claim | Certified resource | Information/operations | Joint conclusion |
|---|---|---|---|
| Supplied fixed-schedule product | Precommitted own-gap envelope actions | Actual fixed own pinches; records unavailable to physical controls | Product of fixed `Q_i` |
| Adaptive hazard-ledger theorem | Hard cap on sum of **preauthorized** `h(a)` on every surviving policy history against every prover | Finite typed classical command/record feedback; complete own cuts; branchwise hard cap within each gap | Product of `1-exp(-L_i)` |
| Expected stopped-action theorem | `E integral j_i(t)dt` actually charged until stopping | Arbitrary complete parity-preserving instruments, including accessible weak heralds, with causal feedback | Singleton `P<=C_i/k_*`; joint supremum is the minimum of the singleton factors, not their product |

The expected-action constraint is a property of an actual shared strategy. It is not a uniform constraint on each independent local tester against every prover. Consequently the mean-resource common-activation example and the positive all-pass strategy theorem are compatible.

The complete-cut restart constant `k_cut=min_a a/sin^2(min(a,pi/2))` uses a fourth, explicitly narrower **attempt-billing** contract: the precommitted attempt envelope is charged when an attempt is reached, including unused portions. It cannot be substituted for the actual stopped action of a weak-instrument protocol. Reusing the letter `A` for both costs is safe only with that distinction retained.

## 2. Adaptive hazard ledger: reconstructed proof

For a fixed finite gap policy and an arbitrary fixed prover, unfold every command measurement and every instrument outcome into a finite classical tree. Angles at the nodes are fixed data of this tree. Scaling rotations by a complex `z` changes the branch amplitudes but not the node maps or the policy cap. Immutable records retain orthogonality of different branches.

Let `A_v` be the maximum remaining charged angle sum on a path below node `v`. A rotation contributes at most `exp(theta |Im z|)`. A complete instrument with fixed Kraus maps `K_b` gives

```
||W_v(z)psi||^2
  = sum_b ||W_b(z)K_b psi||^2
  <= exp(2 A_v |Im z|) sum_b ||K_b psi||^2
  = exp(2 A_v |Im z|)||psi||^2.
```

Backward induction proves type at most the **maximum path** cap, not the sum of all alternative branch costs. On the real axis this is a complete normalized experiment. Deleting all charged rotations leaves parity-preserving instruments and controls, so the opposite-parity amplitude vanishes. The supplied operator sine lemma therefore gives mismatch probability at most `s(a)` for the entire gap instrument. No individual branch is normalized and assigned this same bound.

The hard cap must be structural on the full permitted finite policy tree, including nodes that happen to have zero probability for a particular nominal input. A cap inferred only from one realized transcript would not support the scaling argument. The written contract specifies every classical branch and every prover, which is sufficient.

On histories with no prior mismatch, the preceding actual complete own cut leaves definite even parity. The next authorization `a` is already fixed when the gap starts. Put `H` equal to accumulated authorized hazard and `S` equal to the survival indicator. Since `1-s(a)=exp(-h(a))`,

```
E[S_next exp(H_next) | past, a] >= S exp(H).
```

The fixed finite skeleton permits ordinary finite-tree conditioning and no-op padding of halt branches. The uniform hard ledger `H<=L` on every surviving leaf gives

```
1 <= E[S exp(H)] <= exp(L) Pr(S=1),
Pr(first mismatch) <= 1-exp(-L).
```

Every local policy, including its record disclosure, command archive, ledger and flag, is still one fixed causal tester. Shared decisions enter only through messages from the joint prover. With independent initial local resources and a deterministic finite common round skeleton, its operations tensor exactly. The already checked Gutoski-Watrous positive domination theorem therefore multiplies these uniform singleton values. Variable local completion times do not invalidate tensorization when represented in that finite skeleton.

The edge-by-edge Hamiltonian transfer is valid only for an actual finite classical scheduling tree with predetermined branch envelopes, parity-preserving full controls, and a common record dilation. It does not cover arbitrary continuous stopping times, erased coherent timing records, unlimited message precision, unqualified physical readout, or budgets invented after a successful branch. Concurrent reservation and memory lifecycle hypotheses remain separate physical receiving obligations.

## 3. Expected stopped action: reconstructed universal proof

Write `p=Tr(P rho)` on one genuine conditional branch. The even Hamiltonian preserves `p`. Purifying the state and applying Cauchy-Schwarz to the odd block gives

```
|p'| <= 2 j sqrt(p(1-p)).
```

This is a bound on the full system/reference norm, not a reduced-state calibration. The angle `theta=arcsin(sqrt(p))` is Lipschitz with speed at most `j`, with endpoint cases obtained by the integrated comparison.

For `k_*=(pi+2)/4`, define the proposed potential

```
Phi(p) = arcsin(sqrt(p))/k_*                    if p<=1/2,
Phi(p) = (pi/4+p-1/2)/k_*                      if p>=1/2.
```

It is continuous with matching first derivatives at one half, starts at zero, ends at one and is nonnegative. On the lower interval its second derivative is

```
(2p-1)/(4 k_* [p(1-p)]^(3/2)) <= 0;
```

on the upper interval its slope is constant. Thus it is globally concave. As a function of the angle, its slope is `1/k_*` below `pi/4` and `sin(2 theta)/k_*` above it. Hamiltonian evolution therefore increases potential by at most charged action divided by `k_*`, including endpoint population values without division by zero.

A complete instrument with every Kraus map commuting with `P` preserves the average population:

```
sum_y w_y p_y = p.
```

Concavity implies `sum_y w_y Phi(p_y)<=Phi(p)`. This is true for arbitrary bath/reference states and arbitrary causal choices of the next instrument. Refining hidden Kraus labels in the analysis does not give them to the controller and does not alter the inequality. A single normalized successful filter would fail this argument, but the written protocol includes every branch of every instrument.

Sum these inequalities on the full finite tree, with each node weighted by its actual reach probability. Initial potential is zero; every exact success leaf has `p=1` and hence potential one, while failure leaves have nonnegative potential. Consequently

```
Pr(exact recorded success) <= E Phi(p_terminal)
                            <= E integral j dt / k_*.
```

Countable stopping is justified by finite prefixes and monotone convergence exactly when successes occur at finite prefixes and costs accumulate monotonically. A limiting state in odd parity with no finite certified success is not silently included. The proof requires no unbounded optional-stopping theorem.

## 4. Sharp weak-herald family and its costs

The proposed instrument `C=sqrt(epsilon) P_1`, `N=P_0+sqrt(1-epsilon)P_1` is complete and parity preserving. A click has exact odd output. Starting from angle `pi/4`, its no-click state has angle `atan(sqrt(1-epsilon))`; the specified forward rotation restores the same state. Conditional click probability is `epsilon/2`, so the stated geometric probe/feedback counts and expected odd action follow.

With `u=(1-sqrt(1-epsilon))/(1+sqrt(1-epsilon))`,

```
d=atan(u),
(2-epsilon)/epsilon=(1+u^2)/(2u),
A_infinity=pi/4+(1+u^2)atan(u)/(2u)
          = k_* + u^2/3 - u^4/15 + ... .
```

Since `u=epsilon/4+O(epsilon^2)`, the leading excess is `epsilon^2/48`. This verifies the constant and the limiting mechanism independently of a numerical fit.

For the finite protocol, restoring after the **last** no-click is important and is charged. The surviving probability is `r^n`, `r=1-epsilon/2`; the final actual complete measurement contributes success `r^n/2`. This yields exactly the written `P_n`, `A_n`, expected probe count and expected restore count. My separately authored exact two-level branch check uses `epsilon=3/4`, `n=3`, obtaining

```
P=899/1024,
A=pi/4+(645/512)atan(1/3),
E N_weak=129/64.
```

The displayed decimal action/success ratio in the checker is a diagnostic; the exact expressions and the universal proof carry the mathematical claims. Initial random activation and increasingly accurate finite weak-loop protocols give the claimed success supremum for every mean-action budget. A common activation bit similarly attains the multi-coordinate **minimum** frontier in supremum; independence of conditional qubit constructions is used only for this explicit lower witness.

The instrument and accessible herald are added operations. They are not supplied by a complete private pinch or by a measured marginal coherence multiplier. Probe calls, feedback latency, reset, detector quality, reservations and syndrome readout remain separate costs. Expected probe and feedback counts diverge in the weak limit, so finite positive probe/decision costs defeat a claim of a free limiting controller. The potential theorem optimizes odd action alone.

## 5. Exact correction found during this review

The original adaptive file's remark that a singleton Jensen mean-hazard bound remains true needed qualification. It is true for its displayed one-gap **external** activation example. It is false for a general adaptively stopped hazard bill.

Use at most two complete-cut attempts with angle `pi/4`, stopping at the first mismatch. Success probability is `3/4`. Hazard `log(2)` is charged for the first attempt and, with reach probability `1/2`, for the second, so

```
E H = (3/2) log(2),
1-exp(-E H) = 1-sqrt(2)/4 < 3/4.
```

The exact positive excess is `(sqrt(2)-1)/4`. The correct **hard** ledger cap is `L=2 log(2)` and gives `1-exp(-L)=3/4`. The author has now restricted the Jensen remark to its external one-gap example and added this finite counterexample. The singleton ledger submartingale proof always used `H<=L`, so its main theorem was not affected.

Six independently authored exact check modules passed in `ADAPTIVE_EXACT_CHECKS.json`; maximum system dimension is two. They check the potential identities, the complete weak instrument and exact restore, finite branch sums, limiting series, this stopped-hazard counterexample, and the shared-activation mean-cost product failure. No producer test output, optimization, random search, installation, nested worker or external outreach was used. Model thinking tokens remain unmeasured and UNKNOWN.

Final status: mathematically accept the two stated finite-interface claims after the above correction; retain their distinct action/access contracts, broad physical receiving obligations and unresolved historical comparison. The exact matching-constant prior identified by root prevents treating this reconstruction alone as discovery evidence.

## 6. Subsequent known-pure-angle corollary

After the main adjudication, the author sent a proposed value function for a **known pure qubit**, with initial angle `theta in [0,pi/2]`. I reconstructed it directly without producer test outputs. Its expected odd-action infimum for exact success is

```
V(theta) = k_*-theta       for theta<=pi/4,
V(theta) = cos^2(theta)    for theta>=pi/4.
```

The lower bound is the initial-potential version of the same proof: exact success probability one requires `A>=k_*[1-Phi(sin^2(theta))]`. Below balance, rotate forward by `pi/4-theta`, then use a balanced weak loop whose remaining action infimum is `1/2`. Above balance, set `p=sin^2(theta)` and use the free herald with strength `epsilon=(2p-1)/p`. The click probability is `2p-1`. On no click, both amplitudes equal `sqrt(1-p)` before normalization, so the state is balanced and that branch has probability `2(1-p)`. Its expected optimal remaining cost is therefore `1-p`. At `p=1/2` skip the zero-strength probe; at `p=1` the initial state is already odd and costs zero.

The infimum also holds among **finite protocols with exact success probability one**, under this known-qubit interface. In the finite `n` balanced protocol, the final complete measurement fails with probability `r^n/2` and leaves the known pure state `|0>`. Rotate that branch by `pi/2` and verify odd parity. This repair adds expected action `(pi/4)r^n`, vanishing as `n` grows. The balanced finite-certainty cost is

```
d_epsilon*r*(1-r^n)/(1-r) + (pi/4)*r^n.
```

First take `n` large and then `epsilon` small to approach `1/2`. This does not imply a small worst-case action, bounded controller latency, optimal full detector cost, or attainability from an arbitrary mixed/unknown state. No historical novelty claim is made for this corollary.
