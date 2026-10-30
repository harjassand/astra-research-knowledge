# Independent audit: infinite-phase first-residual-exit contraction

Reviewed 2026-10-30. Verdict: **the stated controlled projected-model result passes**. This is not a physical recurrence theorem or an assertion that the physical coefficient-comparability cone is invariant.

## Residual and finite head

The displayed h has h(b+3)-h(b)=2 for b>=1. Immigration has residual increment +1 exactly at b=3 and b>=6 divisible by 3, otherwise zero. Clearing has increment -1 exactly at b>=7 congruent 1 mod 3, otherwise zero. Activation is disabled at b=0 and is neutral at every enabled b. These identities follow directly by the three residue cases (also checked programmatically through b=9999).

Re-running `check_first_residual_all_exit_degrees.py` reproduced the supplied JSON byte for byte. At K=12 the maximum up exponent is -1 and maximum neutral-tail exponent is -2. The script's initial docstring says “frozen-A”; it should say “fixed residual r, n=r+h_B,” but its actual degrees and topology implement the latter correctly.

The degree arithmetic is exact: eliminating v replaces each remaining off-diagonal rate by q_ij+q_iv q_vj/q_v, discards self returns, and reconstructs q_v as the sum of current outgoing rates. All arithmetic is positive. Thus a sum takes the maximum degree and a quotient subtracts degrees; there is no concealed cancellation in a diagonal subtraction. Source probes have a sole initial rate-one transition into the queried state. Their final rates to absorbing labels equal the corresponding absorption probabilities. Parallel channels are combined by max because they add positively.

At fixed head width, positive compact coefficient intervals give uniform leading-order bounds for every positive Schur expression. Every endpoint row policy is transient: a sequence of at most four immigrations reaches an up exit, from every head state. Maximizing the sum of the endpoint-policy absorption-value vector yields a common supersolution: if another row makes Q'v+b'>0 in that row, then (-Q')^{-1}(Q'v+b') is nonnegative and has a strictly positive entry, contradicting maximality. Reward b' must change with the row; the note does this correctly. This proves bounds for arbitrary adapted controls by stopped Dynkin, not only stationary policies.

The head time bound also follows without any matrix asymptotics. On the finite head total rates are <=C r^3 and immigration rates >=c. A prescribed sequence of at most four immigrations has conditional probability >=c' r^-12, while each holding time has conditional expectation <=1/c. Block attempts give E tau_head <=C' r^12, uniformly over adapted controls. No claim of a sharp exponent is needed.

## Infinite tail

Before the first immigration, down exit or head entry, activation preserves B mod 3 and clearing decreases it by one mod 3. Hence at most three clearings occur, including a possible terminal clearing. Throughout this stopped tail, n>=r and B>=13, so clearing intensity >=c r^3. The stopped counting-process compensator gives

    c r^3 E tau <= E(number of clearings before or at tau) <=3.

One may first stop at finite state/time cutoffs and then pass to the limit. Immigration-first probability is bounded by C_I E tau. This argument works for predictable, history-dependent rate controls; it does not assume an exponential holding time with a constant chosen rate.

There is no explosion loophole. For the killed neutral tail, the function 1+B has uniformly upper-bounded drift at fixed r: activation contributes O((r+B)B), while neutral clearing contributes -4 times a rate of order (r+B)^3(B)_4, and a killing clearing contributes an even more negative cemetery decrement. Localization therefore prevents escape to infinite B in finite time. Alternatively, infinitely many activations before three clearings would require B tending to infinity, whereas the conditional activation/clearing probability ratio is uniformly O(B^-5). Finite-head rates are bounded, and immigration has a bounded global intensity. These observations also justify repeated attempts.

A neutral immigration restarts a tail attempt with probability O(r^-3); summing this geometric correction preserves O(r^-3) time and first-up probability before head entry. The renewal inequalities for H and T therefore hold under arbitrary controls. For time bounds, the head-to-tail probability is O(r^-2), while the tail returns to the head with probability at most one; their product is strictly below one for large r. This establishes the asserted uniform polynomial time bound and almost-sure residual exit.

## Trace and scope

The terminal residual is exactly r+1 or r-1. Consequently the two exact factorial ratios are e^-d(r+1)^alpha and e^d r^-alpha. Combining these with P(up)<=C/r gives contraction tending to zero for every fixed d and 0<alpha<1. Polynomial excursion times are dominated by the factorial trace weight outside a fixed threshold, so summing conditional contractions bounds the expected accumulated excursion time until the residual threshold is reached.

That threshold is not compact in (n,B). Moreover, actual A/N can leave the comparison region during a neutral excursion. Neither defect is repaired by this controlled-model theorem, and neither is suppressed in the source's scope statement. The result is a valid infinite-background advance, not global physical recurrence.
12b36bcbc6cab1b0150f0b2c2d64a20bd7d40a51dfa47380b5f456185686db81  chemical_joint_shell_20261030/INFINITE_PHASE_FIRST_EXIT_CONTRACTION.md
13ce4126a42ca04c22b17a31cb8150de95f28ff89e268bb795c1283c9f15012d  chemical_joint_shell_20261030/check_first_residual_all_exit_degrees.py
31996b9fbc24ba5a3825618567d5f28bb12c0e183b87e8e78622faeead75d36a  chemical_joint_shell_20261030/FIRST_RESIDUAL_ALL_EXIT_DEGREES.json
