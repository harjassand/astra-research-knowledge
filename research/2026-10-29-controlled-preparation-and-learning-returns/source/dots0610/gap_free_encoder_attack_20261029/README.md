# Gap-free online encoder learning — 2026-10-29

## New capability and actual scope
A proposed finite controller learns a useful local-frame encoder from ordinary product-Pauli probes without identifying the full frame or requiring a positive excitation gap. The source may retain causal quantum memory, but its joint operations must lie in one fixed unknown locally rotated collective algebra for the readiness guarantee. Arbitrary-noise guarded soundness is inherited from the separate physical-orbit/outer-code construction, not inferred from the structural promise. Neither broad arbitrary-noise capacity nor physical hardware advantage is established.

The key link is a positive star-swap task loss: the same actual probe shot supplies unbiased feedback for every candidate relative rotation. The full-singlet Poincare bound plus physical permutation orbit transfers learned loss to a chosen small code. Exact rational online updates give polynomial but potentially enormous classical cost. Three-role validation/service interleaving gives conditional readiness tending to one, without future-noise extrapolation.

## Governing files and supersession
1. `GAP_FREE_ONLINE_THEOREM_v1.md`: core task loss, shared feedback and star-Poincare transfer. Its linear net approximation is superseded by v2; its exponential update is not the exact integer implementation.
2. `QUADRATIC_NET_AND_FINITE_ARITHMETIC_v2.md`: quadratic common-zero approximation, rational quaternion net, integer multiplicative weights and exact capped sampling. This governs the finite arithmetic claim.
3. `THREE_ROLE_GUARDED_READINESS_v3.md`: finite stopping roles, model-free accepted soundness and family-conditional readiness. The explicit constant source-exposure rate is not gate/time/hardware rate.
4. `DIRECT_SMALL_CODE_TRANSFER_OBSTRUCTION_v1.md`: pointwise obstruction to transferring the same unweighted star losses directly to a fixed small code, including the full product four-spin block code. Completed fidelity is derived explicitly and extended to every noiseless-exact left-inverse decoder. This is not an all-algorithm learning lower bound.
5. `ROOT_SYNTHESIS_AND_OBLIGATIONS.md`: earlier working orientation, NOT governing where later files resolve or qualify its open items.

Independent receiving review is in `producer-workspace/gap_free_encoder_audit_20261029`; current acceptance scope and file hashes should be read there. Do not treat this README as a substitute for that review.

## Executed reproducible evidence
- `check_gap_free.py` / `.json`: 20,000 actual sampled probe/service calls on four spins plus retained coherent bath; shared bank, nonstationary source and averaged private-orbit service interface.
- `check_gap_free_200k.py` / `.json`: 200,000-round extension. Floating online update, finite27-element candidate set containing true frames; no execution of the large outer code.
- `check_gap_free_one_axis.py` / `.json`:60,000-round permanent one-axis, continuously nonidentifiable source; scope in `PERMANENT_ONE_AXIS_FIXTURE.md`.
- `check_exact_kernel.py` / `.json`: exact rational SO3, integer update and capped sampler identities, including forced32-rejection boundary. Synthetic records, not a physical probe simulation.
- `check_loss_moments.py` / `.json`: exhaustive probe outcome moments for24 arbitrary nonunital two-qubit CPTP channels.
- `check_small_code_obstruction.py` / `.json`: direct physical subspace/reset calculations and exact rational asymptotic ratio bounds.
Programs use Python, NumPy and SciPy as imported; run from any directory and redirect printed JSON if a program does not write it itself. No empirical claim is inferred from a theoretical asymptotic guarantee.

## Dependencies and strongest alternative
This builds on the received nonunital collective-frame acquisition bank, physical permutation-orbit CP memory closure and matching guard, and constructive arbitrary-error outer CSS compiler. Earlier scoped quantum-undecidability work is not a load-bearing dependency of this theorem. Read those governing source proofs for the complete physical interfaces. A high-rate singlet subcode with full-path ordinary logical tests attains the same polynomial learning-transfer order within a constant; the orbit is not claimed uniquely necessary. Cheap product-block matching and six-state tests remain strong verification baselines.

## Remaining practical and scientific obligations
Finite physical gate synthesis/calibration costs, trusted control/private roles, quantum buffers, and outer preparation/decoding remain paid interfaces. The simple exact learner is polynomial but inefficient. No comparative sample/gate optimality or historical novelty established. The useful next attack is a better controller with comparable rigor and honest total-resource comparison, not a stronger extrapolation from the small simulations.
