# Verdict on the uniform finite-horizon refinement

The refined target preserves the decisive finite-seed cone obstruction and removes an unnecessary autonomous-growth requirement.

## Precise quantifier order

Fix the spatial dimension, a burst-radius law with finite dth moment, a finite-range gate set, bounded local rate and information speed, bounded hardware density, and an operating accuracy such as 1/4. The positive theorem should establish:

- a sufficiently small positive intensity range;
- a finite commissioned input-dependent seed radius r_0, allowed to depend on the burst law, intensity and target accuracy but not on the requested horizon T;
- one uniform algorithm which, given T and the allowed description of the burst contract, produces a finite local circuit operation and its explicit resource bounds;
- a specified finite physical readout whose total error is at most 1/4;
- complete charges for horizon-dependent hardware, its construction, commissioning, local updates, energy and readout.

All immutable wiring, gate laws and the input-independent bounded-rate schedule may depend on T. They must not depend on the unknown stored bit. Every mutable input-bearing data/control/decoding record remains within the fault model.

## Necessity is uniform over this entire family

For each horizon-specific device, couple the two input worlds using its own common input-independent architecture, schedule and random resources. Their difference still starts inside the same C_0 and remains inside C_t.

Therefore the previously proved bound

\[
\operatorname{TV}(P_0^T,P_1^T)\le e^{-\Lambda(T)}
\]

holds uniformly over all these architectures and schedules. Unlimited but finite input-independent hardware prepared for T does not alter Lambda. If E R^(d+1) is infinite, no such family with fixed r_0 can maintain error at most 1/4 as T increases.

If T is the storage duration and the readout finishes at T+tau_read(T), evaluate the causal bound at that total endpoint. Input information held in an external transcript or receiver before completion must be included in the coupled state.

This does not revert to the weaker family in which the initial input-dependent radius r_0(T) grows with T. That weaker family was the source of the critical-tail counterexample in the preceding audit.

## What the refinement buys

Predetermined circuit geometry and scheduling can prescribe where and when encoded blocks expand, interact and decode. The proof need not solve translation-invariant self-organization, authentic-seed selection, spontaneous fabrication, or an autonomously repaired global clock.

The hard information operation remains: construct finite-speed local error correction and transfer under the correlated burst law, including interactions of damaged regions and a finite decoding path. Horizon dependence does not supply the stored bit or repair it.

A fixed total accuracy target avoids the impossible demand for arbitrarily reliable output at a fixed noisy endpoint. The explicit terminal protocol still needs a nonzero error floor below its allotted budget; choosing small enough intensity can be part of the theorem. It must not be replaced with a costless global decoder.

## Scope labels to retain

This is a uniform family of horizon-specific finite operations, not one autonomous apparatus that indefinitely fabricates and repairs itself. The initial input-dependent seed radius is uniform in T, while the input-independent hardware and cost need not be.

The fixed reliable local gate laws and input-independent schedule are mathematical premises. A physical implementation must eventually earn their mechanics and costs; declaring them does not supply a physical reduction from the prior Gibbs or skip-free systems.

The uniform construction algorithm, local state/degree/density bounds and explicit resource function prevent the phrase 'finite hardware' from hiding arbitrary nonuniform advice or unbounded packing. Such bounds matter to the positive capability even though the lower cone theorem does not need them.

Conclusion: this is a cleaner core question. It retains the new universal obstruction and a substantial constructive frontier, while separating optional autonomy requirements from the required information-preserving operation.
