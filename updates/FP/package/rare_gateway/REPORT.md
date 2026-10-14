# Computation lane: a hidden-channel gate for certified rare-event rates

**Status: no new frontier operation established.** I pursued a certificate-carrying committor/Doob-tilt operation for a scientifically important output: a rare transition probability, the ingredient needed with an independently measured entry flux to obtain a nucleation or reaction rate. A small exact model shows why its apparent gain fails after charging acquisition of unseen reactive channels. The result is an oracle obstruction, not a claim about a real material or a novelty claim.

This was an instructed independent initial investigation. Isolation from other workers was a workflow instruction, not an enforced technical boundary. I read the campaign brief and capital entry instructions, but did not read another current worker's report or use a historical capital claim as a premise.

## Output, information, and resources

The desired output is $p=P_s(\tau_B<\tau_A)$ to relative error at most $1/4$, with success probability at least $2/3$ for every admissible dynamics. A physical rate would be $\lambda p$, where the entry flux $\lambda$ must be acquired and calibrated separately; no value of $\lambda$, force field, experimental rate, or atomistic result is claimed here. Actual crystal nucleation rates are computed using forward flux sampling in [Jiang et al.'s NaCl study](https://arxiv.org/abs/1711.07804); its force-field rates did not agree with the cited experiments, underscoring the need to separate a model rate from physical validation.

For the exact comparison, let $N=2^n$ candidate conformers and $L\geq0$ barrier stages. From $s$, choose $i\in\{0,\ldots,N\}$ uniformly. At $(i,k)$, $k<L$, move to $(i,k+1)$ with probability $1/2$ and otherwise to absorbing $A$. At $(i,L)$, move deterministically to $B$ if $i$ is reactive and to $A$ otherwise. Conformer 0 is known reactive. The unknown dynamics are either $H_0$, with no additional reactive conformer, or $H_J$, with exactly one additional reactive conformer $J\in\{1,\ldots,N\}$. All labels, graph structure, stage probabilities, and the transition rule for 0 are supplied. The only unknown is the $N$-bit terminal reaction rule, promised to contain zero or one additional 1.

The acquisition interface is deliberately generous: an algorithm may choose **any** state and obtain its exact local transition row at unit cost. It can also generate paths, clone them, choose levels, query adaptively, randomize, and stop at a random time. State preparation, simulation of the known stages, and arithmetic are free in the lower bound. This is stronger than a forward-only molecular simulator. A full transition table or a source program exposing $J$ is *not* supplied. Total transition-row calls are the work measure; parallel calls reduce wall time only with proportional hardware. Query labels require $O(n+\log L)$ bits and exact output fractions require $O(n+L)$ bits. Charging force-field construction, experimental calibration, memory/communication, finite precision, and energy would increase costs, not remove the lower bound.

The exact answers are

\[
p_0=\frac{2^{-L}}{N+1},\qquad p_J=\frac{2^{1-L}}{N+1}=2p_0.
\]

The two allowed relative-error intervals, $[3p_0/4,5p_0/4]$ and $[3p_0/2,5p_0/2]$, are disjoint.

## Attempted operation and the actual gate

The attempted operation learns a trial committor $v$ from short paths, tilts trajectories toward $B$, and corrects the rate using a stopped residual. For an absorbing Markov chain and $v(A)=0,v(B)=1$, the exact identity is

\[
q(s)=v(s)+\mathbb E_s\!\left[\sum_{t<\tau_A\wedge\tau_B}(Pv-v)(X_t)\right]. \tag{1}
\]

For each stopped path, telescope $v(X_\tau)-v(s)$, condition each increment on its current state, and use $v(X_\tau)=\mathbf1_{\{X_\tau=B\}}$. This proves (1) without a model approximation.

If $v=q$, the Doob transition $P^q(x,y)=P(x,y)q(y)/q(x)$ on positive-$q$ states samples conditioned reactive paths with constant likelihood weight. That is the strongest conceptual comparator, not an invention here. Existing work already develops forward-flux efficiency calculations, statistically exact weighted ensembles, lag-corrected variational committors, and committor-based optimal control: [Allen et al.](https://arxiv.org/abs/cond-mat/0602269), [Zhang et al.](https://arxiv.org/abs/0810.1963), [Lorpaiboon et al.](https://arxiv.org/abs/2509.03539), and [Du et al.](https://arxiv.org/abs/2604.13213). These are primary sources; I inspected accessible abstracts and the 2025 committor paper's methods, not every implementation or dataset.

On $H_0$, a learned baseline can be exact: $v=q_0$. On $H_J$, the *same* $v$ has residual zero at every transient state except $(J,L)$, where $(Pv-v)(J,L)=1$. Thus every path or validation query that misses $J$ reports a perfectly harmonic candidate, while (1) still has an omitted correction $p_0$: the claimed rate is wrong by a factor of two. Ordinary forward paths see that residual with probability $p_0$. An exact empirical zero-residual finding on visited states is therefore not a global certificate.

Even granting **perfect, free conditioning through all $L$ barrier stages**, the unseen-channel cost remains. Let an importance proposal assign branch probabilities proportional to $1,\epsilon,\ldots,\epsilon$, with the known branch weighted 1 and every unknown branch weighted $\epsilon>0$. Under $H_J$, the unbiased estimator is $Y=2^{-L}\mathbf1_{\{I\in\{0,J\}\}}/((N+1)r_I)$ when branch $I$ is sampled from proposal $r$. Its relative variance is exactly

\[
\frac{\operatorname{Var}(Y)}{p_J^2}
=\frac{(1+N\epsilon)(1+\epsilon^{-1})}{4}-1.
\]

Only the base and hidden branches contribute to $\mathbb E Y^2$, giving $\mathbb E Y^2=2^{-2L}(r_0^{-1}+r_J^{-1})/(N+1)^2$; divide by $p_J^2=4\cdot2^{-2L}/(N+1)^2$.

Its best symmetric choice is $\epsilon=N^{-1/2}$, giving $(N+2\sqrt N-3)/4=\Theta(N)$. The uniform choice gives $(N-1)/2$. Setting $\epsilon=0$ omits the hidden path and makes the estimate biased rather than zero variance. Learning a good tilt on observed paths does not pay for finding an unobserved channel.

## All-adaptive acquisition lower bound

**Proposition, proved for the stated classical local-row oracle.** Any algorithm that meets the $1/4$-relative, $2/3$-success contract on $H_0$ and every $H_J$, including algorithms with adaptive queries and random stopping, makes at least $N/3$ expected candidate-terminal queries on $H_0$. If every execution is capped at $q$ such queries, then $q\geq N/2$. Exact identification in the worst case requires $N$ terminal queries.

**Proof.** Run the algorithm on $H_0$ with all its randomness fixed. Let $S$ be the set of distinct candidate terminal indices queried, and let $E$ be the event that the algorithm outputs a value in the $H_J$ relative-error interval. Correctness on $H_0$ implies $P_0(E)\leq1/3$. Choose $J$ uniformly and couple the run on $H_J$ to the $H_0$ run with identical random bits and oracle replies until terminal state $J$ is queried. Before that query the full transcripts, including all path, splitting, and learning states, are identical. Thus

\[
P_{J\text{ uniform}}(E)
\leq P_0(E)+\mathbb E_0\big[|S|\mathbf1_{E^c}\big]/N
\leq 1/3+\mathbb E_0|S|/N.
\]

Correctness for every $H_J$ makes the left side at least $2/3$, hence $\mathbb E_0|S|\geq N/3$. If $|S|\leq q$ on every run, retain the $\mathbf1_{E^c}$ factor to get $2/3\leq P_0(E)+(1-P_0(E))q/N\leq1/3+2q/(3N)$, hence $q\geq N/2$. To rule out every possible $J$ with certainty requires all $N$ rows. The expected-cost constant is attainable when $N$ is even: declare $H_J$ without querying on one third of runs; on the other two thirds inspect $N/2$ candidates, declare $H_J$ if found and $H_0$ otherwise. This succeeds with probability $2/3$ in both cases and uses expected $N/3$ terminal calls on $H_0$. The theorem therefore covers arbitrary estimators, not just the attempted tilt. □

The strongest exact classical incumbent for **this** information contract is to evaluate all $N$ unknown terminal rows and compute the rational $p$. It uses $N$ calls, $O(1)$ additional machine words (or $O(n+L)$ bits), and $O(N)$ arithmetic, matching the lower-bound order. FFS, weighted ensembles, adaptive multilevel splitting, learned reaction coordinates, and exact committor linear algebra may eliminate the separate $2^L$ path-barrier factor; the latter still needs the unknown rows. Coherent quantum oracle access changes the interface and admits $O(\sqrt N)$ search via [Grover](https://arxiv.org/abs/quant-ph/9605043), with an oracle lower bound in [Bennett et al.](https://arxiv.org/abs/quant-ph/9701001); building that coherent oracle, including state preparation and error control, is not free and was not done here.

## Executable comparison

Run `python3 benchmark.py > results.json` in this directory. [benchmark.py](benchmark.py) uses exact rational arithmetic for the rates and proposal variance, and exhaustively checks 508 small finite subset-coverage cases. [results.json](results.json) is the saved output. Its numerical entries illustrate the proven formulas; they are not molecular or physical data.

For $N=1024,L=8$: $p_0=1/262400\approx3.81\times10^{-6}$, while $p_J=1/131200\approx7.62\times10^{-6}$. Direct iid forward trajectories need 288,276 fixed trials to have a $2/3$ chance of *seeing the extra channel*. At that trial count the expected work is about 863,702 simulated transitions, including about 1125 unknown terminal-row evaluations; the latter is the information-bearing oracle cost. An exact terminal-row scan needs 1024 calls. Even a fixed-budget algorithm with free terminal preparation needs at least 512 such calls for the requested two-sided guarantee. The best symmetric importance tilt still has relative variance $1085/4=271.25$, versus $1023/2=511.5$ for uniform branch sampling.

## Redesign examined and status ledger

A pooled response that answers whether any branch in a chosen subset is reactive would permit binary group testing in $O(\log N)$ pooled questions. Constructing one such answer from the stated local oracle requires inspecting members of that subset, and repeated pooled tests do not beat the above information bound. A physical global-response measurement with constant cost and enough precision would be a **new acquisition interface**, requiring its own calibration and uncertainty accounting; no such mechanism is supplied or demonstrated. Similarly, a full analytic generator that exposes $J$ lets an incumbent read it cheaply. Neither is a same-information computational breakthrough.

| Claim | Status | Scope |
|---|---|---|
| Exact finite-chain rates and residual identity | PROVED | Stated absorbing-chain model |
| Importance-proposal relative variance and optimum | PROVED | Symmetric branch proposal, free ideal barrier conditioning |
| Adaptive/random-stopping $N/3$ and fixed-budget $N/2$ lower bounds | PROVED | Classical local-row oracle, promise $H_0$ or $H_J$ |
| Strongest exact incumbent attains $O(N)$ calls | PROVED | Same oracle and known topology |
| Any new method obtains the original rate output beyond the strongest incumbent at equal full cost | **NOT ACHIEVED** | No positive operation survives acquisition charge |
| Transfer to atomistic nucleation or actual measured rate | UNKNOWN | No atomistic model, real dataset, flux calibration, or physical validation |
| Novelty of this elementary search reduction | UNKNOWN | No comprehensive prior-art review; do not present as a new theorem |

The useful result is the precise gate: a globally valid rate certificate needs information about terminal reaction behavior on unvisited channels, or justified structure linking those channels to acquired states. Adaptive path generation and a perfect local residual on observed states alone do not provide it.
