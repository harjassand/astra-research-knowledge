# Own matched 4D memory pilot

This is independently written code implementing a classical Pauli trajectory for one CSS sector of a periodic 4D toric memory. No author-supplied simulator or external dependency was downloaded, installed, or executed. This compares the supplied theorem's exact exogenous Poisson vertex sweep with a **matched Poissonized 4D Toom adaptation**, not the original paper's parallel schedule/results.

## Reproduce

```
g++ -O3 -std=c++17 -Wall -Wextra simulator.cpp -o simulator
./simulator test
python run_pilot.py
```

The runner requires `PILOT_GATE_APPROVED.txt` from the independent review gate. `manifest.json` fixes parameters, seeds, RNG transformation, decoder, bit ordering and resource cap. `SHA256SUMS` pins the validated source and executable. `pilot_raw.jsonl` contains one verified endpoint per line; `pilot_resources.json` records aggregate pilot resources. A rerun overwrites raw pilot files. `audit_simulator` is the independent verifier's frozen copy, when present.

A single endpoint is available with `./simulator trial 16 0.01 5 2026101501 sweep`; the final argument can be `toom`. The implementation fixes kappa=1 and accepts finite nonnegative alpha and T. A trial at an odd L or L<4 is rejected. The algebra/decode interfaces allow L2..64 for testing; that is not an authorization to run a larger grid.

Independent interfaces: `./simulator decode L` takes whitespace-separated occupied syndrome edge IDs on stdin, returns fallback 0/1 and then recovery face IDs. `./simulator kernel L sweep VERTEX` or `... toom FACE` reads the same input and returns proposed face IDs. The kernel interface permits synthetic syndromes to test local rules; an odd outgoing trailing pattern raises an invariant error.

## Semantics and checks

Total correction-attempt intensity is L^4 for both methods. Sweep attempts are rate 1 per vertex; Toom is rate 1/6 per face. Each face's physical X-noise rate is alpha. Each method includes null proposals. The complete accumulated error chain is retained when syndrome disappears. All sweep faces are chosen from old syndrome before toggles, so two-face events never cascade. The Toom face decision reads its north and east syndrome edges without an incoming-edge veto.

Both methods receive exactly the same syndrome-only deterministic readout. Every syndrome component must have a consistent integer lift and strict ambient wrapped infinity diameter<L/8 to use local prism filling. Otherwise the whole syndrome is recovered by fixed dense tensor contraction H. Decoder selection never receives E or the trajectory. Only after recovery is selected is E used to score six cut parities of the verified closed residual. Fallback is a complete algebraic recovery, not unresolved; its logical decisions can be poor and are decoder-specific.

Built-in tests exhaust all 393216 L16 single-face faults including seams, all cube boundaries at L3,4,16, each active sweep pattern/veto, every cut for six sheets at odd/even L, and 2000 random/scripted incremental updates against an independent gather-form syndrome. External audit checks tuple-cell incidence, ranks, dense-H agreement, syndrome-only invariance and truth tables separately. See verifier outputs.

## Interpretation

This pilot has only three independent seeds per positive noise ratio and one zero-noise sanity endpoint per method. Matched methods share random proposal times/types/noise locations within a seed, and must not be pooled as independent trials. A zero count out of three has one-sided 95% binomial upper bound 1-0.05^(1/3)=0.6316. Endpoint outcomes do not estimate first-failure lifetimes and establish no threshold, asymptotic exponent, theorem finite-size applicability, physical energy/resource advantage, or optimal decoder performance.

Syndrome inspection counts are algorithmic logical reads (8 versus 2 per attempt), separate from decoder and invariant-check work; they are not hardware memory transaction counts. RSS is OS high-water resident memory for completed child processes, and the runner enforces a 1 GiB virtual-address cap and aggregate 180 CPU-second limit.

## Later separately authorized diagnostics

PHASE2_RESULTS.md records the unchanged-binary L32 diagnostic. PHASE3_RESULTS.md records the separately versioned equal-expected-check-read Toom adaptation. Its code is simulator_equalreads.cpp and its gate/hashes are separate; the original simulator and results are preserved. These remain base instantaneous Pauli trajectories, not finite-gate/shared-bath theorem tests. No broader experiment follows automatically.

PHASE4_RESULTS.md records a separately authorized selected-endpoint readout sensitivity diagnostic. Separate simulator_readouts code preserves D0 and predefines syndrome-only D1/D2; exact endpoint and recovery artifacts are versioned and hashed. This diagnostic must not be treated as an unbiased performance comparison.
