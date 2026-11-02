# Fresh adversarial audit: weak-endcap resonant thermal compiler

2026-11-02. Independently checked the displayed algebra and bounds in `resonant_rod_bound.md`, the exact gas/gauge argument in `native_thermal_interactions_20261101/root_rod_audit.md`, the independent isolated check in `unsuppressed_thermal_interactions_20261102/RESONANT_PATH_AUDIT.md`, and the actual-source resource substitution in `explicit_memory_witness_20261102/ROOT_NATIVE_TRANSFER_COROLLARY.md`. Numerical overlap tests are corroboration, not premises. No historical novelty assertion.

**Verdict:** The full thermal local-potential estimate (R) closes for the specified weak-endcap family, conditional on the stated exact controlled-Pauli Hamiltonian and the signed continuum KP theorem already used by the earlier proof. I found no missing K-dependent factor, wrap omission, X/Z factorization assumption, or unjustified global-vacuum projection. This is not a generic-imperfection or practical-device theorem.

## 1. Exact identities, all K >= 3

The Dirichlet inverse is `G_ij=min(i,j)(K-max(i,j))/(tK)`. Thus `Gv=1/t`, `v^TGv=2/t`, `v^TG²v=(K-1)/t²`, `G_1n=1/(tK)`, and `(G²)_1n=(K²-1)/(6t²K)`. These give precisely M0, M1, J0, and the marked mean duration stated in the target. The gap bounds follow from `2x/pi <= sin x <= x` on `[0,pi/2]`.

For b <= mu/2 the unmarked resolvent bounds use nonnegative spectral weights and are valid. Crucially, the marked endpoint bound does NOT follow from an entrywise PSD comparison: its independent constant-cofactor determinant proof is correct. With `Tr G=(K²-1)/(6t)`, `-log(1-z)<=z/(1-zmax)` yields the stated logarithmic tilt bound. Markov's inequality with c=t/K² and c/mu<=1/4 proves the tail `exp(2/9-beta*t/K²)` without a hidden polynomial prefactor.

## 2. Exact shared-clock gas and signs

For a commuting stabilizer family with commuting one-site factors within each check, the ordered prefix gauge leaves only commuting stabilizer operators and scalar pairwise Pauli commutation signs. The formula in the previous audit correctly includes both earlier-prefix and later-prefix signs. Replacing the two endpoint amplitudes t by g changes scalar path weights, not this algebra. The signs are flux-independent even for X/Z checks sharing data.

Each maximal nonzero interval has one exit start and positive circular duration; its start integration is beta, not beta minus duration. A never-vacuum history is a fixed-origin trace wrap with no extra start integration. Ordinary path interiors cannot cross the closing edge; the parity of endpoint type is precisely the flux exponent. Wraps have no individual flux but still interact with neighboring rods. Same-clock exclusion is hard core; every other pair factor has modulus one. Overlap in time and the clock overlap graph are necessary for a nontrivial interaction. These facts earn `|f|<=2`, temporal overlap-start measure at most l+l', and the continuum signed-gas criterion; replacing this by independent-clock Gibbs traces would not.

The unphysical full flux cube can be used formally since the gas remains uniformly convergent there; the physical syndrome constraint is imposed after the local Fourier estimate. No probability that all clocks are in vacuum is assumed.

## 3. Constant audit

Write `x=D exp(kappa) eta²`. Under x<=1/64 and K>=3,

- `a0=64x/K<=1/3`, so exp(a0)<2.
- `b=32x*t/K²<=mu/8`, stronger than the needed mu/2.
- With (T), the KP integral is at most `16 Dbar (g²/t) l + [16(K-1)+4K] Dbar g²/t²`, hence at most `16 Dbar (g²/t)l+20 Dbar g²K/t²`.
- This is safely below `b*l+a0`. Wrap roots obey the same conservative bound: the neighboring ordinary start measure is beta, no larger than beta+l'.
- The exponent in the marked remainder is
  `a0+b(K²-1)/(3t)=x[64/K+(32/3)(1-1/K²)]`.
  This decreases for K>=3 and is `832x/27 <32x` at K=3.

Therefore the claimed bound

`sup_a sum_(B contains a) exp(kappa diam(B)) |r_B|/J0 <= exp(2/9-beta*t/K²)+exp(32x)-1`

is valid. Marking a winding rod on a selected clock overcounts, never undercounts, Fourier clusters containing that clock. The k-1 other rod weights pay the spatial diameter. The start integral cancels 1/beta. The exact winding integral includes all internal backtracking, so an extra perturbative internal-path remainder would be double counting. The finite-beta missing singleton tail and all wrap-containing clusters have both been accounted for.

