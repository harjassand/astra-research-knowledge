# Fixed-budget result, audit history and practical comparison

The [complete result](package/RESULT.md), [production manifest](package/square_aklt_local_sampler_20261105/production_manifest.json), and [machine-readable run](package/square_aklt_local_sampler_20261105/physical_local_infinite_precision001.json) govern the current [local physical readout](README.md). The original archive retains proofs, executable code, numerical data and historical reports without rewriting them.

## Executed result and full measured work

The producer fixed 542,236 complete attempts and seed 2026110501 before sampling, from a deterministic estimator-range bound rather than an observed standard error. It reports nearest-neighbor expectation estimate -3.559889190566645 and outward-rounded 95% interval [-3.569890,-3.549889]. Exact rational endpoint and confidence data are retained. The empirical standard error 0.00324037 is explicitly not the certificate.

There were 463,946 non-null source paths requiring independent local queries. The run took 722.901 seconds plus 0.106 seconds setup on the producer's shared host. Per local query, measured means included 1.4823 seed proposals, 2.6368 parent proposals, 2.5016 time comparisons and 1.0564 retained clan cylinders. Null proposals, rejected parents, geometry, exact-time ordering, cleaning and rational readout are included in elapsed time. Observed maxima of 35 cylinders and 104 loop edges are not cutoffs.

These are supplied execution records. Capital did not run the sampler, build proposal matrices, load NPZ arrays, perform a new audit or repeat the 12-minute computation. The mathematical confidence assumes independent ideal fair bits; a seeded PRNG supplies reproducibility rather than a physical independent-randomness certificate. Model mismatch and arbitrary boundary states are outside the interval.

## Completed technical review at the right version

Use the [current local-sampler audit](package/independent_audit/LOCAL_SAMPLER_AUDIT.md), [physical correlator audit](package/independent_audit/PHYSICAL_CORRELATOR_AUDIT.md), [independent local implementation audit](package/square_aklt_local_sampler_20261105/INDEPENDENT_LOCAL_AUDIT.md), [resource proof](package/independent_audit/LOCAL_RESOURCE_PROOF.md), and [lazy-time cost proof](package/independent_audit/LAZY_TIME_COST_PROOF.md). These cover all-length birth normalization, residual Poisson revelation, shared ancestors/pair marks, exact primitives, physical normalization, infinite-volume coupling and complete expected arithmetic. The completed reviews support acceptance at those internal scopes; no new Capital reproof is required or claimed.

The [earlier global audit](package/independent_audit/INDEPENDENT_AUDIT.md) concerns a different earlier implementation. Its statement that a local intersecting-loop interface was not implemented records the old boundary, now addressed by the current local engine. Its finite-volume cost and observations remain historical evidence. It must not be used to declare the completed local operation still missing. Some historical artifact links name original workspace locations; the current navigation links here point to included release files.

Exact 4x4 checks cover 793 routed loop types and 21,288 rooted oriented encodings across four query sets. Independent physical tensor calculations check the distinct-site factor 9, signs and source contacts. Separate geometric exposure and high-activity finite-support stress tests exercise overlap, shared ancestors and earlier-region exclusions. Finite enumeration and statistical screens support implementation consistency; the all-size guarantee rests on the proved invariant and certified all-length bounds.

## The anomaly and fixed follow-up remain visible

An early selected rare 3x3 category was low across two pilot batches, about 3.7 standard deviations combined. Those batches remain in the package. A separately coded geometric-exposure sampler checked the full 15-category marginal, and a birth-frequency check tested the selected route.

A fresh main-engine diagnostic was preregistered with 2,000,000 draws, fixed seed 1168304679, exact target probability 1/2558 and two-sided threshold 0.01. It found 770 events against 781.861 expected, exact binomial p=0.693942. The selected deficit was not reproduced. This does not exclude arbitrarily small bias or prove other marginals correct.

The first fixed batch completed but failed when serializing a library boolean before displaying its count or p-value. The same frozen code, seed and random sequence were replayed with serialization repaired and a raw-count checkpoint added. It was not a newly selected random batch. The [failed runner](package/square_aklt_local_sampler_20261105/focused_main_check_failed_serialization.py), [preregistration](package/square_aklt_local_sampler_20261105/focused_main_preregistration.json), [replay metadata](package/square_aklt_local_sampler_20261105/focused_main_replay_metadata.json), and [final check](package/square_aklt_local_sampler_20261105/focused_main_check.json) preserve that history.

An initial oversized stress diagnostic was stopped before output, with no result claimed from it. The smaller stress runs and their purpose remain identified in the audit. Nonrejection is not proof; implementation signoff combines the mathematics, code/primitive review and retained diagnostics.

The producer made one documented path-only portability edit to a resource checker. Its [original source](package/independent_audit/certify_local_resources.py.original) and [change note](package/independent_audit/PORTABILITY_CHANGES.md) are included. Runtime sampling, estimator, confidence primitive and mathematical inequalities were unchanged by that edit. The release-wide manifests describe delivered bytes; earlier frozen hashes remain historical evidence at their own versions.

## Strongest comparators and remaining claims

The included audits credit Silva-Schakel-Vasconcelos's matching crossing loop gas and worm, Wierschem-Beach's AKLT loop observables, and Fernandez-Ferrari-Garcia's generic infinite-volume ancestor simulation. The physical audit also credits earlier spin-clustering results. The operation does not invent these representations or general frameworks.

The scoped addition is the executable exact all-length intersecting-loop oracle, certified subcriticality at this parameter point and independent bounded readout with a finite-sample selected-limit guarantee. A targeted search not locating the same guarantee does not establish priority.

On a recorded 32x32 pilot, the local readout was about 67 times faster per attempt than this project's own global exact sampler. Published worm or valence-bond-loop implementations were not run head-to-head, so this is not a QMC speed record or demonstrated practical superiority. Timing, source construction, setup, random-bit precision and accuracy requirements remain costs. There is no deterministic worst-case runtime, demonstrated linear bit complexity, quantum preparation, gap proof, general boundary solution or civilisation-changing capability claim.
