# Independent shifted-barrier well-current acceptance

**PASS, theorem-only**, bound to `SHIFTED_BARRIER_WELL_CURRENT_ROOT.md`, SHA-256 `3449b040c75840c4b56f699b81b8f4455bb8701a8d3c110d8d56c67ccb5c28dc`. The source was read fully, snapshotted and left unchanged. Its accepted well-current dependency `207d9ee3...` and global reflection dependency `4a8110be...` were rehashed exactly.

This is a later separate acceptance. The earlier coarea review's statement that the shifted current was still open remains a correct historical status in its unchanged receipt; this addendum now closes that mathematical construction. It does not accept the complete new numerical primal/dual receiver or a finite precision improvement.

## 1. The reconstructed current is actually admissible

Use the original factorized quartic potential, the same common Gibbs scale and constant block mobility diag(1,M_z), M_z>=mu I. The parameter a0 is an auxiliary current-density parameter, not a change in the physical barrier, potential or mobility. Its required range is v_b<=a0<=v_*.

The homotopy/conditional j_z branches in the source apply in A; in S the separately specified j_z=0 controls. In the constant-density well segment, the identity div_z F_v=pi_v-pi_a0 cancels the excess source from partial_y(J pi_a0), giving rho1_A. In the conditional segment the usual homogeneous dilation identity gives the same source. The slab has J=M and fixed pi_a0, hence zero divergence there.

At v=a0 both definitions of the longitudinal density coincide. At y=-b, v_b<=a0 ensures the A-side density parameter equals a0, matching the slab. Thus the normal flux is continuous, and transverse jumps at constant-y interfaces create no delta divergence. At endpoint equality a0=v_b, pointwise choices of the transverse branch exactly on the interface are measure-zero choices and do not change source, norm or matching normal traces.

The slab price is exactly beta M² R_a. Throughout S,

    2a0-v(y)>=2v_b-v_*=1+kappa/8>0.

Thus every squared-density integral is finite. The identity a0²/(2a0-v)-v=(a0-v)²/(2a0-v)>=0 also shows R_a>=R, even where v>a0 in the slab. No monotonic-in-a estimate is incorrectly applied to that latter region; the slab is integrated exactly.

## 2. The changed threshold and all four cost regions

On the outer side of the well, v(x_a)=a0 gives

    x_a=sqrt(1+sqrt((a0-1)/kappa)).

Since (a0-1)/kappa lies in [9/16,1],

    sqrt(7/4)<=x_a<=sqrt(2),
    x_a>5/4>=1+delta, delta=1/alpha<=1/4.

The first lower endpoint is sqrt(7/4), not sqrt(7)/4. The inner well root is at most b, so the entire A-side constant-density segment is exactly b<x<x_a, up to endpoints.

### Homotopy transverse price

The support length x_a-b is below one. In its integral v<=s<=a0<=v_*, both endpoint-length factors are at most kappa and s²sqrt(2s-v)>=1. The same monotonicity of s²/(2s-v), followed by the decreasing-in-v bound v_*²/[v²(2v_*-v)]<=G1, gives the old K kappa² G1^alpha ceiling. This uses the actual inverse-mobility moment bound; no new fiber equation or hidden price is assumed.

### Near-well longitudinal price

For x in [b,1+delta], v(x)<=v_b<=a0. The exact density price a²/(2a-v) increases with a for a>=v, since its derivative is 2a(a-v)/(2a-v)²>=0. Therefore the changed price is at most the old v_* price, which in turn is at most Gb because v<=v_b. With J<=M and the same interval length, the old M²(1+delta-b)Gb^alpha term remains valid.

### Remaining constant-density interval

For x in [1+delta,x_a], the length is below one half and v<=a0. Convexity gives J(-x)<=v^(1-alpha)/[(alpha-1)v']; v'>=8kappa delta. After squaring J, the longitudinal integrand contains

    v² [a0²/(v²(2a0-v))]^alpha /[(alpha-1)²v'²].

Monotonicity in a0<=v_* bounds the bracket by G1; v²<=v_*². The interval-length factor therefore produces exactly the old denominator 128. No part of this changed segment is dropped.

### Conditional far tail, including the new band

For x>=x_a, the new current is conditional dilation. The old pointwise far-tail estimate uses only x>1, v>=1, alpha>=4, the cumulative convexity estimate and the globally valid Dmax. It does **not** need v>=v_* or x>=sqrt(2). Hence it remains valid on the newly conditional band [x_a,sqrt(2)] as well as farther out:

    resistance density <=(1+Dmax)/[64kappa²(alpha-1)²(x-1)²].

Since x_a>5/4, extension of its integral down to 5/4 is conservative. The reciprocal-square integral is exactly 4, retaining the denominator 16. This extension may overlap a previously bounded region; that is safe overcounting, not a missing-band argument.

These four bounds cover the complete non-slab current and give the identical E_rest ceiling. The proof therefore establishes the new killed source-A bound

    Q_A^killed <=beta[M²R_a+E_rest].

Here Q_A remains the *killed* inverse form; a global inverse of the nonzero-mean source 1_A is not asserted.

## 3. Global odd reflection and infinity

Restrict this new current to y<0 and reflect by J_ref=-R0 J(R0x), with R0=diag(-1,I). Its normal flux at zero is M pi_a0 and matches. Reflection reverses the source on the right and preserves the inverse-block-mobility norm. Thus the global signed source f=1_A-1_B has the explicit price

    Q_f^global <=beta[M²R_a+2E_rest].

The slab is counted once and wells twice. Complete finite far-tail resistance and compact-core duality extend to the actual closed form. Positive resolvent tests and monotone limits earn finite inverse forms before a gap or zero-inverse operator is used. The global signed source has zero mean, and the previous actual-process/nonexplosion/form assumptions are unchanged. There is no pointwise infinity-flux shortcut.

## 4. Optimized parameter is conditionally admitted, not automatically

For a_opt=v_*(1-1/(2alpha)), its upper bound a_opt<=v_* is automatic. Its lower bound a_opt>=v_b is exactly

    alpha>=8v_*/(7kappa).

This is in addition to alpha>=4, must be checked on the literal model, and is not automatic for small kappa. Merely checking 2a_opt>v_* would not have proved well/slab normal-flux matching for the current in this source. The stated stronger admission is correct, including equality.

## 5. Joining boundary and checks

The shifted source current is now mathematically explicit and fully priced. Combined with the separately accepted energy-sensitive odd-slab source, there is no longer a missing source-flow oracle at this boundary. The full energy-sensitive primal price still requires its actual scalar integral and derivative evaluations, and any new reference-rate/defect/path error must be derived and received consistently. Formal first-order cancellation and actual finite-dimensional numerical accuracy remain unaccepted.

The shifted current proof itself permits arbitrary finite constant SPD transverse mobility with an acquired floor, as the old inverse-mobility bound did. The separate refined pair-quartic derivative shortcut remains diagonal-only; joining the two does not erase that restriction. Neither construction changes the actual dynamics.

`check_shifted.py` passed **1,674 exact assertions**: density monotonicity, positive slab denominator, threshold inequalities, near/middle/far ceilings, exact 16 constant, optimized-parameter equivalence, rational parameter fixtures and all three frozen-source bindings. These supplement the global proof, not replace it. No candidate executable was imported. Source snapshots and new artifacts are bound in `AUDIT_SHA256.json`; all originals and prior receipts remain unchanged.
