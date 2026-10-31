# Review-derived finite-bit threshold Stinespring construction

31 October 2026. This is a fresh paper circuit construction closing the acquired-W seam in the threshold Glauber receiving candidate. It is not an executed quantum gate backend. The weighted inverse-map mechanism is established quantized-coupling machinery; the purpose here is to give the actual finite arithmetic and coherent work interface required by the retained-source compiler.

## 1. Exact input model and size

Use the threshold maps f of the receiving candidate. There are F=O(n 2^k) nonzero interval colors. Each color changes only its designated site, with a predicate on at most k neighbors. Its positive rational weight is w_f=Delta_f/R. Require supplied positive rational local Boltzmann factors, each of at most B input bits, a finite list of local factors, and the declared bounded local context width. Their local products acquire the heat-bath rates and neighboring stationary ratios exactly as rationals; the global partition function cancels. Sort the rational local rates by exact cross multiplication and omit zero intervals. This makes thresholds and every preimage predicate exact, not approximate floating-point comparisons.

All rational numerator/denominator bit lengths below are bounded by a polynomial L in the explicit table/factor count, n, 2^k and B. Products, sums, differences, sorting and reduction by integer gcd have polynomial bit cost. In particular a small positive rational is not treated as a unit-cost inverse-probability oracle: its binary description and the arithmetic precision are charged. This input model does not include arbitrary real rate oracles without a certified comparison/precision interface.

## 2. Conditional probability table at a coherent input

For an input configuration x and a color f updating site i, its only possible preimages are y=x and y=x^i. Define a fixed two-slot table

p_(f,0)(x)=w_f 1_(f(x)=x),
p_(f,1)(x)=w_f (pi_(x^i)/pi_x) 1_(f(x^i)=x).

These slots are distinct labels even when one has zero weight. No other preimage exists. Reversibility and stationarity imply exactly sum_(f,j) p_(f,j)(x)=1 for every x. Each probability is nonnegative and at most one, and has polynomial rational bit length L. The ratios need only the local factor changes for a single spin flip. There is no evaluation of pi_x itself and no division by pi_min.

Given x in superposition, the entire table or any prefix sum can be computed reversibly by the same bounded classical rational algorithm. It uses local context queries, not enumeration over all 2^n source states. Zero probabilities are detected exactly.

## 3. Coherent preparation without small-mass postselection

Pad the 2F table to a power of two with exact zeros. The standard binary probability tree prepares

|x>|0> -> |x> sum_(f,j) sqrt(p_(f,j)(x)) |f,j>.

At each of O(log(2F)) levels, compute the two child masses for the current prefix, divide by their sum if nonzero, apply the corresponding controlled one-qubit rotation, and uncompute all arithmetic scratch. A zero parent mass uses any fixed rotation, since the ideal input amplitude there is zero. Computing a prefix sum by scanning the at most 2F entries is a sufficient polynomial construction; no efficient RAM oracle is assumed.

The child/parent quotient is computed by exact rational integer arithmetic and has polynomial bit length. Approximating its rotation to absolute operator error delta_rot costs polynomial(L,log(1/delta_rot)) arithmetic and rotation synthesis. Endpoint probabilities 0 and 1 are handled explicitly. For example, first approximate the two square-root amplitudes to sufficiently small absolute error and then their unit-circle angle; the square-root modulus bound prevents a hidden inverse-small-probability precision requirement. Equivalently an exact rational input of bit length L supplies an explicit binary scale for any nonzero denominator. Complexity depends on L, not on its exponentially large numerical reciprocal.

Because each controlled rotation has uniform operator error delta_rot, telescoping through the O(log(2F)) levels gives state-preparation error at most O(log(2F) delta_rot), uniformly in x. Reversible computation of angle bits is undone before proceeding. Choose delta_rot <= zeta/[10(1+ceil(log2(2F)))], and charge the elementary synthesis errors within the same budget. This yields a preparation isometry within zeta of the ideal, in operator norm on the input subspace. A more conservative polynomial-small per-rotation budget also suffices.

