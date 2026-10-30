# Independent raw compiler soundness and implementation review

30 October 2026. Frozen sources in `raw_compiler_sources/`: soundness note SHA4538de0e93f8c9c1743ab416ca247dde7a40a3b8fc38886d047b8a1946a25446; acquire.py SHA367f6fec57ab31727041e03e18bf7ae666ce8a45bf13be26e09197d07fc13948; results SHA5827dcec0d7f3c27466f48921b87f9d1c612f325e064d6191b6b0365cf5224a0; raw inputs SHAac8b4070798fc1bae6771017e0900fe09f1fae9766104e29ccafe70aa7349118.

## Verdict

Accept this restricted sufficient-certificate finder and its generic soundness transfer, with the precise interpretation below. No false-positive architecture or code/theory mismatch was found. This acceptance includes the initial mixed population-clock guard; it does not approve any later proposal to remove that guard. No completeness, polynomial-time, practical-conditioning, or novelty conclusion follows.

## Exact finite checks

The connector and common-offset search is genuinely over the raw reaction list. Residual source and product count two and zero residual B give the exact falling-factorial factorization with a0=m-2. Parallel connector edges may cause rejection because they are not consolidated; that is a conservative incompleteness, not a false positive. Zero-rate removal and reaction-ID checks are consistent with the stated input contract.

The inferred D-free nonseed edges must be a-neutral and restore positive D. Consequently F has frozen hidden counts before seed, while each mixed visit has exactly one holding interval before a restoring/seed/terminal event. The cells 0,1,2,3,4+z fix all binary source and shifted-output enablement: shifts have magnitude at most two, and an output starting at four remains at least two. Boundary D equals the exact negative D jump size. Thus all ingress states are covered, including decrements of two and falling-factorial sources such as 2E.

`domination` is conservative but sound: both polynomials have nonnegative coefficients, every numerator monomial has positive denominator coefficient, and the returned maximum coefficient ratio makes C*den-num coefficientwise nonnegative. Per-reaction maxima cover cells and per-reaction constants are summed. The mixed-ingress and initial-mixed checks are distinct, as they must be. The hidden-large X rejection demonstrates a genuine failure of the latter premise, not evidence that its network is transient.

## Pool extraction and affine baseline

The implementation enumerates finite partitions with a singleton a. It rejects nonneutral restoring edges, nonunit nonsilent moves, and non-affine divided sources. For a non-a target it checks exact equality to qY_i, including the protected-pool constant -q. For target a it takes the minimum coefficient over the source pool. Subtracting this baseline leaves nonnegative variable coefficients. After D=1+u_D, the constant remains co[-1]+co[D], exactly the quantity checked in code; this is true whether or not the source pool is protected. Thus the remainder test is not missing the protected offset.

Every nonprotected source pool with a positive physical unit-transfer rate contains a consumed source particle, so it cannot move when empty. A protected pool can have an excess a-producing event at Y_D=0. Its actual output then has no physical particle in that pool. Since every restoring edge preserves pool counts and produces D, no restoring source can be enabled there. The output is true F and the independently checked active-output/linear-hazard guard applies. Such a jump terminates; no negative pooled population is continued.

Abstract pooled labels, with physical channel selected proportionately to the grouped rate, realize the exact generator. Pool-internal identities may be reassigned. This does not claim independent physical-species chains. Only a-directed adapted extras remain; all other baseline transfers have exact rates.

## Generic probabilistic proof

Requiring every baseline type to reach a is sufficient; irreducibility is unnecessary. For each starting type use a shortest path, suppress all nonprescribed baseline rings and all a departures, and place its path rings in successive subintervals. Extras toward a can only shortcut this event. Conditional on the starting history, the forcing events are independent across labels with uniform lower probability c t^L even when starting types are correlated. Last-unit forcing and initial-a no-departure events give the long/short-time cohort bounds. Crossing compensators and separately charged seed deletions do not require survival-conditioned independence.

Accessibility is also generic. A positive pooled label can follow a baseline path; any selected physical channel realizing the next unit transfer has a positive enabled rate. If it exhausts D, it either hits the terminal F guard or reaches a mixed state, where one restoring jump preserves the pooled state. Thus at most one restoring step per path edge suffices. After obtaining a, the required a+D birth supplies 2a or an earlier active F stop. Initial mixed states restore first. H=2L+5 is a sufficient fixed budget, and the deterministic fixed-time block proof earns polynomial moments without assumed recurrence.

The trace ingress inequality pays accumulated mixed occupation; the separate 1+n bound pays an initially mixed wait. Actual bounded A shifts permit fixed weighted physical costs. These facts supply the reset and true-F compensators, the log-squared good-input occupation ratios, and every fixed grade. The derivations therefore do not smuggle a directly supplied pool, stationary distribution, cutoff, or infinite-state Lyapunov vector into the raw input.

## Global-template interface

The dormant Green is a direct sum over frozen hidden metadata/signatures, with supremum norm, not a face-count multiplier. The true-F return estimate controls the total outgoing face law. The previous fixed-b, tilted finite-grade, signed-source and bad-block proofs then apply with the acquired exponents and actual outputs. The good-input log cutoff is used at section/bounded phases; arbitrary-B processing uses all-input grades and the actual tilted Green.

Every positive-D state with n>=2 has a pooled particle/path or the a-born event; every mixed state restores; an F input is active exactly at a>=2. All true-F ingresses were checked active. Consequently fast moves preserve the actual physical activity indicator, subject to A>=a0. Inactive approaches and finite-head clearing trials are covered; if a path first reaches F, its output has an enabled clearing. Residual rates remain quadratic, so the physical holding lower bound and the two-direction Foster cost patch apply. Weak reversibility is checked on the full physical positive-rate graph and supplies closed communicating components. These are the generic global premises, not merely properties observed on the two supplied examples.

## Executable adversarial checks

`test_raw_compiler_challenge.py` imports the frozen module without invoking its source-writing main routine. Results are in the corresponding JSON. It reproduces the four supplied outcomes and additionally checks:

- a new a+D->C+E baseline departure that exhausts D into a mixed hold: accepted, trace total22/7;
- a two-D ingress with restoring source 2E and no C species: accepted, L=1, trace total9/8;
- a non-a D-consuming birth without adequate restoration: rejected on the true-F active-output guard;
- complete species renaming, reversed species order and reversed reaction order: accepted with the same inferred L=2 and trace8/7.

These checks challenge event classes and raw selection, not just population shells. They support implementation consistency but are not the infinite-state proof. Frozen source bytes were preserved; no external action or prohibited source was used.

## Limits

The emitted JSON records constants and inferred structure, not every expanded cell polynomial. A standalone verifier must recompute those exact finite identities from the raw input, or an expanded proof object must be emitted. This does not invalidate the present finder/checker, whose rational computations are inspectable and reproducible. Rejected networks may admit other certificates. The accepted object remains this restricted search plus the stated phase foundations, not an unrestricted algorithm deciding recurrence.
