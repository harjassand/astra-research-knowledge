# Independent audit of the extensive no-emission theorem

Auditor: joint-record-bound child worker, 2026-10-29.

## Verdict

No mathematical error found. The construction does establish an existence-level extensive same-slab absence estimate, and therefore a local-stochastic bound for arbitrary marked site/slab subsets on a chronological slab grid. It does not rely on an unjustified product of marginal probabilities or on mixing alone.

## Checked steps

### Full-qubit local-progress extension

On the full qubit space, the Hamiltonian off-diagonal observable in L*n_x is O_x=ig G_x(sigma-_x-sigma+_x), not the unguarded lowering operator. Its norm is at most g. The self-site double commutator is exactly 2g^2 G_x(1-2n_x). Subtracting 2g^2 G_x leaves a diagonal term whose expectation has magnitude at most 4g^2<f>. Neighboring Hamiltonian contributions remain x-off-diagonal, with each norm <=2g^2; all non-neighbor centers commute. Dissipators outside the closed star cancel, and the remaining dissipators preserve x-off-diagonality. Consequently the previously supplied loose curvature constant remains valid. Neighbor-count damping identities are also unchanged on the full tensor product. Thus the local-progress input really applies to arbitrary illegal/full-qubit configurations as claimed.

### Local Taylor counting

Artificially counting x in the support ensures the added killing term is always included. At most (D+3)|support| local terms are relevant, with individual norm <=2(g+kappa), and the support size after j applications is <=1+jD. This yields the safe coefficient base 2(g+kappa)(D+3)(D+1), which is less than C0=4(g+kappa)(D+2)^2. The k! bound follows. No global generator norm is hidden here.

The graph radius can grow by at most two per generator application because each guarded Hamiltonian is a star, whose diameter is two. Therefore F_x^(m) is indeed supported in B_{2m}(x).

### Polynomial and shifted residual

Applying K to F_m yields sum_{j=1}^{m+1}delta^j K^j(I)/j! EXACTLY. Thus its discrepancy from exp(delta K)I-I starts at j=m+2, not m+1. The geometric tail stated in the theorem is valid.

The survival operator lower bound exp(sK)I>=exp(-kappa s)I follows from a bounded target intensity, or directly from the differential trace inequality for the unnormalized no-target state. Hence aI<=F<=delta I. Approximation error <=a/2 implies a/2<=F_m<=3delta/2. The choice r=c/(3delta) correctly turns K F_m<=-(c/2)I into K F_m<=-rF_m.

### Exact product calculation

For selected centers separated by more than 4m+2, the support B_{2m+2}(x) of L*(F_x^(m)) is disjoint from B_{2m}(z) for every other selected center z. Hamiltonian commutators satisfy the Leibniz rule exactly. Each on-site damping term acts nontrivially on at most one factor, so its dissipative product correction vanishes. Each selected J_x acts only in its own factor. Thus the displayed product-generator identity is exact.

Each operator inequality K_x F_x^(m)<=-rF_x^(m) can be multiplied by the remaining positive factors because their supports commute with the entire local summand. The sum is therefore bounded by -rs F. For additional marked sites, J_x(F)>=0 follows from complete positivity and F>=0; no support or commutation condition is needed for this subtraction.

### Semigroup comparison and extensive exponent

For a positive semigroup, K_S F<=-rsF implies exp(tK_S)F<=exp(-rst)F by applying positivity to the Duhamel integral for K_S+rs. The lower and upper scalar bounds on the product F then give (3delta/a)^s exp(-rst).

The packing bound s>=|S|/B and s<=|S| imply

 (3delta/a)^s exp(-rst)
 <=(3delta/a)^|S| exp[-(r/B)|S|t],

because 3delta/a>=3>1. The degree-dependent ball-volume overestimate B=(D+1)^(4m+3) is safe, including D=0.

### Chronological slab conditioning

After conditioning on no-target emissions in all preceding slabs, the normalized current clock state is arbitrary. The extensive one-slab theorem applies to that state, so multiplying its conditional bounds is valid. This is not conditioning on simultaneous future records. Taking T large enough that C exp(-gamma T)<1 produces the stated product over marked site/slab cells.

## Scope cautions, not proof defects

- The theorem's constants can be extremely poor; no weak-drive-optimal gamma scaling follows.
- It treats the specified ideal Markovian clock. Physical error propagation, complementary auxiliary sectors, implementations, and a fault-tolerant computational threshold remain separate issues.
- The slab law is immediate on a common chronological grid. More general overlapping time windows require a reduction or separate argument and should not be silently included.
- An empty marked set has probability one, consistent with the exponent convention.
