# Independent audit: relative-accuracy quadratic-training exact-erasure receiver

27 October 2026, 02:44 UTC. PASS for exact_erasure_relative_accuracy_quadratic_training_receiver.md.

This receives the complete source-specific recovery operation and its training cost. It does not improve the generic diamond bound for partial-SWAP Hamiltonian simulation, and is consistent with the previously proved code-to-reset leakage floor.

## Resource and spectral interface

The actual signed generator remains4(T-omega), with the accepted wrap-safe QPE grid and known scalar phase. The nine local qutrit Weyl conjugations produce the nine orthogonal rank-one Bell-code projectors summing to Q=I_C tensor VV*. Every controlled A-time uses fresh T and omega programs, each obtainable with one ordinary channel call. The number of controlled evolutions is9Lrm and their total time isS.

With N_t=ceil(512tS/xi), the received elementary error256t^2/N_t sums to at mostxi/2 overall andxi/(18L) per classifier. Two collision angles of magnitude4t/N_t in each ofN_t rounds give total squared-angle budget32sum_t t^2/N_t<=xi/16. This is a separate source-population budget, not a replacement for the generic simulation error. Ceiling costs give2sum N_t<=1024S^2/xi+18Lrm, plus the independent data call. All calls are charged anew per attempt.

## Quantum code-input instrument

With exact evolutions the entire classifier sequence is diagonal in the common P_j sectors. For sectorj, a union bound costsL eta for its own qualification failure and8eta^L for another label qualifying. On every other code sector, accepted output labelj has probability at mosteta^L. These are eigenwise effect-operator bounds, not just tests of one input state.

The accepted-j Stinespring map restricted to the complement has operator norm at mosteta^(L/2). Hence the two input cross blocks cost at most2eta^(L/2) in diamond norm. The P_j and complementary diagonal blocks costL eta+8eta^L andeta^L. Summing the nine accepted branches, then accounting for the FINAL erased complement, gives the stated18L eta+162eta^L+36eta^(L/2) bound. Final erasure discards the remaining data, so its difference is minus the partial trace of the sum of accepted-branch differences; this justifies the doubling. It would not justify replacing intermediate nondestructive rejects by erasure, and the proposed circuit does not do that.

With eta=(xi/(100L))^2 andxi<=1/2,L>=1, the ideal code error is at most.369xi, in particular below the more conservative.378xi used in the theorem. Adding the generic simulation errorxi/2 is belowxi. Known Bell preparation/contraction, label-controlled corrections and discarding are CPTP postprocessing. Untouched external references remain covered even though the locally prepared Bell partner is later corrected.

## Joint controlled-SWAP sector analysis

The needed premise is joint block diagonality with respect to Q, including all controls, retained records and untouched references, not merely block diagonality of the reduced data state. It holds for the initial reset datum and local Bell ancilla. For a fresh programrho commuting withQ, the controlled partial-SWAP formulas preserve it in every control block. With references, the swapped diagonal term isrho tensor the appropriate partial trace; products by rho and commutators preserve the same sectors. Control-only gates and C-only Weyls also preserveQ.

For an exterior-supported input, the projected code contribution contains no identity/SWAP cross term because Q I(I-Q)=0. Its trace is exactlyp sin^2(h) times the active-control population, hence at mostp sin^2(h) times the incoming trace. The formula extends to arbitrary reference-assisted positive inputs.

Because the full joint state is already block diagonal after each collision, virtual Q/(I-Q) pinching leaves the actual circuit unchanged. Keeping the virtual records supplies an exact positive CP decomposition by histories. Restricting to histories with no previous import is therefore legitimate; it does not use a physical unknown-code measurement. A union bound on first import over all collisions gives probability at mostp xi/16. Code leakage outward need not have a factorp and is not claimed to do so.

## Repeated tests and complete exterior error

On any exterior input, ideal single-classifier acceptance is at mosteta; the complete nondestructive simulation error adds at mostxi/(18L), yieldingbeta<1/16. The no-import subinstrument is a positive CP part of this actual accepted map, so dropping imported histories can only reduce its unnormalized acceptance probability. After conditioning on any retained no-import history, the data remain exterior. Thus the same bound is valid at every later test, regardless of ancillary correlations or earlier records. A given label's all-L-pass probability without import is at mostbeta^L. Intervening CP instruments cannot increase its trace mass.

Final acceptance implies at least one label qualifies, so a union bound gives9beta^L<=p0xi/16<=pxi/16. Imported histories add at mostpxi/16, for total reset acceptanceb<=pxi/8. An imported error is not assumed to be rejected by repetition.

Finally, the original source decomposes into a code input with weightp and a replacement input with weightq. Its code-channel error is at mostxi. On the replacement branch the external reference is independent of the fixed replacement datum, and after the known output-flag dephasing the complete deviation from erasure is exactly2b. Therefore the full unhalved diamond error is at mostp xi+2qb<=5p xi/4=5eps p/8<=eps p. All rejects are included.

## Scope

The sample count has quadratic inverse-p0 dependence up to logarithms at fixed relative accuracy, while retaining the original ideal identity throughputp per data invocation. This matches the received worst-case adaptive-query lower exponent for meaningful complete recovery, not a claimed optimal joint accuracy law. It requires the exact orthogonal-reset promise, conditional IID/memoryless source, independent data/programs and access to controlled whole-register SWAPs. No near-erasure, hidden-memory, reusable-decoder, practical-cost, unassisted-capacity or sample-free validation assertion follows. Width/gate cost still depends on output dimension, and total-use rates must pay training, data and any validation calls.
