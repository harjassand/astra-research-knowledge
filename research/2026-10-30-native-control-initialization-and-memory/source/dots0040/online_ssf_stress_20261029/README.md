# Ideal atomic asynchronous SSF: finite stress diagnostic

2026-10-29. No physical-controller validation, threshold claim, or asymptotic expander-family claim.

## Reproduce

Python 3.10+ standard library only; no package installs or external state mutation.

```sh
python stress.py --trials 200
python traps.py
python diagnostics.py
```

The recorded main run took 39.81 seconds. `results.json` contains all 800 independently seeded, paired trajectories at four observation times (1,600 scheduler trajectories), code matrices, parameters, exact verification counts, and summaries. `run.log`, `traps.json`, and `diagnostics.json` are the other outputs. Raw rows include seeds and evaluation/noise counts. No selected seeds were discarded.

## Construction and exact checks

Classical H is explicit cycle incidence: H[i,j]=1 iff j=i or j=i+1 modulo L. For L=3, H=[[1,1,0],[0,1,1],[1,0,1]]; for L=4, H=[[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]]. Use HX=[H tensor I | I tensor H^T] and HZ=[I tensor H | H^T tensor I]. Integer row masks and explicit H matrices are saved.

| L | N | rank HX | rank HZ | k | exact X/Z distance | syndromes/sector |
|---|---:|---:|---:|---:|---:|---:|
|3|18|8|8|2|3|256|
|4|32|15|15|2|4|32768|

Verified HX HZ^T=0; GF(2) ranks; all stabilizer combinations; minimum-syndrome representatives via breadth-first search on the complete syndrome graph; direct syndrome updates for **46,080 + 10,485,760** candidate/syndrome pairs; positive accepted descent; 100 single-qubit sector burst recoveries; and explicit nontrivial zero-syndrome logical witnesses. Distances were found by exhaustive increasing-weight kernel enumeration through L. BFS edge lengths are unit bit flips, hence its representatives are exact Hamming minima. Ties are fixed deterministically by queue insertion/qubit order. No approximate matching decoder is used.

Full FGL equation-(5) family is enumerated at every stabilizer hub: all nonempty subsets F of its four-qubit support satisfying |sigma(F)| >= d_A |F|/2, d_A=2. Every hub has 10 candidates (not singleton-only or sampled candidates). Beta=1/2; accept iff 2 Delta >= |sigma(F)| > 0. Choose maximum Delta, then smallest support, then smallest numeric mask. Every evaluation considers the entire family.

## Online model and fair baseline

Start with encoded identity error, no syndrome noise. Independent Poisson rate lambda=1 **per sector hub**; each ring reads the exact current syndrome and atomically applies the chosen accepted move. Use superposition/thinning: aggregate rate equals number of hubs (18 or 32); independent uniform hub labels give independent Poisson hub processes. Both X and Z sectors are active. Per-qubit independent rate epsilon depolarizing Poisson kicks choose X/Y/Z equiprobably. Rates epsilon={0.002,0.02}; horizons {1,10,50,100}. A Y kick enters both sector errors at the same time.

Round-robin visits all the same sector hubs cyclically **at the identical aggregate Poisson tick times**, with the same noise realization. Thus every paired prefix has exactly the same number of evaluations and noise kicks, not merely equal expected budgets. It is round-robin service, not a deterministic-period clock. Both policies have identical syndrome information, candidate families, beta, and tie-breaking. The baseline is not deliberately weakened. No syndrome-informed hub selection occurs in either policy. Each evaluation has ten candidate tests for both codes and policies.

Idealizations: zero gate/read/reset duration, noiseless classical decision, unlimited instantaneous serial throughput at a tick, no locks/conflicts, no stale reads, no controller faults, no geometric routing, and no correlated/coherent bath noise. No global recovery or reset is applied during the trajectory. Pauli stabilizer tracking is exact for this stochastic Pauli model, not a simulation of general CPTP bath dynamics.

