# The source-conditioned switch works from ANY actual input law

New strengthening of SOURCE_CONDITIONED_CORE_SWITCH.md. Preserve that
source at its original proved boundary scope. Its boundary monotonicity
is unnecessary once one uses the actual killed current rather than the
sign of a Green density. The SOURCE selection remains part of the
operation; this is NOT a uniform bound conditional on a rare source.

## 1. Current bound from a genuine incoming probability

Let Q be any finite reversible birth/death core component, mu any acquired
positive reference, and H>0 the total pre-source killing hazard. Start
with ANY probability rho on that component, including any interior point
or a law received from earlier physical motion. Set

    nu=rho*(-Q+diag H)^(-1), f=nu/mu.

For edge conductance c_j=mu_j Q(j,j+1), exact balance gives

    I_j:=c_j(f_j-f_(j+1))
         =sum_(l<=j)(rho_l-nu_l H_l).                  (1)

Since rho1=nu H=1, |I_j|<=1. No monotonicity of f, stationarity of rho,
profile ratio or mixing rate is required.

If u is ANY monotone function with 0<=u<=1 and a post-source reversible
conductance satisfies 0<=c'_j<=epsilon*c_j, then

    |sum_j c'_j(f_j-f_(j+1))(u_j-u_(j+1))|
       <=epsilon*sum_j |I_j|*|u_j-u_(j+1)|
       <=epsilon.                                     (2)

This is the actual current-total-variation operation. It pays changes
of sign of the interior-input Green gradient, rather than supposing that
gradient has the boundary sign.

## 2. Raw source1-to-source2 consequence

For the two C3/core ports at anchors1,1, choose either port i whose
landing coordinate C_i is at least n throughout the physical core
component. A large negative residual C_i-B_i>=n suffices; the OTHER
port may have either residual sign. Before the first block reaction
let h_i=alpha_i1 B_i, k_i=B0+h_other. After source1_i, retain the actual
anchor2 and C_i+1. Omitting additional competing exits only for an upper
bound, let u be the probability that k_i wins before actual own source2.

The exact source shift supplies

    mu'=mu/(C_i+1), c'_edge<=2c_edge/n,
    mu'*(2 alpha_i2 B_i(C_i+1))=2 alpha_i2 B_i*mu.

The winning function u is monotone in the ordered minority coordinate,
by the ordered nearest-neighbour coupling and increasing own/decreasing
opposing kill hazards. Therefore (2) applies for EVERY rho.

The exact identity (10) in the previous source then proves

    P(first source1_i, then k_i before own source2_i)
       <=3 alpha_i1/(2 alpha_i2 n).                    (3)

The probability includes the actual first-source selection. A very rare
source-conditioned output may have a poor CONDITIONAL activation chance;
(3) pays its complete joint contribution instead of assuming a uniform
conditional receiving law.

For both negative residuals, summing (3) bounds two phase1 source1 events
before source2, with arbitrary incoming law, minority population and hot
ratio. Thus the full corner proof in NATIVE_SIGNED_RETURN_THEOREM.md
does not rely on the accidental empty-endpoint monotonicity. Its actual
boundary input remains valid, and the operation can now be reused after
more general conservative/activation paths.

## 3. Generality and remaining physical obligation

Equations (1),(2) are a general finite ordered-core rule. The precise
mass-action shift and source-weight cancellation are still acquired
premises of the C3 application. On a higher-dimensional conservative
graph, |edge current|<=1 alone does NOT bound the sum of variations of u
over all edges; a corresponding raw variation operation must be earned.
No arbitrary-graph or unrestricted-WR transport theorem is asserted.

The probability bound is distinct from a physical-return theorem.
The actual low-corner residence and every received output are paid in
the signed-return sources. The operator bound alone is not inwardness.
