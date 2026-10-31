# Independent check of the explicit finite-bit threshold Stinespring construction

31 October 2026. Full-source mathematical-existence review by the complementary construction worker. No quantum gate backend was executed.

## Frozen target

FINITE_BIT_THRESHOLD_STINESPRING_CONSTRUCTION.md,9,232 bytes, SHA256 d560f37e39a501a03d3c1c419bed8919eb5149cf9570076e04ce0ac48f2fd1a0.

## Checked acquisition operations

1. **Exact finite local inputs.** Positive rational Boltzmann factors and the supplied local-context list yield rational rates, exact threshold ordering, nonzero interval colors and local stationary ratios. The table has O(n2^k) colors. Bit lengths of sums/products of explicitly polynomially many rational inputs remain polynomial. No global pi_x evaluation, pi_min inverse, uncomputable real comparison or source-state table is assumed.

2. **Actual inverse-fibre preparation.** For each input x the two slots per color are exactly y=x and y=x^i, with probabilities w_f 1{f(x)=x} and w_f(pi_(x^i)/pi_x)1{f(x^i)=x}. The established weighted-map TP identity makes their sum1. Zero branches are decided exactly. Computing prefix sums by scanning the complete finite color list is slow but genuinely polynomial in the admitted input size; it is not QRAM access.

3. **Finite numerical preparation.** Every positive prefix denominator has an acquired binary scale from its rational bit length. Computing child/parent ratios and rotation angles to absolute precision therefore costs polynomial input/precision bits, not the numerical reciprocal of a tiny probability. Exact0/1 branches and fixed definitions at zero parent mass give a consistent ideal unitary on all workspace inputs. Controlled-rotation approximation is uniform in x and the current prefix. Ordinary unitary telescoping over tree levels bounds the isometry error before later permutations. This directly avoids any dimension-dependent conversion from basis-state error to coherent operator error.

4. **Coherent erasure and source retention.** On each ideal branch x=f(y). XORing f(y) erases the old source. The slot is then determined by whether f(y)=y or y^i and can be erased reversibly. Arithmetic work must be uncomputed before the old input is erased, as the source construction states. The color remains the environment label; retaining the full old source instead would define the wrong channel and is not done. The same erasure gates are valid permutations on approximation-error branches, so they do not amplify norm error.

5. **Fixed phase and inverse access.** Nonnegative amplitudes give the intended W and c=sum_f sqrt(w_f)|f>. The ideal pure reference factors with that actual c. Approximate gates are compared to this nominal interface, not declared exactly dark. The complete unitary circuit can be reversed to obtain W^dagger. A consumed channel-only black box would not suffice, but is not used.

6. **Receiving scope.** Coupling, reflection/reference preparation, finite use counts and consumer precision remain separately paid. A fixed deterministic use cap permits a priori error allocation and a standard complete-process circuit hybrid. The construction is polynomial in n,2^k,input bit length and log(1/error), not in k alone and not automatically a practical implementation.

## Verdict and limitations

**PASS at the stated constructive paper-circuit scope.** No additional load-bearing correction was found. This earns a real local acquired W interface for the rational-input threshold family, rather than invoking a free inverse-fibre oracle. The broader weighted-grand-coupling mechanism is established prior machinery; this receipt claims neither originality nor superiority over equally informed retained ordinary algorithms.

The complete native controlled-source theorem must still bind the correct uniformized channel, its return bound, and final source dephasing for a public CQ interpretation. This local receipt does not identify a raw coherent lift density matrix with a classical-source output. No arbitrary coherence-sensitive source intervention, microscopic jump-record disclosure, unknown mechanism learning, or uncharged mean Hamiltonian is granted.
