# Exact Gauss-law tree dressing of the compiled finite term

This is a gate compiler, not a claim of mirror decoupling or a gauged continuum limit. Input A_X is an already charge-pinched term from POLYNOMIAL_QUANTUM_TERM_COMPILER.md, so [A_X,sum_(x in X)Q_x]=0 exactly. The onsite charges are finite integer-valued after the audited D† frame and cutoff.

## Sign convention and algebra

Orient every link e:s->t. Let [E_e,U_e]=U_e, so U_e raises electric flux by1. Define divergence with +E on outgoing and -E on incoming links, and

 G_x=Q_x-div(E)_x.

Under exp(i sum alpha_x G_x), a link U_e transforms by exp[i(alpha_t-alpha_s)]. Fix a spanning tree rooted at r. W_rx is the ordered product of oriented U_e along the tree path r->x (negative exponents for traversing an oppositely oriented link). It transforms by exp[i(alpha_x-alpha_r)]. Define

 T_X=product_(x != r) W_rx^(-Q_x),
 A_X^g=T_X A_X T_X†.

An A matrix element with charge changes Delta q_x acquires product_x W_rx^(-Delta q_x). Its gauge phase cancels the matter phase at each non-root site; the residual root phase vanishes because sum_x Delta q_x=0. Hence [A_X^g,G_x]=0 for every x. If one instead defines G=Q+div(E), all dressing exponents reverse; this is a convention, not an ambiguity left in the compiler.

For edges oriented away from the root, an equivalent electric-basis description is

 Delta E_e=-sum_(x in subtree below e) Delta q_x.

At every vertex div(Delta E)_x=Delta q_x, including the root by total-charge conservation. This directly verifies all Gauss constraints without using gauge angles.

## Polynomial reversible circuit

Compute each onsite integer Q_x and its tree-subtree sums by a bottom-up reversible addition circuit. Applying T_X† shifts each tree-link electric integer by +sum_subtree Q_x. Apply the existing block encoding of A_X. Recompute the output charges and apply T_X, shifting by minus the output subtree sums. Uncompute charge work registers. No matrix element of A_X, no charge-sector basis, and no link-angle integral is enumerated.

The charge-pinching input/output equality register from the existing compiler ensures sum Delta q=0 on the accepted block. Unsuccessful block-encoding branches need not satisfy Gauss law; the encoded Hamiltonian block does exactly. Tree dressing preserves the block-encoding normalization.

For a support with n_X sites, charges bounded by Qmax_x, let Qtree=sum_x Qmax_x. Subtree sums use O(log(Qtree+1)) bits. The circuit costs O(n_X) reversible integer additions plus the original term block encoding, with a polynomial bit-arithmetic overhead. A simple path-by-path implementation would cost O(n_X²), still polynomial. The tree can be chosen inside a connected enlargement of the original radius-r support; its volume is polynomial in r at fixed spatial dimension.

## Finite electric cutoff: padding, then final overflow rejection

On the infinite electric integers, every shift above is unitary. For retained links |E_e|<=M_E, implement the same integer arithmetic in a padded work register covering at least |E_e|<=M_E+Qtree. Do NOT use cyclic wrap as the physical electric field. Do NOT reject an intermediate shift solely because it leaves the retained interval: a later shift may return it, and early rejection changes the target operator.

After both tree factors and the matter block encoding, accept only if all output links return to [-M_E,M_E], along with the matter-cutoff and block-encoding acceptance tests. The resulting Hamiltonian block is exactly

 P_E A_X^g P_E,

up to the already recorded coefficient/circuit approximation. P_E is diagonal in electric fields and commutes with every G_x, so the accepted ideal Hamiltonian block still satisfies Gauss law exactly. Arithmetic padding prevents modular aliasing. The added bit cost is O(n_X log(M_E+Qtree+1)), and all shift/overflow operations have polynomial gate cost.

This construction pays local gauging of the finite compiled interaction. It supplies no spectral estimate for the resulting dynamical gauge theory. Electric cutoff accuracy, background uniformity, low-energy matter content and mirror-decoupling bounds require their own physical/spectral arguments.