Numerically rounded circuits are actual unitary circuits. They do not define a non-trace-preserving approximation by independently rounding matrix entries. There is no conditioning, postselection, or division by the probability of a rare output branch.

## 4. Erasing the old source label and auxiliary slot

From the prepared (x,f,j), compute y=x for j=0 or y=x^i for j=1. Every nonzero ideal branch satisfies x=f(y). Erase the original source register by XORing f(y) into it. The remaining slot j is determined by f and y: it is zero when f(y)=y and one when f(y)=y^i. Compute that predicate and XOR it into j. Thus the old source and slot registers become clean, and the output is

W |x> = sum_(f,y:f(y)=x) sqrt(w_f pi_y/pi_x) |f>|y>.

The ordering can be implemented with reversible XOR operations and local tests; all intermediate arithmetic work is uncomputed. This is the actual Stinespring isometry of the weighted inverse-map channel. The output color f is retained as its environment, not measured or disclosed to the consumer. Recording all input configurations as additional environment data would be a different channel and is not done.

The displayed erasures are reversible permutations on the entire workspace. Their behavior on zero-amplitude or approximation-error branches is therefore well-defined even if such a branch fails the ideal preimage relation. Norm error cannot increase under these permutations. Gate reversal supplies W† with the same query/gate cost. The construction gives a unitary implementation on an enlarged clean-ancilla register; no black-box irreversible-channel inversion is assumed.

The ideal images for different x have disjoint support in (f,y), since f(y) identifies x. This also directly proves W†W=I and prevents an artificial sqrt(2^n) error conversion. More fundamentally the controlled-rotation circuit comparison above is already an operator-norm telescoping bound, so it is uniform on arbitrary coherent source inputs and reference systems.

## 5. Dark output, reference, and compiler error budgets

For the exact ideal construction,

W|psi> = |c>|psi>,    |c>=sum_f sqrt(w_f)|f>.

All amplitudes are chosen nonnegative; the actual implemented circuit fixes their phase convention. The color state c has an explicit polynomial-size probability table and uses the same finite-rotation procedure. If desired, the compiler's general phase-safe route acquires it from actual W on prepared psi followed by psi-unpreparation; the approximation errors then remain explicitly budgeted. An approximate W must not be declared to have an exactly factorized dark output without such an error statement.

For the admitted one-dimensional family, acquire psi and its reflection by the separately specified conditional-message preparation. This cost, including numerical precision, is additional to the local W circuit. For a finite simulator using at most Q_use calls to W, W†, c-preparation or reference operations, set each relevant operator/state error below epsilon_interface/[C(1+Q_use)] with the conservative constants required by the underlying simulator. Standard circuit telescoping then bounds the complete retained-process error; externally prescribed controls are contractions and do not expose the private colors. If the received simulator uses a square-root error robustness convention, reduce the local tolerance accordingly. This still costs polynomial logarithmic precision because its deterministic Q_use bound is fixed before choosing the tolerances.

The return certificate and exact classical law are statements about the ideal rationally specified channel. Approximate circuit errors are charged by this final algorithmic hybrid, not by silently asserting that approximate rates retain exact detailed balance or exact pure fixedness.

## 6. Resource and status conclusion

The acquired W has polynomial gate/arithmetic cost in n, 2^k, the explicit rational input length and log(1/zeta). One sufficient construction scans the full O(n2^k) color list per probability-tree level; no optimized bound is asserted. Global stationary probabilities, inverse-fibre oracles, exponential source-state tables, and a minimum branch-probability promise are unnecessary.

This construction supplies the missing Stinespring operations on paper for the stated positive rational local-table input family. It does not itself implement the full fast-source simulator, eliminate the cost of reference preparation or system mean action, or establish advantage over ordinary methods. The main threshold receiving source must incorporate or explicitly bind this construction before being called a completed acquired-interface theorem.
