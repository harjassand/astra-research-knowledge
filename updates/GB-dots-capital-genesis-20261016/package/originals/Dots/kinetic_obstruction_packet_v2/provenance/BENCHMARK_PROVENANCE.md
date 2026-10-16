# Benchmark, evaluator and baseline provenance

Inspected at Astra commit `3e8a972f2924272e1a89859d2f556b5b1f91d501`:

- `updates/FZ-positive-memory-genesis-20261016/package/originals/sources/kinetic_investigation/REPORT.md`
- same directory: `input_contract.json`, `MANIFEST.json`, `kinetics.py`.

The mechanistic source is Weng et al., *Tracking large chemical reaction networks and rare events by neural networks*, arXiv:2512.10309v1, https://arxiv.org/html/2512.10309v1.

The acquired governing-system file is `Machine-learning-and-complex-systems/NNCME:NNCME-2/nncme/systems/Schlogl_2d.py`, upstream Git blob `91ddf7778cca22beb83d261e372eb85ea32f44f0`. This pins the system-definition file, not a full training environment or learned checkpoint. Public source pointer: https://github.com/Machine-learning-and-complex-systems/NNCME/blob/main/NNCME-2/nncme/systems/Schlogl_2d.py.

The packet manifest lists no trained committor, learned importance-sampling policy, saved neural checkpoint or executable learned first-hit evaluator. Its report explicitly says no learned potential/rate/policy or generator approximation was used, and no neural-network code was executed. This is a statement about the inspected acquired packet, not proof of absence throughout all public literature or upstream branches.

The available matched executable baseline is `kinetics.py`: an independent NumPy/Numba implementation of direct SSA and standard fixed-level sequential splitting for the eight-site deadline-1 first-hit event. The source carries physical elapsed times through resampling and uses the original reaction dynamics. It defaults to unbounded counts (`cap=-1`). Its optional finite `cap` suppresses outward reactions, rather than adding an absorbing-overflow state, and therefore must not be used as if it supplied a one-sided FSP bracket.

Source-reported main benchmark: 12 independent runs, 256 particles at each of 17 interfaces max-count<=47,45,...,15; mean 3.8060689122e-8, empirical standard error 1.4263316151e-8 (37.475% relative); 1,283,689,381 primitive events; summed measured run time163.407s. These are source results, not rerun here and not a rigorous probability interval. The packet contains the twelve `split_rep_00` through `split_rep_11` JSON records and driver/summary scripts.

NNCME-2's M=85 neural experiment supports counts0,...,84 and computes an evolving distribution. It is not a trained first-hit evaluator or matched timing baseline for the unbounded eight-site deadline event. Its reported102.82 V100 GPU hours must not be compared directly with the splitting wall time. The source simulation observed count109, reinforcing that distinction.

`fsp_reference.py` and corresponding records concern a two-site T=.2 sampler diagnostic, not a certified eight-site inside solve. Those floating matrix-exponential outputs do not provide the needed first-hit certificate.

Receiving implication: there is currently no acquired trained first-hit model to seed a certified envelope. The immediate existing evaluator is the SSA/splitting implementation. A stronger certified representation requires new acquisition/training or a separately obtained, genuinely matched evaluator. Existing neural distribution code alone does not close that gap.

No upstream or packet code was executed in this inspection. The new certificate and search programs are independently written.