## 4. Explicit simultaneous thermal/physical scale admission

Let `B=beta*J0` and keep x fixed. Then

`t/J0=K³/(2eta²)=Dbar K³/(2x)`,
`g/J0=K²/(2eta)`,
`beta*t/K²=B*K/(2eta²)`.

The largest individual displayed onsite coefficient is 2t, so its ratio to J0 is `Dbar K³/x` (not merely t/J0). These are polynomial in K and Dbar at fixed margin. They need not be remotely practical. A simple sufficient simultaneous choice is

`x <= min(1/64, log(1+epsilon/2)/32)`

and

`B >= max{B_c, (2eta²/K)[2/9+log(2/epsilon)], (2eta²/K) log[K(K-1)/eta²]/(4-32x)}`.

The last term suffices for (T), using mu>=4t/K²; the middle term pays the tail. Hence there is no conflict between the independent code cold condition and wrap/tail admission. Holding beta*t fixed while changing eta is not this admission. The constants in the code's witness threshold B_c and the overlap degree must be supplied by the actual source, not wished away.

## 5. Raw generic-source column improvement: valid, but separate

For one scalar absolute clock,

`h_abs = [[0,-g v^T],[-g v,A]]`.

Completing the square gives, for a scalar vacuum amplitude z and excited vector y,

`<h_abs> = (y-gA^-1 v z)^* A (y-gA^-1 v z) - (2g²/t)|z|²`.

Thus `h_abs >= -(2g²/t)|0><0| >= -(2g²/t)I`. For m unrestricted clocks the absolute path semigroup therefore obeys

`Tr exp(-beta sum_a h_abs,a) <= K^m exp(2beta*g²*m/t)`.

Time-ordered source insertions obey the same exponential factor by multiplying semigroup operator-norm bounds over intervals whose lengths sum to beta, with insertion norms/entrywise-absolute coefficient overhead charged separately. Consequently replacing the old unrestricted-clock factor `K^m exp(2beta*t*m)` by `K^m exp(2beta*g²*m/t)` is justified for the raw full-column bound. Bath dimensions and all local expansion overheads remain.

At fixed B=beta J0, the improved factor is exactly `K^m exp(B*K*m)`. It is an enormous improvement over the old resonant substitution, but still exponentially costly in K and is NOT a polynomial generic perturbation tolerance. Moreover full-time source/rod KP charges scale with beta Dbar g²/t, and the normalized source ratio/logarithm needs its own proof. A raw bound does not establish a normalized-source future-proof theorem, a mixed-source stability theorem, or a dynamical theorem automatically. The old doubled-charge admission must be recomputed with the resonant resolvents if invoked.

## 6. Actual genealogy and nativity

The earlier original-family join used K=7. The later deterministic small-scale source substitution explicitly does not: its conservative unchanged-cell admission is w_X<=180 and w_Z<=15, hence K=180 is safe. Using K=7 for that latter source without a new incidence/basis proof would be an error. The source's geometric routing theorem and removable-witness/filling hypotheses remain imported components, not established anew by this clock audit.

The specified interactions really are two-body clock–data terms: each hop is a rank-two clock transition tensored with a single-site Pauli; identity padding and the 2t excited-level penalty are onsite. This statement admits an arbitrary K-level local clock and arbitrary corresponding qubit–qudit Hermitian coupling. It is NOT a qubit-only, fixed-exchange, low-control-complexity, low-dimensional gadget implementation; compiling each K-level device into qubits may change body order/resources. The actual code's check geometry/overlap must remain bounded, and all clock-device complexity must be charged. For fixed K=180 and bounded actual D this is a volume-uniform mathematical model, not a realistic-temperature claim.

The baseline inequality `sum H_internal,a >= mu sum Q_a` is valid despite noncommuting shared-data hops: each summand is separately gauge-equivalent to A on Q_a and operator inequalities add. The commuting occupation projectors give the stated baseline kernel/gap; simultaneous diagonalization of the separate path Hamiltonians is neither needed nor earned.

## 7. Excluded variant and stopping scope

This result is exclusively `g=eta*t/K`, no vacuum counterterm. The isolated counterterm construction with g proportional to K^-1/2 is a different, still-unproved many-check family. Its isolated positivity cannot establish intersecting shared-data kernels or a uniform thermal gas, and its K^-2 coefficient must not be credited to the present K^-3 result. Ideal endpoints, actual joint-Gibbs loading, generic perturbations, bath assumptions, and noisy implementation remain their separately charged gates.
