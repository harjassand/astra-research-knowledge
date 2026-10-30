# Finite-phase extension with one exponent chosen before the corner width

Status: personally derived, not independently reviewed. This extends the accepted finite-phase proof mechanism; no global multidimensional recurrence claim follows.

## Statement
For the weakly reversible finite-phase/one-unbounded-count model of the accepted theorem, EVERY fixed rational alpha∈(0,1/2) admits an eventual dual certificate

    mu(r,j)=Gamma(r+1)^(−alpha) v_j(r),

where r=n+beta_j is the accepted integer residual coordinate and v_j is a positive rational function of r^(1/q) when alpha=p/q and rates are rational. Consequently the stationary law on each nontrivial class has moments exp[s n log(n+2)] for every s<alpha. The permitted alpha interval does not depend on the number of phases, rates, or reaction orders; the eventual threshold and polynomial prefactors DO depend on them.

## Accepted ingredients retained exactly
The phase-tree construction supplies integers beta_j, exact frozen phase stationary weights p_j(r), and edge fluxes

    F_e(r)=p_j(r)lambda_e(r)~c_e r^(h(source)),
    h(j,a)=a+beta_j,
    delta_e=h(target)−h(source).

The exact frozen balance gives

    u^T P G u=−(1/2)sum F_e(u_k−u_j)^2
               +sum F_e(t_e−1)u_j u_k.

Projected phase components are treated separately. If all delta_e=0, residual-count classes are finite and no tail argument is required.

## Growing tilt and the changed return path
Use

    t_e(r)=r^(alpha delta_e) 2^|delta_e|.

For downward edges, t_e≤1/2 eventually, and their exact quadratic contribution is

    −t_e F_e(u_k−u_j)^2/2
    −(1−t_e)F_e(u_j²+u_k²)/2
    ≤−F_e(u_j²+u_k²)/4.

DROP the downward Dirichlet term completely. This avoids a coefficient that vanishes as r grows. Horizontal edges retain−F_e(u_k−u_j)^2/2. For upward edges, the same Young inequality as before gives

    contribution≤−F_e(u_k−u_j)^2/4
                  +C_e r^(2alpha delta_e)F_e u_k².

Let E_r be the sum of these retained up/horizontal Dirichlet terms and downward endpoint sinks.

For an upward edge with source height h and increment delta>0, take a weakly reversible return path from its target and stop at the FIRST DOWNWARD EDGE, not at the first return below h. Before that edge every step is horizontal or upward. Hence every path source height is at least h+delta. The last edge has a downward sink at its source; the preceding edges have retained Dirichlet terms with fixed coefficients. Telescoping along the finite path yields

    r^(2alpha delta) F_up u_target²
       ≤C r^[−(1−2alpha)delta] E_r(u).

Since alpha<1/2 and the finitely many nonzero increments are integers, the sum of all upward burdens is eventually≤E_r/2. Thus

    u^T P G u≤−E_r/2<0 for u≠0.

Strictness follows from connectivity: E=0 makes values equal along up/horizontal edges and zero at both ends of every downward edge. Therefore G(r) is Hurwitz eventually.

This proof does NOT establish the entire interval alpha<1. The universal half interval is what the displayed quadratic estimate earns.

## Exact shift lift
Choose v(r)=(−G(r)^T)^−1 1>0. If alpha=p/q, every entry of G is Laurent-polynomial in z=r^(1/q), so every v_j is rational in z. Positivity and its leading Puiseux term give

    v_j(r−delta)/v_j(r)=1+O(1/r),
    lambda_e(r−delta)/lambda_e(r)=1+O(1/r).

For integer delta,

    [Gamma(r+1)/Gamma(r−delta+1)]^alpha
       =r^(alpha delta)[1+O(1/r)].

Thus every nonhorizontal actual incoming adjoint term is eventually bounded by its inflated t_e term. Horizontal shifts are exactly zero and require no approximation. Consequently

    L*mu(r,j)≤−Gamma(r+1)^(−alpha)

outside a finite set. The accepted summable-dual/regeneration argument applies because mu and mu times the polynomial total rate are summable. Returning from r to n changes only polynomial factors.

For arbitrary fixed positive real rate constants, the same asymptotic argument holds with real coefficients; the rational-input statement is the effective algebraic interface, not a restriction of the conceptual proof.

## Why this matters for boundary assembly
One may choose the bulk alpha<1/2 FIRST, then choose a finite corner alphabet of any size, without shrinking alpha a second time. This removes one specific exponent/phase-width circularity for one-unbounded-coordinate corners. It does not remove interface feedback or solve corners with multiple unbounded populations.
