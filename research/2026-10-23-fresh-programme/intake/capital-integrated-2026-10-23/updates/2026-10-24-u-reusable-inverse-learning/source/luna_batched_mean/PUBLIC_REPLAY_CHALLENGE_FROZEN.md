# Finite public-replay challenge — frozen opening

**Status:** challenge/interface frozen after reading only the lead-owned LEAD_PROCEDURE_FROZEN.txt. No benchmark code or run has been produced. The prior PCA and source-only QEC calibration artifacts remain frozen and untouched.

## Bounded executable instance

Use the known recurrence
\[
u_0=b,\qquad u_{k+1}=a\,u_k(1-u_k),\qquad f(a,b)=u_K
\]
with fixed \(K=6\), cell depth \(H=4\), and the 16-by-16 cell-centered parameter grid
\[
a_i=3+\frac{i+1/2}{2^H},\quad
b_j=\frac18+\frac34\frac{j+1/2}{2^H},
\qquad 0\le i,j<2^H.
\]
Thus \(a\in[3,4]\), \(b\in[1/8,7/8]\), and there are 256 grid points. The dyadic quadtree root is the full rectangle; a split bisects both axes, all four children align with the grid, and depth \(H\) cells are singletons. The prior for each task is uniform on the grid; a cell's mass is its grid-point count divided by 256.

Use \(\epsilon=1/8\) and binomial data \((s_t,n_t)\) with \(n_t=8\), \(0\le s_t\le8\), and
\[
p(x)=\epsilon+(1-2\epsilon)f(x),\qquad
W_t(f(x))=p(x)^{s_t}(1-p(x))^{8-s_t}.
\]
All likelihoods are strictly positive and rational. This is a finite synthetic inverse-inference fixture, not a claim about a physical logistic system.

To exercise adaptive task switching without a hidden truth, run at most eight tasks, one posterior draw per task. Set \(s_1=3\). After task \(t\)'s draw returns row-major grid index \(r_t=16i_t+j_t\), set \(s_{t+1}=(s_t+r_t+1)\bmod9\). This public rule depends only on a previously revealed posterior sample; it never reads a latent parameter or exact response table. Each task has the same uniform prior and its displayed \((s_t,8)\) is the entire likelihood input.

## Exact paid interval program

For a cell \(C=A\times B\), evaluate the same recurrence with rational interval arithmetic. Start with \(I_0=B\). For \(I_k=[l,r]\subseteq[0,1]\), compute
\[
g_{\min}=\min\{l(1-l),r(1-r)\},\quad
g_{\max}=\begin{cases}
1/4,&1/2\in[l,r],\\
\max\{l(1-l),r(1-r)\},&1/2\notin[l,r],
\end{cases}
\]
then \(I_{k+1}^{raw}=A\,[g_{\min},g_{\max}]\), intersected with \([0,1]\). The invariant follows because \(a\in[3,4]\) and \(u\in[0,1]\) imply \(0\le a u(1-u)\le1\). Store the final interval intersected with the already-paid parent interval. Every new cell's raw interval requires one charged execution of all \(K\) recurrence steps; a split materializes and charges all four children. Cache hits reuse a stored bound and are logged. At depth \(H\), the interval is the exact rational value at the cell center.

No Lipschitz constant, response table, candidate-point value, or unqueried child range may be supplied to the learner. The evaluator may enumerate the 256 exact grid values separately, but that enumeration is excluded from the learner input and must be separately costed as an exact-grid control/validation workload.

## Exact likelihood and proposal operations

For each active leaf interval \(I_C\), map its endpoints through the known positive affine \(p(f)\). The minimum of \(p^s(1-p)^{8-s}\) on this interval is the smaller endpoint value; the maximum is the larger endpoint value or the value at \(p=s/8\) if that point lies inside. Compute \(L_C,U_C\) as exact rationals. Charge each likelihood-bound conversion for each task and active leaf; source intervals are reusable, likelihood conversions are task-specific.

Choose the proposal cell with probability proportional to \(\pi_C U_C\), then choose a grid point uniformly from that cell. Pin \(U_{old}=U_C\) from the selected cell. Draw one fresh threshold for this proposal. If \(u<L_C/U_{old}\), accept; if \(u\ge U_C/U_{old}\), reject; otherwise split the candidate cell, pay for all four child intervals, and repeat the comparison along the child containing the already-selected point, always using the same \(u\) and \(U_{old}\). This makes every node refinement and pending decision replayable and preserves the original proposal measure.

