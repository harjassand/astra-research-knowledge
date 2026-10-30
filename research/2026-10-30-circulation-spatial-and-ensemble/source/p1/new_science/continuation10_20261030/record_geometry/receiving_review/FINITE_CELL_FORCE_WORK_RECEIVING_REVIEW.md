# Receiving review: actual force work for delayed finite cells

**Actual input:** `physical_mechanism/FINITE_CELL_FORCE_WORK_UNDER_DELAYED_COMMANDS.md`, SHA256 `1b9c88dea4051dfbd7b46c0429cc77a1f0b277dc8c6e19612f08cc1ac43b812c`. Its exact snapshot is `FINITE_CELL_FORCE_WORK_REVIEWED_1b9c88dea405.md` beside this review. The earlier missing plus sign in equation (6), reported during review, is present in this actual version.

**Accepted.** I independently reconstructed the actual displacement cell and its force-work sum, rather than substituting corrected current for physical current. Write `d=1/g+b`, `A=(2/g+b)²/2`, and `e=A−d/g`. The actual cell is

\[
\Delta J_k=P_k/g-dY_k+ReF_k,
\qquad P_{k+1}=-Y_k+RdF_k.
\]

With a force held for L cells and selected from at least one complete block earlier, the fresh source immediately before the block is independent of the new command. Therefore the first-cell mean work contributes `Rd E(F_m F_(m−1))/g`, and each later cell contributes `Rd E(F_m²)/g`, besides the `ReF_m²` terms. Summing gives exactly the input's equation (6), and summation by parts gives equation (7).

The negative switching term has not been omitted. Since the squared force increments plus final squared force are at most four times the sum of squared forces, the lower coefficient is `R(LA−2d/g)`. It is nonnegative for every integer L at least one because `A−2d/g=b²/2`. The upper coefficient is `RLA`. These statements hold for the specified delayed command filtration, not a controller allowed to inspect the next thermal input.

The rare-arming work bound is valid whenever its actual arming event has the probability proved in the separate governor construction and the actual command stays bounded after arming. This review does not silently supply detector reliability or a smaller observation error than the local detector note proves. At that interface, a superpolynomially rare arming event dominates the polynomial worst-case quadratic-force bound and makes mean actual force work tend to zero.

For a sustained nonzero mean current on the N² horizon, the momentum endpoint is `O(Ra)=o(N²)`. Jensen/Cauchy--Schwarz in the force sum yields the stated asymptotic lower bound `[EJ]²/(mu R T_phys)` when block length tends to infinity. A constant force supplies the matching leading mobility. The bound covers this port and command filtration; it is not universal over extra baths or fresh-noise-informed feedback.

The result leaves thermal preparation, coordinate retirement, switching, sensing, synchronization and communication outside this force-work account. The supplier uses O(RN²) fresh thermal coordinates even before arming. No numerical fixture was needed for these exact conditional expectations.

The supplier version originally read by the physical-mechanism role has SHA256 `73d6f367bd012fca68d92358d6a902a5a3741e8d8337905b4869d81f83a29fd9`. Its present SHA256 is `362497578e0a88cd0b85948804ee2526de06fc0198fc60ccc1aeb58db19d6ed6`; the only change was repair of inline mathematical delimiters. The displayed source equations and physical assumptions are unchanged.
