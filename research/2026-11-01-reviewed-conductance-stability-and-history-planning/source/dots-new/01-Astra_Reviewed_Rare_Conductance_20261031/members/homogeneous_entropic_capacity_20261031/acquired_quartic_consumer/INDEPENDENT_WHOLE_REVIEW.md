# Independent whole review: acquired coupled-quartic conductance

## Verdict and immutable bindings

**PASS**, as the declared exact known-polynomial acquisition, full-diffusion mathematical certificate, and finite-budget producer/receiver. No blocking error or required source change was found. This is a separate whole review, not acceptance inherited from a Gaussian engine or the earlier conditional homogeneous theorem. It does not establish novelty, hardware/scientific applicability, arbitrary-start passage times, a sampler, or a general positive-polynomial solver.

I read the complete current proof, executable, author checks, cost/comparison and scope documents, both preceding theorem receipts, and their underlying candidate. I checked every entry of the 15-file immutable manifest before and after the copied executions:

- `FROZEN_SHA256.txt`: `49a881d08a60603f2363f9e3abe68e8340c5af450c8c8ebbf0c5e9ddd15bf4fc`.
- `PROOF.md`: `aadf1b05fcc2c153faf0b3c06a13caa8eeb5ce5c87a86c9150be3af0f3d22055`.
- `compile.py`: `45d75db5d0dac774df58070c66d11e9f7d0918bdd903489fdf71b61b9ea03fbf`.
- `check.py`: `a037547b0aeb3f580441227dad7bae1abcf0cce88306829ea9f49459e13c1d54`.
- `COSTS_AND_COMPARISONS.md`: `1d840fee9db870be241e21905c9d5e68fc2ac742ba02278ea3d7c311baaff827`.
- `SOURCES_AND_SCOPE.md`: `c952b57f48812e9232dea7c192b67ed20ed87e1ce213c205c28f0c1b3ddbf7ba`.
- `results.json`: `10f424c143f18ff8b8454aa0b09a23d33aac70528406e912df585cab70aaf6ac`.
- `dense_graph_raw.json`: `6940247d3357a5604543ddfabc722946f7b7dc57322dab36bb73f8a6186ed628`.
- `dense_graph_certificate.json`: `053ea86857468b0004b90d673b56ff4b46551caac543831dadc55b6295e8d47a`.

The manifest also binds README, executed-results report, dependency record and all three historical theorem files. Their immutable candidate/pending headers are preserved; this separate receipt records the later whole review. No original source, saved numerical certificate, timing report or manifest was edited. The sibling parallel-channel extension is explicitly OUTSIDE this receipt.

## 1. Raw structure is actually acquired

The input is the complete exact rational coefficient dictionary in the actual Euclidean coordinates. The code requires n>=3, no duplicate/zero monomials, strict bounded integer exponent vectors, and degrees 4, 6 or 8. Canonical rational strings or strict integers are used; bool/float aliases and noncanonical rational spellings are rejected.

The degree-four part has exactly one absent coordinate y. This is an acquired ALIGNED physical axis, not a supplied reaction coordinate or a general nonorthogonal metric transform. Positive quartic diagonals in every other coordinate guarantee that the accepted axis is genuinely unique. The ratio of the matching y^4 top coefficient to a degree-four coefficient is t=kappa/(1+kappa). Requiring 0<t<1 acquires positive kappa. Dividing the full degree-four part by 1+kappa acquires U. Every term must be a positive pure quartic or nonnegative mixed square-square term, with omitted interactions representing zero. All fiber diagonals must be strictly positive.

Most importantly, the code constructs and compares the ENTIRE dictionary F=[1+kappa(1-y^2)^2]U, including every degree-six negative coefficient and every degree-eight coefficient. This prevents a favorable Hessian/selected-coefficient recognition from admitting an unrelated potential. Arbitrary permutations/nonfirst axes are admitted. Generic rotated positive quartics may return UNKNOWN; no unsupported rotation acquisition is advertised.

The exact identity m sum z_i^4-(sum z_i^2)^2=sum_(i<j)(z_i^2-z_j^2)^2 proves U>=d_min||z||^4/m from the actual acquired coefficients. Mixed quartics need not be convex: the cited two-variable Hessian has eigenvalue 12-40 at (1,1) for coupling20. Coercivity, not convexity or rapid angular equilibration, is the load-bearing input.

## 2. Full process and partition cancellation

The process remains dX=-grad F dt+sqrt(2/beta)dW in the original Euclidean metric. Homogeneity gives the exact conditional scaling

    integral exp[-beta v(y)U(z)] dz = (beta v(y))^(-m/4) Z_U.

The finite angular constant Z_U is neither computed nor sampled. It cancels from the normalized marginal and the capacity/mass ratio. This is legitimate for this particular output, not acquisition of arbitrary angular observables or a normalized sampler. The true y drift remains -v'(y)U(z); there is no claim that projected y is Markov.

