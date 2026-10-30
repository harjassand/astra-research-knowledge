# Fixed-tilt M-matrix theorem for weakly reversible finite-phase chemistry

29 October 2026. Derived and adversarially reconstructed internally; not externally reviewed or novelty-cleared. This note proves a finite-matrix statement. The separate parent note supplies the actual CTMC dual-measure lift.

## 1. Exact setting and residual coordinate

Use the contract and tree exponents beta_j from `FROZEN_DRIFT_THEOREM.md`. Define the integer residual r=n+beta_j in mode j. The rate of e:(j,a)->(k,b), evaluated at residual r, is

    lambda_e(r)=k_e (r-beta_j)_a,

and its exact residual increment is

    delta_e=b-a+beta_k-beta_j=h(k,b)-h(j,a),
    h(j,a)=a+beta_j.

For large real r all source factors are positive. Define Q(r) as the finite mode generator with these rates, ignoring the count displacement. A fixed shift inside a falling factorial changes neither its degree nor its leading coefficient. Consequently every tree polynomial has the same degree and leading coefficient as in the unshifted calculation, and the exact stationary law satisfies

    p_j(r)=c_j r^{beta_j}(1+O(1/r)), c_j>0.

Write F_e(r)=p_j(r)lambda_e(r). Then

    F_e(r)=k_e c_j r^{h(source_e)}(1+O(1/r)).

The exact finite-mode balance, not this asymptotic approximation, will be used in the quadratic-form identity.

Assume the non-invariant case: at least one delta_e is nonzero. Weak reversibility then supplies at least one downward edge. The projected mode graph is irreducible; disconnected projected components can instead be treated separately.

## 2. Tilted operator

Fix 0<eta<theta. Define t_e=exp(theta delta_e+eta |delta_e|), and the real Metzler matrix G(r) through

    (G(r)u)_j=sum_{e out of j}lambda_e(r)[t_e u_k-u_j].

For same-mode reactions the entire term belongs to the diagonal. Original reaction losses are retained. Horizontal reactions have t_e=1. Downward reactions have 0<t_e<1; upward reactions have t_e>1.

**Theorem.** There is a finite R such that G(r) is Hurwitz for every r>=R. Therefore -G(r) is a nonsingular M-matrix, its inverse is entrywise nonnegative, and

    v(r)=(-G(r)^T)^(-1) 1

is strictly positive. For rational rates and theta=log 4, eta=log 2, all G entries and v entries are rational functions of r over the rationals. The multipliers are 8^delta on upward edges and 2^delta on downward edges.

## 3. Exact weighted quadratic form

Let P=diag(p(r)). For any real vector u, finite-mode stationarity gives

    u^T P G u
      = -1/2 sum_e F_e(u_k-u_j)^2
        + sum_e F_e(t_e-1)u_j u_k.                    (1)

This identity includes self-mode reactions. For a downward edge, with a_e=1-t_e in (0,1), its contribution is exactly

    -t_e F_e(u_k-u_j)^2/2
    -a_e F_e(u_j^2+u_k^2)/2.                        (2)

For an upward edge put b_e=t_e-1>0. Since u_j u_k=u_k^2+(u_j-u_k)u_k and Young's inequality bounds the last term,

    -F_e(u_k-u_j)^2/2 + b_e F_e u_j u_k
      <= -F_e(u_k-u_j)^2/4
         +(b_e+b_e^2)F_e u_k^2.                     (3)

Horizontal edges retain -F_e(u_k-u_j)^2/2. Choose one fixed positive constant

    c0=min{1/4, min_{down e} t_e/2}.

Define

    E_r(u)=c0 sum_e F_e(u_k-u_j)^2
           +sum_{down e}(1-t_e)F_e(u_j^2+u_k^2)/2.

Equations (1)-(3) give

    u^T P G u <= -E_r(u)
                  +sum_{up e}(b_e+b_e^2)F_e u_target(e)^2.   (4)

## 4. Absorb upward edges through their higher return paths

Fix an upward edge e whose source height is h and target height is >h. Choose a directed complex return path from its target to its source. Stop at the first path vertex of height <=h. Every source vertex on this stopped path has height >h, and its final edge f_* is downward. In particular all path source heights exceed h by at least 1, since heights are integers.

Let the path modes be i_0=target_mode(e),i_1,...,i_L, with f_* the edge from i_{L-1} to i_L. By telescoping and Cauchy-Schwarz,

    u_{i_0}^2 <= L [u_{i_{L-1}}^2
                    +sum_{ell=0}^{L-2}(u_{i_{ell+1}}-u_{i_ell})^2].  (5)

The statement is valid also for L=1 (the empty sum is zero). Repeated modes and self-mode reactions do not invalidate it.

For every path edge f, the flux asymptotics give

    F_e(r)/F_f(r) = O(1/r).

Thus (5), the retained Dirichlet weights, and the final downward sink imply a finite constant K_e and threshold R_e such that

    (b_e+b_e^2)F_e(r)u_target(e)^2 <= (K_e/r) E_r(u)

for all r>=R_e and all real u. There are only finitely many upward edges. For sufficiently large r their total contribution is at most E_r(u)/2. Therefore

    u^T P G u <= -E_r(u)/2 <0 for every nonzero real u.       (6)

The strict inequality follows because E_r(u)=0 forces u constant along the connected mode graph, while any downward sink forces that constant to be zero. All fluxes are strictly positive at the large r under consideration.

The symmetric part of P G is therefore negative definite. Applying the same real symmetric form to the real and imaginary parts of a complex eigenvector shows every eigenvalue of G has negative real part. This proves the theorem. Standard finite-dimensional Metzler theory then yields (-G)^(-1)>=0; alternatively use the convergent integral integral_0^infinity exp(tG)dt. Applying the transposed inverse to 1 gives strict positivity because exp(tG^T)1 has strictly positive entries for small t.

## 5. Effective finite constants, not a uniform complexity claim

For rational rates and the rational tilt above, F_e/F_f is a rational function whose leading exponent is <=-1 and whose leading coefficient is positive. A finite rational threshold and K can be obtained by clearing denominators and bounding all lower coefficients by a geometric one-step estimate (the same elementary coefficient-sum bound as in the sign theorem). Select one explicit return path for each upward reaction, compute the finite path lengths and sink/Dirichlet constants, then take the maximum of these thresholds and 2 sum_e K_e.

This is a finite construction. Expanding falling factorials and determinant/tree polynomials may be expensive in numerical exponents and encoded coefficient sizes. No dimension-uniform constant, polynomial bit complexity, small recurrence threshold, or rapid mixing rate is asserted.

## 6. Why this is stronger than the frozen mean sign

The result allows fixed theta and fixed eta>0 independent of r. The extra eta |delta| factor leaves downward edges attenuated and gives a strictly positive multiplicative slack on every nonhorizontal reaction. That slack can absorb the actual count-shift ratios of positive rational functions and their polynomial reaction rates. Horizontal reactions have zero shift exactly, so arbitrarily fast neutral cycles create no such error. The parent dual-measure construction uses precisely this distinction rather than a generic timescale-separation claim.
