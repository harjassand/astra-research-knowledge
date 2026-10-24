# Lipschitz symplectic cylinder exclusion in every even dimension

Status: FROZEN; root's full governing-source review passed on 2026-10-24 after the bounded continuation, shadow and fiber checks and a separate Sol proof review. This is an internally checked mathematical theorem, not external certification, a novelty determination, or an acquired physical control operation. All predecessor sources remain unchanged.

## 1. Exact statement and conventions

Use the standard Euclidean metric and the standard compatible symplectic form on

\[
\mathbb R^{2n}=\mathbb R^2\times\mathbb R^{2n-2},\qquad n\ge2.
\]

Let \(P\) be the orthogonal projection onto the first conjugate coordinate pair, and put

\[
B_R=\{x:|x|<R\},\qquad
Z_b=\{y:|Py|<b\},\qquad
\kappa_d=\frac{\pi^{d/2}}{\Gamma(d/2+1)}.
\]

Thus \(\kappa_d\) is the volume of the unit Euclidean \(d\)-ball. Radii, rather than symplectic capacities, label the balls and cylinders in this source.

**Theorem.** Suppose \(R>b>0\) and \(\phi:B_R\to\mathbb R^{2n}\) is a smooth symplectic embedding with forward Euclidean Lipschitz constant at most \(L\). For every \(r\in(b,R)\),

\[
\begin{split}
\operatorname{Vol}_{2n}\{x\in B_R:|P\phi(x)|\ge b\}
&=\operatorname{Vol}_{2n}\bigl(\phi(B_R)\setminus Z_b\bigr)\\
&\ge
\frac{\pi\kappa_{2n-2}(r^2-b^2)(R-r)^{2n-2}}
{L^{2n-2}}.
\end{split} \tag{1}
\]

In particular, choosing \(r=(R+b)/2\) gives

\[
\operatorname{Vol}_{2n}\bigl(\phi(B_R)\setminus Z_b\bigr)
\ge
\frac{\pi\kappa_{2n-2}}{2^{2n}}
\frac{(R-b)^{2n-1}(R+3b)}{L^{2n-2}}. \tag{2}
\]

Only the forward Lipschitz bound on the stated source ball is assumed. No extension of \(\phi\) to its boundary or to all of phase space, global inverse-Lipschitz estimate on its image, properness hypothesis, or Hamiltonian isotopy is required. A conjugate pair obtained by a unitary symplectic change of coordinates has the same statement.

## 2. Forward Lipschitz control gives an interior image ball

**Lemma.** Under the theorem's assumptions, every \(x_0\in B_R\) satisfies

\[
B\!\left(\phi(x_0),\frac{R-|x_0|}{L}\right)
\subset \phi(B_R). \tag{3}
\]

**Proof.** Let \(J\) be the standard orthogonal complex-structure matrix. At every source point, symplecticity of \(S=D\phi\) gives

\[
S^{\mathsf T}JS=J,\qquad
S^{-1}=-JS^{\mathsf T}J,\qquad
\|S^{-1}\|_2=\|S\|_2\le L. \tag{4}
\]

The last derivative bound follows from forward Lipschitzness. Fix a vector \(w\) with \(L|w|<R-|x_0|\). Lift the output segment \(\phi(x_0)+tw\) by solving

\[
\dot x(t)=D\phi(x(t))^{-1}w,\qquad x(0)=x_0. \tag{5}
\]

On every interval of existence with \(0\le t\le1\),

\[
|\dot x(t)|\le L|w|,\qquad
|x(t)|\le |x_0|+L|w|<R. \tag{6}
\]

Consequently the lift stays in a fixed compact subset of the open source ball. If a maximal interval ended at \(t_*\le1\), the speed bound would give a Cauchy limit \(x_*\) in that compact subset. The smooth vector field in (5), defined because \(D\phi\) is invertible there, would continue the solution past \(t_*\). Hence the lift exists through \(t=1\). The chain rule gives

\[
\frac{d}{dt}\phi(x(t))=w,
\]

so \(\phi(x(1))=\phi(x_0)+w\). This proves (3). In particular, for each \(x_0\in B_r\),

\[
B\!\left(\phi(x_0),\delta\right)\subset\phi(B_R),
\qquad \delta=\frac{R-r}{L}. \tag{7}
\]

This is a local inverse-continuation argument. It does not infer a global inverse-Lipschitz inequality by integrating along a segment that might leave the image. Instead, the compactly confined lift proves that the particular short segment cannot leave the image. \(\square\)

## 3. The standard two-dimensional shadow input

The area formulation of Gromov nonsqueezing states that every smooth symplectic embedding \(\psi:B_r^{2n}\to\mathbb R^{2n}\) obeys

\[
\operatorname{Area}\bigl(P\psi(B_r)\bigr)\ge\pi r^2. \tag{8}
\]