Proposal-cell and within-cell categorical choices have rational probabilities. Use exact integer rejection sampling from a power-of-two bit range: record the range width, every random bit chunk, each rejected integer, and the selected category. For the acceptance threshold, the mathematical sampler is a fresh ideal stream of independent fair bits representing \(u\in[0,1)\) lazily by nested dyadic intervals. Compare that interval exactly to \(L_C/U_{old}\) and \(U_C/U_{old}\); refine the cell with the same bit prefix when the comparison remains undecided, and at a singleton continue drawing bits until its exact rational threshold is separated. Equality with a rational threshold has probability zero under ideal infinite fair bits, so termination is almost sure. The executable transcript records all consumed bits. A finite PRNG run is an implementation fixture only; pseudorandom output does not itself prove the ideal exact sampling law.

Each proposal, cell choice, point choice, rejection, threshold bit, interval split, and final accept/reject is included in the public transcript. Randomness streams are fresh and independent; no revealed bits are recycled as independent randomness. A replay takes the visible program/configuration, counts, paid node log, and consumed bit transcript, recomputes all exact rational bounds, verifies each decision by integer cross-multiplication, and checks that \(U_{old}\) remains the original pinned value. The source tree contains only paid intervals and parent intersections. No hidden evaluator values are imported into the learner or replay.

## Challenge task stream and transcript schema

The transcript must include, in deterministic order:

- Public configuration: \(K,H,\epsilon\), grid formulas, prior, task-count rule, task index, and executable/source-code hash.
- For each paid node: node and parent IDs; exact cell endpoints; raw rational interval and parent-intersected interval; recurrence-step count; numerator/denominator bit lengths for every stored endpoint; interval operation counts; peak and cumulative rational sizes; cache hit/miss.
- For each task and proposal: \(s_t,n_t\), active-leaf likelihood-bound conversions; exact \(\pi_C,L_C,U_C\) and proposal weights; random bits/rejection attempts; chosen cell and grid point; pinned \(U_{old}\); threshold-prefix lengths; every before/after interval comparison; every paid refinement; final decision; posterior sample index; current \(Z_{lower},Z_{upper}\) and \(Z_{lower}/Z_{upper}\).
- Cumulative source calls and recurrence steps; likelihood conversions; accepted and rejected proposals; random bits by use; interval-tree node count and serialized numerator/denominator bytes; retained tree bytes; and exact-arithmetic operand/result sizes.

For rational accounting, report counts of additions, subtractions, multiplications, divisions, comparisons, and gcd reductions, together with input, temporary, and output numerator/denominator bit lengths. Do not convert node-call counts into wall-time advantage. Also report measured wall time separately if the same executable is replayed on the same hardware. Full-grid direct exact evaluation is a strong control: charge all 256 point evaluations, rational work, memory, and posterior-weight calculations rather than treating its table as free validation.

## Critical cost challenge before any run

For this dyadic fixture a common parameter denominator is \(Q=2^{H+3}\). Before reduction, a denominator for \(u_K\) is bounded by \(Q^{2^{K+1}-1}\); with \(H=4,K=6\), it is at most \(2^{889}\), requiring up to 890 binary digits. With \(\epsilon=1/8\), the affine probability denominator is bounded by \(2^{891}\), and a binomial weight with \(n_t=8\) has denominator bounded by \(2^{7128}\), requiring up to 7,129 binary digits before reduction. Proposal weights also include dyadic cell masses. These are finite and manageable at the frozen small setting, but their bit lengths grow exponentially in \(K\); a source-query amortization exponent alone cannot support a practical-cost claim. The run must display actual rational bit lengths and random-bit/rejection costs. Any larger-\(K\) claim remains blocked until those costs are measured.

The replay verifies deterministic decisions conditional on the supplied random-bit transcript. It cannot certify that a PRNG emitted independent fair bits. Exact posterior-law claims therefore remain conditional on the ideal independent fair-bit source and on the mathematical pinned-denominator proof. No benchmark, target comparison, or new-method claim is authorized by this opening.
