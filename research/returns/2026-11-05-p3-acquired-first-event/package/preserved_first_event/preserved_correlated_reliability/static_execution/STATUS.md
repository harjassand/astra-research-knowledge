# Final status: COMPLETE

Actual acquisition, exact reference comparison, finite cost accounting, and final documentation are complete. See `TO_ROOT_RESULTS.md`, `README.md`, and `results.json`. The recorded fixture fits the parent direct cut-enumeration branch; scalable contraction and a time-dependent CDF simulation are outside this implementation. No additional tests or runs were added after completion.

## Earlier checkpoints (retained as history)

# Static acquisition engine — active implementation

Following root's stronger heavy-prefix construction, the canonical engine will estimate pinned partition functions from ordinary heat-bath samples, choose the empirical heavier branch, telescope its probability, and divide the exact rational configuration weight by that probability. Cut probabilities are ratios of pinned partition functions. This removes inverse rare-field cost; JVV sampling/counting is the correct comparator.

The implemented interface will include arbitrary positive rational bounded-arity factors, exact conditional tables and Dobrushin influence bounds, independently restarted pinned heat-bath draws with explicit TV bounds, capped exact integer randomness, explicit cut enumeration for the small fixture, inverse-multiplicity union estimation, and conditional-failure rejection. The diagnostic fixture will be a nonsymmetric connected graph with a very reliable spanning tree and moderately unreliable chords, with rational interactions between rare and common edges. Thus ambient fluctuations genuinely matter while all failures remain extremely rare.

Proof-budget counts will be computed without floating logarithms. Smaller diagnostic sample counts will be clearly labelled and will not be presented as satisfying the requested PAC error. The exact finite-state reference will be isolated from the algorithm.

Own passive-memory theorem and limitations are being preserved in next3_first_principles/02_PASSIVE_MEMORY_PROOF.md. No changes outside the two assigned directories.

## Concrete fixture and implementation decision

Six network vertices, ten edge variables: a five-edge rare spanning tree plus five moderate-probability chords, with asymmetric fields and explicit pair interactions among chords and between tree/chord variables. Add a rare–rare interaction factor 2^40 while its endpoint fields have odds about 2^-90 and 2^-95. Conditional odds contrast is then above 10^12, while a small fixed logarithmic contrast (to be checked exactly) and Dobrushin uniqueness can still hold. This directly exercises the stronger logarithmic-contrast class rather than merely reproducing bounded-odds functionality. The reference enumerates 1024 states and 31 cuts.

The engine will retain exact rational confidence intervals for each heavy branch and partition function. Very narrow *provable local conditional ranges* may be used directly; other stages require fresh independently restarted heat-bath draws. A small native sampler may accelerate the exact rational transitions for the fixture, with arbitrary-precision Python fallback. A hard 128-bit check will prevent silently overflowing native transition probabilities.

## Execution checkpoint
Core exact-rational Python engine and native unsigned-128-bit heat-bath accelerator are written. The 10-edge, 6-vertex nonsymmetric fixture has exact Dobrushin chi < 0.373119 and exactly verified logarithmic contrast c=3, despite ordinary odds contrast approximately 1.8325e12. It has 31 cuts and 1024 states. Next step is the requested one actual acquisition run against an isolated exact finite-state reference; no CDF simulation or expanded implementation scope. Heavy-prefix intervals and actual primitive counts will be saved separately from the conservative whole-theorem schedule.

## Completed
Actual acquisition run and exact comparison finished successfully. See `TO_ROOT_RESULTS.md` for report-ready numbers and explicit scope limitations, `results.json` for exact rational values, and `run_stdout.txt` for the execution transcript.
