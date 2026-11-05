# Exact-rational static acquisition for a correlated rare-failure law

## Completed operation

This package implements the missing static operation in the parent correlated-reliability construction. Given explicit positive rational Gibbs factors on binary network-edge failures, it estimates pinned partition sums using ordinary pinned heat-bath draws, assembles a cut-union probability estimate by inverse multiplicity, and samples configurations conditioned on the union by rejection. The actual demonstration uses all cuts of a small graph, so its union is exactly the disconnection event.

Run from any directory:

```bash
python /workspace/scratch/2958277fc089/next3_gibbs_code/run_demo.py
```

Python 3.12 and a C++17 compiler are sufficient; no Python package dependencies. The native accelerator is compiled automatically. It supports up to 60 binary variables and transition denominators up to 128 bits. The core automatically uses arbitrary-precision Python arithmetic when those accelerator limits are exceeded. The reference enumerator has a separate explicit 18-variable cap and is not imported by the acquisition core.

## Results of the recorded execution

The fixture has 6 vertices, 10 nonsymmetric edge-failure variables, 10 pair interactions, 31 cuts, and 1,024 reference states. Five extremely reliable edges form a spanning tree. The remaining fields are moderate and unequal. One rare–rare pair has interaction multiplier `2^40`; the other nine pair multipliers are unequal rational numbers. Exact rational calculations certify Dobrushin coefficient 0.37311872909698995 and logarithmic contrast `c=3`. The ordinary odds contrast is approximately `1.8325193796267e12`.

| Quantity | Recorded result |
|---|---:|
| Exact disconnection probability | 3.7252956888856366e-28 |
| Acquired probability estimate | 3.800863790182855e-28 |
| Point relative error | +2.0285% |
| Executed confidence interval | [2.894287567127758e-28, 4.754035930511187e-28] |
| Same-marginal independent-edge probability | 1.979382140288482e-28 |
| Correlated / independent probability | 1.8820497634391604 |
| Acquired pinned partitions | 32 |
| Sampled marginal stages | 32 |
| Draws per sampled stage | 12,904 |
| All partition intervals cover exact reference | yes |
| Maximum partition point relative error | 2.0088% |
| Accepted conditional failed configurations | 8,192 |
| Empirical conditional histogram TV | 0.0184463 |
| Maximum conditional marginal error | 0.0085651 |
| Per-output analytic acquired-weight TV bound | 0.1456747 |
| Per-output additional mixing TV bound | 6.2e-7 |

The empirical histogram distance includes finite output-sampling variation. It is not a bound on the output law. The simple joint-TV bound for 8,192 outputs is 1 and therefore vacuous. All confidence statements are conditional on ideal independent fair randomness and include the statistical budgets below; the recorded seeded-PRNG execution is a reproducible numerical diagnostic.

### Actual execution costs

| Phase | Pinned draws | Heat-bath updates | Seconds |
|---|---:|---:|---:|
| Heavy-prefix partitions | 412,928 | 27,821,024 | 1.060 |
| Cut-union probability | 8,192 | 2,220,856 | 0.264 |
| Conditional configurations | 16,384 | 5,038,286 | 0.463 |
| Total acquisition | 437,504 | 35,080,166 | 1.786 |

The conditional phase generates batches and consumes 8,192 of its 16,384 proposals. Those unused proposals are counted. Total wall time including exact validation, compilation, and serialization was 2.992 seconds on this environment. This is one execution, with no performance-generalization claim.

Total primitive counts: 70,160,332 heat-bath integer random operations, 97,645,560 native 64-bit PRNG words, 32,768 Python integer random operations, and 41,428,350 Python PRNG bits. There were 42 native sample batches. Each draw restarts independently at its pinned assignment with all unpinned bits zero. Nontrivial chains used 48–335 updates. Transition denominators required at most 98 bits. The exact categorical weight total required 1,075 bits. Every random-integer rejection has a fixed attempt cap and returns an explicit error if exhausted.

### Confidence schedule actually used

Each sampled marginal uses halfwidth `1/40`, sampler TV tolerance `1/10000`, a maximum of 320 sampled stages, and total marginal failure budget `1/100`. Exact local conditional envelopes replace sampling whenever their width is at most twice the stage halfwidth. Cached prefixes reuse already acquired marginal intervals. Thus only 32 of the 320 allowed sampled stages are needed.

