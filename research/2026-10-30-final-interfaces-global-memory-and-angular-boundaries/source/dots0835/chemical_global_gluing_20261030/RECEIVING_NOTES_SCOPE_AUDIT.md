# Final receiving-notes scope and consistency audit

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal review. Four short notes reviewed; no new fixtures or literature search.

## Verdict

All four claims pass in their stated supporting scope. None is a global recurrence theorem. Two minor precision improvements are noted below; no substantive defect was found.

### EXACT_BULK_CERTIFICATE_SEARCH.md

For alpha=1/p, the boundary dissipativity test becomes a polynomial sentence in nonnegative u with sum u_i^p=1 and product u_i=0. The established small-alpha result guarantees acceptance for all sufficiently large integer p. Compactness supplies a rational strictly negative margin, so reciprocal enumeration and real quantifier elimination terminate.

The exact normalized adjoint L*mu/mu is algebraic even though mu itself contains factorials: all factorial ratios have fixed integer shifts and reduce to finite products or reciprocals thereof. Positive p-th roots can be introduced as uniquely specified auxiliary variables. A rational stoichiometric affine space has rational linear defining equations. The conservation/escape proof works for real positive points as well as integer states, so the bad real semialgebraic set is bounded after choosing K. The final QE search is therefore genuinely justified and is not an implicit appeal to integer quantifier elimination.

Minor precision: explicitly reserve slack, e.g. certify H≤−4eta on the simplex boundary, use continuity to get H≤−2eta nearby, and choose the factorial error≤eta. This makes the eta-to-K-to-R order completely unambiguous. The elementary error constants can be overestimated rationally. No efficiency, manageable coefficient size, or boundary completion follows.

### STATIONARY_SHELL_PRODUCT_LIMIT.md

At (A,C,B)=(0,N,0), only immigration is outgoing, at rate one. The sole valid incoming connector is clearing from (3,N,4), with rate 6*24=144. The sigma ratio is

    binom(N+3,3) [product of three P/Q factors] Z_N/Z_(N+3).

Each product factor is at least 1/2, and three successive normalization bounds give a fixed positive lower bound on Z_N/Z_(N+3). Hence this ratio is at least cN³. The radial factorial ratio contributes order N^(−3beta), proving the positive corner defect for beta<1. The predecessor lies in the already verified physical class and clearing reaches the corner. This defeats the displayed stationary-profile product, not every possible global use of the shell profile.

### RESIDUAL_SOFTMAX_FAILURE.md

At (n,1), the two available residual factorial terms sum to (n+1)/n!, and q=1+2n. Immigration from (n−1,0) contributes n^alpha/(n!)^alpha. At clearing predecessor (n+2,4), the three residual terms, after factoring 1/n!, are exactly 1, 1/[6(n+1)], and 1/[24(n+1)(n+2)]. The clearing fraction of its total activity is exactly the stated R_n. Therefore the normalized adjoint expression is correct and tends to one for 0<alpha<1.

The outward class path gives (3n−2,3n−2)−(n−1)(2,3)=(n,1). The return path gives (n,1)+(3n−2)(1,2)−(2n−1)(2,3)=0. Intermediate source requirements hold, including n=1. At c_A=3/8,c_B=4/3 all three deterministic cycle fluxes equal one, verifying complex balance.

Minor precision: a general expression nu/q is defined only where q>0; the displayed network has immigration q≥1 everywhere, so its counterexample is unaffected. This note falsifies this algebraic residual-softmax ansatz, not all possible algebraic corrections.

### MULTILINKAGE_FRACTIONAL_OBSTRUCTION.md

The exact leading terms are 100c^(2−alpha)+c^(1+alpha)−100c²−c. Differentiation at c=1 gives −99alpha. Thus a fixed c<1 sufficiently close to one gives positive leading coefficient. Finite-factorial errors are O(n), while the immigration/death linkage contributes powers no larger than order n for 0<alpha<1; both are lower than n².

The slow network makes the entire lattice communicate and has exact total-population drift 2−(A+B); fast reactions conserve total population. The standard norm-like drift argument therefore establishes positive recurrence of this example (with nonexplosion also obtainable from its total-population immigration/death process). The calculation is a genuine obstruction to the UNWEIGHTED fractional-factorial extension, not to recurrence or a fugacity-corrected treatment of the fast linkage.

## Overall scope

The search note establishes effective acquisition only of the already proved bulk certificate. The other three notes delimit unsuccessful global representations. None silently supplies boundary feedback control, a stationary law for the general network, or a global Lyapunov function.
3b73778c2f26a40ebf5d2e772d940ecba7144c1fcf76142162a7085ddf692b74  producer-workspace/EXACT_BULK_CERTIFICATE_SEARCH.md
d2055b73d0752d88dd662dfca478f711f558bb71c17c3177cf5b0f4f6bd2bc16  producer-workspace/STATIONARY_SHELL_PRODUCT_LIMIT.md
7a09f9afbf422c8d4e93c573a34e616ac6030dca36d57f1b7d7ec160df8bd984  producer-workspace/RESIDUAL_SOFTMAX_FAILURE.md
cd3df49239e6e6726956c4c35ae349e43463bd3a42f49dd82c6a0e4fc5188526  producer-workspace/MULTILINKAGE_FRACTIONAL_OBSTRUCTION.md
