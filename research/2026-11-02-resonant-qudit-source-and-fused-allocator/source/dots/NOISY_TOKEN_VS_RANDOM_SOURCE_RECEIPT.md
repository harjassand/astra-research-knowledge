# Noisy physical token versus random starts: exact two-check comparison

2026-11-01. **Positive comparator result on the actual finite device.** The noisy physical token removes the dilution tradeoff for this two-check example. This is neither a full-network scheduling theorem nor a noisy-qudit memory threshold.

## Results: g=gamma=handoff rate=1

Private 12-level apparatus for each of ZZ and XX; one shared physical token bit. All entries below are per check, with symmetry numerically verified. Token preparation is enabled only for the owner in PARK, at rate 1. Random-start preparation ignores ownership, at the listed pump rate; it retains exactly the same additional DONE dwell and handoff hardware.

| scheme | pump | token X-flip rate | retained wrong (p=0) | retained wrong (p=.001) | report flux |
|---|---:|---:|---:|---:|---:|
| token | 1 | 0 | <1e-15 | .00100000 | .06666667 |
| token | 1 | .0001 | .0000662797 | .00106615 | .06668608 |
| token | 1 | .001 | .000659917 | .00165860 | .06686014 |
| token | 1 | .01 | .00632301 | .00731037 | .06853785 |
| random | .1 | arbitrary, decoupled | .06399953 | .06487153 | .06030146 |
| random | .01 | arbitrary, decoupled | .00998576 | .01096579 | .00938853 |

Total two-check report flux is twice the last column. In particular, at token noise .001, the physical-token source has both better accuracy and higher throughput than either specified random-start baseline. This comparison does not claim random scheduling has been globally optimized over all possible controllers.

The increase of token flux with token noise is NOT a quality improvement: it accompanies unintended concurrency and more wrong reports. Probability both probes are active is approximately 0, .000161885, .00161351, .0156203 as token noise runs through the four values. It is .115249 and .00277776 for the two random baselines.

At zero noise, the ideal prediction is confirmed exactly to floating-point accuracy: each extraction takes mean 5.5 for two driven stages plus readout, one unit for launch, and one for handoff. Alternating ownership gives per-check flux 1/[2(5.5+1+1)]=1/15. No overlap floor remains.

## Actual finite native generator

Apparatus states 0..10 are the previously audited 11-level sequential source with state 0 renamed PARK; add state 11=DONE. Hamiltonian and collective stage-decay channels are unchanged. Readout is the onsite jump

    R_(a,s) = |DONE_a><final_a,s_X|,

with classical cache overwrite to s. It does NOT change the token. Each gate has the resonant two-body apparatus/data Hamiltonian. The which-probe-value coherence preservation of collective stage emission remains a physical reservoir premise.

Token scheme uses preparation jumps

    sqrt(1-p)|g1,+><PARK| tensor |a><a|_token,
    sqrt(p)  |g1,-><PARK| tensor |a><a|_token.

For each completing apparatus a, use TWO distinct handoff channels:

    |PARK><DONE| tensor |1-a><a|,
    |PARK><DONE| tensor |1-a><1-a|.

The first transfers ownership if a owns the token; the second parks a nonowner without changing ownership. Both have rate 1. These are native apparatus+token operations, not three-body conditions on the other sensor. Separate channels are essential: merging them coherently into one many-to-one token transition would add source cross terms and change the intended instrument.

The physical token fault is eta D[X_token], not an idealized classical error probability per round. No clean token reset or global clock is used. An initially idle nonowner cannot launch; a token flip during an extraction can launch the other source, and the subsequent conditional handoffs are computed rather than assumed harmless.

Random scheme uses the same onsite readout to DONE, preparation at rate r without ownership gating, and |PARK><DONE| tensor I_token at rate 1. The physical token and its X noise remain present but exactly decouple from the reports. Thus all token noise rates give identical random-baseline results; the numerical reduced solve suppresses this inert factor rather than imposing a clean token. The stored outputs label its representative rate .001.

## Exact reductions and validation

DONE and PARK both have identity prefix. Build every microscopic data-coupled term on dimension 12*12*4=576 and reduce only after checking the controlled-prefix Bell-sector isometry. Off-sector residual is at most 1.09e-15. All four dressed Bell sectors were independently evaluated and yield identical relative errors and fluxes.

Token-diagonal observable/density blocks are invariant: H is token identity, each conditional jump has a definite token source/destination, and X noise swaps the blocks. Initial token off-diagonal coherences cannot feed diagonal report observables. This is exact block closure, not a classical-clock approximation. Within each 144-dimensional apparatus block all quantum coherences and overlap-induced signs are retained.

For target readout gain maps J_correct,J_wrong and the actual full block generator L, solve

    L rho = 0, Tr rho=1,
    (L-J_correct-J_wrong) rho_wrong = -J_wrong rho.

The subtracted maps contain ONLY readout gain; all anticommutators and physical DONE/handoff dynamics remain. Retained error is Tr rho_wrong. It is not replaced by wrong-per-report frequency. Both wrong and correct cache densities are checked for positivity.

Across all 12 primary cases: steady residual <=2.01e-15; retained-cache residual <=2.48e-18; density/cache positivity holds up to roughly 1e-16 negative roundoff in the ideal-token zero-eigenvalue sector. No assumed independent source-progress law enters any solve.

## Physical and computational charges

Hardware: two 12-level apparatus, one noisy two-level token, two classical cache bits, two data qubits. Each stage interaction is apparatus/data; each ownership preparation/handoff is apparatus/token; readout and stage reservoirs are onsite apparatus operations. This is a finite-qudit model, NOT a completed compilation to low-dimensional physical qubits. Probe-coherent collective emission, level selectivity, finite-temperature upward faults, non-token apparatus faults, data faults, and coupling drift still require physical admission. Only token X faults and the optional convex preparation impurity were included here.

Mean number of actively extracting apparatus (excluding DONE) is .733333, .733559, .735585, .755117 for the four token noise rates, versus .673368 and .103516 for random starts. Mean DONE occupancy is respectively .133333, .133372, .133720, .137076, versus .120603 and .0187771. Remaining occupation is PARK. In steady state each completed report corresponds to one launch, two stage emissions, one readout and one handoff: total service-jump flux is five times total report flux, plus token flip events at rate eta. These event counts are not thermodynamic energy costs; reservoir energetics are not specified.

Largest numerical Liouvillian is 41472 by 41472 (two classical token blocks over 144^2), sparse throughout; no dense Liouvillian was constructed. Peak resident memory was approximately 137 MiB. Twelve parameter cases take a few seconds locally. Only 144-dimensional density blocks are densely diagonalized for positivity.

## Artifacts and scope

`coherent_lyapunov_memory_20261101/token_source_audit/run.py` contains the complete physical construction, block generator, retained-cache solve, population/resource summaries and positivity tests. `results.json` and `log.txt` contain primary results; `results_sector1.json` through `results_sector3.json` and associated logs verify the remaining Bell sectors. Run with `OPENBLAS_NUM_THREADS=1 python run.py`; optional `BELL_SECTOR=1,2,3` selects another sector.

Earned: a direct, noisy finite physical controller substantially beats the specified dilution-only source on identical augmented two-check hardware. Not earned: large-graph mutex/traffic scalability, a uniform perturbation theorem for every controller fault, autonomous-qubit realization, practical memory threshold, or superiority over every strong conventional controller.