Global evenness of v earns equality of left and right basin masses. The basins are the acquired full fibers y<=-1/2 and y>=1/2, not user-arbitrary sets. The output is cap_mu(A,B)/mu(A), not arbitrary-state MFPT, finite-time crossing probability, or angular mixing time.

Coercivity makes each fiber partition and all polynomial conditional moments finite. For large y, q=v^(-m/4) decays as |y|^-m, so m>=2 is sufficient for global integrability. The explicit tail is actually included in the numerical mass upper endpoint. For nonexplosion, the coercive Lyapunov function 1+y^2+(1+kappa/4)||z||^2 has gradient pairing

    2[yv'+(4+kappa)v]U >= 8U,

because yv'>=-kappa and v>=1. Thus its diffusion-generator drift is bounded above by the displayed finite constant. Smooth local coefficients plus the stopped Lyapunov argument rule out explosion. The integrable smooth Gibbs density and conservative gradient diffusion give the reversible Dirichlet process used here. The unbounded valley z=0 is not silently replaced by reflecting or finite walls.

## 3. Conditional transport and the structural factor

The current w_y=-(v'/(4v))z satisfies partial_y rho+div_z(rho w)=0 exactly, by Euler homogeneity. The scaling/virial identity E U=m/(4 beta v), coercivity and concavity of square root give

    E||z||^2 <= [m/(4 beta a v)]^(1/2),  a=d_min/m.

This earns the stated current cost K=E||w||^2 without a conditional mixing assumption. For smooth admissible h, differentiating its conditional mean gives E[partial_y h+w.grad_z h]. Pointwise Cauchy followed by scalar weighted Cauchy yields the full Dirichlet lower bound 1/(beta Q R1); the source-independent trial h yields the upper bound 1/(beta Q R0). Coercive tails justify integration by parts and the weighted Sobolev extension. Equivalently, the analytical unit flow has energy R1. Its appearance in a proof does not require executing an unknown normalized fiber state.

With W=v^(m/4), -W'>=0 on the half slab. After substituting a=d_min/m, the current estimate is

    K W <= [1/(8 sqrt(beta d_min))] (-v')v^(-3/2)(-W').

Since -v'<=4kappa y and v>=v_min=1+9kappa/16, integrating y(-W') retains the NEGATIVE endpoint -bW(b). Dropping that favorable term proves

    R1/R0 <= C = 1+kappa/[2 sqrt(beta d_min) v_min^(3/2)].

There is no derivative-sign reversal, lost dimension factor, or inference from a pointwise current bound that grows with m. For beta=d_min=kappa=1, v_min=25/16 and C=157/125 exactly. The preceding theorem's looser factor remains valid and unchanged. Normalization Q cancels against mu(A)=MA/Q, giving the claimed full conductance sandwich.

## 4. Exact arithmetic and unbounded-domain receiving

The integrator is standalone standard-library code; it imports neither accepted Gaussian backend. At rational y it forms v^m exactly, then bounds its fourth root and reciprocal fourth root using nested integer square roots. The identity floor(sqrt(floor(sqrt(N))))=floor(N^(1/4)) and the exact powered equality test give outward dyadic endpoints. Nonperfect roots cost at most one dyadic unit. The square-root factor computation is also outward; exact rational perfect squares are recognized so the unit factor is exactly157/125.

Quadrature separates the turning point y=1: q increases on[1/2,1] and decreases on[1,infinity]; W decreases on[0,1/2]. Minima/maxima of endpoint enclosures therefore give valid outward Darboux sums. Geometric segments [1,2],[2,4],... use N cells EACH. The y=0 half-resistance is doubled. No integer-divisibility assumption m/4 is made.

For T>1 the code uses the exact powered upper bound

    tail <= kappa^(-m/4)(1-T^-2)^(-m/2) T^(1-m)/(m-1),

with the prefactor rounded upward by fourth roots. Physical m, not total polynomial degree or number of edges, controls this tail. The borderline admitted m=2 case is genuinely paid: the frozen unit fixture uses T=4096, not a compact-window approximation. A positive certified seed controls cutoff selection; unresolved seed or exhausted cutoff gives UNKNOWN.

Admission checks positive lower mass/resistance and the exact rational product-width inequality. The full interval then divides the free lower endpoint by an OUTWARD UPPER bound on C. These directions are all correct. An arbitrarily small displayed rate is not substituted for a tiny denominator in a sampling procedure: the exact rational arithmetic still carries its bit cost.

## 5. Budgets, verifier and failure scope

External beta/tolerance must be positive Fractions; every budget is a strict positive integer. Dimension/term/input-bit validation precedes acquisition; initial grid/cutoff, precision, accumulated distinct-point count, cutoff and successive grids are bounded. Point/tail high-degree powers and following root shifts are guarded before exponentiation. Failure is the documented Unknown exception, not an incorrect PASS or an unbounded tail-refinement loop.

The power-bit guard is NOT a total-program memory cap: Fraction additions, acquired coefficients, quadrature accumulation and final exact serialization have their own real costs. This limited proxy is explicitly stated in the cost document. Serialization beyond Python's configured decimal limit is UNKNOWN. Optional binary64 displays may be null and are not proof data. Timers exclude raw fixture generation/import/file parsing/output; no hardware performance comparison follows from them.

The receiver takes ORIGINAL raw data and externally supplied task/budget parameters. It repeats acquisition and the complete bounded integration, recursively compares exact types/values for all acquisition metadata except seconds, binds task, basin, observable, factor, grid, cutoff, precision and tail, and checks every exact interval endpoint. A certificate from a different graph is rejected even when its numerical interval happens to agree. Reordered identical raw terms are allowed. Timing, display and operation-count diagnostics are deliberately not authenticated by PASS. This is a sound incomplete deterministic receiver, not a general certificate language accepting every mathematically valid alternative grid.

## 6. Executed independent checks

All author files were copied to `producer-workspace/quartic_review_20261031` before running scripts that regenerate reports. The full author suite passed **2,550 assertions**. I separately implemented and ran **471 exact checks**:

- 306 independent powered-endpoint root enclosures, including perfect/zero cases;
- general unequal rational diagonals, sparse graphs and all four possible physical axes in dimension4;
- independent nonsquare factor inequalities and full receiving;
- all raw coefficients dropped, sign-flipped or perturbed;
- malformed schemas and noncanonical rational/bool/float records;
- recursive integer aliases in task/acquisition/graph metadata;
- interval, observable, basin, grid, factor and external-task substitution;
- exact tail-prefactor and pointwise tail inequalities for m=2,3,7;
- budget exits, including pre-exponentiation rejection with unchanged operation count;
- enormous versus omitted graph coupling giving the same COMMON certified bound;
- exact recomputation of all seven saved chain certificates and the saved dense-graph certificate.

Reproducibility artifacts added without modifying originals:

- `check_independent_review.py`: `94d2166bb7cce405b649a38a23e88beacb43b42a2b2e9959b123a0fbfc1e92f6`.
- `independent_review_checks.json`: `62e0f0a1519726528b7cb4c7e2155c8f794f266674d2d1ada71ef2b1fc10966e`.
- `independent_author_replay.json`: `4cfe00d9b7ff8adad45c044dc111f522b9918e02413c4ba78dcb92370076c78b`.

The independent script is run beside a COPY of compile.py and the three saved raw/result JSONs; it prints its report rather than rewriting those inputs. These finite tests support, not replace, the mathematical argument.

## 7. Consequence, costs and ordinary comparators

The 257-dimensional unit coupled-quartic chain has 1,533 expanded monomials, 6,145 distinct scalar points and exact interval displaying approximately[1.73513954e-18,2.19850233e-18]. Largest recorded point/tail power numerator/denominator is12,544bits; this is not whole-program peak memory. The ratio is at most(157/125)*1.01. All raw vectors and coefficients were inspected. Dense graphs have Theta(m^2) monomials and Theta(m^3) entries in this full-exponent-vector encoding, which must be read and stored; no succinct input claim is substituted.

For fixed m and unit beta,kappa with d_i>=1, arbitrary finite nonnegative static interaction graphs share q and k_free. Every full conductance lies in the same[125k_free/157,k_free] interval, so any two differ by at most157/125. This is a rigorous graph-insensitivity statement about this full-fiber equilibrium observable, NOT equality of true capacities, graph-independent arbitrary-start dynamics, angular equilibration, or a guarantee under unverified time-dependent changes. Each new polynomial still requires acquisition.

Homogeneous scaling, virial identities, coercivity, conditional transport, Dirichlet/Thomson principles and integer root/Darboux arithmetic are conventional components. Equally informed ordinary free-energy calculation obtains the same q and restricted upper bound. Giving it this radial-current argument obtains the same lower bound; no separation from ordinary mathematics is established. Full PDE/sampling methods remain valid and may be superior outside this grammar or for tighter answers. The prior trial-committor boundary-fidelity caveat was independently inspected in the earlier Gaussian review; the new bibliography is not treated as an exhaustive priority audit. No inaccessible source or new external action was needed here.

**Conclusion:** the complete acquisition-to-output conjunction is sound within its stated exact aligned quartic grammar. No physical calibration, hidden-coordinate generalization, fiber sampler, arbitrary first-hit-time theorem, or sibling parallel-channel executable is automatically received by this PASS.
