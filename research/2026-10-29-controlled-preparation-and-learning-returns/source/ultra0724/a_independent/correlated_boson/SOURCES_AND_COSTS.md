# Source, ordinary methods and complete cost boundary

## Scientific destination and prior

The missing operation was sampling the actual positive canonical boson field measure without an exponentially rare independent Gaussian overlap. The frozen phase-law theorem excludes changing the unused higher moments of any independent fixed-size-block phase law on its native diagonal control. It does not exclude the correlated proposals constructed here.

Current Astra was selectively queried and N1091 plus its governing source fetched at revision `3882c05cc803ff107b4d89f4010090ed41c3a392`, input `2f94a3c6ae0d729c91e936b58b84af96f66c9850525b447602b8acb884d86015`. The complete returned metadata/capsule/source bytes are in `sources/ASTRA_N1091.json`; no continuation remained. The source fixes conjugate hopping, separately conserved flavors, and the U1/U2 distinction. We use only U1>=0,U2=0 and no pairing term. The new analysis does not relabel an old source pin as current, reopen N675, or treat a corpus search miss as priority evidence.

The strongest ordinary alternatives were checked before the new construction:

* [Shen et al., canonical AFQMC 2010.09813](https://arxiv.org/html/2010.09813), Sections II.3--II.5, provides the symmetric-power canonical recurrence and samples a correlated auxiliary-field posterior. Its field updates/importance strategies are the actual incumbent; iid Gaussian proposals alone are not. The frozen local PDF/text was reused, not downloaded again. [Shen et al. 2212.08654](https://arxiv.org/abs/2212.08654) supplies improved stable canonical recurrences and an associated code/data route; its displayed application is fermionic. No measured runtime separation from an equally informed canonical AFQMC implementation was performed here.
* [Van Houcke--Rombouts--Pollet, cond-mat/0508431](https://arxiv.org/html/cond-mat/0508431), Section II, constructs a canonical continuous-time nonlocal worm operation, including symmetry projection. This is a stronger conventional route than only local worldline moves. The positive hopping triangles in our inputs have a native occupation-basis sign problem; the prior's canonical/worm principle alone does not remove those signs or give the present independent field-law output.
* [Kuwahara--Saito 1807.08424](https://arxiv.org/html/1807.08424), Setup Eq.(1), and [Kuwahara--Alhambra--Anshu 2007.11174](https://arxiv.org/html/2007.11174), Setup/Section IV, give strong finite-temperature one-dimensional algorithms and MPO representations. Their bounded local norm/dimension inputs must be paid for soft bosons. `OCCUPATION_INTERFACE.md` actually supplies a qualified logarithmic cap and Gibbs-variational replacement theorem to that comparator. It does NOT prove a competing tensor method inefficient: onsite-aware bosonic/tensor improvements and charge-resolved contraction remain serious unexecuted alternatives.
* [Tong--Kuwahara 2509.25572v2](https://arxiv.org/html/2509.25572), Setup and Theorems 1--2/Section S.V, gives high-temperature bosonic partition algorithms using repulsive onsite coercivity and interaction-picture clusters. The paper reports quasi-polynomial costs in its stated settings. Our two-flavor potential U(nb-nc)^2 has an unpenalized total-pair direction, so that coercive hypothesis is not imported by calling it a quartic. Low-fugacity/cluster/conditional-integration methods remain ordinary alternatives. The present sampler uses actual negative-fugacity contraction r<1 rather than claiming all-temperature tractability of generic bosons.
* [Salmhofer 2021, DOI 10.1007/s00220-021-04010-4](https://link.springer.com/article/10.1007/s00220-021-04010-4), establishes rigorous canonical/grand functional-integral and stochastic representations. These are established machinery, not a new Gaussian formalism invented here. No unqualified theorem from it is used to bypass the present canonical count or frustrated-field sampling cost.

The determinant derivative bound, rejection and recursive normalizer estimation are ordinary mathematical operations composed at the stated native class. Historical priority of this composition is UNKNOWN. Neither a generic sign-problem solution nor a civilisation-level outcome is claimed.

## Exact acquired M64 input

The new input is beta1,U4,K64+64,M64,L16 and `T=(1/4)ww^T/(w^Tw)`, w=(65,...,128). This includes all diagonal one-body potentials. Its trace is exactly 1/4 and its positive triangle hopping signs are frustrated; the U4 interaction does not commute with T. Distinct w removes the simple all-site permutation symmetry. This is not the old M9 target.

`acquire.py` uses only Fraction/integer arithmetic for the qualification. It reuses the already frozen exact zero-hopping canonical interval, computes a new positive Laurent-convolution grand normalizer, acquires the density saddle and determinant envelope, and returns the interacting finite-L acceptance floor. Final setup took 0.31148s after imports; no random draw or new diagonal DP was used. The exact receipt contains:

* r=.7048643671236743, total saddle-mean error below2.10e-13;
* base count mass in [.03533764704236527,.03533764704236626];
* determinant envelope at most3.300705842;
* interacting ideal iid acceptance at least.006493570588, expected proposals at most153.999;
* uniform ideal positive-trapezoid G0 error at most2^-40, using2094 phases;
* grand normalizer relative interval width below8.685e-35.

The Fraction compiler first hit Python's decimal-string safety limit before writing a receipt; no random draw occurred. A first successful large-denominator record took.89416s. It was replaced by mathematically outward dyadic serialization of the SAME exact bounds, reducing the metadata to4.4KB. The original oversized metadata was not a scientific source or a different physical model. The first sampler startup also failed before RNG use on those strings. These overheads are retained here; they are not included in the final sampler timer.

## Actual noncommuting canonical execution

`sampler.py` used32,768 fixed proposals and one declared seed. It charged common-phase batching overruns, every rejected total-phase proposal, all Gaussian-bridge variates, character evaluation, G0 evaluation and the final accept coin. It returned222 histories. The execution took71.2267s after imports:1.5515s proposal work,51.5419s propagation/characters,18.0760s G0 quadrature. It consumed57,636,040 seeded raw64 words (3,688,706,560 pseudorandom bits), including45,476,632 inverse-normal quantiles. These are an observed finite PRNG realization, not independent physical fair bits.

The CV partition ratio is.62518435, corresponding to finite-L free-energy shift.46970871. A two-sided ideal-iid empirical Bernstein calculation gives [.41559861,.52691506]; the physical Jensen upper bound is.5. The same-T NONINTERACTING canonical control gives.40171460. This is only a mechanism control, not an equally informed algorithmic incumbent or evidence against Hartree/atomic-limit/RPA/tensor approximations. The interval concerns the ideal iid variable; binary64 and52-bit quantile error are NOT certified by it.

The consumer stores one64x64 one-particle matrix per proposal plus bounded batches, not the approximately1.434e74-state canonical sector. It stores the accepted histories in `ACCEPTED_HISTORIES.npz`. Peak RSS and import/startup time were not measured. Formula memory includes batch M^2 matrices, batch ML phases, M Q quadrature entries, the fixed-length diagnostic arrays and accepted histories. Independent direct trace-power recurrence checks on three proposals disagreed with eigenvalue-based characters by at most5.06e-14; that is a floating diagnostic, not a uniform roundoff theorem.

## Extensive bounded-cut execution

`bounded_cut.py` separately executes only the conditional-common-phase recursion. Its source is M64, U4,beta1,L16, nearest+next-nearest open-chain PSD bond projectors with j=.01. Total hopping trace2.5 is EXTENSIVE under continued system growth; every recursive cut has trace at most.06. It produced32 histories at phi0 and32 at phi=pi/2 in2.90068s after.00301s matrix setup. All54,116 native recursion calls,27,026 merge attempts,708,040 normal quantiles and921,250 raw64 words were charged. Per-merge ideal acceptance is at least.56372686; the rejection recurrence exponent contribution is1.82693, before local arithmetic degree. No determinant-envelope excess was observed.

The corresponding whole-system generic rejection FLOOR is4.24e-11. That is a deliberately conservative bound comparison, not an observed cost or a lower bound on AFQMC/MPO. The construction proves a polynomial recurrence where the whole-system bound is exponential as M grows.

The initial run emitted complex-slogdet floating-point warnings although all finite outputs and bounds remained valid. Its program/receipt are preserved as `INITIAL_bounded_cut.py` and `INITIAL_BOUNDED_CUT_EXECUTION.json` (2.84080s sampling,.01198s setup). The final code uses the uniformly positive Gram's Cholesky log determinant and an analytic scalar leaf. The repeat used identical seed and primitive counts, with no warnings. It is a numerical repair, not a second independently implemented sampler.

The full phase-normalizer FPRAS, global phase-grid law, dense-count selection and prescribed-count self-qualification have NOT been run on this extensive ladder. They are constructive polynomial-cost theorems in `PROOF.md`, not extra execution receipts. Conditional-phi output is not labelled canonical output.

## Independent small control and continuum debt

`small_control.py` constructs an independent36-state many-body transfer for M3,K2+2,U4,J1/4,w=(1,2,3),L2. A deterministic729-history exact-moment quadrature gives4.432614470017637 versus the full transfer4.432614470017641, discrepancy3.55e-15, in.02056s after imports. The continuous Gibbs value is4.404026154186472. This meaningful noncommuting control checks the native HS/character implementation and also exposes finite-slice bias; it does not qualify the64-site continuum error.

For the M64 low-trace source, the uncentered canonical norm bound is R=32800. `CONTINUUM_COST.json` reports the exact integer sufficient slice count from the frozen128 beta^3 R^3/L^2 estimate at log-partition tolerance1/100. That enormous bound is NOT the executed L16. Recursive/canonical rejection envelopes are independent of L, but generating/propagating L histories is real cost. No continuum hot loop or end-to-end interval/fair-bit sampler was executed.

Full polynomial statements hold with fixed beta,r,cut bound and source interaction bounds, and with their explicit accuracy/count-floor dependencies. They do not mean polynomial in arbitrary binary-encoded beta or unqualified source norms. Constants and normalizer-grid exponents can be impractical. No hardware, new material phase, generic prescribed-density theorem, advantage over strong AFQMC/tensor/cluster methods, or completed original mission follows.