The inverse-multiplicity mean uses 8,192 proposals, additive halfwidth `1/32`, proposal TV tolerance `1e-7`, and failure budget `1/100`. The probability interval reported above therefore has failure probability at most `0.02` plus random-cap failure under the ideal-bit model. It does **not** claim a fixed 10% relative error guarantee: its width is about -22.3% to +27.6% around the exact reference. The point relative error happens to be 2.03%.

The conservative parent schedule for `epsilon=0.1`, `delta=0.01`, 32 queries and 10 variables is separately computed: marginal halfwidth `0.000625`, 81,920,000 draws per stage, 26,214,400,000 pinned draws, and an upper bound of 6,291,456,000,000 heat-bath updates. That schedule was not executed. The completed experiment demonstrates the operation and reports valid local intervals, rather than silently substituting its smaller budget for the parent's whole-theorem schedule.

## Why the operation is valid

### 1. Pinned heat bath with an explicit TV bound

Let `c_ij` be the exact maximum change in bit `i`'s Bernoulli conditional when only bit `j` changes. Local factor tables allow these influences to be computed by enumerating the local neighborhood. Assume their maximum row sum is `chi<1`. Pinning variables cannot increase this row-sum bound.

For `p` active variables, couple two random-scan heat-bath chains by using the same chosen coordinate and maximally coupled Bernoulli resampling. If `d_i(t)` is the disagreement probability in coordinate `i`,

\[
 d_i(t+1)\le(1-1/p)d_i(t)+(1/p)\sum_j c_{ij}d_j(t).
\]

Therefore the maximum coordinate disagreement contracts by at least `1-(1-chi)/p`; a union bound gives TV at most

\[
 p\exp[-t(1-\chi)/p].
\]

For a rational target `tau`, the code computes `L=ceil(log2(p/tau))` by integer comparisons and uses `ceil(p*L/(1-chi))` updates. The bound is at most `p*2^-L<=tau`. This argument uses the maximum-coordinate recurrence, avoiding an incorrect substitution of a row-sum condition into an unweighted Hamming column-sum argument.

### 2. Heavy-prefix counting from sampling

For a pin set `A`, sequentially estimate a remaining bit marginal and select its empirically heavier branch. Multiply the estimated selected branch masses and evaluate the final configuration's exact weight:

\[
 Z_A=W(x_*)/\pi_A(x_*).
\]

Every selected empirical branch has mass at least one half. With additive marginal error `a`, its true mass is at least `1/2-a`, so relative product control does not require observing a rare configuration. This is the classical sampling-to-counting self-reduction of Jerrum, Valiant, and Vazirani, used here with explicit rational Gibbs weights and uniformly pinned heat bath; it is not a new primitive attributed to this package.

The local interval `[q_min,q_max]` is also an exact interval for any partially conditioned marginal by the tower property. When its width is small enough, the code uses its midpoint and keeps the whole exact interval. Otherwise, it estimates the marginal using `n` independent fresh chains. Projection of the observed mean onto the exact interval cannot increase error. Choosing

\[
 n\ge \frac{\lceil\log_2(2M/\delta)\rceil}{2(a-\tau)^2}
\]

makes a union bound over at most `M` sampled adaptive stages valid. All branch lower and upper masses are multiplied as fractions, then inverted, producing an interval for `Z_A`. Adaptive pin choices cause no problem: each fresh sample batch satisfies its concentration bound conditional on previous stages. The cache never introduces a new estimate without accounting for it.

### 3. Inverse multiplicity and acquired weights

For cuts `D_j`, let `E_j` mean every edge in `D_j` failed. Let `Z_j` be its pinned partition sum and `c(x)` the number of listed cut events containing `x`. With exact weights, choosing cut `j` proportional to `Z_j` and sampling `pi(.|E_j)` gives proposal density

\[
 Q(x)=W(x)c(x)/S,\qquad S=\sum_j Z_j.
\]

Thus `S E_Q[1/c]=Z_union`, and accepting with exact probability `1/c` yields the union-conditioned Gibbs law. With acquired weights `hat Z_j`, define

\[
 h(x)=\frac1{c(x)}\sum_{j:x\in E_j}\frac{\hat Z_j}{Z_j}.
\]

The acquired partition intervals certify `s_lo<=h(x)<=s_hi`. Then `hat S E_Q[1/c]` lies between `s_lo Z_union` and `s_hi Z_union`. Combining these inequalities with the unconditioned partition interval yields the recorded probability interval. The accepted law is proportional to `W(x)h(x)`, with conservative TV bound `(s_hi-s_lo)/(2*s_lo)`.

