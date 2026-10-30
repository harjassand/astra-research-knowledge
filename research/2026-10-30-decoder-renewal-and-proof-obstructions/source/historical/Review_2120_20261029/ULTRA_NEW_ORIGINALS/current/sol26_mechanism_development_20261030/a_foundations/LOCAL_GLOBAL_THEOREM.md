# Local exact completion at every gradient can coexist with global failure

This is the central principle of this packet. For strictly rank-one-positive homogeneous quartics in two spatial dimensions, local exact-form completion is automatic. Nevertheless global completion is obstructed by a conserved, necessarily non-finitely-supported matrix measure. The obstruction is demonstrably real even for a quantitatively quasiconvex polyconvex energy and even after optimizing all constant linear second-order flows.

The assertions concern the angular heat mechanism, not all quasiconvexity proofs. Its ordinary ingredients are matrix Fejer--Riesz, quadratic null-Lagrangian minors, Cartan's homotopy formula, partition-of-unity gluing, and positive-cone functional separation. Their exact use and a universal finite-expression obstruction are proved in the three companion files.

## 1. Local cubic exact completion is automatic

Let `F` be a homogeneous quartic on `R^(m by 2)` with

`F''(A)[eta tensor xi,eta tensor xi]>=lambda |A|^2 |eta|^2 |xi|^2`, `lambda>0`.

Let `Q_F(theta,h)` be its ordinary-heat compatible-Hessian quadratic form on the gradient unit sphere. For EVERY direction `theta`, there is a homogeneous CUBIC polynomial 1-form `alpha_theta` and a neighborhood `U_theta` such that

`Q_F(A,h)+(d alpha_theta)_A(B1,B2)>=(lambda/4)|A|^2 |h|^2`                 (1)

whenever `A/|A|` lies in `U_theta`.

Proof: `POINTWISE_COMPLETION.md` gives a frozen 2-form `Omega` at `theta` with margin `lambda/2`. Write

`Omega=theta^flat wedge beta+gamma`, `beta=i_theta Omega`, `i_theta gamma=0`.

Regard `Omega_star=theta^flat wedge beta+2gamma` as a CONSTANT ambient 2-form. With `T=|A|^2` and `E=A dot partial_A`, set

`alpha_theta=(T/4)i_E Omega_star`.                         (2)

It is a homogeneous cubic polynomial 1-form. Since `d i_E Omega_star=2Omega_star`, at `A=theta` it satisfies

`d alpha_theta=(1/2)theta^flat wedge beta+(1/2)Omega_star=Omega`.

Continuity preserves half the original strict margin on a neighborhood, and homogeneity extends it along rays. The cubic is odd and its exterior derivative even, so the neighborhood can be made antipodally symmetric. This proves (1).

This is stronger than saying an arbitrary positive 2-form value exists at each point: every local value can be realized by an EXACT homogeneous cubic form, so the obstruction below cannot be diagnosed by any individual gradient direction, any frozen SDP, or local exactness alone.

There is also a converse. On a rank-one Hessian symbol all wedge corrections vanish and `|h|^2>=3|eta|^2|xi|^4/4`. A positive local compatible-Hessian margin therefore implies the Legendre--Hadamard condition at that gradient, with the corresponding `3/4` factor. For homogeneous quartics, compactness makes strict positivity at every nonzero gradient uniform. Thus strict rank-one positivity, strict pointwise completion, and local homogeneous cubic exact completion at every direction are EQUIVALENT local conditions. None is equivalent to the global closed-selection condition.

## 2. The exact gluing term cannot be dropped

By compactness select finitely many of these local forms and an even smooth angular partition of unity `chi_j`, with `supp chi_j` contained in their validity patches. The pointwise convex combination

`omega_mix=sum_j chi_j d alpha_j`

retains (1). But the actual differential of the glued primitive is

`d(sum_j chi_j alpha_j)=omega_mix+Psi`,

`Psi=sum_j d chi_j wedge alpha_j`.                         (3)

Here the weights are extended homogeneously with degree zero. The extra term has exactly the same coefficient homogeneity as `omega_mix`, and cannot be suppressed by radial rescaling. It restores closedness; it has no sign in the compatible-Hessian inequality. This is the literal missing operation when trying to turn many locally correct angular certificates into one global certificate.

The underlying sphere has no relevant nontrivial 2-form cohomology in these dimensions, and homogeneous closed forms already have the explicit Euler primitive. This obstruction is analytic positivity versus closedness, rather than a topological failure of exactness.

## 3. Exact dual obstruction and the impossibility of a finite atomic witness

Let `p(F)` be the optimal homogeneous completion margin for ordinary heat, as in `DUAL_CURRENT.md`. That proof gives

`p(F)=min_M pair(Q_F,M)`,                                  (4)

where `M` is a positive symmetric jet-matrix measure on the gradient sphere, of unit total trace, annihilating the correction from EVERY smooth homogeneous cubic-coefficient 1-form (the coefficients need not be polynomial). The feasible set is weak-star compact and nonempty.

For any such `M` supported on FINITELY MANY gradient directions,

`pair(Q_F,M)>=lambda/4>0`.                                 (5)

