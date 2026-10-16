# Independent asynchronous adversarial result

Author: gd_async_adversary. Date: 2026-10-16. Pinned knowledge revision: `2688d7a383502df4fc1e64001d04bb76e6ec05e5`. Internally derived and externally unreviewed.

## Result

The full arbitrary-asynchronous product `product_i Q_i` remains **OPEN** in this investigation. No admissible finite shared-bath counterexample was obtained. The incoming sine lemma, one-common-gap theorem, synchronized product, singleton minimax, and original-Walsh receiving lift were independently reconstructed without finding an internal mathematical flaw under their stated assumptions.

There is a rigorous improvement to the incoming arbitrary-schedule certificate. Define

    s(a)=sin^2(min(a,pi/2)),
    Q_i=1-product_k(1-s(a_ik)),
    C_i=min(1,sum_k s(a_ik)).

For every nonempty subset A whose own pinch schedules synchronize,

    E_every-coordinate-ever-mismatches
      <= [product_(i in A)Q_i]
         [product_(j outside A)C_j] P_s.                 (R1)

The all-endpoint-flipped effect is smaller and obeys the same bound. The minimum over these scalar certificates and the incoming `product_i C_i` certificate is valid. Every singleton is an available anchor. Thus, for two arbitrary schedules,

    E_history <= min(Q_1 C_2,C_1 Q_2) P_s.              (R2)

For each outside coordinate choose one witness gap and scale its interaction. For all real scales the anchor's synchronized **history** theorem remains valid, since outside interactions and pinches preserve every anchor parity. The selected projected amplitude is therefore bounded on the entire real scale domain by `sqrt(product_A Q_i)`. It vanishes whenever a chosen outside gap is deleted and has that gap's action as its entire type. Iterating the operator sine lemma, unioning one witness gap per outside coordinate, and dropping outside constraints with sums at least one proves (R1). This mixed proof avoids applying an unproved multigap Q contraction to a future-postselected map. Complete details are in [ANALYSIS.md](ANALYSIS.md), Section 5.

An exact strict asynchronous comparison has horizon 3, coordinate-1 cut at 1, coordinate-2 cut at 2, and t=arcsin(3/5). Set j_1=t on [0,1] and t/2 on [1,3]; set j_2=t/2 on [0,2] and t on [2,3]. Every own gap has action t, so Q=369/625 and C=18/25.

| Certificate | Exact value | Decimal |
|---|---:|---:|
| Incoming product C | 324/625 | 0.5184 |
| Proven anchored bound | 6642/15625 | 0.425088 |
| Desired product Q, still unproved | 136161/390625 | 0.34857216 |

The proven upper improves the incoming certificate by exactly 18 percent. These numbers compare sufficient certificates; they are not actual probabilities for a specified Hamiltonian. Sharpness of the anchored upper is not claimed.

## Exact proof-technique obstruction

Global entire contraction, deletion-null hyperplanes, and even/odd reflection symmetry do **not** suffice for the desired multigap Q contraction. With c=cos x,d=cos y, define

    F10=sin x(3+2d)/5,
    F01=sin y(3+2c)/5,
    F11=sin x sin y/5,
    F00=(sqrt(6)(1-c-d-cd)/5,cd/5).

The sum of the squared norms of all four components is identically one, with exactly the reflection parity indicated by each binary label. At sin t=3/5,cos t=4/5, the terminal-odd subvector `(F10,F01)` has squared norm `9522/15625`, exceeding `Q(t,t)=9225/15625` by `297/15625`.

This is an exact abstract isometry, **not a legal causal pinch protocol or an original-Walsh counterexample**. Its complete first-record marginal depends on a future own-gap scale, precluding its use as the full unprojected singleton comb. Such dependence can legitimately appear after postselection on another coordinate's future endpoint, so this fact does not exclude a larger legal embedding. No embedding or exclusion was established. It precisely refutes a tempting analytic tensorization lemma that would otherwise try to prove the central asynchronous product from the sine lemma alone.

## Finite computational evidence

The own authored searches explored 41 local optimizations in legal three-stage and nine-subsegment staggered schedules. Broad-parity baths had dimensions 1 and 2; literal seed-factorized baths had dimensions 2, 3 and 4. Norms and cross-parity algebra were imposed by construction. Every objective was the top eigenvalue of the endpoint effect on the entering bath space, not a single chosen bath state. The largest ratio to Q_1Q_2 among these searches was about 0.915372352 in the broad d=2 family.

An exact product-saturating seed-factorized sink with bath dimension 9 was also tested. Its 960 norm-preserving random bath-control perturbations and four local optimizations with 108 parameters produced no product violation. The closest optimized ratio was about 0.999999979. Some optimizer runs exhausted their stated local evaluation or iteration budgets; they are not certified global optima.

Separate NumPy 2.5/einsum recomputation of all saved best candidates confirmed finite matrices, parity/norm residuals below `2.0e-15`, unitary residuals below `7.1e-15`, and search-candidate probability agreement within `1.5e-15`. `exact_receipt.json` verifies the abstract isometry polynomial identity and all rational comparisons exactly. Finite search receipts do not establish a universal theorem or a refutation.

## Scope and artifacts

The bounds hold for arbitrary finite shared baths and references in the stated one-parity-per-interaction contract. Under the qualified additive private-sign common dilation, the virtual-seed gauge identifies the same averaged positive Walsh effects, with exact `2^(-|S|)` Fourier normalization and fair-refresh complete pinches. Every baseline/coefficient/dilation must remain independent of all selected private bits. Broad conditional-parity couplings are not automatically literal seed-factorized Hamiltonians.

This investigation supplies no finite-width or noisy controller, physical syndrome detector, calibrated envelope, reset operation, complete memory construction, or uncharged simultaneous-control capability. No historical novelty is claimed. The classical Bernstein inequality is primary sourced; the anchored certificate is an internal improvement over this inspected packet. External correctness, exhaustive priority and physical implementation remain separate unresolved questions.

Primary and pinned inputs are listed in `SOURCES.md` and hashed in `source_receipt.json`. Complete arguments and failed approaches are in `ANALYSIS.md`; own programs, bounded search results, numerical verification and exact algebraic receipts are adjacent. `FROZEN.json` identifies this worker snapshot. No incoming original was edited, no current peer output read, no acquired program executed, no package installed, no repository mutated, and no subagent spawned.
