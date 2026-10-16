# Final stable adversarial audit addendum

16 October 2026. This note fixes the state of my independent audit for the root synthesis. Details and provenance are in `REPORT.md`. All claims below concern the **modified** local candidates, not either pinned paper's original generator.

1. **s01 radius-two `B(P)` counter repair:** I found no error in the completed local proof for at most two counter faults. Its distance-four classification follows from crossed-tile pinning: any changed site needs a full changed incident tile, and with four changes that uniform tile moves by one valid gate step. The off-target moat case then cannot validate an unseen exterior fault. This proves a counter-control endpoint with at most one *charged gate-location debt* within the theorem's exact assumptions; it does not prove a decoded quantum channel or threshold. Independent finite evidence: L4 exhaustive 270,480 two-site residue substitutions and 210,123,032 Hamming-one-to-four fields; 100,000 sampled two-fault episodes each on L6 and L8, including both possible repair-event orders. All checks passed. The 210-million-field calculation is finite evidence, **not** a size-uniform proof.
2. **Remaining s01 traps:** Three counter faults `(1,2,3)` on one even tile defeat `R+B`, as s01 itself reports. Independently, two onsite faults can split the four reused program copies `w,w,w,w` into `w',w',w,w`. `G` has no three-copy majority; every `A(v,p)` sees a 2–1 split; `R/B/C` are inert on clean counters/colors. After all other even gates run on L4, no state-changing ideal jump remains (`s01_program_split_trace.py`). Three equal wrong copies can instead establish a persistently wrong program word. These cases are outside the two-**counter** theorem, but inside the physical onsite-control alphabet and block a general fault-damage/service theorem until a program eroder, one-use source, or equivalent repair is supplied.
3. **s03 revised one-use receiving gadget:** Its earlier raw-A-occupancy gate guard had a positive-probability leakage stall (`s03_vacancy_guard_trace.py` records that historical branch). Revised erasure-transparent `G/H` qutrit extensions remove it. The current `T` row atomically discards unowned B before A recovery and transfer, without a B-vacancy guard. For a local A/B fault Kraus `M_α` with B initially vacuum, the induced A Kraus maps after B discard are `⟨b|_B M_α |perp⟩_B`; they remain one-site qutrit errors and are in the code's prescribed Gram/KL recovery span. This repair is valid only because no live incoming packet occupies B before T. A sole post-T B fault belongs to the separately named final decoder. The one-use noncommuting `C_L X_L` numerical algebra script passed, but an atomic five-site terminal jump, noisy static program/color, growing-level compiler, protected idle, and general damage erosion remain outside the finite theorem.
4. **s02 recombination:** The present four-bank table handles the tested one-site wrong-bank phantom and clean one-use/carousel steps at its ideal atomic level. My earlier phantom CNOT chain is a lineage/EC-cut stress trace; its N wrong target values do not imply N faulty gate locations. I found no new decisive counterexample to s02's stated restricted lemmas. Its own multi-fault surface, encoded operation compiler, protected waiting, and recursive drain remain open.
5. **All-history algebra:** Exact path-span/KL saturation is a safety test for a supplied closed finite controller and primitive-fault budget. It does not quantify omitted bad-branch weight, termination, or physical-time output error. The stopped one-qubit Z example in `weighted_episode.py` has exact error `2p/(λ+2p)` while all-path KL fails for every `p>0`. A persistent wrong program word can emit arbitrarily many wrong output packets at zero additional primitive-fault cost; a valid hierarchy must bound that source's full port shadow or consume it once.

## Replay and resource receipt

Run from this directory:

```sh
python3 s01_program_split_trace.py
python3 s03_vacancy_guard_trace.py
python3 weighted_episode.py
clang++ -O3 -std=c++17 moat_l4_exhaustive.cpp -o moat_l4_exhaustive
./moat_l4_exhaustive < L4_CLEAN_STATES.txt
clang++ -O3 -std=c++17 moat_random_interleavings.cpp -o moat_random_interleavings
./moat_random_interleavings 6 100000
./moat_random_interleavings 8 100000
```

The saved `MOAT_*.txt` files are the matching output receipts. s03's own `finite_discharge_check.py` and `quantum_recovery_check.py` were rerun locally and passed (`32` clean counter cuts, `4,480` single-counter perturbations, `96` two-fault forks, and 31 qutrit error images with maximal floating-point KL scalar residual `1.18e−15`). The terminal Kraus reduction above is analytic; the floating-point check does not certify it. These runs used the local CPU through Python and Clang; tool-reported wall times were about 1–6 seconds per script/run. Exact CPU accounting was not recorded. Model-inference compute, energy, monetary cost, and any external validation are unknown. No GPU, publication, cloud experiment, PR, or shared archive change was used for this worker's tests.
