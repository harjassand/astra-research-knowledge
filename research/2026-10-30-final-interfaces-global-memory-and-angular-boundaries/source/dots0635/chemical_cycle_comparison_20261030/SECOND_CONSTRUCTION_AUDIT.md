# Independent child audit: artificial-volume pump and local face repair

2026-10-30. Internal review; not external novelty certification. Reviewed ARTIFICIAL_VOLUME_PUMP.md and COMPOSITION_TRACKING_FACE_REPAIR.md.

## Verdict

The artificial-volume pump is valid and materially stronger than the generic snake. The arbitrary-dimensional radial local dual is also valid, including a sufficiently small neighborhood of its normal after making the exponent-margin argument explicit. Neither proves recurrence. One definite wording defect concerns the first, factorial-envelope composition example: immigration is NOT lower-order in its adjoint. The omission must be described as an algebraic demonstration only, not an asymptotic neglect.

## 1. Exact mass-action artificial-volume pump: pass

For one coordinate the full actual rates are

    lambda_n=R(n)_10+(n)_20,
    delta_n=(n)_11+R(n)_21.

Using (n+1)_(k+1)=(n+1)(n)_k gives the exact ratio

    lambda_n/delta_(n+1)
      =[R(n)_10+(n)_20]/[(n+1)((n)_10+R(n)_20)].

For n≥10 this lies between 1/[R(n+1)] and R/(n+1), and approaches the lower endpoint asymptotically. Thus the unbounded one-coordinate class has a summable factorial stationary law; polynomial rates make its stationary rate integral finite. The full two-coordinate process is their independent product, with the separate absorbing low-coordinate classes handled independently.

On an increasing path edge the lower channel multiplies reference forward flux by R and reverse flux by 1; on a decreasing edge the higher channel does precisely the same relative to the path orientation. Each retained layer is a complete pair of states z+y,z+y', with reference conductance exactly 1/z!, and different path edges do not accidentally create additional state edges. Therefore detailed balance on the retained path gives pi_i/pi_0=R^i mu0(x_i)/mu0(x_0) exactly.

A translated square-shell snake with minimum coordinate 21 and side n has length Theta(n²), all coordinate sums O(n), and is a legitimate finite union of complete reversible layers of the same fixed graph. Its relative density ratio is exp[Theta(n²)], not merely an upper bound exp[O(n²)]. This defeats any truncation-uniform exp[C(|x|+|x_0|)] density-ratio bound for arbitrary such layer selections. The retained process is not itself an unrestricted mass-action model on its finite state set: it is a layer-selected truncation of one. The manuscript makes this distinction correctly. Canonical geometrically complete cutoffs remain untested by this counterexample.

## 2. Composition-tracking pair cancellation: algebra passes, immigration caveat required

Substitution rho=r into both displayed D expressions gives exactly -1-r. For

    F=B(log B−1−(2/3)log A),

its gradient is (-2B/(3A), log B−(2/3)log A), so c_A^2/c_B^3=r exp[-4B/(3A)]→r on the stated rays. The local Hessian tends to zero there, so fixed-shift gradient approximation is justified for fixed positive prefactors.

However, with the implied factorial envelope exp(F)/(A!B!C!), immigration 0→y_i contributes c^(−y_i)(x)_(y_i) to the leading adjoint coefficient. As the local fugacities have finite nonzero limits on these fixed-prefactor rays, this has the SAME exposed monomial order as the displayed terms. It cannot be dropped on the grounds that its source complex is zero. Replace “Ignoring the strictly lower 0-complex inputs” by “Algebraically omitting immigration contributions, which need not be lower-order for this envelope.” The later disclaimer about immigration is correct but does not rescue the earlier lower-order wording. This issue does NOT affect the subsequent nonfactorial radial construction.

## 3. Radial local dual: pass, with explicit uniform margins

Let nu=y'−y, delta=w·nu, N=w·x, m=min_i w_i>0, and h=max_y w·y. For bounded reaction shifts,

    mu_w(x−nu)/mu_w(x)
      =exp(alpha delta) N^(alpha delta)(1+O(1/N)).

On x_i~c_i t^(w_i), N~Ct because max w_i=1. Falling factorials give lambda_y(x−nu)~kappa c^y t^(w·y). This yields the stated incoming exponent w·y+alpha delta.

When delta=0, the radial weight ratio is EXACTLY one. The reaction's incoming-minus-outgoing term is lambda_y(x−nu)−lambda_y(x)=O(t^(w·y−m)); this is a polynomial finite-difference estimate, not a stationary-balance assumption. Every proper top-face exit has negative delta and supplies a negative term of order t^h. Its incoming exponent is strictly smaller. Every below-face source has incoming exponent (1−alpha)w·y+alpha w·y'<h. A fixed face exit exists by strong connectivity. Finitely many reactions supply a strictly positive exponent gap and a uniformly positive exit coefficient for prefactors in a fixed compact positive set. Thus the exact adjoint is negative eventually.

For the neighboring-cone claim, normalize neighboring directions v by max v_i=1 and keep the SAME function mu_w. The incoming exponents become

    v·y+alpha w·nu,

NOT (1−alpha)v·y+alpha v·y'. The internal finite-difference exponents are at most v·y−min_i v_i. Choose one fixed top-face exit source y*. At v=w every possible positive term is separated below w·y*=h by a positive margin. Continuity of these finitely many exponent differences retains the margin for v sufficiently close to w. Also N/t stays uniformly bounded above and below for positive compact prefactors and max v_i=1. This proves uniform local-sector negativity without silently changing the radial function with the direction. The exposed face may change as v varies; sufficiently small perturbations still work by this margin proof.

The measure is positive after defining its harmless value at N=0, and summable with every exponential moment since N≥m|x|. Polynomial mass-action total rates are integrable against it. But its adjoint sign is only local, so this does not supply a global dual measure. The stated minimum-selector and bounded-coordinate assembly blockers remain real.