Terminal decoding is mathematical: for each sector find the fixed exact minimum-weight representative R of the observed syndrome; failure iff E XOR R is outside the same-type stabilizer row span in either sector. The diagnostic never writes R into the online state. Weight of a residual Pauli alone is not used as a logical-failure test. `first_decoded_failure` records first event at which this mathematical decoder would fail, not an irreversible absorption time: later errors can undo a logical error. Snapshots are dependent observations of the same trajectory.

## Main results at t=100

Wilson 95% intervals are marginal binomial intervals for each endpoint; not simultaneous intervals. There are 200 trials in every row. Zero observed failures does not establish zero risk.

| N | epsilon | scheduler | failures/200 | 95% interval | mean syndrome weight |
|---:|---:|---|---:|---|---:|
|18|0.002|async|0/200|0.000–0.019|0.030|
|18|0.002|round_robin|2/200|0.003–0.036|0.000|
|18|0.02|async|148/200|0.675–0.796|0.510|
|18|0.02|round_robin|133/200|0.597–0.727|0.420|
|32|0.002|async|9/200|0.024–0.083|0.130|
|32|0.002|round_robin|2/200|0.003–0.036|0.110|
|32|0.02|async|175/200|0.822–0.914|1.250|
|32|0.02|round_robin|159/200|0.734–0.845|1.010|

## Useful failures and interpretation

1. **Low syndrome is not memory success.** At epsilon=0.02, N=18 asynchronous failure rises from 1/200 at t=1 to 23/200 at t=10, 107/200 at t=50, and 148/200 at t=100, while mean syndrome weight remains 0.33–0.51. At t=100, **115/200 trajectories have exactly zero syndrome and a nontrivial logical error**. N=32 has 99/200 such silent failures. This directly exposes a syndrome-only success metric as invalid.
2. **Full-family SSF has small-code traps.** On N=32, exhaustive weight-2 X-error enumeration finds 32 nonzero-syndrome local minima. Example: qubits {0,1}, syndrome mask 10, exact minimum-syndrome weight 2. No accepted FGL move exists anywhere. No such nonzero-syndrome trap was found through weight 4 on N=18 (this is not a full-state guarantee). All isolated single-qubit sector errors recover under noiseless fair sweeps.
3. **No numerical async advantage established.** The fair round-robin baseline has lower endpoint point estimates in three of four configurations. Paired discordances at high noise are async-only/RR-only failures 42/27 (N=18), 33/17 (N=32). These are finite-code observations, not a universal scheduler ordering or formal significance claim.
4. **Not a theorem counterexample.** These cycle graphs are not verified FGL expanders and in fact fail the required small-set expansion once the tested classical subset cutoff includes two adjacent vertices: their neighbor union has size 3 versus degree sum 4, requiring delta >=1/4. No meaningful asymptotic confinement cutoff or D0/D1 constants is assigned. N=32 performing worse than N=18 is not evidence against an expander-family scaling theorem.
5. **Accounting assertions passed.** Every accepted correction strictly lowers current syndrome, every cached syndrome agrees with direct recomputation after correction, and accepted count never exceeds total noise-induced syndrome upper budget. This checks the atomic implementation interface, not deterministic witness statements D1 or physical compilation.

Stop condition: the diagnostic has exposed online logical accumulation and a strict-descent trap while validating candidate enumeration, exact logical readout, and a fair scheduler comparison. Larger benchmarks would not repair the absent expander hypotheses or validate the physical compiler, so none were run.

## Governing sources

- Local `../ldpc_memory_bridge_20261029/DERIVATION.md` and `ASYNCHRONOUS_WINDOW_WITNESS.md`.
- Local `../coherent_atomic_ssf_20261029/SPACETIME_CPTP_MEMORY.md` (conditional theorem, not certified here).
- Fawzi–Grospellier–Leverrier, equation (5), Algorithm 2: https://arxiv.org/html/1808.03821 . This defines the candidate filter; no theorem constants are fitted from these runs.