To prove this, first combine antipodal atoms: `Q_F` and all admitted exterior derivatives are even. At the remaining finite set of projective directions, choose disjoint angular neighborhoods. Formula (2) permits prescribing an arbitrary 2-form value at any selected direction. Multiply that local homogeneous primitive by an even angular cutoff equal to one near the selected direction and zero near every other support point. Its derivative has precisely the prescribed value at that atom pair and zero at all the others. The dual conservation constraint forces the matrix weight at each atom pair to annihilate EVERY wedge correction individually. Pair the pointwise positive completion of `POINTWISE_COMPLETION.md` with those positive weights and sum. This yields (5).

Thus if `p(F)<0`, no finitely supported exact dual can witness it, no matter how many Hessian jets are mixed at each of its finitely many gradient directions. This does NOT exclude a finite atomic dual in a FINITE-DEGREE relaxation, where only finitely many primitive constraints have been imposed. Nor does it assert that a general exact dual is atom-free. The distinction is between finite support with all differential constraints and a truly distributed exact conservation law.

## 4. A real energy with precisely this local/global obstruction

Take

`F(A)=(det A)^2+2^-100 |A|^4`.                             (6)

This energy is polyconvex and has the strong-QC margin `2^-100/3`. It has the rank-one positivity constant `lambda=4*2^-100`. Thus ALL its local cubic exact completions exist by Section 1.

Yet `LINEAR_FLOW_OBSTRUCTION.md` proves that for EVERY nonzero real constant second-order output/spatial coefficient triple `L`, one of twelve explicitly given periodic rank-one-image maps increases this SAME energy at a fixed rescaled short time. Its proof is universal over the full 12-dimensional coefficient space. Exact Fraction Fourier algebra checks the complete measurement map, rather than testing a finite set of flows. An actual trajectory then gives the dual measure (4) with negative pairing. For ordinary heat the strict margin is bounded above by `-2^-92`, by the normalization and finite-time bounds in `DUAL_CURRENT.md`.

Consequently a negative exact dual exists, every finitely supported exact dual is positive, and every local exact certificate exists. This makes the global differential constraint a genuine mathematical resource; it is not a missing degree in a polynomial search.

For ordinary heat the negative trajectory can even be written in closed form, without selecting a probe or taking a tiny-time Taylor expansion. Put `g=sin x+sin y`, `u(0)=(g,g^2/2)`. Then

`u1(t)=e^-t(sin x+sin y)`,

`u2(t)=1/2-(e^-4t/4)(cos 2x+cos 2y)+e^-2t sin x sin y`,

and

`det Du(t)=(e^-3t-e^-5t)cos x cos y(sin x-sin y)`.

Therefore `integral (det Du(t))^2=(e^-3t-e^-5t)^2/8`. At `t=(log 2)/2`, this is exactly `1/256`. At the initial time the determinant is identically zero and `|Du(0)|^4<=100`, so the SAME energy (6) increases by more than `1/512`. Its finite Fourier coefficients give `|A|<12`, `|h|<=32` throughout this interval, and hence `Z<2^17`. The resulting exact dual satisfies `pair(Q_F,M)<-2^-26`. This explicitly exhibits the geometrical mechanism: componentwise heat takes a map into a parabola and creates two-dimensional Jacobian energy.

For any local cover and partition as in Section 2, take a negative dual `M`. Since the total glued differential in (3) is annihilated,

`pair(Psi,M)=-pair(omega_mix,M)<=pair(Q_F,M)-lambda/4<0`.

In particular

`||Psi||_(sup,op)>=lambda/4-pair(Q_F,M)`                    (7)

for the induced compatible-Hessian matrix of `Psi`. Thus local gluing has a quantitatively unavoidable negative contribution. A construction which keeps only the convexly mixed pointwise completions but drops the derivatives of its angular weights cannot be repaired by making the local atlas finer.

## 5. Consequence for a larger discovery operation

The sol25 hierarchy acquires a finite rational certificate when a uniformly coercive smooth global witness, with quantitative regularity, is already available. The present theorem locates the earlier scientific gate: all local exact witnesses are already supplied by strict rank-one positivity, but their global sign-preserving integration may fail, and no finite atomic exact dual captures that failure.

The accepted original non-polyconvex quartic lies in the angular heat class. Energy (6) lies in the polyconvex class and outside every constant-second-order heat class. Thus even the strongest constant linear-flow version of this operation must be combined with a genuinely different argument, such as the already-established polyconvex one. This is consistent with the explicit polyconvex `det^2` summand kept outside the heat correction in Bruno--Pasqualotto Appendix A. Ordinary methods are granted that decomposition; the no-go energy is not a new difficult quasiconvex example.

What has been obtained is an exact local/global and primal/dual description of a nontrivial proof operation, plus a universal structural obstruction to enlarging it by constant diffusion design alone. It does not settle rank-one convexity versus quasiconvexity, give a complete QC hierarchy, or rule out nonlinear, nonlocal, enlarged-state, or mixed proof operations. Historical priority of this combined theorem is UNKNOWN. Its value is explanatory and constructive at this operation's exact mathematical scope, with no proposed practical-materials threshold or computational advantage.
