# Full three-label affine balancing fails on an actual TP source

The strongest remaining permutation-balancing comparison is false, not merely its pair version. This is a positive-deficit example, not a value counterexample.

Use the actual source and dual Gram conventions of `three_block_pure_success_dual_star_interface.md`. Set p=1/6, d=p/3, and

x=(49/60,1/120,1/120), c=(3/40,1/560,1/560).

All entries are rational, sum x=1-p, and c_i^2<d x_i. Thus physical reset weights are w=x/(1-p)=(49/50,1/100,1/100), and overlaps r_i=c_i^2/(d x_i) lie strictly between zero and one. Logical dimension two suffices: take s=(0,1), v_i=(sqrt(1-r_i),sqrt(r_i)). The channel is p rho tensor P_s+q Tr(rho) sum_i w_i P_i tensor P_vi.

Full averaging of the six code-label permutations in the dual sends x to (q/3,q/3,q/3) and c to (sum c/3,sum c/3,sum c/3). This is the actual uniform-weight source comparison proposed; it is not an arbitrary abstract matrix perturbation.

60-digit spectral evaluation gives

Delta(actual)=0.001278170871053545899534651217830493693310093029217009014,
Delta(balanced)=0.001427928594544555498921218491724875675904700632095554413,
actual minus balanced=-0.0001497577234910095993865672738943819825946076028785453993.

Reproducer `three_star_full_balancing_exact_failure.py` checks positivity, computes the dual spectra at high precision, and independently reconstructs both original TP Choi sources and WH outputs. The replay discrepancies are below 2e-15. The diagnostic optimizer is `three_star_full_balancing_targeted.py`; its floating candidate is not needed for the final witness.

## Structural small-overlap obstruction

Let ell(a,b)=(log a-log b)/(a-b), continuously at equality. At fixed p,x, expansion around c=0 is

Delta=sum_i k_p(x_i)c_i^2+O(||c||^4),
k_p(x)=ell(p/3,x)+(1/3)ell(p,x/3)-(2/3)ell(p/3,x/3).

This follows directly from the exact 2x2 input blocks, 4x4 reference arrowhead and three 3x3 WH pair blocks. Spectators cancel. Every baseline eigenvalue in these supported blocks is positive, so the expansion is analytic. k_p(x)>0 is the previously received linear overlap resource, with its positive scaling factor.

The balanced quadratic term is [k_p(q/3)/3](sum_i c_i)^2. Thus a necessary and sufficient condition for this quadratic balancing inequality is

[k_p(q/3)/3] sum_i 1/k_p(x_i) <= 1.

At the rational p,x above the left side is 1.25301574674338642991392390724470988522589717. In particular, choosing c_i=epsilon/k_p(x_i) yields a whole small-positive-overlap family violating balancing, for sufficiently small epsilon. This establishes the structural obstruction independently of the finite-overlap witness. It does not deny nonnegativity of the deficit or the audited uniform-weight theorem.

## Remaining scope

Zero-weight and zero-overlap boundaries are paid by actual orthogonal direct sums into the received two-block class. All overlaps equal to one reduce to the received arbitrary-qutrit reset theorem. Faces with only one or two overlaps saturated, and the unequal-weight interior, are not closed by this note. Generic affine convexity, pair affine averaging, and full three-label affine averaging are now separately refuted. Any stationary/balancing proof must use a different constraint or an explicit compensating resource.