Each pinned proposal has support within the union and `1/c>=1/J`, even when its Gibbs draw is approximate. Proposal TV `tau` adds at most `2J*tau` to the accepted law. Each conditional output is capped at `J*ceil(log2(n/beta))` proposals, yielding a union abort bound at most `beta` for `n` outputs. The fixture uses cap 1,023 per output, total cap 8,380,416, with `beta=1e-6`.

### 4. Precision, access, and memory

The model input comprises explicit positive rational local factors. All full-conditional probabilities, influence bounds, partition products, configuration weights, cut mixture weights, and reported confidence endpoints are exact fractions. Neither arbitrary-precision physical measurements nor a hidden rare-event oracle are assumed. Logarithmic run budgets use integer comparisons; the rational lower surrogate for `-ln q` is also implemented.

The accelerator accepts only conditional integers fitting in 128 bits and rejects malformed/overflowing inputs. Python handles arbitrary-precision fractions and falls back to Python heat bath when necessary. Rational integer sampling draws enough bits to cover its denominator and rejects the excess range; each attempt accepts with probability at least one half. Fixed rejection caps give an explicit abort event. The heat-bath cap union bound in this execution is below `7.05e-14`; the Python integer-sampling bound is below `7.89e-23`. The mathematical probability statements use fair bits, whereas both `mt19937_64` and Python's seeded generator in this run are reproducibility devices.

This implementation constructs exact conditional tables and influence bounds by enumerating local neighborhoods, with table cost proportional to `sum_i 2^d_i`, where `d_i` is the number of neighboring variables. The fixture has maximum `d_i=3` and 46 conditional-table entries. The code does not claim a polynomial procedure to discover influence certificates on arbitrary unbounded-degree inputs; the parent general theorem accepts certified bounds as explicit input.

Core storage consists of explicit local tables, cached acquired prefixes, per-query rational products, and one proposal batch plus its histograms. No full global state table is supplied to the engine. At the demonstration size, the full reference table is held only by `exact_reference.py` for validation. The largest generated proposal batch is 16,384 states.

## Verification and limits

The reference exhaustively confirms all 10,240 local conditionals, all 1,024 cut-support identities, and the exact inverse-multiplicity identity. For the complete cut family it verifies `c(x)=2^(components(x)-1)-1`, including states with multiple failed cuts. All acquired partition intervals and the acquired failure interval contain the exact reference, and every conditional output is disconnected.

All observed proposals in this extremely rare fixture had multiplicity one. Extra component splits require additional rare failures. The implemented multiplicity correction is therefore tested algebraically on every state, but this run is **not an empirical overlap stress test**. The graph's correlated probability differs substantially from the same-marginal independent reference, so the correlation is consequential despite that overlap limit.

The recorded fixture fits the parent theorem's direct-enumeration branch: for `h=0.1`, `c=3`, and `C=6`, the cutoff multiplier is `a=15`, so `v=6<=2a`. The rational minimum cut weight is approximately 34.6676062955; the largest cut weight, 246.814184699, is below `a*lambda=520.014094433`. Thus all 31 cuts are retained. Direct enumeration has `2^(v-1)<=v^(2a)` cuts in this branch. These branch and cutoff values were supplied by the parent's proof calculation after the recorded run; no further acquisition run was needed. The scalable contraction-based branch is not implemented in this package. No time-dependent CDF experiment is included. Access begins with the specified exact local factors.

The executable uses exact rational random-scan transitions with explicit finite random-bit rejection caps and abort events. The parent proof also gives a systematic-scan dyadic implementation with a deterministic bit budget. Those are distinct finite implementations of pinned Gibbs sampling; the result here uses only the explicitly recorded random-scan bounds and costs.

Files:

- `gibbs_static.py`: acquisition core and fixture.
- `pinned_heatbath.cpp`: exact rational finite-step accelerator.
- `exact_reference.py`: isolated exhaustive static reference.
- `run_demo.py`: actual execution and exact validation.
- `results.json`: complete exact-rational results, settings, and cost accounts.
- `run_stdout.txt`: recorded short execution transcript.
- `TO_ROOT_RESULTS.md`: report-ready checkpoint.

Primary antecedent: M. R. Jerrum, L. G. Valiant, and V. V. Vazirani, *Random generation of combinatorial structures from a uniform distribution*, Theoretical Computer Science 43 (1986), 169–188, DOI [10.1016/0304-3975(86)90174-X](https://doi.org/10.1016/0304-3975(86)90174-X). Heat-bath contraction and inverse multiplicity are established mechanisms; the package's contribution is the completed finite static acquisition operation under the explicit hypotheses, with the rare correlated fixture and cost accounting above.