This exact nonlinear, all-dimensional statement is recorded in the introduction, Eq. (1), of [Abbondandolo–Matveyev, *How large is the shadow of a symplectic ball?*](https://arxiv.org/html/1202.3614v3), with its reduction to ordinary nonsqueezing in the following paragraph. It applies to the entire projected set even if that set is not convex. Their small-shadow results in higher projection dimension do not concern this two-dimensional input.

## 4. Fiber proof of the theorem

Set

\[
\Omega=\phi(B_R),\qquad
A=P\phi(B_r),\qquad
U=A\setminus\overline{B_b^2}.
\]

The image \(\Omega\) and its projection \(A\) are open. By (8),

\[
\operatorname{Area}(U)
\ge\operatorname{Area}(A)-\pi b^2
\ge\pi(r^2-b^2). \tag{9}
\]

For each fixed \(u\in U\), the definition of \(A\) supplies at least one point \((u,v)\in\phi(B_r)\). Equation (7) puts a \(2n\)-ball of radius \(\delta\) about this point inside \(\Omega\). Its section at the same base coordinate \(u\) is the \((2n-2)\)-ball \(B^{2n-2}(v,\delta)\). Therefore the full fiber

\[
\Omega_u=\{v':(u,v')\in\Omega\}
\]

satisfies

\[
\operatorname{Vol}_{2n-2}(\Omega_u)
\ge\kappa_{2n-2}\delta^{2n-2}. \tag{10}
\]

Every point in such a fiber lies outside \(Z_b\), because \(|u|>b\). Tonelli's theorem applied to the indicator of the open set \(\Omega\) now gives

\[
\begin{split}
\operatorname{Vol}_{2n}(\Omega\setminus Z_b)
&\ge\int_U\operatorname{Vol}_{2n-2}(\Omega_u)\,du\\
&\ge\pi(r^2-b^2)\kappa_{2n-2}
\left(\frac{R-r}{L}\right)^{2n-2}.
\end{split} \tag{11}
\]

There is no measurable-selection requirement: the existence of a witness point establishes (10) for each fiber, and the integrated fiber measure is measurable. There is also no sum of potentially overlapping projected disks. The integral runs over distinct base coordinates \(u\), with one lower bound for each entire fiber.

A symplectic embedding preserves Euclidean volume, so change of variables identifies the output volume in (11) with the source exit-set volume in (1). Open versus closed cylinder boundaries have zero \(2n\)-volume. This proves (1); direct substitution of \(r=(R+b)/2\) proves (2). \(\square\)

## 5. Exact prior boundary

For \(n=2\) and \(b=1\), (2) reads

\[
\operatorname{Vol}_4\bigl(\phi(B_R)\setminus Z_1\bigr)
\ge\frac{\pi^2(R-1)^3(R+3)}{16L^2}. \tag{12}
\]

The four-dimensional \(L^{-2}\) exclusion theorem is already [Sackel–Song–Varolgunes–Zhu, *Geometry & Topology* 28 (2024), Theorem 1.6](https://doi.org/10.2140/gt.2024.28.1113). Their Section 5 uses a waist argument. This source gives an explicit constant and a different short derivation after the standard shadow theorem; it does not claim the four-dimensional result or exponent is new.

In [the same paper, Section 6.6](https://arxiv.org/html/2105.00586v3#S6.SS6), the higher-dimensional obstruction with scale \(R^{2n}L^{-(2n-2)}\) is proposed as an expected extension, rather than proved there. Equation (2) establishes a lower bound with that scale at fixed cylinder radius and large \(R\). A bounded search did not identify a later directly matching primary theorem. That no-hit is not novelty clearance: priority of the all-dimensional statement and of this proof remains **UNKNOWN**.

The cited paper's four-dimensional constructive upper bound is of order \(L^{-1}\). No matching upper construction, sharp exponent, or mean-energy asymptotic follows from the present lower bound. The bound also does not settle the separate question of deleting a small set and embedding only its complement.

## 6. Mathematical and operational scope

The compatible Euclidean metric and canonical normalization are part of the contract. A non-isometric symplectic coordinate change changes the numerical Lipschitz bound. The cylinder uses the same conjugate-plane projection as the shadow theorem. The source is a ball, and the map is a smooth embedding on the whole ball.

This theorem is an endpoint geometric obstruction. A bound on an actual Hamiltonian flow's derivative can supply \(L\), but a physical force, field, power, bandwidth, or preparation budget does not automatically supply it. The separate bounded-control discussion is retained in [FINITE_EM_CONTROL_CONTRACT.md](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_boxcar/FINITE_EM_CONTROL_CONTRACT.md); its global-domain, fixed-metric and electromagnetic reachability qualifications remain separate from (1).

No actual energy-recovery protocol, fusion channel, actuator library, material implementation, useful physical performance, or mission achievement is inferred from this theorem.

## 7. Internal dependencies and review record

The proof uses the standard shadow input (8), elementary symplectic matrix algebra, smooth ODE continuation, Tonelli and volume preservation. It does not require a numerical fixture or solver.

Bounded readbacks:

- [Algebra/continuation and literal four-dimensional theorem check](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_resolvent_algebra/FORWARD_LIPSCHITZ_CONTINUATION_AUDIT.md).
- [Independent boundary-distance and distinct-fiber Fubini check](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_single_port/BOUNDARY_DISTANCE_LEMMA.md).
- [Primary theorem and final-publication/higher-dimensional boundary check](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_random_lag_sources/PRIMARY_QUANTITATIVE_NONSQUEEZING_CHECK.md).
- Root independently rederived the continuation and all-dimensional fiber argument, personally reopened the shadow primary and the final paper's Section 6.6, and relayed a separate independent Sol proof_audit adversarial pass. That check included nonproper images, possibly holey shadows, fiber measurability, cylinder boundaries and volume change. These are internal reviews, not external certification.

The present source is the governing statement. Earlier worker notes using a global inverse-Lipschitz assumption are superseded on that assumption by the explicit continuation lemma above; their historical bytes are retained.
